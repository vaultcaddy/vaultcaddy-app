#!/usr/bin/env python3
"""批量创建新西兰、新加坡、爱尔兰版SEO文章"""
import os, re

# 地区配置
REGIONS = {
    'en-nz': {
        'name': 'New Zealand',
        'currency': 'NZD $9.99',
        'currency_extra': 'NZD $0.09',
        'banks': ['ANZ New Zealand', 'ASB', 'Westpac NZ', 'BNZ'],
        'cities': ['Auckland', 'Wellington', 'Christchurch'],
        'tax': 'IRD',
        'regulator': 'FMA',
        'payment': 'EFTPOS/POLi',
        'labor_rate': 'NZD $75/hr',
    },
    'en-sg': {
        'name': 'Singapore',
        'currency': 'SGD $7.99',
        'currency_extra': 'SGD $0.08',
        'banks': ['DBS', 'OCBC', 'UOB', 'Maybank Singapore'],
        'cities': ['Singapore CBD', 'Jurong', 'Orchard'],
        'tax': 'IRAS',
        'regulator': 'MAS',
        'payment': 'PayNow/FAST',
        'labor_rate': 'SGD $80/hr',
    },
    'en-ie': {
        'name': 'Ireland',
        'currency': '€5.99',
        'currency_extra': '€0.05',
        'banks': ['AIB', 'Bank of Ireland', 'Permanent TSB', 'Ulster Bank'],
        'cities': ['Dublin', 'Cork', 'Galway'],
        'tax': 'Revenue Commissioners',
        'regulator': 'Central Bank of Ireland',
        'payment': 'SEPA/instant payments',
        'labor_rate': '€65/hr',
    }
}

