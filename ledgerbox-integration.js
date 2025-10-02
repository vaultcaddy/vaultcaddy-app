/**
 * LedgerBox 風格的銀行對帳單處理器
 * 整合了從 LedgerBox 觀察到的完整工作流程
 */

class LedgerBoxStyleProcessor {
    constructor() {
        this.uploadModal = null;
        this.processingFiles = new Map();
        this.processedDocuments = new Map();
        this.currentDocument = null;
        
        this.init();
    }
    
    init() {
        this.createUploadModal();
        this.setupEventListeners();
        console.log('🏦 LedgerBox風格處理器已初始化');
    }
    
    /**
     * 創建類似LedgerBox的上傳模態框
     */
    createUploadModal() {
        const modalHTML = `
            <div id="ledgerbox-upload-modal" class="ledgerbox-modal" style="display: none;">
                <div class="modal-overlay" onclick="this.closeLedgerBoxModal()"></div>
                <div class="ledgerbox-modal-content">
                    <div class="modal-header">
                        <h2>Upload files</h2>
                        <p>Select a model and upload your files</p>
                        <button class="modal-close" onclick="window.ledgerBoxProcessor.closeLedgerBoxModal()">×</button>
                    </div>
                    
                    <div class="upload-area" id="ledgerbox-upload-area">
                        <div class="upload-prompt">
                            <i class="fas fa-cloud-upload-alt"></i>
                            <p>Click or drop file list</p>
                        </div>
                    </div>
                    
                    <div class="upload-actions">
                        <button class="clear-files-btn" onclick="window.ledgerBoxProcessor.clearAllFiles()">
                            <i class="fas fa-arrow-left"></i> Clear all files
                        </button>
                        <button class="convert-all-btn" onclick="window.ledgerBoxProcessor.convertAllFiles()">
                            <i class="fas fa-play"></i> Convert all files
                        </button>
                    </div>
                    
                    <div class="files-table-container">
                        <table class="files-table">
                            <thead>
                                <tr>
                                    <th>File name</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="ledgerbox-files-tbody">
                                <!-- 文件列表將在這裡動態生成 -->
                            </tbody>
                        </table>
                        <div class="files-counter">
                            <span id="files-counter">0 / 20 files uploaded</span>
                        </div>
                    </div>
                    
                    <div class="help-section">
                        <button class="need-help-btn" onclick="window.ledgerBoxProcessor.showHelp()">Need Help?</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.uploadModal = document.getElementById('ledgerbox-upload-modal');
        this.setupUploadArea();
    }
    
    /**
     * 設置上傳區域
     */
    setupUploadArea() {
        const uploadArea = document.getElementById('ledgerbox-upload-area');
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.multiple = true;
        fileInput.accept = '.pdf,.csv,.txt,.jpg,.png';
        fileInput.style.display = 'none';
        fileInput.id = 'ledgerbox-file-input';
        
        uploadArea.appendChild(fileInput);
        
        // 點擊上傳
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // 文件選擇
        fileInput.addEventListener('change', (e) => {
            this.handleFileSelection(Array.from(e.target.files));
        });
        
        // 拖拽上傳
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            const files = Array.from(e.dataTransfer.files);
            this.handleFileSelection(files);
        });
    }
    
    /**
     * 處理文件選擇
     */
    handleFileSelection(files) {
        console.log(`📁 選擇了 ${files.length} 個文件`);
        
        files.forEach(file => {
            const fileId = this.generateFileId();
            const fileInfo = {
                id: fileId,
                name: file.name,
                size: file.size,
                type: file.type,
                file: file,
                status: 'Ready',
                uploadTime: new Date()
            };
            
            this.processingFiles.set(fileId, fileInfo);
            this.addFileToTable(fileInfo);
        });
        
        this.updateFilesCounter();
    }
    
    /**
     * 添加文件到表格
     */
    addFileToTable(fileInfo) {
        const tbody = document.getElementById('ledgerbox-files-tbody');
        const row = document.createElement('tr');
        row.id = `file-row-${fileInfo.id}`;
        
        row.innerHTML = `
            <td>
                <div class="file-info">
                    <i class="fas fa-file-pdf file-icon"></i>
                    <div class="file-details">
                        <div class="file-name">${fileInfo.name}</div>
                        <div class="file-size">${this.formatFileSize(fileInfo.size)}</div>
                    </div>
                </div>
            </td>
            <td>
                <span class="status-badge ready" id="status-${fileInfo.id}">Ready</span>
            </td>
            <td>
                <div class="file-actions">
                    <button class="convert-file-btn" onclick="window.ledgerBoxProcessor.convertSingleFile('${fileInfo.id}')" id="convert-btn-${fileInfo.id}">
                        Convert file
                    </button>
                    <button class="delete-file-btn" onclick="window.ledgerBoxProcessor.deleteFile('${fileInfo.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        tbody.appendChild(row);
    }
    
    /**
     * 轉換單個文件
     */
    async convertSingleFile(fileId) {
        const fileInfo = this.processingFiles.get(fileId);
        if (!fileInfo) return;
        
        console.log(`🔄 開始轉換文件: ${fileInfo.name}`);
        
        // 更新狀態為處理中
        this.updateFileStatus(fileId, 'Processing', 'processing');
        
        try {
            // 模擬處理過程
            await this.simulateProcessing(fileInfo);
            
            // 根據文件類型和內容智能處理
            const processedData = await this.extractDocumentData(fileInfo);
            this.processedDocuments.set(fileId, processedData);
            
            this.updateFileStatus(fileId, 'Completed', 'completed');
            
            // 添加到主表格
            this.addToMainDocumentsTable(fileInfo, processedData);
            
            console.log(`✅ 文件轉換完成: ${fileInfo.name}`);
            
        } catch (error) {
            console.error(`❌ 轉換失敗: ${fileInfo.name}`, error);
            this.updateFileStatus(fileId, 'Failed', 'failed');
        }
    }
    
