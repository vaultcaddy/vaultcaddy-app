/**
 * Tesseract.js OCR處理器
 * 提供離線OCR功能，支援100+語言
 */

class TesseractOCRProcessor {
    constructor() {
        this.worker = null;
        this.isInitialized = false;
        this.supportedLanguages = ['eng', 'chi_tra', 'chi_sim', 'jpn'];
        this.defaultLanguage = 'eng+chi_tra'; // 支援英文和繁體中文
    }
    
    /**
     * 初始化Tesseract.js OCR引擎
     */
    async initialize(language = this.defaultLanguage) {
        if (this.isInitialized) return;
        
        console.log('🔄 初始化Tesseract.js OCR引擎...');
        
        try {
            // 檢查Tesseract.js是否已載入
            if (typeof Tesseract === 'undefined') {
                throw new Error('Tesseract.js 未載入，請確保已包含CDN腳本');
            }
            
            this.worker = await Tesseract.createWorker(language, 1, {
                logger: m => {
                    if (m.status === 'recognizing text') {
                        console.log(`OCR進度: ${Math.round(m.progress * 100)}%`);
                    }
                }
            });
            
            // 優化OCR參數 - 使用更安全的設置
            try {
                await this.worker.setParameters({
                    'tessedit_pageseg_mode': '6', // 使用數字而不是常量
                    'tessedit_ocr_engine_mode': '1', // LSTM_ONLY
                    'preserve_interword_spaces': '1'
                    // 移除字符白名單以避免兼容性問題
                });
                console.log('✅ Tesseract.js 參數設置完成');
            } catch (paramError) {
                console.warn('⚠️ Tesseract.js 參數設置失敗，使用默認設置:', paramError);
                // 繼續執行，使用默認參數
            }
            
            this.isInitialized = true;
            console.log('✅ Tesseract.js 初始化完成');
        } catch (error) {
            console.error('❌ Tesseract.js 初始化失敗:', error);
            throw error;
        }
    }
    
    /**
     * 處理文檔OCR
     */
    async processDocument(file, documentType) {
        const startTime = Date.now();
        
        try {
            await this.initialize();
            
            console.log(`📄 Tesseract.js 處理文檔: ${file.name} (${documentType})`);
            console.log(`📊 文件信息: 大小=${(file.size/1024/1024).toFixed(2)}MB, 類型=${file.type}`);
            
            // 驗證文件
            if (!file || file.size === 0) {
                throw new Error('文件無效或為空');
            }
            
            if (!file.type.startsWith('image/')) {
                throw new Error(`不支援的文件類型: ${file.type}`);
            }
            
            // 預處理圖像以提高OCR準確度
            console.log('🔄 開始圖像預處理...');
            let processedImage;
            try {
                // 暫時跳過預處理，直接使用原文件以避免Canvas錯誤
                console.log('🔄 使用原始文件（跳過預處理以避免兼容性問題）');
                processedImage = file;
            } catch (preprocessError) {
                console.error('❌ 圖像預處理失敗:', preprocessError);
                processedImage = file;
            }
            
            // 執行OCR識別
            console.log('🔄 開始OCR識別...');
            const { data } = await this.worker.recognize(processedImage, {
                rectangle: null, // 處理整個圖像
            });
            
            console.log(`✅ OCR識別完成，置信度: ${data.confidence}%`);
            
            if (!data.text || data.text.trim().length === 0) {
                throw new Error('OCR未識別到任何文字內容');
            }
            
            // 後處理和數據提取
            console.log('🔄 開始數據提取...');
            const extractedData = await this.extractStructuredData(data, documentType);
            console.log('✅ 數據提取完成');
            
            return {
                success: true,
                confidence: data.confidence,
                text: data.text,
                words: data.words,
                lines: data.lines,
                paragraphs: data.paragraphs,
                blocks: data.blocks,
                extractedData: extractedData,
                processingTime: Date.now() - startTime,
                engine: 'tesseract.js',
                language: this.defaultLanguage
            };
            
        } catch (error) {
            console.error('❌ Tesseract.js 處理失敗:', error);
            throw new Error(`Tesseract.js處理失敗: ${error.message}`);
        }
    }
    
