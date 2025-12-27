#!/usr/bin/env python3
"""
生成剩余的 204 页：
- 80 个银行页面（20 银行 × 4 语言）
- 124 个行业页面（31 行业 × 4 语言）
"""

import json
from pathlib import Path

# 使用之前的模板和配置
from phase2_generate_pages_localized import (
    BANK_PAGE_TEMPLATE,
    LANG_CONFIG,
    generate_feature_html,
    generate_benefits_html,
    generate_bank_page
)

# 行业页面模板（简化版，基于银行页面模板）
INDUSTRY_PAGE_TEMPLATE = BANK_PAGE_TEMPLATE  # 使用相同的模板结构

# 31个行业的数据
INDUSTRIES_DATA = [
    # 服务业 (11个)
    {"id": "restaurant", "name_zh": "餐廳", "name_en": "Restaurant", "name_jp": "レストラン", "name_kr": "레스토랑", "icon": "🍽️", "competitor_usage": 6},
    {"id": "retail", "name_zh": "零售店", "name_en": "Retail Store", "name_jp": "小売店", "name_kr": "소매점", "icon": "🛍️", "competitor_usage": 7},
    {"id": "beauty", "name_zh": "美容院", "name_en": "Beauty Salon", "name_jp": "美容サロン", "name_kr": "미용실", "icon": "💅", "competitor_usage": 5},
    {"id": "cleaning", "name_zh": "清潔服務", "name_en": "Cleaning Service", "name_jp": "清掃サービス", "name_kr": "청소 서비스", "icon": "🧹", "competitor_usage": 5},
    {"id": "pet", "name_zh": "寵物服務", "name_en": "Pet Service", "name_jp": "ペットサービス", "name_kr": "반려동물 서비스", "icon": "🐾", "competitor_usage": 5},
    {"id": "travel", "name_zh": "旅行社", "name_en": "Travel Agency", "name_jp": "旅行代理店", "name_kr": "여행사", "icon": "✈️", "competitor_usage": 7},
    {"id": "event", "name_zh": "活動策劃", "name_en": "Event Planning", "name_jp": "イベント企画", "name_kr": "이벤트 기획", "icon": "🎉", "competitor_usage": 6},
    {"id": "coworking", "name_zh": "共享辦公", "name_en": "Coworking Space", "name_jp": "コワーキングスペース", "name_kr": "공유 오피스", "icon": "🏢", "competitor_usage": 6},
    {"id": "property", "name_zh": "物業管理", "name_en": "Property Management", "name_jp": "不動産管理", "name_kr": "부동산 관리", "icon": "🏘️", "competitor_usage": 7},
    {"id": "delivery", "name_zh": "配送服務", "name_en": "Delivery Service", "name_jp": "配送サービス", "name_kr": "배송 서비스", "icon": "🚚", "competitor_usage": 6},
    {"id": "healthcare", "name_zh": "醫療保健", "name_en": "Healthcare", "name_jp": "ヘルスケア", "name_kr": "의료", "icon": "🏥", "competitor_usage": 8},
    
    # 专业服务 (10个)
    {"id": "accountant", "name_zh": "會計師", "name_en": "Accountant", "name_jp": "会計士", "name_kr": "회계사", "icon": "📊", "competitor_usage": 9},
    {"id": "lawyer", "name_zh": "律師", "name_en": "Lawyer", "name_jp": "弁護士", "name_kr": "변호사", "icon": "⚖️", "competitor_usage": 7},
    {"id": "consultant", "name_zh": "顧問", "name_en": "Consultant", "name_jp": "コンサルタント", "name_kr": "컨설턴트", "icon": "💼", "competitor_usage": 7},
    {"id": "marketing", "name_zh": "營銷機構", "name_en": "Marketing Agency", "name_jp": "マーケティング会社", "name_kr": "마케팅 에이전시", "icon": "📢", "competitor_usage": 7},
    {"id": "realestate", "name_zh": "房地產", "name_en": "Real Estate", "name_jp": "不動産", "name_kr": "부동산", "icon": "🏠", "competitor_usage": 7},
    {"id": "designer", "name_zh": "設計師", "name_en": "Designer", "name_jp": "デザイナー", "name_kr": "디자이너", "icon": "🎨", "competitor_usage": 6},
    {"id": "developer", "name_zh": "開發者", "name_en": "Developer", "name_jp": "開発者", "name_kr": "개발자", "icon": "💻", "competitor_usage": 6},
    {"id": "photographer", "name_zh": "攝影師", "name_en": "Photographer", "name_jp": "写真家", "name_kr": "사진작가", "icon": "📷", "competitor_usage": 5},
    {"id": "tutor", "name_zh": "補習老師", "name_en": "Tutor", "name_jp": "家庭教師", "name_kr": "과외 교사", "icon": "📚", "competitor_usage": 5},
    {"id": "fitness", "name_zh": "健身教練", "name_en": "Fitness Trainer", "name_jp": "フィットネストレーナー", "name_kr": "피트니스 트레이너", "icon": "💪", "competitor_usage": 5},
    
    # 创意和企业 (10个)
    {"id": "artist", "name_zh": "藝術家", "name_en": "Artist", "name_jp": "アーティスト", "name_kr": "예술가", "icon": "🎭", "competitor_usage": 5},
    {"id": "musician", "name_zh": "音樂家", "name_en": "Musician", "name_jp": "ミュージシャン", "name_kr": "음악가", "icon": "🎵", "competitor_usage": 5},
    {"id": "freelancer", "name_zh": "自由職業者", "name_en": "Freelancer", "name_jp": "フリーランサー", "name_kr": "프리랜서", "icon": "🧑‍💼", "competitor_usage": 6},
    {"id": "contractor", "name_zh": "承包商", "name_en": "Contractor", "name_jp": "請負業者", "name_kr": "계약자", "icon": "🔨", "competitor_usage": 6},
    {"id": "smallbiz", "name_zh": "小型企業", "name_en": "Small Business", "name_jp": "中小企業", "name_kr": "소규모 사업", "icon": "🏪", "competitor_usage": 7},
    {"id": "startup", "name_zh": "創業公司", "name_en": "Startup", "name_jp": "スタートアップ", "name_kr": "스타트업", "icon": "🚀", "competitor_usage": 7},
    {"id": "ecommerce", "name_zh": "電商", "name_en": "E-commerce", "name_jp": "Eコマース", "name_kr": "전자상거래", "icon": "🛒", "competitor_usage": 7},
    {"id": "finance", "name_zh": "個人理財", "name_en": "Personal Finance", "name_jp": "個人金融", "name_kr": "개인 금융", "icon": "💰", "competitor_usage": 8},
    {"id": "nonprofit", "name_zh": "非營利組織", "name_en": "Non-profit", "name_jp": "非営利団体", "name_kr": "비영리 단체", "icon": "🤝", "competitor_usage": 6},
    {"id": "education", "name_zh": "教育機構", "name_en": "Education", "name_jp": "教育機関", "name_kr": "교육 기관", "icon": "🎓", "competitor_usage": 7}
]

