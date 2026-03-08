#!/usr/bin/env python3
"""
🔍 添加详细的调试日志，找出为什么菜单不显示

在 toggleExportMenu 函数中添加每一步的日志
"""

import os
import re

def add_detailed_logging():
    """添加详细调试日志"""
    
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
        
        # 在每个关键步骤后添加日志
        
        # 1. 在 menu.style.display = 'block' 后添加日志
        pattern1 = r"(menu\.style\.display = 'block';)"
        replacement1 = r'''\1
            console.log('✅ 已设置 display: block');'''
        content = re.sub(pattern1, replacement1, content)
        
        # 2. 在移动端/桌面端判断后添加日志
        pattern2 = r"(if \(window\.innerWidth <= 768\) \{)"
        replacement2 = r'''\1
                console.log('📱 检测到移动端');'''
        content = re.sub(pattern2, replacement2, content)
        
        pattern3 = r"(\} else \{\s*// 💻 桌面端：在 Export 按钮下方)"
        replacement3 = r'''\1
                console.log('💻 检测到桌面端');'''
        content = re.sub(pattern3, replacement3, content)
        
        # 3. 在最后添加最终状态日志
        pattern4 = r"(console\.log\('✅ 菜单已显示'\);)"
        replacement4 = r'''\1
            
            // 🔍 最终状态检查
            const finalStyle = window.getComputedStyle(menu);
            console.log('🔍 最终菜单状态:');
            console.log('  - display:', finalStyle.display);
            console.log('  - position:', finalStyle.position);
            console.log('  - top:', finalStyle.top);
            console.log('  - left:', finalStyle.left);
            console.log('  - zIndex:', finalStyle.zIndex);
            console.log('  - width:', finalStyle.width);
            console.log('  - height:', finalStyle.height);
            console.log('  - innerHTML length:', menu.innerHTML.length);
            
            const finalRect = menu.getBoundingClientRect();
            console.log('  - rect:', finalRect);
            
            if (finalStyle.display === 'none') {
                console.error('❌❌❌ display 还是 none！');
            }
            if (finalRect.width === 0 || finalRect.height === 0) {
                console.error('❌❌❌ 菜单尺寸是 0！');
            }
            if (menu.innerHTML.length === 0) {
                console.error('❌❌❌ 菜单内容为空！');
            }'''
        content = re.sub(pattern4, replacement4, content)
        
        print("✅ 添加详细日志")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已处理 {html_file}")

def main():
    print("🔍 添加详细调试日志\n")
    
    print("=" * 60)
    print("开始添加...")
    print("=" * 60)
    
    add_detailed_logging()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n🚀 请刷新页面，点击 Export 按钮！")
    print("\n📋 新的日志会显示：")
    print("• ✅ 已设置 display: block")
    print("• 📱/💻 移动端或桌面端检测")
    print("• 🔍 最终菜单状态（display, position, 尺寸等）")
    print("• 如果有问题会显示红色错误")
    
    print("\n⚠️ 请截图完整的 Console 输出！")

if __name__ == '__main__':
    main()

