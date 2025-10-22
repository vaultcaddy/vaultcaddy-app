# ⚠️ **緊急修復：Gemini API 403 錯誤**

## 📌 **問題診斷**

從錯誤日誌可以清楚看到：

```
Failed to load gemini-proxy.vaultcaddy.workers.dev
server responded with a status of 403

{"error":"Gemini API 錯誤","status":403,"details":{"error":
{"code":403,"message":"Requests from referer <empty> are blocked."}}}
```

**根本原因**：你的 Gemini API Key 設置了 **HTTP Referrer 限制**，阻擋了來自 Cloudflare Worker 的請求。

---

## 🛠️ **手動修復步驟**

### **Option 1: 移除 API Key 的 Referer 限制（最簡單）** ⭐

1. **訪問 Google Cloud Console**
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **切換到正確的項目**
   - 點擊頂部的 "My First Project"
   - 確保你在包含 API Key `AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug` 的項目中

3. **找到並編輯 API Key**
   - 在 "API 金鑰" 列表中找到你的 API Key
   - 點擊 API Key 名稱進入編輯頁面

4. **修改應用限制**
   - 找到 "**Application restrictions**"（應用限制）部分
   - 選擇 "**None**"（無）
   - 點擊 "**Save**"（保存）

5. **等待設置生效**
   - 通常需要 **5-10 分鐘**

---

### **Option 2: 添加允許的 Referrers**

如果你想保留一些限制，可以添加允許的域名：

1. 在 "**Application restrictions**" 中選擇 "**HTTP referrers (web sites)**"
2. 添加以下 referrers：
   ```
   https://vaultcaddy.com/*
   https://*.vaultcaddy.workers.dev/*
   http://localhost/*
   http://127.0.0.1/*
   ```
3. 點擊 "**Save**"

---

### **Option 3: 創建新的無限制 API Key**

1. 訪問 Google AI Studio：
   ```
   https://aistudio.google.com/app/apikey
   ```
2. 點擊 "**Create API Key**"
3. 選擇項目
4. **不要設置任何限制**
5. 複製新的 API Key
6. 更新 `cloudflare-worker-gemini.js` 中的 `GEMINI_API_KEY`

---

## 🔄 **重新部署 Cloudflare Worker**

我已經更新了 Worker 代碼，添加了 `Referer` 頭。請重新部署：

1. **打開 Cloudflare Dashboard**
   ```
   https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production
   ```

2. **複製本地文件內容**
   - 打開 `cloudflare-worker-gemini.js`
   - 全選並複製

3. **粘貼並部署**
   - 在 Cloudflare 編輯器中，刪除所有現有代碼
   - 粘貼新代碼
   - 點擊 "**Deploy**" 按鈕

---

## ✅ **驗證修復**

完成上述步驟後：

1. **清除瀏覽器緩存**（重要！）
   - Chrome: Ctrl+Shift+Delete
   - Safari: Cmd+Option+E

2. **訪問測試頁面**
   ```
   https://vaultcaddy.com/firstproject.html
   ```

3. **上傳測試發票**
   - 點擊 "Upload files"
   - 選擇之前的發票圖片
   - 觀察控制台

4. **預期結果**
   ```
   ✅ geminiAI 處理成功
      耗時: ~3500ms
   📋 發票號碼: FI25093602  ✅
   📋 商品明細: 2 個  ✅
   📋 總金額: $1250.00  ✅
   ```

---

## ❓ **常見問題**

### **Q: 我找不到 API Key 在哪個項目中？**

**A**: 嘗試以下方法：

1. 點擊頂部項目選擇器
2. 查看所有項目列表
3. 逐一切換項目，在每個項目中查看 "憑證" 頁面
4. 尋找 API Key 列表

### **Q: 修改後仍然 403？**

**A**: 可能原因：

1. **設置未生效**：等待 5-10 分鐘
2. **Worker 未重新部署**：確保 Cloudflare Worker 已更新
3. **API Key 錯誤**：確認 Worker 中的 API Key 是否正確

### **Q: 完全找不到 API Key？**

**A**: 該 API Key 可能已被刪除，建議創建新的 API Key（Option 3）。

---

## 📝 **下一步**

完成修復後，請：

1. ✅ 清除瀏覽器緩存
2. ✅ 測試上傳發票
3. ✅ 提供控制台截圖

**如果仍然遇到問題，請告訴我具體的錯誤信息！** 🚀
