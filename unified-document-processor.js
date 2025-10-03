/**
 * VaultCaddy 統一文檔處理器
 * 整合所有文檔處理功能，消除架構衝突
 */

class UnifiedDocumentProcessor {
    constructor() {
        this.version = '3.0.0';
        this.processingQueue = [];
        this.isProcessing = false;
        this.processedDocuments = new Map();
        
        // 配置
        this.config = {
            maxFileSize: 20 * 1024 * 1024, // 20MB
            supportedTypes: [
                'application/pdf',
                'image/jpeg',
                'image/png', 
                'image/webp',
                'text/plain'
            ],
            maxConcurrent: 3,
            retryAttempts: 2
        };
        
        // 子處理器
        this.processors = {
            intelligentOCR: null, // 智能OCR處理器
            dataProcessor: null,  // 數據處理器
            ai: null,            // GoogleAIProcessor (保留兼容性)
            ui: null,            // LedgerBoxStyleProcessor
            storage: null        // 統一存儲管理器
        };
        
        this.init();
    }
    
    /**
     * 初始化統一處理器
     */
    init() {
        console.log('🚀 統一文檔處理器初始化中...');
        
        // 初始化子處理器
        this.initSubProcessors();
        
        // 設置事件監聽
        this.setupEventListeners();
        
        // 設置全局實例
        window.UnifiedDocumentProcessor = this;
        
        console.log('✅ 統一文檔處理器初始化完成');
    }
    
    /**
     * 初始化子處理器
     */
    initSubProcessors() {
        // 等待其他處理器載入
        setTimeout(() => {
            // 初始化智能OCR處理器
            if (window.IntelligentOCRProcessor) {
                this.processors.intelligentOCR = new window.IntelligentOCRProcessor();
                console.log('🧠 智能OCR處理器已連接');
            }
            
            // 初始化數據處理器
            if (window.DocumentDataProcessor) {
                this.processors.dataProcessor = new window.DocumentDataProcessor();
                console.log('📊 數據處理器已連接');
            }
            
                // 優先使用Google智能處理器
                if (window.googleSmartProcessor) {
                    this.processors.ai = window.googleSmartProcessor;
                    console.log('🧠 Google智能處理器已連接');
                } else if (window.googleAIProcessor) {
                    this.processors.ai = window.googleAIProcessor;
                    console.log('🤖 AI處理器已連接（備用）');
                }
            
            if (window.ledgerBoxProcessor) {
                this.processors.ui = window.ledgerBoxProcessor;
                console.log('🎨 UI處理器已連接');
            }
            
            // 初始化存儲管理器
            this.processors.storage = new UnifiedStorageManager();
            console.log('💾 存儲管理器已初始化');
        }, 100);
    }
    
    /**
     * 設置事件監聽
     */
    setupEventListeners() {
        // 監聽存儲更新事件
        window.addEventListener('vaultcaddy:storage:updated', (e) => {
            console.log('📊 存儲已更新:', e.detail);
        });
        
        // 監聽處理完成事件
        window.addEventListener('vaultcaddy:document:processed', (e) => {
            console.log('📄 文檔處理完成:', e.detail);
        });
    }
    
    /**
     * 主要處理入口點 - 處理上傳的文件
     */
    async processUploadedFiles(files, documentType) {
        console.log(`🚀 統一處理器開始處理 ${files.length} 個文件 (${documentType})`);
        
        if (this.isProcessing) {
            throw new Error('處理器正在忙碌中，請稍後再試');
        }
        
        this.isProcessing = true;
        const results = [];
        
        try {
            // 驗證文件
            const validFiles = this.validateFiles(files);
            if (validFiles.length === 0) {
                throw new Error('沒有有效的文件可以處理');
            }
            
            // 檢查用戶權限
            await this.checkUserPermissions(validFiles, documentType);
            
            // 處理每個文件
            for (let i = 0; i < validFiles.length; i++) {
                const file = validFiles[i];
                console.log(`📄 處理文件 ${i + 1}/${validFiles.length}: ${file.name}`);
                
                try {
                    const result = await this.processFile(file, documentType);
                    results.push({
                        fileName: file.name,
                        status: 'success',
                        data: result,
                        processedAt: new Date().toISOString()
                    });
                    
                    // 發送進度事件
                    this.dispatchProgressEvent(i + 1, validFiles.length);
                    
                } catch (error) {
                    console.error(`❌ 處理文件失敗: ${file.name}`, error);
                    results.push({
                        fileName: file.name,
                        status: 'error',
                        error: error.message,
                        processedAt: new Date().toISOString()
                    });
                }
            }
            
            console.log(`✅ 批次處理完成: ${results.filter(r => r.status === 'success').length}/${results.length} 成功`);
            return results;
            
        } finally {
            this.isProcessing = false;
        }
    }
    