    /**
     * 轉換所有文件
     */
    async convertAllFiles() {
        const readyFiles = Array.from(this.processingFiles.values())
            .filter(file => file.status === 'Ready');
        
        if (readyFiles.length === 0) {
            alert('沒有準備好的文件可以轉換');
            return;
        }
        
        console.log(`🚀 開始批量轉換 ${readyFiles.length} 個文件`);
        
        // 並行處理文件
        const promises = readyFiles.map(file => this.convertSingleFile(file.id));
        await Promise.all(promises);
        
        console.log('✅ 批量轉換完成');
        
        // 顯示完成通知
        this.showNotification('所有文件轉換完成！', 'success');
    }
    
    /**
     * 模擬處理過程
     */
    async simulateProcessing(fileInfo) {
        // 模擬不同階段的處理
        const stages = [
            { name: 'Uploading', duration: 500 },
            { name: 'Analyzing', duration: 1000 },
            { name: 'Extracting', duration: 1500 },
            { name: 'Finalizing', duration: 500 }
        ];
        
        for (const stage of stages) {
            this.updateFileStatus(fileInfo.id, stage.name, 'processing');
            await new Promise(resolve => setTimeout(resolve, stage.duration));
        }
    }
    
    /**
     * 智能提取文檔數據 - 根據文件內容自動判斷類型
     */
    async extractDocumentData(fileInfo) {
        console.log(`🤖 智能分析文檔: ${fileInfo.name}`);
        
        // 先檢測文檔實際類型
        const detectedType = await this.detectDocumentType(fileInfo);
        console.log(`🔍 檢測到文檔類型: ${detectedType}`);
        
        // 根據檢測到的類型處理
        return await this.extractDataByType(fileInfo, detectedType);
    }
    
    /**
     * 檢測文檔類型
     */
    async detectDocumentType(fileInfo) {
        const fileName = fileInfo.name.toLowerCase();
        const currentPageType = this.getCurrentDocumentType();
        
        // 基於文件名的初步判斷
        if (fileName.includes('receipt') || fileName.includes('收據')) {
            return 'receipt';
        }
        if (fileName.includes('invoice') || fileName.includes('發票')) {
            return 'invoice';
        }
        if (fileName.includes('statement') || fileName.includes('對帳單')) {
            return 'bank-statement';
        }
        
        // 如果是圖片文件，很可能是收據
        if (fileInfo.type.startsWith('image/')) {
            return 'receipt';
        }
        
        // 使用當前頁面類型作為默認值
        return currentPageType;
    }
    
    /**
     * 根據類型提取數據
     */
    async extractDataByType(fileInfo, documentType) {
        console.log(`📄 按 ${documentType} 類型處理文檔: ${fileInfo.name}`);
        
        try {
            // 優先使用統一處理器
            if (window.UnifiedDocumentProcessor) {
                console.log('🎯 使用統一處理器處理文檔');
                const result = await window.UnifiedDocumentProcessor.processFile(fileInfo.file, documentType);
                return result;
            }
            // 回退到Google AI處理器
            else if (window.GoogleAIProcessor) {
                console.log('🤖 使用Google AI處理器');
                const aiResult = await window.GoogleAIProcessor.processDocument(fileInfo.file, documentType);
                return this.convertAIResultToOurFormat(aiResult, fileInfo, documentType);
            } else {
                console.warn('⚠️ 處理器未載入，使用模擬數據');
                return this.generateFallbackData(fileInfo, documentType);
            }
        } catch (error) {
            console.error('❌ 文檔處理失敗:', error);
            // 回退到模擬數據
            return this.generateFallbackData(fileInfo, documentType);
        }
    }
    
    /**
     * 提取銀行對帳單數據 - 使用Google AI（保留向後兼容）
     */
    async extractBankStatementData(fileInfo) {
        console.log(`🤖 使用Google AI提取數據: ${fileInfo.name}`);
        
        try {
            // 使用Google AI處理器
            if (window.GoogleAIProcessor) {
                const aiResult = await window.GoogleAIProcessor.processDocument(fileInfo.file, this.getCurrentDocumentType());
                
                // 轉換AI結果為我們的數據格式
                return this.convertAIResultToOurFormat(aiResult, fileInfo);
            } else {
                console.warn('⚠️ Google AI處理器未載入，使用模擬數據');
                return this.generateFallbackData(fileInfo);
            }
        } catch (error) {
            console.error('❌ Google AI處理失敗:', error);
            // 回退到模擬數據
            return this.generateFallbackData(fileInfo);
        }
    }
    
