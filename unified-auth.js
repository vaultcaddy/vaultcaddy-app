/**
 * VaultCaddy 統一認證管理系統
 * 解決會員狀態不一致問題
 */

class UnifiedAuthManager {
    constructor() {
        this.isInitialized = false;
        this.userState = {
            isLoggedIn: false,
            user: null,
            credits: 10,
            token: null,
            loginTime: null
        };
        
        this.init();
    }
    
    /**
     * 初始化認證管理器
     */
    async init() {
        if (this.isInitialized) return;
        
        try {
            await this.loadUserState();
            this.setupEventListeners();
            this.isInitialized = true;
            
            console.log('🔐 UnifiedAuthManager initialized:', this.userState);
        } catch (error) {
            console.error('認證管理器初始化失敗:', error);
        }
    }
    
    /**
     * 載入用戶狀態
     */
    async loadUserState() {
        try {
            // 優先級1: 真實認證系統
            const token = localStorage.getItem('vaultcaddy_token');
            const userData = localStorage.getItem('vaultcaddy_user');
            
            if (token && userData) {
                this.userState = {
                    isLoggedIn: true,
                    user: JSON.parse(userData),
                    credits: JSON.parse(userData).credits || 7,
                    token: token,
                    loginTime: localStorage.getItem('vaultcaddy_login_time')
                };
                return;
            }
            
            // 優先級2: 簡單模擬系統 (開發用)
            const simpleLogin = localStorage.getItem('userLoggedIn');
            const simpleCredits = localStorage.getItem('userCredits');
            
            if (simpleLogin === 'true') {
                this.userState = {
                    isLoggedIn: true,
                    user: {
                        id: 'demo_user',
                        email: 'demo@vaultcaddy.com',
                        name: 'Demo User',
                        avatar: 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png',
                        role: 'user'
                    },
                    credits: parseInt(simpleCredits || '7'),
                    token: 'demo_token',
                    loginTime: Date.now()
                };
                return;
            }
            
            // 預設狀態: 未登入
            this.userState = {
                isLoggedIn: false,
                user: null,
                credits: 10, // 未登入時的預設 credits
                token: null,
                loginTime: null
            };
            
        } catch (error) {
            console.error('載入用戶狀態失敗:', error);
            this.resetUserState();
        }
    }
    
    /**
     * 重置用戶狀態
     */
    resetUserState() {
        this.userState = {
            isLoggedIn: false,
            user: null,
            credits: 10,
            token: null,
            loginTime: null
        };
        
        // 清除所有認證相關的 localStorage
        [
            'vaultcaddy_token',
            'vaultcaddy_user',
            'vaultcaddy_credits',
            'vaultcaddy_login_time',
            'userLoggedIn',
            'userCredits'
        ].forEach(key => localStorage.removeItem(key));
    }
    
    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 監聽 storage 變化
        window.addEventListener('storage', (e) => {
            if (this.isAuthRelatedKey(e.key)) {
                this.loadUserState().then(() => {
                    this.notifyStateChange();
                });
            }
        });
        
        // 監聽自定義認證事件
        window.addEventListener('authStateChanged', (e) => {
            this.loadUserState().then(() => {
                this.notifyStateChange();
            });
        });
        
