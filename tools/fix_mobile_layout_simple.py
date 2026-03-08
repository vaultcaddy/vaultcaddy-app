#!/usr/bin/env python3
"""
🔥 修改手机版布局：BackDashboard 和 Delete 按钮同行显示

简单方法：
1. 在手机版中，让 .detail-header 使用 flex-wrap
2. back-btn 和 top-actions(Delete) 在第一行
3. document-title 在第二行（占满整行）
"""

import os
import re

def fix_mobile_layout_simple():
    """修改手机版布局 - 简单方法"""
    
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
        
        # 在手机版CSS中找到 .detail-header 的定义
        # 当前是 flex-direction: column，改为 row + flex-wrap
        
        pattern = r'(@media \(max-width: 768px\).*?)(\.detail-header \{)(.*?)(flex-direction: column !important;)(.*?)(\})'
        
        def replace_detail_header(match):
            prefix = match.group(1)
            class_start = match.group(2)
            before_flex = match.group(3)
            old_flex = match.group(4)
            after_flex = match.group(5)
            class_end = match.group(6)
            
            # 替换为 row + wrap
            new_css = f'''{prefix}{class_start}{before_flex}flex-direction: row !important;
                flex-wrap: wrap !important;{after_flex}{class_end}'''
            
            return new_css
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replace_detail_header, content, flags=re.DOTALL)
            print("✅ 修改 .detail-header 为横向换行布局")
        
        # 修改 .back-btn 不占满整行
        pattern_back = r'(\.detail-header \.back-btn \{)(.*?)(width: 100% !important;)(.*?)(\})'
        
        def replace_back_btn(match):
            start = match.group(1)
            before_width = match.group(2)
            old_width = match.group(3)
            after_width = match.group(4)
            end = match.group(5)
            
            # 改为 flex: 1（占据剩余空间，但会给 Delete 留空间）
            new_css = f'''{start}{before_width}flex: 1 1 auto !important;
                max-width: calc(100% - 120px) !important;{after_width}{end}'''
            
            return new_css
        
        if re.search(pattern_back, content, re.DOTALL):
            content = re.sub(pattern_back, replace_back_btn, content, flags=re.DOTALL)
            print("✅ 修改 .back-btn 宽度")
        
        # 修改 .document-title 占满整行（第二行）
        pattern_title = r'(\.detail-header \.document-title \{)(.*?)(width: 100% !important;)(.*?)(\})'
        
        def replace_title(match):
            start = match.group(1)
            before_width = match.group(2)
            old_width = match.group(3)
            after_width = match.group(4)
            end = match.group(5)
            
            # 添加 flex-basis: 100% 确保换行
            new_css = f'''{start}{before_width}{old_width}
                flex-basis: 100% !important;{after_width}{end}'''
            
            return new_css
        
        if re.search(pattern_title, content, re.DOTALL):
            content = re.sub(pattern_title, replace_title, content, flags=re.DOTALL)
            print("✅ 修改 .document-title 为独占一行")
        
        # 修改 .top-actions 不占满整行，自适应宽度
        pattern_actions = r'(\.detail-header \.top-actions \{)(.*?)(width: 100% !important;)(.*?)(\})'
        
        def replace_actions(match):
            start = match.group(1)
            before_width = match.group(2)
            old_width = match.group(3)
            after_width = match.group(4)
            end = match.group(5)
            
            # 改为自适应宽度
            new_css = f'''{start}{before_width}width: auto !important;
                flex: 0 0 auto !important;{after_width}{end}'''
            
            return new_css
        
        if re.search(pattern_actions, content, re.DOTALL):
            content = re.sub(pattern_actions, replace_actions, content, flags=re.DOTALL)
            print("✅ 修改 .top-actions 为自适应宽度")
        
        # 修改 Delete 按钮不占满空间
        pattern_delete = r'(\.detail-header \.top-actions \.icon-btn\.delete \{)(.*?)(flex: 1 !important;)(.*?)(\})'
        
        def replace_delete(match):
            start = match.group(1)
            before_flex = match.group(2)
            old_flex = match.group(3)
            after_flex = match.group(4)
            end = match.group(5)
            
            # 改为自适应宽度
            new_css = f'''{start}{before_flex}flex: 0 0 auto !important;
                width: auto !important;
                white-space: nowrap !important;{after_flex}{end}'''
            
            return new_css
        
        if re.search(pattern_delete, content, re.DOTALL):
            content = re.sub(pattern_delete, replace_delete, content, flags=re.DOTALL)
            print("✅ 修改 Delete 按钮为自适应宽度")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 修改手机版布局：BackDashboard 和 Delete 同行显示\n")
    
    print("=" * 60)
    print("开始修改...")
    print("=" * 60)
    
    fix_mobile_layout_simple()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 修改效果：")
    print("• ✅ 第一行：[BackDashboard]  [Delete]")
    print("• ✅ 第二行：Document Title（完整显示）")
    print("• ✅ BackDashboard 靠左")
    print("• ✅ Delete 靠右")
    print("• ✅ 桌面版布局不变")
    
    print("\n🚀 请在手机版刷新页面测试！")

if __name__ == '__main__':
    main()

