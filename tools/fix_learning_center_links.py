#!/usr/bin/env python3
"""
修复所有4个版本的学习中心链接
从 blog/ 或 /blog/ 改为 resources.html
"""

import re

files_to_fix = {
    'jp/index.html': {
        'desktop': (r'href="blog/"', 'href="resources.html"'),
        'mobile': (r'href="blog/"', 'href="resources.html"')
    },
    'kr/index.html': {
        'desktop': (r'href="blog/"', 'href="resources.html"'),
        'mobile': (r'href="blog/"', 'href="resources.html"')
    }
}

for filepath, patterns in files_to_fix.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有 blog/ 为 resources.html
        new_content = content.replace('href="blog/"', 'href="resources.html"')
        new_content = new_content.replace('href="/blog/"', 'href="resources.html"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {filepath}")
        
    except Exception as e:
        print(f"❌ {filepath} - {str(e)}")

print("\n✅ 日文和韩文版学习中心链接已修复")

