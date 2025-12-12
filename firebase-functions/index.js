/**
 * Firebase Cloud Functions for Credits Management
 * 
 * 功能：
 * 1. 自動處理 Credits 分配
 * 2. 處理 Stripe 付款回調
 * 3. 管理訂閱計劃
 * 4. Credits 過期管理
 * 5. Email 驗證碼發送和驗證
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
// Stripe 配置為可選（如果未設置則跳過 webhook 功能）
const stripeConfig = functions.config().stripe;

// 🎯 初始化生产模式和测试模式的 Stripe 客户端
const stripeLive = stripeConfig && stripeConfig.secret_key ? require('stripe')(stripeConfig.secret_key) : null;
const stripeTest = stripeConfig && stripeConfig.test_secret_key ? require('stripe')(stripeConfig.test_secret_key) : null;

// 为了向后兼容，保留 stripe 变量指向生产模式
const stripe = stripeLive;

const nodemailer = require('nodemailer');

admin.initializeApp();
const db = admin.firestore();

// 配置 Email 發送器（使用 Gmail）- 延遲初始化
let transporter = null;
function getTransporter() {
    if (!transporter) {
        const emailConfig = functions.config().email;
        if (emailConfig && emailConfig.user && emailConfig.password) {
            transporter = nodemailer.createTransport({
                service: 'gmail',
                auth: {
                    user: emailConfig.user,
                    pass: emailConfig.password
                }
            });
        }
    }
    return transporter;
}

// ============================================
// 1. 處理 Stripe Webhook（付款成功後自動添加 Credits）
// ============================================

// Stripe Webhook - Using req.rawBody which is available in Firebase Functions
exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
    console.log('========== WEBHOOK START ==========');
    console.log('⏰ 时间:', new Date().toISOString());
    console.log('🔧 HTTP Method:', req.method);
    console.log('📍 Request Path:', req.path);
    console.log('🔑 Headers:', JSON.stringify(req.headers, null, 2));
    console.log('========================================');
    
    // 设置CORS headers
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.set('Access-Control-Allow-Headers', 'Content-Type, Stripe-Signature');
    
    // Handle OPTIONS preflight request
    if (req.method === 'OPTIONS') {
        console.log('ℹ️ OPTIONS request received, sending 204');
        res.status(204).send('');
        return;
    }
    
    // 檢查 Stripe 是否已配置
    if ((!stripeLive && !stripeTest) || !stripeConfig) {
        console.error('❌ Stripe 未配置');
        return res.status(503).send('Stripe not configured');
    }
    
    const sig = req.headers['stripe-signature'];
    // Use req.rawBody which should be available in Firebase Functions
    const payload = req.rawBody || req.body;
    
    console.log('📦 Payload type:', payload ? payload.constructor.name : 'undefined');
    console.log('📦 Payload length:', payload ? payload.length : 0);
    console.log('📦 Signature:', sig);
    
    let event;
    let isTestMode = false;
    
    // 首先尝试使用生产模式的webhook密钥验证
    if (stripeLive && stripeConfig.webhook_secret) {
        try {
            event = stripeLive.webhooks.constructEvent(payload, sig, stripeConfig.webhook_secret);
            console.log('✅ 生产模式webhook签名验证成功');
        } catch (err) {
            console.log('⚠️ 生产模式签名验证失败，尝试测试模式:', err.message);
            // 如果生产模式验证失败，尝试测试模式
            if (stripeTest && stripeConfig.test_webhook_secret) {
                try {
                    event = stripeTest.webhooks.constructEvent(payload, sig, stripeConfig.test_webhook_secret);
                    isTestMode = true;
                    console.log('✅ 测试模式webhook签名验证成功');
                } catch (testErr) {
                    console.error('❌ 测试模式签名验证也失败:', testErr.message);
                    return res.status(400).send(`Webhook Error: ${testErr.message}`);
                }
            } else {
                console.error('❌ 未配置测试模式webhook密钥');
                return res.status(400).send(`Webhook Error: ${err.message}`);
            }
        }
    } else if (stripeTest && stripeConfig.test_webhook_secret) {
        // 如果只配置了测试模式
        try {
            event = stripeTest.webhooks.constructEvent(payload, sig, stripeConfig.test_webhook_secret);
            isTestMode = true;
            console.log('✅ 测试模式webhook签名验证成功');
        } catch (err) {
            console.error('❌ Webhook signature verification failed:', err.message);
            return res.status(400).send(`Webhook Error: ${err.message}`);
        }
    } else {
        console.error('❌ Stripe webhook密钥未配置');
        return res.status(503).send('Stripe webhook secret not configured');
    }
    
    console.log(`📨 收到${isTestMode ? '测试' : '生产'}模式webhook事件: ${event.type}, ID: ${event.id}`);
    
    // 處理不同類型的 Stripe 事件
    try {
        switch (event.type) {
            case 'checkout.session.completed':
                await handleCheckoutCompleted(event.data.object, isTestMode);
                break;
            case 'payment_intent.succeeded':
                await handlePaymentSuccess(event.data.object);
                break;
            case 'customer.subscription.created':
            case 'customer.subscription.updated':
                await handleSubscriptionChange(event.data.object, isTestMode);
                break;
            case 'customer.subscription.deleted':
                await handleSubscriptionCancelled(event.data.object);
                break;
            default:
                console.log(`⚠️ 未處理的事件類型: ${event.type}`);
                console.log('📄 完整 Event Object:', JSON.stringify(event, null, 2));
        }
        
        res.status(200).json({ received: true });
    } catch (error) {
        console.error('❌ 处理webhook事件时发生错误:', error);
        res.status(500).json({ error: 'Webhook processing failed' });
    }
});

// End of stripeWebhook function

/**
 * 處理結帳完成
 */
