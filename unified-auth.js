/**
 * 統一的認證邏輯
 * 用於所有頁面（index.html, blog pages, dashboard.html, etc.）
 * 
 * 使用方法：
 * 1. 在 HTML 中添加：<script src="unified-auth.js"></script>
 * 2. 確保 simple-auth.js 已加載
 * 3. 在 HTML 中添加用戶菜單容器：<div id="user-menu"></div>
 */

(function() {
    'use strict';
    
    console.log('🔵 unified-auth.js 加載');
    
    /**
     * 更新用戶菜單 UI
     */
    window.updateUserMenu = async function() {
        console.log('🔵 updateUserMenu() 被調用');
        const userMenu = document.getElementById('user-menu');
        if (!userMenu) {
            console.log('❌ 找不到 user-menu 元素');
            return;
        }
        
        console.log('🔵 user-menu 元素存在');
        
        try {
            // 檢查 simpleAuth 是否已加載
            if (!window.simpleAuth) {
                console.log('⏳ simpleAuth 尚未加載，顯示登入按鈕');
                userMenu.innerHTML = `
                    <button onclick="window.location.href='/auth.html'" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;" onmouseover="this.style.background='#7c3aed'" onmouseout="this.style.background='#8b5cf6'">登入</button>
                `;
                return;
            }
            
            // 檢查是否已登入
            const isLoggedIn = window.simpleAuth.isLoggedIn();
            console.log('🔵 isLoggedIn:', isLoggedIn);
            
            if (isLoggedIn) {
                const user = window.simpleAuth.getCurrentUser();
                console.log('✅ 用戶已登入:', user.email);
                
                // 獲取用戶名和 Credits（從 Firestore）
                let displayName = user.displayName || user.email || '';
                let credits = 0;
                
                // 嘗試從 Firestore 獲取更完整的用戶資訊
                // 如果 SimpleDataManager 未就緒，等待它初始化
                if (window.simpleDataManager && window.simpleDataManager.initialized) {
                    try {
                        const userDoc = await window.simpleDataManager.getUserDocument();
                        if (userDoc) {
                            displayName = userDoc.displayName || displayName;
                            credits = userDoc.credits || 0;
                            console.log('📊 Credits 數據:', { 
                                fromFirestore: userDoc.credits, 
                                finalValue: credits,
                                userDocKeys: Object.keys(userDoc)
                            });
                            console.log('✅ 從 Firestore 獲取用戶資訊:', { displayName, credits });
                        }
                    } catch (error) {
                        console.warn('⚠️ 無法從 Firestore 獲取用戶資訊:', error);
                    }
                } else {
                    console.log('⏳ SimpleDataManager 未就緒，等待 app-ready 事件');
                    // 不再使用輪詢，改用事件監聽
                    window.addEventListener('app-ready', async () => {
                        console.log('✅ 收到 app-ready 事件，重新載入用戶菜單');
                        await updateUserMenu();
                    }, { once: true });
                }
                
                // 獲取用戶名前兩個字的首字母
                let initial = 'YC'; // 默認值
                if (user.displayName && user.displayName.trim()) {
                    // 如果有 displayName，取前兩個字的首字母
                    const names = user.displayName.trim().split(' ');
                    if (names.length >= 2) {
                        // 例如 "yeung cavlin" -> "YC"
                        initial = names[0].charAt(0).toUpperCase() + names[1].charAt(0).toUpperCase();
                    } else {
                        // 如果只有一個名字，取前兩個字符
                        initial = user.displayName.substring(0, 2).toUpperCase();
                    }
                }
                
                // 顯示用戶頭像和下拉菜單
                userMenu.innerHTML = `
                    <div style="position: relative;">
                        <div id="user-avatar" onclick="toggleDropdown()" style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; cursor: pointer; font-size: 1rem; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3); transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.4)'" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 8px rgba(102, 126, 234, 0.3)'">
                            ${initial}
                        </div>
                        <div id="user-dropdown" style="display: none !important; position: absolute; top: 50px; right: 0; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); min-width: 200px; z-index: 1000; border: 1px solid #e5e7eb;">
                            <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb;">
                                <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">${user.email}</div>
                                <div style="font-size: 0.75rem; color: #6b7280;">Credits: ${credits}</div>
                            </div>
                            <a href="/account.html" style="display: block; padding: 0.75rem 1rem; color: #374151; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>
                                帳戶
                            </a>
                            <a href="/billing.html" style="display: block; padding: 0.75rem 1rem; color: #374151; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>
                                計費
                            </a>
                            <div style="border-top: 1px solid #e5e7eb; margin: 0.5rem 0;"></div>
                            <a href="#" onclick="event.preventDefault(); handleLogout();" style="display: block; padding: 0.75rem 1rem; color: #ef4444; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>
                                登出
                            </a>
                        </div>
                    </div>
                `;
            } else {
                console.log('❌ 用戶未登入，顯示登入按鈕');
                // 顯示登入按鈕
                userMenu.innerHTML = `
                    <button onclick="window.location.href='/auth.html'" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;" onmouseover="this.style.background='#7c3aed'" onmouseout="this.style.background='#8b5cf6'">登入</button>
                `;
            }
        } catch (error) {
            console.error('❌ updateUserMenu 錯誤:', error);
            // 出錯時顯示登入按鈕
            userMenu.innerHTML = `
                <button onclick="window.location.href='/auth.html'" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;" onmouseover="this.style.background='#7c3aed'" onmouseout="this.style.background='#8b5cf6'">登入</button>
            `;
        }
    };
    
    /**
     * 切換下拉菜單
     */
    window.toggleDropdown = function() {
        const dropdown = document.getElementById('user-dropdown');
        if (dropdown) {
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        }
    };
    
    /**
     * 處理登出
     */
    window.handleLogout = async function() {
        try {
            if (window.simpleAuth) {
                await window.simpleAuth.logout();
                console.log('✅ 登出成功');
                window.location.href = '/';
            }
        } catch (error) {
            console.error('❌ 登出失敗:', error);
            alert('登出失敗，請重試');
        }
    };
    
    /**
     * 點擊外部關閉下拉菜單
     */
    document.addEventListener('click', function(event) {
        const userAvatar = document.getElementById('user-avatar');
        const dropdown = document.getElementById('user-dropdown');
        
        if (dropdown && userAvatar) {
            if (!userAvatar.contains(event.target) && !dropdown.contains(event.target)) {
                dropdown.style.display = 'none';
            }
        }
    });
    
    /**
     * 監聽認證狀態變化
     */
    window.addEventListener('auth-state-changed', (event) => {
        console.log('🔔 收到 auth-state-changed 事件');
        updateUserMenu();
    });
    
    /**
     * 初始化
     */
    function initUnifiedAuth() {
        console.log('🔵 initUnifiedAuth() 開始');
        
        // 如果 simpleAuth 已經加載，立即更新
        if (window.simpleAuth) {
            console.log('✅ simpleAuth 已加載，立即更新用戶菜單');
            updateUserMenu();
        } else {
            console.log('⏳ 等待 simpleAuth 加載...');
            // 否則顯示登入按鈕，等待 auth-state-changed 事件
            const userMenu = document.getElementById('user-menu');
            if (userMenu) {
                userMenu.innerHTML = `
                    <button onclick="window.location.href='/auth.html'" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;" onmouseover="this.style.background='#7c3aed'" onmouseout="this.style.background='#8b5cf6'">登入</button>
                `;
            }
        }
    }
    
    // DOM 加載完成後初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUnifiedAuth);
    } else {
        initUnifiedAuth();
    }
    
    console.log('✅ unified-auth.js 加載完成');
})();

