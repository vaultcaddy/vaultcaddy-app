#!/usr/bin/env python3
"""
🔥 修复 Export 菜单尺寸和显示问题

问题：菜单框太小或样式冲突导致内容不可见
解决：
1. 移除外层 padding（让内容自己控制）
2. 增加 minHeight 确保有足够空间
3. 添加 overflow: auto 防止内容被裁剪
4. 设置明显的背景色和边框用于调试
"""

import os
import re

def fix_menu_display_styles():
    """修复所有版本的菜单显示样式"""
    
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
        
        # 修复 toggleExportMenu 中的菜单样式设置
        # 查找设置菜单样式的部分
        pattern = r"(menu\.style\.display = 'block';)\s+" \
                  r"(menu\.style\.position = 'fixed';)\s+" \
                  r"(menu\.style\.top = '50%';)\s+" \
                  r"(menu\.style\.left = '50%';)\s+" \
                  r"(menu\.style\.transform = 'translate\(-50%, -50%\)';)\s+" \
                  r"(menu\.style\.zIndex = '[^']+';)\s+" \
                  r"(menu\.style\.background = '[^']+';)\s+" \
                  r"(menu\.style\.borderRadius = '[^']+';)\s+" \
                  r"(menu\.style\.boxShadow = '[^']+';)\s+" \
                  r"(menu\.style\.minWidth = '[^']+';)\s+" \
                  r"(menu\.style\.maxWidth = '[^']+';)\s+" \
                  r"(menu\.style\.padding = '[^']+';)"
        
        replacement = r"""\1
            \2
            \3
            \4
            \5
            \6
            menu.style.background = 'white';
            menu.style.borderRadius = '12px';
            menu.style.boxShadow = '0 25px 50px rgba(0,0,0,0.25)';
            menu.style.minWidth = '350px';
            menu.style.maxWidth = '500px';
            menu.style.minHeight = '400px';
            menu.style.maxHeight = '80vh';
            menu.style.overflow = 'auto';
            menu.style.padding = '0';
            menu.style.border = '2px solid #10b981';"""
        
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file} 的菜单样式")

def main():
    print("🔥 修复 Export 菜单尺寸和显示问题...\n")
    
    print("=" * 60)
    print("修复菜单样式")
    print("=" * 60)
    
    fix_menu_display_styles()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• minWidth: 280px → 350px （更宽）")
    print("• maxWidth: 90% → 500px （固定最大宽度）")
    print("• minHeight: 新增 400px （确保有足够高度）")
    print("• maxHeight: 新增 80vh （不超过视口80%）")
    print("• overflow: 新增 auto （内容过多时可滚动）")
    print("• padding: 1rem → 0 （让内容自己控制）")
    print("• border: 新增绿色边框（调试用，可见菜单边界）")
    
    print("\n🔍 验证步骤：")
    print("1. 刷新页面（Cmd/Ctrl + R）")
    print("2. 点击 Export 按钮")
    print("3. 应该看到：")
    print("   - 更大的白色框")
    print("   - 绿色边框（明显可见）")
    print("   - 完整的导出选项")
    
    print("\n💡 如果还是看不到内容：")
    print("说明问题在菜单内容本身，不是框的大小")

if __name__ == '__main__':
    main()

