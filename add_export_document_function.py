#!/usr/bin/env python3
"""
🔧 为 document-detail-new.js 添加 exportDocument 函数

问题：document-detail.html 调用 exportDocument() 但函数未定义
解决：添加 exportDocument() 函数，用于单个文档的导出
"""

import os

def add_export_document_function():
    """在 document-detail-new.js 末尾添加 exportDocument 函数"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查函数是否已存在
    if 'function exportDocument(' in content or 'window.exportDocument' in content:
        print("ℹ️  exportDocument 函数已存在")
        return False
    
    # 添加 exportDocument 函数
    export_function = '''

// ============================================
// 导出当前文档
// ============================================
window.exportDocument = function(format) {
    console.log('📤 导出文档:', format);
    
    // 关闭 Export 菜单
    if (typeof window.closeExportMenu === 'function') {
        window.closeExportMenu();
    }
    
    // 检查当前文档
    if (!window.currentDocument) {
        alert('无法获取文档数据');
        return;
    }
    
    const doc = window.currentDocument;
    const data = doc.processedData || {};
    
    console.log('📄 文档类型:', doc.type || doc.documentType);
    console.log('📊 文档数据:', data);
    
    try {
        // 根据格式导出
        switch(format) {
            case 'bank_statement_csv':
                exportBankStatementCSV(data, doc);
                break;
            case 'invoice_summary_csv':
                exportInvoiceSummaryCSV(data, doc);
                break;
            case 'invoice_detailed_csv':
                exportInvoiceDetailedCSV(data, doc);
                break;
            case 'xero_csv':
                exportXeroCSV(data, doc);
                break;
            case 'quickbooks_csv':
                exportQuickBooksCSV(data, doc);
                break;
            case 'iif':
                exportIIF(data, doc);
                break;
            case 'qbo':
                exportQBO(data, doc);
                break;
            default:
                alert('不支持的导出格式: ' + format);
        }
    } catch (error) {
        console.error('❌ 导出失败:', error);
        alert('导出失败: ' + error.message);
    }
};

// 导出银行对账单 CSV
function exportBankStatementCSV(data, doc) {
    const transactions = data.transactions || [];
    
    let csv = 'Date,Description,Amount,Balance\\n';
    transactions.forEach(t => {
        csv += `"${t.date || ''}","${t.description || ''}","${t.amount || 0}","${t.balance || 0}"\\n`;
    });
    
    downloadFile(csv, `bank_statement_${doc.id || 'export'}.csv`, 'text/csv');
}

// 导出发票汇总 CSV
function exportInvoiceSummaryCSV(data, doc) {
    let csv = 'Invoice Number,Date,Vendor,Total Amount\\n';
    csv += `"${data.invoiceNumber || data.invoice_number || ''}",`;
    csv += `"${data.date || data.invoice_date || ''}",`;
    csv += `"${data.vendor || data.supplier || ''}",`;
    csv += `"${data.total || data.totalAmount || 0}"\\n`;
    
    downloadFile(csv, `invoice_${doc.id || 'export'}.csv`, 'text/csv');
}

// 导出发票详细 CSV
function exportInvoiceDetailedCSV(data, doc) {
    const items = data.items || data.lineItems || [];
    
    let csv = 'Code,Description,Quantity,Unit,Unit Price,Amount\\n';
    items.forEach(item => {
        csv += `"${item.code || item.itemCode || ''}",`;
        csv += `"${item.description || ''}",`;
        csv += `"${item.quantity || 0}",`;
        csv += `"${item.unit || ''}",`;
        csv += `"${item.unit_price || item.unitPrice || 0}",`;
        csv += `"${item.amount || 0}"\\n`;
    });
    
    downloadFile(csv, `invoice_details_${doc.id || 'export'}.csv`, 'text/csv');
}

// 导出 Xero CSV
function exportXeroCSV(data, doc) {
    // Xero 格式
    let csv = '*ContactName,*InvoiceNumber,*InvoiceDate,*DueDate,Description,*Quantity,*UnitAmount,*AccountCode,*TaxType\\n';
    
    const vendor = data.vendor || data.supplier || '';
    const invoiceNumber = data.invoiceNumber || data.invoice_number || '';
    const date = data.date || data.invoice_date || '';
    
    const items = data.items || data.lineItems || [];
    items.forEach(item => {
        csv += `"${vendor}","${invoiceNumber}","${date}","${date}",`;
        csv += `"${item.description || ''}","${item.quantity || 1}",`;
        csv += `"${item.unit_price || item.unitPrice || 0}","200","Tax on Purchases"\\n`;
    });
    
    downloadFile(csv, `xero_${doc.id || 'export'}.csv`, 'text/csv');
}

// 导出 QuickBooks CSV
function exportQuickBooksCSV(data, doc) {
    // QuickBooks 格式
    let csv = '*Vendor,*Date,*Amount,*Account,Memo\\n';
    
    const vendor = data.vendor || data.supplier || '';
    const date = data.date || data.invoice_date || '';
    const amount = data.total || data.totalAmount || 0;
    
    csv += `"${vendor}","${date}","${amount}","Accounts Payable","Invoice ${data.invoiceNumber || data.invoice_number || ''}"\\n`;
    
    downloadFile(csv, `quickbooks_${doc.id || 'export'}.csv`, 'text/csv');
}

// 导出 IIF 格式
function exportIIF(data, doc) {
    const vendor = data.vendor || data.supplier || '';
    const date = data.date || data.invoice_date || '';
    const amount = data.total || data.totalAmount || 0;
    const invoiceNum = data.invoiceNumber || data.invoice_number || '';
    
    let iif = '!TRNS\\tTRNSID\\tTRNSTYPE\\tDATE\\tACCNT\\tNAME\\tAMOUNT\\tMEMO\\n';
    iif += `TRNS\\t\\tBILL\\t${date}\\tAccounts Payable\\t${vendor}\\t${amount}\\tInvoice ${invoiceNum}\\n`;
    iif += 'ENDTRNS\\n';
    
    downloadFile(iif, `invoice_${doc.id || 'export'}.iif`, 'text/plain');
}

// 导出 QBO 格式
function exportQBO(data, doc) {
    const date = (data.date || data.invoice_date || '').replace(/-/g, '');
    const amount = data.total || data.totalAmount || 0;
    const vendor = data.vendor || data.supplier || '';
    
    let qbo = `OFXHEADER:100\\n`;
    qbo += `DATA:OFXSGML\\n`;
    qbo += `VERSION:102\\n`;
    qbo += `<OFX>\\n`;
    qbo += `<SIGNONMSGSRSV1><SONRS><STATUS><CODE>0<SEVERITY>INFO</STATUS></SONRS></SIGNONMSGSRSV1>\\n`;
    qbo += `<BANKMSGSRSV1><STMTTRNRS><TRNUID>1</TRNUID><STATUS><CODE>0<SEVERITY>INFO</STATUS>\\n`;
    qbo += `<STMTRS><CURDEF>USD<BANKACCTFROM><BANKID>000000000<ACCTID>000000000</BANKACCTFROM>\\n`;
    qbo += `<BANKTRANLIST><DTSTART>${date}<DTEND>${date}\\n`;
    qbo += `<STMTTRN><TRNTYPE>DEBIT<DTPOSTED>${date}<TRNAMT>${amount}<FITID>1<NAME>${vendor}</STMTTRN>\\n`;
    qbo += `</BANKTRANLIST></STMTRS></STMTTRNRS></BANKMSGSRSV1></OFX>`;
    
    downloadFile(qbo, `invoice_${doc.id || 'export'}.qbo`, 'application/x-ofx');
}

// 下载文件
function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('✅ 已下载:', filename);
}
'''
    
    content += export_function
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已添加 exportDocument 函数到 {file_path}")
    return True

def main():
    print("🔧 为 document-detail-new.js 添加导出功能...\n")
    
    print("=" * 60)
    print("添加 exportDocument 函数")
    print("=" * 60)
    
    add_export_document_function()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 添加的功能：")
    print("• exportDocument() - 主导出函数")
    print("• exportBankStatementCSV() - 导出银行对账单")
    print("• exportInvoiceSummaryCSV() - 导出发票汇总")
    print("• exportInvoiceDetailedCSV() - 导出发票详情")
    print("• exportXeroCSV() - 导出 Xero 格式")
    print("• exportQuickBooksCSV() - 导出 QuickBooks 格式")
    print("• exportIIF() - 导出 IIF 格式")
    print("• exportQBO() - 导出 QBO 格式")
    print("• downloadFile() - 文件下载辅助函数")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存")
    print("2. 访问 document-detail 页面")
    print("3. 点击 Export 按钮")
    print("4. 应该能看到完整的导出选项")
    print("5. 点击任意选项应该能下载文件")

if __name__ == '__main__':
    main()

