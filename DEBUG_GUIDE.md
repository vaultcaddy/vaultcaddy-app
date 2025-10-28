# 🔍 調試指南：AI 處理失敗

## 📋 當前狀態

根據您的截圖：
- ✅ 文件已成功上傳
- ✅ 顯示「處理中...」
- ✅ Cloudflare Worker 已正確部署
- ❌ AI 處理失敗：所有處理器都無法處理此文檔

## 🎯 問題定位

從控制台日誌中，我們需要找到**具體的錯誤原因**。

### 關鍵日誌位置

請在控制台中查找以下日誌：

1. **混合處理器開始**：
   ```
   🚀 混合處理器開始處理: PHOTO-2025-10-03-18-10-02.jpg (invoice)
   ```

2. **Vision API OCR 調用**：
   ```
   📸 步驟 1: 使用 Vision API 進行 OCR...
   📸 調用 Vision API OCR...
   ```

3. **Vision API 響應**：
   ```
   📄 Vision API 響應: {
     success: true/false,
     hasData: true/false,
     hasFullText: true/false,
     hasText: true/false
   }
   ```

4. **錯誤信息**（最重要）：
   ```
   ❌ Vision API 提取文本失敗: [具體錯誤信息]
   ❌ 處理器 hybridOCRDeepSeek 失敗: [具體錯誤信息]
   ```

---

## 🔧 可能的原因和解決方案

### 原因 1：Google Vision API Key 無效或過期

**症狀**：
```
❌ Vision API 錯誤: 401 - Unauthorized
或
❌ Vision API 錯誤: 403 - Forbidden
```

**解決方案**：

1. 檢查 API Key 是否正確：
   - 打開瀏覽器控制台
   - 輸入：`window.VaultCaddyConfig.apiConfig.google.apiKey`
   - 應該顯示：`AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug`

2. 驗證 API Key：
   ```bash
   curl "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug" \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "requests": [{
         "image": {"content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="},
         "features": [{"type": "TEXT_DETECTION"}]
       }]
     }'
   ```

3. 如果 API Key 無效，需要：
   - 訪問 https://console.cloud.google.com/apis/credentials
   - 創建新的 API Key
   - 啟用 Cloud Vision API
   - 更新 `config.js` 中的 API Key

---

### 原因 2：Vision API 配額用盡

**症狀**：
```
❌ Vision API 錯誤: 429 - Quota exceeded
或
❌ Vision API 錯誤: RESOURCE_EXHAUSTED
```

**解決方案**：

1. 檢查配額：
   - 訪問 https://console.cloud.google.com/apis/api/vision.googleapis.com/quotas
   - 查看「每天請求數」和「每分鐘請求數」

2. 免費配額：
   - 前 1,000 張圖片/月：免費
   - 之後：$1.50 / 1,000 張

3. 如果配額用盡：
   - 等待配額重置（每月 1 日）
   - 或升級到付費計劃

---

### 原因 3：圖片格式或大小問題

**症狀**：
```
❌ Vision API 未能從圖片中提取任何文本
或
❌ Vision API 錯誤: Invalid image
```

**解決方案**：

1. 檢查圖片：
   - **格式**：JPG, PNG, GIF, BMP, WEBP, RAW, ICO, PDF, TIFF
   - **大小**：最大 20MB
   - **分辨率**：建議至少 300 DPI
   - **內容**：文字清晰可讀

2. 測試圖片：
   - 使用簡單的打印文檔
   - 避免手寫文字
   - 避免模糊或傾斜的圖片

---

### 原因 4：CORS 或網絡問題

**症狀**：
```
❌ Failed to fetch
或
❌ Network error
或
❌ CORS policy
```

**解決方案**：

1. 檢查網絡連接
2. 檢查瀏覽器控制台的 Network 標籤
3. 查找失敗的請求（紅色）
4. 查看請求詳情和響應

---

### 原因 5：Vision API 未啟用

**症狀**：
```
❌ Vision API 錯誤: 403 - Cloud Vision API has not been used in project...
```

**解決方案**：

1. 訪問 https://console.cloud.google.com/apis/library/vision.googleapis.com
2. 點擊「啟用」
3. 等待幾分鐘讓 API 生效
4. 重試

