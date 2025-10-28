/**
 * Google Vision API 處理器（簡化版）
 * 
 * 用途：僅用於 OCR 文本提取，不做任何結構化解析
 * 配合：DeepSeek Reasoner 進行文本分析和結構化
 * 
 * 簡化原因：
 * - 現在使用兩階段處理：Vision API OCR → DeepSeek 分析
 * - Vision API 只負責提取原始文本
 * - DeepSeek 負責理解和結構化數據
 * - 不需要 Vision AI 的複雜解析邏輯
 */

class GoogleVisionAI {
    constructor() {
        this.config = window.VaultCaddyConfig?.apiConfig?.google;
        this.apiKey = this.config?.apiKey;
        this.endpoint = this.config?.endpoints?.vision;
        
        console.log('👁️ Google Vision AI 處理器初始化（簡化版 - 僅 OCR）');
        
        if (!this.apiKey) {
            console.warn('⚠️ Google Vision API 密鑰未設置');
        } else {
            console.log('✅ Google Vision API 密鑰已載入');
            console.log('   功能：僅 OCR 文本提取');
            console.log('   不包含：複雜解析邏輯（已移除）');
        }
    }
    
    /**
     * 處理文檔（簡化版 - 僅返回 OCR 文本）
     */
    async processDocument(file, documentType = 'general') {
        const startTime = Date.now();
        
        try {
            if (!this.apiKey) {
                throw new Error('Google Vision API 密鑰未設置');
            }
            
            console.log(`🚀 Vision API OCR: ${file.name}`);
            
            // 將文件轉換為 base64
            const base64Data = await this.fileToBase64(file);
            
            // 構建請求（只使用 DOCUMENT_TEXT_DETECTION）
            const requestBody = {
                requests: [{
                    image: {
                        content: base64Data
                    },
                    features: [
                        {
                            type: 'DOCUMENT_TEXT_DETECTION', // 文檔文本檢測（最適合文檔）
                            maxResults: 1
                        }
                    ]
                }]
            };
            
            // 調用 Vision API
            const response = await fetch(`${this.endpoint}/images:annotate?key=${this.apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Vision API 錯誤: ${response.status} - ${errorText}`);
            }
            
            const result = await response.json();
            const annotations = result.responses[0];
            
            if (!annotations) {
                throw new Error('Vision API 返回空響應');
            }
            
            // 提取文本（優先順序：fullTextAnnotation > textAnnotations）
            let extractedText = '';
            
            if (annotations.fullTextAnnotation && annotations.fullTextAnnotation.text) {
                extractedText = annotations.fullTextAnnotation.text;
            } else if (annotations.textAnnotations && annotations.textAnnotations.length > 0) {
                extractedText = annotations.textAnnotations[0].description;
            }
            
            if (!extractedText) {
                throw new Error('Vision API 未能提取任何文本');
            }
            
            const processingTime = Date.now() - startTime;
            console.log(`✅ Vision API OCR 完成`);
            console.log(`   文本長度: ${extractedText.length} 字符`);
            console.log(`   處理時間: ${processingTime}ms`);
            
            // 返回簡化的結果（只包含文本和基本信息）
            return {
                success: true,
                processor: 'google-vision-ai',
                documentType: documentType,
                data: {
                    text: extractedText,
                    fullTextAnnotation: annotations.fullTextAnnotation,
                    textAnnotations: annotations.textAnnotations
                },
                processingTime: processingTime,
                confidence: 85 // 固定信心度（因為不做解析）
            };
            
        } catch (error) {
            console.error('❌ Vision API OCR 失敗:', error);
            throw error;
        }
    }
    
    /**
     * 將文件轉換為 Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // 移除 data:image/...;base64, 前綴
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
}

// 全局暴露
window.GoogleVisionAI = GoogleVisionAI;
window.googleVisionAI = new GoogleVisionAI();

console.log('✅ Google Vision AI 模塊已載入（簡化版 - 僅 OCR）');
console.log('   已移除：');
console.log('   - 複雜的字段提取邏輯');
console.log('   - 正則表達式解析');
console.log('   - 手動數據結構化');
console.log('   保留：');
console.log('   - 基本 OCR 文本提取');
console.log('   - Base64 轉換');

