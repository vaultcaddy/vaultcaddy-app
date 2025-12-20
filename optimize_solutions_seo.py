#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化Solutions Landing Pages的SEO
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def optimize_solution_page(file_path, language):
    """优化单个solution page的SEO"""
    
    filename = os.path.basename(file_path)
    print(f"🔍 {filename}...", end='')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        changes = 0
        
        # 1. 添加robots meta
        if not soup.find('meta', {'name': 'robots'}):
            robots_tag = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'index, follow'})
            if soup.head:
                soup.head.insert(0, robots_tag)
                changes += 1
        
        # 2. 优化图片alt
        for img in soup.find_all('img'):
            if not img.get('alt') or len(img.get('alt', '')) < 5:
                h1 = soup.find('h1')
                if h1:
                    img['alt'] = h1.get_text(strip=True)[:100]
                    changes += 1
        
        # 3. 添加internal links的title
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/') or 'vaultcaddy.com' in link['href']:
                if not link.get('title'):
                    link_text = link.get_text(strip=True)
                    if link_text:
                        link['title'] = link_text
                        changes += 1
        
        # 4. 确保有canonical URL
        if not soup.find('link', {'rel': 'canonical'}):
            # 从meta og:url获取
            og_url = soup.find('meta', {'property': 'og:url'})
            if og_url and og_url.get('content'):
                canonical_tag = soup.new_tag('link', attrs={'rel': 'canonical', 'href': og_url['content']})
                if soup.head:
                    soup.head.append(canonical_tag)
                    changes += 1
        
        # 写回文件
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            print(f" ✅ {changes}处")
        else:
            print(" ✓")
        
        return changes
        
    except Exception as e:
        print(f" ❌ 错误: {str(e)}")
        return 0

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              🚀 Solutions Landing Pages SEO优化                       ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    languages = ['en', 'jp', 'kr']
    total_changes = 0
    total_files = 0
    
    for lang in languages:
        print(f"\n{'='*70}")
        print(f"📝 处理 {lang.upper()} Solutions")
        print('='*70)
        
        solutions_dir = Path(f'{lang}/solutions')
        if not solutions_dir.exists():
            print(f"   ⚠️  目录不存在: {solutions_dir}")
            continue
        
        # 获取所有HTML文件（包括子目录）
        html_files = list(solutions_dir.rglob('*.html'))
        print(f"\n找到 {len(html_files)} 个Landing Pages")
        print()
        
        for html_file in sorted(html_files):
            changes = optimize_solution_page(str(html_file), lang)
            total_changes += changes
            total_files += 1
    
    # 总结
    print("\n" + "="*70)
    print("🎉 Solutions SEO优化完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   处理文件数: {total_files} 个")
    print(f"   总优化项: {total_changes} 处")
    print(f"\n✨ 优化内容：")
    print(f"   ✅ Robots Meta标签")
    print(f"   ✅ 图片Alt标签")
    print(f"   ✅ 内部链接Title")
    print(f"   ✅ Canonical URLs")

if __name__ == '__main__':
    main()

