#!/usr/bin/env python3
"""批量创建澳大利亚版SEO文章"""
import os, re

def localize_to_au(content, filename):
    # 1. HTML lang
    content = content.replace('<html lang="en">', '<html lang="en-AU">')
    content = re.sub(r'<html lang="en-[A-Z]{2}">', '<html lang="en-AU">', content)
    
    # 2. URL路径
    for old in ['/en/blog/', '/en-us/blog/', '/en-gb/blog/', '/en-ca/blog/']:
        content = content.replace(old, '/en-au/blog/')
    for old in ['../../en/', '../../en-us/', '../../en-gb/', '../../en-ca/']:
        content = content.replace(old, '../../en-au/')
    
    # 3. Hreflang
    if 'hreflang' in content:
        content = re.sub(r'hreflang="en-[^"]+"\s+href="[^"]+/en-[^/]+/', 
                        'hreflang="en-au" href="https://vaultcaddy.com/en-au/', content)
    
    # 4. Title
    content = re.sub(r'<title>(.*?)\((US|UK|GB|CA|Canada)\)(.*?)</title>', r'<title>\1(AU)\3</title>', content)
    content = re.sub(r'<title>(.*?)</title>', 
                    lambda m: f'<title>{m.group(1)} (Australia)</title>' if '(AU)' not in m.group(1) and '(Australia)' not in m.group(1) else m.group(0), content)
    
    # 5. 货币 → AUD
    currency_map = {
        r'CAD \$7\.99': 'AUD $8.99', r'CAD \$11\.99': 'AUD $12.99', r'CAD \$14\.99': 'AUD $16.99',
        r'CAD \$23\.99': 'AUD $26.99', r'CAD \$0\.08': 'AUD $0.09', r'CAD \$59': 'AUD $65',
        r'CAD \$189': 'AUD $209', r'CAD \$595': 'AUD $659', r'CAD \$1,499': 'AUD $1,659',
        r'CAD \$60/hr': 'AUD $70/hr', r'CAD \$50/hr': 'AUD $60/hr',
        r'\$5\.59': 'AUD $8.99', r'\$8\.59': 'AUD $12.99', r'\$11\.59': 'AUD $16.99',
        r'\$0\.06': 'AUD $0.09', r'\$46': 'AUD $65', r'\$149': 'AUD $209', r'\$468': 'AUD $659',
    }
    for old, new in currency_map.items():
        content = re.sub(old, new, content)
    
    # 6. 银行
    bank_map = {
        'RBC': 'Commonwealth Bank', 'TD Canada Trust': 'Westpac', 'TD': 'Westpac',
        'Scotiabank': 'ANZ', 'BMO': 'NAB', 'CIBC': 'Bendigo Bank', 'Desjardins': 'Suncorp',
        'Tangerine': 'ING Direct', 'Simplii Financial': 'Bank of Melbourne',
        'Barclays': 'Commonwealth Bank', 'Lloyds Bank': 'Westpac', 'Lloyds': 'Westpac',
        'HSBC UK': 'ANZ', 'NatWest': 'NAB', 'Chase': 'Commonwealth Bank',
        'Bank of America': 'Westpac', 'Wells Fargo': 'ANZ', 'Citibank': 'NAB',
        '100+ Canadian banks': '100+ Australian banks', '100+ UK banks': '100+ Australian banks',
        '50+ US banks': '100+ Australian banks', 'Canadian banks': 'Australian banks',
        'UK banks': 'Australian banks', 'US banks': 'Australian banks',
    }
    for old, new in bank_map.items():
        content = content.replace(old, new)
    
    # 7. 支付
    payment_map = {
        'Interac e-Transfer/Pre-authorized Debit/EFT': 'BPAY/Direct Debit/NPP',
        'Interac e-Transfer/EFT': 'BPAY/NPP', 'Interac e-Transfer': 'BPAY',
        'EFT': 'NPP', 'Pre-authorized Debit': 'Direct Debit',
        'Recurring Payment': 'Periodical Payment',
        'cheque': 'cheque', 'Cheque': 'Cheque',  # 澳洲也用cheque
    }
    for old, new in payment_map.items():
        content = content.replace(old, new)
    
    # 8. 地点
    location_map = {
        'Canada': 'Australia', 'Canadian': 'Australian',
        'Toronto': 'Sydney', 'Downtown Toronto': 'Sydney CBD', 'Vancouver': 'Melbourne',
        'Montreal': 'Brisbane', 'Calgary': 'Perth', 'Ottawa': 'Adelaide', 'Edmonton': 'Canberra',
        'Winnipeg': 'Hobart', 'London': 'Sydney', 'Manchester': 'Melbourne', 'Birmingham': 'Brisbane',
        'New York': 'Sydney', 'Los Angeles': 'Melbourne', 'Chicago': 'Brisbane',
        'Canadian timezone': 'Australian timezone', 'ET/PT': 'AEST/AEDT',
        '9am-5pm ET': '9am-5pm AEST',
    }
    for old, new in location_map.items():
        content = content.replace(old, new)
    
    # 9. 法规
    reg_map = {
        'CRA compliant': 'ATO compliant', 'CRA': 'ATO', 'Canada Revenue Agency': 'Australian Taxation Office',
        'OSFI regulated': 'APRA regulated', 'OSFI': 'APRA',
        'Office of the Superintendent of Financial Institutions': 'Australian Prudential Regulation Authority',
        'Corporations Canada registered': 'ASIC registered', 'Corporations Canada': 'ASIC',
        'PIPEDA': 'Privacy Act', 'CDIC insured': 'ADI protected', 'CDIC': 'ADI',
        'Canadian GAAP': 'Australian Accounting Standards', 'GAAP': 'Australian Accounting Standards',
    }
    for old, new in reg_map.items():
        content = content.replace(old, new)
    
    # 10. 术语 (澳洲用美式拼写但保留一些英式术语)
    # 保持美式拼写 (已在加拿大版转换)
    
    # 11. 银行代码
    content = content.replace('Transit Number (5-digit) + Institution Number (3-digit)', 'BSB (6-digit)')
    content = content.replace('Transit Number', 'BSB')
    content = content.replace('Sort Code', 'BSB')
    
    # 12. 案例
    case_map = {
        'Toronto Accounting Firm': 'Sydney Accounting Firm',
        'Toronto accounting firm': 'Sydney accounting firm',
        'Vancouver restaurant': 'Melbourne restaurant',
        'Montreal restaurant': 'Brisbane restaurant',
    }
    for old, new in case_map.items():
        content = content.replace(old, new)
    
    # 13. Meta
    content = re.sub(r'<meta property="og:locale" content="[^"]*">', '<meta property="og:locale" content="en_AU">', content)
    content = re.sub(r'"inLanguage": "[^"]*"', '"inLanguage": "en-AU"', content)
    
    # 14. 日期格式 (澳洲用DD/MM/YYYY)
    content = content.replace('YYYY-MM-DD', 'DD/MM/YYYY')
    content = content.replace('MM/DD/YYYY', 'DD/MM/YYYY')
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    en_au_blog_dir = os.path.join(base_dir, 'en-au', 'blog')
    os.makedirs(en_au_blog_dir, exist_ok=True)
    
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
    print("🇦🇺 批量创建澳大利亚版SEO文章")
    print("=" * 70)
    print(f"📂 源: {en_blog_dir}")
    print(f"📂 目标: {en_au_blog_dir}")
    print(f"📝 文章: {len(files)}")
    print("=" * 70)
    
    success = 0
    for filename in files:
        try:
            with open(os.path.join(en_blog_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            content = localize_to_au(content, filename)
            with open(os.path.join(en_au_blog_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            success += 1
        except Exception as e:
            print(f"❌ {filename}: {e}")
    
    print("=" * 70)
    print(f"✅ 成功: {success}/{len(files)}")
    print("=" * 70)
    print("🎉 澳大利亚版完成！")
    print("   ✅ AUD $8.99/month, AUD $0.09/page")
    print("   ✅ Commonwealth, Westpac, ANZ, NAB")
    print("   ✅ Sydney, Melbourne, Brisbane")
    print("   ✅ ATO, APRA, ASIC, ADI")
    print("   ✅ BPAY, NPP, Direct Debit")
    return success

if __name__ == "__main__":
    main()

