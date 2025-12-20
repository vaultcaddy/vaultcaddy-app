#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的Sitemap - 包含所有144个优化的页面
"""

import os
from pathlib import Path
from datetime import datetime

def generate_sitemap():
    """生成完整的sitemap.xml"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
    
'''
    
    urls = []
    
    # 1. 主页（4个）
    print("📝 添加主页...")
    urls.append({
        'loc': 'https://vaultcaddy.com/',
        'priority': '1.0',
        'changefreq': 'weekly',
        'lastmod': today
    })
    urls.append({
        'loc': 'https://vaultcaddy.com/en/index.html',
        'priority': '0.9',
        'changefreq': 'weekly',
        'lastmod': today
    })
    urls.append({
        'loc': 'https://vaultcaddy.com/jp/index.html',
        'priority': '0.9',
        'changefreq': 'weekly',
        'lastmod': today
    })
    urls.append({
        'loc': 'https://vaultcaddy.com/kr/index.html',
        'priority': '0.9',
        'changefreq': 'weekly',
        'lastmod': today
    })
    
    # 2. 博客索引页（4个）
    print("📝 添加博客索引页...")
    for lang in ['', 'en/', 'jp/', 'kr/']:
        urls.append({
            'loc': f'https://vaultcaddy.com/{lang}blog/',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': today
        })
    
    # 3. 博客文章（48篇）
    print("📝 添加博客文章...")
    for lang in ['en', 'jp', 'kr']:
        blog_dir = Path(f'{lang}/blog')
        if blog_dir.exists():
            blog_files = [f for f in blog_dir.glob('*.html') if f.name != 'index.html']
            print(f"   - {lang.upper()}: {len(blog_files)}篇文章")
            
            for blog_file in sorted(blog_files):
                urls.append({
                    'loc': f'https://vaultcaddy.com/{lang}/blog/{blog_file.name}',
                    'priority': '0.7',
                    'changefreq': 'monthly',
                    'lastmod': today
                })
    
    # 4. Solutions索引页（3个）
    print("📝 添加Solutions索引页...")
    for lang in ['en', 'jp', 'kr']:
        urls.append({
            'loc': f'https://vaultcaddy.com/{lang}/solutions/',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': today
        })
    
    # 5. Landing Pages（93个）
    print("📝 添加Landing Pages...")
    for lang in ['en', 'jp', 'kr']:
        solutions_dir = Path(f'{lang}/solutions')
        if solutions_dir.exists():
            # 获取所有子目录
            subdirs = [d for d in solutions_dir.iterdir() if d.is_dir()]
            print(f"   - {lang.upper()}: {len(subdirs)}个Landing Pages")
            
            for subdir in sorted(subdirs):
                urls.append({
                    'loc': f'https://vaultcaddy.com/{lang}/solutions/{subdir.name}/',
                    'priority': '0.7',
                    'changefreq': 'monthly',
                    'lastmod': today
                })
    
    # 6. 其他重要页面
    print("📝 添加其他页面...")
    other_pages = [
        {'loc': 'https://vaultcaddy.com/auth.html', 'priority': '0.6'},
        {'loc': 'https://vaultcaddy.com/privacy.html', 'priority': '0.5'},
        {'loc': 'https://vaultcaddy.com/terms.html', 'priority': '0.5'},
    ]
    
    for page in other_pages:
        urls.append({
            'loc': page['loc'],
            'priority': page['priority'],
            'changefreq': 'monthly',
            'lastmod': today
        })
    
    # 生成XML
    print("\n🔨 生成Sitemap XML...")
    for url_data in urls:
        sitemap_content += f'''    <url>
        <loc>{url_data['loc']}</loc>
        <lastmod>{url_data['lastmod']}</lastmod>
        <changefreq>{url_data['changefreq']}</changefreq>
        <priority>{url_data['priority']}</priority>
    </url>
    
'''
    
    sitemap_content += '</urlset>\n'
    
    # 写入文件
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"\n✅ Sitemap生成完成！")
    print(f"   总URL数：{len(urls)}")
    print(f"   文件：sitemap.xml")
    
    return len(urls)

def generate_url_list():
    """生成URL列表用于Google Search Console提交"""
    
    print("\n📋 生成URL列表...")
    
    urls = []
    
    # 主页
    urls.extend([
        'https://vaultcaddy.com/',
        'https://vaultcaddy.com/en/index.html',
        'https://vaultcaddy.com/jp/index.html',
        'https://vaultcaddy.com/kr/index.html',
    ])
    
    # 博客索引
    urls.extend([
        'https://vaultcaddy.com/blog/',
        'https://vaultcaddy.com/en/blog/',
        'https://vaultcaddy.com/jp/blog/',
        'https://vaultcaddy.com/kr/blog/',
    ])
    
    # 博客文章
    for lang in ['en', 'jp', 'kr']:
        blog_dir = Path(f'{lang}/blog')
        if blog_dir.exists():
            for blog_file in sorted(blog_dir.glob('*.html')):
                if blog_file.name != 'index.html':
                    urls.append(f'https://vaultcaddy.com/{lang}/blog/{blog_file.name}')
    
    # Solutions索引
    for lang in ['en', 'jp', 'kr']:
        urls.append(f'https://vaultcaddy.com/{lang}/solutions/')
    
    # Landing Pages
    for lang in ['en', 'jp', 'kr']:
        solutions_dir = Path(f'{lang}/solutions')
        if solutions_dir.exists():
            for subdir in sorted(solutions_dir.iterdir()):
                if subdir.is_dir():
                    urls.append(f'https://vaultcaddy.com/{lang}/solutions/{subdir.name}/')
    
    # 写入文件
    with open('sitemap-urls.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')
    
    print(f"✅ URL列表生成完成！")
    print(f"   文件：sitemap-urls.txt")
    print(f"   总URL数：{len(urls)}")
    
    return len(urls)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              📋 生成完整Sitemap - 包含所有144个页面                    ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # 生成sitemap
    total_urls = generate_sitemap()
    
    # 生成URL列表
    total_list = generate_url_list()
    
    # 总结
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   Sitemap URL数：{total_urls}")
    print(f"   URL列表数：{total_list}")
    print(f"\n📁 生成的文件：")
    print(f"   ✅ sitemap.xml - 完整的sitemap")
    print(f"   ✅ sitemap-urls.txt - URL列表（用于批量提交）")
    print(f"\n🚀 下一步：")
    print(f"   1. 访问 https://search.google.com/search-console")
    print(f"   2. 在「索引」→「Sitemap」中提交：")
    print(f"      https://vaultcaddy.com/sitemap.xml")
    print(f"   3. 使用sitemap-urls.txt批量请求索引")

if __name__ == '__main__':
    main()

