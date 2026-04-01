#!/usr/bin/env python3
"""
🔍 深度诊断：检查 exportMenu 元素为什么不显示

已知：
- ✅ 按钮的 position 和 z-index 已修复
- ✅ 函数被调用
- ❌ 菜单没有弹出
- ❌ 没有看到 toggleExportMenu 内部的日志

检查：
1. exportMenu 元素是否存在
2. exportMenu 元素的样式
3. exportMenu 的 innerHTML
4. 是否有 JavaScript 错误
"""

import os
import re

def add_deep_diagnostic():
    """添加深度诊断代码"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 深度诊断代码
    diagnostic_code = '''
            
            // 🔍 深度诊断：检查 exportMenu 元素
            console.log('');
            console.log('🔍🔍🔍 exportMenu 元素深度检查 🔍🔍🔍');
            
            const menu = document.getElementById('exportMenu');
            const overlay = document.getElementById('exportMenuOverlay');
            
            console.log('1️⃣ exportMenu 存在?', menu !== null);
            console.log('   元素:', menu);
            
            if (menu) {
                console.log('2️⃣ exportMenu 的样式:');
                const menuStyle = window.getComputedStyle(menu);
                console.log('   - display:', menuStyle.display);
                console.log('   - visibility:', menuStyle.visibility);
                console.log('   - opacity:', menuStyle.opacity);
                console.log('   - position:', menuStyle.position);
                console.log('   - top:', menuStyle.top);
                console.log('   - left:', menuStyle.left);
                console.log('   - transform:', menuStyle.transform);
                console.log('   - z-index:', menuStyle.zIndex);
                console.log('   - width:', menuStyle.width);
                console.log('   - height:', menuStyle.height);
                
                console.log('3️⃣ exportMenu 的位置:');
                const menuRect = menu.getBoundingClientRect();
                console.log('   - top:', menuRect.top);
                console.log('   - left:', menuRect.left);
                console.log('   - right:', menuRect.right);
                console.log('   - bottom:', menuRect.bottom);
                console.log('   - width:', menuRect.width);
                console.log('   - height:', menuRect.height);
                
                console.log('4️⃣ exportMenu 的内容:');
                console.log('   - innerHTML 长度:', menu.innerHTML.length);
                console.log('   - innerHTML 前 100 字符:', menu.innerHTML.substring(0, 100));
                
                if (menu.innerHTML.length === 0 || menu.innerHTML.trim() === '') {
                    console.error('❌❌❌ exportMenu 没有内容！');
                }
            } else {
                console.error('❌❌❌ exportMenu 元素不存在！');
            }
            
            console.log('5️⃣ exportMenuOverlay 存在?', overlay !== null);
            if (overlay) {
                const overlayStyle = window.getComputedStyle(overlay);
                console.log('   - display:', overlayStyle.display);
                console.log('   - z-index:', overlayStyle.zIndex);
            }
            
            console.log('');
            console.log('🧪 手动测试：强制显示菜单...');
            
            if (menu) {
                // 保存原始样式
                console.log('📝 原始 inline style:', menu.getAttribute('style'));
                
                // 强制设置样式
                menu.style.display = 'block';
                menu.style.position = 'fixed';
                menu.style.top = '50%';
                menu.style.left = '50%';
                menu.style.transform = 'translate(-50%, -50%)';
                menu.style.zIndex = '9999999';
                menu.style.backgroundColor = '#ffffff';
                menu.style.border = '5px solid red';  // 红色边框用于调试
                menu.style.padding = '2rem';
                menu.style.minWidth = '300px';
                menu.style.minHeight = '200px';
                
                console.log('✅ 已强制设置样式，菜单应该在屏幕中央显示（红色边框）');
                console.log('👀 请查看页面，是否看到红色边框的菜单？');
                
                setTimeout(function() {
                    const newMenuStyle = window.getComputedStyle(menu);
                    console.log('🔍 强制设置后的样式:');
                    console.log('   - display:', newMenuStyle.display);
                    console.log('   - position:', newMenuStyle.position);
                    console.log('   - top:', newMenuStyle.top);
                    console.log('   - left:', newMenuStyle.left);
                    console.log('   - z-index:', newMenuStyle.zIndex);
                    
                    const newRect = menu.getBoundingClientRect();
                    console.log('   - 位置: top=' + newRect.top + ', left=' + newRect.left);
                    console.log('   - 尺寸: width=' + newRect.width + ', height=' + newRect.height);
                    
                    if (newRect.width === 0 || newRect.height === 0) {
                        console.error('❌❌❌ 菜单的尺寸是 0！可能是内容为空或 CSS 问题');
                    }
                    
                    if (newMenuStyle.display === 'none') {
                        console.error('❌❌❌ display 还是 none！可能被其他 CSS 规则覆盖');
                    }
                }, 100);
            }
            
            console.log('');
            console.log('🔍🔍🔍 深度检查完成 🔍🔍🔍');
            console.log('');
            console.log('📋 请告诉我：');
            console.log('1. exportMenu 存在吗？');
            console.log('2. exportMenu 的 display 是什么？');
            console.log('3. exportMenu 的内容长度是多少？');
            console.log('4. 是否看到红色边框的菜单？');
'''
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {html_file}:")
        print("=" * 50)
        
        # 在 "🔍🔍🔍 诊断完成 🔍🔍🔍" 之前添加深度诊断
        pattern = r"(console\.log\('🔍🔍🔍 诊断完成 🔍🔍🔍'\);)"
        
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                diagnostic_code + r"\n            \g<1>",
                content
            )
            print("✅ 添加 exportMenu 深度诊断代码")
        else:
            print("⚠️ 未找到插入点")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {html_file}")

def main():
    print("🔍 添加 exportMenu 深度诊断\n")
    
    print("=" * 60)
    print("诊断内容")
    print("=" * 60)
    print("1. 检查 exportMenu 元素是否存在")
    print("2. 检查 exportMenu 的所有 CSS 样式")
    print("3. 检查 exportMenu 的位置和尺寸")
    print("4. 检查 exportMenu 的内容")
    print("5. 强制显示菜单（红色边框）")
    
    print("\n" + "=" * 60)
    print("开始添加...")
    print("=" * 60)
    
    add_deep_diagnostic()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 新的诊断会显示：")
    print("• exportMenu 是否存在")
    print("• exportMenu 的所有样式（display, position, top, left 等）")
    print("• exportMenu 的内容长度")
    print("• 强制显示菜单（红色边框）")
    
    print("\n🚀 请刷新页面，等待诊断完成！")
    print("\n⚠️ 重点关注：")
    print("• exportMenu 的 display 是什么？（应该是 block）")
    print("• exportMenu 的内容长度是多少？（应该 > 0）")
    print("• 是否看到红色边框的菜单？")

if __name__ == '__main__':
    main()

