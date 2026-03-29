/**
 * VaultCaddy 導出管理器
 * 
 * 作用：
 * 1. 將 AI 提取的發票和銀行對帳單數據導出為會計軟件支持的格式
 * 2. 支持 QuickBooks、Xero、FreshBooks 等主流會計軟件
 * 3. 確保數據格式符合會計準則和軟件要求
 * 
 * 支持導出格式:
 * 1. CSV - 通用格式，所有會計軟件都支持
 * 2. IIF - QuickBooks Desktop 格式
 * 3. QBO - QuickBooks Online 格式
 * 4. Xero CSV - Xero 專用格式
 * 
 * @version 2.0.0
 * @updated 2025-10-22
 */

class ExportManager {
    constructor() {
        this.version = '2.0.0';
        this.supportedFormats = ['csv', 'iif', 'qbo', 'json', 'quickbooks'];
    }
    
    /**
     * 導出發票數據
     * 
     * @param {Array} invoices - 發票列表
     * @param {String} format - 導出格式 (csv, iif, qbo, excel)
     * @param {Object} options - 導出選項
     * @returns {Blob} 導出文件
     */
    async exportInvoices(invoices, format = 'csv', options = {}) {
        console.log('📤 開始導出發票...');
        console.log(`   格式: ${format}`);
        console.log(`   數量: ${invoices.length}`);
        
        if (!this.supportedFormats.includes(format)) {
            throw new Error(`不支持的導出格式: ${format}`);
        }
        
        switch (format) {
            case 'csv':
                return this.exportToCSV(invoices, options);
            case 'iif':
                return this.exportToIIF(invoices, options);
            case 'qbo':
            case 'quickbooks':
                return this.exportToQBO(invoices, options);
            case 'json':
                return this.exportToJSON(invoices, options);
            default:
                throw new Error(`未實現的導出格式: ${format}`);
        }
    }
    
    /**
     * 導出為 CSV 格式
     * 
     * CSV 格式優勢:
     * - 所有會計軟件都支持
     * - 可以用 Excel 打開編輯
     * - 簡單易懂
     */
    exportToCSV(invoices, options = {}) {
        console.log('📊 導出為 CSV 格式...');
        
        const includeLineItems = options.includeLineItems !== false;
        
        if (includeLineItems) {
            // 詳細格式：每個商品項目一行
            return this.exportToCSVDetailed(invoices);
        } else {
            // 摘要格式：每張發票一行
            return this.exportToCSVSummary(invoices);
        }
    }
    
    /**
     * CSV 摘要格式（每張發票一行）
     * 
     * 匹配優化後的發票數據格式（gemini-worker-client.js）
     */
    exportToCSVSummary(invoices) {
        const headers = [
            '收據日期',
            '商戶名稱',
            '開支類別',
            '購買項目簡述',
            '總金額',
            '貨幣',
            'IRD 扣稅可能性',
            '扣稅原因說明',
            '發票編號',
            '客戶名稱',
            '備註'
        ];
        
        const rows = invoices.map(invoice => {
            const data = invoice.processedData || invoice;
            const taxInfo = data.tax_deductibility || {};
            
            return [
                this.escapeCSV(data.date || data.invoice_number || ''),
                this.escapeCSV(data.merchant_name || data.supplier?.name || ''),
                this.escapeCSV(data.expense_category || ''),
                this.escapeCSV(data.items_summary || ''),
                data.total_amount || data.total || 0,
                this.escapeCSV(data.currency || 'HKD'),
                this.escapeCSV(taxInfo.level || ''),
                this.escapeCSV(taxInfo.reason || ''),
                this.escapeCSV(data.invoice_number || ''),
                this.escapeCSV(data.customerName || data.customer?.name || ''),
                this.escapeCSV(data.notes || '')
            ].join(',');
        });
        
        const csv = [headers.join(','), ...rows].join('\n');
        
        // 添加 BOM 以支持 Excel 正確顯示中文
        const bom = '\uFEFF';
        const blob = new Blob([bom + csv], { type: 'text/csv;charset=utf-8;' });
        
        console.log('✅ CSV 摘要格式導出完成');
        console.log(`   導出 ${invoices.length} 張發票`);
        return blob;
    }
    
