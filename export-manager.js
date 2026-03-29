/**
 * VaultCaddy 導出管理器 (HK Shop IRD Version)
 * 
 * 作用：
 * 1. 將 AI 提取的發票數據導出為 CSV 格式
 * 2. 專為香港小店 IRD 扣稅分析設計
 * 
 * @version 3.0.0
 * @updated 2026-03-29
 */

class ExportManager {
    constructor() {
        this.version = '3.0.0';
        this.supportedFormats = ['csv'];
    }
    
    /**
     * 導出發票數據
     * 
     * @param {Array} invoices - 發票列表
     * @param {String} format - 導出格式 (csv)
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
        
        return this.exportToCSV(invoices, options);
    }
    
    /**
     * 導出為 CSV 格式
     */
    exportToCSV(invoices, options = {}) {
        console.log('📊 導出為 CSV 格式...');
        return this.exportToCSVSummary(invoices);
    }
    
    /**
     * CSV 摘要格式（每張發票一行）
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
            '備註'
        ];
        
        const rows = invoices.map(invoice => {
            const data = invoice.processedData || invoice;
            const taxInfo = data.tax_deductibility || {};
            
            return [
                this.escapeCSV(data.date || ''),
                this.escapeCSV(data.merchant_name || data.vendor || data.supplier || data.merchantName || ''),
                this.escapeCSV(data.expense_category || ''),
                this.escapeCSV(data.items_summary || ''),
                data.total_amount || data.total || data.totalAmount || 0,
                this.escapeCSV(data.currency || 'HKD'),
                this.escapeCSV(taxInfo.level || ''),
                this.escapeCSV(taxInfo.reason || ''),
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
     * 處理 CSV 轉義
     */
    escapeCSV(field) {
        if (field === null || field === undefined) {
            return '';
        }
        const stringField = String(field);
        if (stringField.includes(',') || stringField.includes('"') || stringField.includes('\n')) {
            return `"${stringField.replace(/"/g, '""')}"`;
        }
        return stringField;
    }
    
    /**
     * 下載文件
     */
    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
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
