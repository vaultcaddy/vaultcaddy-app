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
        
        // 檢查 DOM 是否準備好
        if (document.getElementById('navbar-placeholder')) {
            this.render();
            this.bindEvents();
        } else {
            console.log('⏳ navbar-placeholder 尚未準備好，等待 DOM...');
        }
        
        // 監聽用戶狀態變化
        this.watchUserState();
    }
    
    /**
     * 載入用戶狀態
     */
    async loadUserState() {
        try {
            console.log('🔄 導航欄載入用戶狀態...');
            
            // 🔥 優先使用 Firebase Auth（最新）
            if (window.authHandler && window.authHandler.initialized) {
                const currentUser = window.authHandler.getCurrentUser();
                console.log('🔥 導航欄從 Firebase Auth 獲取狀態:', currentUser);
                
                if (currentUser) {
                    this.isLoggedIn = true;
                    this.isAuthenticated = true;
                    this.user = {
                        id: currentUser.uid,
                        email: currentUser.email || 'user@vaultcaddy.com',
                        name: currentUser.displayName || currentUser.email?.split('@')[0] || 'User',
                        avatar: currentUser.photoURL || 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png'
                    };
                    // TODO: 從 Firestore 獲取 credits
                    this.credits = localStorage.getItem('userCredits') || '0';
                    
                    console.log('✅ Firebase Auth 用戶已載入:', this.user.email);
                } else {
                    this.resetUserState();
                }
            }
            // 使用 GlobalAuthSync（向後兼容）
            else if (window.GlobalAuthSync) {
                const authState = window.GlobalAuthSync.getCurrentAuthState();
                console.log('🌐 導航欄從 GlobalAuthSync 獲取狀態:', authState);
                
                this.isLoggedIn = authState.isAuthenticated;
                this.isAuthenticated = authState.isAuthenticated;
                
                if (this.isLoggedIn) {
                    // 安全提取用戶信息
                    let safeEmail = authState.userEmail;
                    let safeName = authState.userName;
                    
                    // 清理可能的 JSON 數據
                    if (safeEmail && safeEmail.includes('{"uid"')) {
                        safeEmail = 'vaultcaddy@gmail.com';
                        console.log('🧹 導航欄清理了異常的郵箱 JSON 數據');
                    }
                    if (safeName && safeName.includes('{"uid"')) {
                        safeName = 'Caddy Vault';
                        console.log('🧹 導航欄清理了異常的姓名 JSON 數據');
                    }
                    
                    this.user = {
                        id: 'auth_user',
                        email: safeEmail || 'vaultcaddy@gmail.com',
                        name: safeName || 'Caddy Vault',
                        avatar: 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png'
                    };
                    this.credits = authState.credits || '7';
                } else {
                    this.resetUserState();
                }
            } else {
                // 兜底：檢查是否有真實的認證 token
                const token = localStorage.getItem('vaultcaddy_token');
                const userData = localStorage.getItem('vaultcaddy_user');
                
                if (token && userData) {
                    // 真實認證系統
                    this.user = JSON.parse(userData);
                    this.credits = this.user.credits || 0;
                    this.isLoggedIn = true;
                    this.isAuthenticated = true;
                } else {
                    // 未登入
                    this.resetUserState();
                }
            }
            
            // 載入語言設置
            this.language = localStorage.getItem('preferred_language') || 'zh-tw';
            
            console.log('📊 導航欄用戶狀態已載入:', {
                isLoggedIn: this.isLoggedIn,
                isAuthenticated: this.isAuthenticated,
                credits: this.credits,
                user: this.user?.email || 'N/A',
                source: window.authHandler ? 'Firebase Auth' : (window.GlobalAuthSync ? 'GlobalAuthSync' : 'localStorage')
            });
            
        } catch (error) {
            console.error('❌ 載入用戶狀態失敗:', error);
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
        this.isAuthenticated = false;
    }
    
    /**
     * 渲染導航欄
     */
    render() {
        // 支持兩種 ID：navbar-placeholder（舊版）和 navbar-root（新版）
        const navbarPlaceholder = document.getElementById('navbar-placeholder') || document.getElementById('navbar-root');
        if (!navbarPlaceholder) {
            console.error('找不到導航欄占位符 #navbar-placeholder 或 #navbar-root');
            return;
        }
        
        console.log('✅ 找到導航欄容器:', navbarPlaceholder.id);
        
        // 創建完整的導航欄結構
        const navbarHTML = `
            <nav class="navbar">
                <div class="nav-container">
                    ${this.getNavbarHTML()}
                </div>
            </nav>
        `;
        
        // 更新導航欄內容
        navbarPlaceholder.innerHTML = navbarHTML;
        console.log('✅ 導航欄 HTML 已插入，長度:', navbarHTML.length);
        
        // 重新綁定事件
        this.bindEvents();
        
        // 設置 Google 登入按鈕（如果用戶未登入）
        this.setupGoogleSignInButton();
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
            <a href="index.html#features" class="nav-link" data-translate="nav_features" onclick="navigateToSection('features')">功能</a>
            <a href="index.html#pricing" class="nav-link" data-translate="nav_pricing" onclick="navigateToSection('pricing')">價格</a>
        `;
        
        // Dashboard 按鈕 - 前往Team Project視圖
        navigation += `
            <a href="dashboard.html" class="nav-link" data-translate="nav_dashboard">儀表板</a>
        `;
        
        return navigation;
    }
    

    
    /**
     * 獲取語言選擇器
     */
    getLanguageSelector() {
        const languages = {
            'en': 'English',
            'zh-tw': '繁體中文'
        };
        
        const currentLang = this.language || 'zh-tw';
        const currentLangName = languages[currentLang] || languages['zh-tw'];
        
        return `
            <div class="language-selector" style="position: relative;">
                <button class="language-btn" onclick="window.VaultCaddyNavbar.toggleLanguageDropdown(event)" style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    background: none;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 0.5rem 0.75rem;
                    color: #374151;
                    cursor: pointer;
                    font-size: 0.875rem;
                    transition: all 0.2s;
                " onmouseover="this.style.borderColor='#d1d5db'; this.style.backgroundColor='#f9fafb'" onmouseout="this.style.borderColor='#e5e7eb'; this.style.backgroundColor='transparent'">
                    <i class="fas fa-globe" style="color: #6b7280;"></i>
                    <span>${currentLangName}</span>
                    <i class="fas fa-chevron-down" style="color: #9ca3af; font-size: 0.75rem;"></i>
                </button>
                
                <div class="language-dropdown" id="language-dropdown" style="
                    display: none;
                    position: absolute;
                    top: 100%;
                    right: 0;
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                    min-width: 160px;
                    z-index: 1000;
                    padding: 0.5rem 0;
                    margin-top: 4px;
                ">
                    ${Object.entries(languages).map(([code, name]) => `
                        <button class="language-option" onclick="window.VaultCaddyNavbar.changeLanguage('${code}')" style="
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            width: 100%;
                            padding: 0.5rem 1rem;
                            background: none;
                            border: none;
                            color: #374151;
                            cursor: pointer;
                            font-size: 0.875rem;
                            transition: background-color 0.2s;
                            ${code === currentLang ? 'background-color: #eff6ff; color: #2563eb;' : ''}
                        " onmouseover="if('${code}' !== '${currentLang}') this.style.backgroundColor='#f3f4f6'" onmouseout="if('${code}' !== '${currentLang}') this.style.backgroundColor='transparent'">
                            <span>${name}</span>
                            ${code === currentLang ? '<i class="fas fa-check" style="color: #2563eb; font-size: 0.75rem;"></i>' : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    /**
     * 獲取用戶區塊
     */
    getUserSection() {
        // 檢查 Google 認證狀態
        const isGoogleLoggedIn = window.googleAuth && window.googleAuth.isLoggedIn();
        const googleUser = isGoogleLoggedIn ? window.googleAuth.getCurrentUser() : null;
        
        // 優先使用 Google 認證，否則使用原有認證
        const currentUser = googleUser || (this.isLoggedIn ? this.user : null);
        const userCredits = googleUser ? 
            (window.googleAuth.getUserDataManager().getUserData()?.credits || 0) : 
            this.credits;
        
        if (currentUser) {
            const userPhotoURL = googleUser ? 
                googleUser.photoURL : 
                'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png';
            
            const userName = googleUser ? googleUser.displayName : (currentUser.name || 'User');
            const userEmail = googleUser ? googleUser.email : (currentUser.email || '');
            
            return `
                <div class="user-profile" id="user-profile" style="position: relative;">
                    <img src="${userPhotoURL}" alt="${userName}" class="user-avatar" onclick="window.VaultCaddyNavbar.toggleUserDropdown(event)" style="cursor: pointer; border-radius: 50%; width: 32px; height: 32px;">
                    <div class="user-dropdown-menu" id="user-dropdown-menu" style="display: none; position: absolute; top: 100%; right: 0; background: white; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); min-width: 220px; z-index: 1000; padding: 0.5rem 0; margin-top: 8px;">
                        <div class="user-info" style="padding: 1rem 1.5rem; background: #f9fafb; border-bottom: 1px solid #e5e7eb;">
                            <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">Credits: ${userCredits}</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">${userEmail}</div>
                            ${googleUser ? '<div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;"><i class="fab fa-google"></i> Google 帳戶</div>' : ''}
                        </div>
                        <a href="account.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #374151; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#f3f4f6'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-user" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>Account</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘A</span>
                        </a>
                        <a href="billing.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #374151; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#f3f4f6'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-credit-card" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>Billing</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘B</span>
                        </a>
                        <div style="margin: 0.5rem 0; border-top: 1px solid #e5e7eb;"></div>
                        <a href="#" class="user-menu-item logout" onclick="window.VaultCaddyNavbar.logout()" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.5rem; color: #dc2626; text-decoration: none; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#fef2f2'" onmouseout="this.style.backgroundColor='transparent'">
                            <div style="display: flex; align-items: center;">
                                <i class="fas fa-sign-out-alt" style="width: 16px; margin-right: 0.75rem;"></i>
                                <span>${googleUser ? 'Google 登出' : 'Log out'}</span>
                            </div>
                            <span style="font-size: 0.75rem; color: #9ca3af;">⌘Q</span>
                        </a>
                    </div>
                </div>
            `;
        } else {
            return `
                <div class="auth-buttons" style="display: flex; align-items: center; gap: 1rem;">
                    <div id="google-signin-button" class="google-signin-container"></div>
                    <button class="nav-link login-btn traditional" data-translate="nav_login" onclick="window.VaultCaddyNavbar.handleLogin()">
                        登入 →
                    </button>
                </div>
            `;
        }
    }
    
    /**
     * 設置 Google 登入按鈕
     */
    setupGoogleSignInButton() {
        // 檢查是否未登入且 Google Auth 可用
        const isLoggedIn = this.isLoggedIn || (window.googleAuth && window.googleAuth.isLoggedIn());
        
        if (!isLoggedIn && window.googleAuth && window.googleAuth.isInitialized) {
            // 延遲設置 Google 登入按鈕，確保 DOM 已更新
            setTimeout(() => {
                const buttonContainer = document.getElementById('google-signin-button');
                if (buttonContainer) {
                    window.googleAuth.renderSignInButton('google-signin-button');
                    console.log('✅ Google 登入按鈕已設置');
                }
            }, 100);
        } else if (!isLoggedIn && window.googleAuth) {
            // 如果 Google Auth 還未初始化，監聽初始化完成事件
            window.addEventListener('authStateChanged', () => {
                this.setupGoogleSignInButton();
            }, { once: true });
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
            if (e.key === 'vaultcaddy_user' || e.key === 'userLoggedIn' || e.key === 'userCredits' || e.key === 'vaultcaddy_token') {
                console.log('📦 localStorage變化檢測到:', e.key);
                this.loadUserState().then(() => this.render());
            }
        });
        
        // 監聽自定義事件
        window.addEventListener('userStateChanged', () => {
            console.log('🔄 userStateChanged事件檢測到');
            this.loadUserState().then(() => this.render());
        });
        
        // 🔥 監聽 Firebase Auth 狀態變化（最新）
        window.addEventListener('auth-state-changed', (e) => {
            console.log('🔥 Firebase Auth 狀態變化檢測到:', e.detail);
            this.loadUserState().then(() => this.render());
        });
        
        // 監聽auth系統的登入/登出事件（向後兼容）
        window.addEventListener('vaultcaddy:auth:login', (e) => {
            console.log('🔐 登入事件檢測到:', e.detail);
            this.loadUserState().then(() => this.render());
        });
        
        window.addEventListener('vaultcaddy:auth:logout', (e) => {
            console.log('🚪 登出事件檢測到:', e.detail);
            this.loadUserState().then(() => this.render());
        });
        
        window.addEventListener('vaultcaddy:auth:creditsUpdated', (e) => {
            console.log('💰 Credits更新事件檢測到:', e.detail);
            this.loadUserState().then(() => this.render());
        });
    }
    
    /**
     * 處理登入 - 引導用戶到登入頁面
     */
    async handleLogin() {
        try {
            console.log('🔐 引導用戶到登入頁面...');
            
            // 保存當前頁面 URL，登入後可以回到原頁面
            const currentUrl = window.location.href;
            if (!currentUrl.includes('auth.html')) {
                localStorage.setItem('vaultcaddy_redirect_after_login', currentUrl);
            }
            
            // 跳轉到登入頁面
            window.location.href = 'auth.html';
            
        } catch (error) {
            console.error('跳轉到登入頁面失敗:', error);
            alert('無法跳轉到登入頁面，請稍後再試。');
        }
    }
    
    /**
     * 處理登出
     */
    async logout() {
        try {
            console.log('🚪 開始登出流程...');
            
            // 優先使用 Firebase Auth 登出
            if (window.authHandler && window.authHandler.isLoggedIn()) {
                console.log('🔐 使用 Firebase Auth 登出');
                await window.authHandler.logout();
                // authHandler.logout() 會自動重定向到 login.html，所以這裡不需要再處理
                return;
            }
            
            // 如果是舊的 Google 用戶，使用 Google 登出
            if (window.googleAuth && window.googleAuth.isLoggedIn()) {
                console.log('🔐 使用 Google Auth 登出');
                await window.googleAuth.signOut();
            }
            
            // 清理 LocalStorage（向後兼容）
            console.log('🧹 清理 LocalStorage...');
            localStorage.removeItem('vaultcaddy_token');
            localStorage.removeItem('vaultcaddy_user');
            localStorage.removeItem('vaultcaddy_credits');
            localStorage.removeItem('userLoggedIn');
            localStorage.removeItem('userCredits');
            
            // 觸發狀態更新
            window.dispatchEvent(new CustomEvent('userStateChanged'));
            window.dispatchEvent(new CustomEvent('vaultcaddy:auth:logout'));
            
            // 顯示登出成功消息
            this.showNotification('已成功登出', 'success');
            
            // 延遲跳轉讓用戶看到消息
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1000);
            
        } catch (error) {
            console.error('❌ 登出失敗:', error);
            this.showNotification('登出失敗，請稍後再試', 'error');
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
    
    /**
     * 切換語言下拉選單
     */
    toggleLanguageDropdown(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const dropdown = document.getElementById('language-dropdown');
        if (dropdown) {
            // 切換顯示狀態
            if (dropdown.style.display === 'none' || dropdown.style.display === '') {
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        }
        
        // 點擊其他地方關閉選單
        setTimeout(() => {
            document.addEventListener('click', this.closeLanguageDropdown.bind(this), { once: true });
        }, 0);
    }
    
    /**
     * 關閉語言下拉選單
     */
    closeLanguageDropdown() {
        const dropdown = document.getElementById('language-dropdown');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    }
    
    /**
     * 切換語言
     */
    changeLanguage(langCode) {
        console.log('切換語言到:', langCode);
        
        // 更新內部狀態
        this.language = langCode;
        localStorage.setItem('preferred_language', langCode);
        localStorage.setItem('language', langCode); // 兼容 translations.js 中的語言管理器
        
        // 關閉下拉選單
        this.closeLanguageDropdown();
        
        // 重新渲染導航欄以更新語言顯示
        this.render();
        
        // 更新頁面語言 - 使用統一的語言管理器
        if (window.languageManager) {
            window.languageManager.currentLanguage = langCode;
            window.languageManager.loadLanguage(langCode);
        } else {
            // 如果 languageManager 不存在，手動更新翻譯
            this.updatePageTranslations(langCode);
        }
        
        // 強制更新導航欄中的翻譯元素
        setTimeout(() => {
            this.updateNavbarTranslations(langCode);
        }, 100);
        
        // 顯示通知
        this.showNotification(`語言已切換為 ${this.getLanguageName(langCode)}`);
    }
    
    /**
     * 更新導航欄中的翻譯元素
     */
    updateNavbarTranslations(langCode) {
        // 確保 translations 對象存在
        if (typeof translations === 'undefined') {
            console.warn('translations 對象不存在');
            return;
        }
        
        const translation = translations[langCode] || translations['en'];
        
        // 更新導航欄內的翻譯元素
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.querySelectorAll('[data-translate]').forEach(element => {
                const key = element.getAttribute('data-translate');
                if (translation[key]) {
                    if (translation[key].includes('<')) {
                        element.innerHTML = translation[key];
                    } else {
                        element.textContent = translation[key];
                    }
                }
            });
        }
        
        console.log('✅ 導航欄翻譯已更新:', langCode);
    }
    
    /**
     * 手動更新頁面翻譯
     */
    updatePageTranslations(langCode) {
        // 確保 translations 對象存在
        if (typeof translations === 'undefined') {
            console.warn('translations 對象未定義');
            return;
        }
        
        const translation = translations[langCode] || translations['en'];
        
        // 更新所有帶有 data-translate 屬性的元素
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translation[key]) {
                // 檢查是否包含HTML標籤
                if (translation[key].includes('<')) {
                    element.innerHTML = translation[key];
                } else {
                    element.textContent = translation[key];
                }
            }
        });
        
        // 更新 placeholder 屬性
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            if (translation[key]) {
                element.placeholder = translation[key];
            }
        });
        
        // 更新HTML lang屬性
        document.documentElement.lang = langCode;
        
        // 觸發語言變更事件
        window.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { language: langCode, translations: translation } 
        }));
    }
    
    /**
     * 獲取語言名稱
     */
    getLanguageName(code) {
        const languages = {
            'en': 'English',
            'zh-tw': '繁體中文'
        };
        return languages[code] || languages['zh-tw'];
    }
}

// 創建全局實例
window.VaultCaddyNavbar = new VaultCaddyNavbar();


// 測試登入狀態的輔助函數
function checkLoginStatus() {
    const token = localStorage.getItem('vaultcaddy_token');
    const userData = localStorage.getItem('vaultcaddy_user');
    const userLoggedIn = localStorage.getItem('userLoggedIn');
    const navbarStatus = window.VaultCaddyNavbar ? window.VaultCaddyNavbar.isLoggedIn : false;
    
    console.log('🔍 當前登入狀態檢查:', {
        vaultcaddyToken: !!token,
        vaultcaddyUser: !!userData,
        userLoggedIn: userLoggedIn,
        navbarInstance: navbarStatus,
        recommendation: (token && userData) || userLoggedIn === 'true' ? '應該已登入' : '應該未登入'
    });
    
    return (token && userData) || userLoggedIn === 'true';
}


// 導航到特定區塊的函數
function navigateToSection(sectionId) {
    // 如果已經在 index.html，直接滑動
    if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    } else {
        // 如果在其他頁面，跳轉到 index.html 並滑動
        window.location.href = `index.html#${sectionId}`;
    }
}

// 頁面載入完成後初始化（實例創建時已自動初始化，這裡只是確保）
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // 確保 navbar-placeholder 存在後再初始化
        if (document.getElementById('navbar-placeholder')) {
            console.log('🔄 DOMContentLoaded: 重新初始化導航欄');
            window.VaultCaddyNavbar.render();
            
            // 監聽全域身份驗證狀態變化
            initNavbarGlobalAuthListener();
        }
    });
} else {
    // 如果文檔已載入，立即檢查並渲染
    if (document.getElementById('navbar-placeholder')) {
        console.log('🔄 Document Ready: 立即渲染導航欄');
        window.VaultCaddyNavbar.render();
        
        // 監聽全域身份驗證狀態變化
        initNavbarGlobalAuthListener();
    }
}

