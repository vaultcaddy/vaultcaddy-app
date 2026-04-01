#!/usr/bin/env python3
"""
阶段 2：批量生成 292 个细分市场专属 Landing Page
- 168 个银行专属页面（42 银行 × 4 语言）
- 124 个行业专属页面（31 行业 × 4 语言）
"""

import json
import os
from pathlib import Path

# 页面模板
BANK_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | VaultCaddy</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title} | VaultCaddy">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://vaultcaddy.com/images/og/og-{page_id}.jpg">
    <meta property="og:url" content="https://vaultcaddy.com/{url_path}">
    
    <link rel="stylesheet" href="{css_path}styles.css">
    <link rel="stylesheet" href="{css_path}landing-page.css">
</head>
<body>
    
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <a href="{base_path}" class="logo">VaultCaddy</a>
            <div class="nav-links">
                <a href="{base_path}features.html">{nav_features}</a>
                <a href="{base_path}pricing.html">{nav_pricing}</a>
                <a href="{base_path}resources.html">{nav_resources}</a>
                <a href="{base_path}auth.html" class="cta-button-small">{nav_cta}</a>
            </div>
        </div>
    </nav>
    
    <!-- 簡化優勢 Hero 區域 -->
    <section class="why-less-is-more" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 80px 20px; text-align: center; color: white; margin-top: 0;">
        <div class="container" style="max-width: 1200px; margin: 0 auto;">
            
            <div style="display: inline-block; background: rgba(255, 255, 255, 0.2); padding: 8px 20px; border-radius: 50px; margin-bottom: 24px; backdrop-filter: blur(10px);">
                <span style="font-size: 14px; font-weight: 600;">💡 {badge_text}</span>
            </div>
            
            <h1 style="font-size: 42px; line-height: 1.2; margin-bottom: 16px; font-weight: 700;">
                {main_title}
            </h1>
            
            <p style="font-size: 20px; opacity: 0.95; margin-bottom: 40px; font-weight: 400;">
                {subtitle}
            </p>
            
            <!-- 核心功能 -->
            <div style="max-width: 600px; margin: 0 auto 40px;">
                {features_html}
            </div>
            
            <!-- 對比框 -->
            <div style="display: flex; justify-content: center; align-items: center; gap: 32px; margin: 40px 0; flex-wrap: wrap;">
                <div style="background: rgba(239, 68, 68, 0.2); border: 2px solid rgba(239, 68, 68, 0.5); padding: 32px; border-radius: 16px; min-width: 200px; backdrop-filter: blur(10px);">
                    <div style="font-size: 24px; font-weight: bold; margin-bottom: 16px;">Dext</div>
                    <div style="font-size: 32px; font-weight: bold; margin-bottom: 8px;">60+ {features_label}</div>
                    <div style="font-size: 14px; opacity: 0.9;">{competitor_text}</div>
                </div>
                <div style="font-size: 24px; font-weight: bold; color: #ffd700;">VS</div>
                <div style="background: rgba(74, 222, 128, 0.1); border: 2px solid rgba(74, 222, 128, 0.8); padding: 32px; border-radius: 16px; min-width: 200px; backdrop-filter: blur(10px);">
                    <div style="font-size: 24px; font-weight: bold; margin-bottom: 16px;">VaultCaddy</div>
                    <div style="font-size: 32px; font-weight: bold; margin-bottom: 8px;">12 {features_label}</div>
                    <div style="font-size: 14px; color: #ffd700; font-weight: bold;">{us_text} ✓</div>
                </div>
            </div>
            
            <!-- 公式 -->
            <div style="margin: 40px 0;">
                <h2 style="font-size: 36px; font-weight: bold; color: #ffd700; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">
                    {formula}
                </h2>
            </div>
            
            <!-- 優勢標籤 -->
            <div style="display: flex; justify-content: center; gap: 32px; margin: 40px 0; flex-wrap: wrap;">
                {benefits_html}
            </div>
            
            <!-- CTA -->
            <div style="margin-top: 40px;">
                <a href="{base_path}auth.html" style="display: inline-block; padding: 18px 48px; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #1a1a1a; font-size: 20px; font-weight: bold; border-radius: 50px; text-decoration: none; box-shadow: 0 8px 24px rgba(255, 215, 0, 0.4); transition: all 0.3s ease;">
                    {cta_button}
                </a>
                <p style="margin-top: 16px; font-size: 14px; opacity: 0.9;">{cta_subtext}</p>
            </div>
            
        </div>
    </section>
    
    <!-- 響應式設計 -->
    <style>
    @media (max-width: 768px) {{
        .why-less-is-more h1 {{
            font-size: 28px !important;
        }}
        .why-less-is-more h2 {{
            font-size: 24px !important;
        }}
    }}
    </style>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 VaultCaddy. {footer_rights}</p>
        </div>
    </footer>
    
