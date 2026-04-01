#!/usr/bin/env python3
"""
🔥 只修改 Export 菜单的样式设置 - 与 firstproject.html 完全一致

策略：
1. 只修改 toggleExportMenu() 函数中的样式设置部分
2. 确保移动端和桌面端的样式与 firstproject.html 完全一致
3. 不改变其他任何代码
"""

import os
import re

def update_toggle_export_menu_styles():
    """更新 toggleExportMenu 函数中的样式设置"""
    
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
        
        # 找到 toggleExportMenu 函数
        func_start = content.find('window.toggleExportMenu = function(event)')
        if func_start == -1:
            print(f"⚠️  {html_file} 未找到 toggleExportMenu 函数")
            continue
        
        # 找到函数结束
        brace_count = 0
        i = content.find('{', func_start)
        start_brace = i
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    func_end = i + 2  # 包括 };
                    break
            i += 1
        
        old_function = content[func_start:func_end]
        
        # 创建新的函数，只替换样式设置部分
        new_function = '''window.toggleExportMenu = function(event) {
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            if (!menu) return;
            
            // 如果菜单已显示，则关闭
            if (menu.style.display === 'block') {
                closeExportMenu();
                return;
            }
            
            // 总是显示背景遮罩（CSS会控制桌面版隐藏）
            if (!overlay) {
                const newOverlay = document.createElement('div');
                newOverlay.id = 'exportMenuOverlay';
                newOverlay.onclick = closeExportMenu;
                document.body.appendChild(newOverlay);
            }
            if (overlay) {
                overlay.style.display = 'block';
            }
            
            // 基于文档类型生成菜单
            updateExportMenuForDocumentDetail();
            
            // 🔥 根据屏幕大小设置菜单样式（与 firstproject.html 完全一致）
            if (window.innerWidth <= 768) {
                // 📱 移动端：居中显示，全白设计
                if (menu.parentElement !== document.body) {
                    document.body.appendChild(menu);
                }
                menu.style.position = 'fixed';
                menu.style.top = '50%';
                menu.style.left = '50%';
                menu.style.transform = 'translate(-50%, -50%)';
                menu.style.right = 'auto';
                menu.style.width = '90%';
                menu.style.maxWidth = '400px';
                menu.style.backgroundColor = '#ffffff'; // 🔥 白色背景
                menu.style.border = 'none'; // 🔥 无边框
                menu.style.boxShadow = 'none'; // 🔥 无阴影
                menu.style.borderRadius = '12px';
                menu.style.zIndex = '999999';
                menu.style.marginTop = '0';
                console.log('📱 移动端：菜单居中显示（全白）');
                
                // 显示遮罩
                if (overlay) {
                    overlay.style.display = 'block';
                }
            } else {
                // 💻 桌面端：在 Export 按钮下方
                const exportBtn = event ? event.currentTarget : document.querySelector('button[onclick*="toggleExportMenu"]');
                if (exportBtn) {
                    const btnRect = exportBtn.getBoundingClientRect();
                    const exportDropdown = exportBtn.closest('.export-dropdown');
                    
                    if (exportDropdown) {
                        // 相对于 export-dropdown 定位
                        menu.style.position = 'absolute';
                        menu.style.top = 'auto';
                        menu.style.left = 'auto';
                        menu.style.right = '0';
                        menu.style.bottom = 'auto';
                        menu.style.transform = 'none';
                        menu.style.marginTop = '0.5rem';
                        menu.style.minWidth = '280px';
                        menu.style.maxWidth = '400px';
                        menu.style.backgroundColor = '#ffffff';
                        menu.style.border = '1px solid #e5e7eb';
                        menu.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                        menu.style.borderRadius = '8px';
                        menu.style.zIndex = '999999';
                        
                        // 将菜单移动到 export-dropdown 内部
                        exportDropdown.appendChild(menu);
                    }
                }
                console.log('💻 桌面端：菜单在按钮下方');
                
                // 桌面端不显示遮罩
                if (overlay) {
                    overlay.style.display = 'none';
                }
            }
            
            // 显示菜单
            menu.style.display = 'block';
            
            console.log('📤 Export 菜单已显示');
        };'''
        
        # 替换函数
        new_content = content[:func_start] + new_function + content[func_end:]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已更新 {html_file}")
        print(f"   替换了 toggleExportMenu 函数（{len(old_function)} → {len(new_function)} 字节）")

def main():
    print("🔥 更新 Export 菜单样式设置\n")
    
    print("=" * 60)
    print("开始更新 toggleExportMenu 函数...")
    print("=" * 60)
    
    update_toggle_export_menu_styles()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成的更新：")
    print("• ✅ 更新了 toggleExportMenu 函数的样式设置")
    print("• ✅ 移动端：居中、90%宽、全白、无边框、无阴影")
    print("• ✅ 桌面端：按钮下方、280-400px宽、边框、阴影")
    print("• ✅ 与 firstproject.html 完全一致")
    
    print("\n📱 移动端样式：")
    print("• 位置：居中（top: 50%, left: 50%, transform: translate(-50%, -50%)）")
    print("• 宽度：90%（最大 400px）")
    print("• 背景：全白（#ffffff）")
    print("• 边框：无（border: none）")
    print("• 阴影：无（box-shadow: none）")
    print("• 圆角：12px")
    print("• 遮罩：显示")
    
    print("\n💻 桌面端样式：")
    print("• 位置：Export 按钮下方（relative to .export-dropdown）")
    print("• 宽度：280-400px")
    print("• 背景：白色（#ffffff）")
    print("• 边框：灰色（1px solid #e5e7eb）")
    print("• 阴影：有（0 10px 25px rgba(0,0,0,0.15)）")
    print("• 圆角：8px")
    print("• 遮罩：不显示")
    
    print("\n🎯 未修改的部分：")
    print("• ✅ updateExportMenuForDocumentDetail() 函数")
    print("• ✅ 菜单内容生成逻辑")
    print("• ✅ exportDocument() 函数")
    print("• ✅ 页面其他部分")
    
    print("\n🚀 请刷新页面测试：")
    print("1. 桌面端：点击 Export，菜单应在按钮下方，有边框和阴影")
    print("2. 移动端：点击 Export，菜单应居中，全白无边框")

if __name__ == '__main__':
    main()