// 初始化導航欄的全域身份驗證監聽器
function initNavbarGlobalAuthListener() {
    console.log('🔗 初始化導航欄全域身份驗證監聽器');
    
    // 監聽全域身份驗證狀態變化
    if (window.onGlobalAuthChange) {
        window.onGlobalAuthChange((authState) => {
            console.log('🔄 導航欄收到全域身份驗證狀態變化:', authState);
            
            // 重新載入用戶狀態並渲染導航欄
            if (window.VaultCaddyNavbar) {
                window.VaultCaddyNavbar.loadUserState();
                window.VaultCaddyNavbar.render();
                console.log('✅ 導航欄已根據新的身份驗證狀態重新渲染');
            }
        });
    } else {
        // 如果 GlobalAuthSync 尚未載入，延遲重試
        setTimeout(() => {
            if (window.onGlobalAuthChange) {
                console.log('🔗 延遲初始化導航欄監聽器成功');
                initNavbarGlobalAuthListener();
            } else {
                console.log('⚠️ GlobalAuthSync 系統未載入，導航欄將使用本地狀態');
            }
        }, 500);
    }
    
    // 額外監聽自定義事件
    window.addEventListener('vaultcaddy:global:authStateChanged', (event) => {
        console.log('📡 導航欄收到自定義身份驗證事件:', event.detail);
        
        if (window.VaultCaddyNavbar) {
            window.VaultCaddyNavbar.loadUserState();
            window.VaultCaddyNavbar.render();
            console.log('✅ 導航欄已根據自定義事件重新渲染');
        }
    });
}
