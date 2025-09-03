/**
 * VaultCaddy 內容管理器
 * 實現單頁應用模式，動態切換主內容區域
 */

class ContentManager {
    constructor() {
        this.currentPage = 'bank-statement';
        this.contentCache = new Map();
        this.init();
    }
    
    init() {
        this.bindNavigationEvents();
        this.setupHashRouting();
        this.loadInitialContent();
    }
    
    // 綁定導航事件
    bindNavigationEvents() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.isInternalLink(link.href)) {
                e.preventDefault();
                const page = this.extractPageFromUrl(link.href);
                this.navigateToPage(page);
            }
        });
    }
    
    // 設置Hash路由
    setupHashRouting() {
        window.addEventListener('hashchange', () => {
            const page = this.getPageFromHash();
            this.navigateToPage(page, false);
        });
    }
    
    // 檢查是否為內部連結
    isInternalLink(href) {
        const internalPages = [
            'dashboard-main.html',
            'dashboard-invoice.html', 
            'dashboard-receipt.html',
            'dashboard-general.html',
            'account.html',
            'billing.html'
        ];
        return internalPages.some(page => href.includes(page));
    }
    
    // 從URL提取頁面名稱
    extractPageFromUrl(url) {
        if (url.includes('dashboard-main.html')) return 'bank-statement';
        if (url.includes('dashboard-invoice.html')) return 'invoice';
        if (url.includes('dashboard-receipt.html')) return 'receipt';
        if (url.includes('dashboard-general.html')) return 'general';
        if (url.includes('account.html')) return 'account';
        if (url.includes('billing.html')) return 'billing';
        return 'bank-statement';
    }
    
    // 從Hash獲取頁面
    getPageFromHash() {
        const hash = window.location.hash.slice(1);
        return hash || 'bank-statement';
    }
    
    // 導航到指定頁面
    async navigateToPage(page, updateHash = true) {
        if (page === this.currentPage) return;
        
        console.log(`🔄 切換到頁面: ${page}`);
        
        // 更新Hash
        if (updateHash) {
            window.location.hash = page;
        }
        
        // 載入內容
        await this.loadPageContent(page);
        
        // 更新側邊欄活躍狀態
        this.updateSidebarActive(page);
        
        // 更新當前頁面
        this.currentPage = page;
        
        // 觸發頁面切換事件
        this.dispatchPageChangeEvent(page);
    }
    
    // 載入頁面內容
    async loadPageContent(page) {
        const mainContent = document.querySelector('.main-content');
        if (!mainContent) {
            console.error('找不到 .main-content 容器');
            return;
        }
        
        // 顯示載入狀態
        this.showLoadingState(mainContent);
        
        try {
            let content = this.contentCache.get(page);
            if (!content) {
                content = await this.fetchPageContent(page);
                this.contentCache.set(page, content);
            }
            
            // 更新內容
            mainContent.innerHTML = content;
            
            // 初始化頁面特定功能
            this.initializePageFeatures(page);
            
            console.log(`✅ 頁面 ${page} 載入完成`);
            
        } catch (error) {
            console.error(`❌ 載入頁面 ${page} 失敗:`, error);
            this.showErrorState(mainContent, page);
        }
    }
    
    // 獲取頁面內容
    async fetchPageContent(page) {
        const contentTemplates = {
            'bank-statement': this.getBankStatementContent(),
            'invoice': this.getInvoiceContent(),
            'receipt': this.getReceiptContent(),
            'general': this.getGeneralContent(),
            'account': this.getAccountContent(),
            'billing': this.getBillingContent()
        };
        
        return contentTemplates[page] || contentTemplates['bank-statement'];
    }
    
    // 獲取銀行對帳單內容
    getBankStatementContent() {
        return `
            <!-- 頂部標題和控制 -->
            <header class="content-header">
                <div class="header-left">
                    <h1 id="current-model-title">Bank statement converter</h1>
                    <p>Manage and view your documents</p>
                </div>
                <div class="header-right">
                    <button class="help-btn" onclick="showHelp('bank-statement')">Need Help?</button>
                </div>
            </header>

            <!-- 控制區域 -->
            <section class="controls-section">
                <div class="controls-bar">
                    <div class="search-filter">
                        <input type="text" placeholder="Filter document name..." class="filter-input">
                    </div>
                    <div class="actions">
                        <button class="upload-btn" onclick="openUploadModal('bank-statement')">
                            <i class="fas fa-upload"></i>
                            Upload files
                        </button>
                        <button class="view-btn" onclick="toggleView()">
                            <i class="fas fa-eye"></i>
                            View
                        </button>
                    </div>
                </div>
            </section>

            <!-- 文檔表格 -->
            <section class="documents-table">
                <div class="table-container">
                    <table class="documents-grid">
                        <thead>
                            <tr>
                                <th><input type="checkbox" class="select-all">Document</th>
                                <th>Statement Period</th>
                                <th>Reconciliation</th>
                                <th>Balance Info</th>
                                <th>Status & Review</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody id="documents-tbody">
                            <!-- 由 document-manager.js 動態生成 -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- 選擇信息 -->
            <div class="selection-info">0 of 0 row(s) selected.</div>
        `;
    }
    
    // 獲取發票內容
    getInvoiceContent() {
        return `
            <header class="content-header" style="margin-bottom: 1.5rem;">
                <div class="header-left">
                    <h1 style="font-size: 1.75rem; font-weight: 700; color: #1f2937; margin: 0 0 0.5rem 0;">Invoice Processing</h1>
                    <p style="color: #6b7280; margin: 0;">Manage and view your invoice documents</p>
                </div>
                <div class="header-right">
                    <button class="help-btn" onclick="showHelp('invoice')" style="background: #6b7280; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer;">Need Help?</button>
                </div>
            </header>

            <section class="controls-section" style="margin-bottom: 1.5rem;">
                <div class="controls-bar" style="display: flex; justify-content: space-between; align-items: center; background: #ffffff; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <div class="search-filter" style="flex: 1; max-width: 400px;">
                        <input type="text" placeholder="Filter document name..." class="filter-input" style="width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; background: #ffffff;">
                    </div>
                    <div class="actions" style="display: flex; gap: 0.75rem;">
                        <button class="upload-btn" onclick="openUploadModal('invoice')" style="background: #3b82f6; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-upload"></i>
                            Upload files
                        </button>
                        <button class="view-btn" onclick="toggleView()" style="background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; padding: 0.75rem 1.5rem; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-eye"></i>
                            View
                        </button>
                    </div>
                </div>
            </section>

            <section class="documents-table" style="background: #ffffff; border-radius: 8px; border: 1px solid #e5e7eb; overflow: hidden;">
                <div class="table-container" style="overflow-x: auto;">
                    <table class="documents-grid" style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f9fafb;">
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;"><input type="checkbox" class="select-all" style="margin-right: 0.5rem;">Document</th>
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Vendor Info</th>
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Amount</th>
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Date Uploaded</th>
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Status & Review</th>
                                <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom: 1px solid #f3f4f6;" onmouseover="this.style.backgroundColor='#f9fafb'" onmouseout="this.style.backgroundColor='#ffffff'">
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                                        <input type="checkbox">
                                        <i class="fas fa-file-invoice" style="color: #3b82f6; font-size: 1.25rem;"></i>
                                        <div>
                                            <div style="font-weight: 600; color: #1f2937; cursor: pointer;" onclick="openDocumentDetail('inv_001')">Invoice_2025_001.pdf</div>
                                            <div style="font-size: 0.875rem; color: #6b7280;">📍 ABC Company Ltd<br>📊 INV-2025-001</div>
                                        </div>
                                    </div>
                                </td>
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="color: #1f2937;">
                                        🏢 ABC Company Ltd
                                        <br><small style="color: #6b7280;">Due: 2025/09/15</small>
                                    </div>
                                </td>
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="font-weight: 600; color: #1f2937;">$5,420.00</div>
                                    <div style="font-size: 0.875rem; color: #6b7280;">Tax: $542.00</div>
                                </td>
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="color: #1f2937;">📅 2025/8/29</div>
                                    <div style="font-size: 0.875rem; color: #6b7280;">Completed</div>
                                </td>
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                                        <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; text-align: center;">✅ Success</span>
                                        <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; text-align: center;">✓ Approved</span>
                                    </div>
                                </td>
                                <td style="padding: 1rem; vertical-align: top;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="color: #6b7280;">Payment processed</span>
                                        <button onclick="showActionMenu(event, 'inv_001')" style="background: none; border: none; color: #6b7280; cursor: pointer; padding: 0.25rem;" title="更多操作">
                                            <i class="fas fa-ellipsis-h"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <div class="selection-info" style="margin-top: 1rem; color: #6b7280; font-size: 0.875rem;">0 of 1 row(s) selected.</div>
        `;
    }
    
    // 獲取收據內容
    getReceiptContent() {
        return `
            <header class="content-header">
                <div class="header-left">
                    <h1>Receipt Scanning</h1>
                    <p>Manage and view your receipt documents</p>
                </div>
                <div class="header-right">
                    <button class="help-btn" onclick="showHelp('receipt')">Need Help?</button>
                </div>
            </header>

            <section class="controls-section">
                <div class="controls-bar">
                    <div class="search-filter">
                        <input type="text" placeholder="Filter document name..." class="filter-input">
                    </div>
                    <div class="actions">
                        <button class="upload-btn" onclick="openUploadModal('receipt')">
                            <i class="fas fa-upload"></i>
                            Upload files
                        </button>
                        <button class="view-btn" onclick="toggleView()">
                            <i class="fas fa-eye"></i>
                            View
                        </button>
                    </div>
                </div>
            </section>

            <section class="documents-table">
                <div class="table-container">
                    <table class="documents-grid">
                        <thead>
                            <tr>
                                <th><input type="checkbox" class="select-all">Document</th>
                                <th>Merchant Info</th>
                                <th>Amount</th>
                                <th>Date Uploaded</th>
                                <th>Status & Review</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody id="documents-tbody">
                            <!-- 動態生成 -->
                        </tbody>
                    </table>
                </div>
            </section>

            <div class="selection-info">0 of 0 row(s) selected.</div>
        `;
    }
    
    // 獲取通用文檔內容
    getGeneralContent() {
        return `
            <header class="content-header">
                <div class="header-left">
                    <h1>General Document Processing</h1>
                    <p>Manage and view your general documents</p>
                </div>
                <div class="header-right">
                    <button class="help-btn" onclick="showHelp('general')">Need Help?</button>
                </div>
            </header>

            <section class="controls-section">
                <div class="controls-bar">
                    <div class="search-filter">
                        <input type="text" placeholder="Filter document name..." class="filter-input">
                    </div>
                    <div class="actions">
                        <button class="upload-btn" onclick="openUploadModal('general')">
                            <i class="fas fa-upload"></i>
                            Upload files
                        </button>
                        <button class="view-btn" onclick="toggleView()">
                            <i class="fas fa-eye"></i>
                            View
                        </button>
                    </div>
                </div>
            </section>

            <section class="documents-table">
                <div class="table-container">
                    <table class="documents-grid">
                        <thead>
                            <tr>
                                <th><input type="checkbox" class="select-all">Document</th>
                                <th>Category</th>
                                <th>Size</th>
                                <th>Date Uploaded</th>
                                <th>Status & Review</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody id="documents-tbody">
                            <!-- 動態生成 -->
                        </tbody>
                    </table>
                </div>
            </section>

            <div class="selection-info">0 of 0 row(s) selected.</div>
        `;
    }
    
    // 獲取帳戶內容
    getAccountContent() {
        return `
            <header class="page-header">
                <h1>Account Settings</h1>
                <p>Manage your profile and account preferences</p>
            </header>

            <div class="account-sections">
                <section class="profile-section">
                    <div class="section-header">
                        <h2>Profile Information</h2>
                        <button class="update-btn" onclick="openUpdateProfileModal()">Update profile</button>
                    </div>
                    
                    <div class="profile-info">
                        <div class="info-group">
                            <label>Name</label>
                            <span id="user-name">John Doe</span>
                        </div>
                        <div class="info-group">
                            <label>Company</label>
                            <span id="user-company">Example Corp</span>
                        </div>
                        <div class="info-group">
                            <label>Phone</label>
                            <span id="user-phone">+1 (555) 123-4567</span>
                        </div>
                    </div>
                </section>

                <section class="email-section">
                    <div class="section-header">
                        <h2>Email Addresses</h2>
                        <button class="add-btn" onclick="addEmailAddress()">Add email</button>
                    </div>
                    
                    <div class="email-list" id="email-list">
                        <!-- 動態生成 -->
                    </div>
                </section>
            </div>
        `;
    }
    
    // 獲取計費內容
    getBillingContent() {
        return `
            <header class="page-header">
                <h1>Billing & Credits</h1>
                <p>Manage your subscription and view usage</p>
            </header>

            <div class="billing-sections">
                <section class="current-plan">
                    <h2>Current Plan</h2>
                    <div class="plan-info">
                        <div class="plan-badge">Professional</div>
                        <div class="plan-details">
                            <p>6,000 pages per year</p>
                            <p>$32/month (billed annually)</p>
                        </div>
                    </div>
                </section>

                <section class="usage-stats">
                    <h2>Usage Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <span class="stat-number">245</span>
                            <span class="stat-label">Pages processed this month</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">5,755</span>
                            <span class="stat-label">Pages remaining</span>
                        </div>
                    </div>
                </section>

                <section class="pricing-plans">
                    <h2>Available Plans</h2>
                    <!-- 價格方案內容 -->
                </section>
            </div>
        `;
    }
    
    // 顯示載入狀態
    showLoadingState(container) {
        container.innerHTML = `
            <div class="loading-state">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading...</p>
            </div>
        `;
    }
    
    // 顯示錯誤狀態
    showErrorState(container, page) {
        container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Failed to load page</h3>
                <p>Unable to load ${page} content. Please try again.</p>
                <button onclick="window.contentManager.navigateToPage('${page}')">Retry</button>
            </div>
        `;
    }
    
    // 更新側邊欄活躍狀態
    updateSidebarActive(page) {
        if (window.vaultcaddySidebar) {
            window.vaultcaddySidebar.updateActivePage(page);
        }
    }
    
    // 初始化頁面特定功能
    initializePageFeatures(page) {
        // 重新綁定事件監聽器
        this.bindPageEvents(page);
        
        // 初始化文檔管理器
        if (['bank-statement', 'invoice', 'receipt', 'general'].includes(page)) {
            this.initializeDocumentManager(page);
        }
    }
    
    // 綁定頁面事件
    bindPageEvents(page) {
        // 重新綁定表格事件
        const selectAll = document.querySelector('.select-all');
        if (selectAll) {
            selectAll.addEventListener('change', this.handleSelectAll.bind(this));
        }
    }
    
    // 初始化文檔管理器
    initializeDocumentManager(type) {
        if (window.DocumentManager) {
            window[`${type}DocumentManager`] = new DocumentManager(type);
        }
    }
    
    // 處理全選
    handleSelectAll(e) {
        const checkboxes = document.querySelectorAll('.documents-grid tbody input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = e.target.checked;
        });
        this.updateSelectionInfo();
    }
    
    // 更新選擇信息
    updateSelectionInfo() {
        const checkboxes = document.querySelectorAll('.documents-grid tbody input[type="checkbox"]');
        const selectedCount = document.querySelectorAll('.documents-grid tbody input[type="checkbox"]:checked').length;
        const selectionInfo = document.querySelector('.selection-info');
        if (selectionInfo) {
            selectionInfo.textContent = `${selectedCount} of ${checkboxes.length} row(s) selected.`;
        }
    }
    
    // 載入初始內容
    loadInitialContent() {
        const initialPage = this.getPageFromHash() || 'bank-statement';
        this.navigateToPage(initialPage, false);
    }
    
    // 觸發頁面切換事件
    dispatchPageChangeEvent(page) {
        window.dispatchEvent(new CustomEvent('pageChanged', {
            detail: { page, timestamp: Date.now() }
        }));
    }
}

// 幫助函數
function showHelp(type) {
    const helpMessages = {
        'bank-statement': 'Bank Statement Processing Help:\n\n1. 上傳銀行對帳單PDF\n2. AI自動提取交易數據\n3. 檢視和編輯結果\n4. 下載處理後的文件',
        'invoice': 'Invoice Processing Help:\n\n1. 上傳發票文件\n2. AI自動提取數據\n3. 查看和編輯結果\n4. 下載處理後的文件',
        'receipt': 'Receipt Scanning Help:\n\n1. 上傳收據圖片\n2. AI自動提取數據\n3. 查看和編輯結果\n4. 下載處理後的文件',
        'general': 'General Document Help:\n\n1. 上傳任何文檔\n2. AI自動處理\n3. 查看結果\n4. 下載文件'
    };
    
    alert(helpMessages[type] || 'Help information');
}

function openUploadModal(type) {
    console.log(`Opening upload modal for ${type}`);
    // 實現上傳模態框
}

function toggleView() {
    console.log('Toggling view');
    // 實現視圖切換
}

// 全局導出
window.ContentManager = ContentManager;

// 自動初始化
document.addEventListener('DOMContentLoaded', function() {
    if (!window.contentManager) {
        window.contentManager = new ContentManager();
    }
});

console.log('📄 Content Manager 載入完成');
