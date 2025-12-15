# 🎯 Stripe 梯度定价修复 - 关键 Bug

## 🎉 你发现了一个非常重要的Bug！

**发现时间：** 2025-12-15  
**发现人：** User  
**部署状态：** ✅ 已修复并部署

---

## 🐛 Bug 描述

### 问题现象

取消订阅后，即使有超额使用（如 -1 Credits），Stripe 也不收费（HK$0）。

### 用户的关键发现

用户注意到 Stripe 定价配置（图7）：

```
VaultCaddy Monthly - 梯度定价：
├─ 0-100个：HK$0.00
└─ 101-∞个：HK$0.50/个
```

**用户的问题：**
> "Stripe 是否知道月费中的 -1 就是第 101 个？年费中的 -1 是第 1201 个？"

**答案：不知道！因为我们的代码有 Bug！**

---

## 🔍 根本原因分析

### Stripe 梯度定价的工作原理

Stripe 的梯度定价（Tiered Pricing）是基于**总使用量**的，不是基于超额量！

#### 梯度定价配置：

```
第 1 档：0-100个    → HK$0.00/个（免费，包含在订阅中）
第 2 档：101个以上  → HK$0.50/个（超出部分收费）
```

#### Stripe 如何计算费用：

```javascript
// Stripe 内部计算逻辑（伪代码）
function calculateCharge(totalUsage) {
    if (totalUsage <= 100) {
        return 0;  // 全部在免费区间
    } else {
        const overageTier = totalUsage - 100;
        return overageTier * 0.5;  // 超出部分收费
    }
}

// 示例
calculateCharge(1);    // = 0（1 < 100）
calculateCharge(100);  // = 0（100 <= 100）
calculateCharge(101);  // = 0.5（(101-100) * 0.5）
calculateCharge(110);  // = 5.0（(110-100) * 0.5）
```

### 我们代码的 Bug

#### ❌ 错误的代码（修复前）：

```javascript
// 月费用户：包含 100 个 Credits
// 实际使用：101 个（超额 1 个，Credits = -1）

const overageAmount = Math.abs(currentCredits);  // 1 个

await stripe.subscriptionItems.createUsageRecord(meteredItemId, {
    quantity: overageAmount  // ← 报告 1 个
});

// Stripe 收到：totalUsage = 1
// Stripe 计算：1 < 100，费用 = HK$0 ❌
```

#### ✅ 正确的代码（修复后）：

```javascript
// 月费用户：包含 100 个 Credits
// 实际使用：101 个（超额 1 个，Credits = -1）

const monthlyCredits = 100;  // 订阅包含的 Credits
const overageAmount = Math.abs(currentCredits);  // 1 个
const totalUsage = monthlyCredits + overageAmount;  // 101 个

await stripe.subscriptionItems.createUsageRecord(meteredItemId, {
    quantity: totalUsage,  // ← 报告 101 个
    action: 'set'  // ← 设置总量，而不是增量
});

// Stripe 收到：totalUsage = 101
// Stripe 计算：101 > 100，超出 1 个，费用 = HK$0.50 ✅
```

---

## 📊 修复对比

### 月费用户（包含 100 Credits）

| 使用情况 | 超额量 | 旧代码报告 | Stripe 收费（旧） | 新代码报告 | Stripe 收费（新） |
|---------|-------|----------|----------------|----------|----------------|
| 使用 100 | 0 | 不报告 | HK$0 ✅ | 不报告 | HK$0 ✅ |
| 使用 101 | 1 | 报告 1 | HK$0 ❌ | 报告 101 | HK$0.50 ✅ |
| 使用 110 | 10 | 报告 10 | HK$0 ❌ | 报告 110 | HK$5.00 ✅ |
| 使用 200 | 100 | 报告 100 | HK$0 ❌ | 报告 200 | HK$50.00 ✅ |

### 年费用户（包含 1200 Credits）