def localize_to_region(content, filename, region_code, region_info):
    """本地化内容到特定地区"""
    
    # 1. HTML lang
    content = re.sub(r'<html lang="en-[A-Z]{2}">', f'<html lang="{region_code}">', content)
    
    # 2. URL路径
    for old in ['/en/blog/', '/en-us/blog/', '/en-gb/blog/', '/en-ca/blog/', '/en-au/blog/']:
        content = content.replace(old, f'/{region_code}/blog/')
    for old in ['../../en/', '../../en-us/', '../../en-gb/', '../../en-ca/', '../../en-au/']:
        content = content.replace(old, f'../../{region_code}/')
    
    # 3. Title
    content = re.sub(r'<title>(.*?)\((US|UK|GB|CA|Canada|AU|Australia)\)(.*?)</title>', 
                    f'<title>\\1({region_info["name"]})\\3</title>', content)
    
    # 4. 货币转换
    currency_map = {
        r'AUD \$8\.99': region_info['currency'],
        r'AUD \$12\.99': f'{region_info["currency"][:3]} ${float(region_info["currency"].split("$")[1]) * 1.5:.2f}',
        r'AUD \$0\.09': region_info['currency_extra'],
        r'\$8\.99': region_info['currency'],
    }
    for old, new in currency_map.items():
        content = re.sub(old, new, content)
    
    # 5. 银行替换
    bank_map = {
        'Commonwealth Bank': region_info['banks'][0],
        'Westpac': region_info['banks'][1],
        'ANZ': region_info['banks'][2],
        'NAB': region_info['banks'][3],
        '100+ Australian banks': f'100+ {region_info["name"]} banks',
        'Australian banks': f'{region_info["name"]} banks',
    }
    for old, new in bank_map.items():
        content = content.replace(old, new)
    
    # 6. 支付方式
    content = content.replace('BPAY/NPP', region_info['payment'])
    content = content.replace('BPAY', region_info['payment'].split('/')[0])
    content = content.replace('NPP', region_info['payment'].split('/')[1])
    
    # 7. 地点
    location_map = {
        'Australia': region_info['name'],
        'Australian': region_info['name'],
        'Sydney': region_info['cities'][0],
        'Sydney CBD': region_info['cities'][0],
        'Melbourne': region_info['cities'][1],
        'Brisbane': region_info['cities'][2],
    }
    for old, new in location_map.items():
        content = content.replace(old, new)
    
    # 8. 法规
    reg_map = {
        'ATO': region_info['tax'],
        'Australian Taxation Office': region_info['tax'],
        'APRA': region_info['regulator'],
        'Australian Prudential Regulation Authority': region_info['regulator'],
    }
    for old, new in reg_map.items():
        content = content.replace(old, new)
    
    # 9. 劳动成本
    content = content.replace('AUD $70/hr', region_info['labor_rate'])
    
    # 10. 银行代码（特殊处理）
    if region_code == 'en-nz':
        content = content.replace('BSB (6-digit)', 'Account Number (15-16 digits)')
        content = content.replace('BSB', 'Account Number')
    elif region_code == 'en-sg':
        content = content.replace('BSB (6-digit)', 'Bank Code (4 digits) + Branch Code (3 digits)')
        content = content.replace('BSB', 'Bank/Branch Code')
    elif region_code == 'en-ie':
        content = content.replace('BSB (6-digit)', 'IBAN (22 characters)')
        content = content.replace('BSB', 'IBAN/BIC')
    
    # 11. 案例
    case_map = {
        'Sydney Accounting Firm': f'{region_info["cities"][0]} Accounting Firm',
        'Melbourne restaurant': f'{region_info["cities"][1]} restaurant',
        'Brisbane restaurant': f'{region_info["cities"][2]} restaurant',
    }
    for old, new in case_map.items():
        content = content.replace(old, new)
    
    # 12. Meta
    locale_map = {'en-nz': 'en_NZ', 'en-sg': 'en_SG', 'en-ie': 'en_IE'}
    content = re.sub(r'<meta property="og:locale" content="[^"]*">', 
                    f'<meta property="og:locale" content="{locale_map[region_code]}">', content)
    content = re.sub(r'"inLanguage": "[^"]*"', f'"inLanguage": "{region_code}"', content)
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    
    files = [
        'vaultcaddy-vs-dext-comparison-2025.html',
        'how-to-convert-bank-statements-to-excel-2025.html',
        'top-10-accounting-software-2025.html',
        'vaultcaddy-vs-expensify-comparison-2025.html',
        'pdf-bank-statement-cannot-copy-text-solutions-2025.html',
        'quickbooks-import-bank-statement-error-fix-2025.html',
        'vaultcaddy-vs-quickbooks-comparison-2025.html',
        'restaurant-accounting-system-guide-2025.html',
        'manual-data-entry-vs-ai-automation-2025.html',
        'bank-statement-ocr-guide-2025.html',
    ]
    
    print("=" * 70)
    print("🌍 批量创建新西兰、新加坡、爱尔兰版SEO文章")
    print("=" * 70)
    
    total_success = 0
    for region_code, region_info in REGIONS.items():
        flag = {'en-nz': '🇳🇿', 'en-sg': '🇸🇬', 'en-ie': '🇮🇪'}[region_code]
        print(f"\n{flag} {region_info['name']} ({region_code})")
        
        target_dir = os.path.join(base_dir, region_code, 'blog')
        os.makedirs(target_dir, exist_ok=True)
        
        success = 0
        for filename in files:
            try:
                with open(os.path.join(en_blog_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                content = localize_to_region(content, filename, region_code, region_info)
                with open(os.path.join(target_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(content)
                success += 1
            except Exception as e:
                print(f"  ❌ {filename}: {e}")
        
        print(f"  ✅ 成功: {success}/{len(files)}")
        total_success += success
    
    print("\n" + "=" * 70)
    print(f"✅ 总计: {total_success}/{len(files) * 3}")
    print("=" * 70)
    print("🎉 Phase 5-7 完成！")
    print(f"   🇳🇿 新西兰: {REGIONS['en-nz']['currency']}/month, {', '.join(REGIONS['en-nz']['banks'][:2])}")
    print(f"   🇸🇬 新加坡: {REGIONS['en-sg']['currency']}/month, {', '.join(REGIONS['en-sg']['banks'][:2])}")
    print(f"   🇮🇪 爱尔兰: {REGIONS['en-ie']['currency']}/month, {', '.join(REGIONS['en-ie']['banks'][:2])}")

if __name__ == "__main__":
    main()