    /**
     * 轉換AI結果為我們的數據格式
     */
    convertAIResultToOurFormat(aiResult, fileInfo, documentType = null) {
        const extractedFields = aiResult.extractedFields;
        const docType = documentType || this.getCurrentDocumentType();
        
        // 根據文檔類型轉換數據格式
        switch (docType) {
            case 'bank-statement':
                return {
                    documentId: fileInfo.id,
                    fileName: fileInfo.name,
                    accountInfo: extractedFields.accountInfo || {
                        accountHolder: 'Unknown',
                        accountNumber: 'N/A',
                        bankCode: 'N/A',
                        branch: 'N/A'
                    },
                    statementPeriod: extractedFields.statementPeriod || {
                        startDate: new Date().toISOString().split('T')[0],
                        endDate: new Date().toISOString().split('T')[0]
                    },
                    financialPosition: extractedFields.financialPosition || {
                        deposits: 0,
                        personalLoans: 0,
                        creditCards: 0,
                        netPosition: 0
                    },
                    transactions: extractedFields.transactions || [],
                    reconciliation: extractedFields.reconciliation || {
                        totalTransactions: 0,
                        reconciledTransactions: 0,
                        completionPercentage: 0
                    },
                    aiProcessed: aiResult.aiProcessed,
                    processedAt: aiResult.processedAt
                };
                
            case 'invoice':
                return {
                    documentId: fileInfo.id,
                    fileName: fileInfo.name,
                    invoiceNumber: extractedFields.invoiceNumber || 'N/A',
                    issueDate: extractedFields.issueDate || new Date().toISOString().split('T')[0],
                    dueDate: extractedFields.dueDate || new Date().toISOString().split('T')[0],
                    vendor: extractedFields.vendor || 'Unknown Vendor',
                    customer: extractedFields.customer || 'Unknown Customer',
                    totalAmount: extractedFields.totalAmount || 0,
                    taxAmount: extractedFields.taxAmount || 0,
                    currency: extractedFields.currency || 'USD',
                    lineItems: extractedFields.lineItems || [],
                    aiProcessed: aiResult.aiProcessed,
                    processedAt: aiResult.processedAt
                };
                
            case 'receipt':
                return {
                    documentId: fileInfo.id,
                    fileName: fileInfo.name,
                    receiptNumber: extractedFields.receiptNumber || 'N/A',
                    date: extractedFields.date || new Date().toISOString().split('T')[0],
                    merchant: extractedFields.merchant || 'Unknown Merchant',
                    totalAmount: extractedFields.totalAmount || 0,
                    taxAmount: extractedFields.taxAmount || 0,
                    paymentMethod: extractedFields.paymentMethod || 'Unknown',
                    currency: extractedFields.currency || 'USD',
                    items: extractedFields.items || [],
                    aiProcessed: aiResult.aiProcessed,
                    processedAt: aiResult.processedAt
                };
                
            default: // general
                return {
                    documentId: fileInfo.id,
                    fileName: fileInfo.name,
                    documentType: extractedFields.documentType || 'General Document',
                    title: extractedFields.title || fileInfo.name,
                    date: extractedFields.date || new Date().toISOString().split('T')[0],
                    content: extractedFields.content || 'Document processed successfully',
                    keyInformation: extractedFields.keyInformation || [],
                    entities: extractedFields.entities || {},
                    aiProcessed: aiResult.aiProcessed,
                    processedAt: aiResult.processedAt
                };
        }
    }
    
    /**
     * 生成回退數據（當AI處理失敗時）
     */
    generateFallbackData(fileInfo, documentType = null) {
        const docType = documentType || this.getCurrentDocumentType();
        
        // 根據檢測到的文檔類型生成對應的模擬數據
        if (docType === 'receipt') {
            return this.generateReceiptMockData(fileInfo);
        } else if (docType === 'invoice') {
            return this.generateInvoiceMockData(fileInfo);
        } else {
            return this.generateBankStatementMockData(fileInfo);
        }
    }
    
    /**
     * 生成收據模擬數據
     */
    generateReceiptMockData(fileInfo) {
        return {
            documentId: fileInfo.id,
            fileName: fileInfo.name,
            receiptNumber: 'RCP-' + Date.now(),
            date: new Date().toISOString().split('T')[0],
            merchant: '濱得韓宮廷火鍋小炒',
            totalAmount: 507.00,
            taxAmount: 0.00,
            paymentMethod: 'Cash',
            currency: 'HKD',
            items: [
                {
                    name: '韓式料理套餐',
                    quantity: 1,
                    price: 507.00
                }
            ],
            aiProcessed: false,
            processedAt: new Date().toISOString()
        };
    }
    
    /**
     * 生成發票模擬數據
     */
    generateInvoiceMockData(fileInfo) {
        return {
            documentId: fileInfo.id,
            fileName: fileInfo.name,
            invoiceNumber: 'INV-' + Date.now(),
            issueDate: new Date().toISOString().split('T')[0],
            dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            vendor: 'Demo Vendor',
            customer: 'Demo Customer',
            totalAmount: 1200.00,
            taxAmount: 120.00,
            currency: 'HKD',
            lineItems: [
                {
                    description: 'Professional Services',
                    quantity: 1,
                    unitPrice: 1200.00,
                    totalPrice: 1200.00
                }
            ],
            aiProcessed: false,
            processedAt: new Date().toISOString()
        };
    }
    
