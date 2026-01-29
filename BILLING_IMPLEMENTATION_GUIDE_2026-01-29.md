# 📋 VaultCaddy 計費系統完整實現指南
**更新日期**: 2026-01-29  
**狀態**: Firebase Function 已創建，等待部署和測試

---

## ✅ 已完成的工作

### 1️⃣ Stripe 價格創建
- ✅ 使用 Stripe API 創建了 8 個價格（4種幣種 × 2種計劃）
- ✅ 所有 Price ID 已記錄在 `stripe-manager.js`

### 2️⃣ 前端價格顯示更新
- ✅ **中文版** (billing.html): HKD $38/月，HKD $28/月 (年付)
- ✅ **英文版** (en/billing.html): USD $4.88/月，USD $3.58/月 (年付)
- ✅ **日文版** (jp/billing.html): JPY ¥788/月，JPY ¥588/月 (年付)
- ✅ **韓文版** (kr/billing.html): KRW ₩6,988/月，KRW ₩5,188/月 (年付)

### 3️⃣ Firebase Function 創建
- ✅ `createStripeCheckoutSession` 函數已創建
- ✅ 自動根據語言版本選擇對應幣種的 Price ID
- ✅ 支持 metadata 記錄（用於 Webhook 處理）

---

## ⚙️ 部署步驟

### 步驟 1: 設置 Stripe API Key

**方式 A: 使用 Firebase CLI 設置環境變數** (推薦)

```bash
cd firebase-functions
firebase functions:config:set stripe.secret="YOUR_STRIPE_SECRET_KEY"
```

**方式 B: 使用環境變數文件**

創建 `firebase-functions/.env`:

```
STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY
```

> ⚠️ **重要**: 將 `YOUR_STRIPE_SECRET_KEY` 替換為您的實際 Stripe Secret Key（從 Stripe Dashboard 獲取）

### 步驟 2: 安裝依賴並部署

```bash
cd firebase-functions
npm install
firebase deploy --only functions
```

**預期輸出**:
```
✔  functions[us-central1-qwenProxy]: Successful update operation.
✔  functions[us-central1-createStripeCheckoutSession]: Successful create operation.
```

### 步驟 3: 測試 Checkout Flow

1. 前往 `https://vaultcaddy.com/billing.html`
2. 點擊「開始使用」按鈕（月付或年付）
3. 應該跳轉到 Stripe Checkout 頁面
4. 使用測試卡完成支付: `4242 4242 4242 4242`
5. 驗證跳轉回 `/account.html?payment=success`

---

## 🚧 待實現：超額計費 (0.3/頁)

### 當前狀態
- ❌ **尚未實現自動超額計費**
- ✅ 頁面上已顯示「超出後每頁 HKD $0.3」

### 實現方案概述

超額計費需要以下組件：

#### A. Firestore 數據結構更新

在 `users/{userId}` 中添加：

```json
{
  "subscription": {
    "stripeSubscriptionId": "sub_xxx",
    "stripePriceId": "price_xxx",
    "planType": "monthly",
    "currency": "hkd",
    "monthlyCredits": 100,
    "currentPeriodStart": "2026-01-01T00:00:00Z",
    "currentPeriodEnd": "2026-02-01T00:00:00Z"
  },
  "credits": 85,  // 當前剩餘 Credits
  "usageThisPeriod": {
    "totalPages": 15,  // 本週期已使用頁數
    "overagePages": 0   // 超出免費額度的頁數
  }
}
```

#### B. Credits 扣減時檢查超額

修改 `simple-data-manager.js` 中的 Credits 扣減邏輯：

```javascript
async function deductCredits(pages) {
    const userId = simpleAuth.getCurrentUser().uid;
    const userDoc = await db.collection('users').doc(userId).get();
    const userData = userDoc.data();
    
    let creditsToDeduct = pages;
    let overagePages = 0;
    
    // 檢查是否為訂閱用戶
    if (userData.subscription && userData.subscription.planType) {
        // 如果 Credits 不足，標記為超額使用
        if (userData.credits < pages) {
            overagePages = pages - userData.credits;
            creditsToDeduct = userData.credits;  // 扣完剩餘 Credits
        }
        
        // 更新數據
        await db.collection('users').doc(userId).update({
            credits: Math.max(0, userData.credits - creditsToDeduct),
            'usageThisPeriod.totalPages': firebase.firestore.FieldValue.increment(pages),
            'usageThisPeriod.overagePages': firebase.firestore.FieldValue.increment(overagePages)
        });
        
        // 如果有超額使用，報告給 Stripe
        if (overagePages > 0) {
            await reportUsageToStripe(userData.subscription.stripeSubscriptionId, overagePages);
        }
    } else {
        // 非訂閱用戶，直接扣 Credits
        await db.collection('users').doc(userId).update({
            credits: userData.credits - pages
        });
    }
}
```

