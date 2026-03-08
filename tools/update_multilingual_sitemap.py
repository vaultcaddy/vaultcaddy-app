#!/usr/bin/env python3
"""
更新多语言Sitemap
作用: 为中文、英文、日文、韩文生成完整的sitemap
"""

from datetime import datetime

def generate_multilingual_sitemap():
    """生成多语言sitemap"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    base_url = 'https://vaultcaddy.com'
    
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
    
    <!-- 首页 - 多语言版本 -->
    <url>
        <loc>https://vaultcaddy.com/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
        <xhtml:link rel="alternate" hreflang="zh-HK" href="https://vaultcaddy.com/" />
        <xhtml:link rel="alternate" hreflang="en" href="https://vaultcaddy.com/en/" />
        <xhtml:link rel="alternate" hreflang="ja" href="https://vaultcaddy.com/ja/" />
        <xhtml:link rel="alternate" hreflang="ko" href="https://vaultcaddy.com/ko/" />
    </url>
'''.format(today=today)
    
    # 中文版银行页面（12个）
    zh_banks = [
        'hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 
        'bea', 'citibank', 'dahsing', 'citic', 'bankcomm',
        'boc-hk', 'hang-seng'  # 旧版本（保留兼容）
    ]
    
    for bank in zh_banks:
        xml_content += f'''    <url>
        <loc>{base_url}/{bank}-bank-statement.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # 英文版银行页面（10个）
    en_banks = ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']
    for bank in en_banks:
        xml_content += f'''    <url>
        <loc>{base_url}/en/{bank}-bank-statement.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # 日文版银行页面（10个）
    for bank in en_banks:
        xml_content += f'''    <url>
        <loc>{base_url}/ja/{bank}-bank-statement.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # 韩文版银行页面（10个）
    for bank in en_banks:
        xml_content += f'''    <url>
        <loc>{base_url}/ko/{bank}-bank-statement.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # 英文Solutions页面（30个）
    en_solutions = [
        'restaurant', 'accountant', 'retail-store', 'freelancer', 'ecommerce', 
        'small-business', 'trading-company', 'logistics', 'clinic', 'education',
        'real-estate', 'hotel', 'beauty-salon', 'gym', 'cafe',
        'hair-salon', 'clothing-store', 'law-firm', 'dental-clinic', 'pharmacy',
        'bakery', 'bookstore', 'electronics-store', 'furniture-store', 'travel-agency',
        'insurance-agency', 'consulting', 'marketing-agency', 'it-services', 'construction'
    ]
    
    for solution in en_solutions:
        xml_content += f'''    <url>
        <loc>{base_url}/en/solutions/{solution}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
    
    # 日文Solutions页面（5个）
    ja_solutions = ['restaurant', 'accountant', 'retail', 'ecommerce', 'trading']
    for solution in ja_solutions:
        xml_content += f'''    <url>
        <loc>{base_url}/ja/solutions/{solution}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
    
    # 韩文Solutions页面（5个）
    for solution in ja_solutions:
        xml_content += f'''    <url>
        <loc>{base_url}/ko/solutions/{solution}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
    
    # 主要功能页面
    main_pages = ['auth', 'dashboard', 'billing', 'account']
    for page in main_pages:
        for lang in ['', 'en/', 'ja/', 'ko/']:
            xml_content += f'''    <url>
        <loc>{base_url}/{lang}{page}.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    xml_content += '</urlset>'
    
    return xml_content

def main():
    """主函数"""
    
    print("=" * 80)
    print("🗺️  生成多語言 Sitemap")
    print("=" * 80)
    print()
    
    xml_content = generate_multilingual_sitemap()
    
    # 写入文件
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    url_count = xml_content.count('<url>')
    
    print("✅ sitemap.xml 已生成!")
    print()
    print("📊 統計:")
    print(f"  - 總URL數: {url_count}")
    print(f"  - 中文銀行頁面: 12")
    print(f"  - 英文銀行頁面: 10")
    print(f"  - 日文銀行頁面: 10")
    print(f"  - 韓文銀行頁面: 10")
    print(f"  - 英文Solutions頁面: 30")
    print(f"  - 日文Solutions頁面: 5")
    print(f"  - 韓文Solutions頁面: 5")
    print(f"  - 主要功能頁面: 16")
    print(f"  - 文件大小: {len(xml_content):,} 字節")
    print()
    print("📋 下一步:")
    print("  1. 上傳 sitemap.xml 到網站根目錄")
    print("  2. 訪問 https://vaultcaddy.com/sitemap.xml 確認可訪問")
    print("  3. 登入 Google Search Console")
    print("  4. 提交 sitemap.xml")

if __name__ == '__main__':
    main()

