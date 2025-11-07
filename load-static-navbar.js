/**
 * 統一靜態導航欄加載器
 * 作用：在所有頁面加載統一的靜態導航欄
 * 使用方式：在 <head> 中引入此腳本
 */

(function() {
    'use strict';
    
    // 等待 DOM 準備好
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', insertNavbar);
    } else {
        insertNavbar();
    }
    
    function insertNavbar() {
        // 檢查是否已經有導航欄
        if (document.querySelector('.vaultcaddy-navbar')) {
            console.log('✅ 導航欄已存在，跳過');
            return;
        }
        
        // 移除舊的 fallback-navbar（但保留 navbar-placeholder）
        const oldFallback = document.querySelector('.fallback-navbar');
        if (oldFallback) {
            oldFallback.remove();
            console.log('🗑️ 移除舊的 Fallback 導航欄');
        }
        
        // 創建導航欄 HTML
        const navbarHTML = `
            <style>
                .vaultcaddy-navbar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 60px;
                    background: #ffffff;
                    border-bottom: 1px solid #e5e7eb;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 2rem;
                    z-index: 1000;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                }
                
                .navbar-left {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .navbar-logo {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    text-decoration: none;
                    color: #1f2937;
                    font-weight: 600;
                    font-size: 1.125rem;
                }
                
                .navbar-logo-icon {
                    width: 32px;
                    height: 32px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 700;
                    font-size: 1rem;
                }
                
                .navbar-subtitle {
                    font-size: 0.75rem;
                    color: #6b7280;
                    font-weight: 400;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                
                .navbar-right {
                    display: flex;
                    align-items: center;
                    gap: 2rem;
                }
                
                .navbar-links {
                    display: flex;
                    align-items: center;
                    gap: 2rem;
                }
                
                .navbar-link {
                    color: #4b5563;
                    text-decoration: none;
                    font-size: 0.9375rem;
                    font-weight: 500;
                    transition: color 0.2s;
                }
                
                .navbar-link:hover {
                    color: #667eea;
                }
                
                .navbar-language {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: #6b7280;
                    font-size: 0.875rem;
                    cursor: pointer;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    transition: background 0.2s;
                }
                
                .navbar-language:hover {
                    background: #f3f4f6;
                }
                
                .navbar-user {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    cursor: pointer;
                    padding: 0.5rem;
                    border-radius: 8px;
                    transition: background 0.2s;
                }
                
                .navbar-user:hover {
                    background: #f3f4f6;
                }
                
                .navbar-avatar {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: #667eea;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 600;
                    font-size: 0.875rem;
                }
                
                @media (max-width: 768px) {
                    .vaultcaddy-navbar {
                        padding: 0 1rem;
                    }
                    
                    .navbar-links {
                        display: none;
                    }
                    
                    .navbar-subtitle {
                        display: none;
                    }
                }
            </style>
            
            <nav class="vaultcaddy-navbar">
                <div class="navbar-left">
                    <a href="index.html" class="navbar-logo">
                        <div class="navbar-logo-icon">V</div>
                        <div>
                            <div>VaultCaddy</div>
                            <div class="navbar-subtitle">AI DOCUMENT PROCESSING</div>
                        </div>
                    </a>
                </div>
                
                <div class="navbar-right">
                    <div class="navbar-links">
                        <a href="index.html#features" class="navbar-link">功能</a>
                        <a href="billing.html" class="navbar-link">價格</a>
                        <a href="index.html#pricing" class="navbar-link">儀表板</a>
                    </div>
                    
                    <div class="navbar-language">
                        <i class="fas fa-globe"></i>
                        <span>繁體中文</span>
                        <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
                    </div>
                    
                    <div class="navbar-user" onclick="window.location.href='account.html'">
                        <div class="navbar-avatar" id="navbar-avatar-letter">U</div>
                    </div>
                </div>
            </nav>
        `;
        
        // 插入到 body 開頭或 navbar-placeholder 中
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = navbarHTML;
        const navbar = tempDiv.firstElementChild;
        
        const placeholder = document.getElementById('navbar-placeholder');
        if (placeholder) {
            // 如果有 placeholder，插入到裡面
            placeholder.appendChild(navbar);
            console.log('✅ 導航欄已插入到 navbar-placeholder');
        } else {
            // 否則插入到 body 開頭
            document.body.insertBefore(navbar, document.body.firstChild);
            console.log('✅ 導航欄已插入到 body 開頭');
        }
        
        // 更新用戶頭像
        updateUserAvatar();
        
        console.log('✅ 統一靜態導航欄已加載');
    }
    
    function updateUserAvatar() {
        try {
            if (window.simpleAuth && window.simpleAuth.isLoggedIn()) {
                const user = window.simpleAuth.getCurrentUser();
                const avatarLetter = document.getElementById('navbar-avatar-letter');
                if (avatarLetter && user) {
                    const letter = (user.email || user.displayName || 'U')[0].toUpperCase();
                    avatarLetter.textContent = letter;
                }
            }
        } catch (e) {
            console.log('無法更新頭像:', e);
        }
    }
    
    // 監聽用戶登入狀態變化
    window.addEventListener('firebase-ready', updateUserAvatar);
    window.addEventListener('user-logged-in', updateUserAvatar);
})();

