#!/usr/bin/env python3
"""批量创建加拿大版SEO文章"""
import os, re

def localize_to_ca(content, filename):
    # 1. HTML lang
    content = content.replace('<html lang="en">', '<html lang="en-CA">')
    content = re.sub(r'<html lang="en-[A-Z]{2}">', '<html lang="en-CA">', content)
    
    # 2. URL路径
    for old in ['/en/blog/', '/en-us/blog/', '/en-gb/blog/']:
        content = content.replace(old, '/en-ca/blog/')
    for old in ['../../en/', '../../en-us/', '../../en-gb/']:
        content = content.replace(old, '../../en-ca/')
    
    # 3. Hreflang
    if 'hreflang' in content:
        content = re.sub(r'hreflang="en-[^"]+"\s+href="[^"]+/en-[^/]+/', 
                        'hreflang="en-ca" href="https://vaultcaddy.com/en-ca/', content)
    
    # 4. Title
    content = re.sub(r'<title>(.*?)\((US|UK|GB)\)(.*?)</title>', r'<title>\1(CA)\3</title>', content)
    content = re.sub(r'<title>(.*?)</title>', 
                    lambda m: f'<title>{m.group(1)} (Canada)</title>' if '(CA)' not in m.group(1) and '(Canada)' not in m.group(1) else m.group(0), content)
    
    # 5. 货币 USD/GBP → CAD
    currency_map = {
        r'£4\.99': 'CAD $7.99', r'£7\.49': 'CAD $11.99', r'£9\.99': 'CAD $14.99', r'£14\.99': 'CAD $23.99',
        r'£0\.05': 'CAD $0.08', r'£39': 'CAD $59', r'£125': 'CAD $189', r'£395': 'CAD $595', r'£995': 'CAD $1,499',
        r'£45/hr': 'CAD $60/hr', r'£40/hr': 'CAD $50/hr',
        r'\$5\.59': 'CAD $7.99', r'\$8\.59': 'CAD $11.99', r'\$11\.59': 'CAD $14.99', r'\$17\.59': 'CAD $23.99',
        r'\$0\.06': 'CAD $0.08', r'\$46': 'CAD $59', r'\$149': 'CAD $189', r'\$468': 'CAD $595', r'\$1,188': 'CAD $1,499',
        r'\$60/hr': 'CAD $60/hr', r'\$50/hr': 'CAD $50/hr',
    }
    for old, new in currency_map.items():
        content = re.sub(old, new, content)
    
    # 6. 银行
    bank_map = {
        'Barclays': 'RBC', 'Lloyds Bank': 'TD Canada Trust', 'Lloyds': 'TD', 'HSBC UK': 'Scotiabank',
        'NatWest': 'BMO', 'Santander UK': 'CIBC', 'Nationwide': 'Desjardins', 'TSB Bank': 'Tangerine',
        'Metro Bank': 'Simplii Financial', 'Chase': 'RBC', 'Bank of America': 'TD Canada Trust',
        'BofA': 'TD', 'Wells Fargo': 'Scotiabank', 'Citibank': 'BMO', 'Citi': 'BMO',
        '100+ UK banks': '100+ Canadian banks', '50+ US banks': '100+ Canadian banks',
        'UK banks': 'Canadian banks', 'US banks': 'Canadian banks', 'British banks': 'Canadian banks',
    }
    for old, new in bank_map.items():
        content = content.replace(old, new)
    
    # 7. 支付
    payment_map = {
        'Direct Debit/Standing Order/BACS/Faster Payments': 'Interac e-Transfer/Pre-authorized Debit/EFT',
        'BACS/Faster Payments/PayPal': 'Interac e-Transfer/EFT',
        'BACS transfer': 'EFT', 'BACS': 'EFT', 'Faster Payments': 'Interac e-Transfer',
        'Direct Debit': 'Pre-authorized Debit', 'Standing Order': 'Recurring Payment',
        'ACH/Wire/Check/Zelle/Venmo': 'Interac e-Transfer/Wire/Cheque/EFT',
        'ACH': 'EFT', 'Zelle': 'Interac e-Transfer', 'Venmo': 'Interac e-Transfer',
    }
    for old, new in payment_map.items():
        content = content.replace(old, new)
    
    # 8. 地点
    location_map = {
        'United Kingdom': 'Canada', 'UK': 'Canadian', 'U.K.': 'Canada', 'British': 'Canadian', 'Britain': 'Canada',
        'United States': 'Canada', 'American': 'Canadian', 'America': 'Canada',
        'London': 'Toronto', 'Central London': 'Downtown Toronto', 'Manchester': 'Vancouver',
        'Birmingham': 'Montreal', 'Leeds': 'Calgary', 'Glasgow': 'Ottawa', 'Edinburgh': 'Edmonton',
        'Bristol': 'Winnipeg', 'New York': 'Toronto', 'Manhattan': 'Downtown Toronto',
        'Los Angeles': 'Vancouver', 'LA': 'Vancouver', 'Chicago': 'Montreal', 'San Francisco': 'Calgary',
        'UK timezone': 'Canadian timezone', 'US timezone': 'Canadian timezone', 
        'GMT/BST': 'EST/PST', 'EST/PST': 'ET/PT', '9am-5pm GMT': '9am-5pm ET',
    }
    for old, new in location_map.items():
        content = content.replace(old, new)
    
    # 9. 法规
    reg_map = {
        'HMRC compliant': 'CRA compliant', 'HMRC': 'CRA', 'HM Revenue & Customs': 'Canada Revenue Agency',
        'FCA regulated': 'OSFI regulated', 'FCA': 'OSFI', 'Financial Conduct Authority': 'Office of the Superintendent of Financial Institutions',
        'Companies House registered': 'Corporations Canada registered', 'Companies House': 'Corporations Canada',
        'UK GDPR': 'PIPEDA', 'FSCS protected': 'CDIC insured', 'FSCS': 'CDIC',
        'IRS compliant': 'CRA compliant', 'IRS': 'CRA', 'SOC2 certified': 'OSFI regulated',
        'US GAAP': 'Canadian GAAP', 'UK GAAP': 'Canadian GAAP', 'GAAP': 'Canadian GAAP',
        'FDIC': 'CDIC',
    }
    for old, new in reg_map.items():
        content = content.replace(old, new)
    
    # 10. 术语
    term_map = {
        'chartered accountant': 'accountant', 'Chartered Accountant': 'Accountant',
        'CPA': 'accountant', 'Certified Public Accountant': 'Chartered Professional Accountant',
    }
    for old, new in term_map.items():
        content = content.replace(old, new)
    
    # 11. 银行代码
    content = content.replace('Sort Code (XX-XX-XX format)', 'Transit Number (5-digit) + Institution Number (3-digit)')
    content = content.replace('Sort Code', 'Transit Number')
    content = content.replace('Routing Number', 'Transit Number')
    
    # 12. 案例
    case_map = {
        'Central London Accounting Firm': 'Toronto Accounting Firm',
        'London accounting firm': 'Toronto accounting firm',
        'Manchester restaurant': 'Vancouver restaurant',
        'Birmingham restaurant': 'Montreal restaurant',
    }
    for old, new in case_map.items():
        content = content.replace(old, new)
    
    # 13. Meta
    content = re.sub(r'<meta property="og:locale" content="[^"]*">', '<meta property="og:locale" content="en_CA">', content)
    content = re.sub(r'"inLanguage": "[^"]*"', '"inLanguage": "en-CA"', content)
    
    # 14. 拼写 (英式→美式，因为加拿大多用美式)
    spell_map = {
        'specialised': 'specialized', 'optimise': 'optimize', 'optimised': 'optimized',
        'organisation': 'organization', 'recognise': 'recognize', 'analyse': 'analyze',
        'centre': 'center', 'colour': 'color', 'labour': 'labor', 'favour': 'favor',
    }
    for old, new in spell_map.items():
        content = re.sub(r'\b' + old + r'\b', new, content, flags=re.IGNORECASE)
    
    # 15. 日期格式 (加拿大用YYYY-MM-DD或MM/DD/YYYY)
    content = content.replace('DD/MM/YYYY', 'YYYY-MM-DD')
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    en_ca_blog_dir = os.path.join(base_dir, 'en-ca', 'blog')
    os.makedirs(en_ca_blog_dir, exist_ok=True)
    
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
    print("🇨🇦 批量创建加拿大版SEO文章")
    print("=" * 70)
    print(f"📂 源: {en_blog_dir}")
    print(f"📂 目标: {en_ca_blog_dir}")
    print(f"📝 文章: {len(files)}")
    print("=" * 70)
    
    success = 0
    for filename in files:
        try:
            with open(os.path.join(en_blog_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            content = localize_to_ca(content, filename)
            with open(os.path.join(en_ca_blog_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            success += 1
        except Exception as e:
            print(f"❌ {filename}: {e}")
    
    print("=" * 70)
    print(f"✅ 成功: {success}/{len(files)}")
    print("=" * 70)
    print("🎉 加拿大版完成！")
    print("   ✅ CAD $7.99/month, CAD $0.08/page")
    print("   ✅ RBC, TD, Scotiabank, BMO")
    print("   ✅ Toronto, Vancouver, Montreal")
    print("   ✅ CRA, OSFI, CDIC, PIPEDA")
    print("   ✅ Interac e-Transfer, EFT")
    return success

if __name__ == "__main__":
    main()

