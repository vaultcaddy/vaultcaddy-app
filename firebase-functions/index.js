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
const admin = require('firebase-admin');
const cors = require('cors')({ origin: true });
const fetch = require('node-fetch');
const stripe = require('stripe')(functions.config().stripe?.secret || process.env.STRIPE_SECRET_KEY);

// 初始化 Firebase Admin
if (!admin.apps.length) {
    admin.initializeApp();
}

// =====================================================
// 配置区域
// =====================================================

// 🔐 從環境變數讀取 API Keys（安全）
const QWEN_API_KEY = functions.config().qwen?.api_key || process.env.QWEN_API_KEY;
const QWEN_API_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions';

const SUPPORTED_MODELS = [
    'qwen3-vl-plus-2025-12-19',
    'qwen3-vl-plus',  // 🔥 添加深度思考模型
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
                // 检查前端是否传入 extra_body（包含 enable_thinking）
                const extraBody = requestBody.extra_body || {};
                const enableThinking = extraBody.enable_thinking === true;
                
                // 深度思考模式最大4000 tokens（阿里云限制），标准模式最大28000
                const maxTokensLimit = enableThinking ? 4000 : 28000;
                
                const qwenRequestBody = {
                    model: model,
                    messages: requestBody.messages,
                    temperature: requestBody.temperature || 0.1,
                    max_tokens: Math.min(requestBody.max_tokens || maxTokensLimit, maxTokensLimit),
                    stream: false  // Firebase Function 使用非流式模式
                };
                
                // 🔥 如果啟用深度思考，添加 extra_body 參數（阿里云官方格式）
                if (enableThinking) {
                    qwenRequestBody.extra_body = {
                        enable_thinking: true,
                        thinking_budget: extraBody.thinking_budget || 4000
                    };
                    console.log(`   深度思考模式: ✅ 開啟 (max_tokens: ${qwenRequestBody.max_tokens}, thinking_budget: ${qwenRequestBody.extra_body.thinking_budget})`);
                } else {
                    console.log(`   標準模式 (max_tokens: ${qwenRequestBody.max_tokens})`);
                }

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
    },
    // 🔥 超額收費 Price ID (Usage-based Billing)
    overage: {
        monthly: 'price_1SfZQQJmiQ31C0GTeUu6TSXE',  // 月付超額收費: $0.3/頁
        yearly: 'price_1SfZQVJmiQ31C0GTOYgabmaJ'    // 年付超額收費: $0.3/頁
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

// =====================================================
// 超額計費功能 - Credits 扣除與使用量報告
// =====================================================

/**
 * 扣除 Credits 並檢查是否超額
 * 
 * 功能：
 * 1. 扣除用戶 Credits
 * 2. 如果是 Pro Plan 且 Credits 變為負數，報告超額使用量給 Stripe
 * 3. 記錄使用量歷史
 */
exports.deductCreditsClient = functions
    .runWith({
        timeoutSeconds: 60,
        memory: '256MB'
    })
    .https.onCall(async (data, context) => {
        try {
            // 1️⃣ 驗證用戶身份
            if (!context.auth) {
                throw new functions.https.HttpsError(
                    'unauthenticated',
                    'User must be logged in'
                );
            }

            const { userId, amount, metadata } = data;
            
            // 驗證 userId 與當前用戶匹配
            if (userId !== context.auth.uid) {
                throw new functions.https.HttpsError(
                    'permission-denied',
                    'User ID mismatch'
                );
            }

            console.log(`💰 扣除 Credits: userId=${userId}, amount=${amount}`);

            const db = admin.firestore();
            const userRef = db.collection('users').doc(userId);

            // 2️⃣ 使用事務扣除 Credits
            const result = await db.runTransaction(async (transaction) => {
                const userDoc = await transaction.get(userRef);

                if (!userDoc.exists) {
                    throw new functions.https.HttpsError(
                        'not-found',
                        'User document not found'
                    );
                }

                const userData = userDoc.data();
                const currentCredits = userData.credits || 0;
                const planType = userData.planType || 'Free Plan';
                const subscription = userData.subscription || null;

                console.log(`   當前 Credits: ${currentCredits}, 計劃: ${planType}`);

                // 計算新的 Credits
                const newCredits = currentCredits - amount;

                // 3️⃣ 檢查是否超額（Pro Plan 允許負數）
                let overagePages = 0;
                if (newCredits < 0 && planType === 'Pro Plan') {
                    overagePages = Math.abs(newCredits);
                    console.log(`   ⚠️ 超額使用: ${overagePages} 頁`);
                }

                // 4️⃣ 更新用戶數據
                const updateData = {
                    credits: newCredits,
                    updatedAt: admin.firestore.FieldValue.serverTimestamp()
                };

                // 如果有訂閱，更新使用量統計
                if (subscription && subscription.stripeSubscriptionId) {
                    updateData['usageThisPeriod.totalPages'] = admin.firestore.FieldValue.increment(amount);
                    if (overagePages > 0) {
                        updateData['usageThisPeriod.overagePages'] = admin.firestore.FieldValue.increment(overagePages);
                    }
                }

                transaction.update(userRef, updateData);

                // 5️⃣ 記錄歷史
                const historyRef = db.collection('users').doc(userId).collection('creditsHistory').doc();
                transaction.set(historyRef, {
                    type: 'deduct',
                    amount: amount,
                    balanceBefore: currentCredits,
                    balanceAfter: newCredits,
                    overagePages: overagePages,
                    metadata: metadata || {},
                    createdAt: admin.firestore.FieldValue.serverTimestamp()
                });

                return {
                    newCredits,
                    overagePages,
                    subscription
                };
            });

            console.log(`✅ Credits 已扣除: 新餘額 ${result.newCredits}`);

            // 6️⃣ 如果有超額且有訂閱，報告使用量給 Stripe
            if (result.overagePages > 0 && result.subscription && result.subscription.stripeSubscriptionId) {
                try {
                    console.log(`📊 報告超額使用量到 Stripe: ${result.overagePages} 頁`);
                    
                    // 調用 Stripe API 報告使用量
                    await reportUsageToStripe(
                        result.subscription.stripeSubscriptionId,
                        result.overagePages,
                        result.subscription.planType
                    );
                    
                    console.log(`✅ 使用量已報告到 Stripe`);
                } catch (error) {
                    console.error(`❌ 報告使用量失敗（不影響 Credits 扣除）:`, error.message);
                    // 不拋出錯誤，因為 Credits 已經扣除成功
                }
            }

            return {
                success: true,
                newCredits: result.newCredits,
                overagePages: result.overagePages
            };

        } catch (error) {
            console.error('❌ 扣除 Credits 失敗:', error);
            throw new functions.https.HttpsError(
                'internal',
                `Failed to deduct credits: ${error.message}`
            );
        }
    });

/**
 * 報告使用量到 Stripe Billing Meter
 * 
 * @param {string} subscriptionId - Stripe 訂閱 ID
 * @param {number} quantity - 使用量（頁數）
 * @param {string} planType - 計劃類型 (monthly/yearly)
 */
async function reportUsageToStripe(subscriptionId, quantity, planType) {
    try {
        // 1️⃣ 獲取訂閱詳情
        const subscription = await stripe.subscriptions.retrieve(subscriptionId);
        
        console.log(`   訂閱 ID: ${subscriptionId}`);
        console.log(`   訂閱項數量: ${subscription.items.data.length}`);

        // 2️⃣ 查找超額計費的訂閱項
        // 需要根據 planType 找到對應的超額計費 Price ID
        const overagePriceId = planType === 'yearly' 
            ? PRICE_IDS.overage.yearly 
            : PRICE_IDS.overage.monthly;

        console.log(`   尋找超額計費項: ${overagePriceId}`);

        // 查找對應的訂閱項
        let subscriptionItem = subscription.items.data.find(
            item => item.price.id === overagePriceId
        );

        // 3️⃣ 如果不存在超額計費項，創建一個
        if (!subscriptionItem) {
            console.log(`   ⚠️ 超額計費項不存在，創建新的訂閱項...`);
            
            const newItem = await stripe.subscriptionItems.create({
                subscription: subscriptionId,
                price: overagePriceId,
                metadata: {
                    type: 'overage',
                    planType: planType
                }
            });
            
            subscriptionItem = newItem;
            console.log(`   ✅ 訂閱項已創建: ${subscriptionItem.id}`);
        }

        // 4️⃣ 報告使用量
        const usageRecord = await stripe.subscriptionItems.createUsageRecord(
            subscriptionItem.id,
            {
                quantity: quantity,
                timestamp: Math.floor(Date.now() / 1000),
                action: 'increment'
            }
        );

        console.log(`   ✅ 使用量記錄已創建: ${usageRecord.id}, 數量: ${quantity}`);
        
        return { success: true, usageRecord };

    } catch (error) {
        console.error('❌ 報告使用量到 Stripe 失敗:', error);
        throw error;
    }
}

/**
 * 手動報告使用量（備用函數，可由前端調用）
 */
exports.reportStripeUsage = functions.https.onCall(async (data, context) => {
    try {
        if (!context.auth) {
            throw new functions.https.HttpsError('unauthenticated', 'User must be logged in');
        }

        const { subscriptionId, quantity, planType } = data;

        console.log(`📊 手動報告使用量: subscription=${subscriptionId}, quantity=${quantity}`);

        const result = await reportUsageToStripe(subscriptionId, quantity, planType);

        return {
            success: true,
            usageRecord: result.usageRecord
        };

    } catch (error) {
        console.error('❌ 報告使用量失敗:', error);
        throw new functions.https.HttpsError(
            'internal',
            `Failed to report usage: ${error.message}`
        );
    }
});

// =====================================================
// Stripe Webhook 處理
// =====================================================

/**
 * Stripe Webhook 端點
 * 
 * 處理事件：
 * - checkout.session.completed - 訂閱創建成功
 * - customer.subscription.created/updated - 訂閱更新
 * - invoice.payment_succeeded - 續費成功，重置 Credits
 * - customer.subscription.deleted - 訂閱取消
 */
exports.stripeWebhook = functions
    .runWith({
        timeoutSeconds: 60,
        memory: '256MB'
    })
    .https.onRequest(async (req, res) => {
        const sig = req.headers['stripe-signature'];
        const webhookSecret = functions.config().stripe?.webhook_secret || process.env.STRIPE_WEBHOOK_SECRET;

        if (!webhookSecret) {
            console.error('❌ Webhook Secret 未配置');
            return res.status(500).send('Webhook secret not configured');
        }

        let event;

        try {
            // 驗證 Webhook 簽名
            event = stripe.webhooks.constructEvent(req.rawBody, sig, webhookSecret);
        } catch (err) {
            console.error('⚠️  Webhook 簽名驗證失敗:', err.message);
            return res.status(400).send(`Webhook Error: ${err.message}`);
        }

        console.log(`📨 收到 Webhook 事件: ${event.type}`);

        try {
            // 處理不同類型的事件
            switch (event.type) {
                case 'checkout.session.completed':
                    await handleCheckoutCompleted(event.data.object);
                    break;

                case 'customer.subscription.created':
                case 'customer.subscription.updated':
                    await handleSubscriptionUpdate(event.data.object);
                    break;

                case 'customer.subscription.deleted':
                    await handleSubscriptionDeleted(event.data.object);
                    break;

                case 'invoice.payment_succeeded':
                    await handleInvoicePaymentSucceeded(event.data.object);
                    break;

                case 'invoice.payment_failed':
                    await handleInvoicePaymentFailed(event.data.object);
                    break;

                default:
                    console.log(`   ℹ️ 未處理的事件類型: ${event.type}`);
            }

            res.json({ received: true });

        } catch (error) {
            console.error(`❌ 處理 Webhook 失敗:`, error);
            res.status(500).send(`Webhook processing failed: ${error.message}`);
        }
    });

/**
 * 處理 Checkout 完成事件
 */
async function handleCheckoutCompleted(session) {
    const userId = session.metadata?.userId || session.client_reference_id;
    const planType = session.metadata?.planType;
    const currency = session.metadata?.currency;

    if (!userId) {
        console.error('⚠️ Checkout session 沒有 userId');
        return;
    }

    console.log(`💳 訂閱成功: userId=${userId}, planType=${planType}`);

    const subscriptionId = session.subscription;
    
    // 獲取訂閱詳情
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);

    // 計算 Credits
    const credits = planType === 'yearly' ? 1200 : 100;
    const monthlyCredits = 100;

    // 更新 Firestore
    const db = admin.firestore();
    await db.collection('users').doc(userId).set({
        subscription: {
            stripeSubscriptionId: subscriptionId,
            stripeCustomerId: session.customer,
            stripePriceId: subscription.items.data[0].price.id,
            planType: planType,
            currency: currency,
            monthlyCredits: monthlyCredits,
            currentPeriodStart: new Date(subscription.current_period_start * 1000),
            currentPeriodEnd: new Date(subscription.current_period_end * 1000),
            status: 'active'
        },
        credits: admin.firestore.FieldValue.increment(credits),
        planType: 'Pro Plan',
        usageThisPeriod: {
            totalPages: 0,
            overagePages: 0
        },
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });

    console.log(`✅ 用戶訂閱數據已更新: +${credits} Credits`);
}

