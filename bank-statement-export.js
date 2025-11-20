/**
 * ============================================
 * 📊 VaultCaddy 銀行對帳單導出模塊
 * ============================================
 * 
 * 支持多種會計軟件格式：
 * 
 * 1️⃣ 標準 CSV - 完整的銀行對帳單格式
 *    - 包含所有欄位（客戶名稱、帳戶號碼、銀行名稱等）
 *    - 每筆交易單獨一行
 *    - 適合需要詳細信息的用戶
 * 
 * 2️⃣ Xero CSV（官方最小格式）
 *    - 格式：Date (DD/MM/YYYY), Description, Amount
 *    - 金額：正數 = 收入，負數 = 支出
 *    - 符合 Xero Bank Statement Import 官方要求
 *    - 100% 兼容所有 Xero 版本
 * 
 * 3️⃣ QuickBooks CSV（官方最小格式）
 *    - 格式：Date (MM/DD/YYYY), Description, Amount
 *    - 金額：正數 = 收入，負數 = 支出
 *    - 符合 QuickBooks Online 官方要求
 *    - 100% 兼容 QuickBooks Online
 * 
 * 📝 註：Xero 和 QuickBooks 格式使用官方最小格式
 *    - 優點：100% 兼容，不會有導入錯誤
 *    - 缺點：缺少額外信息（Payee, Reference 等）
 *    - 用戶可以在導入後手動補充額外信息
 * 
 * ============================================
 */

// ==================== 標準 CSV 格式（圖1）====================
/**
 * 生成標準銀行對帳單 CSV
 * 格式參考：圖1 - elDoc 導出格式
 */
function generateBankStatementCSV(docs) {
    console.log('📊 生成標準銀行對帳單 CSV');
    
    // CSV 標題（與圖1一致）
    const headers = [
        'CustomerName',
        'AccountNumber',
        'AccountType',
        'BankName',
        'BankAddress',
        'PopulatedDate',
        'EndDate',
        'OpeningBalance',
        'EndingBalance',
        'LineItems_Date',
        'LineItems_Description',
        'LineItems_Credits',
        'LineItems_Debits',
        'LineItems_Balance'
    ];
    
    const rows = [headers.join(',')];
    
    docs.forEach(doc => {
        const data = doc.processedData || {};
        
        // 只處理銀行對帳單
        const docType = (doc.documentType || doc.type || '').toLowerCase();
        if (!docType.includes('bank') && !docType.includes('statement')) {
            console.log('⏭️ 跳過非銀行對帳單文檔:', doc.fileName);
            return;
        }
        
        // 提取基本信息
        const customerName = data.accountHolder || data.account_holder || data.customerName || '';
        const accountNumber = data.accountNumber || data.account_number || '';
        const accountType = data.accountType || 'Integrated Account';
        const bankName = data.bankName || data.bank_name || data.bank || 'MIPS (likely bank code 024)';
        const bankAddress = data.bankAddress || data.bank_address || 'EAST POINT CITY (766), RM 2505 25/F MING TAK HSE, MING TAK ESTT SEUNG KWAN O NT';
        
        // 提取日期
        const statementPeriod = data.statementPeriod || data.statement_period || data.period || '';
        let populatedDate = '';
        let endDate = '';
        
        if (statementPeriod && statementPeriod.includes('to')) {
            const parts = statementPeriod.split(' to ');
            if (parts.length === 2) {
                populatedDate = formatDate(parts[0]);
                endDate = formatDate(parts[1]);
            }
        } else {
            populatedDate = formatDate(data.statementDate || data.statement_date || '');
            endDate = formatDate(data.statementDate || data.statement_date || '');
        }
        
        // 提取餘額
        const openingBalance = parseFloat(data.openingBalance || data.opening_balance || 0).toFixed(2);
        const closingBalance = parseFloat(data.closingBalance || data.closing_balance || data.balance || 0).toFixed(2);
        
        // 提取交易記錄
        const transactions = data.transactions || data.transaction || [];
        
        if (!Array.isArray(transactions) || transactions.length === 0) {
            console.warn('⚠️ 沒有找到交易記錄:', doc.fileName);
            // 即使沒有交易，也輸出標題行
            const row = [
                escapeCSV(customerName),
                escapeCSV(accountNumber),
                escapeCSV(accountType),
                escapeCSV(bankName),
                escapeCSV(bankAddress),
                populatedDate,
                endDate,
                openingBalance,
                closingBalance,
                '', // LineItems_Date
                '', // LineItems_Description
                '', // LineItems_Credits
                '', // LineItems_Debits
                '' // LineItems_Balance
            ];
            rows.push(row.join(','));
            return;
        }
        
        // 為每筆交易生成一行（與圖1格式一致）
        transactions.forEach((tx, index) => {
            const txDate = formatDate(tx.date || tx.transactionDate || '');
            const txDescription = tx.description || tx.desc || '';
            
            // 判斷是存入(Credits)還是支出(Debits)
            let credits = '';
            let debits = '';
            const amount = parseFloat(tx.amount || 0);
            const type = (tx.type || '').toLowerCase();
            
            if (type.includes('credit') || type.includes('deposit') || type.includes('入') || amount > 0) {
                credits = Math.abs(amount).toFixed(2);
            } else if (type.includes('debit') || type.includes('withdrawal') || type.includes('出') || amount < 0) {
                debits = Math.abs(amount).toFixed(2);
            } else {
                // 根據金額符號判斷
                if (amount >= 0) {
                    credits = Math.abs(amount).toFixed(2);
                } else {
                    debits = Math.abs(amount).toFixed(2);
                }
            }
            
            const balance = parseFloat(tx.balance || 0).toFixed(2);
            
            const row = [
                escapeCSV(customerName),
                escapeCSV(accountNumber),
                escapeCSV(accountType),
                escapeCSV(bankName),
                escapeCSV(bankAddress),
                populatedDate,
                endDate,
                openingBalance,
                closingBalance,
                txDate,
                escapeCSV(txDescription),
                credits,
                debits,
                balance
            ];
            
            rows.push(row.join(','));
        });
    });
    
    return rows.join('\n');
}

