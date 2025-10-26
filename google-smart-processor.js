/**
 * Google 智能處理器選擇器
 * 自動選擇最適合的Google AI服務
 */

class GoogleSmartProcessor {
    constructor() {
        // ⚠️ 不在構造函數中直接引用 window 對象，而是動態獲取
        this.processors = {
            get deepseekVision() { return window.deepseekVisionClient; },  // ✅ DeepSeek Vision（最優先）
            get openaiVision() { return window.openaiVisionClient; },      // ✅ OpenAI GPT-4 Vision（備用1）
            get geminiAI() { return window.geminiWorkerClient; },          // ✅ Gemini（備用2）
            get visionAI() { return window.googleVisionAI; },              // ⚠️ Vision API（備用3）
            get documentAI() { return window.googleDocumentAI; }           // ❌ Document AI（已停用）
        };
        
        this.processingOrder = [
            'deepseekVision', // ✅ 最優先：DeepSeek Vision（準確度最高，成本最低）
            'openaiVision',   // ✅ 備用1：OpenAI GPT-4 Vision（準確度高）
            'geminiAI',       // ✅ 備用2：Gemini（通過 Cloudflare Worker）
            'visionAI'        // ⚠️ 備用3：Vision API（文本解析能力較弱）
        ];
        
        console.log('🧠 Google 智能處理器初始化');
        this.logAvailableProcessors();
    }
    
    /**
     * 記錄可用處理器（動態檢查）
     */
    logAvailableProcessors() {
        const available = Object.keys(this.processors).filter(key => {
            const processor = this.processors[key];
            return processor !== null && processor !== undefined;
        });
        console.log('可用處理器:', available);
        console.log('   - deepseekVision:', typeof window.deepseekVisionClient);
        console.log('   - openaiVision:', typeof window.openaiVisionClient);
        console.log('   - geminiAI (geminiWorkerClient):', typeof window.geminiWorkerClient);
        console.log('   - visionAI:', typeof window.googleVisionAI);
        console.log('   - documentAI:', typeof window.googleDocumentAI);
    }
    
    /**
     * 智能處理文檔
     */
    async processDocument(file, documentType = 'general') {
        const startTime = Date.now();
        let lastError = null;
        
        console.log(`🚀 開始智能處理: ${file.name} (${documentType})`);
        console.log(`📋 處理順序: ${this.processingOrder.join(' → ')}`);
        
        // 按順序嘗試每個處理器
        for (let i = 0; i < this.processingOrder.length; i++) {
            const processorName = this.processingOrder[i];
            const processor = this.processors[processorName];
            
            if (!processor) {
                console.warn(`⚠️ 處理器 ${processorName} 不可用，跳過`);
                continue;
            }
            
            try {
                console.log(`🔄 嘗試處理器 ${i + 1}/${this.processingOrder.length}: ${processorName}`);
                
                const result = await processor.processDocument(file, documentType);
                
                if (result && result.success) {
                    console.log(`✅ 處理器 ${processorName} 成功處理文檔`);
                    console.log(`⏱️ 總處理時間: ${Date.now() - startTime}ms`);
                    
                    return {
                        ...result,
                        processor: processorName,
                        totalTime: Date.now() - startTime
                    };
                }
                
            } catch (error) {
                console.warn(`⚠️ 處理器 ${processorName} 失敗:`, error.message);
                lastError = error;
                
                // 如果是認證錯誤（401, Unauthorized），跳過
                if (error.message.includes('401') || 
                    error.message.includes('Unauthorized') ||
                    error.message.includes('authentication credentials')) {
                    console.log(`🔐 檢測到認證錯誤（${processorName} 需要 OAuth 2.0），嘗試下一個處理器...`);
                    continue;
                }
                
                // 如果是地理限制錯誤，繼續嘗試下一個
                if (error.message.includes('location is not supported') || 
                    error.message.includes('地理位置') ||
                    error.message.includes('FAILED_PRECONDITION')) {
                    console.log(`🌍 檢測到地理限制，嘗試下一個處理器...`);
                    continue;
                }
                
                // 如果是API配額錯誤，也繼續嘗試
                if (error.message.includes('quota') || 
                    error.message.includes('rate limit') ||
                    error.message.includes('RESOURCE_EXHAUSTED')) {
                    console.log(`📊 檢測到配額限制，嘗試下一個處理器...`);
                    continue;
                }
                
                // 其他錯誤也繼續嘗試
                console.log(`🔄 嘗試下一個處理器...`);
            }
        }
        
        // 所有處理器都失敗
        console.error('❌ 所有Google處理器都失敗了');
        throw lastError || new Error('所有處理器都無法處理此文檔');
    }
    
    /**
     * 獲取處理器狀態
     */
    getProcessorStatus() {
        const status = {};
        
        for (const [name, processor] of Object.entries(this.processors)) {
            if (!processor) {
                status[name] = { available: false, reason: '處理器未載入' };
                continue;
            }
            
            // 檢查API密鑰
            const hasApiKey = processor.apiKey || processor.config?.apiKey;
            
            status[name] = {
                available: !!hasApiKey,
                reason: hasApiKey ? '可用' : 'API密鑰未設置'
            };
        }
        
        return status;
    }
    
    /**
     * 測試所有處理器
     */
    async testAllProcessors() {
        console.log('🧪 測試所有Google處理器...');
        
        const results = {};
        
        for (const [name, processor] of Object.entries(this.processors)) {
            if (!processor) {
                results[name] = { success: false, error: '處理器未載入' };
                continue;
            }
            
            try {
                // 創建測試文件
                const testBlob = new Blob(['測試文檔內容'], { type: 'text/plain' });
                const testFile = new File([testBlob], 'test.txt', { type: 'text/plain' });
                
                const result = await processor.processDocument(testFile, 'general');
                results[name] = { success: true, result: result };
                
            } catch (error) {
                results[name] = { success: false, error: error.message };
            }
        }
        
        console.log('🧪 測試結果:', results);
        return results;
    }
    
    /**
     * 根據文檔類型優化處理順序
     */
    optimizeProcessingOrder(documentType) {
        // ✅ 所有文檔類型統一使用: deepseekVision → openaiVision → geminiAI → visionAI
        
        switch (documentType) {
            case 'invoice':
            case 'receipt':
                // 對於發票和收據，DeepSeek Vision 準確度最高且成本最低
                return ['deepseekVision', 'openaiVision', 'geminiAI', 'visionAI'];
                
            case 'bank_statement':
                // 對於銀行對帳單，DeepSeek Vision 可以更好地理解表格結構
                return ['deepseekVision', 'openaiVision', 'geminiAI', 'visionAI'];
                
            default:
                // 通用文檔，保持默認順序
                return this.processingOrder;
        }
    }
    
    /**
     * 處理文檔（帶優化）
     */
    async processDocumentOptimized(file, documentType = 'general') {
        // 根據文檔類型優化處理順序
        const originalOrder = this.processingOrder;
        this.processingOrder = this.optimizeProcessingOrder(documentType);
        
        try {
            const result = await this.processDocument(file, documentType);
            return result;
        } finally {
            // 恢復原始順序
            this.processingOrder = originalOrder;
        }
    }
}

// 全局暴露
window.GoogleSmartProcessor = GoogleSmartProcessor;
window.googleSmartProcessor = new GoogleSmartProcessor();

console.log('🧠 Google 智能處理器模塊已載入');
