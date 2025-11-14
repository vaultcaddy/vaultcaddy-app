/**
 * 📊 優化版 CSV 導出模塊
 * 
 * 根據文檔類型生成不同的 CSV 格式：
 * - Receipts（收據）：商家、日期、項目、金額
 * - Invoices（發票）：供應商、客戶、發票號、項目明細
 * - Bank Statements（銀行對帳單）：銀行、期間、交易記錄
 * - General（通用）：基本信息和提取的數據
 * 
 * @version 1.0.0
 * @updated 2025-11-13
 */

class ExportOptimizer {
    /**
     * 主導出函數 - 根據文檔類型選擇格式
     */
    static generateCSV(docs) {
        if (!docs || docs.length === 0) {
            return '';
        }
        
        // 檢查所有文檔是否為同一類型
        const types = [...new Set(docs.map(doc => doc.type || doc.processedData?.documentType))];
        
        if (types.length === 1 && types[0]) {
            // 所有文檔同一類型，使用專用格式
            return this.generateTypedCSV(docs, types[0]);
        } else {
            // 混合類型，使用通用格式
            return this.generateMixedCSV(docs);
        }
    }
    
    /**
     * 收據專用 CSV 格式
     */
    static generateReceiptCSV(docs) {
        const headers = [
            '文檔名稱',
            '收據編號',
            '日期',
            '時間',
            '商家名稱',
            '商家地址',
            '商家電話',
            '項目代碼',
            '項目描述',
            '項目類別',
            '數量',
            '單價',
            '金額',
            '小計',
            '服務費',
            '稅額',
            '稅率',
            '總金額',
            '幣別',
            '付款方式',
            '卡號後4位',
            '備註',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            // 如果有項目明細，每個項目一行
            if (data.items && Array.isArray(data.items) && data.items.length > 0) {
                data.items.forEach((item, index) => {
                    const row = [
                        `"${this.escape(doc.fileName || doc.name)}"`,
                        data.receipt_number || data.receiptNumber || '',
                        data.date || '',
                        data.time || '',
                        `"${this.escape(data.merchant_name || data.merchantName)}"`,
                        `"${this.escape(data.merchant_address || data.merchantAddress)}"`,
                        data.merchant_phone || data.merchantPhone || '',
                        item.code || '',
                        `"${this.escape(item.description || item.desc || item.name)}"`,
                        item.category || '',
                        item.quantity || item.qty || 1,
                        item.unit_price || item.unitPrice || item.price || 0,
                        item.amount || item.total || 0,
                        index === 0 ? (data.subtotal || '') : '',  // 只在第一行顯示
                        index === 0 ? (data.service_charge || data.serviceCharge || '') : '',
                        index === 0 ? (data.tax || data.taxAmount || '') : '',
                        index === 0 ? (data.tax_rate || data.taxRate || '') : '',
                        index === 0 ? (data.total || data.totalAmount || '') : '',
                        index === 0 ? (data.currency || 'HKD') : '',
                        index === 0 ? (data.payment_method || data.paymentMethod || '') : '',
                        index === 0 ? (data.card_last_4_digits || data.cardLast4 || '') : '',
                        index === 0 ? `"${this.escape(data.notes || '')}"` : '',
                        index === 0 ? uploadDate : ''
                    ];
                    rows.push(row.join(','));
                });
            } else {
                // 沒有項目明細，只顯示總額
                const row = [
                    `"${this.escape(doc.fileName || doc.name)}"`,
                    data.receipt_number || data.receiptNumber || '',
                    data.date || '',
                    data.time || '',
                    `"${this.escape(data.merchant_name || data.merchantName)}"`,
                    `"${this.escape(data.merchant_address || data.merchantAddress)}"`,
                    data.merchant_phone || data.merchantPhone || '',
                    '',  // 項目代碼
                    '',  // 項目描述
                    '',  // 項目類別
                    '',  // 數量
                    '',  // 單價
                    '',  // 金額
                    data.subtotal || '',
                    data.service_charge || data.serviceCharge || '',
                    data.tax || data.taxAmount || '',
                    data.tax_rate || data.taxRate || '',
                    data.total || data.totalAmount || '',
                    data.currency || 'HKD',
                    data.payment_method || data.paymentMethod || '',
                    data.card_last_4_digits || data.cardLast4 || '',
                    `"${this.escape(data.notes || '')}"`,
                    uploadDate
                ];
                rows.push(row.join(','));
            }
        });
        
