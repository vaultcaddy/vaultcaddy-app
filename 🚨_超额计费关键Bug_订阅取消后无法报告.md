# 🚨 超额计费关键 Bug - 订阅取消后无法报告使用量

## ❌ 问题发现

**时间：** 2025-12-15 17:36:53.791  
**严重程度：** 🔴 严重 - 导致超额使用无法收费

---

## 🐛 Bug 详情

### 错误信息

```
StripeInvalidRequestError: Cannot create a usage record for 'si_TbITgirZHFvrkY' 
because the subscription item is no longer active.
```

### 问题原因

**核心问题：**
当订阅被取消后，Stripe 的 `subscription_item` 立即变为不活跃状态。
我们的代码在 `customer.subscription.deleted` 事件中尝试报告使用量，但此时订阅已经被取消，无法再向 Stripe 报告使用量！

### 当前流程（错误）

```
用户点击"取消订阅"
    ↓
Stripe 立即取消订阅
    ↓
subscription_item 变为 inactive
    ↓
Stripe 触发 customer.subscription.deleted webhook
    ↓
我们的 handleSubscriptionCancelled 函数执行
    ↓
检测到 credits = -51（超额使用）
    ↓
尝试调用 stripe.subscriptionItems.createUsageRecord()
    ↓
❌ 失败！subscription_item 已经不活跃
    ↓
超额使用无法收费 ❌
```

---

## 📊 日志证据

### Firebase Functions 日志

```
时间: 2025-12-15 17:36:53.633
✅ 訂閱取消時的用戶數據: { credits: -51, totalCreditsUsed: 151, planType: 'Pro Plan' }
✅ 檢測到超額使用: -51 Credits
✅ 超額數量: 51 Credits
✅ 檢查訂閱信息: {
    hasSubscription: true,
    meteredItemId: 'si_TbITgirZHFvrkY',
    stripeSubscriptionId: 'sub_1SeXwdJmiQ31C0GTEBxxdwNn',
    monthlyCredits: 100,
    overageAmount: 51
}
✅ 📡 向 Stripe 報告總使用量...
✅ - Subscription ID: sub_1SeXwdJmiQ31C0GTEBxxdwNn
✅ - Metered Item ID: si_TbITgirZHFvrkY
✅ - 總使用量: 151

时间: 2025-12-15 17:36:53.791
❌ 報告超額使用失敗: StripeInvalidRequestError: Cannot create a usage record for 'si_TbITgirZHFvrkY' because...
```

### 结果

```
时间: 2025-12-15 17:36:54.087
✅ 用户已變成為 Free Plan: 3bLhZuU9HOb3ExhwFCJuN4vZeGb2 · Credits: -51 = 0
✅ Function execution took 3333 ms, finished with status code: 200
```

**问题：**
- Credits 被清零了（-51 → 0）
- 但是 Stripe 没有收到使用量报告
- 用户超额使用了 51 个 Credits（价值 HK$25.50），但没有被收费！

---

## 🔧 解决方案

### 方案 A：在订阅取消前报告（推荐）✅

**策略：** 在用户点击"取消订阅"按钮时，先报告超额使用，然后再取消订阅。

#### 实现步骤

1. **修改取消订阅流程**

在用户点击"管理订阅" → "取消订阅"时：

```javascript
// 在 Stripe Customer Portal 中，用户点击取消订阅前
// 我们需要在取消前报告超额使用

// 方法：使用 Stripe Webhooks 的顺序
// customer.subscription.updated (cancel_at_period_end = true)
//   ↓ 在这里报告超额使用
// customer.subscription.deleted
```

2. **修改 Firebase Functions**

```javascript
// firebase-functions/index.js

case 'customer.subscription.updated':
    // 检查是否设置了取消标记
    if (subscription.cancel_at_period_end === true || subscription.status === 'canceled') {
        // 在订阅真正取消前，先报告超额使用
        await reportOverageBeforeCancellation(subscription);
    }
    await handleSubscriptionChange(subscription, isTestMode);
    break;
```

