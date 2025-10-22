# 🛠️ **最終修復指南：解決 Gemini API 403 錯誤**

## 📌 **當前狀況**

1. ✅ **Cloudflare Worker 已部署**
2. ✅ **Worker 代碼已更新**（添加了 `Referer` 頭）
3. ❌ **Gemini API 返回 403 錯誤**：`Requests from referer <empty> are blocked`

---

## 🎯 **兩種解決方案**

### **方案 A：移除 API Key 的 Referer 限制（推薦）** ⭐

#### **Step 1: 訪問 Google Cloud Console**

1. **打開瀏覽器**，訪問：
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **登入正確的 Google 帳戶**（確保是創建 API Key 的帳戶）

3. **切換到正確的項目**
   - 點擊頂部的項目選擇器（例如："My First Project"）
   - 查看所有項目列表
   - 逐一切換項目，尋找包含 API Key 的項目

#### **Step 2: 找到並編輯 API Key**

1. **在 "API 金鑰" 列表中**找到你的 API Key
   - API Key: `AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug`

2. **點擊 API Key 名稱**進入編輯頁面

3. **修改應用限制**
   - 找到 "**Application restrictions**"（應用限制）部分
   - 選擇 "**None**"（無）
   - 點擊 "**Save**"（保存）

4. **等待設置生效**（5-10 分鐘）

---

### **方案 B：創建新的無限制 API Key**

如果找不到原來的 API Key，建議創建新的：

#### **Step 1: 創建新的 API Key**

1. 訪問 Google AI Studio：
   ```
   https://aistudio.google.com/app/apikey
   ```

2. 點擊 "**Create API Key**" 或 "**Get API key**"

3. 選擇項目（或創建新項目）

4. **不要設置任何限制**

5. **複製新的 API Key**

#### **Step 2: 更新 Cloudflare Worker**

1. **打開本地文件** `cloudflare-worker-gemini.js`

2. **找到第 3 行**：
   ```javascript
   const GEMINI_API_KEY = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug';
   ```

3. **替換為新的 API Key**：
   ```javascript
   const GEMINI_API_KEY = '你的新API Key';
   ```

4. **打開 Cloudflare Dashboard**：
   ```
   https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production
   ```

5. **複製更新後的代碼**，粘貼到編輯器，點擊 "**Deploy**"

---

## ✅ **驗證修復**

### **Step 1: 清除瀏覽器緩存**

- **Chrome**: Ctrl+Shift+Delete
- **Safari**: Cmd+Option+E
- 選擇 "**清除所有數據**"

### **Step 2: 測試上傳**

1. 訪問：
   ```
   https://vaultcaddy.com/firstproject.html
   ```

2. **打開開發者工具**（F12）

3. **切換到 Console 標籤**

4. **點擊 "Upload files"**

5. **選擇之前的發票圖片**

6. **觀察控制台輸出**

### **Step 3: 預期結果**

#### **成功的輸出**：
```
🚀 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)
📋 處理順序: ['geminiAI', 'visionAI']
🔄 嘗試 1/2 使用 geminiAI...

🤖 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)
   文件大小: 2063072 bytes
🔄 嘗試 1/3...
📥 Worker 請求已發送

✅ geminiAI 處理成功  ← ✅ 成功！
   耗時: 3542ms

📋 提取的發票數據:
   - 發票號碼: FI25093602  ✅
   - 商品明細: 2 個  ✅
   - 總金額: $1250.00  ✅
```

#### **失敗的輸出**：
```
❌ 嘗試 1/3 失敗: Worker 錯誤: Gemini API 錯誤
   響應錯誤: 403 = {"error":"Gemini API 錯誤","status":403}
```

---

## 📋 **快速檢查清單**

- [ ] 已找到 API Key 所在的項目
- [ ] 已移除 API Key 的 Referer 限制（或創建新的無限制 API Key）
- [ ] 已重新部署 Cloudflare Worker
- [ ] 已清除瀏覽器緩存
- [ ] 已測試上傳發票
- [ ] 控制台顯示 "✅ geminiAI 處理成功"

---

## ❓ **常見問題**

### **Q1: 我在所有項目中都找不到 API Key**

**A**: API Key 可能已被刪除，請使用**方案 B**創建新的 API Key。

### **Q2: 修改後仍然 403 錯誤**

**A**: 可能原因：

1. **設置未生效**：等待 10 分鐘
2. **Worker 未更新**：確認 Cloudflare Worker 已重新部署
3. **API Key 錯誤**：確認 Worker 中的 API Key 正確

### **Q3: Google AI Studio 顯示 "不可用"**

**A**: 你的帳戶或地區可能不支持 Google AI Studio，請使用**方案 A**（Google Cloud Console）創建 API Key。

---

## 🚀 **下一步**

1. **選擇方案**：方案 A（移除限制）或方案 B（創建新 Key）
2. **執行步驟**：按照上述步驟操作
3. **驗證修復**：清除緩存並測試上傳
4. **提供結果**：將控制台截圖發給我

**如果仍然遇到問題，請告訴我具體的錯誤信息！** 🎯
