/**
 * ============================================
 * 🔐 VaultCaddy 簡化認證系統
 * ============================================
 * 功能：
 * - 純 Firebase Auth（無向後兼容）
 * - 自動頁面保護
 * - 自動重定向
 * - 簡潔清晰的代碼
 * ============================================
 */

class SimpleAuth {
    constructor() {
        this.auth = null;
        this.currentUser = null;
        this.initialized = false;
        
        console.log('🔐 SimpleAuth 構造函數執行');
        // 不在構造函數中初始化，等待 firebase-ready 事件
    }
    
    // 初始化
    async init() {
        try {
            console.log('🔐 開始初始化 SimpleAuth...');
            
            // 直接使用 Firebase（已由 firebase-config.js 初始化）
            if (!firebase || !firebase.auth) {
                throw new Error('Firebase SDK 未加載');
            }
            
            this.auth = firebase.auth();
            
            console.log('⏳ 等待第一次 Auth 狀態回調...');
            
            // ✅ 只設置一次 onAuthStateChanged 監聽器
            let isFirstCall = true;
            this.auth.onAuthStateChanged((user) => {
                if (isFirstCall) {
                    console.log('🔔 Auth 初始狀態:', user ? `用戶: ${user.email}` : '未登入');
                    isFirstCall = false;
                } else {
                    console.log('🔔 Auth 狀態變化:', user ? `用戶: ${user.email}` : '未登入');
                }
                
                this.currentUser = user;
                this.handleAuthStateChange(user);
            });
            
            this.initialized = true;
            console.log('✅ SimpleAuth 已初始化');
            console.log('   - currentUser:', this.currentUser ? this.currentUser.email : 'null');
            
        } catch (error) {
            console.error('❌ SimpleAuth 初始化失敗:', error);
            console.error('   錯誤詳情:', error.message);
            console.error('   錯誤堆棧:', error.stack);
        }
    }
    
    // 等待 Firebase 就緒
    waitForFirebase() {
        return new Promise((resolve) => {
            if (window.firebaseInitialized && firebase && firebase.auth) {
                console.log('✅ Firebase 已就緒');
                resolve();
            } else {
                console.log('⏳ 等待 Firebase...');
                const checkInterval = setInterval(() => {
                    if (window.firebaseInitialized && firebase && firebase.auth) {
                        clearInterval(checkInterval);
                        console.log('✅ Firebase 已就緒');
                        resolve();
                    }
                }, 100);
                
                // 超時保護（15 秒）
                setTimeout(() => {
                    clearInterval(checkInterval);
                    console.error('❌ Firebase 初始化超時');
                    resolve(); // 仍然 resolve，避免卡住
                }, 15000);
            }
        });
    }
    
    // 處理用戶狀態變化
    handleAuthStateChange(user) {
        console.log('🔄 用戶狀態變化:', user ? user.email : '未登入');
        
        // 顯示頁面內容（移除加載動畫）
        this.showPage();
        
        if (user) {
            // 用戶已登入
            this.onUserLoggedIn(user);
        } else {
            // 用戶未登入
            this.onUserLoggedOut();
        }
        
        // 觸發自定義事件（供其他模塊使用）
        window.dispatchEvent(new CustomEvent('auth-state-changed', {
            detail: { user }
        }));
    }
    
    // 用戶已登入
    onUserLoggedIn(user) {
        // 只在非 index.html 頁面打印日誌
        const currentPage = this.getCurrentPage();
        if (currentPage !== 'index.html' && currentPage !== '') {
            console.log('✅ 用戶已登入:', user.email);
        }
        
        // 如果在登入/註冊頁面，重定向到 dashboard
        const authPages = ['auth.html', 'login.html', 'register.html'];
        
        if (authPages.includes(currentPage)) {
            console.log('🔄 重定向到 dashboard...');
            window.location.href = 'dashboard.html';
        }
        
        // 觸發自定義事件（只觸發一次）
        window.dispatchEvent(new CustomEvent('user-logged-in', {
            detail: { user }
        }));
    }
    
    // 用戶未登入
    onUserLoggedOut() {
        console.log('❌ 用戶未登入');
        
        // 檢查是否在受保護頁面
        const currentPage = this.getCurrentPage();
        const currentPath = window.location.pathname;
        
        // ✅ 改為白名單制度：只有這些頁面需要登入
        const protectedPages = [
            'dashboard.html',
            'firstproject.html',
            'document-detail.html',
            'account.html',
            'billing.html',
            'settings.html',
            'profile.html'
        ];
        
        // Blog目錄和所有landing page（v2/v3）都是公開的
        const isBlogPage = currentPath.includes('/blog/');
        const isLandingPage = currentPage.includes('-v2.html') || currentPage.includes('-v3.html');
        
        if (protectedPages.includes(currentPage)) {
            console.log('🔒 受保護頁面，重定向到 auth.html...');
            window.location.href = 'auth.html';
        } else if (isBlogPage) {
            console.log('📝 Blog 頁面，允許未登入訪問');
        } else if (isLandingPage) {
            console.log('🌐 Landing Page，允許未登入訪問');
        } else {
            console.log('🌐 公開頁面，允許未登入訪問');
        }
    }
    
