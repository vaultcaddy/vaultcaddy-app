/**
 * VaultCaddy QuickBooks 整合模組
 * 處理 QuickBooks 數據格式轉換和導出
 */

class QuickBooksIntegration {
    constructor() {
        this.supportedFormats = ['qbo', 'iif', 'csv'];
        this.companySettings = {
            companyName: 'VaultCaddy Demo Company',
            baseCurrency: 'USD',
            fiscalYearStart: 'January',
            accountingMethod: 'Accrual'
        };
        
        this.accountMapping = {
            'bank-statement': {
                'checking': '1000', // 支票帳戶
                'savings': '1010',  // 儲蓄帳戶
                'credit-card': '2000' // 信用卡
            },
            'invoice': {
                'accounts-receivable': '1200', // 應收帳款
                'sales-income': '4000',        // 銷售收入
                'sales-tax': '2200'           // 銷售稅
            },
            'receipt': {
                'office-expense': '6000',     // 辦公費用
                'travel-expense': '6100',     // 差旅費
                'meals-expense': '6200'       // 餐飲費
            }
        };
        
        this.init();
    }
    
    init() {
        console.log('🔗 QuickBooks Integration 初始化...');
        this.loadCompanySettings();
        console.log('✅ QuickBooks Integration 初始化完成');
    }
    
    /**
     * 載入公司設定
     */
    loadCompanySettings() {
        try {
            const saved = localStorage.getItem('quickbooks_company_settings');
            if (saved) {
                this.companySettings = { ...this.companySettings, ...JSON.parse(saved) };
            }
        } catch (error) {
            console.error('載入 QuickBooks 設定失敗:', error);
        }
    }
    
    /**
     * 儲存公司設定
     */
    saveCompanySettings() {
        try {
            localStorage.setItem('quickbooks_company_settings', JSON.stringify(this.companySettings));
        } catch (error) {
            console.error('儲存 QuickBooks 設定失敗:', error);
        }
    }
    
    /**
     * 轉換銀行對帳單為 QBO 格式
     */
    convertBankStatementToQBO(data) {
        console.log('🏦 轉換銀行對帳單為 QuickBooks QBO 格式...');
        
        const header = this.generateQBOHeader();
        let transactions = '';
        
        data.forEach(result => {
            if (result.extractedData && result.extractedData.transactions) {
                result.extractedData.transactions.forEach(transaction => {
                    transactions += this.generateQBOBankTransaction(transaction, result.extractedData);
                });
            }
        });
        
        const footer = this.generateQBOFooter();
        
        return header + transactions + footer;
    }
    
    /**
     * 轉換發票為 IIF 格式
     */
    convertInvoiceToIIF(data) {
        console.log('📄 轉換發票為 QuickBooks IIF 格式...');
        
        let iifContent = this.generateIIFHeader();
        
        data.forEach(result => {
            if (result.extractedData) {
                iifContent += this.generateIIFInvoice(result.extractedData);
            }
        });
        
        return iifContent;
    }
    
    /**
     * 轉換收據為費用記錄
     */
    convertReceiptToExpense(data) {
        console.log('🧾 轉換收據為 QuickBooks 費用記錄...');
        
        let expenses = [];
        
        data.forEach(result => {
            if (result.extractedData) {
                expenses.push(this.generateExpenseRecord(result.extractedData));
            }
        });
        
        return expenses;
    }
    
    /**
     * 生成 QBO 檔案標頭
     */
    generateQBOHeader() {
        const now = new Date();
        const timestamp = now.toISOString().replace(/[-:]/g, '').split('.')[0];
        
        return `OFXHEADER:100
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
<CODE>0
<SEVERITY>INFO
</STATUS>
<DTSERVER>${timestamp}
<LANGUAGE>ENG
<FI>
<ORG>VaultCaddy
<FID>12345
</FI>
</SONRS>
</SIGNONMSGSRSV1>
<BANKMSGSRSV1>
<STMTTRNRS>
<TRNUID>1
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<STMTRS>
<CURDEF>${this.companySettings.baseCurrency}
<BANKACCTFROM>
<BANKID>123456789
<ACCTID>1234567890
<ACCTTYPE>CHECKING
</BANKACCTFROM>
<BANKTRANLIST>
<DTSTART>${timestamp}
<DTEND>${timestamp}
`;
    }
    
