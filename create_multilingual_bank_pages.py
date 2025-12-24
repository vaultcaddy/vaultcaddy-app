#!/usr/bin/env python3
"""
批量创建4语言银行Landing Page
作用: 生成英文、日文、韩文的10个银行页面（中文已有）
"""

import os
from pathlib import Path

# 银行配置
BANKS = {
    'hsbc': {
        'zh': {'name': '匯豐銀行', 'name_en': 'HSBC'},
        'en': {'name': 'HSBC', 'name_full': 'HSBC Bank'},
        'ja': {'name': 'HSBC', 'name_full': 'HSBC銀行'},
        'ko': {'name': 'HSBC', 'name_full': 'HSBC 은행'},
        'color': '#DB0011',
        'color_dark': '#8B0008',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'hangseng': {
        'zh': {'name': '恆生銀行', 'name_en': 'Hang Seng'},
        'en': {'name': 'Hang Seng Bank', 'name_full': 'Hang Seng Bank'},
        'ja': {'name': 'ハンセン銀行', 'name_full': 'Hang Seng Bank'},
        'ko': {'name': '항셍은행', 'name_full': 'Hang Seng Bank'},
        'color': '#00857D',
        'color_dark': '#005550',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bochk': {
        'zh': {'name': '中國銀行(香港)', 'name_en': 'BOC Hong Kong'},
        'en': {'name': 'Bank of China (Hong Kong)', 'name_full': 'BOC Hong Kong'},
        'ja': {'name': '中国銀行（香港）', 'name_full': 'Bank of China (Hong Kong)'},
        'ko': {'name': '중국은행(홍콩)', 'name_full': 'Bank of China (Hong Kong)'},
        'color': '#CC092F',
        'color_dark': '#8B0620',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'sc': {
        'zh': {'name': '渣打銀行', 'name_en': 'Standard Chartered'},
        'en': {'name': 'Standard Chartered Bank', 'name_full': 'Standard Chartered'},
        'ja': {'name': 'スタンダードチャータード銀行', 'name_full': 'Standard Chartered'},
        'ko': {'name': '스탠다드차타드은행', 'name_full': 'Standard Chartered'},
        'color': '#00843D',
        'color_dark': '#00562A',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'dbs': {
        'zh': {'name': '星展銀行', 'name_en': 'DBS'},
        'en': {'name': 'DBS Bank', 'name_full': 'DBS'},
        'ja': {'name': 'DBS銀行', 'name_full': 'DBS Bank'},
        'ko': {'name': 'DBS은행', 'name_full': 'DBS Bank'},
        'color': '#D0262D',
        'color_dark': '#8B1A1E',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bea': {
        'zh': {'name': '東亞銀行', 'name_en': 'Bank of East Asia'},
        'en': {'name': 'Bank of East Asia', 'name_full': 'BEA'},
        'ja': {'name': '東亜銀行', 'name_full': 'Bank of East Asia'},
        'ko': {'name': '동아은행', 'name_full': 'Bank of East Asia'},
        'color': '#007A33',
        'color_dark': '#005122',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'citibank': {
        'zh': {'name': '花旗銀行', 'name_en': 'Citibank'},
        'en': {'name': 'Citibank', 'name_full': 'Citibank'},
        'ja': {'name': 'シティバンク', 'name_full': 'Citibank'},
        'ko': {'name': '씨티은행', 'name_full': 'Citibank'},
        'color': '#0072CE',
        'color_dark': '#004C8A',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'dahsing': {
        'zh': {'name': '大新銀行', 'name_en': 'Dah Sing Bank'},
        'en': {'name': 'Dah Sing Bank', 'name_full': 'Dah Sing'},
        'ja': {'name': '大新銀行', 'name_full': 'Dah Sing Bank'},
        'ko': {'name': '다싱은행', 'name_full': 'Dah Sing Bank'},
        'color': '#003A70',
        'color_dark': '#00264C',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'citic': {
        'zh': {'name': '中信銀行國際', 'name_en': 'CITIC Bank'},
        'en': {'name': 'CITIC Bank International', 'name_full': 'CITIC'},
        'ja': {'name': '中信銀行インターナショナル', 'name_full': 'CITIC Bank'},
        'ko': {'name': 'CITIC은행', 'name_full': 'CITIC Bank'},
        'color': '#C8102E',
        'color_dark': '#870B1F',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bankcomm': {
        'zh': {'name': '交通銀行', 'name_en': 'Bank of Communications'},
        'en': {'name': 'Bank of Communications', 'name_full': 'BoCom'},
        'ja': {'name': '交通銀行', 'name_full': 'Bank of Communications'},
        'ko': {'name': '교통은행', 'name_full': 'Bank of Communications'},
        'color': '#004B8D',
        'color_dark': '#00325E',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    }
}

# 翻译文本
TRANSLATIONS = {
    'en': {
        'title_template': '{bank} Bank Statement AI Processing | Convert to Excel/QuickBooks/Xero in 3 Seconds | HK$46/month | VaultCaddy Hong Kong',
        'description_template': '{bank} bank statement AI auto-processing, photo upload supported, converts to Excel/QuickBooks/Xero in 3 seconds, 98% accuracy, from HK$46/month. PDF and photo upload supported. Free trial 20 pages.',
        'hero_title': '{bank} Bank Statement AI Auto-Processing',
        'hero_subtitle': 'Photo Upload · 3-Second Processing · 98% Accuracy · From HK$46/month',
        'simple_label': 'Simple',
        'simple_detail': 'Photo Upload<br>Mobile Ready',
        'fast_label': '3 Seconds',
        'fast_detail': 'Fast Processing<br>vs Manual 2 hours',
        'accurate_label': '98%',
        'accurate_detail': 'High Accuracy<br>vs Manual 85%',
        'cheap_label': '$46',
        'cheap_detail': 'Great Value<br>per month/100 pages',
        'cta_button': 'Free Trial 20 Pages →',
        'trust_1': '✓ No Credit Card',
        'trust_2': '✓ See Results in 3 Seconds',
        'trust_3': '✓ All {bank} Accounts Supported',
        'section_title': '3 Steps to Process {bank} Bank Statements',
        'section_subtitle': 'So simple a student can use it, faster than making a coffee',
        'step1_title': 'Upload {bank} Statement',
        'step1_desc': '· Photo upload<br>· Or upload PDF<br>· Multi-page supported<br>· Drag and drop',
        'step1_time': '30 seconds',
        'step2_title': 'AI Auto-Recognition',
        'step2_desc': '· Auto-recognize {bank} format<br>· Extract all transactions<br>· 98% recognition accuracy<br>· Auto-categorize',
        'step2_time': '3 seconds',
        'step3_title': 'One-Click Export',
        'step3_desc': '· QuickBooks IIF file<br>· Or Excel/CSV format<br>· Edit before export<br>· Direct import to accounting software',
        'step3_time': '5 seconds',
        'faq_title': '{bank} Bank Statement Processing FAQ',
        'faq_subtitle': 'Answers to all your questions about {bank} statement AI processing',
        'final_cta_title': 'Start Processing Your {bank} Statements',
        'final_cta_subtitle': 'Free trial 20 pages, no credit card required, see results in 3 seconds',
        'final_cta_button': 'Start Free Trial Now →',
        'promo_banner': '🎁 Limited Offer: 20% off first month! Use code <span class="promo-code">SAVE20</span>'
    },
    'ja': {
        'title_template': '{bank}の取引明細書AI処理 | 3秒でExcel/QuickBooks/Xeroに変換 | 月額HK$46 | VaultCaddy香港',
        'description_template': '{bank}の取引明細書をAIで自動処理、写真アップロード対応、3秒でExcel/QuickBooks/Xeroに変換、98%の精度、月額HK$46から。PDFと写真アップロードに対応。20ページ無料トライアル。',
        'hero_title': '{bank}取引明細書AI自動処理',
        'hero_subtitle': '写真アップロード · 3秒で処理完了 · 98%の精度 · 月額HK$46から',
        'simple_label': 'シンプル',
        'simple_detail': '写真アップロード<br>モバイル対応',
        'fast_label': '3秒',
        'fast_detail': '高速処理<br>手動2時間 vs',
        'accurate_label': '98%',
        'accurate_detail': '高精度<br>手動85% vs',
        'cheap_label': '$46',
        'cheap_detail': '超お得<br>月額/100ページ',
        'cta_button': '20ページ無料トライアル →',
        'trust_1': '✓ クレジットカード不要',
        'trust_2': '✓ 3秒で結果確認',
        'trust_3': '✓ 全{bank}アカウント対応',
        'section_title': '{bank}取引明細書を3ステップで処理',
        'section_subtitle': '小学生でも使えるほど簡単、コーヒーを淹れる時間もかかりません',
        'step1_title': '{bank}明細書をアップロード',
        'step1_desc': '· 写真撮影でOK<br>· またはPDFアップロード<br>· 複数ページ対応<br>· ドラッグ&ドロップ',
        'step1_time': '30秒',
        'step2_title': 'AI自動認識',
        'step2_desc': '· {bank}形式を自動認識<br>· 全取引を抽出<br>· 98%の認識精度<br>· 自動カテゴリ分類',
        'step2_time': '3秒',
        'step3_title': 'ワンクリックでエクスポート',
        'step3_desc': '· QuickBooks IIFファイル<br>· またはExcel/CSV形式<br>· エクスポート前に編集可能<br>· 会計ソフトに直接インポート',
        'step3_time': '5秒',
        'faq_title': '{bank}取引明細書処理のよくある質問',
        'faq_subtitle': '{bank}明細書AI処理に関するすべての質問にお答えします',
        'final_cta_title': '{bank}明細書の処理を始めましょう',
        'final_cta_subtitle': '20ページ無料トライアル、クレジットカード不要、3秒で結果確認',
        'final_cta_button': '今すぐ無料トライアル →',
        'promo_banner': '🎁 期間限定：初月20%オフ！コード <span class="promo-code">SAVE20</span> を使用'
    },
    'ko': {
        'title_template': '{bank} 은행 명세서 AI 처리 | 3초만에 Excel/QuickBooks/Xero 변환 | 월 HK$46 | VaultCaddy 홍콩',
        'description_template': '{bank} 은행 명세서 AI 자동 처리, 사진 업로드 지원, 3초만에 Excel/QuickBooks/Xero 변환, 98% 정확도, 월 HK$46부터. PDF 및 사진 업로드 지원. 20페이지 무료 체험.',
        'hero_title': '{bank} 은행 명세서 AI 자동 처리',
        'hero_subtitle': '사진 업로드 · 3초 처리 완료 · 98% 정확도 · 월 HK$46부터',
        'simple_label': '간편함',
        'simple_detail': '사진 업로드<br>모바일 지원',
        'fast_label': '3초',
        'fast_detail': '빠른 처리<br>수동 2시간 vs',
        'accurate_label': '98%',
        'accurate_detail': '높은 정확도<br>수동 85% vs',
        'cheap_label': '$46',
        'cheap_detail': '저렴한 가격<br>월/100페이지',
        'cta_button': '20페이지 무료 체험 →',
        'trust_1': '✓ 신용카드 불필요',
        'trust_2': '✓ 3초만에 결과 확인',
        'trust_3': '✓ 모든 {bank} 계좌 지원',
        'section_title': '3단계로 {bank} 은행 명세서 처리',
        'section_subtitle': '초등학생도 사용할 수 있을 만큼 간단, 커피 마시는 시간도 안 걸립니다',
        'step1_title': '{bank} 명세서 업로드',
        'step1_desc': '· 사진 촬영<br>· 또는 PDF 업로드<br>· 여러 페이지 지원<br>· 드래그 앤 드롭',
        'step1_time': '30초',
        'step2_title': 'AI 자동 인식',
        'step2_desc': '· {bank} 형식 자동 인식<br>· 모든 거래 추출<br>· 98% 인식 정확도<br>· 자동 분류',
        'step2_time': '3초',
        'step3_title': '원클릭 내보내기',
        'step3_desc': '· QuickBooks IIF 파일<br>· 또는 Excel/CSV 형식<br>· 내보내기 전 편집 가능<br>· 회계 소프트웨어로 직접 가져오기',
        'step3_time': '5초',
        'faq_title': '{bank} 은행 명세서 처리 FAQ',
        'faq_subtitle': '{bank} 명세서 AI 처리에 대한 모든 질문에 답변드립니다',
        'final_cta_title': '{bank} 명세서 처리 시작하기',
        'final_cta_subtitle': '20페이지 무료 체험, 신용카드 불필요, 3초만에 결과 확인',
        'final_cta_button': '지금 무료 체험 시작 →',
        'promo_banner': '🎁 기간 한정: 첫 달 20% 할인! 코드 <span class="promo-code">SAVE20</span> 사용'
    }
}

def generate_bank_page(bank_id, bank_info, lang):
    """生成单个语言的银行页面"""
    
    t = TRANSLATIONS[lang]
    bank_name = bank_info[lang]['name']
    bank_full = bank_info[lang]['name_full']
    color = bank_info['color']
    color_dark = bank_info['color_dark']
    unsplash_bg = bank_info['unsplash_bg']
    unsplash_demo = bank_info['unsplash_demo']
    
    # 语言代码映射
    lang_codes = {'en': 'en', 'ja': 'ja', 'ko': 'ko'}
    html_lang = lang_codes[lang]
    
    html_content = f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://images.unsplash.com">
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{t['title_template'].format(bank=bank_name)}</title>
    <meta name="description" content="{t['description_template'].format(bank=bank_name)}">
    
    <link rel="canonical" href="https://vaultcaddy.com/{lang}/{bank_id}-bank-statement.html">
    
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #ffffff;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        
        .promo-banner {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            text-align: center;
            padding: 0.75rem 1rem;
            font-weight: 600;
            font-size: 1rem;
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
            background: linear-gradient(135deg, {color} 0%, {color_dark} 100%);
            color: white;
            padding: 4rem 0;
            position: relative;
            overflow: hidden;
        }}
        
        .hero-background {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.15;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
            text-align: center;
        }}
        
        .bank-logo {{
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            display: inline-block;
            margin-bottom: 1.5rem;
        }}
        
        .hero h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        
        .hero-subtitle {{
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.95;
        }}
        
        .core-benefits {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin: 2rem auto;
            max-width: 900px;
        }}
        
        .benefit-card {{
            background: rgba(255, 255, 255, 0.15);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        .benefit-icon {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
            display: block;
        }}
        
        .benefit-number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #fbbf24;
            display: block;
            margin-bottom: 0.25rem;
        }}
        
        .benefit-label {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .benefit-detail {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 0.25rem;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: {color};
            padding: 1.2rem 3rem;
            border-radius: 50px;
            font-size: 1.3rem;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: none;
            cursor: pointer;
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }}
        
        .trust-badges {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 2rem;
            font-size: 0.95rem;
            flex-wrap: wrap;
        }}
        
        .features-section {{
            padding: 5rem 0;
            background: #f9fafb;
        }}
        
        .section-title {{
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            color: #1f2937;
        }}
        
        .section-subtitle {{
            text-align: center;
            font-size: 1.2rem;
            color: #6b7280;
            margin-bottom: 3rem;
        }}
        
        .steps-container {{
            display: grid;
            grid-template-columns: 1fr auto 1fr auto 1fr;
            gap: 1.5rem;
            align-items: center;
            margin-top: 3rem;
        }}
        
        .step-card {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }}
        
        .step-number {{
            background: {color};
            color: white;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}
        
        .step-icon {{
            font-size: 4rem;
            margin-bottom: 1rem;
            display: block;
        }}
        
        .step-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .step-description {{
            color: #6b7280;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}
        
        .step-time {{
            background: #d1fae5;
            color: #065f46;
            padding: 0.35rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
        }}
        
        .arrow {{
            font-size: 2.5rem;
            color: {color};
        }}
        
        .faq-section {{
            padding: 5rem 0;
            background: white;
        }}
        
        .final-cta-section {{
            padding: 5rem 0;
            background: linear-gradient(135deg, {color} 0%, {color_dark} 100%);
            color: white;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 1.8rem; }}
            .core-benefits {{ grid-template-columns: repeat(2, 1fr); }}
            .steps-container {{ grid-template-columns: 1fr; }}
            .arrow {{ transform: rotate(90deg); }}
        }}
    </style>
</head>
<body>
    <div class="promo-banner">{t['promo_banner']}</div>
    
    <section class="hero">
        <img src="https://images.unsplash.com/{unsplash_bg}?w=1920&h=800&fit=crop" 
             alt="{bank_name} Banking" 
             class="hero-background"
             loading="eager">
        
        <div class="container hero-content">
            <div class="bank-logo">
                <strong style="color: {color}; font-size: 1.8rem;">{bank_full}</strong>
            </div>
            
            <h1>{t['hero_title'].format(bank=bank_name)}</h1>
            <p class="hero-subtitle">{t['hero_subtitle']}</p>
            
            <div class="core-benefits">
                <div class="benefit-card">
                    <span class="benefit-icon">📱</span>
                    <span class="benefit-number">{t['simple_label']}</span>
                    <div class="benefit-label">{t['simple_detail']}</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">⚡</span>
                    <span class="benefit-number">{t['fast_label']}</span>
                    <div class="benefit-label">{t['fast_detail']}</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">✓</span>
                    <span class="benefit-number">{t['accurate_label']}</span>
                    <div class="benefit-label">{t['accurate_detail']}</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">💰</span>
                    <span class="benefit-number">{t['cheap_label']}</span>
                    <div class="benefit-label">{t['cheap_detail']}</div>
                </div>
            </div>
            
            <a href="https://vaultcaddy.com/{lang}/auth.html" class="cta-button">{t['cta_button']}</a>
            
            <div class="trust-badges">
                <div>{t['trust_1']}</div>
                <div>{t['trust_2']}</div>
                <div>{t['trust_3'].format(bank=bank_full)}</div>
            </div>
        </div>
    </section>
    
    <section class="features-section">
        <div class="container">
            <h2 class="section-title">{t['section_title'].format(bank=bank_name)}</h2>
            <p class="section-subtitle">{t['section_subtitle']}</p>
            
            <div class="steps-container">
                <div class="step-card">
                    <div class="step-number">1</div>
                    <span class="step-icon">📄</span>
                    <h3 class="step-title">{t['step1_title'].format(bank=bank_full)}</h3>
                    <p class="step-description">{t['step1_desc']}</p>
                    <span class="step-time">{t['step1_time']}</span>
                </div>
                
                <div class="arrow">→</div>
                
                <div class="step-card">
                    <div class="step-number">2</div>
                    <span class="step-icon">🤖</span>
                    <h3 class="step-title">{t['step2_title']}</h3>
                    <p class="step-description">{t['step2_desc'].format(bank=bank_full)}</p>
                    <span class="step-time" style="background: #fbbf24; color: #78350f;">{t['step2_time']}</span>
                </div>
                
                <div class="arrow">→</div>
                
                <div class="step-card">
                    <div class="step-number">3</div>
                    <span class="step-icon">📊</span>
                    <h3 class="step-title">{t['step3_title']}</h3>
                    <p class="step-description">{t['step3_desc']}</p>
                    <span class="step-time" style="background: #dbeafe; color: #1e40af;">{t['step3_time']}</span>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 4rem;">
                <img src="https://images.unsplash.com/{unsplash_demo}?w=1200&h=600&fit=crop" 
                     alt="VaultCaddy {bank_name}"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            </div>
        </div>
    </section>
    
    <section class="final-cta-section">
        <div class="container">
            <h2>{t['final_cta_title'].format(bank=bank_name)}</h2>
            <p>{t['final_cta_subtitle']}</p>
            <a href="https://vaultcaddy.com/{lang}/auth.html" class="cta-button">{t['final_cta_button']}</a>
            
            <div class="trust-badges">
                <div>✓ {t['accurate_label']}</div>
                <div>✓ {t['cheap_label']}/month</div>
                <div>✓ Cancel Anytime</div>
            </div>
        </div>
    </section>
</body>
</html>'''
    
    return html_content

def main():
    """主函数"""
    
    print("=" * 80)
    print("🌍 批量創建多語言銀行Landing Page")
    print("=" * 80)
    print()
    
    created_files = []
    
    for lang in ['en', 'ja', 'ko']:
        # 创建语言目录（如果不存在）
        lang_dir = Path(lang)
        lang_dir.mkdir(exist_ok=True)
        
        print(f"📁 創建 {lang.upper()} 語言頁面...")
        
        for bank_id, bank_info in BANKS.items():
            filename = f"{lang}/{bank_id}-bank-statement.html"
            html_content = generate_bank_page(bank_id, bank_info, lang)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_files.append(filename)
            print(f"  ✅ {filename}")
        
        print()
    
    print("=" * 80)
    print(f"✅ 成功創建 {len(created_files)} 個多語言銀行Landing Page!")
    print("=" * 80)
    print()
    
    print("創建的檔案:")
    for i, filename in enumerate(created_files, 1):
        print(f"  {i}. {filename}")
    
    print()
    print("📋 下一步:")
    print("  1. 為日文/韓文創建5個行業頁面")
    print("  2. 運行 python3 update_multilingual_sitemap.py 更新sitemap")
    print("  3. 提交到 Google Search Console")

if __name__ == '__main__':
    main()

