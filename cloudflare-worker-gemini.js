/**
 * Cloudflare Worker - Gemini API 代理
 * 用途：繞過 CORS 限制，安全地調用 Google Gemini API
 * 部署：https://workers.cloudflare.com/
 */

// 配置
const GEMINI_API_KEY = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug'; // 你的 Gemini API Key
const GEMINI_API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';

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
    
    console.log('📥 收到請求:', {
      origin,
      timestamp: new Date().toISOString(),
      hasContents: !!requestData.contents
    });
    
    // 調用 Gemini API
    const geminiResponse = await fetch(`${GEMINI_API_ENDPOINT}?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Referer': 'https://vaultcaddy.com/',  // 添加 Referer 頭
      },
      body: JSON.stringify(requestData)
    });
    
    // 獲取響應
    const responseData = await geminiResponse.json();
    
    console.log('📤 Gemini 響應:', {
      status: geminiResponse.status,
      ok: geminiResponse.ok,
      timestamp: new Date().toISOString()
    });
    
    // 檢查是否有錯誤
    if (!geminiResponse.ok) {
      console.error('❌ Gemini API 錯誤:', responseData);
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'Gemini API 錯誤',
        status: geminiResponse.status,
        details: responseData
      }), {
        status: geminiResponse.status,
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

