#!/usr/bin/env python3
"""
🔥 Export 按钮终极诊断和修复

策略：
1. 在按钮 onclick 添加内联 alert 测试点击是否生效
2. 简化 toggleExportMenu 函数
3. 添加详细的 console.log 调试信息
"""

import os
import re

def add_inline_test():
    """在 Export 按钮添加内联测试"""
    
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
        
        original_content = content
        
        # 修改按钮的 onclick，添加内联调试
        # 查找: <button onclick="toggleExportMenu(event)"
        # 替换为: <button onclick="console.log('🔥 按钮被点击'); toggleExportMenu(event)"
        
        pattern = r'<button onclick="toggleExportMenu\(event\)"'
        replacement = r'<button onclick="console.log(\'🔥 Export 按钮被点击\'); console.log(\'toggleExportMenu 类型:\', typeof window.toggleExportMenu); if(typeof window.toggleExportMenu === \'function\') { toggleExportMenu(event); } else { alert(\'错误：toggleExportMenu 函数不存在！\'); }"'
        
        content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已添加内联测试到 {html_file}")
        else:
            print(f"ℹ️  {html_file} 未找到匹配或已修改")
    
    print()

def simplify_toggle_function():
    """简化 toggleExportMenu 函数，移除复杂的定位逻辑"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 简化版本的 toggleExportMenu
    simple_function = '''window.toggleExportMenu = function(event) {
            console.log('🎯 toggleExportMenu 被调用');
            console.log('  - event:', event);
            console.log('  - window.exportDocument:', typeof window.exportDocument);
            console.log('  - window.currentDocument:', window.currentDocument);
            
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            
            if (!menu) {
                console.error('❌ Export 菜单元素不存在！');
                alert('错误：Export 菜单元素不存在');
                return;
            }
            
            console.log('✅ Export 菜单元素存在');
            
            // 如果菜单已显示，则关闭
            if (menu.style.display === 'block') {
                console.log('🔄 关闭菜单');
                menu.style.display = 'none';
                if (overlay) overlay.style.display = 'none';
                return;
            }
            
            // 显示遮罩
            if (overlay) {
                overlay.style.display = 'block';
            }
            
            // 更新菜单内容
            console.log('🔄 更新菜单内容...');
            updateExportMenuForDocumentDetail();
            
            // 显示菜单（简化版 - 固定居中显示）
            menu.style.display = 'block';
            menu.style.position = 'fixed';
            menu.style.top = '50%';
            menu.style.left = '50%';
            menu.style.transform = 'translate(-50%, -50%)';
            menu.style.zIndex = '2147483647';
            menu.style.background = 'white';
            menu.style.borderRadius = '12px';
            menu.style.boxShadow = '0 25px 50px rgba(0,0,0,0.25)';
            menu.style.minWidth = '280px';
            menu.style.maxWidth = '90%';
            menu.style.padding = '1rem';
            
            console.log('✅ Export 菜单已显示');
        };'''
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换 toggleExportMenu 函数
        pattern = r'window\.toggleExportMenu = function\(event\) \{[^}]*\{[^}]*\{[^}]*\}[^}]*\}[^}]*\};'
        
        # 使用更安全的方法：查找函数开始和结束
        start_marker = 'window.toggleExportMenu = function(event) {'
        if start_marker in content:
            start_pos = content.find(start_marker)
            # 查找匹配的闭合括号
            brace_count = 0
            i = start_pos + len(start_marker)
            while i < len(content):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    if brace_count == 0:
                        # 找到函数结束
                        end_pos = i + 2  # 包括 }; 
                        old_function = content[start_pos:end_pos]
                        new_content = content[:start_pos] + simple_function + content[end_pos:]
                        
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ 已简化 {html_file} 中的 toggleExportMenu 函数")
                        break
                    brace_count -= 1
                i += 1

def main():
    print("🔥 Export 按钮终极修复...\n")
    
    print("=" * 60)
    print("第 1 步：添加内联调试")
    print("=" * 60)
    add_inline_test()
    
    print("=" * 60)
    print("第 2 步：简化 toggleExportMenu 函数")
    print("=" * 60)
    simplify_toggle_function()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• 在按钮 onclick 添加了内联调试")
    print("• 简化了 toggleExportMenu 函数")
    print("• 菜单现在固定居中显示（更可靠）")
    print("• 添加了详细的 console.log 调试信息")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存")
    print("2. 刷新页面")
    print("3. 打开控制台（F12）")
    print("4. 点击 Export 按钮")
    print("5. 查看控制台输出：")
    print("   - 应该看到 '🔥 Export 按钮被点击'")
    print("   - 应该看到 '🎯 toggleExportMenu 被调用'")
    print("   - 应该看到 '✅ Export 菜单已显示'")
    
    print("\n💡 如果控制台没有任何输出：")
    print("• 说明按钮的 onclick 事件根本没有触发")
    print("• 可能是 CSS 覆盖或 z-index 问题")
    print("• 请截图整个页面和控制台")

if __name__ == '__main__':
    main()

