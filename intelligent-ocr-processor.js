/**
 * 智能OCR處理器
 * 根據不同場景自動選擇最適合的OCR引擎
 */

class IntelligentOCRProcessor {
    constructor() {
        this.googleAI = null;
        this.tesseractJS = null;
        this.isInitialized = false;
        
        this.processingStats = {
            googleAI: { success: 0, failure: 0, totalTime: 0 },
            tesseractJS: { success: 0, failure: 0, totalTime: 0 }
        };
        
        console.log('🧠 智能OCR處理器已初始化');
    }
    
    /**
     * 初始化所有OCR引擎
     */
    async initialize() {
        if (this.isInitialized) return;
        
        console.log('🔄 初始化智能OCR處理器...');
        
        try {
            // 初始化Google AI處理器
            if (window.GoogleAIProcessor) {
                this.googleAI = new window.GoogleAIProcessor();
                console.log('✅ Google AI處理器已載入');
            } else {
                console.warn('⚠️ Google AI處理器未找到');
            }
            
            // 初始化Tesseract.js處理器
            if (window.TesseractOCRProcessor) {
                this.tesseractJS = new window.TesseractOCRProcessor();
                console.log('✅ Tesseract.js處理器已載入');
            } else {
                console.warn('⚠️ Tesseract.js處理器未找到');
            }
            
            this.isInitialized = true;
            console.log('✅ 智能OCR處理器初始化完成');
            
        } catch (error) {
            console.error('❌ 智能OCR處理器初始化失敗:', error);
            throw error;
        }
    }
    
    /**
     * 智能處理文檔
     */
    async processDocument(file, options = {}) {
        await this.initialize();
        
        const {
            documentType = 'general',
            forceOffline = false,
            privacyMode = false,
            budgetMode = false,
            qualityPriority = 'balanced', // 'speed', 'accuracy', 'balanced'
            fallbackEnabled = true
        } = options;
        
        console.log(`🧠 智能OCR處理: ${file.name} (${documentType})`);
        console.log('📋 處理選項:', { forceOffline, privacyMode, budgetMode, qualityPriority });
        
        // 選擇最佳OCR引擎
        const selectedEngine = this.selectOptimalEngine(file, options);
        console.log(`🎯 選擇OCR引擎: ${selectedEngine}`);
        
        try {
            // 嘗試使用選定的引擎
            const result = await this.processWithEngine(selectedEngine, file, documentType);
            
            // 驗證結果質量
            const qualityScore = this.evaluateResultQuality(result);
            console.log(`📊 結果質量評分: ${qualityScore}/100`);
            
            // 如果質量不佳且啟用了回退機制
            if (qualityScore < 60 && fallbackEnabled && this.hasFallbackEngine(selectedEngine)) {
                console.log('⚠️ 結果質量不佳，嘗試備用引擎...');
                const fallbackEngine = this.getFallbackEngine(selectedEngine);
                const fallbackResult = await this.processWithEngine(fallbackEngine, file, documentType);
                
                const fallbackQuality = this.evaluateResultQuality(fallbackResult);
                console.log(`📊 備用引擎質量評分: ${fallbackQuality}/100`);
                
                // 選擇質量更好的結果
                if (fallbackQuality > qualityScore) {
                    console.log('✅ 使用備用引擎結果');
                    return this.enhanceResult(fallbackResult, { usedFallback: true, originalEngine: selectedEngine });
                }
            }
            
            return this.enhanceResult(result, { usedFallback: false });
            
        } catch (error) {
            console.error(`❌ ${selectedEngine} 處理失敗:`, error);
            
            // 嘗試備用引擎
            if (fallbackEnabled && this.hasFallbackEngine(selectedEngine)) {
                console.log('🔄 嘗試備用引擎...');
                try {
                    const fallbackEngine = this.getFallbackEngine(selectedEngine);
                    const fallbackResult = await this.processWithEngine(fallbackEngine, file, documentType);
                    return this.enhanceResult(fallbackResult, { 
                        usedFallback: true, 
                        originalEngine: selectedEngine,
                        originalError: error.message 
                    });
                } catch (fallbackError) {
                    console.error('❌ 備用引擎也失敗了:', fallbackError);
                    throw new Error(`所有OCR引擎都失敗了: ${error.message}, ${fallbackError.message}`);
                }
            }
            
            throw error;
        }
    }
    
