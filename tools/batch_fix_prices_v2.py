#!/usr/bin/env python3
"""批量修正所有文章价格 V2 - 全局替换版本"""
import os
import re

# 真实价格映射（所有可能出现的价格变体）
PRICE_MAPPINGS = {
    'en-us': {
        '$5.59': '$4.79',
        '$8.59': '$7.19',
        '$11.59': '$9.59',
        '$17.59': '$14.39',
        '$0.06': '$0.05',
        '$46': '$39',
        '$66': '$56',
        '$149': '$126',
        '$468': '$395',  # Dext价格保持不变
    },
    'en-gb': {
        '£4.99': '£3.57',
        '£7.49': '£5.36',
        '£9.99': '£7.14',
        '£14.99': '£10.71',
        '£0.05': '£0.04',
        '£39': '£33',
        '£55': '£47',
        '£125': '£106',
        '£395': '£334',
    },
    'en-ca': {
        'CAD $7.99': 'CAD $6.46',
        'CAD $11.99': 'CAD $9.69',
        'CAD $14.99': 'CAD $12.92',
        'CAD $23.99': 'CAD $19.19',
        'CAD $0.08': 'CAD $0.07',
        'CAD $59': 'CAD $50',
        'CAD $189': 'CAD $160',
        'CAD $595': 'CAD $503',
    },
    'en-au': {
        'AUD $8.99': 'AUD $7.18',
        'AUD $12.99': 'AUD $10.78',
        'AUD $16.99': 'AUD $14.37',
        'AUD $26.99': 'AUD $21.59',
        'AUD $0.09': 'AUD $0.07',
        'AUD $65': 'AUD $55',
        'AUD $209': 'AUD $177',
        'AUD $659': 'AUD $558',
    },
    'en-nz': {
        'NZD $9.99': 'NZD $7.66',
        'NZD $14.99': 'NZD $11.49',
        'NZD $19.99': 'NZD $15.32',
        'NZD $29.99': 'NZD $22.98',
        'NZD $0.09': 'NZD $0.08',
        'NZD $69': 'NZD $58',
        'NZD $219': 'NZD $185',
        'NZD $699': 'NZD $591',
    },
    'en-sg': {
        'SGD $7.99': 'SGD $6.46',
        'SGD $11.99': 'SGD $9.69',
        'SGD $15.99': 'SGD $12.92',
        'SGD $23.99': 'SGD $19.19',
        'SGD $0.08': 'SGD $0.07',
        'SGD $59': 'SGD $50',
        'SGD $189': 'SGD $160',
        'SGD $595': 'SGD $503',
    },
    'en-ie': {
        '€5.99': '€4.02',
        '€8.99': '€6.03',
        '€11.99': '€8.04',
        '€17.99': '€12.06',
        '€0.05': '€0.04',
        '€45': '€38',
        '€145': '€123',
        '€459': '€388',
    },
}

def fix_prices_in_file(filepath, region_code):
    """修正文件中的所有价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        mappings = PRICE_MAPPINGS.get(region_code, {})
        total_changes = 0
        
        # 按价格从高到低排序，避免部分匹配问题
        sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_price, new_price in sorted_mappings:
            # 使用简单的字符串替换
            count = content.count(old_price)
            if count > 0:
                content = content.replace(old_price, new_price)
                total_changes += count
        
        # 如果有变化，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_changes
        return False, 0
        
    except Exception as e:
        return False, 0

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    files_to_update = [
        'vaultcaddy-vs-dext-comparison-2025.html',
        'how-to-convert-bank-statements-to-excel-2025.html',
        'top-10-accounting-software-2025.html',
        'vaultcaddy-vs-expensify-comparison-2025.html',
        'pdf-bank-statement-cannot-copy-text-solutions-2025.html',
        'quickbooks-import-bank-statement-error-fix-2025.html',
        'vaultcaddy-vs-quickbooks-comparison-2025.html',
        'restaurant-accounting-system-guide-2025.html',
        'manual-data-entry-vs-ai-automation-2025.html',
        'bank-statement-ocr-guide-2025.html',
    ]
    
    regions = {
        'en-us': '🇺🇸', 'en-gb': '🇬🇧', 'en-ca': '🇨🇦', 'en-au': '🇦🇺',
        'en-nz': '🇳🇿', 'en-sg': '🇸🇬', 'en-ie': '🇮🇪'
    }
    
    print("=" * 70)
    print("💰 批量修正所有文章价格 V2（全局替换）")
    print("=" * 70)
    print("\n📊 新价格（20% OFF后）：")
    new_prices = {
        'en-us': '$4.79/月', 'en-gb': '£3.57/月', 'en-ca': 'CAD $6.46/月',
        'en-au': 'AUD $7.18/月', 'en-nz': 'NZD $7.66/月', 
        'en-sg': 'SGD $6.46/月', 'en-ie': '€4.02/月'
    }
    for region, flag in regions.items():
        print(f"  {flag} {region}: {new_prices[region]}")
    print("=" * 70)
    
    total_updated = 0
    total_changes = 0
    
    for region, flag in regions.items():
        print(f"\n{flag} {region.upper()}")
        
        blog_dir = os.path.join(base_dir, region, 'blog')
        if not os.path.exists(blog_dir):
            print(f"  ⚠️  目录不存在")
            continue
        
        region_updated = 0
        region_changes = 0
        for filename in files_to_update:
            filepath = os.path.join(blog_dir, filename)
            if not os.path.exists(filepath):
                continue
            
            success, changes = fix_prices_in_file(filepath, region)
            if success and changes > 0:
                region_updated += 1
                region_changes += changes
                total_updated += 1
                total_changes += changes
                print(f"  ✅ {filename} ({changes}处)")
        
        if region_updated > 0:
            print(f"  📝 本地区: {region_updated}/10 文件, {region_changes} 处修改")
        else:
            print(f"  ℹ️  本地区无需修改")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 成功更新: {total_updated}/70 文件")
    print(f"✅ 总计修改: {total_changes} 处价格")
    print("=" * 70)
    print("\n💡 修正说明：")
    print("   ✅ 基于真实年费计算月费")
    print("   ✅ 已应用20% OFF优惠")
    print("   ✅ 价格更具竞争力")
    print("\n🎉 价格修正完成！")

if __name__ == "__main__":
    main()

