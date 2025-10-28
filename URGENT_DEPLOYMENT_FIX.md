# 🚨 緊急修復：Cloudflare Worker 部署

## 問題診斷

您看到的錯誤：
```
AI 處理失敗: 所有處理器都無法處理此文檔
```

**原因**：Cloudflare Worker 可能未正確部署或配置

---

## 🔧 立即修復（5 分鐘）

### 步驟 1：打開 Cloudflare Worker 編輯器

1. 訪問：https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/deepseek-proxy/production
2. 點擊 "Quick edit"

### 步驟 2：更新 Worker 代碼

**刪除所有舊代碼**，然後複製以下完整代碼：

```javascript
/**
 * Cloudflare Worker - DeepSeek API 代理
 * 用途：繞過 CORS 限制，安全地調用 DeepSeek API
 * 部署：https://workers.cloudflare.com/
 * 
 * 支持的模型：
 * - deepseek-chat: DeepSeek-V3.2-Exp（非思考模式）
 * - deepseek-reasoner: DeepSeek-V3.2-Exp（思考模式）- 推薦
 * 
 * 最後更新：2025-10-27
 */

// 配置
const DEEPSEEK_API_KEY = 'sk-4a43b49a13a840009052be65f599b7a4'; // ✅ DeepSeek API Key
const DEEPSEEK_API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

// 支持的模型列表
const SUPPORTED_MODELS = ['deepseek-chat', 'deepseek-reasoner'];

// 允許的來源（CORS）
const ALLOWED_ORIGINS = [
  'https://vaultcaddy.com',
  'http://localhost:3000',
  'http://127.0.0.1:3000'
];

/**
 * 處理 CORS 預檢請求
 */
function handleCORS(request) {
  const origin = request.headers.get('Origin');
  
  const headers = {
    'Access-Control-Allow-Origin': origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };
  
  return new Response(null, {
    status: 204,
    headers
  });
}

/**
 * 添加 CORS 頭到響應
 */
function addCORSHeaders(response, origin) {
  const newHeaders = new Headers(response.headers);
  newHeaders.set('Access-Control-Allow-Origin', origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0]);
  newHeaders.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  newHeaders.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  });
}

/**
 * 處理請求
 */
async function handleRequest(request) {
  const origin = request.headers.get('Origin');
  
  // 處理 CORS 預檢請求
  if (request.method === 'OPTIONS') {
    return handleCORS(request);
  }
  
  // 只允許 POST 請求
  if (request.method !== 'POST') {
    const errorResponse = new Response(JSON.stringify({ 
      error: 'Method not allowed',
      message: '只支持 POST 請求'
    }), { 
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
    return addCORSHeaders(errorResponse, origin);
  }
  
  try {
    // 解析請求數據
    const requestData = await request.json();
    
    // ✅ 驗證模型名稱
    if (requestData.model && !SUPPORTED_MODELS.includes(requestData.model)) {
      console.warn(`⚠️  不支持的模型: ${requestData.model}`);
      console.warn(`   支持的模型: ${SUPPORTED_MODELS.join(', ')}`);
    }
    
    // ✅ 記錄請求詳情（包括模型名稱）
    console.log('📥 收到 DeepSeek 請求:', {
      origin,
      model: requestData.model || 'deepseek-chat',
      hasMessages: !!requestData.messages,
      messageCount: requestData.messages?.length || 0,
      hasImages: requestData.messages?.some(m => 
        Array.isArray(m.content) && 
        m.content.some(c => c.type === 'image_url')
      ),
      timestamp: new Date().toISOString()
    });
    
    // ⚠️  警告：DeepSeek API 不支持圖片輸入
    if (requestData.messages?.some(m => 
      Array.isArray(m.content) && 
      m.content.some(c => c.type === 'image_url')
    )) {
      console.warn('⚠️  警告：DeepSeek API 不支持圖片輸入！請使用 Vision API OCR 先提取文本。');
    }
    
    // 調用 DeepSeek API
    const deepseekResponse = await fetch(DEEPSEEK_API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify(requestData)
    });
    
    const responseData = await deepseekResponse.json();
    
    // ✅ 記錄響應詳情（包括 token 用量）
    console.log('📤 DeepSeek 響應:', {
      model: requestData.model,
      status: deepseekResponse.status,
      ok: deepseekResponse.ok,
      hasChoices: !!responseData.choices,
      usage: responseData.usage ? {
        prompt_tokens: responseData.usage.prompt_tokens,
        completion_tokens: responseData.usage.completion_tokens,
        total_tokens: responseData.usage.total_tokens,
        // ✅ 根據官方定價計算成本
        // 輸入: ¥2/百萬tokens (緩存未命中) 或 ¥0.2/百萬tokens (緩存命中)
        // 輸出: ¥3/百萬tokens
        estimated_cost_cny: (
          (responseData.usage.prompt_tokens / 1000000 * 2) + 
          (responseData.usage.completion_tokens / 1000000 * 3)
        ).toFixed(4)
      } : null,
      timestamp: new Date().toISOString()
    });
    
    // 檢查是否有錯誤
    if (!deepseekResponse.ok) {
      console.error('❌ DeepSeek API 錯誤:', {
        model: requestData.model,
        status: deepseekResponse.status,
        error: responseData
      });
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'DeepSeek API 錯誤',
        model: requestData.model,
        status: deepseekResponse.status,
        details: responseData
      }), {
        status: deepseekResponse.status,
        headers: { 'Content-Type': 'application/json' }
      }), origin);
    }
    
    // 返回成功響應
    const successResponse = new Response(JSON.stringify(responseData), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
    
    return addCORSHeaders(successResponse, origin);
    
  } catch (error) {
    console.error('❌ Worker 錯誤:', error);
    
    const errorResponse = new Response(JSON.stringify({
      error: 'Worker 內部錯誤',
      message: error.message,
      stack: error.stack
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
    
    return addCORSHeaders(errorResponse, origin);
  }
}

// 監聽請求
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});
```