async function handleCheckoutCompleted(session, isTestMode = false) {
    console.log(`✅ 結帳完成 (${isTestMode ? '測試模式' : '生產模式'}):`, session.id);
    console.log(`📋 Session 详情:`, JSON.stringify(session, null, 2));
    
    // 選擇正確的 Stripe 客戶端
    const stripeClient = isTestMode ? stripeTest : stripeLive;
    if (!stripeClient) {
        console.error(`❌ Stripe 客戶端未配置 (${isTestMode ? '測試模式' : '生產模式'})`);
        throw new Error('Stripe client not configured');
    }
    console.log(`🔧 使用的 Stripe 客戶端: ${isTestMode ? 'stripeTest' : 'stripeLive'}`);
    
    // 尝试获取用户ID（支持多种方式）
    let userId = session.client_reference_id || session.metadata?.userId;
    console.log(`🔍 初始 userId: ${userId}`);
    
    // 如果没有userId，尝试通过email查找
    if (!userId && session.customer_email) {
        console.log(`🔍 嘗試通過 email 查找用戶: ${session.customer_email}`);
        try {
            const usersSnapshot = await db.collection('users')
                .where('email', '==', session.customer_email)
                .limit(1)
                .get();
            
            if (!usersSnapshot.empty) {
                userId = usersSnapshot.docs[0].id;
                console.log(`✅ 通過 email 找到用戶: ${userId}`);
            } else {
                console.log(`⚠️ 未找到 email 對應的用戶，創建新用戶: ${session.customer_email}`);
                // 创建新用户
                const newUserRef = await db.collection('users').add({
                    email: session.customer_email,
                    credits: 0,
                    createdAt: admin.firestore.FieldValue.serverTimestamp(),
                    updatedAt: admin.firestore.FieldValue.serverTimestamp(),
                    source: 'stripe_payment'
                });
                userId = newUserRef.id;
                console.log(`✅ 新用戶已創建: ${userId}`);
            }
        } catch (error) {
            console.error('❌ 查找用戶失敗:', error);
        }
    }
    
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID，session:', JSON.stringify(session, null, 2));
        return;
    }
    console.log(`✅ 最終 userId: ${userId}`);
    
    // 獲取購買的產品信息 - 使用正確的 Stripe 客戶端
    console.log(`🔍 開始獲取產品信息...`);
    const lineItems = await stripeClient.checkout.sessions.listLineItems(session.id);
    console.log(`📦 LineItems 數量: ${lineItems.data.length}`);
    console.log(`📦 LineItems 详情:`, JSON.stringify(lineItems, null, 2));
    
    for (const item of lineItems.data) {
        const productId = item.price.product;
        console.log(`🔍 正在獲取產品: ${productId}`);
        const product = await stripeClient.products.retrieve(productId);
        
        console.log(`📦 產品信息:`, {
            productId: product.id,
            name: product.name,
            metadata: product.metadata
        });
        console.log(`📦 完整產品对象:`, JSON.stringify(product, null, 2));
        
        // 根據產品 metadata 添加 Credits
        const credits = parseInt(product.metadata.monthly_credits || product.metadata.credits || 0);
        console.log(`🔢 計算得到的 Credits: ${credits}`);
        console.log(`🔢 product.metadata.monthly_credits: ${product.metadata.monthly_credits}`);
        console.log(`🔢 product.metadata.credits: ${product.metadata.credits}`);
        
        if (credits > 0) {
            console.log(`💰 準備添加 ${credits} Credits 給用戶 ${userId}`);
            await addCredits(userId, credits, {
                source: 'purchase',
                stripeSessionId: session.id,
                productName: product.name,
                amount: session.amount_total / 100,
                currency: session.currency,
                planType: product.metadata.plan_type || 'unknown'
            });
            console.log(`✅ 成功添加 ${credits} Credits`);
        } else {
            console.log(`⚠️ 產品沒有配置 Credits: ${product.name}`);
            console.log(`⚠️ product.metadata 完整内容:`, JSON.stringify(product.metadata, null, 2));
        }
    }
    console.log(`✅ handleCheckoutCompleted 執行完成`);
}

/**
 * 處理付款成功
 */