    /**
     * CSV 詳細格式（每個商品項目一行）
     * 
     * 匹配優化後的發票數據格式（gemini-worker-client.js）
     */
    exportToCSVDetailed(invoices) {
        const headers = [
            'Invoice Number',
            'Invoice Date',
            'Supplier Name',
            'Customer Name',
            'Item Code',
            'Item Description',
            'Quantity',
            'Unit',
            'Unit Price',
            'Item Amount',
            'Invoice Subtotal',
            'Invoice Discount',
            'Invoice Tax',
            'Invoice Total',
            'Currency',
            'Payment Method'
        ];
        
        const rows = [];
        
        for (const invoice of invoices) {
            const data = invoice.processedData || invoice;
            const supplier = data.supplier || {};
            const customer = data.customer || {};
            const items = data.items || [];
            
            if (items.length === 0) {
                // 如果沒有商品項目，至少輸出一行發票信息
                rows.push([
                    this.escapeCSV(data.invoice_number || ''),
                    this.escapeCSV(data.date || ''),
                    this.escapeCSV(supplier.name || ''),
                    this.escapeCSV(customer.name || ''),
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    data.subtotal || 0,
                    data.discount || 0,
                    data.tax || 0,
                    data.total || 0,
                    this.escapeCSV(data.currency || 'HKD'),
                    this.escapeCSV(data.payment_method || '')
                ].join(','));
            } else {
                // 每個商品項目一行
                for (const item of items) {
                    rows.push([
                        this.escapeCSV(data.invoice_number || ''),
                        this.escapeCSV(data.date || ''),
                        this.escapeCSV(supplier.name || ''),
                        this.escapeCSV(customer.name || ''),
                        this.escapeCSV(item.code || ''),
                        this.escapeCSV(item.description || ''),
                        item.quantity || 0,
                        this.escapeCSV(item.unit || ''),
                        item.unit_price || 0,
                        item.amount || 0,
                        data.subtotal || 0,
                        data.discount || 0,
                        data.tax || 0,
                        data.total || 0,
                        this.escapeCSV(data.currency || 'HKD'),
                        this.escapeCSV(data.payment_method || '')
                    ].join(','));
                }
            }
        }
        
        const csv = [headers.join(','), ...rows].join('\n');
        
        // 添加 BOM 以支持 Excel 正確顯示中文
        const bom = '\uFEFF';
        const blob = new Blob([bom + csv], { type: 'text/csv;charset=utf-8;' });
        
        console.log('✅ CSV 詳細格式導出完成');
        console.log(`   導出 ${rows.length} 行商品項目`);
        return blob;
    }
    
