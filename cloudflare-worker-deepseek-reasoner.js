/**
 * Cloudflare Worker for DeepSeek API Proxy
 * 
 * 支持模型：
 * - deepseek-chat
 * - deepseek-reasoner ✅ 新增
 * 
 * 功能：
 * - 代理 DeepSeek API 請求
 * - 添加 CORS 頭
 * - 錯誤處理
 * - 超時控制（60 秒）
 * 
 * 部署到：https://deepseek-proxy.vaultcaddy.workers.dev
 * 
 * @version 2.0.0
 * @updated 2025-11-16
 */

// DeepSeek API 配置
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';
const DEEPSEEK_API_KEY = 'YOUR_DEEPSEEK_API_KEY'; // ⚠️ 請替換為您的 API Key

// 支持的模型列表
const SUPPORTED_MODELS = [
    'deepseek-chat',
    'deepseek-reasoner' // ✅ 新增支持
];

// CORS 配置
const CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
};

/**
 * 處理 OPTIONS 請求（CORS 預檢）
 */
function handleOptions() {
    return new Response(null, {
        status: 204,
        headers: CORS_HEADERS
    });
}

/**
 * 處理 POST 請求
 */
async function handlePost(request) {
    try {
        // 1. 解析請求體
        const requestBody = await request.json();
        console.log('📥 收到請求:', JSON.stringify(requestBody, null, 2));
        
        // 2. 驗證模型
        const model = requestBody.model;
        if (!SUPPORTED_MODELS.includes(model)) {
            console.error(`❌ 不支持的模型: ${model}`);
            return new Response(JSON.stringify({
                error: '不支持的模型',
                message: `模型 "${model}" 不在支持列表中。支持的模型: ${SUPPORTED_MODELS.join(', ')}`
            }), {
                status: 400,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        console.log(`✅ 使用模型: ${model}`);
        
        // 3. 驗證 max_tokens（重要！）
        const maxTokens = requestBody.max_tokens || 4096;
        console.log(`📊 max_tokens: ${maxTokens}`);
        
        // 4. 調用 DeepSeek API（添加超時控制）
        console.log('🚀 調用 DeepSeek API...');
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            console.error('⏰ Worker 超時（60 秒）');
            controller.abort();
        }, 60000); // ✅ 60 秒超時（與前端一致）
        
        const deepseekResponse = await fetch(DEEPSEEK_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
            },
            body: JSON.stringify({
                model: requestBody.model,
                messages: requestBody.messages,
                temperature: requestBody.temperature || 0.1,
                max_tokens: maxTokens, // ✅ 使用請求中的 max_tokens
                stream: false // 不使用流式輸出
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        // 5. 處理響應
        if (!deepseekResponse.ok) {
            const errorText = await deepseekResponse.text();
            console.error(`❌ DeepSeek API 錯誤: ${deepseekResponse.status}`);
            console.error(`錯誤內容: ${errorText}`);
            
            let errorData;
            try {
                errorData = JSON.parse(errorText);
            } catch {
                errorData = { message: errorText };
            }
            
            return new Response(JSON.stringify({
                error: 'DeepSeek API 錯誤',
                status: deepseekResponse.status,
                message: errorData.message || errorText
            }), {
                status: deepseekResponse.status,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 6. 返回成功響應
        const responseData = await deepseekResponse.json();
        console.log('✅ DeepSeek API 請求成功');
        console.log(`📊 輸出 tokens: ${responseData.usage?.completion_tokens || 'N/A'}`);
        
        return new Response(JSON.stringify(responseData), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
        
    } catch (error) {
        console.error('❌ Worker 內部錯誤:', error);
        
        // 處理超時錯誤
        if (error.name === 'AbortError') {
            return new Response(JSON.stringify({
                error: 'Worker 超時',
                message: '請求超過 60 秒限制，已中止。'
            }), {
                status: 504,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 處理網絡錯誤
        return new Response(JSON.stringify({
            error: 'Worker 內部錯誤',
            message: error.message || 'Network connection lost.'
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
    }
}

/**
 * 主處理函數
 */
export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        
        console.log(`📨 收到請求: ${request.method} ${url.pathname}`);
        
        // 處理 OPTIONS 請求（CORS 預檢）
        if (request.method === 'OPTIONS') {
            return handleOptions();
        }
        
        // 處理 POST 請求
        if (request.method === 'POST') {
            return handlePost(request);
        }
        
        // 處理 GET 請求（健康檢查）
        if (request.method === 'GET') {
            return new Response(JSON.stringify({
                status: 'ok',
                version: '2.0.0',
                supported_models: SUPPORTED_MODELS,
                max_timeout: '60 seconds',
                updated: '2025-11-16'
            }), {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 不支持的方法
        return new Response(JSON.stringify({
            error: '不支持的方法',
            message: `方法 "${request.method}" 不被支持。支持的方法: GET, POST, OPTIONS`
        }), {
            status: 405,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
    }
};

