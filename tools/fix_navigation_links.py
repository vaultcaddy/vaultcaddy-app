#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有英文版页面的导航链接
"""

import os
import re

def fix_navigation_links():
    """修复所有英文版页面的导航链接"""
    
    # 1. 修复主要页面的 Learning Center 链接
    main_pages = [
        '/Users/cavlinyeung/ai-bank-parser/en/index.html',
        '/Users/cavlinyeung/ai-bank-parser/en/dashboard.html',
        '/Users/cavlinyeung/ai-bank-parser/en/account.html',
        '/Users/cavlinyeung/ai-bank-parser/en/billing.html',
        '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html',
        '/Users/cavlinyeung/ai-bank-parser/en/document-detail.html'
    ]
    
    for file_path in main_pages:
        if not os.path.exists(file_path):
            print(f"⚠️ 文件不存在: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复 Learning Center 链接
        # 可能的格式：
        # href="learning-center.html"
        # href="../learning-center.html"
        # <a href="..." >Learning Center</a>
        
        # 方法1: 查找导航栏中的 Learning Center 链接
        # 通常是 <a href="XXX">Learning Center</a> 或 <a href="XXX" ...>Learning Center</a>
        content = re.sub(
            r'(<a[^>]*href=")[^"]*("(?:[^>]*>|\s+[^>]*>))(\s*)Learning Center',
            r'\1blog/\2\3Learning Center',
            content
        )
        
        # 方法2: 直接替换特定的 href 值（如果有固定的链接）
        content = content.replace('href="learning-center.html"', 'href="blog/"')
        content = content.replace('href="../learning-center.html"', 'href="blog/"')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {os.path.basename(file_path)} 的 Learning Center 链接")
    
    # 2. 修复 blog/index.html 中的导航链接
    blog_file = '/Users/cavlinyeung/ai-bank-parser/en/blog/index.html'
    
    if os.path.exists(blog_file):
        with open(blog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复 Dashboard 链接
        content = re.sub(
            r'(<a[^>]*href=")[^"]*("(?:[^>]*>|\s+[^>]*>))(\s*)Dashboard',
            r'\1../dashboard.html\2\3Dashboard',
            content
        )
        
        # 修复 Home/首頁 链接
        content = re.sub(
            r'(<a[^>]*href=")[^"]*("(?:[^>]*>|\s+[^>]*>))(\s*)(Home|首頁)',
            r'\1../index.html\2\3\4',
            content
        )
        
        # 修复 Pricing 链接
        content = re.sub(
            r'(<a[^>]*href=")[^"]*("(?:[^>]*>|\s+[^>]*>))(\s*)Pricing',
            r'\1../index.html#pricing\2\3Pricing',
            content
        )
        
        # 修复 Features 链接
        content = re.sub(
            r'(<a[^>]*href=")[^"]*("(?:[^>]*>|\s+[^>]*>))(\s*)Features',
            r'\1../index.html#features\2\3Features',
            content
        )
        
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 blog/index.html 的所有导航链接")
    else:
        print(f"⚠️ 文件不存在: {blog_file}")

if __name__ == '__main__':
    print("开始修复英文版页面的导航链接...")
    print()
    
    fix_navigation_links()
    
    print()
    print("=" * 50)
    print("✅ 导航链接修复完成！")
    print()
    print("修复内容：")
    print()
    print("1. 主要页面（6个）:")
    print("   - en/index.html")
    print("   - en/dashboard.html")
    print("   - en/account.html")
    print("   - en/billing.html")
    print("   - en/firstproject.html")
    print("   - en/document-detail.html")
    print("   修复：Learning Center → blog/")
    print()
    print("2. 博客页面:")
    print("   - en/blog/index.html")
    print("   修复：")
    print("   - Dashboard → ../dashboard.html")
    print("   - Home/首頁 → ../index.html")
    print("   - Pricing → ../index.html#pricing")
    print("   - Features → ../index.html#features")

