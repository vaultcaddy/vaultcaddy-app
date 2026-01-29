# 🚀 超額計費功能部署指南
**版本**: 完整版（選項 A）  
**日期**: 2026-01-29

---

## ✅ 已實現的功能

### 1️⃣ Firebase Functions（3個新函數）
- ✅ `deductCreditsClient` - 扣除 Credits 並報告超額使用
- ✅ `reportStripeUsage` - 手動報告使用量到 Stripe
- ✅ `stripeWebhook` - 處理 Stripe 事件（訂閱、續費、取消）

### 2️⃣ 自動化流程
- ✅ Pro Plan 用戶可以負數 Credits
- ✅ 自動檢測超額使用並報告給 Stripe
- ✅ 自動處理每月續費和 Credits 重置
- ✅ 自動追蹤使用量歷史

### 3️⃣ 安全性
- ✅ 所有 API Keys 已移除，改為環境變數
- ✅ Webhook 簽名驗證
- ✅ 用戶身份驗證

---

## 📋 部署步驟

### 步驟 1: 設置環境變數（5 分鐘）

```bash
cd firebase-functions

# 設置 Stripe API Key
firebase functions:config:set stripe.secret="YOUR_STRIPE_SECRET_KEY"

# 設置 Qwen API Key
firebase functions:config:set qwen.api_key="YOUR_QWEN_API_KEY"

# 驗證配置
firebase functions:config:get
```

**如何獲取 API Keys**：參考 `ENV_SETUP_GUIDE.md`

---

### 步驟 2: 安裝依賴（2 分鐘）

```bash
cd firebase-functions
npm install
```

**預期輸出**：
```
added 5 packages
✓ firebase-admin@11.11.0
✓ stripe@14.11.0
```

---

### 步驟 3: 部署 Functions（3-5 分鐘）

```bash
# 部署所有 Functions
firebase deploy --only functions

# 或分別部署
firebase deploy --only functions:qwenProxy
firebase deploy --only functions:createStripeCheckoutSession
firebase deploy --only functions:deductCreditsClient
firebase deploy --only functions:reportStripeUsage
firebase deploy --only functions:stripeWebhook
```

**預期輸出**：
```
✔  functions[qwenProxy]: Successful update operation.
✔  functions[createStripeCheckoutSession]: Successful create operation.
✔  functions[deductCreditsClient]: Successful create operation.
✔  functions[reportStripeUsage]: Successful create operation.
✔  functions[stripeWebhook]: Successful create operation.

Function URL (stripeWebhook):
https://us-central1-YOUR-PROJECT.cloudfunctions.net/stripeWebhook
```

**⚠️ 重要**: 複製 `stripeWebhook` 的 URL，下一步會用到！

---

### 步驟 4: 設置 Stripe Webhook（5 分鐘）

#### 4.1 前往 Stripe Dashboard

https://dashboard.stripe.com/webhooks

#### 4.2 添加 Endpoint

1. 點擊「Add endpoint」
2. **Endpoint URL**: 填入上一步的 `stripeWebhook` URL
   ```
   https://us-central1-YOUR-PROJECT.cloudfunctions.net/stripeWebhook
   ```

3. **選擇事件**（勾選以下 6 個）:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`

4. 點擊「Add endpoint」

#### 4.3 複製 Webhook Secret

1. 在新創建的 Webhook 頁面，點擊「Reveal」
2. 複製 Signing secret（以 `whsec_` 開頭）

#### 4.4 配置 Webhook Secret

```bash
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_WEBHOOK_SECRET"

