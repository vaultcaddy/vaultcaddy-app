# 🔍 Vision API 診斷指南

**錯誤信息：**
```
❌ 混合處理失敗: Error: Vision API 未能提取文本
```

**問題分析：** Vision API 返回了成功的 HTTP 響應，但響應數據中缺少 `fullTextAnnotation` 字段。

---

## ✅ 增強診斷功能

我已經在 `hybrid-vision-deepseek.js` 中添加了詳細的日誌，現在會顯示：

1. **HTTP 錯誤詳情** (如果 Vision API 返回非 200 狀態碼)
   - HTTP 狀態碼
   - 狀態文本
   - 錯誤響應內容

2. **完整的 Vision API 響應** (JSON 格式)

3. **Vision API 錯誤字段** (如果存在)

4. **可用的響應鍵列表** (如果缺少 `fullTextAnnotation`)

---

## 🧪 立即測試

### 步驟 1：上傳 PDF 文件並查看控制台

```
1. Cmd+Shift+R 刷新頁面（清除緩存）
2. 前往項目頁面
3. 上傳 PDF 文件 (eStatementFile_20250829143359.pdf)
4. F12 打開控制台
5. 查看詳細日誌輸出
```

### 預期看到的日誌：

#### 成功情況 ✅
```javascript
📡 Vision API 完整響應: {
  "responses": [{
    "fullTextAnnotation": {
      "text": "... OCR 提取的文本 ..."
    }
  }]
}
✅ 成功提取文本，長度: 1234
```

#### 錯誤情況 ❌
```javascript
📡 Vision API 完整響應: {
  "responses": [{
    "error": {
      "code": 7,
      "message": "Invalid image content",
      "status": "INVALID_ARGUMENT"
    }
  }]
}
❌ Vision API 返回錯誤: Invalid image content
```

或者：

```javascript
📡 Vision API 完整響應: {
  "responses": [{
    "textAnnotations": [...]
  }]
}
❌ Vision API 響應中沒有 fullTextAnnotation
可用的鍵: textAnnotations
```

---

## 🚨 常見錯誤原因

### 1. API 密鑰問題 ❌
```
錯誤: 403 Forbidden
原因: API 密鑰無效或已過期
解決: 檢查 Firebase Functions Config 中的 google.vision_api_key
```

### 2. API 未啟用 ❌
```
錯誤: 403 - Cloud Vision API has not been used in project
原因: Vision API 未在 Google Cloud Console 中啟用
解決: 前往 https://console.cloud.google.com/apis/library/vision.googleapis.com
       點擊「ENABLE」啟用 Vision API
```

### 3. 配額超限 ❌
```
錯誤: 429 - Quota exceeded
原因: 超過每日或每分鐘的請求配額
解決: 等待配額重置或升級 Google Cloud 計費帳戶
```

### 4. 文件格式問題 ❌
```
錯誤: INVALID_ARGUMENT - Invalid image content
原因: 
  - PDF 文件損壞
  - PDF 包含受保護的內容
  - Base64 編碼錯誤
  - 文件大小超過限制（20MB）
解決: 
  - 檢查 PDF 文件是否有效
  - 嘗試用其他工具打開 PDF
  - 檢查 base64Data 長度
```

### 5. 權限問題 ❌
```
錯誤: Permission denied
原因: Service Account 沒有 Vision API 權限
解決: 檢查 Service Account IAM 角色
```

---

## 📋 檢查清單

### Google Cloud Console 檢查

- [ ] **Vision API 已啟用**
  ```
  前往: https://console.cloud.google.com/apis/library/vision.googleapis.com
  狀態: 應顯示「API enabled」
  ```

- [ ] **API 密鑰有效**
  ```
  前往: https://console.cloud.google.com/apis/credentials
  檢查: API 密鑰沒有過期
  限制: API 密鑰應允許 Cloud Vision API
  ```

- [ ] **配額充足**
  ```
  前往: https://console.cloud.google.com/apis/api/vision.googleapis.com/quotas
  檢查: 每日配額未超限
  ```

- [ ] **計費帳戶已連接**
  ```
  前往: https://console.cloud.google.com/billing
  狀態: 計費帳戶應處於活躍狀態
  ```

### Firebase Functions Config 檢查

