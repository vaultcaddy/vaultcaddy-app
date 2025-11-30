#!/usr/bin/env python3
"""
實現智能動態 Export 菜單
根據用戶選擇的文件自動調整顯示的導出選項
"""

import re

def implement_smart_export():
    """替換 firstproject.html 的 Export 邏輯"""
    
    with open('firstproject.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 替換 Export 菜單 HTML 為空容器（動態生成）
    new_export_menu = '''<div class="dropdown" id="export-dropdown" style="position: relative;">
                            <button id="export-btn" onclick="toggleExportMenu()" style="background: #10b981; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500;">
                                <i class="fas fa-download"></i>
                                <span>Export</span>
                                <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
                            </button>
                            <div id="exportMenu" class="export-menu" style="display: none; position: absolute; top: 100%; right: 0; margin-top: 0.5rem; background: white; border: 1px solid #e5e7eb; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-width: 250px; z-index: 1000;">
                                <!-- 動態生成的菜單內容 -->
                            </div>
                        </div>'''
    
    # 找到並替換整個 Export dropdown
    content = re.sub(
        r'<div class="dropdown" id="export-dropdown"[^>]*>.*?</div>\s*</div>',
        new_export_menu,
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # 2. 找到 toggleExportMenu 函數並替換為新的智能版本
    new_toggle_function = '''function toggleExportMenu() {
            const menu = document.getElementById('exportMenu');
            const isVisible = menu.style.display === 'block';
            
            if (isVisible) {
                menu.style.display = 'none';
            } else {
                // 生成動態菜單
                generateSmartExportMenu();
                menu.style.display = 'block';
            }
        }
        
        function generateSmartExportMenu() {
            const menu = document.getElementById('exportMenu');
            const selectedDocs = Array.from(window.selectedDocuments || new Set());
            
            // 獲取選中的文檔
            let docsToAnalyze;
            if (selectedDocs.length > 0) {
                docsToAnalyze = allDocuments.filter(doc => 
                    selectedDocs.includes(doc.id) && 
                    doc.status === 'completed' && 
                    doc.processedData
                );
            } else {
                docsToAnalyze = allDocuments.filter(doc => 
                    doc.status === 'completed' && 
                    doc.processedData
                );
            }
            
            // 按類型分組
            const bankStatements = docsToAnalyze.filter(doc => {
                const type = (doc.documentType || '').toLowerCase();
                return type === 'bank_statement' || type === 'bank_statements' || type.includes('銀行');
            });
            
            const invoices = docsToAnalyze.filter(doc => {
                const type = (doc.documentType || '').toLowerCase();
                return type === 'invoice' || type === 'invoices' || type.includes('發票');
            });
            
            console.log('📊 Export 分析:', {
                total: docsToAnalyze.length,
                bankStatements: bankStatements.length,
                invoices: invoices.length,
                selected: selectedDocs.length
            });
            
            // 構建菜單 HTML
            let menuHTML = '<div style="padding: 0.5rem 0;">';
            
            // 銀行對帳單選項
            if (bankStatements.length > 0) {
                menuHTML += `
                    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">
                        銀行對帳單 (${bankStatements.length})
                    </div>
                    <button onclick="exportDocuments('bank_statement_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">標準 CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">完整欄位格式</div>
                        </div>
                    </button>
                    <button onclick="exportDocuments('xero_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #2563eb; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">Xero CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">官方最小格式</div>
                        </div>
                    </button>
                `;
            }
            
            // 分隔線（如果兩個類型都有）
            if (bankStatements.length > 0 && invoices.length > 0) {
                menuHTML += '<div style="height: 1px; background: #e5e7eb; margin: 0.5rem 0;"></div>';
            }
            
            // 發票選項
            if (invoices.length > 0) {
                menuHTML += `
                    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">
                        發票 (${invoices.length})
                    </div>
                    <button onclick="exportDocuments('invoice_summary_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #f59e0b; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">標準 CSV（總數）</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">快速對帳</div>
                        </div>
                    </button>
                    <button onclick="exportDocuments('invoice_detailed_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #f59e0b; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">完整交易數據 CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">詳細記錄</div>
                        </div>
                    </button>
                `;
            }
            
            // QuickBooks 選項（如果有任何文檔）
            if (docsToAnalyze.length > 0) {
                menuHTML += `
                    <div style="height: 1px; background: #e5e7eb; margin: 0.5rem 0;"></div>
                    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">
                        QuickBooks
                    </div>
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
            }
            
            // 如果沒有可導出的文檔
            if (docsToAnalyze.length === 0) {
                menuHTML += `
                    <div style="padding: 1.5rem; text-align: center; color: #9ca3af;">
                        <i class="fas fa-info-circle" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                        <p style="margin: 0; font-size: 0.875rem;">沒有可導出的文檔</p>
                        <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem;">請先選擇已完成處理的文檔</p>
                    </div>
                `;
            }
            
            menuHTML += '</div>';
            
            menu.innerHTML = menuHTML;
        }'''
    
    # 替換 toggleExportMenu 函數
    content = re.sub(
        r'function toggleExportMenu\(\) \{[^}]*\}',
        new_toggle_function,
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # 3. 替換 exportDocuments 函數為新的智能版本
    new_export_function = '''window.exportDocuments = async function(format) {
            console.log('📤 開始導出:', format);
            
            try {
                // 獲取選中的文檔
                const selectedDocs = Array.from(window.selectedDocuments || new Set());
                
                let docsToExport;
                if (selectedDocs.length > 0) {
                    docsToExport = allDocuments.filter(doc => 
                        selectedDocs.includes(doc.id) && 
                        doc.status === 'completed' && 
                        doc.processedData
                    );
                } else {
                    docsToExport = allDocuments.filter(doc => 
                        doc.status === 'completed' && 
                        doc.processedData
                    );
                }
                
                if (docsToExport.length === 0) {
                    alert('沒有可導出的文檔\\n請先選擇已完成處理的文檔');
                    return;
                }
                
                // 根據格式過濾文檔
                let filteredDocs = docsToExport;
                let exportType = '';
                
                if (format === 'bank_statement_csv' || format === 'xero_csv') {
                    // 只導出銀行對帳單
                    filteredDocs = docsToExport.filter(doc => {
                        const type = (doc.documentType || '').toLowerCase();
                        return type === 'bank_statement' || type === 'bank_statements' || type.includes('銀行');
                    });
                    exportType = '銀行對帳單';
                } else if (format === 'invoice_summary_csv' || format === 'invoice_detailed_csv') {
                    // 只導出發票
                    filteredDocs = docsToExport.filter(doc => {
                        const type = (doc.documentType || '').toLowerCase();
                        return type === 'invoice' || type === 'invoices' || type.includes('發票');
                    });
                    exportType = '發票';
                }
                
                if (filteredDocs.length === 0) {
                    alert(`沒有可導出的${exportType}\\n請確保已選擇${exportType}文檔`);
                    return;
                }
                
                console.log(`✅ 準備導出 ${filteredDocs.length} 個${exportType}`);
                
                // 生成導出內容
                let exportContent = '';
                let fileName = '';
                let mimeType = 'text/csv;charset=utf-8;';
                
                switch(format) {
                    case 'bank_statement_csv':
                        exportContent = generateBankStatementCSV(filteredDocs);
                        fileName = `bank_statements_${new Date().toISOString().split('T')[0]}.csv`;
                        break;
                        
                    case 'xero_csv':
                        exportContent = generateXeroCSV(filteredDocs);
                        fileName = `xero_bank_${new Date().toISOString().split('T')[0]}.csv`;
                        break;
                        
                    case 'invoice_summary_csv':
                        exportContent = generateInvoiceSummaryCSV(filteredDocs);
                        fileName = `invoices_summary_${new Date().toISOString().split('T')[0]}.csv`;
                        break;
                        
                    case 'invoice_detailed_csv':
                        exportContent = generateInvoiceDetailedCSV(filteredDocs);
                        fileName = `invoices_detailed_${new Date().toISOString().split('T')[0]}.csv`;
                        break;
                        
                    case 'iif':
                        exportContent = generateIIF(filteredDocs);
                        fileName = `quickbooks_${new Date().toISOString().split('T')[0]}.iif`;
                        mimeType = 'text/plain;charset=utf-8;';
                        break;
                        
                    case 'qbo':
                        exportContent = generateQBO(filteredDocs);
                        fileName = `quickbooks_online_${new Date().toISOString().split('T')[0]}.qbo`;
                        mimeType = 'application/vnd.intu.qbo;charset=utf-8;';
                        break;
                        
                    default:
                        throw new Error(`不支持的格式: ${format}`);
                }
                
                // 下載文件
                const blob = new Blob([exportContent], { type: mimeType });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = fileName;
                link.click();
                URL.revokeObjectURL(link.href);
                
                // 關閉菜單
                toggleExportMenu();
                
                alert(`✅ 導出成功！\\n文件名: ${fileName}\\n文檔數量: ${filteredDocs.length}`);
                
            } catch (error) {
                console.error('❌ 導出錯誤:', error);
                alert(`導出失敗: ${error.message}`);
            }
        };'''
    
    # 替換 exportDocuments 函數
    content = re.sub(
        r'window\.exportDocuments\s*=\s*async\s*function\([^)]*\)\s*\{.*?^\s*\};',
        new_export_function,
        content,
        flags=re.MULTILINE | re.DOTALL,
        count=1
    )
    
    with open('firstproject.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已實現智能動態 Export 菜單")
    print("\n功能：")
    print("  - 根據選中文檔自動顯示相關選項")
    print("  - 只有銀行對帳單時，只顯示銀行對帳單選項")
    print("  - 只有發票時，只顯示發票選項")
    print("  - 兩者都有時，顯示所有選項")
    print("  - QuickBooks 選項始終顯示（如果有文檔）")
    print("  - 只導出選中的對應類型文檔")

if __name__ == "__main__":
    implement_smart_export()

