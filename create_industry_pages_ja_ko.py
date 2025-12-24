#!/usr/bin/env python3
"""
创建日文/韩文行业Landing Page
作用: 为日文和韩文各创建5个行业页面，帮助达到100+关键词目标
"""

import os
from pathlib import Path

# 行业配置（前5个最重要的）
INDUSTRIES = {
    'restaurant': {
        'ja': {'name': 'レストラン', 'name_full': 'レストラン業界'},
        'ko': {'name': '레스토랑', 'name_full': '레스토랑 업계'},
        'icon': '🍽️',
        'color': '#ef4444'
    },
    'accountant': {
        'ja': {'name': '会計士', 'name_full': '会計事務所'},
        'ko': {'name': '회계사', 'name_full': '회계 사무소'},
        'icon': '💼',
        'color': '#3b82f6'
    },
    'retail': {
        'ja': {'name': '小売店', 'name_full': '小売業界'},
        'ko': {'name': '소매점', 'name_full': '소매 업계'},
        'icon': '🏪',
        'color': '#10b981'
    },
    'ecommerce': {
        'ja': {'name': 'EC', 'name_full': '電子商取引'},
        'ko': {'name': '전자상거래', 'name_full': '이커머스'},
        'icon': '🛒',
        'color': '#f59e0b'
    },
    'trading': {
        'ja': {'name': '貿易会社', 'name_full': '貿易・商社'},
        'ko': {'name': '무역회사', 'name_full': '무역 회사'},
        'icon': '🌐',
        'color': '#8b5cf6'
    }
}

# 翻译文本
TRANSLATIONS = {
    'ja': {
        'title_template': '{industry}銀行明細書AI自動処理 | 3秒でExcel/QuickBooks/Xero変換 | VaultCaddy',
        'description_template': '{industry}向け銀行明細書AI処理。写真アップロード対応、3秒でExcel/QuickBooks/Xero変換、98%精度、月額HK$46から。会計業務を自動化し、時間を節約。',
        'hero_title': '{industry}向け銀行明細書AI自動処理',
        'hero_subtitle': '会計業務を自動化 · 毎月数時間節約 · 98%の精度 · 月額HK$46から',
        'challenge_title': '{industry}の財務管理における課題',
        'challenge_1': '大量の取引データの手動入力',
        'challenge_2': '複数の銀行口座の管理',
        'challenge_3': '取引カテゴリの分類に時間がかかる',
        'challenge_4': '人為的ミスのリスク',
        'solution_title': 'VaultCaddyが{industry}をどのようにサポートするか',
        'solution_1': '✅ 3秒で全ての銀行明細書を処理',
        'solution_2': '✅ 取引を自動カテゴリ分類',
        'solution_3': '✅ 複数口座の一元管理',
        'solution_4': '✅ QuickBooks/Xeroにワンクリックでインポート',
        'case_study_title': '{industry}のお客様事例',
        'case_study_text': 'VaultCaddyを使用する前は、毎月5時間かけて銀行明細書を手動入力していました。今では10分で完了します。',
        'case_study_author': '香港の{industry}オーナー',
        'roi_title': 'ROI計算',
        'roi_before': '使用前',
        'roi_after': 'VaultCaddy使用後',
        'roi_time': '月間処理時間',
        'roi_cost': '月間コスト',
        'roi_accuracy': '正確性',
        'cta_title': '{industry}の会計業務を自動化',
        'cta_subtitle': '20ページ無料トライアル、クレジットカード不要',
        'cta_button': '今すぐ無料トライアル →',
        'promo_banner': '🎁 期間限定：初月20%オフ！コード <span class="promo-code">SAVE20</span> を使用'
    },
    'ko': {
        'title_template': '{industry} 은행 명세서 AI 자동 처리 | 3초만에 Excel/QuickBooks/Xero 변환 | VaultCaddy',
        'description_template': '{industry}를 위한 은행 명세서 AI 처리. 사진 업로드 지원, 3초만에 Excel/QuickBooks/Xero 변환, 98% 정확도, 월 HK$46부터. 회계 업무 자동화로 시간 절약.',
        'hero_title': '{industry}를 위한 은행 명세서 AI 자동 처리',
        'hero_subtitle': '회계 업무 자동화 · 매월 수 시간 절약 · 98% 정확도 · 월 HK$46부터',
        'challenge_title': '{industry}의 재무 관리 과제',
        'challenge_1': '대량 거래 데이터 수동 입력',
        'challenge_2': '여러 은행 계좌 관리',
        'challenge_3': '거래 분류에 시간 소요',
        'challenge_4': '사람의 실수 위험',
        'solution_title': 'VaultCaddy가 {industry}를 어떻게 지원하는지',
        'solution_1': '✅ 3초만에 모든 은행 명세서 처리',
        'solution_2': '✅ 거래 자동 분류',
        'solution_3': '✅ 여러 계좌 통합 관리',
        'solution_4': '✅ QuickBooks/Xero로 원클릭 가져오기',
        'case_study_title': '{industry} 고객 사례',
        'case_study_text': 'VaultCaddy 사용 전에는 매월 5시간을 은행 명세서 수동 입력에 할애했습니다. 이제는 10분이면 완료됩니다.',
        'case_study_author': '홍콩 {industry} 오너',
        'roi_title': 'ROI 계산',
        'roi_before': '사용 전',
        'roi_after': 'VaultCaddy 사용 후',
        'roi_time': '월 처리 시간',
        'roi_cost': '월 비용',
        'roi_accuracy': '정확도',
        'cta_title': '{industry}의 회계 업무 자동화',
        'cta_subtitle': '20페이지 무료 체험, 신용카드 불필요',
        'cta_button': '지금 무료 체험 시작 →',
        'promo_banner': '🎁 기간 한정: 첫 달 20% 할인! 코드 <span class="promo-code">SAVE20</span> 사용'
    }
}

