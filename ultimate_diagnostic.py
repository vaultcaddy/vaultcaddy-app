#!/usr/bin/env python3
"""
🔍 终极诊断：为什么点击 Export 按钮没有反应？

已知：
- ✅ 代码正常加载（4行日志）
- ✅ Event listener 已绑定
- ❌ 点击后没有日志 → 事件被阻止

检查：
1. 是否有其他元素覆盖在按钮上
2. 是否有 CSS 阻止点击
3. 是否有 JavaScript 错误
4. 手动触发事件测试
"""

import os
import re

def add_ultimate_diagnostic():
    """添加终极诊断代码"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 终极诊断代码
    diagnostic_code = '''
        
        // 🔍 终极诊断：找出为什么点击不工作
        setTimeout(function() {
            console.log('');
            console.log('🔍🔍🔍 开始终极诊断 🔍🔍🔍');
            console.log('');
            
            const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
            
            if (!exportBtn) {
                console.error('❌ Export 按钮不存在');
                return;
            }
            
            console.log('✅ Export 按钮存在:', exportBtn);
            
            // 1. 检查按钮的 CSS 属性
            const computedStyle = window.getComputedStyle(exportBtn);
            console.log('📊 按钮样式:');
            console.log('  - display:', computedStyle.display);
            console.log('  - visibility:', computedStyle.visibility);
            console.log('  - opacity:', computedStyle.opacity);
            console.log('  - pointer-events:', computedStyle.pointerEvents);
            console.log('  - z-index:', computedStyle.zIndex);
            console.log('  - position:', computedStyle.position);
            
            // 2. 检查按钮的位置
            const rect = exportBtn.getBoundingClientRect();
            console.log('📍 按钮位置:');
            console.log('  - top:', rect.top);
            console.log('  - left:', rect.left);
            console.log('  - width:', rect.width);
            console.log('  - height:', rect.height);
            
            // 3. 检查按钮中心点的元素
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const elementAtCenter = document.elementFromPoint(centerX, centerY);
            
            console.log('🎯 按钮中心点 (' + centerX + ', ' + centerY + ') 的元素:');
            console.log('  - 元素:', elementAtCenter);
            console.log('  - 是否是按钮本身?', elementAtCenter === exportBtn);
            console.log('  - 是否在按钮内部?', exportBtn.contains(elementAtCenter));
            
            if (elementAtCenter !== exportBtn && !exportBtn.contains(elementAtCenter)) {
                console.error('❌❌❌ 发现问题！按钮被其他元素覆盖了！');
                console.error('覆盖元素:', elementAtCenter);
                console.error('覆盖元素的 class:', elementAtCenter.className);
                console.error('覆盖元素的 id:', elementAtCenter.id);
                
                // 检查覆盖元素的 z-index
                const overlayStyle = window.getComputedStyle(elementAtCenter);
                console.error('覆盖元素的 z-index:', overlayStyle.zIndex);
                console.error('覆盖元素的 position:', overlayStyle.position);
            }
            
            // 4. 手动触发点击测试
            console.log('');
            console.log('🧪 测试：手动触发点击事件...');
            
            // 测试 1: 直接调用函数
            if (typeof window.toggleExportMenu === 'function') {
                console.log('✅ toggleExportMenu 函数存在');
                console.log('🧪 测试 1: 直接调用 window.toggleExportMenu()...');
                try {
                    window.toggleExportMenu();
                    console.log('✅ 函数调用成功');
                } catch (e) {
                    console.error('❌ 函数调用失败:', e);
                }
            } else {
                console.error('❌ toggleExportMenu 函数不存在');
            }
            
            console.log('');
            console.log('🔍🔍🔍 诊断完成 🔍🔍🔍');
            console.log('');
            console.log('📋 如果看到 "按钮被其他元素覆盖"，请告诉我覆盖元素的信息');
            console.log('📋 如果没有看到菜单弹出，请截图整个 Console');
            
        }, 2000);  // 等待2秒后执行，确保页面完全加载
'''
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {html_file}:")
        print("=" * 50)
        
        # 在 </script> 标签前（Export 功能的最后）添加诊断代码
        # 找到最后一个包含 Export 功能的 </script>
        pattern = r"(console\.log\('✅ Export 功能已加载（全新版本 \+ 备用 listener）'\);)"
        
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                r"\g<1>" + diagnostic_code,
                content
            )
            print("✅ 添加终极诊断代码")
        else:
            print("⚠️ 未找到插入点")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {html_file}")

def main():
    print("🔍 添加终极诊断代码\n")
    
    print("=" * 60)
    print("诊断内容")
    print("=" * 60)
    print("1. 检查按钮的 CSS 属性（display, visibility, pointer-events 等）")
    print("2. 检查按钮的位置和尺寸")
    print("3. 检查按钮中心点是否有其他元素覆盖")
    print("4. 手动触发点击事件测试")
    print("5. 直接调用 toggleExportMenu 函数测试")
    
    print("\n" + "=" * 60)
    print("开始添加...")
    print("=" * 60)
    
    add_ultimate_diagnostic()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 新的日志流程：")
    print("页面加载后 2 秒：")
    print("  🔍🔍🔍 开始终极诊断 🔍🔍🔍")
    print("  ✅ Export 按钮存在: ...")
    print("  📊 按钮样式: ...")
    print("  📍 按钮位置: ...")
    print("  🎯 按钮中心点的元素: ...")
    print("  🧪 测试：手动触发点击事件...")
    print("  ✅ toggleExportMenu 函数存在")
    print("  🧪 测试 1: 直接调用 window.toggleExportMenu()...")
    print("  ✅ 函数调用成功")
    print("  🔍 toggleExportMenu Called  ← 如果看到这个，说明函数可以工作")
    print("  ... （菜单应该弹出）")
    print("  🔍🔍🔍 诊断完成 🔍🔍🔍")
    
    print("\n🚀 请刷新页面，等待 2 秒，查看 Console 输出！")
    print("\n⚠️ 重点关注：")
    print("• 是否有 '❌❌❌ 发现问题！按钮被其他元素覆盖了！'")
    print("• 手动调用函数后，菜单是否弹出")
    print("• 如果手动调用可以弹出，说明是点击事件被阻止")

if __name__ == '__main__':
    main()

