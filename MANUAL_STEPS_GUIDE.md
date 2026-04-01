# 🎯 手動完成步驟詳細指南
**日期**: 2026-01-29  
**預計時間**: 10 分鐘

---

## 📋 任務清單

- [ ] 任務 1: 驗證 Stripe Webhook（5 分鐘）
- [ ] 任務 2: 測試文件上傳（5 分鐘）

---

## 🔴 任務 1: 驗證 Stripe Webhook（5 分鐘）

### 步驟 1.1: 打開 Stripe Dashboard

**操作**:
1. 打開瀏覽器
2. 訪問：https://dashboard.stripe.com/webhooks
3. 登入您的 Stripe 帳號

### 步驟 1.2: 檢查現有 Webhook

**查找內容**:
- 尋找指向以下 URL 的端點：
  ```
  https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
  ```

**可能的情況**:

#### 🟢 情況 A: 找到了，但 URL 是舊的

**舊 URL 可能是**:
- `https://your-old-cloudflare-worker.workers.dev`
- 或其他 Firebase Function URL

**操作步驟**:
1. ✅ 點擊該 Webhook 端點
2. ✅ 點擊右上角的「⋮」（三個點）
3. ✅ 選擇「Update details」
4. ✅ 在「Endpoint URL」欄位中，更新為：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```
5. ✅ 滾動到「Events to send」部分
6. ✅ 確保選中以下 6 個事件：
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`
7. ✅ 點擊「Update endpoint」保存

**截圖位置**: 
- 更新前：截圖保存為 `webhook-before.png`
- 更新後：截圖保存為 `webhook-after.png`

#### 🟡 情況 B: 找到了，URL 已經正確

**操作步驟**:
1. ✅ 點擊該 Webhook 端點
2. ✅ 驗證「Endpoint URL」為：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```
3. ✅ 驗證「Events to send」包含上述 6 個事件
4. ✅ 如果都正確，跳到「步驟 1.3: 發送測試事件」

#### 🔴 情況 C: 沒有找到任何 Webhook

**操作步驟**:
1. ✅ 點擊右上角的「+ Add endpoint」按鈕
2. ✅ 在「Endpoint URL」中填入：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```
3. ✅ 在「Description」中填入：
   ```
   VaultCaddy Production - Subscription & Overage Billing
   ```
