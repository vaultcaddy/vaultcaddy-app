# 🔗 Stripe Webhook 設置指南
**日期**: 2026-01-29  
**用途**: 配置 Stripe Webhook 以接收訂閱和付款事件

---

## 📍 Webhook URL（已部署）

```
https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
```

---

## 🔧 設置步驟（5 分鐘）

### 步驟 1: 打開 Stripe Webhooks 頁面

訪問：https://dashboard.stripe.com/webhooks

### 步驟 2: 添加端點

1. 點擊 **「+ Add endpoint」** 按鈕
2. 在 **「Endpoint URL」** 中填入：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```
3. 在 **「Description」** 中填入：
   ```
   VaultCaddy Production - Subscription & Overage Billing
   ```

### 步驟 3: 選擇監聽事件

**選擇以下 6 個事件**（必須全選）：

#### 訂閱相關事件
- ✅ `customer.subscription.created` - 訂閱創建
- ✅ `customer.subscription.updated` - 訂閱更新
- ✅ `customer.subscription.deleted` - 訂閱取消

#### 支付相關事件
- ✅ `checkout.session.completed` - 訂閱成功
- ✅ `invoice.payment_succeeded` - 支付成功（含超額計費）
- ✅ `invoice.payment_failed` - 支付失敗

### 步驟 4: 選擇 API 版本

- **API version**: 使用最新版本（通常是默認選中）

### 步驟 5: 保存並獲取 Webhook Secret

1. 點擊 **「Add endpoint」** 保存
2. 保存後會顯示 **「Signing secret」**，格式為：`whsec_xxx...`
3. **複製這個 Secret**（下一步需要）

---

## 🔑 步驟 6: 設置 Webhook Secret（必須）

將剛才複製的 Webhook Secret 設置到 Firebase：

```bash
firebase functions:config:set stripe.webhook_secret="whsec_xxx..."
```

**⚠️ 重要**：設置後必須重新部署：

```bash
firebase deploy --only functions
```

---

## ✅ 驗證設置

### 測試 1: 發送測試事件

1. 在 Stripe Webhook 頁面，點擊您剛創建的端點
2. 點擊 **「Send test webhook」**
3. 選擇事件：`checkout.session.completed`
4. 點擊 **「Send test webhook」**

### 測試 2: 檢查響應

**成功標誌**：
- HTTP 狀態碼：`200`
- 響應內容：`{ received: true }`

**失敗標誌**：
- HTTP 狀態碼：`4xx` 或 `5xx`
- 需要檢查 Firebase Functions 日誌

### 測試 3: 查看日誌

訪問 Firebase Console：
https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs

應該看到：
```
✅ Stripe 事件已接收: checkout.session.completed
✅ 訂閱成功: userId=xxx, +100 Credits
```

---

## 🔍 故障排除

### 問題 1: Webhook 簽名驗證失敗

**錯誤訊息**：
```
Webhook signature verification failed
```

**解決方法**：
1. 確認 `stripe.webhook_secret` 設置正確
2. 重新部署：`firebase deploy --only functions`

### 問題 2: Webhook 收不到事件

**檢查清單**：
- ✅ URL 是否正確（包含 https://）
- ✅ 6 個事件是否全部選中
- ✅ 端點狀態是否為「Enabled」

### 問題 3: 函數超時

**查看日誌**：
```bash
firebase functions:log --only stripeWebhook
```

**可能原因**：
- Firestore 寫入緩慢
- Stripe API 調用失敗

---

## 📊 監控健康狀態

### Stripe Dashboard 監控

1. **Webhooks 頁面**：https://dashboard.stripe.com/webhooks
   - 查看成功/失敗率
   - 查看最近事件

2. **Events 頁面**：https://dashboard.stripe.com/events
   - 查看所有事件詳情
   - 手動重試失敗的事件

### Firebase Console 監控

1. **Functions 日誌**：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs
   - 查看實時日誌
   - 搜尋錯誤訊息

2. **Firestore 數據**：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore
   - 驗證用戶數據更新
   - 檢查 Credits 變化

---

## 🎯 完成檢查清單

- [ ] 添加 Webhook 端點
- [ ] 配置 6 個事件
- [ ] 複製 Webhook Secret
- [ ] 設置環境變數 `stripe.webhook_secret`
- [ ] 重新部署 Functions
- [ ] 發送測試事件
- [ ] 驗證日誌輸出
- [ ] 監控健康狀態

---

## 💡 下一步

完成 Webhook 設置後：

1. **測試訂閱流程**
   - 創建測試訂閱
   - 驗證 Credits 正確添加

2. **測試超額計費**
   - 上傳超過 100 頁的文件
   - 驗證超額記錄到 Stripe

3. **測試續費流程**
   - 等待計費日或手動觸發
   - 驗證 Credits 重置

---

**設置完成後，整個超額計費系統就完全啟用了！** 🎉


