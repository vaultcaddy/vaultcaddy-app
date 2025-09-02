/**
 * VaultCaddy 完整文檔處理系統
 * 整合 AI 服務、文件處理、數據驗證和導出功能
 */

class VaultCaddyDocumentProcessor {
    constructor() {
        this.processingResults = new Map();
        this.processingQueue = [];
        this.isProcessing = false;
        this.uploadedFiles = new Map();
        
        // 初始化統計數據
        this.statistics = {
            totalProcessed: 0,
            successRate: 0,
            creditsUsed: 0,
            processingTime: 0
        };
        
        this.init();
    }
    
    async init() {
        console.log('🚀 VaultCaddy Document Processor 初始化...');
        this.loadStoredData();
        this.setupEventListeners();
        console.log('✅ Document Processor 初始化完成');
    }
    
    /**
     * 載入儲存的數據
     */
    loadStoredData() {
        try {
            const storedResults = localStorage.getItem('vaultcaddy_processing_results');
            if (storedResults) {
                const results = JSON.parse(storedResults);
                Object.entries(results).forEach(([key, value]) => {
                    this.processingResults.set(key, value);
                });
            }
            
            const storedStats = localStorage.getItem('vaultcaddy_statistics');
            if (storedStats) {
                this.statistics = { ...this.statistics, ...JSON.parse(storedStats) };
            }
        } catch (error) {
            console.error('載入儲存數據失敗:', error);
        }
    }
    
    /**
     * 儲存數據到 localStorage
     */
    saveData() {
        try {
            const resultsObj = Object.fromEntries(this.processingResults);
            localStorage.setItem('vaultcaddy_processing_results', JSON.stringify(resultsObj));
            localStorage.setItem('vaultcaddy_statistics', JSON.stringify(this.statistics));
        } catch (error) {
            console.error('儲存數據失敗:', error);
        }
    }
    
    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 監聽處理完成事件
        document.addEventListener('documentProcessed', (event) => {
            this.handleProcessingComplete(event.detail);
        });
        
