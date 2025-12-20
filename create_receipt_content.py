#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建收据相关内容 - 博客文章（多语言）
针对银行对账单和收据的SEO优化
"""

import os
from pathlib import Path
from datetime import datetime

# 收据相关文章配置
RECEIPT_ARTICLES = {
    'receipt-scanning-guide': {
        'en': {
            'title': 'Complete Receipt Scanning Guide: Digitize & Organize in 2024',
            'description': 'Master receipt scanning with AI-powered OCR. Learn how to digitize paper receipts, extract data automatically, and organize expense records. Save 10+ hours monthly with smart receipt management.',
            'category': 'Receipt Management',
            'keywords': 'receipt scanning, OCR receipt scanner, digital receipt management, expense tracking, receipt OCR, mobile receipt scanner, automated receipt processing',
            'content_title': 'Complete Receipt Scanning Guide',
            'subtitle': 'Digitize & Organize Your Receipts',
            'intro': 'In today\'s digital age, managing paper receipts is time-consuming and error-prone. This comprehensive guide shows you how AI-powered receipt scanning can transform your expense management.',
            'key_benefit': 'Learn how to scan, extract, and organize receipt data automatically with 99% accuracy, saving 10+ hours monthly.'
        },
        'jp': {
            'title': '完全な領収書スキャンガイド：2024年版デジタル化と整理',
            'description': 'AIを活用したOCRで領収書スキャンをマスター。紙の領収書をデジタル化し、データを自動抽出し、経費記録を整理する方法を学びます。スマートな領収書管理で月間10時間以上を節約。',
            'category': '領収書管理',
            'keywords': '領収書スキャン, OCR領収書スキャナー, デジタル領収書管理, 経費追跡, 領収書OCR, モバイル領収書スキャナー, 自動領収書処理',
            'content_title': '完全な領収書スキャンガイド',
            'subtitle': '領収書のデジタル化と整理',
            'intro': '今日のデジタル時代において、紙の領収書管理は時間がかかり、エラーが発生しやすいものです。この包括的なガイドでは、AIを活用した領収書スキャンが経費管理をどのように変革するかを紹介します。',
            'key_benefit': '99%の精度で領収書データを自動的にスキャン、抽出、整理する方法を学び、月間10時間以上を節約します。'
        },
        'kr': {
            'title': '완벽한 영수증 스캔 가이드: 2024년 디지털화 및 정리',
            'description': 'AI 기반 OCR로 영수증 스캔 마스터. 종이 영수증을 디지털화하고 데이터를 자동으로 추출하며 비용 기록을 정리하는 방법을 배우세요. 스마트 영수증 관리로 월 10시간 이상 절약.',
            'category': '영수증 관리',
            'keywords': '영수증 스캔, OCR 영수증 스캐너, 디지털 영수증 관리, 비용 추적, 영수증 OCR, 모바일 영수증 스캐너, 자동 영수증 처리',
            'content_title': '완벽한 영수증 스캔 가이드',
            'subtitle': '영수증 디지털화 및 정리',
            'intro': '오늘날의 디지털 시대에 종이 영수증 관리는 시간이 많이 걸리고 오류가 발생하기 쉽습니다. 이 종합 가이드는 AI 기반 영수증 스캔이 비용 관리를 어떻게 혁신할 수 있는지 보여줍니다.',
            'key_benefit': '99% 정확도로 영수증 데이터를 자동으로 스캔, 추출 및 정리하는 방법을 배우고 월 10시간 이상을 절약하세요.'
        }
    },
    'expense-tracking-receipts': {
        'en': {
            'title': 'Expense Tracking with Receipt Automation: Complete 2024 Guide',
            'description': 'Transform expense tracking with automated receipt processing. Learn best practices for managing business expenses, tax deductions, and financial records with AI-powered receipt scanning.',
            'category': 'Expense Management',
            'keywords': 'expense tracking, receipt management, business expenses, tax deductions, automated expense reports, receipt organization, expense software',
            'content_title': 'Expense Tracking with Receipts',
            'subtitle': 'Automate Your Expense Management',
            'intro': 'Manual expense tracking is tedious and error-prone. Discover how automated receipt processing can streamline your expense management, improve accuracy, and save valuable time.',
            'key_benefit': 'Automate expense tracking with smart receipt scanning. Reduce manual entry by 90% and never miss a tax deduction again.'
        },
        'jp': {
            'title': '領収書自動化による経費追跡：完全版2024年ガイド',
            'description': '自動化された領収書処理で経費追跡を変革。AIを活用した領収書スキャンで、ビジネス経費、税控除、財務記録を管理するためのベストプラクティスを学びます。',
            'category': '経費管理',
            'keywords': '経費追跡, 領収書管理, ビジネス経費, 税控除, 自動化経費レポート, 領収書整理, 経費ソフトウェア',
            'content_title': '領収書による経費追跡',
            'subtitle': '経費管理を自動化',
            'intro': '手動での経費追跡は面倒でエラーが発生しやすいものです。自動化された領収書処理が経費管理をどのように効率化し、精度を向上させ、貴重な時間を節約できるかを発見してください。',
            'key_benefit': 'スマート領収書スキャンで経費追跡を自動化。手動入力を90%削減し、税控除を見逃すことはありません。'
        },
        'kr': {
            'title': '영수증 자동화를 통한 비용 추적: 완벽한 2024 가이드',
            'description': '자동화된 영수증 처리로 비용 추적을 혁신하세요. AI 기반 영수증 스캔으로 비즈니스 비용, 세금 공제 및 재무 기록을 관리하는 모범 사례를 배우세요.',
            'category': '비용 관리',
            'keywords': '비용 추적, 영수증 관리, 비즈니스 비용, 세금 공제, 자동 비용 보고서, 영수증 정리, 비용 소프트웨어',
            'content_title': '영수증을 통한 비용 추적',
            'subtitle': '비용 관리 자동화',
            'intro': '수동 비용 추적은 지루하고 오류가 발생하기 쉽습니다. 자동화된 영수증 처리가 비용 관리를 간소화하고 정확성을 향상시키며 귀중한 시간을 절약하는 방법을 알아보세요.',
            'key_benefit': '스마트 영수증 스캔으로 비용 추적을 자동화하세요. 수동 입력을 90% 줄이고 세금 공제를 절대 놓치지 마세요.'
        }
    }
}

# 图片映射
ARTICLE_IMAGES = {
    'receipt-scanning-guide': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=1200&h=600&fit=crop&q=80',
    'expense-tracking-receipts': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&h=600&fit=crop&q=80'
}

def generate_receipt_article(slug, lang):
    """生成收据相关文章HTML"""
    
    article = RECEIPT_ARTICLES[slug][lang]
    image_url = ARTICLE_IMAGES[slug]
    
    # 语言特定配置
    lang_config = {
        'en': {
            'read_time': 'min read',
            'key_points': 'Key Points:',
            'why_matters': 'Why This Matters',
            'how_works': 'How It Works',
            'best_practices': 'Best Practices',
            'get_started': 'Get Started Today',
            'cta_text': 'Start Free Trial',
            'free_docs': 'Process your first 20 documents free.',
            'blog_link': '/en/blog/',
            'home_link': '/en/index.html'
        },
        'jp': {
            'read_time': '分',
            'key_points': '重要ポイント：',
            'why_matters': 'なぜ重要か',
            'how_works': '仕組み',
            'best_practices': 'ベストプラクティス',
            'get_started': '今すぐ始める',
            'cta_text': '無料トライアルを開始',
            'free_docs': 'クレジットカード不要。最初の20書類は無料で処理できます。',
            'blog_link': '/jp/blog/',
            'home_link': '/jp/index.html'
        },
        'kr': {
            'read_time': '분',
            'key_points': '주요 사항:',
            'why_matters': '왜 중요한가',
            'how_works': '작동 방식',
            'best_practices': '모범 사례',
            'get_started': '지금 시작하기',
            'cta_text': '무료 평가판 시작',
            'free_docs': '신용카드 필요 없습니다. 처음 20개 문서를 무료로 처리할 수 있습니다.',
            'blog_link': '/kr/blog/',
            'home_link': '/kr/index.html'
        }
    }
    
    config = lang_config[lang]
    
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="{article['description']}">
    <meta name="keywords" content="{article['keywords']}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{article['title']}">
    <meta property="og:description" content="{article['description']}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:url" content="https://vaultcaddy.com/{lang}/blog/{slug}.html">
    <meta property="og:type" content="article">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{article['title']}">
    <meta name="twitter:description" content="{article['description']}">
    <meta name="twitter:image" content="{image_url}">
    
    <link rel="canonical" content="https://vaultcaddy.com/{lang}/blog/{slug}.html">
    <link rel="stylesheet" href="../../styles.css">
    
    <style>
        .article-header {{
            background: #ffffff;
            padding: 8rem 2rem 3rem;
            border-bottom: 1px solid #e5e7eb;
        }}
        .article-container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .article-meta {{
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 1rem;
        }}
        .article-image {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 12px;
            margin: 2rem 0;
        }}
        .article-content {{
            padding: 3rem 2rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.7;
        }}
        .article-content h2 {{
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #1f2937;
        }}
        .article-content p {{
            margin-bottom: 1.5rem;
            color: #4b5563;
        }}
        .highlight-box {{
            background: #f3f4f6;
            padding: 1.5rem;
            border-left: 4px solid #8b5cf6;
            border-radius: 8px;
            margin: 2rem 0;
        }}
        .cta-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 3rem 0;
        }}
        .cta-button {{
            display: inline-block;
            padding: 1rem 2rem;
            background: white;
            color: #667eea;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 1rem;
        }}
    </style>
</head>
<body>
    <!-- 导航栏占位 -->
    <div style="height: 60px;"></div>
    
    <article>
        <header class="article-header">
            <div class="article-container">
                <div class="article-meta">
                    <span>{article['category']}</span> • <span>12 {config['read_time']}</span> • <span>2024</span>
                </div>
                <h1>{article['content_title']}</h1>
                <p style="font-size: 1.25rem; color: #6b7280; margin-top: 1rem;">{article['subtitle']}</p>
            </div>
        </header>
        
        <div class="article-container">
            <img src="{image_url}" alt="{article['content_title']}" class="article-image" loading="lazy">
        </div>
        
        <div class="article-content">
            <div class="highlight-box">
                <p><strong>{config['key_points']}</strong> {article['key_benefit']}</p>
            </div>
            
            <h2>{config['why_matters']}</h2>
            <p>{article['intro']}</p>
            
            <h2>{config['how_works']}</h2>
            <p>VaultCaddy uses advanced AI and OCR technology to automatically extract data from receipts. Simply take a photo or upload a PDF, and our system will:</p>
            <ul>
                <li>Extract merchant name, date, total amount, and line items</li>
                <li>Categorize expenses automatically</li>
                <li>Organize receipts by date and category</li>
                <li>Export to Excel or integrate with accounting software</li>
            </ul>
            
            <h2>{config['best_practices']}</h2>
            <p>To get the most out of receipt scanning:</p>
            <ul>
                <li>Scan receipts immediately after purchase</li>
                <li>Ensure good lighting for photos</li>
                <li>Keep digital backups of all receipts</li>
                <li>Review and categorize expenses regularly</li>
            </ul>
            
            <div class="cta-section">
                <h2>{config['get_started']}</h2>
                <p>{config['free_docs']}</p>
                <a href="/auth.html" class="cta-button">{config['cta_text']}</a>
            </div>
        </div>
    </article>
    
    <script>
        // Add simple navbar
        const navbar = document.createElement('nav');
        navbar.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000;';
        navbar.innerHTML = '<a href="{config['home_link']}" style="font-weight: 600; text-decoration: none; color: #1f2937;">VaultCaddy</a><a href="{config['blog_link']}" style="color: #6b7280; text-decoration: none;">Blog</a>';
        document.body.insertBefore(navbar, document.body.firstChild);
    </script>
</body>
</html>'''
    
    return html

def create_receipt_articles():
    """创建所有收据相关文章"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              📝 创建收据相关博客文章                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    total_created = 0
    
    for slug in RECEIPT_ARTICLES.keys():
        print(f"\n📄 创建文章: {slug}")
        print("="*70)
        
        for lang in ['en', 'jp', 'kr']:
            blog_dir = Path(f'{lang}/blog')
            blog_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = blog_dir / f'{slug}.html'
            
            # 生成HTML
            html = generate_receipt_article(slug, lang)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"   ✅ {lang.upper()}: {file_path}")
            total_created += 1
    
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   创建文章数: {total_created}")
    print(f"   文章主题数: {len(RECEIPT_ARTICLES)}")
    print(f"   语言版本: 3 (EN, JP, KR)")
    print(f"\n🌐 验证链接：")
    print(f"   https://vaultcaddy.com/en/blog/receipt-scanning-guide.html")
    print(f"   https://vaultcaddy.com/jp/blog/receipt-scanning-guide.html")
    print(f"   https://vaultcaddy.com/kr/blog/receipt-scanning-guide.html")

if __name__ == '__main__':
    create_receipt_articles()

