/**
 * VaultCaddy 統一文件上傳處理器
 * 處理拖拽上傳、批次處理、進度顯示和結果管理
 */

class VaultCaddyUploadHandler {
    constructor(uploadAreaSelector, documentType = 'general') {
        this.uploadArea = document.querySelector(uploadAreaSelector);
        this.documentType = documentType;
        this.fileInput = null;
        this.uploadedFiles = [];
        this.processingResults = [];
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        if (!this.uploadArea) {
            console.error('Upload area not found:', uploadAreaSelector);
            return;
        }
        
        this.createFileInput();
        this.setupEventListeners();
        this.createProgressIndicator();
        this.createResultsArea();
        
        console.log(`📤 Upload Handler 已初始化 (${this.documentType})`);
    }
    
    /**
     * 創建隱藏的文件輸入
     */
    createFileInput() {
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.multiple = true;
        this.fileInput.style.display = 'none';
        
        // 根據文檔類型設置接受的文件格式
        const acceptMap = {
            'bank-statement': '.pdf,.csv,.txt',
            'invoice': '.pdf,.jpg,.jpeg,.png',
            'receipt': '.jpg,.jpeg,.png,.pdf',
            'general': '.pdf,.jpg,.jpeg,.png,.doc,.docx,.txt'
        };
        
        this.fileInput.accept = acceptMap[this.documentType] || acceptMap['general'];
        
        document.body.appendChild(this.fileInput);
    }
    
    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 文件輸入變化
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(Array.from(e.target.files));
        });
        
        // 拖拽事件
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        
        // 點擊上傳區域
        this.uploadArea.addEventListener('click', (e) => {
            if (!e.target.closest('button')) {
                this.fileInput.click();
            }
        });
        
        // 監聽處理進度
        document.addEventListener('batchProgress', this.handleProgress.bind(this));
        document.addEventListener('documentProcessed', this.handleDocumentProcessed.bind(this));
    }
    
    /**
     * 處理拖拽懸停
     */
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('drag-over');
        this.uploadArea.style.borderColor = this.getThemeColor();
        this.uploadArea.style.backgroundColor = this.getThemeBackgroundColor();
    }
    
    /**
     * 處理拖拽離開
     */
    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
        this.uploadArea.style.borderColor = '#d1d5db';
        this.uploadArea.style.backgroundColor = '#f9fafb';
    }
    
    /**
     * 處理文件放置
     */
    handleDrop(e) {
        e.preventDefault();
        this.handleDragLeave(e);
        
        const files = Array.from(e.dataTransfer.files);
        this.handleFiles(files);
    }
    
    /**
     * 處理文件
     */
    async handleFiles(files) {
        if (!files || files.length === 0) return;
        
        console.log(`📁 收到 ${files.length} 個文件`);
        
        // 驗證文件
        const validFiles = this.validateFiles(files);
        if (validFiles.length === 0) {
            this.showError('沒有有效的文件可以處理');
            return;
        }
        
        if (validFiles.length !== files.length) {
            this.showWarning(`已過濾 ${files.length - validFiles.length} 個無效文件`);
        }
        
        this.uploadedFiles = validFiles;
        this.showFileList(validFiles);
        
        // 開始處理
        await this.processFiles(validFiles);
    }
    
    /**
     * 驗證文件
     */
    validateFiles(files) {
        const validFiles = [];
        const maxSize = 10 * 1024 * 1024; // 10MB
        
        const allowedTypes = {
            'bank-statement': ['application/pdf', 'text/csv', 'text/plain'],
            'invoice': ['application/pdf', 'image/jpeg', 'image/png'],
            'receipt': ['image/jpeg', 'image/png', 'application/pdf'],
            'general': ['application/pdf', 'image/jpeg', 'image/png', 'text/plain', 
                       'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        };
        
        const allowed = allowedTypes[this.documentType] || allowedTypes['general'];
        
        for (const file of files) {
            // 檢查文件大小
            if (file.size > maxSize) {
                console.warn(`文件 ${file.name} 超過大小限制 (${maxSize / 1024 / 1024}MB)`);
                continue;
            }
            
            // 檢查文件類型
            if (!allowed.includes(file.type)) {
                console.warn(`文件 ${file.name} 類型不支援 (${file.type})`);
                continue;
            }
            
            validFiles.push(file);
        }
        
        return validFiles;
    }
    
    /**
     * 顯示文件列表
     */
    showFileList(files) {
        const fileListContainer = this.getOrCreateFileList();
        fileListContainer.innerHTML = '';
        
        files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 6px; margin-bottom: 0.5rem; background: white;">
                    <div style="display: flex; align-items: center;">
                        <i class="fas fa-file-${this.getFileIcon(file.type)}" style="margin-right: 0.75rem; color: ${this.getThemeColor()};"></i>
                        <div>
                            <div style="font-weight: 500; color: #1f2937;">${file.name}</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">${this.formatFileSize(file.size)}</div>
                        </div>
                    </div>
                    <div class="file-status" id="status-${index}">
                        <span style="color: #6b7280;">等待處理</span>
                    </div>
                </div>
            `;
            fileListContainer.appendChild(fileItem);
        });
    }
    
    /**
     * 處理文件
     */
    async processFiles(files) {
        if (this.isProcessing) {
            this.showWarning('正在處理其他文件，請稍候...');
            return;
        }
        
        this.isProcessing = true;
        this.showProcessingIndicator(true);
        
        try {
            // 檢查用戶 Credits
            const requiredCredits = this.calculateRequiredCredits(files);
            const availableCredits = parseInt(localStorage.getItem('userCredits') || '7');
            
            if (requiredCredits > availableCredits) {
                throw new Error(`處理需要 ${requiredCredits} Credits，但您只有 ${availableCredits} Credits`);
            }
            
            // 使用批次處理
            const batchResult = await window.VaultCaddyProcessor.batchProcess(files, this.documentType, {
                maxConcurrent: 2
            });
            
            this.processingResults = batchResult.results;
            this.showResults(batchResult);
            
        } catch (error) {
            console.error('處理文件失敗:', error);
            this.showError(error.message);
        } finally {
            this.isProcessing = false;
            this.showProcessingIndicator(false);
        }
    }
    
    /**
     * 計算所需 Credits
     */
    calculateRequiredCredits(files) {
        const creditsPerType = {
            'bank-statement': 2,
            'invoice': 1,
            'receipt': 1,
            'general': 1
        };
        
        const baseCredits = creditsPerType[this.documentType] || 1;
        return files.length * baseCredits;
    }
    
    /**
     * 處理進度更新
     */
    handleProgress(event) {
        const { progress, processed, total } = event.detail;
        
        // 更新總進度
        const progressBar = document.getElementById('upload-progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        
        const progressText = document.getElementById('upload-progress-text');
        if (progressText) {
            progressText.textContent = `處理中... ${processed}/${total} (${progress}%)`;
        }
    }
    
    /**
     * 處理單個文檔完成
     */
    handleDocumentProcessed(event) {
        const { file, result } = event.detail;
        
        // 找到對應的文件狀態元素並更新
        const fileIndex = this.uploadedFiles.findIndex(f => f.name === file);
        if (fileIndex !== -1) {
            const statusElement = document.getElementById(`status-${fileIndex}`);
            if (statusElement) {
                if (result.status === 'success') {
                    statusElement.innerHTML = `<span style="color: #059669;"><i class="fas fa-check-circle"></i> 完成</span>`;
                } else {
                    statusElement.innerHTML = `<span style="color: #dc2626;"><i class="fas fa-times-circle"></i> 失敗</span>`;
                }
            }
        }
    }
    
    /**
     * 顯示結果
     */
    showResults(batchResult) {
        const resultsContainer = this.getOrCreateResultsArea();
        
        const successCount = batchResult.successfulFiles;
        const totalCount = batchResult.totalFiles;
        
        let html = `
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1.5rem; margin-top: 1.5rem;">
                <h4 style="color: #1f2937; margin: 0 0 1rem 0; display: flex; align-items: center;">
                    <i class="fas fa-chart-bar" style="margin-right: 0.5rem; color: ${this.getThemeColor()};"></i>
                    處理結果
                </h4>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="text-align: center; padding: 1rem; background: #f0fdf4; border-radius: 6px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #059669;">${successCount}</div>
                        <div style="color: #065f46;">成功處理</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: ${totalCount - successCount > 0 ? '#fef2f2' : '#f9fafb'}; border-radius: 6px;">
                        <div style="font-size: 2rem; font-weight: bold; color: ${totalCount - successCount > 0 ? '#dc2626' : '#6b7280'};">${totalCount - successCount}</div>
                        <div style="color: ${totalCount - successCount > 0 ? '#991b1b' : '#6b7280'};">處理失敗</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #eff6ff; border-radius: 6px;">
                        <div style="font-size: 2rem; font-weight: bold; color: #2563eb;">${Math.round((successCount / totalCount) * 100)}%</div>
                        <div style="color: #1d4ed8;">成功率</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    ${successCount > 0 ? `
                        <button onclick="uploadHandler.downloadResults('csv')" style="padding: 0.5rem 1rem; background: ${this.getThemeColor()}; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.875rem;">
                            <i class="fas fa-download" style="margin-right: 0.5rem;"></i>下載 CSV
                        </button>
                        <button onclick="uploadHandler.downloadResults('json')" style="padding: 0.5rem 1rem; background: #6b7280; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.875rem;">
                            <i class="fas fa-download" style="margin-right: 0.5rem;"></i>下載 JSON
                        </button>
                        ${this.documentType === 'bank-statement' ? `
                            <button onclick="uploadHandler.downloadResults('quickbooks')" style="padding: 0.5rem 1rem; background: #0077c5; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.875rem;">
                                <i class="fas fa-download" style="margin-right: 0.5rem;"></i>QuickBooks
                            </button>
                        ` : ''}
                    ` : ''}
                    <button onclick="uploadHandler.clearResults()" style="padding: 0.5rem 1rem; background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; border-radius: 4px; cursor: pointer; font-size: 0.875rem;">
                        <i class="fas fa-trash" style="margin-right: 0.5rem;"></i>清除結果
                    </button>
                </div>
            </div>
        `;
        
        resultsContainer.innerHTML = html;
    }
    
    /**
     * 下載結果
     */
    downloadResults(format) {
        if (!this.processingResults || this.processingResults.length === 0) {
            this.showError('沒有可下載的結果');
            return;
        }
        
        const successfulResults = this.processingResults.filter(r => r.status === 'success');
        if (successfulResults.length === 0) {
            this.showError('沒有成功處理的結果可下載');
            return;
        }
        
        try {
            let content, fileName, mimeType;
            
            switch (format) {
                case 'csv':
                    content = window.VaultCaddyProcessor.exportToCSV(successfulResults, this.documentType);
                    fileName = `vaultcaddy_${this.documentType}_${new Date().toISOString().split('T')[0]}.csv`;
                    mimeType = 'text/csv';
                    break;
                    
                case 'json':
                    content = window.VaultCaddyProcessor.exportToJSON(successfulResults);
                    fileName = `vaultcaddy_${this.documentType}_${new Date().toISOString().split('T')[0]}.json`;
                    mimeType = 'application/json';
                    break;
                    
                case 'quickbooks':
                    content = window.VaultCaddyProcessor.exportToQuickBooks(successfulResults, this.documentType);
                    fileName = `vaultcaddy_${this.documentType}_${new Date().toISOString().split('T')[0]}.qbo`;
                    mimeType = 'application/vnd.intu.qbo';
                    break;
                    
                default:
                    throw new Error('不支援的格式');
            }
            
            window.VaultCaddyProcessor.downloadFile(content, fileName, mimeType);
            
        } catch (error) {
            console.error('下載失敗:', error);
            this.showError(`下載失敗: ${error.message}`);
        }
    }
    
    /**
     * 清除結果
     */
    clearResults() {
        this.uploadedFiles = [];
        this.processingResults = [];
        
        const fileList = document.getElementById('upload-file-list');
        const results = document.getElementById('upload-results');
        
        if (fileList) fileList.innerHTML = '';
        if (results) results.innerHTML = '';
        
        // 重置上傳區域
        this.uploadArea.style.borderColor = '#d1d5db';
        this.uploadArea.style.backgroundColor = '#f9fafb';
    }
    
    /**
     * 獲取或創建文件列表容器
     */
    getOrCreateFileList() {
        let container = document.getElementById('upload-file-list');
        if (!container) {
            container = document.createElement('div');
            container.id = 'upload-file-list';
            container.style.marginTop = '1rem';
            this.uploadArea.parentNode.insertBefore(container, this.uploadArea.nextSibling);
        }
        return container;
    }
    
    /**
     * 獲取或創建結果區域
     */
    getOrCreateResultsArea() {
        let container = document.getElementById('upload-results');
        if (!container) {
            container = document.createElement('div');
            container.id = 'upload-results';
            this.uploadArea.parentNode.insertBefore(container, this.uploadArea.nextSibling);
        }
        return container;
    }
    
    /**
     * 創建進度指示器
     */
    createProgressIndicator() {
        const progressContainer = document.createElement('div');
        progressContainer.id = 'upload-progress';
        progressContainer.style.display = 'none';
        progressContainer.style.marginTop = '1rem';
        progressContainer.innerHTML = `
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem;">
                <div id="upload-progress-text" style="margin-bottom: 0.5rem; color: #374151; font-weight: 500;">準備處理...</div>
                <div style="background: #f3f4f6; border-radius: 4px; height: 8px; overflow: hidden;">
                    <div id="upload-progress-bar" style="background: ${this.getThemeColor()}; height: 100%; width: 0%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        `;
        
        this.uploadArea.parentNode.insertBefore(progressContainer, this.uploadArea.nextSibling);
    }
    
    /**
     * 顯示/隱藏處理指示器
     */
    showProcessingIndicator(show) {
        const progressContainer = document.getElementById('upload-progress');
        if (progressContainer) {
            progressContainer.style.display = show ? 'block' : 'none';
        }
        
        if (show) {
            const progressText = document.getElementById('upload-progress-text');
            const progressBar = document.getElementById('upload-progress-bar');
            if (progressText) progressText.textContent = '準備處理...';
            if (progressBar) progressBar.style.width = '0%';
        }
    }
    
    /**
     * 顯示錯誤信息
     */
    showError(message) {
        this.showNotification(message, 'error');
    }
    
    /**
     * 顯示警告信息
     */
    showWarning(message) {
        this.showNotification(message, 'warning');
    }
    
    /**
     * 顯示通知
     */
    showNotification(message, type = 'info') {
        const colors = {
            error: { bg: '#fef2f2', border: '#fecaca', text: '#991b1b' },
            warning: { bg: '#fffbeb', border: '#fed7aa', text: '#92400e' },
            info: { bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8' }
        };
        
        const color = colors[type] || colors.info;
        
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${color.bg};
            border: 1px solid ${color.border};
            color: ${color.text};
            padding: 1rem;
            border-radius: 8px;
            max-width: 400px;
            z-index: 10000;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // 3秒後自動移除
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    /**
     * 格式化文件大小
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    /**
     * 獲取文件圖標
     */
    getFileIcon(mimeType) {
        if (mimeType.includes('pdf')) return 'pdf';
        if (mimeType.includes('image')) return 'image';
        if (mimeType.includes('word')) return 'word';
        if (mimeType.includes('csv')) return 'csv';
        return 'alt';
    }
    
    /**
     * 獲取主題顏色
     */
    getThemeColor() {
        const colors = {
            'bank-statement': '#3b82f6',
            'invoice': '#3b82f6',
            'receipt': '#059669',
            'general': '#f59e0b'
        };
        return colors[this.documentType] || '#3b82f6';
    }
    
    /**
     * 獲取主題背景顏色
     */
    getThemeBackgroundColor() {
        const colors = {
            'bank-statement': '#eff6ff',
            'invoice': '#eff6ff',
            'receipt': '#f0fdf4',
            'general': '#fffbeb'
        };
        return colors[this.documentType] || '#eff6ff';
    }
}

// 自動初始化函數（在頁面加載時調用）
function initializeUploadHandler(uploadAreaSelector, documentType) {
    return new VaultCaddyUploadHandler(uploadAreaSelector, documentType);
}
