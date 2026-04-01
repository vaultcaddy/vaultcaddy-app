#!/usr/bin/env python3
"""
🔥 强制修复 Export 按钮 - 移除 defer 确保立即执行

问题：defer 属性可能导致 exportDocument 函数延迟加载
解决：移除 document-detail-new.js 的 defer 属性
"""

import os
import re

def remove_defer_from_script():
    """移除 document-detail-new.js 的 defer 属性"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    fixed_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"⚠️  文件不存在: {html_file}")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除 defer 属性
        # 匹配: <script defer src="../document-detail-new.js?v=...">
        # 或: <script defer src="document-detail-new.js?v=...">
        pattern = r'<script\s+defer\s+src="(\.\./)?document-detail-new\.js\?v=[^"]*">'
        replacement = r'<script src="\1document-detail-new.js?v=20251107-rewrite">'
        
        content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复 {html_file}")
            fixed_count += 1
        else:
            print(f"ℹ️  {html_file} 无需修复或未找到匹配")
    
    return fixed_count

def add_console_debug():
    """在 toggleExportMenu 函数开始处添加调试信息"""
    
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
        
        # 在 toggleExportMenu 函数开始处添加调试
        if 'window.toggleExportMenu = function(event) {' in content:
            # 查找并替换
            pattern = r'(window\.toggleExportMenu = function\(event\) \{)'
            replacement = r'\1\n            console.log("🔥 Export 按钮被点击！", event);\n            console.log("🔥 exportDocument 类型:", typeof window.exportDocument);\n            console.log("🔥 currentDocument:", window.currentDocument);'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 已添加调试信息到 {html_file}")

def main():
    print("🔧 强制修复 Export 按钮...\n")
    
    print("=" * 60)
    print("第 1 步：移除 defer 属性")
    print("=" * 60)
    
    fixed = remove_defer_from_script()
    print(f"\n共修复 {fixed} 个文件\n")
    
    print("=" * 60)
    print("第 2 步：添加调试信息")
    print("=" * 60)
    
    add_console_debug()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• 移除了 document-detail-new.js 的 defer 属性")
    print("• 确保 exportDocument 函数立即可用")
    print("• 添加了调试信息帮助诊断")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存（Ctrl+Shift+Delete）")
    print("2. 刷新页面")
    print("3. 打开控制台（F12）")
    print("4. 点击 Export 按钮")
    print("5. 查看控制台输出（应该看到 🔥 开头的调试信息）")
    
    print("\n⚠️  注意：")
    print("如果控制台没有任何输出，说明按钮的 onclick 事件没有触发")
    print("如果看到 'exportDocument is undefined'，需要检查脚本加载顺序")

if __name__ == '__main__':
    main()

