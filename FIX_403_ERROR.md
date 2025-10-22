# 🔧 修復 Gemini API 403 錯誤

## ❌ **錯誤詳情**

```
Failed to load gemini-proxy.vaultcaddy.workers.dev
server responded with a status of 403

{"error":"Gemini API 錯誤","status":403,"details":{"error":
{"code":403,"message":"Requests from referer <empty> are blocked."}}}
```

## 🎯 **根本原因**

Gemini API Key 設置了 **HTTP Referrer 限制**，阻擋了來自 Cloudflare Worker 的請求。

---

## ✅ **解決方案**

### **Step 1: 訪問 Google Cloud Console**

打開以下連結：
```
https://console.cloud.google.com/apis/credentials
```

或者訪問：
```
https://aistudio.google.com/app/apikey
```

---

### **Step 2: 找到你的 API Key**

查找 API Key：
```
AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug
```

---

### **Step 3: 編輯 API Key 設置**

1. **點擊 API Key 名稱**
2. **找到 "Application restrictions"（應用限制）**
3. **選擇以下其中一個選項**：

#### **選項 A：移除所有限制（最簡單）** ⭐

- 選擇 "**None**"（無）
- 點擊 "Save"（保存）

#### **選項 B：添加允許的 Referrers**

- 選擇 "**HTTP referrers (web sites)**"
- 添加以下 referrers：
  ```
  https://vaultcaddy.com/*
  https://*.vaultcaddy.workers.dev/*
  http://localhost/*
  http://127.0.0.1/*
  ```
- 點擊 "Save"（保存）

---

### **Step 4: 等待設置生效**

API Key 限制更改通常會在 **幾分鐘內**生效，但可能需要最多 **10 分鐘**。

---

### **Step 5: 重新部署 Cloudflare Worker**

我已經更新了 Worker 代碼，添加了 `Referer` 頭。請重新部署：

1. **打開 Cloudflare Dashboard**
   ```
   https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production
   ```

2. **複製更新後的代碼**
   - 打開本地文件：`cloudflare-worker-gemini.js`
   - 全選並複製

3. **粘貼並部署**
   - 在 Cloudflare 編輯器中，刪除所有現有代碼
   - 粘貼新代碼
   - 點擊 "Deploy" 按鈕

**關鍵更改**（第 91 行）：
```javascript
headers: {
  'Content-Type': 'application/json',
  'Referer': 'https://vaultcaddy.com/',  // 新增
}
```

---

### **Step 6: 測試**

1. **清除瀏覽器緩存**
2. **訪問** `https://vaultcaddy.com/firstproject.html`
3. **上傳發票**
4. **檢查控制台**，應該看到：
   ```
   ✅ geminiAI 處理成功
   ```

---

## 🔍 **驗證 API Key 設置**

### **檢查當前設置**

1. 訪問：https://console.cloud.google.com/apis/credentials
2. 點擊你的 API Key
3. 查看 "Application restrictions"：
   - ✅ **應該是**: `None` 或包含 `https://vaultcaddy.com/*`
   - ❌ **不應該是**: `HTTP referrers` 但列表為空，或只有其他域名

---

## 📊 **預期結果**

### **修復前（當前）**
```
❌ 嘗試 1/3 失敗: Worker 錯誤: Gemini API 錯誤
   響應錯誤: 403 = {"error":"Gemini API 錯誤","status":403}
   
🔧 開始Vision AI處理  ← 回退到 Vision AI
```

### **修復後**
```
✅ geminiAI 處理成功
   耗時: 3542ms
   
📋 提取的發票數據:
   - 發票號碼: FI25093602  ✅
   - 商品明細: 2 個  ✅
   - 總金額: $1250.00  ✅
```

---

## ❓ **常見問題**

### **Q1: 移除限制安全嗎？**

**A**: 有一定風險，但可以通過以下方式降低：

1. **監控使用量**：在 Google Cloud Console 中設置配額警報
2. **限制 API 訪問**：只啟用 "Generative Language API"
3. **定期輪換 API Key**：每月更換一次

### **Q2: 設置已更改，但仍然 403**

**A**: 可能原因：

1. **設置未生效**：等待 5-10 分鐘
2. **Worker 未重新部署**：確保 Cloudflare Worker 已更新
3. **API Key 錯誤**：檢查 Worker 中的 API Key 是否正確

### **Q3: 能否只允許 Cloudflare Worker？**

**A**: 可以，但需要知道 Cloudflare Worker 的 IP 範圍。更簡單的方法是：

1. 使用環境變量存儲 API Key（而不是硬編碼）
2. 設置 Cloudflare Worker 的 Secret

---

## 🚀 **立即行動**

1. **現在就打開** Google Cloud Console
2. **移除 API Key 的 Referer 限制**
3. **重新部署 Cloudflare Worker**（使用更新後的代碼）
4. **等待 5 分鐘**
5. **測試上傳發票**

---

**完成後請告訴我結果！** 🎯
