#!/usr/bin/env python3
"""
更新sitemap.xml添加学习中心页面
作用：将4个新创建的resources.html学习中心页面添加到sitemap
"""

import xml.etree.ElementTree as ET
from datetime import date

def update_sitemap():
    """更新sitemap添加学习中心页面"""
    
    # 读取现有sitemap
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
    except FileNotFoundError:
        print("❌ sitemap.xml不存在")
        return False
    
    # 定义命名空间
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # 学习中心页面URLs
    resource_pages = [
        {
            'loc': 'https://vaultcaddy.com/resources.html',
            'priority': '0.9',
            'changefreq': 'weekly'
        },
        {
            'loc': 'https://vaultcaddy.com/en/resources.html',
            'priority': '0.9',
            'changefreq': 'weekly'
        },
        {
            'loc': 'https://vaultcaddy.com/jp/resources.html',
            'priority': '0.9',
            'changefreq': 'weekly'
        },
        {
            'loc': 'https://vaultcaddy.com/kr/resources.html',
            'priority': '0.9',
            'changefreq': 'weekly'
        }
    ]
    
    # 获取今天日期
    today = str(date.today())
    
    # 检查是否已存在
    existing_urls = set()
    for url_elem in root.findall('ns:url', ns):
        loc_elem = url_elem.find('ns:loc', ns)
        if loc_elem is not None:
            existing_urls.add(loc_elem.text)
    
    added_count = 0
    
    # 添加新页面
    for page in resource_pages:
        if page['loc'] in existing_urls:
            print(f"⏭️  已存在：{page['loc']}")
            continue
        
        # 创建新的URL元素
        url_elem = ET.SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        
        loc = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        loc.text = page['loc']
        
        lastmod = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        lastmod.text = today
        
        changefreq = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
        changefreq.text = page['changefreq']
        
        priority = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
        priority.text = page['priority']
        
        print(f"✅ 添加：{page['loc']}")
        added_count += 1
    
    # 保存sitemap
    tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    
    print()
    print("=" * 80)
    print(f"✅ Sitemap更新完成！添加了{added_count}个学习中心页面")
    print("=" * 80)
    print()
    print("📋 添加的页面：")
    for page in resource_pages:
        print(f"  - {page['loc']}")
    print()
    print("📊 统计：")
    print(f"  - 新增页面：{added_count}")
    print(f"  - 总URL数：{len(root.findall('ns:url', ns))}")
    print()
    print("🚀 下一步：")
    print("  1. 上传更新后的sitemap.xml到网站根目录")
    print("  2. 在Google Search Console重新提交sitemap")
    print("  3. 手动请求这4个页面的索引")
    print()
    
    return True

if __name__ == '__main__':
    update_sitemap()

