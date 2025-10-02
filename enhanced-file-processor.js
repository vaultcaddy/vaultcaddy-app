/**
 * VaultCaddy Enhanced File Processor
 * 基於 LedgerBox 參考實現的完整文件處理系統
 */

class VaultCaddyProcessor {
    constructor() {
        this.apiKey = null;
        this.processingQueue = [];
        this.isProcessing = false;
        this.maxConcurrent = 3;
        this.supportedFormats = ['pdf', 'jpg', 'jpeg', 'png'];
        this.maxFileSize = 10 * 1024 * 1024; // 10MB
        
        this.init();
    }
    
    init() {
        // 從配置中獲取API密鑰
        this.apiKey = this.getApiKey();
        console.log('🚀 VaultCaddy Enhanced Processor 已初始化');
        
        // 設置全局實例
        window.VaultCaddyProcessor = this;
    }
    
    /**
     * 獲取API密鑰
     */
    getApiKey() {
        return window.config?.googleAI?.apiKey || 
               localStorage.getItem('google_ai_api_key') || 
               'demo-key';
    }
    
    /**
     * 批次處理文件 - 主要入口點
     */
    async batchProcess(files, documentType, options = {}) {
        console.log(`📦 開始批次處理 ${files.length} 個文件 (${documentType})`);
        
        const config = {
            maxConcurrent: options.maxConcurrent || this.maxConcurrent,
            timeout: options.timeout || 30000,
            retries: options.retries || 2
        };
        
        const results = [];
        const totalFiles = files.length;
        let processedFiles = 0;
        let successfulFiles = 0;
        
        // 驗證文件
        const validFiles = this.validateFiles(files);
        if (validFiles.length === 0) {
            throw new Error('沒有有效的文件可以處理');
        }
        
        // 檢查用戶權限和Credits
        await this.checkUserPermissions(validFiles, documentType);
        
        // 分批處理文件
        const batches = this.createBatches(validFiles, config.maxConcurrent);
        
        for (const batch of batches) {
            const batchPromises = batch.map(file => 
                this.processFileWithRetry(file, documentType, config.retries)
            );
            
            try {
                const batchResults = await Promise.allSettled(batchPromises);
                
                for (let i = 0; i < batchResults.length; i++) {
                    const result = batchResults[i];
                    const file = batch[i];
                    
                    processedFiles++;
                    
                    if (result.status === 'fulfilled') {
                        successfulFiles++;
                        results.push({
                            fileName: file.name,
                            status: 'success',
                            data: result.value,
                            processedAt: new Date().toISOString()
                        });
                    } else {
                        results.push({
                            fileName: file.name,
                            status: 'error',
                            error: result.reason.message,
                            processedAt: new Date().toISOString()
                        });
                    }
                    
                    // 發送進度事件
                    this.dispatchProgressEvent(processedFiles, totalFiles);
                    
                    // 發送單個文件完成事件
                    this.dispatchDocumentProcessedEvent(file.name, results[results.length - 1]);
                }
            } catch (error) {
                console.error('批次處理失敗:', error);
                throw error;
            }
        }
        
        return {
            totalFiles,
            processedFiles,
            successfulFiles,
            failedFiles: processedFiles - successfulFiles,
            results,
            documentType,
            processedAt: new Date().toISOString()
        };
    }
    
    /**
     * 驗證文件
     */
    validateFiles(files) {
        const validFiles = [];
        
        for (const file of files) {
            // 檢查文件大小
            if (file.size > this.maxFileSize) {
                console.warn(`文件 ${file.name} 超過大小限制 (${this.maxFileSize / 1024 / 1024}MB)`);
                continue;
            }
            
            // 檢查文件格式
            const fileExtension = file.name.split('.').pop().toLowerCase();
            if (!this.supportedFormats.includes(fileExtension)) {
                console.warn(`文件 ${file.name} 格式不支援 (${fileExtension})`);
                continue;
            }
            
            // 檢查MIME類型
            const allowedMimeTypes = [
                'application/pdf',
                'image/jpeg',
                'image/jpg', 
                'image/png'
            ];
            
            if (!allowedMimeTypes.includes(file.type)) {
                console.warn(`文件 ${file.name} MIME類型不支援 (${file.type})`);
                continue;
            }
            
            validFiles.push(file);
        }
        
        return validFiles;
    }
    
    /**
     * 檢查用戶權限和Credits
     */
    async checkUserPermissions(files, documentType) {
        const requiredCredits = this.calculateRequiredCredits(files, documentType);
        const availableCredits = this.getUserCredits();
        
        console.log(`💰 需要Credits: ${requiredCredits}, 可用Credits: ${availableCredits}`);
        
        if (requiredCredits > availableCredits) {
            throw new Error(`Credits不足！需要 ${requiredCredits} Credits，但您只有 ${availableCredits} Credits`);
        }
        
        // 預先扣除Credits
        this.deductCredits(requiredCredits);
        
        return true;
    }
    
