# 🚨 缺少 stripeCustomerId 字段

## 🐛 问题诊断

从 Firebase Logs 可以看到：
```
❌ 用户没有 Stripe Customer ID: 3bLhZuU9H0b3ExhwFCJuN4vZeGb2
```

**根本原因**：用户的 Firestore 文档中**缺少 `stripeCustomerId` 字段**！

`reportUsageToStripe` 函数的检查逻辑（第 1233-1236 行）：
```javascript
const stripeCustomerId = userData?.stripeCustomerId;

if (!stripeCustomerId) {
    console.error(`❌ 用户没有 Stripe Customer ID: ${userId}`);
    return;  // ← 提前返回，无法报告使用量
}
```

---

## 🔧 解决方案

### 方案1：手动添加 stripeCustomerId（最快）

根据之前的截图，你的 Stripe Customer ID 是：`cus_TcZTukSbC3QlVh`

1. **打开 Firestore**：
   https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore

2. **找到你的用户文档**：
   `users/3bLhZuU9H0b3ExhwFCJuN4vZeGb2`

3. **添加字段**：
   - 字段名：`stripeCustomerId`
   - 类型：`string`
   - 值：`cus_TcZTukSbC3QlVh`

4. **保存并测试**

---

### 方案2：修改代码从 subscription 获取（更通用）

有些用户可能将 Customer ID 存储在 `subscription.stripeCustomerId` 中。

修改 `reportUsageToStripe` 函数：
```javascript
const stripeCustomerId = userData?.stripeCustomerId 
    || userData?.subscription?.stripeCustomerId
    || userData?.subscription?.customerId;

if (!stripeCustomerId) {
    console.error(`❌ 用户没有 Stripe Customer ID: ${userId}`);
    return;
}
```

---

## 📋 下一步

### 请先截图 Firestore 用户数据

1. 打开：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore
2. 进入 `users` 集合
3. 找到：`3bLhZuU9H0b3ExhwFCJuN4vZeGb2`
4. 截图给我看，让我确认：
   - ✅ 是否有 `stripeCustomerId` 字段
   - ✅ `subscription` 对象的完整结构
   - ✅ 是否有其他地方存储了 Customer ID

---

## 🎯 预期结果

添加 `stripeCustomerId` 后，再上传文档时应该看到：
```
📡 reportUsageToStripe: userId=..., quantity=1
🔧 使用测试模式的 Stripe 客户端
✅ 使用量已报告给 Stripe Billing Meter: meterEventId=...
```

然后 Stripe Meter 就会有数据了！


