const functions = require('firebase-functions');
const admin = require('firebase-admin');
const fetch = require('node-fetch'); // 確保 package.json 有 node-fetch

admin.initializeApp();

// 雲端函數：處理收據 OCR
exports.processReceipt = functions.region('asia-east1').https.onCall(async (data, context) => {
    // 1. 權限驗證 (確保是用戶或授權的員工)
    // 這裡可以根據你的業務邏輯調整，例如檢查 data.companyId 是否有效
    if (!data.base64Image) {
        throw new functions.https.HttpsError('invalid-argument', '沒有提供圖片數據');
    }

    try {
        const API_KEY = functions.config().qwen.api_key; // 從 Firebase Config 獲取
        
        // 2. 呼叫 Qwen3-VL-Plus (DashScope)
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
        
        // 3. 解析 JSON
        const jsonStr = content.replace(/```json\n?|\n?```/g, '').trim();
        const extractedData = JSON.parse(jsonStr);

        // 4. 返回給前端
        return {
            success: true,
            data: extractedData
        };

    } catch (error) {
        console.error('OCR Processing Error:', error);
        throw new functions.https.HttpsError('internal', 'AI 辨識失敗', error.message);
    }
});
