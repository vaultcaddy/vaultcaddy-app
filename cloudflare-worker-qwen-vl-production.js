/**
 * Cloudflare Worker - Qwen-VL Max API 代理
 * 
 * 功能：
 * - 代理 Qwen-VL Max API 請求
 * - 添加 CORS 頭
 * - 錯誤處理
 * - 超時控制（240 秒，支持大型文档）
 * 
 * 部署到：https://deepseek-proxy.vaultcaddy.workers.dev
 * (保持原URL不变，避免修改前端代码)
 * 
 * @version 3.0.0 (Qwen-VL Max)
 * @updated 2026-01-07
 */

// =====================================================
// Qwen-VL Max API 配置
// =====================================================

// Qwen-VL Max API Key (阿里云百炼)
const QWEN_API_KEY = 

// Qwen-VL API 端点 (新加坡地域 - 国际版)
const QWEN_API_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions';

// 支持的模型列表
const SUPPORTED_MODELS = [
    'qwen3-vl-plus-2025-12-19',  // ⭐ 推荐（最新、最全能）
    'qwen-vl-plus',              // 通用版本
    'qwen-vl-max',               // 高级版本
    'qwen-vl-ocr-2025-11-20'     // 纯 OCR 版本
];

// 默认模型
const DEFAULT_MODEL = 'qwen3-vl-plus-2025-12-19';

// CORS 配置
const CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
};

// =====================================================
// Worker 主函数
// =====================================================

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
                service: 'Qwen-VL Max Proxy',
                version: '3.0.0',
                processor: 'qwen-vl-max',
                supported_models: SUPPORTED_MODELS,
                default_model: DEFAULT_MODEL,
                max_timeout: '240 seconds',
                updated: '2026-01-07',
                note: '已从 DeepSeek 切换到 Qwen-VL Max，提供端到端 OCR + AI 分析'
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
        console.log('📥 收到請求:', {
            model: requestBody.model,
            messageCount: requestBody.messages?.length,
            hasImages: requestBody.messages?.some(m => 
                Array.isArray(m.content) && 
                m.content.some(c => c.type === 'image_url')
            )
        });
        
        // 2. 驗證和設置模型
        let model = requestBody.model || DEFAULT_MODEL;
        
        // 如果請求使用舊的 deepseek 模型，自動轉換為 Qwen-VL
        if (model === 'deepseek-chat' || model === 'deepseek-reasoner') {
            console.log(`⚠️ 檢測到舊模型 "${model}"，自動轉換為 ${DEFAULT_MODEL}`);
            model = DEFAULT_MODEL;
        }
        
        // 驗證模型
        if (!SUPPORTED_MODELS.includes(model)) {
            console.error(`❌ 不支持的模型: ${model}`);
            return new Response(JSON.stringify({
                error: '不支持的模型',
                message: `模型 "${model}" 不在支持列表中。`,
                supportedModels: SUPPORTED_MODELS,
                defaultModel: DEFAULT_MODEL
            }), {
                status: 400,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        console.log(`✅ 使用模型: ${model}`);
        
        // 3. 構建 Qwen-VL API 請求
        const qwenRequestBody = {
            model: model,
            messages: requestBody.messages,
            temperature: requestBody.temperature || 0.1,
            max_tokens: requestBody.max_tokens || 4000,
            stream: false  // 不使用流式輸出
        };
        
        console.log('📊 請求參數:', {
            model: qwenRequestBody.model,
            temperature: qwenRequestBody.temperature,
            max_tokens: qwenRequestBody.max_tokens
        });
        
        // 4. 調用 Qwen-VL API（添加超時控制）
        console.log('🚀 調用 Qwen-VL Max API...');
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            console.error('⏰ Worker 超時（240 秒）');
            controller.abort();
        }, 240000); // ✅ 240 秒超時（4 分鐘，支持大型文檔）
        
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
        
        // 5. 處理響應
        if (!qwenResponse.ok) {
            const errorText = await qwenResponse.text();
            console.error(`❌ Qwen-VL API 錯誤: ${qwenResponse.status}`);
            console.error(`錯誤內容: ${errorText}`);
            
            let errorData;
            try {
                errorData = JSON.parse(errorText);
            } catch {
                errorData = { message: errorText };
            }
            
            return new Response(JSON.stringify({
                error: 'Qwen-VL API 錯誤',
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
        
        // 6. 返回成功響應
        const responseData = await qwenResponse.json();
        console.log('✅ Qwen-VL API 請求成功');
        console.log(`📊 使用情況:`, {
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
        console.error('❌ Worker 內部錯誤:', error);
        
        // 處理超時錯誤
        if (error.name === 'AbortError') {
            return new Response(JSON.stringify({
                error: 'Worker 超時',
                message: 'Qwen-VL API 請求超時（240 秒），請稍後重試。',
                code: 'TIMEOUT'
            }), {
                status: 504,
                headers: {
                    'Content-Type': 'application/json',
                    ...CORS_HEADERS
                }
            });
        }
        
        // 處理其他錯誤
        return new Response(JSON.stringify({
            error: 'Worker 內部錯誤',
            message: error.message || 'Network connection lost.',
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
// 部署說明
// =====================================================

/**
 * 部署步驟：
 * 
 * 1. 登錄 Cloudflare Dashboard: https://dash.cloudflare.com/
 * 2. 進入 Workers & Pages
 * 3. 找到 "deepseek-proxy" Worker
 * 4. 點擊 "Edit Code"
 * 5. 複製本文件的全部內容
 * 6. 粘貼並替換所有現有代碼
 * 7. 點擊 "Save and Deploy"
 * 8. 測試 Worker URL: https://deepseek-proxy.vaultcaddy.workers.dev
 * 
 * 測試命令：
 * curl https://deepseek-proxy.vaultcaddy.workers.dev
 * 
 * 預期響應：
 * {
 *   "status": "ok",
 *   "service": "Qwen-VL Max Proxy",
 *   "version": "3.0.0",
 *   "processor": "qwen-vl-max",
 *   ...
 * }
 * 
 * 注意事項：
 * - Worker URL 保持不變（deepseek-proxy），避免修改前端代碼
 * - 自動兼容舊的 deepseek-chat 模型請求（自動轉換為 qwen-vl）
 * - 超時時間從 120 秒增加到 240 秒，支持大型文檔
 * - 已移除 Google Vision API，使用 Qwen-VL 端到端處理
 */

