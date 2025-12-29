#!/usr/bin/env python3
"""修正日本和韩国版本的价格"""
import os

# 日本和韩国的价格映射
PRICE_MAPPINGS = {
    'jp': {
        '¥926': '¥741',  # ¥11,117/12*0.8 = ¥741
        '¥1,389': '¥1,111',  # 150页
        '¥1,852': '¥1,482',  # 200页
        '¥10': '¥8',  # 额外页费
    },
    'kr': {
        '₩7,998': '₩6,968',  # ₩104,525/12*0.8 = ₩8,710*0.8 = ₩6,968
        '₩8,710': '₩6,968',  # 正确的原价/12再*0.8
        '₩11,998': '₩10,453',
        '₩15,996': '₩13,937',
        '₩80': '₩70',
    },
}

def fix_prices_in_file(filepath, lang):
    """修正文件中的价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        mappings = PRICE_MAPPINGS.get(lang, {})
        total_changes = 0
        
        # 按长度排序避免部分匹配
        sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
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
    
    files_to_update = [
        'vaultcaddy-vs-dext-hikaku-2025.html',
        'ginko-meisai-excel-henkan-guide-2025.html',
        'kaikei-software-top-10-2025.html',
        'vaultcaddy-vs-expensify-hikaku-2025.html',
        'pdf-copy-dekinai-kaiketsu-2025.html',
        'quickbooks-import-error-fix-2025.html',
        'vaultcaddy-vs-quickbooks-hikaku-2025.html',
        'restaurant-kaikei-system-guide-2025.html',
        'manual-vs-ai-automation-2025.html',
        'ginko-meisai-ocr-guide-2025.html',
    ]
    
    kr_files = [
        'vaultcaddy-vs-dext-bigyeo-2025.html',
        'eunhaeng-myeongse-excel-byeonhwan-guide-2025.html',
        'hoegye-software-top-10-2025.html',
        'vaultcaddy-vs-expensify-bigyeo-2025.html',
        'pdf-boksa-andoem-haegyeol-2025.html',
        'quickbooks-gajyeogi-silpae-fix-2025.html',
        'vaultcaddy-vs-quickbooks-bigyeo-2025.html',
        'sikdang-hoegye-system-guide-2025.html',
        'sudong-vs-ai-jadong-2025.html',
        'eunhaeng-myeongse-ocr-guide-2025.html',
    ]
    
    print("=" * 70)
    print("💰 修正日本和韩国版本价格")
    print("=" * 70)
    print("\n📊 新价格（20% OFF后）：")
    print("  🇯🇵 日本: ¥741/月（原价¥11,117/年）")
    print("  🇰🇷 韩国: ₩6,968/月（原价₩104,525/年）")
    print("=" * 70)
    
    # 日本版
    print("\n🇯🇵 日本版")
    jp_blog_dir = os.path.join(base_dir, 'jp', 'blog')
    jp_updated = 0
    jp_changes = 0
    
    if os.path.exists(jp_blog_dir):
        for filename in files_to_update:
            filepath = os.path.join(jp_blog_dir, filename)
            if os.path.exists(filepath):
                success, changes = fix_prices_in_file(filepath, 'jp')
                if success and changes > 0:
                    jp_updated += 1
                    jp_changes += changes
                    print(f"  ✅ {filename} ({changes}处)")
        print(f"  📝 更新: {jp_updated}/10 文件, {jp_changes} 处修改")
    else:
        print("  ⚠️  目录不存在")
    
    # 韩国版
    print("\n🇰🇷 韩国版")
    kr_blog_dir = os.path.join(base_dir, 'kr', 'blog')
    kr_updated = 0
    kr_changes = 0
    
    if os.path.exists(kr_blog_dir):
        for filename in kr_files:
            filepath = os.path.join(kr_blog_dir, filename)
            if os.path.exists(filepath):
                success, changes = fix_prices_in_file(filepath, 'kr')
                if success and changes > 0:
                    kr_updated += 1
                    kr_changes += changes
                    print(f"  ✅ {filename} ({changes}处)")
        print(f"  📝 更新: {kr_updated}/10 文件, {kr_changes} 处修改")
    else:
        print("  ⚠️  目录不存在")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 日本版: {jp_updated}/10 文件, {jp_changes} 处")
    print(f"✅ 韩国版: {kr_updated}/10 文件, {kr_changes} 处")
    print(f"✅ 总计: {jp_changes + kr_changes} 处修改")
    print("=" * 70)
    print("\n🎉 日韩版本价格修正完成！")

if __name__ == "__main__":
    main()