#### C. Firebase Function: 報告使用量給 Stripe

在 `firebase-functions/index.js` 添加：

```javascript
exports.reportUsageToStripe = functions
    .https.onCall(async (data, context) => {
        if (!context.auth) {
            throw new functions.https.HttpsError('unauthenticated', 'User must be logged in');
        }
        
        const { subscriptionId, quantity } = data;
        
        try {
            // 獲取訂閱的計費項 ID (subscription item ID)
            const subscription = await stripe.subscriptions.retrieve(subscriptionId);
            const subscriptionItemId = subscription.items.data[0].id;
            
            // 報告使用量
            const usageRecord = await stripe.subscriptionItems.createUsageRecord(
                subscriptionItemId,
                {
                    quantity: quantity,
                    timestamp: Math.floor(Date.now() / 1000),
                    action: 'increment'
                }
            );
            
            console.log(`✅ 使用量已報告: ${quantity} 頁`);
            return { success: true, usageRecord };
            
        } catch (error) {
            console.error('❌ 報告使用量失敗:', error);
            throw new functions.https.HttpsError('internal', error.message);
        }
    });
```

#### D. Stripe Webhook 處理訂閱事件

在 `firebase-functions/index.js` 添加：

```javascript
exports.stripeWebhook = functions
    .runWith({ memory: '256MB' })
    .https.onRequest(async (req, res) => {
        const sig = req.headers['stripe-signature'];
        const webhookSecret = functions.config().stripe?.webhook_secret || process.env.STRIPE_WEBHOOK_SECRET;
        
        let event;
        
        try {
            event = stripe.webhooks.constructEvent(req.rawBody, sig, webhookSecret);
        } catch (err) {
            console.error('⚠️  Webhook 簽名驗證失敗:', err.message);
            return res.status(400).send(`Webhook Error: ${err.message}`);
        }
        
        console.log(`📨 收到 Webhook 事件: ${event.type}`);
        
        switch (event.type) {
            case 'checkout.session.completed':
                await handleCheckoutCompleted(event.data.object);
                break;
                
            case 'customer.subscription.created':
            case 'customer.subscription.updated':
                await handleSubscriptionUpdate(event.data.object);
                break;
                
            case 'customer.subscription.deleted':
                await handleSubscriptionDeleted(event.data.object);
                break;
                
            case 'invoice.payment_succeeded':
                await handleInvoicePaymentSucceeded(event.data.object);
                break;
                
            case 'invoice.payment_failed':
                await handleInvoicePaymentFailed(event.data.object);
                break;
        }
        
        res.json({ received: true });
    });

async function handleCheckoutCompleted(session) {
    const userId = session.metadata.userId || session.client_reference_id;
    const planType = session.metadata.planType;
    const currency = session.metadata.currency;
    
    console.log(`💳 訂閱成功: userId=${userId}, planType=${planType}`);
    
    // 獲取訂閱 ID
    const subscriptionId = session.subscription;
    
    // 更新 Firestore 用戶數據
    await admin.firestore().collection('users').doc(userId).set({
        subscription: {
            stripeSubscriptionId: subscriptionId,
            stripePriceId: PRICE_IDS[planType][currency],
            planType: planType,
            currency: currency,
            monthlyCredits: 100,
            status: 'active'
        },
        credits: admin.firestore.FieldValue.increment(planType === 'yearly' ? 1200 : 100),
        planType: 'Pro',
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });
}

async function handleInvoicePaymentSucceeded(invoice) {
    // 每月續費成功，重置 Credits 和使用量
    const subscriptionId = invoice.subscription;
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
    const userId = subscription.metadata.userId;
    
    if (!userId) {
        console.warn('⚠️  訂閱沒有關聯的 userId');
        return;
    }
    
    console.log(`💰 續費成功: userId=${userId}`);
    
    // 重置 Credits 和使用量
    await admin.firestore().collection('users').doc(userId).update({
        credits: 100,  // 重置為 100 Credits
        'usageThisPeriod.totalPages': 0,
        'usageThisPeriod.overagePages': 0,
        'subscription.currentPeriodStart': new Date(subscription.current_period_start * 1000),
        'subscription.currentPeriodEnd': new Date(subscription.current_period_end * 1000),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
}
```

