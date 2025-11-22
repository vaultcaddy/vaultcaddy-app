# 🚀 Stripe 整合 - 下一步操作指南

**文檔作用**：提供完成 Stripe 整合的詳細步驟，幫助您快速完成 Payment Links 創建、Webhook 配置和部署。

**更新日期**：2025-11-22

---

## ✅ 已完成的工作

1. ✅ **Stripe 產品配置**
   - 月費產品：`prod_TSmKnHeaQVxZXC` (HK$78/月 + 100 Credits)
   - 年費產品：`prod_TSsEWI5bv9pSkz` (HK$744/年 + 1,200 Credits)
   - 使用量計費：階梯定價（0-100/1200 頁免費，超出後 HK$0.5/頁）

2. ✅ **前端代碼**
   - `index.html`：客戶評價區域已優化
   - `billing.html`：已整合 Stripe 產品 ID
   - `stripe-manager.js`：已添加訂閱和使用量追蹤功能

3. ✅ **後端代碼**
   - `firebase-functions/index.js`：已添加使用量報告功能

---

## 📋 待完成的步驟

### 步驟 1：創建 Payment Links

#### 1.1 創建月費 Payment Link

1. 打開 Stripe Dashboard：https://dashboard.stripe.com/acct_1S6Qv3JmiQ31C0GT/payment-links
2. 點擊右上角的「+ 新建」按鈕
3. 填寫以下信息：
   - **產品**：選擇 `VaultCaddy 月費` (`prod_TSmKnHeaQVxZXC`)
   - **價格**：選擇 `HK$78.00/月` + 使用量計費價格
   - **名稱**：VaultCaddy 月費訂閱
   - **描述**：每月 HK$78，包含 100 Credits，超出後每頁 HK$0.5
   - **成功頁面**：`https://vaultcaddy.com/billing.html?success=true`
   - **取消頁面**：`https://vaultcaddy.com/billing.html?cancelled=true`
   - **允許促銷代碼**：✅ 啟用
   - **收集客戶信息**：
     - ✅ 電子郵件地址
     - ✅ 姓名
   - **稅務設置**：根據您的需求配置

4. 點擊「創建 Payment Link」
5. **複製生成的 Payment Link URL**（格式：`https://buy.stripe.com/xxxxx`）

#### 1.2 創建年費 Payment Link

重複上述步驟，但選擇：
- **產品**：`VaultCaddy 年費` (`prod_TSsEWI5bv9pSkz`)
- **價格**：`HK$744.00/年` + 使用量計費價格
- **名稱**：VaultCaddy 年費訂閱
- **描述**：每年 HK$744（平均每月 HK$62），包含 1,200 Credits，超出後每頁 HK$0.5

---

### 步驟 2：更新代碼中的 Payment Link URL

#### 2.1 更新 `stripe-manager.js`

打開 `/Users/cavlinyeung/ai-bank-parser/stripe-manager.js`

找到第 42 和 50 行，替換為您剛創建的實際 Payment Link：

```javascript
// 第 42 行
paymentLink: 'https://buy.stripe.com/YOUR_ACTUAL_MONTHLY_LINK'  // 替換為實際的月費 Payment Link

// 第 50 行
paymentLink: 'https://buy.stripe.com/YOUR_ACTUAL_YEARLY_LINK'   // 替換為實際的年費 Payment Link
```

**示例**（假設您的 Payment Link 是）：
```javascript
monthly: {
    productId: 'prod_TSmKnHeaQVxZXC',
    price: 78,
    credits: 100,
    period: 'monthly',
    overage: 0.5,
    paymentLink: 'https://buy.stripe.com/test_28o3cwga8alc1CSeIOf7i03'  // ✅ 實際的月費 Link
},
yearly: {
    productId: 'prod_TSsEWI5bv9pSkz',
    price: 744,
    credits: 1200,
    period: 'yearly',
    overage: 0.5,
    paymentLink: 'https://buy.stripe.com/test_xxxxxxxxxxxxxxxxxxxxx'  // ✅ 實際的年費 Link
}
```

