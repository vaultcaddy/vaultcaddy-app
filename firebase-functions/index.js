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
const stripe = require('stripe')(functions.config().stripe?.secret || process.env.STRIPE_SECRET_KEY);

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

// =====================================================
// Stripe Checkout Session 創建函數
// =====================================================

/**
 * 2026-01-29 新定價結構的 Price ID 映射
 * 根據語言自動選擇對應幣種的 Price ID
 */
const PRICE_IDS = {
    monthly: {
        hkd: 'price_1SuruFJmiQ31C0GTdJxUaknj',  // HKD $38/月
        usd: 'price_1SuruGJmiQ31C0GThdoiTbTM',  // USD $4.88/月
        jpy: 'price_1SuruGJmiQ31C0GTGQVpiEuP',  // JPY ¥788/月
        krw: 'price_1SuruGJmiQ31C0GTpBz3jbMo'   // KRW ₩6,988/月
    },
    yearly: {
        hkd: 'price_1SuruEJmiQ31C0GTWqMAZeuM',  // HKD $336/年 ($28/月)
        usd: 'price_1SuruEJmiQ31C0GTBVhLSAtA',  // USD $42.96/年 ($3.58/月)
        jpy: 'price_1SuruEJmiQ31C0GTde3o97rx',  // JPY ¥7056/年 (¥588/月)
        krw: 'price_1SuruFJmiQ31C0GTUL0Yxltm'   // KRW ₩62,256/年 (₩5,188/月)
    }
};

/**
 * 根據請求來源判斷幣種
 * @param {string} referer - 請求來源 URL
 * @returns {string} 幣種代碼 (hkd, usd, jpy, krw)
 */
function getCurrencyFromReferer(referer) {
    if (!referer) return 'hkd';  // 默認中文版 = HKD
    
    if (referer.includes('/en/')) return 'usd';
    if (referer.includes('/jp/')) return 'jpy';
    if (referer.includes('/kr/')) return 'krw';
    
    return 'hkd';  // 默認中文版
}

exports.createStripeCheckoutSession = functions
    .runWith({
        timeoutSeconds: 60,
        memory: '256MB'
    })
    .https.onCall(async (data, context) => {
        try {
            // 驗證用戶已登錄
            if (!context.auth) {
                throw new functions.https.HttpsError(
                    'unauthenticated',
                    'User must be logged in to create checkout session'
                );
            }

            const { planType, successUrl, cancelUrl, currency } = data;
            
            console.log(`🛒 創建 Checkout Session: planType=${planType}, currency=${currency}`);

            // 驗證計劃類型
            if (!['monthly', 'yearly'].includes(planType)) {
                throw new functions.https.HttpsError(
                    'invalid-argument',
                    'Invalid plan type. Must be "monthly" or "yearly"'
                );
            }

            // 獲取對應的 Price ID（優先使用傳入的幣種，否則默認 HKD）
            const currencyCode = currency || 'hkd';
            const priceId = PRICE_IDS[planType][currencyCode];

            if (!priceId) {
                throw new functions.https.HttpsError(
                    'not-found',
                    `No price ID found for ${planType} plan in ${currencyCode}`
                );
            }

            console.log(`💳 使用 Price ID: ${priceId} (${currencyCode.toUpperCase()})`);

            // 創建 Stripe Checkout Session
            const session = await stripe.checkout.sessions.create({
                payment_method_types: ['card'],
                line_items: [{
                    price: priceId,
                    quantity: 1,
                }],
                mode: 'subscription',
                success_url: successUrl || `${process.env.SITE_URL || 'https://vaultcaddy.com'}/account.html?payment=success&session_id={CHECKOUT_SESSION_ID}`,
                cancel_url: cancelUrl || `${process.env.SITE_URL || 'https://vaultcaddy.com'}/billing.html?payment=cancelled`,
                client_reference_id: context.auth.uid,
                customer_email: context.auth.token.email || undefined,
                metadata: {
                    userId: context.auth.uid,
                    planType: planType,
                    currency: currencyCode
                },
                subscription_data: {
                    metadata: {
                        userId: context.auth.uid,
                        planType: planType,
                        currency: currencyCode
                    }
                }
            });

            console.log(`✅ Checkout Session 創建成功: ${session.id}`);

            return {
                sessionId: session.id,
                url: session.url
            };

        } catch (error) {
            console.error('❌ 創建 Checkout Session 失敗:', error.message);
            throw new functions.https.HttpsError(
                'internal',
                `Failed to create checkout session: ${error.message}`
            );
        }
    });
