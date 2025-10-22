# 🚀 立即部署 Cloudflare Worker

## ✅ 前端代碼已更新

我已經完成了以下更新：

### 1. **`google-smart-processor.js`** ✅
```javascript
geminiAI: window.geminiWorkerClient  // ✅ 使用 Cloudflare Worker 代理
```

### 2. **`firstproject.html`** ✅
```javascript
// 初始化 Gemini Worker Client
const geminiClient = new GeminiWorkerClient(
    'https://gemini-proxy.vaultcaddy.workers.dev/v1beta/models/gemini-1.5-flash-latest:generateContent'
);
window.geminiWorkerClient = geminiClient;
```

---

## 🔧 需要部署 Worker 代碼

當前 Worker 還在返回 "Hello World!"，需要部署我們寫的 `cloudflare-worker-gemini.js`。

### **選項 A：手動部署（推薦）** ⭐

1. **打開 Cloudflare Dashboard**
   - https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production

2. **複製 Worker 代碼**
   - 打開本地文件 `cloudflare-worker-gemini.js`
   - 全選並複製代碼

3. **粘貼到 Cloudflare**
   - 在 Cloudflare Worker 編輯器中，刪除所有現有代碼
   - 粘貼 `cloudflare-worker-gemini.js` 的內容

4. **點擊 "Deploy" 按鈕**

### **選項 B：使用 Wrangler CLI**

```bash
# 安裝 Wrangler
npm install -g wrangler

# 登入 Cloudflare
wrangler login

# 部署 Worker
wrangler deploy cloudflare-worker-gemini.js --name gemini-proxy
```

---

## 🧪 測試 Worker

部署後，訪問：
```
https://gemini-proxy.vaultcaddy.workers.dev
```

應該看到：
```
Method Not Allowed
```

這是正常的，因為 Worker 只接受 POST 請求。

---

## ✅ 完成後

1. 刷新 `https://vaultcaddy.com/firstproject.html`
2. 上傳一張發票圖片
3. 檢查控制台，應該看到：
   ```
   🤖 初始化 Gemini Worker Client...
   ✅ Gemini Worker Client 已初始化
   🚀 開始處理文檔: xxx.jpg (invoice)
   ```

準確率應該達到 **95%+**！🎉
