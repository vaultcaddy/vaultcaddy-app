# 🎯 修复根本问题：客户端直接扣除 Credits

## 🐛 问题根源

**客户端直接在 Firestore 中扣除 Credits，没有调用后端函数！**

### 旧流程（有问题）❌
```
用户上传文档
    ↓
客户端 credits-manager.js
    ↓
直接在 Firestore 中 transaction.update()
    ↓
Credits 被扣除 ✅
    ↓
但没有调用后端 deductCredits 函数 ❌
    ↓
reportUsageToStripe 从未被调用 ❌
    ↓
Stripe 没有收到 Meter Events ❌
```

### 为什么 Firebase Logs 中找不到日志？
因为**根本没有调用后端函数**！客户端直接操作 Firestore。

---

## ✅ 解决方案

### 新流程（正确）✅
```
用户上传文档
    ↓
客户端 credits-manager.js
    ↓
调用后端 Cloud Function: deductCreditsClient() ✨
    ↓
后端 deductCreditsClient()
    ↓
调用内部 deductCredits()
    ↓
扣除 Credits 并自动调用 reportUsageToStripe()
    ↓
使用 Billing Meter Events API 报告给 Stripe ✅
    ↓
Stripe 收到 Meter Event ✅
```

---

## 📝 修改内容

### 1. 客户端（credits-manager.js）

**旧代码**：
```javascript
// 直接在 Firestore 中更新
await db.runTransaction(async (transaction) => {
    transaction.update(userRef, { 
        credits: newCredits,
        // ...
    });
});
```

**新代码**：
```javascript
// 调用后端 Cloud Function
const deductCreditsFunction = firebase.functions().httpsCallable('deductCreditsClient');
const result = await deductCreditsFunction({
    userId: user.uid,
    amount: pages,
    metadata: {
        source: 'document_upload'
    }
});
```

### 2. 后端（firebase-functions/index.js）

新增 `deductCreditsClient` 函数：
```javascript
exports.deductCreditsClient = functions.https.onCall(async (data, context) => {
    // 验证用户身份
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '请先登录');
    }
    
    // 调用内部 deductCredits 函数（会自动报告使用量）
    await deductCredits(userId, amount, metadata || {});
    
    return { success: true, newCredits: newCredits };
});
```

---

## 🧪 测试步骤

1. **清除浏览器缓存**
   - 按 `Cmd + Shift + R`（Mac）强制刷新

2. **重新登录**
   - https://vaultcaddy.com/auth.html

3. **上传 1 个文档**

4. **查看 Firebase Logs**
   - 应该看到：
     - `📞 客户端调用 deductCreditsClient`
     - `🔍 扣除 Credits: userId=...`
     - `📡 reportUsageToStripe: userId=...`
     - `✅ 使用量已报告给 Stripe Billing Meter`

5. **查看 Stripe Meter**
   - 应该有新的 Meter Event

---

## 📊 预期结果

### Firebase Logs 应该显示：
```
2025-12-17 22:XX:XX  deductCreditsClient  📞 客户端调用 deductCreditsClient
2025-12-17 22:XX:XX  deductCredits        🔍 扣除 Credits: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2
2025-12-17 22:XX:XX  reportUsageToStripe  📡 reportUsageToStripe: userId=..., quantity=1
2025-12-17 22:XX:XX  reportUsageToStripe  ✅ 使用量已报告给 Stripe Billing Meter
```

### Stripe Meter 应该显示：
- 新的 Meter Event
- Event Name: `vaultcaddy_credit_usage`
- Customer ID: `cus_TcZTukSbC3QlVh`
- Quantity: 1（或 2）

---

## ⚠️ 重要提醒

**必须清除浏览器缓存！**

因为 `credits-manager.js` 是客户端 JavaScript 文件，浏览器会缓存。

清除方法：
1. 打开开发者工具（F12）
2. 右键点击刷新按钮
3. 选择"清空缓存并硬性重新加载"

或：
- Mac: `Cmd + Shift + R`
- Windows: `Ctrl + Shift + R`



