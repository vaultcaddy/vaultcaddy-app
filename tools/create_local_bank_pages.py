#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为日文版和韩文版创建本地银行页面"""

# 日本银行配置
japanese_banks = [
    {
        'id': 'mufg',
        'name_ja': '三菱UFJ銀行',
        'name_en': 'MUFG',
        'description': '日本最大のメガバンク · 98%精度',
        'color': '#DC143C'
    },
    {
        'id': 'smbc',
        'name_ja': '三井住友銀行',
        'name_en': 'SMBC',
        'description': '日本2位の銀行',
        'color': '#00A040'
    },
    {
        'id': 'mizuho',
        'name_ja': 'みずほ銀行',
        'name_en': 'Mizuho',
        'description': '総合金融サービス',
        'color': '#0068B7'
    },
    {
        'id': 'resona',
        'name_ja': 'りそな銀行',
        'name_en': 'Resona',
        'description': '第五大銀行 · 多店舗展開',
        'color': '#E60012'
    },
    {
        'id': 'shinsei',
        'name_ja': '新生銀行',
        'name_en': 'Shinsei',
        'description': 'オンラインバンキング',
        'color': '#004B8D'
    }
]

# 韩国银行配置
korean_banks = [
    {
        'id': 'kb',
        'name_kr': 'KB국민은행',
        'name_en': 'KB Kookmin Bank',
        'description': '한국 최대 은행 · 98% 정확도',
        'color': '#FFBE00'
    },
    {
        'id': 'shinhan',
        'name_kr': '신한은행',
        'name_en': 'Shinhan Bank',
        'description': '한국 2위 은행',
        'color': '#0046FF'
    },
    {
        'id': 'hana',
        'name_kr': '하나은행',
        'name_en': 'Hana Bank',
        'description': '종합 금융 서비스',
        'color': '#008485'
    },
    {
        'id': 'woori',
        'name_kr': '우리은행',
        'name_en': 'Woori Bank',
        'description': '공공 은행 · 안정성',
        'color': '#0067AC'
    },
    {
        'id': 'nh',
        'name_kr': 'NH농협은행',
        'name_en': 'NH Bank',
        'description': '농협 금융 · 전국 네트워크',
        'color': '#007A33'
    }
]

