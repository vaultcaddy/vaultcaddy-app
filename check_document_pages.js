/**
 * 检查Firestore中文档的页面处理情况
 * 
 * 使用方法：
 * 1. 在浏览器Console中运行此脚本
 * 2. 查看该文档是否包含所有页面的数据
 */

async function checkDocumentPages(documentId) {
    console.log('🔍 检查文档页面处理情况...');
    console.log('文档ID:', documentId);
    
    try {
        // 获取当前文档
        const docRef = firebase.firestore()
            .collection('documents')
            .doc(documentId);
        
        const doc = await docRef.get();
        
        if (!doc.exists) {
            console.error('❌ 文档不存在');
            return;
        }
        
        const data = doc.data();
        console.log('\n📊 文档基本信息:');
        console.log('  文件名:', data.fileName);
        console.log('  文档类型:', data.documentType);
        console.log('  状态:', data.status);
        console.log('  上传时间:', data.uploadedAt);
        
        // 检查processedData
        console.log('\n📦 处理数据:');
        if (!data.processedData) {
            console.warn('⚠️  没有processedData字段');
            return;
        }
        
        const processed = data.processedData;
        console.log('  银行名称:', processed.bankName || processed.bank_name || '未提取');
        console.log('  账户号码:', processed.accountNumber || processed.account_number || '未提取');
        console.log('  对账单日期:', processed.statementDate || processed.statement_date || '未提取');
        
        // 关键：检查交易记录
        console.log('\n💰 交易记录分析:');
        const transactions = processed.transactions || 
                           processed.transaction || 
                           processed.items || 
                           [];
        
        console.log('  交易数量:', transactions.length);
        
        if (transactions.length === 0) {
            console.error('❌ 没有交易记录！');
            console.log('\n🔍 可能的原因:');
            console.log('  1. PDF只处理了第1页（恒生银行交易通常在第2-3页）');
            console.log('  2. AI未能识别交易表格格式');
            console.log('  3. OCR文本质量不佳');
            
            // 检查是否有多页标记
            if (processed.total_pages) {
                console.log('\n📄 页面信息:');
                console.log('  总页数:', processed.total_pages);
            } else {
                console.warn('⚠️  没有total_pages字段，可能只处理了1页');
            }
            
            // 检查OCR原始文本
            if (data.ocrText || data.rawText) {
                const text = data.ocrText || data.rawText;
                console.log('\n📝 OCR文本长度:', text.length, '字符');
                
                // 检查是否包含"下一頁"标记
                const pageMarkers = (text.match(/=== 下一頁 ===/g) || []).length;
                console.log('  检测到页面分隔符:', pageMarkers, '个');
                console.log('  推测处理页数:', pageMarkers + 1);
                
                // 检查是否包含交易相关关键词
                const hasTransactionKeywords = /transaction|deposit|withdrawal|debit|credit|交易|存款|取款/i.test(text);
                console.log('  包含交易关键词:', hasTransactionKeywords ? '是' : '否');
            }
        } else {
            console.log('✅ 找到交易记录！');
            console.log('  前3笔交易:');
            transactions.slice(0, 3).forEach((tx, i) => {
                console.log(`    ${i+1}. ${tx.date} | ${tx.description} | ${tx.amount}`);
            });
        }
        
        // 检查期初/期末余额
        console.log('\n💵 余额信息:');
        console.log('  期初余额:', processed.openingBalance || processed.opening_balance || '未提取');
        console.log('  期末余额:', processed.closingBalance || processed.closing_balance || '未提取');
        
        // 生成诊断报告
        console.log('\n' + '='.repeat(70));
        console.log('📋 诊断总结');
        console.log('='.repeat(70));
        
        if (transactions.length === 0) {
            console.log('❌ 问题确认：文档未包含交易记录');
            console.log('\n💡 建议解决方案：');
            console.log('  1. ✅ 删除此文档');
            console.log('  2. ✅ 重新上传同一份PDF');
            console.log('  3. ✅ 在上传时打开Console观察处理日志');
            console.log('  4. ✅ 确认看到"批量 OCR 3 頁"的日志');
        } else {
            console.log('✅ 文档处理正常，包含', transactions.length, '笔交易');
        }
        
    } catch (error) {
        console.error('❌ 检查失败:', error);
    }
}

// 使用示例
console.log(`
╔══════════════════════════════════════════════════════════════════════╗
║         📊 文档页面处理检查工具                                      ║
╚══════════════════════════════════════════════════════════════════════╝

使用方法：
1. 复制此脚本到浏览器Console
2. 运行以下命令：

checkDocumentPages('CkcR1opFx5EuPscwRfv8');

将会显示详细的诊断信息。
`);

