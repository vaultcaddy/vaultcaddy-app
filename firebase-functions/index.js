const functions = require('firebase-functions');
const admin = require('firebase-admin');
const fetch = require('node-fetch'); // 確保 package.json 有 node-fetch

admin.initializeApp();

// 雲端函數：處理收據 OCR (已加入企業級安全與利潤防禦機制)
exports.processReceipt = functions.region('asia-east1').https.onCall(async (data, context) => {
    // ==========================================
    // 🛡️ 第一道防線：身份與參數驗證 (Payload Validation)
    // ==========================================
    const companyId = data.companyId;
    
    // 1. 必須提供公司 ID (用於扣除額度與追蹤)
    if (!companyId) {
        throw new functions.https.HttpsError('invalid-argument', '缺少公司識別碼 (companyId)，拒絕存取。');
    }
    
    // 2. 必須提供圖片
    if (!data.base64Image) {
        throw new functions.https.HttpsError('invalid-argument', '沒有提供圖片數據。');
    }

    // 3. 限制圖片大小 (防禦超大 Base64 導致內存溢出或 API 費用暴增)
    // 限制約為 5MB (Base64 長度約 7,000,000)
    if (data.base64Image.length > 7000000) {
        throw new functions.https.HttpsError('invalid-argument', '圖片檔案過大，請在前端壓縮後再上傳（限制 5MB）。');
    }

    const db = admin.firestore();
    const monthStr = new Date().toISOString().slice(0, 7); // e.g., "2026-04"
    const usageRef = db.collection('api_usage').doc(`${companyId}_${monthStr}`);

    try {
        // ==========================================
        // 🛡️ 第二道防線：Firestore 速率與額度限制 (Rate Limiting)
        // ==========================================
        // 使用 Transaction 確保高併發下的計數準確性，防止腳本狂刷
        await db.runTransaction(async (transaction) => {
            const usageDoc = await transaction.get(usageRef);
            let currentCount = 0;
            
            if (usageDoc.exists) {
                currentCount = usageDoc.data().receiptCount || 0;
            }

            // 💡 總顧問設定：HK$78/月 方案的硬性防禦上限是 500 張/月
            // (500張 * Qwen-VL 成本極低，保證 90% 利潤，同時防止腳本惡意刷破產)
            const MAX_MONTHLY_LIMIT = 500;
            if (currentCount >= MAX_MONTHLY_LIMIT) {
                throw new functions.https.HttpsError(
                    'resource-exhausted', 
                    `公司 ${companyId} 本月 AI 辨識額度 (${MAX_MONTHLY_LIMIT}張) 已耗盡。為保護系統，請升級方案或下個月再試。`
                );
            }

            // 額度內，計數器 +1
            transaction.set(usageRef, { 
                companyId: companyId,
                month: monthStr,
                receiptCount: currentCount + 1,
                lastUpdatedAt: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });
        });

        // ==========================================
        // 🛡️ 第三道防線：安全呼叫外部 AI API (隱藏 API Key)
        // ==========================================
        const API_KEY = functions.config().qwen.api_key; 
        
        const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'qwen-vl-plus',
                messages: [
                    {
                        role: 'user',
                        content: [
                            { type: 'image_url', image_url: { url: data.base64Image } },
                            { type: 'text', text: 'Extract receipt details for Hong Kong tax filing. Return ONLY a JSON object with: merchantName (string), date (YYYY-MM-DD), amount (number), category (choose one: Transportation, Entertainment, Meals, Fine, Software_SaaS, Office_Supplies), categoryLabel (Chinese translation of category).' }
                        ]
                    }
                ]
            })
        });

        if (!response.ok) {
            throw new Error(`DashScope API Error: ${response.statusText}`);
        }

        const result = await response.json();
        const content = result.choices[0].message.content;
        
        // 解析 JSON
        const jsonStr = content.replace(/```json\n?|\n?```/g, '').trim();
        const extractedData = JSON.parse(jsonStr);

        // 返回給前端
        return {
            success: true,
            data: extractedData
        };

    } catch (error) {
        console.error('OCR Processing Error:', error);
        // 如果是我們自定義的額度耗盡錯誤，直接拋出給前端顯示
        if (error instanceof functions.https.HttpsError) {
            throw error;
        }
        throw new functions.https.HttpsError('internal', 'AI 辨識失敗', error.message);
    }
});
