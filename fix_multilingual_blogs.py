#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复多语言博客页面
1. 修复图片显示问题
2. 更新免费页数：10页 → 20页
3. 地区本地化：日文版（香港→日本），韩文版（香港→韩国），英文版（香港→美国）
"""

import re
import os

# 为每篇文章配置合适的Unsplash图片
ARTICLE_IMAGES = {
    'manual-vs-ai-cost-analysis': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop',
    'personal-bookkeeping-best-practices': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=400&fit=crop',
    'complete-ai-invoice-processing': 'https://images.unsplash.com/photo-1554224154-26032ffc0d07?w=800&h=400&fit=crop',
    'ai-invoice-processing-small-business': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=800&h=400&fit=crop',
    'accounting-firm-automation': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=400&fit=crop',
    'accounting-workflow-optimization': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop',
    'automate-financial-documents': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop',
    'best-pdf-to-excel-converter': 'https://images.unsplash.com/photo-1589652717521-10c0d092dea9?w=800&h=400&fit=crop',
    'client-document-management': 'https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=400&fit=crop',
    'freelancer-invoice-management': 'https://images.unsplash.com/photo-1556742521-9713bf272865?w=800&h=400&fit=crop',
    'freelancer-tax-preparation': 'https://images.unsplash.com/photo-1554224154-22dec7ec8818?w=800&h=400&fit=crop',
    'how-to-convert-pdf-bank-statement': 'https://images.unsplash.com/photo-1554224311-beee1c7c4818?w=800&h=400&fit=crop',
    'ocr-accuracy-for-accounting': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop',
    'ocr-technology-for-accountants': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&h=400&fit=crop',
    'quickbooks-integration-guide': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800&h=400&fit=crop',
    'small-business-document-management': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=400&fit=crop',
}

def fix_blog_index(file_path, language, region_replacements):
    """修复博客索引页面"""
    
    print(f"\n🔧 修复 {language} 版博客索引页面...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 修复图片URL - 将source.unsplash.com替换为images.unsplash.com
    if 'source.unsplash.com' in content:
        # 为每篇文章配置特定图片
        for article_slug, image_url in ARTICLE_IMAGES.items():
            # 查找对应的博客卡片
            pattern = f'href="{article_slug}.html".*?<img src="[^"]*"'
            matches = list(re.finditer(pattern, content, re.DOTALL))
            if matches:
                for match in matches:
                    old_img_tag = re.search(r'<img src="[^"]*"', match.group()).group()
                    new_img_tag = f'<img src="{image_url}"'
                    content = content.replace(old_img_tag, new_img_tag, 1)
                changes.append(f"✅ 修复文章图片: {article_slug}")
    
    # 2. 地区本地化替换
    for old_text, new_text in region_replacements.items():
        if old_text in content:
            count = content.count(old_text)
            content = content.replace(old_text, new_text)
            changes.append(f"✅ 地区本地化: {old_text} → {new_text} ({count}处)")
    
    # 3. 更新免费页数：10页 → 20页
    free_page_patterns = [
        ('10 page', '20 page'),
        ('10頁', '20頁'),
        ('10ページ', '20ページ'),
        ('10페이지', '20페이지'),
        ('免費試用 10 頁', '免費試用 20 頁'),
        ('免费试用 10 页', '免费试用 20 页'),
        ('10 pages free', '20 pages free'),
        ('Try 10 Pages', 'Try 20 Pages'),
        ('10 Pages Free', '20 Pages Free'),
    ]
    
    for old_text, new_text in free_page_patterns:
        if old_text in content:
            count = content.count(old_text)
            content = content.replace(old_text, new_text)
            changes.append(f"✅ 更新免费页数: {old_text} → {new_text} ({count}处)")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if changes:
        for change in changes:
            print(f"   {change}")
    else:
        print("   ℹ️  无需更改")
    
    print(f"✅ {language} 版博客索引页面修复完成")
    
    return len(changes)

def fix_blog_articles(blog_dir, language, region_replacements):
    """修复博客文章"""
    
    print(f"\n🔧 修复 {language} 版博客文章...")
    
    total_changes = 0
    
    # 遍历所有HTML文章
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html') and filename != 'index.html':
            file_path = os.path.join(blog_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 地区本地化替换
            for old_text, new_text in region_replacements.items():
                content = content.replace(old_text, new_text)
            
            # 2. 更新免费页数
            free_page_patterns = [
                ('10 page', '20 page'),
                ('10頁', '20頁'),
                ('10ページ', '20ページ'),
                ('10페이지', '20페이지'),
                ('免費試用 10 頁', '免費試用 20 頁'),
                ('免费试用 10 页', '免费试用 20 页'),
                ('10 pages free', '20 pages free'),
                ('Try 10 Pages', 'Try 20 Pages'),
                ('10 Pages Free', '20 Pages Free'),
            ]
            
            for old_text, new_text in free_page_patterns:
                content = content.replace(old_text, new_text)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ 修复文章: {filename}")
                total_changes += 1
    
    print(f"✅ {language} 版博客文章修复完成 (修改了 {total_changes} 篇文章)")
    
    return total_changes

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              修复多语言博客页面工具                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    total_changes = 0
    
    # 英文版：香港 → 美国
    print("\n" + "="*70)
    print("📝 英文版 (en)")
    print("="*70)
    en_replacements = {
        'Hong Kong': 'United States',
        'HKD': 'USD',
        'HK$': '$',
        '香港': 'United States',
    }
    total_changes += fix_blog_index('en/blog/index.html', '英文', en_replacements)
    total_changes += fix_blog_articles('en/blog', '英文', en_replacements)
    
    # 日文版：香港 → 日本
    print("\n" + "="*70)
    print("📝 日文版 (jp)")
    print("="*70)
    jp_replacements = {
        '香港': '日本',
        'Hong Kong': '日本',
        'HKD': 'JPY',
        'HK$': '¥',
    }
    total_changes += fix_blog_index('jp/blog/index.html', '日文', jp_replacements)
    total_changes += fix_blog_articles('jp/blog', '日文', jp_replacements)
    
    # 韩文版：香港 → 韩国
    print("\n" + "="*70)
    print("📝 韩文版 (kr)")
    print("="*70)
    kr_replacements = {
        '香港': '한국',
        'Hong Kong': '한국',
        'HKD': 'KRW',
        'HK$': '₩',
    }
    total_changes += fix_blog_index('kr/blog/index.html', '韩文', kr_replacements)
    total_changes += fix_blog_articles('kr/blog', '韩文', kr_replacements)
    
    # 总结
    print("\n" + "="*70)
    print("🎉 修复完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   总修复项: {total_changes} 处")
    print(f"\n🌐 请访问以下页面验证效果：")
    print(f"   - https://vaultcaddy.com/en/blog/")
    print(f"   - https://vaultcaddy.com/jp/blog/")
    print(f"   - https://vaultcaddy.com/kr/blog/")

if __name__ == '__main__':
    main()