### 步驟 3：保存並部署

1. 點擊 "Save and Deploy"
2. 等待 5-10 秒
3. 確認看到 "Deployed" 狀態

### 步驟 4：測試 Worker

在終端運行：

```bash
curl https://deepseek-proxy.vaultcaddy.workers.dev
```

**預期結果**：
```json
{
  "error": "Method not allowed",
  "message": "只支持 POST 請求"
}
```

✅ 如果看到這個，說明 Worker 已成功部署！

---

## 🧪 測試完整流程

### 步驟 5：清除瀏覽器緩存

**重要**：必須清除緩存以加載最新代碼！

```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

### 步驟 6：打開測試頁面

```
https://vaultcaddy.com/firstproject.html
```

### 步驟 7：檢查控制台日誌

打開瀏覽器控制台（F12），應該看到：

```
🔄 立即初始化混合處理器...
✅ 混合處理器已初始化
   ✅ Vision API OCR + DeepSeek 文本處理

🧠 智能處理器初始化
   🔄 使用: Vision API OCR + DeepSeek Reasoner (思考模式)
   ❌ 已禁用: OpenAI, Gemini, 其他 AI
```

✅ 如果看到這些日誌，說明系統初始化成功！

### 步驟 8：上傳測試發票

1. 點擊 "Upload files"
2. 選擇 "Invoice"
3. 選擇測試圖片
4. 點擊 "確定"

**預期日誌**：

```
🚀 混合處理器開始處理: invoice.jpg (invoice)

📸 步驟 1/2: 使用 Vision API 進行 OCR...
✅ OCR 完成，耗時: 1500ms
📄 提取的文本長度: 1234 字符

🤖 步驟 2/2: 使用 DeepSeek 處理文本...
✅ DeepSeek 處理完成，耗時: 2000ms

🎉 混合處理完成，總耗時: 3500ms
```

---

## 🔍 故障排除

### 問題 1：Worker 仍然返回 404

**原因**：Worker 未正確部署

**解決方案**：
1. 確認 Worker 名稱是 `deepseek-proxy`
2. 確認 URL 是 `https://deepseek-proxy.vaultcaddy.workers.dev`
3. 重新部署 Worker

### 問題 2：控制台沒有初始化日誌

**原因**：瀏覽器緩存未清除

**解決方案**：
1. 強制刷新（Ctrl+Shift+R）
2. 或清除瀏覽器緩存
3. 或使用無痕模式

### 問題 3：Vision API 錯誤

**原因**：Google Vision API Key 無效或未設置

**解決方案**：
1. 檢查 `config.js` 中的 API Key
2. 確認 API Key 有效
3. 確認 Vision API 已啟用

### 問題 4：DeepSeek API 錯誤

**原因**：DeepSeek API Key 無效或請求格式錯誤

**解決方案**：
1. 檢查 Worker 中的 API Key：`sk-4a43b49a13a840009052be65f599b7a4`
2. 確認使用 `deepseek-reasoner` 模型
3. 查看 Worker 日誌了解詳細錯誤

---

## ✅ 驗證清單

- [ ] Cloudflare Worker 已更新
- [ ] Worker 測試通過（curl 命令）
- [ ] 瀏覽器緩存已清除
- [ ] 控制台顯示初始化日誌
- [ ] 可以上傳文件
- [ ] OCR 正常工作
- [ ] DeepSeek 正常工作
- [ ] 數據顯示在表格中

---

## 📞 需要幫助？

如果問題仍然存在，請提供：

1. **Worker 測試結果**：
   ```bash
   curl https://deepseek-proxy.vaultcaddy.workers.dev
   ```

2. **瀏覽器控制台日誌**：
   - 打開 F12
   - 複製所有日誌
   - 特別是紅色錯誤信息

3. **上傳測試結果**：
   - 上傳發票後的控制台日誌
   - 是否有錯誤信息

---

**最後更新**：2025-10-27  
**狀態**：🚨 緊急修復  
**預計時間**：5-10 分鐘

