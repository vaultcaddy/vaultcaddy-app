# ✅ Webhook 驗證步驟
**日期**: 2026-01-29  
**狀態**: Webhook Secret 已配置

---

## 📍 當前配置

### Firebase Function URL（新部署）
```
https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
```

### Webhook Secret（已配置）
```
whsec_MNrldnhxEM8HC0HZJ4OT1V44ywoMCLit
```

---

## 🔍 需要驗證的事項

### ✅ 步驟 1: 檢查 Stripe Dashboard 中的 Webhook URL

1. **訪問**: https://dashboard.stripe.com/webhooks
2. **查找**: VaultCaddy 相關的 Webhook 端點
3. **驗證**: URL 是否為：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```

### 🔄 如果 URL 不匹配

**情況 A: URL 不同（例如舊的 URL）**

**解決方法**：
1. 點擊該端點
2. 點擊右上角的 **「⋮」** → **「Update details」**
3. 更新 **「Endpoint URL」** 為：
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```
4. 保存

**情況 B: 沒有找到任何 Webhook 端點**

**解決方法**：按照 `STRIPE_WEBHOOK_SETUP_GUIDE.md` 創建新端點

---

## ✅ 步驟 2: 驗證監聽事件（必須包含以下 6 個）

在 Webhook 詳情頁面，確認已選中：

- ✅ `checkout.session.completed`
- ✅ `customer.subscription.created`
- ✅ `customer.subscription.updated`
- ✅ `customer.subscription.deleted`
- ✅ `invoice.payment_succeeded`
- ✅ `invoice.payment_failed`

**如果缺少任何事件**：
1. 點擊 **「⋮」** → **「Update details」**
2. 在 **「Events to send」** 中添加缺少的事件
3. 保存

---

## ✅ 步驟 3: 發送測試事件

1. 在 Webhook 詳情頁面，點擊 **「Send test webhook」**
2. 選擇事件：`invoice.payment_succeeded`
3. 點擊 **「Send test webhook」**

### 預期結果

**成功響應**：
```json
{
  "received": true
}
```

**HTTP 狀態碼**: `200`

---

## ✅ 步驟 4: 檢查 Firebase 日誌

1. **訪問**: https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs

2. **篩選**: `stripeWebhook`

3. **預期日誌**：
```
🔗 Stripe Webhook 收到請求
✅ Stripe 事件已接收: invoice.payment_succeeded
ℹ️ 非訂閱發票，跳過（測試事件通常沒有關聯訂閱）
```

---

## 🎯 完成檢查清單

- [ ] Webhook URL 指向新的 Firebase Function
- [ ] 6 個事件全部配置
- [ ] Webhook Secret 已設置（✅ 已完成）
- [ ] 測試事件返回 200
- [ ] Firebase 日誌顯示事件接收

---

## 🚀 下一步：測試完整流程

### 測試 1: 訂閱流程（10 分鐘）

**使用測試模式**：
1. 切換到 Stripe Test Mode
2. 創建測試訂閱（使用測試卡號：4242 4242 4242 4242）
3. 驗證 Firestore 中用戶 Credits 增加

**驗證點**：
- ✅ `checkout.session.completed` 事件觸發
- ✅ Firestore 中 `credits` 增加 100
- ✅ `planType` 更新為 "Pro Plan"

### 測試 2: 超額計費流程（15 分鐘）

**步驟**：
1. 上傳超過 100 頁的文件（例如 120 頁）
2. 檢查 Firestore：`credits` 應為 -20
3. 檢查 Stripe Usage Records

**驗證點**：
- ✅ Credits 變為負數
- ✅ Stripe 記錄 20 頁超額使用
- ✅ `usageThisPeriod.overagePages` = 20

### 測試 3: 續費流程（手動觸發）

**在 Stripe Dashboard**：
1. 找到測試訂閱
2. 點擊 **「⋮」** → **「Create invoice」**
3. 添加訂閱項目
4. 發送發票

**驗證點**：
- ✅ `invoice.payment_succeeded` 事件觸發
- ✅ Credits 重置為 100（月付）或保持不變（年付月度）
- ✅ `usageThisPeriod` 清零

---

## 📊 監控建議

### 每日檢查（生產環境）

1. **Webhook 健康狀態**
   - 訪問：https://dashboard.stripe.com/webhooks
   - 查看成功率（應 > 95%）

2. **失敗事件重試**
   - 訪問：https://dashboard.stripe.com/events
   - 篩選失敗事件
   - 手動重試

3. **Firebase 日誌**
   - 搜尋 "error" 或 "failed"
   - 修復問題後重新部署

---

**完成所有驗證後，系統就完全就緒了！** 🎉


