/**
 * VaultCaddy DeepSeek Vision 客戶端
 * 
 * 作用：
 * 1. 處理圖片文檔，提取關鍵信息
 * 2. 使用 DeepSeek Vision 模型，提供高準確度的數據提取
 * 3. 支持發票、收據、銀行對帳單等文檔類型
 * 
 * @version 1.0.0
 * @updated 2025-10-26
 */
class DeepSeekVisionClient {
    constructor(workerUrl) {
        if (!workerUrl) {
            console.error('❌ Cloudflare Worker URL 未提供！');
            throw new Error('Cloudflare Worker URL is required.');
        }
        this.workerUrl = workerUrl;
        
        // ✅ 嘗試使用支持圖片的模型
        // 可能的模型名稱：
        // - deepseek-vl2 (DeepSeek-VL2)
        // - deepseek-ocr (DeepSeek-OCR)
        // - janus-pro (Janus-Pro)
        // 如果不支持，會自動降級
        this.modelsToTry = [
            'deepseek-vl2',      // DeepSeek-VL2 (最推薦)
            'deepseek-ocr',      // DeepSeek-OCR
            'janus-pro-7b',      // Janus-Pro 7B
            'janus-pro-1b',      // Janus-Pro 1B
            'deepseek-chat'      // 純文本模型（降級選項）
        ];
        
        this.model = this.modelsToTry[0]; // 默認使用第一個
        this.maxRetries = 3;
        this.retryDelay = 2000; // 2 seconds
        
        console.log('🤖 DeepSeek Vision Client 初始化');
        console.log('   ✅ Worker URL:', this.workerUrl);
        console.log('   ✅ 嘗試模型:', this.modelsToTry);
        console.log('   ✅ 默認模型:', this.model);
    }
    
