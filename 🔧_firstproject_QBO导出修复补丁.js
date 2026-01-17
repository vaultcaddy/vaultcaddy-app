/**
 * 🔧 firstproject.html QBO 导出功能修复补丁
 * 
 * 问题: 旧版 generateQBO() 函数只为每个文档创建1笔交易
 * 解决: 遍历每个文档的 transactions 数组，为每笔交易创建 STMTTRN
 * 
 * 使用方法:
 * 1. 打开 firstproject.html
 * 2. 找到第 4724-4827 行的 generateQBO() 函数
 * 3. 完整替换为下面的新函数
 */

// ✅ 新版 generateQBO() 函数 - 完整版
function generateQBO(docs) {
    console.log('📊 生成 QBO 文件（批量导出）...');
    console.log(`📋 文档数量: ${docs.length}`);
    
    const now = new Date();
    const formatQBODateTime = (date) => {
        const d = new Date(date);
        return d.getFullYear() + 
               String(d.getMonth() + 1).padStart(2, '0') + 
               String(d.getDate()).padStart(2, '0') + 
               String(d.getHours()).padStart(2, '0') + 
               String(d.getMinutes()).padStart(2, '0') + 
               String(d.getSeconds()).padStart(2, '0');
    };
    
    const formatQBODate = (dateStr) => {
        if (!dateStr) return formatQBODateTime(now);
        const d = new Date(dateStr);
        if (isNaN(d)) return formatQBODateTime(now);
        return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0');
    };
    
    const escapeXML = (str) => {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&apos;');
    };
    
    // ✅ 将交易类型映射到 OFX TRNTYPE
    const mapTransactionType = (type) => {
        if (!type) return 'OTHER';
        const t = type.toLowerCase();
        if (t.includes('deposit') || t.includes('存款') || t.includes('入账')) return 'CREDIT';
        if (t.includes('withdraw') || t.includes('提款') || t.includes('转出')) return 'DEBIT';
        if (t.includes('check') || t.includes('支票')) return 'CHECK';
        if (t.includes('atm')) return 'ATM';
        if (t.includes('pos') || t.includes('刷卡')) return 'POS';
        if (t.includes('transfer') || t.includes('转账')) return 'XFER';
        if (t.includes('payment') || t.includes('付款')) return 'PAYMENT';
        if (t.includes('fee') || t.includes('费用')) return 'FEE';
        if (t.includes('interest') || t.includes('利息')) return 'INT';
        return 'OTHER';
    };
    
    // ✅ 获取第一个文档的银行信息
    const firstDoc = docs[0];
    const firstData = firstDoc?.processedData || {};
    const bankCode = firstData.bankCode || firstData.bankName || '000000000';
    const accountNumber = firstData.accountNumber || '123456789';
    const currency = firstData.currency || 'HKD';
    
    // QBO 文件头
    let qbo = `OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<DTSERVER>${formatQBODateTime(now)}</DTSERVER>
<LANGUAGE>ENG</LANGUAGE>
</SONRS>
</SIGNONMSGSRSV1>
<BANKMSGSRSV1>
<STMTTRNRS>
<TRNUID>1</TRNUID>
<STATUS>
<CODE>0</CODE>
<SEVERITY>INFO</SEVERITY>
</STATUS>
<STMTRS>
<CURDEF>${currency}</CURDEF>
<BANKACCTFROM>
<BANKID>${escapeXML(bankCode)}</BANKID>
<ACCTID>${escapeXML(accountNumber)}</ACCTID>
<ACCTTYPE>CHECKING</ACCTTYPE>
</BANKACCTFROM>
<BANKTRANLIST>
<DTSTART>${formatQBODateTime(now)}</DTSTART>
<DTEND>${formatQBODateTime(now)}</DTEND>
`;
    
    // ✅ 遍历每个文档的交易记录
    let transactionIndex = 0;
    let totalTransactions = 0;
    
    docs.forEach(doc => {
        const data = doc.processedData || {};
        
        // ✅ 检查是否是银行对账单（有 transactions 数组）
        if (data.transactions && Array.isArray(data.transactions) && data.transactions.length > 0) {
            // ✅ 银行对账单：遍历所有交易记录
            console.log(`  📄 处理银行对账单: ${doc.fileName} (${data.transactions.length} 笔交易)`);
            
            data.transactions.forEach(tx => {
                const amount = parseFloat(tx.amount || 0);
                const trnType = mapTransactionType(tx.transactionType);
                const payee = escapeXML(tx.payee || tx.description || '');
                const memo = escapeXML(tx.memo || tx.referenceNumber || '');
                
                qbo += `<STMTTRN>
<TRNTYPE>${trnType}</TRNTYPE>
<DTPOSTED>${formatQBODate(tx.date)}</DTPOSTED>
<TRNAMT>${amount.toFixed(2)}</TRNAMT>
<FITID>${++transactionIndex}</FITID>
<NAME>${payee}</NAME>
<MEMO>${memo}</MEMO>
`;
                
                // ✅ 如果有支票号码，添加 CHECKNUM 字段
                if (tx.checkNumber) {
                    qbo += `<CHECKNUM>${escapeXML(tx.checkNumber)}</CHECKNUM>\n`;
                }
                
                qbo += `</STMTTRN>
`;
                totalTransactions++;
            });
        } else {
            // ✅ 发票/收据：为整个文档创建1笔交易
            console.log(`  📄 处理发票/收据: ${doc.fileName}`);
            
            const amount = -(parseFloat(data.totalAmount || data.total || data.amount || 0));
            const name = escapeXML(data.vendor || data.supplier || data.merchantName || data.source || 'Unknown');
            const invoiceNumber = data.invoiceNumber || data.receiptNumber || data.documentNumber || '';
            
            let memo = '';
            if (invoiceNumber) {
                memo += `Invoice: ${invoiceNumber}`;
            }
            if (data.items && Array.isArray(data.items) && data.items.length > 0) {
                const itemsSummary = data.items.map(item => item.description || item.name).filter(Boolean).join(', ');
                memo += (memo ? ' | ' : '') + itemsSummary.substring(0, 100);
            }
            if (!memo) {
                memo = data.notes || data.memo || doc.fileName || '';
            }
            
            let trntype = 'OTHER';
            if (data.documentType === 'invoice') {
                trntype = 'DEBIT';
            } else if (data.documentType === 'receipt') {
                trntype = 'POS';
            }
            
            qbo += `<STMTTRN>
<TRNTYPE>${trntype}</TRNTYPE>
<DTPOSTED>${formatQBODate(data.invoiceDate || data.transactionDate || data.date)}</DTPOSTED>
<TRNAMT>${amount.toFixed(2)}</TRNAMT>
<FITID>${++transactionIndex}</FITID>
<NAME>${name}</NAME>
<MEMO>${escapeXML(memo)}</MEMO>
`;
            
            if (invoiceNumber) {
                qbo += `<CHECKNUM>${escapeXML(invoiceNumber)}</CHECKNUM>\n`;
            }
            
            qbo += `</STMTTRN>
`;
            totalTransactions++;
        }
    });
    
    // QBO 文件尾
    const closingBalance = firstData.closingBalance || firstData.balance || 0;
    qbo += `</BANKTRANLIST>
<LEDGERBAL>
<BALAMT>${parseFloat(closingBalance).toFixed(2)}</BALAMT>
<DTASOF>${formatQBODateTime(now)}</DTASOF>
</LEDGERBAL>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
</OFX>
`;
    
    console.log(`✅ QBO 文件生成完成：${totalTransactions} 笔交易`);
    return qbo;
}







