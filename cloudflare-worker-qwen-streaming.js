/**
 * Cloudflare Worker - Qwen-VL Max API 代理（流式響應版本）
 * 
 * 用途：
 * - 隐藏 Qwen-VL Max API Key (安全)
 * - 处理 CORS 跨域请求
 * - 🔥 流式響應避免超時問題
 * - 支持處理大型文檔（5+ 頁）
 * 
 * @version 2.0.0 - Streaming
 * @created 2026-01-27
 */

// =====================================================
// 配置区域
// =====================================================

const QWEN_API_KEY = 'YOUR_QWEN_API_KEY'; // 🔐 Replace with your actual API key
const QWEN_API_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions';

const SUPPORTED_MODELS = [
    'qwen3-vl-plus-2025-12-19',
    'qwen-vl-plus',
    'qwen-vl-max',
    'qwen-vl-ocr-2025-11-20'
];

const CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
};

// =====================================================
// Worker 主函数
// =====================================================

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
    if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
            status: 405,
            headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
        });
    }
    
    return await handlePost(request);
}

/**
 * 處理 POST 請求（支持流式響應）
 */
async function handlePost(request) {
    try {
        const requestBody = await request.json();
        const model = requestBody.model;
        const useStreaming = requestBody.stream === true;
        
        console.log(`📥 收到請求: model=${model}, streaming=${useStreaming}`);
        
        if (!SUPPORTED_MODELS.includes(model)) {
            return new Response(JSON.stringify({
                error: '不支持的模型',
                supportedModels: SUPPORTED_MODELS
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
            });
        }
        
        // 構建 Qwen API 請求
        const qwenRequestBody = {
            model: model,
            messages: requestBody.messages,
            temperature: requestBody.temperature || 0.1,
            max_tokens: Math.min(requestBody.max_tokens || 28000, 28000),
            stream: useStreaming  // 🔥 根據前端請求決定是否流式
        };
        
        console.log(`🚀 調用 Qwen API (streaming=${useStreaming})...`);
        
        const qwenResponse = await fetch(QWEN_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${QWEN_API_KEY}`
            },
            body: JSON.stringify(qwenRequestBody)
        });
        
        if (!qwenResponse.ok) {
            const errorText = await qwenResponse.text();
            console.error(`❌ Qwen API 錯誤: ${qwenResponse.status}`);
            return new Response(JSON.stringify({
                error: `Qwen API 錯誤: ${qwenResponse.status}`,
                details: errorText
            }), {
                status: qwenResponse.status,
                headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
            });
        }
        
        // 🔥 流式響應模式
        if (useStreaming) {
            console.log('📡 開始流式轉發...');
            
            // 直接轉發流式響應
            return new Response(qwenResponse.body, {
                status: 200,
                headers: {
                    'Content-Type': 'text/event-stream',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 非流式模式（原有邏輯）
        const data = await qwenResponse.json();
        console.log(`✅ 完成: tokens=${data.usage?.total_tokens || 'N/A'}`);
        
        return new Response(JSON.stringify(data), {
            status: 200,
            headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
        });
        
    } catch (error) {
        console.error('❌ Worker 錯誤:', error.message);
        return new Response(JSON.stringify({
            error: 'Worker 處理失敗',
            message: error.message
        }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...CORS_HEADERS }
        });
    }
}