    /**
     * 將文件轉換為 Base64 格式
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]); // 只取 Base64 部分
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
    
    /**
     * 根據文檔類型生成優化後的提示詞
     */
    generatePrompt(documentType, file) {
        let prompt = '';
        
        // 統一的 JSON 輸出格式要求
        const jsonFormatInstruction = `
        CRITICAL RULE: The output MUST be a pure JSON object. Do NOT include any other text, explanations, or markdown outside the JSON.
        The JSON structure should be as follows:
        {
            "document_type": "invoice | receipt | bank_statement | general",
            "confidence_score": 0-100, // Overall confidence of extraction
            "extracted_data": { ... } // Document-specific data
        }
        `;
        
        switch (documentType) {
            case 'invoice':
                prompt = `
                You are an expert accounting AI. Analyze the provided invoice image.
                Extract ALL relevant information for bookkeeping and reconciliation.
                
                CRITICAL RULES:
                1. Extract ALL line items with their code, description, quantity, unit, unit_price, and amount. If any field is missing, use an empty string or 0.
                2. Calculate subtotal, discount, tax, and total. If tax is not explicitly stated, assume 0.
                3. Identify currency (e.g., HKD, USD). Default to HKD if not found.
                4. Extract supplier and customer details including name, address, phone, and email.
                5. Extract payment method, payment status, due date, and any specific payment IDs (e.g., FPS ID, PayMe Number).
                6. If a field is not present, return an empty string or 0, do NOT make up data.
                7. Ensure all numerical values are parsed as numbers (float or integer).
                8. Dates should be in YYYY-MM-DD format.
                
                Extract the following fields:
                - invoice_number (string)
                - date (YYYY-MM-DD)
                - due_date (YYYY-MM-DD)
                - supplier: { name (string), name_en (string, if available), address (string), phone (string), email (string) }
                - customer: { name (string), address (string), contact (string), phone (string) }
                - items: [ { code (string), description (string), quantity (number), unit (string), unit_price (number), amount (number) } ]
                - subtotal (number)
                - discount (number)
                - tax (number)
                - total (number)
                - currency (string, e.g., HKD)
                - payment_method (string)
                - payment_status (string)
                - payment_info: { fps_id (string), payme_number (string) }
                - notes (string)
                
                Example for line items:
                "items": [
                    { "code": "ITEM001", "description": "Product A", "quantity": 2, "unit": "pcs", "unit_price": 100.00, "amount": 200.00 },
                    { "code": "ITEM002", "description": "Service B", "quantity": 1, "unit": "hr", "unit_price": 500.00, "amount": 500.00 }
                ]
                `;
                break;
            
            case 'receipt':
                prompt = `
                You are an expert accounting AI. Analyze the provided receipt image.
                Extract ALL relevant information for bookkeeping and reconciliation.
                
                CRITICAL RULES:
                1. Extract merchant details including name, address, phone, and email.
                2. Extract transaction date and time.
                3. Extract ALL line items with their description, quantity, unit_price, and amount.
                4. Calculate subtotal, tax, and total. If tax is not explicitly stated, assume 0.
                5. Identify currency (e.g., HKD, USD). Default to HKD if not found.
                6. Extract payment method.
                7. If a field is not present, return an empty string or 0, do NOT make up data.
                8. Ensure all numerical values are parsed as numbers (float or integer).
                9. Dates should be in YYYY-MM-DD format, time in HH:MM.
                
                Extract the following fields:
                - transaction_id (string)
                - date (YYYY-MM-DD)
                - time (HH:MM)
                - merchant: { name (string), address (string), phone (string), email (string) }
                - items: [ { description (string), quantity (number), unit_price (number), amount (number) } ]
                - subtotal (number)
                - tax (number)
                - total (number)
                - currency (string, e.g., HKD)
                - payment_method (string)
                - notes (string)
                `;
                break;
            
            case 'bank_statement':
                prompt = `
                You are an expert accounting AI. Analyze the provided bank statement image.
                Extract ALL relevant information for bookkeeping and reconciliation.
                
                CRITICAL RULES:
                1. Extract bank name, account number, and account holder name.
                2. Extract the statement period (start and end dates).
                3. Extract opening and closing balances.
                4. Extract ALL transactions with their date, description, type (credit/debit), amount, and running balance.
                5. If a field is not present, return an empty string or 0, do NOT make up data.
                6. Ensure all numerical values are parsed as numbers (float or integer).
                7. Dates should be in YYYY-MM-DD format.
                
                Extract the following fields:
                - bank: { name (string), address (string) }
                - account_number (string)
                - account_holder: { name (string) }
                - statement_period: { from (YYYY-MM-DD), to (YYYY-MM-DD) }
                - opening_balance (number)
                - closing_balance (number)
                - currency (string, e.g., HKD)
                - transactions: [ { date (YYYY-MM-DD), description (string), type (string, "credit" or "debit"), amount (number), balance (number) } ]
                `;
                break;
            
            default: // general document
                prompt = `
                You are an expert document analysis AI. Analyze the provided document image.
                Extract key entities and a summary of the document's content.
                
                CRITICAL RULES:
                1. Identify the main purpose or type of the document.
                2. Extract any dates, names, addresses, and monetary values.
                3. Provide a concise summary of the document's content.
                4. If a field is not present, return an empty string or 0, do NOT make up data.
                
                Extract the following fields:
                - document_type_identified (string, e.g., "General Document", "Letter", "Contract")
                - main_entities: [ { type (string, e.g., "Person", "Organization", "Date", "Amount"), value (string) } ]
                - summary (string)
                `;
                break;
        }
        
        return {
            system: `You are a highly accurate AI assistant specialized in extracting structured data from financial documents.
            Your task is to meticulously analyze the provided image and extract all requested information.
            ${jsonFormatInstruction}`,
            user: prompt
        };
    }
    
