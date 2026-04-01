/**
 * 統一側邊欄加載器
 * 根據頁面類型加載不同的側邊欄
 * 
 * 使用方法：
 * 1. 在 HTML 中添加：<div id="sidebar-container"></div>
 * 2. 在 </body> 前添加：<script src="load-unified-sidebar.js"></script>
 */

(function() {
    'use strict';
    
    console.log('🔵 load-unified-sidebar.js 開始加載');
    
    /**
     * 判斷側邊欄類型
     */
    function getSidebarType() {
        const path = window.location.pathname;
        
        // 博客頁面
        if (path.includes('/blog/')) {
            return 'blog';
        }
        
        // Dashboard/Account/Billing/FirstProject 頁面
        if (path.includes('/dashboard.html') || 
            path.includes('/account.html') || 
            path.includes('/billing.html') || 
            path.includes('/firstproject.html')) {
            return 'app';
        }
        
        // 其他頁面不需要側邊欄
        return null;
    }
    
    /**
     * 載入統一側邊欄
     */
    async function loadUnifiedSidebar() {
        const container = document.getElementById('sidebar-container');
        
        if (!container) {
            console.log('⏭️  頁面沒有 sidebar-container，跳過');
            return;
        }
        
        const sidebarType = getSidebarType();
        
        if (!sidebarType) {
            console.log('⏭️  此頁面不需要側邊欄');
            return;
        }
        
        try {
            // 決定側邊欄文件路徑
            const isInBlogFolder = window.location.pathname.includes('/blog/');
            let sidebarPath;
            
            if (sidebarType === 'blog') {
                sidebarPath = isInBlogFolder ? '../unified-blog-sidebar.html' : 'unified-blog-sidebar.html';
            } else if (sidebarType === 'app') {
                sidebarPath = 'unified-sidebar.html';
            }
            
            console.log(`🔵 載入側邊欄：${sidebarPath} (類型：${sidebarType})`);
            
            // 使用 fetch 載入側邊欄 HTML
            const response = await fetch(sidebarPath);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            container.innerHTML = html;
            
            console.log('✅ 側邊欄載入成功');
            
            // 觸發自定義事件
            window.dispatchEvent(new Event('sidebar-loaded'));
            
        } catch (error) {
            console.error('❌ 載入側邊欄失敗:', error);
            
            // 失敗時隱藏容器
            container.style.display = 'none';
        }
    }
    
    // DOM 加載完成後載入側邊欄
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadUnifiedSidebar);
    } else {
        loadUnifiedSidebar();
    }
    
    console.log('✅ load-unified-sidebar.js 載入完成');
})();