#### 2.2 提交更改

```bash
cd /Users/cavlinyeung/ai-bank-parser
git add stripe-manager.js
git commit -m "✅ 更新 Stripe Payment Links

- 月費 Payment Link: [YOUR_LINK]
- 年費 Payment Link: [YOUR_LINK]"
git push
```

---

### 步驟 3：配置 Stripe Webhook

#### 3.1 創建 Webhook Endpoint

1. 打開 Stripe Dashboard：https://dashboard.stripe.com/acct_1S6Qv3JmiQ31C0GT/webhooks
2. 點擊「+ 添加端點」
3. 填寫以下信息：
   - **端點 URL**：`https://YOUR_PROJECT_ID.cloudfunctions.net/stripeWebhook`
     - 替換 `YOUR_PROJECT_ID` 為您的 Firebase 項目 ID
     - 例如：`https://vaultcaddy-12345.cloudfunctions.net/stripeWebhook`
   
4. **選擇要監聽的事件**：
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`

5. 點擊「添加端點」
6. **複製 Webhook 簽名密鑰**（格式：`whsec_xxxxx`）

#### 3.2 配置 Firebase Functions Config

在終端執行以下命令：

```bash
# 設置 Stripe Secret Key（從 Stripe Dashboard → 開發者 → API 密鑰）
firebase functions:config:set stripe.secret_key="sk_test_YOUR_SECRET_KEY"

# 設置 Webhook Secret（剛才複製的簽名密鑰）
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_WEBHOOK_SECRET"

# 查看配置（確認設置成功）
firebase functions:config:get
```

---

### 步驟 4：部署 Cloud Functions

#### 4.1 安裝依賴

```bash
cd /Users/cavlinyeung/ai-bank-parser/firebase-functions
npm install
```

#### 4.2 部署到 Firebase

```bash
firebase deploy --only functions
```

**預期輸出**：
```
✔  functions: Finished running predeploy script.
i  functions: ensuring required API cloudfunctions.googleapis.com is enabled...
i  functions: ensuring required API cloudbuild.googleapis.com is enabled...
✔  functions: required API cloudfunctions.googleapis.com is enabled
✔  functions: required API cloudbuild.googleapis.com is enabled
i  functions: preparing functions directory for uploading...
i  functions: packaged functions (XX.XX KB) for uploading
✔  functions: functions folder uploaded successfully
i  functions: creating Node.js 16 function stripeWebhook(us-central1)...
i  functions: creating Node.js 16 function reportStripeUsage(us-central1)...
i  functions: creating Node.js 16 function reportDailyUsage(us-central1)...
✔  functions[stripeWebhook(us-central1)]: Successful create operation.
✔  functions[reportStripeUsage(us-central1)]: Successful create operation.
✔  functions[reportDailyUsage(us-central1)]: Successful create operation.

✔  Deploy complete!
```

#### 4.3 驗證部署

1. 打開 Firebase Console：https://console.firebase.google.com/
2. 選擇您的項目
3. 左側菜單 → Functions
4. 確認以下函數已部署：
   - ✅ `stripeWebhook`
   - ✅ `reportStripeUsage`
   - ✅ `reportDailyUsage`

---

### 步驟 5：測試完整流程

#### 5.1 測試訂閱流程

1. 打開您的網站：https://vaultcaddy.com/billing.html
2. 點擊「立即開始」按鈕（月費或年費）
3. 應該跳轉到 Stripe Checkout 頁面
4. 使用 Stripe 測試卡號完成支付：
   - **卡號**：`4242 4242 4242 4242`
   - **到期日期**：任何未來日期（例如：12/25）
   - **CVC**：任何 3 位數字（例如：123）
   - **郵編**：任何 5 位數字（例如：12345）

5. 完成支付後，應該：
   - 跳轉回 `https://vaultcaddy.com/billing.html?success=true`
   - 顯示成功通知
   - Credits 自動添加到用戶帳戶

#### 5.2 測試使用量計費