| 使用情况 | 超额量 | 旧代码报告 | Stripe 收费（旧） | 新代码报告 | Stripe 收费（新） |
|---------|-------|----------|----------------|----------|----------------|
| 使用 1200 | 0 | 不报告 | HK$0 ✅ | 不报告 | HK$0 ✅ |
| 使用 1201 | 1 | 报告 1 | HK$0 ❌ | 报告 1201 | HK$0.50 ✅ |
| 使用 1210 | 10 | 报告 10 | HK$0 ❌ | 报告 1210 | HK$5.00 ✅ |
| 使用 1300 | 100 | 报告 100 | HK$0 ❌ | 报告 1300 | HK$50.00 ✅ |

**关键发现：**
- ❌ 旧代码：无论超额多少，Stripe 都收费 HK$0（因为报告的数量 < 100）
- ✅ 新代码：正确计算超出 100/1200 的部分，按 HK$0.50/个收费

---

## 🔧 修复详情

### 修复的函数

#### 1. handleSubscriptionCancelled（取消订阅时报告）

```javascript
// 获取用户订阅信息
const monthlyCredits = userData?.subscription?.monthlyCredits || 100;  // 包含的 Credits
const overageAmount = Math.abs(currentCredits);  // 超额量
const totalUsage = monthlyCredits + overageAmount;  // 总使用量

console.log(`📡 向 Stripe 報告總使用量...`);
console.log(`   - 包含的 Credits: ${monthlyCredits}`);
console.log(`   - 超額數量: ${overageAmount}`);
console.log(`   - 總使用量: ${totalUsage}（這是 Stripe 計費的基礎）`);

// 报告总使用量
const usageRecord = await stripeClient.subscriptionItems.createUsageRecord(
    meteredItemId,
    {
        quantity: totalUsage,  // ← 总使用量，不是超额量
        timestamp: Math.floor(Date.now() / 1000),
        action: 'set'  // ← 设置总量
    }
);

console.log(`💵 Stripe 會根據梯度定價計算費用:`);
console.log(`   - 前 ${monthlyCredits} 個 Credits: HK$0（已包含在訂閱中）`);
console.log(`   - 第 ${monthlyCredits + 1} 到 ${totalUsage} 個: HK$0.50/個`);
console.log(`   - 預期收費: HK$${(overageAmount * 0.5).toFixed(2)}`);
```

#### 2. manualReportOverage（手动报告工具）

同样的逻辑，确保诊断工具也能正确报告总使用量。

---

## 🧪 测试步骤

### 完整测试流程

#### 步骤 1：准备测试环境

```bash
1. 确保已重新订阅 Pro Plan（选择 A 已完成）✅
2. 使用诊断工具验证：canReportUsage: true ✅
```

#### 步骤 2：清零 Credits

```bash
Firebase Console → Firestore → users → 3bLhZuU9HOb3ExhwFCJuN4vZeGb2

修改字段：
- credits: 100 → 0
- currentCredits: 100 → 0
```

#### 步骤 3：使用服务（制造超额）

```bash
1. 打开 https://vaultcaddy.com
2. 上传并处理 1 个文档
3. 验证 Credits 变成 -1 ✅
```

#### 步骤 4：取消订阅

```bash
方法 1：https://vaultcaddy.com/account.html → 管理订阅 → 取消订阅
方法 2：Stripe Dashboard → Actions → Cancel immediately
```

#### 步骤 5：查看 Firebase 日志（关键！）

```bash
Firebase Console → Functions → 日志

搜索：「1234@gmail.com」或「向 Stripe 報告總使用量」

预期日志：
✅ "💰 檢測到超額使用: -1 Credits"
✅ "📊 超額數量: 1 Credits"
✅ "📡 向 Stripe 報告總使用量..."
✅ "   - 包含的 Credits: 100"
✅ "   - 超額數量: 1"
✅ "   - 總使用量: 101"  ← 关键！应该是 101，不是 1
✅ "✅ 總使用量已報告給 Stripe: mbur_xxxxx"
✅ "💵 預期收費: HK$0.50"
```

#### 步骤 6：验证 Stripe 使用记录

