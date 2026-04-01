/**
 * 🔍 診斷工具：檢查圖2文檔為何沒有交易記錄
 * 
 * 使用方法：
 * 1. 打開文檔詳情頁面 (eStatementFile_20250829143359.pdf)
 * 2. 按 F12 打開 Console
 * 3. 複製此文件內容到 Console
 * 4. 運行命令：diagnoseDocument()
 */

async function diagnoseDocument() {
    console.log('🔍 開始診斷文檔...\n');
    
    try {
        // 1. 獲取文檔 ID
        const params = new URLSearchParams(window.location.search);
        const projectId = params.get('project');
        const documentId = params.get('id');
        
        if (!projectId || !documentId) {
            console.error('❌ 無法獲取文檔信息（請在文檔詳情頁面運行）');
            return;
        }
        
        console.log('📄 文檔信息:');
        console.log('  Project ID:', projectId);
        console.log('  Document ID:', documentId);
        console.log('');
        
        // 2. 從 Firestore 獲取文檔數據
        const db = firebase.firestore();
        const docRef = db.collection('projects').doc(projectId)
                         .collection('documents').doc(documentId);
        const docSnap = await docRef.get();
        
        if (!docSnap.exists) {
            console.error('❌ 文檔不存在');
            return;
        }
        
        const docData = docSnap.data();
        
        // 3. 分析文檔基本信息
        console.log('📊 基本信息:');
        console.log('  文件名:', docData.name);
        console.log('  類型:', docData.type);
        console.log('  狀態:', docData.status);
        console.log('  上傳時間:', docData.uploadedAt?.toDate?.() || '未知');
        console.log('');
        
        // 4. 分析處理數據
        const processedData = docData.processedData || {};
        const extractedData = docData.extractedData || {};
        const data = { ...processedData, ...extractedData };
        
        console.log('💰 財務數據:');
        console.log('  銀行名稱:', data.bankName || data.bank_name || '未提取');
        console.log('  賬戶號碼:', data.accountNumber || data.account_number || '未提取');
        console.log('  期初餘額:', data.openingBalance || data.opening_balance || '$0.00');
        console.log('  期末餘額:', data.closingBalance || data.closing_balance || '未提取');
        console.log('');
        
        // 5. 分析交易記錄
        const transactions = data.transactions || data.transaction || data.items || [];
        console.log('🔄 交易記錄分析:');
        console.log('  交易數量:', transactions.length);
        
        if (transactions.length > 0) {
            console.log('  ✅ 文檔包含交易記錄');
            console.log('  前3筆交易:');
            transactions.slice(0, 3).forEach((t, i) => {
                console.log(`    ${i + 1}. ${t.date} | ${t.description} | $${t.amount}`);
            });
        } else {
            console.log('  ❌ 沒有交易記錄！');
        }
        console.log('');
        
        // 6. 分析 OCR 文本
        const ocrText = docData.ocrText || '';
        console.log('📝 OCR 文本分析:');
        console.log('  文本長度:', ocrText.length, '字符');
        
        // 檢查頁面分隔符
        const pageMarkers = (ocrText.match(/=== 下一頁 ===/g) || []).length;
        console.log('  頁面分隔符:', pageMarkers, '個');
        console.log('  推測處理頁數:', pageMarkers + 1);
        
        // 檢查是否包含交易相關關鍵詞
        const hasTransactionKeywords = /transaction|交易|payment|deposit|withdrawal|存款|提款/i.test(ocrText);
        console.log('  包含交易關鍵詞:', hasTransactionKeywords ? '是' : '否');
        console.log('');
        
        // 7. 檢查圖片URL
        const imageUrls = docData.imageUrls || docData.imageUrl ? [docData.imageUrl] : [];
        console.log('📸 圖片文件:');
        console.log('  圖片數量:', imageUrls.length);
        if (imageUrls.length > 0) {
            imageUrls.forEach((url, i) => {
                console.log(`  圖片 ${i + 1}:`, url.split('/').pop());
            });
        }
        console.log('');
        
        // 8. 診斷總結
        console.log('━'.repeat(70));
        console.log('📋 診斷總結');
        console.log('━'.repeat(70));
        
        if (transactions.length === 0) {
            console.log('❌ 問題確認：文檔未包含交易記錄\n');
            
            // 分析可能原因
            console.log('🔎 可能原因:');
            if (pageMarkers === 0 && ocrText.length < 2000) {
                console.log('  ⚠️  只處理了第1頁（PDF拆分失敗）');
                console.log('     OCR文本過短，可能第2-3頁的交易記錄未被處理');
            } else if (!hasTransactionKeywords) {
                console.log('  ⚠️  OCR文本中沒有交易關鍵詞');
                console.log('     AI可能無法識別交易表格格式');
            } else {
                console.log('  ⚠️  AI提取失敗');
                console.log('     OCR文本正常但AI未能提取交易記錄');
            }
            
            console.log('\n💡 解決方案:');
            console.log('  1. ✅ 刪除此文檔');
            console.log('  2. ✅ 重新上傳同一份PDF');
            console.log('  3. ✅ 在上傳時打開Console觀察處理日誌');
            console.log('  4. ✅ 確認看到"PDF 載入成功，共 3 頁"的日誌');
            console.log('  5. ✅ 確認看到"批量 OCR 3 頁"的日誌');
            
        } else {
            console.log('✅ 文檔處理正常，包含', transactions.length, '筆交易');
        }
        
        console.log('━'.repeat(70));
        console.log('\n📌 提示：如需查看完整原始數據，運行: showRawData()');
        
        // 保存數據供進一步檢查
        window.diagnosticData = docData;
        
    } catch (error) {
        console.error('❌ 診斷失敗:', error);
    }
}

// 輔助函數：顯示原始數據
function showRawData() {
    if (!window.diagnosticData) {
        console.error('請先運行 diagnoseDocument()');
        return;
    }
    
    console.log('\n📊 完整原始數據:');
    console.log(JSON.stringify(window.diagnosticData, null, 2));
}

console.log('✅ 診斷工具已加載');
console.log('運行命令: diagnoseDocument()');