    /**
     * 選擇最佳OCR引擎
     */
    selectOptimalEngine(file, options) {
        const {
            forceOffline,
            privacyMode,
            budgetMode,
            qualityPriority,
            documentType
        } = options;
        
        // 強制離線或隱私模式：只能使用Tesseract.js
        if (forceOffline || privacyMode) {
            if (!this.tesseractJS) {
                throw new Error('離線模式需要Tesseract.js，但未載入');
            }
            return 'tesseract';
        }
        
        // 預算模式：優先使用免費的Tesseract.js
        if (budgetMode) {
            return this.tesseractJS ? 'tesseract' : 'google';
        }
        
        // 根據質量優先級選擇
        switch (qualityPriority) {
            case 'speed':
                // 速度優先：選擇更快的引擎
                return this.getFasterEngine();
                
            case 'accuracy':
                // 準確度優先：選擇更準確的引擎
                return this.getMoreAccurateEngine(documentType);
                
            case 'balanced':
            default:
                // 平衡模式：根據文檔類型和歷史表現選擇
                return this.getBalancedEngine(file, documentType);
        }
    }
    
    /**
     * 使用指定引擎處理文檔
     */
    async processWithEngine(engine, file, documentType) {
        const startTime = Date.now();
        
        try {
            let result;
            
            switch (engine) {
                case 'google':
                    if (!this.googleAI) {
                        throw new Error('Google AI處理器未載入');
                    }
                    result = await this.googleAI.processDocument(file, documentType);
                    break;
                    
                case 'tesseract':
                    if (!this.tesseractJS) {
                        throw new Error('Tesseract.js處理器未載入');
                    }
                    result = await this.tesseractJS.processDocument(file, documentType);
                    break;
                    
                default:
                    throw new Error(`不支援的OCR引擎: ${engine}`);
            }
            
            // 記錄成功統計
            const processingTime = Date.now() - startTime;
            this.processingStats[engine === 'google' ? 'googleAI' : 'tesseractJS'].success++;
            this.processingStats[engine === 'google' ? 'googleAI' : 'tesseractJS'].totalTime += processingTime;
            
            return {
                ...result,
                engine: engine,
                processingTime: processingTime
            };
            
        } catch (error) {
            // 記錄失敗統計
            this.processingStats[engine === 'google' ? 'googleAI' : 'tesseractJS'].failure++;
            throw error;
        }
    }
    
    /**
     * 評估結果質量
     */
    evaluateResultQuality(result) {
        let score = 0;
        
        // 基礎分數：有文本就給30分
        if (result.text && result.text.trim().length > 0) {
            score += 30;
        }
        
        // 置信度分數：最多40分
        if (result.confidence !== undefined) {
            score += Math.min(40, result.confidence * 0.4);
        }
        
        // 結構化數據分數：最多30分
        if (result.extractedData) {
            const dataKeys = Object.keys(result.extractedData);
            const nonEmptyKeys = dataKeys.filter(key => {
                const value = result.extractedData[key];
                return value !== null && value !== undefined && value !== '';
            });
            
            score += Math.min(30, (nonEmptyKeys.length / dataKeys.length) * 30);
        }
        
        return Math.round(score);
    }
    
    /**
     * 增強處理結果
     */
    enhanceResult(result, metadata = {}) {
        return {
            ...result,
            metadata: {
                ...result.metadata,
                intelligentOCR: {
                    version: '1.0.0',
                    processedAt: new Date().toISOString(),
                    ...metadata
                }
            },
            qualityScore: this.evaluateResultQuality(result)
        };
    }
    
    /**
     * 獲取更快的引擎
     */
    getFasterEngine() {
        // 根據歷史統計選擇更快的引擎
        const googleAvgTime = this.getAverageProcessingTime('googleAI');
        const tesseractAvgTime = this.getAverageProcessingTime('tesseractJS');
        
        if (googleAvgTime > 0 && tesseractAvgTime > 0) {
            return googleAvgTime < tesseractAvgTime ? 'google' : 'tesseract';
        }
        
        // 默認Google AI通常更快
        return this.googleAI ? 'google' : 'tesseract';
    }
    
    /**
     * 獲取更準確的引擎
     */
    getMoreAccurateEngine(documentType) {
        // 根據文檔類型選擇更準確的引擎
        switch (documentType) {
            case 'bank-statement':
            case 'invoice':
                // 表格數據：Google AI更準確
                return this.googleAI ? 'google' : 'tesseract';
                
            case 'receipt':
                // 收據：兩者差不多，優先Google AI
                return this.googleAI ? 'google' : 'tesseract';
                
            case 'general':
            default:
                // 一般文檔：根據歷史成功率選擇
                const googleSuccessRate = this.getSuccessRate('googleAI');
                const tesseractSuccessRate = this.getSuccessRate('tesseractJS');
                
                if (googleSuccessRate > tesseractSuccessRate) {
                    return this.googleAI ? 'google' : 'tesseract';
                } else {
                    return this.tesseractJS ? 'tesseract' : 'google';
                }
        }
    }
    
