/**
 * VaultCaddy 統一側邊欄組件
 * 用於所有Dashboard頁面的一致導航
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
                        <a href="dashboard-main.html">
                            <i class="fas fa-university"></i>
                            <span>Bank statements</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'invoice' ? 'active' : ''}">
                        <a href="dashboard-invoice.html">
                            <i class="fas fa-file-invoice"></i>
                            <span>Invoices</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'receipt' ? 'active' : ''}">
                        <a href="dashboard-receipt.html">
                            <i class="fas fa-receipt"></i>
                            <span>Receipts</span>
                        </a>
                    </li>
                    <li class="nav-item ${this.activePage === 'general' ? 'active' : ''}">
                        <a href="dashboard-general.html">
                            <i class="fas fa-file-alt"></i>
                            <span>General</span>
                        </a>
                    </li>
                </ul>
                
                <h3>Configurations</h3>
                <ul>
                    <li class="nav-item">
                        <a href="account.html">
                            <i class="fas fa-user"></i>
                            <span>Account</span>
                        </a>
                    </li>
                    <li class="nav-item">
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
        // 導航項目點擊事件已經通過href處理
        console.log('側邊欄事件已綁定');
    }
    
    loadStats() {
        // 從VaultCaddyStats載入統計數據
        if (window.VaultCaddyStats) {
            window.VaultCaddyStats.updateDashboardDisplays();
        }
    }
    
    updateActivePage(pageName) {
        this.activePage = pageName;
        this.render();
    }
}

// 導出類
window.VaultCaddySidebar = VaultCaddySidebar;