def generate_industry_page(industry_id, industry_info, lang):
    """生成单个行业页面"""
    
    t = TRANSLATIONS[lang]
    industry_name = industry_info[lang]['name']
    industry_full = industry_info[lang]['name_full']
    icon = industry_info['icon']
    color = industry_info['color']
    
    html_lang = 'ja' if lang == 'ja' else 'ko'
    
    html_content = f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{t['title_template'].format(industry=industry_name)}</title>
    <meta name="description" content="{t['description_template'].format(industry=industry_full)}">
    
    <link rel="canonical" href="https://vaultcaddy.com/{lang}/solutions/{industry_id}/">
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.6; color: #1f2937; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }}
        
        .promo-banner {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            text-align: center;
            padding: 0.75rem 1rem;
            font-weight: 600;
        }}
        
        .promo-code {{
            background: white;
            color: #f59e0b;
            padding: 0.25rem 1rem;
            border-radius: 20px;
            margin-left: 0.5rem;
            font-weight: 700;
        }}
        
        .hero {{
            background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
            color: white;
            padding: 5rem 0;
            text-align: center;
        }}
        
        .hero h1 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; }}
        .hero-subtitle {{ font-size: 1.2rem; opacity: 0.95; }}
        
        .section {{ padding: 4rem 0; }}
        .section-alt {{ background: #f9fafb; }}
        
        .section-title {{ font-size: 2rem; font-weight: 700; margin-bottom: 2rem; text-align: center; }}
        
        .challenge-grid, .solution-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .case-study {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            max-width: 800px;
            margin: 2rem auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .roi-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .roi-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .cta-section {{
            background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: {color};
            padding: 1rem 2.5rem;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 700;
            text-decoration: none;
            margin-top: 1.5rem;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 1.8rem; }}
            .roi-comparison {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="promo-banner">{t['promo_banner']}</div>
    
    <section class="hero">
        <div class="container">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h1>{t['hero_title'].format(industry=industry_name)}</h1>
            <p class="hero-subtitle">{t['hero_subtitle']}</p>
            <a href="https://vaultcaddy.com/{lang}/auth.html" class="cta-button">{t['cta_button']}</a>
        </div>
    </section>
    
    <section class="section">
        <div class="container">
            <h2 class="section-title">{t['challenge_title'].format(industry=industry_name)}</h2>
            <div class="challenge-grid">
                <div class="card">❌ {t['challenge_1']}</div>
                <div class="card">❌ {t['challenge_2']}</div>
                <div class="card">❌ {t['challenge_3']}</div>
                <div class="card">❌ {t['challenge_4']}</div>
            </div>
        </div>
    </section>
    
    <section class="section section-alt">
        <div class="container">
            <h2 class="section-title">{t['solution_title'].format(industry=industry_name)}</h2>
            <div class="solution-grid">
                <div class="card">{t['solution_1']}</div>
                <div class="card">{t['solution_2']}</div>
                <div class="card">{t['solution_3']}</div>
                <div class="card">{t['solution_4']}</div>
            </div>
        </div>
    </section>
    
    <section class="section">
        <div class="container">
            <h2 class="section-title">{t['case_study_title'].format(industry=industry_name)}</h2>
            <div class="case-study">
                <p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 1rem;">"{t['case_study_text']}"</p>
                <p style="font-weight: 600; color: #6b7280;">— {t['case_study_author'].format(industry=industry_name)}</p>
            </div>
        </div>
    </section>
    
    <section class="section section-alt">
        <div class="container">
            <h2 class="section-title">{t['roi_title']}</h2>
            <div class="roi-comparison">
                <div class="roi-card">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">❌ {t['roi_before']}</h3>
                    <p>{t['roi_time']}: <strong>5時間/5시간</strong></p>
                    <p>{t['roi_cost']}: <strong>HK$1,000</strong></p>
                    <p>{t['roi_accuracy']}: <strong>85%</strong></p>
                </div>
                <div class="roi-card" style="border: 3px solid {color};">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: {color};">✅ {t['roi_after']}</h3>
                    <p>{t['roi_time']}: <strong>10分</strong></p>
                    <p>{t['roi_cost']}: <strong>HK$46</strong></p>
                    <p>{t['roi_accuracy']}: <strong>98%</strong></p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="cta-section">
        <div class="container">
            <h2 style="font-size: 2rem; margin-bottom: 1rem;">{t['cta_title'].format(industry=industry_name)}</h2>
            <p>{t['cta_subtitle']}</p>
            <a href="https://vaultcaddy.com/{lang}/auth.html" class="cta-button">{t['cta_button']}</a>
        </div>
    </section>
</body>
</html>'''
    
    return html_content

def main():
    """主函数"""
    
    print("=" * 80)
    print("🏢 創建日文/韓文行業Landing Page")
    print("=" * 80)
    print()
    
    created_files = []
    
    for lang in ['ja', 'ko']:
        print(f"📁 創建 {lang.upper()} 語言行業頁面...")
        
        for industry_id, industry_info in INDUSTRIES.items():
            # 创建目录结构
            dir_path = Path(f"{lang}/solutions/{industry_id}")
            dir_path.mkdir(parents=True, exist_ok=True)
            
            filename = f"{lang}/solutions/{industry_id}/index.html"
            html_content = generate_industry_page(industry_id, industry_info, lang)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_files.append(filename)
            print(f"  ✅ {filename}")
        
        print()
    
    print("=" * 80)
    print(f"✅ 成功創建 {len(created_files)} 個行業Landing Page!")
    print("=" * 80)
    print()
    
    print("創建的檔案:")
    for i, filename in enumerate(created_files, 1):
        print(f"  {i}. {filename}")

if __name__ == '__main__':
    main()