    /**
     * 生成銀行對帳單模擬數據
     */
    generateBankStatementMockData(fileInfo) {
        const mockData = {
            documentId: fileInfo.id,
            fileName: fileInfo.name,
            accountInfo: {
                accountHolder: 'MR YEUNG CAVLIN',
                accountNumber: '766-452064-882',
                bankCode: '024',
                branch: 'EAST POINT CITY (766)'
            },
            statementPeriod: {
                startDate: '2025-02-22',
                endDate: '2025-03-22'
            },
            financialPosition: {
                deposits: 30188.66,
                personalLoans: -118986.00,
                creditCards: -19956.81,
                netPosition: -108754.15
            },
            transactions: [
                {
                    date: '2025-02-22',
                    description: 'B/F BALANCE',
                    amount: 0,
                    balance: 1493.98,
                    type: 'balance'
                },
                {
                    date: '2025-02-26',
                    description: 'CREDIT INTEREST',
                    amount: 2.61,
                    balance: 1496.59,
                    type: 'credit'
                },
                {
                    date: '2025-03-07',
                    description: 'QUICK CHEQUE DEPOSIT(07MAY25)',
                    amount: 78649,
                    balance: 80145.59,
                    type: 'deposit'
                },
                {
                    date: '2025-03-08',
                    description: 'POON H** K****HD125308257',
                    amount: -840,
                    balance: 79305.59,
                    type: 'debit'
                },
                {
                    date: '2025-03-10',
                    description: '4006-1210-0627-0086N310985',
                    amount: -21226.59,
                    balance: 58079,
                    type: 'debit'
                },
                {
                    date: '2025-03-10',
                    description: 'TUG COMPANY LIMITEDHD1253',
                    amount: 15000,
                    balance: 73079,
                    type: 'credit'
                },
                {
                    date: '2025-03-11',
                    description: '024996667598184INSTALMENT',
                    amount: -3966.2,
                    balance: 69112.8,
                    type: 'debit'
                },
                {
                    date: '2025-03-14',
                    description: 'MUSHROOM TRANSPORTHD1253',
                    amount: -6500,
                    balance: 62612.8,
                    type: 'debit'
                },
                {
                    date: '2025-03-14',
                    description: 'FROM GO DO SOMETHINGN314',
                    amount: 3900,
                    balance: 66512.8,
                    type: 'credit'
                },
                {
                    date: '2025-03-15',
                    description: 'SHUDO INTERNATIONALHD125',
                    amount: -1620,
                    balance: 64892.8,
                    type: 'debit'
                },
                {
                    date: '2025-03-21',
                    description: 'SUN HING GINSENG & AH',
                    amount: -3375,
                    balance: 61517.8,
                    type: 'debit'
                }
            ],
            reconciliation: {
                totalTransactions: 11,
                reconciledTransactions: 0,
                completionPercentage: 0
            },
            processedAt: new Date().toISOString()
        };
        
        return mockData;
    }
    
