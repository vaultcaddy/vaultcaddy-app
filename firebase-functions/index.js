/**
 * Firebase Cloud Function - Qwen-VL Max API 代理
 * 
 * 用途：
 * - 隐藏 Qwen-VL Max API Key (安全)
 * - 处理 CORS 跨域请求
 * - 🔥 無超時問題（最長可設 9 分鐘）
 * 
 * @version 1.0.0
 * @created 2026-01-27
 */

const functions = require('firebase-functions');
const cors = require('cors')({ origin: true });
const fetch = require('node-fetch');

// =====================================================
// 配置区域
// =====================================================

const QWEN_API_KEY = 'sk-b4016d4560e44c6b925217578004aa9c';
const QWEN_API_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions';

const SUPPORTED_MODELS = [
    'qwen3-vl-plus-2025-12-19',
    'qwen-vl-plus',
    'qwen-vl-max',
    'qwen-vl-ocr-2025-11-20'
];

// =====================================================
// Firebase Function（設置 5 分鐘超時，512MB 內存）
// =====================================================

exports.qwenProxy = functions
    .runWith({
        timeoutSeconds: 300,  // 5 分鐘超時
        memory: '512MB'       // 512MB 內存（處理大型圖片）
    })
    .https.onRequest((req, res) => {
        return cors(req, res, async () => {
            // OPTIONS 預檢請求
            if (req.method === 'OPTIONS') {
                res.status(204).send('');
                return;
            }

            // 只接受 POST 請求
            if (req.method !== 'POST') {
                res.status(405).json({ error: 'Method not allowed' });
                return;
            }

            try {
                const requestBody = req.body;
                const model = requestBody.model;

                console.log(`📥 收到請求: model=${model}`);

                // 驗證模型
                if (!SUPPORTED_MODELS.includes(model)) {
                    res.status(400).json({
                        error: '不支持的模型',
                        supportedModels: SUPPORTED_MODELS
                    });
                    return;
                }

                // 構建 Qwen API 請求
                const qwenRequestBody = {
                    model: model,
                    messages: requestBody.messages,
                    temperature: requestBody.temperature || 0.1,
                    max_tokens: Math.min(requestBody.max_tokens || 28000, 28000),
                    stream: false  // Firebase Function 使用非流式模式
                };

                console.log(`🚀 調用 Qwen API...`);
                const startTime = Date.now();

                const qwenResponse = await fetch(QWEN_API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${QWEN_API_KEY}`
                    },
                    body: JSON.stringify(qwenRequestBody)
                });

                const duration = Date.now() - startTime;
                console.log(`⏱️ API 響應時間: ${duration}ms`);

                if (!qwenResponse.ok) {
                    const errorText = await qwenResponse.text();
                    console.error(`❌ Qwen API 錯誤: ${qwenResponse.status}`);
                    res.status(qwenResponse.status).json({
                        error: `Qwen API 錯誤: ${qwenResponse.status}`,
                        details: errorText
                    });
                    return;
                }

                const data = await qwenResponse.json();
                console.log(`✅ 完成: tokens=${data.usage?.total_tokens || 'N/A'}`);

                res.status(200).json(data);

            } catch (error) {
                console.error('❌ Function 錯誤:', error.message);
                res.status(500).json({
                    error: 'Function 處理失敗',
                    message: error.message
                });
            }
        });
    });
