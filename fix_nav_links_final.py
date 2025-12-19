#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有英文版页面的导航链接
"""

import os

def fix_main_pages_learning_center():
    """修复主要页面的 Learning Center 链接"""
    
    pages = [
        '/Users/cavlinyeung/ai-bank-parser/en/index.html',
        '/Users/cavlinyeung/ai-bank-parser/en/dashboard.html',
        '/Users/cavlinyeung/ai-bank-parser/en/account.html',
        '/Users/cavlinyeung/ai-bank-parser/en/billing.html',
        '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html',
        '/Users/cavlinyeung/ai-bank-parser/en/document-detail.html'
    ]
    
    for file_path in pages:
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复所有 Learning Center 链接
        # 1. href="/blog/" → href="blog/"
        content = content.replace('href="/blog/"', 'href="blog/"')
        
        # 2. href="../blog/" → href="blog/" (for en/ subdir files)
        content = content.replace('href="../blog/"', 'href="blog/"')
        
        # 3. href="learning-center.html" → href="blog/"
        content = content.replace('href="learning-center.html"', 'href="blog/"')
        
        # 4. href="../learning-center.html" → href="blog/"
        content = content.replace('href="../learning-center.html"', 'href="blog/"')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复 {os.path.basename(file_path)} 的 Learning Center 链接")
        else:
            print(f"ℹ️  {os.path.basename(file_path)} 无需修改")

def fix_blog_navigation():
    """修复 blog/index.html 的所有导航链接"""
    
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/blog/index.html'
    
    if not os.path.exists(file_path):
        print(f"⚠️  文件不存在: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复所有导航链接
    # 1. Dashboard: ../en/dashboard.html → ../dashboard.html
    content = content.replace('href="../en/dashboard.html"', 'href="../dashboard.html"')
    
    # 2. Home: ../en/index.html → ../index.html
    content = content.replace('href="../en/index.html"', 'href="../index.html"')
    
    # 3. Features: ../en/index.html#features → ../index.html#features
    content = content.replace('href="../en/index.html#features"', 'href="../index.html#features"')
    
    # 4. Pricing: ../en/index.html#pricing → ../index.html#pricing
    content = content.replace('href="../en/index.html#pricing"', 'href="../index.html#pricing"')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修复 blog/index.html 的所有导航链接")

def verify_fixes():
    """验证修复结果"""
    print()
    print("=" * 50)
    print("验证修复结果...")
    print()
    
    # 检查主要页面
    print("1. 检查主要页面的 Learning Center 链接:")
    pages = [
        '/Users/cavlinyeung/ai-bank-parser/en/index.html',
        '/Users/cavlinyeung/ai-bank-parser/en/dashboard.html',
    ]
    
    for file_path in pages:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'href="blog/"' in content and 'Learning Center' in content:
                print(f"   ✅ {os.path.basename(file_path)}: Learning Center → blog/")
            else:
                print(f"   ⚠️  {os.path.basename(file_path)}: 可能需要手动检查")
    
    # 检查博客页面
    print()
    print("2. 检查 blog/index.html 的导航链接:")
    blog_file = '/Users/cavlinyeung/ai-bank-parser/en/blog/index.html'
    
    if os.path.exists(blog_file):
        with open(blog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ('Dashboard', 'href="../dashboard.html"'),
            ('Home', 'href="../index.html"'),
            ('Features', 'href="../index.html#features"'),
            ('Pricing', 'href="../index.html#pricing"')
        ]
        
        for label, link in checks:
            if link in content:
                print(f"   ✅ {label}: {link}")
            else:
                print(f"   ⚠️  {label}: 可能需要手动检查")

if __name__ == '__main__':
    print("🔧 开始修复英文版页面的导航链接...")
    print()
    
    # 1. 修复主要页面的 Learning Center 链接
    print("=" * 50)
    print("步骤 1: 修复主要页面的 Learning Center 链接")
    print("=" * 50)
    fix_main_pages_learning_center()
    
    print()
    
    # 2. 修复 blog 页面的导航链接
    print("=" * 50)
    print("步骤 2: 修复 blog 页面的导航链接")
    print("=" * 50)
    fix_blog_navigation()
    
    # 3. 验证修复
    verify_fixes()
    
    print()
    print("=" * 50)
    print("✅ 所有导航链接修复完成！")
    print()
    print("修复总结:")
    print()
    print("📄 主要页面 (6个):")
    print("   • en/index.html")
    print("   • en/dashboard.html")
    print("   • en/account.html")
    print("   • en/billing.html")
    print("   • en/firstproject.html")
    print("   • en/document-detail.html")
    print("   🔗 Learning Center → blog/")
    print()
    print("📝 博客页面:")
    print("   • en/blog/index.html")
    print("   🔗 Dashboard → ../dashboard.html")
    print("   🔗 Home → ../index.html")
    print("   🔗 Features → ../index.html#features")
    print("   🔗 Pricing → ../index.html#pricing")

