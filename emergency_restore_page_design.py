#!/usr/bin/env python3
"""
🔥 紧急恢复：移除我添加的所有代码，恢复原始设计

然后只做最小的Export菜单修改
"""

import os
import re

def clean_added_code():
    """移除我添加的代码"""
    
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
        
        original_length = len(content)
        
        # 1. 移除我添加的 exportMenu HTML（在body末尾）
        # 查找 "<!-- 🔥 Export Menu（独立容器，与 firstproject.html 完全相同）-->"
        pattern1 = r'<!-- 🔥 Export Menu（独立容器，与 firstproject\.html 完全相同）-->.*?</div>\s*\n\s*<!-- Export Menu 背景遮罩 -->.*?</div>'
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        
        # 2. 移除我添加的 CSS
        pattern2 = r'<style>\s*/\* Export Menu 样式.*?</style>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        # 3. 移除我添加的 JavaScript（最后一个 <script> 标签）
        # 查找包含 "// 🔥 Export 功能 - 完整复制自 firstproject.html" 的script
        pattern3 = r'<script>\s*// 🔥 Export 功能.*?</script>'
        content = re.sub(pattern3, '', content, flags=re.DOTALL)
        
        # 4. 移除重复的 toggleExportMenu 函数定义
        # 保留第一个，删除第二个
        toggle_pattern = r'(window\.toggleExportMenu = function.*?};)'
        matches = list(re.finditer(toggle_pattern, content, re.DOTALL))
        
        if len(matches) > 1:
            # 删除第二个及之后的所有匹配
            for match in reversed(matches[1:]):
                content = content[:match.start()] + content[match.end():]
                print(f"  删除了重复的 toggleExportMenu 定义")
        
        new_length = len(content)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已清理 {html_file}")
        print(f"   原始大小: {original_length} 字节")
        print(f"   清理后: {new_length} 字节")
        print(f"   删除了: {original_length - new_length} 字节")

def main():
    print("🔥 紧急恢复 document-detail.html 原始设计\n")
    
    print("=" * 60)
    print("移除我添加的代码...")
    print("=" * 60)
    
    clean_added_code()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成：")
    print("• 移除了重复的 exportMenu HTML")
    print("• 移除了重复的 CSS")
    print("• 移除了重复的 JavaScript")
    print("• 移除了重复的函数定义")
    
    print("\n🎯 下一步：")
    print("1. 刷新页面，确认设计已恢复正常")
    print("2. 然后告诉我，我会做更精确的Export菜单修改")
    print("3. 这次只会修改Export菜单的显示逻辑，不会改变页面设计")

if __name__ == '__main__':
    main()

