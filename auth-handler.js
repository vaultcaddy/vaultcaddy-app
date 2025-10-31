// ============================================
// VaultCaddy 身份驗證處理器
// ============================================

class AuthHandler {
    constructor() {
        this.auth = null;
        this.currentUser = null;
        this.initialized = false;
        
        console.log('🔐 創建 AuthHandler...');
        
        // 等待 Firebase 初始化
        if (window.firebaseInitialized && window.getAuth) {
            console.log('✅ Firebase 已初始化，立即初始化 AuthHandler');
            this.initialize();
        } else {
            console.log('⏳ Firebase 尚未初始化，等待 firebase-ready 事件...');
            window.addEventListener('firebase-ready', () => {
                console.log('✅ 收到 firebase-ready 事件');
                this.initialize();
            });
            
            // 備用方案：輪詢檢查（防止錯過事件）
            const checkFirebase = setInterval(() => {
                if (window.firebaseInitialized && window.getAuth && !this.initialized) {
                    console.log('✅ 檢測到 Firebase 已初始化（輪詢）');
                    clearInterval(checkFirebase);
                    this.initialize();
                }
            }, 200);
            
            // 超時保護（15 秒）
            setTimeout(() => {
                clearInterval(checkFirebase);
                if (!this.initialized) {
                    console.error('❌ AuthHandler 初始化超時（15 秒）');
                    console.error('   firebaseInitialized:', window.firebaseInitialized);
                    console.error('   getAuth 存在:', !!window.getAuth);
                }
            }, 15000);
        }
    }
    
    // 初始化
    initialize() {
        try {
            this.auth = window.getAuth();
            
            // 確保 auth 不是 null 才標記為已初始化
            if (!this.auth) {
                console.error('❌ Auth Handler 初始化失敗: window.getAuth() 返回 null');
                console.log('⏳ 等待 Firebase Auth 準備好...');
                
                // 重試機制：每 500ms 檢查一次，最多 20 次（10 秒）
                let retryCount = 0;
                const retryInterval = setInterval(() => {
                    retryCount++;
                    console.log(`🔄 重試 Auth 初始化 (${retryCount}/20)...`);
                    
                    this.auth = window.getAuth();
                    if (this.auth) {
                        clearInterval(retryInterval);
                        this.finishInitialization();
                    } else if (retryCount >= 20) {
                        clearInterval(retryInterval);
                        console.error('❌ Auth Handler 初始化超時：10 秒後仍然無法獲取 Auth');
                    }
                }, 500);
                return;
            }
            
            this.finishInitialization();
        } catch (error) {
            console.error('❌ Auth Handler 初始化失敗:', error);
        }
    }
    
    // 完成初始化
    finishInitialization() {
        this.initialized = true;
        console.log('✅ Auth Handler 已成功初始化');
        console.log('   Auth 對象:', this.auth ? '✓' : '✗');
        
        // 監聽用戶狀態變化
        this.auth.onAuthStateChanged((user) => {
            this.currentUser = user;
            this.handleAuthStateChange(user);
        });
    }
    
    // 處理用戶狀態變化
    handleAuthStateChange(user) {
        // 移除 auth-checking 類，顯示頁面
        document.documentElement.classList.remove('auth-checking');
        document.documentElement.classList.add('auth-ready');
        document.body.classList.remove('auth-checking');
        document.body.classList.add('auth-ready');
        
        if (user) {
            console.log('👤 用戶已登入:', user.email);
            console.log('   UID:', user.uid);
            console.log('   名稱:', user.displayName);
            
            // 觸發自定義事件
            window.dispatchEvent(new CustomEvent('auth-state-changed', { detail: { user } }));
            
            // 重定向到 dashboard（如果在登錄/註冊頁面）
            const currentPage = window.location.pathname.split('/').pop();
            if (currentPage === 'login.html' || currentPage === 'register.html' || currentPage === 'auth.html') {
                console.log('🔄 重定向到 dashboard...');
                window.location.href = 'dashboard.html';
            }
        } else {
            console.log('👤 用戶未登入');
            
            // 觸發自定義事件
            window.dispatchEvent(new CustomEvent('auth-state-changed', { detail: { user: null } }));
            
            // 重定向到登錄頁（如果在受保護頁面）
            this.checkPageProtection();
        }
    }
    
    // 檢查頁面保護
    checkPageProtection() {
        // 公開頁面列表
        const publicPages = [
            'login.html',
            'register.html',
            'auth.html',
            'index.html',
            'privacy.html',
            'terms.html',
            'billing.html',
            ''
        ];
        
        const currentPage = window.location.pathname.split('/').pop();
        
        // 如果不是公開頁面，重定向到登錄頁
        if (!publicPages.includes(currentPage)) {
            console.log('🔒 受保護頁面，重定向到登錄頁...');
            window.location.href = 'login.html';
        } else {
            // 如果是公開頁面，移除 auth-checking 類
            document.documentElement.classList.remove('auth-checking');
            document.documentElement.classList.add('auth-ready');
            document.body.classList.remove('auth-checking');
            document.body.classList.add('auth-ready');
        }
    }
    
