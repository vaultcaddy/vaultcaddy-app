/**
 * VaultCaddy 文檔管理器
 * 統一的文檔列表、過濾、操作功能
 */

class DocumentManager {
    constructor(documentType) {
        this.documentType = documentType;
        this.documents = [];
        this.filteredDocuments = [];
        this.selectedDocuments = new Set();
        this.currentView = 'list';
        
        this.init();
    }
    
    init() {
        this.loadMockData();
        this.setupEventListeners();
        this.render();
    }
    
    loadMockData() {
        // 根據文檔類型載入不同的模擬數據
        const mockData = {
            'bank-statement': [
                {
                    id: 'doc_001',
                    name: 'eStatementFile_2025_02.pdf',
                    details: 'MR YEUNG CAVLIN\n760-452064-882 • MIPSSTM',
                    period: '02/01/2025 to 03/22/2025',
                    transactions: 13,
                    reconciliation: { completed: 4, total: 13, percentage: 31 },
                    balance: { start: 121080.49, end: 30188.66 },
                    status: 'success',
                    reviewStatus: 'review',
                    notes: '—',
                    uploadDate: '2025/8/29',
                    processingStatus: 'In Progress'
                }
            ],
            'invoice': [
                {
                    id: 'inv_001',
                    name: 'Invoice_2025_001.pdf',
                    details: 'ABC Company Ltd\nINV-2025-001',
                    vendor: 'ABC Company Ltd',
                    amount: 5420.00,
                    dueDate: '2025/09/15',
                    status: 'success',
                    reviewStatus: 'approved',
                    notes: 'Payment processed',
                    uploadDate: '2025/8/29',
                    processingStatus: 'Completed'
                }
            ],
            'receipt': [
                {
                    id: 'rec_001',
                    name: 'Receipt_Store_001.jpg',
                    details: 'Store Receipt\nTransaction #12345',
                    merchant: 'Local Store',
                    amount: 85.30,
                    date: '2025/08/25',
                    status: 'success',
                    reviewStatus: 'approved',
                    notes: 'Business expense',
                    uploadDate: '2025/8/29',
                    processingStatus: 'Completed'
                }
            ],
            'general': [
                {
                    id: 'gen_001',
                    name: 'Document_001.pdf',
                    details: 'General Document\nMixed content',
                    category: 'Miscellaneous',
                    pages: 5,
                    status: 'success',
                    reviewStatus: 'pending',
                    notes: 'Needs review',
                    uploadDate: '2025/8/29',
                    processingStatus: 'Completed'
                }
            ]
        };
        
        this.documents = mockData[this.documentType] || [];
        this.filteredDocuments = [...this.documents];
    }
    
