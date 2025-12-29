#!/usr/bin/env python3
"""创建爱尔兰版SEO文章（修复版）"""
import os, re

def localize_to_ie(content, filename):
    """本地化到爱尔兰"""
    
    # 1. HTML lang
    content = re.sub(r'<html lang="en-[A-Z]{2}">', '<html lang="en-IE">', content)
    
    # 2. URL路径
    for old in ['/en/blog/', '/en-us/blog/', '/en-gb/blog/', '/en-ca/blog/', '/en-au/blog/', '/en-nz/blog/', '/en-sg/blog/']:
        content = content.replace(old, '/en-ie/blog/')
    for old in ['../../en/', '../../en-us/', '../../en-gb/', '../../en-ca/', '../../en-au/', '../../en-nz/', '../../en-sg/']:
        content = content.replace(old, '../../en-ie/')
    
    # 3. Title
    content = re.sub(r'<title>(.*?)\((US|UK|GB|CA|Canada|AU|Australia|New Zealand|Singapore)\)(.*?)</title>', 
                    r'<title>\1(Ireland)\3</title>', content)
    
    # 4. 货币 AUD → EUR
    currency_map = {
        r'AUD \$8\.99': '€5.99',
        r'AUD \$12\.99': '€8.99',
        r'AUD \$16\.99': '€11.99',
        r'AUD \$0\.09': '€0.05',
        r'AUD \$65': '€45',
        r'AUD \$70/hr': '€65/hr',
        r'\$8\.99': '€5.99',
    }
    for old, new in currency_map.items():
        content = re.sub(old, new, content)
    
    # 5. 银行
    bank_map = {
        'Commonwealth Bank': 'AIB',
        'Westpac': 'Bank of Ireland',
        'ANZ': 'Permanent TSB',
        'NAB': 'Ulster Bank',
        '100+ Australian banks': '100+ Irish banks',
        'Australian banks': 'Irish banks',
    }
    for old, new in bank_map.items():
        content = content.replace(old, new)
    
    # 6. 支付
    content = content.replace('BPAY/NPP', 'SEPA/instant payments')
    content = content.replace('BPAY', 'SEPA')
    content = content.replace('NPP', 'instant payments')
    
    # 7. 地点
    location_map = {
        'Australia': 'Ireland',
        'Australian': 'Irish',
        'Sydney': 'Dublin',
        'Sydney CBD': 'Dublin',
        'Melbourne': 'Cork',
        'Brisbane': 'Galway',
        'Perth': 'Limerick',
        'Adelaide': 'Waterford',
    }
    for old, new in location_map.items():
        content = content.replace(old, new)
    
    # 8. 法规
    reg_map = {
        'ATO': 'Revenue Commissioners',
        'Australian Taxation Office': 'Revenue Commissioners',
        'APRA': 'Central Bank of Ireland',
        'ASIC': 'Companies Registration Office',
        'Australian Accounting Standards': 'Irish GAAP',
    }
    for old, new in reg_map.items():
        content = content.replace(old, new)
    
    # 9. 银行代码
    content = content.replace('BSB (6-digit)', 'IBAN (22 characters)')
    content = content.replace('BSB', 'IBAN/BIC')
    
    # 10. 案例
    case_map = {
        'Sydney Accounting Firm': 'Dublin Accounting Firm',
        'Melbourne restaurant': 'Cork restaurant',
        'Brisbane restaurant': 'Galway restaurant',
    }
    for old, new in case_map.items():
        content = content.replace(old, new)
    
    # 11. Meta
    content = re.sub(r'<meta property="og:locale" content="[^"]*">', 
                    '<meta property="og:locale" content="en_IE">', content)
    content = re.sub(r'"inLanguage": "[^"]*"', '"inLanguage": "en-IE"', content)
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    ie_blog_dir = os.path.join(base_dir, 'en-ie', 'blog')
    os.makedirs(ie_blog_dir, exist_ok=True)
    
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
    print("🇮🇪 创建爱尔兰版SEO文章")
    print("=" * 70)
    
    success = 0
    for filename in files:
        try:
            with open(os.path.join(en_blog_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            content = localize_to_ie(content, filename)
            with open(os.path.join(ie_blog_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filename}")
            success += 1
        except Exception as e:
            print(f"  ❌ {filename}: {e}")
    
    print("=" * 70)
    print(f"✅ 成功: {success}/{len(files)}")
    print("=" * 70)
    print("🎉 爱尔兰版完成！")
    print("   ✅ €5.99/month, AIB, Bank of Ireland")

if __name__ == "__main__":
    main()

