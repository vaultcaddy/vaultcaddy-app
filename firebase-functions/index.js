/**
 * Firebase Cloud Functions for Credits Management
 * 
 * 功能：
 * 1. 自動處理 Credits 分配
 * 2. 處理 Stripe 付款回調
 * 3. 管理訂閱計劃
 * 4. Credits 過期管理
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const stripe = require('stripe')(functions.config().stripe.secret_key);

admin.initializeApp();
const db = admin.firestore();

// ============================================
// 1. 處理 Stripe Webhook（付款成功後自動添加 Credits）
// ============================================

exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = functions.config().stripe.webhook_secret;
    
    let event;
    
    try {
        event = stripe.webhooks.constructEvent(req.rawBody, sig, endpointSecret);
    } catch (err) {
        console.error('❌ Webhook signature verification failed:', err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    
    // 處理不同類型的 Stripe 事件
    switch (event.type) {
        case 'checkout.session.completed':
            await handleCheckoutCompleted(event.data.object);
            break;
        case 'payment_intent.succeeded':
            await handlePaymentSuccess(event.data.object);
            break;
        case 'customer.subscription.created':
        case 'customer.subscription.updated':
            await handleSubscriptionChange(event.data.object);
            break;
        case 'customer.subscription.deleted':
            await handleSubscriptionCancelled(event.data.object);
            break;
        default:
            console.log(`未處理的事件類型: ${event.type}`);
    }
    
    res.json({ received: true });
});

/**
 * 處理結帳完成
 */
async function handleCheckoutCompleted(session) {
    console.log('✅ 結帳完成:', session.id);
    
    const userId = session.client_reference_id || session.metadata?.userId;
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID');
        return;
    }
    
    // 獲取購買的產品信息
    const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
    
    for (const item of lineItems.data) {
        const productId = item.price.product;
        const product = await stripe.products.retrieve(productId);
        
        // 根據產品類型添加 Credits
        const credits = parseInt(product.metadata.credits || 0);
        
        if (credits > 0) {
            await addCredits(userId, credits, {
                source: 'purchase',
                stripeSessionId: session.id,
                productName: product.name,
                amount: session.amount_total / 100,
                currency: session.currency
            });
        }
    }
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
async function handleSubscriptionChange(subscription) {
    console.log('✅ 訂閱變更:', subscription.id);
    
    const userId = subscription.metadata?.userId;
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID');
        return;
    }
    
    // 獲取訂閱計劃信息
    const priceId = subscription.items.data[0].price.id;
    const product = await stripe.products.retrieve(subscription.items.data[0].price.product);
    
    // 確定計劃類型和 Credits
    let planType = 'free';
    let monthlyCredits = 0;
    
    if (product.metadata.plan_type) {
        planType = product.metadata.plan_type; // basic, pro, business
        monthlyCredits = parseInt(product.metadata.monthly_credits || 0);
    }
    
    // 更新用戶訂閱信息
    await db.collection('users').doc(userId).update({
        subscription: {
            stripeSubscriptionId: subscription.id,
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
    if (subscription.status === 'active') {
        await addCredits(userId, monthlyCredits, {
            source: 'subscription',
            planType: planType,
            period: `${new Date(subscription.current_period_start * 1000).toISOString()} - ${new Date(subscription.current_period_end * 1000).toISOString()}`
        });
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

console.log('✅ Firebase Cloud Functions 已載入');

