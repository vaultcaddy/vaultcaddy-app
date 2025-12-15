# 🚨 Credits 异常 - 紧急修复指南

## 📊 **问题**

用户 `osclin2002@gmail.com` 完成 1 次 Monthly 订阅，但 Credits 显示为 **80070**（应该是 **100**）

```
预期 Credits：100
实际 Credits：80070
异常倍数：800.7x ❌
```

---

## 🔧 **紧急修复（5 分钟）**

### **步骤 1：访问 Firebase Console**

```
https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/firestore/databases/-default-/data/~2Fusers?hl=zh-cn
```

### **步骤 2：找到用户文档**

1. 在 `users` 集合中
2. 搜索或浏览找到 `osclin2002@gmail.com`
3. 点击进入用户文档

### **步骤 3：修改 Credits 字段**

| 字段 | 当前值 | 修改为 | 说明 |
|------|--------|--------|------|
| `credits` | 80070 | **100** | 当前可用 Credits |
| `currentCredits` | 80070 | **100** | 当前可用 Credits（同步）|
| `totalCreditsUsed` | ? | **0** | 累计使用量（重置）|
| `includedCredits` | ? | **100** | 订阅包含的 Credits |

### **步骤 4：保存**

点击"保存"按钮，刷新 https://vaultcaddy.com/account.html，Credits 应该显示为 **100**。

---

## 🔍 **诊断工具（已部署）**

### **使用浏览器控制台查询 Credits 历史**

1. 访问 https://vaultcaddy.com/account.html
2. 打开开发者工具 → Console
3. 粘贴以下代码并运行：

```javascript
// 查询 Credits 历史
const queryFunc = firebase.functions().httpsCallable('queryUserCredits');
const result = await queryFunc({ email: 'osclin2002@gmail.com' });
console.log('📊 Credits 诊断结果:', result.data);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`📧 Email: ${result.data.email}`);
console.log(`💰 当前 Credits: ${result.data.currentCredits}`);
console.log(`📋 Plan: ${result.data.planType}`);
console.log(`➕ 总添加次数: ${result.data.addCount} 次`);
console.log(`💵 总添加金额: ${result.data.totalAdded} Credits`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('📜 最近 30 条历史记录:');
result.data.history.forEach((h, i) => {
    console.log(`${i+1}. [${h.timestamp}] ${h.type} ${h.amount > 0 ? '+' : ''}${h.amount}`);
});
```

4. **查看结果**：
   - `addCount`：应该是 1，如果是 800+ 说明重复添加
   - `totalAdded`：应该是 100，如果是 80070 说明累计重复
   - `history`：查看是否有大量重复的添加记录

---

## 🔍 **手动诊断步骤**

### **检查 1：Firestore - processedStripeEvents**

```
https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/firestore/databases/-default-/data/~2FprocessedStripeEvents?hl=zh-cn
```

**查看内容**：
- 有多少个 `checkout.session.completed` 事件？
- 是否有相同的 event ID 被重复处理？
- 时间戳是否正常？

**预期结果**：
- ✅ 只有 1 个 checkout 事件
- ❌ 有 800+ 个 checkout 事件（说明 idempotency 失效）

---

### **检查 2：Stripe Dashboard - Webhook 日志**

```
https://dashboard.stripe.com/test/workbench/webhooks
```

**查看内容**：
- 最近的 `checkout.session.completed` 事件
- 查看"Attempts"（尝试次数）
- 查看返回状态码

**预期结果**：
- ✅ 只发送 1 次，返回 200 OK
- ❌ 发送了多次，或返回 500 错误

---

### **检查 3：Stripe Dashboard - Webhook 配置**

```
https://dashboard.stripe.com/test/webhooks
```

**查看内容**：
- 有多少个 webhook endpoint？
- 是否有重复的 URL？

**预期结果**：
- ✅ 只有 1 个 webhook endpoint
- ❌ 有多个 webhook endpoint 指向同一个 URL

---

### **检查 4：Firebase Functions - 日志**

```
https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/functions/logs?hl=zh-cn
```

**查看内容**：
- 搜索 `checkout.session.completed`
- 查看有多少条"✅ 結帳完成"日志
- 查看是否有错误日志

**预期结果**：
- ✅ 只有 1 条处理日志
- ❌ 有 800+ 条重复日志

---

## 💡 **可能的原因分析**

### **原因 1：Idempotency 检查失效（最可能）**