```bash
Stripe Dashboard → Subscriptions → 订阅详情

找到「Usage-based items」部分：
- 应该显示：101 units（不是 1 unit！）✅
```

#### 步骤 7：生成发票并验证

```bash
Stripe Dashboard → Customers → 1234@gmail.com

点击「Create invoice」：
- 应该自动包含 101 units 的使用
- 计算：
  - 前 100 个：HK$0（免费）
  - 第 101 个：HK$0.50
- 发票总额：HK$0.50 ✅
```

---

## 📋 验证清单

### 修复前（Bug 存在）

- [x] 取消订阅时报告 1 个超额使用
- [x] Stripe 收到：totalUsage = 1
- [x] Stripe 计算：1 < 100，费用 = HK$0 ❌
- [x] 用户白嫖超额使用 ❌

### 修复后（Bug 已修复）

- [ ] 取消订阅时报告 101 个总使用量
- [ ] Stripe 收到：totalUsage = 101
- [ ] Stripe 计算：101 > 100，超出 1 个，费用 = HK$0.50 ✅
- [ ] 用户正确被收取超额费用 ✅
- [ ] Firebase 日志显示正确的总使用量
- [ ] Stripe Usage records 显示 101 units
- [ ] Stripe 发票金额为 HK$0.50

---

## 💡 为什么会有这个 Bug？

### 理解误区

**错误的理解：**
> "Stripe 知道用户订阅包含 100 个 Credits，所以我只需要报告超额的 1 个，Stripe 会自动计算第 101 个。"

**正确的理解：**
> "Stripe 的梯度定价是基于总使用量的。我需要报告总使用量（100 + 1 = 101），Stripe 才能根据梯度配置（0-100: 免费，101+: 收费）正确计算费用。"

### 类比

**错误做法（旧代码）：**
```
酒店住房：
- 前 3 晚免费（包含在套餐中）
- 第 4 晚开始收费 $100/晚

客人住了 5 晚，我们告诉酒店："客人超额住了 2 晚"
酒店：2 晚 < 3 晚，免费！❌

结果：客人白住了 2 晚 ❌
```

**正确做法（新代码）：**
```
酒店住房：
- 前 3 晚免费（包含在套餐中）
- 第 4 晚开始收费 $100/晚

客人住了 5 晚，我们告诉酒店："客人一共住了 5 晚"
酒店：5 晚 > 3 晚，超出 2 晚，收费 $200！✅

结果：客人正确被收费 ✅
```

---

## 🎯 关键要点

### ✅ 正确的做法

1. **获取订阅包含的 Credits**：
   - 月费：100 个
   - 年费：1200 个

2. **计算总使用量**：
   - 总使用量 = 包含的 Credits + 超额量
   - 例如：100 + 1 = 101

3. **向 Stripe 报告总使用量**：
   - `quantity: totalUsage`（101）
   - `action: 'set'`（设置总量）

4. **Stripe 根据梯度定价自动计算**：
   - 前 100 个：HK$0（免费）
   - 第 101 个：HK$0.50
   - 总费用：HK$0.50 ✅

### ❌ 错误的做法

1. **只报告超额量**：
   - `quantity: overageAmount`（1）

2. **Stripe 误认为总使用量只有 1 个**：
   - 1 < 100，全部免费 ❌

---

## 📁 已修改的文件

- ✅ `firebase-functions/index.js` - 修复梯度定价计算
- ✅ `🎯_Stripe梯度定价修复_关键Bug.md` - 本文档

---

## 🚀 下一步

1. ✅ **执行完整测试**：按照上述测试步骤验证修复
2. ✅ **验证 Firebase 日志**：确认报告的是总使用量（101），不是超额量（1）
3. ✅ **验证 Stripe 使用记录**：确认显示 101 units
4. ✅ **验证发票金额**：确认为 HK$0.50

---

**你的发现非常重要！这个 Bug 可能导致所有超额使用都无法收费！** 🎉

现在修复已部署，请按照测试步骤验证，然后告诉我结果！🚀

