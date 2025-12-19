#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新所有页面的优惠横幅文字
将"首月 8 折"改为"8 折"
"""

import os
import glob

def update_promo_text(filepath):
    """更新单个文件的优惠文字"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含旧文字
        if '首月 8 折' not in content and '首月8折' not in content:
            return False
        
        # 替换所有变体
        content = content.replace('首月 8 折', '8 折')
        content = content.replace('首月8折', '8折')
        content = content.replace('本月註冊立享首月 8 折', '本月註冊立享 8 折')
        content = content.replace('本月註冊立享首月8折', '本月註冊立享8折')
        
        # 同时更新英文版本
        content = content.replace('First Month 20% Off', '20% Off')
        content = content.replace('首月20% Off', '20% Off')
        
        # 同时更新CTA按钮文字
        content = content.replace('免費試用（首月8折）', '免費試用（8折）')
        content = content.replace('免費試用20頁（首月8折）', '免費試用20頁（8折）')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ⚠️  错误: {filepath} - {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🔄 批量更新优惠横幅文字：首月 8 折 → 8 折")
    print("=" * 70)
    print()
    
    updated_count = 0
    total_count = 0
    
    # 定义所有需要更新的文件模式
    file_patterns = [
        '/Users/cavlinyeung/ai-bank-parser/index.html',
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
            if update_promo_text(filepath):
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
    print("更新内容：")
    print("  • '首月 8 折' → '8 折'")
    print("  • '本月註冊立享首月 8 折' → '本月註冊立享 8 折'")
    print("  • '免費試用（首月8折）' → '免費試用（8折）'")
    print("  • 'First Month 20% Off' → '20% Off'")
    print()
    print("所有Landing Page的优惠文字已统一更新！🎉")

if __name__ == '__main__':
    main()