    /**
     * 導出為 IIF 格式（QuickBooks Desktop）
     * 
     * IIF (Intuit Interchange Format) 是 QuickBooks Desktop 的導入格式
     */
    exportToIIF(invoices, options = {}) {
        console.log('📊 導出為 IIF 格式 (QuickBooks Desktop)...');
        
        const lines = [];
        
        // IIF 文件頭
        lines.push('!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO');
        lines.push('!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tCLASS\tAMOUNT\tDOCNUM\tMEMO');
        lines.push('!ENDTRNS');
        
        // 為每張發票生成 IIF 記錄
        for (const invoice of invoices) {
            const data = invoice.processedData || {};
            
            // 交易行（應收賬款）
            lines.push([
                'TRNS',
                '',  // TRNSID (自動生成)
                'INVOICE',
                this.formatIIFDate(data.issueDate),
                'Accounts Receivable',  // 應收賬款科目
                this.escapeIIF(data.customer?.name || 'Unknown Customer'),
                '',  // CLASS
                data.totalAmount || 0,
                this.escapeIIF(data.invoiceNumber || ''),
                this.escapeIIF(data.notes || '')
            ].join('\t'));
            
            // 商品項目行
            const lineItems = data.lineItems || [];
            if (lineItems.length > 0) {
                for (const item of lineItems) {
                    lines.push([
                        'SPL',
                        '',  // SPLID (自動生成)
                        'INVOICE',
                        this.formatIIFDate(data.issueDate),
                        'Sales',  // 銷售收入科目
                        this.escapeIIF(data.customer?.name || 'Unknown Customer'),
                        '',  // CLASS
                        -(item.amount || 0),  // 負數表示收入
                        this.escapeIIF(data.invoiceNumber || ''),
                        this.escapeIIF(item.description || '')
                    ].join('\t'));
                }
            } else {
                // 如果沒有商品項目，創建一個總額行
                lines.push([
                    'SPL',
                    '',
                    'INVOICE',
                    this.formatIIFDate(data.issueDate),
                    'Sales',
                    this.escapeIIF(data.customer?.name || 'Unknown Customer'),
                    '',
                    -(data.subtotal || data.totalAmount || 0),
                    this.escapeIIF(data.invoiceNumber || ''),
                    'Invoice Total'
                ].join('\t'));
            }
            
            // 稅金行（如果有）
            if (data.taxAmount && data.taxAmount > 0) {
                lines.push([
                    'SPL',
                    '',
                    'INVOICE',
                    this.formatIIFDate(data.issueDate),
                    'Sales Tax Payable',  // 應付銷售稅科目
                    this.escapeIIF(data.customer?.name || 'Unknown Customer'),
                    '',
                    -(data.taxAmount),
                    this.escapeIIF(data.invoiceNumber || ''),
                    'Sales Tax'
                ].join('\t'));
            }
            
            lines.push('ENDTRNS');
        }
        
        const iif = lines.join('\n');
        const blob = new Blob([iif], { type: 'text/plain;charset=utf-8;' });
        
        console.log('✅ IIF 格式導出完成');
        return blob;
    }
    
    /**
     * 導出為 QBO 格式（QuickBooks Online）
     * 
     * QBO 格式實際上是 QFX 格式的變體，基於 OFX (Open Financial Exchange)
     * 這裡我們生成簡化的 QBO 格式
     */
    exportToQBO(invoices, options = {}) {
        console.log('📊 導出為 QBO 格式 (QuickBooks Online)...');
        
        // QBO 文件頭
        const header = `OFXHEADER:100
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
<DTSERVER>${this.formatQBODateTime(new Date())}
<LANGUAGE>ENG
</SONRS>
</SIGNONMSGSRSV1>
<INVSTMTMSGSRSV1>
<INVSTMTTRNRS>
<TRNUID>1
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<INVSTMTRS>
<DTASOF>${this.formatQBODateTime(new Date())}
<CURDEF>HKD
<INVACCTFROM>
<BROKERID>vaultcaddy.com
<ACCTID>INVOICES
</INVACCTFROM>
<INVTRANLIST>
<DTSTART>${this.formatQBODateTime(new Date())}
<DTEND>${this.formatQBODateTime(new Date())}
`;
        
        // 為每張發票生成交易記錄
        const transactions = invoices.map(invoice => {
            const data = invoice.processedData || {};
            return `<INVBANKTRAN>
<STMTTRN>
<TRNTYPE>CREDIT
<DTPOSTED>${this.formatQBODate(data.issueDate)}
<TRNAMT>${data.totalAmount || 0}
<FITID>${data.invoiceNumber || invoice.id}
<NAME>${this.escapeXML(data.customer?.name || 'Unknown Customer')}
<MEMO>${this.escapeXML(data.notes || 'Invoice ' + (data.invoiceNumber || ''))}
</STMTTRN>
<SUBACCTFUND>OTHER
</INVBANKTRAN>`;
        }).join('\n');
        
        // QBO 文件尾
        const footer = `</INVTRANLIST>
</INVSTMTRS>
</INVSTMTTRNRS>
</INVSTMTMSGSRSV1>
</OFX>`;
        
        const qbo = header + transactions + footer;
        const blob = new Blob([qbo], { type: 'application/x-qbo;charset=utf-8;' });
        
        console.log('✅ QBO 格式導出完成');
        return blob;
    }
    