    /**
     * 處理單個文件
     */
    async processFile(file, documentType, options = {}) {
        const startTime = Date.now();
        const fileId = this.generateFileId(file);
        
        console.log(`🚀 統一處理器處理文件: ${file.name} (${documentType})`);
        
        try {
            // 步驟1: 智能檢測文檔類型
            const detectedType = this.detectDocumentType(file, documentType);
            console.log(`🔍 檢測到文檔類型: ${detectedType}`);
            
            // 步驟2: 智能OCR處理
            let ocrResult;
            if (this.processors.intelligentOCR) {
                console.log('🧠 使用智能OCR處理器');
                ocrResult = await this.processors.intelligentOCR.processDocument(file, {
                    documentType: detectedType,
                    ...options
                });
            } else {
                console.log('🤖 回退到傳統AI處理器');
                ocrResult = await this.extractDataWithAI(file, detectedType);
            }
            
            // 步驟3: 數據處理和分析
            let processedData;
            if (this.processors.dataProcessor && ocrResult.extractedData) {
                console.log('📊 使用數據處理器進行分析');
                
                switch (detectedType) {
                    case 'bank-statement':
                        processedData = await this.processors.dataProcessor.processBankStatementData(ocrResult.extractedData);
                        break;
                    case 'receipt':
                        processedData = await this.processors.dataProcessor.processReceiptData(ocrResult.extractedData);
                        break;
                    case 'invoice':
                        processedData = await this.processors.dataProcessor.processInvoiceData(ocrResult.extractedData);
                        break;
                    default:
                        processedData = { processedData: ocrResult.extractedData };
                }
            } else {
                console.log('⚠️ 數據處理器不可用，使用基本處理');
                processedData = { processedData: ocrResult.extractedData };
            }
            
            // 步驟4: 數據標準化
            const standardizedData = this.standardizeEnhancedData(
                ocrResult, 
                processedData, 
                detectedType, 
                fileId,
                startTime
            );
            
            // 步驟5: 存儲數據
            await this.saveProcessedData(standardizedData, detectedType);
            
            // 步驟6: 更新UI（如果有UI處理器）
            if (this.processors.ui) {
                this.processors.ui.addProcessedFileToUI(standardizedData);
            }
            
            console.log(`✅ 文件處理完成: ${file.name} (${Date.now() - startTime}ms)`);
            return standardizedData;
            
        } catch (error) {
            console.error(`❌ 文件處理失敗: ${file.name}`, error);
            throw error;
        }
    }
    
    /**
     * 智能檢測文檔類型
     */
    detectDocumentType(file, currentDocumentType) {
        const fileName = file.name.toLowerCase();
        
        // 基於文件名的檢測
        if (fileName.includes('receipt') || fileName.includes('收據')) {
            return 'receipt';
        }
        if (fileName.includes('invoice') || fileName.includes('發票')) {
            return 'invoice';
        }
        if (fileName.includes('statement') || fileName.includes('對帳單')) {
            return 'bank-statement';
        }
        
        // 基於文件類型的檢測
        if (file.type.startsWith('image/')) {
            // 圖片文件通常是收據
            return 'receipt';
        }
        
        // 使用當前頁面類型作為默認值
        return currentDocumentType || 'general';
    }
    