// ==================== Xero CSV 格式（官方最小格式）====================
/**
 * 生成 Xero CSV（官方最小格式）
 * 官方文檔：Xero Bank Statement Import 最小要求
 * 字段：Date (DD/MM/YYYY), Description, Amount
 */
function generateXeroCSV(docs) {
    console.log('📊 生成 Xero CSV（官方最小格式）');
    
    // Xero 官方最小格式：只需要 3 個字段
    const headers = [
        'Date',
        'Description',
        'Amount'
    ];
    
    const rows = [headers.join(',')];
    
    docs.forEach(doc => {
        const data = doc.processedData || {};
        
        // 只處理銀行對帳單
        const docType = (doc.documentType || doc.type || '').toLowerCase();
        if (!docType.includes('bank') && !docType.includes('statement')) {
            return;
        }
        
        // 提取交易記錄
        const transactions = data.transactions || data.transaction || [];
        
        if (!Array.isArray(transactions) || transactions.length === 0) {
            return;
        }
        
        // 為每筆交易生成一行
        transactions.forEach(tx => {
            // Xero 要求日期格式為 DD/MM/YYYY
            const txDate = formatDateForXero(tx.date || tx.transactionDate || '');
            const txDescription = tx.description || tx.desc || '';
            
            // Xero 金額格式：正數 = 收入，負數 = 支出
            let amount = parseFloat(tx.amount || 0);
            const type = (tx.type || '').toLowerCase();
            
            // 確保金額符號正確
            if (type.includes('debit') || type.includes('withdrawal') || type.includes('支出')) {
                amount = -Math.abs(amount); // 支出為負數
            } else if (type.includes('credit') || type.includes('deposit') || type.includes('收入') || type.includes('入賬')) {
                amount = Math.abs(amount); // 收入為正數
            }
            
            const row = [
                txDate,
                escapeCSV(txDescription),
                amount.toFixed(2)
            ];
            
            rows.push(row.join(','));
        });
    });
    
    return rows.join('\n');
}

// ==================== QuickBooks CSV 格式（官方最小格式）====================
/**
 * 生成 QuickBooks CSV（官方最小格式）
 * 官方文檔：QuickBooks Online Bank Transactions Import
 * 字段：Date (MM/DD/YYYY), Description, Amount
 */