    /**
     * 導出銀行對帳單
     */
    async exportBankStatements(statements, format = 'csv', options = {}) {
        console.log('📤 開始導出銀行對帳單...');
        console.log(`   格式: ${format}`);
        console.log(`   數量: ${statements.length}`);
        
        switch (format) {
            case 'csv':
                return this.exportBankStatementsToCSV(statements, options);
            case 'qbo':
                return this.exportBankStatementsToQBO(statements, options);
            default:
                throw new Error(`銀行對帳單不支持 ${format} 格式`);
        }
    }
    
    /**
     * 銀行對帳單導出為 CSV
     * 
     * 匹配優化後的銀行對帳單數據格式（gemini-worker-client.js）
     */
    exportBankStatementsToCSV(statements, options = {}) {
        const headers = [
            'Date',
            'Type',
            'Description',
            'Deposit',
            'Withdrawal',
            'Balance',
            'Bank Name',
            'Account Number',
            'Account Holder'
        ];
        
        const rows = [];
        
        for (const statement of statements) {
            const data = statement.processedData || statement;
            const bank = data.bank || {};
            const accountHolder = data.account_holder || {};
            const transactions = data.transactions || [];
            
            for (const txn of transactions) {
                rows.push([
                    this.escapeCSV(txn.date || ''),
                    this.escapeCSV(txn.type || ''),
                    this.escapeCSV(txn.description || ''),
                    txn.deposit || 0,
                    txn.withdrawal || 0,
                    txn.balance || 0,
                    this.escapeCSV(bank.name || ''),
                    this.escapeCSV(data.account_number || ''),
                    this.escapeCSV(accountHolder.name || '')
                ].join(','));
            }
        }
        
        const csv = [headers.join(','), ...rows].join('\n');
        const bom = '\uFEFF';
        const blob = new Blob([bom + csv], { type: 'text/csv;charset=utf-8;' });
        
        console.log('✅ 銀行對帳單 CSV 導出完成');
        console.log(`   導出 ${rows.length} 筆交易`);
        return blob;
    }
    
