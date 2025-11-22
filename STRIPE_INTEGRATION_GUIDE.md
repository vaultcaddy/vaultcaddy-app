# 🔌 Stripe 訂閱整合指南

**本文檔作用**：說明如何配置和使用 VaultCaddy 的 Stripe 訂閱功能，包括基於使用量的計費系統。幫助 AI 和開發者快速理解 Stripe 整合架構。

**更新日期**：2025-11-22

---

## 📋 概覽

VaultCaddy 使用 Stripe 實現以下計費模式：
1. **固定訂閱費用**：月費/年費
2. **包含免費額度**：每月 100 Credits 或每年 1,200 Credits
3. **使用量計費**：超出免費額度後，每頁 HKD $0.5

---

## 🎯 定價方案

### 月費方案
- **Stripe 產品 ID**：`prod_TSmKnHeaQVxZXC`
- **價格**：HKD $78/月
- **包含**：100 Credits（100 頁）
- **超出計費**：HKD $0.5/頁

### 年費方案
- **Stripe 產品 ID**：`prod_TSsEWI5bv9pSkz`
- **價格**：HKD $744/年（平均 $62/月）
- **包含**：1,200 Credits（1,200 頁）
- **超出計費**：HKD $0.5/頁

---

## 🏗️ 系統架構

```
用戶使用 VaultCaddy
       ↓
每處理 1 頁文件 = 消耗 1 Credit
       ↓
前端 (stripe-manager.js) 計算超出頁數
       ↓
呼叫 Cloud Function: reportStripeUsage()
       ↓
後端報告使用量給 Stripe
       ↓
Stripe 自動計費並在月底收費
```

---

## 📁 相關文件

### 1. 前端文件

#### `index.html` - 首頁
- **客戶評價區域**：6 張評價卡片（BankGPT 風格）
- **功能展示**：保留原有的功能一和功能二設計

#### `billing.html` - 計費頁面
- **訂閱方案展示**：月費和年費並列顯示
- **訂閱按鈕**：調用 `subscribeToPlan(planType)`
- **產品映射**：連接到實際的 Stripe 產品 ID

#### `stripe-manager.js` - Stripe 管理器
- **產品配置**：
  ```javascript
  subscriptions: {
    monthly: {
      productId: 'prod_TSmKnHeaQVxZXC',
      price: 78,
      credits: 100,
      period: 'monthly',
      overage: 0.5
    },
    yearly: {
      productId: 'prod_TSsEWI5bv9pSkz',
      price: 744,
      credits: 1200,
      period: 'yearly',
      overage: 0.5
    }
  }
  ```
- **關鍵方法**：
  - `subscribeToPlan(planKey)` - 處理訂閱流程
  - `trackUsageMetered(pagesUsed, subscriptionId)` - 追蹤使用量
  - `calculateOverage(totalPagesUsed, includedCredits)` - 計算超出頁數
  - `handlePaymentSuccess()` - 處理支付成功回調

### 2. 後端文件

#### `firebase-functions/index.js` - Cloud Functions
- **reportStripeUsage()** - 手動報告使用量
  - **觸發方式**：前端 HTTPS Callable
  - **功能**：報告超出的頁數給 Stripe
  - **參數**：
    ```javascript
    {
      subscriptionId: string,  // Stripe 訂閱 ID
      quantity: number,         // 超出的頁數
      timestamp: number         // 時間戳（可選）
    }
    ```
  - **返回**：
    ```javascript
    {
      success: boolean,
      usageRecordId: string,
      quantity: number
    }
    ```

- **reportDailyUsage()** - 定時任務
  - **執行時間**：每天午夜（Hong Kong 時區）
  - **功能**：
    1. 遍歷所有活躍訂閱用戶
    2. 計算當月總使用量
    3. 計算超出免費額度的頁數
    4. 報告給 Stripe
  - **Firestore 查詢**：
    ```javascript
    db.collection('users')
      .where('subscriptionStatus', '==', 'active')
      .get()
    ```

---

## 🔧 配置步驟

### 1. Stripe Dashboard 配置

#### 步驟 1：創建產品（已完成）
- 月費產品：`prod_TSmKnHeaQVxZXC`
- 年費產品：`prod_TSsEWI5bv9pSkz`

#### 步驟 2：為每個產品添加價格
1. **固定訂閱價格**
   - 月費：HKD $78/月
   - 年費：HKD $744/年

2. **使用量計費價格**
   - 計費模式：`Metered Billing`（基於使用量）
   - 定價模型：`Graduated Pricing`（階梯定價）
   - 階梯設置：
     ```
     第 1 層：0-100 頁 → HKD $0/頁
     第 2 層：101+ 頁 → HKD $0.5/頁
     ```
   - 或使用 `Volume Pricing`（每層定價）

#### 步驟 3：創建 Payment Links（待完成）
```bash
# 月費 Payment Link
https://buy.stripe.com/test_YOUR_MONTHLY_LINK

# 年費 Payment Link
https://buy.stripe.com/test_YOUR_YEARLY_LINK
```

**更新位置**：
- `stripe-manager.js` 第 40 行和第 48 行

### 2. Firebase 配置

