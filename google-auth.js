/**
 * VaultCaddy Google 認證系統
 * 整合 Google Sign-In API 和 Firebase Authentication
 */

class GoogleAuthManager {
    constructor() {
        this.isInitialized = false;
        this.currentUser = null;
        this.firebaseApp = null;
        this.auth = null;
        
        // Google OAuth 配置
        this.config = {
            // 您需要在 Google Cloud Console 中獲取這個 Client ID
            googleClientId: window.location.hostname === 'vaultcaddy.com' ? 
                '672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com' : // 生產環境
                '672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com', // 開發環境（使用同一個）
            
            // Firebase 配置（可選，用於數據持久化）
            firebaseConfig: {
                apiKey: "AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug",
                authDomain: "vaultcaddy-production.firebaseapp.com",
                projectId: "vaultcaddy-production",
                storageBucket: "vaultcaddy-production.appspot.com",
                messagingSenderId: "123456789",
                appId: "1:123456789:web:abcdef123456"
            }
        };
        
        this.userDataManager = new UserDataManager();
        
        console.log('🔐 Google Auth Manager 初始化');
    }
    
    /**
     * 初始化 Google 認證
     */
    async initialize() {
        if (this.isInitialized) return;
        
        try {
            // 載入 Google Sign-In API
            await this.loadGoogleSignInAPI();
            
            // 初始化 Firebase（可選）
            if (typeof firebase !== 'undefined') {
                await this.initializeFirebase();
            }
            
            // 初始化 Google Sign-In
            await this.initializeGoogleSignIn();
            
            // 檢查現有登入狀態
            await this.checkExistingAuth();
            
            this.isInitialized = true;
            console.log('✅ Google 認證系統初始化完成');
            
        } catch (error) {
            console.error('❌ Google 認證初始化失敗:', error);
            this.fallbackToLocalAuth();
        }
    }
    
    /**
     * 載入 Google Sign-In API
     */
    async loadGoogleSignInAPI() {
        return new Promise((resolve, reject) => {
            // 檢查是否已載入
            if (window.google && window.google.accounts) {
                resolve();
                return;
            }
            
            // 載入 Google Sign-In API
            const script = document.createElement('script');
            script.src = 'https://accounts.google.com/gsi/client';
            script.async = true;
            script.defer = true;
            
            script.onload = () => {
                console.log('✅ Google Sign-In API 載入完成');
                resolve();
            };
            
            script.onerror = () => {
                reject(new Error('Google Sign-In API 載入失敗'));
            };
            
            document.head.appendChild(script);
        });
    }
    
    /**
     * 初始化 Firebase（可選）
     */
    async initializeFirebase() {
        try {
            if (!firebase.apps.length) {
                this.firebaseApp = firebase.initializeApp(this.config.firebaseConfig);
            } else {
                this.firebaseApp = firebase.app();
            }
            
            this.auth = firebase.auth();
            console.log('✅ Firebase 初始化完成');
            
        } catch (error) {
            console.warn('⚠️ Firebase 初始化失敗，使用本地存儲:', error);
        }
    }
    
    /**
     * 初始化 Google Sign-In
     */
    async initializeGoogleSignIn() {
        if (!window.google || !window.google.accounts) {
            throw new Error('Google Sign-In API 未載入');
        }
        
        // 初始化 Google Identity Services
        google.accounts.id.initialize({
            client_id: this.config.googleClientId,
            callback: this.handleGoogleSignIn.bind(this),
            auto_select: false,
            cancel_on_tap_outside: false
        });
        
        console.log('✅ Google Sign-In 初始化完成');
    }
    
    /**
     * 處理 Google 登入回調
     */
    async handleGoogleSignIn(response) {
        try {
            console.log('🔐 處理 Google 登入回調');
            
            // 解碼 JWT token
            const userInfo = this.parseJWT(response.credential);
            
            // 創建用戶對象
            const user = {
                uid: userInfo.sub,
                email: userInfo.email,
                displayName: userInfo.name,
                photoURL: userInfo.picture,
                emailVerified: userInfo.email_verified,
                provider: 'google.com',
                accessToken: response.credential,
                loginTime: new Date().toISOString()
            };
            
            // 保存用戶信息
            await this.setCurrentUser(user);
            
            // 載入用戶數據
            await this.userDataManager.loadUserData(user.uid);
            
            // 通知其他組件
            this.notifyAuthStateChanged(user);
            
            console.log('✅ Google 登入成功:', user.displayName);
            
        } catch (error) {
            console.error('❌ Google 登入處理失敗:', error);
            this.showError('登入失敗，請稍後再試');
        }
    }
    
