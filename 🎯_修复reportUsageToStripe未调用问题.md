# 🎯 修复 reportUsageToStripe 未调用问题

## 🐛 问题诊断

### 症状
- ✅ `deductCreditsClient` 成功执行（返回 200）
- ✅ Credits 成功扣除（-54 → -55）
- ❌ 搜索 `reportUsageToStripe` → **0 事结果**（找不到日志）
- ❌ Stripe Billing Meter → **没有任何数据**

### 根本原因

`deductCredits` 函数的旧逻辑：
```javascript
// 只有 Pro Plan 且 Credits 为负时才标记
if (isProPlan && newCredits < 0) {
    transaction.update(userRef, {
        'usageTracking.pendingOverageReport': admin.firestore.FieldValue.increment(overageCredits),
    });
}

// 事务后检查
if (pendingOverage > 0) {
    await reportUsageToStripe(userId, pendingOverage);
}
```

**问题**：
1. `isProPlan` 需要 `planType === 'Pro Plan'` **且** `subscription.status === 'active'`
2. 用户的订阅可能是**已取消状态**（`status === 'canceled'`）
3. 所以 `isProPlan = false`
4. 所以不会设置 `pendingOverageReport`
5. 所以 `reportUsageToStripe` **永远不会被调用**！

---

## ✅ 解决方案

### 设计理念

根据 **Stripe Billing Meters** 的设计：
- ✅ **实时报告每次使用量**（不管是否超额）
- ✅ 由 Stripe 自动累计和计算收费
- ✅ 不需要在后端判断是否超额

### 新逻辑

```javascript
// 🔥 事务完成后，无条件报告使用量给 Stripe Billing Meter
const userDoc = await userRef.get();
const userData = userDoc.data();
const hasSubscription = userData?.subscription?.stripeSubscriptionId;
const isTestMode = userData?.isTestMode || false;

// 只有有订阅记录或测试模式的用户才报告使用量
if (hasSubscription || isTestMode) {
    console.log(`📡 向 Stripe Billing Meter 报告使用量: ${amount} Credits`);
    
    try {
        await reportUsageToStripe(userId, amount);
        console.log(`✅ 使用量已报告给 Stripe Billing Meter`);
    } catch (error) {
        console.error(`❌ 报告使用量失败:`, error);
        // 不抛出错误，确保 Credits 扣除不受影响
    }
} else {
    console.log(`⚠️ 用户无订阅记录，跳过 Stripe 报告`);
}
```

---

## 🔄 关键改进

### 修改前
- ❌ 只在 `isProPlan && newCredits < 0` 时才报告
- ❌ 需要 `subscription.status === 'active'`
- ❌ 报告的是累积的超额数量
- ❌ 已取消订阅的用户无法报告使用量

### 修改后
- ✅ **无条件报告每次使用量**（只要有订阅记录）
- ✅ **支持已取消的订阅**（只要有 `stripeSubscriptionId`）
- ✅ **报告的是本次扣除的数量**（`amount`）
- ✅ **符合 Stripe Billing Meters 的设计理念**
- ✅ **简化了逻辑，减少出错机会**

---

## 📊 预期行为

### 报告条件（任一满足）
1. ✅ 有 Stripe 订阅记录（包括已取消的订阅）
2. ✅ 测试模式（`isTestMode: true`）

### 不报告的情况
- ❌ Free Plan 用户（无订阅记录）

### 报告内容
- **Event Name**: `vaultcaddy_credit_usage`
- **Quantity**: 本次扣除的 Credits 数量（如 1 页 = 1 credit）
- **Customer**: Stripe Customer ID
- **Timestamp**: 当前时间

---

## 🚀 已部署

```bash
✔  functions[deductCreditsClient(us-central1)] Successful update operation.
```

---

## 🧪 现在请重新测试

### 步骤1：刷新页面
- 按 **Cmd + Shift + R**

### 步骤2：上传 1 个新文档
- 任何 PDF 或图片都可以

### 步骤3：查看浏览器控制台（F12）
- 应该看到：
  ```
  ✅ Credits 已通過後端扣除: 1 頁
  ```

### 步骤4：查看 Firebase Logs
- 搜索：**`reportUsageToStripe`**
- **这次应该能找到日志了！** 🎉
- 预期看到：
  ```
  📡 向 Stripe Billing Meter 报告使用量: 1 Credits
  📡 reportUsageToStripe: userId=..., quantity=1
  ✅ 使用量已报告给 Stripe Billing Meter
  ```

### 步骤5：查看 Stripe Meter
- 等待 1-2 分钟（Stripe 处理延迟）
- 应该看到新的 Meter Event！
- Event Name: `vaultcaddy_credit_usage`
- Value: `1`

---

## 🎯 时间线总结

### 问题演变
1. ❌ 使用旧的 Usage Records API（已弃用）
2. ✅ 迁移到新的 Billing Meters API
3. ❌ 客户端直接操作 Firestore（绕过后端）
4. ✅ 修复为调用后端 Cloud Function
5. ❌ Firebase 初始化时序问题
6. ✅ 修复 Firebase `firebase-ready` 事件
7. ❌ Credits 不足检查拦截
8. ✅ 允许有订阅记录的用户超额使用
9. ❌ `reportUsageToStripe` 未被调用（本次修复）
10. ✅ **无条件报告使用量给 Billing Meter**

---

## 📝 修改的文件

- ✅ `firebase-functions/index.js`（`deductCredits` 函数，第1138-1163行）

---

## 🎉 下一步

测试成功后：
1. ✅ 确认 Stripe Meter 数据正常
2. ✅ 清理旧代码和文档
3. ✅ 完成迁移到 Billing Meters API


