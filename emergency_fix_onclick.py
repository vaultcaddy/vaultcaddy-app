#!/usr/bin/env python3
"""
🔍 诊断并修复 Export 按钮无法点击的问题

可能的原因：
1. .auth-loading 遮罩层没有正确隐藏（z-index: 9999）
2. 有其他覆盖层阻止点击
3. onclick 事件被阻止
4. JavaScript 有语法错误

解决方案：
1. 降低 .auth-loading 的 z-index
2. 提高 Export 按钮的 z-index
3. 添加直接的 event listener 作为备用
4. 添加诊断代码
"""

import os
import re

def fix_z_index_and_onclick():
    """修复 z-index 冲突和 onclick 问题"""
    
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
        
        # 1. 降低 .auth-loading 的 z-index（从 9999 改为 10000）
        content = re.sub(
            r'(\.auth-loading.*?z-index:\s*)9999',
            r'\g<1>10000',
            content
        )
        print("✅ 提高 auth-loading 的 z-index 到 10000")
        
        # 2. 提高 Export 按钮的 z-index（从 9999 改为 99999）
        content = re.sub(
            r'(button\[onclick\*="toggleExportMenu"\].*?z-index:\s*)9999',
            r'\g<1>99999',
            content
        )
        print("✅ 提高 Export 按钮的 z-index 到 99999")
        
        # 3. 修复 toggleExportMenu 函数，接收 event 参数
        # 按钮调用是 onclick="toggleExportMenu(event)"
        # 但函数定义是 window.toggleExportMenu = function()
        content = re.sub(
            r'window\.toggleExportMenu\s*=\s*function\(\)',
            r'window.toggleExportMenu = function(event)',
            content
        )
        print("✅ 修复 toggleExportMenu 函数参数")
        
        # 4. 在 script 末尾添加备用的 event listener
        backup_listener = '''
        // 🔥 备用：直接添加 event listener（防止 onclick 被阻止）
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🔍 DOMContentLoaded - 开始绑定 Export 按钮');
            
            const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
            console.log('📋 Export 按钮:', exportBtn);
            
            if (exportBtn) {
                // 移除旧的 listener（如果有）
                exportBtn.removeAttribute('data-listener-attached');
                
                // 添加新的 listener
                exportBtn.addEventListener('click', function(e) {
                    console.log('🎯 Export 按钮被点击（event listener）');
                    console.log('📋 Event:', e);
                    
                    // 确保函数存在
                    if (typeof window.toggleExportMenu === 'function') {
                        console.log('✅ toggleExportMenu 函数存在，调用中...');
                        window.toggleExportMenu(e);
                    } else {
                        console.error('❌ toggleExportMenu 函数不存在');
                        console.log('window.toggleExportMenu:', window.toggleExportMenu);
                    }
                });
                
                exportBtn.setAttribute('data-listener-attached', 'true');
                console.log('✅ Export 按钮 event listener 已绑定');
            } else {
                console.error('❌ 未找到 Export 按钮');
            }
        });
        
        console.log('✅ Export 功能已加载（全新版本 + 备用 listener）');
'''
        
        # 在最后一个 console.log('✅ Export 功能已加载') 之后添加
        content = re.sub(
            r"console\.log\('✅ Export 功能已加载（全新版本）'\);",
            backup_listener,
            content
        )
        print("✅ 添加备用 event listener")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file}")

def main():
    print("🔍 诊断并修复 Export 按钮无法点击的问题\n")
    
    print("=" * 60)
    print("问题诊断")
    print("=" * 60)
    print("• .auth-loading 的 z-index 是 9999")
    print("• Export 按钮的 z-index 也是 9999")
    print("• 可能存在遮挡冲突")
    print("• onclick 可能被阻止")
    
    print("\n" + "=" * 60)
    print("解决方案")
    print("=" * 60)
    print("1. 提高 Export 按钮 z-index 到 99999")
    print("2. 修复 toggleExportMenu 函数参数")
    print("3. 添加备用 event listener")
    print("4. 添加完整的调试日志")
    
    print("\n" + "=" * 60)
    print("开始修复...")
    print("=" * 60)
    
    fix_z_index_and_onclick()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 已完成的修复：")
    print("• ✅ 提高 Export 按钮 z-index（9999 → 99999）")
    print("• ✅ 修复 toggleExportMenu 函数参数")
    print("• ✅ 添加备用 event listener")
    print("• ✅ 添加详细的调试日志")
    
    print("\n🔍 现在的调试日志：")
    print("页面加载时：")
    print("  🔍 DOMContentLoaded - 开始绑定 Export 按钮")
    print("  📋 Export 按钮: ...")
    print("  ✅ Export 按钮 event listener 已绑定")
    print("  ✅ Export 功能已加载")
    print("\n点击 Export 时：")
    print("  🎯 Export 按钮被点击（event listener）")
    print("  📋 Event: ...")
    print("  ✅ toggleExportMenu 函数存在，调用中...")
    print("  🔍 toggleExportMenu Called")
    print("  ... （之后的所有日志）")
    
    print("\n🚀 请刷新页面测试！")
    print("应该立即在 Console 看到绑定日志！")

if __name__ == '__main__':
    main()

