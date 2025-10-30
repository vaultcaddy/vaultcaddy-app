/**
 * Cloudflare Worker - Hugging Face Inference API Proxy
 * 
 * 用途：繞過 CORS 限制，安全地調用 Hugging Face Inference API
 * 保護：Hugging Face Access Token 不會暴露在客戶端
 * 部署：https://workers.cloudflare.com/
 * 
 * 支持的模型：
 * - llava-hf/llava-1.5-7b-hf（LLaVA 1.5 7B 視覺語言模型）✅ 推薦
 * - 其他 Hugging Face 視覺模型
 * 
 * 最後更新：2025-10-30
 */

// ⚠️ 配置：請在部署到 Cloudflare 時設置您的 Token
// 部署步驟：
// 1. 登入 Cloudflare Dashboard
// 2. 創建新 Worker: huggingface-proxy
// 3. 將此代碼複製到 Worker
// 4. 將第22行的 YOUR_HUGGINGFACE_TOKEN_HERE 替換為實際 Token
// 5. 點擊「Save and Deploy」
const HUGGINGFACE_TOKEN = 'YOUR_HUGGINGFACE_TOKEN_HERE'; // ⚠️ 在 Cloudflare Worker 中替換為實際 Token
const DEFAULT_MODEL = 'llava-hf/llava-1.5-7b-hf'; // ✅ LLaVA 1.5 7B

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
    
    // 獲取模型 ID（使用默認模型如果未指定）
    const modelId = requestData.model || DEFAULT_MODEL;
    const apiUrl = `https://api-inference.huggingface.co/models/${modelId}`;
    
    // 記錄請求詳情
    console.log('📥 收到 Hugging Face 請求:', {
      origin,
      model: modelId,
      hasInputs: !!requestData.inputs,
      timestamp: new Date().toISOString()
    });
    
    // 構建請求體（移除 model 字段，因為它在 URL 中）
    const hfRequestBody = {
      inputs: requestData.inputs,
      parameters: requestData.parameters || {}
    };
    
    // 調用 Hugging Face Inference API
    const hfResponse = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${HUGGINGFACE_TOKEN}`
      },
      body: JSON.stringify(hfRequestBody)
    });
    
    // 讀取原始響應文本
    const responseText = await hfResponse.text();
    console.log('📄 Hugging Face 原始響應長度:', responseText.length);
    
    // 嘗試解析 JSON
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (parseError) {
      console.error('❌ Hugging Face 返回無效 JSON!');
      console.error('   原始響應:', responseText.substring(0, 500));
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'Hugging Face 返回無效 JSON',
        details: responseText.substring(0, 500),
        parseError: parseError.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }), origin);
    }
    
    // 記錄響應詳情
    console.log('📤 Hugging Face 響應:', {
      model: modelId,
      status: hfResponse.status,
      ok: hfResponse.ok,
      hasData: !!responseData,
      timestamp: new Date().toISOString()
    });
    
    if (!hfResponse.ok) {
      console.error('❌ Hugging Face API 錯誤:', {
        model: modelId,
        status: hfResponse.status,
        error: responseData
      });
      
      return addCORSHeaders(new Response(JSON.stringify({
        error: 'Hugging Face API 錯誤',
        model: modelId,
        status: hfResponse.status,
        details: responseData
      }), {
        status: hfResponse.status,
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

