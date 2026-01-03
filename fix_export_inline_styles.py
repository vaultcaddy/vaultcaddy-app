#!/usr/bin/env python3
"""
🔥 修复 Export 菜单 - 移除冲突的 inline styles

问题：
- 静态 HTML 中的 exportMenu 有大量 inline styles
- 这些 inline styles 优先级比 JavaScript 更高
- 导致 JavaScript 设置的样式被覆盖

解决方案：
- 清空 exportMenu 的 inline style
- 只保留必要的初始样式
- 让 JavaScript 完全控制样式
"""

import os
import re

def fix_export_menu_inline_styles():
    """移除 exportMenu 和 exportMenuOverlay 的冲突 inline styles"""
    
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
        
        # 1. 替换 exportMenu 的 inline style
        # 旧的：大量 inline styles 强制居中
        old_export_menu_pattern = r'<div id="exportMenu" class="export-menu" style="[^"]*">'
        
        # 新的：只保留必要的初始样式
        new_export_menu = '<div id="exportMenu" class="export-menu" style="display: none; z-index: 999999;">'
        
        content = re.sub(old_export_menu_pattern, new_export_menu, content)
        
        # 2. 替换 exportMenuOverlay 的 inline style
        old_overlay_pattern = r'<div id="exportMenuOverlay" style="[^"]*" onclick="closeExportMenu\(\)"></div>'
        
        new_overlay = '<div id="exportMenuOverlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999998;" onclick="closeExportMenu()"></div>'
        
        content = re.sub(old_overlay_pattern, new_overlay, content)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file}")
        print(f"   - 清空了 exportMenu 的冲突 inline styles")
        print(f"   - 只保留 display: none 和 z-index")
        print(f"   - JavaScript 现在可以完全控制样式")

def main():
    print("🔥 修复 Export 菜单 inline styles 冲突\n")
    
    print("=" * 60)
    print("问题诊断")
    print("=" * 60)
    print("• 静态 HTML 中的 exportMenu 有大量 inline styles")
    print("• 包括: position, top, left, transform, background, border, etc.")
    print("• 这些 inline styles 优先级比 JavaScript 更高")
    print("• 导致无论移动端还是桌面端都强制居中")
    print("• 点击后日志没有更新 = JavaScript 设置的样式被覆盖")
    
    print("\n" + "=" * 60)
    print("解决方案")
    print("=" * 60)
    print("• 清空 exportMenu 的所有 inline styles")
    print("• 只保留 display: none 和 z-index")
    print("• 让 JavaScript 的 toggleExportMenu 完全控制样式")
    
    print("\n" + "=" * 60)
    print("开始修复...")
    print("=" * 60)
    
    fix_export_menu_inline_styles()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修改内容：")
    print("\n旧的（冲突）:")
    print('  <div id="exportMenu" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; ...">')
    print("  ↓ 这些样式强制居中，覆盖 JavaScript")
    
    print("\n新的（干净）:")
    print('  <div id="exportMenu" style="display: none; z-index: 999999;">')
    print("  ↓ 只保留必要的，让 JavaScript 控制其他")
    
    print("\n🎯 现在应该：")
    print("• 移动端：JavaScript 设置居中样式 ✅")
    print("• 桌面端：JavaScript 设置按钮下方样式 ✅")
    print("• console.log 正常输出 ✅")
    print("• 样式不再被覆盖 ✅")
    
    print("\n🚀 请刷新页面测试！")

if __name__ == '__main__':
    main()

