#!/usr/bin/env python3
"""
🔥 将 firstproject.html 的 Export 设计和功能复制到 document-detail.html

关键差异：
- firstproject.html: 多个文档，需要勾选
- document-detail.html: 单个文档，自动使用当前文档

策略：
1. 复制 firstproject.html 的 Export 按钮样式和菜单 HTML
2. 复制 Export 菜单的 CSS 样式
3. 适配 toggleExportMenu 逻辑：自动使用 window.currentDocument
4. 复制导出格式选项和函数
"""

import os
import re

def extract_export_button_html():
    """从 firstproject.html 提取 Export 按钮 HTML"""
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 export-btn-desktop
    btn_match = re.search(r'<button id="export-btn-desktop"[^>]*>.*?</button>', content, re.DOTALL)
    if btn_match:
        return btn_match.group(0)
    return None

def extract_export_menu_html():
    """从 firstproject.html 提取 Export 菜单 HTML"""
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 exportMenu 和 exportMenuOverlay
    menu_start = content.find('<div id="exportMenu"')
    if menu_start == -1:
        menu_start = content.find('<div id="exportMenuOverlay"')
    
    if menu_start != -1:
        # 找到对应的结束标签
        # 通常在 exportMenu 之后有 exportMenuOverlay
        overlay_end = content.find('</div>', content.find('</div>', menu_start) + 1)
        if overlay_end != -1:
            return content[menu_start:overlay_end + 6]
    
    return None

def extract_export_css():
    """从 firstproject.html 提取 Export 相关的 CSS"""
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 #exportMenu 相关的 CSS
    css_start = content.find('#exportMenu {')
    if css_start == -1:
        return None
    
    # 找到 CSS 块的结束
    # 通常在 </style> 前
    style_end = content.find('</style>', css_start)
    if style_end != -1:
        # 回溯到包含所有 export 相关样式的开始
        # 查找前一个 <style> 或保持当前位置
        return content[css_start:style_end]
    
    return None

