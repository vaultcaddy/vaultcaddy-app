#!/usr/bin/env python3
"""
🔥 修改手机版布局：BackDashboard 和 Delete 按钮同行显示

修改：
1. 在手机版中，BackDashboard 和 Delete 按钮在同一行
2. BackDashboard 在左，Delete 在右
3. 保持桌面版不变
"""

import os
import re

def fix_mobile_layout():
    """修改手机版布局"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    for file in files:
        if not os.path.exists(file):
            continue
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {file}:")
        print("=" * 50)
        
        # 1. 修改手机版CSS - 找到 @media (max-width: 768px) 中的 .detail-header 部分
        # 修改 .detail-header 为 flex-direction: row (第一行是横向的)
        
        old_css = r'''(\s+)(\.detail-header \{[^}]*?)flex-direction: column !important;([^}]*?\})'''
        
        new_css = r'''\1\2flex-direction: row !important;
            flex-wrap: wrap !important;\3'''
        
        if re.search(old_css, content):
            content = re.sub(old_css, new_css, content)
            print("✅ 修改 .detail-header 为横向布局")
        
        # 2. 修改 .back-btn 在手机版中不占满整行，而是自适应宽度
        old_back_btn = r'''(\.detail-header \.back-btn \{[^}]*?)width: 100% !important;([^}]*?\})'''
        
        new_back_btn = r'''\1flex: 0 0 auto !important;
                width: auto !important;\2'''
        
        if re.search(old_back_btn, content):
            content = re.sub(old_back_btn, new_back_btn, content)
            print("✅ 修改 .back-btn 为自适应宽度")
        
        # 3. 为 Delete 按钮添加手机版专用样式 - 添加在 .detail-header .back-btn 之后
        # 查找是否已存在 .detail-header .icon-btn.delete 在手机版中的样式
        
        mobile_delete_pattern = r'\.detail-header \.top-actions \.icon-btn\.delete \{'
        
        if re.search(mobile_delete_pattern, content):
            # 已存在，修改它
            old_delete_css = r'''(\.detail-header \.top-actions \.icon-btn\.delete \{[^}]*?)flex: 1 !important;([^}]*?\})'''
            
            new_delete_css = r'''\1flex: 0 0 auto !important;
                width: auto !important;
                margin-left: auto !important;\2'''
            
            content = re.sub(old_delete_css, new_delete_css, content)
            print("✅ 修改 Delete 按钮样式（靠右显示）")
        else:
            # 不存在，在 .detail-header .back-btn:hover 之后添加
            insert_point = r'(\.detail-header \.back-btn:hover \{[^}]+\})'
            
            new_delete_style = r'''\1
            
            /* 🔥 手機版：Delete 按钮靠右显示 */
            .detail-header .top-actions {
                position: absolute !important;
                right: 1rem !important;
                top: 0.75rem !important;
                width: auto !important;
            }
            
            .detail-header .top-actions .icon-btn.delete {
                flex: 0 0 auto !important;
                width: auto !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.875rem !important;
            }'''
            
            content = re.sub(insert_point, new_delete_style, content)
            print("✅ 添加 Delete 按钮手机版样式")
        
        # 4. 确保文档标题在第二行完整显示
        old_title = r'''(\.detail-header \.document-title \{[^}]*?)width: 100% !important;([^}]*?\})'''
        
        new_title = r'''\1width: 100% !important;
                flex-basis: 100% !important;
                order: 2 !important;\2'''
        
        if re.search(old_title, content):
            content = re.sub(old_title, new_title, content)
            print("✅ 修改文档标题为第二行")
        
        # 5. 设置 .back-btn 和 .top-actions 的 order
        # 给 .back-btn 添加 order: 1
        back_btn_order = r'(\.detail-header \.back-btn \{[^}]*?)(transition: all 0\.2s !important;)'
        
        content = re.sub(
            back_btn_order,
            r'\1\2\n                order: 1 !important;',
            content
        )
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 修改手机版布局：BackDashboard 和 Delete 同行显示\n")
    
    print("=" * 60)
    print("开始修改...")
    print("=" * 60)
    
    fix_mobile_layout()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 修改内容：")
    print("• ✅ BackDashboard 在左边")
    print("• ✅ Delete 按钮在右边")
    print("• ✅ 两个按钮在同一行")
    print("• ✅ 文档标题在第二行")
    print("• ✅ 桌面版布局不变")
    
    print("\n🚀 请在手机版刷新页面测试！")

if __name__ == '__main__':
    main()

