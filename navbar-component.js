/**
 * VaultCaddy 統一導航欄組件
 * 解決會員狀態不一致問題，實現市場標準做法
 */

class VaultCaddyNavbar {
    constructor() {
        this.user = null;
        this.credits = 0;
        this.isLoggedIn = false;
        this.language = 'zh-tw';
        
        this.init();
    }
    
    /**
     * 初始化導航欄
     */
    async init() {
        await this.loadUserState();
        this.render();
        this.bindEvents();
        
        // 監聽用戶狀態變化
        this.watchUserState();
    }
    
    /**
     * 載入用戶狀態
     */
    async loadUserState() {
        try {
            // 檢查是否有真實的認證 token
            const token = localStorage.getItem('vaultcaddy_token');
            const userData = localStorage.getItem('vaultcaddy_user');
            
            if (token && userData) {
                // 真實認證系統
                this.user = JSON.parse(userData);
                this.credits = this.user.credits || 0;
                this.isLoggedIn = true;
            } else {
                // 回退到簡單模擬（開發階段）
                this.isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
                this.credits = parseInt(localStorage.getItem('userCredits') || '10');
                
                if (this.isLoggedIn) {
                    this.user = {
                        id: 'demo_user',
                        email: 'demo@vaultcaddy.com',
                        name: 'Demo User',
                        avatar: 'https://ui-avatars.com/api/?name=User&background=3b82f6&color=ffffff&size=32'
                    };
                }
            }
            
            // 載入語言設置
            this.language = localStorage.getItem('preferred_language') || 'zh-tw';
            
        } catch (error) {
            console.error('載入用戶狀態失敗:', error);
            this.resetUserState();
        }
    }
    
    /**
     * 重置用戶狀態
     */
    resetUserState() {
        this.user = null;
        this.credits = 10; // 預設 credits
        this.isLoggedIn = false;
    }
    
    /**
     * 渲染導航欄
     */
    render() {
        const navbarContainer = document.querySelector('.navbar .nav-container');
        if (!navbarContainer) {
            console.error('找不到導航欄容器');
            return;
        }
        
        // 更新導航欄內容
        navbarContainer.innerHTML = this.getNavbarHTML();
        
        // 重新綁定事件
        this.bindEvents();
    }
    
    /**
     * 獲取導航欄 HTML
     */
    getNavbarHTML() {
        return `
            <div class="nav-logo">
                <a href="index.html" style="text-decoration: none;">
                    <div class="logo-container" style="display: flex; align-items: center; gap: 0.75rem;">
                        <div class="logo-icon" style="position: relative;">
                            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <defs>
                                    <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="#3b82f6"/>
                                        <stop offset="50%" stop-color="#8b5cf6"/>
                                        <stop offset="100%" stop-color="#d946ef"/>
                                    </linearGradient>
                                </defs>
                                <path d="M8 6 L20 28 L32 6 L28 6 L20 20 L12 6 Z" fill="url(#logoGradient)" stroke="none"/>
                            </svg>
                        </div>
                        <div class="logo-text" style="display: flex; flex-direction: column;">
                            <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #1f2937; letter-spacing: -0.025em;">VaultCaddy</h2>
                            <span style="margin: 0; font-size: 0.75rem; color: #6b7280; font-weight: 500;">AI Document Processing</span>
                        </div>
                    </div>
                </a>
            </div>
            
            <div class="nav-menu" id="nav-menu">
                ${this.getMainNavigation()}
                ${this.getCreditsDisplay()}
                ${this.getLanguageSelector()}
                ${this.getUserSection()}
            </div>
            
            <div class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        `;
    }
    
    /**
     * 獲取主導航
     */
    getMainNavigation() {
        let navigation = `
            <a href="#features" class="nav-link" data-translate="nav_features">功能</a>
            <a href="#pricing" class="nav-link" data-translate="nav_pricing">價格</a>
        `;
        
        // 只有登入後才顯示 Dashboard 連結
        if (this.isLoggedIn) {
            navigation += `<a href="dashboard-main.html" class="nav-link" data-translate="nav_dashboard" onclick="window.location.href='dashboard-main.html'">Dashboard</a>`;
        }
        
        return navigation;
    }
    
    /**
     * 獲取 Credits 顯示
     */
    getCreditsDisplay() {
        return `
            <div class="credits-display">
                <span data-translate="nav_credits">Credits:</span>
                <span class="credits-count" id="credits-count">${this.credits}</span>
                <div class="credits-icon">
                    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiNGRkQ3MDAiLz4KPHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4PSI1IiB5PSI1Ij4KPHBhdGggZD0iTTcgMUw4LjA5IDQuMjZMMTIgNUw4LjA5IDUuNzRMNyA5TDUuOTEgNS43NEwyIDVMNS45MSA0LjI2TDcgMVoiIGZpbGw9IiNGRkZGRkYiLz4KPHN2Zz4KPHN2Zz4=" alt="Credits" />
                </div>
            </div>
        `;
    }
    
    /**
     * 獲取語言選擇器（暫時移除，沒有實際功能）
     */
    getLanguageSelector() {
        return ''; // 移除語言選擇器
    }
    
