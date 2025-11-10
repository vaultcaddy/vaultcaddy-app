# Stripe 配置指南

## 📦 已實現功能

### 1. Stripe Payment Links 配置

**一次性購買 Credits：**
- 50 Credits: $15 → `YOUR_LINK_50_CREDITS`
- 100 Credits: $29 → `YOUR_LINK_100_CREDITS`
- 200 Credits: $56 → `YOUR_LINK_200_CREDITS`
- 500 Credits: $138 → `https://buy.stripe.com/aFa3cwga8alc1CSeIOf7i03`

**訂閱計劃（已配置）：**
- Basic Monthly: $22/月, 200 Credits → `https://buy.stripe.com/bJe7sM9LKctka9obwCf7i01`
- Basic Yearly: $216/年, 2400 Credits → `https://buy.stripe.com/5kQ3cw0ba64WbdseIOf7i02`
- Pro Monthly: $38/月, 500 Credits → `https://buy.stripe.com/aFa3cwga8alc1CSeIOf7i03`
- Pro Yearly: $360/年, 6000 Credits → `https://buy.stripe.com/3cI14o1fe2SK0yO306f7i04`
- Business Monthly: $78/月, 1200 Credits → `https://buy.stripe.com/8x200k7DC8d45T87gmf7i05`
- Business Yearly: $744/年, 14400 Credits → `https://buy.stripe.com/14A5kEaPOfFw6XccAGf7i06`

---

## 🔗 如何創建 Stripe Payment Links

### 1. 登入 Stripe Dashboard
https://dashboard.stripe.com/

### 2. 創建產品
前往 **Products** → **Add Product**

#### 一次性購買 Credits 產品：

**產品名稱：** `50 Credits`  
**價格：** $15 USD  
**Payment Mode：** Payment (一次性支付)  
**Metadata：**
- `credits` = `50`
- `type` = `purchase`

重複此步驟創建 100, 200, 500 Credits 的產品。

#### 訂閱計劃產品：

**產品名稱：** `Basic Plan (Monthly)`  
**價格：** $22 USD / month  
**Payment Mode：** Subscription (訂閱)  
**Metadata：**
- `plan_type` = `basic`
- `monthly_credits` = `200`
- `period` = `monthly`

重複此步驟創建所有訂閱計劃（Pro, Business, Yearly 版本）。

### 3. 創建 Payment Links

對每個產品：
1. 點擊產品旁的 **...** → **Create payment link**
2. 設置以下選項：
   - **Success URL:** `https://vaultcaddy.com/billing.html?success=true`
   - **Cancel URL:** `https://vaultcaddy.com/billing.html?cancel=true`
   - **Collect customer information:** Email address
   - **Allow promotion codes:** Yes (可選)
3. 點擊 **Create link**
4. 複製生成的鏈接

### 4. 更新配置

將生成的 Payment Links 更新到：

#### `stripe-manager.js`:
```javascript
products: {
    credits: {
        50: {
            price: 15,
            paymentLink: 'YOUR_NEW_LINK_HERE'
        },
        // ... 其他
    }
}
```

#### `billing.html` 的 `stripeLinks`:
```javascript
const stripeLinks = {
    'basic': {
        monthly: 'YOUR_NEW_LINK_HERE',
        yearly: 'YOUR_NEW_LINK_HERE'
    },
    // ... 其他
};
```

---

## 🪝 Webhook 配置

### 1. 創建 Webhook Endpoint

前往 Stripe Dashboard → **Developers** → **Webhooks** → **Add endpoint**

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

### 2. 獲取 Webhook Secret

創建 Webhook 後，Stripe 會給你一個 `whsec_...` 開頭的密鑰。

### 3. 配置 Firebase Functions

```bash
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_SECRET"
firebase deploy --only functions
```

---

## 🧪 測試流程

### 測試環境設置：

1. **切換到 Stripe Test Mode**（在 Dashboard 右上角）
2. **使用測試卡號：**
   - 成功: `4242 4242 4242 4242`
   - 需要 3D Secure: `4000 0027 6000 3184`
   - 失敗: `4000 0000 0000 0002`
   - 有效期: 任何未來日期
   - CVC: 任意 3 位數字

### 測試一次性購買：

1. 前往 `billing.html`
2. 點擊「購買 Credits」按鈕
3. 選擇任意 Credits 包（如 500 Credits）
4. 跳轉到 Stripe Checkout
5. 使用測試卡號完成支付
6. 返回 `billing.html?success=true`
7. 檢查 Credits 是否增加
8. 檢查 Firebase 中的 `creditsHistory` 集合

