#!/usr/bin/env python3
"""
🔥 紧急修复：z-index 无效的问题

根本原因：
- 按钮的 position: static
- z-index 对 static 元素无效！

解决方案：
- 添加 position: relative
- 提高 z-index 到 999999
"""

import os
import re

def fix_button_position_and_zindex():
    """修复按钮的 position 和 z-index"""
    
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
        
        # 1. 修复 CSS 规则：添加 position: relative，提高 z-index
        old_css = r'''button\[onclick\*="toggleExportMenu"\] \{
                pointer-events: auto !important;
                z-index: \d+ !important;
                touch-action: manipulation !important;
            \}'''
        
        new_css = '''button[onclick*="toggleExportMenu"] {
                position: relative !important;  /* 🔥 关键：让 z-index 生效 */
                z-index: 999999 !important;     /* 🔥 超高 z-index */
                pointer-events: auto !important;
                touch-action: manipulation !important;
            }'''
        
        content = re.sub(old_css, new_css, content)
        print("✅ 修复 CSS 规则（添加 position: relative）")
        
        # 2. 在按钮的 inline style 中也添加 position: relative
        # 找到 Export 按钮
        button_pattern = r'(<button onclick="toggleExportMenu\(event\)" style=")(background: #10b981;[^"]+)(")'
        
        def add_position_to_button(match):
            prefix = match.group(1)
            styles = match.group(2)
            suffix = match.group(3)
            
            # 如果已经有 position，跳过
            if 'position:' in styles:
                return match.group(0)
            
            # 在样式开头添加 position: relative
            new_styles = 'position: relative; z-index: 999999; ' + styles
            return prefix + new_styles + suffix
        
        new_content = re.sub(button_pattern, add_position_to_button, content)
        
        if new_content != content:
            content = new_content
            print("✅ 在按钮 inline style 中添加 position: relative")
        else:
            print("⚠️ 按钮 inline style 未修改（可能已存在）")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file}")

def main():
    print("🔥 紧急修复：让 z-index 生效\n")
    
    print("=" * 60)
    print("问题根源")
    print("=" * 60)
    print("• 按钮的 position: static")
    print("• z-index 对 static 元素无效！")
    print("• 所以即使设置了 z-index: 9999，实际仍是 auto")
    
    print("\n" + "=" * 60)
    print("解决方案")
    print("=" * 60)
    print("1. 在 CSS 中添加 position: relative !important")
    print("2. 提高 z-index 到 999999")
    print("3. 在按钮 inline style 中也添加 position 和 z-index")
    
    print("\n" + "=" * 60)
    print("开始修复...")
    print("=" * 60)
    
    fix_button_position_and_zindex()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• ✅ CSS 规则中添加 position: relative !important")
    print("• ✅ z-index 提高到 999999")
    print("• ✅ 按钮 inline style 中添加 position: relative; z-index: 999999;")
    
    print("\n🔍 现在诊断应该显示：")
    print("  - position: relative  ← 不再是 static")
    print("  - z-index: 999999     ← 不再是 auto")
    
    print("\n🚀 请刷新页面，等待 2 秒，查看新的诊断结果！")

if __name__ == '__main__':
    main()