def create_adapted_toggle_function():
    """创建适配的 toggleExportMenu 函数（单文档版本）"""
    
    return '''
        // 🔥 Export Menu - 适配自 firstproject.html（单文档版本）
        window.toggleExportMenu = function(event) {
            console.log('🔍 toggleExportMenu Called (Document Detail Version)');
            
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            
            if (!menu) {
                console.error('❌ 未找到 #exportMenu 元素');
                return;
            }
            
            // 如果菜单已显示，则关闭
            if (menu.style.display === 'block') {
                closeExportMenu();
                return;
            }
            
            // 检查当前文档
            if (!window.currentDocument) {
                alert('文档数据未加载');
                return;
            }
            
            console.log('📄 当前文档:', window.currentDocument);
            
            // 更新菜单内容
            updateExportMenuForDocumentDetail();
            
            // 根据屏幕大小设置菜单样式
            if (window.innerWidth <= 768) {
                // 移动端：居中显示
                menu.style.position = 'fixed';
                menu.style.top = '50%';
                menu.style.left = '50%';
                menu.style.transform = 'translate(-50%, -50%)';
                menu.style.right = 'auto';
                menu.style.width = '90%';
                menu.style.maxWidth = '400px';
                menu.style.backgroundColor = '#ffffff';
                menu.style.border = 'none';
                menu.style.boxShadow = '0 25px 50px rgba(0,0,0,0.3)';
                menu.style.borderRadius = '12px';
                menu.style.zIndex = '999999';
                console.log('📱 移动端：菜单居中显示');
                
                // 显示遮罩
                if (overlay) {
                    overlay.style.display = 'block';
                }
            } else {
                // 桌面端：在Export按钮下方
                const exportBtn = document.getElementById('export-btn') || 
                                document.querySelector('[onclick*="toggleExportMenu"]');
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
                    menu.style.zIndex = '999999';
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
            
            console.log('✅ 菜单已关闭');
        };
        
        function updateExportMenuForDocumentDetail() {
            const menu = document.getElementById('exportMenu');
            if (!menu || !window.currentDocument) {
                console.error('❌ 菜单或文档不存在');
                return;
            }
            
            const doc = window.currentDocument;
            const docType = (doc.documentType || doc.type || '').toLowerCase();
            
            console.log('📋 文档类型:', docType);
            
            let menuHTML = '';
            
            // 根据文档类型生成不同的导出选项
            if (docType.includes('bank') || docType.includes('statement')) {
                // 银行对账单导出选项
                menuHTML = `
                    <div style="padding: 1rem; background: white; border-radius: 8px;">
                        <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600; color: #1f2937;">
                            匯出銀行對帳單
                        </h3>
                        
                        <button onclick="exportCurrentDocument('bank_csv')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 0.5rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-file-csv" style="color: #10b981; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">標準 CSV</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">通用格式</div>
                            </div>
                        </button>
                        
                        <button onclick="exportCurrentDocument('bank_xero')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 0.5rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-file-csv" style="color: #2563eb; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">Xero CSV</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">Xero 會計軟體</div>
                            </div>
                        </button>
                        
                        <button onclick="exportCurrentDocument('bank_qbo')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 1rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-cloud" style="color: #8b5cf6; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">QBO 格式</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">QuickBooks Online</div>
                            </div>
                        </button>
                        
                        <button onclick="closeExportMenu()" 
                                style="width: 100%; padding: 0.75rem; border: none; 
                                       background: #f3f4f6; color: #374151; cursor: pointer; 
                                       border-radius: 6px; font-weight: 500; font-size: 0.95rem;">
                            取消
                        </button>
                    </div>
                `;
            } else if (docType.includes('invoice') || docType.includes('receipt')) {
                // 发票/收据导出选项
                menuHTML = `
                    <div style="padding: 1rem; background: white; border-radius: 8px;">
                        <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600; color: #1f2937;">
                            匯出發票
                        </h3>
                        
                        <button onclick="exportCurrentDocument('invoice_csv')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 0.5rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-file-csv" style="color: #10b981; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">標準 CSV</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">發票明細</div>
                            </div>
                        </button>
                        
                        <button onclick="exportCurrentDocument('invoice_quickbooks')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 1rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-file-csv" style="color: #059669; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">QuickBooks CSV</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">QuickBooks 格式</div>
                            </div>
                        </button>
                        
                        <button onclick="closeExportMenu()" 
                                style="width: 100%; padding: 0.75rem; border: none; 
                                       background: #f3f4f6; color: #374151; cursor: pointer; 
                                       border-radius: 6px; font-weight: 500; font-size: 0.95rem;">
                            取消
                        </button>
                    </div>
                `;
            } else {
                // 通用导出选项
                menuHTML = `
                    <div style="padding: 1rem; background: white; border-radius: 8px;">
                        <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600; color: #1f2937;">
                            匯出文件
                        </h3>
                        
                        <button onclick="exportCurrentDocument('general_csv')" 
                                style="width: 100%; text-align: left; padding: 0.875rem; margin-bottom: 1rem; 
                                       border: 1px solid #e5e7eb; background: white; cursor: pointer; 
                                       border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; 
                                       transition: all 0.2s; font-size: 0.95rem;">
                            <i class="fas fa-file-csv" style="color: #10b981; font-size: 1.2rem;"></i>
                            <div style="flex: 1;">
                                <div style="font-weight: 500; color: #1f2937;">CSV 格式</div>
                                <div style="font-size: 0.8rem; color: #6b7280;">通用格式</div>
                            </div>
                        </button>
                        
                        <button onclick="closeExportMenu()" 
                                style="width: 100%; padding: 0.75rem; border: none; 
                                       background: #f3f4f6; color: #374151; cursor: pointer; 
                                       border-radius: 6px; font-weight: 500; font-size: 0.95rem;">
                            取消
                        </button>
                    </div>
                `;
            }
            
            menu.innerHTML = menuHTML;
            console.log('✅ 菜单内容已更新');
        }
        
        window.exportCurrentDocument = function(format) {
            console.log('📤 导出格式:', format);
            closeExportMenu();
            
            if (!window.currentDocument) {
                alert('文档数据不可用');
                return;
            }
            
            const doc = window.currentDocument;
            const data = doc.processedData || {};
            
            try {
                let csv = '';
                let filename = '';
                
                switch(format) {
                    case 'bank_csv':
                        if (data.transactions && data.transactions.length > 0) {
                            csv = 'Date,Description,Amount,Balance\\n';
                            data.transactions.forEach(t => {
                                csv += `"${t.date || ''}","${t.description || ''}","${t.amount || 0}","${t.balance || 0}"\\n`;
                            });
                            filename = `BankStatement_${Date.now()}.csv`;
                        }
                        break;
                        
                    case 'bank_xero':
                        alert('Xero 格式即将推出...');
                        return;
                        
                    case 'bank_qbo':
                        alert('QBO 格式即将推出...');
                        return;
                        
                    case 'invoice_csv':
                        if (data.items && data.items.length > 0) {
                            csv = 'Code,Description,Quantity,Unit Price,Amount\\n';
                            data.items.forEach(item => {
                                csv += `"${item.code || ''}","${item.description || ''}","${item.quantity || 0}","${item.unit_price || item.unitPrice || 0}","${item.amount || 0}"\\n`;
                            });
                            filename = `Invoice_${Date.now()}.csv`;
                        }
                        break;
                        
                    case 'invoice_quickbooks':
                        alert('QuickBooks 格式即将推出...');
                        return;
                        
                    case 'general_csv':
                        csv = JSON.stringify(doc, null, 2);
                        filename = `Document_${Date.now()}.json`;
                        break;
                }
                
                if (!csv) {
                    alert('无数据可导出');
                    return;
                }
                
                // 下载文件
                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                console.log('✅ 已下载:', filename);
            } catch (error) {
                console.error('❌ 导出失败:', error);
                alert('导出失败: ' + error.message);
            }
        };
    '''