# 重新部署以使配置生效
firebase deploy --only functions:stripeWebhook
```

---

### 步驟 5: 在 Stripe 中添加超額計費項目（10 分鐘）

#### 5.1 配置月付超額計費

1. 前往: https://dashboard.stripe.com/products/prod_Tb24SiE4usHRDS
2. 點擊「Add another price」
3. 選擇「Usage is metered」
4. 配置：
   - **Billing period**: Monthly
   - **Usage is metered**: Yes
   - **Price**: Use the existing overage price `price_1SfZQQJmiQ31C0GTeUu6TSXE`
   - 如果不存在，創建新價格: $0.3/unit
5. 保存

#### 5.2 配置年付超額計費

1. 前往: https://dashboard.stripe.com/products/prod_Tb2443GvCbe4Pp
2. 點擊「Add another price」
3. 配置（同上）：
   - **Billing period**: Yearly
   - **Usage is metered**: Yes
   - **Price**: Use `price_1SfZQVJmiQ31C0GTOYgabmaJ`
   - 如果不存在，創建新價格: $0.3/unit
4. 保存

---

## 🧪 測試流程

### 測試 1: 基本訂閱流程（5 分鐘）

1. **前往網站**: https://vaultcaddy.com/billing.html
2. **點擊「開始使用」**（月付或年付）
3. **使用測試卡**: `4242 4242 4242 4242`
4. **驗證結果**:
   - ✅ 跳轉回 `account.html?payment=success`
   - ✅ Credits 增加（月付 +100，年付 +1200）
   - ✅ planType 變為 "Pro Plan"

---

### 測試 2: Credits 扣除（3 分鐘）

1. **上傳文件**: 任意 PDF 文件（例如 5 頁）
2. **查看 Console Log**:
   ```
   💰 扣除 Credits: amount=5
   ✅ Credits 已扣除: 新餘額 95
   ```
3. **驗證 Firestore**:
   - `credits`: 應該減少 5
   - `usageThisPeriod.totalPages`: 應該增加 5

---

### 測試 3: 超額使用（5 分鐘）

1. **準備**: 將用戶 Credits 手動改為 5（在 Firestore）
2. **上傳文件**: 10 頁的 PDF
3. **查看 Console Log**:
   ```
   💰 扣除 Credits: amount=10
   當前 Credits: 5, 計劃: Pro Plan
   ⚠️ 超額使用: 5 頁
   📊 報告超額使用量到 Stripe: 5 頁
   ✅ 使用量已報告到 Stripe
   ✅ Credits 已扣除: 新餘額 -5
   ```
4. **驗證 Stripe**:
   - 前往 Stripe Dashboard > Subscriptions
   - 查看用戶訂閱的「Usage」標籤
   - 應該看到 5 頁的使用記錄

---

### 測試 4: 續費和 Credits 重置（手動觸發）

1. **在 Stripe Dashboard 手動創建發票**:
   - 前往用戶的訂閱頁面
   - 點擊「Send test invoice」

2. **驗證 Webhook**:
   - 查看 Firebase Functions 日誌
   - 應該看到 `invoice.payment_succeeded` 事件
   - Credits 應該重置為 100（或 1200）

3. **驗證 Firestore**:
   - `credits`: 100（月付）或 1200（年付）
   - `usageThisPeriod.totalPages`: 0
   - `usageThisPeriod.overagePages`: 0

---

## 🔍 監控和調試

### 查看 Firebase Functions 日誌

```bash
# 實時日誌
firebase functions:log --only stripeWebhook

# 查看特定函數
firebase functions:log --only deductCreditsClient

# 查看所有日誌
firebase functions:log
```

### Stripe Webhook 日誌

https://dashboard.stripe.com/webhooks/we_xxx/logs

---

## ⚠️ 常見問題

### Q1: Webhook 沒有觸發？

**檢查**:
1. Webhook URL 是否正確
2. Webhook Secret 是否已配置
3. 查看 Stripe Dashboard > Webhooks > 日誌

**解決**:
```bash
# 重新配置並部署
firebase functions:config:set stripe.webhook_secret="whsec_..."
firebase deploy --only functions:stripeWebhook
```

---

### Q2: Credits 扣除失敗？

**檢查 Console Log**:
```javascript
// 前端 (firstproject.html)
console.log('💳 檢查 Credits:', window.creditsManager.currentCredits);

// Firebase Function 日誌
firebase functions:log --only deductCreditsClient
```

---

### Q3: 超額使用沒有報告到 Stripe？

**檢查**:
1. 用戶是否為 Pro Plan
2. 訂閱是否有超額計費項
3. Price ID 是否正確

**手動添加超額計費項**:
```bash
# 在 Stripe Dashboard 中
1. 前往訂閱頁面
2. 點擊「Add item」
3. 選擇超額計費 Price
```

---

## 📊 成本分析

### 每月 100 Credits + 超額 50 頁的用戶

| 項目 | 成本 |
|------|------|
| **月付訂閱** | HKD $38 |
| **超額 50 頁** | HKD $15 (50 × $0.3) |
| **總收入** | **HKD $53** |
| API 成本 | -$2.4 (150 頁 × $0.016) |
| Stripe 費用 | -$1.85 ($53 × 2.9% + $0.30) |
| **淨利潤** | **$48.75** (92%) |

---

## ✅ 完成檢查清單

- [ ] 環境變數已配置
- [ ] Firebase Functions 已部署
- [ ] Stripe Webhook 已設置
- [ ] Webhook Secret 已配置
- [ ] 超額計費項已添加到產品
- [ ] 基本訂閱流程測試通過
- [ ] Credits 扣除功能測試通過
- [ ] 超額使用報告測試通過
- [ ] Webhook 事件處理測試通過

---

## 🎉 恭喜！

超額計費功能已完全實現並部署！

**下一步**：
1. 監控生產環境運行
2. 收集用戶反饋
3. 優化使用體驗

---

**需要幫助？** 查看以下文檔：
- `OVERAGE_BILLING_ANALYSIS_2026-01-29.md` - 功能分析
- `ENV_SETUP_GUIDE.md` - 環境變數設置
- `BILLING_IMPLEMENTATION_GUIDE_2026-01-29.md` - 實現細節