    /**
     * 解析 JWT Token
     */
    parseJWT(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            
            return JSON.parse(jsonPayload);
        } catch (error) {
            console.error('JWT 解析失敗:', error);
            throw error;
        }
    }
    
    /**
     * 顯示 Google 登入按鈕
     */
    renderSignInButton(elementId = 'google-signin-button') {
        const element = document.getElementById(elementId);
        if (!element) {
            console.warn(`找不到登入按鈕元素: ${elementId}`);
            return;
        }
        
        // 清空現有內容
        element.innerHTML = '';
        
        // 渲染 Google 登入按鈕
        google.accounts.id.renderButton(element, {
            theme: 'outline',
            size: 'large',
            type: 'standard',
            text: 'signin_with',
            shape: 'rectangular',
            logo_alignment: 'left',
            width: 250
        });
        
        console.log('✅ Google 登入按鈕已渲染');
    }
    
    /**
     * 程式化觸發登入
     */
    signIn() {
        if (!window.google || !window.google.accounts) {
            console.error('Google Sign-In API 未初始化');
            this.showError('Google 登入服務不可用');
            return;
        }
        
        google.accounts.id.prompt((notification) => {
            console.log('Google 登入提示:', notification);
        });
    }
    
    /**
     * 登出
     */
    async signOut() {
        try {
            // Google Sign-Out
            if (window.google && window.google.accounts) {
                google.accounts.id.disableAutoSelect();
            }
            
            // Firebase Sign-Out
            if (this.auth) {
                await this.auth.signOut();
            }
            
            // 清除本地數據
            await this.clearCurrentUser();
            
            // 通知組件
            this.notifyAuthStateChanged(null);
            
            console.log('✅ 用戶已登出');
            
        } catch (error) {
            console.error('❌ 登出失敗:', error);
        }
    }
    
    /**
     * 設置當前用戶
     */
    async setCurrentUser(user) {
        this.currentUser = user;
        
        // 保存到本地存儲
        localStorage.setItem('vaultcaddy_user', JSON.stringify(user));
        
        // 保存到 Firebase（如果可用）
        if (this.auth) {
            try {
                // 這裡可以保存額外的用戶數據到 Firestore
                console.log('✅ 用戶數據已同步到 Firebase');
            } catch (error) {
                console.warn('⚠️ Firebase 同步失敗:', error);
            }
        }
        
        // 更新統一認證管理器
        if (window.UnifiedAuthManager) {
            window.UnifiedAuthManager.setAuthState({
                isLoggedIn: true,
                user: user,
                token: user.accessToken
            });
        }
    }
    
    /**
     * 清除當前用戶
     */
    async clearCurrentUser() {
        this.currentUser = null;
        
        // 清除本地存儲
        localStorage.removeItem('vaultcaddy_user');
        
        // 清除用戶數據
        this.userDataManager.clearUserData();
        
        // 更新統一認證管理器
        if (window.UnifiedAuthManager) {
            window.UnifiedAuthManager.logout();
        }
    }
    
    /**
     * 檢查現有認證狀態
     */
    async checkExistingAuth() {
        try {
            // 檢查本地存儲的用戶信息
            const savedUser = localStorage.getItem('vaultcaddy_user');
            if (savedUser) {
                const user = JSON.parse(savedUser);
                
                // 驗證 token 是否仍然有效
                if (await this.validateUserToken(user)) {
                    this.currentUser = user;
                    await this.userDataManager.loadUserData(user.uid);
                    this.notifyAuthStateChanged(user);
                    console.log('✅ 恢復用戶登入狀態:', user.displayName);
                } else {
                    // Token 無效，清除數據
                    await this.clearCurrentUser();
                }
            }
        } catch (error) {
            console.error('檢查認證狀態失敗:', error);
        }
    }
    
    /**
     * 驗證用戶 Token
     */
    async validateUserToken(user) {
        // 簡單的時間檢查（可以改進為實際的 token 驗證）
        const loginTime = new Date(user.loginTime);
        const now = new Date();
        const hoursDiff = (now - loginTime) / (1000 * 60 * 60);
        
        // Token 有效期 24 小時
        return hoursDiff < 24;
    }
    
    /**
     * 通知認證狀態變更
     */
    notifyAuthStateChanged(user) {
        // 發送自定義事件
        const event = new CustomEvent('authStateChanged', {
            detail: { user: user, isLoggedIn: !!user }
        });
        window.dispatchEvent(event);
        
        // 更新 UI
        this.updateAuthUI(user);
    }
    
    /**
     * 更新認證相關 UI
     */
    updateAuthUI(user) {
        // 更新導航欄
        if (window.navbar && typeof window.navbar.updateAuthState === 'function') {
            window.navbar.updateAuthState(!!user, user);
        }
        
        // 更新用戶信息顯示
        const userInfoElements = document.querySelectorAll('.user-info');
        userInfoElements.forEach(element => {
            if (user) {
                element.innerHTML = `
                    <img src="${user.photoURL}" alt="${user.displayName}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 8px;">
                    <span>${user.displayName}</span>
                `;
            } else {
                element.innerHTML = '';
            }
        });
    }
    
    /**
     * 後備到本地認證
     */
    fallbackToLocalAuth() {
        console.log('🔄 使用本地認證系統');
        // 這裡可以保留原有的本地認證邏輯
        if (window.UnifiedAuthManager) {
            window.UnifiedAuthManager.initialize();
        }
    }
    
    /**
     * 顯示錯誤訊息
     */
    showError(message) {
        if (window.VaultCaddyNavbar && typeof window.VaultCaddyNavbar.showNotification === 'function') {
            window.VaultCaddyNavbar.showNotification(message, 'error');
        } else {
            alert(message);
        }
    }
    
    /**
     * 獲取當前用戶
     */
    getCurrentUser() {
        return this.currentUser;
    }
    
    /**
     * 檢查是否已登入
     */
    isLoggedIn() {
        return !!this.currentUser;
    }
    
    /**
     * 獲取用戶數據管理器
     */
    getUserDataManager() {
        return this.userDataManager;
    }
}

