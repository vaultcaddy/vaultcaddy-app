#!/usr/bin/env python3
"""
批量创建美国版SEO文章
将现有英文版文章本地化为美国版本
"""

import os
import re

def localize_to_us(content, filename):
    """
    将内容本地化为美国版本
    """
    # 1. 更新HTML lang标签
    content = content.replace('<html lang="en">', '<html lang="en-US">')
    
    # 2. 更新URL路径
    content = content.replace('/en/blog/', '/en-us/blog/')
    content = content.replace('../../en/', '../../en-us/')
    content = content.replace('"../../en/', '"../../en-us/')
    content = content.replace('href="../../en/', 'href="../../en-us/')
    
    # 3. 添加hreflang标签（如果不存在）
    if 'hreflang' not in content:
        # 在Open Graph标签之前插入hreflang
        og_position = content.find('<!-- Open Graph -->')
        if og_position != -1:
            hreflang_tags = '''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en-us" href="https://vaultcaddy.com/en-us/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="en-gb" href="https://vaultcaddy.com/en-gb/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="en" href="https://vaultcaddy.com/en/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="x-default" href="https://vaultcaddy.com/en-us/blog/''' + filename + '''" />
    
'''
            content = content[:og_position] + hreflang_tags + content[og_position:]
    
    # 4. 更新Title和Meta（添加US标识）
    content = re.sub(
        r'<title>(.*?)</title>',
        r'<title>\1 (US)</title>',
        content
    )
    
    # 如果title已经有(US)，不要重复添加
    content = content.replace(' (US) (US)', ' (US)')
    
    # 5. 更新meta description（添加US相关内容）
    def update_description(m):
        desc = m.group(1)
        if "IRS" not in desc and "SOC2" not in desc:
            return f'<meta name="description" content="{desc} IRS compliant, SOC2 certified. Optimized for US banks (Chase, Bank of America, Wells Fargo, Citibank).">'
        return m.group(0)
    
    content = re.sub(
        r'<meta name="description" content="(.*?)">',
        update_description,
        content
    )
    
    # 6. 更新keywords（添加US关键词）
    def update_keywords(m):
        keywords = m.group(1)
        if "US accounting" not in keywords:
            return f'<meta name="keywords" content="{keywords},US accounting,IRS compliant,Chase bank,Bank of America,Wells Fargo,Citibank">'
        return m.group(0)
    
    content = re.sub(
        r'<meta name="keywords" content="(.*?)">',
        update_keywords,
        content
    )
    
    # 7. 香港银行 → 美国银行
    hong_kong_banks_to_us = {
        'Hong Kong banks': 'US banks',
        'Hong Kong bank': 'US bank',
        'HK banks': 'US banks',
        'HSBC': 'Chase',
        'Hang Seng': 'Bank of America',
        'Bank of China': 'Wells Fargo',
        'DBS Bank': 'Citibank',
        'Standard Chartered': 'US Bank',
        'Bank of East Asia': 'TD Bank',
        'HSBC Hong Kong': 'Chase',
        'Hang Seng Bank': 'Bank of America',
        '12 Hong Kong banks': '50+ US banks',
        '12 banks optimized': '50+ US banks optimized',
    }
    
    for hk_bank, us_bank in hong_kong_banks_to_us.items():
        content = content.replace(hk_bank, us_bank)
    
    # 8. 支付方式: 香港 → 美国
    content = content.replace('FPS/PayMe/AlipayHK', 'ACH/Wire/Check/Zelle/Venmo')
    content = content.replace('FPS/PayMe', 'ACH/Zelle')
    content = content.replace('PayMe', 'Venmo')
    content = content.replace('AlipayHK', 'Zelle')
    
    # 9. 地点: 香港 → 美国
    hong_kong_locations_to_us = {
        'Hong Kong': 'United States',
        'Central': 'New York',
        'Central Accounting Firm': 'Manhattan CPA Firm',
        'Wan Chai': 'Los Angeles',
        'Tsim Sha Tsui': 'Chicago',
        'Causeway Bay': 'San Francisco',
        'Mong Kok': 'Boston',
        'HK timezone': 'US timezone',
        'HKT': 'EST/PST',
        '9am-6pm HKT': '9am-6pm EST/PST',
    }
    
    for hk_location, us_location in hong_kong_locations_to_us.items():
        content = content.replace(hk_location, us_location)
    
    # 10. 法规: 添加美国法规
    content = content.replace('PDPO', 'IRS')
    content = content.replace('GDPR', 'SOC2')
    
    # 添加IRS compliance提及（如果不存在）
    if 'IRS compliant' not in content and 'accounting' in content.lower():
        # 在第一次提到"compliant"或"secure"的地方添加
        content = re.sub(
            r'(\bsecure\b)',
            r'IRS compliant, SOC2 certified, \1',
            content,
            count=1,
            flags=re.IGNORECASE
        )
    
    # 11. 货币符号已经是USD，无需修改
    
    # 12. 劳动成本: $50/hr → $60/hr (美国市场)
    content = content.replace('$50/hr', '$60/hr')
    content = content.replace('$50/hour', '$60/hour')
    
    # 13. 案例研究本地化
    content = content.replace('Seoul accounting firm', 'New York CPA firm')
    content = content.replace('Tokyo restaurant', 'Los Angeles restaurant')
    content = content.replace('Osaka', 'Chicago')
    content = content.replace('Busan', 'San Francisco')
    content = content.replace('Seoul', 'New York')
    content = content.replace('Tokyo', 'Los Angeles')
    
    # 14. Open Graph locale
    if 'og:locale' not in content:
        content = re.sub(
            r'(<meta property="og:image".*?>)',
            r'\1\n    <meta property="og:locale" content="en_US">',
            content
        )
    
    # 15. Schema标记 - 添加inLanguage
    if '"dateModified"' in content and '"inLanguage"' not in content:
        content = content.replace(
            '"dateModified": "2025-12-28"',
            '"dateModified": "2025-12-28",\n        "inLanguage": "en-US"'
        )
    
    # 16. Footer更新
    content = re.sub(
        r'AI-powered document processing platform\. 90% cheaper than.*?98% accuracy\.',
        'AI-powered document processing platform for US businesses. 90% cheaper than competitors, 200x faster, specialized for US banks (Chase, Bank of America, Wells Fargo, Citibank). 3-second processing, 98% accuracy. IRS compliant, SOC2 certified.',
        content
    )
    
    # 17. 标题中添加"US"或"American"（如果合适）
    def update_h1(m):
        title = m.group(1)
        if 'US' not in title and 'American' not in title and '?' in title:
            return f'<h1>{title} for US Businesses?</h1>'
        return m.group(0)
    
    content = re.sub(
        r'<h1>(.*?)\?</h1>',
        update_h1,
        content
    )
    
    # 18. 添加"accountant" → "CPA" (Certified Public Accountant)
    content = re.sub(
        r'\baccountant\b',
        'CPA',
        content,
        count=5  # 只替换前5次
    )
    content = re.sub(
        r'\baccountants\b',
        'CPAs',
        content,
        count=5  # 只替换前5次
    )
    
    # 19. 添加US GAAP提及
    if 'GAAP' not in content:
        content = re.sub(
            r'(IRS compliant)',
            r'\1, US GAAP format',
            content,
            count=2
        )
    
    # 20. 更新相关文章链接（保持不变，已在步骤2中处理）
    # content已经在步骤2中更新了所有相关链接
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    en_us_blog_dir = os.path.join(base_dir, 'en-us', 'blog')
    
    # 确保目标目录存在
    os.makedirs(en_us_blog_dir, exist_ok=True)
    
    # 要处理的文件列表（跳过第一篇，已手动创建）
    files_to_process = [
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
    
    print("=" * 70)
    print("🇺🇸 批量创建美国版SEO文章")
    print("=" * 70)
    print(f"📂 源目录: {en_blog_dir}")
    print(f"📂 目标目录: {en_us_blog_dir}")
    print(f"📝 待处理文章: {len(files_to_process)}")
    print("=" * 70)
    
    success_count = 0
    error_count = 0
    
    for filename in files_to_process:
        try:
            source_file = os.path.join(en_blog_dir, filename)
            target_file = os.path.join(en_us_blog_dir, filename)
            
            # 检查源文件是否存在
            if not os.path.exists(source_file):
                print(f"⚠️  {filename} - 源文件不存在，跳过")
                error_count += 1
                continue
            
            # 读取源文件
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 本地化内容
            localized_content = localize_to_us(content, filename)
            
            # 写入目标文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(localized_content)
            
            print(f"✅ {filename} - 创建成功")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {filename} - 错误: {str(e)}")
            error_count += 1
    
    print("=" * 70)
    print("📊 处理完成统计")
    print("=" * 70)
    print(f"✅ 成功: {success_count}/{len(files_to_process)}")
    print(f"❌ 失败: {error_count}/{len(files_to_process)}")
    print("=" * 70)
    
    if success_count > 0:
        print("\n🎉 美国版SEO文章创建完成！")
        print("\n📝 关键本地化修改:")
        print("   ✅ HTML lang: en → en-US")
        print("   ✅ 添加hreflang标签 (en-us, en-gb, en, x-default)")
        print("   ✅ 银行: HSBC/Hang Seng → Chase/Bank of America/Wells Fargo")
        print("   ✅ 地点: Central/Hong Kong → New York/United States")
        print("   ✅ 法规: PDPO/GDPR → IRS/SOC2")
        print("   ✅ 支付: FPS/PayMe → ACH/Zelle/Venmo")
        print("   ✅ 劳动成本: $50/hr → $60/hr")
        print("   ✅ 案例: 香港案例 → 美国案例")
        print("   ✅ 添加: IRS compliant, SOC2 certified, US GAAP")
        print("   ✅ 术语: accountant → CPA (Certified Public Accountant)")
    
    if error_count > 0:
        print(f"\n⚠️  {error_count} 个文件处理失败，请检查错误信息")
    
    return success_count, error_count

if __name__ == "__main__":
    success, errors = main()
    exit(0 if errors == 0 else 1)