---

## 🔐 Stripe Webhook 設置

### 步驟 1: 部署 Webhook Function

```bash
firebase deploy --only functions:stripeWebhook
```

### 步驟 2: 在 Stripe Dashboard 添加 Webhook

1. 前往: https://dashboard.stripe.com/webhooks
2. 點擊「Add endpoint」
3. URL: `https://us-central1-<your-project-id>.cloudfunctions.net/stripeWebhook`
4. 選擇事件:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. 複製「Signing secret」（例如：`whsec_xxx`）

### 步驟 3: 設置 Webhook Secret

```bash
firebase functions:config:set stripe.webhook_secret="whsec_xxx"
firebase deploy --only functions:stripeWebhook
```

---

## 🧪 測試清單

### 基本支付流程
- [ ] 中文版月付訂閱（HKD $38）
- [ ] 中文版年付訂閱（HKD $336）
- [ ] 英文版月付訂閱（USD $4.88）
- [ ] 英文版年付訂閱（USD $42.96）
- [ ] 日文版月付訂閱（JPY ¥788）
- [ ] 韓文版月付訂閱（KRW ₩6,988）

### 超額計費測試
- [ ] 用戶使用 100 Credits 後，系統自動扣費
- [ ] Firestore 正確記錄 `overagePages`
- [ ] Stripe 收到使用量報告
- [ ] 下個計費週期 Credits 正確重置

### Webhook 測試
- [ ] 訂閱成功後用戶獲得 Credits
- [ ] 續費成功後 Credits 重置
- [ ] 訂閱取消後用戶計劃降級
- [ ] 支付失敗後系統通知用戶

---

## 📊 成本估算

### 100 Credits/月方案（訂閱用戶）

| 項目 | 免費額度內 | 超出額度 (101-200 頁) | 總成本 |
|------|----------|---------------------|--------|
| **月付 (HKD $38)** | 100 頁 | 100 頁 × $0.3 = $30 | **$68** |
| **年付 (HKD $28/月)** | 100 頁 | 100 頁 × $0.3 = $30 | **$58** |

### API 成本（Qwen-VL Max）

- **輸入**: ~5,000 tokens/頁 × $0.002/1K = **$0.01/頁**
- **輸出**: ~1,000 tokens/頁 × $0.006/1K = **$0.006/頁**
- **總成本**: ~**$0.016/頁**

### 毛利分析

假設用戶使用 200 頁/月：
- **收入**: $38 (月付) + $30 (超額) = **$68**
- **API 成本**: 200 頁 × $0.016 = **$3.2**
- **Stripe 手續費**: $68 × 2.9% + $0.30 = **$2.27**
- **毛利**: $68 - $3.2 - $2.27 = **$62.53** (92%)

---

## 🚀 下一步行動

### 立即執行
1. ✅ 部署 Firebase Functions
   ```bash
   cd firebase-functions
   npm install
   firebase deploy --only functions
   ```

2. ⏳ 測試基本支付流程

### 後續實施（需要時）
3. 實現超額計費邏輯
4. 設置 Stripe Webhook
5. 全面測試所有場景

---

## 💡 重要提醒

### 當前狀態
- ✅ **價格顯示**: 已更新為新定價
- ✅ **Stripe 價格**: 已創建所有 Price ID
- ✅ **Checkout Function**: 已創建，待部署
- ❌ **超額計費**: 尚未實現

### 風險評估
- **低風險**: 基本訂閱流程（月付/年付 100 Credits）
- **中風險**: 超額計費（需要正確實現使用量報告）
- **建議**: 先部署和測試基本訂閱流程，確認無誤後再實現超額計費

---

**文檔版本**: 1.0.0  
**最後更新**: 2026-01-29  
**維護者**: VaultCaddy Development Team

