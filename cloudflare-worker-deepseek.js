/**
 * Cloudflare Worker - DeepSeek API Proxy
 * 
 * ✅ 用於 VaultCaddy Vision OCR + DeepSeek Chat 混合處理器
 * ✅ 模型：deepseek-chat（文本分析）
 * ✅ 部署：https://deepseek-proxy.vaultcaddy.workers.dev
 * 
 * 工作流程：
 * 1. Vision API 提取文本（OCR）
 * 2. DeepSeek Chat 分析文本並提取結構化數據
 * 
 * 最後更新：2025-10-30
 */

// ✅ DeepSeek API Key（已配置）
const DEEPSEEK_API_KEY = 'sk-258e40c87c4d47d08e62cd18d4bbfc0c';
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';
const DEFAULT_MODEL = 'deepseek-chat'; // ✅ 使用 deepseek-chat（文本分析）

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
      'Access-Control-Max-Age': '86400',
    }
  });
}

/**
 * 添加 CORS 頭
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
    
    // 獲取模型（默認使用 deepseek-chat）
    const model = requestData.model || DEFAULT_MODEL;
    
    console.log('📥 收到 DeepSeek 請求:', {
      origin,
      model: model,
      hasMessages: !!requestData.messages,
      timestamp: new Date().toISOString()
    });
    
    // 構建 DeepSeek API 請求
    const deepseekRequestBody = {
      model: model,
      messages: requestData.messages,
      temperature: requestData.temperature || 0.1,
      max_tokens: requestData.max_tokens || 4096,
      top_p: requestData.top_p || 0.95,
      stream: false
    };
    
    console.log('📤 發送到 DeepSeek API:', {
      model: model,
      messageCount: requestData.messages?.length || 0
    });
    
    // 調用 DeepSeek API
    const deepseekResponse = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify(deepseekRequestBody)
    });
    
    // 讀取原始響應文本
    const responseText = await deepseekResponse.text();
    console.log('📄 DeepSeek 原始響應:', {
      status: deepseekResponse.status,
      length: responseText.length,
      preview: responseText.substring(0, 200)
    });
    
    // 嘗試解析 JSON
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (parseError) {
      console.error('❌ DeepSeek 返回無效 JSON!');
      console.error('   原始響應:', responseText.substring(0, 500));
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'DeepSeek 返回無效 JSON',
        details: responseText.substring(0, 500),
        parseError: parseError.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }), origin);
    }
    
    // 記錄響應詳情
    console.log('📤 DeepSeek 響應:', {
      model: model,
      status: deepseekResponse.status,
      ok: deepseekResponse.ok,
      hasData: !!responseData,
      timestamp: new Date().toISOString()
    });
    
    if (!deepseekResponse.ok) {
      console.error('❌ DeepSeek API 錯誤:', {
        model: model,
        status: deepseekResponse.status,
        error: responseData
      });
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'DeepSeek API 錯誤',
        model: model,
        status: deepseekResponse.status,
        details: responseData
      }), {
        status: deepseekResponse.status,
        headers: { 'Content-Type': 'application/json' }
      }), origin);
    }
    
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

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});
