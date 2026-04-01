#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韩文版索引页面和Sitemap生成器
作用：生成blog索引、solutions索引和sitemap
"""

from pathlib import Path
from datetime import datetime

class KoreanIndexGenerator:
    def __init__(self):
        self.base_dir = Path('/Users/cavlinyeung/ai-bank-parser')
        self.kr_blog_dir = self.base_dir / 'kr' / 'blog'
        self.kr_solutions_dir = self.base_dir / 'kr' / 'solutions'
    
    def generate_blog_index(self):
        """生成韩文blog索引页面"""
        
        blogs = {
            'manual-vs-ai-cost-analysis': ('수동 처리 vs AI 자동화', '비용 분석', '8분'),
            'personal-bookkeeping-best-practices': ('개인 부기 모범 사례', '개인 재무', '10분'),
            'ai-invoice-processing-guide': ('AI 송장 처리 가이드', '송장 관리', '12분'),
            'ai-invoice-processing-for-smb': ('중소기업용 AI 송장 처리', '중소기업', '9분'),
            'accounting-firm-automation': ('회계 사무소 자동화', '회계 업무', '11분'),
            'accounting-workflow-optimization': ('회계 워크플로우 최적화', '워크플로우 관리', '10분'),
            'automate-financial-documents': ('재무 문서 자동화', '디지털 혁신', '13분'),
            'best-pdf-to-excel-converter': ('최고의 PDF-Excel 변환 도구', '도구 비교', '15분'),
            'client-document-management-for-accountants': ('고객 문서 관리', '고객 관리', '11분'),
            'freelancer-invoice-management': ('프리랜서 송장 관리', '프리랜싱', '9분'),
            'freelancer-tax-preparation-guide': ('프리랜서 세금 준비', '세금 계획', '14분'),
            'how-to-convert-pdf-bank-statement-to-excel': ('PDF 은행 명세서 Excel 변환', '튜토리얼', '10분'),
            'ocr-accuracy-for-accounting': ('회계에서의 OCR 정확도', '기술', '12분'),
            'ocr-technology-for-accountants': ('회계사를 위한 OCR 기술', '기술', '13분'),
            'quickbooks-integration-guide': ('QuickBooks 통합 가이드', '통합', '11분'),
            'small-business-document-management': ('중소기업 문서 관리', '비즈니스 관리', '12분')
        }
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaultCaddy 블로그 - 회계 자동화 및 재무 관리 팁</title>
    <meta name="description" content="회계 자동화, 송장 처리, 부기 모범 사례, 재무 관리에 대한 전문 가이드. 시간을 절약하고 비즈니스를 성장시키는 방법을 배우세요.">
    <meta name="keywords" content="회계 블로그,자동화 가이드,송장 처리,부기 팁,재무 관리,비즈니스 효율성">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="canonical" href="https://vaultcaddy.com/kr/blog/">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif; }
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
        <h1>VaultCaddy 블로그</h1>
        <p style="font-size: 1.25rem; max-width: 800px; margin: 0 auto;">
            회계 자동화, 재무 관리, 비즈니스 효율성에 대한 전문 가이드
        </p>
    </section>
    
    <div class="blog-grid">
"""
        
        for filename, (title, category, reading_time) in blogs.items():
            image_keyword = filename.replace('-', ',')
            html += f"""        <a href="{filename}.html" class="blog-card">
            <img src="https://source.unsplash.com/800x400/?{image_keyword},business,korea" 
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
        """生成韩文solutions索引页面"""
        
        solutions = {
            'freelancer': ('프리랜서', 'fa-user-tie'),
            'small-business': ('중소기업', 'fa-store'),
            'accountant': ('회계사', 'fa-calculator'),
            'ecommerce': ('이커머스', 'fa-shopping-cart'),
            'restaurant': ('레스토랑', 'fa-utensils'),
            'real-estate': ('부동산', 'fa-building'),
            'consultant': ('컨설턴트', 'fa-briefcase'),
            'startup': ('스타트업', 'fa-rocket'),
            'nonprofit': ('비영리', 'fa-hands-helping'),
            'photographer': ('사진작가', 'fa-camera'),
            'healthcare': ('의료', 'fa-heartbeat'),
            'lawyer': ('변호사', 'fa-gavel'),
            'contractor': ('건설업자', 'fa-hard-hat'),
            'personal-finance': ('개인 재무', 'fa-piggy-bank'),
            'fitness-coach': ('피트니스 코치', 'fa-dumbbell'),
            'designer': ('디자이너', 'fa-paint-brush'),
            'property-manager': ('부동산 관리', 'fa-key'),
            'travel-agent': ('여행사', 'fa-plane'),
            'tutor': ('과외', 'fa-graduation-cap'),
            'event-planner': ('이벤트 기획', 'fa-calendar-alt'),
            'delivery-driver': ('배달 드라이버', 'fa-truck'),
            'beauty-salon': ('미용실', 'fa-cut'),
            'retail-store': ('소매점', 'fa-cash-register'),
            'marketing-agency': ('마케팅 에이전시', 'fa-bullhorn'),
            'coworking-space': ('코워킹 스페이스', 'fa-users'),
            'cleaning-service': ('청소 서비스', 'fa-broom'),
            'pet-service': ('애완동물 서비스', 'fa-paw'),
            'artist': ('아티스트', 'fa-palette'),
            'musician': ('뮤지션', 'fa-music'),
            'developer': ('개발자', 'fa-code')
        }
        
        html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>모든 전문가를 위한 솔루션 | VaultCaddy</title>
    <meta name="description" content="프리랜서, 중소기업, 회계사 등을 위한 AI 문서 처리 솔루션. 완벽한 자동화 솔루션을 찾으세요.">
    <meta name="keywords" content="회계 자동화,송장 처리,문서 관리,AI OCR,비즈니스 솔루션">
    <link rel="stylesheet" href="../../styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif; }
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
        <h1>모든 전문가를 위한 솔루션</h1>
        <p style="font-size: 1.25rem; max-width: 800px; margin: 0 auto;">
            특정 요구사항에 맞춘 AI 문서 처리 솔루션
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
        """生成韩文sitemap条目"""
        
        urls = []
        
        # 主页面
        urls.append('https://vaultcaddy.com/kr/')
        urls.append('https://vaultcaddy.com/kr/blog/')
        urls.append('https://vaultcaddy.com/kr/solutions/')
        
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
            urls.append(f'https://vaultcaddy.com/kr/blog/{blog}.html')
        
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
            urls.append(f'https://vaultcaddy.com/kr/solutions/{solution}/')
        
        return urls
    
    def run(self):
        """执行完整流程"""
        print("🚀 한국어 인덱스 페이지 및 sitemap 생성...")
        print("=" * 80)
        
        # 生成blog索引
        print("\n📑 blog 인덱스 페이지 생성...")
        blog_index = self.generate_blog_index()
        blog_index_path = self.kr_blog_dir / 'index.html'
        with open(blog_index_path, 'w', encoding='utf-8') as f:
            f.write(blog_index)
        print(f"   ✅ {blog_index_path}")
        
        # 生成solutions索引
        print("\n📑 solutions 인덱스 페이지 생성...")
        solutions_index = self.generate_solutions_index()
        solutions_index_path = self.kr_solutions_dir / 'index.html'
        with open(solutions_index_path, 'w', encoding='utf-8') as f:
            f.write(solutions_index)
        print(f"   ✅ {solutions_index_path}")
        
        # 生成sitemap
        print("\n🗺️  sitemap 항목 생성...")
        urls = self.generate_sitemap()
        sitemap_file = self.base_dir / 'kr-sitemap-urls.txt'
        with open(sitemap_file, 'w') as f:
            f.write('\n'.join(urls))
        print(f"   ✅ {sitemap_file}")
        print(f"   📊 총: {len(urls)} 개 URL")
        
        print("\n" + "=" * 80)
        print("✅ 완료!")

if __name__ == "__main__":
    generator = KoreanIndexGenerator()
    generator.run()

