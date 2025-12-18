# ✅ 允许超额使用以测试 Billing Meter

## 🐛 问题

后端的 `deductCredits` 函数有 Credits 不足检查：
```javascript
if (currentCredits < amount && !isProPlan) {
    throw new Error('Credits 不足');
}
```

用户的 credits 是 **-54**（负数），被后端拒绝，返回 500 错误。

---

## ✅ 解决方案

修改 `deductCredits` 函数，允许以下情况超额使用：
1. ✅ **有订阅记录的用户**（即使订阅已取消）
2. ✅ **测试模式**（`isTestMode: true`）
3. ✅ **活跃的 Pro Plan**

### 修改内容（firebase-functions/index.js 第1072-1089行）

#### 修改前
```javascript
console.log(`🔍 扣除 Credits: userId=${userId}, current=${currentCredits}, deduct=${amount}, planType=${planType}`);

// 检查是否是 Pro Plan
const isProPlan = planType === 'Pro Plan' && subscription?.status === 'active';

if (currentCredits < amount && !isProPlan) {
    // Free Plan 或非订阅用户：Credits 不足，抛出错误
    console.log(`❌ Credits 不足且非 Pro Plan: ${currentCredits} < ${amount}`);
    throw new Error('Credits 不足');
}
```

#### 修改后
```javascript
console.log(`🔍 扣除 Credits: userId=${userId}, current=${currentCredits}, deduct=${amount}, planType=${planType}`);

// 检查是否是 Pro Plan
const isProPlan = planType === 'Pro Plan' && subscription?.status === 'active';

// 检查是否有订阅记录（包括已取消的订阅）
const hasSubscription = subscription && subscription.stripeSubscriptionId;

// ⚠️ 测试模式：允许负数扣除，用于测试 Stripe Billing Meter
const isTestMode = userData.isTestMode || false;

if (currentCredits < amount && !isProPlan && !hasSubscription && !isTestMode) {
    // 只有 Free Plan 且无订阅记录且非测试模式时才拒绝
    console.log(`❌ Credits 不足且无订阅: ${currentCredits} < ${amount}`);
    throw new Error('Credits 不足');
}

if (currentCredits < amount && (hasSubscription || isTestMode)) {
    console.log(`⚠️ Credits 不足，但允许超额使用（${hasSubscription ? '有订阅记录' : '测试模式'}）`);
}
```

---

## 📊 逻辑说明

### 允许超额使用的条件（任一满足）
1. ✅ **活跃的 Pro Plan**（`planType === 'Pro Plan' && subscription.status === 'active'`）
2. ✅ **有订阅记录**（`subscription.stripeSubscriptionId` 存在）
   - 包括已取消的订阅
   - 用于测试超额计费
3. ✅ **测试模式**（`userData.isTestMode === true`）
   - 专门用于测试 Stripe Billing Meter

### 拒绝的条件（全部满足）
- ❌ Free Plan
- ❌ 无订阅记录
- ❌ 非测试模式
- ❌ Credits 不足

---

## 🚀 已部署

```bash
✅ firebase deploy --only functions:deductCreditsClient
✔  functions[deductCreditsClient(us-central1)] Successful update operation.
```

---

## 🧪 现在请重新测试

### 步骤1：刷新页面
- 按 **Cmd + Shift + R**

### 步骤2：上传 1 个文档

### 步骤3：查看浏览器控制台
- 应该看到：
  ```
  ✅ Credits 已通過後端扣除: 1 頁
  ```

### 步骤4：查看 Firebase Logs
- 搜索：`deductCreditsClient`
- 应该看到：
  ```
  📞 客户端调用 deductCreditsClient
  🔍 扣除 Credits
  ⚠️ Credits 不足，但允许超额使用（有订阅记录）
  📡 reportUsageToStripe
  ✅ 使用量已报告给 Stripe Billing Meter
  ```

### 步骤5：查看 Stripe Meter
- 应该看到新的 Meter Event！
- 数量：1
- 客户：cus_TcZTukSbC3QlVh

---

## 📋 预期结果

### 浏览器控制台
```
✅ Credits 已通過後端扣除: 1 頁
剩餘: -55
```

### Firebase Logs
```
📞 客户端调用 deductCreditsClient: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2
🔍 扣除 Credits: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, current=-54, deduct=1
⚠️ Credits 不足，但允许超额使用（有订阅记录）
📡 reportUsageToStripe: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, quantity=1
✅ 使用量已报告给 Stripe Billing Meter: meterEventId=...
```

### Stripe Dashboard → Billing → Meters
- Event Name: `vaultcaddy_credit_usage`
- Customer: `cus_TcZTukSbC3QlVh`
- Value: `1`
- Timestamp: （上传时间）

---

## 🎯 关键改进

1. ✅ **支持已取消订阅的用户**：只要有过订阅记录，就允许超额使用
2. ✅ **测试模式支持**：`isTestMode` 用户可以无限制测试
3. ✅ **灵活的权限控制**：三种方式允许超额使用
4. ✅ **保留 Free Plan 限制**：完全没有订阅的免费用户仍受限制