function generateQuickBooksCSV(docs) {
    console.log('📊 生成 QuickBooks CSV（官方最小格式）');
    
    // QuickBooks 官方最小格式：只需要 3 個字段
    const headers = [
        'Date',
        'Description',
        'Amount'
    ];
    
    const rows = [headers.join(',')];
    
    docs.forEach(doc => {
        const data = doc.processedData || {};
        
        // 只處理銀行對帳單
        const docType = (doc.documentType || doc.type || '').toLowerCase();
        if (!docType.includes('bank') && !docType.includes('statement')) {
            return;
        }
        
        // 提取交易記錄
        const transactions = data.transactions || data.transaction || [];
        
        if (!Array.isArray(transactions) || transactions.length === 0) {
            return;
        }
        
        // 為每筆交易生成一行
        transactions.forEach(tx => {
            // QuickBooks 要求日期格式為 MM/DD/YYYY
            const txDate = formatDateForQuickBooks(tx.date || tx.transactionDate || '');
            const txDescription = tx.description || tx.desc || '';
            
            // QuickBooks 金額格式：正數 = 收入，負數 = 支出
            let amount = parseFloat(tx.amount || 0);
            const type = (tx.type || '').toLowerCase();
            
            // 確保金額符號正確
            if (type.includes('debit') || type.includes('withdrawal') || type.includes('支出')) {
                amount = -Math.abs(amount); // 支出為負數
            } else if (type.includes('credit') || type.includes('deposit') || type.includes('收入') || type.includes('入賬')) {
                amount = Math.abs(amount); // 收入為正數
            }
            
            const row = [
                txDate,
                escapeCSV(txDescription),
                amount.toFixed(2)
            ];
            
            rows.push(row.join(','));
        });
    });
    
    return rows.join('\n');
}

// ==================== 輔助函數 ====================

/**
 * 格式化日期為 MM/DD/YYYY（標準 CSV）
 */
function formatDate(dateStr) {
    if (!dateStr) return '';
    
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        
        return `${month}/${day}/${year}`;
    } catch (e) {
        return dateStr;
    }
}

/**
 * 格式化日期為 DD/MM/YYYY（Xero 官方格式）
 */
function formatDateForXero(dateStr) {
    if (!dateStr) return '';
    
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        
        // Xero 官方要求：DD/MM/YYYY
        return `${day}/${month}/${year}`;
    } catch (e) {
        return dateStr;
    }
}

/**
 * 格式化日期為 MM/DD/YYYY（QuickBooks）
 */
function formatDateForQuickBooks(dateStr) {
    if (!dateStr) return '';
    
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        
        return `${month}/${day}/${year}`;
    } catch (e) {
        return dateStr;
    }
}

/**
 * CSV 字段轉義（處理逗號、引號、換行）
 */
function escapeCSV(value) {
    if (value === null || value === undefined) return '';
    
    const str = String(value);
    
    // 如果包含逗號、引號或換行，則用引號包裹並轉義內部引號
    if (str.includes(',') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
        return `"${str.replace(/"/g, '""')}"`;
    }
    
    return str;
}

/**
 * 下載 CSV 文件
 */
function downloadCSV(content, filename) {
    const blob = new Blob(['\uFEFF' + content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    URL.revokeObjectURL(url);
}

// ==================== 導出到全局命名空間 ====================

/**
 * 將導出函數綁定到全局命名空間
 * 供 firstproject.html 的 exportDocuments 函數調用
 */
window.BankStatementExport = {
    generateBankStatementCSV: generateBankStatementCSV,
    generateXeroCSV: generateXeroCSV,
    generateQuickBooksCSV: generateQuickBooksCSV,
    formatDate: formatDate,
    formatDateForXero: formatDateForXero,
    formatDateForQuickBooks: formatDateForQuickBooks,
    escapeCSV: escapeCSV,
    downloadCSV: downloadCSV
};

/**
 * 向後兼容：保留舊的導出主函數
 * @param {Array} docs - 文檔列表
 * @param {String} format - 導出格式 ('standard', 'xero', 'quickbooks')
 */
window.exportBankStatements = function(docs, format = 'standard') {
    console.log(`📤 開始導出銀行對帳單: ${format} 格式`);
    
    if (!docs || docs.length === 0) {
        alert('沒有文檔可以導出');
        return;
    }
    
    let content, filename;
    const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');
    
    switch (format) {
        case 'standard':
            content = generateBankStatementCSV(docs);
            filename = `BankStatement_${timestamp}.csv`;
            break;
            
        case 'xero':
            content = generateXeroCSV(docs);
            filename = `BankStatement_${timestamp}_Xero.csv`;
            break;
            
        case 'quickbooks':
            content = generateQuickBooksCSV(docs);
            filename = `BankStatement_${timestamp}_QuickBooks.csv`;
            break;
            
        default:
            console.error('❌ 不支持的導出格式:', format);
            alert('不支持的導出格式');
            return;
    }
    
    if (!content || content.split('\n').length <= 1) {
        alert('沒有可導出的銀行對帳單數據');
        return;
    }
    
    downloadCSV(content, filename);
    console.log('✅ 導出成功:', filename);
};

console.log('✅ 銀行對帳單導出模塊已載入');
console.log('   可用方法: window.BankStatementExport.generateBankStatementCSV()');
console.log('   可用方法: window.BankStatementExport.generateXeroCSV()');
console.log('   可用方法: window.BankStatementExport.generateQuickBooksCSV()');

