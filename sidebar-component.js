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
        
        sidebarContainer.innerHTML = this.getSidebarHTML();
    }
    
    getSidebarHTML() {
        return `
            <div class="sidebar-header">
                <h2 data-translate="models">模型</h2>
            </div>
            <nav class="sidebar-nav">
                <ul>
                    <li class="nav-item ${this.activePage === 'bank-statement' ? 'active' : ''}">
                        <a href="dashboard.html#bank-statement">
                            <i class="fas fa-university"></i>
                            <span data-translate="sidebar_bank_statements">銀行對帳單</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'invoice' ? 'active' : ''}">
                        <a href="dashboard.html#invoice">
                            <i class="fas fa-file-invoice"></i>
                            <span data-translate="sidebar_invoices">發票</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'receipt' ? 'active' : ''}">
                        <a href="dashboard.html#receipt">
                            <i class="fas fa-receipt"></i>
                            <span data-translate="sidebar_receipts">收據</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'general' ? 'active' : ''}">
                        <a href="dashboard.html#general">
                            <i class="fas fa-file-alt"></i>
                            <span data-translate="sidebar_general">一般文檔</span>
                        </a>
                    </li>
                </ul>
                
                <h3 data-translate="configurations">配置</h3>
                <ul>
                    <li class="nav-item ${this.activePage === 'account' ? 'active' : ''}">
                        <a href="account.html">
                            <i class="fas fa-user"></i>
                            <span data-translate="account">帳戶</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'billing' ? 'active' : ''}">
                        <a href="billing.html">
                            <i class="fas fa-credit-card"></i>
                            <span data-translate="billing">計費</span>
                        </a>
                    </li>
                </ul>
            </nav>
            
            <!-- 側邊欄底部統計區域 -->
            <div class="sidebar-footer">
                <div class="sidebar-stats">
                    <div class="sidebar-stat-item">
                        <div class="stat-icon-text">📄</div>
                        <div class="stat-text">
                            <span class="stat-number" data-stat="total-processed">0</span>
                            <span class="stat-label" data-translate="processed_documents_count">處理文檔總數</span>
                        </div>
                    </div>
                    
                    <div class="sidebar-stat-item">
                        <div class="stat-icon-text">💰</div>
                        <div class="stat-text">
                            <span class="stat-number" data-stat="current-credits">7</span>
                            <span class="stat-label" data-translate="remaining_credits">剩餘Credits</span>
                        </div>
                    </div>
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