    /**
     * 生成 QBO 銀行交易
     */
    generateQBOBankTransaction(transaction, accountData) {
        const date = transaction.date.replace(/-/g, '');
        const amount = parseFloat(transaction.amount);
        const transactionType = amount >= 0 ? 'CREDIT' : 'DEBIT';
        const fitid = `${transaction.date}_${Math.random().toString(36).substr(2, 9)}`;
        
        return `<STMTTRN>
<TRNTYPE>${transactionType}
<DTPOSTED>${date}
<TRNAMT>${Math.abs(amount).toFixed(2)}
<FITID>${fitid}
<NAME>${this.escapeXML(transaction.description || 'Transaction')}
<MEMO>${this.escapeXML(transaction.description || '')}
</STMTTRN>
`;
    }
    
    /**
     * 生成 QBO 檔案結尾
     */
    generateQBOFooter() {
        const now = new Date();
        const timestamp = now.toISOString().replace(/[-:]/g, '').split('.')[0];
        
        return `</BANKTRANLIST>
<LEDGERBAL>
<BALAMT>0.00
<DTASOF>${timestamp}
</LEDGERBAL>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
</OFX>`;
    }
    
    /**
     * 生成 IIF 檔案標頭
     */
    generateIIFHeader() {
        return `!HDR	PROD	VER	REL	IIFVER	DATE	TIME	ACCNT
!HDR	VaultCaddy	2025	1	1	${new Date().toLocaleDateString()}	${new Date().toLocaleTimeString()}	N
!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	TOPRINT	NAMEADDR	ADDR1	ADDR2	ADDR3	ADDR4	ADDR5	DUEDATE	TERMS	PAID	SHIPDATE
!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	CLASS	AMOUNT	DOCNUM	MEMO	CLEAR	QNTY	PRICE	INVITEM	PAYMETH	TAXABLE	VALADJ	SERVICEDATE
!ENDTRNS
`;
    }
    
    /**
     * 生成 IIF 發票記錄
     */
    generateIIFInvoice(invoiceData) {
        const date = this.formatDateForIIF(invoiceData.date);
        const invoiceNumber = invoiceData.invoiceNumber || '';
        const vendor = this.escapeIIF(invoiceData.vendor || 'Unknown Vendor');
        const total = parseFloat(invoiceData.totalAmount || 0);
        
        let iifLines = '';
        
        // 主要交易行（應收帳款）
        iifLines += `TRNS		INVOICE	${date}	Accounts Receivable	${vendor}		${total.toFixed(2)}	${invoiceNumber}			N		\n`;
        
        // 銷售行項目
        if (invoiceData.lineItems && invoiceData.lineItems.length > 0) {
            invoiceData.lineItems.forEach(item => {
                const itemTotal = parseFloat(item.totalPrice || 0);
                const description = this.escapeIIF(item.description || '');
                
                iifLines += `SPL		INVOICE	${date}	Sales	${vendor}		${(-itemTotal).toFixed(2)}	${invoiceNumber}	${description}	N	${item.quantity || 1}	${item.unitPrice || 0}		N	Y		\n`;
            });
        } else {
            // 如果沒有行項目，創建一個通用銷售項目
            iifLines += `SPL		INVOICE	${date}	Sales	${vendor}		${(-total).toFixed(2)}	${invoiceNumber}	Sales Income	N	1	${total.toFixed(2)}		N	Y		\n`;
        }
        
        iifLines += `ENDTRNS\n`;
        
        return iifLines;
    }
    
    /**
     * 生成費用記錄
     */
    generateExpenseRecord(receiptData) {
        return {
            date: receiptData.date || new Date().toISOString().split('T')[0],
            merchant: receiptData.merchant || 'Unknown Merchant',
            amount: parseFloat(receiptData.totalAmount || 0),
            category: this.categorizeExpense(receiptData),
            account: this.mapExpenseAccount(receiptData),
            items: receiptData.items || [],
            taxAmount: parseFloat(receiptData.taxAmount || 0),
            memo: `Receipt from ${receiptData.merchant || 'Unknown'}`
        };
    }
    
