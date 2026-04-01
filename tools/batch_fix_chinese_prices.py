#!/usr/bin/env python3
"""修正中文版本（香港）的价格"""
import os

# 香港的价格映射（假设使用HKD）
# 基于 HKD 1 = USD 0.128 的汇率
# USD $71.81 ≈ HKD $561
# 月费: HKD $561/12 = HKD $46.75
# 20% OFF: HKD $46.75 * 0.8 = HKD $37.40

PRICE_MAPPINGS = {
    'HK$69': 'HK$37',  # 月费（20% OFF后取整）
    'HK$103': 'HK$56',  # 150页
    'HK$138': 'HK$74',  # 200页
    'HK$0.60': 'HK$0.48',  # 额外页费
    'HK$828': 'HK$448',  # 年费（20% OFF后）
}

def fix_prices_in_file(filepath):
    """修正文件中的价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_changes = 0
        
        # 按长度排序避免部分匹配
        sorted_mappings = sorted(PRICE_MAPPINGS.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_price, new_price in sorted_mappings:
            count = content.count(old_price)
            if count > 0:
                content = content.replace(old_price, new_price)
                total_changes += count
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_changes
        return False, 0
        
    except Exception as e:
        return False, 0

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    blog_dir = os.path.join(base_dir, 'blog')
    
    files_to_update = [
        'vaultcaddy-vs-dext-comparison-2025.html',
        'hsbc-bank-statement-to-excel-guide-2025.html',
        'hong-kong-accounting-software-top-10-2025.html',
        'restaurant-accounting-system-guide-2025.html',
        'vaultcaddy-vs-expensify-comparison-2025.html',
        'hang-seng-bank-statement-to-excel-guide-2025.html',
        'pdf-bank-statement-cannot-copy-text-solutions-2025.html',
        'quickbooks-import-bank-statement-error-fix-2025.html',
        'vaultcaddy-vs-quickbooks-comparison-2025.html',
        'manual-data-entry-vs-ai-automation-2025.html',
    ]
    
    print("=" * 70)
    print("💰 修正中文版（香港）价格")
    print("=" * 70)
    print("\n📊 新价格（20% OFF后）：")
    print("  🇭🇰 香港: HK$37/月（原价HK$561/年，月费HK$46.75）")
    print("  💡 计算: HK$46.75 × 0.8 = HK$37.40 ≈ HK$37")
    print("=" * 70)
    
    if not os.path.exists(blog_dir):
        print("\n⚠️  中文博客目录不存在")
        return
    
    print("\n🇭🇰 中文版（香港）")
    updated = 0
    total_changes = 0
    
    for filename in files_to_update:
        filepath = os.path.join(blog_dir, filename)
        if os.path.exists(filepath):
            success, changes = fix_prices_in_file(filepath)
            if success and changes > 0:
                updated += 1
                total_changes += changes
                print(f"  ✅ {filename} ({changes}处)")
    
    print(f"\n  📝 更新: {updated}/10 文件, {total_changes} 处修改")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 成功更新: {updated}/10 文件")
    print(f"✅ 总计修改: {total_changes} 处")
    print("=" * 70)
    print("\n🎉 中文版价格修正完成！")

if __name__ == "__main__":
    main()

