# 🧪 Gemini AI 測試指南

## ✅ 修復內容

### **問題**
- Gemini Worker Client 未正確初始化
- `google-smart-processor.js` 在構造時靜態引用 `window` 對象
- 導致 `geminiWorkerClient` 未被識別，系統回退到 Vision AI

### **解決方案**

1. **google-smart-processor.js**
   - 改用 getter 動態獲取處理器
   - 新增詳細的處理器狀態日誌

2. **firstproject.html**
   - 調整腳本載入順序（`gemini-worker-client.js` 在前）
   - 增強初始化日誌

---

## 🧪 測試步驟

### **Step 1: 清除瀏覽器緩存**

**重要！** 必須清除緩存，否則會載入舊代碼。

#### **Chrome / Edge**
1. 打開 DevTools（F12）
2. 右鍵點擊刷新按鈕
3. 選擇 "清空緩存並硬性重新載入"

#### **Safari**
1. 按 `Cmd + Option + E` 清空緩存
2. 按 `Cmd + R` 重新載入

---

### **Step 2: 打開項目頁面**

訪問：
```
https://vaultcaddy.com/firstproject.html
```

---

### **Step 3: 檢查控制台初始化日誌**

打開控制台（F12），應該看到：

```
🎯 Dashboard 頁面載入中...

🤖 初始化 Gemini Worker Client...
   window.GeminiWorkerClient: function
✅ Gemini Worker Client 已初始化
   Worker URL: https://gemini-proxy.vaultcaddy.workers.dev/...
   Client 實例: GeminiWorkerClient {...}

🧠 Google 智能處理器初始化
可用處理器: ['geminiAI', 'visionAI']
   - documentAI: undefined
   - visionAI: object
   - geminiAI (geminiWorkerClient): object  ← ✅ 應該是 'object'，不是 'undefined'
```

**關鍵檢查點：**
- ✅ `window.GeminiWorkerClient: function`（不是 `undefined`）
- ✅ `可用處理器` 包含 `geminiAI`
- ✅ `geminiAI (geminiWorkerClient): object`（不是 `undefined`）

---

### **Step 4: 上傳發票測試**

1. 點擊 "Upload files" 按鈕
2. 選擇一張發票圖片（建議使用之前的測試圖片）
3. 觀察控制台輸出

---

### **Step 5: 驗證處理器使用**

控制台應顯示：

```
🚀 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)

📋 處理順序: ['geminiAI', 'visionAI']
🔄 嘗試 1/2 使用 geminiAI...  ← ✅ 應該優先使用 geminiAI

🤖 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)
   文件大小: 2063072 bytes

🔄 嘗試 1/3...
�� Worker 請求已發送

✅ geminiAI 處理成功  ← ✅ 成功使用 Gemini AI
   耗時: 3542ms
```

**不應該看到：**
- ❌ `🔧 開始Vision AI處理`（這表示跳過了 Gemini）
- ❌ `⚠️ geminiAI 處理失敗`

---

### **Step 6: 驗證提取結果**

#### **發票號碼**
- ✅ 應該完整且正確（例如：`FI25093602`）
- ❌ 不應該是 `OICE` 或其他錯誤值

#### **商品明細**
- ✅ 應該提取**所有**商品行（例如：2 個商品項目）
- ❌ 不應該只有 1 個商品

#### **總金額**
- ✅ 應該準確（例如：`HKD $1250.00`）
- ❌ 不應該是估算值或錯誤金額

#### **供應商信息**
- ✅ 應該包含完整的公司名稱（例如：`HW海運達（香港）有限公司`）

---

## 🎯 預期結果對比

| 項目 | Vision AI（舊） | Gemini AI（新） |
|------|----------------|----------------|
| **處理器** | visionAI | **geminiAI** ✅ |
| **準確率** | ~70% | **95%+** ✅ |
| **發票號碼** | ⚠️ OICE | **✅ FI25093602** |
| **商品明細** | ❌ 1 個 | **✅ 2 個** |
| **總金額** | ⚠️ $0.00 | **✅ $1250.00** |
| **處理時間** | ~364ms | ~3500ms |

---

## ❌ 常見問題排查

### **問題 1：仍然使用 Vision AI**

**症狀：**
```
🔧 開始Vision AI處理
```

**解決方案：**
1. 清除瀏覽器緩存（Ctrl+Shift+Delete）
2. 硬性重新載入（Ctrl+F5）
3. 檢查控制台是否顯示 `geminiAI (geminiWorkerClient): object`

---

### **問題 2：GeminiWorkerClient 未找到**

**症狀：**
```
❌ GeminiWorkerClient 類別未找到
   window.GeminiWorkerClient 類型: undefined
```

**解決方案：**
1. 檢查 `gemini-worker-client.js` 是否載入成功（Network 標籤）
2. 確認腳本載入順序正確
3. 檢查 Console 是否有載入錯誤

---

### **問題 3：Worker 404 錯誤**

**症狀：**
```
❌ Worker 響應錯誤: 404
```

**解決方案：**
1. 確認 Cloudflare Worker 已部署
2. 訪問 `https://gemini-proxy.vaultcaddy.workers.dev` 應該返回 "Method Not Allowed"
3. 檢查 Worker URL 是否正確

---

## 📊 成功標準

測試通過的標準：

1. ✅ 控制台顯示 `可用處理器: ['geminiAI', 'visionAI']`
2. ✅ 上傳文件優先使用 `geminiAI`
3. ✅ 發票號碼提取正確（不是 `OICE`）
4. ✅ 商品明細提取完整（所有行項目）
5. ✅ 總金額提取準確（不是 `$0.00`）

---

**準備好測試了嗎？** 🚀

請按照上述步驟測試，並將控制台截圖發給我！
