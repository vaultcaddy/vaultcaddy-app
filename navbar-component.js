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
                        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face&auto=format'
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
                <a href="index.html">
                    <div class="logo-container">
                        <div class="logo-icon">
                            <i class="fas fa-file-contract"></i>
                        </div>
                        <div class="logo-text">
                            <h2>VaultCaddy</h2>
                            <span>AI Document Processing</span>
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
        return `
            <a href="#features" class="nav-link" data-translate="nav_features">功能</a>
            <a href="#pricing" class="nav-link" data-translate="nav_pricing">價格</a>
            <a href="#api" class="nav-link" data-translate="nav_api">API</a>
        `;
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
     * 獲取語言選擇器
     */
    getLanguageSelector() {
        const languages = [
            { code: 'zh-tw', name: '繁體中文' },
            { code: 'en', name: 'English' },
            { code: 'zh-cn', name: '简体中文' },
            { code: 'ja', name: '日本語' }
        ];
        
        const options = languages.map(lang => 
            `<option value="${lang.code}" ${lang.code === this.language ? 'selected' : ''}>${lang.name}</option>`
        ).join('');
        
        return `
            <div class="language-selector">
                <select class="language-select" onchange="window.VaultCaddyNavbar.changeLanguage(this.value)">
                    ${options}
                </select>
            </div>
        `;
    }
    
    /**
     * 獲取用戶區塊
     */
    getUserSection() {
        if (this.isLoggedIn && this.user) {
            return `
                <div class="user-profile" id="user-profile">
                    <img src="${this.user.avatar}" alt="User" class="user-avatar" onclick="window.VaultCaddyNavbar.toggleUserDropdown(event)">
                    <div class="user-dropdown-menu" id="user-dropdown-menu">
                        <div class="user-info">
                            <span class="user-credits">Credits: ${this.credits}</span>
                            <span class="user-email">${this.user.email}</span>
                        </div>
                        <hr>
                        <a href="#" class="user-menu-item" onclick="window.VaultCaddyNavbar.userAction('account')">
                            <i class="fas fa-user"></i>
                            <span>Account</span>
                            <span class="shortcut">⌘A</span>
                        </a>
                        <a href="#" class="user-menu-item" onclick="window.VaultCaddyNavbar.userAction('integrations')">
                            <i class="fas fa-puzzle-piece"></i>
                            <span>Integrations</span>
                            <span class="shortcut">⌘I</span>
                        </a>
                        <a href="#" class="user-menu-item" onclick="window.VaultCaddyNavbar.userAction('billing')">
                            <i class="fas fa-credit-card"></i>
                            <span>Billing</span>
                            <span class="shortcut">⌘B</span>
                        </a>
                        <a href="#" class="user-menu-item" onclick="window.VaultCaddyNavbar.userAction('settings')">
                            <i class="fas fa-cog"></i>
                            <span>Settings</span>
                            <span class="shortcut">⌘S</span>
                        </a>
                        <hr>
                        <a href="#" class="user-menu-item logout" onclick="window.VaultCaddyNavbar.logout()">
                            <i class="fas fa-sign-out-alt"></i>
                            <span>Log out</span>
                            <span class="shortcut">⌘Q</span>
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
                userDropdown.classList.remove('show');
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
            userDropdown.classList.remove('show');
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
        const menu = document.getElementById('user-dropdown-menu');
        if (menu) {
            menu.classList.toggle('show');
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
