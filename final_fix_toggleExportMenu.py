#!/usr/bin/env python3
"""
🎯 最终修复：修复 toggleExportMenu 函数的样式设置

已知：
- ✅ exportMenu 元素存在
- ✅ 强制设置样式可以显示（红色框测试成功）
- ❌ toggleExportMenu 函数的样式设置有问题

解决：
- 使用和强制显示测试一样的样式设置逻辑
- 简化样式设置，去掉复杂的判断
"""

import os
import re

def fix_toggleExportMenu_function():
    """修复 toggleExportMenu 函数"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 新的 toggleExportMenu 函数（简化版，参考强制显示的逻辑）
    new_function = '''        // 切换菜单显示（简化版，确保能显示）
        window.toggleExportMenu = function(event) {
            console.log('🔍 toggleExportMenu Called');
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            console.log('📋 菜单元素:', menu);
            
            if (!menu) {
                console.error('❌ 未找到 #exportMenu 元素');
                return;
            }
            
            // 如果菜单已显示，则关闭
            if (menu.style.display === 'block') {
                console.log('🔒 菜单已显示，关闭中...');
                closeExportMenu();
                return;
            }
            
            // 检查当前文档
            console.log('📄 window.currentDocument:', window.currentDocument);
            
            // 更新菜单内容
            console.log('🔄 更新菜单内容...');
            updateExportMenuContent();
            
            console.log('📱 设置菜单样式...');
            
            // 🔥 使用简化的、确保有效的样式设置（参考强制显示测试）
            menu.style.display = 'block';
            menu.style.position = 'fixed';
            menu.style.zIndex = '9999999';
            menu.style.backgroundColor = '#ffffff';
            menu.style.padding = '1.5rem';
            menu.style.borderRadius = '12px';
            menu.style.minWidth = '300px';
            menu.style.maxWidth = '90%';
            
            if (window.innerWidth <= 768) {
                // 📱 移动端：居中显示
                menu.style.top = '50%';
                menu.style.left = '50%';
                menu.style.transform = 'translate(-50%, -50%)';
                menu.style.width = '90%';
                menu.style.maxWidth = '400px';
                menu.style.border = 'none';
                menu.style.boxShadow = '0 25px 50px rgba(0,0,0,0.25)';
                console.log('📱 移动端：菜单居中显示');
                
                // 显示遮罩
                if (overlay) {
                    overlay.style.display = 'block';
                }
            } else {
                // 💻 桌面端：在按钮下方
                const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
                if (exportBtn) {
                    const rect = exportBtn.getBoundingClientRect();
                    menu.style.top = (rect.bottom + 8) + 'px';
                    menu.style.right = (window.innerWidth - rect.right) + 'px';
                    menu.style.left = 'auto';
                    menu.style.transform = 'none';
                    menu.style.width = 'auto';
                    menu.style.minWidth = '300px';
                    menu.style.maxWidth = '450px';
                    menu.style.border = '1px solid #e5e7eb';
                    menu.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                    console.log('💻 桌面端：菜单在按钮下方 (top=' + menu.style.top + ', right=' + menu.style.right + ')');
                } else {
                    // 如果找不到按钮，居中显示
                    console.warn('⚠️ 未找到 Export 按钮，使用居中显示');
                    menu.style.top = '50%';
                    menu.style.left = '50%';
                    menu.style.transform = 'translate(-50%, -50%)';
                    menu.style.border = '1px solid #e5e7eb';
                    menu.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                }
                
                // 桌面端不显示遮罩
                if (overlay) {
                    overlay.style.display = 'none';
                }
            }
            
            menu.classList.add('active');
            
            console.log('✅ 菜单已显示');
            console.log('📊 最终样式: display=' + menu.style.display + ', position=' + menu.style.position + ', zIndex=' + menu.style.zIndex);
        };'''
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {html_file}:")
        print("=" * 50)
        
        # 替换整个 toggleExportMenu 函数
        # 从 "// 切换菜单显示" 到下一个 "// " 或 "window." 开头的行
        pattern = r'// 切换菜单显示（与 firstproject 完全相同的逻辑）\s*window\.toggleExportMenu\s*=\s*function\(event\)\s*\{.*?^\s*\};'
        
        if re.search(pattern, content, re.DOTALL | re.MULTILINE):
            content = re.sub(
                pattern,
                new_function,
                content,
                flags=re.DOTALL | re.MULTILINE
            )
            print("✅ 替换 toggleExportMenu 函数")
        else:
            print("⚠️ 未找到 toggleExportMenu 函数（尝试其他模式）")
            
            # 尝试更简单的模式
            pattern2 = r'window\.toggleExportMenu\s*=\s*function\(event\)\s*\{(?:(?!window\.\w+\s*=).)*?\};'
            if re.search(pattern2, content, re.DOTALL):
                content = re.sub(
                    pattern2,
                    new_function.strip(),
                    content,
                    flags=re.DOTALL
                )
                print("✅ 替换 toggleExportMenu 函数（模式2）")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file}")

def main():
    print("🎯 最终修复：修复 toggleExportMenu 函数\n")
    
    print("=" * 60)
    print("修复内容")
    print("=" * 60)
    print("• 简化样式设置逻辑")
    print("• 使用和强制显示测试一样的样式")
    print("• 确保 display: block")
    print("• 确保 position: fixed")
    print("• 确保 z-index: 9999999")
    print("• 移动端和桌面端分别设置")
    
    print("\n" + "=" * 60)
    print("开始修复...")
    print("=" * 60)
    
    fix_toggleExportMenu_function()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n🎉 现在点击 Export 按钮应该能正常显示菜单了！")
    print("\n📋 移动端效果：")
    print("• 菜单在屏幕正中央")
    print("• 有灰色遮罩背景")
    print("• 宽度 90%（最大 400px）")
    
    print("\n📋 桌面端效果：")
    print("• 菜单在 Export 按钮下方")
    print("• 无遮罩背景")
    print("• 有边框和阴影")
    
    print("\n🚀 请刷新页面，点击 Export 按钮测试！")

if __name__ == '__main__':
    main()