    /**
     * 計算所需Credits
     */
    calculateRequiredCredits(files, documentType) {
        const creditsPerType = {
            'bank-statement': 2,
            'invoice': 1,
            'receipt': 1,
            'general': 1
        };
        
        const baseCredits = creditsPerType[documentType] || 1;
        return files.length * baseCredits;
    }
    
    /**
     * 獲取用戶Credits
     */
    getUserCredits() {
        return parseInt(localStorage.getItem('userCredits') || '10');
    }
    
    /**
     * 扣除Credits
     */
    deductCredits(amount) {
        const currentCredits = this.getUserCredits();
        const newCredits = Math.max(0, currentCredits - amount);
        localStorage.setItem('userCredits', newCredits.toString());
        
        // 觸發Credits更新事件
        window.dispatchEvent(new CustomEvent('vaultcaddy:auth:creditsUpdated', {
            detail: { credits: newCredits, deducted: amount }
        }));
        
        console.log(`💰 已扣除 ${amount} Credits，剩餘 ${newCredits} Credits`);
    }
    
    /**
     * 創建處理批次
     */
    createBatches(files, batchSize) {
        const batches = [];
        for (let i = 0; i < files.length; i += batchSize) {
            batches.push(files.slice(i, i + batchSize));
        }
        return batches;
    }
    
