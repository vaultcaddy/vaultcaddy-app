# ✅ 自动从 Stripe API 获取 Customer ID

## 🎯 问题根源

从 Firestore（图3）和 Firebase Logs（图5）可以看到：
- ✅ 有 `subscription.stripeSubscriptionId: "sub_1SfKxPJmiQ31C0GTaIFfWRoL"`
- ❌ 但是**没有** `stripeCustomerId` 字段

这导致 `reportUsageToStripe` 无法向 Stripe 报告使用量。

---

## ✅ 解决方案

### 新增功能：自动获取 Customer ID

修改后的 `reportUsageToStripe` 函数会：

1. **首先**从 Firestore 查找 `stripeCustomerId`
2. **如果找不到**，使用 `stripeSubscriptionId` 去 Stripe API 查询订阅
3. **从订阅中获取** `customer` 字段（这就是 Customer ID）
4. **自动保存**到 Firestore，避免下次再查询

### 关键代码

```javascript
// 如果没有找到，尝试从 Stripe API 获取
if (!stripeCustomerId && subscription?.stripeSubscriptionId) {
    console.log(`⚠️ 未找到 Customer ID，尝试从 Stripe 订阅中获取: ${subscription.stripeSubscriptionId}`);
    
    const stripeSubscription = await stripeClient.subscriptions.retrieve(subscription.stripeSubscriptionId);
    stripeCustomerId = stripeSubscription.customer;
    
    console.log(`✅ 从 Stripe API 获取到 Customer ID: ${stripeCustomerId}`);
    
    // 保存到 Firestore，避免下次再查询
    await db.collection('users').doc(userId).update({
        stripeCustomerId: stripeCustomerId
    });
}
```

---

## 🚀 已部署

```bash
✔  functions[deductCreditsClient(us-central1)] Successful update operation.
```

---

## 🧪 现在请重新测试！

### 步骤1：刷新页面并上传文档
- 按 **Cmd + Shift + R** 刷新页面
- 上传 **1 个新文档**

### 步骤2：查看 Firebase Logs

搜索：`reportUsageToStripe`

**预期看到的新日志**：
```
📡 reportUsageToStripe: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, quantity=1
🔍 查找 Customer ID: userData.stripeCustomerId=undefined, ...
⚠️ 未找到 Customer ID，尝试从 Stripe 订阅中获取: sub_1SfKxPJmiQ31C0GTaIFfWRoL
✅ 从 Stripe API 获取到 Customer ID: cus_TcZTukSbC3QlVh
✅ Customer ID 已保存到 Firestore
✅ 使用 Stripe Customer ID: cus_TcZTukSbC3QlVh
🔧 使用测试模式的 Stripe 客户端
✅ 使用量已报告给 Stripe Billing Meter: meterEventId=...
```

### 步骤3：查看 Firestore

刷新 Firestore 中的用户文档，应该看到新增的字段：
```
stripeCustomerId: "cus_TcZTukSbC3QlVh"
```

### 步骤4：查看 Stripe Meter

等待 **1-2 分钟**，刷新 Stripe Dashboard，应该看到新的 Meter Event！

---

## 🎉 预期结果

### 第一次上传文档后
1. ✅ 系统自动从 Stripe API 获取 Customer ID
2. ✅ Customer ID 保存到 Firestore
3. ✅ 使用量成功报告给 Stripe Billing Meter
4. ✅ Stripe Meter 显示数据

### 第二次上传文档后
1. ✅ 直接使用 Firestore 中保存的 Customer ID
2. ✅ 无需再次查询 Stripe API（更快）
3. ✅ 使用量成功报告

---

## 📊 修改的文件

- ✅ `firebase-functions/index.js`（`reportUsageToStripe` 函数）

---

## 🎯 下一步

请重新测试并截图：
1. ✅ Firebase Logs（应该看到自动获取 Customer ID 的日志）
2. ✅ Firestore（应该看到新增的 `stripeCustomerId` 字段）
3. ✅ Stripe Meter（应该看到新的 Event）

**这次一定会成功！** 🚀

