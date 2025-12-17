/**
 * Credits 管理模塊
 * 
 * 功能：
 * 1. 從 Firebase 實時同步 Credits
 * 2. 上傳前檢查 Credits 是否足夠
 * 3. Credits 不足時彈出提示並跳轉到 billing 頁面
 * 4. 扣除 Credits（每頁消耗 1 個 Credit）
 */

(function() {
    'use strict';
    
    // ============================================
    // 全局變量
    // ============================================
    
    window.creditsManager = {
        currentCredits: 0,
        isLoaded: false,
        listeners: []
    };
    
    // ============================================
    // Credits 同步功能
    // ============================================
    
    /**
     * 從 Firebase 加載用戶 Credits
     */
    async function loadUserCredits() {
        try {
            if (!window.simpleAuth || !window.simpleAuth.isLoggedIn()) {
                console.log('⚠️ 用戶未登入，無法加載 Credits');
                return 0;
            }
            
            const user = window.simpleAuth.getCurrentUser();
            if (!user || !user.uid) {
                console.log('⚠️ 無法獲取用戶信息');
                return 0;
            }
            
            // 從 Firestore 獲取用戶數據
            const db = firebase.firestore();
            const userDoc = await db.collection('users').doc(user.uid).get();
            
            if (userDoc.exists) {
                const userData = userDoc.data();
                // 支持兩種欄位名稱：currentCredits 優先，然後是 credits
                const credits = userData.currentCredits || userData.credits || 0;
                const planType = userData.planType || 'Free Plan'; // 獲取用戶計劃類型
                
                window.creditsManager.currentCredits = credits;
                window.creditsManager.planType = planType; // 保存計劃類型
                window.creditsManager.isLoaded = true;
                
                console.log(`📋 用戶計劃: ${planType}, Credits: ${credits}`);
                
                // 更新所有顯示 Credits 的地方
                updateCreditsDisplay(credits);
                
                // 通知所有監聽器
                notifyCreditsListeners(credits);
                
                console.log('✅ Credits 已加載:', credits);
                return credits;
            } else {
                console.log('⚠️ 用戶文檔不存在，初始化 Credits 為 0');
                
                // 創建用戶文檔
                await db.collection('users').doc(user.uid).set({
                    email: user.email,
                    credits: 10, // 新用戶贈送 10 個 Credits
                    createdAt: new Date().toISOString()
                }, { merge: true });
                
                window.creditsManager.currentCredits = 10;
                window.creditsManager.isLoaded = true;
                updateCreditsDisplay(10);
                notifyCreditsListeners(10);
                
                return 10;
            }
        } catch (error) {
            console.error('❌ 加載 Credits 失敗:', error);
            return 0;
        }
    }
    
    /**
     * 更新頁面上所有顯示 Credits 的元素
     */
    function updateCreditsDisplay(credits) {
        // 更新導航欄中的 Credits
        const creditsElements = document.querySelectorAll('#user-credits');
        creditsElements.forEach(el => {
            el.textContent = credits;
        });
        
        console.log('🔄 Credits 顯示已更新:', credits);
    }
    
    /**
     * 通知所有 Credits 監聽器
     */
    function notifyCreditsListeners(credits) {
        window.creditsManager.listeners.forEach(callback => {
            try {
                callback(credits);
            } catch (error) {
                console.error('❌ Credits 監聽器執行失敗:', error);
            }
        });
    }
    
    /**
     * 添加 Credits 變化監聽器
     */
    window.creditsManager.addListener = function(callback) {
        if (typeof callback === 'function') {
            window.creditsManager.listeners.push(callback);
        }
    };
    
    /**
     * 實時監聽 Credits 變化
     */
    function setupCreditsListener() {
        if (!window.simpleAuth || !window.simpleAuth.isLoggedIn()) {
            return;
        }
        
        const user = window.simpleAuth.getCurrentUser();
        if (!user || !user.uid) {
            return;
        }
        
        const db = firebase.firestore();
        
        // 監聽用戶文檔的變化
        db.collection('users').doc(user.uid).onSnapshot((doc) => {
            if (doc.exists) {
                const userData = doc.data();
                // 支持兩種欄位名稱：currentCredits 優先，然後是 credits
                const credits = userData.currentCredits || userData.credits || 0;
                
                window.creditsManager.currentCredits = credits;
                updateCreditsDisplay(credits);
                notifyCreditsListeners(credits);
                
                console.log('🔔 Credits 已更新:', credits);
            }
        }, (error) => {
            console.error('❌ Credits 監聽失敗:', error);
        });
        
        console.log('✅ Credits 實時監聽已啟動');
    }
    
    // ============================================
    // Credits 檢查功能
    // ============================================
    
    /**
     * 檢查 Credits 是否足夠
     * @param {number} requiredPages - 需要的頁數
     * @returns {boolean} - 是否足夠
     */
    window.creditsManager.checkCredits = async function(requiredPages) {
        // 確保 Credits 已加載
        if (!window.creditsManager.isLoaded) {
            console.log('⚠️ Credits 尚未加載，正在加載...');
            await loadUserCredits();
        }
        
        const currentCredits = window.creditsManager.currentCredits;
        const planType = window.creditsManager.planType || 'Free Plan';
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('💳 檢查 Credits (credits-manager.js v2.0)');
        console.log(`   需要: ${requiredPages} 頁`);
        console.log(`   當前: ${currentCredits} 個 Credits`);
        console.log(`   計劃: ${planType}`);
        console.log(`   isLoaded: ${window.creditsManager.isLoaded}`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        
        // ✅ Pro Plan 用戶可以使用負數 Credits（按量計費）
        if (planType === 'Pro Plan') {
            console.log('✅ Pro Plan 用戶，允許使用負數 Credits（按量計費）');
            console.log('✅ 跳過 Credits 檢查，允許繼續');
            return true;
        }
        
        console.log('⚠️ Free Plan 用戶，需要檢查 Credits 是否足夠');
        
        // Free Plan 用戶需要檢查 Credits 是否足夠
        if (currentCredits < requiredPages) {
            console.log('❌ Credits 不足，顯示購買對話框');
            showInsufficientCreditsDialog(requiredPages, currentCredits);
            return false;
        }
        
        console.log('✅ Credits 足夠，允許繼續');
        return true;
    };
    
    /**
     * 顯示 Credits 不足對話框
     */
    function showInsufficientCreditsDialog(required, current) {
        const shortage = required - current;
        
        const confirmed = confirm(
            `❌ Credits 不足！\n\n` +
            `需要: ${required} Credits\n` +
            `目前: ${current} Credits\n` +
            `缺少: ${shortage} Credits\n\n` +
            `點擊「確定」前往購買頁面，立即增加 Credits。`
        );
        
        if (confirmed) {
            window.location.href = 'billing.html';
        }
    }
    
    // ============================================
    // Credits 扣除功能
    // ============================================
    
    /**
     * 扣除 Credits
     * @param {number} pages - 要扣除的頁數
     * @returns {boolean} - 是否成功
     */
    window.creditsManager.deductCredits = async function(pages) {
        try {
            if (!window.simpleAuth || !window.simpleAuth.isLoggedIn()) {
                console.error('❌ 用戶未登入');
                return false;
            }
            
            const user = window.simpleAuth.getCurrentUser();
            if (!user || !user.uid) {
                console.error('❌ 無法獲取用戶信息');
                return false;
            }
            
            const db = firebase.firestore();
            const userRef = db.collection('users').doc(user.uid);
            
            // 用於儲存事務結果的變量
            let transactionResult = null;
            
            // 使用事務確保原子性
            await db.runTransaction(async (transaction) => {
                const userDoc = await transaction.get(userRef);
                
                if (!userDoc.exists) {
                    throw new Error('用戶文檔不存在');
                }
                
                const userData = userDoc.data();
                // 支持兩種欄位名稱：credits 和 currentCredits
                const currentCredits = userData.currentCredits || userData.credits || 0;
                const planType = userData.planType || 'Free Plan';
                const totalCreditsUsed = userData.totalCreditsUsed || 0; // 累計使用量
                const includedCredits = userData.includedCredits || 0; // 訂閱包含的 Credits
                
                console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
                console.log(`💰 扣除 Credits (credits-manager.js v3.0)`);
                console.log(`   當前 Credits: ${currentCredits}`);
                console.log(`   扣除頁數: ${pages}`);
                console.log(`   計劃類型: ${planType}`);
                console.log(`   累計使用: ${totalCreditsUsed}`);
                console.log(`   包含 Credits: ${includedCredits}`);
                console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
                
                // ✅ Pro Plan 用戶可以使用負數 Credits（按量計費）
                if (planType === 'Free Plan' && currentCredits < pages) {
                    console.log(`❌ Free Plan 用戶 Credits 不足`);
                    throw new Error('Credits 不足');
                }
                
                const newCredits = currentCredits - pages;
                const newTotalCreditsUsed = totalCreditsUsed + pages; // 累計使用量增加
                console.log(`   新 Credits: ${newCredits}`);
                console.log(`   新累計使用: ${newTotalCreditsUsed}`);
                
                // 同時更新兩個欄位以確保兼容性
                transaction.update(userRef, { 
                    credits: newCredits,
                    currentCredits: newCredits,
                    totalCreditsUsed: newTotalCreditsUsed, // ✅ 更新累計使用量
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                
                // 記錄使用歷史
                const historyRef = db.collection('users').doc(user.uid).collection('creditsHistory').doc();
                transaction.set(historyRef, {
                    type: 'deduction',
                    amount: -pages,
                    description: `處理文檔，使用 ${pages} Credits`,
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    balanceAfter: newCredits,
                    planType: planType
                });
                
                console.log(`✅ Credits 已扣除: ${pages} 頁，剩餘: ${newCredits}`);
                
                // 更新本地狀態
                window.creditsManager.currentCredits = newCredits;
                
                // 🔔 更新顯示
                updateCreditsDisplay(newCredits);
                notifyCreditsListeners(newCredits);
                
                // 🚀 保存事務結果，供後續使用
                transactionResult = {
                    newCredits,
                    newTotalCreditsUsed,
                    planType,
                    includedCredits
                };
            });
            
            // 📊 如果是 Pro Plan 且超額使用，報告給 Stripe
            if (transactionResult.planType === 'Pro Plan' && 
                transactionResult.newTotalCreditsUsed > transactionResult.includedCredits) {
                
                console.log(`🔔 Pro Plan 用戶超額使用`);
                console.log(`   累計使用: ${transactionResult.newTotalCreditsUsed}`);
                console.log(`   包含 Credits: ${transactionResult.includedCredits}`);
                console.log(`   超額: ${transactionResult.newTotalCreditsUsed - transactionResult.includedCredits}`);
                
                // ✅ 使用量報告已由後端 deductCredits 函數自動處理（使用 Billing Meter Events API）
                // 客戶端不再需要手動調用 reportCreditsUsage
                console.log(`ℹ️ 使用量將由後端自動報告給 Stripe（Billing Meter Events API）`)
            }
            
            return true;
        } catch (error) {
            console.error('❌ 扣除 Credits 失敗:', error);
            return false;
        }
    };
    
    /**
     * 退回 Credits（處理失敗時）
     * @param {number} pages - 要退回的頁數
     * @returns {boolean} - 是否成功
     */
    window.creditsManager.refundCredits = async function(pages) {
        try {
            if (!window.simpleAuth || !window.simpleAuth.isLoggedIn()) {
                console.error('❌ 用戶未登入');
                return false;
            }
            
            const user = window.simpleAuth.getCurrentUser();
            if (!user || !user.uid) {
                console.error('❌ 無法獲取用戶信息');
                return false;
            }
            
            const db = firebase.firestore();
            const userRef = db.collection('users').doc(user.uid);
            
            // 使用事務確保原子性
            await db.runTransaction(async (transaction) => {
                const userDoc = await transaction.get(userRef);
                
                if (!userDoc.exists) {
                    throw new Error('用戶文檔不存在');
                }
                
                const userData = userDoc.data();
                // 支持兩種欄位名稱：credits 和 currentCredits
                const currentCredits = userData.currentCredits || userData.credits || 0;
                const newCredits = currentCredits + pages;
                
                // 同時更新兩個欄位以確保兼容性
                transaction.update(userRef, { 
                    credits: newCredits,
                    currentCredits: newCredits,
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                
                // 記錄退款歷史
                const historyRef = db.collection('users').doc(user.uid).collection('creditsHistory').doc();
                transaction.set(historyRef, {
                    type: 'refund',
                    amount: pages,
                    reason: 'processing_failed',
                    description: `處理失敗，退回 ${pages} Credits`,
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    balanceAfter: newCredits
                });
                
                console.log(`✅ Credits 已退回: ${pages} 頁，新餘額: ${newCredits}`);
                
                // 更新本地狀態
                window.creditsManager.currentCredits = newCredits;
            });
            
            return true;
        } catch (error) {
            console.error('❌ 退回 Credits 失敗:', error);
            return false;
        }
    };
    
    /**
     * 獲取當前 Credits
     */
    window.creditsManager.getCurrentCredits = function() {
        return window.creditsManager.currentCredits;
    };
    
    /**
     * 刷新 Credits
     */
    window.creditsManager.refresh = async function() {
        return await loadUserCredits();
    };
    
    // ============================================
    // 初始化
    // ============================================
    
    /**
     * 初始化 Credits 管理器
     */
    function initCreditsManager() {
        console.log('🚀 初始化 Credits 管理器...');
        
        // 等待 Firebase 準備好
        if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
            loadUserCredits();
            setupCreditsListener();
        } else {
            // 監聽登入事件
            window.addEventListener('user-logged-in', () => {
                loadUserCredits();
                setupCreditsListener();
            });
        }
    }
    
    // 當 DOM 準備好時初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCreditsManager);
    } else {
        initCreditsManager();
    }
    
    // 監聽 Firebase 準備好事件
    window.addEventListener('firebase-ready', initCreditsManager);
    
    console.log('📦 Credits 管理器已載入');
})();

