/**
 * Xero & QuickBooks Exporter (4-Way Export 之一)
 *
 * 專為會計師設計，嚴格遵循 Xero "Bank Statement Import" 及 QuickBooks 格式。
 * 實現「0 修改直接 Import」，大幅提升會計師工作效率。
 */
export class AccountingExporter {
    /**
     * 生成 Xero Bank Statement CSV
     * 格式: *Date, *Amount, *Payee, Description, Reference, Check Number
     * @param records
     */
    generateXeroCSV(records) {
        // Xero 官方強制要求的標題列 (帶星號為必填)
        let csv = '*Date,*Amount,*Payee,Description,Reference,Check Number,TrackingCategory\n';
        records.forEach(record => {
            var _a, _b;
            const date = record.date.toISOString().split('T')[0]; // YYYY-MM-DD
            // 支出必須是負數 (Negative for expenses)
            const amount = `-${record.amount.toFixed(2)}`;
            const payee = this.escapeCSV(record.merchantName);
            // 將 IRD 標籤寫入 Description，方便會計師做 Reconcile
            const description = this.escapeCSV(((_a = record.taxMapping) === null || _a === void 0 ? void 0 : _a.label_zh) || record.category);
            const reference = this.escapeCSV(`VaultCaddy-${record.id}`);
            // Xero 的 Tracking Category (如部門或項目)，這裡預留給會計師使用
            const trackingCategory = this.escapeCSV(((_b = record.taxMapping) === null || _b === void 0 ? void 0 : _b.ird_tag) || '');
            csv += `"${date}",${amount},"${payee}","${description}","${reference}","","${trackingCategory}"\n`;
        });
        return csv;
    }
    /**
     * 生成 QuickBooks Online (QBO) CSV
     * 格式: Date, Description, Amount
     * @param records
     */
    generateQuickBooksCSV(records) {
        // QBO 官方支援的 3 欄式標準格式
        let csv = 'Date,Description,Amount\n';
        records.forEach(record => {
            var _a;
            const date = record.date.toISOString().split('T')[0]; // MM/DD/YYYY 或 YYYY-MM-DD
            // 組合商戶與分類作為描述
            const descText = `${record.merchantName} - ${((_a = record.taxMapping) === null || _a === void 0 ? void 0 : _a.label_zh) || record.category}`;
            const description = this.escapeCSV(descText);
            // 支出必須是負數
            const amount = `-${record.amount.toFixed(2)}`;
            csv += `"${date}","${description}",${amount}\n`;
        });
        return csv;
    }
    /**
     * 處理 CSV 欄位中的逗號與換行符
     */
    escapeCSV(str) {
        if (!str)
            return '';
        // 如果字串包含雙引號，必須將其替換為兩個雙引號
        return str.replace(/"/g, '""');
    }
    /**
     * 觸發瀏覽器下載
     */
    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