    /**
     * 獲取平衡引擎
     */
    getBalancedEngine(file, documentType) {
        // 文件大小考量
        const fileSizeMB = file.size / (1024 * 1024);
        
        // 大文件優先使用Google AI（處理能力更強）
        if (fileSizeMB > 5) {
            return this.googleAI ? 'google' : 'tesseract';
        }
        
        // 小文件可以使用Tesseract.js（節省API費用）
        if (fileSizeMB < 1) {
            return this.tesseractJS ? 'tesseract' : 'google';
        }
        
        // 中等大小文件：根據文檔類型選擇
        return this.getMoreAccurateEngine(documentType);
    }
    
    /**
     * 檢查是否有備用引擎
     */
    hasFallbackEngine(primaryEngine) {
        switch (primaryEngine) {
            case 'google':
                return !!this.tesseractJS;
            case 'tesseract':
                return !!this.googleAI;
            default:
                return false;
        }
    }
    
    /**
     * 獲取備用引擎
     */
    getFallbackEngine(primaryEngine) {
        switch (primaryEngine) {
            case 'google':
                return 'tesseract';
            case 'tesseract':
                return 'google';
            default:
                throw new Error(`沒有 ${primaryEngine} 的備用引擎`);
        }
    }
    
    /**
     * 獲取平均處理時間
     */
    getAverageProcessingTime(engine) {
        const stats = this.processingStats[engine];
        const totalProcesses = stats.success + stats.failure;
        
        return totalProcesses > 0 ? stats.totalTime / totalProcesses : 0;
    }
    
    /**
     * 獲取成功率
     */
    getSuccessRate(engine) {
        const stats = this.processingStats[engine];
        const totalProcesses = stats.success + stats.failure;
        
        return totalProcesses > 0 ? stats.success / totalProcesses : 0;
    }
    
    /**
     * 獲取處理統計
     */
    getProcessingStats() {
        return {
            ...this.processingStats,
            summary: {
                googleAI: {
                    successRate: this.getSuccessRate('googleAI'),
                    averageTime: this.getAverageProcessingTime('googleAI')
                },
                tesseractJS: {
                    successRate: this.getSuccessRate('tesseractJS'),
                    averageTime: this.getAverageProcessingTime('tesseractJS')
                }
            }
        };
    }
    
    /**
     * 重置統計數據
     */
    resetStats() {
        this.processingStats = {
            googleAI: { success: 0, failure: 0, totalTime: 0 },
            tesseractJS: { success: 0, failure: 0, totalTime: 0 }
        };
        console.log('📊 處理統計已重置');
    }
    
    /**
     * 獲取可用引擎列表
     */
    getAvailableEngines() {
        const engines = [];
        
        if (this.googleAI) {
            engines.push({
                name: 'google',
                displayName: 'Google AI',
                features: ['高準確度', '快速處理', '表格識別', '多語言'],
                limitations: ['需要網絡', 'API費用']
            });
        }
        
        if (this.tesseractJS) {
            engines.push({
                name: 'tesseract',
                displayName: 'Tesseract.js',
                features: ['離線處理', '免費使用', '100+語言', '隱私保護'],
                limitations: ['準確度較低', '處理較慢']
            });
        }
        
        return engines;
    }
    
    /**
     * 檢查引擎可用性
     */
    async checkEngineHealth() {
        const health = {
            googleAI: false,
            tesseractJS: false,
            overall: false
        };
        
        // 檢查Google AI
        if (this.googleAI) {
            try {
                // 這裡可以添加健康檢查邏輯
                health.googleAI = true;
            } catch (error) {
                console.warn('Google AI健康檢查失敗:', error);
            }
        }
        
        // 檢查Tesseract.js
        if (this.tesseractJS) {
            try {
                health.tesseractJS = this.tesseractJS.isReady();
            } catch (error) {
                console.warn('Tesseract.js健康檢查失敗:', error);
            }
        }
        
        health.overall = health.googleAI || health.tesseractJS;
        
        return health;
    }
}

// 全局實例
window.IntelligentOCRProcessor = IntelligentOCRProcessor;

console.log('✅ 智能OCR處理器已載入');