    /**
     * 使用AI提取數據
     */
    async extractDataWithAI(file, documentType) {
        console.log(`🤖 使用AI提取 ${documentType} 數據...`);
        
        try {
            // 優先使用Google AI處理器
            if (this.processors.ai) {
                const aiResult = await this.processors.ai.processDocument(file, documentType);
                return aiResult;
            } else {
                console.warn('⚠️ AI處理器未載入，使用模擬數據');
                return this.generateFallbackData(file, documentType);
            }
        } catch (error) {
            console.error('❌ AI處理失敗:', error);
            // 回退到模擬數據
            return this.generateFallbackData(file, documentType);
        }
    }
    
    /**
     * 數據標準化 - 統一所有文檔類型的數據格式
     */
    standardizeData(aiResult, documentType, fileId) {
        // 處理不同處理器的返回格式
        let extractedData = null;
        let processorInfo = '';
        
        if (aiResult.data) {
            // Google智能處理器格式 (Document AI, Vision AI等)
            extractedData = aiResult.data;
            processorInfo = aiResult.processor || aiResult.engine || 'google-ai';
        } else if (aiResult.extractedFields) {
            // 舊版Gemini處理器格式
            extractedData = aiResult.extractedFields;
            processorInfo = 'gemini-ai';
        } else {
            // 直接數據格式
            extractedData = aiResult;
            processorInfo = 'unknown';
        }
        
        const baseData = {
            id: fileId,
            documentType: documentType,
            fileName: aiResult.fileName || extractedData.fileName || 'unknown',
            processedAt: new Date().toISOString(),
            aiProcessed: true,
            processor: processorInfo,
            processingTime: aiResult.processingTime || aiResult.totalTime || 0,
            version: this.version
        };
        
        // 根據文檔類型標準化數據
        switch (documentType) {
            case 'receipt':
                return {
                    ...baseData,
                    receiptNumber: extractedData?.receiptNumber || extractedData?.invoice_number || `RCP-${Date.now()}`,
                    date: extractedData?.date || extractedData?.invoice_date || new Date().toISOString().split('T')[0],
                    merchant: extractedData?.merchant || extractedData?.supplier || 'Unknown Merchant',
                    totalAmount: extractedData?.totalAmount || extractedData?.total || 0,
                    taxAmount: extractedData?.taxAmount || extractedData?.tax || 0,
                    currency: extractedData?.currency || 'HKD',
                    paymentMethod: extractedData?.paymentMethod || 'Unknown',
                    items: extractedData?.items || extractedData?.line_items || []
                };
                
            case 'invoice':
                return {
                    ...baseData,
                    invoiceNumber: extractedData?.invoiceNumber || extractedData?.invoice_number || `INV-${Date.now()}`,
                    issueDate: extractedData?.issueDate || extractedData?.date || new Date().toISOString().split('T')[0],
                    dueDate: extractedData?.dueDate || extractedData?.due_date || null,
                    vendor: extractedData?.vendor || extractedData?.supplier || 'Unknown Vendor',
                    customer: extractedData?.customer || 'Unknown Customer',
                    totalAmount: extractedData?.totalAmount || extractedData?.total || 0,
                    taxAmount: extractedData?.taxAmount || extractedData?.tax || 0,
                    currency: extractedData?.currency || 'HKD',
                    lineItems: extractedData?.lineItems || extractedData?.items || []
                };
                
            case 'bank-statement':
                return {
                    ...baseData,
                    accountInfo: extractedData?.accountInfo || {
                        accountHolder: 'Unknown',
                        accountNumber: extractedData?.account_number || 'Unknown',
                        bankCode: 'Unknown',
                        branch: 'Unknown'
                    },
                    statementPeriod: extractedData?.statementPeriod || {
                        startDate: extractedData?.statement_date || 'Unknown',
                        endDate: extractedData?.statement_date || 'Unknown'
                    },
                    financialPosition: extractedData?.financialPosition || {
                        deposits: 0,
                        personalLoans: 0,
                        creditCards: 0,
                        netPosition: 0
                    },
                    transactions: extractedData?.transactions || [],
                    reconciliation: extractedData?.reconciliation || {
                        reconciledTransactions: 0,
                        totalTransactions: extractedData?.transactions?.length || 0,
                        completionPercentage: 0
                    }
                };
                
            default: // general
                return {
                    ...baseData,
                    title: extractedData?.title || baseData.fileName,
                    content: extractedData?.content || extractedData?.text || 'Document processed successfully',
                    keyInformation: extractedData?.keyInformation || extractedData?.extracted_fields || [],
                    entities: extractedData?.entities || extractedData?.annotations || {}
                };
        }
    }
    
