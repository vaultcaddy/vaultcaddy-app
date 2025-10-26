/**
 * Cloudflare Worker - DeepSeek API 代理
 * 用途：繞過 CORS 限制，安全地調用 DeepSeek API
 * 部署：https://workers.cloudflare.com/
 */

// 配置
const DEEPSEEK_API_KEY = 'sk-4a43b49a13a840009052be65f599b7a4'; // ✅ DeepSeek API Key（已更新）
const DEEPSEEK_API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

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
    return new Response(JSON.stringify({ 
      error: 'Method not allowed',
      message: '只支持 POST 請求'
    }), { 
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  try {
    // 解析請求體
    const requestData = await request.json();
    
    console.log('📥 收到 DeepSeek 請求:', {
      origin,
      timestamp: new Date().toISOString(),
      hasMessages: !!requestData.messages
    });
    
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
    
    console.log('📤 DeepSeek 響應:', {
      status: deepseekResponse.status,
      ok: deepseekResponse.ok,
      timestamp: new Date().toISOString()
    });
    
    // 檢查是否有錯誤
    if (!deepseekResponse.ok) {
      console.error('❌ DeepSeek API 錯誤:', responseData);
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'DeepSeek API 錯誤',
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

