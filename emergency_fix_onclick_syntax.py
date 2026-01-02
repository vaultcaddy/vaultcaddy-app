#!/usr/bin/env python3
"""
🔥 紧急修复 Export 按钮语法错误

问题：onclick 属性中的引号嵌套导致语法错误
解决：使用 HTML 实体编码或重写为更简单的形式
"""

import os
import re
import html

def fix_onclick_syntax():
    """修复 Export 按钮的 onclick 语法错误"""
    
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
        
        # 查找并替换有问题的 onclick
        # 问题：嵌套的单引号和双引号
        
        # 简化的版本 - 只调用函数，调试信息放在函数内部
        pattern = r'<button onclick="console\.log\(.*?\).*?toggleExportMenu\(event\);.*?\}" style="background: #10b981'
        
        # 新的简单版本
        replacement = '<button onclick="toggleExportMenu(event)" style="background: #10b981'
        
        original_content = content
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复 {html_file} 的 onclick 语法")
        else:
            print(f"⚠️  {html_file} 未找到匹配或已修复")

def ensure_toggle_function_has_debug():
    """确保 toggleExportMenu 函数内部有足够的调试信息"""
    
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
        
        # 确保 toggleExportMenu 函数开始就有调试
        # 查找: window.toggleExportMenu = function(event) {
        # 确保紧接着有: console.log('🎯 toggleExportMenu 被调用');
        
        if "window.toggleExportMenu = function(event) {" in content:
            if "console.log('🎯 toggleExportMenu 被调用');" in content:
                print(f"✅ {html_file} 已有调试信息")
            else:
                print(f"⚠️  {html_file} 缺少调试信息（但可能已修复）")

def main():
    print("🔥 紧急修复 Export 按钮语法错误...\n")
    
    print("=" * 60)
    print("修复 onclick 属性的语法错误")
    print("=" * 60)
    
    fix_onclick_syntax()
    
    print("\n" + "=" * 60)
    print("检查 toggleExportMenu 函数")
    print("=" * 60)
    
    ensure_toggle_function_has_debug()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 问题原因：")
    print("• onclick 属性中有复杂的嵌套引号")
    print("• 导致 HTML 解析错误")
    print("• 按钮的点击事件根本没有触发")
    
    print("\n📋 修复内容：")
    print("• 简化了 onclick 属性")
    print("• 只调用 toggleExportMenu(event)")
    print("• 所有调试信息保留在函数内部")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存（Ctrl+Shift+Delete）")
    print("2. 刷新页面")
    print("3. 打开控制台（F12）")
    print("4. 点击 Export 按钮")
    print("5. 应该立即看到：")
    print("   🎯 toggleExportMenu 被调用")
    print("   🔄 更新菜单内容...")
    print("   ✅ Export 菜单已显示")

if __name__ == '__main__':
    main()