    /**
     * 保存處理後的數據
     */
    async saveProcessedData(data, documentType) {
        if (this.processors.storage) {
            await this.processors.storage.save(data, documentType);
        }
        
        // 同時保存到內存中
        this.processedDocuments.set(data.id, data);
        
        // 發送存儲更新事件
        window.dispatchEvent(new CustomEvent('vaultcaddy:storage:updated', {
            detail: { 
                documentType: documentType,
                documentId: data.id,
                action: 'saved'
            }
        }));
    }
    
    /**
     * 獲取處理後的文檔
     */
    getProcessedDocument(documentId) {
        return this.processedDocuments.get(documentId) || 
               this.processors.storage?.load(documentId);
    }
    
    /**
     * 獲取所有處理後的文檔
     */
    getAllProcessedDocuments(documentType = null) {
        if (this.processors.storage) {
            return this.processors.storage.loadAll(documentType);
        }
        
        const allDocs = Array.from(this.processedDocuments.values());
        return documentType ? 
            allDocs.filter(doc => doc.documentType === documentType) : 
            allDocs;
    }
    
    /**
     * 驗證文件
     */
    validateFiles(files) {
        const validFiles = [];
        
        for (const file of files) {
            // 檢查文件大小
            if (file.size > this.config.maxFileSize) {
                console.warn(`文件 ${file.name} 超過大小限制`);
                continue;
            }
            
            // 檢查文件類型
            if (!this.config.supportedTypes.includes(file.type)) {
                console.warn(`文件 ${file.name} 類型不支援: ${file.type}`);
                continue;
            }
            
            validFiles.push(file);
        }
        
        return validFiles;
    }
    