    /**
     * 獲取用戶區塊
     */
    getUserSection() {
        if (this.isLoggedIn && this.user) {
            return `
                <div class="user-profile" id="user-profile" style="position: relative;">
                    <img src="https://ui-avatars.com/api/?name=${encodeURIComponent(this.user.name || 'User')}&background=3b82f6&color=ffffff&size=32" alt="User" class="user-avatar" onclick="window.VaultCaddyNavbar.toggleUserDropdown(event)" style="cursor: pointer; border-radius: 50%; width: 32px; height: 32px;">
                    <div class="user-dropdown-menu" id="user-dropdown-menu" style="display: none; position: absolute; top: 100%; right: 0; background: white; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); min-width: 220px; z-index: 1000; padding: 0.5rem 0; margin-top: 8px;">
                        <div class="user-info" style="padding: 1rem 1.5rem; background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
                            <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">Credits: ${this.credits}</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">${this.user.email}</div>
                        </div>
                        <a href="account.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #374151; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#f3f4f6'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-user" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>Account</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘A</span>
                        </a>
                        <a href="integrations.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #374151; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#f3f4f6'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-puzzle-piece" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>Integrations</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘I</span>
                        </a>
                        <div style="margin: 0.5rem 0; border-top: 1px solid #e5e7eb;"></div>
                        <a href="#" class="user-menu-item logout" onclick="window.VaultCaddyNavbar.logout()" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #dc2626; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#fef2f2'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-sign-out-alt" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>Log out</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘Q</span>
                        </a>
                    </div>
                </div>
            `;
        } else {
            return `
                <button class="nav-link login-btn" data-translate="nav_login" onclick="window.VaultCaddyNavbar.handleLogin()">登入 →</button>
            `;
        }
    }
    
    /**
     * 綁定事件
     */
    bindEvents() {
        // 點擊外部關閉下拉選單
        document.addEventListener('click', (event) => {
            const userProfile = document.getElementById('user-profile');
            const userDropdown = document.getElementById('user-dropdown-menu');
            
            if (userDropdown && userProfile && !userProfile.contains(event.target)) {
                userDropdown.style.display = 'none';
            }
        });
        
        // 響應式導航切換
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
            });
        }
    }
    
    /**
     * 監聽用戶狀態變化
     */
    watchUserState() {
        // 監聽 storage 變化
        window.addEventListener('storage', (e) => {
            if (e.key === 'vaultcaddy_user' || e.key === 'userLoggedIn' || e.key === 'userCredits') {
                this.loadUserState().then(() => this.render());
            }
        });
        
        // 監聽自定義事件
        window.addEventListener('userStateChanged', () => {
            this.loadUserState().then(() => this.render());
        });
    }
    
    /**
     * 處理登入
     */
    async handleLogin() {
        try {
            // 如果有真實的認證系統
            if (window.VaultCaddyAuth) {
                window.location.href = 'auth.html';
            } else {
                // 簡單模擬登入
                localStorage.setItem('userLoggedIn', 'true');
                localStorage.setItem('userCredits', '7');
                
                // 觸發狀態更新
                window.dispatchEvent(new CustomEvent('userStateChanged'));
                
                // 跳轉到 dashboard
                window.location.href = 'dashboard-main.html';
            }
        } catch (error) {
            console.error('登入失敗:', error);
        }
    }
    
    /**
     * 處理登出
     */
    async logout() {
        try {
            // 清除認證資料
            localStorage.removeItem('vaultcaddy_token');
            localStorage.removeItem('vaultcaddy_user');
            localStorage.removeItem('vaultcaddy_credits');
            localStorage.removeItem('userLoggedIn');
            localStorage.removeItem('userCredits');
            
            // 觸發狀態更新
            window.dispatchEvent(new CustomEvent('userStateChanged'));
            
            // 跳轉到首頁
            window.location.href = 'index.html';
        } catch (error) {
            console.error('登出失敗:', error);
        }
    }
    
    /**
     * 用戶操作
     */
    userAction(action) {
        const userDropdown = document.getElementById('user-dropdown-menu');
        if (userDropdown) {
            userDropdown.style.display = 'none';
        }
        
        switch(action) {
            case 'account':
                this.showNotification('Account settings coming soon!');
                break;
            case 'integrations':
                this.showNotification('Integrations page coming soon!');
                break;
            case 'billing':
                this.showNotification('Billing page coming soon!');
                break;
            case 'settings':
                this.showNotification('Settings page coming soon!');
                break;
        }
    }
    
    /**
     * 切換用戶下拉選單
     */
    toggleUserDropdown(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const menu = document.getElementById('user-dropdown-menu');
        if (menu) {
            // 切換顯示狀態
            if (menu.style.display === 'none' || menu.style.display === '') {
                menu.style.display = 'block';
            } else {
                menu.style.display = 'none';
            }
        }
    }
    
    /**
     * 改變語言
     */
    changeLanguage(language) {
        this.language = language;
        localStorage.setItem('preferred_language', language);
        
        // 觸發語言變更事件
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: language }));
        
        this.showNotification(`Language changed to ${language}`);
    }
    
    /**
     * 顯示通知
     */
    showNotification(message, type = 'info') {
        // 創建通知元素
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            border-radius: 6px;
            z-index: 10000;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        document.body.appendChild(notification);
        
        // 3秒後自動移除
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    /**
     * 更新 Credits
     */
    updateCredits(newCredits) {
        this.credits = newCredits;
        localStorage.setItem('userCredits', newCredits.toString());
        
        // 更新顯示
        const creditsElement = document.getElementById('credits-count');
        if (creditsElement) {
            creditsElement.textContent = newCredits;
        }
        
        // 更新用戶下拉選單中的 credits
        const userCreditsElement = document.querySelector('.user-credits');
        if (userCreditsElement) {
            userCreditsElement.textContent = `Credits: ${newCredits}`;
        }
    }
}

// 創建全局實例
window.VaultCaddyNavbar = new VaultCaddyNavbar();

// 頁面載入完成後初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.VaultCaddyNavbar.init();
    });
} else {
    window.VaultCaddyNavbar.init();
}
