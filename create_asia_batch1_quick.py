#!/usr/bin/env python3
"""
快速创建亚洲Batch 1: 日本+韩国银行页面 (6个)
使用简化版SEO模板，30分钟完成
"""

BANKS = [
    {
        'filename': 'mufg-bank-statement-v2.html',
        'name': 'Mitsubishi UFJ',
        'full_name': 'Mitsubishi UFJ Financial Group',
        'country': 'Japan',
        'currency': 'JPY',
        'symbol': '¥',
        'monthly': '926',
        'annual': '11,112',
        'extra': '10',
        'brand_start': '#E60012',
        'brand_end': '#CC0000',
        'businesses': '100K+',
        'title': 'MUFG Bank Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy',
        'description': 'AI-powered Mitsubishi UFJ statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ¥926/month | 100K+ Japanese businesses',
        'keywords': 'MUFG bank statement,Japanese bank statement converter,三菱UFJ to Excel,Japan accounting automation'
    },
    {
        'filename': 'kb-kookmin-statement-v2.html',
        'name': 'KB Kookmin Bank',
        'full_name': 'KB Kookmin Bank',
        'country': 'South Korea',
        'currency': 'KRW',
        'symbol': '₩',
        'monthly': '7,998',
        'annual': '95,976',
        'extra': '80',
        'brand_start': '#FFCC00',
        'brand_end': '#FFB800',
        'businesses': '80K+',
        'title': 'KB Kookmin Bank Statement Converter | PDF to Excel | 98% Accuracy',
        'description': 'AI-powered KB Kookmin statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ₩7,998/month | 80K+ Korean businesses',
        'keywords': 'KB Kookmin statement,Korean bank statement converter,국민은행 to Excel,Korea accounting automation'
    },
    {
        'filename': 'smbc-bank-statement-v2.html',
        'name': 'Sumitomo Mitsui',
        'full_name': 'Sumitomo Mitsui Banking Corporation',
        'country': 'Japan',
        'currency': 'JPY',
        'symbol': '¥',
        'monthly': '926',
        'annual': '11,112',
        'extra': '10',
        'brand_start': '#00A74F',
        'brand_end': '#008C3F',
        'businesses': '90K+',
        'title': 'SMBC Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy',
        'description': 'AI-powered Sumitomo Mitsui statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ¥926/month | 90K+ Japanese businesses',
        'keywords': 'SMBC statement,Sumitomo Mitsui converter,三井住友 to Excel,Japan banking automation'
    },
    {
        'filename': 'shinhan-bank-statement-v2.html',
        'name': 'Shinhan Bank',
        'full_name': 'Shinhan Bank',
        'country': 'South Korea',
        'currency': 'KRW',
        'symbol': '₩',
        'monthly': '7,998',
        'annual': '95,976',
        'extra': '80',
        'brand_start': '#0046AB',
        'brand_end': '#003A8C',
        'businesses': '70K+',
        'title': 'Shinhan Bank Statement Converter | PDF to Excel | 98% Accuracy',
        'description': 'AI-powered Shinhan Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ₩7,998/month | 70K+ Korean businesses',
        'keywords': 'Shinhan Bank statement,신한은행 converter,Korean bank to Excel,K-IFRS automation'
    },
    {
        'filename': 'mizuho-bank-statement-v2.html',
        'name': 'Mizuho Bank',
        'full_name': 'Mizuho Bank',
        'country': 'Japan',
        'currency': 'JPY',
        'symbol': '¥',
        'monthly': '926',
        'annual': '11,112',
        'extra': '10',
        'brand_start': '#005BAC',
        'brand_end': '#004A8C',
        'businesses': '85K+',
        'title': 'Mizuho Bank Statement Converter | PDF to Excel | 98% Accuracy',
        'description': 'AI-powered Mizuho Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ¥926/month | 85K+ Japanese businesses',
        'keywords': 'Mizuho Bank statement,みずほ銀行 converter,Japanese bank to Excel,Japan accounting'
    },
    {
        'filename': 'hana-bank-statement-v2.html',
        'name': 'Hana Bank',
        'full_name': 'Hana Bank',
        'country': 'South Korea',
        'currency': 'KRW',
        'symbol': '₩',
        'monthly': '7,998',
        'annual': '95,976',
        'extra': '80',
        'brand_start': '#008C95',
        'brand_end': '#007075',
        'businesses': '65K+',
        'title': 'Hana Bank Statement Converter | PDF to Excel | 98% Accuracy',
        'description': 'AI-powered Hana Bank statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds. ₩7,998/month | 65K+ Korean businesses',
        'keywords': 'Hana Bank statement,하나은행 converter,Korean bank to Excel,Korea accounting automation'
    }
]

print("🚀 亚洲Batch 1: 日本+韩国银行页面")
print(f"📊 总计: {len(BANKS)} 个银行\n")

for i, bank in enumerate(BANKS, 1):
    country_flag = '🇯🇵' if bank['country'] == 'Japan' else '🇰🇷'
    print(f"{i}. {bank['name']} {country_flag} - {bank['filename']}")

print(f"\n✅ 配置完成，准备生成页面...")
