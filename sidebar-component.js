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
                <h2>Models</h2>
            </div>
            <nav class="sidebar-nav">
                <ul>
                    <li class="nav-item ${this.activePage === 'bank-statement' ? 'active' : ''}">
                        <a href="dashboard.html#bank-statement">
                            <i class="fas fa-university"></i>
                            <span>Bank statements</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'invoice' ? 'active' : ''}">
                        <a href="dashboard.html#invoice">
                            <i class="fas fa-file-invoice"></i>
                            <span>Invoices</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'receipt' ? 'active' : ''}">
                        <a href="dashboard.html#receipt">
                            <i class="fas fa-receipt"></i>
                            <span>Receipts</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'general' ? 'active' : ''}">
                        <a href="dashboard.html#general">
                            <i class="fas fa-file-alt"></i>
                            <span>General</span>
                        </a>
                    </li>
                </ul>
                
                <h3>Configurations</h3>
                <ul>
                    <li class="nav-item ${this.activePage === 'account' ? 'active' : ''}">
                        <a href="account.html">
                            <i class="fas fa-user"></i>
                            <span>Account</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'billing' ? 'active' : ''}">
                        <a href="billing.html">
                            <i class="fas fa-credit-card"></i>
                            <span>Billing</span>
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
                            <span class="stat-label">處理文檔總數</span>
                        </div>
                    </div>
                    
                    <div class="sidebar-stat-item">
                        <div class="stat-icon-text">⏱️</div>
                        <div class="stat-text">
                            <span class="stat-number" data-stat="avg-processing-time">0ms</span>
                            <span class="stat-label">平均處理時間</span>
                        </div>
                    </div>
                    
                    <div class="sidebar-stat-item">
                        <div class="stat-icon-text">✅</div>
                        <div class="stat-text">
                            <span class="stat-number" data-stat="success-rate">0%</span>
                            <span class="stat-label">處理成功率</span>
                        </div>
                    </div>
                    
                    <div class="sidebar-stat-item">
                        <div class="stat-icon-text">💰</div>
                        <div class="stat-text">
                            <span class="stat-number" data-stat="current-credits">7</span>
                            <span class="stat-label">剩餘Credits</span>
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
