/**
 * VaultCaddy 統一側邊欄組件
 * 用於所有Dashboard頁面的一致導航
 * Google Cloud Vision API Client ID: 672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com
 */

class VaultCaddySidebar {
    constructor(activePage = 'bank-statement') {
        this.activePage = activePage;
        this.init();
    }
    
    init() {
        this.render();
        this.bindEvents();
        this.loadStats();
        this.setupLanguageListener();
    }
    
    render() {
        const sidebarContainer = document.querySelector('.sidebar');
        if (!sidebarContainer) {
            console.error('找不到側邊欄容器 .sidebar');
            return;
        }
        
        // 設置側邊欄為 flexbox 布局
        sidebarContainer.style.cssText = 'width: 280px; background: #ffffff; border-right: 1px solid #e5e7eb; padding: 1.5rem; display: flex; flex-direction: column; visibility: visible;';
        
        sidebarContainer.innerHTML = this.getSidebarHTML();
    }
    
    getSidebarHTML() {
        return `
            <!-- 搜索欄 -->
            <div style="margin-bottom: 1.5rem;">
                <input type="text" placeholder="篩選文檔名稱..." style="width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 0.875rem; color: #6b7280;">
            </div>
            
            <!-- Project 區塊 -->
            <div style="margin-bottom: auto;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <span style="font-size: 0.875rem; font-weight: 500; color: #6b7280;">project</span>
                    <button onclick="createNewProject()" style="background: none; border: none; color: #6b7280; cursor: pointer; font-size: 1.25rem; padding: 0; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;">+</button>
                </div>
                <div onclick="navigateToTeamProject ? navigateToTeamProject() : window.location.href='dashboard.html'" style="display: flex; align-items: center; padding: 0.5rem; color: #6b7280; cursor: pointer; border-radius: 4px; transition: background 0.2s;">
                    <i class="fas fa-folder" style="margin-right: 0.5rem; font-size: 1rem;"></i>
                    <span style="font-size: 0.875rem;">Team project</span>
                </div>
            </div>
            
            <!-- 配置區塊 (底部) -->
            <div style="border-top: 1px solid #e5e7eb; padding-top: 1rem;">
                <h3 style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.75rem 0;">配置</h3>
                <div onclick="window.location.href='account.html'" style="display: flex; align-items: center; padding: 0.5rem; color: #6b7280; cursor: pointer; border-radius: 4px; transition: background 0.2s; margin-bottom: 0.25rem;">
                    <i class="fas fa-user" style="margin-right: 0.5rem; font-size: 1rem; width: 20px;"></i>
                    <span style="font-size: 0.875rem;">帳戶</span>
                </div>
                <div onclick="window.location.href='billing.html'" style="display: flex; align-items: center; padding: 0.5rem; color: ${this.activePage === 'billing' ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; ${this.activePage === 'billing' ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem);' : ''}">
                    <i class="fas fa-credit-card" style="margin-right: 0.5rem; font-size: 1rem; width: 20px; color: ${this.activePage === 'billing' ? '#2563eb' : '#6b7280'};"></i>
                    <span style="font-size: 0.875rem;">計費</span>
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // 為側邊欄導航項目添加點擊事件
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('.sidebar .nav-item a');
            if (navLink) {
                e.preventDefault();
                const href = navLink.getAttribute('href');
                
                // 如果當前在文檔詳細視圖，先回到列表視圖
                const detailView = document.getElementById('document-detail-view');
                const listView = document.getElementById('document-list-view');
                
                if (detailView && listView) {
                    if (detailView.style.display !== 'none') {
                        // 隱藏詳細視圖，顯示列表視圖
                        detailView.style.display = 'none';
                        listView.style.display = 'block';
                    }
                }
                
                // 導航到新的hash
                window.location.href = href;
                
                console.log('側邊欄導航到:', href);
            }
        });
        
        console.log('側邊欄事件已綁定');
    }
    
    loadStats() {
        // 從VaultCaddyStats載入統計數據
        if (window.VaultCaddyStats) {
            window.VaultCaddyStats.updateDashboardDisplays();
        }
    }
    
    setupLanguageListener() {
        // 監聽語言變更事件
        window.addEventListener('languageChanged', (e) => {
            console.log('Sidebar: 語言已變更為', e.detail.language);
            // 重新渲染側邊欄以應用新的翻譯
            this.render();
            // 重新應用翻譯
            if (window.languageManager) {
                window.languageManager.loadLanguage(e.detail.language);
            }
        });
    }
    
    updateActivePage(activePage) {
        this.activePage = activePage;
        
        // 更新側邊欄中的活躍狀態
        const navItems = document.querySelectorAll('.sidebar .nav-item');
        navItems.forEach(item => {
            item.classList.remove('active');
            
            const link = item.querySelector('a');
            if (link) {
                const href = link.getAttribute('href');
                if (href === `dashboard.html#${activePage}`) {
                    item.classList.add('active');
                }
            }
        });
        
        console.log('✅ 側邊欄活躍頁面已更新:', activePage);
    }
}

// 導出類
window.VaultCaddySidebar = VaultCaddySidebar;
