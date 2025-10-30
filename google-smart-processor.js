/**
 * Google 智能處理器選擇器 - 版本 2025-10-30 HYBRID
 * ✅ 使用混合處理器：Vision API OCR + DeepSeek Chat
 * ✅ 兩步處理：先 OCR 提取文本，再 AI 分析
 * ✅ 香港可用，高準確度（85%）
 */

class GoogleSmartProcessor {
    constructor() {
        // 版本標記（用於確認是否加載最新版本）
        this.version = '2025-10-30-HYBRID';
        
        console.log('🔄 加載 GoogleSmartProcessor 版本:', this.version);
        
        // ⚠️ 不在構造函數中直接引用 window 對象，而是動態獲取
        this.processors = {
            get hybrid() { return window.hybridProcessor; }  // ✅ 混合處理器（Vision OCR + DeepSeek Chat）
        };
        
        this.processingOrder = [
            'hybrid'          // ✅ 混合處理器 (85% 準確度，香港可用)
        ];
        
        console.log('🧠 智能處理器初始化');
        console.log('   ✅ 版本:', this.version);
        console.log('   🔄 處理器: 混合處理器 (Vision OCR + DeepSeek Chat)');
        console.log('   📊 預期準確度: 85%');
        console.log('   🌏 香港可用: ✅');
        console.log('   💰 成本: ~$0.001/張');
        console.log('   📋 處理順序:', this.processingOrder);
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
        console.log('   - hybrid:', typeof window.hybridProcessor);
        
        if (typeof window.hybridProcessor === 'undefined') {
            console.error('❌ 混合處理器未初始化！');
            console.error('   請檢查 hybrid-vision-deepseek.js 是否正確加載');
        } else {
            console.log('✅ 混合處理器已就緒');
        }
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
        // ✅ 所有文檔類型統一使用混合處理器：Vision API OCR + DeepSeek Chat
        // 不再使用舊的處理器（deepseekVision, openaiVision, geminiAI, visionAI）
        
        // 所有文檔類型都使用相同的處理順序
        return ['hybrid']; // Vision API OCR + DeepSeek Chat
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
