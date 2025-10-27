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
  const allowedOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': allowedOrigin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400', // 24 hours
    }
  });
}

/**
 * 添加 CORS 頭到響應
 */
function addCORSHeaders(response, origin) {
  const allowedOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  
  const headers = new Headers(response.headers);
  headers.set('Access-Control-Allow-Origin', allowedOrigin);
  headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type');
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: headers
  });
}

/**
 * 主處理函數
 */
async function handleRequest(request) {
  const origin = request.headers.get('Origin');
  
  // 處理 OPTIONS 預檢請求
  if (request.method === 'OPTIONS') {
    return handleCORS(request);
  }
  
  // 只接受 POST 請求
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
    // 解析請求體
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
    
    // 獲取響應
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

/**
 * Cloudflare Workers 入口點
 */
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

