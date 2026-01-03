#!/usr/bin/env python3
"""
🔥 完整复制 firstproject.html 的 Export 功能到 document-detail.html

包括：
1. exportMenu 和 exportMenuOverlay 的 HTML
2. updateExportMenuContent() 函数（适配单文档）
3. toggleExportMenu() 函数（完整复制）
4. exportDocuments() 和 exportByType() 函数（适配单文档）
5. 所有 CSS 样式（移动端和桌面端）
"""

import os
import re

def get_complete_export_code_for_document_detail():
    """生成适配 document-detail.html 的完整 Export 代码"""
    
    # Export Menu HTML（与 firstproject 完全相同）
    export_menu_html = '''
<!-- 🔥 Export Menu（独立容器，与 firstproject.html 完全相同）-->
<div class="export-menu" id="exportMenu" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #ffffff !important; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); min-width: 280px; max-width: 400px; z-index: 999999; padding: 1rem; overflow: hidden;">
<!-- 动态生成内容 -->
</div>

<!-- Export Menu 背景遮罩 -->
<div id="exportMenuOverlay" onclick="closeExportMenu()" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999998;"></div>
'''
    
    # Export JavaScript（适配单文档）
    export_javascript = '''
<script>
    // 🔥 Export 功能 - 完整复制自 firstproject.html（适配单文档版本）
    
    // 🔄 更新 Export 菜单内容（适配单文档）
    function updateExportMenuContent() {
        const menu = document.getElementById('exportMenu');
        if (!menu) {
            console.error('❌ 未找到 exportMenu 元素');
            return;
        }
        
        // 获取当前文档
        const currentDoc = window.currentDocument;
        if (!currentDoc) {
            console.error('❌ 当前文档不存在');
            return;
        }
        
        // 判断文档类型
        const docType = (currentDoc.documentType || currentDoc.type || '').toLowerCase();
        console.log('📋 当前文档类型:', docType);
        
        let hasBankStatement = false;
        let hasInvoice = false;
        
        if (docType.includes('bank') || docType.includes('statement')) {
            hasBankStatement = true;
        } else if (docType.includes('invoice') || docType.includes('receipt')) {
            hasInvoice = true;
        }
        
        // 动态生成菜单内容（与 firstproject 完全相同）
        let menuHTML = '<div style="padding: 0.5rem 0; background: #ffffff;">';
        
        // Bank Statement 选项
        if (hasBankStatement) {
            menuHTML += `
                <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">Bank Statement</div>
                <button onclick="exportDocuments('bank_statement_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                    <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                    <div>
                        <div style="font-weight: 500;">Standard CSV</div>
                        <div style="font-size: 0.75rem; color: #6b7280;">complete fields Format</div>
                    </div>
                </button>
            `;
        }
        
        // Invoice 选项
        if (hasInvoice) {
            menuHTML += `
                <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">Invoice</div>
                <button onclick="exportDocuments('invoice_summary_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                    <i class="fas fa-file-invoice" style="color: #f59e0b; width: 20px;"></i>
                    <div>
                        <div style="font-weight: 500;">Standard CSV（Total）</div>
                        <div style="font-size: 0.75rem; color: #6b7280;">fast Pair account</div>
                    </div>
                </button>
                <button onclick="exportDocuments('invoice_detailed_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                    <i class="fas fa-file-invoice" style="color: #f59e0b; width: 20px;"></i>
                    <div>
                        <div style="font-weight: 500;">complete whole transaction Data CSV</div>
                        <div style="font-size: 0.75rem; color: #6b7280;">details record</div>
                    </div>
                </button>
            `;
        }
        
        // 其他选项（Xero、QuickBooks、IIF、QBO）- 始终显示
        menuHTML += `
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">Other</div>
            <button onclick="exportDocuments('xero_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-csv" style="color: #3b82f6; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">Xero CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">official Minimum Format</div>
                </div>
            </button>
            <button onclick="exportDocuments('quickbooks_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">QuickBooks CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">official Minimum Format</div>
                </div>
            </button>
            <button onclick="exportDocuments('iif')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-file-alt" style="color: #3b82f6; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">IIF</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks Desktop</div>
                </div>
            </button>
            <button onclick="exportDocuments('qbo')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                <i class="fas fa-cloud" style="color: #8b5cf6; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">QBO</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks Online</div>
                </div>
            </button>
        `;
        
        menuHTML += '</div>';
        
        // 更新菜单内容
        menu.innerHTML = menuHTML;
        console.log('✅ 菜单内容已更新');
    }
    
    // 🔄 关闭 Export 菜单（与 firstproject 完全相同）
    window.closeExportMenu = function() {
        const menu = document.getElementById('exportMenu');
        const overlay = document.getElementById('exportMenuOverlay');
        if (menu) {
            menu.style.display = 'none';
            menu.classList.remove('active');
        }
        if (overlay) {
            overlay.style.display = 'none';
        }
        console.log('🔒 菜单已关闭');
    };
    
    // 🔄 切换 Export 菜单显示/隐藏（与 firstproject 完全相同的逻辑）
    window.toggleExportMenu = function() {
        console.log('🔍 toggleExportMenu Called');
        const menu = document.getElementById('exportMenu');
        const overlay = document.getElementById('exportMenuOverlay');
        console.log('📋 菜单元素:', menu);
        
        if (!menu) {
            console.error('❌ 未找到 #exportMenu 元素');
            return;
        }
        
        // 如果菜单已显示，则关闭
        if (menu.style.display === 'block') {
            closeExportMenu();
            return;
        }
        
        // 检查当前文档（适配：不需要勾选）
        if (!window.currentDocument) {
            alert('文档数据未加载');
            return;
        }
        
        console.log('📄 当前文档已加载');
        
        // 更新菜单内容并显示
        console.log('🔄 更新菜单内容...');
        updateExportMenuContent();
        
        // 🔥 根据屏幕大小设置菜单样式（与 firstproject 完全相同）
        if (window.innerWidth <= 768) {
            // 移动端：居中显示，全白设计
            menu.style.position = 'fixed';
            menu.style.top = '50%';
            menu.style.left = '50%';
            menu.style.transform = 'translate(-50%, -50%)';
            menu.style.right = 'auto';
            menu.style.width = '90%';
            menu.style.maxWidth = '400px';
            menu.style.backgroundColor = '#ffffff'; // 🔥 白色背景
            menu.style.border = 'none'; // 🔥 无边框
            menu.style.boxShadow = 'none'; // 🔥 无阴影
            menu.style.borderRadius = '12px';
            console.log('📱 移动端：菜单居中显示（全白）');
            
            // 显示遮罩
            if (overlay) {
                overlay.style.display = 'block';
            }
        } else {
            // 桌面端：在 Export 按钮下方
            const exportBtn = document.querySelector('[onclick*="toggleExportMenu"]') || 
                            document.getElementById('export-btn');
            if (exportBtn) {
                const rect = exportBtn.getBoundingClientRect();
                menu.style.position = 'fixed';
                menu.style.top = (rect.bottom + 8) + 'px';
                menu.style.right = (window.innerWidth - rect.right) + 'px';
                menu.style.left = 'auto';
                menu.style.transform = 'none';
                menu.style.width = 'auto';
                menu.style.minWidth = '280px';
                menu.style.maxWidth = '400px';
                menu.style.backgroundColor = '#ffffff';
                menu.style.border = '1px solid #e5e7eb';
                menu.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                menu.style.borderRadius = '8px';
            }
            console.log('💻 桌面端：菜单在按钮下方');
            
            // 桌面端不显示遮罩
            if (overlay) {
                overlay.style.display = 'none';
            }
        }
        
        menu.style.display = 'block';
        menu.classList.add('active');
        
        console.log('✅ 菜单已显示');
    };
    
    // ✅ 按类型导出文档（内部辅助函数，适配单文档）
    async function exportByType(docs, format) {
        if (!docs || docs.length === 0) {
            console.log('⚠️ 无文档需要导出');
            return;
        }
        
        let exportContent = '';
        let fileName = '';
        const mimeType = 'text/csv;charset=utf-8;';
        
        switch(format) {
            case 'bank_statement_csv':
                if (window.BankStatementExport) {
                    exportContent = window.BankStatementExport.generateBankStatementCSV(docs);
                    fileName = `BankStatement_${new Date().toISOString().split('T')[0]}.csv`;
                } else {
                    // 简单版本
                    exportContent = 'Date,Description,Amount,Balance\\n';
                    docs.forEach(doc => {
                        if (doc.processedData && doc.processedData.transactions) {
                            doc.processedData.transactions.forEach(t => {
                                exportContent += `"${t.date || ''}","${t.description || ''}","${t.amount || 0}","${t.balance || 0}"\\n`;
                            });
                        }
                    });
                    fileName = `BankStatement_${new Date().toISOString().split('T')[0]}.csv`;
                }
                break;
                
            case 'invoice_summary_csv':
                if (window.InvoiceExport) {
                    exportContent = window.InvoiceExport.generateInvoiceSummaryCSV(docs);
                    fileName = `Invoice_${new Date().toISOString().split('T')[0]}.csv`;
                } else {
                    // 简单版本
                    exportContent = 'Invoice Number,Date,Vendor,Amount\\n';
                    docs.forEach(doc => {
                        if (doc.processedData) {
                            const data = doc.processedData;
                            exportContent += `"${data.invoiceNumber || ''}","${data.date || ''}","${data.vendor || ''}","${data.totalAmount || 0}"\\n`;
                        }
                    });
                    fileName = `Invoice_${new Date().toISOString().split('T')[0]}.csv`;
                }
                break;
                
            case 'invoice_detailed_csv':
                exportContent = 'Code,Description,Quantity,Unit Price,Amount\\n';
                docs.forEach(doc => {
                    if (doc.processedData && doc.processedData.items) {
                        doc.processedData.items.forEach(item => {
                            exportContent += `"${item.code || ''}","${item.description || ''}","${item.quantity || 0}","${item.unit_price || item.unitPrice || 0}","${item.amount || 0}"\\n`;
                        });
                    }
                });
                fileName = `InvoiceDetailed_${new Date().toISOString().split('T')[0]}.csv`;
                break;
                
            case 'general_csv':
                exportContent = JSON.stringify(docs, null, 2);
                fileName = `Export_${new Date().toISOString().split('T')[0]}.json`;
                break;
                
            default:
                alert(`${format} 格式即将推出...`);
                return;
        }
        
        if (!exportContent) {
            console.error('❌ 导出内容为空');
            alert('无数据可导出');
            return;
        }
        
        // 下载文件
        const blob = new Blob(['\\uFEFF' + exportContent], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        console.log(`✅ 已导出: ${fileName}`);
    }
    
    // 📤 导出文档（适配单文档）
    window.exportDocuments = async function(format) {
        console.log('📤 开始导出:', format);
        
        // 🔥 关闭菜单
        closeExportMenu();
        
        try {
            // 获取当前文档（适配：使用 window.currentDocument）
            const currentDoc = window.currentDocument;
            
            if (!currentDoc) {
                alert('文档数据未加载');
                return;
            }
            
            // 检查文档是否已处理
            if (currentDoc.status !== 'completed' || !currentDoc.processedData) {
                alert('文档尚未完成处理');
                return;
            }
            
            console.log('📋 准备导出当前文档');
            
            // 按类型分组（虽然只有一个文档，但保持与 firstproject 相同的结构）
            const groupedDocs = {
                bank_statements: [],
                invoices: [],
                receipts: [],
                general: []
            };
            
            const docType = (currentDoc.documentType || '').toLowerCase();
            if (docType === 'bank_statement' || docType === 'bank_statements') {
                groupedDocs.bank_statements.push(currentDoc);
            } else if (docType === 'invoice' || docType === 'invoices') {
                groupedDocs.invoices.push(currentDoc);
            } else if (docType === 'receipt' || docType === 'receipts') {
                groupedDocs.receipts.push(currentDoc);
            } else {
                groupedDocs.general.push(currentDoc);
            }
            
            console.log('📊 文档分组结果:', {
                bank_statements: groupedDocs.bank_statements.length,
                invoices: groupedDocs.invoices.length,
                receipts: groupedDocs.receipts.length,
                general: groupedDocs.general.length
            });
            
            // 根据格式选择合适的文档组
            let docsToExport = [];
            
            switch(format) {
                case 'bank_statement_csv':
                    docsToExport = groupedDocs.bank_statements;
                    if (docsToExport.length === 0) {
                        alert('当前文档不是银行对账单');
                        return;
                    }
                    break;
                    
                case 'invoice_summary_csv':
                case 'invoice_detailed_csv':
                    docsToExport = [...groupedDocs.invoices, ...groupedDocs.receipts];
                    if (docsToExport.length === 0) {
                        alert('当前文档不是发票或收据');
                        return;
                    }
                    break;
                    
                case 'xero_csv':
                case 'quickbooks_csv':
                case 'iif':
                case 'qbo':
                    // 这些格式支持所有类型
                    docsToExport = [currentDoc];
                    break;
                    
                case 'general_csv':
                    docsToExport = [currentDoc];
                    break;
                    
                default:
                    docsToExport = [currentDoc];
            }
            
            console.log(`📤 准备导出 ${docsToExport.length} 个文档`);
            
            // 执行导出
            await exportByType(docsToExport, format);
            
        } catch (error) {
            console.error('❌ 导出失败:', error);
            alert('导出失败: ' + error.message);
        }
    };
    
    console.log('✅ Export 功能已加载（document-detail 单文档版本）');
</script>
'''
    
    # CSS 样式（与 firstproject 完全相同）
    export_css = '''
<style>
    /* Export Menu 样式 - 与 firstproject.html 完全相同 */
    .export-menu-item:hover {
        background: #f3f4f6 !important;
    }
    
    /* 移动端样式 */
    @media (max-width: 768px) {
        #exportMenu {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            right: auto !important;
            margin: 0 !important;
            z-index: 999999 !important;
            width: 90% !important;
            max-width: 400px !important;
            background-color: #ffffff !important;
            box-shadow: none !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            overflow: hidden !important;
        }
    }
</style>
'''
    
    return export_menu_html + export_css + export_javascript

