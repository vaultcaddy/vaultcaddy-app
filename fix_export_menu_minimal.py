#!/usr/bin/env python3
"""
🔥 只修改 Export 菜单 - 不改变页面其他设计

策略：
1. 找到现有的 exportMenu 和相关代码
2. 只替换这部分代码
3. 保持页面其他部分完全不变
"""

import os
import re

def extract_export_menu_from_firstproject():
    """从 firstproject.html 提取 Export 菜单的完整代码"""
    
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 提取 exportMenu HTML
    menu_start = content.find('<div class="export-menu" id="exportMenu"')
    menu_end = content.find('</div>', menu_start) + 6
    
    # 找到 exportMenuOverlay
    overlay_start = content.find('<div id="exportMenuOverlay"', menu_end)
    overlay_end = content.find('</div>', overlay_start) + 6
    
    export_menu_html = content[menu_start:overlay_end]
    
    # 2. 提取 updateExportMenuContent 函数
    update_start = content.find('// 🔄 Update Export MenuContent')
    if update_start == -1:
        update_start = content.find('function updateExportMenuContent()')
    
    # 找到函数结束
    brace_count = 0
    i = content.find('{', update_start)
    start_pos = i
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                update_function = content[update_start:i+1]
                break
        i += 1
    
    # 3. 提取 toggleExportMenu 函数（只需要关键部分）
    toggle_start = content.find('window.toggleExportMenu = function()')
    toggle_end = content.find('};', toggle_start) + 2
    toggle_function = content[toggle_start:toggle_end]
    
    return {
        'menu_html': export_menu_html,
        'update_function': update_function,
        'toggle_function': toggle_function
    }

def update_only_export_menu_minimal():
    """最小化修改：只更新 Export 菜单的生成逻辑"""
    
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
        
        # 找到现有的 toggleExportMenu 函数
        # 只修改移动端和桌面端的样式设置部分
        
        # 替换移动端样式设置
        mobile_old_pattern = r"if \(window\.innerWidth <= 768\) \{[^}]+\}"
        mobile_new = '''if (window.innerWidth <= 768) {
            // 📱 移动端：居中显示，全白设计
            menu.style.position = 'fixed';
            menu.style.top = '50%';
            menu.style.left = '50%';
            menu.style.transform = 'translate(-50%, -50%)';
            menu.style.right = 'auto';
            menu.style.width = '90%';
            menu.style.maxWidth = '400px';
            menu.style.backgroundColor = '#ffffff';
            menu.style.border = 'none';
            menu.style.boxShadow = 'none';
            menu.style.borderRadius = '12px';
            console.log('📱 移动端：菜单居中显示');
            
            if (overlay) {
                overlay.style.display = 'block';
            }
        }'''
        
        # 这个方法太复杂，让我换一个更简单的方法
        
        print(f"⚠️  跳过 {html_file} - 需要手动检查")

def create_simple_fix_script():
    """创建一个简单的浏览器console脚本来测试"""
    
    script = '''
// 🔥 在浏览器console运行这个脚本来测试 Export 菜单

// 1. 更新 toggleExportMenu 函数
window.toggleExportMenu_NEW = function() {
    console.log('🔍 新版 toggleExportMenu 被调用');
    const menu = document.getElementById('exportMenu');
    const overlay = document.getElementById('exportMenuOverlay');
    
    if (!menu) {
        console.error('❌ 未找到菜单元素');
        return;
    }
    
    // 如果已显示，则关闭
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
        if (overlay) overlay.style.display = 'none';
        return;
    }
    
    // 检查文档
    if (!window.currentDocument) {
        alert('文档数据未加载');
        return;
    }
    
    // 更新菜单内容（使用现有函数）
    if (typeof updateExportMenuForDocumentDetail === 'function') {
        updateExportMenuForDocumentDetail();
    }
    
    // 🔥 根据屏幕大小设置样式
    if (window.innerWidth <= 768) {
        // 移动端
        menu.style.position = 'fixed';
        menu.style.top = '50%';
        menu.style.left = '50%';
        menu.style.transform = 'translate(-50%, -50%)';
        menu.style.width = '90%';
        menu.style.maxWidth = '400px';
        menu.style.backgroundColor = '#ffffff';
        menu.style.border = 'none';
        menu.style.boxShadow = 'none';
        menu.style.borderRadius = '12px';
        
        if (overlay) overlay.style.display = 'block';
    } else {
        // 桌面端
        const exportBtn = document.querySelector('[onclick*="toggleExportMenu"]');
        if (exportBtn) {
            const rect = exportBtn.getBoundingClientRect();
            menu.style.position = 'fixed';
            menu.style.top = (rect.bottom + 8) + 'px';
            menu.style.right = (window.innerWidth - rect.right) + 'px';
            menu.style.left = 'auto';
            menu.style.transform = 'none';
            menu.style.width = 'auto';
            menu.style.minWidth = '280px';
            menu.style.maxWidth = '400px';
            menu.style.backgroundColor = '#ffffff';
            menu.style.border = '1px solid #e5e7eb';
            menu.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
            menu.style.borderRadius = '8px';
        }
        
        if (overlay) overlay.style.display = 'none';
    }
    
    menu.style.display = 'block';
    console.log('✅ 菜单已显示');
};

// 2. 替换原函数
window.toggleExportMenu = window.toggleExportMenu_NEW;

console.log('✅ Export 菜单函数已更新 - 请点击 Export 按钮测试');
'''
    
    with open('test_export_menu.js', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("✅ 已创建测试脚本: test_export_menu.js")
    print("📋 请在浏览器console复制粘贴这个脚本来测试")

def main():
    print("🔥 Export 菜单修复 - 最小化修改方案\n")
    
    print("=" * 60)
    print("问题分析")
    print("=" * 60)
    print("• 之前的脚本可能改变了页面的整体设计")
    print("• 用户只想要修改 Export **菜单**的显示")
    print("• 页面其他部分应保持不变")
    
    print("\n" + "=" * 60)
    print("解决方案")
    print("=" * 60)
    print("• 创建一个浏览器console测试脚本")
    print("• 先在浏览器测试，确认效果正确")
    print("• 再修改实际文件")
    
    print("\n" + "=" * 60)
    print("生成测试脚本")
    print("=" * 60)
    
    create_simple_fix_script()
    
    print("\n" + "=" * 60)
    print("下一步")
    print("=" * 60)
    print("1. 打开 document-detail.html 页面")
    print("2. 打开浏览器Console (F12)")
    print("3. 复制 test_export_menu.js 的内容")
    print("4. 粘贴到Console并回车")
    print("5. 点击 Export 按钮测试效果")
    print("6. 如果效果正确，告诉我，我会修改实际文件")

if __name__ == '__main__':
    main()