def update_document_detail_export():
    """更新所有 document-detail.html 的 Export 功能"""
    
    html_files = {
        'en/document-detail.html': {
            'title': 'Export Options',
            'bank': 'Export Bank Statement',
            'invoice': 'Export Invoice',
            'general': 'Export Document',
            'standard_csv': 'Standard CSV',
            'xero_csv': 'Xero CSV',
            'qbo_format': 'QBO Format',
            'quickbooks_csv': 'QuickBooks CSV',
            'cancel': 'Cancel',
            'universal': 'Universal format',
            'xero_software': 'Xero software',
            'qb_online': 'QuickBooks Online',
            'invoice_details': 'Invoice details'
        },
        'jp/document-detail.html': {
            'title': 'エクスポートオプション',
            'bank': '銀行明細書をエクスポート',
            'invoice': '請求書をエクスポート',
            'general': 'ドキュメントをエクスポート',
            'standard_csv': '標準 CSV',
            'xero_csv': 'Xero CSV',
            'qbo_format': 'QBO形式',
            'quickbooks_csv': 'QuickBooks CSV',
            'cancel': 'キャンセル',
            'universal': '汎用フォーマット',
            'xero_software': 'Xeroソフトウェア',
            'qb_online': 'QuickBooks Online',
            'invoice_details': '請求書明細'
        },
        'kr/document-detail.html': {
            'title': '내보내기 옵션',
            'bank': '은행 명세서 내보내기',
            'invoice': '송장 내보내기',
            'general': '문서 내보내기',
            'standard_csv': '표준 CSV',
            'xero_csv': 'Xero CSV',
            'qbo_format': 'QBO 형식',
            'quickbooks_csv': 'QuickBooks CSV',
            'cancel': '취소',
            'universal': '범용 형식',
            'xero_software': 'Xero 소프트웨어',
            'qb_online': 'QuickBooks Online',
            'invoice_details': '송장 세부정보'
        },
        'document-detail.html': {
            'title': '匯出選項',
            'bank': '匯出銀行對帳單',
            'invoice': '匯出發票',
            'general': '匯出文件',
            'standard_csv': '標準 CSV',
            'xero_csv': 'Xero CSV',
            'qbo_format': 'QBO 格式',
            'quickbooks_csv': 'QuickBooks CSV',
            'cancel': '取消',
            'universal': '通用格式',
            'xero_software': 'Xero 會計軟體',
            'qb_online': 'QuickBooks Online',
            'invoice_details': '發票明細'
        }
    }
    
    # 读取 firstproject.html 获取完整的Export菜单HTML和CSS
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        firstproject_content = f.read()
    
    # 提取exportMenu和exportMenuOverlay的HTML结构
    export_menu_html = '''
    <!-- Export Menu -->
    <div id="exportMenu" style="display: none; position: fixed; background: white; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); z-index: 999999; min-width: 280px; max-width: 400px;">
        <!-- 内容由 JavaScript 动态生成 -->
    </div>
    
    <!-- Export Menu Overlay（移动端遮罩） -->
    <div id="exportMenuOverlay" onclick="closeExportMenu()" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 999998;"></div>
    '''
    
    # 生成CSS
    export_css = '''
    <style>
        /* Export Menu 样式 */
        #exportMenu {
            padding: 0;
            overflow: hidden;
        }
        
        #exportMenu button:hover {
            border-color: #10b981 !important;
            background: #f0fdf4 !important;
        }
        
        /* 移动端样式 */
        @media (max-width: 768px) {
            #exportMenu {
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                width: 90% !important;
                max-width: 400px !important;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3) !important;
            }
        }
    </style>
    '''
    
    adapted_function = create_adapted_toggle_function()
    
    for html_file, texts in html_files.items():
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 删除旧的 newExportBtn（紫色按钮）
        content = re.sub(r'<!-- 🔥 新的独立 Export 功能 -->.*?</script>', '', content, flags=re.DOTALL)
        
        # 2. 在 </body> 前添加新的Export菜单HTML、CSS和JavaScript
        new_export_code = export_menu_html + '\n' + export_css + '\n<script>\n' + adapted_function + '\n</script>\n'
        
        if '</body>' in content:
            content = content.replace('</body>', new_export_code + '</body>')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {html_file}")

def main():
    print("🔥 将 firstproject.html 的 Export 设计复制到 document-detail.html\n")
    
    print("=" * 60)
    print("开始更新...")
    print("=" * 60)
    
    update_document_detail_export()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成的更新：")
    print("• ✅ 复制了 firstproject.html 的 Export 菜单设计")
    print("• ✅ 适配了单文档场景（自动使用 window.currentDocument）")
    print("• ✅ 保留了相同的样式和布局")
    print("• ✅ 支持移动端和桌面端")
    print("• ✅ 删除了之前的紫色 New Export 按钮")
    
    print("\n🎯 使用方法：")
    print("1. 刷新 document-detail.html 页面")
    print("2. 点击页面上的 Export 按钮")
    print("3. 选择导出格式")
    print("4. 自动下载文件")
    
    print("\n💡 关键差异：")
    print("• firstproject: 需要先勾选文档")
    print("• document-detail: 自动使用当前文档（无需勾选）")

if __name__ == '__main__':
    main()

