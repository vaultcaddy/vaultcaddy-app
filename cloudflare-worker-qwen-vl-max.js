/**
 * Cloudflare Worker - Qwen-VL Max API 代理
 * 
 * 用途：
 * - 隐藏 Qwen-VL Max API Key (安全)
 * - 处理 CORS 跨域请求
 * - 统一错误处理
 * - 请求日志记录
 * 
 * API 端点: https://qwen-vl-proxy.vaultcaddy.workers.dev
 * 
 * @version 1.0.0
 * @created 2026-01-07
 */

// =====================================================
// 配置区域 (在 Cloudflare Worker 环境变量中设置)
// =====================================================

// Qwen-VL Max API Key
// 获取方式：https://www.alibabacloud.com/ → Model Studio → API Keys
const QWEN_API_KEY = 'sk-b4016d4560e44c6b925217578004aa9c'; // ⚠️ 部署时应从环境变量读取

// Qwen-VL API 端点 (新加坡地域 - 国际版)
const QWEN_API_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions';

// 支持的模型
const SUPPORTED_MODELS = [
    'qwen3-vl-plus-2025-12-19',  // ⭐ 推荐（最新、最全能）
    'qwen-vl-plus',              // 通用版本
    'qwen-vl-max',               // 高级版本
    'qwen-vl-ocr-2025-11-20'     // 纯 OCR 版本
];

// CORS 头
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

/**
 * 处理请求
 */
async function handleRequest(request) {
    // 1. 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
        return handleOptions();
    }
    
    // 2. 只允许 POST 请求
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({
            error: 'Method not allowed',
            message: '只支持 POST 请求'
        }), {
            status: 405,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
    }
    
    // 3. 处理 POST 请求
    return await handlePost(request);
}

/**
 * 处理 OPTIONS 请求 (CORS 预检)
 */
function handleOptions() {
    return new Response(null, {
        status: 204,
        headers: CORS_HEADERS
    });
}

/**
 * 处理 POST 请求
 */
async function handlePost(request) {
    try {
        // 1. 解析请求体
        const requestBody = await request.json();
        console.log('📥 收到请求:', {
            model: requestBody.model,
            messageCount: requestBody.messages?.length,
            hasImages: requestBody.messages?.some(m => 
                Array.isArray(m.content) && 
                m.content.some(c => c.type === 'image_url')
            )
        });
        
        // 2. 验证模型
        const model = requestBody.model;
        if (!SUPPORTED_MODELS.includes(model)) {
            console.error(`❌ 不支持的模型: ${model}`);
            return new Response(JSON.stringify({
                error: '不支持的模型',
                message: `模型 "${model}" 不在支持列表中。支持的模型: ${SUPPORTED_MODELS.join(', ')}`,
                supportedModels: SUPPORTED_MODELS
            }), {
                status: 400,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        console.log(`✅ 使用模型: ${model}`);
        
        // 3. 构建 Qwen-VL API 请求
        const qwenRequestBody = {
            model: requestBody.model,
            messages: requestBody.messages,
            temperature: requestBody.temperature || 0.1,
            max_tokens: requestBody.max_tokens || 4000,
            stream: false  // 不使用流式输出
        };
        
        console.log('📊 请求参数:', {
            model: qwenRequestBody.model,
            temperature: qwenRequestBody.temperature,
            max_tokens: qwenRequestBody.max_tokens
        });
        
        // 4. 调用 Qwen-VL API (添加超时控制)
        console.log('🚀 调用 Qwen-VL API...');
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            console.log('⏰ Worker 超时 (240 秒)');
            controller.abort();
        }, 240000); // ✅ 240 秒超时 (4 分钟，支持大型文档)
        
        const qwenResponse = await fetch(QWEN_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${QWEN_API_KEY}`
            },
            body: JSON.stringify(qwenRequestBody),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        // 5. 处理响应
        if (!qwenResponse.ok) {
            const errorText = await qwenResponse.text();
            console.error(`❌ Qwen-VL API 错误: ${qwenResponse.status}`);
            console.error(`错误内容: ${errorText}`);
            
            let errorData;
            try {
                errorData = JSON.parse(errorText);
            } catch {
                errorData = { message: errorText };
            }
            
            return new Response(JSON.stringify({
                error: 'Qwen-VL API 错误',
                status: qwenResponse.status,
                message: errorData.message || errorData.error?.message || errorText,
                details: errorData
            }), {
                status: qwenResponse.status,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 6. 返回成功响应
        const responseData = await qwenResponse.json();
        console.log('✅ Qwen-VL API 请求成功');
        console.log(`📊 使用情况:`, {
            prompt_tokens: responseData.usage?.prompt_tokens || 'N/A',
            completion_tokens: responseData.usage?.completion_tokens || 'N/A',
            total_tokens: responseData.usage?.total_tokens || 'N/A'
        });
        
        return new Response(JSON.stringify(responseData), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
        
    } catch (error) {
        console.error('❌ Worker 错误:', error);
        
        // 处理超时错误
        if (error.name === 'AbortError') {
            return new Response(JSON.stringify({
                error: '请求超时',
                message: 'Qwen-VL API 请求超时 (240 秒)，请稍后重试',
                code: 'TIMEOUT'
            }), {
                status: 504,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 处理其他错误
        return new Response(JSON.stringify({
            error: 'Worker 内部错误',
            message: error.message,
            stack: error.stack
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                ...CORS_HEADERS
            }
        });
    }
}

// =====================================================
// 部署说明
// =====================================================

/**
 * Cloudflare Worker 部署步骤：
 * 
 * 1. 登录 Cloudflare Dashboard: https://dash.cloudflare.com/
 * 2. 进入 "Workers & Pages"
 * 3. 创建新 Worker，命名为: qwen-vl-proxy
 * 4. 复制本文件内容，粘贴到 Worker 编辑器
 * 5. (推荐) 在 Settings → Variables 中添加环境变量:
 *    - QWEN_API_KEY: sk-b4016d4560e44c6b925217578004aa9c
 * 6. 点击 "Save and Deploy"
 * 7. 复制 Worker URL (例如: https://qwen-vl-proxy.vaultcaddy.workers.dev)
 * 8. 在前端代码中使用此 URL
 * 
 * 环境变量配置 (推荐):
 * - 在 Worker Settings → Variables 中添加 QWEN_API_KEY
 * - 修改第16行为: const QWEN_API_KEY = env.QWEN_API_KEY;
 * - 这样 API Key 不会暴露在代码中
 * 
 * 测试 Worker:
 * curl -X POST https://qwen-vl-proxy.vaultcaddy.workers.dev \
 *   -H "Content-Type: application/json" \
 *   -d '{
 *     "model": "qwen3-vl-plus-2025-12-19",
 *     "messages": [
 *       {
 *         "role": "user",
 *         "content": [
 *           {"type": "text", "text": "Hello"}
 *         ]
 *       }
 *     ]
 *   }'
 */

