# Credits 管理系統 - 快速開始指南

## 🚀 5 步驟完成部署

### 步驟 1: 安裝 Firebase CLI

```bash
npm install -g firebase-tools
firebase login
```

### 步驟 2: 部署 Cloud Functions

```bash
cd firebase-functions
npm install

# 配置 Stripe 密鑰（先使用測試密鑰）
firebase functions:config:set stripe.secret_key="sk_test_YOUR_TEST_KEY"
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_TEST_WEBHOOK_SECRET"

# 部署
firebase deploy --only functions
```

**完成後你會看到：**
```
✔  functions: Finished running deploy script.
✔  functions[stripeWebhook]: Successful create operation.
✔  functions[monthlyCreditsReset]: Successful create operation.
✔  functions[checkExpiredSubscriptions]: Successful create operation.
✔  functions[addCreditsManual]: Successful create operation.
✔  functions[getCreditsHistory]: Successful create operation.
```

複製 `stripeWebhook` 的 URL：
```
https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/stripeWebhook
```

---

### 步驟 3: 配置 Stripe Webhook

1. 前往 Stripe Dashboard（**Test Mode**）：https://dashboard.stripe.com/test/webhooks

2. 點擊「Add endpoint」

3. 填入：
   - **Endpoint URL:** `https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/stripeWebhook`
   - **Events to send:**
     - ✅ `checkout.session.completed`
     - ✅ `payment_intent.succeeded`
     - ✅ `customer.subscription.created`
     - ✅ `customer.subscription.updated`
     - ✅ `customer.subscription.deleted`

4. 點擊「Add endpoint」

5. 複製「Signing secret」（`whsec_...`）

6. 更新 Firebase 配置：
```bash
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_NEW_SECRET"
firebase deploy --only functions
```

---

### 步驟 4: 創建 Stripe 產品（使用現有的）

您已經有一些 Stripe Payment Links，我們只需要：

1. 確認現有的訂閱計劃 Payment Links：
   - Basic Monthly: `https://buy.stripe.com/bJe7sM9LKctka9obwCf7i01`
   - Basic Yearly: `https://buy.stripe.com/5kQ3cw0ba64WbdseIOf7i02`
   - Pro Monthly: `https://buy.stripe.com/aFa3cwga8alc1CSeIOf7i03`
   - Pro Yearly: `https://buy.stripe.com/3cI14o1fe2SK0yO306f7i04`
   - Business Monthly: `https://buy.stripe.com/8x200k7DC8d45T87gmf7i05`
   - Business Yearly: `https://buy.stripe.com/14A5kEaPOfFw6XccAGf7i06`

2. 創建一次性購買 Credits 產品（**可選**）：
   - 前往 https://dashboard.stripe.com/test/products
   - 創建 4 個產品：50, 100, 200, 500 Credits
   - 每個產品創建 Payment Link
   - 更新 `stripe-manager.js` 中的 `paymentLink`

---

### 步驟 5: 測試系統

#### 5.1 測試訂閱流程

1. 前往 `https://vaultcaddy.com/billing.html`
2. 點擊任意訂閱計劃的「開始使用」按鈕
3. 使用測試卡號：`4242 4242 4242 4242`
   - 有效期：任何未來日期（如 `12/34`）
   - CVC：任意 3 位數字（如 `123`）
   - 郵編：任意 5 位數字（如 `12345`）
4. 完成支付
5. 返回 `billing.html?success=true`

**預期結果：**
- ✅ 頁面顯示成功通知
- ✅ Credits 增加（如 Basic Monthly = 200 Credits）
- ✅ `localStorage` 中的 `userPlan` 更新為 `Basic`
- ✅ Firebase Firestore 中創建 `creditsHistory` 記錄

#### 5.2 驗證 Firestore

打開 Firebase Console → Firestore：

