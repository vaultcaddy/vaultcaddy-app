/**
 * VaultCaddy AI文檔處理器
 * 處理文件上傳後的完整工作流程
 */

class AIDocumentProcessor {
    constructor() {
        this.apiKey = null;
        this.processingQueue = [];
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        // 從配置中獲取API密鑰
        this.apiKey = window.config?.googleAI?.apiKey || 'demo-key';
        console.log('🤖 AI文檔處理器已初始化');
    }
    
    /**
     * 主要處理函數 - 處理上傳的文件
     */
    async processUploadedFiles(files, documentType) {
        console.log(`🚀 開始處理 ${files.length} 個文件 (${documentType})`);
        
        const results = [];
        
        for (const file of files) {
            try {
                const result = await this.processFile(file, documentType);
                results.push(result);
            } catch (error) {
                console.error(`❌ 處理文件 ${file.name} 失敗:`, error);
                results.push({
                    fileName: file.name,
                    status: 'error',
                    error: error.message
                });
            }
        }
        
        return results;
    }
    
    /**
     * 處理單個文件的完整流程
     */
    async processFile(file, documentType) {
        console.log(`📄 處理文件: ${file.name} (${documentType})`);
        
        // 步驟1: 估算頁數
        const pageCount = await this.estimatePageCount(file);
        console.log(`📊 估算頁數: ${pageCount} 頁`);
        
        // 步驟2: 檢查Credits
        const creditsRequired = pageCount; // 1頁 = 1 Credit
        const creditsAvailable = this.getUserCredits();
        
        console.log(`💰 需要Credits: ${creditsRequired}, 可用Credits: ${creditsAvailable}`);
        
        if (creditsRequired > creditsAvailable) {
            throw new Error(`Credits不足！需要 ${creditsRequired} Credits，但您只有 ${creditsAvailable} Credits`);
        }
        
        // 步驟3: 扣除Credits
        this.deductCredits(creditsRequired);
        
        // 步驟4: 使用AI工具處理文件
        const extractedData = await this.extractDataWithAI(file, documentType);
        
        // 步驟5: 返回處理結果
        return {
            fileName: file.name,
            documentType: documentType,
            pageCount: pageCount,
            creditsUsed: creditsRequired,
            status: 'success',
            extractedData: extractedData,
            processedAt: new Date().toISOString()
        };
    }
    
    /**
     * 估算PDF文件頁數
     */
    async estimatePageCount(file) {
        return new Promise((resolve) => {
            if (file.type === 'application/pdf') {
                // 簡單估算：每MB約10頁
                const estimatedPages = Math.max(1, Math.ceil(file.size / (1024 * 1024) * 10));
                resolve(estimatedPages);
            } else {
                // 圖片文件算1頁
                resolve(1);
            }
        });
    }
    
