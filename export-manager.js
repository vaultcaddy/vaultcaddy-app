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
        this.supportedFormats = ['csv', 'xero'];
    }
    
    /**
     * 導出發票數據
     * 
     * @param {Array} invoices - 發票列表
     * @param {String} format - 導出格式 (csv 或 xero)
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
        
        if (format === 'xero') {
            return this.exportToXeroCSV(invoices);
        }
        
        return this.exportToCSV(invoices, options);
    }
    
    /**
     * 導出為 Excel 格式 (如果支持) 或 CSV
     */
    exportToCSV(invoices, options = {}) {
        if (typeof XLSX !== 'undefined') {
            console.log('📊 導出為 Excel 格式...');
            return this.exportToExcel(invoices);
        } else {
            console.log('📊 導出為 CSV 格式 (降級)...');
            return this.exportToCSVSummary(invoices);
        }
    }
    
    /**
     * 導出為真正的 Excel (.xlsx)
     */
    exportToExcel(invoices) {
        // 準備數據
        const excelData = invoices.map(invoice => {
            const data = invoice.processedData || invoice;
            const taxInfo = data.tax_deductibility || {};
            
            return {
                '收據日期': data.date || '',
                '商戶名稱': data.merchant_name || data.vendor || data.supplier || data.merchantName || '',
                '開支類別': data.expense_category || '',
                '購買項目簡述': data.items_summary || '',
                '總金額': parseFloat(data.total_amount || data.total || data.totalAmount || 0),
                '貨幣': data.currency || 'HKD',
                'IRD 扣稅可能性': taxInfo.level || '',
                '扣稅原因說明': taxInfo.reason || '',
                '備註': data.notes || '',
                '收據圖片連結': invoice.fileUrl || invoice.url || ''
            };
        });
        
        // 計算總計
        let totalAmount = 0;
        let totalTaxDeductible = 0;
        
        excelData.forEach(row => {
            const amount = row['總金額'] || 0;
            totalAmount += amount;
            
            if (row['IRD 扣稅可能性'] === 'High') {
                totalTaxDeductible += amount;
            } else if (row['IRD 扣稅可能性'] === 'Medium') {
                totalTaxDeductible += amount * 0.5;
            }
        });
        
        // 添加空行和總計行
        excelData.push({}); // 空行
        excelData.push({
            '收據日期': '總計',
            '總金額': totalAmount,
            'IRD 扣稅可能性': '預計可扣稅總額:',
            '扣稅原因說明': totalTaxDeductible
        });
        
        // 創建工作表
        const ws = XLSX.utils.json_to_sheet(excelData);
        
        // 設置列寬
        const wscols = [
            {wch: 12}, // 日期
            {wch: 25}, // 商戶
            {wch: 20}, // 類別
            {wch: 30}, // 簡述
            {wch: 10}, // 金額
            {wch: 8},  // 貨幣
            {wch: 15}, // 扣稅可能性
            {wch: 40}, // 說明
            {wch: 20}, // 備註
            {wch: 50}  // 圖片連結
        ];
        ws['!cols'] = wscols;
        
        // 創建工作簿
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "單據明細");
        
        // 生成二進制數據
        const wbout = XLSX.write(wb, {bookType:'xlsx', type:'array'});
        
        // 創建 Blob
        const blob = new Blob([wbout], {type: "application/octet-stream"});
        
        // 標記為 xlsx 以便下載時使用正確副檔名
        blob.isXlsx = true;
        
        return blob;
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
            '備註',
            '收據圖片連結'
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
                this.escapeCSV(data.notes || ''),
                this.escapeCSV(invoice.fileUrl || invoice.url || '')
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
     * 導出為 Xero 專用匯入 CSV 格式
     */
    exportToXeroCSV(invoices) {
        console.log('📊 導出為 Xero 專用 CSV 格式...');
        
        // Xero 官方要求的必備欄位 (Bank Statement Import format)
        const headers = [
            '*Date',
            '*Amount',
            'Payee',
            'Description',
            'Reference',
            'Cheque Number'
        ];
        
        const rows = invoices.map(invoice => {
            const data = invoice.processedData || invoice;
            
            // 處理日期格式 (Xero 偏好 DD/MM/YYYY 或 MM/DD/YYYY)
            // 假設我們原本的 date 是 YYYY-MM-DD
            let formattedDate = data.date || '';
            if (formattedDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
                const parts = formattedDate.split('-');
                formattedDate = `${parts[2]}/${parts[1]}/${parts[0]}`; // 轉換為 DD/MM/YYYY
            }
            
            // 處理金額 (支出在 Xero 中通常是負數)
            let amount = parseFloat(data.total_amount || data.total || data.totalAmount || 0);
            // 假設收據都是支出，所以加上負號
            amount = -Math.abs(amount);
            
            // 組合描述 (包含 AI 分類和圖片連結，方便會計師查閱)
            const category = data.expense_category ? `[${data.expense_category}] ` : '';
            const summary = data.items_summary || '';
            const imgLink = invoice.fileUrl || invoice.url ? ` (Receipt: ${invoice.fileUrl || invoice.url})` : '';
            const description = `${category}${summary}${imgLink}`;
            
            return [
                this.escapeCSV(formattedDate),
                amount,
                this.escapeCSV(data.merchant_name || data.vendor || data.supplier || data.merchantName || ''),
                this.escapeCSV(description),
                this.escapeCSV(`VC-${Date.now().toString().slice(-6)}`), // 生成一個簡單的 Reference ID
                '' // Cheque Number 留空
            ].join(',');
        });
        
        const csv = [headers.join(','), ...rows].join('\n');
        
        // 添加 BOM 以支持 Excel 正確顯示
        const bom = '\uFEFF';
        const blob = new Blob([bom + csv], { type: 'text/csv;charset=utf-8;' });
        
        console.log('✅ Xero CSV 導出完成');
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
