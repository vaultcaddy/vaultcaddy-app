#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复日文博客的四项改进：
1. 确保导航栏为日文
2. 在所有文章顶部添加高质量的特色图片
3. 将"最初の10書類は無料で処理できます"改为"最初の20書類は無料で処理できます"
4. 将所有"香港"改为"日本"
"""

import os
import re
from pathlib import Path

# 为不同类型文章配置合适的图片
ARTICLE_IMAGES = {
    'manual-vs-ai-cost-analysis': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop&q=80',
    'personal-bookkeeping-best-practices': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=1200&h=600&fit=crop&q=80',
    'ai-invoice-processing-guide': 'https://images.unsplash.com/photo-1554224154-26032ffc0d07?w=1200&h=600&fit=crop&q=80',
    'ai-invoice-processing-small-business': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1200&h=600&fit=crop&q=80',
    'accounting-firm-automation': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=600&fit=crop&q=80',
    'accounting-workflow-optimization': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop&q=80',
    'automate-financial-documents': 'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1200&h=600&fit=crop&q=80',
    'best-pdf-to-excel-converter': 'https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1200&h=600&fit=crop&q=80',
    'client-document-management': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=1200&h=600&fit=crop&q=80',
    'freelancer-invoice-management': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&h=600&fit=crop&q=80',
    'freelancer-tax-preparation': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=600&fit=crop&q=80',
    'how-to-convert-pdf-bank-statement': 'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1200&h=600&fit=crop&q=80',
    'ocr-accuracy-for-accounting': 'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1200&h=600&fit=crop&q=80',
    'ocr-technology-for-accountants': 'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1200&h=600&fit=crop&q=80',
    'quickbooks-integration-guide': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop&q=80',
    'small-business-document-management': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&h=600&fit=crop&q=80',
}

def fix_blog_article(file_path):
    """修复单个博客文章"""
    
    filename = os.path.basename(file_path)
    article_slug = filename.replace('.html', '')
    
    print(f"\n🔧 处理: {filename}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 更新图片 - 替换Unsplash动态链接为稳定链接
    if article_slug in ARTICLE_IMAGES:
        new_image_url = ARTICLE_IMAGES[article_slug]
        
        # 查找现有的图片标签
        old_image_pattern = r'<img src="https://source\.unsplash\.com/[^"]*"'
        if re.search(old_image_pattern, content):
            # 替换为新的图片URL
            content = re.sub(
                old_image_pattern,
                f'<img src="{new_image_url}"',
                content
            )
            changes.append("✅ 更新图片URL为稳定链接")
        else:
            # 如果没有图片，在文章内容开始处添加
            # 查找 <article class="blog-content"> 后面的第一个元素
            article_start = content.find('<article class="blog-content">')
            if article_start != -1:
                # 找到article标签结束的位置
                insert_pos = content.find('>', article_start) + 1
                
                # 插入图片HTML
                image_html = f'\n        <img src="{new_image_url}" \n             alt="{article_slug}" \n             style="width: 100%; border-radius: 12px; margin-bottom: 2rem;"\n             loading="lazy">\n        '
                
                content = content[:insert_pos] + image_html + content[insert_pos:]
                changes.append("✅ 添加特色图片")
    
    # 2. 更新免费文档数量：10 -> 20
    old_text = "最初の10書類は無料で処理できます"
    new_text = "最初の20書類は無料で処理できます"
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        changes.append(f"✅ 更新免费文档数：10 → 20")
    
    # 3. 将所有"香港"替换为"日本"
    hong_kong_replacements = [
        ('香港', '日本'),
        ('ホンコン', '日本'),
        ('HK$', '¥'),
        ('HKD', 'JPY'),
    ]
    
    for old, new in hong_kong_replacements:
        if old in content:
            content = content.replace(old, new)
            changes.append(f"✅ 地区本地化：{old} → {new}")
    
    # 4. 检查并确保导航栏相关内容为日文（检查页面内的任何中文导航文本）
    chinese_nav_patterns = [
        ('首頁', 'ホーム'),
        ('功能', '機能'),
        ('價格', '価格'),
        ('學習中心', '学習センター'),
        ('儀表板', 'ダッシュボード'),
        ('登入', 'ログイン'),
        ('帳戶', 'アカウント'),
        ('計費', '請求'),
        ('登出', 'ログアウト'),
    ]
    
    for chinese, japanese in chinese_nav_patterns:
        if chinese in content:
            content = content.replace(chinese, japanese)
            changes.append(f"✅ 导航文本：{chinese} → {japanese}")
    
    # 写回文件
    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        for change in changes:
            print(f"   {change}")
    else:
        print("   ℹ️  无需修改")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              日文博客改进（导航+图片+免费页数+地区本地化）            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    blog_dir = Path('jp/blog')
    
    if not blog_dir.exists():
        print(f"❌ 错误：找不到目录 {blog_dir}")
        return
    
    # 获取所有HTML文件（排除index.html）
    html_files = [f for f in blog_dir.glob('*.html') if f.name != 'index.html']
    
    print(f"\n📊 找到 {len(html_files)} 个博客文章文件")
    print("="*70)
    
    total_changes = 0
    
    for html_file in sorted(html_files):
        total_changes += fix_blog_article(str(html_file))
    
    # 总结
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   处理文章数: {len(html_files)} 篇")
    print(f"   总修改项: {total_changes} 处")
    print(f"\n✨ 完成的改进：")
    print(f"   ✅ 图片更新为高质量稳定链接")
    print(f"   ✅ 免费文档数量：10 → 20")
    print(f"   ✅ 地区本地化：香港 → 日本")
    print(f"   ✅ 导航栏文本检查并日文化")
    print(f"\n🌐 请访问验证：")
    print(f"   https://vaultcaddy.com/jp/blog/manual-vs-ai-cost-analysis.html")
    print(f"   https://vaultcaddy.com/jp/blog/")

if __name__ == '__main__':
    main()