---

## 🧪 調試步驟

### 步驟 1：獲取完整錯誤日誌

1. 打開瀏覽器控制台（F12）
2. 清除所有日誌（垃圾桶圖標）
3. 強制刷新頁面（Cmd+Shift+R）
4. 上傳測試文件
5. 複製所有日誌（右鍵 → Save as...）

### 步驟 2：檢查 Vision API 調用

在控制台中輸入以下代碼來測試 Vision API：

```javascript
// 測試 Vision API
async function testVisionAPI() {
    const config = window.VaultCaddyConfig.apiConfig.google;
    const apiKey = config.apiKey;
    const endpoint = config.endpoints.vision;
    
    console.log('🔍 測試 Vision API');
    console.log('   API Key:', apiKey);
    console.log('   Endpoint:', endpoint);
    
    // 使用一個簡單的測試圖片（1x1 像素的 PNG）
    const testImage = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
    
    const requestBody = {
        requests: [{
            image: { content: testImage },
            features: [{ type: 'TEXT_DETECTION' }]
        }]
    };
    
    try {
        const response = await fetch(`${endpoint}/images:annotate?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        
        console.log('📊 響應狀態:', response.status);
        
        const result = await response.json();
        console.log('📄 響應內容:', result);
        
        if (response.ok) {
            console.log('✅ Vision API 正常工作');
        } else {
            console.error('❌ Vision API 錯誤:', result);
        }
    } catch (error) {
        console.error('❌ 請求失敗:', error);
    }
}

// 運行測試
testVisionAPI();
```

### 步驟 3：檢查混合處理器

在控制台中輸入：

```javascript
// 檢查混合處理器狀態
console.log('🔍 混合處理器狀態:');
console.log('   存在:', typeof window.hybridOCRDeepSeekProcessor);
console.log('   Vision API:', typeof window.googleVisionAI);
console.log('   DeepSeek Worker:', window.hybridOCRDeepSeekProcessor?.deepseekWorkerUrl);
console.log('   DeepSeek Model:', window.hybridOCRDeepSeekProcessor?.deepseekModel);
console.log('   使用 DeepSeek:', window.hybridOCRDeepSeekProcessor?.useDeepSeek);
```

### 步驟 4：測試完整流程

```javascript
// 測試完整的 AI 處理流程
async function testFullProcess() {
    // 創建一個測試文件
    const testFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
    
    console.log('🧪 測試完整 AI 處理流程');
    
    try {
        const result = await window.hybridOCRDeepSeekProcessor.processDocument(testFile, 'invoice');
        console.log('✅ 處理成功:', result);
    } catch (error) {
        console.error('❌ 處理失敗:', error);
        console.error('   錯誤類型:', error.name);
        console.error('   錯誤消息:', error.message);
        console.error('   錯誤堆棧:', error.stack);
    }
}

// 運行測試
testFullProcess();
```

---

## 📝 報告問題

如果問題仍然存在，請提供以下信息：

### 1. 完整的控制台日誌

從頁面加載到上傳失敗的所有日誌。

### 2. Vision API 測試結果

運行 `testVisionAPI()` 的結果。

### 3. 混合處理器狀態

運行混合處理器狀態檢查的結果。

### 4. Network 標籤信息

- 打開 F12 → Network 標籤
- 上傳文件
- 查找失敗的請求（紅色）
- 提供請求 URL、狀態碼、響應內容

### 5. 測試圖片信息

- 文件名
- 文件大小
- 文件格式
- 圖片內容描述（是否清晰、是否有文字等）

---

## 🎯 快速診斷清單

- [ ] 瀏覽器緩存已清除（Cmd+Shift+R）
- [ ] 控制台沒有紅色錯誤（除了預期的警告）
- [ ] Vision API Key 正確顯示
- [ ] `hybridOCRDeepSeekProcessor` 已初始化
- [ ] `googleVisionAI` 已初始化
- [ ] Cloudflare Worker 正常運行
- [ ] 測試圖片格式正確（JPG/PNG）
- [ ] 測試圖片大小 < 20MB
- [ ] 測試圖片內容清晰可讀

---

**最後更新**：2025-10-27  
**版本**：v20251027-004  
**狀態**：🔍 調試中