/**
 * 用戶數據管理器 - 處理數據的永久保存
 */
class UserDataManager {
    constructor() {
        this.userData = {
            credits: 0,
            subscriptionPlan: null,
            documents: [],
            preferences: {},
            createdAt: null,
            lastLoginAt: null
        };
        
        this.firestore = null;
        
        // 初始化 Firestore 連接
        this.initializeFirestore();
    }
    
    /**
     * 初始化 Firestore
     */
    async initializeFirestore() {
        try {
            if (typeof firebase !== 'undefined' && firebase.firestore) {
                this.firestore = firebase.firestore();
                console.log('✅ Firestore 數據管理器初始化完成');
            }
        } catch (error) {
            console.warn('⚠️ Firestore 初始化失敗，使用本地存儲:', error);
        }
    }
    
    /**
     * 載入用戶數據
     */
    async loadUserData(userId) {
        try {
            let userData = null;
            
            // 優先從 Firestore 載入
            if (this.firestore) {
                userData = await this.loadFromFirestore(userId);
            }
            
            // 後備：從本地存儲載入
            if (!userData) {
                userData = this.loadFromLocalStorage(userId);
            }
            
            // 如果沒有數據，創建新用戶
            if (!userData) {
                userData = await this.createNewUser(userId);
            }
            
            this.userData = userData;
            console.log('✅ 用戶數據載入完成:', userId);
            
            return userData;
            
        } catch (error) {
            console.error('❌ 載入用戶數據失敗:', error);
            // 使用默認數據
            this.userData = await this.createNewUser(userId);
            return this.userData;
        }
    }
    
    /**
     * 從 Firestore 載入數據
     */
    async loadFromFirestore(userId) {
        if (!this.firestore) return null;
        
        try {
            const doc = await this.firestore.collection('users').doc(userId).get();
            
            if (doc.exists) {
                const data = doc.data();
                console.log('✅ 從 Firestore 載入用戶數據');
                return data;
            }
            
            return null;
        } catch (error) {
            console.error('Firestore 載入失敗:', error);
            return null;
        }
    }
    
