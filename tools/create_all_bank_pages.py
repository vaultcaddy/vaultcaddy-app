#!/usr/bin/env python3
"""
批量创建所有银行Landing Page
作用: 一键生成10个香港主要银行的完整Landing Page
特点: 包含SEO优化、4大核心卖点、FAQ、使用免费图片
"""

import os
from pathlib import Path

# 银行配置
BANKS = {
    'hsbc': {
        'name_zh': '匯豐銀行',
        'name_en': 'HSBC',
        'color': '#DB0011',
        'color_dark': '#8B0008',
        'description': '匯豐銀行是香港最大的銀行，服務超過200萬客戶',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',  # 金融背景
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'  # 数据分析
    },
    'hangseng': {
        'name_zh': '恆生銀行',
        'name_en': 'Hang Seng',
        'color': '#00857D',
        'color_dark': '#005550',
        'description': '恆生銀行是香港領先的商業銀行，以卓越服務聞名',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bochk': {
        'name_zh': '中國銀行(香港)',
        'name_en': 'BOC Hong Kong',
        'color': '#CC092F',
        'color_dark': '#8B0620',
        'description': '中國銀行(香港)是香港三大發鈔銀行之一',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'sc': {
        'name_zh': '渣打銀行',
        'name_en': 'Standard Chartered',
        'color': '#00843D',
        'color_dark': '#00562A',
        'description': '渣打銀行是香港歷史最悠久的銀行之一',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'dbs': {
        'name_zh': '星展銀行',
        'name_en': 'DBS',
        'color': '#D0262D',
        'color_dark': '#8B1A1E',
        'description': '星展銀行是亞洲領先的金融服務集團',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bea': {
        'name_zh': '東亞銀行',
        'name_en': 'Bank of East Asia',
        'color': '#007A33',
        'color_dark': '#005122',
        'description': '東亞銀行是香港最大的獨立本地銀行',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'citibank': {
        'name_zh': '花旗銀行',
        'name_en': 'Citibank',
        'color': '#0072CE',
        'color_dark': '#004C8A',
        'description': '花旗銀行是全球領先的國際銀行',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'dahsing': {
        'name_zh': '大新銀行',
        'name_en': 'Dah Sing Bank',
        'color': '#003A70',
        'color_dark': '#00264C',
        'description': '大新銀行是香港主要商業銀行之一',
        'unsplash_bg': 'photo-1554224155-6726b3ff858f',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    },
    'citic': {
        'name_zh': '中信銀行國際',
        'name_en': 'CITIC Bank',
        'color': '#C8102E',
        'color_dark': '#870B1F',
        'description': '中信銀行國際是中國中信集團成員',
        'unsplash_bg': 'photo-1563013544-824ae1b704d3',
        'unsplash_demo': 'photo-1551288049-bebda4e38f71'
    },
    'bankcomm': {
        'name_zh': '交通銀行',
        'name_en': 'Bank of Communications',
        'color': '#004B8D',
        'color_dark': '#00325E',
        'description': '交通銀行是中國五大國有銀行之一',
        'unsplash_bg': 'photo-1565372195458-9de0b320ef04',
        'unsplash_demo': 'photo-1460925895917-afdab827c52f'
    }
}

def generate_bank_page(bank_id, bank_info):
    """生成单个银行的Landing Page"""
    
    name_zh = bank_info['name_zh']
    name_en = bank_info['name_en']
    color = bank_info['color']
    color_dark = bank_info['color_dark']
    description = bank_info['description']
    unsplash_bg = bank_info['unsplash_bg']
    unsplash_demo = bank_info['unsplash_demo']
    
    # 文件名
    filename = f"{bank_id}-bank-statement.html"
    
    # HTML内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <!-- 性能优化 - 预连接 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://images.unsplash.com">
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO优化 - 标题 -->
    <title>{name_zh}({name_en})對帳單AI處理 | 3秒轉QuickBooks | HK$46/月 | VaultCaddy香港</title>
    
    <!-- SEO优化 - 描述 -->
    <meta name="description" content="{name_zh}({name_en})對帳單AI自動處理，拍照即可上傳，3秒轉QuickBooks/Excel，98%準確率，HK$46/月起。支援PDF和手機拍照，香港會計師推薦。免費試用20頁。">
    
    <!-- SEO优化 - 关键词 -->
    <meta name="keywords" content="{name_zh}對帳單,{name_en} bank statement,{name_zh}QuickBooks,{name_en}對帳單轉Excel,{name_zh}AI處理,{name_en} PDF轉換,香港銀行對帳單">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://vaultcaddy.com/{filename}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{name_zh}({name_en})對帳單AI處理 | 3秒轉QuickBooks | HK$46/月">
    <meta property="og:description" content="拍照即可上傳，3秒處理，98%準確率，HK$46/月起。支援所有{name_en}帳戶類型。">
    <meta property="og:url" content="https://vaultcaddy.com/{filename}">
    <meta property="og:type" content="website">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="alternate icon" type="image/png" href="favicon.png">
    
    <!-- 结构化数据 - SoftwareApplication -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "VaultCaddy - {name_zh}對帳單AI處理",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Web, iOS, Android",
      "offers": {{
        "@type": "Offer",
        "price": "46",
        "priceCurrency": "HKD",
        "priceValidUntil": "2026-12-31"
      }},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "15",
        "bestRating": "5",
        "worstRating": "1"
      }},
      "description": "{name_zh}對帳單AI自動處理，3秒轉QuickBooks/Excel，98%準確率"
    }}
    </script>
    
    <!-- 结构化数据 - FAQ -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "如何從{name_zh}網上銀行下載對帳單？",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "登入{name_zh}網上銀行 → 選擇賬戶 → 電子結單 → 選擇月份 → 下載PDF。PDF檔案可直接上傳到VaultCaddy，3秒完成處理。"
          }}
        }},
        {{
          "@type": "Question",
          "name": "VaultCaddy支援{name_zh}所有帳戶類型嗎？",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "是的，我們支援{name_zh}的商業帳戶、個人儲蓄帳戶、綜合帳戶、信用卡對帳單等所有類型。"
          }}
        }},
        {{
          "@type": "Question",
          "name": "處理{name_zh}對帳單需要多少費用？",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "年付方案HK$46/月，包含100頁免費處理。月付方案HK$58/月。超出後每頁HK$0.5。新用戶免費試用20頁。"
          }}
        }}
      ]
    }}
    </script>
    
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
        
        /* 优惠横幅 */
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
        
        /* Hero Section */
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
            width: 120px;
            height: auto;
            margin-bottom: 1.5rem;
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
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
        
        /* 4大核心卖点 */
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
        }}
        
        .trust-badge {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* 功能说明 */
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
            transition: transform 0.3s;
        }}
        
        .step-card:hover {{
            transform: translateY(-5px);
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
            color: #1f2937;
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
            font-weight: 300;
        }}
        
        /* FAQ */
        .faq-section {{
            padding: 5rem 0;
            background: #f9fafb;
        }}
        
        .faq-grid {{
            display: grid;
            gap: 1.5rem;
            margin-top: 3rem;
        }}
        
        .faq-item {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .faq-item h3 {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 1rem;
        }}
        
        .faq-item p, .faq-item ul, .faq-item ol {{
            color: #4b5563;
            line-height: 1.8;
        }}
        
        .faq-item ul, .faq-item ol {{
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }}
        
        .faq-item li {{
            margin-bottom: 0.5rem;
        }}
        
        /* Final CTA */
        .final-cta-section {{
            padding: 5rem 0;
            background: linear-gradient(135deg, {color} 0%, {color_dark} 100%);
            color: white;
            text-align: center;
        }}
        
        .final-cta-section h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .final-cta-section p {{
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.95;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 1.8rem;
            }}
            
            .hero-subtitle {{
                font-size: 1.1rem;
            }}
            
            .core-benefits {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .steps-container {{
                grid-template-columns: 1fr;
            }}
            
            .arrow {{
                transform: rotate(90deg);
            }}
        }}
    </style>