1. 在您的應用中處理超過 100 頁的文件（月費用戶）
2. 檢查 Firebase Console → Firestore → `usageRecords` 集合
3. 確認使用量記錄已創建
4. 檢查 Stripe Dashboard → 客戶 → 訂閱 → 使用量
5. 確認使用量已報告給 Stripe

#### 5.3 測試定時任務

手動觸發定時任務（測試環境）：

```bash
firebase functions:shell

# 在 shell 中執行
> reportDailyUsage()

# 查看日誌
firebase functions:log --only reportDailyUsage
```

---

## 🐛 常見問題排查

### Q1: Payment Link 無法跳轉？
**解決方案**：
1. 確認 `stripe-manager.js` 中的 URL 已更新
2. 清除瀏覽器緩存
3. 檢查瀏覽器控制台是否有錯誤

### Q2: Webhook 未觸發？
**解決方案**：
1. 檢查 Webhook URL 是否正確
2. 確認 Cloud Function 已部署
3. 查看 Stripe Dashboard → Webhooks → 查看日誌
4. 查看 Firebase Functions 日誌：`firebase functions:log --only stripeWebhook`

### Q3: Credits 未自動添加？
**解決方案**：
1. 檢查 Webhook 配置
2. 確認 `client_reference_id` 或 `metadata.userId` 已設置
3. 查看 `stripeWebhook` 日誌

### Q4: 使用量未報告給 Stripe？
**解決方案**：
1. 確認 Cloud Function `reportStripeUsage` 已部署
2. 檢查 Stripe API 密鑰是否正確
3. 確認訂閱包含使用量計費項目
4. 查看日誌：`firebase functions:log --only reportStripeUsage`

---

## 📊 監控和維護

### 日誌監控

```bash
# 查看所有 Cloud Functions 日誌
firebase functions:log

# 查看特定函數日誌
firebase functions:log --only reportStripeUsage
firebase functions:log --only reportDailyUsage
firebase functions:log --only stripeWebhook
```

### Stripe Dashboard 監控

1. **訂閱管理**：Subscriptions → Active subscriptions
2. **使用量報告**：Billing → Usage reports
3. **收入統計**：Home → Revenue
4. **Webhook 日誌**：Developers → Webhooks → View logs

### Firestore 監控

在 Firebase Console 中查看：
- `users` 集合：用戶 Credits 和訂閱狀態
- `usageRecords` 集合：使用量記錄
- `users/{userId}/creditsHistory` 子集合：Credits 歷史

---

## ✅ 完成檢查清單

在完成所有步驟後，請確認以下項目：

- [ ] 月費 Payment Link 已創建並測試
- [ ] 年費 Payment Link 已創建並測試
- [ ] `stripe-manager.js` 中的 URL 已更新
- [ ] Webhook 已配置並驗證
- [ ] Firebase Functions Config 已設置
- [ ] Cloud Functions 已部署成功
- [ ] 測試訂閱流程成功
- [ ] 測試使用量計費成功
- [ ] 定時任務已測試
- [ ] 監控和日誌系統正常運行

---

## 🎉 完成後的下一步

1. **切換到生產模式**
   - 使用生產環境的 Stripe API 密鑰
   - 更新 Webhook URL 為生產環境
   - 重新部署 Cloud Functions

2. **優化用戶體驗**
   - 添加訂閱管理頁面（查看、升級、取消）
   - 顯示當月使用量和預估費用
   - 提供使用量歷史圖表

3. **法律合規**
   - 添加訂閱條款和條件
   - 實施退款政策
   - 確保符合 PCI DSS 標準

4. **市場推廣**
   - 準備上線公告
   - 設置促銷代碼
   - 配置電子郵件通知

---

**需要幫助？**
- 查看完整文檔：`STRIPE_INTEGRATION_GUIDE.md`
- Firebase 文檔：https://firebase.google.com/docs/functions
- Stripe 文檔：https://stripe.com/docs

**文檔維護者**：AI Assistant  
**最後更新**：2025-11-22  
**版本**：1.0