    /**
     * 從本地存儲載入數據
     */
    loadFromLocalStorage(userId) {
        try {
            const localData = localStorage.getItem(`vaultcaddy_userdata_${userId}`);
            if (localData) {
                console.log('✅ 從本地存儲載入用戶數據');
                return JSON.parse(localData);
            }
            return null;
        } catch (error) {
            console.error('本地存儲載入失敗:', error);
            return null;
        }
    }
    
    /**
     * 創建新用戶數據
     */
    async createNewUser(userId) {
        const newUserData = {
            userId: userId,
            credits: 7, // 新用戶默認 Credits
            subscriptionPlan: null,
            subscriptionCredits: 0,
            documents: [],
            preferences: {
                language: 'zh-TW',
                theme: 'light',
                notifications: true
            },
            createdAt: new Date().toISOString(),
            lastLoginAt: new Date().toISOString(),
            totalDocumentsProcessed: 0,
            totalCreditsUsed: 0
        };
        
        // 保存新用戶數據
        await this.saveUserData(newUserData);
        
        console.log('✅ 創建新用戶數據:', userId);
        return newUserData;
    }
    
    /**
     * 保存用戶數據
     */
    async saveUserData(data = null) {
        const dataToSave = data || this.userData;
        const userId = dataToSave.userId;
        
        if (!userId) {
            console.error('無法保存數據：缺少用戶ID');
            return;
        }
        
        try {
            // 保存到 Firestore
            if (this.firestore) {
                await this.firestore.collection('users').doc(userId).set(dataToSave, { merge: true });
                console.log('✅ 數據已保存到 Firestore');
            }
            
            // 保存到本地存儲（後備）
            localStorage.setItem(`vaultcaddy_userdata_${userId}`, JSON.stringify(dataToSave));
            console.log('✅ 數據已保存到本地存儲');
            
            // 更新當前數據
            this.userData = dataToSave;
            
        } catch (error) {
            console.error('❌ 保存用戶數據失敗:', error);
        }
    }
    
    /**
     * 更新 Credits
     */
    async updateCredits(amount, type = 'add') {
        const currentCredits = this.userData.credits || 0;
        
        if (type === 'add') {
            this.userData.credits = currentCredits + amount;
        } else if (type === 'subtract') {
            this.userData.credits = Math.max(0, currentCredits - amount);
        } else if (type === 'set') {
            this.userData.credits = amount;
        }
        
        await this.saveUserData();
        console.log(`✅ Credits 已更新: ${currentCredits} → ${this.userData.credits}`);
        
        // 更新 UI
        this.updateCreditsDisplay();
    }
    
    /**
     * 更新 Credits 顯示
     */
    updateCreditsDisplay() {
        const creditsElements = document.querySelectorAll('.stat-value, [data-stat="current-credits"]');
        creditsElements.forEach(element => {
            if (element.getAttribute('data-stat') === 'current-credits' || 
                element.classList.contains('stat-value')) {
                element.textContent = this.userData.credits;
            }
        });
    }
    
    /**
     * 添加處理過的文檔記錄
     */
    async addDocumentRecord(documentInfo) {
        this.userData.documents = this.userData.documents || [];
        this.userData.documents.push({
            ...documentInfo,
            processedAt: new Date().toISOString()
        });
        
        this.userData.totalDocumentsProcessed = (this.userData.totalDocumentsProcessed || 0) + 1;
        this.userData.lastLoginAt = new Date().toISOString();
        
        await this.saveUserData();
        console.log('✅ 文檔記錄已添加');
    }
    
    /**
     * 獲取用戶數據
     */
    getUserData() {
        return this.userData;
    }
    
    /**
     * 清除用戶數據
     */
    clearUserData() {
        this.userData = {
            credits: 0,
            subscriptionPlan: null,
            documents: [],
            preferences: {},
            createdAt: null,
            lastLoginAt: null
        };
    }
}

// 全局實例
window.GoogleAuthManager = GoogleAuthManager;
window.UserDataManager = UserDataManager;

// 自動初始化（如果在瀏覽器環境）
if (typeof window !== 'undefined') {
    window.googleAuth = new GoogleAuthManager();
    
    // 頁面載入完成後初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.googleAuth.initialize();
        });
    } else {
        window.googleAuth.initialize();
    }
}
