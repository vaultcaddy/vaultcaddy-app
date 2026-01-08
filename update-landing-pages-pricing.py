#!/usr/bin/env python3
"""
批量更新所有Landing Page的价格信息
从 HKD $46 更新为 USD $2.88
"""

import os
import re
from pathlib import Path

# 定义需要更新的文件模式
PATTERNS = [
    'convert-*.html',
    '*-bank-statement-*.html',
    '*-to-qbo.html',
    '*-to-xero.html',
    'index.html'
]

# 定义替换规则
REPLACEMENTS = {
    # 中文版更新
    (r'月費\$46起', '從 $2.88/月起'),
    (r'月费\$46', '從 $2.88/月'),
    (r'HKD\s*\$?\s*46', 'USD $2.88'),
    (r'港幣\s*\$?\s*46', '美元 $2.88'),
    (r'比Dext便宜70%', '比競品便宜85%'),
    
    # Schema.org更新
    (r'"price":\s*"46"', '"price": "2.88"'),
    (r'"priceCurrency":\s*"HKD"', '"priceCurrency": "USD"'),
    (r'"priceRange":\s*"HKD\s+0\.46\s*-\s*HKD\s+58"', '"priceRange": "USD 2.88 - USD 14.99"'),
    
    # 英文版更新
    (r'From \$5\.59/month', 'From $2.88/month'),
    (r'Starting at \$5\.59', 'Starting at $2.88'),
    (r'\$5\.59\s*/\s*month', '$2.88/month'),
    (r'HKD\s+46', 'USD 2.88'),
    
    # 日文版更新 (假设有的话)
    (r'月額\s*\$?\s*46', '月額 $2.88'),
    (r'HKD\s*46', 'USD 2.88'),
    
    # 韩文版更新 (假设有的话)
    (r'월\s*\$?\s*46', '월 $2.88'),
    (r'HKD\s*46', 'USD 2.88'),
}

def update_file(filepath):
    """更新单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # 应用所有替换规则
        for pattern, replacement in REPLACEMENTS:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes += count
        
        # 如果有更改，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
    except Exception as e:
        print(f"❌ 更新失败 {filepath}: {e}")
        return 0

def main():
    """主函数"""
    root = Path('.')
    updated_files = []
    total_changes = 0
    
    print("🚀 开始批量更新Landing Page价格...")
    print()
    
    # 遍历所有HTML文件
    for pattern in PATTERNS:
        for filepath in sorted(root.glob(pattern)):
            changes = update_file(filepath)
            if changes > 0:
                updated_files.append((str(filepath), changes))
                total_changes += changes
                print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    # 同步更新多语言版本
    for lang in ['en', 'kr', 'jp']:
        lang_dir = root / lang
        if lang_dir.exists():
            print(f"\n📂 更新 {lang.upper()} 版本...")
            for pattern in PATTERNS:
                for filepath in sorted(lang_dir.glob(pattern)):
                    changes = update_file(filepath)
                    if changes > 0:
                        updated_files.append((str(filepath), changes))
                        total_changes += changes
                        print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    print()
    print("=" * 80)
    print(f"📊 更新总结:")
    print(f"✅ 已更新 {len(updated_files)} 个文件")
    print(f"🔢 总共 {total_changes} 处修改")
    print()
    
    if updated_files:
        print(f"📋 详细列表:")
        for filepath, changes in updated_files:
            print(f"  - {filepath}: {changes} 处修改")
    else:
        print("⚠️  未找到需要更新的文件")
    
    print()
    print("✨ 更新完成！")
    print()
    print("🎯 下一步:")
    print("  1. 测试更新后的页面")
    print("  2. 检查价格显示是否正确")
    print("  3. 验证Schema.org标记")
    print("  4. 提交到Git")

if __name__ == '__main__':
    main()

