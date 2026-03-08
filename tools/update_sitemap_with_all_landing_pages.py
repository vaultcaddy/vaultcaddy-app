#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新sitemap.xml，添加所有新的Landing Pages
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# 读取现有sitemap
tree = ET.parse('sitemap.xml')
root = tree.getroot()

# 命名空间
ns = {'': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

# 所有新的Landing Pages
NEW_PAGES = [
    'restaurant', 'retail-store', 'consultant', 'designer', 'developer',
    'marketing-agency', 'photographer', 'property-manager', 'startup',
    'contractor', 'fitness-coach', 'healthcare', 'real-estate',
    'beauty-salon', 'cleaning-service', 'travel-agent', 'artist',
    'coworking-space', 'delivery-driver', 'event-planner', 'musician',
    'nonprofit', 'personal-finance', 'pet-service'
]

# 获取现有的URLs
existing_urls = set()
for url_elem in root.findall('.//url', ns):
    loc = url_elem.find('loc', ns)
    if loc is not None:
        existing_urls.add(loc.text)

# 当前日期
today = datetime.now().strftime('%Y-%m-%d')

# 添加新的Landing Pages
added_count = 0
for page in NEW_PAGES:
    url = f'https://vaultcaddy.com/solutions/{page}/'
    
    if url not in existing_urls:
        # 创建新的URL元素
        url_elem = ET.SubElement(root, 'url')
        ET.SubElement(url_elem, 'loc').text = url
        ET.SubElement(url_elem, 'lastmod').text = today
        ET.SubElement(url_elem, 'changefreq').text = 'weekly'
        ET.SubElement(url_elem, 'priority').text = '0.8'
        added_count += 1
        print(f"✅ 添加: {url}")

# 保存更新后的sitemap
tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)

print(f"\n{'='*70}")
print(f"🎉 Sitemap更新完成！")
print(f"   共添加 {added_count} 個新URL")
print(f"   總URL數: {len(root.findall('.//url', ns))}")
print(f"{'='*70}")

if __name__ == '__main__':
    pass