def generate_industry_page(industry_data, lang='zh'):
    """生成行业专属页面（本地化版本）"""
    config = LANG_CONFIG[lang]
    
    # 根据语言选择行业名称
    industry_name = industry_data.get(f'name_{lang}', industry_data['name_zh'])
    
    # 标题和描述（本地化）
    if lang == 'zh':
        title = f"為什麼{industry_name}選擇 VaultCaddy？"
        main_title = f"為什麼 VaultCaddy 功能更少？"
        description = f"{industry_name}專屬AI對賬單/收據處理方案 | 98%準確率 | {config['price']} | 專為{industry_name}設計"
        keywords = f"{industry_name},對賬單處理,收據管理,AI識別,Excel導出,會計軟件,香港,VaultCaddy"
        competitor_text = f"但{industry_name}只用 {industry_data['competitor_usage']} 個"
        us_text = f"{industry_name}全部都會用"
    elif lang == 'en':
        title = f"Why {industry_name}s Choose VaultCaddy?"
        main_title = f"Why Does VaultCaddy Have Fewer Features?"
        description = f"{industry_name}-exclusive AI receipt/invoice processing | 98% accuracy | {config['price']} | Designed for {industry_name}s"
        keywords = f"{industry_name},receipt processing,invoice management,AI recognition,Excel export,accounting software,VaultCaddy"
        competitor_text = f"But {industry_name}s only use {industry_data['competitor_usage']} of them"
        us_text = f"{industry_name}s use them all"
    elif lang == 'jp':
        title = f"なぜ{industry_name}がVaultCaddyを選ぶのか？"
        main_title = f"なぜVaultCaddyは機能が少ないのか？"
        description = f"{industry_name}専用AI領収書・請求書処理 | 98%精度 | {config['price']} | {industry_name}向け設計"
        keywords = f"{industry_name},領収書処理,請求書管理,AI認識,Excelエクスポート,会計ソフト,VaultCaddy"
        competitor_text = f"しかし{industry_name}は{industry_data['competitor_usage']}個しか使わない"
        us_text = f"{industry_name}はすべて使います"
    else:  # kr
        title = f"왜 {industry_name}가 VaultCaddy를 선택할까요?"
        main_title = f"왜 VaultCaddy는 기능이 적을까요?"
        description = f"{industry_name} 전용 AI 영수증/인보이스 처리 | 98% 정확도 | {config['price']} | {industry_name}용 설계"
        keywords = f"{industry_name},영수증 처리,인보이스 관리,AI 인식,Excel 내보내기,회계 소프트웨어,VaultCaddy"
        competitor_text = f"하지만 {industry_name}는 {industry_data['competitor_usage']}개만 사용"
        us_text = f"{industry_name}는 모두 사용합니다"
    
    # 核心功能（本地化）
    features = [
        ("對賬單/收據/發票識別（98% 準確率）" if lang == 'zh' else 
         "Bank Statement/Receipt/Invoice Recognition (98% Accuracy)" if lang == 'en' else
         "銀行明細・領収書・請求書認識（98%精度）" if lang == 'jp' else
         "은행 명세서/영수증/인보이스 인식 (98% 정확도)"),
        "Excel " + ("一鍵導出" if lang == 'zh' else 
         "One-Click Export" if lang == 'en' else
         "ワンクリックエクスポート" if lang == 'jp' else
         "원클릭 내보내기"),
        ("雲端存儲和搜索" if lang == 'zh' else 
         "Cloud Storage & Search" if lang == 'en' else
         "クラウドストレージと検索" if lang == 'jp' else
         "클라우드 저장 및 검색")
    ]
    
    # 優勢標籤（本地化）
    benefits = [
        {'icon': '💰', 'text': config['price_vs']},
        {'icon': '⚡', 'text': '3' + ('秒でセットアップ' if lang == 'jp' else '초 설정' if lang == 'kr' else '秒上手' if lang == 'zh' else '-Second Setup')},
        {'icon': industry_data['icon'], 'text': industry_name + (' 専用' if lang == 'jp' else ' 전용' if lang == 'kr' else ' 專用' if lang == 'zh' else ' Exclusive')}
    ]
    
    # 文件路径
    if lang == 'zh':
        url_path = f"{industry_data['id']}-accounting-solution.html"
    else:
        url_path = f"{lang}/{industry_data['id']}-accounting-solution.html"
    
    # 生成页面
    page_html = BANK_PAGE_TEMPLATE.format(
        lang=config['lang'],
        title=title,
        description=description,
        keywords=keywords,
        page_id=f"{industry_data['id']}-{lang}",
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
        competitor_name=config['competitor_name'],
        competitor_text=competitor_text,
        us_text=us_text,
        formula=config['formula'],
        benefits_html=generate_benefits_html(benefits),
        target_title=config['target_title'],
        target_customers=config['target_customers'],
        cta_button=config['cta_button'],
        cta_subtext=config['cta_subtext'],
        footer_rights=config['footer_rights']
    )
    
    return page_html, url_path

