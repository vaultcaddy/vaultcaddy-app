// Dashboard JavaScript 功能
document.addEventListener('DOMContentLoaded', function() {
    // 初始化Dashboard
    initDashboard();
    
    function initDashboard() {
        // 檢查登入狀態
        checkAuthStatus();
        
        // 初始化各種功能
        initUploadModal();
        initFileUpload();
        initTableFunctions();
        initCreditsDisplay();
        initNavigation();
        
        console.log('Dashboard已初始化完成');
    }
    
    // 檢查登入狀態
    function checkAuthStatus() {
        const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';
        if (!isLoggedIn) {
            window.location.href = 'login.html';
            return;
        }
        
        // 設置用戶為已登入狀態
        document.body.classList.add('user-logged-in');
    }
    
    // 初始化上傳模態框
    function initUploadModal() {
        const uploadBtn = document.querySelector('.upload-btn');
        const modal = document.getElementById('upload-modal');
        const closeBtn = document.querySelector('.close-btn');
        const uploadArea = document.querySelector('.upload-area');
        const browseBtn = document.querySelector('.browse-files-btn');
        const fileInput = document.getElementById('file-upload');
        
        if (uploadBtn && modal) {
            uploadBtn.addEventListener('click', () => {
                modal.classList.add('active');
            });
        }
        
        if (closeBtn && modal) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }
        
        // 點擊模態框外部關閉
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }
        
        // 上傳區域拖放處理
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                handleFileUpload(files);
            });
            
            uploadArea.addEventListener('click', () => {
                fileInput?.click();
            });
        }
        
        if (browseBtn && fileInput) {
            browseBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                fileInput.click();
            });
        }
    }
    
    // 初始化文件上傳
    function initFileUpload() {
        const fileInput = document.getElementById('file-upload');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                handleFileUpload(e.target.files);
            });
        }
    }
    
    // 處理文件上傳
    function handleFileUpload(files) {
        if (!files || files.length === 0) return;
        
        const userCredits = parseInt(localStorage.getItem('userCredits') || '10');
        let totalCreditsNeeded = 0;
        
        // 計算所需Credits
        Array.from(files).forEach(file => {
            if (file.type === 'application/pdf') {
                // 模擬：每個PDF文件需要1-5個Credits
                totalCreditsNeeded += Math.floor(Math.random() * 5) + 1;
            }
        });
        
        if (userCredits < totalCreditsNeeded) {
            showNotification(`Credits不足！需要 ${totalCreditsNeeded} Credits，您當前有 ${userCredits} Credits。`, 'error');
            return;
        }
        
        // 處理文件上傳
        processFiles(files, totalCreditsNeeded);
    }
    
    // 處理文件
    function processFiles(files, creditsUsed) {
        // 關閉模態框
        const modal = document.getElementById('upload-modal');
        if (modal) {
            modal.classList.remove('active');
        }
        
        // 顯示處理中狀態
        showNotification('正在處理文件...', 'info');
        
        // 模擬文件處理
        setTimeout(() => {
            // 扣除Credits
            const currentCredits = parseInt(localStorage.getItem('userCredits') || '10');
            const newCredits = currentCredits - creditsUsed;
            localStorage.setItem('userCredits', newCredits.toString());
            updateCreditsDisplay();
            
            // 添加文件到表格
            addFilesToTable(files);
            
            showNotification(`成功處理 ${files.length} 個文件，使用了 ${creditsUsed} Credits`, 'success');
        }, 2000);
    }
    
    // 添加文件到表格
    function addFilesToTable(files) {
        const tbody = document.getElementById('documents-tbody');
        if (!tbody) return;
        
        Array.from(files).forEach((file, index) => {
            const row = createDocumentRow(file, index);
            tbody.appendChild(row);
        });
        
        updateTableInfo();
    }
    
    // 創建文檔行
    function createDocumentRow(file, index) {
        const row = document.createElement('tr');
        row.className = 'document-row';
        
        const fileName = file.name.length > 20 ? file.name.substring(0, 20) + '...' : file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2) + ' MB';
        const uploadTime = new Date().toLocaleString();
        
        row.innerHTML = `
            <td>
                <input type="checkbox">
                <div class="document-info">
                    <i class="fas fa-file-pdf"></i>
                    <div>
                        <strong>${fileName}</strong>
                        <small>${fileSize} • 上傳時間: ${uploadTime}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="period-info">
                    <strong>處理中...</strong>
                    <small>分析交易中</small>
                </div>
            </td>
            <td>
                <div class="reconciliation">
                    <span class="reconciliation-fraction">0/0</span>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <span class="status-indicator in-progress">處理中</span>
                </div>
            </td>
            <td>
                <div class="balance-info">
                    <div>Start: <strong>計算中...</strong></div>
                    <div>End: <strong>計算中...</strong></div>
                </div>
            </td>
            <td>
                <span class="status-badge" style="background: #374151; color: #9ca3af;">
                    <i class="fas fa-clock"></i>
                    處理中
                </span>
            </td>
            <td>
                <span class="status-badge" style="background: #374151; color: #9ca3af;">
                    <i class="fas fa-hourglass-half"></i>
                    等待中
                </span>
            </td>
            <td>新上傳</td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn" title="View" onclick="viewDocument('${file.name}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn" title="Download" onclick="downloadDocument('${file.name}')">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="action-btn" title="Delete" onclick="deleteDocument(this)">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        // 模擬處理完成
        setTimeout(() => {
            updateRowAfterProcessing(row);
        }, 3000 + index * 1000);
        
        return row;
    }
    
    // 處理完成後更新行
    function updateRowAfterProcessing(row) {
        const periodInfo = row.querySelector('.period-info');
        const reconciliation = row.querySelector('.reconciliation');
        const balanceInfo = row.querySelector('.balance-info');
        const statusBadge = row.querySelector('.status-badge');
        const reviewBadge = row.querySelectorAll('.status-badge')[1];
        
        if (periodInfo) {
            periodInfo.innerHTML = `
                <strong>${generateRandomPeriod()}</strong>
                <small>${Math.floor(Math.random() * 50) + 1} transactions</small>
            `;
        }
        
        if (reconciliation) {
            const total = Math.floor(Math.random() * 50) + 1;
            const completed = Math.floor(Math.random() * total);
            reconciliation.innerHTML = `
                <span class="reconciliation-fraction">${completed}/${total}</span>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(completed/total)*100}%"></div>
                </div>
                <span class="status-indicator in-progress">已完成</span>
            `;
        }
        
        if (balanceInfo) {
            const startBalance = (Math.random() * 100000).toFixed(2);
            const endBalance = (Math.random() * 100000).toFixed(2);
            balanceInfo.innerHTML = `
                <div>Start: <strong>$${startBalance}</strong></div>
                <div>End: <strong>$${endBalance}</strong></div>
            `;
        }
        
        if (statusBadge) {
            statusBadge.className = 'status-badge success';
            statusBadge.innerHTML = `
                <i class="fas fa-check-circle"></i>
                Success
            `;
        }
        
        if (reviewBadge) {
            reviewBadge.className = 'status-badge review';
            reviewBadge.innerHTML = `
                <i class="fas fa-exclamation-circle"></i>
                Review
            `;
        }
    }
    
    // 生成隨機日期範圍
    function generateRandomPeriod() {
        const start = new Date();
        start.setDate(start.getDate() - Math.floor(Math.random() * 90));
        const end = new Date(start);
        end.setDate(end.getDate() + 30);
        
        return `${start.toLocaleDateString()} to ${end.toLocaleDateString()}`;
    }
    
    // 初始化表格功能
    function initTableFunctions() {
        // 全選功能
        const selectAll = document.querySelector('.select-all');
        if (selectAll) {
            selectAll.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
                checkboxes.forEach(cb => cb.checked = this.checked);
                updateTableInfo();
            });
        }
        
        // 行選擇
        document.addEventListener('change', function(e) {
            if (e.target.type === 'checkbox' && e.target.closest('tbody')) {
                updateTableInfo();
                
                const row = e.target.closest('tr');
                if (row) {
                    row.classList.toggle('selected', e.target.checked);
                }
            }
        });
        
        // 過濾功能
        const filterInput = document.querySelector('.filter-input');
        if (filterInput) {
            filterInput.addEventListener('input', function() {
                filterTable(this.value);
            });
        }
    }
    
    // 更新表格資訊
    function updateTableInfo() {
        const selectedCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]:checked');
        const totalRows = document.querySelectorAll('tbody tr').length;
        const paginationInfo = document.querySelector('.pagination-info');
        
        if (paginationInfo) {
            paginationInfo.textContent = `${selectedCheckboxes.length} of ${totalRows} row(s) selected.`;
        }
    }
    
    // 過濾表格
    function filterTable(searchTerm) {
        const rows = document.querySelectorAll('tbody tr');
        const term = searchTerm.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    }
    
    // 初始化Credits顯示
    function initCreditsDisplay() {
        updateCreditsDisplay();
    }
    
    // 更新Credits顯示
    function updateCreditsDisplay() {
        const userCredits = localStorage.getItem('userCredits') || '10';
        const creditsDisplay = document.getElementById('dashboard-credits');
        if (creditsDisplay) {
            creditsDisplay.textContent = userCredits;
        }
    }
    
    // 初始化導航
    function initNavigation() {
        // 側邊欄導航點擊
        const navItems = document.querySelectorAll('.nav-item a');
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // 移除所有active狀態
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                // 添加active到當前項目
                this.closest('.nav-item').classList.add('active');
            });
        });
    }
    
    // 顯示通知
    function showNotification(message, type = 'info') {
        // 移除現有通知
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // 樣式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1001;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // 動畫顯示
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // 關閉按鈕
        const closeBtn = notification.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                removeNotification(notification);
            });
        }
        
        // 自動移除
        setTimeout(() => {
            removeNotification(notification);
        }, 5000);
    }
    
    // 移除通知
    function removeNotification(notification) {
        if (notification && notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }
    
    // 檢查是否有待處理的文檔類型
    const pendingDocumentType = localStorage.getItem('pendingDocumentType');
    if (pendingDocumentType) {
        localStorage.removeItem('pendingDocumentType');
        // 可以根據文檔類型執行特定操作
        console.log('處理待處理的文檔類型:', pendingDocumentType);
    }
});

// 全局函數
function viewDocument(fileName) {
    showNotification(`查看文檔: ${fileName}`, 'info');
}

function downloadDocument(fileName) {
    showNotification(`下載文檔: ${fileName}`, 'success');
}

function deleteDocument(button) {
    const row = button.closest('tr');
    if (row && confirm('確定要刪除此文檔嗎？')) {
        row.remove();
        updateTableInfo();
        showNotification('文檔已刪除', 'success');
    }
}

function updateTableInfo() {
    const selectedCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]:checked');
    const totalRows = document.querySelectorAll('tbody tr').length;
    const paginationInfo = document.querySelector('.pagination-info');
    
    if (paginationInfo) {
        paginationInfo.textContent = `${selectedCheckboxes.length} of ${totalRows} row(s) selected.`;
    }
}
