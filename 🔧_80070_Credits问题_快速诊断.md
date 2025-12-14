# 🔧 80070 Credits 问题 - 快速诊断指南

## 🚨 **问题**

用户 `AZ55k5F...` 完成 1 次 Monthly 订阅，但 Credits 显示为 **80070**（应该是 **100**）

---

## ⚡ **快速诊断（5 分钟）**

### **步骤 1：查看 processedStripeEvents 数量**

1. 访问 Firebase Console
   ```
   https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/firestore/databases/-default-/data/~2FprocessedStripeEvents?hl=zh-cn
   ```

2. **查看事件数量**
   - 左侧显示的文档总数
   - 如果有 800+ 个文档 → **确认是重复处理问题**
   - 如果只有 1-5 个文档 → **问题不在这里**

3. **筛选 checkout 事件**
   - 点击"添加过滤器"
   - 字段：`eventType`
   - 运算符：`==`
   - 值：`checkout.session.completed`
   - **查看结果数量**

---

### **步骤 2：查看 Stripe Webhook 日志**

1. 访问 Stripe Dashboard
   ```
   https://dashboard.stripe.com/test/workbench/webhooks
   ```

2. **找到最近的 checkout 事件**
   - 搜索 `checkout.session.completed`
   - 点击进入事件详情

3. **查看 Webhook attempts（尝试次数）**
   - 如果只有 1 次，返回 200 OK → **正常**
   - 如果有多次尝试 → **确认是 Stripe 重试问题**
   - 如果有 500 错误 → **确认是 Cloud Function 错误**

---

### **步骤 3：使用诊断函数**

1. 访问 `https://vaultcaddy.com/account.html`
2. 按 `F12` 打开控制台
3. 粘贴以下代码：

```javascript
// 查询 Credits 历史
const f = firebase.functions().httpsCallable('queryUserCredits');

// 替换为实际的 email（如果知道）
const email = prompt('输入用户 email（或留空查询当前登录用户）');

const result = await f({ 
    email: email || firebase.auth().currentUser.email 
});

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('📊 Credits 诊断结果');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`📧 Email: ${result.data.email}`);
console.log(`💰 当前 Credits: ${result.data.currentCredits}`);
console.log(`➕ 添加次数: ${result.data.addCount} 次`);
console.log(`💵 总添加金额: ${result.data.totalAdded} Credits`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

if (result.data.addCount > 1) {
    console.log('🚨 发现异常：Credits 被添加了多次！');
    console.log('📜 添加记录:');
    const addRecords = result.data.history.filter(h => h.type === 'add');
    addRecords.slice(0, 10).forEach((h, i) => {
        const time = new Date(h.timestamp).toLocaleString('zh-TW');
        console.log(`${i+1}. [${time}] +${h.amount} Credits`);
    });
} else {
    console.log('✅ Credits 添加次数正常');
}
```

4. **查看输出**
   - `addCount: 1` → **正常**
   - `addCount: 800+` → **确认是重复添加问题**

---

## 📊 **诊断结果判断**

### **情况 A：processedStripeEvents 有 800+ 条**

**原因**：Idempotency 检查失效

**证据**：
- `processedStripeEvents` 集合有大量事件
- 每个事件的 `eventId` 都不同（不是真正的重复）
- `addCount` 显示为 800+

**解决方案**：
1. 改进 idempotency 检查（使用 Firestore Transaction）
2. 清空 `processedStripeEvents` 测试数据
3. 重新测试

---

### **情况 B：Stripe Webhook 显示多次尝试**

**原因**：Cloud Function 返回 500 错误，Stripe 自动重试

**证据**：
- Stripe Webhook 日志显示多次尝试
- 部分请求返回 500 错误
- `processedStripeEvents` 可能只有 1 条（首次成功后的记录）

**解决方案**：
1. 查看 Firebase Functions 日志，找出 500 错误原因
2. 修复导致错误的代码
3. 确保所有错误都被捕获，总是返回 200

---

### **情况 C：只有 1 条 processedStripeEvents，但 Credits 还是 80070**

**原因**：可能是 `addCredits` 函数内部的问题

**证据**：
- `processedStripeEvents` 只有 1 条
- Stripe Webhook 只尝试 1 次
- 但 `addCount` 显示为 800+

**解决方案**：
1. 检查 `addCredits` 函数是否有循环或重复调用
2. 检查 `creditsHistory` 子集合是否有重复记录
3. 检查是否有其他代码路径调用 `addCredits`

---

## 🛠️ **根本修复方案**

### **方案 1：使用 Firestore Transaction（推荐）**

在 `stripeWebhook` 函数中，使用事务确保原子性：

```javascript
exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
    // ...验证签名...
    
    const eventId = event.id;
    const processedRef = db.collection('processedStripeEvents').doc(eventId);
    
    try {
        await db.runTransaction(async (transaction) => {
            const doc = await transaction.get(processedRef);
            
            if (doc.exists) {
                console.log(`⚠️ 事件 ${eventId} 已处理过，跳过`);
                throw new Error('ALREADY_PROCESSED');
            }
            
            // 标记为处理中（原子性操作）
            transaction.set(processedRef, {
                eventId,
                eventType: event.type,
                processedAt: admin.firestore.FieldValue.serverTimestamp(),
                isTestMode: isTestMode
            });
            
            // 处理事件
            // ...
        });
        
        res.status(200).json({ received: true });
        
    } catch (error) {
        if (error.message === 'ALREADY_PROCESSED') {
            res.status(200).json({ received: true, skipped: true });
        } else {
            // 只有真正的错误才返回 500
            res.status(500).json({ error: error.message });
        }
    }
});
```

### **方案 2：添加 Session ID 检查**

在 `handleCheckoutCompleted` 函数中，增加基于 Session ID 的二次检查：

```javascript
async function handleCheckoutCompleted(session, isTestMode) {
    const sessionId = session.id;
    
    // 🔒 二次检查：这个 session 是否已经处理过
    const sessionRef = db.collection('processedCheckouts').doc(sessionId);
    
    try {
        // 使用 create() 确保原子性
        await sessionRef.create({
            sessionId,
            processedAt: admin.firestore.FieldValue.serverTimestamp(),
            userId: session.client_reference_id || 'unknown'
        });
        console.log(`✅ Session ${sessionId} 首次处理`);
    } catch (error) {
        if (error.code === 6) { // ALREADY_EXISTS
            console.log(`⚠️ Session ${sessionId} 已处理过，跳过`);
            return;
        }
        throw error;
    }
    
    // 继续处理...
}
```

---

## 📋 **立即执行清单**

- [ ] 1. 访问 Firebase Console，查看 `processedStripeEvents` 数量
- [ ] 2. 访问 Stripe Dashboard，查看 Webhook 日志
- [ ] 3. 运行浏览器控制台诊断代码
- [ ] 4. 根据诊断结果判断原因（A、B 或 C）
- [ ] 5. 截图所有诊断结果
- [ ] 6. 提供截图以便进一步分析

---

## ⚠️ **临时解决方案**

在找到根本原因前：

1. **手动修正 Credits**
   - Firebase Console → users → AZ55k5F...
   - credits: 80070 → **100**
   - currentCredits: 80070 → **100**
   - totalCreditsUsed: → **0**

2. **清空测试数据**
   - 删除 `processedStripeEvents` 中的所有文档
   - 删除 `processedCheckouts` 集合（如果存在）

3. **暂停新测试**
   - 在修复完成前，不要再进行新的支付测试
   - 避免继续产生异常数据

---

**🔍 请立即执行以上诊断步骤，并提供截图！**