    // 顯示頁面（移除加載動畫）
    showPage() {
        document.documentElement.classList.remove('auth-checking');
        document.documentElement.classList.add('auth-ready');
        document.body.classList.remove('auth-checking');
        document.body.classList.add('auth-ready');
    }
    
    // 獲取當前頁面名稱
    getCurrentPage() {
        return window.location.pathname.split('/').pop();
    }
    
    // ============================================
    // 公開 API
    // ============================================
    
    // 電子郵件登入
    async loginWithEmail(email, password) {
        try {
            console.log('🔐 正在登入...', email);
            const result = await this.auth.signInWithEmailAndPassword(email, password);
            console.log('✅ 登入成功');
            return result.user;
        } catch (error) {
            console.error('❌ 登入失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // Google 登入
    async loginWithGoogle() {
        try {
            console.log('🔐 正在使用 Google 登入...');
            const provider = new firebase.auth.GoogleAuthProvider();
            const result = await this.auth.signInWithPopup(provider);
            console.log('✅ Google 登入成功');
            
            // 🎯 檢查並創建 Firestore 用戶文檔（如果不存在）
            if (result.user) {
                const db = firebase.firestore();
                const userRef = db.collection('users').doc(result.user.uid);
                const userDoc = await userRef.get();
                
                if (!userDoc.exists) {
                    console.log('📝 首次 Google 登入，創建 Firestore 用戶文檔...');
                    const normalizedEmail = result.user.email.toLowerCase().trim();
                    
                    const userData = {
                        email: normalizedEmail,
                        displayName: result.user.displayName || '',
                        company: '',  // 🏢 Google 登入時公司名稱為空，用戶可後續填寫
                        credits: 20,  // 🎁 註冊即送 20 個 Credits
                        currentCredits: 20,  // 🎁 註冊即送 20 個 Credits
                        emailVerified: result.user.emailVerified,
                        planType: 'Free Plan',  // 📋 初始為 Free Plan
                        photoURL: result.user.photoURL || '',
                        provider: 'google',
                        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                        updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                    };
                    
                    await userRef.set(userData);
                    console.log('✅ Firestore 用戶文檔已創建（Google）');
                    console.log('   Email:', normalizedEmail);
                    console.log('   UID:', result.user.uid);
                    
                    // 🎁 添加 Credits 歷史記錄
                    try {
                        const historyRef = userRef.collection('creditsHistory').doc();
                        await historyRef.set({
                            type: 'bonus',
                            amount: 20,
                            reason: 'registration_bonus',
                            description: 'Google 註冊獎勵',
                            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                            balanceAfter: 20
                        });
                        console.log('✅ Credits 歷史記錄已添加');
                    } catch (historyError) {
                        console.error('⚠️ 添加 Credits 歷史記錄失敗:', historyError);
                        // 不拋出錯誤，因為用戶文檔已創建成功
                    }
                    
                    // 驗證文檔創建成功
                    const verifyDoc = await userRef.get();
                    if (!verifyDoc.exists || !verifyDoc.data().email) {
                        console.error('❌ Google 登入文檔創建驗證失敗');
                    } else {
                        console.log('✅ Google 登入用戶文檔驗證成功');
                        console.log('🎁 已贈送 20 個 Credits');
                    }
                } else {
                    console.log('✅ Firestore 用戶文檔已存在');
                }
            }
            
            return result.user;
        } catch (error) {
            console.error('❌ Google 登入失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // 電子郵件註冊
    async registerWithEmail(email, password, displayName = null, additionalData = {}) {
        try {
            console.log('📝 正在註冊...', email);
            
            // ✅ 統一轉換為小寫，避免大小寫匹配問題
            const normalizedEmail = email.toLowerCase().trim();
            
            const result = await this.auth.createUserWithEmailAndPassword(normalizedEmail, password);
            
            // 設置顯示名稱
            if (displayName && result.user) {
                await result.user.updateProfile({ displayName });
                console.log('✅ 用戶名稱已設置:', displayName);
            }
            
            // 🎯 創建 Firestore 用戶文檔（重要！驗證後需要這個文檔來添加 Credits）
            console.log('📝 正在創建 Firestore 用戶文檔...');
            console.log('   用戶 ID:', result.user.uid);
            console.log('   Email:', normalizedEmail);
            console.log('   額外資料:', additionalData);
            
            try {
                const db = firebase.firestore();
                const userDoc = {
                    email: normalizedEmail,  // ✅ 統一小寫
                    displayName: displayName || '',
                    company: additionalData.company || '',  // 🏢 公司名稱
                    credits: 0,  // 初始為 0，驗證後會加 20
                    currentCredits: 0,
                    emailVerified: false,
                    planType: 'Free Plan',  // 📋 初始為 Free Plan
                    photoURL: '',  // 📷 Email 註冊無頭像
                    provider: 'email',  // 🔐 註冊方式
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                };
                
                await db.collection('users').doc(result.user.uid).set(userDoc);
                console.log('✅ Firestore 用戶文檔已創建');
                console.log('   文檔內容:', { ...userDoc, createdAt: 'serverTimestamp', updatedAt: 'serverTimestamp' });
                
                // ✅ 驗證文檔是否真的創建成功
                const docSnapshot = await db.collection('users').doc(result.user.uid).get();
                if (!docSnapshot.exists) {
                    throw new Error('文檔創建後無法讀取，可能創建失敗');
                }
                const docData = docSnapshot.data();
                if (!docData.email) {
                    throw new Error('文檔創建成功但缺少 email 字段');
                }
                console.log('✅ 用戶文檔驗證成功，email 字段:', docData.email);
                
            } catch (firestoreError) {
                console.error('❌ 創建 Firestore 用戶文檔失敗:', firestoreError);
                console.error('   錯誤詳情:', firestoreError.message);
                console.error('   錯誤堆棧:', firestoreError.stack);
                
                // ⚠️ 如果 Firestore 文檔創建失敗，刪除 Auth 用戶並拋出錯誤
                console.warn('⚠️ 由於 Firestore 文檔創建失敗，將刪除 Auth 用戶');
                try {
                    await result.user.delete();
                    console.log('✅ Auth 用戶已刪除');
                } catch (deleteError) {
                    console.error('❌ 刪除 Auth 用戶失敗:', deleteError);
                }
                
                throw new Error('註冊失敗：無法創建用戶資料。請稍後再試。');
            }
            
            console.log('✅ 註冊成功');
            return result.user;
        } catch (error) {
            console.error('❌ 註冊失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // 登出
    async logout() {
        try {
            console.log('🚪 正在登出...');
            await this.auth.signOut();
            console.log('✅ 已登出');
            window.location.href = 'auth.html';
        } catch (error) {
            console.error('❌ 登出失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // 重置密碼
    async resetPassword(email) {
        try {
            console.log('📧 正在發送密碼重置郵件...', email);
            await this.auth.sendPasswordResetEmail(email);
            console.log('✅ 密碼重置郵件已發送');
        } catch (error) {
            console.error('❌ 密碼重置失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // 更新個人資料
    async updateProfile(updates) {
        try {
            if (!this.currentUser) {
                throw new Error('用戶未登入');
            }
            
            console.log('📝 正在更新個人資料...', updates);
            await this.currentUser.updateProfile(updates);
            console.log('✅ 個人資料已更新');
        } catch (error) {
            console.error('❌ 更新個人資料失敗:', error);
            throw this.formatError(error);
        }
    }
    
    // 獲取當前用戶
    getCurrentUser() {
        return this.currentUser;
    }
    
    // 檢查是否已登入
    isLoggedIn() {
        return this.currentUser !== null;
    }
    
    // 格式化錯誤信息（中文）
    formatError(error) {
        const errorMessages = {
            'auth/email-already-in-use': '此電子郵件已被使用',
            'auth/invalid-email': '電子郵件格式無效',
            'auth/operation-not-allowed': '此操作不被允許',
            'auth/weak-password': '密碼強度太弱（至少 6 個字符）',
            'auth/user-disabled': '此帳戶已被停用',
            'auth/user-not-found': '找不到此用戶',
            'auth/wrong-password': '密碼錯誤',
            'auth/too-many-requests': '請求過於頻繁，請稍後再試',
            'auth/popup-closed-by-user': '您取消了登入',
            'auth/network-request-failed': '網絡連接失敗，請檢查您的網絡'
        };
        
        const message = errorMessages[error.code] || error.message || '發生未知錯誤';
        
        return {
            code: error.code,
            message: message,
            originalError: error
        };
    }
}

// 創建全局實例
console.log('🔐 加載 SimpleAuth...');
window.simpleAuth = new SimpleAuth();

// 向後兼容（供舊代碼使用）
window.authHandler = window.simpleAuth;

// 監聽 firebase-ready 事件，自動初始化
window.addEventListener('firebase-ready', async () => {
    console.log('🔥 收到 firebase-ready 事件，初始化 SimpleAuth');
    if (!window.simpleAuth.initialized) {
        await window.simpleAuth.init();
    } else {
        console.log('ℹ️ SimpleAuth 已經初始化，跳過');
    }
});

// ✅ 後備檢查：如果 Firebase 已經就緒，立即初始化
setTimeout(async () => {
    if (window.firebaseInitialized && !window.simpleAuth.initialized) {
        console.log('🔄 Firebase 已就緒但 SimpleAuth 未初始化，立即初始化...');
        await window.simpleAuth.init();
    }
}, 100); // 100ms 後檢查

// ✅✅ 終極後備：強制初始化（3秒後）
setTimeout(async () => {
    if (!window.simpleAuth.initialized) {
        console.warn('⚠️ SimpleAuth 3秒後仍未初始化，強制初始化');
        try {
            await window.simpleAuth.init();
        } catch (error) {
            console.error('❌ 強制初始化失敗:', error);
        }
    }
}, 3000);