4. ✅ 在「Events to send」中，點擊「Select events」
5. ✅ 搜尋並選擇以下 6 個事件：
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`
6. ✅ 點擊「Add endpoint」保存

### 步驟 1.3: 發送測試事件

**操作步驟**:
1. ✅ 在 Webhook 詳情頁面（點擊剛才的端點進入）
2. ✅ 滾動到「Send test webhook」部分
3. ✅ 點擊「Send test webhook」按鈕
4. ✅ 在彈出的對話框中：
   - 選擇「Event type」：`invoice.payment_succeeded`
   - 點擊「Send test webhook」
5. ✅ 查看響應

**預期結果**:

✅ **成功標誌**:
```
Response: 200 OK
Body: {"received":true}
```

❌ **失敗標誌**:
```
Response: 400 Bad Request
或
Response: 500 Internal Server Error
```

**如果失敗**:
1. 檢查 Firebase Functions 日誌
2. 訪問：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs
3. 篩選：`stripeWebhook`
4. 查看錯誤訊息

### 步驟 1.4: 檢查 Firebase 日誌（驗證）

**操作步驟**:
1. ✅ 打開新分頁
2. ✅ 訪問：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs
3. ✅ 在「Filter」中輸入：`stripeWebhook`
4. ✅ 查看最新的日誌條目

**預期日誌內容**:
```
🔗 Stripe Webhook 收到請求
✅ Stripe 事件已接收: invoice.payment_succeeded
ℹ️ 非訂閱發票，跳過
```

或者（如果有用戶 ID）:
```
🔗 Stripe Webhook 收到請求
✅ Stripe 事件已接收: invoice.payment_succeeded
💰 續費成功: userId=xxx
✅ Credits 已重置: 100
```

### 📸 截圖清單（任務 1）

請截圖以下內容並保存：
- [ ] Stripe Webhook 列表頁面
- [ ] Webhook 詳情頁面（顯示 URL 和事件）
- [ ] 測試事件響應
- [ ] Firebase 日誌（顯示事件接收）

---

## 🟢 任務 2: 測試文件上傳（5 分鐘）

### 步驟 2.1: 準備測試文件

**選項 A: 使用現有文件**
- 找一個 5 頁左右的 PDF 文件
- 最好是銀行對賬單或收據

**選項 B: 創建測試文件**（如果沒有）
- 可以使用之前測試過的文件
- 或者從 Stripe 導出測試發票 PDF

### 步驟 2.2: 打開 VaultCaddy 網站

**操作步驟**:
1. ✅ 打開瀏覽器
2. ✅ 訪問：https://vaultcaddy.com
3. ✅ 登入您的帳號

### 步驟 2.3: 檢查當前 Credits

**操作步驟**:
1. ✅ 在頂部導航欄查看 Credits 餘額
2. ✅ 記錄當前 Credits 數量：______

**範例**:
- 當前 Credits: 95

### 步驟 2.4: 上傳文件

**操作步驟**:
1. ✅ 點擊「Upload」或「上傳文件」按鈕
2. ✅ 選擇準備好的 PDF 文件（5 頁）
3. ✅ 點擊「開始處理」或「Process」

### 步驟 2.5: 觀察處理過程

**預期行為**:

**階段 1: 上傳和分析（5 秒）**
```
✅ 文件上傳中...
✅ 分析文件結構...
✅ 檢測到 5 頁
✅ 檢查 Credits...
```

**階段 2: 處理（~50 秒）**
```
⏳ 處理第 1 批（第 1-5 頁）...
⏳ 使用 AI 提取數據...
```

**階段 3: 完成（5 秒）**
```
✅ 數據提取完成
✅ 保存到數據庫
✅ Credits 已扣除: -5
```

### 步驟 2.6: 驗證結果

**檢查項目**:

1. ✅ **Credits 扣除正確**
   - 上傳前：95
   - 上傳後：90
   - 差異：5 ✅

2. ✅ **數據提取正確**
   - 查看提取的交易記錄
   - 驗證帳戶信息
   - 檢查金額和日期

3. ✅ **處理時間合理**
   - 5 頁文件：預期 40-60 秒
   - 如果超過 2 分鐘，可能有問題

### 步驟 2.7: 檢查 Firebase 日誌（可選）

**操作步驟**:
1. ✅ 訪問：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs
2. ✅ 篩選：`qwenProxy`
3. ✅ 查看處理日誌

**預期日誌**:
```
📥 收到 Qwen API 請求
📊 處理 5 張圖片
⏱️  批次處理耗時: 45123ms
✅ API 請求成功
📤 返回數據
```

### 步驟 2.8: 測試超額計費（可選，需要更多 Credits）

**如果您想測試超額計費**:

**操作步驟**:
1. ✅ 確認當前 Credits < 100
2. ✅ 上傳一個大文件（例如 120 頁）
3. ✅ 預期結果：
   - Credits 變為負數（例如：-20）
   - Firestore 中 `usageThisPeriod.overagePages` = 20
4. ✅ 檢查 Stripe Dashboard：
   - 訪問：https://dashboard.stripe.com/test/subscriptions
   - 找到您的訂閱
   - 點擊「Usage」標籤
   - 應該看到 20 頁的使用記錄

### 📸 截圖清單（任務 2）

請截圖以下內容並保存：
- [ ] 上傳前的 Credits 餘額
- [ ] 文件處理過程
- [ ] 處理完成畫面
- [ ] 上傳後的 Credits 餘額
- [ ] 提取的數據詳情
- [ ] Firebase 日誌（qwenProxy）

---

## ✅ 完成檢查清單

### 任務 1: Stripe Webhook
- [ ] Webhook URL 已更新/創建
- [ ] 6 個事件已配置
- [ ] 測試事件返回 200
- [ ] Firebase 日誌顯示事件接收

### 任務 2: 文件上傳
- [ ] 文件上傳成功
- [ ] 處理時間合理（~10 秒/頁）
- [ ] Credits 扣除正確
- [ ] 數據提取準確

---

## 🚨 常見問題

### Q1: Webhook 測試失敗（400 錯誤）

**可能原因**:
- Webhook Secret 不匹配
- Firebase Function 代碼錯誤

**解決方法**:
1. 檢查 Firebase 日誌
2. 確認 `stripe.webhook_secret` 配置正確
3. 重新部署：`firebase deploy --only functions`

### Q2: 文件處理超時

**可能原因**:
- Firebase Function 未部署成功
- Qwen API Key 無效
- 網絡問題

**解決方法**:
1. 檢查 Firebase Functions 狀態
2. 查看 qwenProxy 日誌
3. 驗證 API Key

### Q3: Credits 沒有扣除

**可能原因**:
- deductCreditsClient 函數錯誤
- Firestore 權限問題

**解決方法**:
1. 檢查 Firebase 日誌
2. 查看 deductCreditsClient 調用記錄
3. 驗證 Firestore 規則

### Q4: 超額沒有記錄到 Stripe

**可能原因**:
- Stripe API Key 無效
- Subscription Item 未創建

**解決方法**:
1. 檢查 Firebase 日誌中的 Stripe API 調用
2. 在 Stripe Dashboard 中手動檢查訂閱
3. 驗證訂閱有超額計費項目

---

## 📞 需要幫助？

如果遇到問題：

1. **查看日誌**:
   - Firebase: https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs
   - Stripe: https://dashboard.stripe.com/logs

2. **檢查狀態**:
   - Firebase Functions: https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions
   - Stripe Webhooks: https://dashboard.stripe.com/webhooks

3. **查看文檔**:
   - `DEPLOYMENT_SUCCESS_2026-01-29.md`
   - `OVERAGE_BILLING_FLOW.md`
   - `WEBHOOK_VERIFICATION_STEPS.md`

---

## 🎉 完成後

**恭喜！您已完成所有部署和測試！**

您的 VaultCaddy 系統現在已完全啟用：
- ✅ 文件處理功能正常
- ✅ Credits 自動扣除
- ✅ 超額自動計費
- ✅ 訂閱自動續費
- ✅ Webhook 事件處理

**享受您的全自動計費系統！** 🚀