        // 監聽頁面卸載時儲存數據
        window.addEventListener('beforeunload', () => {
            this.saveData();
        });
    }
    
    /**
     * 處理文件上傳
     */
    async processFiles(files, documentType = 'general') {
        console.log(`📄 開始處理 ${files.length} 個文件，類型: ${documentType}`);
        
        const results = [];
        
        for (const file of files) {
            try {
                const result = await this.processFile(file, documentType);
                results.push(result);
                
                // 更新統計數據
                this.updateStatistics(result);
                
                // 觸發處理完成事件
                document.dispatchEvent(new CustomEvent('documentProcessed', {
                    detail: { file: file.name, result, documentType }
                }));
                
            } catch (error) {
                console.error(`處理文件 ${file.name} 失敗:`, error);
                results.push({
                    fileName: file.name,
                    status: 'error',
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        this.saveData();
        return results;
    }
    
    /**
     * 處理單個文件
     */
    async processFile(file, documentType) {
        const startTime = Date.now();
        const fileId = this.generateFileId(file);
        
        console.log(`🔄 處理文件: ${file.name} (${documentType})`);
        
        // 模擬 AI 處理（真實環境中會調用 AI 服務）
        const processingResult = await this.simulateAIProcessing(file, documentType);
        
        const endTime = Date.now();
        const processingTime = endTime - startTime;
        
        const result = {
            fileId,
            fileName: file.name,
            fileSize: file.size,
            documentType,
            status: 'success',
            processingTime,
            timestamp: new Date().toISOString(),
            extractedData: processingResult.extractedData,
            confidence: processingResult.confidence,
            creditsUsed: this.calculateCredits(file.size, documentType)
        };
        
        // 儲存結果
        this.processingResults.set(fileId, result);
        
        return result;
    }
    
    /**
     * 模擬 AI 處理（開發階段）
     */
    async simulateAIProcessing(file, documentType) {
        // 模擬處理延遲
        await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
        
        const mockData = this.generateMockData(documentType, file.name);
        
        return {
            extractedData: mockData,
            confidence: 0.85 + Math.random() * 0.14 // 85-99% 信心度
        };
    }
    
    /**
     * 生成模擬數據
     */
    generateMockData(documentType, fileName) {
        const baseData = {
            fileName,
            processedAt: new Date().toISOString()
        };
        
        switch (documentType) {
            case 'bank-statement':
                return {
                    ...baseData,
                    accountNumber: '****' + Math.random().toString().slice(2, 6),
                    accountHolder: 'YEUNG CAVLIN',
                    bankName: 'Sample Bank',
                    statementPeriod: {
                        from: '2024-01-01',
                        to: '2024-01-31'
                    },
                    openingBalance: (Math.random() * 50000).toFixed(2),
                    closingBalance: (Math.random() * 50000).toFixed(2),
                    transactions: this.generateMockTransactions()
                };
                
            case 'invoice':
                return {
                    ...baseData,
                    invoiceNumber: 'INV-' + Math.random().toString().slice(2, 8),
                    vendor: 'ABC Company Ltd.',
                    date: '2024-03-14',
                    dueDate: '2024-04-14',
                    totalAmount: (Math.random() * 5000).toFixed(2),
                    taxAmount: (Math.random() * 500).toFixed(2),
                    lineItems: this.generateMockLineItems()
                };
                
            case 'receipt':
                return {
                    ...baseData,
                    merchant: 'Sample Store',
                    date: new Date().toISOString().split('T')[0],
                    totalAmount: (Math.random() * 200).toFixed(2),
                    taxAmount: (Math.random() * 20).toFixed(2),
                    items: this.generateMockReceiptItems()
                };
                
            default:
                return {
                    ...baseData,
                    extractedText: `這是從 ${fileName} 提取的文本內容。包含各種信息和數據。`,
                    keyFields: {
                        dates: ['2024-03-14', '2024-03-15'],
                        amounts: ['$1,234.56', '$567.89'],
                        entities: ['公司名稱', '地址信息']
                    }
                };
        }
    }
    
    /**
     * 生成模擬交易記錄
     */
    generateMockTransactions() {
        const transactions = [];
        const count = 5 + Math.floor(Math.random() * 10);
        
        for (let i = 0; i < count; i++) {
            transactions.push({
                date: new Date(2024, 0, i + 1).toISOString().split('T')[0],
                description: `Transaction ${i + 1}`,
                amount: (Math.random() * 1000 - 500).toFixed(2),
                balance: (Math.random() * 10000).toFixed(2),
                type: Math.random() > 0.5 ? 'credit' : 'debit'
            });
        }
        
        return transactions;
    }
    
    /**
     * 生成模擬發票項目
     */
    generateMockLineItems() {
        const items = [];
        const count = 2 + Math.floor(Math.random() * 5);
        
        for (let i = 0; i < count; i++) {
            items.push({
                description: `Product ${i + 1}`,
                quantity: Math.floor(Math.random() * 10) + 1,
                unitPrice: (Math.random() * 100).toFixed(2),
                totalPrice: (Math.random() * 500).toFixed(2)
            });
        }
        
        return items;
    }
    
    /**
     * 生成模擬收據項目
     */
    generateMockReceiptItems() {
        const items = [];
        const count = 1 + Math.floor(Math.random() * 8);
        
        for (let i = 0; i < count; i++) {
            items.push({
                name: `Item ${i + 1}`,
                price: (Math.random() * 50).toFixed(2),
                quantity: Math.floor(Math.random() * 3) + 1
            });
        }
        
        return items;
    }
    
    /**
     * 計算處理所需 Credits
     */
    calculateCredits(fileSize, documentType) {
        const baseCredits = {
            'bank-statement': 2,
            'invoice': 1,
            'receipt': 1,
            'general': 1
        };
        
        const sizeMultiplier = Math.ceil(fileSize / (1024 * 1024)); // 每 MB
        return (baseCredits[documentType] || 1) * Math.max(1, sizeMultiplier);
    }
    
    /**
     * 更新統計數據
     */
    updateStatistics(result) {
        this.statistics.totalProcessed++;
        this.statistics.creditsUsed += result.creditsUsed || 0;
        
        // 計算成功率
        const successfulResults = Array.from(this.processingResults.values())
            .filter(r => r.status === 'success');
        this.statistics.successRate = 
            Math.round((successfulResults.length / this.statistics.totalProcessed) * 100);
        
        // 更新用戶 Credits
        this.updateUserCredits(result.creditsUsed || 0);
    }
    
    /**
     * 更新用戶 Credits
     */
    updateUserCredits(creditsUsed) {
        const currentCredits = parseInt(localStorage.getItem('userCredits') || '7');
        const newCredits = Math.max(0, currentCredits - creditsUsed);
        localStorage.setItem('userCredits', newCredits.toString());
        
        // 觸發 Credits 更新事件
        document.dispatchEvent(new CustomEvent('creditsUpdated', {
            detail: { credits: newCredits, used: creditsUsed }
        }));
    }
    
    /**
     * 生成文件 ID
     */
    generateFileId(file) {
        return `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    /**
     * 獲取處理結果
     */
    getProcessingResults() {
        return Array.from(this.processingResults.values());
    }
    
    /**
     * 獲取統計數據
     */
    getStatistics() {
        return this.statistics;
    }
    
    /**
     * 導出數據為 CSV
     */
    exportToCSV(results, documentType) {
        console.log('📥 導出 CSV 格式數據...');
        
        if (!results || results.length === 0) {
            throw new Error('沒有可導出的數據');
        }
        
        let csvContent = '';
        
        switch (documentType) {
            case 'bank-statement':
                csvContent = this.exportBankStatementCSV(results);
                break;
            case 'invoice':
                csvContent = this.exportInvoiceCSV(results);
                break;
            case 'receipt':
                csvContent = this.exportReceiptCSV(results);
                break;
            default:
                csvContent = this.exportGeneralCSV(results);
        }
        
        return csvContent;
    }
    
    /**
     * 銀行對帳單 CSV 導出
     */
    exportBankStatementCSV(results) {
        const headers = ['Date', 'Description', 'Amount', 'Balance', 'Type', 'Account Number'];
        let csv = headers.join(',') + '\n';
        
        results.forEach(result => {
            if (result.extractedData && result.extractedData.transactions) {
                result.extractedData.transactions.forEach(transaction => {
                    const row = [
                        transaction.date,
                        `"${transaction.description}"`,
                        transaction.amount,
                        transaction.balance,
                        transaction.type,
                        result.extractedData.accountNumber || ''
                    ];
                    csv += row.join(',') + '\n';
                });
            }
        });
        
        return csv;
    }
    
    /**
     * 發票 CSV 導出
     */
    exportInvoiceCSV(results) {
        const headers = ['Invoice Number', 'Vendor', 'Date', 'Due Date', 'Item Description', 'Quantity', 'Unit Price', 'Total Price'];
        let csv = headers.join(',') + '\n';
        
        results.forEach(result => {
            if (result.extractedData && result.extractedData.lineItems) {
                result.extractedData.lineItems.forEach(item => {
                    const row = [
                        result.extractedData.invoiceNumber || '',
                        `"${result.extractedData.vendor || ''}"`,
                        result.extractedData.date || '',
                        result.extractedData.dueDate || '',
                        `"${item.description}"`,
                        item.quantity,
                        item.unitPrice,
                        item.totalPrice
                    ];
                    csv += row.join(',') + '\n';
                });
            }
        });
        
        return csv;
    }
    
    /**
     * 收據 CSV 導出
     */
    exportReceiptCSV(results) {
        const headers = ['Date', 'Merchant', 'Item Name', 'Price', 'Quantity', 'Total Amount'];
        let csv = headers.join(',') + '\n';
        
        results.forEach(result => {
            if (result.extractedData && result.extractedData.items) {
                result.extractedData.items.forEach(item => {
                    const row = [
                        result.extractedData.date || '',
                        `"${result.extractedData.merchant || ''}"`,
                        `"${item.name}"`,
                        item.price,
                        item.quantity,
                        result.extractedData.totalAmount || ''
                    ];
                    csv += row.join(',') + '\n';
                });
            }
        });
        
        return csv;
    }
    
    /**
     * 通用 CSV 導出
     */
    exportGeneralCSV(results) {
        const headers = ['File Name', 'Processed At', 'Extracted Text', 'Confidence'];
        let csv = headers.join(',') + '\n';
        
        results.forEach(result => {
            const row = [
                `"${result.fileName}"`,
                result.timestamp,
                `"${result.extractedData.extractedText || ''}"`,
                result.confidence || ''
            ];
            csv += row.join(',') + '\n';
        });
        
        return csv;
    }
    
    /**
     * 導出數據為 JSON
     */
    exportToJSON(results) {
        console.log('📥 導出 JSON 格式數據...');
        return JSON.stringify(results, null, 2);
    }
    
    /**
     * 導出數據為 Excel (模擬)
     */
    exportToExcel(results, documentType) {
        console.log('📥 導出 Excel 格式數據...');
        // 實際實現需要使用 SheetJS 或類似庫
        // 這裡返回 CSV 格式作為簡化實現
        return this.exportToCSV(results, documentType);
    }
    
    /**
     * QuickBooks 格式導出
     */
    exportToQuickBooks(results, documentType) {
        console.log('📥 導出 QuickBooks 格式數據...');
        
        if (documentType !== 'bank-statement') {
            throw new Error('QuickBooks 導出目前只支援銀行對帳單');
        }
        
        // QuickBooks 需要 QBO 格式
        let qboContent = this.generateQBOHeader();
        
        results.forEach(result => {
            if (result.extractedData && result.extractedData.transactions) {
                result.extractedData.transactions.forEach(transaction => {
                    qboContent += this.generateQBOTransaction(transaction, result.extractedData);
                });
            }
        });
        
        qboContent += this.generateQBOFooter();
        return qboContent;
    }
    
    /**
     * 生成 QBO 標頭
     */
    generateQBOHeader() {
        return `OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<DTSERVER>${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}
<LANGUAGE>ENG
</SONRS>
</SIGNONMSGSRSV1>
<BANKMSGSRSV1>
<STMTTRNRS>
<TRNUID>1
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<STMTRS>
<CURDEF>USD
<BANKACCTFROM>
<BANKID>123456789
<ACCTID>1234567890
<ACCTTYPE>CHECKING
</BANKACCTFROM>
<BANKTRANLIST>
<DTSTART>${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}
<DTEND>${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}
`;
    }
    
    /**
     * 生成 QBO 交易記錄
     */
    generateQBOTransaction(transaction, accountData) {
        const date = transaction.date.replace(/-/g, '');
        return `<STMTTRN>
<TRNTYPE>${transaction.type === 'credit' ? 'CREDIT' : 'DEBIT'}
<DTPOSTED>${date}
<TRNAMT>${transaction.amount}
<FITID>${transaction.date}_${Math.random().toString(36).substr(2, 9)}
<NAME>${transaction.description}
</STMTTRN>
`;
    }
    
    /**
     * 生成 QBO 結尾
     */
    generateQBOFooter() {
        return `</BANKTRANLIST>
<LEDGERBAL>
<BALAMT>0.00
<DTASOF>${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}
</LEDGERBAL>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
</OFX>`;
    }
    
    /**
     * 下載文件
     */
    downloadFile(content, fileName, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        console.log(`✅ 文件已下載: ${fileName}`);
    }
    
    /**
     * 批次處理檔案
     */
    async batchProcess(files, documentType, options = {}) {
        console.log(`🔄 開始批次處理 ${files.length} 個檔案...`);
        
        const batchId = `batch_${Date.now()}`;
        const batchResults = [];
        const maxConcurrent = options.maxConcurrent || 3;
        
        // 分批處理以避免過載
        for (let i = 0; i < files.length; i += maxConcurrent) {
            const batch = Array.from(files).slice(i, i + maxConcurrent);
            const promises = batch.map(file => this.processFile(file, documentType));
            
            try {
                const results = await Promise.all(promises);
                batchResults.push(...results);
                
                // 更新進度
                const progress = Math.round(((i + batch.length) / files.length) * 100);
                document.dispatchEvent(new CustomEvent('batchProgress', {
                    detail: { batchId, progress, processed: i + batch.length, total: files.length }
                }));
                
            } catch (error) {
                console.error(`批次處理錯誤:`, error);
            }
        }
        
        // 儲存批次結果
        const batchSummary = {
            batchId,
            timestamp: new Date().toISOString(),
            documentType,
            totalFiles: files.length,
            successfulFiles: batchResults.filter(r => r.status === 'success').length,
            failedFiles: batchResults.filter(r => r.status === 'error').length,
            results: batchResults
        };
        
        localStorage.setItem(`batch_${batchId}`, JSON.stringify(batchSummary));
        this.saveData();
        
        console.log(`✅ 批次處理完成: ${batchSummary.successfulFiles}/${batchSummary.totalFiles} 成功`);
        
        return batchSummary;
    }
    
    /**
     * 數據驗證
     */
    validateExtractedData(result, documentType) {
        const validations = [];
        
        switch (documentType) {
            case 'bank-statement':
                validations.push(...this.validateBankStatement(result.extractedData));
                break;
            case 'invoice':
                validations.push(...this.validateInvoice(result.extractedData));
                break;
            case 'receipt':
                validations.push(...this.validateReceipt(result.extractedData));
                break;
        }
        
        return {
            isValid: validations.every(v => v.isValid),
            validations,
            confidence: result.confidence
        };
    }
    
    /**
     * 銀行對帳單驗證
     */
    validateBankStatement(data) {
        const validations = [];
        
        // 檢查必要欄位
        validations.push({
            field: 'accountNumber',
            isValid: !!data.accountNumber,
            message: data.accountNumber ? '帳戶號碼已識別' : '缺少帳戶號碼'
        });
        
        validations.push({
            field: 'transactions',
            isValid: data.transactions && data.transactions.length > 0,
            message: data.transactions ? `識別到 ${data.transactions.length} 筆交易` : '未找到交易記錄'
        });
        
        // 檢查餘額計算
        if (data.transactions && data.transactions.length > 0) {
            const balanceCheck = this.validateBalanceCalculation(data.transactions);
            validations.push(balanceCheck);
        }
        
        return validations;
    }
    
    /**
     * 發票驗證
     */
    validateInvoice(data) {
        const validations = [];
        
        validations.push({
            field: 'invoiceNumber',
            isValid: !!data.invoiceNumber,
            message: data.invoiceNumber ? '發票號碼已識別' : '缺少發票號碼'
        });
        
        validations.push({
            field: 'totalAmount',
            isValid: !!data.totalAmount && !isNaN(parseFloat(data.totalAmount)),
            message: data.totalAmount ? '總金額已識別' : '缺少有效總金額'
        });
        
        return validations;
    }
    
    /**
     * 收據驗證
     */
    validateReceipt(data) {
        const validations = [];
        
        validations.push({
            field: 'merchant',
            isValid: !!data.merchant,
            message: data.merchant ? '商家已識別' : '缺少商家信息'
        });
        
        validations.push({
            field: 'totalAmount',
            isValid: !!data.totalAmount && !isNaN(parseFloat(data.totalAmount)),
            message: data.totalAmount ? '總金額已識別' : '缺少有效總金額'
        });
        
        return validations;
    }
    
    /**
     * 驗證餘額計算
     */
    validateBalanceCalculation(transactions) {
        // 簡化的餘額驗證邏輯
        let calculatedBalance = parseFloat(transactions[0]?.balance || 0);
        let isValid = true;
        
        for (let i = 1; i < transactions.length; i++) {
            const prevTransaction = transactions[i - 1];
            const currentTransaction = transactions[i];
            
            const expectedBalance = parseFloat(prevTransaction.balance) + parseFloat(currentTransaction.amount);
            const actualBalance = parseFloat(currentTransaction.balance);
            
            if (Math.abs(expectedBalance - actualBalance) > 0.01) {
                isValid = false;
                break;
            }
        }
        
        return {
            field: 'balanceCalculation',
            isValid,
            message: isValid ? '餘額計算正確' : '發現餘額計算不一致'
        };
    }
}

// 全局實例
window.VaultCaddyProcessor = new VaultCaddyDocumentProcessor();

// 導出給其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaultCaddyDocumentProcessor;
}