    /**
     * 圖像預處理以提高OCR準確度
     */
    async preprocessImage(file) {
        return new Promise((resolve, reject) => {
            // 驗證文件類型
            if (!file || !file.type || !file.type.startsWith('image/')) {
                reject(new Error('無效的圖像文件'));
                return;
            }
            
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            // 設置超時
            const timeout = setTimeout(() => {
                reject(new Error('圖像載入超時'));
            }, 10000);
            
            img.onload = () => {
                clearTimeout(timeout);
                try {
                    // 設置畫布尺寸
                    canvas.width = img.width;
                    canvas.height = img.height;
                    
                    // 清除濾鏡，先繪製原始圖像
                    ctx.filter = 'none';
                    ctx.drawImage(img, 0, 0);
                    
                    // 應用圖像增強 - 暫時禁用以避免兼容性問題
                    try {
                        // 簡單的對比度增強
                        ctx.filter = 'contrast(120%) brightness(110%)';
                        ctx.globalCompositeOperation = 'source-over';
                        
                        // 不進行複雜的像素級處理，避免Canvas相關錯誤
                        console.log('✅ 應用基本圖像增強');
                    } catch (enhanceError) {
                        console.warn('圖像增強失敗，使用原始圖像:', enhanceError);
                        // 重置濾鏡
                        ctx.filter = 'none';
                    }
                    
                    // 清理URL對象
                    URL.revokeObjectURL(img.src);
                    resolve(canvas);
                } catch (error) {
                    clearTimeout(timeout);
                    URL.revokeObjectURL(img.src);
                    reject(new Error(`圖像處理失敗: ${error.message}`));
                }
            };
            
            img.onerror = (error) => {
                clearTimeout(timeout);
                URL.revokeObjectURL(img.src);
                reject(new Error(`圖像載入失敗: ${error.message || '未知錯誤'}`));
            };
            
            try {
                img.src = URL.createObjectURL(file);
            } catch (error) {
                clearTimeout(timeout);
                reject(new Error(`創建圖像URL失敗: ${error.message}`));
            }
        });
    }
    
    /**
     * 增強圖像數據
     */
    enhanceImageData(imageData) {
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            // 轉換為灰度
            const gray = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
            
            // 二值化處理
            const threshold = 128;
            const binary = gray > threshold ? 255 : 0;
            
            data[i] = binary;     // Red
            data[i + 1] = binary; // Green
            data[i + 2] = binary; // Blue
            // Alpha保持不變
        }
        