    /**
     * 獲取用戶當前Credits
     */
    getUserCredits() {
        return parseInt(localStorage.getItem('userCredits') || '0');
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
     * 使用AI工具提取數據
     */
    async extractDataWithAI(file, documentType) {
        console.log(`🤖 使用AI提取 ${documentType} 數據...`);
        
        // 根據文檔類型決定要提取的數據
        const extractionConfig = this.getExtractionConfig(documentType);
        
        // 模擬AI處理（實際應該調用Google AI API）
        await this.simulateAIProcessing();
        
        // 根據文檔類型生成模擬數據
        return this.generateMockData(file.name, documentType, extractionConfig);
    }
    
    /**
     * 獲取不同文檔類型的提取配置
     */
    getExtractionConfig(documentType) {
        const configs = {
            'bank-statement': {
                fields: [
                    'accountNumber',
                    'accountHolder',
                    'statementPeriod',
                    'openingBalance',
                    'closingBalance',
                    'transactions'
                ],
                transactionFields: [
                    'date',
                    'description', 
                    'amount',
                    'balance',
                    'type'
                ]
            },
            'invoice': {
                fields: [
                    'invoiceNumber',
                    'issueDate',
                    'dueDate',
                    'vendor',
                    'customer',
                    'totalAmount',
                    'taxAmount',
                    'lineItems'
                ],
                lineItemFields: [
                    'description',
                    'quantity',
                    'unitPrice',
                    'totalPrice'
                ]
            },
            'receipt': {
                fields: [
                    'receiptNumber',
                    'date',
                    'merchant',
                    'totalAmount',
                    'taxAmount',
                    'paymentMethod',
                    'items'
                ],
                itemFields: [
                    'name',
                    'quantity',
                    'price'
                ]
            },
            'general': {
                fields: [
                    'documentType',
                    'date',
                    'title',
                    'content',
                    'keyInformation'
                ]
            }
        };
        
        return configs[documentType] || configs['general'];
    }
    
    /**
     * 模擬AI處理時間
     */
    async simulateAIProcessing() {
        // 模擬1-3秒的處理時間
        const processingTime = Math.random() * 2000 + 1000;
        await new Promise(resolve => setTimeout(resolve, processingTime));
    }
    
    /**
     * 生成模擬提取數據
     */
    generateMockData(fileName, documentType, config) {
        const mockData = {
            documentType: documentType,
            fileName: fileName,
            extractedFields: {}
        };
        
        switch (documentType) {
            case 'bank-statement':
                mockData.extractedFields = {
                    accountNumber: '****1234',
                    accountHolder: 'Caddy Vault',
                    statementPeriod: '2025-02-01 to 2025-02-28',
                    openingBalance: 1493.98,
                    closingBalance: 34892.80,
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
                        }
                    ]
                };
                break;
                
            case 'invoice':
                mockData.extractedFields = {
                    invoiceNumber: 'INV-2025-001',
                    issueDate: '2025-02-15',
                    dueDate: '2025-03-15',
                    vendor: 'VaultCaddy Services',
                    customer: 'Demo Customer',
                    totalAmount: 1200.00,
                    taxAmount: 120.00,
                    lineItems: [
                        {
                            description: 'Document Processing Service',
                            quantity: 1,
                            unitPrice: 1000.00,
                            totalPrice: 1000.00
                        }
                    ]
                };
                break;
                
            case 'receipt':
                mockData.extractedFields = {
                    receiptNumber: 'RCP-001',
                    date: '2025-02-20',
                    merchant: 'Demo Store',
                    totalAmount: 45.99,
                    taxAmount: 4.59,
                    paymentMethod: 'Credit Card',
                    items: [
                        {
                            name: 'Office Supplies',
                            quantity: 2,
                            price: 22.99
                        }
                    ]
                };
                break;
                
            default:
                mockData.extractedFields = {
                    documentType: 'General Document',
                    date: new Date().toISOString().split('T')[0],
                    title: fileName,
                    content: 'Document content extracted by AI',
                    keyInformation: ['Key point 1', 'Key point 2']
                };
        }
        
        return mockData;
    }
    
    /**
     * 導出數據為不同格式
     */
    exportData(data, format = 'json') {
        switch (format) {
            case 'csv':
                return this.exportToCSV(data);
            case 'excel':
                return this.exportToExcel(data);
            case 'json':
            default:
                return JSON.stringify(data, null, 2);
        }
    }
    
    /**
     * 導出為CSV格式
     */
    exportToCSV(data) {
        if (data.documentType === 'bank-statement' && data.extractedFields.transactions) {
            const headers = ['Date', 'Description', 'Amount', 'Balance', 'Type'];
            const rows = data.extractedFields.transactions.map(t => [
                t.date, t.description, t.amount, t.balance, t.type
            ]);
            
            return [headers, ...rows].map(row => row.join(',')).join('\n');
        }
        
        // 其他文檔類型的CSV導出邏輯...
        return 'CSV export not implemented for this document type';
    }
}

// 已停用：避免與其他處理器衝突
// window.AIDocumentProcessor = new AIDocumentProcessor();

console.log('⚠️ AI文檔處理器已停用 - 使用統一處理器');

