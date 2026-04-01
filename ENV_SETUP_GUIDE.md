# 🔐 環境變數設置指南
**用途**: 安全地管理 API Keys，避免洩露到 Git 倉庫

---

## ⚠️ 重要安全提醒

**絕對不要**將以下敏感信息提交到 Git:
- ❌ Stripe Secret Key (sk_live_...)
- ❌ Qwen API Key (sk-...)
- ❌ Firebase Service Account Keys
- ❌ 任何其他 API Keys 或密碼

---

## 🔧 Firebase Functions 環境變數設置

### 方法 1: 使用 Firebase CLI（推薦）

```bash
# 設置 Stripe API Key
firebase functions:config:set stripe.secret="YOUR_STRIPE_SECRET_KEY_HERE"

# 設置 Qwen API Key
firebase functions:config:set qwen.api_key="YOUR_QWEN_API_KEY_HERE"

# 設置 Stripe Webhook Secret（稍後配置）
firebase functions:config:set stripe.webhook_secret="YOUR_WEBHOOK_SECRET_HERE"

# 查看所有配置
firebase functions:config:get

# 部署後配置生效
firebase deploy --only functions
```

### 方法 2: 使用 .env 文件（本地測試）

創建 `firebase-functions/.env`:

```env
STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY_HERE
QWEN_API_KEY=YOUR_QWEN_API_KEY_HERE
STRIPE_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE
```

⚠️ **重要**: 確保 `.env` 在 `.gitignore` 中（已配置）

---

## 📍 如何獲取 API Keys

### 1️⃣ Stripe Secret Key

1. 前往 https://dashboard.stripe.com/apikeys
2. 選擇「Standard keys」標籤
3. 複製 **Secret key**（以 `sk_live_` 或 `sk_test_` 開頭）
4. ⚠️ 生產環境使用 `sk_live_`，測試環境使用 `sk_test_`

### 2️⃣ Qwen API Key

1. 前往 https://bailian.console.aliyun.com/
2. 進入「API Key 管理」
3. 創建新的 API Key（選擇新加坡地域）
4. 複製 API Key（以 `sk-` 開頭）

### 3️⃣ Stripe Webhook Secret（稍後配置）

1. 部署 Firebase Function 後獲取 URL
2. 在 Stripe Dashboard 添加 Webhook
3. 複製 Webhook signing secret（以 `whsec_` 開頭）

---

## ✅ 驗證配置

```bash
# 查看 Firebase Functions 配置
firebase functions:config:get

# 預期輸出：
# {
#   "stripe": {
#     "secret": "sk_live_...",
#     "webhook_secret": "whsec_..."
#   },
#   "qwen": {
#     "api_key": "sk-..."
#   }
# }
```

---

## 🚀 下一步

配置完成後：
1. ✅ 部署 Firebase Functions
2. ✅ 設置 Stripe Webhook
3. ✅ 測試完整支付流程

**現在可以安全地提交代碼到 Git！**

