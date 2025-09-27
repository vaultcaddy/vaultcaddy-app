#!/usr/bin/env node

/**
 * VaultCaddy Google AI API 測試腳本
 * 測試配置的 API 金鑰是否正常工作
 */

const https = require('https');

// API 金鑰
const API_KEY = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug';

// 測試數據
const testData = {
    contents: [{
        parts: [{
            text: '請用繁體中文回答：VaultCaddy API 測試成功！請確認你能正常回答。'
        }]
    }]
};

function testGoogleAI() {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify(testData);
        
        const options = {
            hostname: 'generativelanguage.googleapis.com',
            port: 443,
            path: `/v1beta/models/gemini-pro:generateContent?key=${API_KEY}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        console.log('🧪 測試 Google AI API...');
        console.log(`📡 API 端點: ${options.hostname}${options.path}`);

        const req = https.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    
                    if (res.statusCode === 200) {
                        console.log('✅ API 測試成功！');
                        console.log('📊 狀態碼:', res.statusCode);
                        
                        if (response.candidates && response.candidates[0]) {
                            const generatedText = response.candidates[0].content.parts[0].text;
                            console.log('🤖 AI 回應:');
                            console.log('-'.repeat(50));
                            console.log(generatedText);
                            console.log('-'.repeat(50));
                            
                            if (response.usageMetadata) {
                                console.log('📈 用量統計:');
                                console.log(`   輸入 tokens: ${response.usageMetadata.promptTokenCount || 'N/A'}`);
                                console.log(`   輸出 tokens: ${response.usageMetadata.candidatesTokenCount || 'N/A'}`);
                                console.log(`   總共 tokens: ${response.usageMetadata.totalTokenCount || 'N/A'}`);
                            }
                        }
                        
                        resolve(response);
                    } else {
                        console.log('❌ API 測試失敗');
                        console.log('📊 狀態碼:', res.statusCode);
                        console.log('📄 錯誤回應:', data);
                        reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                    }
                } catch (error) {
                    console.log('❌ 解析回應失敗');
                    console.log('📄 原始回應:', data);
                    reject(error);
                }
            });
        });

        req.on('error', (error) => {
            console.log('❌ 請求失敗');
            console.error('🚨 錯誤詳情:', error.message);
            reject(error);
        });

        req.on('timeout', () => {
            console.log('❌ 請求超時');
            req.destroy();
            reject(new Error('Request timeout'));
        });

        req.setTimeout(30000); // 30 秒超時
        req.write(postData);
        req.end();
    });
}

// 執行測試
async function main() {
    console.log('🚀 VaultCaddy Google AI API 測試');
    console.log('=' .repeat(50));
    console.log(`🔑 API 金鑰: ${API_KEY.substring(0, 10)}...`);
    console.log('⏰ 測試時間:', new Date().toISOString());
    console.log();

    try {
        await testGoogleAI();
        console.log();
        console.log('🎉 所有測試通過！VaultCaddy 的 Google AI 整合已就緒。');
        console.log();
        console.log('📋 下一步：');
        console.log('1. 執行部署：./simple-deploy.sh');
        console.log('2. 測試網站：https://vaultcaddy.com');
        console.log('3. 驗證功能：上傳文檔測試 AI 處理');
        
        process.exit(0);
    } catch (error) {
        console.log();
        console.log('🚨 測試失敗！');
        console.error('錯誤：', error.message);
        console.log();
        console.log('🔧 可能的解決方案：');
        console.log('1. 檢查 API 金鑰是否正確');
        console.log('2. 確認 Generative Language API 已啟用');
        console.log('3. 檢查網絡連接');
        console.log('4. 驗證 API 配額限制');
        
        process.exit(1);
    }
}

// 處理未捕獲的異常
process.on('unhandledRejection', (reason, promise) => {
    console.error('未處理的 Promise 拒絕:', reason);
    process.exit(1);
});

process.on('uncaughtException', (error) => {
    console.error('未捕獲的異常:', error);
    process.exit(1);
});

main();
