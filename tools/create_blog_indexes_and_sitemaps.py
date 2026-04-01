#!/usr/bin/env python3
"""创建4个地区的博客索引页面和sitemap文件"""
import os
from datetime import datetime

# 地区配置
REGIONS = {
    'en-us': {'name': 'United States', 'currency': '$', 'lang': 'en-US', 'locale': 'en_US', 'flag': '🇺🇸'},
    'en-gb': {'name': 'United Kingdom', 'currency': '£', 'lang': 'en-GB', 'locale': 'en_GB', 'flag': '🇬🇧'},
    'en-ca': {'name': 'Canada', 'currency': 'CAD $', 'lang': 'en-CA', 'locale': 'en_CA', 'flag': '🇨🇦'},
    'en-au': {'name': 'Australia', 'currency': 'AUD $', 'lang': 'en-AU', 'locale': 'en_AU', 'flag': '🇦🇺'},
}

# 文章列表（所有地区相同）
ARTICLES = [
    {'file': 'vaultcaddy-vs-dext-comparison-2025.html', 'title': 'VaultCaddy vs Dext: Complete Comparison', 'date': '2025-12-28'},
    {'file': 'how-to-convert-bank-statements-to-excel-2025.html', 'title': 'How to Convert Bank Statements to Excel', 'date': '2025-12-28'},
    {'file': 'top-10-accounting-software-2025.html', 'title': 'Top 10 Accounting Software', 'date': '2025-12-28'},
    {'file': 'vaultcaddy-vs-expensify-comparison-2025.html', 'title': 'VaultCaddy vs Expensify Comparison', 'date': '2025-12-28'},
    {'file': 'pdf-bank-statement-cannot-copy-text-solutions-2025.html', 'title': 'PDF Bank Statement Cannot Copy Text - Solutions', 'date': '2025-12-28'},
    {'file': 'quickbooks-import-bank-statement-error-fix-2025.html', 'title': 'QuickBooks Import Bank Statement Error Fix', 'date': '2025-12-28'},
    {'file': 'vaultcaddy-vs-quickbooks-comparison-2025.html', 'title': 'VaultCaddy vs QuickBooks Comparison', 'date': '2025-12-28'},
    {'file': 'restaurant-accounting-system-guide-2025.html', 'title': 'Restaurant Accounting System Guide', 'date': '2025-12-28'},
    {'file': 'manual-data-entry-vs-ai-automation-2025.html', 'title': 'Manual Data Entry vs AI Automation', 'date': '2025-12-28'},
    {'file': 'bank-statement-ocr-guide-2025.html', 'title': 'Bank Statement OCR Guide', 'date': '2025-12-28'},
]

def create_blog_index(region_code, region_info):
    """创建博客索引页面"""
    html = f'''<!DOCTYPE html>
<html lang="{region_info['lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaultCaddy Blog ({region_info['name']}) - Bank Statement & Accounting Tips</title>
    <meta name="description" content="Expert tips on bank statement processing, accounting automation, and AI-powered document management for {region_info['name']} businesses.">
    <meta name="keywords" content="accounting blog, bank statement tips, AI automation, accounting software, {region_info['name']}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="VaultCaddy Blog ({region_info['name']})">
    <meta property="og:description" content="Expert accounting and bank statement processing tips">
    <meta property="og:url" content="https://vaultcaddy.com/{region_code}/blog/">
    <meta property="og:locale" content="{region_info['locale']}">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a202c; background: #f7fafc; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; text-align: center; }}
        header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        header p {{ font-size: 1.2rem; opacity: 0.9; }}
        .region-flag {{ font-size: 3rem; margin-bottom: 1rem; }}
        .articles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2rem; margin-top: 3rem; }}
        .article-card {{ background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s, box-shadow 0.2s; }}
        .article-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 12px rgba(0,0,0,0.15); }}
        .article-card h2 {{ font-size: 1.5rem; margin-bottom: 0.75rem; color: #2d3748; }}
        .article-card .date {{ color: #718096; font-size: 0.9rem; margin-bottom: 1rem; }}
        .article-card a {{ display: inline-block; margin-top: 1rem; color: #667eea; font-weight: 600; text-decoration: none; }}
        .article-card a:hover {{ color: #764ba2; }}
        .back-home {{ display: inline-block; margin: 2rem 0; padding: 0.75rem 1.5rem; background: #667eea; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; }}
        .back-home:hover {{ background: #764ba2; }}
        @media (max-width: 768px) {{
            header h1 {{ font-size: 2rem; }}
            .articles-grid {{ grid-template-columns: 1fr; gap: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="region-flag">{region_info['flag']}</div>
        <h1>VaultCaddy Blog</h1>
        <p>Expert Accounting & Bank Statement Tips for {region_info['name']}</p>
    </header>
    
    <div class="container">
        <a href="../../index.html" class="back-home">← Back to Home</a>
        
        <div class="articles-grid">
'''
    
    for article in ARTICLES:
        html += f'''            <article class="article-card">
                <div class="date">{article['date']}</div>
                <h2>{article['title']}</h2>
                <a href="{article['file']}">Read Article →</a>
            </article>
'''
    
    html += '''        </div>
    </div>
</body>
</html>'''
    
    return html

def create_sitemap(region_code):
    """创建sitemap.xml"""
    base_url = f"https://vaultcaddy.com/{region_code}/blog"
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # 添加博客索引页
    xml += f'''    <url>
        <loc>{base_url}/</loc>
        <lastmod>2025-12-28</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    # 添加所有文章
    for article in ARTICLES:
        xml += f'''    <url>
        <loc>{base_url}/{article['file']}</loc>
        <lastmod>{article['date']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
'''
    
    xml += '''</urlset>'''
    return xml

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("=" * 70)
    print("🚀 创建博客索引页面和Sitemap文件")
    print("=" * 70)
    
    for region_code, region_info in REGIONS.items():
        print(f"\n{region_info['flag']} 处理 {region_info['name']} ({region_code})")
        
        # 创建博客索引
        blog_dir = os.path.join(base_dir, region_code, 'blog')
        os.makedirs(blog_dir, exist_ok=True)
        
        index_html = create_blog_index(region_code, region_info)
        index_path = os.path.join(blog_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"  ✅ 博客索引: /{region_code}/blog/index.html")
        
        # 创建sitemap
        sitemap_xml = create_sitemap(region_code)
        sitemap_path = os.path.join(base_dir, f'sitemap-{region_code}.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_xml)
        print(f"  ✅ Sitemap: /sitemap-{region_code}.xml")
    
    print("\n" + "=" * 70)
    print("✅ 全部完成！")
    print("=" * 70)
    print("\n📝 创建的文件:")
    print("   博客索引页面:")
    for region_code in REGIONS:
        print(f"      ✅ /{region_code}/blog/index.html")
    print("\n   Sitemap文件:")
    for region_code in REGIONS:
        print(f"      ✅ /sitemap-{region_code}.xml")
    
    print("\n🚀 下一步:")
    print("   1. 提交sitemap到Google Search Console")
    print("   2. 在robots.txt中添加sitemap链接")
    print("   3. 测试所有链接")

if __name__ == "__main__":
    main()

