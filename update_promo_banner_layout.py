#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新所有Landing Page的优惠横幅布局
将单行横幅改为两行布局
"""

import os
import glob
import re

def update_banner_layout(filepath):
    """更新单个文件的横幅布局"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 模式1：查找并替换优惠横幅（单行带优惠码和人数）
        pattern1 = r'<div class="promo-banner">[\s\S]*?⚡ 限時優惠：本月註冊立享 8 折！<span class="promo-code">優惠碼：SAVE20</span>[\s\S]*?</div>'
        
        replacement1 = '''<div class="promo-banner">
        <div style="margin-bottom: 0.5rem;">
            ⚡ 限時優惠：本月註冊立享 8 折！<span class="promo-code">優惠碼：SAVE20</span>
        </div>
        <div style="font-size: 1rem;">
            已有 237 位香港會計師加入
        </div>
    </div>'''
        
        content = re.sub(pattern1, replacement1, content)
        
        # 模式2：查找并替换内联样式的优惠横幅
        pattern2 = r'<div style="background: linear-gradient\(135deg, #f59e0b 0%, #d97706 100%\); color: white; text-align: center; padding: 0\.75rem; font-weight: 600; font-size: 1\.125rem;">[\s\S]*?⚡ 限時優惠：本月註冊立享 8 折！<span[^>]*>優惠碼：SAVE20</span>[\s\S]*?</div>'
        
        replacement2 = '''<div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; text-align: center; padding: 1rem 0.75rem; font-weight: 600; font-size: 1.125rem;">
        <div style="margin-bottom: 0.5rem;">
            ⚡ 限時優惠：本月註冊立享 8 折！<span style="background: white; color: #f59e0b; padding: 0.25rem 1rem; border-radius: 20px; margin-left: 1rem; font-weight: 700;">優惠碼：SAVE20</span>
        </div>
        <div style="font-size: 1rem;">
            已有 237 位香港會計師加入
        </div>
    </div>'''
        
        content = re.sub(pattern2, replacement2, content)
        
        # 如果内容有变化，保存文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ⚠️  错误: {filepath} - {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🔄 批量更新优惠横幅布局：单行 → 两行")
    print("=" * 70)
    print()
    
    updated_count = 0
    total_count = 0
    
    # 定义所有需要更新的文件模式
    file_patterns = [
        '/Users/cavlinyeung/ai-bank-parser/en/index.html',
        '/Users/cavlinyeung/ai-bank-parser/jp/index.html',
        '/Users/cavlinyeung/ai-bank-parser/kr/index.html',
        '/Users/cavlinyeung/ai-bank-parser/*-statement.html',
        '/Users/cavlinyeung/ai-bank-parser/*-bank-*.html',
        '/Users/cavlinyeung/ai-bank-parser/*-helper.html',
        '/Users/cavlinyeung/ai-bank-parser/*-processing.html',
        '/Users/cavlinyeung/ai-bank-parser/*-scanner.html',
        '/Users/cavlinyeung/ai-bank-parser/solutions/*.html',
        '/Users/cavlinyeung/ai-bank-parser/integrations/*.html',
        '/Users/cavlinyeung/ai-bank-parser/for/*.html'
    ]
    
    print("📝 扫描并更新文件...")
    print("-" * 70)
    
    for pattern in file_patterns:
        files = glob.glob(pattern)
        for filepath in files:
            total_count += 1
            if update_banner_layout(filepath):
                updated_count += 1
                filename = os.path.basename(filepath)
                print(f"  ✅ {filename}")
    
    print()
    print("=" * 70)
    print("✅ 更新完成！")
    print("=" * 70)
    print()
    print(f"总计扫描：{total_count} 个文件")
    print(f"成功更新：{updated_count} 个文件")
    print()
    print("布局变化：")
    print("  旧布局（单行）：")
    print("    ⚡ 限時優惠：本月註冊立享 8 折！優惠碼：SAVE20 已有 237 位香港會計師加入")
    print()
    print("  新布局（两行）：")
    print("    第1行：⚡ 限時優惠：本月註冊立享 8 折！優惠碼：SAVE20")
    print("    第2行：已有 237 位香港會計師加入")
    print()
    print("所有Landing Page的优惠横幅布局已统一更新！🎉")

if __name__ == '__main__':
    main()

