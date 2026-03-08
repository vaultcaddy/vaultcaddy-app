#!/usr/bin/env python3
"""
生成Sitemap.xml
作用: 自动生成包含所有银行页面的sitemap
"""

import os
from datetime import datetime

# 银行页面列表
BANK_PAGES = [
    'hsbc-bank-statement.html',
    'hangseng-bank-statement.html',
    'bochk-bank-statement.html',
    'sc-bank-statement.html',
    'dbs-bank-statement.html',
    'bea-bank-statement.html',
    'citibank-bank-statement.html',
    'dahsing-bank-statement.html',
    'citic-bank-statement.html',
    'bankcomm-bank-statement.html'
]

# 主要页面
MAIN_PAGES = [
    {'loc': '', 'priority': '1.0', 'changefreq': 'daily'},
    {'loc': 'auth.html', 'priority': '0.9', 'changefreq': 'weekly'},
    {'loc': 'dashboard.html', 'priority': '0.8', 'changefreq': 'weekly'},
    {'loc': 'billing.html', 'priority': '0.7', 'changefreq': 'weekly'},
]

def generate_sitemap():
    """生成sitemap.xml"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    base_url = 'https://vaultcaddy.com'
    
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # 主要页面
    for page in MAIN_PAGES:
        loc = f"{base_url}/{page['loc']}" if page['loc'] else base_url
        xml_content += f'''    <url>
        <loc>{loc}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{page['changefreq']}</changefreq>
        <priority>{page['priority']}</priority>
    </url>
'''
    
    # 银行页面
    for bank_page in BANK_PAGES:
        xml_content += f'''    <url>
        <loc>{base_url}/{bank_page}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # 英文版本页面(如果存在)
    if os.path.exists('en/index.html'):
        xml_content += f'''    <url>
        <loc>{base_url}/en/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    
    # Solutions页面
    solutions = [
        'restaurant', 'accountant', 'retail-store', 'freelancer', 
        'ecommerce', 'small-business'
    ]
    
    for solution in solutions:
        solution_path = f'en/solutions/{solution}/index.html'
        if os.path.exists(solution_path):
            xml_content += f'''    <url>
        <loc>{base_url}/en/solutions/{solution}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
    
    xml_content += '</urlset>'
    
    return xml_content

def main():
    """主函数"""
    
    print("=" * 80)
    print("🗺️  生成 Sitemap.xml")
    print("=" * 80)
    print()
    
    xml_content = generate_sitemap()
    
    # 写入文件
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ sitemap.xml 已生成!")
    print()
    print("📊 统计:")
    print(f"  - 总URL数: {xml_content.count('<url>')}")
    print(f"  - 银行页面: {len([p for p in BANK_PAGES])}")
    print(f"  - 文件大小: {len(xml_content)} 字节")
    print()
    print("📋 下一步:")
    print("  1. 上傳 sitemap.xml 到網站根目錄")
    print("  2. 訪問 https://vaultcaddy.com/sitemap.xml 確認可訪問")
    print("  3. 登入 Google Search Console")
    print("  4. 選擇 vaultcaddy.com → Sitemap → 添加新的 Sitemap")
    print("  5. 輸入: https://vaultcaddy.com/sitemap.xml")
    print("  6. 點擊提交")

if __name__ == '__main__':
    main()

