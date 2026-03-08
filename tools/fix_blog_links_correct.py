#!/usr/bin/env python3
"""
正确修复blog链接 - 应该链接到各自语言版本的blog
中文版：blog/
英文版：blog/ (相对路径，会找到 en/blog/)
日文版：blog/ (相对路径，会找到 jp/blog/)
韩文版：blog/ (相对路径，会找到 kr/blog/)
"""

files_to_fix = ['jp/index.html', 'kr/index.html']

for filepath in files_to_fix:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换 resources.html 为 blog/
        new_content = content.replace('href="resources.html"', 'href="blog/"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {filepath} - blog链接已修复")
        
    except Exception as e:
        print(f"❌ {filepath} - {str(e)}")

print("\n✅ 所有语言版本的blog链接已正确设置")