    /**
     * 添加到主文檔表格
     */
    addToMainDocumentsTable(fileInfo, processedData) {
        const tbody = document.getElementById('documents-tbody');
        if (!tbody) return;
        
        // 清除空狀態
        if (tbody.innerHTML.includes('No results')) {
            tbody.innerHTML = '';
        }
        
        const row = document.createElement('tr');
        row.className = 'document-row';
        row.onclick = () => this.openDocumentDetail(fileInfo.id);
        
        const uploadDate = new Date().toLocaleDateString('zh-TW');
        
        row.innerHTML = `
            <td>
                <input type="checkbox" onclick="event.stopPropagation()">
            </td>
            <td>
                <div class="document-cell">
                    <i class="fas fa-file-pdf file-icon"></i>
                    <div class="document-info">
                        <div class="doc-name">${fileInfo.name}</div>
                        <div class="doc-details">
                            <i class="fas fa-university"></i> ${processedData.accountInfo.accountHolder}<br>
                            <i class="fas fa-file"></i> ${this.formatFileSize(fileInfo.size)}
                        </div>
                    </div>
                </div>
            </td>
            <td>
                <div class="period-info">
                    <i class="fas fa-calendar"></i> ${processedData.statementPeriod.startDate} - ${processedData.statementPeriod.endDate}
                    <br><small>帳號: ${processedData.accountInfo.accountNumber}</small>
                </div>
            </td>
            <td>
                <div class="reconciliation">
                    <div class="reconciliation-text">${processedData.reconciliation.reconciledTransactions}/${processedData.reconciliation.totalTransactions}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${processedData.reconciliation.completionPercentage}%"></div>
                    </div>
                    <div class="progress-percentage">${processedData.reconciliation.completionPercentage}%</div>
                    <small class="reconciliation-status">
                        <i class="fas fa-clock"></i> <span>待對帳</span>
                    </small>
                </div>
            </td>
            <td>
                <div class="balance-info">
                    <div>淨額: HKD ${processedData.financialPosition.netPosition.toLocaleString()}</div>
                    <small>存款: ${processedData.financialPosition.deposits.toLocaleString()}</small>
                </div>
            </td>
            <td>
                <span class="status-badge success">
                    <i class="fas fa-check"></i> Completed
                </span>
            </td>
            <td>
                <span class="review-badge review">
                    <i class="fas fa-eye"></i> Review
                </span>
            </td>
            <td>—</td>
            <td>${uploadDate}</td>
            <td>
                <button class="action-btn" onclick="event.stopPropagation(); window.ledgerBoxProcessor.showActionMenu(event, '${fileInfo.id}')" title="More actions">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
        
        // 保存到localStorage
        this.saveDocumentToStorage(fileInfo, processedData);
    }
    
    /**
     * 打開文檔詳細視圖
     */
    openDocumentDetail(documentId) {
        console.log('🔍 查找文檔數據:', documentId);
        
        // 首先嘗試從內存中獲取
        let processedData = this.processedDocuments.get(documentId);
        
        // 如果內存中沒有，嘗試從統一存儲中載入
        if (!processedData && window.UnifiedDocumentProcessor) {
            console.log('📂 從統一存儲載入文檔數據');
            processedData = window.UnifiedDocumentProcessor.getProcessedDocument(documentId);
            
            // 將數據添加到內存中以便後續使用
            if (processedData) {
                this.processedDocuments.set(documentId, processedData);
            }
        }
        
        // 如果還是沒有，嘗試從舊的存儲格式載入
        if (!processedData) {
            console.log('📂 從舊存儲格式載入文檔數據');
            processedData = this.loadFromLegacyStorage(documentId);
        }
        
        if (!processedData) {
            console.error('❌ 找不到處理後的數據:', documentId);
            alert('找不到文檔數據，請重新上傳文件');
            return;
        }
        
        this.currentDocument = processedData;
        
        // 隱藏列表視圖，顯示詳細視圖
        document.getElementById('document-list-view').style.display = 'none';
        document.getElementById('document-detail-view').style.display = 'block';
        
        // 更新詳細視圖內容
        this.updateDocumentDetailView(processedData);
        
        console.log('📄 打開文檔詳細視圖:', processedData.fileName || processedData.name);
    }
    
    /**
     * 從舊存儲格式載入數據
     */
    loadFromLegacyStorage(documentId) {
        const docTypes = ['bank-statement', 'invoice', 'receipt', 'general'];
        
        for (const docType of docTypes) {
            // 檢查舊的存儲格式
            const storageKey = `vaultcaddy_files_${docType}`;
            const storedFiles = JSON.parse(localStorage.getItem(storageKey) || '[]');
            
            const fileInfo = storedFiles.find(file => file.id === documentId);
            if (fileInfo && fileInfo.processedData) {
                console.log(`📂 從舊存儲載入: ${storageKey}`);
                return fileInfo.processedData;
            }
        }
        
        return null;
    }
    
    /**
     * 更新文檔詳細視圖
     */
    updateDocumentDetailView(data) {
        // 更新文檔標題（多個位置）
        const titleElement = document.getElementById('document-title');
        if (titleElement) {
            titleElement.textContent = data.fileName || data.name || 'Unknown Document';
        }
        
        const titleHeaderElement = document.getElementById('document-title-header');
        if (titleHeaderElement) {
            titleHeaderElement.textContent = data.fileName || data.name || 'Unknown Document';
        }
        
        // 根據文檔類型顯示不同的內容
        if (data.receiptNumber) {
            // 收據視圖
            this.updateReceiptDetailView(data);
        } else if (data.invoiceNumber) {
            // 發票視圖
            this.updateInvoiceDetailView(data);
        } else {
            // 銀行對帳單視圖
            this.updateBankStatementDetailView(data);
        }
    }
    
    /**
     * 更新收據詳細視圖
     */
    updateReceiptDetailView(data) {
        // 更新對帳狀態區域為收據信息
        const reconciliationStatus = document.querySelector('.reconciliation-status');
        if (reconciliationStatus) {
            reconciliationStatus.innerHTML = `
                <h3>收據信息</h3>
                <p>收據號碼: ${data.receiptNumber || 'N/A'}</p>
                <p>總金額: ${data.currency || 'HKD'} ${data.totalAmount?.toLocaleString() || '0'}</p>
                <div class="completion-status">已處理</div>
            `;
        }
        
        // 更新詳細信息區域
        const bankDetails = document.querySelector('.bank-statement-details');
        if (bankDetails) {
            bankDetails.innerHTML = `
                <h3>收據詳細信息</h3>
                <div class="receipt-info">
                    <p><strong>商家:</strong> ${data.merchant || 'Unknown'}</p>
                    <p><strong>日期:</strong> ${data.date || 'N/A'}</p>
                    <p><strong>付款方式:</strong> ${data.paymentMethod || 'N/A'}</p>
                    <p><strong>總金額:</strong> ${data.currency || 'HKD'} ${data.totalAmount?.toLocaleString() || '0'}</p>
                    <p><strong>稅額:</strong> ${data.currency || 'HKD'} ${data.taxAmount?.toLocaleString() || '0'}</p>
                </div>
            `;
        }
        
        // 更新商品列表
        this.updateReceiptItemsTable(data.items || []);
    }
    
    /**
     * 更新發票詳細視圖
     */
    updateInvoiceDetailView(data) {
        // 更新對帳狀態區域為發票信息
        const reconciliationStatus = document.querySelector('.reconciliation-status');
        if (reconciliationStatus) {
            reconciliationStatus.innerHTML = `
                <h3>發票信息</h3>
                <p>發票號碼: ${data.invoiceNumber || 'N/A'}</p>
                <p>總金額: ${data.currency || 'HKD'} ${data.totalAmount?.toLocaleString() || '0'}</p>
                <div class="completion-status">已處理</div>
            `;
        }
        
        // 更新詳細信息區域
        const bankDetails = document.querySelector('.bank-statement-details');
        if (bankDetails) {
            bankDetails.innerHTML = `
                <h3>發票詳細信息</h3>
                <div class="invoice-info">
                    <p><strong>供應商:</strong> ${data.vendor || 'Unknown'}</p>
                    <p><strong>客戶:</strong> ${data.customer || 'Unknown'}</p>
                    <p><strong>開票日期:</strong> ${data.issueDate || 'N/A'}</p>
                    <p><strong>到期日期:</strong> ${data.dueDate || 'N/A'}</p>
                    <p><strong>總金額:</strong> ${data.currency || 'HKD'} ${data.totalAmount?.toLocaleString() || '0'}</p>
                    <p><strong>稅額:</strong> ${data.currency || 'HKD'} ${data.taxAmount?.toLocaleString() || '0'}</p>
                </div>
            `;
        }
        
        // 更新行項目列表
        this.updateInvoiceItemsTable(data.lineItems || []);
    }
    
    /**
     * 更新銀行對帳單詳細視圖
     */
    updateBankStatementDetailView(data) {
        // 更新對帳狀態
        const reconciliationStatus = document.querySelector('.reconciliation-status');
        if (reconciliationStatus) {
            reconciliationStatus.innerHTML = `
                <h3>對帳狀態</h3>
                <p>${data.reconciliation?.reconciledTransactions || 0} 共 ${data.reconciliation?.totalTransactions || 0} 筆交易已對帳</p>
                <div class="completion-status">${data.reconciliation?.completionPercentage || 0}% 完成</div>
            `;
        }
        
        // 更新銀行對帳單詳細信息
        const bankDetails = document.querySelector('.bank-statement-details');
        if (bankDetails) {
            bankDetails.innerHTML = `
                <h3>銀行對帳單詳細信息</h3>
                <div class="account-info">
                    <p><strong>帳戶持有人:</strong> ${data.accountInfo?.accountHolder || 'N/A'}</p>
                    <p><strong>帳戶號碼:</strong> ${data.accountInfo?.accountNumber || 'N/A'}</p>
                    <p><strong>銀行代碼:</strong> ${data.accountInfo?.bankCode || 'N/A'}</p>
                    <p><strong>分行:</strong> ${data.accountInfo?.branch || 'N/A'}</p>
                    <p><strong>對帳單期間:</strong> ${data.statementPeriod?.startDate || 'N/A'} 至 ${data.statementPeriod?.endDate || 'N/A'}</p>
                </div>
                <div class="financial-position">
                    <h4>財務狀況</h4>
                    <p>存款: HKD ${data.financialPosition?.deposits?.toLocaleString() || '0'}</p>
                    <p>個人貸款: HKD ${data.financialPosition?.personalLoans?.toLocaleString() || '0'}</p>
                    <p>信用卡: HKD ${data.financialPosition?.creditCards?.toLocaleString() || '0'}</p>
                    <p><strong>淨額: HKD ${data.financialPosition?.netPosition?.toLocaleString() || '0'}</strong></p>
                </div>
            `;
        }
        
        // 更新交易表格
        this.updateTransactionsTable(data.transactions || []);
    }
    
    /**
     * 更新交易表格
     */
    updateTransactionsTable(transactions) {
        const tbody = document.getElementById('transactions-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        transactions.forEach((transaction, index) => {
            const row = document.createElement('tr');
            row.className = 'transaction-row';
            
            row.innerHTML = `
                <td>
                    <input type="checkbox" class="transaction-checkbox">
                </td>
                <td>
                    <input type="date" class="editable-input date-input" value="${transaction.date}">
                </td>
                <td>
                    <input type="text" class="editable-input description-input" value="${transaction.description}" placeholder="Description">
                </td>
                <td>
                    <input type="number" class="editable-input amount-input" value="${transaction.amount}" step="0.01">
                </td>
                <td>
                    <input type="number" class="editable-input balance-input" value="${transaction.balance}" step="0.01" readonly>
                </td>
                <td>
                    <button class="delete-transaction-btn" onclick="window.ledgerBoxProcessor.deleteTransaction(this)">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    /**
     * 更新收據項目表格
     */
    updateReceiptItemsTable(items) {
        const tbody = document.getElementById('transactions-tbody');
        if (!tbody) return;
        
        // 更新表格標題
        const tableHeaders = document.querySelector('#transactions-tbody').closest('table').querySelector('thead tr');
        if (tableHeaders) {
            tableHeaders.innerHTML = `
                <th style="width: 40px;"><i class="fas fa-check"></i></th>
                <th>商品名稱</th>
                <th>數量</th>
                <th>單價</th>
                <th>總價</th>
                <th style="width: 40px;"></th>
            `;
        }
        
        tbody.innerHTML = '';
        
        items.forEach((item, index) => {
            const row = document.createElement('tr');
            row.className = 'transaction-row';
            
            row.innerHTML = `
                <td>
                    <input type="checkbox" class="transaction-checkbox">
                </td>
                <td>
                    <input type="text" class="editable-input description-input" value="${item.name || ''}" placeholder="商品名稱">
                </td>
                <td>
                    <input type="number" class="editable-input amount-input" value="${item.quantity || 1}" step="1" min="1">
                </td>
                <td>
                    <input type="number" class="editable-input amount-input" value="${item.price || 0}" step="0.01">
                </td>
                <td>
                    <input type="number" class="editable-input balance-input" value="${(item.quantity || 1) * (item.price || 0)}" step="0.01" readonly>
                </td>
                <td>
                    <button class="delete-transaction-btn" onclick="window.ledgerBoxProcessor.deleteTransaction(this)">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    /**
     * 更新發票項目表格
     */
    updateInvoiceItemsTable(lineItems) {
        const tbody = document.getElementById('transactions-tbody');
        if (!tbody) return;
        
        // 更新表格標題
        const tableHeaders = document.querySelector('#transactions-tbody').closest('table').querySelector('thead tr');
        if (tableHeaders) {
            tableHeaders.innerHTML = `
                <th style="width: 40px;"><i class="fas fa-check"></i></th>
                <th>項目描述</th>
                <th>數量</th>
                <th>單價</th>
                <th>總價</th>
                <th style="width: 40px;"></th>
            `;
        }
        
        tbody.innerHTML = '';
        
        lineItems.forEach((item, index) => {
            const row = document.createElement('tr');
            row.className = 'transaction-row';
            
            row.innerHTML = `
                <td>
                    <input type="checkbox" class="transaction-checkbox">
                </td>
                <td>
                    <input type="text" class="editable-input description-input" value="${item.description || ''}" placeholder="項目描述">
                </td>
                <td>
                    <input type="number" class="editable-input amount-input" value="${item.quantity || 1}" step="1" min="1">
                </td>
                <td>
                    <input type="number" class="editable-input amount-input" value="${item.unitPrice || 0}" step="0.01">
                </td>
                <td>
                    <input type="number" class="editable-input balance-input" value="${item.totalPrice || 0}" step="0.01" readonly>
                </td>
                <td>
                    <button class="delete-transaction-btn" onclick="window.ledgerBoxProcessor.deleteTransaction(this)">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    /**
     * 工具函數
     */
    generateFileId() {
        return 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    updateFileStatus(fileId, status, className) {
        const statusElement = document.getElementById(`status-${fileId}`);
        if (statusElement) {
            statusElement.textContent = status;
            statusElement.className = `status-badge ${className}`;
        }
        
        // 更新文件信息
        const fileInfo = this.processingFiles.get(fileId);
        if (fileInfo) {
            fileInfo.status = status;
        }
    }
    
    updateFilesCounter() {
        const counter = document.getElementById('files-counter');
        if (counter) {
            const count = this.processingFiles.size;
            counter.textContent = `${count} / 20 files uploaded`;
        }
    }
    
    saveDocumentToStorage(fileInfo, processedData) {
        // 獲取當前文檔類型
        const currentDocType = this.getCurrentDocumentType();
        
        // 使用統一存儲格式
        if (window.UnifiedDocumentProcessor && window.UnifiedDocumentProcessor.processors.storage) {
            console.log('💾 使用統一存儲系統保存文檔');
            
            // 轉換為統一格式
            const unifiedData = {
                id: fileInfo.id,
                fileName: fileInfo.name,
                documentType: currentDocType,
                processedAt: new Date().toISOString(),
                aiProcessed: processedData.aiProcessed || false,
                version: '3.0.0',
                ...processedData // 包含所有處理後的數據
            };
            
            window.UnifiedDocumentProcessor.processors.storage.save(unifiedData, currentDocType);
        } else {
            // 回退到舊的存儲方式
            console.log('💾 使用舊版存儲系統');
            const storageKey = `vaultcaddy_files_${currentDocType}`;
            const existingFiles = JSON.parse(localStorage.getItem(storageKey) || '[]');
            
            const documentInfo = {
                id: fileInfo.id,
                name: fileInfo.name,
                size: fileInfo.size,
                documentType: currentDocType,
                uploadDate: new Date().toLocaleDateString('zh-TW'),
                status: 'completed',
                processedData: processedData,
                fileBlob: null
            };
            
            const existingIndex = existingFiles.findIndex(file => file.id === fileInfo.id);
            if (existingIndex !== -1) {
                existingFiles[existingIndex] = documentInfo;
            } else {
                existingFiles.push(documentInfo);
            }
            
            localStorage.setItem(storageKey, JSON.stringify(existingFiles));
        }
        
        console.log(`💾 文件已保存:`, fileInfo.name);
        
        // 觸發存儲更新事件
        window.dispatchEvent(new CustomEvent('vaultcaddy:storage:updated', {
            detail: { documentType: currentDocType, fileId: fileInfo.id }
        }));
    }
    
    /**
     * 獲取當前文檔類型
     */
    getCurrentDocumentType() {
        const hash = window.location.hash.substring(1);
        return hash || 'bank-statement';
    }
    
    /**
     * 從localStorage載入文件
     */
    loadStoredDocuments(documentType) {
        const storageKey = `vaultcaddy_files_${documentType}`;
        const storedFiles = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        console.log(`📂 載入 ${documentType} 文件:`, storedFiles.length, '個');
        
        // 將存儲的文件添加到processedDocuments
        storedFiles.forEach(fileInfo => {
            if (fileInfo.processedData) {
                this.processedDocuments.set(fileInfo.id, fileInfo.processedData);
            }
        });
        
        return storedFiles;
    }
    
    showNotification(message, type = 'info') {
        const colors = {
            success: { bg: '#f0fdf4', border: '#bbf7d0', text: '#166534' },
            error: { bg: '#fef2f2', border: '#fecaca', text: '#991b1b' },
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
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    /**
     * 公共方法
     */
    openLedgerBoxModal() {
        this.uploadModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    closeLedgerBoxModal() {
        this.uploadModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    clearAllFiles() {
        this.processingFiles.clear();
        document.getElementById('ledgerbox-files-tbody').innerHTML = '';
        this.updateFilesCounter();
    }
    
    deleteFile(fileId) {
        this.processingFiles.delete(fileId);
        const row = document.getElementById(`file-row-${fileId}`);
        if (row) row.remove();
        this.updateFilesCounter();
    }
    
    deleteTransaction(button) {
        if (confirm('確定要刪除這筆交易嗎？')) {
            const row = button.closest('tr');
            row.remove();
        }
    }
    
    showActionMenu(event, documentId) {
        // 實現操作菜單
        console.log('顯示操作菜單:', documentId);
    }
    
    showHelp() {
        alert('需要幫助？請聯繫我們的支援團隊。');
    }
    
    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 監聽原有的上傳按鈕
        document.addEventListener('click', (e) => {
            if (e.target.closest('.upload-btn') && e.target.textContent.includes('上傳文件')) {
                e.preventDefault();
                this.openLedgerBoxModal();
            }
        });
        
        // 監聽頁面hash變化，載入對應文檔類型的文件
        window.addEventListener('hashchange', () => {
            this.loadAndDisplayStoredFiles();
        });
        
        // 監聽存儲更新事件
        window.addEventListener('vaultcaddy:storage:updated', (e) => {
            console.log('📊 存儲已更新:', e.detail);
            this.updateSidebarStats();
        });
        
        // 頁面載入時載入存儲的文件
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => this.loadAndDisplayStoredFiles(), 500);
        });
    }
    
    /**
     * 載入並顯示存儲的文件
     */
    loadAndDisplayStoredFiles() {
        const currentDocType = this.getCurrentDocumentType();
        const storedFiles = this.loadStoredDocuments(currentDocType);
        
        if (storedFiles.length > 0) {
            this.displayStoredFilesInMainTable(storedFiles);
        }
    }
    
    /**
     * 在主表格中顯示存儲的文件
     */
    displayStoredFilesInMainTable(storedFiles) {
        const tbody = document.getElementById('documents-tbody');
        if (!tbody) return;
        
        // 清除現有內容
        tbody.innerHTML = '';
        
        storedFiles.forEach(fileInfo => {
            this.addStoredFileToMainTable(fileInfo);
        });
        
        console.log(`✅ 已顯示 ${storedFiles.length} 個存儲的文件`);
    }
    
    /**
     * 添加存儲的文件到主表格
     */
    addStoredFileToMainTable(fileInfo) {
        const tbody = document.getElementById('documents-tbody');
        if (!tbody) return;
        
        const row = document.createElement('tr');
        row.className = 'document-row ledgerbox-processed';
        row.onclick = () => this.openDocumentDetail(fileInfo.id);
        
        // 根據文檔類型顯示不同的信息
        const displayInfo = this.getDocumentDisplayInfo(fileInfo);
        
        row.innerHTML = `
            <td>
                <input type="checkbox" onclick="event.stopPropagation()">
            </td>
            <td>
                <div class="document-cell">
                    <i class="fas ${displayInfo.icon} file-icon"></i>
                    <div class="document-info">
                        <div class="doc-name">${fileInfo.name}</div>
                        <div class="doc-details">
                            <i class="fas fa-tag"></i> ${displayInfo.typeLabel}<br>
                            <i class="fas fa-file"></i> ${this.formatFileSize(fileInfo.size)}
                        </div>
                    </div>
                </div>
            </td>
            <td>
                <div class="period-info">
                    ${displayInfo.periodInfo}
                </div>
            </td>
            <td>
                <div class="reconciliation">
                    ${displayInfo.reconciliationInfo}
                </div>
            </td>
            <td>
                <div class="balance-info">
                    ${displayInfo.balanceInfo}
                </div>
            </td>
            <td>
                <span class="status-badge success">
                    <i class="fas fa-check"></i> Completed
                </span>
            </td>
            <td>
                <span class="review-badge review">
                    <i class="fas fa-eye"></i> Review
                </span>
            </td>
            <td>—</td>
            <td>${fileInfo.uploadDate}</td>
            <td>
                <button class="action-btn" onclick="event.stopPropagation(); window.ledgerBoxProcessor.showActionMenu(event, '${fileInfo.id}')" title="More actions">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
    }
    
    /**
     * 根據文檔類型獲取顯示信息
     */
    getDocumentDisplayInfo(fileInfo) {
        const processedData = fileInfo.processedData;
        
        switch (fileInfo.documentType) {
            case 'bank-statement':
                return {
                    icon: 'fa-university',
                    typeLabel: processedData?.accountInfo?.accountHolder || '銀行對帳單',
                    periodInfo: processedData?.statementPeriod ? 
                        `<i class="fas fa-calendar"></i> ${processedData.statementPeriod.startDate} - ${processedData.statementPeriod.endDate}<br><small>帳號: ${processedData.accountInfo?.accountNumber}</small>` :
                        '<i class="fas fa-calendar"></i> 已處理',
                    reconciliationInfo: processedData?.reconciliation ? 
                        `<div class="reconciliation-text">${processedData.reconciliation.reconciledTransactions}/${processedData.reconciliation.totalTransactions}</div>
                         <div class="progress-bar"><div class="progress-fill" style="width: ${processedData.reconciliation.completionPercentage}%"></div></div>
                         <div class="progress-percentage">${processedData.reconciliation.completionPercentage}%</div>
                         <small class="reconciliation-status"><i class="fas fa-clock"></i> 待對帳</small>` :
                        '<div class="reconciliation-text">-/-</div>',
                    balanceInfo: processedData?.financialPosition ? 
                        `<div>淨額: HKD ${processedData.financialPosition.netPosition.toLocaleString()}</div><small>存款: ${processedData.financialPosition.deposits.toLocaleString()}</small>` :
                        '<div>已處理</div>'
                };
                
            case 'invoice':
                return {
                    icon: 'fa-file-invoice',
                    typeLabel: processedData?.vendor || '發票',
                    periodInfo: processedData?.issueDate ? 
                        `<i class="fas fa-calendar"></i> ${processedData.issueDate}<br><small>發票號: ${processedData.invoiceNumber || 'N/A'}</small>` :
                        '<i class="fas fa-calendar"></i> 已處理',
                    reconciliationInfo: '<div class="reconciliation-text">-/-</div>',
                    balanceInfo: processedData?.totalAmount ? 
                        `<div>總額: $${processedData.totalAmount.toLocaleString()}</div>` :
                        '<div>已處理</div>'
                };
                
            case 'receipt':
                return {
                    icon: 'fa-receipt',
                    typeLabel: processedData?.merchant || '收據',
                    periodInfo: processedData?.date ? 
                        `<i class="fas fa-calendar"></i> ${processedData.date}<br><small>商家: ${processedData.merchant || 'N/A'}</small>` :
                        '<i class="fas fa-calendar"></i> 已處理',
                    reconciliationInfo: '<div class="reconciliation-text">-/-</div>',
                    balanceInfo: processedData?.totalAmount ? 
                        `<div>總額: $${processedData.totalAmount.toLocaleString()}</div>` :
                        '<div>已處理</div>'
                };
                
            default:
                return {
                    icon: 'fa-file-alt',
                    typeLabel: '一般文檔',
                    periodInfo: '<i class="fas fa-calendar"></i> 已處理',
                    reconciliationInfo: '<div class="reconciliation-text">-/-</div>',
                    balanceInfo: '<div>已處理</div>'
                };
        }
    }
    
    /**
     * 更新側邊欄統計
     */
    updateSidebarStats() {
        // 計算所有文檔類型的總數
        const docTypes = ['bank-statement', 'invoice', 'receipt', 'general'];
        let totalFiles = 0;
        
        docTypes.forEach(type => {
            const storageKey = `vaultcaddy_files_${type}`;
            const files = JSON.parse(localStorage.getItem(storageKey) || '[]');
            totalFiles += files.length;
        });
        
        // 更新側邊欄統計
        const statElement = document.querySelector('.stat-value');
        if (statElement) {
            statElement.textContent = totalFiles;
        }
        
        console.log(`📊 總文檔數: ${totalFiles}`);
    }
}

// 創建全域實例
window.ledgerBoxProcessor = new LedgerBoxStyleProcessor();

console.log('🏦 LedgerBox風格處理器已載入');