    /**
     * 處理文檔（智能模型選擇）
     */
    async processDocument(file, documentType = 'general') {
        console.log(`🚀 DeepSeek Vision Client 處理文檔: ${file.name} (${documentType})`);
        
        let base64Data;
        try {
            base64Data = await this.fileToBase64(file);
        } catch (error) {
            console.error('❌ 文件轉 Base64 失敗:', error);
            throw new Error('Failed to convert file to Base64 for DeepSeek Vision.');
        }
        
        const { system, user } = this.generatePrompt(documentType, file);
        
        // 🔄 智能模型選擇：按順序嘗試每個模型
        for (let modelIndex = 0; modelIndex < this.modelsToTry.length; modelIndex++) {
            const currentModel = this.modelsToTry[modelIndex];
            console.log(`\n🤖 嘗試模型 ${modelIndex + 1}/${this.modelsToTry.length}: ${currentModel}`);
            
            const requestBody = {
                model: currentModel,
                messages: [
                    {
                        role: "system",
                        content: system
                    },
                    {
                        role: "user",
                        content: [
                            {
                                type: "text",
                                text: user
                            },
                            {
                                type: "image_url",
                                image_url: {
                                    url: `data:${file.type};base64,${base64Data}`
                                }
                            }
                        ]
                    }
                ],
                max_tokens: 4000,
                temperature: 0.1
            };
            
            try {
                console.log(`   📤 發送請求到 DeepSeek API...`);
                const response = await fetch(this.workerUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    console.warn(`   ⚠️ 模型 ${currentModel} 失敗 (${response.status}):`, errorData.error?.message || errorData.message);
                    
                    // 如果是 400 錯誤（模型不支持），嘗試下一個模型
                    if (response.status === 400) {
                        console.log(`   ⏭️  跳過模型 ${currentModel}，嘗試下一個...`);
                        continue;
                    }
                    
                    throw new Error(`DeepSeek API error: ${response.status} - ${errorData.error?.message || response.statusText}`);
                }
                
                const data = await response.json();
                
                if (!data.choices || data.choices.length === 0 || !data.choices[0].message) {
                    throw new Error('DeepSeek API 返回無效響應');
                }
                
                const content = data.choices[0].message.content;
                console.log(`   ✅ 模型 ${currentModel} 成功返回響應`);
                console.log(`   📄 響應內容:`, content.substring(0, 200) + '...');
                
                let parsedData;
                try {
                    parsedData = JSON.parse(content);
                } catch (jsonError) {
                    console.error('   ❌ JSON 解析失敗:', jsonError);
                    // 嘗試清理響應（移除 markdown 代碼塊）
                    const cleaned = content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
                    try {
                        parsedData = JSON.parse(cleaned);
                        console.log('   ✅ 清理後 JSON 解析成功');
                    } catch (cleanError) {
                        throw new Error('Failed to parse DeepSeek response as JSON.');
                    }
                }
                
                // 檢查並確保返回的 JSON 結構符合預期
                if (!parsedData.document_type || !parsedData.extracted_data) {
                    console.warn('   ⚠️ JSON 結構不完整，嘗試下一個模型...');
                    continue;
                }
                
                // 🎉 成功！記錄使用的模型
                this.model = currentModel; // 更新為成功的模型
                console.log(`\n🎉 成功使用模型: ${currentModel}`);
                
                return {
                    success: true,
                    documentType: parsedData.document_type,
                    confidence: parsedData.confidence_score || 0,
                    extractedData: parsedData.extracted_data,
                    model: currentModel, // 返回使用的模型名稱
                    rawResponse: data
                };
                
            } catch (error) {
                console.error(`   ❌ 模型 ${currentModel} 處理失敗:`, error.message);
                
                // 如果不是最後一個模型，繼續嘗試下一個
                if (modelIndex < this.modelsToTry.length - 1) {
                    console.log(`   ⏭️  嘗試下一個模型...`);
                    continue;
                } else {
                    // 所有模型都失敗了
                    throw new Error(`所有 DeepSeek 模型都失敗了。最後錯誤: ${error.message}`);
                }
            }
        }
        
        // 如果所有模型都失敗（不應該到達這裡）
        throw new Error('無法使用任何 DeepSeek 模型處理文檔');
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.DeepSeekVisionClient = DeepSeekVisionClient;
    console.log('✅ DeepSeek Vision Client 模塊已載入');
}

// Node.js 環境導出 (如果需要)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DeepSeekVisionClient;
}

