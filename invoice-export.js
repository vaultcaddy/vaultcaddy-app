/**
 * VaultCaddy Invoice Export Module
 * 
 * 功能：
 * - 生成發票總數 CSV（快速對帳）
 * - 生成發票詳細交易數據 CSV（詳細記錄）
 * 
 * 作用：幫助用戶快速導出發票數據，支援兩種格式以滿足不同需求
 */

(function() {
    'use strict';
    
    console.log('🧾 InvoiceExport 模塊正在載入...');
    
    /**
     * 生成發票總數 CSV（快速對帳）
     * 
     * @param {Array} invoices - 發票文檔數組
     * @returns {string} CSV 內容
     */
    function generateInvoiceSummaryCSV(invoices) {
        console.log(`📊 生成發票總數 CSV，共 ${invoices.length} 個發票`);
        
        const headers = ['發票編號', '供應商', '日期', '總金額', '稅額', '狀態'];
        const rows = [headers];
        
        invoices.forEach(invoice => {
            const data = invoice.processedData || {};
            
            // 提取數據，支援多種可能的字段名稱
            const invoiceNumber = data.invoiceNumber || data.invoice_number || data.number || '';
            const vendor = data.vendorName || data.vendor || data.supplier || data.supplierName || '';
            const date = data.invoiceDate || data.date || data.issueDate || '';
            const total = data.totalAmount || data.total || data.amount || data.grandTotal || '0';
            const tax = data.taxAmount || data.tax || data.gst || data.vat || '0';
            const status = data.status || data.paymentStatus || '已付款';
            
            const row = [
                invoiceNumber,
                vendor,
                date,
                total,
                tax,
                status
            ];
            
            rows.push(row);
        });
        
        const csv = rows.map(row => row.map(escapeCSV).join(',')).join('\n');
        console.log('✅ 發票總數 CSV 生成成功');
        return csv;
    }
    
    /**
     * 生成發票詳細交易數據 CSV（詳細記錄）
     * 
     * @param {Array} invoices - 發票文檔數組
     * @returns {string} CSV 內容
     */
    function generateInvoiceDetailedCSV(invoices) {
        console.log(`📊 生成發票詳細數據 CSV，共 ${invoices.length} 個發票`);
        
        const headers = ['發票編號', '供應商', '日期', '項目名稱', '數量', '單價', '小計', '總金額'];
        const rows = [headers];
        
        invoices.forEach(invoice => {
            const data = invoice.processedData || {};
            
            // 提取基本信息
            const invoiceNumber = data.invoiceNumber || data.invoice_number || data.number || '';
            const vendor = data.vendorName || data.vendor || data.supplier || data.supplierName || '';
            const date = data.invoiceDate || data.date || data.issueDate || '';
            const total = data.totalAmount || data.total || data.amount || data.grandTotal || '0';
            
            // 提取項目列表
            const items = data.items || data.lineItems || data.products || data.services || [];
            
            if (items.length === 0) {
                // 如果沒有項目明細，至少添加一行總計
                const row = [
                    invoiceNumber,
                    vendor,
                    date,
                    '總計',
                    '1',
                    total,
                    total,
                    total
                ];
                rows.push(row);
            } else {
                // 為每個項目添加一行
                items.forEach(item => {
                    const itemName = item.description || item.itemName || item.name || item.product || '';
                    const quantity = item.quantity || item.qty || '1';
                    const unitPrice = item.unitPrice || item.price || item.rate || '0';
                    const subtotal = item.subtotal || item.amount || item.total || (parseFloat(quantity) * parseFloat(unitPrice)) || '0';
                    
                    const row = [
                        invoiceNumber,
                        vendor,
                        date,
                        itemName,
                        quantity,
                        unitPrice,
                        subtotal,
                        total
                    ];
                    
                    rows.push(row);
                });
            }
        });
        
        const csv = rows.map(row => row.map(escapeCSV).join(',')).join('\n');
        console.log('✅ 發票詳細數據 CSV 生成成功');
        return csv;
    }
    
    /**
     * Escape CSV 字段，處理特殊字符
     * 
     * @param {*} value - 要轉義的值
     * @returns {string} 轉義後的字符串
     */
    function escapeCSV(value) {
        if (value === null || value === undefined) return '';
        const str = String(value);
        if (str.includes(',') || str.includes('"') || str.includes('\n')) {
            return `"${str.replace(/"/g, '""')}"`;
        }
        return str;
    }
    
    /**
     * 下載 CSV 文件
     * 
     * @param {string} content - CSV 內容
     * @param {string} filename - 文件名
     */
    function downloadCSV(content, filename) {
        const blob = new Blob(['\uFEFF' + content], { type: 'text/csv;charset=utf-8;' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        console.log(`✅ 文件已下載: ${filename}`);
    }
    
    // 全局暴露
    window.InvoiceExport = {
        generateInvoiceSummaryCSV,
        generateInvoiceDetailedCSV,
        downloadCSV,
        
        // 便捷方法
        exportSummary: function(invoices, filename) {
            const csv = generateInvoiceSummaryCSV(invoices);
            const defaultFilename = filename || `Invoice_Summary_${new Date().toISOString().split('T')[0]}.csv`;
            downloadCSV(csv, defaultFilename);
        },
        
        exportDetailed: function(invoices, filename) {
            const csv = generateInvoiceDetailedCSV(invoices);
            const defaultFilename = filename || `Invoice_Detailed_${new Date().toISOString().split('T')[0]}.csv`;
            downloadCSV(csv, defaultFilename);
        }
    };
    
    console.log('✅ InvoiceExport 模塊已載入');
})();