        return rows.join('\n');
    }
    
    /**
     * 發票專用 CSV 格式
     */
    static generateInvoiceCSV(docs) {
        const headers = [
            '文檔名稱',
            '發票號碼',
            '發票日期',
            '到期日',
            '供應商名稱',
            '供應商地址',
            '供應商電話',
            '供應商電郵',
            '供應商稅號',
            '客戶名稱',
            '客戶地址',
            '客戶電話',
            '客戶電郵',
            '項目代碼',
            '項目描述',
            '數量',
            '單位',
            '單價',
            '項目小計',
            '小計',
            '稅額',
            '稅率',
            '總金額',
            '幣別',
            '付款條款',
            '付款方式',
            '銀行賬號',
            '備註',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            // 如果有項目明細，每個項目一行
            if (data.items && Array.isArray(data.items) && data.items.length > 0) {
                data.items.forEach((item, index) => {
                    const row = [
                        `"${this.escape(doc.fileName || doc.name)}"`,
                        data.invoice_number || data.invoiceNumber || '',
                        data.invoice_date || data.invoiceDate || data.date || '',
                        data.due_date || data.dueDate || '',
                        `"${this.escape(data.supplier || data.vendor)}"`,
                        `"${this.escape(data.supplier_address || data.vendorAddress)}"`,
                        data.supplier_phone || data.vendorPhone || '',
                        data.supplier_email || data.vendorEmail || '',
                        data.supplier_tax_id || data.vendorTaxId || '',
                        `"${this.escape(data.customer || data.customerName)}"`,
                        `"${this.escape(data.customer_address || data.customerAddress)}"`,
                        data.customer_phone || data.customerPhone || '',
                        data.customer_email || data.customerEmail || '',
                        item.product_code || item.productCode || item.code || '',
                        `"${this.escape(item.description || item.desc || item.name)}"`,
                        item.quantity || item.qty || 1,
                        item.unit || '件',
                        item.unit_price || item.unitPrice || item.price || 0,
                        item.subtotal || item.total || item.amount || 0,
                        index === 0 ? (data.subtotal || data.subTotal || '') : '',
                        index === 0 ? (data.tax || data.taxAmount || '') : '',
                        index === 0 ? (data.tax_rate || data.taxRate || '') : '',
                        index === 0 ? (data.total || data.totalAmount || '') : '',
                        index === 0 ? (data.currency || 'HKD') : '',
                        index === 0 ? `"${this.escape(data.payment_terms || data.paymentTerms)}"` : '',
                        index === 0 ? (data.payment_method || data.paymentMethod || '') : '',
                        index === 0 ? (data.bank_account || data.bankAccount || '') : '',
                        index === 0 ? `"${this.escape(data.notes || data.memo)}"` : '',
                        index === 0 ? uploadDate : ''
                    ];
                    rows.push(row.join(','));
                });
            } else {
                // 沒有項目明細
                const row = [
                    `"${this.escape(doc.fileName || doc.name)}"`,
                    data.invoice_number || data.invoiceNumber || '',
                    data.invoice_date || data.invoiceDate || data.date || '',
                    data.due_date || data.dueDate || '',
                    `"${this.escape(data.supplier || data.vendor)}"`,
                    `"${this.escape(data.supplier_address || data.vendorAddress)}"`,
                    data.supplier_phone || data.vendorPhone || '',
                    data.supplier_email || data.vendorEmail || '',
                    data.supplier_tax_id || data.vendorTaxId || '',
                    `"${this.escape(data.customer || data.customerName)}"`,
                    `"${this.escape(data.customer_address || data.customerAddress)}"`,
                    data.customer_phone || data.customerPhone || '',
                    data.customer_email || data.customerEmail || '',
                    '',  // 項目代碼
                    '',  // 項目描述
                    '',  // 數量
                    '',  // 單位
                    '',  // 單價
                    '',  // 項目小計
                    data.subtotal || data.subTotal || '',
                    data.tax || data.taxAmount || '',
                    data.tax_rate || data.taxRate || '',
                    data.total || data.totalAmount || '',
                    data.currency || 'HKD',
                    `"${this.escape(data.payment_terms || data.paymentTerms)}"`,
                    data.payment_method || data.paymentMethod || '',
                    data.bank_account || data.bankAccount || '',
                    `"${this.escape(data.notes || data.memo)}"`,
                    uploadDate
                ];
                rows.push(row.join(','));
            }
        });
        
        return rows.join('\n');
    }
    
    /**
     * 銀行對帳單專用 CSV 格式
     */
    static generateStatementCSV(docs) {
        const headers = [
            '文檔名稱',
            '銀行名稱',
            '賬戶號碼',
            '賬戶名稱',
            '對帳單期間',
            '期初餘額',
            '期末餘額',
            '交易日期',
            '交易描述',
            '交易類型',
            '金額',
            '餘額',
            '參考號碼',
            '備註',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            // 如果有交易記錄，每筆交易一行
            if (data.transactions && Array.isArray(data.transactions) && data.transactions.length > 0) {
                data.transactions.forEach((txn, index) => {
                    const row = [
                        `"${this.escape(doc.fileName || doc.name)}"`,
                        index === 0 ? `"${this.escape(data.bank_name || data.bankName)}"` : '',
                        index === 0 ? (data.account_number || data.accountNumber || '') : '',
                        index === 0 ? `"${this.escape(data.account_name || data.accountName)}"` : '',
                        index === 0 ? (data.statement_period || data.period || '') : '',
                        index === 0 ? (data.opening_balance || data.openingBalance || '') : '',
                        index === 0 ? (data.closing_balance || data.closingBalance || '') : '',
                        txn.date || '',
                        `"${this.escape(txn.description || txn.desc)}"`,
                        txn.type || txn.transaction_type || '',
                        txn.amount || 0,
                        txn.balance || '',
                        txn.reference || txn.ref || '',
                        `"${this.escape(txn.notes || '')}"`,
                        index === 0 ? uploadDate : ''
                    ];
                    rows.push(row.join(','));
                });
            } else {
                // 沒有交易記錄
                const row = [
                    `"${this.escape(doc.fileName || doc.name)}"`,
                    `"${this.escape(data.bank_name || data.bankName)}"`,
                    data.account_number || data.accountNumber || '',
                    `"${this.escape(data.account_name || data.accountName)}"`,
                    data.statement_period || data.period || '',
                    data.opening_balance || data.openingBalance || '',
                    data.closing_balance || data.closingBalance || '',
                    '',  // 交易日期
                    '',  // 交易描述
                    '',  // 交易類型
                    '',  // 金額
                    '',  // 餘額
                    '',  // 參考號碼
                    '',  // 備註
                    uploadDate
                ];
                rows.push(row.join(','));
            }
        });
        
        return rows.join('\n');
    }
    
    /**
     * 通用文檔 CSV 格式
     */
    static generateGeneralCSV(docs) {
        const headers = [
            '文檔名稱',
            '文檔類型',
            '標題',
            '文檔編號',
            '日期',
            '實體名稱',
            '實體類型',
            '金額',
            '幣別',
            '摘要',
            '關鍵詞',
            '語言',
            '備註',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            // 提取實體信息
            let entities = '';
            if (data.entities && Array.isArray(data.entities)) {
                entities = data.entities.map(e => `${e.name || e.value} (${e.type || ''})`).join('; ');
            }
            
            // 提取金額
            let amounts = '';
            if (data.amounts && Array.isArray(data.amounts)) {
                amounts = data.amounts.join('; ');
            }
            
            // 提取關鍵詞
            let keywords = '';
            if (data.key_terms && Array.isArray(data.key_terms)) {
                keywords = data.key_terms.join('; ');
            }
            
            const row = [
                `"${this.escape(doc.fileName || doc.name)}"`,
                data.document_type || data.documentType || '',
                `"${this.escape(data.title)}"`,
                data.document_number || data.documentNumber || '',
                data.date || '',
                `"${this.escape(entities)}"`,
                '',  // 實體類型（已在實體名稱中）
                amounts,
                data.currency || '',
                `"${this.escape(data.summary)}"`,
                `"${this.escape(keywords)}"`,
                data.language || '',
                `"${this.escape(data.notes || '')}"`,
                uploadDate
            ];
            rows.push(row.join(','));
        });
        
        return rows.join('\n');
    }
    
    /**
     * 混合類型 CSV 格式（簡化版）
     */
    static generateMixedCSV(docs) {
        const headers = [
            '文檔名稱',
            '文檔類型',
            '編號',
            '日期',
            '來源/供應商',
            '金額',
            '幣別',
            '狀態',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            const row = [
                `"${this.escape(doc.fileName || doc.name)}"`,
                data.documentType || doc.type || '',
                data.invoice_number || data.receiptNumber || data.documentNumber || '',
                data.date || data.invoiceDate || data.transactionDate || '',
                `"${this.escape(data.supplier || data.vendor || data.merchantName || data.source)}"`,
                data.total || data.totalAmount || data.amount || '',
                data.currency || 'HKD',
                doc.status || '',
                uploadDate
            ];
            rows.push(row.join(','));
        });
        
        return rows.join('\n');
    }
    
    /**
     * 發票/收據合併 CSV 格式（統一版）
     * 合併原因：數據結構相似，AI 可自動識別，簡化用戶選擇
     */
    static generateInvoiceReceiptCSV(docs) {
        const headers = [
            '文檔名稱',
            '編號',
            '日期',
            '時間',
            '供應商/來源/銀行',
            '供應商地址',
            '供應商電話',
            '供應商電郵',
            '客戶名稱',
            '客戶地址',
            '項目代碼',
            '項目描述',
            '項目類別',
            '數量',
            '單位',
            '單價',
            '項目金額',
            '小計',
            '服務費',
            '稅額',
            '稅率',
            '總金額',
            '幣別',
            '付款方式',
            '卡號後4位',
            '付款條款',
            '到期日',
            '備註',
            '上傳日期'
        ];
        
        const rows = [headers.join(',')];
        
        docs.forEach(doc => {
            const data = doc.processedData || {};
            const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
            
            // 如果有項目明細，每個項目一行
            if (data.items && Array.isArray(data.items) && data.items.length > 0) {
                data.items.forEach((item, index) => {
                    const row = [
                        `"${this.escape(doc.fileName || doc.name)}"`,
                        // 編號（發票號或收據號）
                        data.invoice_number || data.invoiceNumber || data.receipt_number || data.receiptNumber || '',
                        // 日期
                        data.date || data.invoice_date || data.invoiceDate || '',
                        // 時間（收據才有）
                        data.time || '',
                        // 供應商/來源/銀行（統一欄位）
                        `"${this.escape(data.supplier || data.vendor || data.merchant_name || data.merchantName)}"`,
                        // 供應商地址
                        `"${this.escape(data.supplier_address || data.vendorAddress || data.merchant_address || data.merchantAddress)}"`,
                        // 供應商電話
                        data.supplier_phone || data.vendorPhone || data.merchant_phone || data.merchantPhone || '',
                        // 供應商電郵
                        data.supplier_email || data.vendorEmail || '',
                        // 客戶名稱（發票才有）
                        `"${this.escape(data.customer || data.customerName)}"`,
                        // 客戶地址（發票才有）
                        `"${this.escape(data.customer_address || data.customerAddress)}"`,
                        // 項目代碼
                        item.code || item.product_code || item.productCode || '',
                        // 項目描述
                        `"${this.escape(item.description || item.desc || item.name)}"`,
                        // 項目類別（收據才有）
                        item.category || '',
                        // 數量
                        item.quantity || item.qty || 1,
                        // 單位
                        item.unit || '件',
                        // 單價
                        item.unit_price || item.unitPrice || item.price || 0,
                        // 項目金額
                        item.amount || item.total || item.subtotal || 0,
                        // 小計（只在第一行顯示）
                        index === 0 ? (data.subtotal || data.subTotal || '') : '',
                        // 服務費（收據才有，只在第一行顯示）
                        index === 0 ? (data.service_charge || data.serviceCharge || '') : '',
                        // 稅額（只在第一行顯示）
                        index === 0 ? (data.tax || data.taxAmount || '') : '',
                        // 稅率（只在第一行顯示）
                        index === 0 ? (data.tax_rate || data.taxRate || '') : '',
                        // 總金額（只在第一行顯示）
                        index === 0 ? (data.total || data.totalAmount || '') : '',
                        // 幣別（只在第一行顯示）
                        index === 0 ? (data.currency || 'HKD') : '',
                        // 付款方式（只在第一行顯示）
                        index === 0 ? (data.payment_method || data.paymentMethod || '') : '',
                        // 卡號後4位（收據才有，只在第一行顯示）
                        index === 0 ? (data.card_last_4_digits || data.cardLast4 || '') : '',
                        // 付款條款（發票才有，只在第一行顯示）
                        index === 0 ? `"${this.escape(data.payment_terms || data.paymentTerms)}"` : '',
                        // 到期日（發票才有，只在第一行顯示）
                        index === 0 ? (data.due_date || data.dueDate || '') : '',
                        // 備註（只在第一行顯示）
                        index === 0 ? `"${this.escape(data.notes || data.memo)}"` : '',
                        // 上傳日期（只在第一行顯示）
                        index === 0 ? uploadDate : ''
                    ];
                    rows.push(row.join(','));
                });
            } else {
                // 沒有項目明細
                const row = [
                    `"${this.escape(doc.fileName || doc.name)}"`,
                    data.invoice_number || data.invoiceNumber || data.receipt_number || data.receiptNumber || '',
                    data.date || data.invoice_date || data.invoiceDate || '',
                    data.time || '',
                    `"${this.escape(data.supplier || data.vendor || data.merchant_name || data.merchantName)}"`,
                    `"${this.escape(data.supplier_address || data.vendorAddress || data.merchant_address || data.merchantAddress)}"`,
                    data.supplier_phone || data.vendorPhone || data.merchant_phone || data.merchantPhone || '',
                    data.supplier_email || data.vendorEmail || '',
                    `"${this.escape(data.customer || data.customerName)}"`,
                    `"${this.escape(data.customer_address || data.customerAddress)}"`,
                    '', '', '', '', '', '', '',
                    data.subtotal || data.subTotal || '',
                    data.service_charge || data.serviceCharge || '',
                    data.tax || data.taxAmount || '',
                    data.tax_rate || data.taxRate || '',
                    data.total || data.totalAmount || '',
                    data.currency || 'HKD',
                    data.payment_method || data.paymentMethod || '',
                    data.card_last_4_digits || data.cardLast4 || '',
                    `"${this.escape(data.payment_terms || data.paymentTerms)}"`,
                    data.due_date || data.dueDate || '',
                    `"${this.escape(data.notes || data.memo)}"`,
                    uploadDate
                ];
                rows.push(row.join(','));
            }
        });
        
        return rows.join('\n');
    }
    
    /**
     * 根據類型選擇生成函數（更新版）
     */
    static generateTypedCSV(docs, type) {
        const normalizedType = (type || '').toLowerCase();
        
        // 發票和收據使用同一格式（合併）
        if (normalizedType.includes('receipt') || normalizedType.includes('invoice') || 
            normalizedType === 'receipts' || normalizedType === 'invoices') {
            return this.generateInvoiceReceiptCSV(docs);
        } else if (normalizedType.includes('statement') || normalizedType === 'bank_statements') {
            return this.generateStatementCSV(docs);
        } else if (normalizedType === 'general') {
            return this.generateGeneralCSV(docs);
        } else {
            return this.generateMixedCSV(docs);
        }
    }
    
    /**
     * 工具函數：轉義 CSV 字段
     */
    static escape(value) {
        if (!value) return '';
        return String(value).replace(/"/g, '""');
    }
}

// 全局導出
window.ExportOptimizer = ExportOptimizer;

console.log('✅ Export Optimizer 已加載');

