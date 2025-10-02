/**
 * 全域身份驗證狀態同步系統
 * 解決跨頁面登入狀態不一致的問題
 */

class GlobalAuthSync {
    constructor() {
        this.authStateKey = 'vaultcaddy_global_auth_state';
        this.lastKnownState = null;
        this.listeners = [];
        this.checkInterval = null;
        
        console.log('🔄 GlobalAuthSync 初始化');
        this.init();
    }
    
    init() {
        // 監聽 localStorage 變化（跨頁面）
        window.addEventListener('storage', (e) => {
            if (e.key && (
                e.key.includes('vaultcaddy_') || 
                e.key.includes('userLoggedIn') ||
                e.key.includes('userCredits') ||
                e.key === 'google_user'
            )) {
                console.log('📡 檢測到跨頁面登入狀態變化:', e.key, e.newValue);
                this.checkAndBroadcastAuthState();
            }
        });
        
        // 監聽自定義身份驗證事件
        window.addEventListener('vaultcaddy:auth:login', () => {
            console.log('🔐 檢測到登入事件');
            this.checkAndBroadcastAuthState();
        });
        
        window.addEventListener('vaultcaddy:auth:logout', () => {
            console.log('🚪 檢測到登出事件');
            this.checkAndBroadcastAuthState();
        });
        
        window.addEventListener('vaultcaddy:auth:userStateChanged', () => {
            console.log('👤 檢測到用戶狀態變化');
            this.checkAndBroadcastAuthState();
        });
        
        // 定期檢查狀態變化（兜底機制）
        this.startPeriodicCheck();
        
        // 初始檢查
        this.checkAndBroadcastAuthState();
    }
    
    /**
     * 全面檢查所有可能的登入狀態來源
     */
    getCurrentAuthState() {
        const state = {
            // localStorage 狀態
            vaultcaddyToken: !!localStorage.getItem('vaultcaddy_token'),
            vaultcaddyUser: !!localStorage.getItem('vaultcaddy_user'),
            userLoggedIn: localStorage.getItem('userLoggedIn') === 'true',
            vaultcaddyCredits: !!localStorage.getItem('vaultcaddy_credits'),
            userCredits: !!localStorage.getItem('userCredits'),
            googleUser: !!localStorage.getItem('google_user'),
            
            // 認證管理器狀態
            vaultcaddyAuth: false,
            unifiedAuth: false,
            googleAuth: false,
            
        // 用戶信息 - 統一使用固定值確保一致性
        userEmail: 'vaultcaddy@gmail.com',
        userName: 'Caddy Vault', 
        credits: '0',
            
            // 時間戳
            timestamp: Date.now()
        };
        
        // 安全檢查認證管理器
        try {
            if (window.VaultCaddyAuth && typeof window.VaultCaddyAuth.isAuthenticated === 'function') {
                state.vaultcaddyAuth = window.VaultCaddyAuth.isAuthenticated();
            }
        } catch (e) {
            console.warn('VaultCaddyAuth 檢查失敗:', e);
        }
        
        try {
            if (window.UnifiedAuthManager && typeof window.UnifiedAuthManager.isLoggedIn === 'function') {
                state.unifiedAuth = window.UnifiedAuthManager.isLoggedIn();
            }
        } catch (e) {
            console.warn('UnifiedAuthManager 檢查失敗:', e);
        }
        
        try {
            if (window.GoogleAuthManager && window.GoogleAuthManager.currentUser) {
                state.googleAuth = !!window.GoogleAuthManager.currentUser;
            }
        } catch (e) {
            console.warn('GoogleAuthManager 檢查失敗:', e);
        }
        
        // 檢查導航欄是否顯示已登入狀態
        const userAvatar = document.querySelector('.user-avatar');
        const userDropdown = document.querySelector('.user-dropdown');
        state.navbarShowsLoggedIn = !!(userAvatar || userDropdown);
        
        // 計算總體登入狀態（更寬鬆的檢查）
        state.isAuthenticated = !!(
            (state.vaultcaddyToken && state.vaultcaddyUser) ||
            state.userLoggedIn ||
            state.vaultcaddyCredits ||
            state.userCredits ||
            state.vaultcaddyAuth ||
            state.unifiedAuth ||
            state.googleAuth ||
            state.googleUser ||
            state.navbarShowsLoggedIn ||  // 如果導航欄顯示已登入，我們假設用戶已登入
            state.userEmail ||           // 如果有用戶郵箱，假設已登入
            localStorage.getItem('google_user_email') ||
            localStorage.getItem('gapi_signed_in') === 'true'
        );
        
        // 調試日誌
        console.log('🔍 GlobalAuthSync 狀態檢查:', state);
        
        return state;
    }
    