        return imageData;
    }
    
    /**
     * 從OCR結果提取結構化數據
     */
    async extractStructuredData(ocrData, documentType) {
        const text = ocrData.text;
        const words = ocrData.words;
        const lines = ocrData.lines;
        
        console.log(`📊 提取 ${documentType} 結構化數據`);
        
        switch (documentType) {
            case 'bank-statement':
                return this.extractBankStatementData(text, words, lines);
            case 'receipt':
                return this.extractReceiptData(text, words, lines);
            case 'invoice':
                return this.extractInvoiceData(text, words, lines);
            case 'general':
                return this.extractGeneralData(text, words, lines);
            default:
                return this.extractGeneralData(text, words, lines);
        }
    }
    
    /**
     * 提取銀行對帳單數據
     */
    extractBankStatementData(text, words, lines) {
        const patterns = {
            accountNumber: /(?:account|帳戶|戶口)[:\s#]*([0-9\-]+)/i,
            statementPeriod: /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\s*(?:to|至|到)\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i,
            openingBalance: /(?:opening|期初|上期).*?balance[:\s]*([0-9,]+\.?[0-9]*)/i,
            closingBalance: /(?:closing|期末|本期).*?balance[:\s]*([0-9,]+\.?[0-9]*)/i,
            transactions: /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\s+(.+?)\s+([\-\+]?[0-9,]+\.?[0-9]*)\s+([0-9,]+\.?[0-9]*)/g
        };
        
        // 提取基本信息
        const accountNumber = text.match(patterns.accountNumber)?.[1];
        const periodMatch = text.match(patterns.statementPeriod);
        const openingBalance = text.match(patterns.openingBalance)?.[1];
        const closingBalance = text.match(patterns.closingBalance)?.[1];
        
        // 提取交易記錄
        const transactions = [];
        let match;
        while ((match = patterns.transactions.exec(text)) !== null) {
            transactions.push({
                date: match[1],
                description: match[2].trim(),
                amount: parseFloat(match[3].replace(/[,\s]/g, '')),
                balance: parseFloat(match[4].replace(/[,\s]/g, ''))
            });
        }
        
        return {
            accountInfo: {
                accountNumber: accountNumber,
                bankName: this.extractBankName(text)
            },
            statementPeriod: {
                startDate: periodMatch?.[1],
                endDate: periodMatch?.[2]
            },
            financialPosition: {
                openingBalance: openingBalance ? parseFloat(openingBalance.replace(/[,\s]/g, '')) : null,
                closingBalance: closingBalance ? parseFloat(closingBalance.replace(/[,\s]/g, '')) : null
            },
            transactions: transactions,
            summary: {
                totalTransactions: transactions.length,
                totalCredits: transactions.filter(t => t.amount > 0).reduce((sum, t) => sum + t.amount, 0),
                totalDebits: transactions.filter(t => t.amount < 0).reduce((sum, t) => sum + t.amount, 0)
            },
            rawText: text
        };
    }
    
    /**
     * 提取收據數據
     */
    extractReceiptData(text, words, lines) {
        const patterns = {
            total: /(?:total|總計|合計|小計)[:\s]*([0-9,]+\.?[0-9]*)/i,
            subtotal: /(?:subtotal|小計)[:\s]*([0-9,]+\.?[0-9]*)/i,
            tax: /(?:tax|稅|gst|vat)[:\s]*([0-9,]+\.?[0-9]*)/i,
            date: /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/,
            time: /(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)/i,
            receiptNumber: /(?:receipt|收據|單號)[:\s#]*([A-Z0-9\-]+)/i,
            items: /(.+?)\s+([0-9,]+\.?[0-9]*)/g
        };
        
        // 提取基本信息
        const total = text.match(patterns.total)?.[1];
        const subtotal = text.match(patterns.subtotal)?.[1];
        const tax = text.match(patterns.tax)?.[1];
        const date = text.match(patterns.date)?.[1];
        const time = text.match(patterns.time)?.[1];
        const receiptNumber = text.match(patterns.receiptNumber)?.[1];
        
        // 提取商家名稱（通常在第一行）
        const firstLine = lines[0]?.text || text.split('\n')[0];
        const merchant = firstLine.replace(/[^A-Za-z\u4e00-\u9fff\s]/g, '').trim();
        
        // 提取商品項目
        const items = [];
        let match;
        const itemPattern = /(.+?)\s+([0-9,]+\.?[0-9]*)/g;
        while ((match = itemPattern.exec(text)) !== null) {
            const itemName = match[1].trim();
            const amount = parseFloat(match[2].replace(',', ''));
            
            // 過濾掉總計、小計等非商品項目
            if (!itemName.match(/(?:total|subtotal|tax|總計|小計|稅)/i) && amount > 0) {
                items.push({
                    name: itemName,
                    amount: amount,
                    quantity: 1 // 默認數量，可以進一步解析
                });
            }
        }
        
        return {
            receiptNumber: receiptNumber,
            date: date,
            time: time,
            merchant: merchant,
            totalAmount: total ? parseFloat(total.replace(',', '')) : null,
            subtotalAmount: subtotal ? parseFloat(subtotal.replace(',', '')) : null,
            taxAmount: tax ? parseFloat(tax.replace(',', '')) : null,
            items: items,
            paymentMethod: this.extractPaymentMethod(text),
            rawText: text
        };
    }
    
    /**
     * 提取發票數據
     */
    extractInvoiceData(text, words, lines) {
        const patterns = {
            invoiceNumber: /(?:invoice|發票)[:\s#]*([A-Z0-9\-]+)/i,
            issueDate: /(?:date|日期|開立日期)[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i,
            dueDate: /(?:due|到期)[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i,
            total: /(?:total|總計|合計)[:\s]*([0-9,]+\.?[0-9]*)/i,
            tax: /(?:tax|稅)[:\s]*([0-9,]+\.?[0-9]*)/i
        };
        
        return {
            invoiceNumber: text.match(patterns.invoiceNumber)?.[1],
            issueDate: text.match(patterns.issueDate)?.[1],
            dueDate: text.match(patterns.dueDate)?.[1],
            vendor: this.extractVendorInfo(text),
            customer: this.extractCustomerInfo(text),
            totalAmount: text.match(patterns.total)?.[1],
            taxAmount: text.match(patterns.tax)?.[1],
            lineItems: this.extractLineItems(text),
            rawText: text
        };
    }
    
    /**
     * 提取一般文檔數據
     */
    extractGeneralData(text, words, lines) {
        return {
            title: lines[0]?.text || '未知文檔',
            content: text,
            wordCount: words.length,
            lineCount: lines.length,
            keyInformation: this.extractKeyInformation(text),
            entities: this.extractEntities(text),
            rawText: text
        };
    }
    
    /**
     * 輔助方法：提取銀行名稱
     */
    extractBankName(text) {
        const bankPatterns = [
            /(?:bank|銀行)\s*(?:of|的)?\s*([A-Za-z\u4e00-\u9fff\s]+)/i,
            /(匯豐|中銀|渣打|恆生|東亞|建行|工銀|招商|民生|浦發)/
        ];
        
        for (const pattern of bankPatterns) {
            const match = text.match(pattern);
            if (match) {
                return match[1] || match[0];
            }
        }
        
        return null;
    }
    
    /**
     * 輔助方法：提取付款方式
     */
    extractPaymentMethod(text) {
        const methods = ['cash', 'card', 'credit', 'debit', '現金', '信用卡', '借記卡', '八達通'];
        
        for (const method of methods) {
            if (text.toLowerCase().includes(method.toLowerCase())) {
                return method;
            }
        }
        
        return 'unknown';
    }
    
    /**
     * 輔助方法：提取關鍵信息
     */
    extractKeyInformation(text) {
        const keyPatterns = [
            /(?:金額|amount)[:\s]*([0-9,]+\.?[0-9]*)/gi,
            /(?:日期|date)[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi,
            /(?:編號|number|no)[:\s]*([A-Z0-9\-]+)/gi
        ];
        
        const keyInfo = [];
        
        keyPatterns.forEach(pattern => {
            let match;
            while ((match = pattern.exec(text)) !== null) {
                keyInfo.push({
                    type: match[0].split(/[:\s]/)[0],
                    value: match[1]
                });
            }
        });
        
        return keyInfo;
    }
    
    /**
     * 輔助方法：提取實體
     */
    extractEntities(text) {
        return {
            dates: this.extractDates(text),
            amounts: this.extractAmounts(text),
            emails: this.extractEmails(text),
            phones: this.extractPhones(text)
        };
    }
    
    /**
     * 提取日期
     */
    extractDates(text) {
        const datePattern = /\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}/g;
        return text.match(datePattern) || [];
    }
    
    /**
     * 提取金額
     */
    extractAmounts(text) {
        const amountPattern = /[0-9,]+\.?[0-9]*/g;
        return text.match(amountPattern) || [];
    }
    
    /**
     * 提取電子郵件
     */
    extractEmails(text) {
        const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
        return text.match(emailPattern) || [];
    }
    
    /**
     * 提取電話號碼
     */
    extractPhones(text) {
        const phonePattern = /(?:\+?[0-9]{1,3}[-.\s]?)?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}/g;
        return text.match(phonePattern) || [];
    }
    
    /**
     * 終止OCR引擎
     */
    async terminate() {
        if (this.worker) {
            await this.worker.terminate();
            this.worker = null;
            this.isInitialized = false;
            console.log('🔄 Tesseract.js OCR引擎已終止');
        }
    }
    
    /**
     * 獲取支援的語言列表
     */
    getSupportedLanguages() {
        return this.supportedLanguages;
    }
    
    /**
     * 檢查是否已初始化
     */
    isReady() {
        return this.isInitialized;
    }
}

// 全局實例
window.TesseractOCRProcessor = TesseractOCRProcessor;

console.log('✅ Tesseract OCR處理器已載入');
