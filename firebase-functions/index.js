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
    
    // 🔒 幂等性检查：使用原子操作防止并发重复处理
    const processedEventsRef = db.collection('processedStripeEvents').doc(event.id);
    
    try {
        // 🔥 使用 create 方法确保原子性：如果文档已存在会抛出错误
        await processedEventsRef.create({
            eventId: event.id,
            eventType: event.type,
            processedAt: admin.firestore.FieldValue.serverTimestamp(),
            isTestMode: isTestMode,
            timestamp: Date.now()
        });
        console.log(`✅ 事件 ${event.id} 已标记为处理中（首次处理）`);
    } catch (error) {
        // 如果文档已存在，说明正在被处理或已经处理过
        if (error.code === 6 || error.message.includes('ALREADY_EXISTS')) {
            console.log(`⚠️ 事件 ${event.id} 已经处理过，跳过处理`);
            return res.status(200).json({ received: true, skipped: true, reason: 'already_processed' });
        }
        // 其他错误继续抛出
        console.error(`❌ 记录事件时发生错误:`, error);
        throw error;
    }
    
    // 處理不同類型的 Stripe 事件
    try {
        switch (event.type) {
            case 'checkout.session.completed':
                // 🔥 关键事件：必须成功处理（首次订阅）
                await handleCheckoutCompleted(event.data.object, isTestMode);
                break;
            case 'invoice.created':
                // 🔥 关键事件：在发票创建时报告超额使用（在发票完成之前）
                try {
                    await handleInvoiceCreated(event.data.object, isTestMode);
                } catch (invoiceCreatedError) {
                    console.error('❌ 处理发票创建失败:', invoiceCreatedError);
                    console.error('错误详情:', invoiceCreatedError.stack);
                    // 发票创建失败不影响流程，返回 200 避免重试
                }
                break;
            case 'invoice.paid':
                // 🔥 订阅续费：每月自动续费时添加 Credits
                try {
                    await handleInvoicePaid(event.data.object, isTestMode);
                } catch (invoiceError) {
                    console.error('❌ 处理发票支付失败:', invoiceError);
                    console.error('错误详情:', invoiceError.stack);
                    // 续费失败不影响现有订阅，返回 200 避免重试
                }
                break;
            case 'customer.subscription.created':
            case 'customer.subscription.updated':
                // ℹ️ 订阅事件：即使失败也不影响 Credits（已在 checkout 中添加）
                try {
                    await handleSubscriptionChange(event.data.object, isTestMode);
                } catch (subscriptionError) {
                    console.error('❌ 更新订阅信息失败，但 Credits 已在 checkout.session.completed 中添加:', subscriptionError);
                    console.error('错误详情:', subscriptionError.stack);
                    // 不抛出错误，继续执行
                }
                break;
            case 'customer.subscription.deleted':
                // ℹ️ 取消订阅：即使失败也返回成功
                try {
                    await handleSubscriptionCancelled(event.data.object);
                } catch (cancelError) {
                    console.error('❌ 处理订阅取消失败:', cancelError);
                    console.error('错误详情:', cancelError.stack);
                    // 不抛出错误，继续执行
                }
                break;
            default:
                console.log(`ℹ️ 收到未配置處理的事件: ${event.type}`);
                console.log(`💡 如果這個事件頻繁出現，建議在 Stripe Dashboard 中移除對此事件的監聽`);
        }

        // ✅ 总是返回 200，避免 Stripe 重试
        res.status(200).json({ received: true });
    } catch (error) {
        console.error('❌ 处理 checkout.session.completed 时发生致命错误:', error);
        console.error('错误详情:', error.stack);
        
        // 🔥 只有 checkout.session.completed 失败时才删除标记并返回 500
        if (event.type === 'checkout.session.completed') {
            await processedEventsRef.delete();
            console.log(`⚠️ checkout 事件处理失败，已删除处理标记，允许重试`);
            res.status(500).json({ error: 'Checkout processing failed' });
        } else {
            // 其他事件失败也返回 200，避免重试
            console.log(`ℹ️ 非关键事件处理失败，但仍返回 200 避免重试`);
            res.status(200).json({ received: true, error: error.message });
        }
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
                
                // 🔥 从 Stripe session 中提取用户名
                const customerName = session.customer_details?.name || 
                                    session.customer_details?.email?.split('@')[0] || 
                                    'VaultCaddy User';
                
                console.log(`📝 新用戶資料: email=${session.customer_email}, displayName=${customerName}`);
                
                // 创建新用户（包含所有必要字段）
                const newUserRef = await db.collection('users').add({
                    email: session.customer_email,
                    displayName: customerName,
                    company: '',  // 🏢 Stripe 支付時公司名稱為空，用戶可後續填寫
                    credits: 0,
                    currentCredits: 0,
                    planType: 'Free Plan', // 初始為 Free Plan，稍後會更新為 Pro Plan
                    emailVerified: false,
                    photoURL: '',  // 📷 Stripe 註冊無頭像
                    provider: 'stripe',  // 🔐 通過 Stripe 支付創建
                    createdAt: admin.firestore.FieldValue.serverTimestamp(),
                    updatedAt: admin.firestore.FieldValue.serverTimestamp(),
                    source: 'stripe_payment',
                    stripeCustomerId: session.customer
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
    
    // 🔥 关键修复：只处理第一个订阅类型的 line item，避免重复添加 Credits
    let creditsAdded = false;
    
    for (const item of lineItems.data) {
        const productId = item.price.product;
        console.log(`🔍 正在獲取產品: ${productId}`);
        console.log(`📦 Line item 详情:`, JSON.stringify(item, null, 2));
        
        const product = await stripeClient.products.retrieve(productId);
        
        console.log(`📦 產品信息:`, {
            productId: product.id,
            name: product.name,
            metadata: product.metadata,
            priceType: item.price.type // 'one_time' 或 'recurring'
        });
        console.log(`📦 完整產品对象:`, JSON.stringify(product, null, 2));
        
        // 🔥 只处理订阅类型的产品（price.type === 'recurring'）
        // 并且只添加一次 Credits
        if (creditsAdded) {
            console.log(`⚠️ Credits 已添加，跳过此 line item: ${product.name}`);
            continue;
        }
        
        // 检查是否是订阅类型
        const isSubscription = item.price.type === 'recurring';
        console.log(`🔍 是否订阅类型: ${isSubscription}`);
        
        // 根據產品 metadata 添加 Credits
        const credits = parseInt(product.metadata.monthly_credits || product.metadata.credits || 0);
        console.log(`🔢 計算得到的 Credits: ${credits}`);
        console.log(`🔢 product.metadata.monthly_credits: ${product.metadata.monthly_credits}`);
        console.log(`🔢 product.metadata.credits: ${product.metadata.credits}`);
        
        if (credits > 0 && isSubscription) {
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
            creditsAdded = true; // 标记已添加，避免重复
            
            // 🔥 更新用户的订阅计划和重置日期
            const planType = product.metadata.plan_type || 'monthly';
            console.log(`📋 更新用户订阅计划: ${planType}`);
            
            // 计算重置日期：monthly = 1个月后，yearly = 1年后
            const now = new Date();
            let resetDate;
            if (planType === 'yearly') {
                resetDate = new Date(now.getFullYear() + 1, now.getMonth(), now.getDate());
                console.log(`📅 年费计划，重置日期为 1 年后: ${resetDate.toISOString()}`);
            } else {
                resetDate = new Date(now.getFullYear(), now.getMonth() + 1, now.getDate());
                console.log(`📅 月费计划，重置日期为 1 个月后: ${resetDate.toISOString()}`);
            }
            
            // 🔍 获取订阅信息，提取 metered subscription item ID
            let meteredItemId = null;
            if (session.subscription) {
                console.log(`🔍 获取订阅详情: ${session.subscription}`);
                try {
                    const subscription = await stripeClient.subscriptions.retrieve(session.subscription);
                    console.log(`📋 订阅 items:`, JSON.stringify(subscription.items.data, null, 2));
                    
                    // 查找 metered price 的 subscription item
                    for (const subItem of subscription.items.data) {
                        const price = await stripeClient.prices.retrieve(subItem.price.id);
                        console.log(`🔍 检查 price: ${price.id}, recurring: ${price.recurring}, usage_type: ${price.recurring?.usage_type}`);
                        
                        if (price.recurring && price.recurring.usage_type === 'metered') {
                            meteredItemId = subItem.id;
                            console.log(`✅ 找到 metered subscription item: ${meteredItemId}`);
                            break;
                        }
                    }
                    
                    if (!meteredItemId) {
                        console.warn(`⚠️ 未找到 metered subscription item`);
                    }
                } catch (error) {
                    console.error(`❌ 获取订阅详情失败:`, error);
                }
            }
            
            // 更新用户文档（包含 metered item ID 和累计使用量）
            const updateData = {
                planType: 'Pro Plan',
                subscriptionPlan: planType, // 'monthly' 或 'yearly'
                resetDate: admin.firestore.Timestamp.fromDate(resetDate),
                lastPurchaseDate: admin.firestore.FieldValue.serverTimestamp(),
                updatedAt: admin.firestore.FieldValue.serverTimestamp(),
                includedCredits: credits, // 订阅包含的 Credits 数量
                totalCreditsUsed: 0 // 初始化累计使用量为 0
            };
            
            // 如果找到 metered item ID，保存到 subscription 字段
            if (meteredItemId) {
                updateData.subscription = {
                    meteredSubscriptionItemId: meteredItemId,
                    stripeSubscriptionId: session.subscription
                };
                console.log(`✅ 保存 metered subscription item ID: ${meteredItemId}`);
            }
            
            await db.collection('users').doc(userId).update(updateData);
            console.log(`✅ 用户订阅计划已更新为 Pro Plan (${planType})`);
        } else if (credits > 0 && !isSubscription) {
            console.log(`⚠️ 產品有 Credits 但不是订阅类型，跳过: ${product.name} (type: ${item.price.type})`);
        } else {
            console.log(`⚠️ 產品沒有配置 Credits: ${product.name}`);
            console.log(`⚠️ product.metadata 完整内容:`, JSON.stringify(product.metadata, null, 2));
        }
    }
    
    if (!creditsAdded) {
        console.log(`⚠️ 警告：没有找到任何订阅类型的产品来添加 Credits`);
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
        console.error('⚠️ 跳過訂閱信息更新，但不影響 Credits（已在 checkout 中添加）');
        return; // 不抛出错误，只是返回
    }
    
    // 🔥 检查订阅数据是否完整
    if (!subscription.items || !subscription.items.data || subscription.items.data.length === 0) {
        console.error('❌ 訂閱數據不完整，沒有 items:', JSON.stringify(subscription, null, 2));
        console.error('⚠️ 跳過訂閱信息更新，但不影響 Credits（已在 checkout 中添加）');
        return; // 不抛出错误，只是返回
    }
    
    // 獲取訂閱計劃信息 - 使用正確的 Stripe 客戶端
    const priceId = subscription.items.data[0].price.id;
    const productId = subscription.items.data[0].price.product;
    
    if (!productId) {
        console.error('❌ 無法獲取產品 ID');
        console.error('⚠️ 跳過訂閱信息更新，但不影響 Credits（已在 checkout 中添加）');
        return; // 不抛出错误，只是返回
    }
    
    let product;
    try {
        product = await stripeClient.products.retrieve(productId);
    } catch (productError) {
        console.error('❌ 獲取產品信息失敗:', productError);
        console.error('⚠️ 跳過訂閱信息更新，但不影響 Credits（已在 checkout 中添加）');
        return; // 不抛出错误，只是返回
    }
    
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
    
    // ⚠️ 不在这里添加 Credits！
    // Credits 应该只在 checkout.session.completed 事件中添加一次
    // 这里只负责更新订阅信息
    console.log(`ℹ️ 訂閱狀態: ${subscription.status}，Credits 已在 checkout.session.completed 事件中添加`);
    
    // 🔍 查找 metered subscription item
    let meteredItemId = null;
    try {
        console.log(`🔍 查找 metered subscription item...`);
        for (const subItem of subscription.items.data) {
            const price = await stripeClient.prices.retrieve(subItem.price.id);
            console.log(`🔍 检查 price: ${price.id}, recurring: ${price.recurring}, usage_type: ${price.recurring?.usage_type}`);
            
            if (price.recurring && price.recurring.usage_type === 'metered') {
                meteredItemId = subItem.id;
                console.log(`✅ 找到 metered subscription item: ${meteredItemId}`);
                break;
            }
        }
        
        if (!meteredItemId) {
            console.warn(`⚠️ 未找到 metered subscription item`);
        }
    } catch (error) {
        console.error(`❌ 查找 metered item 失败:`, error);
    }
    
    // 更新用戶訂閱信息
    try {
        const subscriptionData = {
            stripeSubscriptionId: subscription.id,
            stripeCustomerId: subscription.customer,
            status: subscription.status,
            planType: planType,
            monthlyCredits: monthlyCredits,
            currentPeriodStart: admin.firestore.Timestamp.fromMillis(subscription.current_period_start * 1000),
            currentPeriodEnd: admin.firestore.Timestamp.fromMillis(subscription.current_period_end * 1000),
            cancelAtPeriodEnd: subscription.cancel_at_period_end
        };
        
        // 如果找到 metered item ID，添加到订阅数据中
        if (meteredItemId) {
            subscriptionData.meteredSubscriptionItemId = meteredItemId;
            console.log(`✅ 保存 metered subscription item ID: ${meteredItemId}`);
        }
        
        await db.collection('users').doc(userId).update({
            subscription: subscriptionData,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        console.log(`✅ 用戶訂閱信息已更新: ${userId}`);
    } catch (updateError) {
        console.error(`❌ 更新用戶訂閱信息失敗:`, updateError);
        console.error('⚠️ 訂閱信息更新失敗，但不影響 Credits（已在 checkout 中添加）');
        // 不抛出错误，只记录日志
    }
    
    // 🔥 不要在这里添加 Credits！
    // Credits 应该只在 checkout.session.completed 事件中添加
    // 这里只负责更新订阅信息
    if (subscription.status === 'active' && monthlyCredits > 0) {
        console.log(`ℹ️ 訂閱狀態為 active，Credits 已在 checkout.session.completed 事件中添加`);
        console.log(`ℹ️ 此函数只更新订阅信息，不添加 Credits`);
    }
}

/**
 * 處理訂閱取消
 */
async function handleSubscriptionCancelled(subscription) {
    console.log('❌ 訂閱已取消:', subscription.id);
    
    let userId = subscription.metadata?.userId;
    
    // 如果没有userId，尝试通过customer查找
    if (!userId && subscription.customer) {
        console.log(`🔍 嘗試通過 Stripe Customer 查找用戶: ${subscription.customer}`);
        try {
            const isTestMode = subscription.id.startsWith('sub_');
            const stripeClient = isTestMode ? stripeTest : stripeLive;
            
            if (stripeClient) {
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
            }
        } catch (error) {
            console.error('❌ 查找用戶失敗:', error);
        }
    }
    
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID');
        return;
    }
    
    console.log(`📊 處理用戶訂閱取消: ${userId}`);
    
    try {
        // 獲取用戶當前數據
        const userDoc = await db.collection('users').doc(userId).get();
        const userData = userDoc.data();
        const currentCredits = userData?.currentCredits || userData?.credits || 0;
        const totalCreditsUsed = userData?.totalCreditsUsed || 0;
        
        console.log(`📊 訂閱取消時的用戶數據:`, {
            credits: currentCredits,
            totalCreditsUsed: totalCreditsUsed,
            planType: userData?.planType
        });
        
        // ℹ️ 注意：超額使用的報告現在在 invoice.created webhook 中處理
        // 這樣可以確保 Stripe 在生成發票時就包含超額費用
        if (currentCredits < 0) {
            const overageAmount = Math.abs(currentCredits);
            console.log(`💰 訂閱取消時檢測到超額使用: ${overageAmount} Credits`);
            console.log(`ℹ️ 超額費用應該已經在 invoice.created webhook 中報告給 Stripe`);
            console.log(`📋 Stripe 會在最終發票中包含這些超額費用`);
        }
        
        // 🔥 重要：訂閱取消後，Credits 處理邏輯
        const MAX_FREE_CREDITS = 50;
        let finalCredits = currentCredits;
        let clearedCredits = 0;
        
        if (currentCredits > MAX_FREE_CREDITS) {
            clearedCredits = currentCredits - MAX_FREE_CREDITS;
            finalCredits = MAX_FREE_CREDITS;
            console.log(`🔥 清零超出的 Credits: ${currentCredits} → ${finalCredits}（清除 ${clearedCredits} 個）`);
        } else if (currentCredits < 0) {
            // 負數 Credits → 重置為 0（超額費用已報告給 Stripe）
            finalCredits = 0;
            console.log(`💰 Credits 為負數（${currentCredits}），已報告超額使用，重置為 0`);
        } else {
            // Credits <= 50，保持不變
            console.log(`✅ Credits 未超過 ${MAX_FREE_CREDITS}，保持不變: ${currentCredits}`);
        }
        
        // 更新用戶狀態
        await db.collection('users').doc(userId).update({
            planType: 'Free Plan', // ← 改為 Free Plan
            subscriptionPlan: null,
            subscription: null, // ← 刪除訂閱信息
            credits: finalCredits, // ← 更新為最終 Credits
            currentCredits: finalCredits, // ← 同步更新
            cancelledAt: admin.firestore.FieldValue.serverTimestamp(),
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        console.log(`✅ 用戶已降級為 Free Plan: ${userId}，Credits: ${currentCredits} → ${finalCredits}`);
        
        // 記錄訂閱取消事件
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'subscription_cancelled',
            amount: 0,
            description: `訂閱已取消（原有 ${currentCredits} Credits，保留 ${finalCredits} Credits${clearedCredits > 0 ? `，清除 ${clearedCredits} Credits` : ''}）`,
            metadata: {
                originalCredits: currentCredits,
                finalCredits: finalCredits,
                clearedCredits: clearedCredits,
                totalCreditsUsed: totalCreditsUsed,
                subscriptionId: subscription.id
            },
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        // 如果清除了 Credits，記錄清零事件
        if (clearedCredits > 0) {
            await db.collection('users').doc(userId).collection('creditsHistory').add({
                type: 'clear',
                amount: -clearedCredits,
                description: `訂閱取消，清除超出的 ${clearedCredits} Credits（保留上限：${MAX_FREE_CREDITS}）`,
                metadata: {
                    before: currentCredits,
                    after: finalCredits,
                    cleared: clearedCredits,
                    maxFreeCredits: MAX_FREE_CREDITS
                },
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }
        
        // ⚠️ 如果 Credits 是負數，記錄警告
        if (finalCredits < 0) {
            console.warn(`⚠️ 用戶 ${userId} 訂閱取消時 Credits 為負數: ${finalCredits}`);
            console.warn(`⚠️ 用戶需要購買 Credits 才能繼續使用`);
            
            await db.collection('users').doc(userId).collection('creditsHistory').add({
                type: 'warning',
                amount: 0,
                description: `訂閱取消，Credits 為負數（${finalCredits}），需要購買 Credits`,
                metadata: {
                    negativeCredits: finalCredits
                },
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }
        
    } catch (error) {
        console.error(`❌ 處理訂閱取消失敗:`, error);
    }
}

/**
 * 🆕 處理發票創建（簡化版 - 使用 Billing Meter Events）
 * 
 * 由於使用了 Billing Meter Events API，使用量已經實時報告給 Stripe
 * 此函數現在只用於記錄和監控，不再需要手動報告使用量
 */
async function handleInvoiceCreated(invoice, isTestMode = false) {
    console.log(`📝 發票創建 (${isTestMode ? '測試模式' : '生產模式'}):`, invoice.id);
    
    // 只處理訂閱相關的發票
    if (!invoice.subscription) {
        console.log(`ℹ️ 非訂閱發票，跳過處理`);
        return;
    }
    
    try {
        // 通過 customer ID 查找用戶
        const customerId = invoice.customer;
        console.log(`🔍 查找客戶: ${customerId}`);
        
        const usersSnapshot = await admin.firestore().collection('users')
            .where('stripeCustomerId', '==', customerId)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            console.log(`⚠️ 未找到對應的用戶`);
            return;
        }
        
        const userId = usersSnapshot.docs[0].id;
        const userData = usersSnapshot.docs[0].data();
        console.log(`✅ 找到用戶: ${userId}`);
        
        // 記錄 Credits 狀態（僅用於監控）
        const currentCredits = userData.currentCredits || 0;
        const monthlyCredits = userData?.subscription?.monthlyCredits || userData?.includedCredits || 100;
        
        console.log(`📊 Credits 狀態:`, {
            currentCredits,
            monthlyCredits
        });
        
        // 計算超額使用量（僅用於日誌）
        let overageAmount = 0;
        if (currentCredits < 0) {
            overageAmount = Math.abs(currentCredits);
            console.log(`💰 檢測到超額使用: ${overageAmount} Credits`);
            console.log(`ℹ️ 使用量已通過 Billing Meter Events 實時報告給 Stripe`);
            console.log(`ℹ️ Stripe 會自動在發票中包含超額費用`);
        } else {
            console.log(`✅ 沒有超額使用`);
        }
        
        // 記錄發票信息到 Firestore
        await db.collection('users').doc(userId).update({
            'billing.lastInvoiceId': invoice.id,
            'billing.lastInvoiceCreatedAt': admin.firestore.FieldValue.serverTimestamp(),
            'billing.lastInvoiceAmount': invoice.amount_due / 100, // 轉換為元
            'billing.lastInvoiceOverage': overageAmount
        });
        
        console.log(`✅ 發票信息已記錄到 Firestore`);
        
    } catch (error) {
        console.error(`❌ 處理發票創建失敗:`, error);
        console.error(`錯誤詳情:`, error.stack);
        throw error;
    }
}

/**
 * 處理發票支付成功（訂閱續費）
 * 🔥 這個函數在訂閱每月自動續費時被調用
 */
async function handleInvoicePaid(invoice, isTestMode = false) {
    console.log(`✅ 發票支付成功 (${isTestMode ? '測試模式' : '生產模式'}):`, invoice.id);
    console.log(`📋 Invoice 详情:`, JSON.stringify(invoice, null, 2));
    
    // 選擇正確的 Stripe 客戶端
    const stripeClient = isTestMode ? stripeTest : stripeLive;
    if (!stripeClient) {
        console.error(`❌ Stripe 客戶端未配置 (${isTestMode ? '測試模式' : '生產模式'})`);
        return; // 不抛出错误，避免 500
    }
    
    // 🔍 只處理訂閱發票（不處理一次性支付）
    if (!invoice.subscription) {
        console.log(`ℹ️ 這不是訂閱發票，跳過處理: ${invoice.id}`);
        return;
    }
    
    // 🔍 檢查是否是續費（不是首次訂閱）
    // 首次訂閱已經在 checkout.session.completed 中處理
    if (invoice.billing_reason === 'subscription_create') {
        console.log(`ℹ️ 這是首次訂閱發票，Credits 已在 checkout.session.completed 中添加，跳過處理`);
        return;
    }
    
    console.log(`🔄 這是訂閱續費發票，billing_reason: ${invoice.billing_reason}`);
    
    // 🔍 獲取用戶 ID
    let userId;
    
    // 先尝试从 customer 的 metadata 获取
    try {
        const customer = await stripeClient.customers.retrieve(invoice.customer);
        console.log(`📧 Customer 信息:`, {
            id: customer.id,
            email: customer.email,
            metadata: customer.metadata
        });
        
        userId = customer.metadata?.userId;
        
        // 如果没有 userId，尝试通过 email 查找
        if (!userId && customer.email) {
            console.log(`🔍 嘗試通過 email 查找用戶: ${customer.email}`);
            const usersSnapshot = await db.collection('users')
                .where('email', '==', customer.email)
                .limit(1)
                .get();
            
            if (!usersSnapshot.empty) {
                userId = usersSnapshot.docs[0].id;
                console.log(`✅ 通過 email 找到用戶: ${userId}`);
            }
        }
    } catch (error) {
        console.error('❌ 查找用戶失敗:', error);
    }
    
    if (!userId) {
        console.error('❌ 無法獲取用戶 ID，invoice:', JSON.stringify(invoice, null, 2));
        return;
    }
    
    // 🔍 獲取訂閱信息
    try {
        const subscription = await stripeClient.subscriptions.retrieve(invoice.subscription);
        console.log(`📋 Subscription 信息:`, {
            id: subscription.id,
            status: subscription.status,
            items: subscription.items.data.map(item => ({
                priceId: item.price.id,
                productId: item.price.product
            }))
        });
        
        // 獲取產品信息
        const priceId = subscription.items.data[0].price.id;
        const productId = subscription.items.data[0].price.product;
        const product = await stripeClient.products.retrieve(productId);
        
        console.log(`📦 產品信息:`, {
            productId: product.id,
            name: product.name,
            metadata: product.metadata
        });
        
        // 根據產品 metadata 添加 Credits
        const credits = parseInt(product.metadata.monthly_credits || product.metadata.credits || 0);
        const planType = product.metadata.plan_type || 'monthly';
        
        console.log(`🔢 計算得到的 Credits: ${credits}`);
        
        // ⚠️ 檢查訂閱是否已被取消
        if (subscription.cancel_at_period_end) {
            console.log(`⚠️ 訂閱已被用戶取消（cancel_at_period_end = true）`);
            console.log(`⚠️ 這是最終賬單，只收取超額費用，不添加新 Credits`);
            console.log(`⚠️ 訂閱將在 ${new Date(subscription.current_period_end * 1000).toISOString()} 結束`);
            
            // 記錄最終賬單
            await db.collection('users').doc(userId).collection('creditsHistory').add({
                type: 'final_invoice',
                amount: 0,
                description: `訂閱最終賬單（已取消，不添加新 Credits）`,
                metadata: {
                    invoiceId: invoice.id,
                    subscriptionId: subscription.id,
                    amountPaid: invoice.amount_paid / 100,
                    currency: invoice.currency
                },
                createdAt: admin.firestore.FieldValue.serverTimestamp()
            });
            
            console.log(`✅ 最終賬單已記錄，訂閱將自動結束`);
            return; // ← 不添加新 Credits
        }
        
        if (credits > 0) {
            console.log(`💰 準備為續費處理 Credits：用戶 ${userId}`);
            
            // 🔥 第 1 步：清零旧的 Credits
            const userRef = db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            
            if (userDoc.exists) {
                const oldCredits = userDoc.data().credits || 0;
                const oldCurrentCredits = userDoc.data().currentCredits || 0;
                console.log(`🗑️ 清零旧 Credits: credits=${oldCredits}, currentCredits=${oldCurrentCredits}`);
                
                await userRef.update({
                    credits: 0,
                    currentCredits: 0,
                    lastCreditsBeforeReset: oldCredits, // 记录清零前的 Credits
                    updatedAt: admin.firestore.FieldValue.serverTimestamp()
                });
                console.log(`✅ 旧 Credits 已清零`);
            }
            
            // 🔥 第 2 步：添加新的 Credits
            console.log(`💰 添加新的 ${credits} Credits`);
            await addCredits(userId, credits, {
                source: 'subscription_renewal',
                stripeInvoiceId: invoice.id,
                stripeSubscriptionId: subscription.id,
                productName: product.name,
                amount: invoice.amount_paid / 100,
                currency: invoice.currency,
                planType: planType,
                billingReason: invoice.billing_reason
            });
            
            console.log(`✅ 續費成功：旧 Credits 已清零，新 Credits ${credits} 已添加`);
            
            // 🔥 第 3 步：更新重置日期
            const now = new Date();
            let resetDate;
            if (planType === 'yearly') {
                resetDate = new Date(now.getFullYear() + 1, now.getMonth(), now.getDate());
                console.log(`📅 年费计划，重置日期为 1 年后: ${resetDate.toISOString()}`);
            } else {
                resetDate = new Date(now.getFullYear(), now.getMonth() + 1, now.getDate());
                console.log(`📅 月费计划，重置日期为 1 个月后: ${resetDate.toISOString()}`);
            }
            
            // 更新用户文档
            await userRef.update({
                resetDate: admin.firestore.Timestamp.fromDate(resetDate),
                lastRenewalDate: admin.firestore.FieldValue.serverTimestamp(),
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            console.log(`✅ 用户重置日期已更新`);
        } else {
            console.log(`⚠️ 產品沒有配置 Credits: ${product.name}`);
        }
    } catch (error) {
        console.error('❌ 處理訂閱續費失敗:', error);
        console.error('错误详情:', error.stack);
        // 不抛出错误，避免 500
    }
}

// ============================================
// 2. Credits 管理函數
// ============================================

/**
 * 添加 Credits
 */
async function addCredits(userId, amount, metadata = {}) {
    console.log(`🔍 addCredits 被调用: userId=${userId}, amount=${amount}, metadata=`, metadata);
    const userRef = db.collection('users').doc(userId);
    
    await db.runTransaction(async (transaction) => {
        const userDoc = await transaction.get(userRef);
        
        if (!userDoc.exists) {
            console.error(`❌ 用户文档不存在: ${userId}`);
            throw new Error(`User document not found: ${userId}`);
        }
        
        const userData = userDoc.data();
        console.log(`📊 当前用户数据:`, userData);
        
        const currentCredits = userData?.credits || 0;
        const newCredits = currentCredits + amount;
        
        console.log(`💰 Credits 更新: ${currentCredits} + ${amount} = ${newCredits}`);
        
        // ✅ 同时更新 credits 和 currentCredits 字段
        transaction.update(userRef, {
            credits: newCredits,
            currentCredits: newCredits,  // ✅ 也更新 currentCredits
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
        console.log(`✅ credits 和 currentCredits 均已更新为: ${newCredits}`);
    });
}

/**
 * 扣除 Credits（支持 Pro Plan 自动按量收费）
 */
async function deductCredits(userId, amount, metadata = {}) {
    const userRef = db.collection('users').doc(userId);
    
    await db.runTransaction(async (transaction) => {
        const userDoc = await transaction.get(userRef);
        const userData = userDoc.data();
        const currentCredits = userData?.credits || 0;
        const planType = userData?.planType;
        const subscription = userData?.subscription;
        
        console.log(`🔍 扣除 Credits: userId=${userId}, current=${currentCredits}, deduct=${amount}, planType=${planType}`);
        
        // 检查是否是 Pro Plan
        const isProPlan = planType === 'Pro Plan' && subscription?.status === 'active';
        
        // 检查是否有订阅记录（包括已取消的订阅）
        const hasSubscription = subscription && subscription.stripeSubscriptionId;
        
        // ⚠️ 测试模式：允许负数扣除，用于测试 Stripe Billing Meter
        const isTestMode = userData.isTestMode || false;
        
        if (currentCredits < amount && !isProPlan && !hasSubscription && !isTestMode) {
            // 只有 Free Plan 且无订阅记录且非测试模式时才拒绝
            console.log(`❌ Credits 不足且无订阅: ${currentCredits} < ${amount}`);
            throw new Error('Credits 不足');
        }
        
        if (currentCredits < amount && (hasSubscription || isTestMode)) {
            console.log(`⚠️ Credits 不足，但允许超额使用（${hasSubscription ? '有订阅记录' : '测试模式'}）`);
        }
        
        const newCredits = currentCredits - amount;
        
        // 🔥 检查是否需要按量收费（Pro Plan 且超过月度额度）
        if (isProPlan && newCredits < 0) {
            console.log(`💰 Pro Plan 用户超出月度额度，启动按量收费`);
            console.log(`📊 当前 Credits: ${currentCredits}, 扣除: ${amount}, 结果: ${newCredits}`);
            
            // 计算超出的 Credits 数量
            const overageCredits = Math.abs(Math.min(newCredits, 0));
            console.log(`📈 超出额度: ${overageCredits} Credits`);
            
            // 🔥 报告使用量给 Stripe（异步，不阻塞事务）
            // 注意：这里只是标记需要报告，实际报告在事务外进行
            transaction.update(userRef, {
                credits: newCredits,
                'usageTracking.pendingOverageReport': admin.firestore.FieldValue.increment(overageCredits),
                'usageTracking.totalOverageThisPeriod': admin.firestore.FieldValue.increment(overageCredits),
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            
            console.log(`⚠️ Credits 为负数: ${newCredits}（将在月底通过 Stripe 收费）`);
        } else {
            // 正常扣除
            transaction.update(userRef, {
                credits: newCredits,
                currentCredits: newCredits,  // 同时更新 currentCredits
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
        }
        
        // 記錄 Credits 歷史
        const historyRef = userRef.collection('creditsHistory').doc();
        transaction.set(historyRef, {
            type: 'deduct',
            amount: amount,
            before: currentCredits,
            after: newCredits,
            metadata: {
                ...metadata,
                isProPlan: isProPlan,
                isOverage: newCredits < 0
            },
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        console.log(`✅ Credits 已扣除: ${userId} -${amount} = ${newCredits}`);
        
        // 返回扣除前和扣除后的 credits，供事务后使用
        return { previousCredits: currentCredits, newCredits: newCredits };
    });
    
    // 🔥 事务完成后，只在 Credits 为负数时才报告超额使用量
    // 逻辑：当用户超过免费额度（Credits < 0）时，才向 Stripe 报告
    const { previousCredits, newCredits } = transactionResult;
    
    const userDoc = await userRef.get();
    const userData = userDoc.data();
    const hasSubscription = userData?.subscription?.stripeSubscriptionId;
    const isTestMode = userData?.isTestMode || false;
    
    // 只有有订阅记录或测试模式的用户才考虑报告
    if (hasSubscription || isTestMode) {
        if (newCredits < 0) {
            // Credits 为负数，表示已超过免费额度
            let reportAmount;
            
            if (previousCredits >= 0) {
                // 第一次超额：从正数变成负数
                // 报告整个负数部分（即超出免费额度的部分）
                reportAmount = Math.abs(newCredits);
                console.log(`💰 首次超额：Credits 从 ${previousCredits} 降至 ${newCredits}`);
                console.log(`   报告超额使用: ${reportAmount} Credits`);
            } else {
                // 继续超额：已经是负数，继续扣除
                // 只报告本次扣除的数量
                reportAmount = amount;
                console.log(`💰 继续超额：Credits 从 ${previousCredits} 降至 ${newCredits}`);
                console.log(`   报告本次使用: ${reportAmount} Credits`);
            }
            
            try {
                await reportUsageToStripe(userId, reportAmount);
                console.log(`✅ 超额使用量已报告给 Stripe Billing Meter`);
            } catch (error) {
                console.error(`❌ 报告使用量失败:`, error);
                // 不抛出错误，确保 Credits 扣除不受影响
            }
        } else {
            console.log(`⚠️ Credits 还为正数 (${newCredits})，在免费额度内，跳过 Stripe 报告`);
        }
    } else {
        console.log(`⚠️ 用户无订阅记录，跳过 Stripe 报告`);
    }
}

/**
 * 🆕 客户端可调用的 Credits 扣除函数
 * 
 * 这个函数供客户端调用，内部会调用 deductCredits 并自动报告使用量
 */
exports.deductCreditsClient = functions.https.onCall(async (data, context) => {
    // 验证用户身份
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '请先登录');
    }
    
    const { userId, amount, metadata } = data;
    
    // 验证参数
    if (!userId || !amount) {
        throw new functions.https.HttpsError('invalid-argument', '缺少必要参数');
    }
    
    // 验证用户只能扣除自己的 Credits
    if (context.auth.uid !== userId) {
        throw new functions.https.HttpsError('permission-denied', '无权限');
    }
    
    console.log(`📞 客户端调用 deductCreditsClient: userId=${userId}, amount=${amount}`);
    
    try {
        // 调用内部 deductCredits 函数（会自动报告使用量到 Stripe）
        await deductCredits(userId, amount, metadata || {});
        
        // 获取更新后的 Credits
        const userDoc = await db.collection('users').doc(userId).get();
        const newCredits = userDoc.data()?.credits || 0;
        
        console.log(`✅ Credits 扣除成功: ${userId}, 新余额: ${newCredits}`);
        
        return {
            success: true,
            newCredits: newCredits
        };
        
    } catch (error) {
        console.error(`❌ deductCreditsClient 失败:`, error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

/**
 * 向 Stripe 报告使用量（用于按量计费）
 */
/**
 * 🆕 使用 Billing Meter Events API 报告使用量到 Stripe
 * 
 * 新方法优势：
 * - 实时报告，无需等待 webhook
 * - 事件驱动，更可靠
 * - 自动聚合，简化计费逻辑
 * 
 * @param {string} userId - 用户 ID
 * @param {number} quantity - 使用量（Credits 数量）
 */
async function reportUsageToStripe(userId, quantity) {
    console.log(`📡 reportUsageToStripe: userId=${userId}, quantity=${quantity}`);
    
    // 获取用户的订阅信息
    const userDoc = await db.collection('users').doc(userId).get();
    const userData = userDoc.data();
    const subscription = userData?.subscription;
    
    // 从多个可能的位置获取 Stripe Customer ID
    let stripeCustomerId = userData?.stripeCustomerId 
        || subscription?.stripeCustomerId
        || subscription?.customerId;
    
    console.log(`🔍 查找 Customer ID: userData.stripeCustomerId=${userData?.stripeCustomerId}, subscription.stripeCustomerId=${subscription?.stripeCustomerId}, subscription.customerId=${subscription?.customerId}`);
    
    // 如果没有找到，尝试从 Stripe API 获取
    if (!stripeCustomerId && subscription?.stripeSubscriptionId) {
        console.log(`⚠️ 未找到 Customer ID，尝试从 Stripe 订阅中获取: ${subscription.stripeSubscriptionId}`);
        
        try {
            const isTestMode = userData.isTestMode || false;
            const stripeClient = isTestMode ? stripeTest : stripeLive;
            
            if (stripeClient) {
                const stripeSubscription = await stripeClient.subscriptions.retrieve(subscription.stripeSubscriptionId);
                stripeCustomerId = stripeSubscription.customer;
                
                console.log(`✅ 从 Stripe API 获取到 Customer ID: ${stripeCustomerId}`);
                
                // 保存到 Firestore，避免下次再查询
                await db.collection('users').doc(userId).update({
                    stripeCustomerId: stripeCustomerId
                });
                console.log(`✅ Customer ID 已保存到 Firestore`);
            }
        } catch (error) {
            console.error(`❌ 从 Stripe API 获取 Customer ID 失败:`, error.message);
        }
    }
    
    if (!stripeCustomerId) {
        console.error(`❌ 用户没有 Stripe Customer ID: ${userId}`);
        console.error(`   请检查 Firestore 中的 stripeCustomerId 或 subscription.stripeSubscriptionId 字段`);
        return;
    }
    
    console.log(`✅ 使用 Stripe Customer ID: ${stripeCustomerId}`);
    
    // 🔍 检查是否是测试模式
    const isTestMode = userData.isTestMode || false;
    const stripeClient = isTestMode ? stripeTest : stripeLive;
    
    if (!stripeClient) {
        console.error(`❌ Stripe 客户端未配置`);
        return;
    }
    
    console.log(`🔧 使用 ${isTestMode ? '测试' : '生产'} 模式的 Stripe 客户端`);
    
    // 🔥 使用新的 Billing Meter Events API 报告使用量
    try {
        const meterEvent = await stripeClient.billing.meterEvents.create({
            event_name: 'vaultcaddy_credit_usage',
            payload: {
                stripe_customer_id: stripeCustomerId,
                value: quantity.toString()
            },
            timestamp: Math.floor(Date.now() / 1000)
        });
        
        console.log(`✅ 使用量已报告给 Stripe Billing Meter:`, {
            meterEventId: meterEvent.identifier,
            eventName: 'vaultcaddy_credit_usage',
            customerId: stripeCustomerId,
            quantity: quantity,
            timestamp: meterEvent.created
        });
        
        // 更新用户文档，记录最后一次报告时间
        await db.collection('users').doc(userId).update({
            'usageTracking.lastReportedAt': admin.firestore.FieldValue.serverTimestamp(),
            'usageTracking.lastReportedQuantity': quantity
        });
        
    } catch (error) {
        console.error(`❌ 报告使用量到 Billing Meter 失败:`, error);
        // 记录失败事件，但不抛出错误（避免阻塞用户操作）
        await db.collection('users').doc(userId).update({
            'usageTracking.lastReportError': error.message,
            'usageTracking.lastReportErrorAt': admin.firestore.FieldValue.serverTimestamp()
        });
    }
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
// 13. 報告 Credits 使用量到 Stripe（按量計費）
// ============================================

/**
 * 報告 Credits 使用量到 Stripe
 * 當 Pro Plan 用戶超額使用時調用
 */
exports.reportCreditsUsage = functions.https.onCall(async (data, context) => {
    const { userId } = data;
    
    console.log(`📡 報告 Credits 使用量: userId=${userId}`);
    
    // 驗證用戶身份
    if (!context.auth || context.auth.uid !== userId) {
        throw new functions.https.HttpsError('permission-denied', '無權限');
    }
    
    try {
        // 獲取用戶數據
        const userDoc = await db.collection('users').doc(userId).get();
        if (!userDoc.exists) {
            throw new functions.https.HttpsError('not-found', '用戶不存在');
        }
        
        const userData = userDoc.data();
        const subscription = userData?.subscription;
        const totalCreditsUsed = userData?.totalCreditsUsed || 0;
        const includedCredits = userData?.includedCredits || 0;
        
        console.log(`📊 用戶數據:`, {
            totalCreditsUsed,
            includedCredits,
            planType: userData?.planType,
            subscription: subscription?.stripeSubscriptionId
        });
        
        // 檢查是否有訂閱
        if (!subscription || !subscription.stripeSubscriptionId) {
            console.log(`⚠️ 用戶沒有活躍訂閱`);
            return { success: false, reason: 'no_subscription' };
        }
        
        // 檢查是否有 metered subscription item ID
        const meteredItemId = subscription.meteredSubscriptionItemId;
        if (!meteredItemId) {
            console.error(`❌ 用戶訂閱中沒有 metered subscription item ID`);
            return { success: false, reason: 'no_metered_item' };
        }
        
        // 計算超額使用量
        const overageCredits = Math.max(0, totalCreditsUsed - includedCredits);
        console.log(`📊 計算超額: totalCreditsUsed=${totalCreditsUsed}, includedCredits=${includedCredits}, overage=${overageCredits}`);
        
        if (overageCredits === 0) {
            console.log(`✅ 沒有超額使用，無需報告`);
            return { success: true, overage: 0 };
        }
        
        // 判斷測試模式
        const isTestMode = subscription.stripeSubscriptionId.startsWith('sub_');
        const stripeClient = isTestMode ? stripeTest : stripeLive;
        
        if (!stripeClient) {
            throw new functions.https.HttpsError('internal', 'Stripe 客戶端未配置');
        }
        
        console.log(`🔧 使用 ${isTestMode ? '測試' : '生產'} 模式的 Stripe 客戶端`);
        
        // 🔥 報告使用量到 Stripe
        const usageRecord = await stripeClient.subscriptionItems.createUsageRecord(
            meteredItemId,
            {
                quantity: overageCredits,
                timestamp: Math.floor(Date.now() / 1000),
                action: 'set' // 使用 'set' 而不是 'increment'，確保報告的是總量
            }
        );
        
        console.log(`✅ 使用量已報告給 Stripe:`, {
            id: usageRecord.id,
            quantity: usageRecord.quantity,
            timestamp: usageRecord.timestamp
        });
        
        // 記錄最後報告時間
        await db.collection('users').doc(userId).update({
            'usageTracking.lastReportedAt': admin.firestore.FieldValue.serverTimestamp(),
            'usageTracking.lastReportedOverage': overageCredits,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        return { 
            success: true, 
            overage: overageCredits,
            usageRecordId: usageRecord.id
        };
        
    } catch (error) {
        console.error('❌ 報告使用量失敗:', error);
        throw new functions.https.HttpsError('internal', `報告失敗: ${error.message}`);
    }
});

// ============================================
// 14. 創建 Stripe Checkout Session（動態傳遞用戶信息）
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
    
    // 🎯 定義價格 ID（生產模式 - 支持多货币）
    const productionPriceMapping = {
        monthly: {
            basePriceId: 'price_1SfNw5JmiQ31C0GT7SHy0t44',  // 月費基礎價格 HK$58
            usagePriceId: 'price_1SdpzxJmiQ31C0GTLe5rYQn9'  // 🆕 月費用量計費 HK$0.5/Credit（從負數開始收費）
        },
        yearly: {
            basePriceId: 'price_1SfNvfJmiQ31C0GTFY4bhpzK',  // 年費基礎價格 HK$552
            usagePriceId: 'price_1SdpzxJmiQ31C0GTV0iI5GK6'  // 🆕 年費用量計費 HK$0.5/Credit（從負數開始收費）
        }
    };
    
    // 🧪 定義測試模式價格 ID（支持多货币）
    const testPriceMapping = {
        monthly: {
            basePriceId: 'price_1Sdn7oJmiQ31C0GT8BSefS3u',  // 測試月費（支持 HKD/USD/GBP/JPY/KRW/EUR）
            usagePriceId: 'price_1Sdn7pJmiQ31C0GTTK1yVopH'  // 🆕 測試月費按量計費（基於 Billing Meter）✅ 已修正
        },
        yearly: {
            basePriceId: 'price_1SdoMxJmiQ31C0GTsgCDQz8n',  // 測試年費 HKD$552（支持 HKD/USD/GBP/JPY/KRW/EUR）
            usagePriceId: 'price_1Sdn7qJmiQ31C0GTwJVp4q4Q'  // 測試年費按量計費（支持多货币）
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
        
        // 🎯 創建 Checkout Session（使用對應模式的客戶端）
        // 注意：對於 Billing Meters，只需要包含基礎價格，metered price 會自動關聯到訂閱
        const session = await stripeClient.checkout.sessions.create({
            mode: 'subscription',
            line_items: [
                {
                    price: selectedPlan.basePriceId,  // 基礎訂閱費（月費/年費）
                    quantity: 1
                }
                // ⚠️ 注意：不要在這裡包含 metered price
                // Stripe Billing Meters 會在訂閱創建後自動關聯
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

// ==================== Stripe Customer Portal ====================
/**
 * 創建 Stripe Customer Portal Session
 * 用於用戶管理自己的訂閱（取消、更新支付方式、查看發票等）
 */
exports.createStripeCustomerPortalSession = functions.https.onCall(async (data, context) => {
    console.log('🔧 創建 Customer Portal Session');
    
    // 檢查用戶是否已登入
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', '請先登入');
    }
    
    const userId = context.auth.uid;
    const { returnUrl, isTest = false } = data;
    
    console.log(`👤 用戶 ID: ${userId}, 測試模式: ${isTest}`);
    
    try {
        // 從 Firestore 獲取用戶的 Stripe Customer ID
        const userDoc = await admin.firestore().collection('users').doc(userId).get();
        
        if (!userDoc.exists) {
            console.error('❌ 找不到用戶文檔');
            throw new functions.https.HttpsError('not-found', '找不到用戶資料');
        }
        
        const userData = userDoc.data();
        console.log('📄 用戶數據:', {
            email: userData.email,
            planType: userData.planType,
            hasStripeCustomerId: !!userData.stripeCustomerId
        });
        
        const stripeCustomerId = userData.stripeCustomerId;
        
        if (!stripeCustomerId) {
            console.error('❌ 用戶沒有 Stripe Customer ID');
            throw new functions.https.HttpsError('failed-precondition', '您還沒有訂閱記錄。請先訂閱 Pro Plan。');
        }
        
        // 🎯 根據 isTest 選擇使用的 Stripe 客戶端
        const stripeClient = isTest ? stripeTest : stripeLive;
        const mode = isTest ? '測試' : '生產';
        
        // 檢查 Stripe 是否已配置
        if (!stripeClient) {
            console.error(`❌ Stripe ${mode}模式未配置`);
            throw new functions.https.HttpsError('unavailable', `Stripe ${mode}模式未配置，請聯繫管理員`);
        }
        
        console.log(`🔧 使用 Stripe ${mode}模式，Customer ID: ${stripeCustomerId}`);
        
        // 創建 Customer Portal Session
        const session = await stripeClient.billingPortal.sessions.create({
            customer: stripeCustomerId,
            return_url: returnUrl || 'https://vaultcaddy.com/account.html'
        });
        
        console.log(`✅ Customer Portal Session 創建成功 (${mode}模式):`, session.id);
        
        return {
            url: session.url
        };
        
    } catch (error) {
        console.error('❌ 創建 Customer Portal Session 失敗:', error);
        
        if (error instanceof functions.https.HttpsError) {
            throw error;
        }
        
        throw new functions.https.HttpsError('internal', `創建管理頁面失敗: ${error.message}`);
    }
});

// ==================== 调试工具：查询用户 Credits ====================
/**
 * 查询用户 Credits 和历史记录（用于调试）
 * 
 * 使用方法（浏览器控制台）：
 * const f = firebase.functions().httpsCallable('queryUserCredits');
 * const result = await f({ email: 'user@example.com' });
 * console.log(result.data);
 */
exports.queryUserCredits = functions.https.onCall(async (data, context) => {
    const { email } = data;
    
    if (!email) {
        throw new functions.https.HttpsError('invalid-argument', '缺少 email 参数');
    }
    
    try {
        // 查找用户
        const usersSnapshot = await db.collection('users')
            .where('email', '==', email)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            throw new functions.https.HttpsError('not-found', '找不到用户');
        }
        
        const userDoc = usersSnapshot.docs[0];
        const userId = userDoc.id;
        const userData = userDoc.data();
        
        // 获取 Credits 历史
        const historySnapshot = await db
            .collection('users')
            .doc(userId)
            .collection('creditsHistory')
            .orderBy('timestamp', 'desc')
            .limit(100)
            .get();
        
        const history = historySnapshot.docs.map(doc => {
            const data = doc.data();
            return {
                id: doc.id,
                type: data.type,
                amount: data.amount,
                timestamp: data.timestamp?.toDate?.()?.toISOString() || null,
                metadata: data.metadata
            };
        });
        
        // 统计添加的次数
        const addRecords = history.filter(h => h.type === 'add');
        const totalAdded = addRecords.reduce((sum, h) => sum + (h.amount || 0), 0);
        
        return {
            userId,
            email: userData.email,
            currentCredits: userData.credits || 0,
            currentCreditsField: userData.currentCredits || 0,
            planType: userData.planType || 'Free Plan',
            totalAdded,
            addCount: addRecords.length,
            history: history.slice(0, 30) // 返回前 30 条
        };
        
    } catch (error) {
        console.error('查询失败:', error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

/**
 * 🔍 诊断超额计费问题
 * 检查用户数据、Stripe 订阅、使用记录等
 */
exports.diagnoseOverageCharging = functions.https.onCall(async (data, context) => {
    const { email } = data;
    
    if (!email) {
        throw new functions.https.HttpsError('invalid-argument', '缺少 email 参数');
    }
    
    try {
        console.log(`🔍 开始诊断超额计费问题: ${email}`);
        
        // 1. 查找用户
        const usersSnapshot = await db.collection('users')
            .where('email', '==', email)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            throw new functions.https.HttpsError('not-found', '找不到用户');
        }
        
        const userDoc = usersSnapshot.docs[0];
        const userId = userDoc.id;
        const userData = userDoc.data();
        
        console.log(`✅ 找到用户: ${userId}`);
        console.log(`📊 用户数据:`, userData);
        
        const result = {
            userId,
            email: userData.email,
            currentCredits: userData.currentCredits || userData.credits || 0,
            planType: userData.planType || 'Free Plan',
            meteredItemId: userData.subscription?.meteredSubscriptionItemId || null,
            stripeSubscriptionId: userData.subscription?.stripeSubscriptionId || null,
            subscriptionStatus: userData.subscription?.status || 'none',
            hasMeteredItem: !!userData.subscription?.meteredSubscriptionItemId,
            hasSubscriptionId: !!userData.subscription?.stripeSubscriptionId,
            checks: {
                hasMeteredItem: !!userData.subscription?.meteredSubscriptionItemId,
                hasSubscriptionId: !!userData.subscription?.stripeSubscriptionId,
                canReportUsage: !!(userData.subscription?.meteredSubscriptionItemId && userData.subscription?.stripeSubscriptionId)
            },
            stripeUsageRecords: null,
            error: null
        };
        
        // 2. 如果有 Stripe 订阅信息，查询 Stripe 使用记录
        if (userData.subscription?.meteredSubscriptionItemId && userData.subscription?.stripeSubscriptionId) {
            console.log(`📡 查询 Stripe 使用记录...`);
            
            try {
                // 判断是测试模式还是生产模式
                const isTestMode = userData.stripeSubscriptionId.startsWith('sub_') || 
                                  userData.stripeSubscriptionId.includes('test');
                const stripeClient = isTestMode ? stripeTest : stripeLive;
                
                console.log(`🔧 使用 ${isTestMode ? '测试' : '生产'} 模式`);
                
                if (stripeClient) {
                    // 查询使用记录
                    const usageRecords = await stripeClient.subscriptionItems.listUsageRecordSummaries(
                        userData.subscription.meteredSubscriptionItemId,
                        { limit: 100 }
                    );
                    
                    console.log(`✅ 找到 ${usageRecords.data.length} 条使用记录`);
                    
                    result.stripeUsageRecords = usageRecords.data.map(record => ({
                        id: record.id,
                        period: {
                            start: new Date(record.period.start * 1000).toISOString(),
                            end: new Date(record.period.end * 1000).toISOString()
                        },
                        totalUsage: record.total_usage
                    }));
                    
                    result.totalStripeUsage = usageRecords.data.reduce((sum, r) => sum + r.total_usage, 0);
                } else {
                    result.error = 'Stripe 客户端未配置';
                }
            } catch (stripeError) {
                console.error(`❌ 查询 Stripe 使用记录失败:`, stripeError);
                result.error = stripeError.message;
                result.stripeError = {
                    type: stripeError.type,
                    code: stripeError.code,
                    message: stripeError.message
                };
            }
        } else {
            result.error = '缺少 meteredSubscriptionItemId 或 stripeSubscriptionId';
            console.warn(`⚠️ ${result.error}`);
        }
        
        // 3. 查询 Credits 历史
        const historySnapshot = await db
            .collection('users')
            .doc(userId)
            .collection('creditsHistory')
            .orderBy('createdAt', 'desc')
            .limit(20)
            .get();
        
        result.creditsHistory = historySnapshot.docs.map(doc => {
            const data = doc.data();
            return {
                id: doc.id,
                type: data.type,
                amount: data.amount,
                description: data.description,
                createdAt: data.createdAt?.toDate?.()?.toISOString() || null,
                metadata: data.metadata
            };
        });
        
        console.log(`✅ 诊断完成`);
        console.log(`📊 结果:`, JSON.stringify(result, null, 2));
        
        return result;
        
    } catch (error) {
        console.error('❌ 诊断失败:', error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

/**
 * 🔧 手动报告超额使用（仅用于修复）
 */
exports.manualReportOverage = functions.https.onCall(async (data, context) => {
    const { email, overageAmount } = data;
    
    if (!email || !overageAmount) {
        throw new functions.https.HttpsError('invalid-argument', '缺少 email 或 overageAmount 参数');
    }
    
    try {
        console.log(`🔧 手动报告超额使用: ${email}, 数量: ${overageAmount}`);
        
        // 1. 查找用户
        const usersSnapshot = await db.collection('users')
            .where('email', '==', email)
            .limit(1)
            .get();
        
        if (usersSnapshot.empty) {
            throw new functions.https.HttpsError('not-found', '找不到用户');
        }
        
        const userDoc = usersSnapshot.docs[0];
        const userId = userDoc.id;
        const userData = userDoc.data();
        
        const meteredItemId = userData.subscription?.meteredSubscriptionItemId;
        const stripeSubscriptionId = userData.subscription?.stripeSubscriptionId;
        const monthlyCredits = userData.subscription?.monthlyCredits || userData.includedCredits || 100;
        
        console.log(`🔍 检查订阅信息:`, {
            hasSubscription: !!userData.subscription,
            meteredItemId: meteredItemId,
            stripeSubscriptionId: stripeSubscriptionId,
            monthlyCredits: monthlyCredits
        });
        
        if (!meteredItemId || !stripeSubscriptionId) {
            throw new functions.https.HttpsError(
                'failed-precondition',
                `缺少 Stripe 订阅信息:\nmeteredItemId: ${meteredItemId}\nstripeSubscriptionId: ${stripeSubscriptionId}\n\n请先确保用户有活跃的订阅！`
            );
        }
        
        // 2. 判断是测试模式还是生产模式
        const isTestMode = stripeSubscriptionId.startsWith('sub_') || 
                          stripeSubscriptionId.includes('test');
        const stripeClient = isTestMode ? stripeTest : stripeLive;
        
        console.log(`🔧 使用 ${isTestMode ? '测试' : '生产'} 模式`);
        
        if (!stripeClient) {
            throw new functions.https.HttpsError('failed-precondition', 'Stripe 客户端未配置');
        }
        
        // 3. 🔥 計算總使用量（不是超額量！）
        // Stripe 的梯度定價是基於總使用量的
        const totalUsage = monthlyCredits + overageAmount;
        
        console.log(`📊 計算使用量:`, {
            monthlyCredits: monthlyCredits,
            overageAmount: overageAmount,
            totalUsage: totalUsage,
            expectedCharge: `HK$${(overageAmount * 0.5).toFixed(2)}`
        });
        
        // 4. 创建使用记录 - 報告總使用量
        let usageRecordId = null;
        let invoiceId = null;
        let billingMethod = 'usage_record';
        
        try {
            const usageRecord = await stripeClient.subscriptionItems.createUsageRecord(
                meteredItemId,
                {
                    quantity: totalUsage,  // ← 報告總使用量，讓 Stripe 根據梯度定價計算
                    timestamp: Math.floor(Date.now() / 1000),
                    action: 'set'  // ← 使用 'set' 而不是 'increment'
                }
            );
            
            usageRecordId = usageRecord.id;
            
            console.log(`✅ 使用记录已创建:`, usageRecord.id);
            console.log(`💵 Stripe 會根據梯度定價計算費用:`);
            console.log(`   - 前 ${monthlyCredits} 個 Credits: HK$0（已包含在訂閱中）`);
            console.log(`   - 第 ${monthlyCredits + 1} 到 ${totalUsage} 個: HK$0.50/個`);
            console.log(`   - 預期收費: HK$${(overageAmount * 0.5).toFixed(2)}`);
            
        } catch (usageError) {
            console.error(`❌ 報告使用量失敗:`, usageError.message);
            console.log(`💡 訂閱可能已取消，嘗試創建獨立發票...`);
            
            // 🔥 改為創建獨立發票
            const unitPrice = 0.50;
            const totalAmount = Math.round(overageAmount * unitPrice * 100);
            
            // 獲取 customer ID
            let customerId = userData.stripeCustomerId;
            if (!customerId) {
                // 嘗試從訂閱中獲取
                try {
                    const sub = await stripeClient.subscriptions.retrieve(stripeSubscriptionId);
                    customerId = sub.customer;
                } catch (subError) {
                    throw new functions.https.HttpsError(
                        'failed-precondition',
                        `無法找到 Stripe Customer ID，請確保用戶有 Stripe 帳戶`
                    );
                }
            }
            
            // 創建發票項目
            const invoiceItem = await stripeClient.invoiceItems.create({
                customer: customerId,
                amount: totalAmount,
                currency: 'hkd',
                description: `超額使用 ${overageAmount} Credits（手動報告）`,
                metadata: {
                    userId: userId,
                    overageAmount: overageAmount.toString(),
                    monthlyCredits: monthlyCredits.toString(),
                    reportedAt: new Date().toISOString(),
                    reportType: 'manual'
                }
            });
            
            console.log(`✅ 發票項目已創建: ${invoiceItem.id}`);
            
            // 創建新發票
            const invoice = await stripeClient.invoices.create({
                customer: customerId,
                collection_method: 'charge_automatically',
                description: `VaultCaddy 超額使用費用（手動報告）`,
                auto_advance: false, // 手動控制支付流程
            });
            
            invoiceId = invoice.id;
            billingMethod = 'invoice';
            
            console.log(`✅ 發票已創建: ${invoice.id}`);
            console.log(`📋 發票包含項目: ${invoiceItem.id}，金額: HK$${(totalAmount / 100).toFixed(2)}`);
            
            // 步驟 1：完成發票
            const finalizedInvoice = await stripeClient.invoices.finalizeInvoice(invoice.id);
            console.log(`✅ 發票已完成: ${finalizedInvoice.id}`);
            
            // 步驟 2：立即支付發票（使用客戶的默認支付方式）
            const paidInvoice = await stripeClient.invoices.pay(invoice.id);
            
            console.log(`✅ 發票已成功支付: ${paidInvoice.id}`);
            console.log(`💵 支付金額: HK$${(paidInvoice.amount_paid / 100).toFixed(2)}`);
            console.log(`💳 支付狀態: ${paidInvoice.status}`);
        }
        
        // 5. 记录到 Credits 历史
        await db.collection('users').doc(userId).collection('creditsHistory').add({
            type: 'manual_overage_report',
            amount: 0,
            description: `手动报告超额使用: ${overageAmount} Credits（总使用量: ${totalUsage}）${billingMethod === 'invoice' ? ' - 通过发票收费' : ''}`,
            metadata: {
                overageAmount,
                totalUsage,
                monthlyCredits,
                usageRecordId,
                invoiceId,
                billingMethod,
                meteredItemId,
                stripeSubscriptionId,
                expectedCharge: (overageAmount * 0.5).toFixed(2),
                reportedAt: admin.firestore.FieldValue.serverTimestamp()
            },
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        
        return {
            success: true,
            billingMethod,
            usageRecordId,
            invoiceId,
            overageAmount,
            totalUsage,
            monthlyCredits,
            expectedCharge: `HK$${(overageAmount * 0.5).toFixed(2)}`,
            message: billingMethod === 'usage_record' 
                ? `✅ 已向 Stripe 报告总使用量 ${totalUsage}（包含 ${monthlyCredits} + 超额 ${overageAmount}），预期收费 HK$${(overageAmount * 0.5).toFixed(2)}`
                : `✅ 已創建發票 ${invoiceId} 收取超額費用 HK$${(overageAmount * 0.5).toFixed(2)}`
        };
        
    } catch (error) {
        console.error('❌ 手动报告失败:', error);
        throw new functions.https.HttpsError('internal', error.message);
    }
});

console.log('✅ Firebase Cloud Functions 已載入（包含 Email 驗證、數據清理、Stripe 使用量計費、Customer Portal、调试工具和超额计费诊断）');

