const fs = require('fs');

const htmlPath = 'document-detail.html';
let html = fs.readFileSync(htmlPath, 'utf8');

// Inject the script tag before the closing </body> tag
if (!html.includes('vaultcaddy-exports.js')) {
    html = html.replace('</body>', '    <script src="public/js/vaultcaddy-exports.js"></script>\n</body>');
}

// Now replace the vaultcaddyExportDocument function
const newLogic = `    window.vaultcaddyExportDocument = async function(format) {
        const doc = window.currentDocument;
        if (!doc) {
            alert('沒有可導出的文檔數據');
            return;
        }

        try {
            console.log('🚀 開始 VaultCaddy 專屬導出:', format);
            
            // 轉換文檔格式以符合導出引擎要求
            const standardReceipt = {
                id: doc.id || 'doc_' + Date.now(),
                merchantName: doc.merchantName || doc.merchant_name || 'Unknown Merchant',
                date: doc.date || new Date().toISOString().split('T')[0],
                totalAmount: doc.totalAmount || doc.total_amount || 0,
                taxAmount: doc.taxAmount || doc.tax_amount || 0,
                currency: doc.currency || 'HKD',
                category: doc.category || 'Uncategorized',
                description: doc.description || '',
                imageUrl: doc.imageUrl || doc.image_url || '',
                status: doc.status || 'approved'
            };

            const receipts = [standardReceipt];
            const companyInfo = {
                name: 'My Company (HK) Limited',
                brNumber: '12345678-000',
                yearEnd: '2025-12-31'
            };

            let exportContent = '';
            let exportFileName = '';
            let mimeType = 'text/csv;charset=utf-8;';

            switch (format) {
                case 'ixbrl':
                    exportContent = window.VaultCaddyExports.iXBRLGenerator.generate(receipts, companyInfo);
                    exportFileName = \`iXBRL_Export_\${standardReceipt.date}.xhtml\`;
                    mimeType = 'application/xhtml+xml;charset=utf-8;';
                    break;
                case 'audit_excel':
                    const excelBuffer = window.VaultCaddyExports.AuditExcelGenerator.generate(receipts, companyInfo);
                    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = \`Audit_Excel_\${standardReceipt.date}.xlsx\`;
                    link.click();
                    URL.revokeObjectURL(link.href);
                    console.log('✅ Audit Excel 導出成功');
                    return; // Excel handles its own download
                case 'xero_csv':
                    exportContent = window.VaultCaddyExports.AccountingExporter.generateXeroCSV(receipts);
                    exportFileName = \`Xero_Export_\${standardReceipt.date}.csv\`;
                    break;
                case 'qbo_csv':
                    exportContent = window.VaultCaddyExports.AccountingExporter.generateQuickBooksCSV(receipts);
                    exportFileName = \`QBO_Export_\${standardReceipt.date}.csv\`;
                    break;
                default:
                    alert('未知導出格式: ' + format);
                    return;
            }

            // 下載 CSV 或 iXBRL 文件
            if (exportContent) {
                const blob = new Blob(['\\uFEFF' + exportContent], { type: mimeType });
                const link = document.createElement('a');
                const url = URL.createObjectURL(blob);
                
                link.setAttribute('href', url);
                link.setAttribute('download', exportFileName);
                link.style.visibility = 'hidden';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                URL.revokeObjectURL(url);
                console.log('✅ 文件已下載:', exportFileName);
            }
            
        } catch (error) {
            console.error('❌ 導出失敗:', error);
            alert('導出失敗: ' + error.message);
        }
    };`;

const regex = /window\.vaultcaddyExportDocument = async function\(format\) \{[\s\S]*?\n    \};\n/m;
html = html.replace(regex, newLogic + '\n');

fs.writeFileSync(htmlPath, html);
console.log('Updated document-detail.html export logic');
