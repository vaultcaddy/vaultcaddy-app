/**
 * Stripe 充值功能集成
 * 
 * 功能：
 * 1. 管理 Stripe Checkout 流程
 * 2. 處理支付成功回調
 * 3. 更新用戶 Credits
 */

window.StripeManager = {
    // Stripe 產品配置
    products: {
        // 一次性購買 Credits（使用 Stripe Payment Links）
        credits: {
            50: {
                price: 15,
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_50_CREDITS'
            },
            100: {
                price: 29,
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_100_CREDITS'
            },
            200: {
                price: 56,
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_200_CREDITS'
            },
            500: {
                price: 138,
                paymentLink: 'https://buy.stripe.com/aFa3cwga8alc1CSeIOf7i03' // 用戶提供的示例鏈接
            }
        },
        
        // ✅ 訂閱計劃（2026-04-04 更新 - 專注 VaultCaddyCloud API Gateway）
        subscriptions: {
            // 月費方案：無限 Credits
            monthly: {
                productId: 'prod_UFBOv0VPfnG0qz',  // VaultCaddy Monthly
                credits: 99999, // 代表無限
                monthly_credits: 99999,
                period: 'monthly',
                overage: 0,
                
                // 價格配置
                prices: {
                    usd: {
                        priceId: 'price_REPLACE_WITH_YOUR_MONTHLY_PRICE_ID', // TODO: 替換為實際 Stripe Price ID
                        amount: 19,  // USD $19/月
                        currency: 'USD',
                        symbol: '$'
                    }
                },
                paymentLink: 'https://buy.stripe.com/dRmeVecXW9h8a9o0RYf7i0c' // 💰 真實 Stripe Payment Link (月費)
            },
            // 年費方案：無限 Credits
            yearly: {
                productId: 'prod_UFlaAAvEfrp7eM',  // VaultCaddy Yearly
                credits: 99999,
                monthly_credits: 99999,
                period: 'yearly',
                overage: 0,
                
                // 價格配置
                prices: {
                    usd: {
                        priceId: 'price_REPLACE_WITH_YOUR_YEARLY_PRICE_ID', // TODO: 替換為實際 Stripe Price ID
                        amount: 190,  // USD $190/年
                        monthlyEquivalent: 15.83,
                        currency: 'USD',
                        symbol: '$'
                    }
                },
                paymentLink: 'https://buy.stripe.com/8x26oIga87902GWbwCf7i0d' // 💰 真實 Stripe Payment Link (年費)
            },
            
            // 舊方案（保留兼容性）
            basicMonthly: {
                price: 22,
                credits: 200,
                period: 'monthly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_BASIC_MONTHLY'
            },
            basicYearly: {
                price: 216,
                credits: 2400,
                period: 'yearly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_BASIC_YEARLY'
            },
            proMonthly: {
                price: 38,
                credits: 500,
                period: 'monthly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_PRO_MONTHLY'
            },
            proYearly: {
                price: 360,
                credits: 6000,
                period: 'yearly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_PRO_YEARLY'
            },
            businessMonthly: {
                price: 78,
                credits: 1200,
                period: 'monthly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_BUSINESS_MONTHLY'
            },
            businessYearly: {
                price: 744,
                credits: 14400,
                period: 'yearly',
                paymentLink: 'https://buy.stripe.com/YOUR_LINK_BUSINESS_YEARLY'
            }
        }
    },
    
    /**
     * 根據當前頁面語言獲取幣種
     * @returns {string} 幣種代碼 (hkd, usd, jpy, krw)
     */
    getCurrencyFromLanguage() {
        const pathname = window.location.pathname;
        
        // 檢測語言版本目錄
        if (pathname.includes('/en/')) {
            return 'usd';
        } else if (pathname.includes('/jp/')) {
            return 'jpy';
        } else if (pathname.includes('/kr/')) {
            return 'krw';
        } else {
            // 默認中文版使用 HKD
            return 'hkd';
        }
    },
    
    /**
     * 獲取指定計劃的價格信息
     * @param {string} planKey - 計劃鍵值 ('monthly' 或 'yearly')
     * @param {string} currency - 幣種 (可選，不提供則自動檢測)
     * @returns {object} 價格信息
     */
    getPriceInfo(planKey, currency = null) {
        const plan = this.products.subscriptions[planKey];
        
        if (!plan) {
            console.error('無效的計劃鍵值:', planKey);
            return null;
        }
        
        // 如果沒有提供幣種，自動檢測
        if (!currency) {
            currency = this.getCurrencyFromLanguage();
        }
        
        const priceInfo = plan.prices[currency];
        
        if (!priceInfo) {
            console.error(`計劃 ${planKey} 沒有幣種 ${currency} 的價格`);
            return null;
        }
        
        return {
            ...priceInfo,
            planKey: planKey,
            credits: plan.credits,
            monthly_credits: plan.monthly_credits,
            period: plan.period,
            overage: plan.overage
        };
    },
    
    /**
     * 購買 Credits
     * @param {number} credits - Credits 數量
     */
    purchaseCredits(credits) {
        const product = this.products.credits[credits];
        
        if (!product) {
            alert(`無效的 Credits 數量: ${credits}`);
            console.error('無效的 Credits 數量:', credits);
            return;
        }
        
        console.log(`購買 ${credits} Credits，價格 $${product.price}`);
        
        // 確認購買
        if (!confirm(`確認購買 ${credits} Credits，價格 $${product.price} USD？`)) {
            return;
        }
        
        // 保存購買信息到 localStorage（用於支付成功後處理）
        const purchaseData = {
            type: 'credits',
            credits: credits,
            price: product.price,
            timestamp: new Date().toISOString(),
            userId: window.simpleAuth?.currentUser?.uid || 'guest'
        };
        
        localStorage.setItem('pendingPurchase', JSON.stringify(purchaseData));
        
        // 獲取當前用戶的 Email (如果已登入)
        const userEmail = window.simpleAuth?.currentUser?.email || '';
        
        // 構建帶有 prefilled_email 的 Stripe 連結
        let finalPaymentLink = product.paymentLink;
        if (userEmail) {
            // 檢查連結是否已經有參數
            const separator = finalPaymentLink.includes('?') ? '&' : '?';
            finalPaymentLink = `${finalPaymentLink}${separator}prefilled_email=${encodeURIComponent(userEmail)}`;
        }
        
        // 跳轉到 Stripe Payment Link
        window.location.href = finalPaymentLink;
    },
    
    /**
     * 訂閱計劃
     * @param {string} planKey - 計劃鍵值（如 'basicMonthly'）
     */
    subscribeToPlan(planKey) {
        const plan = this.products.subscriptions[planKey];
        
        if (!plan) {
            alert(`無效的訂閱計劃: ${planKey}`);
            console.error('無效的訂閱計劃:', planKey);
            return;
        }
        
        const priceInfo = plan.prices.usd;
        console.log(`訂閱 ${planKey} 計劃，價格 ${priceInfo.symbol}${priceInfo.amount}`);
        
        // 確認訂閱
        const periodText = plan.period === 'yearly' ? '年' : '月';
        if (!confirm(`確認訂閱，每${periodText} ${priceInfo.symbol}${priceInfo.amount}？\n您將獲得無限量單據處理額度。`)) {
            return;
        }
        
        // 檢查是否配置了真實的 Payment Link
        if (!plan.paymentLink || plan.paymentLink.includes('REPLACE_WITH_YOUR')) {
            alert('系統正在設置中，請稍後再試。');
            console.error('⚠️ 尚未配置 Stripe Payment Link。請在 Stripe Dashboard 創建 Payment Link 並更新到 stripe-manager.js 中。');
            return;
        }
        
        // 保存訂閱信息到 localStorage
        const subscriptionData = {
            type: 'subscription',
            planKey: planKey,
            credits: plan.credits,
            price: priceInfo.amount,
            currency: priceInfo.currency,
            period: plan.period,
            timestamp: new Date().toISOString(),
            userId: window.simpleAuth?.currentUser?.uid || 'guest'
        };
        
        localStorage.setItem('pendingSubscription', JSON.stringify(subscriptionData));
        
        // 獲取當前用戶的 Email (如果已登入)
        const userEmail = window.simpleAuth?.currentUser?.email || '';
        
        // 構建帶有 prefilled_email 的 Stripe 連結
        let finalPaymentLink = plan.paymentLink;
        if (userEmail) {
            // 檢查連結是否已經有參數
            const separator = finalPaymentLink.includes('?') ? '&' : '?';
            finalPaymentLink = `${finalPaymentLink}${separator}prefilled_email=${encodeURIComponent(userEmail)}`;
        }
        
        // 跳轉到 Stripe Payment Link
        window.location.href = finalPaymentLink;
    },
    
    /**
     * 處理支付成功回調
     * 這個函數應該在頁面載入時調用
     */
    async handlePaymentSuccess() {
        // 檢查是否有待處理的購買
        const pendingPurchase = localStorage.getItem('pendingPurchase');
        const pendingSubscription = localStorage.getItem('pendingSubscription');
        
        // 檢查 URL 是否包含 success 參數（Stripe 回調）
        const urlParams = new URLSearchParams(window.location.search);
        const isSuccess = urlParams.get('success') === 'true' || 
                         urlParams.get('payment') === 'success' ||
                         urlParams.get('session_id'); // Stripe Checkout 會返回 session_id
        
        if (!isSuccess) {
            return; // 不是支付成功回調
        }
        
        console.log('檢測到支付成功回調');
        
        try {
            // 處理一次性購買
            if (pendingPurchase) {
                const purchase = JSON.parse(pendingPurchase);
                console.log('處理待處理的購買:', purchase);
                
                await this.grantCredits(purchase.credits, {
                    source: 'purchase',
                    price: purchase.price,
                    timestamp: purchase.timestamp
                });
                
                localStorage.removeItem('pendingPurchase');
                
                if (window.VaultCaddyNavbar) {
                    window.VaultCaddyNavbar.showNotification(
                        `成功購買 ${purchase.credits} Credits！`, 
                        'success'
                    );
                }
            }
            
            // 處理訂閱
            if (pendingSubscription) {
                const subscription = JSON.parse(pendingSubscription);
                console.log('處理待處理的訂閱:', subscription);
                
                await this.grantCredits(subscription.credits, {
                    source: 'subscription',
                    planKey: subscription.planKey,
                    period: subscription.period,
                    price: subscription.price,
                    timestamp: subscription.timestamp
                });
                
                // 更新用戶訂閱狀態
                const planType = subscription.planKey.includes('basic') ? 'Basic' : 
                               subscription.planKey.includes('pro') ? 'Pro' : 'Business';
                
                localStorage.setItem('userPlan', planType);
                localStorage.setItem('userPlanPeriod', subscription.period);
                
                localStorage.removeItem('pendingSubscription');
                
                if (window.VaultCaddyNavbar) {
                    window.VaultCaddyNavbar.showNotification(
                        `成功訂閱 ${planType} 計劃！已獲得 ${subscription.credits} Credits`, 
                        'success'
                    );
                }
            }
            
            // 清理 URL 參數
            if (window.history && window.history.replaceState) {
                const cleanUrl = window.location.pathname;
                window.history.replaceState({}, document.title, cleanUrl);
            }
            
            // 刷新頁面以更新 UI
            setTimeout(() => {
                window.location.reload();
            }, 1500);
            
        } catch (error) {
            console.error('處理支付回調失敗:', error);
            if (window.VaultCaddyNavbar) {
                window.VaultCaddyNavbar.showNotification(
                    '處理支付失敗，請聯繫客服', 
                    'error'
                );
            }
        }
    },
    
    /**
     * 追蹤使用量計費
     * @param {number} pagesUsed - 使用的頁數
     * @param {string} subscriptionId - Stripe 訂閱 ID
     */
    async trackUsageMetered(pagesUsed, subscriptionId) {
        try {
            // 呼叫後端 Cloud Function 報告使用量給 Stripe
            const reportUsage = firebase.functions().httpsCallable('reportStripeUsage');
            
            const result = await reportUsage({
                subscriptionId: subscriptionId,
                quantity: pagesUsed,  // 超出免費額度的頁數
                timestamp: Date.now()
            });
            
            console.log('✅ 使用量已報告給 Stripe:', result.data);
            return result.data;
            
        } catch (error) {
            console.error('❌ 報告使用量失敗:', error);
            throw error;
        }
    },
    
    /**
     * 計算當月超出的頁數
     * @param {number} totalPagesUsed - 當月總使用頁數
     * @param {number} includedCredits - 包含的免費頁數
     * @returns {number} 超出的頁數
     */
    calculateOverage(totalPagesUsed, includedCredits) {
        const overage = Math.max(0, totalPagesUsed - includedCredits);
        console.log(`📊 使用量計算: 總使用 ${totalPagesUsed} 頁，包含 ${includedCredits} 頁，超出 ${overage} 頁`);
        return overage;
    },
    
    /**
     * 授予 Credits
     * @param {number} amount - Credits 數量
     * @param {object} metadata - 元數據
     */
    async grantCredits(amount, metadata = {}) {
        try {
            if (!window.simpleAuth || !window.simpleAuth.currentUser) {
                throw new Error('用戶未登入');
            }
            
            const userId = window.simpleAuth.currentUser.uid;
            const userRef = firebase.firestore().collection('users').doc(userId);
            
            // 使用事務來確保數據一致性
            await firebase.firestore().runTransaction(async (transaction) => {
                const userDoc = await transaction.get(userRef);
                
                let currentCredits = 0;
                if (userDoc.exists) {
                    currentCredits = userDoc.data().credits || 0;
                }
                
                const newCredits = currentCredits + amount;
                
                // 更新 Credits
                transaction.set(userRef, {
                    credits: newCredits,
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                }, { merge: true });
                
                // 添加歷史記錄
                const historyRef = userRef.collection('creditsHistory').doc();
                transaction.set(historyRef, {
                    type: 'add',
                    amount: amount,
                    before: currentCredits,
                    after: newCredits,
                    metadata: metadata,
                    createdAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                
                console.log(`✅ Credits 已授予: ${userId} +${amount} = ${newCredits}`);
                
                // 更新 navbar 的 Credits 顯示
                if (window.creditsManager) {
                    window.creditsManager.updateCreditsDisplay(newCredits);
                }
            });
            
        } catch (error) {
            console.error('授予 Credits 失敗:', error);
            throw error;
        }
    }
};

// 頁面載入時自動處理支付回調
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        window.StripeManager.handlePaymentSuccess();
    });
} else {
    window.StripeManager.handlePaymentSuccess();
}

console.log('✅ Stripe Manager 已載入');

