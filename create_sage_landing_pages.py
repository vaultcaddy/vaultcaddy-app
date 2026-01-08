#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建Sage Landing Pages - 价格优化版
基于Xero模板,强化价格优势（免费试用 + $2.88/月）
"""

# Sage页面配置 - 价格优化版
SAGE_PAGES = {
    'convert-bank-statement-to-sage': {
        'title': 'Convert Bank Statement to Sage | Free 20-Page Trial + From $2.88/month ⭐4.9/5 - VaultCaddy',
        'description': 'Convert PDF/CSV bank statements to Sage 50/Accounting format in 3 seconds. Free 20-page trial, no credit card. From $2.88/month (annual) or $5.59/month. 15x cheaper than competitors. 98% accuracy.',
        'keywords': 'convert bank statement to sage, sage 50 converter, sage accounting import, bank statement to sage csv, pdf to sage 50, cheap sage converter',
        'h1': 'Convert Bank Statements to<br><span class="highlight">Sage Format</span>',
        'subtitle': 'Instantly convert PDF/CSV bank statements to Sage 50 & Sage Accounting format.<br>Supporting all major banks in UK 🇬🇧, US 🇺🇸, and Canada 🇨🇦',
        'og_image': 'og-sage.jpg',
        'primary_color': '#00DC06',  # Sage Green
        'primary_dark': '#00B005',
        'secondary_color': '#6366f1',
        'software_name': 'Sage',
        'format_description': 'A perfectly formatted Sage CSV file with Date (DD/MM/YYYY), Type (BP/BR), Account Ref, Description, Debit, Credit, and Reference fields. Ready for instant import into Sage 50 or Sage Accounting.',
        'import_instructions': 'After downloading your converted CSV file from VaultCaddy: 1) Log into Sage, 2) Go to Bank → Import Transactions, 3) Select your bank account, 4) Upload the CSV file, 5) Sage will automatically process transactions.',
        'free_trial_text': 'Yes! You get a <strong>completely free 20-page trial</strong> with no credit card required. After the trial, choose the <strong>$2.88/month annual plan</strong> (save $313/year vs competitors) or the <strong>$5.59/month monthly plan</strong> for flexibility.',
        'countries': [
            {'code': '🇬🇧', 'name': 'United Kingdom', 'banks': [
                'Barclays', 'HSBC UK', 'Lloyds Bank', 'NatWest', 'Santander UK',
                'RBS', 'Halifax', 'Nationwide', 'TSB Bank', 'Metro Bank'
            ]},
            {'code': '🇺🇸', 'name': 'United States', 'banks': [
                'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank',
                'US Bank', 'Capital One', 'PNC Bank', 'TD Bank'
            ]},
            {'code': '🇨🇦', 'name': 'Canada', 'banks': [
                'RBC', 'TD Canada Trust', 'Scotiabank', 'BMO',
                'CIBC', 'Tangerine Bank'
            ]}
        ]
    },
    'convert-csv-to-sage': {
        'title': 'CSV to Sage Converter | Free 20-Page Trial | From $2.88/month - VaultCaddy',
        'description': 'Convert any CSV to Sage 50/Accounting format instantly. Free trial (20 pages, no credit card). Cheapest solution at $2.88/month annual or $5.59/month. Supports all banks worldwide.',
        'keywords': 'csv to sage, sage csv converter, bank csv to sage 50, csv to sage accounting, sage csv import, sage csv format',
        'h1': 'Convert CSV to<br><span class="highlight">Sage Format</span>',
        'subtitle': 'Convert any CSV bank statement to Sage 50 & Sage Accounting format in seconds.<br><strong style="color: #fbbf24;">Free 20-page trial, then just $2.88/month (annual) or $5.59/month!</strong>',
        'og_image': 'og-sage-csv.jpg',
        'primary_color': '#00DC06',
        'primary_dark': '#00B005',
        'secondary_color': '#6366f1',
        'software_name': 'Sage',
        'format_description': 'A Sage-compatible CSV with DD/MM/YYYY date format, Debit/Credit columns, BP/BR transaction types, and proper account references. Perfect for Sage 50 and Sage Accounting.',
        'import_instructions': 'Simply upload your CSV to VaultCaddy, download the Sage-formatted file, then import it into Sage using Bank → Import Transactions. Our format matches exactly what Sage expects.',
        'free_trial_text': '<strong>Absolutely!</strong> Process 20 pages completely free, no credit card needed. Then continue with our <strong>unbeatable pricing: $2.88/month (annual)</strong> - that\'s <strong>15x cheaper</strong> than competitors charging $29-39/month!',
        'countries': [
            {'code': '🇬🇧', 'name': 'United Kingdom', 'banks': [
                'Barclays', 'HSBC UK', 'Lloyds Bank', 'NatWest', 'Santander UK',
                'RBS', 'Halifax', 'Nationwide'
            ]},
            {'code': '🇺🇸', 'name': 'United States', 'banks': [
                'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank'
            ]}
        ]
    },
    'convert-pdf-to-sage': {
        'title': 'PDF to Sage Converter | Free Trial + 98% Accurate | $2.88/month - VaultCaddy',
        'description': 'Convert PDF bank statements to Sage 50/Accounting in 3 seconds. AI-powered OCR, 98% accuracy. Free 20-page trial + affordable pricing from $2.88/month (annual). 15x cheaper than competitors.',
        'keywords': 'pdf to sage, sage pdf converter, pdf bank statement to sage 50, pdf to sage accounting, sage ocr, convert pdf to sage csv',
        'h1': 'Convert PDF to<br><span class="highlight">Sage Format</span>',
        'subtitle': 'Convert PDF bank statements to Sage 50 & Sage Accounting format with AI-powered OCR.<br><strong style="color: #10b981;">98% accuracy • 3-second processing • From $2.88/month</strong>',
        'og_image': 'og-sage-pdf.jpg',
        'primary_color': '#00DC06',
        'primary_dark': '#00B005',
        'secondary_color': '#6366f1',
        'software_name': 'Sage',
        'format_description': 'Our AI extracts all transaction data from your PDF and outputs a perfectly formatted Sage CSV with DD/MM/YYYY dates, Debit/Credit columns, and transaction codes (BP/BR). No manual typing required.',
        'import_instructions': 'Upload your PDF bank statement to VaultCaddy, wait 3 seconds for AI processing, download the Sage CSV, then import directly into Sage 50 or Sage Accounting. It\'s that easy!',
        'free_trial_text': '<strong>Yes, completely free!</strong> Try our AI-powered PDF conversion with <strong>20 pages free</strong>. After that, enjoy the <strong>lowest prices in the market: $2.88/month (annual plan)</strong>. You save <strong>$313-433 per year</strong> compared to other tools!',
        'countries': [
            {'code': '🇬🇧', 'name': 'United Kingdom', 'banks': [
                'Barclays', 'HSBC UK', 'Lloyds Bank', 'NatWest', 'Santander UK',
                'RBS', 'Halifax', 'Nationwide', 'TSB Bank'
            ]},
            {'code': '🇺🇸', 'name': 'United States', 'banks': [
                'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank',
                'US Bank', 'Capital One'
            ]}
        ]
    }
}

def create_sage_page(filename, config):
    """创建单个Sage Landing Page - 价格优化版"""
    
    html = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Optimization - 价格强化版 -->
    <title>{config['title']}</title>
    <meta name="description" content="{config['description']}">
    <meta name="keywords" content="{config['keywords']}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://vaultcaddy.com/{filename}.html">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{config['title']}">
    <meta property="og:description" content="{config['description']}">
    <meta property="og:url" content="https://vaultcaddy.com/{filename}.html">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://vaultcaddy.com/assets/{config['og_image']}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Schema.org Structured Data - 价格信息 -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "VaultCaddy - Bank Statement to {config['software_name']} Converter",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "offers": {{
            "@type": "Offer",
            "price": "2.88",
            "priceCurrency": "USD",
            "priceValidUntil": "2027-12-31"
        }},
        "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "ratingCount": "500",
            "bestRating": "5",
            "worstRating": "1"
        }},
        "description": "{config['description']}"
    }}
    </script>
    
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-H6C6SNHKVR"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-H6C6SNHKVR');
    </script>
    
    <style>
        :root {{
            --primary: {config['primary_color']};  /* Sage Green */
            --primary-dark: {config['primary_dark']};
            --secondary: {config['secondary_color']};
            --success: #10b981;
            --warning: #f59e0b;
            --dark: #0f172a;
            --light: #f8fafc;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--dark);
            color: #1e293b;
            overflow-x: hidden;
        }}
        
        /* Hero Section - Full Screen with Price Badge */
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, {config['primary_color']} 0%, {config['primary_dark']} 50%, {config['secondary_color']} 100%);
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: moveBackground 20s linear infinite;
        }}
        
        @keyframes moveBackground {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(50px, 50px); }}
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* 💰 价格Badge - 最显眼位置 */
        .hero-badge-price {{
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: #1a202c;
            padding: 14px 32px;
            border-radius: 50px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 20px;
            font-size: 18px;
            box-shadow: 0 10px 30px rgba(251, 191, 36, 0.4);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .hero-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: 50px;
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: fadeInDown 0.8s ease-out;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .hero h1 {{
            font-size: clamp(36px, 6vw, 72px);
            font-weight: 900;
            color: white;
            margin-bottom: 24px;
            line-height: 1.1;
            animation: fadeInUp 1s ease-out;
        }}
        
        .hero h1 .highlight {{
            background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .hero p {{
            font-size: clamp(18px, 2.5vw, 24px);
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 30px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
            animation: fadeIn 1.2s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        /* Hero Stats - 添加价格统计 */
        .hero-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            max-width: 800px;
            margin: 40px auto;
            animation: fadeIn 1.4s ease-out;
        }}
        
        .stat {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .stat-number {{
            display: block;
            font-size: 2em;
            font-weight: 900;
            color: white;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            display: block;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.9);
        }}
        
        .stat.price-highlight {{
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            border-color: #fbbf24;
        }}
        
        .stat.price-highlight .stat-number,
        .stat.price-highlight .stat-label {{
            color: #1a202c;
        }}
        
        .rating {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 40px;
            animation: fadeIn 1.4s ease-out;
        }}
        
        .stars {{
            color: #fbbf24;
            font-size: 24px;
            display: flex;
            gap: 4px;
        }}
        
        .rating-text {{
            color: white;
            font-size: 16px;
            font-weight: 600;
        }}
        
        .cta-buttons {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 1.6s ease-out;
        }}
        
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 18px 40px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }}
        
        .cta-button.primary {{
            background: white;
            color: var(--primary);
        }}
        
        .cta-button.primary:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }}
        
        .cta-button.secondary {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid white;
            backdrop-filter: blur(10px);
        }}
        
        .cta-button.secondary:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-4px);
        }}
        
        /* Trust Badges - 价格对比 */
        .trust-badges {{
            margin-top: 40px;
            display: flex;
            gap: 30px;
            justify-content: center;
            flex-wrap: wrap;
            font-size: 16px;
            color: white;
            animation: fadeIn 1.8s ease-out;
        }}
        
        .trust-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .trust-item i {{
            color: #fbbf24;
        }}
        
        /* 💰 Pricing Comparison Section - 新增独立部分 */
        .pricing-comparison {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 100px 24px;
        }}
        
        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 60px auto 0;
        }}
        
        .pricing-card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            border: 3px solid #e2e8f0;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .pricing-card.competitor {{
            opacity: 0.7;
        }}
        
        .pricing-card.vaultcaddy {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border-color: #10b981;
            transform: scale(1.05);
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3);
        }}
        
        .best-value-badge {{
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: #fbbf24;
            color: #1a202c;
            padding: 8px 24px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
        }}
        
        .price {{
            font-size: 3em;
            font-weight: 900;
            margin: 20px 0 10px;
        }}
        
        .price-period {{
            opacity: 0.8;
            margin-bottom: 20px;
        }}
        
        .pricing-features {{
            text-align: left;
            margin-top: 30px;
        }}
        
        .pricing-features div {{
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .pricing-cta {{
            display: block;
            margin-top: 30px;
            background: white;
            color: #059669;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            transition: all 0.3s ease;
        }}
        
        .pricing-cta:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .savings-calculator {{
            margin-top: 60px;
            background: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .savings-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }}
        
        .savings-amount {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 25px;
            border-radius: 16px;
            font-size: 1.4em;
            font-weight: 700;
        }}
        
        /* Features Section - 添加价格特性 */
        .section {{
            padding: 100px 20px;
            background: white;
        }}
        
        .section.dark {{
            background: var(--dark);
            color: white;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .section-title {{
            font-size: clamp(32px, 5vw, 48px);
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .section-subtitle {{
            text-align: center;
            font-size: 1.2em;
            color: #64748b;
            margin-bottom: 60px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .section-title .highlight {{
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }}
        
        .feature-card {{
            background: var(--light);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .section.dark .feature-card {{
            background: #1e293b;
        }}
        
        .feature-card:hover {{
            transform: translateY(-8px);
            border-color: var(--primary);
            box-shadow: 0 20px 60px rgba(0, 220, 6, 0.2);
        }}
        
        .feature-icon {{
            width: 80px;
            height: 80px;
            margin: 0 auto 24px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            color: white;
        }}
        
        .feature-card h3 {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 16px;
        }}
        
        .feature-card p {{
            font-size: 16px;
            line-height: 1.6;
            color: #64748b;
        }}
        
        .section.dark .feature-card p {{
            color: #94a3b8;
        }}
        
        /* How It Works */
        .how-it-works {{
            background: var(--light);
        }}
        
        .steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }}
        
        .step {{
            text-align: center;
            position: relative;
        }}
        
        .step-number {{
            width: 70px;
            height: 70px;
            margin: 0 auto 24px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: 900;
            color: white;
        }}
        
        .step h3 {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 12px;
        }}
        
        .step p {{
            font-size: 16px;
            color: #64748b;
            line-height: 1.6;
        }}
        
        /* Demo Section */
        .demo-section {{
            padding: 100px 20px;
            background: white;
            text-align: center;
        }}
        
        .demo-video {{
            max-width: 900px;
            margin: 40px auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }}
        
        .demo-video img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        /* Supported Banks */
        .banks-section {{
            background: var(--dark);
            color: white;
            padding: 100px 20px;
        }}
        
        .banks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
        
        .bank-card {{
            background: #1e293b;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .bank-card:hover {{
            border-color: var(--primary);
            transform: translateY(-4px);
        }}
        
        .bank-flag {{
            font-size: 28px;
            margin-right: 8px;
        }}
        
        /* FAQ Section - 包含价格问题 */
        .faq-section {{
            background: white;
            padding: 100px 20px;
        }}
        
        .faq-list {{
            max-width: 900px;
            margin: 60px auto 0;
        }}
        
        .faq-item {{
            background: var(--light);
            border-radius: 16px;
            margin-bottom: 20px;
            overflow: hidden;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .faq-item:hover {{
            border-color: var(--primary);
        }}
        
        .faq-question {{
            padding: 28px;
            font-size: 19px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .faq-answer {{
            padding: 0 28px 28px;
            font-size: 16px;
            line-height: 1.8;
            color: #4a5568;
            display: none;
        }}
        
        .faq-answer ul {{
            margin: 15px 0;
            padding-left: 25px;
        }}
        
        .faq-answer li {{
            margin-bottom: 10px;
        }}
        
        .faq-item.active .faq-answer {{
            display: block;
        }}
        
        .faq-icon {{
            transition: transform 0.3s ease;
        }}
        
        .faq-item.active .faq-icon {{
            transform: rotate(180deg);
        }}
        
        /* CTA Section - 强化价格 */
        .final-cta {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 100px 20px;
            text-align: center;
        }}
        
        .final-cta h2 {{
            font-size: clamp(32px, 5vw, 52px);
            font-weight: 900;
            margin-bottom: 20px;
        }}
        
        .final-cta p {{
            font-size: 20px;
            margin-bottom: 30px;
            opacity: 0.95;
        }}
        
        .price-reminder {{
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            margin: 40px auto;
            max-width: 600px;
        }}
        
        .price-comparison-cta {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 30px;
        }}
        
        .old-price {{
            text-decoration: line-through;
            opacity: 0.7;
            font-size: 1.2em;
        }}
        
        .new-price {{
            font-size: 2.5em;
            font-weight: 900;
            color: #fbbf24;
        }}
        
        /* Footer */
        footer {{
            background: var(--dark);
            color: white;
            padding: 60px 20px 30px;
            text-align: center;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .footer-links a {{
            color: white;
            text-decoration: none;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }}
        
        .footer-links a:hover {{
            opacity: 1;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 36px;
            }}
            
            .hero p {{
                font-size: 18px;
            }}
            
            .hero-stats {{
                grid-template-columns: 1fr 1fr;
            }}
            
            .cta-buttons {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .cta-button {{
                width: 100%;
                justify-content: center;
            }}
            
            .section {{
                padding: 60px 20px;
            }}
            
            .features-grid,
            .steps {{
                grid-template-columns: 1fr;
            }}
            
            .pricing-grid {{
                grid-template-columns: 1fr;
            }}
            
            .pricing-card.vaultcaddy {{
                transform: scale(1);
            }}
            
            .savings-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section - 价格优化版 -->
    <section class="hero">
        <div class="hero-content">
            <!-- 💰 价格Badge - 最显眼位置 -->
            <div class="hero-badge-price">
                💰 FREE 20-Page Trial • From $2.88/month (15x Cheaper!)
            </div>
            
            <div class="hero-badge">
                <i class="fas fa-bolt"></i> AI-Powered OCR Technology
            </div>
            
            <h1>
                {config['h1']}
            </h1>
            
            <p>
                {config['subtitle']}
            </p>
            
            <!-- Hero Stats - 包含价格 -->
            <div class="hero-stats">
                <div class="stat">
                    <span class="stat-number">3s</span>
                    <span class="stat-label">Processing Time</span>
                </div>
                <div class="stat">
                    <span class="stat-number">98%</span>
                    <span class="stat-label">Accuracy</span>
                </div>
                <div class="stat">
                    <span class="stat-number">100+</span>
                    <span class="stat-label">Banks Supported</span>
                </div>
                <div class="stat price-highlight">
                    <span class="stat-number">$2.88</span>
                    <span class="stat-label">Per Month (Annual)</span>
                </div>
            </div>
            
            <div class="rating">
                <div class="stars">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star-half-alt"></i>
                </div>
                <span class="rating-text">4.9/5 from 500+ users</span>
            </div>
            
            <div class="cta-buttons">
                <a href="/firstproject.html" class="cta-button primary">
                    <i class="fas fa-rocket"></i>
                    Start FREE Trial - 20 Pages (No Card)
                </a>
                <a href="#how-it-works" class="cta-button secondary">
                    <i class="fas fa-play-circle"></i>
                    See How It Works
                </a>
            </div>
            
            <!-- Trust Badges - 价格对比 -->
            <div class="trust-badges">
                <div class="trust-item">
                    <i class="fas fa-check-circle"></i>
                    <span>No Credit Card Required</span>
                </div>
                <div class="trust-item">
                    <i class="fas fa-shield-alt"></i>
                    <span>Bank-Level Security</span>
                </div>
                <div class="trust-item">
                    <i class="fas fa-tag"></i>
                    <span><strong>15x Cheaper</strong> than Competitors</span>
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加Pricing Comparison Section
    html += '''
    
    <!-- 💰 Pricing Comparison Section - 独立突出显示 -->
    <section class="pricing-comparison">
        <div class="container">
            <h2 class="section-title" style="color: #1a202c;">
                💰 Unbeatable <span class="highlight">Pricing</span>
            </h2>
            <p class="section-subtitle">
                Why pay 10-15x more? Get enterprise-grade features at a fraction of the cost.
            </p>
            
            <div class="pricing-grid">
                <!-- Competitor 1 -->
                <div class="pricing-card competitor">
                    <div style="font-size: 1.3em; font-weight: 600; color: #4a5568; margin-bottom: 10px;">Competitor A</div>
                    <div class="price" style="color: #ef4444;">$39</div>
                    <div class="price-period" style="color: #718096;">per month</div>
                    <div class="pricing-features">
                        <div style="color: #4a5568;">❌ No free trial</div>
                        <div style="color: #4a5568;">❌ Limited features</div>
                        <div style="color: #4a5568;">❌ Slow processing</div>
                    </div>
                </div>
                
                <!-- Competitor 2 -->
                <div class="pricing-card competitor">
                    <div style="font-size: 1.3em; font-weight: 600; color: #4a5568; margin-bottom: 10px;">Competitor B</div>
                    <div class="price" style="color: #ef4444;">$29</div>
                    <div class="price-period" style="color: #718096;">per month</div>
                    <div class="pricing-features">
                        <div style="color: #4a5568;">❌ 10-page limit</div>
                        <div style="color: #4a5568;">❌ Manual corrections needed</div>
                        <div style="color: #4a5568;">❌ Basic support only</div>
                    </div>
                </div>
                
                <!-- VaultCaddy - Highlighted -->
                <div class="pricing-card vaultcaddy">
                    <div class="best-value-badge">
                        ⭐ BEST VALUE
                    </div>
                    <div style="font-size: 1.3em; font-weight: 600; margin-bottom: 10px; margin-top: 10px;">VaultCaddy</div>
                    <div class="price">$2.88</div>
                    <div class="price-period">per month (annual)</div>
                    <div style="opacity: 0.9; font-size: 0.95em; margin-bottom: 20px;">or $5.59/month (monthly)</div>
                    <div class="pricing-features">
                        <div>✅ <strong>FREE 20-page trial</strong></div>
                        <div>✅ 98% AI accuracy</div>
                        <div>✅ 3-second processing</div>
                        <div>✅ 100+ banks supported</div>
                        <div>✅ Priority support included</div>
                        <div>✅ Unlimited conversions</div>
                    </div>
                    <a href="/firstproject.html" class="pricing-cta">
                        Start Free Trial →
                    </a>
                </div>
            </div>
            
            <!-- Savings Calculator -->
            <div class="savings-calculator">
                <h3 style="font-size: 2em; margin-bottom: 20px; color: #1a202c;">💡 Annual Savings</h3>
                <div class="savings-grid">
                    <div style="text-align: center;">
                        <div style="color: #718096; margin-bottom: 10px; font-size: 1.1em;">Other Tools</div>
                        <div style="font-size: 2.5em; font-weight: 700; color: #ef4444;">$348-468</div>
                        <div style="color: #718096;">/year</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #718096; margin-bottom: 10px; font-size: 1.1em;">VaultCaddy</div>
                        <div style="font-size: 2.5em; font-weight: 700; color: #10b981;">$34.62</div>
                        <div style="color: #718096;">/year</div>
                    </div>
                </div>
                <div class="savings-amount">
                    🎉 You Save $313-433 Per Year!
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加Features Section (包含价格特性)
    html += f'''
    
    <!-- Features Section - 包含价格特性 -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">
                Why Choose <span class="highlight">VaultCaddy</span> for {config['software_name']}?
            </h2>
            <p class="section-subtitle">
                The most affordable, accurate, and fastest bank statement converter in the market
            </p>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>AI-Powered OCR</h3>
                    <p>Advanced AI technology extracts data with 98% accuracy from any bank statement format - PDF, scanned images, or photos</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3>Instant 3s Conversion</h3>
                    <p>Convert bank statements to {config['software_name']} CSV format in just 3 seconds, not hours. Save time, reduce errors</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3>100% Secure</h3>
                    <p>Your data is encrypted with 256-bit SSL and automatically deleted after 24 hours. We never store your financial information</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon" style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);">
                        <i class="fas fa-tag"></i>
                    </div>
                    <h3>Unbeatable Price</h3>
                    <p><strong>$2.88/month</strong> (annual) or $5.59/month. <strong>15x cheaper</strong> than competitors. Free 20-page trial, no credit card required!</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-check-double"></i>
                    </div>
                    <h3>{config['software_name']} Compatible</h3>
                    <p>Perfect format for direct import into {config['software_name']} with DD/MM/YYYY dates, Debit/Credit columns, and BP/BR codes</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-file-alt"></i>
                    </div>
                    <h3>Multi-Page & Batch</h3>
                    <p>Handle multi-page PDFs and batch process multiple statements effortlessly. Perfect for month-end reconciliation</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-gift"></i>
                    </div>
                    <h3>20-Page Free Trial</h3>
                    <p>Try it completely free with 20 pages, no credit card needed. See the quality before you pay anything</p>
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加How It Works
    html += f'''
    
    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works">
        <div class="container">
            <h2 class="section-title">
                How It <span class="highlight">Works</span>
            </h2>
            <p class="section-subtitle">
                Convert your bank statements to {config['software_name']} format in 4 simple steps
            </p>
            
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>📤 Upload Statement</h3>
                    <p>Upload your bank statement PDF, JPG, PNG, or existing CSV from any device or bank</p>
                </div>
                
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>🤖 AI Processing</h3>
                    <p>Our AI extracts all transaction data with 98% accuracy in just 3 seconds</p>
                </div>
                
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>📊 Download {config['software_name']} CSV</h3>
                    <p>Get your {config['software_name']}-compatible CSV file with perfect formatting</p>
                </div>
                
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>✅ Import to {config['software_name']}</h3>
                    <p>Import directly into {config['software_name']} and start reconciling immediately</p>
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加Demo Section
    html += f'''
    
    <!-- Demo Section -->
    <section class="demo-section">
        <div class="container">
            <h2 class="section-title">
                See It In <span class="highlight">Action</span>
            </h2>
            <p class="section-subtitle">
                Watch how VaultCaddy converts a bank statement to {config['software_name']} format in 3 seconds
            </p>
            
            <div class="demo-video">
                <img src="video/chase-bank-demo.gif" alt="VaultCaddy Demo - Convert Bank Statement to {config['software_name']}" loading="lazy">
            </div>
            
            <div style="max-width: 900px; margin: 40px auto 0; text-align: left; background: var(--light); padding: 40px; border-radius: 20px;">
                <h3 style="font-size: 1.8em; margin-bottom: 20px; color: #1a202c;">📋 What You'll Get:</h3>
                <p style="font-size: 16px; color: #4a5568; line-height: 1.8; margin-bottom: 20px;">
                    {config['format_description']}
                </p>
                <div style="background: white; padding: 20px; border-radius: 12px; border-left: 4px solid var(--primary);">
                    <strong style="color: var(--primary);">✓ {config['software_name']} CSV Format Includes:</strong>
                    <ul style="margin-top: 15px; color: #4a5568; line-height: 1.8;">
                        <li>Date (DD/MM/YYYY format)</li>
                        <li>Type (BP for payments, BR for receipts)</li>
                        <li>Account Reference</li>
                        <li>Description</li>
                        <li>Debit and Credit columns</li>
                        <li>Reference numbers</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加Supported Banks
    banks_html = '''
    
    <!-- Supported Banks Section -->
    <section class="banks-section">
        <div class="container">
            <h2 class="section-title">
                Supported <span class="highlight">Banks</span>
            </h2>
            <p class="section-subtitle" style="color: rgba(255,255,255,0.9);">
                Works with 100+ banks worldwide. Upload any bank statement format!
            </p>'''
    
    for country in config['countries']:
        banks_html += f'''
            
            <h3 style="font-size: 28px; margin: 60px 0 30px; opacity: 0.95;">{country['code']} {country['name']}</h3>
            <div class="banks-grid">'''
        
        for bank in country['banks']:
            banks_html += f'''
                <div class="bank-card"><span class="bank-flag">{country['code']}</span> {bank}</div>'''
        
        banks_html += '''
            </div>'''
    
    banks_html += '''
        </div>
    </section>'''
    
    html += banks_html
    
    # 添加FAQ Section (包含价格问题)
    html += f'''
    
    <!-- FAQ Section - 包含价格问题 -->
    <section class="faq-section">
        <div class="container">
            <h2 class="section-title">
                Frequently Asked <span class="highlight">Questions</span>
            </h2>
            
            <div class="faq-list">
                <div class="faq-item">
                    <div class="faq-question">
                        <span>💰 How much does it cost?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            We offer the <strong>most affordable pricing</strong> in the market:
                        </p>
                        <ul>
                            <li>✅ <strong>FREE Trial</strong>: 20 pages, no credit card required</li>
                            <li>✅ <strong>Annual Plan</strong>: $2.88/month (billed $34.62/year) - BEST VALUE</li>
                            <li>✅ <strong>Monthly Plan</strong>: $5.59/month (cancel anytime)</li>
                        </ul>
                        <p>
                            <strong>Compare:</strong> Other tools charge $29-$39/month. 
                            You save <strong>$313-433 per year</strong> with VaultCaddy!
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>🎁 Is there a free trial?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            {config['free_trial_text']}
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>🤔 Why is VaultCaddy so much cheaper?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            We believe <strong>powerful tools should be affordable</strong> for everyone. By using:
                        </p>
                        <ul>
                            <li>✅ Advanced AI technology (more efficient)</li>
                            <li>✅ Cloud infrastructure (lower costs)</li>
                            <li>✅ Direct-to-user model (no middlemen)</li>
                            <li>✅ High volume automation</li>
                        </ul>
                        <p>
                            We can offer <strong>better quality at 10-15x lower prices</strong> than competitors. 
                            Our mission is to make professional accounting tools accessible to every business.
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>📄 What is {config['software_name']} CSV format?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            {config['software_name']} CSV format is the standardized file format that {config['software_name']} accepts for importing bank transactions. 
                            It includes fields like Date (DD/MM/YYYY), Type (BP/BR), Account Ref, Description, Debit, Credit, and Reference. 
                            VaultCaddy automatically converts your bank statements to this exact format.
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>📥 How do I import the CSV file into {config['software_name']}?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            {config['import_instructions']}
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>📂 What file formats do you support?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            We support <strong>all common file formats</strong>:
                        </p>
                        <ul>
                            <li>✅ PDF (even scanned or password-protected)</li>
                            <li>✅ JPG/JPEG images</li>
                            <li>✅ PNG images</li>
                            <li>✅ CSV files (from other banks)</li>
                            <li>✅ Even photos taken with your phone!</li>
                        </ul>
                        <p>
                            Our AI can extract data from scanned PDFs, photos, and even handwritten bank statements with 98% accuracy.
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>🔒 Is my financial data secure?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            <strong>Absolutely!</strong> Security is our top priority:
                        </p>
                        <ul>
                            <li>✅ <strong>256-bit SSL encryption</strong> for all data transmission</li>
                            <li>✅ <strong>Automatic deletion</strong> after 24 hours</li>
                            <li>✅ <strong>No permanent storage</strong> of your financial data</li>
                            <li>✅ <strong>GDPR compliant</strong></li>
                            <li>✅ <strong>No sharing</strong> with third parties</li>
                        </ul>
                        <p>
                            Your privacy is guaranteed. We process your files and automatically delete them. We never store or share your financial information.
                        </p>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>📦 Can I process multiple statements at once?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            <strong>Yes!</strong> VaultCaddy supports <strong>batch processing</strong>. You can:
                        </p>
                        <ul>
                            <li>✅ Upload multiple bank statement PDFs at once</li>
                            <li>✅ Process multi-page PDFs automatically</li>
                            <li>✅ Convert them all to {config['software_name']} format in one go</li>
                            <li>✅ Perfect for catching up on months of bank reconciliation</li>
                        </ul>
                    </div>
                </div>
                
                <div class="faq-item">
                    <div class="faq-question">
                        <span>⚡ How long does the conversion take?</span>
                        <i class="fas fa-chevron-down faq-icon"></i>
                    </div>
                    <div class="faq-answer">
                        <p>
                            Our AI processes bank statements in <strong>approximately 3 seconds per page</strong>. 
                            A typical 5-page bank statement takes only <strong>15 seconds</strong> from upload to download. 
                            That's <strong>10x faster</strong> than manual data entry!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>'''
    
    # 添加Final CTA (强化价格)
    html += f'''
    
    <!-- Final CTA - 价格强化版 -->
    <section class="final-cta">
        <div class="container">
            <!-- 价格提醒Badge -->
            <div class="price-reminder">
                <div style="font-size: 1.2em; margin-bottom: 20px; opacity: 0.95;">
                    💎 Limited Time Offer
                </div>
                <div class="price-comparison-cta">
                    <div>
                        <div style="font-size: 0.9em; opacity: 0.8; margin-bottom: 5px;">Other Tools</div>
                        <div class="old-price">$29-39/month</div>
                    </div>
                    <div style="font-size: 2em; opacity: 0.7;">→</div>
                    <div>
                        <div style="font-size: 0.9em; opacity: 0.8; margin-bottom: 5px;">VaultCaddy</div>
                        <div class="new-price">$2.88/month</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">(or $5.59/month monthly)</div>
                    </div>
                </div>
                <div style="font-size: 1.3em; font-weight: 700; margin-top: 20px;">
                    🎉 Save $313-433 Per Year!
                </div>
            </div>
            
            <h2>Ready to Convert Your Bank Statements to {config['software_name']}?</h2>
            <p>
                Join 10,000+ accountants and businesses using VaultCaddy.<br>
                <strong style="font-size: 1.3em; color: #fbbf24;">Start FREE trial now - no credit card required!</strong>
            </p>
            
            <a href="/firstproject.html" class="cta-button primary" style="margin: 40px auto 30px; display: inline-flex;">
                <i class="fas fa-rocket"></i>
                Start FREE Trial - 20 Pages
            </a>
            
            <p style="font-size: 16px; opacity: 0.9;">
                <i class="fas fa-check-circle"></i> No credit card required • 
                <i class="fas fa-check-circle"></i> 20 pages free • 
                <i class="fas fa-check-circle"></i> Cancel anytime • 
                <i class="fas fa-check-circle"></i> 98% accuracy guaranteed
            </p>
        </div>
    </section>'''
    
    # 添加Footer
    html += '''
    
    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/firstproject.html">Features</a>
                <a href="/pricing.html">Pricing</a>
                <a href="/convert-bank-statement-to-qbo.html">QBO Converter</a>
                <a href="/convert-bank-statement-to-xero.html">Xero Converter</a>
                <a href="/privacy-policy.html">Privacy Policy</a>
                <a href="/terms-of-service.html">Terms of Service</a>
            </div>
            
            <p style="opacity: 0.6; font-size: 14px; margin-top: 30px;">
                © 2026 VaultCaddy. All rights reserved.
            </p>
        </div>
    </footer>'''
    
    # 添加JavaScript
    html += '''
    
    <script>
        // FAQ Toggle
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', () => {
                const faqItem = question.parentElement;
                const isActive = faqItem.classList.contains('active');
                
                // Close all other FAQs
                document.querySelectorAll('.faq-item').forEach(item => {
                    item.classList.remove('active');
                });
                
                // Toggle current FAQ
                if (!isActive) {
                    faqItem.classList.add('active');
                }
            });
        });
        
        // Smooth Scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Track CTA clicks
        document.querySelectorAll('a[href="/firstproject.html"]').forEach(button => {
            button.addEventListener('click', function() {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        'event_category': 'CTA',
                        'event_label': 'Sage Converter - Start Trial',
                        'value': 1
                    });
                }
            });
        });
    </script>
</body>
</html>'''
    
    return html

def main():
    """批量创建所有Sage页面"""
    print("🚀 开始创建Sage Landing Pages - 价格优化版...")
    print(f"共需创建 {len(SAGE_PAGES)} 个页面\n")
    
    for filename, config in SAGE_PAGES.items():
        print(f"📝 创建: {filename}.html")
        html_content = create_sage_page(filename, config)
        
        with open(f"{filename}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ 完成: {filename}.html")
        print(f"   📊 Title: {config['title'][:80]}...")
        print()
    
    print("\n🎉 所有Sage页面创建完成!")
    print("\n📋 创建的页面列表:")
    for filename in SAGE_PAGES.keys():
        print(f"   ✅ {filename}.html")
    
    print("\n🔗 下一步操作:")
    print("   1. 测试所有页面是否正常显示")
    print("   2. 验证Sage CSV导出功能")
    print("   3. 提交到Google Search Console")
    print("   4. 添加到sitemap.xml")
    print("   5. 从首页和其他页面添加内部链接")

if __name__ == "__main__":
    main()

