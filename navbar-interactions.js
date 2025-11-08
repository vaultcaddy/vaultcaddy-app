/**
 * 統一導航欄交互功能
 * 作用：處理語言切換下拉菜單和用戶菜單的顯示與交互
 * 幫助：為所有頁面提供一致的導航欄行為
 */

(function() {
    'use strict';
    
    console.log('🎯 初始化導航欄交互功能...');
    
    // 等待 DOM 加載完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavbar);
    } else {
        initNavbar();
    }
    
    function initNavbar() {
        initLanguageDropdown();
        initUserMenu();
        initUserAvatar();
    }
    
    /**
     * 初始化語言切換下拉菜單
     */
    function initLanguageDropdown() {
        const languageDropdown = document.getElementById('language-dropdown');
        if (!languageDropdown) {
            console.warn('⚠️ 找不到語言下拉菜單元素');
            return;
        }
        
        // 創建下拉菜單
        const dropdownMenu = document.createElement('div');
        dropdownMenu.id = 'language-menu';
        dropdownMenu.style.cssText = `
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 0.5rem;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            min-width: 150px;
            display: none;
            z-index: 1001;
        `;
        
        dropdownMenu.innerHTML = `
            <div style="padding: 0.5rem;">
                <div class="language-option" data-lang="zh-TW" style="padding: 0.5rem 1rem; cursor: pointer; border-radius: 6px; transition: background 0.2s; display: flex; align-items: center; justify-content: space-between;">
                    <span>繁體中文</span>
                    <i class="fas fa-check" style="color: #667eea; display: block;"></i>
                </div>
                <div class="language-option" data-lang="en" style="padding: 0.5rem 1rem; cursor: pointer; border-radius: 6px; transition: background 0.2s; display: flex; align-items: center; justify-content: space-between;">
                    <span>English</span>
                    <i class="fas fa-check" style="color: #667eea; display: none;"></i>
                </div>
            </div>
        `;
        
        languageDropdown.appendChild(dropdownMenu);
        
        // 點擊語言下拉按鈕
        languageDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = document.getElementById('language-menu');
            const userMenuEl = document.getElementById('user-menu-dropdown');
            
            // 關閉用戶菜單
            if (userMenuEl) {
                userMenuEl.style.display = 'none';
            }
            
            // 切換語言菜單
            if (menu.style.display === 'none' || menu.style.display === '') {
                menu.style.display = 'block';
            } else {
                menu.style.display = 'none';
            }
        });
        
        // 選擇語言
        const languageOptions = dropdownMenu.querySelectorAll('.language-option');
        languageOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.stopPropagation();
                const lang = this.getAttribute('data-lang');
                const langText = this.querySelector('span').textContent;
                
                // 更新顯示
                document.getElementById('current-language').textContent = langText;
                
                // 更新勾選標記
                languageOptions.forEach(opt => {
                    opt.querySelector('.fa-check').style.display = 'none';
                });
                this.querySelector('.fa-check').style.display = 'block';
                
                // 關閉菜單
                dropdownMenu.style.display = 'none';
                
                // 保存語言設置
                localStorage.setItem('preferredLanguage', lang);
                
                console.log('✅ 語言已切換:', langText);
            });
            
            // Hover 效果
            option.addEventListener('mouseenter', function() {
                this.style.background = '#f3f4f6';
            });
            option.addEventListener('mouseleave', function() {
                this.style.background = 'transparent';
            });
        });
        
        // 從 localStorage 載入語言設置
        const savedLang = localStorage.getItem('preferredLanguage');
        if (savedLang) {
            const option = dropdownMenu.querySelector(`[data-lang="${savedLang}"]`);
            if (option) {
                option.click();
            }
        }
        
        console.log('✅ 語言下拉菜單已初始化');
    }
    
    /**
     * 初始化用戶菜單
     */
    function initUserMenu() {
        const userMenu = document.getElementById('user-menu');
        if (!userMenu) {
            console.warn('⚠️ 找不到用戶菜單元素');
            return;
        }
        
        // 創建用戶下拉菜單
        const dropdownMenu = document.createElement('div');
        dropdownMenu.id = 'user-menu-dropdown';
        dropdownMenu.style.cssText = `
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 0.5rem;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            min-width: 220px;
            display: none;
            z-index: 1001;
        `;
        
        dropdownMenu.innerHTML = `
            <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb;">
                <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">Credits: <span id="user-credits">--</span></div>
                <div id="user-email" style="font-size: 0.875rem; color: #6b7280;">載入中...</div>
                <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.25rem; color: #667eea; font-size: 0.875rem;">
                    <i class="fas fa-shield-alt"></i>
                    <span>Firebase 帳戶</span>
                </div>
            </div>
            <div style="padding: 0.5rem;">
                <a href="account.html" class="user-menu-item" style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; cursor: pointer; border-radius: 6px; transition: background 0.2s; text-decoration: none; color: #1f2937;">
                    <i class="fas fa-user" style="width: 16px; color: #6b7280;"></i>
                    <span>Account</span>
                    <span style="margin-left: auto; color: #9ca3af; font-size: 0.875rem;">⌘A</span>
                </a>
                <a href="billing.html" class="user-menu-item" style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; cursor: pointer; border-radius: 6px; transition: background 0.2s; text-decoration: none; color: #1f2937;">
                    <i class="fas fa-credit-card" style="width: 16px; color: #6b7280;"></i>
                    <span>Billing</span>
                    <span style="margin-left: auto; color: #9ca3af; font-size: 0.875rem;">⌘B</span>
                </a>
            </div>
            <div style="padding: 0.5rem; border-top: 1px solid #e5e7eb;">
                <div id="logout-btn" class="user-menu-item" style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; cursor: pointer; border-radius: 6px; transition: background 0.2s; color: #dc2626;">
                    <i class="fas fa-sign-out-alt" style="width: 16px;"></i>
                    <span>Log out</span>
                    <span style="margin-left: auto; color: #9ca3af; font-size: 0.875rem;">⌘Q</span>
                </div>
            </div>
        `;
        
        userMenu.appendChild(dropdownMenu);
        
        // 點擊用戶菜單按鈕
        userMenu.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = document.getElementById('user-menu-dropdown');
            const langMenu = document.getElementById('language-menu');
            
            // 關閉語言菜單
            if (langMenu) {
                langMenu.style.display = 'none';
            }
            
            // 切換用戶菜單
            if (menu.style.display === 'none' || menu.style.display === '') {
                menu.style.display = 'block';
                loadUserInfo();
            } else {
                menu.style.display = 'none';
            }
        });
        
        // Hover 效果
        const menuItems = dropdownMenu.querySelectorAll('.user-menu-item');
        menuItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.background = '#f3f4f6';
            });
            item.addEventListener('mouseleave', function() {
                this.style.background = 'transparent';
            });
        });
        
        // 登出按鈕
        const logoutBtn = dropdownMenu.querySelector('#logout-btn');
        logoutBtn.addEventListener('click', async function() {
            try {
                if (window.simpleAuth && typeof window.simpleAuth.logout === 'function') {
                    await window.simpleAuth.logout();
                } else if (window.firebase && window.firebase.auth) {
                    await window.firebase.auth().signOut();
                }
                window.location.href = 'index.html';
            } catch (error) {
                console.error('❌ 登出失敗:', error);
                alert('登出失敗，請重試');
            }
        });
        
        console.log('✅ 用戶菜單已初始化');
    }
    
    /**
     * 載入用戶信息
     */
    async function loadUserInfo() {
        try {
            let user = null;
            let credits = '--';
            
            // 嘗試從 simpleAuth 獲取用戶信息
            if (window.simpleAuth && window.simpleAuth.currentUser) {
                user = window.simpleAuth.currentUser;
            } else if (window.firebase && window.firebase.auth) {
                user = window.firebase.auth().currentUser;
            }
            
            if (user) {
                // 更新郵箱
                const emailEl = document.getElementById('user-email');
                if (emailEl) {
                    emailEl.textContent = user.email || '未設置郵箱';
                }
                
                // 嘗試獲取 credits
                if (window.simpleDataManager && typeof window.simpleDataManager.getUserCredits === 'function') {
                    credits = await window.simpleDataManager.getUserCredits();
                }
                
                // 更新 credits
                const creditsEl = document.getElementById('user-credits');
                if (creditsEl) {
                    creditsEl.textContent = credits;
                }
            }
        } catch (error) {
            console.error('❌ 載入用戶信息失敗:', error);
        }
    }
    
    /**
     * 初始化用戶頭像
     * 從 account.html 頁面同步頭像
     */
    function initUserAvatar() {
        const avatarEl = document.getElementById('user-avatar');
        if (!avatarEl) {
            console.warn('⚠️ 找不到用戶頭像元素');
            return;
        }
        
        // 從 localStorage 載入頭像
        const savedAvatar = localStorage.getItem('userAvatar');
        if (savedAvatar) {
            // 如果是圖片 URL
            if (savedAvatar.startsWith('http') || savedAvatar.startsWith('data:')) {
                avatarEl.style.backgroundImage = `url(${savedAvatar})`;
                avatarEl.style.backgroundSize = 'cover';
                avatarEl.style.backgroundPosition = 'center';
                avatarEl.textContent = '';
            } else {
                // 如果是文字（首字母）
                avatarEl.textContent = savedAvatar;
            }
        } else {
            // 嘗試從用戶郵箱獲取首字母
            updateAvatarFromUser();
        }
        
        // 監聽 storage 事件，當 account.html 更新頭像時同步
        window.addEventListener('storage', function(e) {
            if (e.key === 'userAvatar') {
                const newAvatar = e.newValue;
                if (newAvatar) {
                    if (newAvatar.startsWith('http') || newAvatar.startsWith('data:')) {
                        avatarEl.style.backgroundImage = `url(${newAvatar})`;
                        avatarEl.style.backgroundSize = 'cover';
                        avatarEl.style.backgroundPosition = 'center';
                        avatarEl.textContent = '';
                    } else {
                        avatarEl.textContent = newAvatar;
                        avatarEl.style.backgroundImage = 'none';
                    }
                }
            }
        });
        
        console.log('✅ 用戶頭像已初始化');
    }
    
    /**
     * 從用戶信息更新頭像
     */
    async function updateAvatarFromUser() {
        try {
            let user = null;
            
            if (window.simpleAuth && window.simpleAuth.currentUser) {
                user = window.simpleAuth.currentUser;
            } else if (window.firebase && window.firebase.auth) {
                user = window.firebase.auth().currentUser;
            }
            
            if (user && user.email) {
                const firstLetter = user.email.charAt(0).toUpperCase();
                const avatarEl = document.getElementById('user-avatar');
                if (avatarEl && !localStorage.getItem('userAvatar')) {
                    avatarEl.textContent = firstLetter;
                    localStorage.setItem('userAvatar', firstLetter);
                }
            }
        } catch (error) {
            console.error('❌ 更新頭像失敗:', error);
        }
    }
    
    /**
     * 點擊外部關閉所有下拉菜單
     */
    document.addEventListener('click', function() {
        const langMenu = document.getElementById('language-menu');
        const userMenuDropdown = document.getElementById('user-menu-dropdown');
        
        if (langMenu) {
            langMenu.style.display = 'none';
        }
        if (userMenuDropdown) {
            userMenuDropdown.style.display = 'none';
        }
    });
    
    console.log('✅ 導航欄交互功能初始化完成');
})();