    setupEventListeners() {
        // 過濾輸入
        const filterInput = document.querySelector('.filter-input');
        if (filterInput) {
            filterInput.addEventListener('input', (e) => {
                this.filterDocuments(e.target.value);
            });
        }
        
        // 上傳按鈕
        const uploadBtn = document.querySelector('.upload-btn');
        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => {
                this.openUploadModal();
            });
        }
        
        // 查看切換按鈕
        const viewBtn = document.querySelector('.view-btn');
        if (viewBtn) {
            viewBtn.addEventListener('click', () => {
                this.toggleView();
            });
        }
        
        // 全選checkbox
        const selectAllCheckbox = document.querySelector('.select-all');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                this.toggleSelectAll(e.target.checked);
            });
        }
    }
    
    filterDocuments(query) {
        if (!query.trim()) {
            this.filteredDocuments = [...this.documents];
        } else {
            this.filteredDocuments = this.documents.filter(doc => 
                doc.name.toLowerCase().includes(query.toLowerCase()) ||
                doc.details.toLowerCase().includes(query.toLowerCase())
            );
        }
        this.renderTable();
    }
    
    render() {
        this.renderTable();
        this.updateSelectionInfo();
    }
    
    renderTable() {
        const tableBody = document.querySelector('.documents-grid tbody');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        if (this.filteredDocuments.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 2rem; color: #6b7280;">
                        <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                        No documents found
                    </td>
                </tr>
            `;
            return;
        }
        
        this.filteredDocuments.forEach(doc => {
            const row = this.createDocumentRow(doc);
            tableBody.appendChild(row);
        });
    }
    
    createDocumentRow(doc) {
        const row = document.createElement('tr');
        row.setAttribute('data-doc-id', doc.id);
        row.style.cursor = 'pointer';
        row.addEventListener('click', (e) => this.handleRowClick(e, doc.id));
        
        // 根據文檔類型生成不同的表格內容
        if (this.documentType === 'bank-statement') {
            row.innerHTML = this.createBankStatementRow(doc);
        } else if (this.documentType === 'invoice') {
            row.innerHTML = this.createInvoiceRow(doc);
        } else if (this.documentType === 'receipt') {
            row.innerHTML = this.createReceiptRow(doc);
        } else {
            row.innerHTML = this.createGeneralRow(doc);
        }
        
        return row;
    }
    
    createBankStatementRow(doc) {
        return `
            <td>
                <div class="document-cell">
                    <input type="checkbox" data-doc-id="${doc.id}">
                    <i class="fas fa-file-pdf file-icon"></i>
                    <div class="document-info">
                        <span class="doc-name" onclick="openDocumentDetail('${doc.id}')">${doc.name}</span>
                        <small class="doc-details">${doc.details.replace(/\n/g, '<br>')}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="period-info">
                    📅 ${doc.period}
                    <br><small>${doc.transactions} transactions</small>
                </div>
            </td>
            <td>
                <div class="reconciliation">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${doc.reconciliation.percentage}%"></div>
                    </div>
                    <span class="progress-text">${doc.reconciliation.completed}/${doc.reconciliation.total} ${doc.reconciliation.percentage}%</span>
                    <small class="status-text">🔄 ${doc.processingStatus}</small>
                </div>
            </td>
            <td>
                <div class="balance-info">
                    <div>Start: $${doc.balance.start.toLocaleString()}</div>
                    <div>End: $${doc.balance.end.toLocaleString()}</div>
                </div>
            </td>
            <td>
                <div class="status-review-cell">
                    <span class="status-badge ${doc.status}">✅ Success</span>
                    <span class="review-badge ${doc.reviewStatus}">🔍 Review</span>
                </div>
            </td>
            <td>
                <div class="action-cell">
                    <span class="notes">${doc.notes}</span>
                    <button class="action-menu-btn" onclick="showActionMenu(event, '${doc.id}')" title="更多操作">
                        <i class="fas fa-ellipsis-h"></i>
                    </button>
                </div>
            </td>
        `;
    }
    
    createInvoiceRow(doc) {
        return `
            <td>
                <div class="document-cell">
                    <input type="checkbox" data-doc-id="${doc.id}">
                    <i class="fas fa-file-invoice file-icon"></i>
                    <div class="document-info">
                        <span class="doc-name" onclick="openDocumentDetail('${doc.id}')">${doc.name}</span>
                        <small class="doc-details">${doc.details.replace(/\n/g, '<br>')}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="vendor-info">
                    🏢 ${doc.vendor}
                    <br><small>Due: ${doc.dueDate}</small>
                </div>
            </td>
            <td>
                <div class="amount-info">
                    <strong>$${doc.amount.toLocaleString()}</strong>
                    <br><small class="status-text">💰 Invoice Amount</small>
                </div>
            </td>
            <td>
                <div class="status-info">
                    📅 ${doc.uploadDate}
                    <br><small>${doc.processingStatus}</small>
                </div>
            </td>
            <td>
                <div class="status-review-cell">
                    <span class="status-badge ${doc.status}">✅ Success</span>
                    <span class="review-badge ${doc.reviewStatus}">✓ Approved</span>
                </div>
            </td>
            <td>
                <div class="action-cell">
                    <span class="notes">${doc.notes}</span>
                    <button class="action-menu-btn" onclick="showActionMenu(event, '${doc.id}')" title="更多操作">
                        <i class="fas fa-ellipsis-h"></i>
                    </button>
                </div>
            </td>
        `;
    }
    
    createReceiptRow(doc) {
        return `
            <td>
                <div class="document-cell">
                    <input type="checkbox" data-doc-id="${doc.id}">
                    <i class="fas fa-receipt file-icon"></i>
                    <div class="document-info">
                        <span class="doc-name" onclick="openDocumentDetail('${doc.id}')">${doc.name}</span>
                        <small class="doc-details">${doc.details.replace(/\n/g, '<br>')}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="merchant-info">
                    🏪 ${doc.merchant}
                    <br><small>${doc.date}</small>
                </div>
            </td>
            <td>
                <div class="amount-info">
                    <strong>$${doc.amount.toLocaleString()}</strong>
                    <br><small class="status-text">💳 Receipt Total</small>
                </div>
            </td>
            <td>
                <div class="status-info">
                    📅 ${doc.uploadDate}
                    <br><small>${doc.processingStatus}</small>
                </div>
            </td>
            <td>
                <div class="status-review-cell">
                    <span class="status-badge ${doc.status}">✅ Success</span>
                    <span class="review-badge ${doc.reviewStatus}">✓ Approved</span>
                </div>
            </td>
            <td>
                <div class="action-cell">
                    <span class="notes">${doc.notes}</span>
                    <button class="action-menu-btn" onclick="showActionMenu(event, '${doc.id}')" title="更多操作">
                        <i class="fas fa-ellipsis-h"></i>
                    </button>
                </div>
            </td>
        `;
    }
    
    createGeneralRow(doc) {
        return `
            <td>
                <div class="document-cell">
                    <input type="checkbox" data-doc-id="${doc.id}">
                    <i class="fas fa-file-alt file-icon"></i>
                    <div class="document-info">
                        <span class="doc-name" onclick="openDocumentDetail('${doc.id}')">${doc.name}</span>
                        <small class="doc-details">${doc.details.replace(/\n/g, '<br>')}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="category-info">
                    📂 ${doc.category}
                    <br><small>${doc.pages} pages</small>
                </div>
            </td>
            <td>
                <div class="processing-info">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 100%"></div>
                    </div>
                    <span class="progress-text">Complete</span>
                    <small class="status-text">✅ ${doc.processingStatus}</small>
                </div>
            </td>
            <td>
                <div class="status-info">
                    📅 ${doc.uploadDate}
                    <br><small>General Document</small>
                </div>
            </td>
            <td>
                <div class="status-review-cell">
                    <span class="status-badge ${doc.status}">✅ Success</span>
                    <span class="review-badge ${doc.reviewStatus}">⏳ Pending</span>
                </div>
            </td>
            <td>
                <div class="action-cell">
                    <span class="notes">${doc.notes}</span>
                    <button class="action-menu-btn" onclick="showActionMenu(event, '${doc.id}')" title="更多操作">
                        <i class="fas fa-ellipsis-h"></i>
                    </button>
                </div>
            </td>
        `;
    }
    
    handleRowClick(event, docId) {
        // 如果點擊的是checkbox或操作按鈕，不處理行選擇
        if (event.target.type === 'checkbox' || 
            event.target.closest('.action-menu-btn') || 
            event.target.closest('.doc-name')) {
            return;
        }
        
        const checkbox = event.currentTarget.querySelector(`input[data-doc-id="${docId}"]`);
        if (checkbox) {
            checkbox.checked = !checkbox.checked;
            this.toggleDocumentSelection(docId, checkbox.checked);
        }
    }
    
    toggleDocumentSelection(docId, selected) {
        if (selected) {
            this.selectedDocuments.add(docId);
        } else {
            this.selectedDocuments.delete(docId);
        }
        
        this.updateRowHighlight(docId, selected);
        this.updateSelectionInfo();
        this.updateSelectAllCheckbox();
    }
    
    updateRowHighlight(docId, selected) {
        const row = document.querySelector(`tr[data-doc-id="${docId}"]`);
        if (row) {
            if (selected) {
                row.classList.add('selected');
                row.style.background = '#1f2937';
                row.style.color = '#ffffff';
            } else {
                row.classList.remove('selected');
                row.style.background = '';
                row.style.color = '';
            }
        }
    }
    
    toggleSelectAll(selectAll) {
        this.selectedDocuments.clear();
        
        const checkboxes = document.querySelectorAll('input[data-doc-id]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAll;
            const docId = checkbox.getAttribute('data-doc-id');
            if (selectAll) {
                this.selectedDocuments.add(docId);
            }
            this.updateRowHighlight(docId, selectAll);
        });
        
        this.updateSelectionInfo();
    }
    
    updateSelectAllCheckbox() {
        const selectAllCheckbox = document.querySelector('.select-all');
        if (selectAllCheckbox) {
            const totalDocs = this.filteredDocuments.length;
            const selectedCount = this.selectedDocuments.size;
            
            selectAllCheckbox.checked = selectedCount === totalDocs && totalDocs > 0;
            selectAllCheckbox.indeterminate = selectedCount > 0 && selectedCount < totalDocs;
        }
    }
    
    updateSelectionInfo() {
        const selectedCount = this.selectedDocuments.size;
        const totalCount = this.filteredDocuments.length;
        
        // 更新選擇信息顯示
        const selectionInfo = document.querySelector('.selection-info');
        if (selectionInfo) {
            selectionInfo.textContent = `${selectedCount} of ${totalCount} row(s) selected.`;
        }
    }
    
    openUploadModal() {
        // 觸發文件上傳
        if (window.uploadHandler) {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = '.pdf,.jpg,.jpeg,.png';
            fileInput.multiple = true;
            fileInput.onchange = (e) => {
                if (e.target.files.length > 0) {
                    window.uploadHandler.handleFiles(Array.from(e.target.files));
                }
            };
            fileInput.click();
        }
    }
    
    toggleView() {
        this.currentView = this.currentView === 'list' ? 'grid' : 'list';
        console.log('切換查看模式:', this.currentView);
    }
}

// 全局操作函數
function showActionMenu(event, docId) {
    event.preventDefault();
    event.stopPropagation();
    
    // 移除現有的操作選單
    const existingMenu = document.querySelector('.action-menu');
    if (existingMenu) {
        existingMenu.remove();
    }
    
    // 創建操作選單
    const menu = document.createElement('div');
    menu.className = 'action-menu';
    menu.innerHTML = `
        <div class="action-menu-item" onclick="approveDocument('${docId}')">
            <i class="fas fa-check"></i>
            <span>Approve</span>
        </div>
        <div class="action-menu-item" onclick="reprocessDocument('${docId}')">
            <i class="fas fa-redo"></i>
            <span>Re-process</span>
        </div>
        <div class="action-menu-item" onclick="downloadDocument('${docId}')">
            <i class="fas fa-download"></i>
            <span>Download</span>
        </div>
        <div class="action-menu-item delete" onclick="deleteDocument('${docId}')">
            <i class="fas fa-trash"></i>
            <span>Delete</span>
        </div>
    `;
    
    // 定位選單
    const rect = event.currentTarget.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.top = (rect.bottom + 5) + 'px';
    menu.style.left = (rect.left - 150) + 'px';
    menu.style.zIndex = '1000';
    
    document.body.appendChild(menu);
    
    // 點擊外部關閉選單
    setTimeout(() => {
        document.addEventListener('click', function closeMenu() {
            menu.remove();
            document.removeEventListener('click', closeMenu);
        });
    }, 100);
}

function openDocumentDetail(docId) {
    // 導航到文檔詳細頁面
    window.location.href = `document-detail.html?id=${docId}`;
}

function approveDocument(docId) {
    console.log('批准文檔:', docId);
    // 實現批准邏輯
}

function reprocessDocument(docId) {
    console.log('重新處理文檔:', docId);
    // 實現重新處理邏輯
}

function downloadDocument(docId) {
    console.log('下載文檔:', docId);
    // 實現下載邏輯
}

function deleteDocument(docId) {
    if (confirm('確定要刪除這個文檔嗎？')) {
        console.log('刪除文檔:', docId);
        // 實現刪除邏輯
    }
}

// 導出類
window.DocumentManager = DocumentManager;