/**
 * 處理訂閱更新事件
 */
async function handleSubscriptionUpdate(subscription) {
    const userId = subscription.metadata?.userId;

    if (!userId) {
        console.warn('⚠️ 訂閱沒有關聯的 userId');
        return;
    }

    console.log(`🔄 訂閱更新: userId=${userId}, status=${subscription.status}`);

    const db = admin.firestore();
    await db.collection('users').doc(userId).update({
        'subscription.status': subscription.status,
        'subscription.currentPeriodStart': new Date(subscription.current_period_start * 1000),
        'subscription.currentPeriodEnd': new Date(subscription.current_period_end * 1000),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    console.log(`✅ 訂閱狀態已更新`);
}

/**
 * 處理訂閱取消事件
 */
async function handleSubscriptionDeleted(subscription) {
    const userId = subscription.metadata?.userId;

    if (!userId) {
        console.warn('⚠️ 訂閱沒有關聯的 userId');
        return;
    }

    console.log(`❌ 訂閱已取消: userId=${userId}`);

    const db = admin.firestore();
    await db.collection('users').doc(userId).update({
        'subscription.status': 'cancelled',
        planType: 'Free Plan',
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    console.log(`✅ 用戶已降級為 Free Plan`);
}

/**
 * 處理續費成功事件 - 重置 Credits（區分月付/年付）
 * 
 * 計費邏輯：
 * - 月付：每月計費日重置 Credits 為 100 + 收取超額費用
 * - 年付：
 *   - 年度續費：重置 Credits 為 1200
 *   - 月度超額：僅收取超額費用，不重置 Credits
 */
async function handleInvoicePaymentSucceeded(invoice) {
    const subscriptionId = invoice.subscription;

    if (!subscriptionId) {
        console.log('   ℹ️ 非訂閱發票，跳過');
        return;
    }

    // 獲取訂閱詳情
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
    const userId = subscription.metadata?.userId;

    if (!userId) {
        console.warn('⚠️ 訂閱沒有關聯的 userId');
        return;
    }

    // 獲取用戶當前計劃
    const db = admin.firestore();
    const userDoc = await db.collection('users').doc(userId).get();
    const userData = userDoc.data();
    const planType = userData.subscription?.planType || 'monthly';

    // 檢查發票類型
    const billingReason = invoice.billing_reason;
    const isYearlyRenewal = planType === 'yearly' && billingReason === 'subscription_cycle';
    const isMonthlyOverage = planType === 'yearly' && billingReason !== 'subscription_cycle';

    console.log(`💰 續費成功: userId=${userId}, planType=${planType}, billingReason=${billingReason}`);

    // 根據計劃類型處理
    if (planType === 'monthly') {
        // 🔄 月付：每月重置 Credits 為 100
        const creditsToAdd = 100;

        await db.collection('users').doc(userId).update({
            credits: creditsToAdd,
            'usageThisPeriod.totalPages': 0,
            'usageThisPeriod.overagePages': 0,
            'subscription.currentPeriodStart': new Date(subscription.current_period_start * 1000),
            'subscription.currentPeriodEnd': new Date(subscription.current_period_end * 1000),
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        // 記錄歷史
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'renewal',
            amount: creditsToAdd,
            reason: 'monthly_renewal',
            description: `月付續費，重置 Credits 為 ${creditsToAdd}`,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        console.log(`✅ 月付續費: Credits 已重置為 ${creditsToAdd}`);

    } else if (isYearlyRenewal) {
        // 🔄 年付 - 年度續費：重置 Credits 為 1200
        const creditsToAdd = 1200;

        await db.collection('users').doc(userId).update({
            credits: creditsToAdd,
            'usageThisPeriod.totalPages': 0,
            'usageThisPeriod.overagePages': 0,
            'subscription.currentPeriodStart': new Date(subscription.current_period_start * 1000),
            'subscription.currentPeriodEnd': new Date(subscription.current_period_end * 1000),
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        // 記錄歷史
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'renewal',
            amount: creditsToAdd,
            reason: 'yearly_renewal',
            description: `年付續費，重置 Credits 為 ${creditsToAdd}`,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        console.log(`✅ 年付續費: Credits 已重置為 ${creditsToAdd}`);

    } else if (isMonthlyOverage) {
        // 💰 年付 - 月度超額：僅清除超額統計，不重置 Credits
        const currentCredits = userData.credits || 0;

        await db.collection('users').doc(userId).update({
            // ⚠️ 不重置 Credits！保持當前值（可能是負數）
            'usageThisPeriod.totalPages': 0,
            'usageThisPeriod.overagePages': 0,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        // 記錄歷史
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'overage_billing',
            amount: 0,  // 不改變 Credits
            reason: 'monthly_overage_billing',
            description: `年付月度超額計費，Credits 保持為 ${currentCredits}`,
            metadata: {
                invoiceId: invoice.id,
                overageAmount: invoice.amount_due / 100  // Stripe 金額單位為分
            },
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        console.log(`✅ 年付月度超額計費: Credits 保持為 ${currentCredits}`);
    }
}

/**
 * 處理支付失敗事件
 */
async function handleInvoicePaymentFailed(invoice) {
    const subscriptionId = invoice.subscription;

    if (!subscriptionId) {
        return;
    }

    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
    const userId = subscription.metadata?.userId;

    if (!userId) {
        console.warn('⚠️ 訂閱沒有關聯的 userId');
        return;
    }

    console.log(`⚠️ 支付失敗: userId=${userId}`);

    // 可以在這裡添加通知用戶的邏輯
    // 例如發送郵件提醒用戶更新支付方式
}