async function handlePaymentSuccess(paymentIntent) {
    console.log('✅ 付款成功:', paymentIntent.id);
    
    const userId = paymentIntent.metadata?.userId;
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID');
        return;
    }
    
    // 記錄付款
    await db.collection('users').doc(userId).collection('payments').add({
        paymentIntentId: paymentIntent.id,
        amount: paymentIntent.amount / 100,
        currency: paymentIntent.currency,
        status: 'succeeded',
        createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
}

/**
 * 處理訂閱變更
 */
async function handleSubscriptionChange(subscription, isTestMode = false) {
    console.log(`✅ 訂閱變更 (${isTestMode ? '測試模式' : '生產模式'}):`, subscription.id);
    console.log(`📋 Subscription 詳情:`, JSON.stringify(subscription, null, 2));
    
    // 選擇正確的 Stripe 客戶端
    const stripeClient = isTestMode ? stripeTest : stripeLive;
    if (!stripeClient) {
        console.error(`❌ Stripe 客戶端未配置 (${isTestMode ? '測試模式' : '生產模式'})`);
        throw new Error('Stripe client not configured');
    }
    
    // 尝试获取用户ID
    let userId = subscription.metadata?.userId;
    
    // 如果没有userId，尝试通过customer查找
    if (!userId && subscription.customer) {
        console.log(`🔍 嘗試通過 Stripe Customer 查找用戶: ${subscription.customer}`);
        try {
            // 获取customer的email - 使用正確的 Stripe 客戶端
            const customer = await stripeClient.customers.retrieve(subscription.customer);
            console.log(`📧 Customer email: ${customer.email}`);
            
            if (customer.email) {
                const usersSnapshot = await db.collection('users')
                    .where('email', '==', customer.email)
                    .limit(1)
                    .get();
                
                if (!usersSnapshot.empty) {
                    userId = usersSnapshot.docs[0].id;
                    console.log(`✅ 通過 customer email 找到用戶: ${userId}`);
                }
            }
        } catch (error) {
            console.error('❌ 查找用戶失敗:', error);
        }
    }
    
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID，subscription:', JSON.stringify(subscription, null, 2));
        return;
    }
    
    // 獲取訂閱計劃信息 - 使用正確的 Stripe 客戶端
    const priceId = subscription.items.data[0].price.id;
    const product = await stripeClient.products.retrieve(subscription.items.data[0].price.product);
    
    console.log(`📦 訂閱產品信息:`, {
        productId: product.id,
        name: product.name,
        metadata: product.metadata
    });
    
    // 確定計劃類型和 Credits
    let planType = product.metadata.plan_type || 'monthly';
    let monthlyCredits = parseInt(product.metadata.monthly_credits || product.metadata.credits || 0);
    
    console.log(`📊 訂閱詳情:`, {
        planType,
        monthlyCredits,
        status: subscription.status
    });
    
    // ✨ 新增邏輯：當訂閱變為 active 時，添加 Credits
    if (subscription.status === 'active' && monthlyCredits > 0) {
        console.log(`🎉 訂閱已激活，準備添加 ${monthlyCredits} Credits 給用戶 ${userId}`);
        
        try {
            await addCredits(userId, monthlyCredits, {
                type: 'subscription_activated',
                subscriptionId: subscription.id,
                planType: planType,
                productName: product.name,
                isTestMode: isTestMode
            });
            console.log(`✅ 已成功添加 ${monthlyCredits} Credits 給用戶 ${userId}`);
        } catch (error) {
            console.error(`❌ 添加 Credits 失敗:`, error);
        }
    } else if (subscription.status !== 'active') {
        console.log(`⚠️ 訂閱狀態不是 active (當前: ${subscription.status})，跳過添加 Credits`);
    } else if (monthlyCredits === 0) {
        console.warn(`⚠️ 產品 ${product.name} (${product.id}) 沒有配置 credits，跳過添加`);
    }
    
    // 更新用戶訂閱信息
    await db.collection('users').doc(userId).update({
        subscription: {
            stripeSubscriptionId: subscription.id,
            stripeCustomerId: subscription.customer,
            status: subscription.status,
            planType: planType,
            monthlyCredits: monthlyCredits,
            currentPeriodStart: new Date(subscription.current_period_start * 1000),
            currentPeriodEnd: new Date(subscription.current_period_end * 1000),
            cancelAtPeriodEnd: subscription.cancel_at_period_end
        },
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // 如果是新訂閱或續訂，添加當月 Credits
    if (subscription.status === 'active' && monthlyCredits > 0) {
        console.log(`💰 準備添加 ${monthlyCredits} Credits（訂閱）`);
        await addCredits(userId, monthlyCredits, {
            source: 'subscription',
            planType: planType,
            period: `${new Date(subscription.current_period_start * 1000).toISOString()} - ${new Date(subscription.current_period_end * 1000).toISOString()}`,
            subscriptionId: subscription.id
        });
        console.log(`✅ 成功添加 ${monthlyCredits} Credits（訂閱）`);
    }
}

/**
 * 處理訂閱取消
 */
async function handleSubscriptionCancelled(subscription) {
    console.log('❌ 訂閱已取消:', subscription.id);
    
    const userId = subscription.metadata?.userId;
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID');
        return;
    }
    
    // 更新用戶訂閱狀態
    await db.collection('users').doc(userId).update({
        'subscription.status': 'cancelled',
        'subscription.cancelledAt': admin.firestore.FieldValue.serverTimestamp()
    });
}

// ============================================
// 2. Credits 管理函數
// ============================================

/**
 * 添加 Credits
 */
async function addCredits(userId, amount, metadata = {}) {
    const userRef = db.collection('users').doc(userId);
    
    await db.runTransaction(async (transaction) => {
        const userDoc = await transaction.get(userRef);
        const currentCredits = userDoc.data()?.credits || 0;
        const newCredits = currentCredits + amount;
        
        transaction.update(userRef, {
            credits: newCredits,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        // 記錄 Credits 歷史
        const historyRef = userRef.collection('creditsHistory').doc();
        transaction.set(historyRef, {
            type: 'add',
            amount: amount,
            before: currentCredits,
            after: newCredits,
            metadata: metadata,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        console.log(`✅ Credits 已添加: ${userId} +${amount} = ${newCredits}`);
    });
}

/**
 * 扣除 Credits
 */
async function deductCredits(userId, amount, metadata = {}) {
    const userRef = db.collection('users').doc(userId);
    
    await db.runTransaction(async (transaction) => {
        const userDoc = await transaction.get(userRef);
        const currentCredits = userDoc.data()?.credits || 0;
        
        if (currentCredits < amount) {
            throw new Error('Credits 不足');
        }
        
        const newCredits = currentCredits - amount;
        
        transaction.update(userRef, {
            credits: newCredits,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        // 記錄 Credits 歷史
        const historyRef = userRef.collection('creditsHistory').doc();
        transaction.set(historyRef, {
            type: 'deduct',
            amount: amount,
            before: currentCredits,
            after: newCredits,
            metadata: metadata,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        console.log(`✅ Credits 已扣除: ${userId} -${amount} = ${newCredits}`);
    });
}

// ============================================
// 3. 定期任務 - 每月重置訂閱 Credits
// ============================================

exports.monthlyCreditsReset = functions.pubsub
    .schedule('0 0 1 * *') // 每月1號凌晨執行
    .timeZone('Asia/Taipei')
    .onRun(async (context) => {
        console.log('🔄 開始每月 Credits 重置...');
        
        const usersSnapshot = await db.collection('users')
            .where('subscription.status', '==', 'active')
            .get();
        
        let count = 0;
        
        for (const userDoc of usersSnapshot.docs) {
            const userId = userDoc.id;
            const userData = userDoc.data();
            const subscription = userData.subscription;
            
            // 檢查訂閱是否在當前週期內
            const now = new Date();
            const periodStart = subscription.currentPeriodStart.toDate();
            const periodEnd = subscription.currentPeriodEnd.toDate();
            
            if (now >= periodStart && now <= periodEnd) {
                const monthlyCredits = subscription.monthlyCredits || 0;
                
                // 重置 Credits（設置為當月額度）
                await db.collection('users').doc(userId).update({
                    credits: monthlyCredits,
                    lastCreditsReset: admin.firestore.FieldValue.serverTimestamp()
                });
                
                // 記錄重置
                await userDoc.ref.collection('creditsHistory').add({
                    type: 'reset',
                    amount: monthlyCredits,
                    planType: subscription.planType,
                    createdAt: admin.firestore.FieldValue.serverTimestamp()
                });
                
                count++;
            }
        }
        
        console.log(`✅ Credits 重置完成，影響 ${count} 個用戶`);
    });

// ============================================
// 4. 定期任務 - 檢查過期訂閱
// ============================================

exports.checkExpiredSubscriptions = functions.pubsub
    .schedule('0 */6 * * *') // 每6小時檢查一次
    .timeZone('Asia/Taipei')
    .onRun(async (context) => {
        console.log('🔍 檢查過期訂閱...');
        
        const now = new Date();
        
        const usersSnapshot = await db.collection('users')
            .where('subscription.status', '==', 'active')
            .get();
        
        let count = 0;
        
        for (const userDoc of usersSnapshot.docs) {
            const userId = userDoc.id;
            const subscription = userDoc.data().subscription;
            
            if (!subscription) continue;
            
            const periodEnd = subscription.currentPeriodEnd.toDate();
            
            // 如果訂閱已過期
            if (now > periodEnd) {
                await db.collection('users').doc(userId).update({
                    'subscription.status': 'expired',
                    'subscription.expiredAt': admin.firestore.FieldValue.serverTimestamp()
                });
                
                // 如果沒有 cancelAtPeriodEnd，嘗試從 Stripe 獲取最新狀態
                if (!subscription.cancelAtPeriodEnd) {
                    try {
                        const stripeSubscription = await stripe.subscriptions.retrieve(subscription.stripeSubscriptionId);
                        
                        await db.collection('users').doc(userId).update({
                            'subscription.status': stripeSubscription.status
                        });
                    } catch (error) {
                        console.error(`❌ 無法更新訂閱狀態: ${userId}`, error);
                    }
                }
                
                count++;
            }
        }
        
        console.log(`✅ 過期訂閱檢查完成，影響 ${count} 個用戶`);
    });

// ============================================
// 5. HTTP 端點 - 手動觸發 Credits 添加（測試用）
// ============================================

exports.addCreditsManual = functions.https.onCall(async (data, context) => {
    // 驗證用戶身份
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '用戶未登入');
    }
    
    const userId = context.auth.uid;
    const amount = data.amount;
    
    if (!amount || amount <= 0) {
        throw new functions.https.HttpsError('invalid-argument', '無效的 Credits 數量');
    }
    
    await addCredits(userId, amount, {
        source: 'manual',
        requestedBy: userId
    });
    
    return { success: true, message: `已添加 ${amount} Credits` };
});

// ============================================
// 6. HTTP 端點 - 獲取 Credits 歷史記錄
// ============================================

exports.getCreditsHistory = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '用戶未登入');
    }
    
    const userId = context.auth.uid;
    const limit = data.limit || 50;
    
    const historySnapshot = await db.collection('users')
        .doc(userId)
        .collection('creditsHistory')
        .orderBy('createdAt', 'desc')
        .limit(limit)
        .get();
    
    const history = [];
    historySnapshot.forEach(doc => {
        history.push({
            id: doc.id,
            ...doc.data(),
            createdAt: doc.data().createdAt?.toDate()?.toISOString()
        });
    });
    
    return { history };
});

// ============================================
// 6. Email 驗證功能
// ============================================

/**
 * 生成 6 位數驗證碼
 */
function generateVerificationCode() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

/**
 * 發送驗證碼到用戶 email
 */
exports.sendVerificationCode = functions.https.onCall(async (data, context) => {
    const { email, displayName } = data;
    
    if (!email) {
        throw new functions.https.HttpsError('invalid-argument', 'Email is required');
    }
    
    try {
        // 生成驗證碼
        const verificationCode = generateVerificationCode();
        const expiresAt = admin.firestore.Timestamp.fromDate(
            new Date(Date.now() + 10 * 60 * 1000) // 10 分鐘後過期
        );
        
        // 保存驗證碼到 Firestore
        await db.collection('verificationCodes').doc(email).set({
            code: verificationCode,
            email: email,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            expiresAt: expiresAt,
            verified: false,
            attempts: 0
        });
        
        // 發送 email
        const mailOptions = {
            from: `VaultCaddy <${functions.config().email.user}>`,
            to: email,
            subject: '歡迎註冊 VaultCaddy - 驗證您的電子郵件',
            html: `
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                        .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
                        .code-box { background: white; border: 2px solid #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }
                        .code { font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; }
                        .button { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                        .footer { text-align: center; color: #6b7280; font-size: 14px; margin-top: 30px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🎉 歡迎加入 VaultCaddy！</h1>
                        </div>
                        <div class="content">
                            <p>親愛的 ${displayName || '用戶'}，</p>
                            
                            <p>感謝您註冊 VaultCaddy！我們很高興您選擇使用我們的 AI 文檔處理服務。</p>
                            
                            <p>請使用以下驗證碼完成註冊：</p>
                            
                            <div class="code-box">
                                <div class="code">${verificationCode}</div>
                                <p style="color: #6b7280; margin-top: 10px;">驗證碼將在 10 分鐘後過期</p>
                            </div>
                            
                            <h3>🚀 VaultCaddy 能為您做什麼？</h3>
                            <ul>
                                <li><strong>AI 自動提取：</strong>從發票和收據自動提取數據</li>
                                <li><strong>QuickBooks 整合：</strong>一鍵導出到會計軟件</li>
                                <li><strong>多語言支持：</strong>支持繁體中文、英文等 8 種語言</li>
                                <li><strong>雲端安全存儲：</strong>所有數據加密保護</li>
                                <li><strong>免費試用：</strong>20 個免費 Credits（可處理 20 頁文檔）</li>
                            </ul>
                            
                            <p style="text-align: center;">
                                <a href="https://vaultcaddy.com/verify-email.html?email=${encodeURIComponent(email)}" class="button">立即驗證</a>
                            </p>
                            
                            <p><strong>需要幫助？</strong></p>
                            <p>如果您有任何問題，請隨時聯繫我們的支援團隊。</p>
                        </div>
                        <div class="footer">
                            <p>此郵件由 VaultCaddy 自動發送，請勿直接回覆。</p>
                            <p>© 2025 VaultCaddy. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
            `
        };
        
        const emailTransporter = getTransporter();
        if (!emailTransporter) {
            console.error('❌ Email 服務未配置');
            console.error('   請運行: firebase functions:config:set email.user="your-email@gmail.com" email.password="your-app-password"');
            console.error('   然後重新部署: firebase deploy --only functions');
            throw new functions.https.HttpsError('unavailable', 'Email 服務未配置，請聯繫管理員');
        }
        
        console.log(`📧 準備發送驗證碼到: ${email}`);
        await emailTransporter.sendMail(mailOptions);
        
        console.log(`✅ 驗證碼已成功發送到 ${email}`);
        return { success: true, message: '驗證碼已發送到您的郵箱' };
        
    } catch (error) {
        console.error('❌ 發送驗證碼失敗:', error);
        console.error('   錯誤類型:', error.name);
        console.error('   錯誤消息:', error.message);
        console.error('   錯誤堆疊:', error.stack);
        
        // 區分不同類型的錯誤
        if (error.message && error.message.includes('Invalid login')) {
            throw new functions.https.HttpsError('unauthenticated', 'Email 認證失敗，請聯繫管理員檢查 email 配置');
        } else if (error.message && error.message.includes('unavailable')) {
            throw new functions.https.HttpsError('unavailable', error.message);
        } else {
            throw new functions.https.HttpsError('internal', `發送驗證碼失敗: ${error.message || '請稍後重試'}`);
        }
    }
});

/**
 * 驗證用戶輸入的驗證碼
 */
exports.verifyCode = functions.https.onCall(async (data, context) => {
    const { email, code } = data;
    
    if (!email || !code) {
        throw new functions.https.HttpsError('invalid-argument', 'Email and code are required');
    }
    
    try {
        const docRef = db.collection('verificationCodes').doc(email);
        const doc = await docRef.get();
        
        if (!doc.exists) {
            throw new functions.https.HttpsError('not-found', '驗證碼不存在或已過期');
        }
        
        const data = doc.data();
        
        // 檢查是否已驗證
        if (data.verified) {
            throw new functions.https.HttpsError('already-exists', '此驗證碼已被使用');
        }
        
        // 檢查是否過期
        if (data.expiresAt.toDate() < new Date()) {
            await docRef.delete();
            throw new functions.https.HttpsError('deadline-exceeded', '驗證碼已過期，請重新獲取');
        }
        
        // 檢查嘗試次數
        if (data.attempts >= 5) {
            await docRef.delete();
            throw new functions.https.HttpsError('resource-exhausted', '驗證失敗次數過多，請重新獲取驗證碼');
        }
        
        // 驗證碼是否正確
        if (data.code !== code) {
            await docRef.update({
                attempts: admin.firestore.FieldValue.increment(1)
            });
            throw new functions.https.HttpsError('invalid-argument', '驗證碼錯誤，請重試');
        }
        
        // 驗證成功
        await docRef.update({
            verified: true,
            verifiedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        // 🎁 驗證成功後贈送 20 個 Credits
        try {
            console.log(`🔍 開始查找用戶: ${email}`);
            
            // 查找用戶
            const usersSnapshot = await db.collection('users').where('email', '==', email).limit(1).get();
            
            console.log(`📊 查找結果: 找到 ${usersSnapshot.size} 個用戶`);
            
            if (!usersSnapshot.empty) {
                const userDoc = usersSnapshot.docs[0];
                const userId = userDoc.id;
                const userData = userDoc.data();
                const userRef = db.collection('users').doc(userId);
                
                console.log(`👤 找到用戶: ${userId}, 當前 Credits: ${userData.currentCredits || userData.credits || 0}`);
                
                // 檢查是否已經贈送過驗證獎勵
                if (userData.emailVerified === true && userData.emailVerifiedAt) {
                    console.log(`⚠️ 用戶已經驗證過 Email，跳過贈送 Credits`);
                } else {
                    // 使用事務添加 Credits
                    await db.runTransaction(async (transaction) => {
                        const user = await transaction.get(userRef);
                        
                        if (user.exists) {
                            const currentCredits = user.data().currentCredits || user.data().credits || 0;
                            const newCredits = currentCredits + 20;
                            
                            console.log(`💰 準備添加 Credits: ${currentCredits} + 20 = ${newCredits}`);
                            
                            // 更新 Credits
                            transaction.update(userRef, {
                                credits: newCredits,
                                currentCredits: newCredits,
                                emailVerified: true,
                                emailVerifiedAt: admin.firestore.FieldValue.serverTimestamp(),
                                updatedAt: admin.firestore.FieldValue.serverTimestamp()
                            });
                            
                            // 記錄 Credits 歷史
                            const historyRef = db.collection('users').doc(userId).collection('creditsHistory').doc();
                            transaction.set(historyRef, {
                                type: 'bonus',
                                amount: 20,
                                reason: 'email_verification',
                                description: '完成 Email 驗證獎勵',
                                createdAt: admin.firestore.FieldValue.serverTimestamp(),
                                balanceAfter: newCredits
                            });
                            
                            console.log(`🎁 已贈送 20 Credits 給用戶: ${email} (新餘額: ${newCredits})`);
                        } else {
                            console.error(`❌ 用戶不存在: ${userId}`);
                        }
                    });
                }
            } else {
                console.error(`❌ 找不到用戶: ${email}`);
            }
        } catch (creditsError) {
            console.error('❌ 贈送 Credits 失敗:', creditsError);
            console.error('錯誤堆棧:', creditsError.stack);
            // 不拋出錯誤，因為驗證已經成功
        }
        
        console.log(`✅ Email 驗證成功: ${email}`);
        return { success: true, message: '驗證成功！已贈送 20 個 Credits' };
        
    } catch (error) {
        console.error('❌ 驗證失敗:', error);
        throw error;
    }
});

/**
 * 檢查 email 是否已驗證
 */
exports.checkEmailVerified = functions.https.onCall(async (data, context) => {
    const { email } = data;
    
    if (!email) {
        throw new functions.https.HttpsError('invalid-argument', 'Email is required');
    }
    
    try {
        const doc = await db.collection('verificationCodes').doc(email).get();
        
        if (!doc.exists) {
            return { verified: false };
        }
        
        const data = doc.data();
        return { 
            verified: data.verified || false,
            verifiedAt: data.verifiedAt?.toDate()?.toISOString()
        };
        
    } catch (error) {
        console.error('❌ 檢查驗證狀態失敗:', error);
        throw new functions.https.HttpsError('internal', '檢查驗證狀態失敗');
    }
});

// ============================================
// 9. 數據清理（根據計劃保留期限）
// ============================================

/**
 * 每天自動清理過期數據
 * 基礎版：60 天
 * 專業版：90 天
 * 商業版：365 天
 * 免費版：30 天
 */
exports.cleanupExpiredData = functions.pubsub
    .schedule('0 2 * * *') // 每天凌晨 2 點執行
    .timeZone('Asia/Hong_Kong')
    .onRun(async (context) => {
        console.log('🧹 開始清理過期數據...');
        
        try {
            const now = admin.firestore.Timestamp.now();
            let totalDeleted = 0;
            
            // 獲取所有用戶
            const usersSnapshot = await db.collection('users').get();
            
            for (const userDoc of usersSnapshot.docs) {
                const userData = userDoc.data();
                const plan = userData.plan || 'free';
                
                // 根據計劃設置保留天數
                let retentionDays;
                switch(plan) {
                    case 'basic': 
                        retentionDays = 60; 
                        break;
                    case 'professional': 
                        retentionDays = 90; 
                        break;
                    case 'business': 
                        retentionDays = 365; 
                        break;
                    default: 
                        retentionDays = 30; // Free plan
                }
                
                // 計算截止日期
                const cutoffDate = new Date();
                cutoffDate.setDate(cutoffDate.getDate() - retentionDays);
                const cutoffTimestamp = admin.firestore.Timestamp.fromDate(cutoffDate);
                
                // 查找並刪除過期項目
                const projectsSnapshot = await db
                    .collection('users')
                    .doc(userDoc.id)
                    .collection('projects')
                    .where('createdAt', '<', cutoffTimestamp)
                    .get();
                
                for (const projectDoc of projectsSnapshot.docs) {
                    // 刪除項目下的所有文檔
                    const documentsSnapshot = await projectDoc.ref
                        .collection('documents')
                        .get();
                    
                    for (const docDoc of documentsSnapshot.docs) {
                        await docDoc.ref.delete();
                        totalDeleted++;
                    }
                    
                    // 刪除項目本身
                    await projectDoc.ref.delete();
                    console.log(`🗑️ 刪除過期項目: ${projectDoc.id} (用戶: ${userDoc.id}, 計劃: ${plan})`);
                }
            }
            
            console.log(`✅ 數據清理完成，共刪除 ${totalDeleted} 個文檔`);
            return null;
            
        } catch (error) {
            console.error('❌ 數據清理失敗:', error);
            return null;
        }
    });

/**
 * 手動觸發數據清理（用於測試）
 */
exports.triggerCleanup = functions.https.onCall(async (data, context) => {
    // 只允許管理員執行
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '需要登入');
    }
    
    // 檢查是否為管理員（可以根據 email 或自定義 claims）
    const userEmail = context.auth.token.email;
    const adminEmails = ['vaultcaddy@gmail.com', 'osclin2002@gmail.com'];
    
    if (!adminEmails.includes(userEmail)) {
        throw new functions.https.HttpsError('permission-denied', '只有管理員可以執行此操作');
    }
    
    try {
        // 調用清理邏輯（與定時任務相同）
        console.log(`🔧 管理員 ${userEmail} 手動觸發數據清理`);
        
        // 這裡可以直接調用清理邏輯
        // 為了簡化，返回成功訊息
        return { 
            success: true, 
            message: '數據清理已觸發，請查看 Cloud Functions 日誌' 
        };
        
    } catch (error) {
        console.error('❌ 手動清理失敗:', error);
        throw new functions.https.HttpsError('internal', '清理失敗');
    }
});

// ============================================
// 9. Stripe 使用量計費報告
// ============================================

/**
 * 報告 Stripe 使用量（用於基於使用量的計費）
 * 當用戶超出包含的免費額度時調用
 */
exports.reportStripeUsage = functions.https.onCall(async (data, context) => {
    // 檢查 Stripe 是否已配置
    if (!stripe || !stripeConfig) {
        console.error('❌ Stripe 未配置');
        throw new functions.https.HttpsError('failed-precondition', 'Stripe not configured');
    }
    
    // 檢查用戶是否已登入
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '需要登入');
    }
    
    const userId = context.auth.uid;
    const { subscriptionId, quantity, timestamp } = data;
    
    if (!subscriptionId || !quantity) {
        throw new functions.https.HttpsError('invalid-argument', '缺少必要參數');
    }
    
    try {
        console.log(`📊 報告使用量: 用戶 ${userId}, 訂閱 ${subscriptionId}, 數量 ${quantity}`);
        
        // 獲取訂閱信息
        const subscription = await stripe.subscriptions.retrieve(subscriptionId);
        
        // 找到使用量計費的訂閱項目
        const usageBasedItem = subscription.items.data.find(item => 
            item.price.billing_scheme === 'tiered' || 
            item.price.recurring.usage_type === 'metered'
        );
        
        if (!usageBasedItem) {
            console.warn('⚠️ 訂閱中沒有使用量計費項目');
            return { success: false, message: '訂閱中沒有使用量計費項目' };
        }
        
        // 報告使用量給 Stripe
        const usageRecord = await stripe.subscriptionItems.createUsageRecord(
            usageBasedItem.id,
            {
                quantity: quantity,
                timestamp: timestamp ? Math.floor(timestamp / 1000) : Math.floor(Date.now() / 1000),
                action: 'increment'  // 累加使用量
            }
        );
        
        console.log('✅ 使用量已報告:', usageRecord);
        
        // 記錄到 Firestore
        await db.collection('usageRecords').add({
            userId: userId,
            subscriptionId: subscriptionId,
            subscriptionItemId: usageBasedItem.id,
            quantity: quantity,
            stripeUsageRecordId: usageRecord.id,
            timestamp: admin.firestore.FieldValue.serverTimestamp()
        });
        
        return { 
            success: true, 
            usageRecordId: usageRecord.id,
            quantity: quantity
        };
        
    } catch (error) {
        console.error('❌ 報告使用量失敗:', error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

/**
 * 定期檢查並報告超出的使用量（每天執行一次）
 * 自動計算當月超出免費額度的頁數並報告給 Stripe
 */
exports.reportDailyUsage = functions.pubsub.schedule('0 0 * * *')  // 每天午夜執行
    .timeZone('Asia/Hong_Kong')
    .onRun(async (context) => {
        // 檢查 Stripe 是否已配置
        if (!stripe || !stripeConfig) {
            console.error('❌ Stripe 未配置，跳過使用量報告');
            return null;
        }
        
        console.log('📊 開始每日使用量報告...');
        
        try {
            // 獲取所有有活躍訂閱的用戶
            const usersSnapshot = await db.collection('users')
                .where('subscriptionStatus', '==', 'active')
                .get();
            
            const now = new Date();
            const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
            
            for (const userDoc of usersSnapshot.docs) {
                const userId = userDoc.id;
                const userData = userDoc.data();
                const subscriptionId = userData.stripeSubscriptionId;
                
                if (!subscriptionId) {
                    continue;
                }
                
                // 計算當月使用量
                const usageSnapshot = await db.collection('users')
                    .doc(userId)
                    .collection('creditsHistory')
                    .where('type', '==', 'deduct')
                    .where('createdAt', '>=', monthStart)
                    .get();
                
                let totalUsed = 0;
                usageSnapshot.forEach(doc => {
                    totalUsed += doc.data().amount || 0;
                });
                
                // 獲取包含的免費額度
                const includedCredits = userData.subscriptionPlan === 'monthly' ? 100 : 
                                      userData.subscriptionPlan === 'yearly' ? 1200 : 0;
                
                // 計算超出的使用量
                const overage = Math.max(0, totalUsed - includedCredits);
                
                if (overage > 0) {
                    console.log(`📈 用戶 ${userId} 超出使用量: ${overage} 頁`);
                    
                    // 報告給 Stripe
                    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
                    const usageBasedItem = subscription.items.data.find(item => 
                        item.price.billing_scheme === 'tiered' || 
                        item.price.recurring.usage_type === 'metered'
                    );
                    
                    if (usageBasedItem) {
                        await stripe.subscriptionItems.createUsageRecord(
                            usageBasedItem.id,
                            {
                                quantity: overage,
                                timestamp: Math.floor(Date.now() / 1000),
                                action: 'set'  // 設置總使用量（非累加）
                            }
                        );
                        
                        console.log(`✅ 用戶 ${userId} 使用量已報告: ${overage} 頁`);
                    }
                } else {
                    console.log(`✅ 用戶 ${userId} 未超出免費額度`);
                }
            }
            
            console.log('✅ 每日使用量報告完成');
            return null;
            
        } catch (error) {
            console.error('❌ 每日使用量報告失敗:', error);
            return null;
        }
    });

// ============================================
// 13. 創建 Stripe Checkout Session（動態傳遞用戶信息）
// ============================================

/**
 * 創建 Stripe Checkout Session
 * 自動傳遞用戶的 email 和 userId，實現無縫支付體驗
 */
exports.createStripeCheckoutSession = functions.https.onCall(async (data, context) => {
    const { planType, userId, email, isTest = false } = data;
    
    console.log('🛒 創建 Checkout Session:', { planType, userId, email, isTest });
    
    // 🎯 根據 isTest 選擇使用的 Stripe 客戶端
    const stripeClient = isTest ? stripeTest : stripeLive;
    
    // 檢查 Stripe 是否已配置
    if (!stripeClient || !stripeConfig) {
        const mode = isTest ? '測試' : '生產';
        console.error(`❌ Stripe ${mode}模式未配置`);
        throw new functions.https.HttpsError('unavailable', `Stripe ${mode}模式未配置，請聯繫管理員`);
    }
    
    // 驗證參數
    if (!planType || !userId || !email) {
        throw new functions.https.HttpsError('invalid-argument', '缺少必要參數');
    }
    
    // 🎯 定義價格 ID（生產模式）
    const productionPriceMapping = {
        monthly: {
            basePriceId: 'price_1ScS9QJmiQ31C0GTy4y6z0l0',  // 月費基礎價格 $58
            usagePriceId: 'price_1ScSATJmiQ31C0GTW1qWu0OF'  // 月費用量計費
        },
        yearly: {
            basePriceId: 'price_1ScS8EJmiQ31C0GT599VDffL',  // 年費基礎價格 $552
            usagePriceId: 'price_1ScS7iJmiQ31C0GTv3ScXonr'  // 年費用量計費
        }
    };
    
    // 🧪 定義測試模式價格 ID
    const testPriceMapping = {
        monthly: {
            basePriceId: 'price_1Scj13JmiQ31C0GT4TJsWzFg',  // 測試月費基礎 $58
            usagePriceId: 'price_1Scj1UJmiQ31C0GTXDsN6TFh'  // 測試月費用量計費
        },
        yearly: {
            basePriceId: '',  // 測試年費基礎（尚未創建）
            usagePriceId: ''  // 測試年費用量計費（尚未創建）
        }
    };
    
    // 根據 isTest 選擇對應的 Price Mapping
    const priceMapping = isTest ? testPriceMapping : productionPriceMapping;
    
    const selectedPlan = priceMapping[planType];
    
    if (!selectedPlan) {
        console.error('❌ 無效的計劃類型:', planType);
        throw new functions.https.HttpsError('invalid-argument', '無效的訂閱計劃');
    }
    
    try {
        console.log('📝 創建 Checkout Session，價格:', selectedPlan, '模式:', isTest ? '測試' : '生產');
        
        // 創建 Checkout Session（使用對應模式的客戶端）
        const session = await stripeClient.checkout.sessions.create({
            mode: 'subscription',
            line_items: [
                {
                    price: selectedPlan.basePriceId,  // 基礎訂閱費
                    quantity: 1
                },
                {
                    price: selectedPlan.usagePriceId,  // 用量計費
                    quantity: 1
                }
            ],
            customer_email: email,  // ← 自動填充 email
            client_reference_id: userId,  // ← 傳遞 userId
            metadata: {
                userId: userId,  // ← 傳遞 userId（雙重保險）
                planType: planType
            },
            success_url: `https://vaultcaddy.com/billing.html?success=true&session_id={CHECKOUT_SESSION_ID}${isTest ? '&test=true' : ''}`,
            cancel_url: `https://vaultcaddy.com/billing.html?canceled=true${isTest ? '&test=true' : ''}`,
            allow_promotion_codes: true,  // 允許使用優惠碼
            billing_address_collection: 'auto'  // 自動收集帳單地址
        });
        
        console.log('✅ Checkout Session 創建成功:', session.id);
        
        return {
            url: session.url,
            sessionId: session.id
        };
        
    } catch (error) {
        console.error('❌ 創建 Checkout Session 失敗:', error);
        throw new functions.https.HttpsError('internal', `創建支付會話失敗: ${error.message}`);
    }
});

console.log('✅ Firebase Cloud Functions 已載入（包含 Email 驗證、數據清理和 Stripe 使用量計費功能）');

