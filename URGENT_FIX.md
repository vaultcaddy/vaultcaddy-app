# 🚨 **緊急修復：立即更新 Cloudflare Worker**

## ❌ **當前問題**
Cloudflare Worker 使用的是**舊代碼**，導致持續 404 錯誤。

---

## ✅ **3 步驟修復（5 分鐘完成）**

### **Step 1: 複製代碼**

1. 打開本地文件：`cloudflare-worker-gemini.js`
2. **全選**（Cmd+A）
3. **複製**（Cmd+C）

---

### **Step 2: 訪問 Cloudflare**

打開瀏覽器，訪問：
```
https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production
```

（這個標籤應該已經打開了）

---

### **Step 3: 部署新代碼**

在 Cloudflare 編輯器中：

1. **全選現有代碼**（Cmd+A）
2. **刪除**（Delete）
3. **粘貼新代碼**（Cmd+V）
4. **找到右上角的 "Save and Deploy" 按鈕**
5. **點擊部署**
6. **等待 3-5 秒**，直到看到 "Successfully deployed" 消息

---

## 🔍 **如何確認已部署成功？**

部署後，在終端執行：

```bash
curl -X POST https://gemini-proxy.vaultcaddy.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}'
```

**預期響應**：
- ❌ 如果還是 404：代碼沒有更新成功，重試 Step 3
- ✅ 如果是其他錯誤（如 400）：代碼已更新，可以測試上傳了

---

## 📝 **關鍵檢查點**

部署新代碼後，第 9 行應該是：
```javascript
const GEMINI_API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent';
```

**確認要點**：
- ✅ `v1`（不是 `v1beta`）
- ✅ `gemini-1.5-flash`（不是 `gemini-1.5-flash-latest`）
- ✅ `:generateContent`（不要漏掉）

---

## 🚀 **部署後測試**

1. **清除瀏覽器緩存**（Cmd+Shift+Delete）
2. **訪問**：`https://vaultcaddy.com/firstproject.html`
3. **打開 Console**（Cmd+Option+I）
4. **上傳測試發票**
5. **觀察輸出**

**預期成功輸出**：
```
✅ geminiAI 處理成功
   耗時: 3000-5000ms
📊 提取的發票數據: {...}
```

---

## ⚠️ **常見錯誤**

### **錯誤 1: 部署按鈕找不到**
- 可能文字是 "Deploy"、"Save"、"Save and Deploy"
- 通常在右上角，可能是藍色或綠色按鈕

### **錯誤 2: 部署後還是 404**
- 等待 10-30 秒讓 Cloudflare CDN 更新
- 清除瀏覽器緩存
- 重新測試

### **錯誤 3: 403 Forbidden**
- 確認 Google Cloud API Key 限制已設為 "無"
- 等待 5-10 分鐘

---

## 📞 **如果還是不行**

請提供：
1. Cloudflare 編輯器第 9 行的截圖
2. 部署成功的截圖
3. 最新的 Console 錯誤截圖

---

**現在就去部署吧！** 🚀