---

### 方案 B：创建独立发票（备用）✅

**策略：** 订阅取消后，如果有超额使用，创建一个独立的发票。

```javascript
async function handleSubscriptionCancelled(subscription) {
    // ... 检测超额使用 ...
    
    if (currentCredits < 0) {
        const overageAmount = Math.abs(currentCredits);
        const unitPrice = 0.50; // HK$0.50 per credit
        const totalAmount = overageAmount * unitPrice * 100; // 转换为分
        
        try {
            // 创建独立发票项
            const invoiceItem = await stripeClient.invoiceItems.create({
                customer: subscription.customer,
                amount: totalAmount,
                currency: 'hkd',
                description: `超額使用 ${overageAmount} Credits (訂閱取消後)`,
            });
            
            // 创建并立即收取发票
            const invoice = await stripeClient.invoices.create({
                customer: subscription.customer,
                auto_advance: true, // 自动完成并收费
            });
            
            await stripeClient.invoices.finalizeInvoice(invoice.id);
            
            console.log(`✅ 已為超額使用創建發票: ${invoice.id}`);
            console.log(`💵 發票金額: HK$${(totalAmount / 100).toFixed(2)}`);
        } catch (error) {
            console.error(`❌ 創建超額發票失敗:`, error);
        }
    }
}
```

---

### 方案 C：定期检查并提前报告（最佳）🌟

**策略：** 每小时自动检查所有用户的 Credits，如果发现负数，立即报告给 Stripe。

```javascript
// 新增 Cloud Function
exports.checkAndReportOverageUsage = functions.pubsub
    .schedule('every 1 hours')
    .onRun(async (context) => {
        console.log('🔍 開始檢查超額使用...');
        
        const usersSnapshot = await db.collection('users')
            .where('planType', '==', 'Pro Plan')
            .where('currentCredits', '<', 0)
            .get();
        
        for (const doc of usersSnapshot.docs) {
            const userData = doc.data();
            const userId = doc.id;
            const currentCredits = userData.currentCredits;
            
            if (currentCredits < 0) {
                console.log(`⚠️ 發現用戶 ${userId} 超額使用: ${currentCredits}`);
                
                // 立即报告给 Stripe
                await reportOverageToStripe(userId, userData);
            }
        }
    });
```

---

## 🎯 立即临时解决方案

### 手动为用户 1234@gmail.com 创建发票

```bash
1. 打开 Stripe Dashboard：
   https://dashboard.stripe.com/test/customers/cus_TbITMVDgDLqLrR

2. 滚动到「Invoice items」部分

3. 点击「Add invoice item」

4. 填写：
   - Description: 超額使用 51 Credits
   - Unit price: HK$0.50
   - Quantity: 51
   - Total: HK$25.50

5. 点击「Add item」

6. 点击「Create invoice」

7. 点击「Finalize and send」

8. 完成！用户会收到 HK$25.50 的发票
```

---

## 📋 下一步行动

### 优先级 1：立即修复（方案 B）✅

1. 修改 `handleSubscriptionCancelled` 函数
2. 添加创建独立发票的逻辑
3. 部署到生产环境
4. 测试验证

### 优先级 2：长期优化（方案 C）🌟

1. 创建定期检查 Cloud Function
2. 设置每小时自动运行
3. 提前报告超额使用
4. 避免取消订阅时的问题

---

## 📝 总结

**问题：**
- 订阅取消后，subscription_item 立即失效
- 无法再向 Stripe 报告使用量
- 导致超额使用无法收费

**影响：**
- 用户超额使用不会被收费
- 公司损失收入

**紧急程度：**
- 🔴 高 - 直接影响收入

**解决方案：**
- ✅ 短期：创建独立发票（方案 B）
- 🌟 长期：定期检查并提前报告（方案 C）

---

**现在需要立即实施方案 B，修复这个 Bug！** 🚀