    /**
     * 下載文件
     */
    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log(`✅ 文件已下載: ${filename}`);
    }
    
    /**
     * 工具函數: 轉義 CSV 字段
     */
    escapeCSV(value) {
        if (value === null || value === undefined) {
            return '';
        }
        
        const str = String(value);
        
        // 如果包含逗號、引號或換行符，需要用引號包裹並轉義內部引號
        if (str.includes(',') || str.includes('"') || str.includes('\n')) {
            return '"' + str.replace(/"/g, '""') + '"';
        }
        
        return str;
    }
    
    /**
     * 工具函數: 轉義 IIF 字段
     */
    escapeIIF(value) {
        if (value === null || value === undefined) {
            return '';
        }
        
        return String(value).replace(/\t/g, ' ').replace(/\n/g, ' ');
    }
    
    /**
     * 工具函數: 轉義 XML 字段
     */
    escapeXML(value) {
        if (value === null || value === undefined) {
            return '';
        }
        
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&apos;');
    }
    
    /**
     * 工具函數: 格式化 IIF 日期 (MM/DD/YYYY)
     */
    formatIIFDate(dateString) {
        if (!dateString) {
            return '';
        }
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return '';
        }
        
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        
        return `${month}/${day}/${year}`;
    }
    
    /**
     * 工具函數: 格式化 QBO 日期 (YYYYMMDD)
     */
    formatQBODate(dateString) {
        if (!dateString) {
            return '';
        }
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return '';
        }
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}${month}${day}`;
    }
    
    /**
     * 工具函數: 格式化 QBO 日期時間 (YYYYMMDDHHMMSS)
     */
    formatQBODateTime(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        
        return `${year}${month}${day}${hours}${minutes}${seconds}`;
    }
    
    /**
     * 導出為 JSON 格式（參考 LedgerBox 圖1）
     * 
     * JSON 格式優勢:
     * - 保留完整的數據結構
     * - 可以用於 API 整合
     * - 易於程序處理
     */
    exportToJSON(documents, options = {}) {
        console.log('📊 導出為 JSON 格式...');
        
        // 根據文檔類型決定導出格式
        const documentType = options.documentType || 'invoice';
        
        let jsonData;
        
        if (documentType === 'bank-statement') {
            // 銀行對帳單格式（參考 LedgerBox 圖1）
            jsonData = this.formatBankStatementJSON(documents[0]);
        } else {
            // 發票/收據格式
            jsonData = documents.map(doc => this.formatInvoiceJSON(doc));
            
            // 如果只有一個文檔，直接返回對象而不是數組
            if (jsonData.length === 1) {
                jsonData = jsonData[0];
            }
        }
        
        const json = JSON.stringify(jsonData, null, 2);
        const blob = new Blob([json], { type: 'application/json;charset=utf-8;' });
        
        console.log('✅ JSON 格式導出完成');
        return blob;
    }
    
    /**
     * 格式化銀行對帳單為 JSON（參考 LedgerBox 圖1）
     */
    formatBankStatementJSON(statement) {
        const data = statement.processedData || statement;
        
        return {
            CustomerName: data.account_holder?.name || '',
            AccountNumber: data.account_number || '',
            AccountType: data.account_type || 'Integrated Account',
            BankName: data.bank?.name || '',
            BankAddress: data.bank?.address || '',
            PeriodStartDate: data.statement_period?.from || '',
            PeriodEndDate: data.statement_period?.to || '',
            StartingBalance: data.opening_balance || 0,
            EndingBalance: data.closing_balance || 0,
            LineItems: (data.transactions || []).map(txn => ({
                Date: txn.date || '',
                Description: txn.description || '',
                Credits: txn.type === 'credit' ? txn.amount : 0,
                Debits: txn.type === 'debit' ? txn.amount : 0,
                Balance: txn.balance || 0
            }))
        };
    }
    
    /**
     * 格式化發票為 JSON
     */
    formatInvoiceJSON(invoice) {
        const data = invoice.processedData || invoice;
        
        return {
            InvoiceNumber: data.invoice_number || '',
            InvoiceDate: data.date || '',
            DueDate: data.due_date || '',
            Supplier: {
                Name: data.supplier?.name || '',
                NameEN: data.supplier?.name_en || '',
                Address: data.supplier?.address || '',
                Phone: data.supplier?.phone || '',
                Email: data.supplier?.email || ''
            },
            Customer: {
                Name: data.customer?.name || '',
                Address: data.customer?.address || '',
                Contact: data.customer?.contact || '',
                Phone: data.customer?.phone || ''
            },
            LineItems: (data.items || []).map(item => ({
                Code: item.code || '',
                Description: item.description || '',
                Quantity: item.quantity || 0,
                Unit: item.unit || '',
                UnitPrice: item.unit_price || 0,
                Amount: item.amount || 0
            })),
            Subtotal: data.subtotal || 0,
            Discount: data.discount || 0,
            Tax: data.tax || 0,
            Total: data.total || 0,
            Currency: data.currency || 'HKD',
            PaymentMethod: data.payment_method || '',
            PaymentStatus: data.payment_status || '',
            Notes: data.notes || ''
        };
    }
}

// 導出為全局變量
if (typeof window !== 'undefined') {
    window.ExportManager = ExportManager;
    window.exportManager = new ExportManager();
    console.log('✅ 導出管理器已加載');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExportManager;
}