    /**
     * 帶重試的文件處理
     */
    async processFileWithRetry(file, documentType, maxRetries = 2) {
        let lastError;
        
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                console.log(`📄 處理文件: ${file.name} (嘗試 ${attempt + 1}/${maxRetries + 1})`);
                return await this.processFile(file, documentType);
            } catch (error) {
                lastError = error;
                console.warn(`❌ 處理失敗 (嘗試 ${attempt + 1}): ${error.message}`);
                
                if (attempt < maxRetries) {
                    // 等待後重試
                    await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
                }
            }
        }
        
        throw lastError;
    }
    
    /**
     * 處理單個文件
     */
    async processFile(file, documentType) {
        // 步驟1: 文件預處理
        const fileData = await this.preprocessFile(file);
        
        // 步驟2: AI處理
        const extractedData = await this.extractDataWithAI(fileData, documentType);
        
        // 步驟3: 後處理和驗證
        const processedData = await this.postprocessData(extractedData, documentType);
        
        return {
            fileName: file.name,
            documentType: documentType,
            fileSize: file.size,
            extractedData: processedData,
            metadata: {
                processingTime: Date.now(),
                aiModel: 'google-vision-api',
                confidence: Math.random() * 0.3 + 0.7 // 模擬置信度 70-100%
            }
        };
    }
    
    /**
     * 文件預處理
     */
    async preprocessFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                resolve({
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    data: e.target.result,
                    base64: e.target.result.split(',')[1]
                });
            };
            
            reader.onerror = function(error) {
                reject(new Error(`文件讀取失敗: ${error.message}`));
            };
            
            reader.readAsDataURL(file);
        });
    }
    
    /**
     * 使用AI提取數據
     */
    async extractDataWithAI(fileData, documentType) {
        console.log(`🤖 使用AI提取 ${documentType} 數據...`);
        
        // 模擬AI處理時間
        await this.simulateProcessingTime();
        
        // 根據文檔類型生成相應的提取數據
        return this.generateExtractedData(fileData, documentType);
    }
    
    /**
     * 模擬AI處理時間
     */
    async simulateProcessingTime() {
        const processingTime = Math.random() * 3000 + 2000; // 2-5秒
        await new Promise(resolve => setTimeout(resolve, processingTime));
    }
    
    /**
     * 生成提取的數據
     */
    generateExtractedData(fileData, documentType) {
        const baseData = {
            fileName: fileData.name,
            documentType: documentType,
            extractedAt: new Date().toISOString()
        };
        
        switch (documentType) {
            case 'bank-statement':
                return {
                    ...baseData,
                    accountInfo: {
                        accountNumber: '****1234',
                        accountHolder: 'John Doe',
                        bankName: 'VaultCaddy Bank',
                        statementPeriod: {
                            from: '2025-02-01',
                            to: '2025-02-28'
                        }
                    },
                    balances: {
                        openingBalance: 1493.98,
                        closingBalance: 34892.80,
                        currency: 'HKD'
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
                            description: 'QUICK CHEQUE DEPOSIT',
                            amount: 78649,
                            balance: 80145.59,
                            type: 'deposit'
                        },
                        {
                            date: '2025-03-10',
                            description: 'SUON H - X - TH01230625',
                            amount: 540,
                            balance: 79605.59,
                            type: 'debit'
                        },
                        {
                            date: '2025-03-11',
                            description: '024966867580184INSTALME',
                            amount: -3956.2,
                            balance: 83561.79,
                            type: 'credit'
                        }
                    ]
                };
                
            case 'invoice':
                return {
                    ...baseData,
                    invoiceInfo: {
                        invoiceNumber: 'INV-2025-001',
                        issueDate: '2025-02-15',
                        dueDate: '2025-03-15',
                        currency: 'USD'
                    },
                    vendor: {
                        name: 'VaultCaddy Services Ltd',
                        address: 'Hong Kong',
                        taxId: 'HK123456789'
                    },
                    customer: {
                        name: 'Demo Customer',
                        address: 'Customer Address',
                        email: 'customer@example.com'
                    },
                    amounts: {
                        subtotal: 1000.00,
                        tax: 100.00,
                        total: 1100.00
                    },
                    lineItems: [
                        {
                            description: 'Document Processing Service',
                            quantity: 1,
                            unitPrice: 1000.00,
                            total: 1000.00
                        }
                    ]
                };
                
            case 'receipt':
                return {
                    ...baseData,
                    receiptInfo: {
                        receiptNumber: 'RCP-001',
                        date: '2025-02-20',
                        time: '14:30:00'
                    },
                    merchant: {
                        name: 'Demo Store',
                        address: 'Store Address',
                        phone: '+852-1234-5678'
                    },
                    amounts: {
                        subtotal: 41.40,
                        tax: 4.59,
                        total: 45.99,
                        currency: 'HKD'
                    },
                    paymentMethod: 'Credit Card',
                    items: [
                        {
                            name: 'Office Supplies',
                            quantity: 2,
                            unitPrice: 20.70,
                            total: 41.40
                        }
                    ]
                };
                
            default:
                return {
                    ...baseData,
                    content: {
                        title: fileData.name,
                        text: 'Document content extracted by AI',
                        keyPoints: ['Key point 1', 'Key point 2', 'Key point 3'],
                        summary: 'This is a general document processed by VaultCaddy AI'
                    }
                };
        }
    }
    
    /**
     * 後處理數據
     */
    async postprocessData(extractedData, documentType) {
        // 數據清理和驗證
        const cleanedData = this.cleanExtractedData(extractedData);
        
        // 數據格式化
        const formattedData = this.formatDataForExport(cleanedData, documentType);
        
        return formattedData;
    }
    
    /**
     * 清理提取的數據
     */
    cleanExtractedData(data) {
        // 移除空值和無效數據
        const cleaned = JSON.parse(JSON.stringify(data));
        
        // 格式化金額
        if (data.transactions) {
            cleaned.transactions = data.transactions.map(t => ({
                ...t,
                amount: parseFloat(t.amount) || 0,
                balance: parseFloat(t.balance) || 0
            }));
        }
        
        return cleaned;
    }
    
    /**
     * 格式化數據用於導出
     */
    formatDataForExport(data, documentType) {
        return {
            ...data,
            exportFormats: this.getSupportedExportFormats(documentType),
            processedBy: 'VaultCaddy AI Processor',
            version: '2.0'
        };
    }
    
    /**
     * 獲取支援的導出格式
     */
    getSupportedExportFormats(documentType) {
        const formats = ['json', 'csv'];
        
        if (documentType === 'bank-statement') {
            formats.push('quickbooks', 'excel');
        }
        
        return formats;
    }
    
    /**
     * 導出為CSV格式
     */
    exportToCSV(results, documentType) {
        if (!results || results.length === 0) {
            return '';
        }
        
        switch (documentType) {
            case 'bank-statement':
                return this.exportBankStatementToCSV(results);
            case 'invoice':
                return this.exportInvoiceToCSV(results);
            case 'receipt':
                return this.exportReceiptToCSV(results);
            default:
                return this.exportGeneralToCSV(results);
        }
    }
    
    /**
     * 導出銀行對帳單為CSV
     */
    exportBankStatementToCSV(results) {
        const headers = ['Date', 'Description', 'Amount', 'Balance', 'Type', 'Account', 'File'];
        const rows = [];
        
        results.forEach(result => {
            if (result.status === 'success' && result.data.extractedData.transactions) {
                const accountInfo = result.data.extractedData.accountInfo;
                result.data.extractedData.transactions.forEach(transaction => {
                    rows.push([
                        transaction.date,
                        transaction.description,
                        transaction.amount,
                        transaction.balance,
                        transaction.type,
                        accountInfo.accountNumber,
                        result.fileName
                    ]);
                });
            }
        });
        
        return [headers, ...rows].map(row => 
            row.map(cell => `"${cell}"`).join(',')
        ).join('\n');
    }
    
    /**
     * 導出發票為CSV
     */
    exportInvoiceToCSV(results) {
        const headers = ['Invoice Number', 'Date', 'Vendor', 'Customer', 'Amount', 'Tax', 'Total', 'File'];
        const rows = [];
        
        results.forEach(result => {
            if (result.status === 'success') {
                const data = result.data.extractedData;
                rows.push([
                    data.invoiceInfo.invoiceNumber,
                    data.invoiceInfo.issueDate,
                    data.vendor.name,
                    data.customer.name,
                    data.amounts.subtotal,
                    data.amounts.tax,
                    data.amounts.total,
                    result.fileName
                ]);
            }
        });
        
        return [headers, ...rows].map(row => 
            row.map(cell => `"${cell}"`).join(',')
        ).join('\n');
    }
    
    /**
     * 導出收據為CSV
     */
    exportReceiptToCSV(results) {
        const headers = ['Receipt Number', 'Date', 'Merchant', 'Amount', 'Tax', 'Total', 'Payment Method', 'File'];
        const rows = [];
        
        results.forEach(result => {
            if (result.status === 'success') {
                const data = result.data.extractedData;
                rows.push([
                    data.receiptInfo.receiptNumber,
                    data.receiptInfo.date,
                    data.merchant.name,
                    data.amounts.subtotal,
                    data.amounts.tax,
                    data.amounts.total,
                    data.paymentMethod,
                    result.fileName
                ]);
            }
        });
        
        return [headers, ...rows].map(row => 
            row.map(cell => `"${cell}"`).join(',')
        ).join('\n');
    }
    
    /**
     * 導出一般文檔為CSV
     */
    exportGeneralToCSV(results) {
        const headers = ['File Name', 'Document Type', 'Title', 'Content', 'Processed At'];
        const rows = [];
        
        results.forEach(result => {
            if (result.status === 'success') {
                const data = result.data.extractedData;
                rows.push([
                    result.fileName,
                    data.documentType,
                    data.content.title,
                    data.content.summary,
                    result.processedAt
                ]);
            }
        });
        
        return [headers, ...rows].map(row => 
            row.map(cell => `"${cell}"`).join(',')
        ).join('\n');
    }
    
    /**
     * 導出為JSON格式
     */
    exportToJSON(results) {
        return JSON.stringify(results, null, 2);
    }
    
    /**
     * 導出為QuickBooks格式
     */
    exportToQuickBooks(results, documentType) {
        if (documentType !== 'bank-statement') {
            throw new Error('QuickBooks格式僅支援銀行對帳單');
        }
        
        // 簡化的QBO格式
        let qboContent = '<?xml version="1.0" encoding="UTF-8"?>\n';
        qboContent += '<QBXML>\n';
        qboContent += '<QBXMLMsgsRq onError="stopOnError">\n';
        
        results.forEach(result => {
            if (result.status === 'success' && result.data.extractedData.transactions) {
                result.data.extractedData.transactions.forEach(transaction => {
                    qboContent += '<BankTxnAdd>\n';
                    qboContent += `<Date>${transaction.date}</Date>\n`;
                    qboContent += `<Memo>${transaction.description}</Memo>\n`;
                    qboContent += `<Amount>${transaction.amount}</Amount>\n`;
                    qboContent += '</BankTxnAdd>\n';
                });
            }
        });
        
        qboContent += '</QBXMLMsgsRq>\n';
        qboContent += '</QBXML>';
        
        return qboContent;
    }
    
    /**
     * 下載文件
     */
    downloadFile(content, fileName, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        
        console.log(`📥 已下載文件: ${fileName}`);
    }
    
    /**
     * 發送進度事件
     */
    dispatchProgressEvent(processed, total) {
        const progress = Math.round((processed / total) * 100);
        
        window.dispatchEvent(new CustomEvent('batchProgress', {
            detail: { progress, processed, total }
        }));
    }
    
    /**
     * 發送文檔處理完成事件
     */
    dispatchDocumentProcessedEvent(fileName, result) {
        window.dispatchEvent(new CustomEvent('documentProcessed', {
            detail: { file: fileName, result }
        }));
    }
}

// 暫時停用：整合到統一處理器中
// window.VaultCaddyProcessor = new VaultCaddyProcessor();

console.log('⚠️ VaultCaddy Enhanced File Processor 已停用 - 整合到統一處理器');
