# Firebase Cloud Functions 設置指南

## 📦 安裝與部署

### 1. 安裝 Firebase CLI

```bash
npm install -g firebase-tools
```

### 2. 登入 Firebase

```bash
firebase login
```

### 3. 初始化 Firebase Functions

```bash
cd firebase-functions
npm install
```

### 4. 配置 Stripe 密鑰

```bash
firebase functions:config:set stripe.secret_key="sk_live_YOUR_STRIPE_SECRET_KEY"
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_WEBHOOK_SECRET"
```

### 5. 部署 Cloud Functions

```bash
firebase deploy --only functions
```

---

## 🔧 Stripe Webhook 配置

### 1. 在 Stripe Dashboard 設置 Webhook

前往：https://dashboard.stripe.com/webhooks

點擊「Add endpoint」

**Endpoint URL:** 
```
https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/stripeWebhook
```

**監聽的事件：**
- ✅ `checkout.session.completed`
- ✅ `payment_intent.succeeded`
- ✅ `customer.subscription.created`
- ✅ `customer.subscription.updated`
- ✅ `customer.subscription.deleted`

### 2. 複製 Webhook 簽名密鑰

從 Stripe Dashboard 複製 `whsec_...` 密鑰，並設置：

```bash
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_KEY"
```

---

## 🏷️ Stripe 產品配置

### 在 Stripe Dashboard 創建產品時，添加以下 metadata：

#### **一次性購買 Credits 產品：**

| 產品名稱 | metadata.credits | 價格 |
|---------|------------------|------|
| 50 Credits | 50 | $15 |
| 100 Credits | 100 | $29 |
| 200 Credits | 200 | $56 |
| 500 Credits | 500 | $138 |

#### **訂閱計劃產品：**

| 產品名稱 | metadata.plan_type | metadata.monthly_credits | 價格 |
|---------|-------------------|-------------------------|------|
| Basic Plan (月訂閱) | basic | 200 | $22 |
| Pro Plan (月訂閱) | pro | 500 | $38 |
| Business Plan (月訂閱) | business | 1200 | $78 |
| Basic Plan (年訂閱) | basic | 2400 | $216 |
| Pro Plan (年訂閱) | pro | 6000 | $360 |
| Business Plan (年訂閱) | business | 14400 | $744 |

**重要：**
- 年訂閱的 `monthly_credits` 是整年的總額
- 系統會根據 `current_period_start` 和 `current_period_end` 自動分配

---

## 📊 Firestore 數據結構

### users/{userId}

```javascript
{
  email: "user@example.com",
  credits: 200,                    // 當前 Credits
  createdAt: timestamp,
  updatedAt: timestamp,
  lastCreditsReset: timestamp,     // 最後一次重置時間
  subscription: {
    stripeSubscriptionId: "sub_xxx",
    status: "active",               // active, expired, cancelled
    planType: "basic",              // free, basic, pro, business
    monthlyCredits: 200,            // 每月 Credits 額度
    currentPeriodStart: timestamp,
    currentPeriodEnd: timestamp,
    cancelAtPeriodEnd: false,
    cancelledAt: timestamp,         // 取消時間（如果已取消）
    expiredAt: timestamp            // 過期時間（如果已過期）
  }
}
```

### users/{userId}/creditsHistory/{historyId}

```javascript
{
  type: "add",                     // add, deduct, reset
  amount: 200,
  before: 0,
  after: 200,
  metadata: {
    source: "subscription",        // subscription, purchase, manual
    planType: "basic",
    period: "2025-11-01 - 2025-12-01",
    stripeSessionId: "cs_xxx",
    productName: "Basic Plan",
    amount: 22.00,
    currency: "usd"
  },
  createdAt: timestamp
}
```

### users/{userId}/payments/{paymentId}

```javascript
{
  paymentIntentId: "pi_xxx",
  amount: 22.00,
  currency: "usd",
  status: "succeeded",
  createdAt: timestamp
}
```

---

## 🔄 Cloud Functions 功能說明

### 1. `stripeWebhook`
- **觸發：** HTTP POST from Stripe
- **功能：** 處理 Stripe 的所有 webhook 事件
- **URL:** `https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/stripeWebhook`

### 2. `monthlyCreditsReset`
- **觸發：** 每月1號凌晨
- **功能：** 為活躍訂閱用戶重置 Credits 為當月額度

### 3. `checkExpiredSubscriptions`
- **觸發：** 每6小時
- **功能：** 檢查並標記過期的訂閱

### 4. `addCreditsManual`
- **觸發：** HTTP Call
- **功能：** 手動添加 Credits（測試用）
- **使用方式：**
```javascript
const addCredits = firebase.functions().httpsCallable('addCreditsManual');
await addCredits({ amount: 100 });
```

### 5. `getCreditsHistory`
- **觸發：** HTTP Call
- **功能：** 獲取 Credits 歷史記錄
- **使用方式：**
```javascript
const getHistory = firebase.functions().httpsCallable('getCreditsHistory');
const result = await getHistory({ limit: 50 });
console.log(result.data.history);
```

---

## 🧪 測試

### 測試 Webhook（本地）

```bash
# 1. 啟動本地模擬器
firebase emulators:start

# 2. 使用 Stripe CLI 轉發 webhooks
stripe listen --forward-to localhost:5001/YOUR_PROJECT_ID/us-central1/stripeWebhook

# 3. 觸發測試事件
stripe trigger checkout.session.completed
```

### 測試手動添加 Credits

在瀏覽器控制台：

```javascript
const addCredits = firebase.functions().httpsCallable('addCreditsManual');
addCredits({ amount: 100 }).then(result => {
  console.log(result.data);
});
```

---

## 📝 日誌監控

### 查看實時日誌

```bash
firebase functions:log
```

### 查看特定函數的日誌

```bash
firebase functions:log --only stripeWebhook
```

---

## ⚠️ 注意事項

1. **Stripe 密鑰安全：**
   - 永遠不要將密鑰提交到 Git
   - 使用 `firebase functions:config:set` 設置

2. **Webhook 驗證：**
   - 必須驗證 Stripe 簽名
   - 防止惡意請求

3. **事務使用：**
   - Credits 操作必須使用事務
   - 防止併發問題

4. **錯誤處理：**
   - 所有 webhook 都應該返回 200
   - 記錄詳細錯誤日誌

5. **測試環境：**
   - 使用 Stripe 測試密鑰進行測試
   - 使用本地模擬器進行開發

---

## 🚀 部署後檢查清單

- [ ] Cloud Functions 部署成功
- [ ] Stripe Webhook 配置正確
- [ ] Stripe 產品 metadata 設置正確
- [ ] 測試一次性購買流程
- [ ] 測試訂閱流程
- [ ] 測試 Credits 重置（手動觸發）
- [ ] 查看 Cloud Functions 日誌
- [ ] 監控 Firestore 數據

---

## 📞 支持

如有問題，請查看：
- Firebase Console: https://console.firebase.google.com
- Stripe Dashboard: https://dashboard.stripe.com
- Firebase Functions 文檔: https://firebase.google.com/docs/functions

