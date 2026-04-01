#!/usr/bin/env python3
"""
🎯 直接替换：用 firstproject 的工作代码替换 document-detail 的 Export 功能

简单策略：
1. 删除 document-detail 中所有 Export 相关代码
2. 直接插入 firstproject 的工作代码
3. 只修改文档选择部分（使用 window.currentDocument）
"""

import os
import re

def replace_with_working_code():
    """直接替换为工作的代码"""
    
    # 工作的代码（从 firstproject.html 复制，已验证可用）
    working_export_code = '''        // 🔥 Export 功能 - 工作版本（从 firstproject.html）
        
        // 关闭菜单
        window.closeExportMenu = function() {
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            if (menu) {
                menu.style.display = 'none';
                menu.classList.remove('active');
            }
            if (overlay) {
                overlay.style.display = 'none';
            }
            console.log('🔒 菜单已关闭');
        };
        
        // 切换菜单显示
        window.toggleExportMenu = function() {
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
                closeExportMenu();
                return;
            }
            
            // 使用当前文档（document-detail 场景）
            if (!window.currentDocument) {
                console.warn('⚠️ window.currentDocument 不存在');
            }
            
            // 更新菜单内容
            console.log('🔄 更新菜单内容...');
            updateExportMenuContent();
            
            // 根据屏幕大小设置菜单样式
            if (window.innerWidth <= 768) {
                // 移动端：居中显示
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
                
                // 显示遮罩
                if (overlay) {
                    overlay.style.display = 'block';
                }
            } else {
                // 桌面端：在 Export 按钮下方
                const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
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
                }
                console.log('💻 桌面端：菜单在按钮下方');
                
                // 不显示遮罩
                if (overlay) {
                    overlay.style.display = 'none';
                }
            }
            
            menu.style.display = 'block';
            menu.classList.add('active');
            
            console.log('✅ 菜单已显示');
        };
        
        console.log('✅ Export 功能已加载（工作版本）');
'''
    
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
        
        # 找到并删除从 "// 🔥 Export 功能" 到下一个主要 script 标签或 </script> 的所有内容
        # 使用更宽松的模式
        pattern = r'//.*?Export.*?功能.*?console\.log\(.*?Export.*?功能.*?已加载.*?\);'
        
        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            print(f"找到 {len(matches)} 个 Export 代码块")
            # 只替换最后一个（最新的）
            last_match = matches[-1]
            content = content[:last_match.start()] + working_export_code + content[last_match.end():]
            print("✅ 已替换为工作版本")
        else:
            print("⚠️ 未找到 Export 代码块，在文件末尾添加")
            # 在最后一个 </script> 前添加
            last_script = content.rfind('</script>')
            if last_script != -1:
                content = content[:last_script] + working_export_code + '\n' + content[last_script:]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {html_file}")

def main():
    print("🎯 替换为工作的 Export 代码\n")
    
    print("=" * 60)
    print("开始替换...")
    print("=" * 60)
    
    replace_with_working_code()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n🎉 已使用 firstproject.html 的工作代码！")
    print("\n🚀 请刷新页面测试！")
    print("\n📋 预期：")
    print("• 点击 Export 按钮")
    print("• 菜单应该立即显示")
    print("• 桌面端：在按钮下方")
    print("• 移动端：屏幕中央")

if __name__ == '__main__':
    main()

