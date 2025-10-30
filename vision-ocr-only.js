/**
 * Vision API OCR Only Client
 * 
 * 專注於 OCR 文本提取，不進行 AI 分析
 * 適用於香港用戶，無區域限制
 * 
 * 優勢：
 * - Google Vision API 在香港可用
 * - 高準確度 OCR
 * - 無需額外 AI 處理
 * - 成本低（每月 1000 次免費）
 * 
 * @version 1.0.0
 * @updated 2025-10-30
 */

class VisionOCROnlyClient {
    constructor() {
        this.apiKey = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug';  // ✅ VaultCaddy 的 Vision API Key（2025-10-30）
        this.apiUrl = 'https://vision.googleapis.com/v1/images:annotate';
        
        console.log('🔍 Vision OCR Only Client 初始化');
        console.log('   ✅ Google Vision API（香港可用）');
        console.log('   ✅ 專注於 OCR 文本提取');
        console.log('   ✅ 高準確度文本識別');
        console.log('   💰 成本：每月 1000 次免費');
    }
    
    /**
     * 處理文檔（僅 OCR）
     */
    async processDocument(file, documentType = 'invoice') {
        const startTime = Date.now();
        console.log(`\n🔍 Vision OCR 開始處理: ${file.name} (${documentType})`);
        
        try {
            // 1. 將文件轉換為 base64
            const base64Data = await this.fileToBase64(file);
            
            console.log('📸 文件信息:');
            console.log(`   類型: ${file.type}`);
            console.log(`   大小: ${(file.size / 1024).toFixed(2)} KB`);
            
            // 2. 調用 Vision API 進行 OCR
            const response = await fetch(`${this.apiUrl}?key=${this.apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    requests: [{
                        image: {
                            content: base64Data
                        },
                        features: [{
                            type: 'DOCUMENT_TEXT_DETECTION',
                            maxResults: 1
                        }]
                    }]
                })
            });
            
            if (!response.ok) {
                throw new Error(`Vision API 錯誤: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.responses && data.responses[0] && data.responses[0].fullTextAnnotation) {
                const extractedText = data.responses[0].fullTextAnnotation.text;
                console.log('📄 提取的文本長度:', extractedText.length, '字符');
                
                // 3. 解析文本（簡單版本）
                const parsedData = this.parseText(extractedText, documentType);
                
                const processingTime = Date.now() - startTime;
                console.log(`✅ Vision OCR 處理完成，耗時: ${processingTime}ms`);
                
                return {
                    success: true,
                    documentType: documentType,
                    confidence: parsedData.confidence || 70,
                    extractedData: parsedData,
                    rawText: extractedText,
                    processingTime: processingTime,
                    processor: 'vision-ocr'
                };
            } else {
                throw new Error('未能提取文本');
            }
            
        } catch (error) {
            console.error('❌ Vision OCR 處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 解析提取的文本
     */
    parseText(text, documentType) {
        console.log('📊 開始解析文本...');
        
        switch (documentType) {
            case 'invoice':
                return this.parseInvoiceText(text);
            case 'receipt':
                return this.parseReceiptText(text);
            case 'bank-statement':
                return this.parseBankStatementText(text);
            default:
                return {
                    raw_text: text,
                    confidence: 70
                };
        }
    }
    
    /**
     * 解析發票文本
     */
    parseInvoiceText(text) {
        const data = {
            invoice_number: '',
            date: '',
            due_date: '',
            supplier: '',
            customer: '',
            items: [],
            subtotal: 0,
            tax: 0,
            total: 0,
            currency: 'HKD',
            confidence: 70
        };
        
        // 提取發票號碼
        const invoiceNumMatch = text.match(/(?:INVOICE|發票|INV|#)[\s:：#]*(\w+[-\d]+)/i);
        if (invoiceNumMatch) data.invoice_number = invoiceNumMatch[1];
        
        // 提取日期
        const dateMatch = text.match(/(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)/);
        if (dateMatch) data.date = dateMatch[1].replace(/[年月日]/g, '-');
        
        // 提取總金額
        const totalMatch = text.match(/(?:TOTAL|總計|合計|金額)[\s:：]*\$?[\s]*([0-9,]+\.?\d{0,2})/i);
        if (totalMatch) {
            data.total = parseFloat(totalMatch[1].replace(/,/g, ''));
        }
        
        // 提取供應商
        const lines = text.split('\n');
        if (lines.length > 0) {
            data.supplier = lines[0].trim();
        }
        
        console.log('✅ 發票解析完成');
        return data;
    }
    
    /**
     * 解析收據文本
     */
    parseReceiptText(text) {
        const data = {
            receipt_number: '',
            date: '',
            merchant: '',
            items: [],
            total: 0,
            payment_method: 'CASH',
            currency: 'HKD',
            confidence: 70
        };
        
        // 提取日期
        const dateMatch = text.match(/(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)/);
        if (dateMatch) data.date = dateMatch[1].replace(/[年月日]/g, '-');
        
        // 提取總金額
        const totalMatch = text.match(/(?:TOTAL|總計|合計|金額)[\s:：]*\$?[\s]*([0-9,]+\.?\d{0,2})/i);
        if (totalMatch) {
            data.total = parseFloat(totalMatch[1].replace(/,/g, ''));
        }
        
        // 檢測支付方式
        if (text.toUpperCase().includes('CASH')) data.payment_method = 'CASH';
        if (text.toUpperCase().includes('CARD') || text.toUpperCase().includes('VISA') || text.toUpperCase().includes('MASTER')) {
            data.payment_method = 'CARD';
        }
        
        console.log('✅ 收據解析完成');
        return data;
    }
    
    /**
     * 解析銀行對帳單文本
     */
    parseBankStatementText(text) {
        const data = {
            account_holder: '',
            account_number: '',
            statement_period: {
                from: '',
                to: ''
            },
            opening_balance: 0,
            closing_balance: 0,
            transactions: [],
            currency: 'HKD',
            confidence: 70
        };
        
        // 提取日期範圍
        const periodMatch = text.match(/(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)[\s至到\-~]+(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)/);
        if (periodMatch) {
            data.statement_period.from = periodMatch[1].replace(/[年月日]/g, '-');
            data.statement_period.to = periodMatch[2].replace(/[年月日]/g, '-');
        }
        
        // 提取餘額
        const balanceMatch = text.match(/(?:BALANCE|餘額|結餘)[\s:：]*\$?[\s]*([0-9,]+\.?\d{0,2})/i);
        if (balanceMatch) {
            data.closing_balance = parseFloat(balanceMatch[1].replace(/,/g, ''));
        }
        
        console.log('✅ 銀行對帳單解析完成');
        return data;
    }
    
    /**
     * 將文件轉換為 Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.VisionOCROnlyClient = VisionOCROnlyClient;
    window.visionOCRClient = new VisionOCROnlyClient(); // 自動初始化
    console.log('✅ Vision OCR Only Client 模塊已載入');
}

