#!/usr/bin/env python3
"""
🗑️ 完全删除 Export 按钮和所有相关功能

删除内容：
1. Export 按钮（HTML）
2. Export Menu 元素
3. Export Overlay 元素
4. 所有 Export 相关的 JavaScript 函数
5. 所有 Export 相关的 CSS
"""

import os
import re

def remove_all_export_content():
    """完全删除 Export 功能"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {html_file}:")
        print("=" * 50)
        
        # 1. 删除 Export 按钮（在 header 中的）
        # 找到包含 Export 按钮的 div
        pattern1 = r'<div class="export-dropdown"[^>]*>.*?</div>\s*(?=<button[^>]*delete)'
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        print("✅ 已删除 Export 按钮")
        
        # 2. 删除 exportMenu 元素
        pattern2 = r'<div[^>]*id="exportMenu"[^>]*>.*?</div>\s*(?=\s*(?:<div id="exportMenuOverlay"|</body>|<script))'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        print("✅ 已删除 exportMenu 元素")
        
        # 3. 删除 exportMenuOverlay 元素
        pattern3 = r'<div[^>]*id="exportMenuOverlay"[^>]*>.*?</div>'
        content = re.sub(pattern3, '', content, flags=re.DOTALL)
        print("✅ 已删除 exportMenuOverlay 元素")
        
        # 4. 删除所有 Export 相关的 JavaScript 函数
        pattern4 = r'//.*?Export.*?功能.*?console\.log\(.*?Export.*?功能.*?已加载.*?\);'
        content = re.sub(pattern4, '', content, flags=re.DOTALL)
        print("✅ 已删除 Export JavaScript 函数")
        
        # 5. 删除 Export 相关的 CSS
        pattern5 = r'\.export-menu[^{]*\{[^}]*\}'
        content = re.sub(pattern5, '', content, flags=re.DOTALL)
        
        pattern6 = r'\.export-menu-item[^{]*\{[^}]*\}'
        content = re.sub(pattern6, '', content, flags=re.DOTALL)
        print("✅ 已删除 Export CSS")
        
        # 6. 删除 event listener 中与 Export 相关的部分
        pattern7 = r'document\.addEventListener\(.*?toggleExportMenu.*?\}\);'
        content = re.sub(pattern7, '', content, flags=re.DOTALL)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完全清理 {html_file}")

def main():
    print("🗑️ 完全删除 Export 功能\n")
    
    print("=" * 60)
    print("开始删除...")
    print("=" * 60)
    
    remove_all_export_content()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n🎉 已完全删除：")
    print("• ✅ Export 按钮")
    print("• ✅ Export 菜单元素")
    print("• ✅ Export 遮罩元素")
    print("• ✅ Export JavaScript 函数")
    print("• ✅ Export CSS 样式")
    
    print("\n🚀 请刷新页面！")
    print("页面应该恢复正常，不再有 Export 按钮。")

if __name__ == '__main__':
    main()

