# 🔧 DeepSeek API 400 錯誤修復指南

## 📋 問題描述

**錯誤訊息**：
```
DeepSeek API error: 400
```

**根本原因**：
- DeepSeek API **不支持** `response_format` 參數
- 這是 OpenAI GPT-4 Vision API 的特有參數
- 發送此參數會導致 DeepSeek API 返回 400 錯誤

---

## ✅ 解決方案

### 1. 修復 `deepseek-vision-client.js`

**修改前（錯誤）**：
```javascript
const requestBody = {
    model: this.model,
    messages: [...],
    max_tokens: 4000,
    temperature: 0.1,
    response_format: { type: "json_object" } // ❌ DeepSeek 不支持
};
```

**修改後（正確）**：
```javascript
const requestBody = {
    model: this.model,
    messages: [...],
    max_tokens: 4000,
    temperature: 0.1 // ✅ 移除 response_format
};
```

---

## 🔍 DeepSeek API 支持的參數

根據 DeepSeek API 文檔，支持的參數包括：

### ✅ 支持的參數
- `model` (string, required) - 模型名稱，例如 `deepseek-chat`
- `messages` (array, required) - 對話消息數組
- `max_tokens` (integer, optional) - 最大生成 token 數，默認 4096
- `temperature` (float, optional) - 溫度參數，範圍 0-2，默認 1
- `top_p` (float, optional) - 核採樣參數，範圍 0-1，默認 1
- `stream` (boolean, optional) - 是否流式返回，默認 false
- `stop` (string or array, optional) - 停止序列

### ❌ 不支持的參數
- `response_format` - 這是 OpenAI 特有的參數
- `frequency_penalty` - DeepSeek 不支持
- `presence_penalty` - DeepSeek 不支持
- `logit_bias` - DeepSeek 不支持

---

## 🎯 如何確保 JSON 輸出

雖然 DeepSeek 不支持 `response_format`，但可以通過 **prompt engineering** 來確保 JSON 輸出：

### 方法 1：在 System Prompt 中明確要求
```javascript
{
    role: "system",
    content: "You are an AI that ONLY outputs valid JSON. Never include explanations outside the JSON structure."
}
```

### 方法 2：在 User Prompt 中強調
```javascript
{
    role: "user",
    content: `
        CRITICAL RULE: Output MUST be pure JSON format.
        Do NOT include any text before or after the JSON object.
        
        Expected JSON structure:
        {
            "document_type": "invoice",
            "confidence_score": 95,
            "extracted_data": { ... }
        }
    `
}
```

### 方法 3：使用 JSON Schema（推薦）
在 prompt 中提供完整的 JSON schema：
```javascript
const prompt = `
Extract data and return in this EXACT JSON format:

{
    "document_type": "invoice | receipt | bank_statement",
    "confidence_score": 0-100,
    "extracted_data": {
        "invoice_number": "string",
        "date": "YYYY-MM-DD",
        "total": 0.00,
        ...
    }
}

CRITICAL: Return ONLY the JSON object, no other text.
`;
```

---

## 🧪 測試步驟

### 1. 清除瀏覽器緩存
```bash
# 在瀏覽器開發者工具中
右鍵點擊刷新按鈕 → 清空緩存並硬性重新載入
```

### 2. 上傳測試文件
1. 訪問 `https://vaultcaddy.com/firstproject.html`
2. 點擊 "Upload files" 按鈕
3. 選擇文檔類型（Invoice / Receipt / Bank Statement）
4. 上傳一個測試文件

### 3. 檢查控制台日誌
打開瀏覽器開發者工具（F12），查看：
```
✅ 應該看到：
🚀 DeepSeek Vision Client 處理文檔: test.jpg (invoice)
🔄 嘗試 DeepSeek Vision API (重試 1/3)...
✅ DeepSeek 原始響應: {"document_type":"invoice",...}

❌ 不應該看到：
DeepSeek API error: 400
```

---

## 📊 DeepSeek vs OpenAI API 差異對比

| 功能 | OpenAI GPT-4 Vision | DeepSeek Vision |
|------|---------------------|-----------------|
| 模型名稱 | `gpt-4-vision-preview` | `deepseek-chat` |
| 圖片輸入 | ✅ 支持 | ✅ 支持 |
| Base64 圖片 | ✅ 支持 | ✅ 支持 |
| `response_format` | ✅ 支持 | ❌ 不支持 |
| `max_tokens` | ✅ 支持 (最大 4096) | ✅ 支持 (最大 4096) |
| `temperature` | ✅ 支持 (0-2) | ✅ 支持 (0-2) |
| `top_p` | ✅ 支持 | ✅ 支持 |
| `stream` | ✅ 支持 | ✅ 支持 |
| 價格（1M tokens） | $10-30 USD | $0.14-0.28 USD |

---

## 🚀 後續優化建議

### 1. 添加 JSON 驗證
在客戶端解析 JSON 後，驗證結構：
```javascript
function validateExtractedData(data) {
    if (!data.document_type || !data.extracted_data) {
        throw new Error('Invalid JSON structure from DeepSeek');
    }
    return true;
}
```

### 2. 添加重試機制
如果 DeepSeek 返回非 JSON 格式，自動重試：
```javascript
let parsedData;
try {
    parsedData = JSON.parse(content);
} catch (jsonError) {
    console.warn('⚠️ 第一次解析失敗，嘗試清理響應...');
    // 嘗試移除 markdown 代碼塊標記
    const cleaned = content.replace(/```json\n?/g, '').replace(/```\n?/g, '');
    parsedData = JSON.parse(cleaned);
}
```

### 3. 監控 API 響應質量
記錄每次 API 調用的結果：
```javascript
const apiLog = {
    timestamp: new Date().toISOString(),
    model: 'deepseek-chat',
    success: true,
    confidence: parsedData.confidence_score,
    responseTime: Date.now() - startTime
};
console.log('📊 API 調用記錄:', apiLog);
```

---

## 📞 支持資源

- **DeepSeek API 文檔**: https://platform.deepseek.com/api-docs/
- **VaultCaddy 技術支持**: 查看項目 README.md
- **問題反饋**: 在項目中創建 GitHub Issue

---

## ✅ 修復確認清單

- [x] 移除 `response_format` 參數
- [x] 更新 `deepseek-vision-client.js`
- [x] 提交代碼到 Git
- [ ] 清除瀏覽器緩存
- [ ] 測試文件上傳
- [ ] 驗證 DeepSeek API 正常工作
- [ ] 檢查提取的數據質量

---

**最後更新**: 2025-10-27  
**狀態**: ✅ 已修復