    // 電子郵件/密碼登錄
    async loginWithEmail(email, password) {
        try {
            console.log('🔐 正在登入...', email);
            const userCredential = await this.auth.signInWithEmailAndPassword(email, password);
            console.log('✅ 登入成功:', userCredential.user.email);
            return userCredential.user;
        } catch (error) {
            console.error('❌ 登入失敗:', error.code, error.message);
            throw error;
        }
    }
    
    // Google 登錄
    async loginWithGoogle() {
        try {
            console.log('🔐 正在使用 Google 登入...');
            const provider = new firebase.auth.GoogleAuthProvider();
            const userCredential = await this.auth.signInWithPopup(provider);
            console.log('✅ Google 登入成功:', userCredential.user.email);
            return userCredential.user;
        } catch (error) {
            console.error('❌ Google 登入失敗:', error.code, error.message);
            throw error;
        }
    }
    
    // 註冊
    async registerWithEmail(email, password, displayName = null) {
        try {
            console.log('📝 正在註冊...', email);
            const userCredential = await this.auth.createUserWithEmailAndPassword(email, password);
            
            // 如果提供了名稱，更新 displayName
            if (displayName && userCredential.user) {
                await userCredential.user.updateProfile({
                    displayName: displayName
                });
                console.log('✅ 用戶名稱已設置:', displayName);
            }
            
            console.log('✅ 註冊成功:', userCredential.user.email);
            return userCredential.user;
        } catch (error) {
            console.error('❌ 註冊失敗:', error.code, error.message);
            throw error;
        }
    }
    
    // 登出
    async logout() {
        try {
            console.log('🔐 正在登出...');
            await this.auth.signOut();
            console.log('✅ 已登出');
            window.location.href = 'login.html';
        } catch (error) {
            console.error('❌ 登出失敗:', error);
            throw error;
        }
    }
    
    // 重置密碼
    async resetPassword(email) {
        try {
            console.log('📧 正在發送密碼重置郵件...', email);
            await this.auth.sendPasswordResetEmail(email);
            console.log('✅ 密碼重置郵件已發送');
            alert('密碼重置郵件已發送到 ' + email + '\n\n請檢查您的郵箱（包括垃圾郵件文件夾）');
        } catch (error) {
            console.error('❌ 密碼重置失敗:', error.code, error.message);
            throw error;
        }
    }
    
    // 更新用戶資料
    async updateProfile(updates) {
        try {
            if (!this.currentUser) {
                throw new Error('用戶未登入');
            }
            
            console.log('📝 正在更新用戶資料...', updates);
            await this.currentUser.updateProfile(updates);
            console.log('✅ 用戶資料已更新');
        } catch (error) {
            console.error('❌ 更新用戶資料失敗:', error);
            throw error;
        }
    }
    
    // 更改密碼
    async changePassword(newPassword) {
        try {
            if (!this.currentUser) {
                throw new Error('用戶未登入');
            }
            
            console.log('🔐 正在更改密碼...');
            await this.currentUser.updatePassword(newPassword);
            console.log('✅ 密碼已更改');
            alert('密碼已成功更改');
        } catch (error) {
            console.error('❌ 更改密碼失敗:', error);
            
            // 如果需要重新認證
            if (error.code === 'auth/requires-recent-login') {
                alert('為了安全起見，請先登出再重新登入，然後再更改密碼');
            }
            
            throw error;
        }
    }
    
    // 刪除帳戶
    async deleteAccount() {
        try {
            if (!this.currentUser) {
                throw new Error('用戶未登入');
            }
            
            const confirmed = confirm('確定要刪除帳戶嗎？\n\n此操作無法撤銷，所有數據將被永久刪除。');
            if (!confirmed) {
                return;
            }
            
            console.log('🗑️ 正在刪除帳戶...');
            await this.currentUser.delete();
            console.log('✅ 帳戶已刪除');
            window.location.href = 'index.html';
        } catch (error) {
            console.error('❌ 刪除帳戶失敗:', error);
            
            // 如果需要重新認證
            if (error.code === 'auth/requires-recent-login') {
                alert('為了安全起見，請先登出再重新登入，然後再刪除帳戶');
            }
            
            throw error;
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
    
    // 獲取用戶 ID
    getUserId() {
        return this.currentUser ? this.currentUser.uid : null;
    }
    
    // 獲取用戶名稱
    getUserName() {
        if (!this.currentUser) return null;
        
        // 優先使用 displayName，否則使用 email 的前綴
        return this.currentUser.displayName || this.currentUser.email.split('@')[0];
    }
    
    // 獲取用戶郵箱
    getUserEmail() {
        return this.currentUser ? this.currentUser.email : null;
    }
    
    // 等待初始化完成
    async waitForInit() {
        // 必須確保 initialized 為 true 且 auth 不是 null
        if (this.initialized && this.auth) return true;
        
        return new Promise((resolve) => {
            const checkInit = setInterval(() => {
                if (this.initialized && this.auth) {
                    clearInterval(checkInit);
                    resolve(true);
                }
            }, 100);
            
            // 超時保護（10 秒）
            setTimeout(() => {
                clearInterval(checkInit);
                console.error('❌ waitForInit 超時:', {
                    initialized: this.initialized,
                    authExists: !!this.auth
                });
                resolve(false);
            }, 10000);
        });
    }
}

// 全局實例
const authHandler = new AuthHandler();
window.authHandler = authHandler;

// 暴露給全局
window.AuthHandler = AuthHandler;

console.log('✅ auth-handler.js 已加載');

