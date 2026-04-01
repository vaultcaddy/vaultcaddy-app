#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为所有HTML页面添加语言选择器
Add Language Selector to All HTML Pages
"""

import os
import re
from pathlib import Path

# 需要处理的HTML文件列表
HTML_FILES = [
    'auth.html',
    'dashboard.html',
    'account.html',
    'billing.html',
    'firstproject.html',
    'document-detail.html',
    'privacy.html',
    'terms.html',
    'forgot-password.html',
    'blog/index.html'
]

def add_language_selector_to_file(filepath):
    """为单个HTML文件添加语言选择器"""
    print(f"\n处理文件: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 1. 检查是否已经添加了语言选择器
        if 'language-selector-desktop' in content:
            print(f"  ⏭️  已存在语言选择器，跳过")
            return
        
        # 2. 在桌面导航栏中添加语言选择器（在 user-menu 之前）
        # 查找 user-menu 或 user-avatar
        desktop_pattern = r'(<div id="user-menu"[^>]*>|<div id="user-avatar"[^>]*>)'
        if re.search(desktop_pattern, content):
            replacement = r'<!-- 🌍 桌面版語言選擇器 -->\n            <div id="language-selector-desktop"></div>\n            \1'
            content = re.sub(desktop_pattern, replacement, content, count=1)
            modified = True
            print(f"  ✅ 添加桌面版语言选择器")
        
        # 3. 在手机侧边栏中添加语言选择器
        # 查找 mobile-sidebar 中的分隔线
        mobile_pattern = r'(<div style="height: 1px; background: #e5e7eb; margin: 1rem 0;"></div>)'
        matches = list(re.finditer(mobile_pattern, content))
        
        if len(matches) >= 1:
            # 在第一个分隔线后添加语言选择器
            first_match = matches[0]
            insert_pos = first_match.end()
            
            mobile_selector = '''
                
                <!-- 🌍 手機版語言選擇器 -->
                <div id="language-selector-mobile" style="padding: 0 0.5rem; margin-bottom: 1rem;"></div>
                
                <div style="height: 1px; background: #e5e7eb; margin: 1rem 0;"></div>'''
            
            content = content[:insert_pos] + mobile_selector + content[insert_pos:]
            modified = True
            print(f"  ✅ 添加手机版语言选择器")
        
        # 4. 在 </body> 之前添加 language-selector.js 引用
        if 'language-selector.js' not in content:
            body_end_pattern = r'(</body>)'
            script_tag = '    \n    <!-- 🌍 語言選擇器 -->\n    <script src="language-selector.js?v=20251205"></script>\n\n'
            
            # 对于blog页面，路径需要调整
            if 'blog/' in str(filepath):
                script_tag = '    \n    <!-- 🌍 語言選擇器 -->\n    <script src="../language-selector.js?v=20251205"></script>\n\n'
            
            content = re.sub(body_end_pattern, script_tag + r'\1', content)
            modified = True
            print(f"  ✅ 添加 language-selector.js 引用")
        
        # 5. 保存修改
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  💾 文件已保存")
        else:
            print(f"  ⚠️  未做任何修改")
            
    except Exception as e:
        print(f"  ❌ 错误: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🌍 批量添加语言选择器")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    
    for html_file in HTML_FILES:
        filepath = base_dir / html_file
        if filepath.exists():
            add_language_selector_to_file(filepath)
        else:
            print(f"\n⚠️  文件不存在: {filepath}")
    
    print("\n" + "=" * 60)
    print("✅ 批量处理完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()

