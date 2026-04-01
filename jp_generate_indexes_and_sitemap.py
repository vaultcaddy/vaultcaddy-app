#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日文版索引页面和Sitemap生成器
作用：生成blog索引、solutions索引和sitemap
"""

from pathlib import Path
from datetime import datetime

class JapaneseIndexGenerator:
    def __init__(self):
        self.base_dir = Path('/Users/cavlinyeung/ai-bank-parser')
        self.jp_blog_dir = self.base_dir / 'jp' / 'blog'
        self.jp_solutions_dir = self.base_dir / 'jp' / 'solutions'
    
    def generate_blog_index(self):
        """生成日文blog索引页面"""
        
        blogs = {
            'manual-vs-ai-cost-analysis': ('手動処理 vs AI自動化', 'コスト分析', '8分'),
            'personal-bookkeeping-best-practices': ('個人簿記のベストプラクティス', '個人財務', '10分'),
            'ai-invoice-processing-guide': ('AI請求書処理ガイド', '請求書管理', '12分'),
            'ai-invoice-processing-for-smb': ('中小企業向けAI請求書処理', '中小企業', '9分'),
            'accounting-firm-automation': ('会計事務所の自動化', '会計業務', '11分'),
            'accounting-workflow-optimization': ('会計ワークフロー最適化', 'ワークフロー管理', '10分'),
            'automate-financial-documents': ('財務書類の自動化', 'デジタル変革', '13分'),
            'best-pdf-to-excel-converter': ('最高のPDF-Excel変換ツール', 'ツール比較', '15分'),
            'client-document-management-for-accountants': ('クライアント書類管理', 'クライアント管理', '11分'),
            'freelancer-invoice-management': ('フリーランサー請求書管理', 'フリーランス', '9分'),
            'freelancer-tax-preparation-guide': ('フリーランサー税務準備', '税務計画', '14分'),
            'how-to-convert-pdf-bank-statement-to-excel': ('PDF銀行明細をExcelに変換', 'チュートリアル', '10分'),
            'ocr-accuracy-for-accounting': ('会計におけるOCR精度', '技術', '12分'),
            'ocr-technology-for-accountants': ('会計士向けOCR技術', '技術', '13分'),
            'quickbooks-integration-guide': ('QuickBooks統合ガイド', '統合', '11分'),
            'small-business-document-management': ('中小企業書類管理', 'ビジネス管理', '12分')
        }
        
        html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaultCaddyブログ - 会計自動化と財務管理のヒント</title>
    <meta name="description" content="会計自動化、請求書処理、簿記のベストプラクティス、財務管理に関する専門ガイド。時間を節約してビジネスを成長させる方法を学びましょう。">
    <meta name="keywords" content="会計ブログ,自動化ガイド,請求書処理,簿記ヒント,財務管理,ビジネス効率">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="canonical" href="https://vaultcaddy.com/jp/blog/">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; }
        .blog-hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6rem 2rem 4rem;
            text-align: center;
        }
        .blog-hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .blog-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 4rem auto;
            padding: 0 2rem;
        }
        .blog-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        .blog-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }
        .blog-card-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .blog-card-content { padding: 1.5rem; }
        .blog-card-category {
            color: #667eea;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .blog-card h3 {
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
            color: #1f2937;
        }
        .blog-card-meta {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e5e7eb;
            font-size: 0.875rem;
            color: #9ca3af;
        }
    </style>
</head>
<body>
    <div id="navbar-container"></div>
    
    <section class="blog-hero">
        <h1>VaultCaddyブログ</h1>
        <p style="font-size: 1.25rem; max-width: 800px; margin: 0 auto;">
            会計自動化、財務管理、ビジネス効率に関する専門ガイド
        </p>
    </section>
    
    <div class="blog-grid">
"""
        
        for filename, (title, category, reading_time) in blogs.items():
            image_keyword = filename.replace('-', ',')
            html += f"""        <a href="{filename}.html" class="blog-card">
            <img src="https://source.unsplash.com/800x400/?{image_keyword},business,japan" 
                 alt="{title}" 
                 class="blog-card-image"
                 loading="lazy">
            <div class="blog-card-content">
                <div class="blog-card-category">{category}</div>
                <h3>{title}</h3>
                <div class="blog-card-meta">
                    <span><i class="fas fa-clock"></i> {reading_time}</span>
                    <span><i class="fas fa-calendar"></i> 2024</span>
                </div>
            </div>
        </a>
"""
        
        html += """    </div>
    
    <script src="../../load-unified-navbar.js"></script>
</body>
</html>"""
        
        return html
    
    def generate_solutions_index(self):
        """生成日文solutions索引页面"""
        
        solutions = {
            'freelancer': ('フリーランサー', 'fa-user-tie'),
            'small-business': ('中小企業', 'fa-store'),
            'accountant': ('会計士', 'fa-calculator'),
            'ecommerce': ('Eコマース', 'fa-shopping-cart'),
            'restaurant': ('レストラン', 'fa-utensils'),
            'real-estate': ('不動産', 'fa-building'),
            'consultant': ('コンサルタント', 'fa-briefcase'),
            'startup': ('スタートアップ', 'fa-rocket'),
            'nonprofit': ('非営利団体', 'fa-hands-helping'),
            'photographer': ('フォトグラファー', 'fa-camera'),
            'healthcare': ('医療', 'fa-heartbeat'),
            'lawyer': ('弁護士', 'fa-gavel'),
            'contractor': ('建設業者', 'fa-hard-hat'),
            'personal-finance': ('個人財務', 'fa-piggy-bank'),
            'fitness-coach': ('フィットネスコーチ', 'fa-dumbbell'),
            'designer': ('デザイナー', 'fa-paint-brush'),
            'property-manager': ('不動産管理', 'fa-key'),
            'travel-agent': ('旅行代理店', 'fa-plane'),
            'tutor': ('家庭教師', 'fa-graduation-cap'),
            'event-planner': ('イベントプランナー', 'fa-calendar-alt'),
            'delivery-driver': ('配達ドライバー', 'fa-truck'),
            'beauty-salon': ('美容サロン', 'fa-cut'),
            'retail-store': ('小売店', 'fa-cash-register'),
            'marketing-agency': ('マーケティングエージェンシー', 'fa-bullhorn'),
            'coworking-space': ('コワーキングスペース', 'fa-users'),
            'cleaning-service': ('清掃サービス', 'fa-broom'),
            'pet-service': ('ペットサービス', 'fa-paw'),
            'artist': ('アーティスト', 'fa-palette'),
            'musician': ('ミュージシャン', 'fa-music'),
            'developer': ('開発者', 'fa-code')
        }
        
        html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>あらゆる専門家向けソリューション | VaultCaddy</title>
    <meta name="description" content="フリーランサー、中小企業、会計士など向けのAI書類処理ソリューション。あなたにぴったりの自動化ソリューションを見つけましょう。">
    <meta name="keywords" content="会計自動化,請求書処理,書類管理,AI OCR,ビジネスソリューション">
    <link rel="stylesheet" href="../../styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6rem 2rem 4rem;
            text-align: center;
        }
        .hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .solutions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 4rem auto;
            padding: 0 2rem;
        }
        .solution-card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
            text-align: center;
        }
        .solution-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }
        .solution-card i {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 1rem;
        }
        .solution-card h3 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: #1f2937;
        }
    </style>
