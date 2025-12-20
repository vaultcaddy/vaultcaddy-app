#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新博客索引页，添加新的收据相关文章
"""

import os
import re
from pathlib import Path

# 新文章配置
NEW_ARTICLES = {
    'en': [
        {
            'slug': 'receipt-scanning-guide',
            'title': 'Complete Receipt Scanning Guide',
            'category': 'Receipt Management',
            'description': 'Master receipt scanning with AI-powered OCR. Learn how to digitize paper receipts, extract data automatically, and organize expense records.',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        },
        {
            'slug': 'expense-tracking-receipts',
            'title': 'Expense Tracking with Receipts',
            'category': 'Expense Management',
            'description': 'Transform expense tracking with automated receipt processing. Learn best practices for managing business expenses and tax deductions.',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        }
    ],
    'jp': [
        {
            'slug': 'receipt-scanning-guide',
            'title': '完全な領収書スキャンガイド',
            'category': '領収書管理',
            'description': 'AIを活用したOCRで領収書スキャンをマスター。紙の領収書をデジタル化し、データを自動抽出し、経費記録を整理する方法を学びます。',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        },
        {
            'slug': 'expense-tracking-receipts',
            'title': '領収書による経費追跡',
            'category': '経費管理',
            'description': '自動化された領収書処理で経費追跡を変革。ビジネス経費と税控除を管理するためのベストプラクティスを学びます。',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        }
    ],
    'kr': [
        {
            'slug': 'receipt-scanning-guide',
            'title': '완벽한 영수증 스캔 가이드',
            'category': '영수증 관리',
            'description': 'AI 기반 OCR로 영수증 스캔 마스터. 종이 영수증을 디지털화하고 데이터를 자동으로 추출하며 비용 기록을 정리하는 방법을 배우세요.',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        },
        {
            'slug': 'expense-tracking-receipts',
            'title': '영수증을 통한 비용 추적',
            'category': '비용 관리',
            'description': '자동화된 영수증 처리로 비용 추적을 혁신하세요. 비즈니스 비용과 세금 공제를 관리하는 모범 사례를 배우세요.',
            'read_time': '12',
            'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80',
            'data_category': 'smb'
        }
    ]
}

def generate_blog_card(article):
    """生成博客卡片HTML"""
    
    return f'''   <a href="{article['slug']}.html" class="blog-card" data-category="{article['data_category']}">
        <img src="{article['image']}" alt="{article['title']}" class="blog-card-image" loading="lazy">
        <div class="blog-card-content">
            <div class="blog-card-category">{article['category']}</div>
            <h3>{article['title']}</h3>
            <p>{article['description']}</p>
            <div class="blog-card-meta">
                <span><i class="far fa-clock"></i> {article['read_time']} min read</span>
                <span><i class="far fa-calendar"></i> 2024</span>
            </div>
        </div>
    </a>'''

def update_blog_index(lang):
    """更新博客索引页"""
    
    file_path = f'{lang}/blog/index.html'
    
    if not os.path.exists(file_path):
        print(f"   ⚠️  文件不存在: {file_path}")
        return 0
    
    print(f"\n🔧 更新: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 blog-grid 区域
    blog_grid_pattern = r'(<div class="blog-grid">)(.*?)(</div>\s*<script)'
    
    match = re.search(blog_grid_pattern, content, re.DOTALL)
    
    if not match:
        print(f"   ❌ 找不到blog-grid区域")
        return 0
    
    # 获取现有的blog cards
    existing_cards = match.group(2)
    
    # 生成新的blog cards
    new_cards = []
    for article in NEW_ARTICLES[lang]:
        new_cards.append(generate_blog_card(article))
    
    # 插入新卡片到开头
    new_cards_html = '\n\n' + '\n\n'.join(new_cards)
    updated_grid = match.group(1) + new_cards_html + existing_cards + match.group(3)
    
    # 替换内容
    content = re.sub(blog_grid_pattern, updated_grid, content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ 添加 {len(NEW_ARTICLES[lang])} 篇新文章")
    
    return len(NEW_ARTICLES[lang])

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          更新博客索引页 - 添加收据相关文章                             ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    total_added = 0
    
    for lang in ['en', 'jp', 'kr']:
        total_added += update_blog_index(lang)
    
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   更新索引页: 3个")
    print(f"   添加文章总数: {total_added}")
    print(f"\n🌐 验证链接：")
    print(f"   https://vaultcaddy.com/en/blog/")
    print(f"   https://vaultcaddy.com/jp/blog/")
    print(f"   https://vaultcaddy.com/kr/blog/")

if __name__ == '__main__':
    main()

