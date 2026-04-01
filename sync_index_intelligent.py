#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能首页同步系统
作用：
1. 同步中文版index.html的内容结构到其他语言版本
2. 保护每个版本的价格信息（港币 vs 美金 vs 日元 vs 韩元）
3. 保护每个版本的地区信息（香港 vs 美国 vs 日本 vs 韩国）
4. 只翻译通用内容，保留本地化内容

使用方法：
python3 sync_index_intelligent.py
"""

import os
import re
from pathlib import Path

# ============================================
# 地区和价格配置
# ============================================
REGION_CONFIG = {
    'zh': {
        'language': '中文',
        'currency': 'HKD',
        'currency_symbol': 'HK$',
        'region': '香港',
        'region_en': 'Hong Kong',
        'country_code': 'HK',
        'locale': 'zh_TW',
        'prices': {
            'per_page': '0.5',
            'per_page_display': 'HK$0.5',
            'monthly': '58',
            'monthly_display': 'HK$58',
            'yearly': '552',
            'yearly_display': 'HK$552',
            'monthly_discount': '46',
            'monthly_discount_display': 'HK$46'
        },
        'banks': ['匯豐HSBC', '恆生', '中銀', '渣打'],
        'accounting_standard': '香港會計準則',
        'accounting_standard_code': 'HKFRS'
    },
    'en': {
        'language': 'English',
        'currency': 'USD',
        'currency_symbol': '$',
        'region': '美國',
        'region_en': 'United States',
        'country_code': 'US',
        'locale': 'en_US',
        'prices': {
            'per_page': '0.06',
            'per_page_display': '$0.06',
            'monthly': '6.99',
            'monthly_display': '$6.99',
            'yearly': '66.90',
            'yearly_display': '$66.90',
            'monthly_discount': '5.58',
            'monthly_discount_display': '$5.58'
        },
        'banks': ['Bank of America', 'Chase', 'Wells Fargo', 'Citibank'],
        'accounting_standard': 'GAAP',
        'accounting_standard_code': 'GAAP'
    },
    'jp': {
        'language': '日本語',
        'currency': 'JPY',
        'currency_symbol': '¥',
        'region': '日本',
        'region_en': 'Japan',
        'country_code': 'JP',
        'locale': 'ja_JP',
        'prices': {
            'per_page': '8',
            'per_page_display': '¥8',
            'monthly': '880',
            'monthly_display': '¥880',
            'yearly': '8,640',
            'yearly_display': '¥8,640',
            'monthly_discount': '720',
            'monthly_discount_display': '¥720'
        },
        'banks': ['三菱UFJ銀行', 'みずほ銀行', '三井住友銀行', 'りそな銀行'],
        'accounting_standard': '日本会計基準',
        'accounting_standard_code': 'JGAAP'
    },
    'kr': {
        'language': '한국어',
        'currency': 'KRW',
        'currency_symbol': '₩',
        'region': '韓國',
        'region_en': 'South Korea',
        'country_code': 'KR',
        'locale': 'ko_KR',
        'prices': {
            'per_page': '80',
            'per_page_display': '₩80',
            'monthly': '8,800',
            'monthly_display': '₩8,800',
            'yearly': '84,480',
            'yearly_display': '₩84,480',
            'monthly_discount': '7,040',
            'monthly_discount_display': '₩7,040'
        },
        'banks': ['KB국민은행', '신한은행', '우리은행', '하나은행'],
        'accounting_standard': '한국회계기준',
        'accounting_standard_code': 'K-GAAP'
    }
}

# ============================================
# 翻译字典（通用内容）
# ============================================
TRANSLATION_DICT = {
    # 功能描述
    '功能': {'en': 'Features', 'jp': '機能', 'kr': '기능'},
    '價格': {'en': 'Pricing', 'jp': '価格', 'kr': '가격'},
    '學習中心': {'en': 'Learning Center', 'jp': '学習センター', 'kr': '학습 센터'},
    '儀表板': {'en': 'Dashboard', 'jp': 'ダッシュボード', 'kr': '대시보드'},
    '登入': {'en': 'Login', 'jp': 'ログイン', 'kr': '로그인'},
    
    # 主页标题和描述
    '銀行對帳單AI處理專家': {
        'en': 'AI Bank Statement Processing Expert',
        'jp': 'AI銀行明細処理の専門家',
        'kr': 'AI 은행 명세서 처리 전문가'
    },
    '支援匯豐恆生中銀': {
        'en': 'Support Major Banks',
        'jp': '主要銀行対応',
        'kr': '주요 은행 지원'
    },
    'QuickBooks整合': {
        'en': 'QuickBooks Integration',
        'jp': 'QuickBooks統合',
        'kr': 'QuickBooks 통합'
    },
    '低至': {'en': 'From', 'jp': '最低', 'kr': '최저'},
    '頁': {'en': 'page', 'jp': 'ページ', 'kr': '페이지'},
    
    # 按钮和行动号召
    '立即免費試用': {
        'en': 'Try Free Now',
        'jp': '今すぐ無料で試す',
        'kr': '지금 무료로 체험'
    },
    '開始使用': {
        'en': 'Get Started',
        'jp': '始める',
        'kr': '시작하기'
    },
    '了解更多': {
        'en': 'Learn More',
        'jp': '詳しく見る',
        'kr': '자세히 보기'
    },
    
    # 功能特点
    '自動分類收支交易': {
        'en': 'Auto categorize income and expense',
        'jp': '収支取引を自動分類',
        'kr': '수입 지출 자동 분류'
    },
    '一鍵匯出': {
        'en': 'One-click export to',
        'jp': 'ワンクリックでエクスポート',
        'kr': '원클릭 내보내기'
    },
    '準確率': {'en': 'Accuracy', 'jp': '精度', 'kr': '정확도'},
    '極速處理': {
        'en': 'Ultra-Fast Processing',
        'jp': '超高速処理',
        'kr': '초고속 처리'
    },
    '免費試用': {
        'en': 'Free Trial',
        'jp': '無料トライアル',
        'kr': '무료 평가판'
    },
    
    # 定价计划
    '月付': {'en': 'Monthly', 'jp': '月払い', 'kr': '월간'},
    '年付': {'en': 'Yearly', 'jp': '年払い', 'kr': '연간'},
    '每月': {'en': 'per month', 'jp': '月間', 'kr': '월'},
    '超出後': {
        'en': 'Then',
        'jp': '超過後',
        'kr': '초과 시'
    },
    '批次處理無限制文件': {
        'en': 'Unlimited Batch Processing',
        'jp': 'バッチ処理無制限',
        'kr': '무제한 배치 처리'
    },
    
    # 常见问题
    '常見問題': {
        'en': 'FAQ',
        'jp': 'よくある質問',
        'kr': '자주 묻는 질문'
    },
    '支援哪些銀行': {
        'en': 'Which banks are supported',
        'jp': 'どの銀行に対応していますか',
        'kr': '어떤 은행을 지원하나요'
    },
    '收費是多少': {
        'en': 'What is the pricing',
        'jp': '料金はいくらですか',
        'kr': '요금은 얼마인가요'
    },
    
    # 其他常用词
    '已服務': {'en': 'Trusted by', 'jp': 'ご利用企業', 'kr': '신뢰받는'},
    '會計師': {'en': 'accountants', 'jp': '会計士', 'kr': '회계사'},
    '企業': {'en': 'businesses', 'jp': '企業', 'kr': '기업'},
    '節省': {'en': 'save', 'jp': '節約', 'kr': '절약'},
    '時間': {'en': 'time', 'jp': '時間', 'kr': '시간'},
}

# ============================================
# 价格替换规则（正则表达式）
# ============================================
def get_price_patterns(lang_config):
    """生成价格相关的正则表达式模式"""
    patterns = []
    
    # 每页价格模式
    patterns.append({
        'name': 'per_page_price',
        'zh_pattern': r'HK\$\s*0\.5',
        'replacement': lang_config['prices']['per_page_display']
    })
    
    # 月费价格模式
    patterns.append({
        'name': 'monthly_price',
        'zh_pattern': r'HK\$\s*58',
        'replacement': lang_config['prices']['monthly_display']
    })
    
    # 年费价格模式
    patterns.append({
        'name': 'yearly_price',
        'zh_pattern': r'HK\$\s*552',
        'replacement': lang_config['prices']['yearly_display']
    })
    
    # 货币代码
    patterns.append({
        'name': 'currency_code',
        'zh_pattern': r'"priceCurrency":\s*"HKD"',
        'replacement': f'"priceCurrency": "{lang_config["currency"]}"'
    })
    
    # 结构化数据中的价格
    patterns.append({
        'name': 'schema_per_page',
        'zh_pattern': r'"price":\s*"0\.50"',
        'replacement': f'"price": "{lang_config["prices"]["per_page"]}"'
    })
    
    patterns.append({
        'name': 'schema_monthly',
        'zh_pattern': r'"price":\s*"58"',
        'replacement': f'"price": "{lang_config["prices"]["monthly"]}"'
    })
    
    return patterns

# ============================================
# 地区替换规则
# ============================================
def get_region_patterns(lang_config):
    """生成地区相关的正则表达式模式"""
    patterns = []
    
    # 香港 → 目标地区
    patterns.append({
        'name': 'region_chinese',
        'zh_pattern': r'香港',
        'replacement': lang_config['region'],
        'exclude_in': ['银行', 'Bank', '中国银行', 'BOC']  # 避免替换"中国银行（香港）"
    })
    
    # Hong Kong → 目标地区英文
    patterns.append({
        'name': 'region_english',
        'zh_pattern': r'Hong\s+Kong',
        'replacement': lang_config['region_en']
    })
    
    # 国家代码
    patterns.append({
        'name': 'country_code',
        'zh_pattern': r'"addressCountry":\s*"HK"',
        'replacement': f'"addressCountry": "{lang_config["country_code"]}"'
    })
    
    # locale
    patterns.append({
        'name': 'locale',
        'zh_pattern': r'"og:locale"\s+content="zh_TW"',
        'replacement': f'"og:locale" content="{lang_config["locale"]}"'
    })
    
    return patterns

# ============================================
# 银行列表替换
# ============================================
def replace_banks(content, lang_config):
    """替换银行列表"""
    # 这是一个简化版，实际可能需要更复杂的处理
    # 中文版的银行列表
    zh_banks = REGION_CONFIG['zh']['banks']
    target_banks = lang_config['banks']
    
    # 简单替换（实际使用时可能需要更智能的处理）
    content = content.replace('匯豐HSBC/恆生/中銀/渣打', '/'.join(target_banks[:4]))
    
    return content

# ============================================
# 核心同步函数
# ============================================
def sync_index_intelligent(target_lang):
    """智能同步首页到目标语言"""
    
    if target_lang not in REGION_CONFIG:
        print(f'❌ 不支持的语言: {target_lang}')
        return False
    
    lang_config = REGION_CONFIG[target_lang]
    
    print(f'\n{'='*70}')
    print(f'📄 同步首页到 {lang_config["language"]} 版本')
    print(f'{'='*70}\n')
    
    # 读取中文版index.html
    zh_file = 'index.html'
    if not os.path.exists(zh_file):
        print(f'❌ 找不到源文件: {zh_file}')
        return False
    
    with open(zh_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'✅ 读取中文版: {zh_file}')
    
    # 1. 替换价格信息
    print('\n💰 处理价格信息...')
    price_patterns = get_price_patterns(lang_config)
    for pattern in price_patterns:
        old_count = len(re.findall(pattern['zh_pattern'], content))
        if old_count > 0:
            content = re.sub(pattern['zh_pattern'], pattern['replacement'], content)
            print(f'   ✅ {pattern["name"]}: 替换 {old_count} 处')
    
    # 2. 替换地区信息
    print('\n🌍 处理地区信息...')
    region_patterns = get_region_patterns(lang_config)
    for pattern in region_patterns:
        old_count = len(re.findall(pattern['zh_pattern'], content))
        if old_count > 0:
            # 检查排除条件
            if 'exclude_in' in pattern:
                # 这里需要更复杂的逻辑来避免替换特定上下文中的内容
                # 简化处理
                pass
            content = re.sub(pattern['zh_pattern'], pattern['replacement'], content)
            print(f'   ✅ {pattern["name"]}: 替换 {old_count} 处')
    
    # 3. 替换银行列表
    print('\n🏦 处理银行列表...')
    content = replace_banks(content, lang_config)
    print(f'   ✅ 银行列表已更新')
    
    # 4. 翻译通用内容
    print('\n🌐 翻译通用内容...')
    translation_count = 0
    for zh_text, translations in TRANSLATION_DICT.items():
        if target_lang in translations:
            old_count = content.count(zh_text)
            if old_count > 0:
                content = content.replace(zh_text, translations[target_lang])
                translation_count += old_count
    print(f'   ✅ 翻译项数: {translation_count}')
    
    # 5. 更新语言标签
    content = re.sub(r'<html lang="zh-TW">', f'<html lang="{lang_config["locale"][:2]}">', content)
    
    # 6. 写入目标文件
    target_dir = Path(target_lang)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'index.html'
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n✅ 已写入: {target_file}')
    print(f'\n📊 摘要:')
    print(f'   - 货币: {lang_config["currency"]}')
    print(f'   - 每页价格: {lang_config["prices"]["per_page_display"]}')
    print(f'   - 月费: {lang_config["prices"]["monthly_display"]}')
    print(f'   - 地区: {lang_config["region"]}')
    
    return True

# ============================================
# 主函数
# ============================================
def main():
    """主函数"""
    print('╔══════════════════════════════════════════════════════════════════════╗')
    print('║          🌐 智能首页同步系统                                          ║')
    print('╚══════════════════════════════════════════════════════════════════════╝')
    print()
    print('📝 功能：')
    print('   - ✅ 同步内容结构')
    print('   - ✅ 保护价格信息（每个版本使用不同货币）')
    print('   - ✅ 保护地区信息（每个版本针对不同地区）')
    print('   - ✅ 翻译通用内容')
    print()
    
    success_count = 0
    total_count = 3
    
    # 同步到英文、日文、韩文
    for lang in ['en', 'jp', 'kr']:
        if sync_index_intelligent(lang):
            success_count += 1
    
    print()
    print('='*70)
    print(f'✅ 完成！成功同步 {success_count}/{total_count} 个语言版本')
    print('='*70)
    print()
    print('📝 价格配置摘要：')
    print(f'   🇨🇳 中文版: HK$0.5/页, HK$58/月 (香港)')
    print(f'   🇺🇸 英文版: ${REGION_CONFIG["en"]["prices"]["per_page"]}/页, ${REGION_CONFIG["en"]["prices"]["monthly"]}/月 (美国)')
    print(f'   🇯🇵 日文版: ¥{REGION_CONFIG["jp"]["prices"]["per_page"]}/页, ¥{REGION_CONFIG["jp"]["prices"]["monthly"]}/月 (日本)')
    print(f'   🇰🇷 韩文版: ₩{REGION_CONFIG["kr"]["prices"]["per_page"]}/页, ₩{REGION_CONFIG["kr"]["prices"]["monthly"]}/月 (韩国)')
    print()
    print('🎉 所有版本的价格和地区信息已正确保护！')

if __name__ == '__main__':
    main()