</body>
</html>
'''

# 语言配置
LANG_CONFIG = {
    'zh': {
        'lang': 'zh-HK',
        'base_path': '/',
        'css_path': '/',
        'nav_features': '功能',
        'nav_pricing': '定價',
        'nav_resources': '資源',
        'nav_cta': '立即試用',
        'badge_text': '為什麼選擇 VaultCaddy？',
        'subtitle': '因為我們只保留您真正需要的',
        'features_label': '功能',
        'formula': '更少 = 更簡單 = 更快 = 更便宜',
        'cta_button': '立即免費試用 20 頁 →',
        'cta_subtext': '無需信用卡 | 3秒看到效果',
        'footer_rights': '版權所有'
    },
    'en': {
        'lang': 'en',
        'base_path': '/',
        'css_path': '../',
        'nav_features': 'Features',
        'nav_pricing': 'Pricing',
        'nav_resources': 'Resources',
        'nav_cta': 'Try Now',
        'badge_text': 'Why Choose VaultCaddy?',
        'subtitle': 'Because we only keep what you actually need',
        'features_label': 'Features',
        'formula': 'Less = Simpler = Faster = Cheaper',
        'cta_button': 'Start Free Trial (20 Pages) →',
        'cta_subtext': 'No credit card required | See results in 3 seconds',
        'footer_rights': 'All rights reserved'
    },
    'jp': {
        'lang': 'ja',
        'base_path': '/',
        'css_path': '../',
        'nav_features': '機能',
        'nav_pricing': '料金',
        'nav_resources': 'リソース',
        'nav_cta': '今すぐ試す',
        'badge_text': 'なぜVaultCaddyを選ぶのか？',
        'subtitle': '本当に必要な機能だけを残しているから',
        'features_label': '機能',
        'formula': '少ない = シンプル = 速い = 安い',
        'cta_button': '無料トライアル（20ページ）→',
        'cta_subtext': 'クレジットカード不要 | 3秒で結果表示',
        'footer_rights': '無断転載禁止'
    },
    'kr': {
        'lang': 'ko',
        'base_path': '/',
        'css_path': '../',
        'nav_features': '기능',
        'nav_pricing': '가격',
        'nav_resources': '리소스',
        'nav_cta': '지금 시도',
        'badge_text': '왜 VaultCaddy를 선택해야 할까요?',
        'subtitle': '정말 필요한 기능만 남겨두었기 때문입니다',
        'features_label': '기능',
        'formula': '적음 = 간단함 = 빠름 = 저렴함',
        'cta_button': '무료 체험 (20페이지) →',
        'cta_subtext': '신용카드 불필요 | 3초 결과 확인',
        'footer_rights': '저작권 소유'
    }
}

def generate_feature_html(features):
    """生成核心功能 HTML"""
    html = ""
    for feature in features:
        html += f'''
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(255, 255, 255, 0.1); padding: 16px 24px; border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(5px);">
                    <span style="color: #4ade80; font-size: 24px; font-weight: bold;">✓</span>
                    <span style="font-size: 18px; text-align: left;">{feature}</span>
                </div>'''
    return html

def generate_benefits_html(benefits):
    """生成優勢標籤 HTML"""
    html = ""
    for benefit in benefits:
        html += f'''
                <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                    <span style="font-size: 32px;">{benefit['icon']}</span>
                    <span style="font-size: 16px; font-weight: 600;">{benefit['text']}</span>
                </div>'''
    return html

def generate_bank_page(bank_data, lang='zh'):
    """生成银行专属页面"""
    config = LANG_CONFIG[lang]
    
    # 根据语言选择银行名称
    bank_name = bank_data.get(f'name_{lang}', bank_data['name'])
    
    # 标题和描述
    if lang == 'zh':
        title = f"為什麼選擇 VaultCaddy 處理 {bank_name} 對賬單？"
        main_title = f"為什麼 VaultCaddy 功能更少？"
        description = f"{bank_name} 客戶專屬AI對賬單處理方案 | 98%準確率 | 比Dext便宜83% | 3秒上手"
        keywords = f"{bank_name},對賬單處理,AI識別,Excel導出,會計軟件,香港,VaultCaddy,Dext替代"
        competitor_text = f"但{bank_name}客戶只用 {bank_data['competitor_usage']} 個"
        us_text = f"{bank_name}客戶全部都會用"
    elif lang == 'en':
        title = f"Why Choose VaultCaddy for {bank_name} Bank Statement Processing?"
        main_title = f"Why Does VaultCaddy Have Fewer Features?"
        description = f"{bank_name} customer-exclusive AI bank statement processing | 98% accuracy | 83% cheaper than Dext | 3-second setup"
        keywords = f"{bank_name},bank statement processing,AI recognition,Excel export,accounting software,Hong Kong,VaultCaddy,Dext alternative"
        competitor_text = f"But {bank_name} customers only use {bank_data['competitor_usage']} of them"
        us_text = f"{bank_name} customers use them all"
    elif lang == 'jp':
        title = f"なぜ{bank_name}の銀行明細処理にVaultCaddyを選ぶのか？"
        main_title = f"なぜVaultCaddyは機能が少ないのか？"
        description = f"{bank_name}顧客専用AI銀行明細処理 | 98%精度 | Dextより83%安い | 3秒でセットアップ"
        keywords = f"{bank_name},銀行明細処理,AI認識,Excelエクスポート,会計ソフト,香港,VaultCaddy,Dext代替"
        competitor_text = f"しかし{bank_name}顧客は{bank_data['competitor_usage']}個しか使わない"
        us_text = f"{bank_name}顧客はすべて使います"
    else:  # kr
        title = f"왜 {bank_name} 은행 명세서 처리에 VaultCaddy를 선택해야 할까요?"
        main_title = f"왜 VaultCaddy는 기능이 적을까요?"
        description = f"{bank_name} 고객 전용 AI 은행 명세서 처리 | 98% 정확도 | Dext보다 83% 저렴 | 3초 설정"
        keywords = f"{bank_name},은행 명세서 처리,AI 인식,Excel 내보내기,회계 소프트웨어,홍콩,VaultCaddy,Dext 대안"
        competitor_text = f"하지만 {bank_name} 고객은 {bank_data['competitor_usage']}개만 사용"
        us_text = f"{bank_name} 고객은 모두 사용합니다"
    
    # 核心功能
    features = [
        f"{bank_name} " + ("對賬單識別（98% 準確率）" if lang == 'zh' else 
         "Bank Statement Recognition (98% Accuracy)" if lang == 'en' else
         "銀行明細認識（98%精度）" if lang == 'jp' else
         "은행 명세서 인식 (98% 정확도)"),
        "Excel " + ("一鍵導出" if lang == 'zh' else 
         "One-Click Export" if lang == 'en' else
         "ワンクリックエクスポート" if lang == 'jp' else
         "원클릭 내보내기"),
        ("雲端存儲和搜索" if lang == 'zh' else 
         "Cloud Storage & Search" if lang == 'en' else
         "クラウドストレージと検索" if lang == 'jp' else
         "클라우드 저장 및 검색")
    ]
    
    # 優勢標籤
    benefits = [
        {'icon': '💰', 'text': 'Dext' + ('より83%安い' if lang == 'jp' else '보다 83% 저렴' if lang == 'kr' else '比 Dext 便宜 83%' if lang == 'zh' else ' 83% Cheaper than Dext')},
        {'icon': '⚡', 'text': '3' + ('秒でセットアップ' if lang == 'jp' else '초 설정' if lang == 'kr' else '秒上手' if lang == 'zh' else '-Second Setup')},
        {'icon': '🇭🇰', 'text': bank_name + (' 専項支援' if lang == 'jp' else ' 전용 지원' if lang == 'kr' else ' 專項支援' if lang == 'zh' else ' Exclusive Support')}
    ]
    
    # 文件路径
    if lang == 'zh':
        url_path = f"{bank_data['id']}-bank-statement-simple.html"
    else:
        url_path = f"{lang}/{bank_data['id']}-bank-statement-simple.html"
    
    # 生成页面
    page_html = BANK_PAGE_TEMPLATE.format(
        lang=config['lang'],
        title=title,
        description=description,
        keywords=keywords,
        page_id=f"{bank_data['id']}-{lang}",
        url_path=url_path,
        css_path=config['css_path'],
        base_path=config['base_path'],
        nav_features=config['nav_features'],
        nav_pricing=config['nav_pricing'],
        nav_resources=config['nav_resources'],
        nav_cta=config['nav_cta'],
        badge_text=config['badge_text'],
        main_title=main_title,
        subtitle=config['subtitle'],
        features_html=generate_feature_html(features),
        features_label=config['features_label'],
        competitor_text=competitor_text,
        us_text=us_text,
        formula=config['formula'],
        benefits_html=generate_benefits_html(benefits),
        cta_button=config['cta_button'],
        cta_subtext=config['cta_subtext'],
        footer_rights=config['footer_rights']
    )
    
    return page_html, url_path

def main():
    """主函数"""
    # 读取银行数据
    with open('phase2_banks_data.json', 'r', encoding='utf-8') as f:
        banks_data = json.load(f)
    
    # 统计
    total_pages = 0
    generated_pages = []
    
    print("🚀 开始生成阶段 2 银行专属页面...")
    print("=" * 60)
    
    # 生成所有银行页面
    all_banks = (
        banks_data['hong_kong_banks'] + 
        banks_data.get('international_banks', [])[:5] +  # 先生成前5个国际银行
        banks_data.get('asian_banks', [])[:5]  # 先生成前5个亚洲银行
    )
    
    for bank in all_banks:
        for lang in ['zh', 'en', 'jp', 'kr']:
            # 生成页面
            page_html, url_path = generate_bank_page(bank, lang)
            
            # 确定输出路径
            if lang == 'zh':
                output_dir = Path('.')
                output_file = output_dir / url_path
            else:
                output_dir = Path(lang)
                output_dir.mkdir(exist_ok=True)
                output_file = output_dir / f"{bank['id']}-bank-statement-simple.html"
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            total_pages += 1
            generated_pages.append(str(output_file))
            print(f"✅ 已生成：{output_file}")
    
    print("=" * 60)
    print(f"🎉 完成！共生成 {total_pages} 个银行专属页面")
    print(f"📝 生成的页面列表已保存")
    
    # 保存生成的页面列表
    with open('phase2_generated_pages.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(generated_pages))
    
    return generated_pages

if __name__ == '__main__':
    main()

