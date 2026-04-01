# Webhook 當前狀態檢查
**時間**: 2026-01-29 19:07

## ✅ 已確認

- **Webhook 名稱**: vibrant-splendor
- **URL**: https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook ✅ 正確
- **狀態**: 使用中 ✅
- **事件數量**: 5 個 ⚠️ 需要 6 個

## 🔍 需要驗證的事件清單

請在 Stripe Dashboard 中確認以下事件是否全部配置：

### 必需的 6 個事件：

1. ✅ / ❌ `checkout.session.completed`
2. ✅ / ❌ `customer.subscription.created`
3. ✅ / ❌ `customer.subscription.updated`
4. ✅ / ❌ `customer.subscription.deleted`
5. ✅ / ❌ `invoice.payment_succeeded`
6. ✅ / ❌ `invoice.payment_failed`

## 📋 下一步操作

### 如果缺少事件：

1. 點擊右上角的「編輯接收端」按鈕
2. 滾動到「侦听事件」部分
3. 點擊「+ 添加事件」
4. 搜尋並添加缺失的事件
5. 點擊「更新端點」保存

### 如果事件完整：

直接進行測試！

## 🧪 測試步驟

### 方法 1: 在 Stripe Dashboard 發送測試事件

1. 在當前 Webhook 詳情頁面
2. 找到「發送測試 Webhook」按鈕（可能需要向下滾動）
3. 選擇事件類型：`invoice.payment_succeeded`
4. 點擊「發送測試 Webhook」
5. 查看響應狀態（應該是 200 OK）

### 方法 2: 使用命令行測試（已為您準備好）

執行以下命令測試 Webhook 連接：

```bash
node test-webhook-script.js
```

## ✅ 驗證成功標誌

### Stripe Dashboard 中：
- 響應狀態：200 OK
- 響應內容：`{"received":true}`

### Firebase Console 中：
訪問：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs

篩選：`stripeWebhook`

應該看到：
```
🔗 Stripe Webhook 收到請求
✅ Stripe 事件已接收: invoice.payment_succeeded
```

---

**完成事件配置和測試後，Webhook 設置就完成了！** ✅


