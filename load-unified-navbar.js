/**
 * 統一導航欄加載器
 * 從 unified-navbar.html 加載導航欄，實現全站統一
 * 
 * 使用方法：
 * 1. 在 HTML 的 <body> 開頭添加：<div id="navbar-container"></div>
 * 2. 在 </body> 前添加：<script src="load-unified-navbar.js"></script>
 */

(function() {
    'use strict';
    
    console.log('🔵 load-unified-navbar.js 開始加載');
    
    /**
     * 加載統一導航欄
     */
    async function loadUnifiedNavbar() {
        const container = document.getElementById('navbar-container');
        
        if (!container) {
            console.error('❌ 找不到 navbar-container 元素');
            return;
        }
        
        try {
            // 判斷當前路徑，決定導航欄 HTML 的路徑
            const isInBlogFolder = window.location.pathname.includes('/blog/');
            const navbarPath = isInBlogFolder ? '../unified-navbar.html' : 'unified-navbar.html';
            
            console.log(`🔵 載入導航欄：${navbarPath}`);
            
            // 使用 fetch 加載導航欄 HTML
            const response = await fetch(navbarPath);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            container.innerHTML = html;
            
            console.log('✅ 導航欄載入成功');
            
            // 觸發自定義事件，通知其他腳本導航欄已載入
            window.dispatchEvent(new Event('navbar-loaded'));
            
        } catch (error) {
            console.error('❌ 載入導航欄失敗:', error);
            
            // 失敗時顯示基本導航欄
            container.innerHTML = `
                <nav class="vaultcaddy-navbar" style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000;">
                    <a href="/" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600;">
                        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">V</div>
                        <span>VaultCaddy</span>
                    </a>
                    <div style="display: flex; gap: 2rem;">
                        <a href="/index.html#features" style="color: #4b5563; text-decoration: none;">功能</a>
                        <a href="/index.html#pricing" style="color: #4b5563; text-decoration: none;">價格</a>
                        <a href="/dashboard.html" style="color: #4b5563; text-decoration: none;">儀表板</a>
                        <a href="/auth.html" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none;">登入</a>
                    </div>
                </nav>
            `;
        }
    }
    
    // DOM 加載完成後載入導航欄
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadUnifiedNavbar);
    } else {
        loadUnifiedNavbar();
    }
    
    console.log('✅ load-unified-navbar.js 載入完成');
})();