    /**
     * 費用分類
     */
    categorizeExpense(receiptData) {
        const merchant = (receiptData.merchant || '').toLowerCase();
        
        if (merchant.includes('restaurant') || merchant.includes('cafe') || merchant.includes('food')) {
            return 'Meals & Entertainment';
        } else if (merchant.includes('gas') || merchant.includes('fuel') || merchant.includes('shell')) {
            return 'Travel Expense';
        } else if (merchant.includes('office') || merchant.includes('supply') || merchant.includes('staples')) {
            return 'Office Expense';
        } else {
            return 'General Expense';
        }
    }
    
    /**
     * 映射費用科目
     */
    mapExpenseAccount(receiptData) {
        const category = this.categorizeExpense(receiptData);
        
        switch (category) {
            case 'Meals & Entertainment':
                return this.accountMapping['receipt']['meals-expense'];
            case 'Travel Expense':
                return this.accountMapping['receipt']['travel-expense'];
            case 'Office Expense':
                return this.accountMapping['receipt']['office-expense'];
            default:
                return this.accountMapping['receipt']['office-expense'];
        }
    }
    
    /**
     * 格式化日期為 IIF 格式
     */
    formatDateForIIF(dateString) {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return new Date().toLocaleDateString('en-US');
        }
        return date.toLocaleDateString('en-US');
    }
    
    /**
     * 轉義 XML 特殊字符
     */
    escapeXML(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&apos;');
    }
    
    /**
     * 轉義 IIF 特殊字符
     */
    escapeIIF(text) {
        if (!text) return '';
        return text.replace(/\t/g, ' ').replace(/\n/g, ' ').replace(/\r/g, ' ');
    }
    
    /**
     * 驗證 QuickBooks 數據
     */
    validateQuickBooksData(data, format) {
        const validations = [];
        
        switch (format) {
            case 'qbo':
                validations.push(...this.validateQBOData(data));
                break;
            case 'iif':
                validations.push(...this.validateIIFData(data));
                break;
            case 'csv':
                validations.push(...this.validateCSVData(data));
                break;
        }
        
        return {
            isValid: validations.every(v => v.isValid),
            validations
        };
    }
    
    /**
     * 驗證 QBO 數據
     */
    validateQBOData(data) {
        const validations = [];
        
        data.forEach(result => {
            if (result.extractedData && result.extractedData.transactions) {
                result.extractedData.transactions.forEach((transaction, index) => {
                    // 檢查必要欄位
                    validations.push({
                        field: `transaction_${index}_date`,
                        isValid: !!transaction.date && !isNaN(Date.parse(transaction.date)),
                        message: transaction.date ? '日期格式正確' : '無效或缺少交易日期'
                    });
                    
                    validations.push({
                        field: `transaction_${index}_amount`,
                        isValid: transaction.amount !== undefined && !isNaN(parseFloat(transaction.amount)),
                        message: !isNaN(parseFloat(transaction.amount)) ? '金額格式正確' : '無效或缺少交易金額'
                    });
                });
            }
        });
        
        return validations;
    }
    
    /**
     * 驗證 IIF 數據
     */
    validateIIFData(data) {
        const validations = [];
        
        data.forEach(result => {
            if (result.extractedData) {
                const invoice = result.extractedData;
                
                validations.push({
                    field: 'invoice_number',
                    isValid: !!invoice.invoiceNumber,
                    message: invoice.invoiceNumber ? '發票號碼已識別' : '缺少發票號碼'
                });
                
                validations.push({
                    field: 'vendor_name',
                    isValid: !!invoice.vendor,
                    message: invoice.vendor ? '供應商已識別' : '缺少供應商信息'
                });
                
                validations.push({
                    field: 'total_amount',
                    isValid: !!invoice.totalAmount && !isNaN(parseFloat(invoice.totalAmount)),
                    message: !isNaN(parseFloat(invoice.totalAmount)) ? '總金額正確' : '無效或缺少總金額'
                });
            }
        });
        
        return validations;
    }
    
    /**
     * 驗證 CSV 數據
     */
    validateCSVData(data) {
        const validations = [];
        
        validations.push({
            field: 'data_format',
            isValid: Array.isArray(data) && data.length > 0,
            message: data.length > 0 ? `${data.length} 筆記錄準備導出` : '沒有可導出的數據'
        });
        
        return validations;
    }
    
    /**
     * 生成 QuickBooks 報告
     */
    generateQuickBooksReport(data, documentType) {
        const report = {
            generated: new Date().toISOString(),
            documentType,
            totalRecords: data.length,
            summary: {},
            recommendations: []
        };
        
        switch (documentType) {
            case 'bank-statement':
                report.summary = this.generateBankStatementSummary(data);
                break;
            case 'invoice':
                report.summary = this.generateInvoiceSummary(data);
                break;
            case 'receipt':
                report.summary = this.generateReceiptSummary(data);
                break;
        }
        
        report.recommendations = this.generateRecommendations(data, documentType);
        
        return report;
    }
    
    /**
     * 生成銀行對帳單摘要
     */
    generateBankStatementSummary(data) {
        let totalTransactions = 0;
        let totalDebit = 0;
        let totalCredit = 0;
        
        data.forEach(result => {
            if (result.extractedData && result.extractedData.transactions) {
                totalTransactions += result.extractedData.transactions.length;
                
                result.extractedData.transactions.forEach(transaction => {
                    const amount = parseFloat(transaction.amount || 0);
                    if (amount >= 0) {
                        totalCredit += amount;
                    } else {
                        totalDebit += Math.abs(amount);
                    }
                });
            }
        });
        
        return {
            totalTransactions,
            totalDebit: totalDebit.toFixed(2),
            totalCredit: totalCredit.toFixed(2),
            netAmount: (totalCredit - totalDebit).toFixed(2)
        };
    }
    
    /**
     * 生成發票摘要
     */
    generateInvoiceSummary(data) {
        let totalInvoices = data.length;
        let totalAmount = 0;
        let totalTax = 0;
        
        data.forEach(result => {
            if (result.extractedData) {
                totalAmount += parseFloat(result.extractedData.totalAmount || 0);
                totalTax += parseFloat(result.extractedData.taxAmount || 0);
            }
        });
        
        return {
            totalInvoices,
            totalAmount: totalAmount.toFixed(2),
            totalTax: totalTax.toFixed(2),
            averageInvoice: (totalAmount / totalInvoices).toFixed(2)
        };
    }
    
    /**
     * 生成收據摘要
     */
    generateReceiptSummary(data) {
        let totalReceipts = data.length;
        let totalAmount = 0;
        const categories = {};
        
        data.forEach(result => {
            if (result.extractedData) {
                totalAmount += parseFloat(result.extractedData.totalAmount || 0);
                
                const category = this.categorizeExpense(result.extractedData);
                categories[category] = (categories[category] || 0) + parseFloat(result.extractedData.totalAmount || 0);
            }
        });
        
        return {
            totalReceipts,
            totalAmount: totalAmount.toFixed(2),
            averageReceipt: (totalAmount / totalReceipts).toFixed(2),
            categories
        };
    }
    
    /**
     * 生成建議
     */
    generateRecommendations(data, documentType) {
        const recommendations = [];
        
        // 通用建議
        recommendations.push({
            type: 'data-review',
            message: '導入 QuickBooks 前請仔細檢查所有數據的準確性',
            priority: 'high'
        });
        
        // 特定文檔類型建議
        switch (documentType) {
            case 'bank-statement':
                recommendations.push({
                    type: 'reconciliation',
                    message: '建議先完成銀行對帳再導入交易記錄',
                    priority: 'medium'
                });
                break;
                
            case 'invoice':
                recommendations.push({
                    type: 'customer-setup',
                    message: '確保所有客戶資料在 QuickBooks 中已正確設置',
                    priority: 'medium'
                });
                break;
                
            case 'receipt':
                recommendations.push({
                    type: 'expense-categories',
                    message: '檢查費用分類是否符合您的會計需求',
                    priority: 'low'
                });
                break;
        }
        
        return recommendations;
    }
    
    /**
     * 更新公司設定
     */
    updateCompanySettings(newSettings) {
        this.companySettings = { ...this.companySettings, ...newSettings };
        this.saveCompanySettings();
        
        console.log('📊 QuickBooks 公司設定已更新');
    }
    
    /**
     * 獲取支援的格式
     */
    getSupportedFormats() {
        return this.supportedFormats;
    }
    
    /**
     * 獲取帳戶映射
     */
    getAccountMapping() {
        return this.accountMapping;
    }
}

// 全局實例
window.QuickBooksIntegration = new QuickBooksIntegration();

// 導出給其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuickBooksIntegration;
}
