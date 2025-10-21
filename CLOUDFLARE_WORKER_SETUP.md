# Cloudflare Worker 設置指南

## 📋 總覽

這個指南將幫助你設置 Cloudflare Worker 來代理 Gemini API，解決 CORS 問題。

**預計時間**：10-15 分鐘  
**成本**：完全免費

---

## 🚀 步驟 1：註冊 Cloudflare 帳戶

1. 訪問：https://dash.cloudflare.com/sign-up
2. 輸入你的電子郵件和密碼
3. 驗證電子郵件
4. 登入 Cloudflare Dashboard

**注意**：如果你已有 Cloudflare 帳戶，直接登入即可。

---

## 🔧 步驟 2：創建 Worker

### 2.1 進入 Workers 頁面

1. 登入後，點擊左側菜單的 **"Workers & Pages"**
2. 點擊 **"Create application"** 按鈕
3. 選擇 **"Create Worker"**

### 2.2 配置 Worker

1. **Worker 名稱**：輸入 `gemini-proxy`（或任何你喜歡的名稱）
2. 點擊 **"Deploy"** 按鈕（先用默認代碼部署）

### 2.3 編輯 Worker 代碼

1. 部署完成後，點擊 **"Edit code"** 按鈕
2. **刪除所有默認代碼**
3. **複製粘貼** `cloudflare-worker-gemini.js` 文件中的所有代碼
4. 點擊右上角的 **"Save and Deploy"** 按鈕

---

## 🔑 步驟 3：記錄 Worker URL

部署完成後，你會看到類似這樣的 URL：

```
https://gemini-proxy.你的用戶名.workers.dev
```

**請記錄這個 URL，稍後需要在網站中使用！**

---

## ✅ 步驟 4：測試 Worker

### 4.1 使用 curl 測試（可選）

```bash
curl -X POST https://gemini-proxy.你的用戶名.workers.dev \
  -H "Content-Type: application/json" \
  -H "Origin: https://vaultcaddy.com" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Hello, this is a test!"
      }]
    }]
  }'
```

### 4.2 檢查響應

如果設置正確，你應該會收到 Gemini API 的響應（JSON 格式）。

---

## 🔒 步驟 5：更新 API Key（重要！）

**為了安全**，你應該：

1. 訪問：https://aistudio.google.com/app/apikey
2. 創建一個**新的** Gemini API Key
3. 在 Worker 代碼中，將第 8 行的 API Key 替換為新的：

```javascript
const GEMINI_API_KEY = '你的新API_KEY'; // 替換這裡
```

4. 點擊 **"Save and Deploy"**

---

## 📝 步驟 6：更新網站代碼

完成 Worker 設置後，我會幫你更新 `firstproject.html` 和相關文件，將 Gemini API 調用改為通過 Worker。

---

## 🎯 下一步

完成上述步驟後，請告訴我：

1. ✅ Worker 已創建並部署
2. 📝 Worker URL 是：`https://gemini-proxy.你的用戶名.workers.dev`
3. 🔑 已更新 API Key

然後我會立即更新你的網站代碼！

---

## 🆘 常見問題

### Q1: 為什麼需要 Worker？
A: Google Gemini API 不支持從瀏覽器直接調用（CORS 限制）。Worker 作為中間代理，繞過這個限制。

### Q2: Worker 安全嗎？
A: 是的！Worker 只接受來自 `vaultcaddy.com` 的請求，並且 API Key 存儲在 Cloudflare 的服務器上，不會暴露給用戶。

### Q3: 成本如何？
A: 完全免費！Cloudflare Workers 免費計劃提供每天 10萬次請求，足夠使用。

### Q4: 如果超過免費配額怎麼辦？
A: 可以升級到 Workers Paid 計劃（$5/月），獲得每月 1000萬次請求。

---

## 📧 需要幫助？

如果遇到任何問題，請告訴我：
- 具體的錯誤信息
- 你進行到哪一步
- Worker URL

我會立即幫你解決！🚀

