#!/usr/bin/env python3
"""
🔥 重新建立 Export 功能 - 全新简单版本

策略：
1. 创建一个新的独立Export按钮
2. 使用完全内联的JavaScript（不依赖外部函数）
3. 简单的弹窗菜单
4. 基本的CSV导出功能
"""

import os

def create_new_export_button():
    """在所有 document-detail.html 添加新的独立Export按钮"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 不同语言的文字
    texts = {
        'en/document-detail.html': {
            'title': 'Export Options',
            'csv': 'Standard CSV',
            'xero': 'Xero CSV',
            'qb': 'QuickBooks CSV',
            'qbo': 'QBO Format',
            'close': 'Close'
        },
        'jp/document-detail.html': {
            'title': 'エクスポートオプション',
            'csv': '標準 CSV',
            'xero': 'Xero CSV',
            'qb': 'QuickBooks CSV',
            'qbo': 'QBO形式',
            'close': '閉じる'
        },
        'kr/document-detail.html': {
            'title': '내보내기 옵션',
            'csv': '표준 CSV',
            'xero': 'Xero CSV',
            'qb': 'QuickBooks CSV',
            'qbo': 'QBO 형식',
            'close': '닫기'
        },
        'document-detail.html': {
            'title': '匯出選項',
            'csv': '標準 CSV',
            'xero': 'Xero CSV',
            'qb': 'QuickBooks CSV',
            'qbo': 'QBO 格式',
            'close': '關閉'
        }
    }
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        text = texts.get(html_file, texts['en/document-detail.html'])
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在 </body> 前添加新的Export按钮和脚本
        new_export_code = f'''
    <!-- 🔥 新的独立 Export 功能 -->
    <button id="newExportBtn" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999999;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 15px 40px rgba(102, 126, 234, 0.5)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(102, 126, 234, 0.4)';">
        <i class="fas fa-download"></i>
        <span>New Export</span>
    </button>
    
    <div id="newExportMenu" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 999998; background: rgba(0,0,0,0.5);">
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 16px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            width: 90%;
            max-width: 400px;
            padding: 2rem;
        ">
            <h2 style="margin: 0 0 1.5rem 0; font-size: 1.5rem; color: #1f2937; text-align: center;">{text['title']}</h2>
            
            <button onclick="newExportCSV()" style="width: 100%; text-align: left; padding: 1rem; margin-bottom: 0.75rem; border: 2px solid #e5e7eb; background: white; cursor: pointer; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: all 0.2s; font-size: 1rem;" onmouseover="this.style.borderColor='#10b981'; this.style.background='#f0fdf4';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='white';">
                <div style="width: 40px; height: 40px; background: #10b981; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-file-csv" style="color: white; font-size: 1.2rem;"></i>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{text['csv']}</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">Universal format</div>
                </div>
            </button>
            
            <button onclick="newExportXero()" style="width: 100%; text-align: left; padding: 1rem; margin-bottom: 0.75rem; border: 2px solid #e5e7eb; background: white; cursor: pointer; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: all 0.2s; font-size: 1rem;" onmouseover="this.style.borderColor='#2563eb'; this.style.background='#eff6ff';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='white';">
                <div style="width: 40px; height: 40px; background: #2563eb; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-file-csv" style="color: white; font-size: 1.2rem;"></i>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{text['xero']}</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">Xero software</div>
                </div>
            </button>
            
            <button onclick="newExportQB()" style="width: 100%; text-align: left; padding: 1rem; margin-bottom: 0.75rem; border: 2px solid #e5e7eb; background: white; cursor: pointer; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: all 0.2s; font-size: 1rem;" onmouseover="this.style.borderColor='#059669'; this.style.background='#f0fdf4';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='white';">
                <div style="width: 40px; height: 40px; background: #059669; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-file-csv" style="color: white; font-size: 1.2rem;"></i>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{text['qb']}</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">QuickBooks</div>
                </div>
            </button>
            
            <button onclick="newExportQBO()" style="width: 100%; text-align: left; padding: 1rem; margin-bottom: 1.5rem; border: 2px solid #e5e7eb; background: white; cursor: pointer; border-radius: 12px; display: flex; align-items: center; gap: 1rem; transition: all 0.2s; font-size: 1rem;" onmouseover="this.style.borderColor='#8b5cf6'; this.style.background='#faf5ff';" onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='white';">
                <div style="width: 40px; height: 40px; background: #8b5cf6; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-cloud" style="color: white; font-size: 1.2rem;"></i>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1f2937;">{text['qbo']}</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">QB Online</div>
                </div>
            </button>
            
            <button onclick="closeNewExportMenu()" style="width: 100%; padding: 1rem; border: none; background: #ef4444; color: white; cursor: pointer; border-radius: 12px; font-weight: 600; font-size: 1rem; transition: all 0.2s;" onmouseover="this.style.background='#dc2626';" onmouseout="this.style.background='#ef4444';">
                {text['close']}
            </button>
        </div>
    </div>
    
    <script>
        // 打开新Export菜单
        document.getElementById('newExportBtn').addEventListener('click', function() {{
            console.log('🟢 新 Export 按钮被点击');
            document.getElementById('newExportMenu').style.display = 'block';
            document.body.style.overflow = 'hidden';
        }});
        
        // 关闭菜单
        function closeNewExportMenu() {{
            document.getElementById('newExportMenu').style.display = 'none';
            document.body.style.overflow = 'auto';
        }}
        
        // 点击背景关闭
        document.getElementById('newExportMenu').addEventListener('click', function(e) {{
            if (e.target === this) {{
                closeNewExportMenu();
            }}
        }});
        
        // 导出CSV
        function newExportCSV() {{
            console.log('📥 导出 CSV');
            closeNewExportMenu();
            
            try {{
                const doc = window.currentDocument;
                if (!doc) {{
                    alert('Document data not available');
                    return;
                }}
                
                let csv = '';
                const data = doc.processedData || {{}};
                
                // 银行对账单
                if (data.transactions && data.transactions.length > 0) {{
                    csv = 'Date,Description,Amount,Balance\\n';
                    data.transactions.forEach(t => {{
                        csv += `"${{t.date || ''}}","${{t.description || ''}}","${{t.amount || 0}}","${{t.balance || 0}}"\\n`;
                    }});
                }}
                // 发票
                else if (data.items && data.items.length > 0) {{
                    csv = 'Code,Description,Quantity,Unit Price,Amount\\n';
                    data.items.forEach(item => {{
                        csv += `"${{item.code || ''}}","${{item.description || ''}}","${{item.quantity || 0}}","${{item.unit_price || item.unitPrice || 0}}","${{item.amount || 0}}"\\n`;
                    }});
                }}
                else {{
                    csv = 'No data available';
                }}
                
                downloadFile(csv, `export_${{Date.now()}}.csv`, 'text/csv');
            }} catch(e) {{
                console.error('Export error:', e);
                alert('Export failed: ' + e.message);
            }}
        }}
        
        // 导出Xero
        function newExportXero() {{
            console.log('📥 导出 Xero');
            alert('Xero export coming soon...');
            closeNewExportMenu();
        }}
        
        // 导出QuickBooks
        function newExportQB() {{
            console.log('📥 导出 QuickBooks');
            alert('QuickBooks export coming soon...');
            closeNewExportMenu();
        }}
        
        // 导出QBO
        function newExportQBO() {{
            console.log('📥 导出 QBO');
            alert('QBO export coming soon...');
            closeNewExportMenu();
        }}
        
        // 下载文件
        function downloadFile(content, filename, mimeType) {{
            const blob = new Blob([content], {{ type: mimeType }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            console.log('✅ 已下载:', filename);
        }}
        
        console.log('✅ 新Export功能已加载');
    </script>
'''
        
        # 在 </body> 前插入
        if '</body>' in content:
            content = content.replace('</body>', new_export_code + '\n</body>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已添加新Export按钮到 {html_file}")
        else:
            print(f"⚠️  {html_file} 未找到 </body> 标签")

def main():
    print("🔥 重新建立 Export 功能...\n")
    
    print("=" * 60)
    print("创建全新的独立 Export 按钮")
    print("=" * 60)
    
    create_new_export_button()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 新Export功能特点：")
    print("• 完全独立，不依赖原有代码")
    print("• 漂亮的紫色渐变按钮（右下角）")
    print("• 现代化的弹窗菜单")
    print("• 基本的CSV导出功能")
    print("• 完全内联JavaScript（无依赖）")
    
    print("\n🔍 使用方法：")
    print("1. 刷新页面（不需要清除缓存）")
    print("2. 查看右下角的紫色 'New Export' 按钮")
    print("3. 点击按钮打开菜单")
    print("4. 选择导出格式")
    
    print("\n💡 优势：")
    print("• 立即可用，无需等待")
    print("• 绕过所有旧代码的问题")
    print("• 如果工作正常，可以替换原按钮")
    print("• 可以同时保留两个按钮，逐步迁移")

if __name__ == '__main__':
    main()