- [ ] **Vision API Key 已設置**
  ```bash
  firebase functions:config:get google.vision_api_key
  
  # 應返回：
  # "AIzaSy..."
  ```

- [ ] **Vision API URL 正確**
  ```javascript
  // hybrid-vision-deepseek.js
  this.visionApiUrl = 'https://vision.googleapis.com/v1/images:annotate';
  ```

### 文件檢查

- [ ] **PDF 文件有效**
  ```
  - 文件可以在本地 PDF 閱讀器中打開
  - 文件大小 < 20MB
  - 文件不包含密碼保護
  - 文件不是純圖像掃描（Vision API 需要文本內容）
  ```

- [ ] **Base64 編碼正確**
  ```javascript
  // 檢查 base64Data 長度（應該很長）
  console.log('Base64 長度:', base64Data.length);
  // 預期: > 100000 (對於多頁 PDF)
  ```

---

## 🔧 手動測試 Vision API

### 使用 curl 測試

```bash
# 1. 將 PDF 轉換為 Base64
base64 -i eStatementFile_20250829143359.pdf -o test.b64

# 2. 創建請求 JSON
cat > request.json << 'EOF'
{
  "requests": [{
    "image": {
      "content": "PASTE_BASE64_HERE"
    },
    "features": [{
      "type": "DOCUMENT_TEXT_DETECTION",
      "maxResults": 1
    }]
  }]
}
EOF

# 3. 發送請求
curl -X POST \
  -H "Content-Type: application/json" \
  "https://vision.googleapis.com/v1/images:annotate?key=YOUR_API_KEY" \
  -d @request.json

# 4. 檢查響應
# 成功: 應包含 "fullTextAnnotation"
# 失敗: 應包含 "error" 字段
```

---

## 💡 可能的解決方案

### 方案 1：檢查 Vision API 狀態
```
使用 Chrome MCP 工具前往：
https://console.cloud.google.com/apis/api/vision.googleapis.com

確認:
1. API 已啟用
2. 配額充足
3. 無錯誤警告
```

### 方案 2：檢查 API 密鑰權限
```
前往: https://console.cloud.google.com/apis/credentials
選擇你的 API 密鑰
檢查:
1. API restrictions -> Cloud Vision API 已勾選
2. Application restrictions -> 適當設置（推薦 HTTP referrers）
3. Key restrictions -> None 或允許你的域名
```

### 方案 3：檢查 Service Account 權限 (如果使用)
```
前往: https://console.cloud.google.com/iam-admin/iam
找到你的 Service Account
檢查角色:
1. Cloud Vision API User
2. Storage Object Viewer (如果從 Storage 讀取文件)
```

### 方案 4：切換到 PDF 轉圖片方案（臨時）
如果 Vision API 確實不支持 PDF（雖然官方文檔說支持），可以恢復 PDF 轉圖片邏輯：

```javascript
// 恢復 pdf-to-image-converter.js
// 恢復 firstproject.html 中的轉換邏輯
// 恢復 batch-upload-processor.js 中的轉換邏輯
```

---

## 📞 下一步

### 立即執行：

1. **刷新頁面並重新上傳 PDF**
   ```
   Cmd+Shift+R 刷新頁面
   上傳 eStatementFile_20250829143359.pdf
   查看控制台詳細日誌
   ```

2. **截圖控制台完整輸出**
   ```
   包含：
   - 📡 Vision API 完整響應
   - 📋 First Response
   - ❌ 錯誤信息（如果有）
   - 可用的鍵列表（如果有）
   ```

3. **提供截圖給我**
   ```
   我會根據實際的 Vision API 響應
   來診斷具體問題並提供精準的解決方案
   ```

---

## 🎯 測試重點

- 是否是 **HTTP 錯誤**？（401, 403, 429, 500）
- 是否是 **Vision API 錯誤**？（INVALID_ARGUMENT, PERMISSION_DENIED）
- 是否是 **數據結構問題**？（缺少 fullTextAnnotation，但有其他字段）
- 是否是 **文件問題**？（PDF 格式、大小、編碼）

---

**請立即測試並提供控制台完整日誌截圖！** 🚀

根據實際的 Vision API 響應，我可以精準診斷問題並提供解決方案。