#### 步驟 1：設置 Stripe API 密鑰
```bash
firebase functions:config:set stripe.secret_key="sk_test_YOUR_SECRET_KEY"
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_WEBHOOK_SECRET"
```

#### 步驟 2：配置 Webhook
1. 在 Stripe Dashboard 創建 Webhook
2. URL：`https://YOUR_PROJECT.cloudfunctions.net/stripeWebhook`
3. 監聽事件：
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`

#### 步驟 3：部署 Cloud Functions
```bash
cd firebase-functions
npm install
firebase deploy --only functions
```

---

## 🧪 測試流程

### 1. 測試訂閱流程
```javascript
// 前端調用
subscribeToPlan('monthly');

// 預期行為：
// 1. 跳轉到 Stripe Checkout
// 2. 完成支付
// 3. 返回並顯示成功通知
// 4. Credits 自動添加到用戶帳戶
```

### 2. 測試使用量計費
```javascript
// 模擬用戶處理 120 頁文件（超出 20 頁）
const overage = StripeManager.calculateOverage(120, 100);
console.log(overage);  // 輸出: 20

// 報告使用量
await StripeManager.trackUsageMetered(20, 'sub_xxxxx');

// 預期行為：
// 1. 呼叫 Cloud Function
// 2. 記錄到 Firestore
// 3. 報告給 Stripe
// 4. 月底自動計費 HKD $10（20 頁 × $0.5）
```

### 3. 測試定時任務
```bash
# 手動觸發定時任務（測試環境）
firebase functions:shell
> reportDailyUsage()

# 檢查日誌
firebase functions:log --only reportDailyUsage
```

---

## 📊 數據庫架構

### Firestore 集合結構

#### `users` 集合
```javascript
{
  uid: string,
  credits: number,
  subscriptionStatus: 'active' | 'inactive' | 'cancelled',
  subscriptionPlan: 'monthly' | 'yearly',
  stripeSubscriptionId: string,
  stripeCustomerId: string,
  updatedAt: Timestamp
}
```

#### `users/{userId}/creditsHistory` 子集合
```javascript
{
  type: 'add' | 'deduct',
  amount: number,
  before: number,
  after: number,
  metadata: {
    source: 'purchase' | 'subscription' | 'usage',
    ...
  },
  createdAt: Timestamp
}
```

#### `usageRecords` 集合
```javascript
{
  userId: string,
  subscriptionId: string,
  subscriptionItemId: string,
  quantity: number,
  stripeUsageRecordId: string,
  timestamp: Timestamp
}
```

---

## 🐛 常見問題

### Q1: Payment Link 無法跳轉？
**A:** 確認 `stripe-manager.js` 中的 `paymentLink` 已更新為實際的 Stripe Payment Link。

### Q2: 使用量未報告給 Stripe？
**A:** 檢查：
1. Cloud Function 是否已部署
2. Stripe API 密鑰是否正確
3. 訂閱是否包含使用量計費項目
4. 查看 Cloud Functions 日誌

### Q3: 定時任務未執行？
**A:** 
1. 確認 Cloud Scheduler 已啟用
2. 檢查時區設置（Asia/Hong_Kong）
3. 查看執行日誌：`firebase functions:log --only reportDailyUsage`

### Q4: Credits 未自動添加？
**A:**
1. 檢查 Webhook 配置
2. 確認 `client_reference_id` 或 `metadata.userId` 已設置
3. 查看 `stripeWebhook` 日誌

---

## 🔒 安全考慮

1. **Webhook 簽名驗證**：所有 Webhook 請求必須通過 Stripe 簽名驗證
2. **API 密鑰保護**：使用 Firebase Functions Config 存儲，不提交到 Git
3. **用戶身份驗證**：所有 Cloud Functions 都需要 Firebase Auth
4. **事務處理**：使用 Firestore Transactions 確保數據一致性
5. **錯誤處理**：完整的 try-catch 和日誌記錄

---

## 📈 監控和維護

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
```javascript
// 查詢當月使用量記錄
db.collection('usageRecords')
  .where('timestamp', '>=', monthStart)
  .get();

// 查詢用戶 Credits 歷史
db.collection('users')
  .doc(userId)
  .collection('creditsHistory')
  .orderBy('createdAt', 'desc')
  .limit(50)
  .get();
```

---

## 🚀 下一步建議

1. **創建 Stripe Payment Links**
   - 為月費和年費產品創建實際的 Payment Links
   - 更新 `stripe-manager.js` 中的 URL

2. **測試完整流程**
   - 使用 Stripe Test Mode 進行端到端測試
   - 驗證 Credits 自動添加
   - 驗證使用量計費

3. **設置監控和警報**
   - 配置 Firebase 性能監控
   - 設置 Stripe Webhook 失敗警報
   - 監控 Cloud Functions 執行時間和錯誤率

4. **優化用戶體驗**
   - 添加訂閱管理頁面（查看、升級、取消）
   - 顯示當月使用量和預估費用
   - 提供使用量歷史圖表

5. **法律合規**
   - 添加訂閱條款和條件
   - 實施退款政策
   - 確保符合 PCI DSS 標準

---

**文檔維護者**：AI Assistant  
**最後更新**：2025-11-22  
**版本**：1.0