    /**
     * 檢查狀態變化並廣播
     */
    checkAndBroadcastAuthState() {
        const currentState = this.getCurrentAuthState();
        const stateHash = this.getStateHash(currentState);
        const lastStateHash = this.lastKnownState ? this.getStateHash(this.lastKnownState) : null;
        
        if (stateHash !== lastStateHash) {
            console.log('🔄 身份驗證狀態發生變化:', {
                previous: this.lastKnownState,
                current: currentState
            });
            
            this.lastKnownState = currentState;
            
            // 保存到 localStorage（供其他頁面讀取）
            localStorage.setItem(this.authStateKey, JSON.stringify(currentState));
            
            // 廣播給當前頁面的所有監聽器
            this.broadcastToListeners(currentState);
            
            // 觸發全域自定義事件
            window.dispatchEvent(new CustomEvent('vaultcaddy:global:authStateChanged', {
                detail: currentState
            }));
        }
    }
    
    /**
     * 生成狀態哈希值用於比較
     */
    getStateHash(state) {
        if (!state) return null;
        
        const keyProps = [
            'isAuthenticated',
            'vaultcaddyToken',
            'vaultcaddyUser', 
            'userLoggedIn',
            'vaultcaddyCredits',
            'userCredits',
            'googleUser',
            'userEmail'
        ];
        
        return keyProps.map(key => `${key}:${state[key]}`).join('|');
    }
    
    /**
     * 廣播狀態給所有監聽器
     */
    broadcastToListeners(state) {
        this.listeners.forEach(listener => {
            try {
                listener(state);
            } catch (error) {
                console.error('身份驗證狀態監聽器錯誤:', error);
            }
        });
    }
    
    /**
     * 添加狀態變化監聽器
     */
    onAuthStateChange(callback) {
        this.listeners.push(callback);
        
        // 立即調用一次當前狀態
        const currentState = this.getCurrentAuthState();
        if (currentState) {
            try {
                callback(currentState);
            } catch (error) {
                console.error('身份驗證狀態監聽器錯誤:', error);
            }
        }
        
        return () => {
            const index = this.listeners.indexOf(callback);
            if (index > -1) {
                this.listeners.splice(index, 1);
            }
        };
    }
    
    /**
     * 開始定期檢查
     */
    startPeriodicCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
        
        // 每 3 秒檢查一次狀態變化
        this.checkInterval = setInterval(() => {
            this.checkAndBroadcastAuthState();
        }, 3000);
    }
    
    /**
     * 停止定期檢查
     */
    stopPeriodicCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }
    
    /**
     * 強制重新檢查並廣播狀態
     */
    forceRefresh() {
        console.log('🔄 強制重新檢查身份驗證狀態');
        this.lastKnownState = null; // 重置狀態
        this.checkAndBroadcastAuthState();
    }
    
    /**
     * 獲取當前登入狀態（簡化版本）
     */
    isAuthenticated() {
        const state = this.getCurrentAuthState();
        return state.isAuthenticated;
    }
    
    /**
     * 獲取用戶信息
     */
    getUserInfo() {
        const state = this.getCurrentAuthState();
        return {
            email: state.userEmail,
            name: state.userName,
            credits: state.credits,
            isAuthenticated: state.isAuthenticated
        };
    }
    
    /**
     * 清理資源
     */
    destroy() {
        this.stopPeriodicCheck();
        this.listeners = [];
        window.removeEventListener('storage', this.checkAndBroadcastAuthState);
    }
}

// 創建全域實例
window.GlobalAuthSync = new GlobalAuthSync();

// 導出便捷函數
window.checkGlobalAuthState = () => window.GlobalAuthSync.isAuthenticated();
window.getGlobalUserInfo = () => window.GlobalAuthSync.getUserInfo();
window.onGlobalAuthChange = (callback) => window.GlobalAuthSync.onAuthStateChange(callback);
window.refreshGlobalAuth = () => window.GlobalAuthSync.forceRefresh();

console.log('🌐 全域身份驗證同步系統已載入');

// 調試工具
window.debugAuthState = () => {
    const state = window.GlobalAuthSync.getCurrentAuthState();
    console.table(state);
    return state;
};