```
users/{userId}/
  ├── credits: 200
  ├── subscription: { ... }
  └── creditsHistory/
      └── {historyId}/
          ├── type: "add"
          ├── amount: 200
          ├── before: 0
          ├── after: 200
          └── createdAt: ...
```

#### 5.3 驗證 UI

1. 前往 `account.html`
   - ✅ 「目前計劃」顯示「Basic Plan」
   - ✅ 「Credits 使用情況」卡片顯示「200 / 200」
   - ✅ 進度條顯示 100%

2. 前往 `billing.html`
   - ✅ 「Credits 使用記錄」表格顯示記錄
   - ✅ 顯示「訂閱計劃 - BASIC」、「增加」、「+200」

---

## 🧪 測試卡號

**成功支付：**
- `4242 4242 4242 4242`

**需要 3D Secure 驗證：**
- `4000 0027 6000 3184`

**支付失敗：**
- `4000 0000 0000 0002`

**其他資料：**
- 有效期：任何未來日期
- CVC：任意 3 位數字
- 郵編：任意值

---

## ✅ 檢查清單

### 部署前：

- [ ] Firebase CLI 已安裝
- [ ] Cloud Functions 已部署
- [ ] Stripe Webhook 已配置
- [ ] Webhook 密鑰已更新
- [ ] 測試卡號支付成功

### 測試通過：

- [ ] 訂閱流程完整
- [ ] Credits 正確增加
- [ ] Firestore 記錄正確
- [ ] UI 正確顯示
- [ ] 歷史記錄正確保存

### 上線準備（當測試通過後）：

- [ ] 切換到 Stripe Live Mode
- [ ] 使用 Live Mode 密鑰重新配置
- [ ] 創建 Live Mode Webhook
- [ ] 更新所有 Payment Links 為 Live 版本
- [ ] 使用真實信用卡測試（小額）

---

## 🐛 常見問題

### Q1: Cloud Functions 部署失敗

**A:** 檢查：
1. Node.js 版本（需要 Node 18）
2. Firebase 項目 ID 是否正確
3. 是否有計費帳戶（Cloud Functions 需要 Blaze 計劃）

```bash
firebase use --add  # 選擇正確的項目
node -v            # 檢查 Node 版本
```

### Q2: Webhook 沒有觸發

**A:** 檢查：
1. Webhook URL 是否正確
2. 選擇的事件是否包含 `checkout.session.completed`
3. Firebase Console → Functions → Logs 查看日誌

```bash
firebase functions:log --only stripeWebhook
```

### Q3: Credits 沒有增加

**A:** 檢查：
1. Firebase Console → Firestore 是否有寫入
2. 瀏覽器控制台是否有錯誤
3. `localStorage` 中的 `pendingSubscription` 是否存在

```javascript
// 在瀏覽器控制台執行
console.log(localStorage.getItem('pendingSubscription'));
```

### Q4: UI 沒有更新

**A:** 刷新頁面，檢查：
1. `stripe-manager.js` 是否正確載入
2. 瀏覽器控制台是否有 JavaScript 錯誤
3. Firebase Authentication 是否已登入

---

## 📞 需要幫助？

**文檔：**
- `CREDITS_SYSTEM_COMPLETE_SUMMARY.md` - 完整總結
- `CLOUD_FUNCTIONS_SETUP.md` - Cloud Functions 詳細指南
- `STRIPE_CONFIGURATION_GUIDE.md` - Stripe 配置指南

**外部資源：**
- Firebase Functions: https://firebase.google.com/docs/functions
- Stripe Webhooks: https://stripe.com/docs/webhooks
- Stripe Testing: https://stripe.com/docs/testing

---

## 🎉 完成！

如果所有測試通過，您的 Credits 管理系統已經可以使用了！

**下一步建議：**
1. 多次測試訂閱和購買流程
2. 驗證 Credits 使用（上傳文件）
3. 檢查 Credits 扣除是否正確
4. 準備切換到生產環境

**恭喜！系統已經就緒！** 🚀

