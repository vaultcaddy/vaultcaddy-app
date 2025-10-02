/**
 * 🚨 VaultCaddy 緊急修復腳本
 * 解決文件消失和數據顯示問題
 */

// 在瀏覽器控制台中運行此腳本

console.log('🚨 開始 VaultCaddy 緊急修復...');

// 1. 檢查當前問題
function diagnoseProblems() {
    console.log('🔍 診斷當前問題...');
    
    const problems = [];
    
    // 檢查處理器載入狀態
    if (!window.UnifiedDocumentProcessor) {
        problems.push('❌ 統一處理器未載入');
    }
    
    if (!window.GoogleAIProcessor) {
        problems.push('❌ Google AI處理器未載入');
    }
    
    if (!window.ledgerBoxProcessor) {
        problems.push('❌ LedgerBox處理器未載入');
    }
    
    // 檢查API Key
    const apiKey = localStorage.getItem('google_ai_api_key');
    if (!apiKey) {
        problems.push('❌ 缺少Google AI API Key');
    }
    
    // 檢查存儲數據
    const storageKeys = Object.keys(localStorage).filter(key => key.includes('vaultcaddy'));
    console.log(`📁 找到 ${storageKeys.length} 個存儲項目:`, storageKeys);
    
    if (problems.length > 0) {
        console.error('🚨 發現問題:', problems);
    } else {
        console.log('✅ 基本檢查通過');
    }
    
    return problems;
}

// 2. 修復存儲格式不一致問題
function fixStorageInconsistency() {
    console.log('🔧 修復存儲格式不一致...');
    
    const docTypes = ['bank-statement', 'invoice', 'receipt', 'general'];
    let totalFixed = 0;
    
    docTypes.forEach(docType => {
        // 檢查舊格式存儲
        const oldKey = `vaultcaddy_files_${docType}`;
        const newKey = `vaultcaddy_unified_files_${docType}`;
        
        const oldData = localStorage.getItem(oldKey);
        const newData = localStorage.getItem(newKey);
        
        if (oldData && !newData) {
            console.log(`📦 遷移 ${docType} 數據從舊格式到統一格式`);
            
            try {
                const oldFiles = JSON.parse(oldData);
                const unifiedFiles = oldFiles.map(file => ({
                    id: file.id,
                    fileName: file.name,
                    documentType: file.documentType,
                    processedAt: new Date().toISOString(),
                    aiProcessed: file.processedData?.aiProcessed || false,
                    version: '3.0.0',
                    fileSize: file.size || 0,
                    ...file.processedData
                }));
                
                localStorage.setItem(newKey, JSON.stringify(unifiedFiles));
                console.log(`✅ 遷移了 ${unifiedFiles.length} 個 ${docType} 文件`);
                totalFixed += unifiedFiles.length;
            } catch (error) {
                console.error(`❌ 遷移 ${docType} 失敗:`, error);
            }
        }
    });
    
    console.log(`🎉 總共修復了 ${totalFixed} 個文件的存儲格式`);
}

// 3. 清理重複和損壞的數據
function cleanupCorruptedData() {
    console.log('🧹 清理損壞的數據...');
    
    const allKeys = Object.keys(localStorage);
    const vaultcaddyKeys = allKeys.filter(key => key.includes('vaultcaddy'));
    
    vaultcaddyKeys.forEach(key => {
        try {
            const data = localStorage.getItem(key);
            JSON.parse(data); // 測試是否為有效JSON
        } catch (error) {
            console.warn(`🗑️ 移除損壞的存儲項目: ${key}`);
            localStorage.removeItem(key);
        }
    });
}