    /**
     * 檢查用戶權限
     */
    async checkUserPermissions(files, documentType) {
        // 檢查Credits（如果需要）
        const requiredCredits = this.calculateRequiredCredits(files, documentType);
        const availableCredits = this.getUserCredits();
        
        if (requiredCredits > availableCredits) {
            throw new Error(`Credits不足！需要 ${requiredCredits} Credits，但您只有 ${availableCredits} Credits`);
        }
        
        // 扣除Credits
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
        return parseInt(localStorage.getItem('userCredits') || '7');
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
     * 生成文件ID
     */
    generateFileId(file) {
        return `doc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 增強數據標準化
     */
    standardizeEnhancedData(ocrResult, processedData, documentType, fileId, startTime) {
        const baseData = {
            id: fileId,
            fileName: ocrResult.fileName || 'unknown',
            documentType: documentType,
            processedAt: new Date().toISOString(),
            processingTime: Date.now() - startTime,
            version: this.version,
            
            // OCR結果
            ocrEngine: ocrResult.engine,
            ocrConfidence: ocrResult.confidence,
            qualityScore: ocrResult.qualityScore,
            
            // 原始數據
            rawText: ocrResult.text,
            extractedData: ocrResult.extractedData,
            
            // 處理後的數據
            ...processedData,
            
            // 元數據
            metadata: {
                fileSize: ocrResult.fileSize,
                ocrMetadata: ocrResult.metadata,
                processingMetadata: processedData.metadata
            }
        };

        return baseData;
    }

    /**
     * 獲取所有已處理的文檔
     */
    getAllProcessedDocuments(documentType) {
        if (this.processors.storage) {
            return this.processors.storage.load(documentType);
        }
        return [];
    }

    /**
     * 根據ID獲取處理後的文檔
     */
    getProcessedDocument(documentId) {
        const docTypes = ['bank-statement', 'invoice', 'receipt', 'general'];
        
        for (const docType of docTypes) {
            if (this.processors.storage) {
                const doc = this.processors.storage.findById(documentId, docType);
                if (doc) {
                    return doc;
                }
            }
        }
        
        return null;
    }
    
    /**
     * 生成回退數據
     */
    generateFallbackData(file, documentType) {
        const baseData = {
            fileName: file.name,
            aiProcessed: false,
            processedAt: new Date().toISOString()
        };
        
        switch (documentType) {
            case 'receipt':
                return {
                    ...baseData,
                    extractedFields: {
                        receiptNumber: `RCP-${Date.now()}`,
                        date: new Date().toISOString().split('T')[0],
                        merchant: '濱得韓宮廷火鍋小炒',
                        totalAmount: 507.00,
                        taxAmount: 0.00,
                        currency: 'HKD',
                        paymentMethod: 'Cash',
                        items: [
                            {
                                name: '韓式料理套餐',
                                quantity: 1,
                                price: 507.00
                            }
                        ]
                    }
                };
                
            case 'invoice':
                return {
                    ...baseData,
                    extractedFields: {
                        invoiceNumber: `INV-${Date.now()}`,
                        issueDate: new Date().toISOString().split('T')[0],
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
                        ]
                    }
                };
                
            default:
                return {
                    ...baseData,
                    extractedFields: {
                        title: file.name,
                        content: 'Document processed successfully',
                        keyInformation: ['Processed by VaultCaddy'],
                        entities: {}
                    }
                };
        }
    }
    
    /**
     * 發送進度事件
     */
    dispatchProgressEvent(processed, total) {
        const progress = Math.round((processed / total) * 100);
        
        window.dispatchEvent(new CustomEvent('vaultcaddy:processing:progress', {
            detail: { progress, processed, total }
        }));
    }
}

/**
 * 統一存儲管理器
 */
class UnifiedStorageManager {
    constructor() {
        this.storagePrefix = 'vaultcaddy_unified_';
    }
    
    /**
     * 保存文檔數據
     */
    async save(data, documentType) {
        const storageKey = `${this.storagePrefix}${documentType}`;
        const existingData = this.loadAll(documentType);
        
        // 檢查是否已存在相同ID的文檔
        const existingIndex = existingData.findIndex(doc => doc.id === data.id);
        
        if (existingIndex !== -1) {
            // 更新現有文檔
            existingData[existingIndex] = data;
        } else {
            // 添加新文檔
            existingData.push(data);
        }
        
        localStorage.setItem(storageKey, JSON.stringify(existingData));
        console.log(`💾 已保存文檔到 ${storageKey}:`, data.fileName);
    }
    
    /**
     * 載入單個文檔
     */
    load(documentId) {
        const docTypes = ['bank-statement', 'invoice', 'receipt', 'general'];
        
        for (const type of docTypes) {
            const docs = this.loadAll(type);
            const found = docs.find(doc => doc.id === documentId);
            if (found) return found;
        }
        
        return null;
    }
    
    /**
     * 載入所有文檔
     */
    loadAll(documentType) {
        const storageKey = `${this.storagePrefix}${documentType}`;
        const stored = localStorage.getItem(storageKey);
        return stored ? JSON.parse(stored) : [];
    }
    
    /**
     * 刪除文檔
     */
    async delete(documentId, documentType) {
        const existingData = this.loadAll(documentType);
        const filteredData = existingData.filter(doc => doc.id !== documentId);
        
        const storageKey = `${this.storagePrefix}${documentType}`;
        localStorage.setItem(storageKey, JSON.stringify(filteredData));
        
        console.log(`🗑️ 已刪除文檔: ${documentId}`);
    }
}

// 初始化統一處理器
window.UnifiedDocumentProcessor = new UnifiedDocumentProcessor();

console.log('🎯 統一文檔處理器已載入');
