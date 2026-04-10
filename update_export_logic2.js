const fs = require('fs');

const htmlPath = 'document-detail.html';
let html = fs.readFileSync(htmlPath, 'utf8');

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
                // ensure date is a Date object for the TS services
                date: doc.date ? new Date(doc.date) : new Date(),
                amount: parseFloat(doc.totalAmount || doc.total_amount || 0),
                taxAmount: parseFloat(doc.taxAmount || doc.tax_amount || 0),
                currency: doc.currency || 'HKD',
                category: doc.category || 'Uncategorized',
                description: doc.description || '',
                receiptImage: { url: doc.imageUrl || doc.image_url || 'https://vaultcaddy.com/placeholder.jpg' },
                status: doc.status || 'processed',
                taxMapping: {
                    label_zh: doc.category || '未分類',
                    ird_tag: 'ird:OtherOperatingExpenses',
                    deductible: true
                }
            };

            const receipts = [standardReceipt];
            const companyName = 'My Company (HK) Limited';
            const companyBrNumber = '12345678-000';
            const yearEnd = '2025-12-31';

            let exportContent = '';
            let exportFileName = '';
            let mimeType = 'text/csv;charset=utf-8;';

            switch (format) {
                case 'ixbrl':
                    const ixbrlGen = new window.VaultCaddyExports.iXBRLGenerator(companyBrNumber, companyName, yearEnd);
                    exportContent = ixbrlGen.generate(receipts);
                    exportFileName = \`iXBRL_Export_\${standardReceipt.date.toISOString().split('T')[0]}.xhtml\`;
                    mimeType = 'application/xhtml+xml;charset=utf-8;';
                    break;
                case 'audit_excel':
                    const excelGen = new window.VaultCaddyExports.AuditExcelGenerator();
                    excelGen.generateAndDownload(receipts, companyName);
                    console.log('✅ Audit Excel 導出成功');
                    return; // Excel handles its own download
                case 'xero_csv':
                    const xeroGen = new window.VaultCaddyExports.AccountingExporter();
                    exportContent = xeroGen.generateXeroCSV(receipts);
                    exportFileName = \`Xero_Export_\${standardReceipt.date.toISOString().split('T')[0]}.csv\`;
                    break;
                case 'qbo_csv':
                    const qboGen = new window.VaultCaddyExports.AccountingExporter();
                    exportContent = qboGen.generateQuickBooksCSV(receipts);
                    exportFileName = \`QBO_Export_\${standardReceipt.date.toISOString().split('T')[0]}.csv\`;
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
console.log('Updated document-detail.html export logic with class instantiation');
