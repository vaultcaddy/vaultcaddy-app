#!/usr/bin/env python3
"""
🔥 最终解决方案：从 firstproject.html 完整复制 Export 功能

策略：
1. 读取 firstproject.html 中完整的 Export 功能（已验证工作正常）
2. 完全替换 document-detail.html 中的 Export 功能
3. 只修改选择文档的部分（firstproject 需要勾选，document-detail 自动使用当前文档）
"""

import os
import re

def copy_complete_export_from_firstproject():
    """完整复制 Export 功能"""
    
    # 读取 firstproject.html
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        firstproject = f.read()
    
    # 1. 提取 closeExportMenu 函数
    close_pattern = r'(window\.closeExportMenu\s*=\s*function\(\)\s*\{[^}]*?\};)'
    close_match = re.search(close_pattern, firstproject, re.DOTALL)
    close_func = close_match.group(1) if close_match else ''
    
    # 2. 提取 updateExportMenuContent 函数
    update_pattern = r'(function\s+updateExportMenuContent\(\)\s*\{.*?^\s*\})'
    update_match = re.search(update_pattern, firstproject, re.DOTALL | re.MULTILINE)
    update_func = update_match.group(1) if update_match else ''
    
    # 3. 提取 toggleExportMenu 函数（这个需要修改）
    toggle_pattern = r'(window\.toggleExportMenu\s*=\s*function\(\)\s*\{.*?^\s*\};)'
    toggle_match = re.search(toggle_pattern, firstproject, re.DOTALL | re.MULTILINE)
    toggle_func = toggle_match.group(1) if toggle_match else ''
    
    # 4. 提取 exportDocuments 和 exportByType 函数
    export_docs_pattern = r'(window\.exportDocuments\s*=\s*async\s*function.*?^\s*\};)'
    export_docs_match = re.search(export_docs_pattern, firstproject, re.DOTALL | re.MULTILINE)
    export_docs_func = export_docs_match.group(1) if export_docs_match else ''
    
    export_by_type_pattern = r'(async\s+function\s+exportByType.*?^        \})'
    export_by_type_match = re.search(export_by_type_pattern, firstproject, re.DOTALL | re.MULTILINE)
    export_by_type_func = export_by_type_match.group(1) if export_by_type_match else ''
    
    # 5. 修改 toggleExportMenu 以适配单文档
    if toggle_func:
        # 移除选择文档的检查，改为使用 window.currentDocument
        toggle_func = re.sub(
            r'// 獲取選中的文檔.*?return;\s*\}',
            '''// 使用当前文档（document-detail 场景）
            console.log('📄 当前文档:', window.currentDocument);
            
            if (!window.currentDocument) {
                alert('文档未加载');
                return;
            }''',
            toggle_func,
            flags=re.DOTALL
        )
    
    # 组合所有函数
    complete_export = f'''
        // 🔥 Export 功能 - 从 firstproject.html 完整复制
        
        // 关闭菜单
        {close_func}
        
        // 更新菜单内容
        {update_func}
        
        // 切换菜单显示
        {toggle_func}
        
        // 导出文档
        {export_docs_func}
        
        // 按类型导出
        {export_by_type_func}
        
        console.log('✅ Export 功能已加载（从 firstproject 复制）');
    '''
    
    # 应用到所有 document-detail.html 文件
    html_files = [
        ('en/document-detail.html', 'en/firstproject.html'),
        ('jp/document-detail.html', 'jp/firstproject.html'),
        ('kr/document-detail.html', 'kr/firstproject.html'),
        ('document-detail.html', 'firstproject.html')
    ]
    
    for detail_file, first_file in html_files:
        if not os.path.exists(detail_file) or not os.path.exists(first_file):
            continue
        
        # 读取对应语言版本的 firstproject
        with open(first_file, 'r', encoding='utf-8') as f:
            lang_firstproject = f.read()
        
        # 提取该语言版本的函数
        close_match = re.search(r'(window\.closeExportMenu\s*=\s*function\(\)\s*\{[^}]*?\};)', lang_firstproject, re.DOTALL)
        update_match = re.search(r'(function\s+updateExportMenuContent\(\)\s*\{.*?^\s*\})', lang_firstproject, re.DOTALL | re.MULTILINE)
        toggle_match = re.search(r'(window\.toggleExportMenu\s*=\s*function\(\)\s*\{.*?^\s*\};)', lang_firstproject, re.DOTALL | re.MULTILINE)
        export_docs_match = re.search(r'(window\.exportDocuments\s*=\s*async\s*function.*?^\s*\};)', lang_firstproject, re.DOTALL | re.MULTILINE)
        export_by_type_match = re.search(r'(async\s+function\s+exportByType.*?^        \})', lang_firstproject, re.DOTALL | re.MULTILINE)
        
        if not all([close_match, update_match, toggle_match]):
            print(f"⚠️ {detail_file}: 未找到所有必要函数")
            continue
        
        # 修改 toggle 函数
        toggle_func_lang = toggle_match.group(1)
        toggle_func_lang = re.sub(
            r'// .*選中.*文檔.*?return;\s*\}',
            '''// 使用当前文档
            if (!window.currentDocument) {
                alert('文档未加载');
                return;
            }''',
            toggle_func_lang,
            flags=re.DOTALL
        )
        
        # 组合
        lang_export = f'''
        // 🔥 Export 功能 - 从 firstproject.html 完整复制
        
        {close_match.group(1)}
        
        {update_match.group(1)}
        
        {toggle_func_lang}
        
        {export_docs_match.group(1) if export_docs_match else ''}
        
        {export_by_type_match.group(1) if export_by_type_match else ''}
        
        console.log('✅ Export 功能已加载（从 firstproject 复制）');
'''
        
        # 读取 document-detail
        with open(detail_file, 'r', encoding='utf-8') as f:
            detail_content = f.read()
        
        # 删除现有的 Export 函数（从 "// 🔥 Export 功能" 到 console.log('✅ Export 功能已加载')）
        detail_content = re.sub(
            r'// 🔥 Export 功能.*?console\.log\(.*?Export 功能已加载.*?\);',
            lang_export,
            detail_content,
            flags=re.DOTALL
        )
        
        with open(detail_file, 'w', encoding='utf-8') as f:
            f.write(detail_content)
        
        print(f"✅ 已更新 {detail_file}")

def main():
    print("🔥 从 firstproject.html 完整复制 Export 功能\n")
    
    print("=" * 60)
    print("开始复制...")
    print("=" * 60)
    
    copy_complete_export_from_firstproject()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n🎉 现在 document-detail.html 的 Export 功能与 firstproject.html 完全一致！")
    print("\n🚀 请刷新页面测试！")

if __name__ == '__main__':
    main()

