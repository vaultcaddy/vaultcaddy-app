/**
 * Cloudflare Worker - Claude Vision API Proxy
 * 
 * 用途：繞過 CORS 限制，安全地調用 Claude API
 * 部署：https://workers.cloudflare.com/
 * 
 * 模型：
 * - claude-3-5-sonnet-20241022: 最高準確度（95-98%）
 * - claude-3-haiku-20240307: 經濟型（90-93%）
 * 
 * 成本：
 * - Claude 3.5 Sonnet: $3/1M 輸入, $15/1M 輸出
 * - Claude 3 Haiku: $0.25/1M 輸入, $1.25/1M 輸出
 * 
 * 最後更新：2025-10-28
 */

// ⚠️ 配置：請在 Cloudflare Workers 環境變量中設置 CLAUDE_API_KEY
// 或直接在這裡設置（不推薦用於生產環境）
const CLAUDE_API_KEY = 'YOUR_CLAUDE_API_KEY_HERE';
const CLAUDE_API_ENDPOINT = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';

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
    
    // 記錄請求詳情
    console.log('📥 收到 Claude 請求:', {
      origin,
      model: requestData.model || 'claude-3-5-sonnet-20241022',
      hasMessages: !!requestData.messages,
      messageCount: requestData.messages?.length || 0,
      timestamp: new Date().toISOString()
    });
    
    // 檢查是否有圖片
    const hasImage = requestData.messages?.some(m =>
      Array.isArray(m.content) &&
      m.content.some(c => c.type === 'image')
    );
    console.log('📸 包含圖片:', hasImage);
    
    // 調用 Claude API
    const claudeResponse = await fetch(CLAUDE_API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': ANTHROPIC_VERSION
      },
      body: JSON.stringify(requestData)
    });
    
    // 讀取原始響應文本
    const responseText = await claudeResponse.text();
    console.log('📄 Claude 原始響應長度:', responseText.length);
    
    // 嘗試解析 JSON
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (parseError) {
      console.error('❌ Claude 返回無效 JSON!');
      console.error('   原始響應:', responseText.substring(0, 500));
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'Claude 返回無效 JSON',
        details: responseText.substring(0, 500),
        parseError: parseError.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }), origin);
    }
    
    // 記錄響應詳情
    console.log('📤 Claude 響應:', {
      model: responseData.model,
      status: claudeResponse.status,
      ok: claudeResponse.ok,
      hasContent: !!responseData.content,
      usage: responseData.usage ? {
        input_tokens: responseData.usage.input_tokens,
        output_tokens: responseData.usage.output_tokens,
        // 計算成本（Claude 3.5 Sonnet）
        estimated_cost_usd: (
          (responseData.usage.input_tokens / 1000000 * 3) + 
          (responseData.usage.output_tokens / 1000000 * 15)
        ).toFixed(4)
      } : null,
      timestamp: new Date().toISOString()
    });
    
    if (!claudeResponse.ok) {
      console.error('❌ Claude API 錯誤:', {
        status: claudeResponse.status,
        error: responseData
      });
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'Claude API 錯誤',
        status: claudeResponse.status,
        details: responseData
      }), {
        status: claudeResponse.status,
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