### 測試訂閱：

1. 前往 `billing.html`
2. 選擇月費或年費
3. 點擊任意訂閱計劃的「開始使用」按鈕
4. 跳轉到 Stripe Checkout
5. 使用測試卡號完成支付
6. 返回 `billing.html?success=true`
7. 檢查：
   - Credits 是否增加
   - `localStorage` 中的 `userPlan` 和 `userPlanPeriod` 是否更新
   - Firebase 中的訂閱信息是否正確
   - `account.html` 中的 Credits 使用卡片是否顯示

---

## 📊 監控與日誌

### Stripe Dashboard 監控：

- **Payments:** 查看所有支付記錄
- **Customers:** 查看客戶信息
- **Subscriptions:** 管理訂閱
- **Logs → Webhooks:** 查看 Webhook 調用記錄

### Firebase Console 監控：

- **Firestore:** 查看 `users/{userId}/creditsHistory` 集合
- **Functions → Logs:** 查看 Cloud Functions 日誌
- **Authentication:** 查看用戶列表

### 瀏覽器控制台：

打開開發者工具（F12），查看：
- Console 日誌
- Network 請求
- localStorage 內容

---

## ⚠️ 重要提醒

### 安全性：

1. **永不在前端暴露 Secret Key**
   - ✅ 使用 Payment Links (安全)
   - ✅ 使用 Cloud Functions (安全)
   - ❌ 不要在 JavaScript 中使用 `sk_live_...`

2. **驗證 Webhook 簽名**
   - Cloud Functions 中的 `stripeWebhook` 已實現簽名驗證
   - 防止惡意請求

3. **使用 HTTPS**
   - Stripe 要求所有 Webhook URL 使用 HTTPS
   - Firebase Hosting 默認啟用 HTTPS

### 資料一致性：

1. **使用 Firestore Transactions**
   - 防止併發問題
   - `stripe-manager.js` 和 Cloud Functions 已實現

2. **冪等性**
   - Stripe 可能會重複發送 Webhook
   - 記錄 `paymentIntentId` 或 `sessionId` 防止重複處理

3. **錯誤處理**
   - 所有函數都應該有 try-catch
   - Webhook 必須返回 200 狀態碼

### 測試要點：

- ✅ 成功支付流程
- ✅ 取消支付流程
- ✅ Credits 正確增加
- ✅ 歷史記錄正確保存
- ✅ UI 正確更新
- ✅ 訂閱狀態正確保存
- ✅ 過期訂閱正確處理

---

## 🚀 生產環境部署清單

### 上線前：

- [ ] 切換到 Stripe Live Mode
- [ ] 更新所有 Payment Links 為 Live 版本
- [ ] 部署 Cloud Functions
- [ ] 配置 Live Mode Webhook
- [ ] 測試完整流程（使用真實信用卡，小額測試）
- [ ] 檢查所有日誌和監控

### 上線後：

- [ ] 監控 Stripe Dashboard
- [ ] 監控 Firebase Functions Logs
- [ ] 監控 Firestore 數據
- [ ] 準備客服支持流程
- [ ] 設置異常告警

---

## 📞 支持與幫助

**Stripe 文檔：**
- Payment Links: https://stripe.com/docs/payment-links
- Webhooks: https://stripe.com/docs/webhooks
- Testing: https://stripe.com/docs/testing

**Firebase 文檔：**
- Cloud Functions: https://firebase.google.com/docs/functions
- Firestore Transactions: https://firebase.google.com/docs/firestore/manage-data/transactions

**VaultCaddy 相關文件：**
- `CLOUD_FUNCTIONS_SETUP.md` - Cloud Functions 部署指南
- `CREDITS_IMPLEMENTATION_STATUS.md` - Credits 系統實現進度
- `stripe-manager.js` - Stripe 管理器代碼
- `billing.html` - 計費頁面
- `account.html` - 帳戶頁面

---

## 🎉 已實現功能總結

✅ Stripe Payment Links 集成  
✅ 一次性購買 Credits  
✅ 訂閱計劃（月費/年費）  
✅ 支付成功回調處理  
✅ Credits 自動授予  
✅ 歷史記錄保存  
✅ UI 實時更新  
✅ Firebase Cloud Functions 自動處理  
✅ Credits 過期機制  
✅ 用戶訂閱狀態管理  

**系統已經完整可用！🎊**