</head>
<body>
    <!-- 优惠横幅 -->
    <div class="promo-banner">
        🎁 限時優惠：首月8折！使用優惠碼 <span class="promo-code">SAVE20</span>
    </div>
    
    <!-- Hero Section -->
    <section class="hero">
        <!-- 背景图片：使用Unsplash免费图片 -->
        <img src="https://images.unsplash.com/{unsplash_bg}?w=1920&h=800&fit=crop" 
             alt="{name_zh} Banking Background" 
             class="hero-background"
             loading="eager">
        
        <div class="container hero-content">
            <!-- 银行Logo占位 -->
            <div class="bank-logo" style="display: inline-block;">
                <strong style="color: {color}; font-size: 1.8rem;">{name_en} {name_zh}</strong>
            </div>
            
            <h1>{name_zh}對帳單AI自動處理</h1>
            <p class="hero-subtitle">拍照即可上傳 · 3秒完成處理 · 98%準確率 · HK$46/月起</p>
            
            <!-- 4大核心卖点 -->
            <div class="core-benefits">
                <div class="benefit-card">
                    <span class="benefit-icon">📱</span>
                    <span class="benefit-number">簡單</span>
                    <div class="benefit-label">拍照上傳</div>
                    <div class="benefit-detail">手機即可</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">⚡</span>
                    <span class="benefit-number">3秒</span>
                    <div class="benefit-label">快速處理</div>
                    <div class="benefit-detail">vs 手動2小時</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">✓</span>
                    <span class="benefit-number">98%</span>
                    <div class="benefit-label">超高準確</div>
                    <div class="benefit-detail">vs 手動85%</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">💰</span>
                    <span class="benefit-number">$46</span>
                    <div class="benefit-label">極致平價</div>
                    <div class="benefit-detail">每月/100頁</div>
                </div>
            </div>
            
            <a href="https://vaultcaddy.com/auth.html" class="cta-button">免費試用20頁 →</a>
            
            <div class="trust-badges">
                <div class="trust-badge">✓ 無需信用卡</div>
                <div class="trust-badge">✓ 3秒看到效果</div>
                <div class="trust-badge">✓ 支援所有{name_en}帳戶</div>
            </div>
        </div>
    </section>
    
    <!-- 功能说明 -->
    <section class="features-section">
        <div class="container">
            <h2 class="section-title">3步驟完成{name_zh}對帳單處理</h2>
            <p class="section-subtitle">簡單到小學生都會用，快速到喝杯咖啡的時間都不用</p>
            
            <div class="steps-container">
                <!-- Step 1 -->
                <div class="step-card">
                    <div class="step-number">1</div>
                    <span class="step-icon">📄</span>
                    <h3 class="step-title">上傳{name_en}對帳單</h3>
                    <p class="step-description">
                        · 手機拍照即可<br>
                        · 或上傳PDF檔案<br>
                        · 支援多頁對帳單<br>
                        · 拖放即可上傳
                    </p>
                    <span class="step-time">30秒</span>
                </div>
                
                <div class="arrow">→</div>
                
                <!-- Step 2 -->
                <div class="step-card">
                    <div class="step-number">2</div>
                    <span class="step-icon">🤖</span>
                    <h3 class="step-title">AI自動識別</h3>
                    <p class="step-description">
                        · 自動識別{name_en}格式<br>
                        · 提取所有交易<br>
                        · 98%識別準確率<br>
                        · 自動分類交易
                    </p>
                    <span class="step-time" style="background: #fbbf24; color: #78350f;">3秒</span>
                </div>
                
                <div class="arrow">→</div>
                
                <!-- Step 3 -->
                <div class="step-card">
                    <div class="step-number">3</div>
                    <span class="step-icon">📊</span>
                    <h3 class="step-title">一鍵匯出</h3>
                    <p class="step-description">
                        · QuickBooks IIF文件<br>
                        · 或Excel/CSV格式<br>
                        · 可編輯後再匯出<br>
                        · 直接匯入會計軟件
                    </p>
                    <span class="step-time" style="background: #dbeafe; color: #1e40af;">5秒</span>
                </div>
            </div>
            
            <!-- 演示图片 -->
            <div style="text-align: center; margin-top: 4rem;">
                <img src="https://images.unsplash.com/{unsplash_demo}?w=1200&h=600&fit=crop" 
                     alt="VaultCaddy處理{name_zh}對帳單演示"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            </div>
        </div>
    </section>
    
    <!-- FAQ -->
    <section class="faq-section">
        <div class="container">
            <h2 class="section-title">{name_zh}對帳單處理常見問題</h2>
            <p class="section-subtitle">解答您關於{name_en}對帳單AI處理的所有疑問</p>
            
            <div class="faq-grid">
                <div class="faq-item">
                    <h3>1. 如何從{name_zh}網上銀行下載對帳單？</h3>
                    <p>登入{name_zh}網上銀行 → 選擇"賬戶" → "電子結單" → 選擇月份 → 點擊"下載PDF"。下載的PDF檔案可直接上傳到VaultCaddy，3秒完成處理。</p>
                </div>
                
                <div class="faq-item">
                    <h3>2. VaultCaddy支援{name_en}所有帳戶類型嗎？</h3>
                    <p>是的，我們支援{name_zh}的所有帳戶類型：</p>
                    <ul>
                        <li>✓ {name_en}商業帳戶</li>
                        <li>✓ {name_en}個人儲蓄帳戶</li>
                        <li>✓ {name_en}商業綜合帳戶</li>
                        <li>✓ {name_en}信用卡對帳單</li>
                    </ul>
                </div>
                
                <div class="faq-item">
                    <h3>3. 手機拍照的{name_zh}對帳單能處理嗎？</h3>
                    <p>完全可以！我們的拍照上傳功能專為此設計：</p>
                    <ul>
                        <li>✓ 用手機拍攝清晰照片即可</li>
                        <li>✓ 支援多頁拍照</li>
                        <li>✓ AI自動校正傾斜和模糊</li>
                        <li>✓ 識別率與PDF相同(98%)</li>
                    </ul>
                </div>
                
                <div class="faq-item">
                    <h3>4. 處理{name_zh}對帳單需要多少費用？</h3>
                    <p>定價靈活透明：</p>
                    <ul>
                        <li>🆓 <strong>免費試用</strong>: 20頁額度</li>
                        <li>💰 <strong>年付方案</strong>: HK$46/月(相當於HK$552/年)，包含100頁</li>
                        <li>💰 <strong>月付方案</strong>: HK$58/月，包含100頁</li>
                        <li>💼 超出後每頁HK$0.5</li>
                    </ul>
                    <p><em>註：1頁 = 1張{name_en}對帳單紙（不是交易數量）</em></p>
                </div>
                
                <div class="faq-item">
                    <h3>5. 處理一份{name_zh}對帳單真的只需要3秒嗎？</h3>
                    <p>是的！從上傳到完成處理，平均只需3秒：</p>
                    <ul>
                        <li>✓ 無論對帳單有多少頁</li>
                        <li>✓ 無論有多少筆交易</li>
                        <li>✓ 無論是PDF還是拍照</li>
                    </ul>
                    <p>這比手動輸入快1,200倍（手動平均需要60分鐘）。</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Final CTA -->
    <section class="final-cta-section">
        <div class="container">
            <h2>開始處理您的{name_zh}對帳單</h2>
            <p>免費試用20頁，無需信用卡，3秒看到效果</p>
            <a href="https://vaultcaddy.com/auth.html" class="cta-button">立即免費試用 →</a>
            
            <div class="trust-badges">
                <div class="trust-badge">✓ 98%準確率</div>
                <div class="trust-badge">✓ HK$46/月起</div>
                <div class="trust-badge">✓ 隨時取消</div>
            </div>
        </div>
    </section>
    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'YOUR-GA-ID');
    </script>
</body>
</html>'''
    
    return filename, html_content

def main():
    """主函数"""
    
    print("=" * 80)
    print("🏦 批量創建所有銀行Landing Page")
    print("=" * 80)
    print()
    
    print(f"準備創建 {len(BANKS)} 個銀行頁面...")
    print()
    
    created_files = []
    
    for bank_id, bank_info in BANKS.items():
        filename, html_content = generate_bank_page(bank_id, bank_info)
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_files.append(filename)
        print(f"✅ 已創建: {filename} ({bank_info['name_zh']})")
    
    print()
    print("=" * 80)
    print(f"✅ 成功創建 {len(created_files)} 個銀行Landing Page!")
    print("=" * 80)
    print()
    
    print("創建的檔案:")
    for i, filename in enumerate(created_files, 1):
        print(f"  {i}. {filename}")
    
    print()
    print("📋 下一步:")
    print("  1. 運行 python3 create_sitemap.py 生成sitemap.xml")
    print("  2. 提交到 Google Search Console")
    print("  3. 使用 python3 submit_to_search_console.py 批量請求索引")

if __name__ == '__main__':
    main()

