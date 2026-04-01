#!/usr/bin/env python3
"""
更新最终sitemap.xml
作用: 添加新创建的中文行业页面
"""

from datetime import datetime
from pathlib import Path

def create_sitemap():
    """创建完整的sitemap.xml"""
    
    base_url = "https://vaultcaddy.com"
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = []
    
    # 首页
    urls.append({
        'loc': f'{base_url}/',
        'priority': '1.0',
        'changefreq': 'daily'
    })
    
    # 中文银行页面
    zh_banks = ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm', 'fubon', 'ocbc']
    for bank in zh_banks:
        urls.append({
            'loc': f'{base_url}/{bank}-bank-statement.html',
            'priority': '0.9',
            'changefreq': 'weekly'
        })
    
    # 中文行业页面 (新增)
    zh_industries = ['restaurant', 'accountant', 'retail']
    for industry in zh_industries:
        urls.append({
            'loc': f'{base_url}/solutions/{industry}/',
            'priority': '0.9',
            'changefreq': 'weekly'
        })
    
    # 英文银行页面
    en_banks = ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']
    for bank in en_banks:
        urls.append({
            'loc': f'{base_url}/en/{bank}-bank-statement.html',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 日文银行页面
    ja_banks = ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']
    for bank in ja_banks:
        urls.append({
            'loc': f'{base_url}/ja/{bank}-bank-statement.html',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 日文行业页面
    ja_industries = ['restaurant', 'accountant', 'retail', 'ecommerce', 'trading']
    for industry in ja_industries:
        urls.append({
            'loc': f'{base_url}/ja/solutions/{industry}/',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 韩文银行页面
    ko_banks = ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']
    for bank in ko_banks:
        urls.append({
            'loc': f'{base_url}/ko/{bank}-bank-statement.html',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 韩文行业页面
    ko_industries = ['restaurant', 'accountant', 'retail', 'ecommerce', 'trading']
    for industry in ko_industries:
        urls.append({
            'loc': f'{base_url}/ko/solutions/{industry}/',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 生成sitemap XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{today}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    return xml_content, len(urls)

def main():
    """主函数"""
    
    print("=" * 80)
    print("🗺️  更新最終Sitemap.xml")
    print("=" * 80)
    print()
    
    xml_content, url_count = create_sitemap()
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ sitemap.xml 已更新!")
    print()
    print(f"📊 統計:")
    print(f"  - 總URL數: {url_count}")
    print(f"  - 中文頁面: 15 (12銀行 + 3行業)")
    print(f"  - 英文頁面: 10 (10銀行)")
    print(f"  - 日文頁面: 15 (10銀行 + 5行業)")
    print(f"  - 韓文頁面: 15 (10銀行 + 5行業)")
    print(f"  - 首頁: 1")
    print()
    print("📍 下一步:")
    print("  1. 上傳 sitemap.xml 到網站根目錄")
    print("  2. 提交到 Google Search Console")
    print("  3. 驗證所有URL可訪問")

if __name__ == '__main__':
    main()