def main():
    """主函数"""
    total_pages = 0
    generated_pages = []
    
    print("🚀 开始生成剩余的 204 页...")
    print("=" * 60)
    
    # 1. 生成剩余的 80 个银行页面
    print("\n📊 第1部分：生成剩余 80 个银行页面...")
    print("-" * 60)
    
    with open('phase2_complete_banks_data.json', 'r', encoding='utf-8') as f:
        new_banks_data = json.load(f)
    
    all_new_banks = (
        new_banks_data['remaining_international_banks'] +
        new_banks_data['remaining_asian_banks']
    )
    
    for bank in all_new_banks:
        for lang in ['zh', 'en', 'jp', 'kr']:
            page_html, url_path = generate_bank_page(bank, lang)
            
            if lang == 'zh':
                output_dir = Path('.')
                output_file = output_dir / url_path
            else:
                output_dir = Path(lang)
                output_dir.mkdir(exist_ok=True)
                output_file = output_dir / f"{bank['id']}-bank-statement-simple.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            total_pages += 1
            generated_pages.append(str(output_file))
            
            config = LANG_CONFIG[lang]
            print(f"✅ {output_file.name} - {config['price']}")
    
    print(f"\n✅ 银行页面完成：{len(all_new_banks) * 4} 页")
    
    # 2. 生成 124 个行业页面
    print("\n📊 第2部分：生成 124 个行业页面...")
    print("-" * 60)
    
    for industry in INDUSTRIES_DATA:
        for lang in ['zh', 'en', 'jp', 'kr']:
            page_html, url_path = generate_industry_page(industry, lang)
            
            if lang == 'zh':
                output_dir = Path('.')
                output_file = output_dir / url_path
            else:
                output_dir = Path(lang)
                output_dir.mkdir(exist_ok=True)
                output_file = output_dir / f"{industry['id']}-accounting-solution.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_html)
            
            total_pages += 1
            generated_pages.append(str(output_file))
            
            industry_name = industry.get(f'name_{lang}', industry['name_zh'])
            config = LANG_CONFIG[lang]
            print(f"✅ {industry['icon']} {industry_name} - {config['price']}")
    
    print("\n" + "=" * 60)
    print(f"🎉 完成！共生成 {total_pages} 个页面")
    print(f"   - 80 个银行页面（20 银行 × 4 语言）")
    print(f"   - 124 个行业页面（31 行业 × 4 语言）")
    
    # 保存生成的页面列表
    with open('phase2_generated_remaining_204_pages.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(generated_pages))
    
    return generated_pages

if __name__ == '__main__':
    main()