def generate_japanese_bank_page(bank):
    """生成日文银行页面"""
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{bank['name_ja']}取引明細AI処理 | 写真アップロード ¥660/月 3秒完了 | VaultCaddy</title>
    <meta name="description" content="{bank['name_ja']}の取引明細をVaultCaddy AIで自動処理。年間わずか¥7,920、手動処理より95%節約。写真アップロードだけで、3秒で完了、98%の精度。Excel/QuickBooks/Xeroに出力可能。">
    <meta name="keywords" content="{bank['name_ja']} AI処理, {bank['name_ja']} 取引明細, 銀行明細AI, 会計自動化, QuickBooks連携, Xero連携, 日本 銀行明細処理">
    
    <link rel="canonical" href="https://vaultcaddy.com/jp/{bank['id']}-bank-statement.html">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
            line-height: 1.8;
            color: #1f2937;
            background: #f9fafb;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, {bank['color']} 0%, {bank['color']}dd 100%);
            color: white;
            padding: 5rem 0 3rem;
            text-align: center;
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
            opacity: 0.1;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        
        .bank-logo {{
            display: inline-block;
            margin-bottom: 2rem;
        }}
        
        .bank-logo strong {{
            font-size: 2rem;
            display: block;
            margin-bottom: 0.5rem;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            max-width: 1000px;
            margin: 3rem auto;
        }}
        
        .benefit-card {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 2rem 1.5rem;
            text-align: center;
        }}
        
        .benefit-icon {{
            font-size: 3rem;
            display: block;
            margin-bottom: 1rem;
        }}
        
        .benefit-number {{
            font-size: 2rem;
            font-weight: 800;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .benefit-label {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .benefit-detail {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: {bank['color']};
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 2rem;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        /* Content Sections */
        .content-section {{
            background: white;
            border-radius: 12px;
            padding: 3rem 2rem;
            margin: 3rem auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .content-section h2 {{
            font-size: 2rem;
            font-weight: 700;
            color: {bank['color']};
            margin-bottom: 2rem;
            border-left: 5px solid {bank['color']};
            padding-left: 1rem;
        }}
        
        .content-section h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1f2937;
            margin: 2rem 0 1rem;
        }}
        
        .content-section p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }}
        
        .content-section ul {{
            list-style: none;
            margin: 1.5rem 0;
        }}
        
        .content-section li {{
            padding: 0.75rem 0;
            padding-left: 2rem;
            position: relative;
            font-size: 1.05rem;
            color: #4b5563;
        }}
        
        .content-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: {bank['color']};
            font-weight: bold;
            font-size: 1.2rem;
        }}
        
        /* Final CTA */
        .final-cta {{
            background: linear-gradient(135deg, {bank['color']} 0%, {bank['color']}dd 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 12px;
            margin: 4rem auto;
        }}
        
        .final-cta h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: white;
            border: none;
            padding: 0;
        }}
        
        .final-cta p {{
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.95;
            color: white;
        }}
        
        .final-cta .cta-button {{
            background: white;
            color: {bank['color']};
            font-size: 1.3rem;
            padding: 1.25rem 3rem;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 1.75rem;
            }}
            
            .core-benefits {{
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }}
            
            .content-section {{
                padding: 2rem 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <img src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1920&h=800&fit=crop" 
             alt="{bank['name_ja']} Banking Background" 
             class="hero-background"
             loading="eager">
        
        <div class="container hero-content">
            <div class="bank-logo">
                <strong>{bank['name_ja']}</strong>
                <span style="font-size: 0.8em; opacity: 0.9;">{bank['name_en']}</span>
            </div>
            
            <h1>{bank['name_ja']}取引明細AI自動処理</h1>
            <p class="hero-subtitle">写真アップロードだけで · 3秒で完了 · 98%精度 · ¥660/月から</p>
            
            <!-- 4大核心卖点 -->
            <div class="core-benefits">
                <div class="benefit-card">
                    <span class="benefit-icon">📱</span>
                    <span class="benefit-number">簡単</span>
                    <div class="benefit-label">写真アップロード</div>
                    <div class="benefit-detail">スマホで完結</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">⚡</span>
                    <span class="benefit-number">3秒</span>
                    <div class="benefit-label">高速処理</div>
                    <div class="benefit-detail">vs 手動2時間</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">✓</span>
                    <span class="benefit-number">98%</span>
                    <div class="benefit-label">超高精度</div>
                    <div class="benefit-detail">vs 手動85%</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">💰</span>
                    <span class="benefit-number">¥660</span>
                    <div class="benefit-label">極限平価</div>
                    <div class="benefit-detail">月/100ページ</div>
                </div>
            </div>
            
            <a href="/jp/auth.html" class="cta-button">20ページ無料お試し · 3秒で効果を確認 →</a>
        </div>
    </section>
    
    <!-- 主要功能说明 -->
    <div class="container">
        <div class="content-section">
            <h2>🚀 VaultCaddyで{bank['name_ja']}取引明細を簡単処理</h2>
            
            <h3>写真アップロードだけで完了</h3>
            <p>{bank['name_ja']}の取引明細を受け取ったら、スマホで写真を撮ってアップロードするだけ。スキャナーもパソコンも不要です。通勤中やカフェでも、いつでもどこでも処理できます。</p>
            
            <ul>
                <li><strong>スマホで撮影</strong>：いつでもどこでも、取引明細を受け取ったらすぐに撮影してアップロード</li>
                <li><strong>スキャナー不要</strong>：高価なスキャン設備を購入する必要なし（¥30,000-80,000節約）</li>
                <li><strong>パソコン不要</strong>：スマホだけで完結、通勤時間でも処理可能</li>
                <li><strong>リアルタイム処理</strong>：アップロード後3秒で結果を表示、待ち時間なし</li>
                <li><strong>複数ページ自動結合</strong>：3ページの取引明細も自動認識・結合、手動作業不要</li>
            </ul>
            
            <h3>3秒で処理完了 - 手動処理の600倍高速</h3>
            <p>従来の手動処理では、1枚の取引明細を処理するのに30-48分かかりました。VaultCaddy AIなら、わずか3秒で完了します。</p>
            
            <ul>
                <li><strong>処理時間比較</strong>：VaultCaddy 3秒 vs 手動処理 30-48分 = <strong>600-960倍高速</strong></li>
                <li><strong>月間50枚処理</strong>：VaultCaddy 2.5分 vs 手動処理 25-40時間 = <strong>月間38時間節約</strong></li>
                <li><strong>年間600枚処理</strong>：VaultCaddy 30分 vs 手動処理 300-480時間 = <strong>年間450時間節約</strong></li>
            </ul>
            
            <h3>98%の精度 - 手動処理を13%上回る</h3>
            <p>業界調査によると、手動で取引明細を処理した場合の平均精度は85%に過ぎません。VaultCaddy AIの精度は98%で、手動処理を13%上回ります。</p>
            
            <ul>
                <li><strong>口座情報</strong>：99%（銀行名、口座番号、口座名義）</li>
                <li><strong>取引記録</strong>：98%（日付、説明、金額、残高）</li>
                <li><strong>金額認識</strong>：99.5%（小数点2桁まで）</li>
                <li><strong>自動照合</strong>：期首+取引=期末（自動検証）</li>
            </ul>
            
            <h3>年間わずか¥7,920 - 手動処理より95%節約</h3>
            <p><strong>VaultCaddy料金</strong>：</p>
            <ul>
                <li>月額：¥660/月</li>
                <li>年額：¥7,920/年（<strong>約15%割引</strong>）</li>
                <li>超過料金：¥10/ページ（月間上限を超えた場合）</li>
            </ul>
            
            <p><strong>手動処理コスト</strong>：</p>
            <ul>
                <li>パートタイム経理：¥20,000-50,000/月 = <strong>¥240,000-600,000/年</strong></li>
                <li>フルタイム経理（配分20%）：¥36,000-60,000/月 = <strong>¥432,000-720,000/年</strong></li>
            </ul>
            
            <p><strong>節約率</strong>：VaultCaddy vs 手動処理 = <strong>95-98.9%節約</strong></p>
            
            <h3>Excel/QuickBooks/Xeroにワンクリック出力</h3>
            <p>VaultCaddyは孤立したツールではなく、既存の会計フローとシームレスに連携します：</p>
            <ul>
                <li>✅ <strong>Excel形式CSV</strong>：汎用形式、すべての会計ソフトに対応</li>
                <li>✅ <strong>QuickBooks</strong>：QuickBooks Online/Desktopに直接インポート</li>
                <li>✅ <strong>Xero</strong>：Xero会計システムに直接インポート</li>
                <li>✅ <strong>カスタム形式</strong>：会計フローに応じてカスタマイズ</li>
            </ul>
        </div>
    </div>
    
    <!-- Final CTA -->
    <div class="container">
        <div class="final-cta">
            <h2>今日から年間¥450,000節約</h2>
            <p>20ページ無料お試し · 3秒で効果確認 · クレジットカード不要 · いつでもキャンセル可能</p>
            <a href="/jp/auth.html" class="cta-button">無料お試し →</a>
        </div>
    </div>
    
</body>
</html>
'''
    
    return html

def generate_korean_bank_page(bank):
    """生成韩文银行页面"""
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{bank['name_kr']} 명세서 AI 처리 | 사진 업로드 ₩9,900/월 3초 완료 | VaultCaddy</title>
    <meta name="description" content="{bank['name_kr']} 명세서를 VaultCaddy AI로 자동 처리. 연간 ₩118,800, 수동 처리보다 95% 절약. 사진 업로드만으로 3초 완료, 98% 정확도. Excel/QuickBooks/Xero로 출력 가능.">
    <meta name="keywords" content="{bank['name_kr']} AI 처리, {bank['name_kr']} 명세서, 은행 명세서 AI, 회계 자동화, QuickBooks 연동, Xero 연동, 한국 은행 명세서 처리">
    
    <link rel="canonical" href="https://vaultcaddy.com/kr/{bank['id']}-bank-statement.html">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
            line-height: 1.8;
            color: #1f2937;
            background: #f9fafb;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, {bank['color']} 0%, {bank['color']}dd 100%);
            color: white;
            padding: 5rem 0 3rem;
            text-align: center;
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
            opacity: 0.1;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        
        .bank-logo {{
            display: inline-block;
            margin-bottom: 2rem;
        }}
        
        .bank-logo strong {{
            font-size: 2rem;
            display: block;
            margin-bottom: 0.5rem;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            max-width: 1000px;
            margin: 3rem auto;
        }}
        
        .benefit-card {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 2rem 1.5rem;
            text-align: center;
        }}
        
        .benefit-icon {{
            font-size: 3rem;
            display: block;
            margin-bottom: 1rem;
        }}
        
        .benefit-number {{
            font-size: 2rem;
            font-weight: 800;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .benefit-label {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .benefit-detail {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: {bank['color']};
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 2rem;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        /* Content Sections */
        .content-section {{
            background: white;
            border-radius: 12px;
            padding: 3rem 2rem;
            margin: 3rem auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .content-section h2 {{
            font-size: 2rem;
            font-weight: 700;
            color: {bank['color']};
            margin-bottom: 2rem;
            border-left: 5px solid {bank['color']};
            padding-left: 1rem;
        }}
        
        .content-section h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1f2937;
            margin: 2rem 0 1rem;
        }}
        
        .content-section p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }}
        
        .content-section ul {{
            list-style: none;
            margin: 1.5rem 0;
        }}
        
        .content-section li {{
            padding: 0.75rem 0;
            padding-left: 2rem;
            position: relative;
            font-size: 1.05rem;
            color: #4b5563;
        }}
        
        .content-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: {bank['color']};
            font-weight: bold;
            font-size: 1.2rem;
        }}
        
        /* Final CTA */
        .final-cta {{
            background: linear-gradient(135deg, {bank['color']} 0%, {bank['color']}dd 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 12px;
            margin: 4rem auto;
        }}
        
        .final-cta h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: white;
            border: none;
            padding: 0;
        }}
        
        .final-cta p {{
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.95;
            color: white;
        }}
        
        .final-cta .cta-button {{
            background: white;
            color: {bank['color']};
            font-size: 1.3rem;
            padding: 1.25rem 3rem;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 1.75rem;
            }}
            
            .core-benefits {{
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }}
            
            .content-section {{
                padding: 2rem 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <img src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1920&h=800&fit=crop" 
             alt="{bank['name_kr']} Banking Background" 
             class="hero-background"
             loading="eager">
        
        <div class="container hero-content">
            <div class="bank-logo">
                <strong>{bank['name_kr']}</strong>
                <span style="font-size: 0.8em; opacity: 0.9;">{bank['name_en']}</span>
            </div>
            
            <h1>{bank['name_kr']} 명세서 AI 자동 처리</h1>
            <p class="hero-subtitle">사진 업로드만으로 · 3초 만에 완료 · 98% 정확도 · ₩9,900/월부터</p>
            
            <!-- 4大核心卖点 -->
            <div class="core-benefits">
                <div class="benefit-card">
                    <span class="benefit-icon">📱</span>
                    <span class="benefit-number">간단</span>
                    <div class="benefit-label">사진 업로드</div>
                    <div class="benefit-detail">스마트폰으로 완료</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">⚡</span>
                    <span class="benefit-number">3초</span>
                    <div class="benefit-label">고속 처리</div>
                    <div class="benefit-detail">vs 수동 2시간</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">✓</span>
                    <span class="benefit-number">98%</span>
                    <div class="benefit-label">초고정확도</div>
                    <div class="benefit-detail">vs 수동 85%</div>
                </div>
                
                <div class="benefit-card">
                    <span class="benefit-icon">💰</span>
                    <span class="benefit-number">₩9,900</span>
                    <div class="benefit-label">극한 저가</div>
                    <div class="benefit-detail">월/100페이지</div>
                </div>
            </div>
            
            <a href="/kr/auth.html" class="cta-button">20페이지 무료 체험 · 3초에 효과 확인 →</a>
        </div>
    </section>
    
    <!-- 主要功能说明 -->
    <div class="container">
        <div class="content-section">
            <h2>🚀 VaultCaddy로 {bank['name_kr']} 명세서 간편 처리</h2>
            
            <h3>사진 업로드만으로 완료</h3>
            <p>{bank['name_kr']} 명세서를 받으면 스마트폰으로 사진을 찍어 업로드하기만 하면 됩니다. 스캐너도 컴퓨터도 필요 없습니다. 출퇴근 중이나 카페에서도 언제 어디서나 처리할 수 있습니다.</p>
            
            <ul>
                <li><strong>스마트폰 촬영</strong>：언제 어디서나, 명세서를 받으면 즉시 촬영하여 업로드</li>
                <li><strong>스캐너 불필요</strong>：고가의 스캔 장비 구입 불필요（₩400,000-1,200,000 절약）</li>
                <li><strong>컴퓨터 불필요</strong>：스마트폰만으로 완료, 출퇴근 시간에도 처리 가능</li>
                <li><strong>실시간 처리</strong>：업로드 후 3초에 결과 표시, 대기 시간 없음</li>
                <li><strong>여러 페이지 자동 결합</strong>：3페이지 명세서도 자동 인식·결합, 수동 작업 불필요</li>
            </ul>
            
            <h3>3초 만에 처리 완료 - 수동 처리의 600배 고속</h3>
            <p>기존 수동 처리로는 명세서 1장을 처리하는 데 30-48분이 걸렸습니다. VaultCaddy AI는 단 3초 만에 완료합니다.</p>
            
            <ul>
                <li><strong>처리 시간 비교</strong>：VaultCaddy 3초 vs 수동 처리 30-48분 = <strong>600-960배 고속</strong></li>
                <li><strong>월간 50장 처리</strong>：VaultCaddy 2.5분 vs 수동 처리 25-40시간 = <strong>월간 38시간 절약</strong></li>
                <li><strong>연간 600장 처리</strong>：VaultCaddy 30분 vs 수동 처리 300-480시간 = <strong>연간 450시간 절약</strong></li>
            </ul>
            
            <h3>98% 정확도 - 수동 처리보다 13% 높음</h3>
            <p>업계 조사에 따르면, 수동으로 명세서를 처리할 경우 평균 정확도는 85%에 불과합니다. VaultCaddy AI의 정확도는 98%로 수동 처리보다 13% 높습니다.</p>
            
            <ul>
                <li><strong>계좌 정보</strong>：99%（은행명, 계좌번호, 계좌명）</li>
                <li><strong>거래 기록</strong>：98%（날짜, 설명, 금액, 잔액）</li>
                <li><strong>금액 인식</strong>：99.5%（소수점 2자리까지）</li>
                <li><strong>자동 대조</strong>：기초+거래=기말（자동 검증）</li>
            </ul>
            
            <h3>연간 ₩118,800 - 수동 처리보다 95% 절약</h3>
            <p><strong>VaultCaddy 요금</strong>：</p>
            <ul>
                <li>월액：₩9,900/월</li>
                <li>연액：₩118,800/년（<strong>약 15% 할인</strong>）</li>
                <li>초과 요금：₩150/페이지（월간 한도 초과 시）</li>
            </ul>
            
            <p><strong>수동 처리 비용</strong>：</p>
            <ul>
                <li>파트타임 경리：₩300,000-750,000/월 = <strong>₩3,600,000-9,000,000/년</strong></li>
                <li>풀타임 경리（배분 20%）：₩540,000-900,000/월 = <strong>₩6,480,000-10,800,000/년</strong></li>
            </ul>
            
            <p><strong>절약율</strong>：VaultCaddy vs 수동 처리 = <strong>95-98.9% 절약</strong></p>
            
            <h3>Excel/QuickBooks/Xero로 원클릭 출력</h3>
            <p>VaultCaddy는 독립된 도구가 아니라 기존 회계 프로세스와 원활하게 연동됩니다：</p>
            <ul>
                <li>✅ <strong>Excel 형식 CSV</strong>：범용 형식, 모든 회계 소프트웨어 지원</li>
                <li>✅ <strong>QuickBooks</strong>：QuickBooks Online/Desktop에 직접 가져오기</li>
                <li>✅ <strong>Xero</strong>：Xero 회계 시스템에 직접 가져오기</li>
                <li>✅ <strong>커스텀 형식</strong>：회계 프로세스에 맞게 맞춤화</li>
            </ul>
        </div>
    </div>
    
    <!-- Final CTA -->
    <div class="container">
        <div class="final-cta">
            <h2>오늘부터 연간 ₩6,750,000 절약</h2>
            <p>20페이지 무료 체험 · 3초에 효과 확인 · 신용카드 불필요 · 언제든지 취소 가능</p>
            <a href="/kr/auth.html" class="cta-button">무료 체험 →</a>
        </div>
    </div>
    
</body>
</html>
'''
    
    return html

# 生成日本银行页面
print("=" * 70)
print("📄 生成日文版银行页面")
print("=" * 70)
print()

for bank in japanese_banks:
    filename = f"jp/{bank['id']}-bank-statement.html"
    html = generate_japanese_bank_page(bank)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 已生成：{filename} - {bank['name_ja']}")

print()
print("=" * 70)
print("📄 生成韩文版银行页面")
print("=" * 70)
print()

for bank in korean_banks:
    filename = f"kr/{bank['id']}-bank-statement.html"
    html = generate_korean_bank_page(bank)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 已生成：{filename} - {bank['name_kr']}")

print()
print("=" * 70)
print("✅ 所有银行页面生成完成！")
print()
print("📊 生成统计：")
print(f"   - 日文版：5个银行页面")
print(f"   - 韩文版：5个银行页面")
print(f"   - 总计：10个新页面")
print()
print("📝 下一步：")
print("   1. 上传所有新生成的银行页面到服务器")
print("   2. 验证链接是否正确跳转")
print("   3. 更新sitemap（添加新页面）")
print("=" * 70)