```javascript
// 代码中有 idempotency 检查
await processedEventsRef.create({...});

// 但如果出现以下情况，检查会失效：
// 1. 网络延迟导致 create() 超时
// 2. Firestore 写入失败但没有抛出错误
// 3. 并发请求之间的竞态条件
```

**特征**：
- processedStripeEvents 中有大量重复事件
- 所有事件的 eventId 都不同（不是真正的重复）

---

### **原因 2：Stripe Webhook 重试（次可能）**

```
1. Cloud Function 返回 500 错误
2. Stripe 认为处理失败
3. Stripe 自动重试（最多 72 小时）
4. 每次重试都添加 Credits
```

**特征**：
- Stripe Webhook 日志显示多次尝试
- 部分请求返回 500 错误

---

### **原因 3：多个 Webhook Endpoint（不太可能）**

```
如果配置了 800 个 webhook endpoint...
（这几乎不可能，除非配置严重错误）
```

---

## 🛠️ **根本修复方案**

### **方案 1：改进 Idempotency 检查（推荐）**

使用 Firestore Transaction 确保原子性：

```javascript
exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
    // ...验证签名...
    
    // 🔒 使用事务确保幂等性
    const eventId = event.id;
    const processedRef = db.collection('processedStripeEvents').doc(eventId);
    
    try {
        await db.runTransaction(async (transaction) => {
            const doc = await transaction.get(processedRef);
            
            if (doc.exists) {
                console.log(`⚠️ 事件 ${eventId} 已处理过，跳过`);
                throw new Error('ALREADY_PROCESSED');
            }
            
            // 标记为处理中
            transaction.set(processedRef, {
                eventId,
                eventType: event.type,
                processedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            
            // 处理事件
            // ...
        });
        
        res.status(200).json({ received: true });
        
    } catch (error) {
        if (error.message === 'ALREADY_PROCESSED') {
            res.status(200).json({ received: true, skipped: true });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});
```

---

### **方案 2：添加基于 Session ID 的检查**

```javascript
async function handleCheckoutCompleted(session, isTestMode) {
    const sessionId = session.id;
    
    // 🔒 检查这个 session 是否已经处理过
    const sessionRef = db.collection('processedCheckouts').doc(sessionId);
    const sessionDoc = await sessionRef.get();
    
    if (sessionDoc.exists) {
        console.log(`⚠️ Session ${sessionId} 已处理过，跳过`);
        return;
    }
    
    // 标记为已处理
    await sessionRef.set({
        sessionId,
        processedAt: admin.firestore.FieldValue.serverTimestamp(),
        userId: session.client_reference_id
    });
    
    // 继续处理...
}
```

---

## 📋 **诊断清单**

请按顺序完成以下检查，并截图：

- [ ] 1. 在浏览器控制台运行 `queryUserCredits` 函数
- [ ] 2. 查看 `addCount`（添加次数）和 `totalAdded`（总添加量）
- [ ] 3. 访问 Firestore `processedStripeEvents` 集合
- [ ] 4. 统计 `checkout.session.completed` 事件数量
- [ ] 5. 访问 Stripe Webhook 日志
- [ ] 6. 查看最近的 checkout 事件发送次数
- [ ] 7. 访问 Stripe Webhook 配置
- [ ] 8. 检查是否有重复的 endpoint

---

## ⚡ **临时解决方案（立即执行）**

### **1. 手动修正 Credits**
- Firebase Console → users → osclin2002@gmail.com
- credits: 80070 → **100**
- currentCredits: 80070 → **100**

### **2. 清空异常记录**
- 删除 processedStripeEvents 中所有测试事件
- 避免污染数据

### **3. 暂停测试**
- 在找到根本原因前，不要再测试订阅
- 避免继续产生异常数据

---

## 📞 **需要您提供的信息**

为了准确诊断，请提供以下截图：

1. **Firebase Console**
   - processedStripeEvents 集合（最近 20 条）
   - osclin2002@gmail.com 的 creditsHistory（最近 20 条）

2. **Stripe Dashboard**
   - Webhook 日志（最近的 checkout.session.completed 事件）
   - Webhook 配置页面（显示所有 endpoint）

3. **浏览器控制台**
   - 运行 `queryUserCredits` 的输出结果

---

**🚨 这是严重 bug，需要立即处理！**  
**请先手动修正 Credits，然后提供诊断信息！**


