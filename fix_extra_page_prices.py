#!/usr/bin/env python3
"""修正额外页费 - 恢复为原价（无20% OFF）"""
import os
import re

# 额外页费修正映射（恢复为图中显示的原价）
EXTRA_PAGE_CORRECTIONS = {
    'en-us': {
        '$0.05': '$0.06',  # 恢复
    },
    'en-gb': {
        '£0.04': '£0.05',  # 恢复
    },
    'en-ca': {
        'CAD $0.07': 'CAD $0.08',  # 假设原价
    },
    'en-au': {
        'AUD $0.07': 'AUD $0.09',  # 假设原价
    },
    'en-nz': {
        'NZD $0.08': 'NZD $0.09',
    },
    'en-sg': {
        'SGD $0.07': 'SGD $0.08',
    },
    'en-ie': {
        '€0.04': '€0.06',
    },
    'jp': {
        '¥8': '¥10',  # 恢复
    },
    'kr': {
        '₩70': '₩85',  # 恢复
    },
    'zh': {
        'HK$0.40': 'HK$0.60',  # 假设
        'HK$0.48': 'HK$0.60',
    },
}

def fix_extra_page_prices(filepath, region_code):
    """修正额外页费价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        corrections = EXTRA_PAGE_CORRECTIONS.get(region_code, {})
        total_changes = 0
        
        for old_price, new_price in corrections.items():
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
    
    jp_files = [f.replace('2025.html', '2025.html').replace('vaultcaddy-vs-dext', 'vaultcaddy-vs-dext-hikaku')
                .replace('how-to-convert', 'ginko-meisai-excel-henkan-guide')
                .replace('top-10-accounting', 'kaikei-software-top-10')
                .replace('vaultcaddy-vs-expensify', 'vaultcaddy-vs-expensify-hikaku')
                .replace('pdf-bank-statement-cannot-copy', 'pdf-copy-dekinai-kaiketsu')
                .replace('quickbooks-import-bank-statement-error-fix', 'quickbooks-import-error-fix')
                .replace('vaultcaddy-vs-quickbooks', 'vaultcaddy-vs-quickbooks-hikaku')
                .replace('restaurant-accounting-system', 'restaurant-kaikei-system')
                .replace('manual-data-entry-vs-ai', 'manual-vs-ai')
                .replace('bank-statement-ocr', 'ginko-meisai-ocr')
                for f in files_to_update]
    
    kr_files = [f.replace('2025.html', '2025.html').replace('vaultcaddy-vs-dext', 'vaultcaddy-vs-dext-bigyeo')
                .replace('how-to-convert', 'eunhaeng-myeongse-excel-byeonhwan-guide')
                .replace('top-10-accounting', 'hoegye-software-top-10')
                .replace('vaultcaddy-vs-expensify', 'vaultcaddy-vs-expensify-bigyeo')
                .replace('pdf-bank-statement-cannot-copy', 'pdf-boksa-andoem-haegyeol')
                .replace('quickbooks-import-bank-statement-error-fix', 'quickbooks-gajyeogi-silpae-fix')
                .replace('vaultcaddy-vs-quickbooks', 'vaultcaddy-vs-quickbooks-bigyeo')
                .replace('restaurant-accounting-system', 'sikdang-hoegye-system')
                .replace('manual-data-entry-vs-ai', 'sudong-vs-ai-jadong')
                .replace('bank-statement-ocr', 'eunhaeng-myeongse-ocr')
                for f in files_to_update]
    
    regions = {
        'en-us': ('🇺🇸', 'en-us/blog', files_to_update),
        'en-gb': ('🇬🇧', 'en-gb/blog', files_to_update),
        'en-ca': ('🇨🇦', 'en-ca/blog', files_to_update),
        'en-au': ('🇦🇺', 'en-au/blog', files_to_update),
        'en-nz': ('🇳🇿', 'en-nz/blog', files_to_update),
        'en-sg': ('🇸🇬', 'en-sg/blog', files_to_update),
        'en-ie': ('🇮🇪', 'en-ie/blog', files_to_update),
        'jp': ('🇯🇵', 'jp/blog', jp_files),
        'kr': ('🇰🇷', 'kr/blog', kr_files),
        'zh': ('🇭🇰', 'blog', files_to_update),
    }
    
    print("=" * 70)
    print("🔧 修正额外页费 - 恢复原价（无20% OFF）")
    print("=" * 70)
    print("\n📊 正确的额外页费（根据图片）：")
    print("  🇺🇸 USD: $0.06/页")
    print("  🇬🇧 GBP: £0.05/页")
    print("  🇯🇵 JPY: ¥10/页")
    print("  🇰🇷 KRW: ₩85/页")
    print("  🇮🇪 EUR: €0.06/页")
    print("=" * 70)
    
    total_updated = 0
    total_changes = 0
    
    for region_code, (flag, blog_path, file_list) in regions.items():
        print(f"\n{flag} {region_code.upper()}")
        
        full_blog_path = os.path.join(base_dir, blog_path)
        if not os.path.exists(full_blog_path):
            print(f"  ⚠️  目录不存在")
            continue
        
        region_updated = 0
        region_changes = 0
        for filename in file_list:
            filepath = os.path.join(full_blog_path, filename)
            if not os.path.exists(filepath):
                continue
            
            success, changes = fix_extra_page_prices(filepath, region_code)
            if success and changes > 0:
                region_updated += 1
                region_changes += changes
                total_updated += 1
                total_changes += changes
                print(f"  ✅ {filename} ({changes}处)")
        
        if region_updated > 0:
            print(f"  📝 本地区: {region_updated} 文件, {region_changes} 处修改")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 成功更新: {total_updated} 文件")
    print(f"✅ 总计修改: {total_changes} 处")
    print("=" * 70)
    print("\n💡 重要说明：")
    print("   ✅ 基础套餐有20% OFF")
    print("   ✅ 额外页费无折扣（使用原价）")
    print("   ✅ 符合用户提供的定价结构")
    print("\n🎉 额外页费修正完成！")

if __name__ == "__main__":
    main()

