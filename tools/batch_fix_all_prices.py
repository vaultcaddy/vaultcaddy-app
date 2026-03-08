#!/usr/bin/env python3
"""批量修正所有7个地区70篇文章的价格（使用真实价格 + 20% OFF）"""
import os
import re

# 真实价格数据（基于用户提供的年费）
REAL_PRICES = {
    'en-us': {
        'old': ['$5.59', '$8.59', '$11.59', '$0.06'],
        'new': ['$4.79', '$7.19', '$9.59', '$0.05'],  # $71.81/12*0.8 = $4.79
        'annual': '$71.81',
        'discount_annual': '$57.45',  # $71.81 * 0.8
    },
    'en-gb': {
        'old': ['£4.99', '£7.49', '£9.99', '£0.05'],
        'new': ['£3.57', '£5.36', '£7.14', '£0.04'],  # £53.57/12*0.8 = £3.57
        'annual': '£53.57',
        'discount_annual': '£42.86',
    },
    'en-ca': {
        'old': ['CAD $7.99', 'CAD $11.99', 'CAD $14.99', 'CAD $0.08'],
        'new': ['CAD $6.46', 'CAD $9.69', 'CAD $12.92', 'CAD $0.07'],
        'annual': 'CAD $96.94',
        'discount_annual': 'CAD $77.55',
    },
    'en-au': {
        'old': ['AUD $8.99', 'AUD $12.99', 'AUD $16.99', 'AUD $0.09'],
        'new': ['AUD $7.18', 'AUD $10.78', 'AUD $14.37', 'AUD $0.07'],
        'annual': 'AUD $107.72',
        'discount_annual': 'AUD $86.18',
    },
    'en-nz': {
        'old': ['NZD $9.99', 'NZD $14.99', 'NZD $19.99', 'NZD $0.09'],
        'new': ['NZD $7.66', 'NZD $11.49', 'NZD $15.32', 'NZD $0.08'],
        'annual': 'NZD $114.90',
        'discount_annual': 'NZD $91.92',
    },
    'en-sg': {
        'old': ['SGD $7.99', 'SGD $11.99', 'SGD $15.99', 'SGD $0.08'],
        'new': ['SGD $6.46', 'SGD $9.69', 'SGD $12.92', 'SGD $0.07'],
        'annual': 'SGD $96.94',
        'discount_annual': 'SGD $77.55',
    },
    'en-ie': {
        'old': ['€5.99', '€8.99', '€11.99', '€0.05'],
        'new': ['€4.02', '€6.03', '€8.04', '€0.04'],
        'annual': '€60.29',
        'discount_annual': '€48.23',
    },
}

def fix_prices_in_file(filepath, region_code):
    """修正单个文件中的价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        prices = REAL_PRICES[region_code]
        changes = 0
        
        # 替换价格
        for old_price, new_price in zip(prices['old'], prices['new']):
            # 精确匹配价格（避免部分匹配）
            old_escaped = re.escape(old_price)
            pattern = r'\b' + old_escaped + r'\b'
            new_content = re.sub(pattern, new_price, content)
            if new_content != content:
                changes += 1
                content = new_content
        
        # 如果有变化，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        return False, 0
        
    except Exception as e:
        print(f"      ❌ 错误: {e}")
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
    
    regions = ['en-us', 'en-gb', 'en-ca', 'en-au', 'en-nz', 'en-sg', 'en-ie']
    region_flags = {
        'en-us': '🇺🇸', 'en-gb': '🇬🇧', 'en-ca': '🇨🇦', 'en-au': '🇦🇺',
        'en-nz': '🇳🇿', 'en-sg': '🇸🇬', 'en-ie': '🇮🇪'
    }
    
    print("=" * 70)
    print("💰 批量修正所有文章价格（真实价格 + 20% OFF）")
    print("=" * 70)
    print("\n📊 正确价格：")
    for region in regions:
        prices = REAL_PRICES[region]
        flag = region_flags[region]
        print(f"  {flag} {region}: {prices['new'][0]}/月 (原价 {prices['annual']}/年)")
    print("=" * 70)
    
    total_files = 0
    total_updated = 0
    
    for region in regions:
        flag = region_flags[region]
        print(f"\n{flag} {region.upper()}")
        
        blog_dir = os.path.join(base_dir, region, 'blog')
        if not os.path.exists(blog_dir):
            print(f"  ⚠️  目录不存在，跳过")
            continue
        
        region_updated = 0
        for filename in files_to_update:
            filepath = os.path.join(blog_dir, filename)
            if not os.path.exists(filepath):
                continue
            
            success, changes = fix_prices_in_file(filepath, region)
            total_files += 1
            if success:
                region_updated += 1
                total_updated += 1
                print(f"  ✅ {filename} (修改{changes}处)")
            else:
                print(f"  ℹ️  {filename} (无需修改)")
        
        print(f"  📝 本地区更新: {region_updated}/10")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 处理文件: {total_files}")
    print(f"✅ 成功更新: {total_updated}")
    print("=" * 70)
    
    print("\n💡 价格修正说明：")
    print("   ✅ 所有价格基于真实年费")
    print("   ✅ 已应用20% OFF优惠")
    print("   ✅ 价格更具竞争力")
    print("\n🎉 价格修正完成！")

if __name__ == "__main__":
    main()