def update_all_document_detail_files():
    """更新所有 document-detail.html 文件"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    complete_export_code = get_complete_export_code_for_document_detail()
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"⚠️  {html_file} 不存在")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 删除所有旧的 Export 相关代码
        # 删除旧的 exportMenu
        content = re.sub(r'<!-- 🔥 新的独立 Export 功能 -->.*?(?=</body>)', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- 🔥 Export Menu.*?</div>\s*(?=<script|</body>)', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Export Menu -->.*?</div>\s*(?=<script|</body>)', '', content, flags=re.DOTALL)
        content = re.sub(r'<div[^>]*id="exportMenu"[^>]*>.*?</div>\s*(?=<div|<script|</body>)', '', content, flags=re.DOTALL)
        content = re.sub(r'<div[^>]*id="exportMenuOverlay"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        
        # 删除旧的 Export JavaScript
        content = re.sub(r'<script>\s*//.*?Export.*?</script>', '', content, flags=re.DOTALL)
        
        # 2. 在 </body> 前添加新的完整 Export 代码
        if '</body>' in content:
            content = content.replace('</body>', complete_export_code + '\n</body>')
        else:
            print(f"⚠️  {html_file} 未找到 </body> 标签")
            continue
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {html_file}")

def main():
    print("🔥 完整复制 firstproject.html 的 Export 功能...\n")
    
    print("=" * 60)
    print("开始更新所有 document-detail.html 文件")
    print("=" * 60)
    
    update_all_document_detail_files()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成的更新：")
    print("• ✅ exportMenu 和 exportMenuOverlay HTML（完全相同）")
    print("• ✅ updateExportMenuContent() 函数（适配单文档）")
    print("• ✅ toggleExportMenu() 函数（完全相同的逻辑）")
    print("• ✅ exportDocuments() 函数（适配单文档）")
    print("• ✅ exportByType() 函数（适配单文档）")
    print("• ✅ CSS 样式（移动端和桌面端）")
    
    print("\n🎯 关键特点：")
    print("• 设计和显示：与 firstproject 完全相同")
    print("• 菜单内容：与 firstproject 完全相同")
    print("• 响应式：支持移动端和桌面端")
    print("• 唯一区别：自动使用当前文档（无需勾选）")
    
    print("\n📱 移动端：")
    print("• 菜单居中显示")
    print("• 90% 宽度，最大 400px")
    print("• 全白背景，无边框，无阴影")
    print("• 灰色遮罩背景")
    
    print("\n💻 桌面端：")
    print("• 菜单在 Export 按钮下方")
    print("• 280-400px 宽度")
    print("• 白色背景，灰色边框，阴影效果")
    print("• 无遮罩背景")
    
    print("\n🚀 请刷新页面测试！")

if __name__ == '__main__':
    main()