</head>
<body>
    <div id="navbar-container"></div>
    
    <section class="hero">
        <h1>あらゆる専門家向けソリューション</h1>
        <p style="font-size: 1.25rem; max-width: 800px; margin: 0 auto;">
            あなたの特定のニーズに合わせたAI書類処理ソリューション
        </p>
    </section>
    
    <div class="solutions-grid">
"""
        
        for key, (title, icon) in solutions.items():
            html += f"""        <a href="{key}/" class="solution-card">
            <i class="fas {icon}"></i>
            <h3>{title}</h3>
        </a>
"""
        
        html += """    </div>
    
    <script src="../../load-unified-navbar.js"></script>
</body>
</html>"""
        
        return html
    
    def generate_sitemap(self):
        """生成日文sitemap条目"""
        
        urls = []
        
        # 主页面
        urls.append('https://vaultcaddy.com/jp/')
        urls.append('https://vaultcaddy.com/jp/blog/')
        urls.append('https://vaultcaddy.com/jp/solutions/')
        
        # Blog文章
        blogs = [
            'manual-vs-ai-cost-analysis', 'personal-bookkeeping-best-practices',
            'ai-invoice-processing-guide', 'ai-invoice-processing-for-smb',
            'accounting-firm-automation', 'accounting-workflow-optimization',
            'automate-financial-documents', 'best-pdf-to-excel-converter',
            'client-document-management-for-accountants', 'freelancer-invoice-management',
            'freelancer-tax-preparation-guide', 'how-to-convert-pdf-bank-statement-to-excel',
            'ocr-accuracy-for-accounting', 'ocr-technology-for-accountants',
            'quickbooks-integration-guide', 'small-business-document-management'
        ]
        
        for blog in blogs:
            urls.append(f'https://vaultcaddy.com/jp/blog/{blog}.html')
        
        # Landing pages
        solutions = [
            'freelancer', 'small-business', 'accountant', 'ecommerce', 'restaurant',
            'real-estate', 'consultant', 'startup', 'nonprofit', 'photographer',
            'healthcare', 'lawyer', 'contractor', 'personal-finance', 'fitness-coach',
            'designer', 'property-manager', 'travel-agent', 'tutor', 'event-planner',
            'delivery-driver', 'beauty-salon', 'retail-store', 'marketing-agency',
            'coworking-space', 'cleaning-service', 'pet-service', 'artist', 'musician', 'developer'
        ]
        
        for solution in solutions:
            urls.append(f'https://vaultcaddy.com/jp/solutions/{solution}/')
        
        return urls
    
    def run(self):
        """执行完整流程"""
        print("🚀 生成日文索引页面和sitemap...")
        print("=" * 80)
        
        # 生成blog索引
        print("\n📑 生成blog索引页面...")
        blog_index = self.generate_blog_index()
        blog_index_path = self.jp_blog_dir / 'index.html'
        with open(blog_index_path, 'w', encoding='utf-8') as f:
            f.write(blog_index)
        print(f"   ✅ {blog_index_path}")
        
        # 生成solutions索引
        print("\n📑 生成solutions索引页面...")
        solutions_index = self.generate_solutions_index()
        solutions_index_path = self.jp_solutions_dir / 'index.html'
        with open(solutions_index_path, 'w', encoding='utf-8') as f:
            f.write(solutions_index)
        print(f"   ✅ {solutions_index_path}")
        
        # 生成sitemap
        print("\n🗺️  生成sitemap条目...")
        urls = self.generate_sitemap()
        sitemap_file = self.base_dir / 'jp-sitemap-urls.txt'
        with open(sitemap_file, 'w') as f:
            f.write('\n'.join(urls))
        print(f"   ✅ {sitemap_file}")
        print(f"   📊 总计: {len(urls)} 个URL")
        
        print("\n" + "=" * 80)
        print("✅ 完成！")

if __name__ == "__main__":
    generator = JapaneseIndexGenerator()
    generator.run()

