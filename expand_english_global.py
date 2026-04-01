#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英文版SEO全球扩展：从UK扩展到US、AU、CA、NZ
English Version Global Expansion: Expand from UK to US, AU, CA, NZ
"""

def expand_english_global():
    """扩展英文版到5个英语国家"""
    
    file_path = 'en/index.html'
    
    print("🌍 扩展英文版SEO到全球英语市场...")
    print("="*70)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    
    # 1. 更新hreflang标签 - 添加US, AU, CA, NZ
    print("\n1️⃣ 更新hreflang标签...")
    
    # 查找现有的en-GB hreflang
    if 'hreflang="en-GB"' in content and 'hreflang="en-US"' not in content:
        # 在en-GB后添加其他英语国家
        old_hreflang = '<link rel="alternate" hreflang="en-GB" href="https://vaultcaddy.com/en/index.html" />'
        new_hreflang = '''<link rel="alternate" hreflang="en-GB" href="https://vaultcaddy.com/en/index.html" />
    <link rel="alternate" hreflang="en-US" href="https://vaultcaddy.com/en/index.html" />
    <link rel="alternate" hreflang="en-AU" href="https://vaultcaddy.com/en/index.html" />
    <link rel="alternate" hreflang="en-CA" href="https://vaultcaddy.com/en/index.html" />
    <link rel="alternate" hreflang="en-NZ" href="https://vaultcaddy.com/en/index.html" />'''
        
        content = content.replace(old_hreflang, new_hreflang)
        changes_made.append("✅ hreflang标签已扩展到5个英语国家")
    else:
        changes_made.append("ℹ️  hreflang标签已存在或格式不同")
    
    # 2. 更新geo.region
    print("\n2️⃣ 更新地理定位标签...")
    
    if '<meta name="geo.region" content="GB"' in content:
        content = content.replace(
            '<meta name="geo.region" content="GB"',
            '<meta name="geo.region" content="GB;US;AU;CA;NZ"'
        )
        changes_made.append("✅ geo.region已扩展")
    elif 'geo.region' not in content:
        changes_made.append("ℹ️  geo.region标签不存在，Bing优化已添加")
    
    # 3. 更新description - 添加多国银行
    print("\n3️⃣ 更新meta description...")
    
    old_desc_patterns = [
        'UK (HSBC, Barclays, Lloyds, NatWest)',
        'Support for UK banks',
        'British banks',
    ]
    
    new_desc = 'Support for UK (HSBC, Barclays), US (Chase, Bank of America), AU, CA, NZ banks'
    
    for pattern in old_desc_patterns:
        if pattern in content:
            content = content.replace(pattern, new_desc)
            changes_made.append(f"✅ Description已更新支持多国银行")
            break
    
    # 4. 更新keywords
    print("\n4️⃣ 更新keywords...")
    
    if '<meta name="keywords"' in content and 'Bank of America' not in content:
        # 在关键词中添加美国银行
        content = content.replace(
            'Barclays, HSBC, Lloyds, NatWest',
            'HSBC, Barclays, Lloyds, NatWest, Chase, Bank of America, Wells Fargo'
        )
        changes_made.append("✅ Keywords已添加美国银行")
    
    # 5. 更新JSON-LD中的银行列表
    print("\n5️⃣ 更新JSON-LD结构化数据...")
    
    if '"bank_list":' in content:
        # 更新银行列表
        old_bank_list = '"bank_list": "Barclays, HSBC, Lloyds, NatWest"'
        new_bank_list = '"bank_list": "UK: HSBC, Barclays, Lloyds | US: Chase, Bank of America, Wells Fargo | AU: CommBank, Westpac, NAB"'
        
        if old_bank_list in content:
            content = content.replace(old_bank_list, new_bank_list)
            changes_made.append("✅ JSON-LD银行列表已全球化")
    
    # 6. 更新og:locale
    print("\n6️⃣ 更新Open Graph locale...")
    
    if '<meta property="og:locale" content="en_GB"' in content:
        # 添加其他地区的og:locale备选
        old_og_locale = '<meta property="og:locale" content="en_GB">'
        new_og_locale = '''<meta property="og:locale" content="en_GB">
    <meta property="og:locale:alternate" content="en_US">
    <meta property="og:locale:alternate" content="en_AU">'''
        
        content = content.replace(old_og_locale, new_og_locale)
        changes_made.append("✅ Open Graph locale已添加备选")
    
    # 保存文件
    print("\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 总结
    print("\n" + "="*70)
    print("🎉 英文版全球扩展完成！")
    print("="*70)
    
    for change in changes_made:
        print(f"  {change}")
    
    print("\n📊 现在支持的英语市场:")
    print("  🇬🇧 英国（UK）- HSBC, Barclays, Lloyds, NatWest")
    print("  🇺🇸 美国（US）- Chase, Bank of America, Wells Fargo")
    print("  🇦🇺 澳洲（AU）- CommBank, Westpac, NAB")
    print("  🇨🇦 加拿大（CA）- RBC, TD, Scotiabank")
    print("  🇳🇿 新西兰（NZ）- ANZ, ASB, BNZ")
    
    print("\n💡 建议后续行动:")
    print("  1. 在英文版添加美国银行示例（Chase, BofA）")
    print("  2. 创建澳洲/加拿大子页面（可选）")
    print("  3. 监控各国搜索流量变化")
    
    print("="*70)

if __name__ == '__main__':
    expand_english_global()