// 4. 強制重新載入處理器
function forceReloadProcessors() {
    console.log('🔄 強制重新載入處理器...');
    
    // 清理現有實例
    if (window.UnifiedDocumentProcessor) {
        delete window.UnifiedDocumentProcessor;
    }
    if (window.ledgerBoxProcessor) {
        delete window.ledgerBoxProcessor;
    }
    
    // 重新載入腳本（如果在頁面中）
    const scripts = ['unified-document-processor.js', 'ledgerbox-integration.js'];
    scripts.forEach(scriptName => {
        const existingScript = document.querySelector(`script[src="${scriptName}"]`);
        if (existingScript) {
            const newScript = document.createElement('script');
            newScript.src = scriptName + '?t=' + Date.now(); // 緩存破壞
            document.head.appendChild(newScript);
            console.log(`🔄 重新載入 ${scriptName}`);
        }
    });
}

// 5. 設置API Key（如果缺少）
function setupApiKey() {
    const apiKey = localStorage.getItem('google_ai_api_key');
    if (!apiKey) {
        const userApiKey = prompt('請輸入您的 Google AI API Key:');
        if (userApiKey && userApiKey.trim()) {
            localStorage.setItem('google_ai_api_key', userApiKey.trim());
            console.log('✅ API Key 已設置');
            return true;
        } else {
            console.warn('⚠️ 未設置 API Key，AI功能將無法使用');
            return false;
        }
    }
    return true;
}

// 6. 測試修復結果
async function testFix() {
    console.log('🧪 測試修復結果...');
    
    // 測試存儲載入
    if (window.UnifiedDocumentProcessor) {
        const receiptFiles = window.UnifiedDocumentProcessor.getAllProcessedDocuments('receipt');
        console.log(`📄 找到 ${receiptFiles.length} 個收據文件`);
        
        if (receiptFiles.length > 0) {
            console.log('收據文件:', receiptFiles.map(f => f.fileName));
        }
    }
    
    // 測試API連接
    const apiKey = localStorage.getItem('google_ai_api_key');
    if (apiKey) {
        try {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`);
            if (response.ok) {
                console.log('✅ Google AI API 連接正常');
            } else {
                console.error('❌ Google AI API 連接失敗:', response.status);
            }
        } catch (error) {
            console.error('❌ API 測試失敗:', error.message);
        }
    }
}

// 7. 主修復函數
async function emergencyFix() {
    console.log('🚨🔧 開始緊急修復程序...');
    
    try {
        // 步驟1：診斷問題
        const problems = diagnoseProblems();
        
        // 步驟2：修復存儲
        fixStorageInconsistency();
        
        // 步驟3：清理損壞數據
        cleanupCorruptedData();
        
        // 步驟4：設置API Key
        const apiKeySet = setupApiKey();
        
        // 步驟5：強制重新載入處理器
        forceReloadProcessors();
        
        // 等待處理器載入
        setTimeout(async () => {
            // 步驟6：測試修復結果
            await testFix();
            
            console.log('🎉 緊急修復完成！');
            console.log('📋 建議操作:');
            console.log('1. 重新載入頁面 (location.reload())');
            console.log('2. 重新上傳 img_5268.JPG');
            console.log('3. 檢查是否正確顯示收據數據');
            
            if (confirm('修復完成！是否立即重新載入頁面？')) {
                location.reload();
            }
        }, 2000);
        
    } catch (error) {
        console.error('❌ 緊急修復失敗:', error);
    }
}

// 導出函數供手動調用
window.VaultCaddyEmergencyFix = {
    diagnoseProblems,
    fixStorageInconsistency,
    cleanupCorruptedData,
    forceReloadProcessors,
    setupApiKey,
    testFix,
    emergencyFix
};

console.log('🔧 緊急修復腳本已載入');
console.log('💡 使用方法:');
console.log('  - 自動修復: VaultCaddyEmergencyFix.emergencyFix()');
console.log('  - 診斷問題: VaultCaddyEmergencyFix.diagnoseProblems()');
console.log('  - 修復存儲: VaultCaddyEmergencyFix.fixStorageInconsistency()');

// 如果直接在控制台運行，自動開始修復
if (typeof window !== 'undefined' && window.location) {
    console.log('🚀 自動開始緊急修復...');
    emergencyFix();
}