        // 頁面可見性變化時重新檢查狀態
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.loadUserState().then(() => {
                    this.notifyStateChange();
                });
            }
        });
    }
    
    /**
     * 檢查是否為認證相關的 key
     */
    isAuthRelatedKey(key) {
        const authKeys = [
            'vaultcaddy_token',
            'vaultcaddy_user',
            'vaultcaddy_credits',
            'userLoggedIn',
            'userCredits'
        ];
        return authKeys.includes(key);
    }
    
    /**
     * 通知狀態變化
     */
    notifyStateChange() {
        // 觸發全局事件
        window.dispatchEvent(new CustomEvent('userStateUpdated', {
            detail: this.userState
        }));
        
        // 更新導航欄 (如果存在)
        // ⚠️ 已禁用：Firebase Auth 現在處理導航欄更新
        // if (window.VaultCaddyNavbar) {
        //     window.VaultCaddyNavbar.loadUserState().then(() => {
        //         window.VaultCaddyNavbar.render();
        //     });
        // }
        
        console.log('🔄 User state updated:', this.userState);
    }
    
    /**
     * 執行登入
     */
    async login(credentials) {
        try {
            // 嘗試真實認證系統
            if (window.VaultCaddyAuth) {
                const result = await window.VaultCaddyAuth.login(credentials);
                if (result.success) {
                    await this.loadUserState();
                    this.notifyStateChange();
                    return result;
                }
            }
            
            // 回退到簡單模擬
            return await this.simulateLogin(credentials);
            
        } catch (error) {
            console.error('登入失敗:', error);
            throw error;
        }
    }
    
    /**
     * 模擬登入 (開發用)
     */
    async simulateLogin(credentials) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (credentials.email && credentials.password) {
                    // 模擬成功登入
                    const userData = {
                        id: 'demo_user',
                        email: credentials.email,
                        name: credentials.email.split('@')[0],
                        avatar: 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png',
                        credits: 7,
                        role: 'user'
                    };
                    
                    // 保存到 localStorage
                    localStorage.setItem('userLoggedIn', 'true');
                    localStorage.setItem('userCredits', '7');
                    localStorage.setItem('vaultcaddy_user', JSON.stringify(userData));
                    localStorage.setItem('vaultcaddy_token', 'demo_token_' + Date.now());
                    localStorage.setItem('vaultcaddy_login_time', Date.now().toString());
                    
                    // 更新內部狀態
                    this.loadUserState().then(() => {
                        this.notifyStateChange();
                        
                        resolve({
                            success: true,
                            user: userData,
                            redirectUrl: 'dashboard-main.html',
                            message: '登入成功'
                        });
                    });
                } else {
                    reject({
                        success: false,
                        message: '請輸入有效的郵箱和密碼'
                    });
                }
            }, 1000); // 模擬網絡延遲
        });
    }
    
    /**
     * 執行登出
     */
    async logout() {
        try {
            // 如果有真實認證系統
            if (window.VaultCaddyAuth && this.userState.token !== 'demo_token') {
                await window.VaultCaddyAuth.logout();
            }
            
            // 清除狀態
            this.resetUserState();
            this.notifyStateChange();
            
            return {
                success: true,
                redirectUrl: 'index.html',
                message: '已成功登出'
            };
            
        } catch (error) {
            console.error('登出失敗:', error);
            throw error;
        }
    }
    
    /**
     * 檢查登入狀態
     */
    isLoggedIn() {
        return this.userState.isLoggedIn;
    }
    
    /**
     * 獲取用戶信息
     */
    getUser() {
        return this.userState.user;
    }
    
    /**
     * 獲取 Credits
     */
    getCredits() {
        return this.userState.credits;
    }
    
    /**
     * 更新 Credits
     */
    async updateCredits(newCredits) {
        try {
            this.userState.credits = newCredits;
            
            // 同步到 localStorage
            localStorage.setItem('userCredits', newCredits.toString());
            
            if (this.userState.user) {
                this.userState.user.credits = newCredits;
                localStorage.setItem('vaultcaddy_user', JSON.stringify(this.userState.user));
            }
            
            this.notifyStateChange();
            
            return { success: true, credits: newCredits };
        } catch (error) {
            console.error('更新 Credits 失敗:', error);
            throw error;
        }
    }
    
    /**
     * 獲取完整狀態
     */
    getState() {
        return { ...this.userState };
    }
    
    /**
     * 檢查認證狀態是否有效
     */
    async validateAuth() {
        try {
            // 如果有真實的 token，驗證它
            if (this.userState.token && this.userState.token !== 'demo_token') {
                // TODO: 實現真實的 token 驗證
                return true;
            }
            
            // 簡單模擬驗證
            return this.userState.isLoggedIn;
            
        } catch (error) {
            console.error('認證驗證失敗:', error);
            return false;
        }
    }
    
    /**
     * 獲取認證標頭 (用於 API 請求)
     */
    getAuthHeaders() {
        if (this.userState.token) {
            return {
                'Authorization': `Bearer ${this.userState.token}`,
                'Content-Type': 'application/json'
            };
        }
        return {};
    }
}

// 創建全局實例
window.UnifiedAuthManager = new UnifiedAuthManager();

// 為了向後兼容，提供簡單的全局函數
window.handleLogin = function() {
    if (window.UnifiedAuthManager.isLoggedIn()) {
        window.location.href = 'dashboard-main.html';
    } else {
        window.location.href = 'auth.html';
    }
};

window.handleLogout = function() {
    window.UnifiedAuthManager.logout().then((result) => {
        if (result.success) {
            window.location.href = result.redirectUrl;
        }
    });
};

// 頁面載入完成後初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.UnifiedAuthManager.init();
    });
} else {
    window.UnifiedAuthManager.init();
}

console.log('🚀 Unified Auth Manager loaded');
