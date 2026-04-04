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
        
        // ✅ 防抖動機制 - 減少重複渲染
        this._renderTimeout = null;
        this._lastRenderTime = 0;
        this._renderCount = 0;
        
        this.init();
    }
    
    /**
     * 初始化導航欄
     */
    async init() {
        // 先同步渲染一次，確保佔位符不為空
        this.render();
        
        await this.loadUserState();
        
        // 檢查 DOM 是否準備好
        if (document.getElementById('navbar-placeholder') || document.getElementById('navbar-root')) {
            this.render();
            this.bindEvents();
        } else {
            console.log('⏳ navbar-placeholder 尚未準備好，等待 DOM...');
            // 如果還沒準備好，等一下再試
            setTimeout(() => {
                if (document.getElementById('navbar-placeholder') || document.getElementById('navbar-root')) {
                    console.log('✅ 延遲檢查：navbar-placeholder 已準備好');
                    this.render();
                    this.bindEvents();
                }
            }, 100);
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
            
            // ✅ 簡化：只使用 SimpleAuth
            if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
                const currentUser = window.simpleAuth.getCurrentUser();
                console.log('✅ 導航欄從 SimpleAuth 獲取用戶:', currentUser);
                
                this.isLoggedIn = true;
                this.isAuthenticated = true;
                this.user = {
                    id: currentUser.uid,
                    email: currentUser.email || 'user@vaultcaddy.com',
                    name: currentUser.displayName || currentUser.email?.split('@')[0] || 'User',
                    avatar: currentUser.photoURL || 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png'
                };
                
                // 從 SimpleDataManager 獲取 credits 和 planType
                if (window.simpleDataManager && window.simpleDataManager.initialized) {
                    try {
                        this.credits = await window.simpleDataManager.getUserCredits();
                        console.log('✅ 從 Firestore 獲取 credits:', this.credits);
                        
                        // 🎯 獲取套餐類型
                        const userDoc = await window.simpleDataManager.db.collection('users').doc(currentUser.uid).get();
                        if (userDoc.exists) {
                            const userData = userDoc.data();
                            this.planType = userData.planType || 'Free Plan';
                            console.log('✅ 從 Firestore 獲取 planType:', this.planType);
                        } else {
                            this.planType = 'Free Plan';
                        }
                    } catch (error) {
                        console.error('❌ 獲取用戶數據失敗:', error);
                        this.credits = '10';
                        this.planType = 'Free Plan';
                    }
                } else {
                    this.credits = '10';
                    this.planType = 'Free Plan';
                }
                
                console.log('✅ 用戶已載入:', this.user.email);
            } else {
                // 未登入
                this.resetUserState();
            }
            
            // 載入語言設置（根据URL路径检测）
            const path = window.location.pathname;
            if (path.includes('/en/')) {
                this.language = 'en';
            } else if (path.includes('/ja/')) {
                this.language = 'ja';
            } else if (path.includes('/ko/')) {
                this.language = 'ko';
            } else {
                this.language = localStorage.getItem('preferred_language') || 'zh-tw';
            }
            
            console.log('📊 導航欄用戶狀態已載入:', {
                isLoggedIn: this.isLoggedIn,
                isAuthenticated: this.isAuthenticated,
                credits: this.credits,
                user: this.user?.email || 'N/A',
                source: 'SimpleAuth'
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
     * 渲染導航欄（統一使用靜態導航欄的樣式）
     */
    render() {
        // 支持兩種 ID：navbar-placeholder（舊版）和 navbar-root（新版）
        const navbarPlaceholder = document.getElementById('navbar-placeholder') || document.getElementById('navbar-root');
        if (!navbarPlaceholder) {
            console.error('找不到導航欄占位符 #navbar-placeholder 或 #navbar-root');
            // 如果找不到，試著在 body 最前面插入一個
            if (document.body) {
                console.log('🔄 嘗試自動創建 navbar-placeholder');
                const newPlaceholder = document.createElement('div');
                newPlaceholder.id = 'navbar-placeholder';
                document.body.insertBefore(newPlaceholder, document.body.firstChild);
                // 遞歸調用一次
                setTimeout(() => this.render(), 50);
            }
            return;
        }
        
        console.log('✅ 找到導航欄容器:', navbarPlaceholder.id);
        
        // ✅ 使用與 index.html 靜態導航欄完全一致的樣式
        const navbarHTML = `
            <style>
                /* 手機版導航欄樣式優化 */
                @media (max-width: 768px) {
                    #main-navbar {
                        padding: 0 1rem !important;
                        height: 50px !important;
                        min-height: 50px !important;
                    }
                    .vaultcaddy-navbar {
                        height: 50px !important;
                        min-height: 50px !important;
                    }
                    #main-navbar .desktop-nav-links {
                        display: none !important; /* 手機版隱藏中間的功能/價格/儀表板連結 */
                    }
                    .desktop-only-link {
                        display: none !important; /* 確保隱藏所有桌面專屬連結 */
                    }
                    #main-navbar .mobile-menu-btn {
                        display: block !important; /* 恢復顯示漢堡菜單 */
                    }
                    #mobile-dropdown {
                        display: none !important;
                    }
                    #mobile-dropdown.active {
                        display: flex !important;
                        flex-direction: column !important;
                        top: 50px !important; /* 確保下拉選單在手機版導航欄正下方 */
                        background: white !important; /* 確保背景為白色 */
                    }
                    #main-navbar > div:nth-child(1) .desktop-text {
                        display: none !important; /* 手機版隱藏 VaultCaddy 文字，只留 V logo */
                    }
                    #main-navbar .user-menu-item span {
                        display: none !important; /* 手機版隱藏用戶選單文字 */
                    }
                    #main-navbar .user-menu-item {
                        padding: 0.25rem !important;
                    }
                    #main-navbar .user-menu-item i {
                        font-size: 1.2rem !important;
                    }
                }
                /* 桌面版導航欄樣式優化 */
                @media (min-width: 769px) {
                    #main-navbar .desktop-nav-links {
                        display: none !important; /* 隱藏桌面版中間的功能/價格/儀表板連結 */
                    }
                    /* 確保中間的導航連結在桌面版正確顯示且不重疊 */
                    #main-navbar > div:nth-child(2) {
                        flex: 1;
                        justify-content: flex-end;
                    }
                    #main-navbar .mobile-menu-btn {
                        display: none !important;
                    }
                    #mobile-dropdown {
                        display: none !important;
                    }
                    #mobile-dropdown.active {
                        display: none !important;
                    }
                }
            </style>
            <nav class="vaultcaddy-navbar" id="main-navbar" style="position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; height: 60px; width: 100% !important; background: #ffffff !important; border-bottom: 1px solid #e5e7eb !important; display: flex !important; align-items: center !important; justify-content: space-between !important; padding: 0 2rem !important; z-index: 999999 !important; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; box-sizing: border-box !important; margin: 0 !important; overflow: visible !important;">
                <div style="display: flex !important; align-items: center !important; gap: 0.5rem !important; z-index: 10000 !important; pointer-events: auto !important; visibility: visible !important; opacity: 1 !important;">
                    <a href="index.html" style="display: flex !important; align-items: center !important; gap: 0.75rem !important; text-decoration: none !important; color: #1f2937 !important; font-weight: 600 !important; font-size: 1.125rem !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;">
                        <div style="width: 32px !important; height: 32px !important; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; border-radius: 8px !important; display: flex !important; align-items: center !important; justify-content: center !important; color: white !important; font-weight: 700 !important; font-size: 1.25rem !important; visibility: visible !important; opacity: 1 !important; flex-shrink: 0 !important;">
                            V
                        </div>
                        <div class="desktop-text" style="display: flex !important; flex-direction: column !important; visibility: visible !important; opacity: 1 !important;">
                            <div style="color: #1f2937 !important; display: block !important; visibility: visible !important; opacity: 1 !important; font-size: 1.125rem !important; font-weight: 600 !important; line-height: 1.2 !important;">VaultCaddy</div>
                            <div style="font-size: 0.75rem !important; color: #6b7280 !important; font-weight: 400 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; display: block !important; visibility: visible !important; opacity: 1 !important; line-height: 1.2 !important;">AI DOCUMENT PROCESSING</div>
                        </div>
                    </a>
                </div>
                <div style="display: flex !important; align-items: center !important; gap: 1rem !important; z-index: 10000 !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; height: 100% !important; justify-content: flex-end !important; flex: 1 !important;">
                    <div class="desktop-nav-links" style="display: none !important;">
                    </div>
                    <!-- Hamburger Menu for Mobile -->
                    <div class="mobile-menu-btn" style="cursor: pointer; padding: 0.5rem; z-index: 10001;" onclick="const dropdown = document.getElementById('mobile-dropdown'); if(dropdown) { dropdown.classList.toggle('active'); if(dropdown.classList.contains('active')) { dropdown.style.setProperty('display', 'flex', 'important'); } else { dropdown.style.setProperty('display', 'none', 'important'); } }">
                        <i class="fas fa-bars" style="font-size: 1.25rem; color: #4b5563;"></i>
                    </div>
                    
                    <div style="display: flex !important; align-items: center !important; height: 100% !important; z-index: 10000 !important; visibility: visible !important; opacity: 1 !important;">
                        ${this.getUserSection()}
                    </div>
                </div>
                <!-- Mobile Dropdown Menu -->
                <div id="mobile-dropdown" style="display: none !important; position: absolute; top: 50px; left: 0; right: 0; background: white !important; border-bottom: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 1rem; flex-direction: column; gap: 1rem; z-index: 99999;">
                </div>
            </nav>
        `;
        
        // 更新導航欄內容
        // 為了確保不覆蓋靜態導航欄，我們將動態導航欄附加到容器中
        const existingMainNavbar = navbarPlaceholder.querySelector('#main-navbar');
        if (existingMainNavbar) {
            existingMainNavbar.remove();
        }
        
        // 隱藏靜態導航欄（如果存在）
        const staticNavbar = navbarPlaceholder.querySelector('nav:not(#main-navbar)');
        if (staticNavbar) {
            staticNavbar.style.setProperty('display', 'none', 'important');
            staticNavbar.remove(); // 直接移除靜態導航欄
        }
        
        // 確保所有靜態導航欄都被移除
        const allStaticNavs = document.querySelectorAll('.vaultcaddy-navbar:not(#main-navbar)');
        allStaticNavs.forEach(nav => {
            nav.style.setProperty('display', 'none', 'important');
            nav.remove();
        });
        if (existingMainNavbar) {
            existingMainNavbar.remove();
        }
        
        // 隱藏所有現有的靜態導航欄
        const staticNavs = navbarPlaceholder.querySelectorAll('nav:not(#main-navbar)');
        staticNavs.forEach(nav => {
            nav.style.setProperty('display', 'none', 'important');
            nav.style.setProperty('opacity', '0', 'important');
            nav.style.setProperty('visibility', 'hidden', 'important');
            nav.style.setProperty('z-index', '-1', 'important');
            nav.remove(); // 確保移除
        });
        // 清除可能殘留的文本節點或其他元素
        navbarPlaceholder.innerHTML = navbarHTML;
        console.log('✅ 導航欄 HTML 已插入，長度:', navbarHTML.length);
        
        // 強制移除可能隱藏導航欄的類或樣式
        navbarPlaceholder.classList.remove('hidden', 'invisible');
        
        // 確保導航欄可見
        navbarPlaceholder.style.cssText = 'display: block !important; visibility: visible !important; opacity: 1 !important; width: 100% !important; position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; z-index: 999999 !important; background: #ffffff !important; margin: 0 !important; padding: 0 !important; min-height: 60px;';
        
        // 確保內部 nav 也可見
        let innerNav = navbarPlaceholder.querySelector('nav#main-navbar');
        
        // 如果沒有找到 innerNav，這意味著插入失敗，我們需要重新插入
        if (!innerNav) {
            console.error('❌ 導航欄插入失敗，嘗試重新插入');
            navbarPlaceholder.insertAdjacentHTML('beforeend', navbarHTML);
            innerNav = navbarPlaceholder.querySelector('nav#main-navbar');
        }
        
        if (innerNav) {
            innerNav.style.cssText = 'position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; height: 60px; width: 100% !important; background: #ffffff !important; border-bottom: 1px solid #e5e7eb !important; display: flex !important; align-items: center !important; justify-content: space-between !important; padding: 0 2rem !important; z-index: 999999 !important; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; box-sizing: border-box !important; margin: 0 !important;';
            
            // 移除任何可能覆蓋樣式的 inline style
            innerNav.style.setProperty('display', 'flex', 'important');
            innerNav.style.setProperty('visibility', 'visible', 'important');
            innerNav.style.setProperty('opacity', '1', 'important');
            
            // 強制顯示所有子元素 (只針對 main-navbar 內的元素)
            const allChildren = innerNav.querySelectorAll('*');
            allChildren.forEach(child => {
                if (child.id !== 'user-dropdown-menu' && !child.closest('#user-dropdown-menu')) {
                    // 避免覆蓋由 CSS 媒體查詢控制的元素的 display 屬性
                    const isResponsiveElement = child.classList.contains('desktop-only-link') || 
                                                child.classList.contains('desktop-text') || 
                                                child.classList.contains('desktop-nav-links') ||
                                                child.classList.contains('mobile-menu-btn');
                                                
                    child.classList.remove('hidden', 'invisible');
                    
                    if (!isResponsiveElement) {
                        // 確保標籤正確顯示
                        if (child.tagName === 'A') {
                            child.style.setProperty('display', 'inline-flex', 'important');
                            child.style.setProperty('align-items', 'center', 'important');
                        } else if (child.tagName === 'DIV') {
                            child.style.setProperty('display', 'flex', 'important');
                            child.style.setProperty('align-items', 'center', 'important');
                        } else if (child.tagName === 'SPAN') {
                            child.style.setProperty('display', 'inline-block', 'important');
                        } else {
                            child.style.setProperty('display', 'block', 'important');
                        }
                    }
                    
                    child.style.setProperty('visibility', 'visible', 'important');
                    child.style.setProperty('opacity', '1', 'important');
                    
                    // 確保文字顏色正確
                    if (!child.style.color && !child.classList.contains('user-avatar') && !child.closest('#user-menu')) {
                        child.style.setProperty('color', '#1f2937', 'important');
                    }
                }
            });
        }
        
        // 強制檢查 user-menu 內的元素
        const userMenu = navbarPlaceholder.querySelector('#main-navbar #user-menu');
        if (userMenu) {
            userMenu.style.setProperty('display', 'flex', 'important');
            userMenu.style.setProperty('visibility', 'visible', 'important');
            userMenu.style.setProperty('opacity', '1', 'important');
            
            const loginBtn = userMenu.querySelector('a');
            if (loginBtn) {
                loginBtn.style.setProperty('display', 'inline-flex', 'important');
                loginBtn.style.setProperty('visibility', 'visible', 'important');
                loginBtn.style.setProperty('opacity', '1', 'important');
                loginBtn.style.setProperty('color', 'white', 'important');
                loginBtn.style.setProperty('background', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'important');
            }
        }
        
        // 確保整個導航欄不會被隱藏
        if (innerNav) {
            innerNav.classList.remove('hidden', 'invisible');
            innerNav.style.setProperty('display', 'flex', 'important');
        }
        
        // 重新綁定事件
        this.bindEvents();
        
        // 設置 Google 登入按鈕（如果用戶未登入）
        this.setupGoogleSignInButton();
        
        // 確保預設靜態導航欄被隱藏（如果存在）
        const extraStaticNavs = navbarPlaceholder.querySelectorAll('nav:not(#main-navbar)');
        extraStaticNavs.forEach(nav => {
            nav.style.setProperty('display', 'none', 'important');
            nav.style.setProperty('opacity', '0', 'important');
            nav.style.setProperty('visibility', 'hidden', 'important');
            nav.style.setProperty('z-index', '-1', 'important');
            nav.remove(); // 直接移除靜態導航欄
        });
        
        // 確保靜態下拉選單被隱藏
        const staticDropdowns = document.querySelectorAll('#mobile-dropdown-static');
        staticDropdowns.forEach(dropdown => {
            dropdown.style.setProperty('display', 'none', 'important');
            dropdown.remove();
        });
        
        const staticDropdown2 = document.getElementById('mobile-dropdown');
        if (staticDropdown2 && !staticDropdown2.closest('#main-navbar')) {
            staticDropdown2.style.setProperty('display', 'none', 'important');
            staticDropdown2.remove();
        }
        
        // 確保靜態漢堡菜單按鈕被隱藏
        const staticMobileMenuBtns1 = document.querySelectorAll('.mobile-menu-btn');
        staticMobileMenuBtns1.forEach(btn => {
            if (!btn.closest('#main-navbar')) {
                btn.style.setProperty('display', 'none', 'important');
                btn.remove();
            }
        });
        
        // 確保靜態 desktop-links 被隱藏
        const staticDesktopLinks = document.querySelectorAll('.desktop-links');
        staticDesktopLinks.forEach(links => {
            if (!links.closest('#main-navbar')) {
                links.style.setProperty('display', 'none', 'important');
                links.remove();
            }
        });
        
        // 確保靜態 .desktop-nav-links 被隱藏
        const staticDesktopNavLinks = document.querySelectorAll('.desktop-nav-links');
        staticDesktopNavLinks.forEach(links => {
            if (!links.closest('#main-navbar')) {
                links.style.setProperty('display', 'none', 'important');
                links.remove();
            }
        });
        
        // 確保 main-navbar 的漢堡菜單按鈕在手機版顯示
        const mainMobileMenuBtn = document.querySelector('#main-navbar .mobile-menu-btn');
        if (mainMobileMenuBtn) {
            if (window.innerWidth <= 768) {
                mainMobileMenuBtn.style.setProperty('display', 'block', 'important');
            } else {
                mainMobileMenuBtn.style.setProperty('display', 'none', 'important');
            }
            
            // 監聽視窗大小改變
            window.addEventListener('resize', () => {
                if (window.innerWidth <= 768) {
                    mainMobileMenuBtn.style.setProperty('display', 'block', 'important');
                } else {
                    mainMobileMenuBtn.style.setProperty('display', 'none', 'important');
                    // 桌面版自動關閉下拉選單
                    const dropdown = document.getElementById('mobile-dropdown');
                    if (dropdown) {
                        dropdown.classList.remove('active');
                        dropdown.style.setProperty('display', 'none', 'important');
                    }
                }
            });
        }
        
        // 確保靜態漢堡菜單按鈕被隱藏
        const staticMobileMenuBtns2 = document.querySelectorAll('.mobile-menu-btn:not(#main-navbar .mobile-menu-btn)');
        staticMobileMenuBtns2.forEach(btn => {
            btn.style.setProperty('display', 'none', 'important');
            btn.remove();
        });
        
        // 確保動態下拉選單預設隱藏
        const dynamicDropdown = document.getElementById('mobile-dropdown');
        if (dynamicDropdown) {
            dynamicDropdown.classList.remove('active');
            dynamicDropdown.style.setProperty('display', 'none', 'important');
        }
        
        // 確保 main-navbar 顯示
        const mainNav = navbarPlaceholder.querySelector('#main-navbar');
        if (mainNav) {
            mainNav.style.setProperty('display', 'flex', 'important');
            mainNav.style.setProperty('opacity', '1', 'important');
            mainNav.style.setProperty('visibility', 'visible', 'important');
            mainNav.style.setProperty('z-index', '999999', 'important');
        }
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
            <a href="index.html#features" class="nav-link desktop-only-link" data-translate="nav_features" onclick="navigateToSection('features')">功能</a>
            <a href="index.html#pricing" class="nav-link desktop-only-link" data-translate="nav_pricing" onclick="navigateToSection('pricing')">價格</a>
        `;
        
        // Dashboard 按鈕 - 前往Team Project視圖
        navigation += `
            <a href="dashboard.html" class="nav-link desktop-only-link" data-translate="nav_dashboard">儀表板</a>
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
            <div class="language-selector" style="display: none !important;">
                <button class="language-btn" onclick="window.vaultcaddyNavbar.toggleLanguageDropdown(event)" style="
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
                        <button class="language-option" onclick="window.vaultcaddyNavbar.changeLanguage('${code}')" style="
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
        // 🔥 優先檢查 Firebase Auth（最新）
        // 多语言文本映射
        const t = {
            'zh-tw': { firebaseAccount: 'Firebase 帳戶', googleAccount: 'Google 帳戶', account: '帳戶', billing: '計費', logout: '登出', login: '登入 →' },
            'en': { firebaseAccount: 'Firebase Account', googleAccount: 'Google Account', account: 'Account', billing: 'Billing', logout: 'Logout', login: 'Login →' },
            'ja': { firebaseAccount: 'Firebase アカウント', googleAccount: 'Google アカウント', account: 'アカウント', billing: '請求', logout: 'ログアウト', login: 'ログイン →' },
            'ko': { firebaseAccount: 'Firebase 계정', googleAccount: 'Google 계정', account: '계정', billing: '결제', logout: '로그아웃', login: '로그인 →' }
        };
        const lang = t[this.language] || t['zh-tw'];
        
        let currentUser = null;
        let userCredits = 0;
        let userPhotoURL = 'https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png';
        let userName = 'User';
        let userEmail = '';
        let userPlanType = 'Free Plan';  // 🎯 新增套餐類型
        let isFirebaseUser = false;
        let isGoogleUser = false;
        
        if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
            const firebaseUser = window.simpleAuth.getCurrentUser();
            if (firebaseUser) {
                currentUser = firebaseUser;
                userPhotoURL = firebaseUser.photoURL || userPhotoURL;
                userName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || 'User';
                userEmail = firebaseUser.email || '';
                userCredits = this.credits || 0;
                userPlanType = this.planType || 'Free Plan';
                isFirebaseUser = true;
                console.log('🔥 導航欄顯示 SimpleAuth 用戶:', userEmail);
            }
        }
        
        // 向後兼容：檢查 Google 認證狀態
        if (!currentUser) {
            const isGoogleLoggedIn = window.googleAuth && window.googleAuth.isLoggedIn();
            const googleUser = isGoogleLoggedIn ? window.googleAuth.getCurrentUser() : null;
            
            if (googleUser) {
                currentUser = googleUser;
                userPhotoURL = googleUser.photoURL || userPhotoURL;
                userName = googleUser.displayName || 'User';
                userEmail = googleUser.email || '';
                userCredits = window.googleAuth.getUserDataManager().getUserData()?.credits || 0;
                isGoogleUser = true;
                console.log('🌐 導航欄顯示 Google Auth 用戶:', userEmail);
            }
        }
        
        // 向後兼容：使用原有認證
        if (!currentUser && this.isLoggedIn && this.user) {
            currentUser = this.user;
            userPhotoURL = this.user.avatar || userPhotoURL;
            userName = this.user.name || 'User';
            userEmail = this.user.email || '';
            userCredits = this.credits || 0;
            console.log('📦 導航欄顯示 LocalStorage 用戶:', userEmail);
        }
        
        if (currentUser) {
            
            return `
                <div class="user-profile" id="user-profile" style="position: relative; display: flex !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; align-items: center !important; height: 100% !important; z-index: 10000 !important;">
                    <img src="${userPhotoURL}" alt="${userName}" class="user-avatar" onclick="window.vaultcaddyNavbar.toggleUserDropdown(event)" style="cursor: pointer; border-radius: 50%; width: 32px; height: 32px; object-fit: cover; border: 2px solid #e5e7eb; transition: border-color 0.2s; display: block !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; z-index: 10000 !important;" onmouseover="this.style.borderColor='#667eea'" onmouseout="this.style.borderColor='#e5e7eb'">
                    <div class="user-dropdown-menu" id="user-dropdown-menu" style="display: none !important; position: absolute !important; top: 100% !important; right: -10px !important; background: white !important; border: 1px solid #e5e7eb !important; border-radius: 12px !important; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15) !important; min-width: 280px !important; z-index: 1000000 !important; padding: 0 !important; margin-top: 8px !important; overflow: hidden !important; max-width: calc(100vw - 2rem) !important;">
                        <!-- 用戶信息區 -->
                        <div class="user-info" style="padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                                <img src="${userPhotoURL}" alt="${userName}" style="width: 48px; height: 48px; border-radius: 50%; border: 3px solid rgba(255,255,255,0.3); object-fit: cover;">
                                <div style="flex: 1; min-width: 0;">
                                    <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${userName}</div>
                                    <div style="font-size: 0.75rem; opacity: 0.9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${userEmail}</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background: rgba(255,255,255,0.15); border-radius: 8px; backdrop-filter: blur(10px);">
                                <div>
                                    <div style="font-size: 0.75rem; opacity: 0.9; margin-bottom: 0.25rem;">Credits</div>
                                    <div style="font-size: 1.25rem; font-weight: 700;">${userCredits}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 0.75rem; opacity: 0.9; margin-bottom: 0.25rem;">套餐</div>
                                    <div style="font-size: 0.875rem; font-weight: 600; background: rgba(255,255,255,0.25); padding: 0.25rem 0.75rem; border-radius: 12px;">${userPlanType}</div>
                                </div>
                            </div>
                        </div>
                        <!-- 菜單項目 -->
                        <div style="padding: 0.5rem;">
                            <a href="account.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: all 0.2s ease; font-weight: 500;" onmouseover="this.style.backgroundColor='#f3f4f6'; this.style.transform='translateX(4px)'" onmouseout="this.style.backgroundColor='transparent'; this.style.transform='translateX(0)'">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <div style="width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px;">
                                        <i class="fas fa-user" style="color: white; font-size: 0.875rem;"></i>
                                    </div>
                                    <span>${lang.account}</span>
                                </div>
                                <span style="font-size: 0.75rem; color: #9ca3af;">⌘A</span>
                            </a>
                            <a href="billing.html" class="user-menu-item" style="display: flex; align-items: center; justify-content: space-between; padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: all 0.2s ease; font-weight: 500;" onmouseover="this.style.backgroundColor='#f3f4f6'; this.style.transform='translateX(4px)'" onmouseout="this.style.backgroundColor='transparent'; this.style.transform='translateX(0)'">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <div style="width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 8px;">
                                        <i class="fas fa-credit-card" style="color: white; font-size: 0.875rem;"></i>
                                    </div>
                                    <span>${lang.billing}</span>
                                </div>
                                <span style="font-size: 0.75rem; color: #9ca3af;">⌘B</span>
                            </a>
                        </div>
                        <!-- 登出按鈕 -->
                        <div style="padding: 0.5rem; border-top: 1px solid #e5e7eb;">
                            <a href="#" class="user-menu-item logout" onclick="window.vaultcaddyNavbar.logout()" style="display: flex; align-items: center; justify-content: space-between; padding: 0.875rem 1rem; color: #dc2626; text-decoration: none; border-radius: 8px; transition: all 0.2s ease; font-weight: 500;" onmouseover="this.style.backgroundColor='#fef2f2'; this.style.transform='translateX(4px)'" onmouseout="this.style.backgroundColor='transparent'; this.style.transform='translateX(0)'">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <div style="width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: #fef2f2; border-radius: 8px;">
                                        <i class="fas fa-sign-out-alt" style="color: #dc2626; font-size: 0.875rem;"></i>
                                    </div>
                                    <span>${lang.logout}</span>
                                </div>
                                <span style="font-size: 0.75rem; color: #9ca3af;">⌘Q</span>
                            </a>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // ✅ 未登入：顯示「登入 →」按鈕（與圖1靜態導航欄樣式一致）
            return `
                <div id="user-menu" style="position: relative; display: flex !important; align-items: center !important; gap: 0.75rem !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;">
                    <a href="auth.html" style="display: inline-flex !important; align-items: center !important; gap: 0.5rem !important; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; padding: 0.5rem 1rem !important; border-radius: 8px !important; text-decoration: none !important; font-weight: 500 !important; font-size: 0.875rem !important; transition: transform 0.2s, box-shadow 0.2s !important; visibility: visible !important; opacity: 1 !important; pointer-events: auto !important; white-space: nowrap !important;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                        ${lang.login}
                    </a>
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
                userDropdown.style.setProperty('display', 'none', 'important');
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
        
        // ✅ 監聽用戶資料加載完成事件
        window.addEventListener('user-profile-loaded', (e) => {
            console.log('📊 用戶資料加載完成，更新導航欄:', e.detail);
            this.loadUserState().then(() => this.render());
        });
        
        // ✅ 監聽用戶資料更新事件
        window.addEventListener('user-profile-updated', (e) => {
            console.log('🔄 用戶資料已更新，刷新導航欄:', e.detail);
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
            
            // 使用 SimpleAuth 登出
            if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
                console.log('🔐 使用 SimpleAuth 登出');
                await window.simpleAuth.logout();
            }
            
            // 使用 Firebase Auth 登出
            if (window.firebase && window.firebase.auth) {
                console.log('🔐 使用 Firebase Auth 登出');
                await window.firebase.auth().signOut();
            }
            
            // 清理 LocalStorage
            console.log('🧹 清理 LocalStorage...');
            localStorage.removeItem('vaultcaddy_token');
            localStorage.removeItem('vaultcaddy_user');
            localStorage.removeItem('vaultcaddy_credits');
            localStorage.removeItem('userLoggedIn');
            localStorage.removeItem('userCredits');
            
            // 重置用戶狀態
            this.resetUserState();
            
            // 觸發狀態更新事件
            window.dispatchEvent(new CustomEvent('userStateChanged'));
            window.dispatchEvent(new CustomEvent('vaultcaddy:auth:logout'));
            
            // 顯示登出成功消息
            this.showNotification('已成功登出', 'success');
            
            // 延遲跳轉讓用戶看到消息
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
            
            console.log('✅ 登出完成，即將跳轉到首頁');
            
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
            userDropdown.style.setProperty('display', 'none', 'important');
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
            const currentDisplay = window.getComputedStyle(menu).getPropertyValue('display');
            if (currentDisplay === 'none' || menu.style.getPropertyValue('display') === 'none') {
                menu.style.setProperty('display', 'block', 'important');
            } else {
                menu.style.setProperty('display', 'none', 'important');
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
    async updateCredits(newCredits) {
        this.credits = newCredits;
        
        // ✅ 保存到 Firebase（移除 LocalStorage）
        if (window.simpleDataManager && window.simpleDataManager.initialized) {
            try {
                await window.simpleDataManager.updateUserCredits(newCredits);
                console.log('✅ Credits 已保存到 Firebase:', newCredits);
            } catch (error) {
                console.error('❌ 保存 Credits 到 Firebase 失敗:', error);
            }
        }
        
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
        
        // ✅ 使用新的 LanguageManager
        const normalizedLangCode = langCode === 'zh-tw' ? 'zh' : langCode;
        
        if (window.languageManager) {
            console.log('✅ 使用 LanguageManager 切換語言');
            window.languageManager.setLanguage(normalizedLangCode);
        } else {
            console.warn('⚠️ LanguageManager 未載入，手動更新翻譯');
            this.updatePageTranslations(langCode);
        }
        
        // 強制更新導航欄中的翻譯元素
        setTimeout(() => {
            this.updateNavbarTranslations(langCode);
        }, 100);
        
        // 顯示通知
        const langName = this.getLanguageName(langCode);
        this.showNotification(
            normalizedLangCode === 'zh' ? `語言已切換為 ${langName}` : `Language changed to ${langName}`
        );
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
function initNavbar() {
    console.log('🎨 開始初始化 VaultCaddy Navbar... [VERSION: 20260329.52]');
    
    // 不再等待 SimpleAuth，直接創建並渲染導航欄（未登入狀態）
    // 當 SimpleAuth 初始化完成並觸發狀態變化時，導航欄會自動更新
    if (!window.vaultcaddyNavbar) {
        console.log('✅ 創建 navbar 實例');
        window.vaultcaddyNavbar = new VaultCaddyNavbar();
        // 強制立即渲染一次
        window.vaultcaddyNavbar.render();
    } else {
        console.log('✅ navbar 實例已存在，強制重新渲染');
        window.vaultcaddyNavbar.render();
    }
}

// 在 DOM 加載完成後初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNavbar);
} else {
    // 立即執行，不要延遲
    initNavbar();
}


// ✅ 簡化：直接使用 SimpleAuth
function checkLoginStatus() {
    return window.simpleAuth && window.simpleAuth.isLoggedIn();
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
        if (document.getElementById('navbar-placeholder') || document.getElementById('navbar-root')) {
            console.log('🔄 DOMContentLoaded: 重新初始化導航欄');
            if (window.vaultcaddyNavbar && window.vaultcaddyNavbar.render) {
                window.vaultcaddyNavbar.render();
            }
            
            // 監聽全域身份驗證狀態變化
            initNavbarGlobalAuthListener();
        }
    });
} else {
    // 如果文檔已載入，延遲一下確保 DOM 真的準備好了
    setTimeout(() => {
        if (document.getElementById('navbar-placeholder') || document.getElementById('navbar-root')) {
            console.log('🔄 Document Ready: 立即渲染導航欄');
            if (window.vaultcaddyNavbar && window.vaultcaddyNavbar.render) {
                window.vaultcaddyNavbar.render();
            }
            
            // 監聽全域身份驗證狀態變化
            initNavbarGlobalAuthListener();
        }
    }, 50);
}

// 初始化導航欄的全域身份驗證監聽器
function initNavbarGlobalAuthListener() {
    console.log('🔗 初始化導航欄全域身份驗證監聽器');
    
    // 監聽全域身份驗證狀態變化
    if (window.onGlobalAuthChange) {
        window.onGlobalAuthChange((authState) => {
            console.log('🔄 導航欄收到全域身份驗證狀態變化:', authState);
            
            // 重新載入用戶狀態並渲染導航欄
            if (window.vaultcaddyNavbar) {
                window.vaultcaddyNavbar.loadUserState().then(() => {
                    window.vaultcaddyNavbar.render();
                    console.log('✅ 導航欄已根據新的身份驗證狀態重新渲染');
                });
            }
        });
    }
    // ✅ GlobalAuthSync 已刪除，只使用 SimpleAuth
    
    // 額外監聽自定義事件
    window.addEventListener('vaultcaddy:global:authStateChanged', (event) => {
        console.log('📡 導航欄收到自定義身份驗證事件:', event.detail);
        
        if (window.vaultcaddyNavbar) {
            window.vaultcaddyNavbar.loadUserState().then(() => {
                window.vaultcaddyNavbar.render();
                console.log('✅ 導航欄已根據自定義事件重新渲染');
            });
        }
    });
    
    // 監聽 auth-state-changed 事件（由 simple-auth.js 觸發）
    window.addEventListener('auth-state-changed', (event) => {
        console.log('📡 導航欄收到 auth-state-changed 事件:', event.detail);
        if (window.vaultcaddyNavbar) {
            window.vaultcaddyNavbar.loadUserState().then(() => {
                window.vaultcaddyNavbar.render();
            });
        }
    });
}
