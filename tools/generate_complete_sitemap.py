#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成完整的sitemap.xml"""

import glob
import os
from datetime import datetime

def get_all_landing_pages():
    """获取所有landing page"""
    pages = []
    
    # 1. 主页（4个版本）
    for path in ['index.html', 'en/index.html', 'ja/index.html', 'kr/index.html']:
        if os.path.exists(path):
            pages.append({
                'loc': 'https://vaultcaddy.com/' + path.replace('index.html', ''),
                'priority': '1.0',
                'changefreq': 'daily'
            })
    
    # 2. Resources页面（4个版本）
    for path in ['resources.html', 'en/resources.html', 'ja/resources.html', 'kr/resources.html']:
        if os.path.exists(path):
            url = 'https://vaultcaddy.com/' + path
            pages.append({
                'loc': url,
                'priority': '0.9',
                'changefreq': 'weekly'
            })
    
    # 3. 银行页面
    # 中文版
    for file in glob.glob('*-bank-statement.html'):
        pages.append({
            'loc': f'https://vaultcaddy.com/{file}',
            'priority': '0.9',
            'changefreq': 'weekly'
        })
    
    # 英文版
    for file in glob.glob('en/*-bank-statement.html'):
        pages.append({
            'loc': f'https://vaultcaddy.com/{file}',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 日文版
    for file in glob.glob('ja/*-bank-statement.html'):
        pages.append({
            'loc': f'https://vaultcaddy.com/{file}',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 韩文版
    for file in glob.glob('kr/*-bank-statement.html'):
        pages.append({
            'loc': f'https://vaultcaddy.com/{file}',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 4. Solutions页面
    # 中文版
    for file in glob.glob('solutions/*/index.html'):
        dir_name = file.replace('solutions/', '').replace('/index.html', '')
        pages.append({
            'loc': f'https://vaultcaddy.com/solutions/{dir_name}/',
            'priority': '0.85',
            'changefreq': 'weekly'
        })
    
    # 英文版
    for file in glob.glob('en/solutions/*/index.html'):
        dir_name = file.replace('en/solutions/', '').replace('/index.html', '')
        pages.append({
            'loc': f'https://vaultcaddy.com/en/solutions/{dir_name}/',
            'priority': '0.75',
            'changefreq': 'weekly'
        })
    
    # 日文版
    for file in glob.glob('ja/solutions/*/index.html'):
        dir_name = file.replace('ja/solutions/', '').replace('/index.html', '')
        pages.append({
            'loc': f'https://vaultcaddy.com/ja/solutions/{dir_name}/',
            'priority': '0.75',
            'changefreq': 'weekly'
        })
    
    # 韩文版
    for file in glob.glob('kr/solutions/*/index.html'):
        dir_name = file.replace('kr/solutions/', '').replace('/index.html', '')
        pages.append({
            'loc': f'https://vaultcaddy.com/kr/solutions/{dir_name}/',
            'priority': '0.75',
            'changefreq': 'weekly'
        })
    
    # 5. Blog页面
    # 中文版
    for file in glob.glob('blog/*.html'):
        if 'index.html' not in file:
            pages.append({
                'loc': f'https://vaultcaddy.com/{file}',
                'priority': '0.7',
                'changefreq': 'monthly'
            })
    
    # Blog主页
    if os.path.exists('blog/index.html'):
        pages.append({
            'loc': 'https://vaultcaddy.com/blog/',
            'priority': '0.85',
            'changefreq': 'weekly'
        })
    
    # 英文版
    for file in glob.glob('en/blog/*.html'):
        if 'index.html' not in file:
            pages.append({
                'loc': f'https://vaultcaddy.com/{file}',
                'priority': '0.65',
                'changefreq': 'monthly'
            })
    
    if os.path.exists('en/blog/index.html'):
        pages.append({
            'loc': 'https://vaultcaddy.com/en/blog/',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 日文版
    for file in glob.glob('ja/blog/*.html'):
        if 'index.html' not in file:
            pages.append({
                'loc': f'https://vaultcaddy.com/{file}',
                'priority': '0.65',
                'changefreq': 'monthly'
            })
    
    if os.path.exists('ja/blog/index.html'):
        pages.append({
            'loc': 'https://vaultcaddy.com/ja/blog/',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # 韩文版
    for file in glob.glob('kr/blog/*.html'):
        if 'index.html' not in file:
            pages.append({
                'loc': f'https://vaultcaddy.com/{file}',
                'priority': '0.65',
                'changefreq': 'monthly'
            })
    
    if os.path.exists('kr/blog/index.html'):
        pages.append({
            'loc': 'https://vaultcaddy.com/kr/blog/',
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    return pages

def generate_sitemap(pages):
    """生成sitemap XML"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml

# 获取所有页面
pages = get_all_landing_pages()

# 按priority降序排序
pages.sort(key=lambda x: float(x['priority']), reverse=True)

# 生成sitemap
sitemap_xml = generate_sitemap(pages)

# 保存
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)

# 保存旧版本为备份
if os.path.exists('sitemap.xml.old'):
    os.remove('sitemap.xml.old')
os.system('cp sitemap.xml.backup sitemap.xml.old 2>/dev/null || true')

# 创建新备份
with open('sitemap.xml.backup', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)

print("=" * 70)
print("🎉 完整Sitemap生成成功！")
print("=" * 70)
print()
print(f"✅ 总计: {len(pages)} 个URL")
print()

# 统计
by_type = {}
by_lang = {'zh': 0, 'en': 0, 'ja': 0, 'kr': 0}

for page in pages:
    url = page['loc']
    
    # 统计语言
    if '/en/' in url:
        by_lang['en'] += 1
    elif '/ja/' in url:
        by_lang['ja'] += 1
    elif '/kr/' in url:
        by_lang['kr'] += 1
    else:
        by_lang['zh'] += 1
    
    # 统计类型
    if 'bank-statement' in url:
        by_type['银行页面'] = by_type.get('银行页面', 0) + 1
    elif 'solutions' in url:
        by_type['Solutions页面'] = by_type.get('Solutions页面', 0) + 1
    elif 'blog' in url:
        by_type['Blog页面'] = by_type.get('Blog页面', 0) + 1
    elif 'resources' in url:
        by_type['Resources页面'] = by_type.get('Resources页面', 0) + 1
    else:
        by_type['主页/其他'] = by_type.get('主页/其他', 0) + 1

print("📊 按类型统计:")
for type_name, count in by_type.items():
    print(f"  {type_name}: {count} 个")

print()
print("📊 按语言统计:")
print(f"  中文: {by_lang['zh']} 个")
print(f"  英文: {by_lang['en']} 个")
print(f"  日文: {by_lang['ja']} 个")
print(f"  韩文: {by_lang['kr']} 个")

print()
print("=" * 70)
print("📝 下一步:")
print("=" * 70)
print("1. 上传 sitemap.xml 到服务器")
print("2. 在 Google Search Console 提交新sitemap")
print("3. 在 robots.txt 中确保有: Sitemap: https://vaultcaddy.com/sitemap.xml")
print()

