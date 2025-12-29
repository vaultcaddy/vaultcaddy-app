#!/usr/bin/env python3
"""
批量创建英国版SEO文章
将现有英文版文章本地化为英国版本
"""

import os
import re

def localize_to_gb(content, filename):
    """
    将内容本地化为英国版本
    """
    # 1. 更新HTML lang标签
    content = content.replace('<html lang="en">', '<html lang="en-GB">')
    content = content.replace('<html lang="en-US">', '<html lang="en-GB">')
    
    # 2. 更新URL路径
    content = content.replace('/en/blog/', '/en-gb/blog/')
    content = content.replace('/en-us/blog/', '/en-gb/blog/')
    content = content.replace('../../en/', '../../en-gb/')
    content = content.replace('../../en-us/', '../../en-gb/')
    content = content.replace('"../../en/', '"../../en-gb/')
    content = content.replace('href="../../en/', 'href="../../en-gb/')
    
    # 3. 添加hreflang标签
    if 'hreflang' not in content:
        og_position = content.find('<!-- Open Graph -->')
        if og_position != -1:
            hreflang_tags = '''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en-us" href="https://vaultcaddy.com/en-us/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="en-gb" href="https://vaultcaddy.com/en-gb/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="en" href="https://vaultcaddy.com/en/blog/''' + filename + '''" />
    <link rel="alternate" hreflang="x-default" href="https://vaultcaddy.com/en-us/blog/''' + filename + '''" />
    
'''
            content = content[:og_position] + hreflang_tags + content[og_position:]
    else:
        # 更新现有hreflang标签
        content = re.sub(
            r'<link rel="alternate" hreflang="en-us"([^>]+)>',
            r'<link rel="alternate" hreflang="en-gb"\1>',
            content
        )
    
    # 4. 更新Title和Meta（添加UK标识）
    content = re.sub(
        r'<title>(.*?)\(US\)(.*?)</title>',
        r'<title>\1(UK)\2</title>',
        content
    )
    content = re.sub(
        r'<title>(.*?)</title>',
        lambda m: f'<title>{m.group(1)} (UK)</title>' if '(UK)' not in m.group(1) and '(US)' not in m.group(1) else m.group(0),
        content
    )
    
    # 5. 更新meta description（添加UK相关内容）
    def update_description(m):
        desc = m.group(1)
        # 移除US相关内容
        desc = re.sub(r'IRS compliant,?\s*', '', desc)
        desc = re.sub(r'SOC2 certified,?\s*', '', desc)
        desc = re.sub(r'US banks.*?\)', '', desc)
        desc = re.sub(r'\(Chase.*?Citibank\)', '', desc)
        # 添加UK相关内容
        if "HMRC" not in desc and "UK" not in desc:
            desc += " HMRC compliant, FCA regulated. Optimized for UK banks (Barclays, Lloyds, HSBC UK, NatWest)."
        return f'<meta name="description" content="{desc}">'
    
    content = re.sub(
        r'<meta name="description" content="(.*?)">',
        update_description,
        content
    )
    
    # 6. 更新keywords（添加UK关键词）
    def update_keywords(m):
        keywords = m.group(1)
        # 移除US关键词
        keywords = re.sub(r',?US accounting,?', '', keywords)
        keywords = re.sub(r',?IRS compliant,?', '', keywords)
        keywords = re.sub(r',?Chase bank,?', '', keywords)
        keywords = re.sub(r',?Bank of America,?', '', keywords)
        keywords = re.sub(r',?Wells Fargo,?', '', keywords)
        keywords = re.sub(r',?Citibank,?', '', keywords)
        # 添加UK关键词
        if "UK accounting" not in keywords:
            keywords += ",UK accounting,HMRC compliant,Barclays bank,Lloyds bank,HSBC UK,NatWest,FCA regulated"
        return f'<meta name="keywords" content="{keywords}">'
    
    content = re.sub(
        r'<meta name="keywords" content="(.*?)">',
        update_keywords,
        content
    )
    
    # 7. 货币: USD → GBP
    # 价格转换
    currency_conversions = {
        r'\$5\.59': '£4.99',
        r'\$8\.59': '£7.49',
        r'\$11\.59': '£9.99',
        r'\$17\.59': '£14.99',
        r'\$0\.06': '£0.05',
        r'\$46': '£39',
        r'\$66': '£55',
        r'\$149': '£125',
        r'\$468': '£395',
        r'\$708': '£595',
        r'\$1,188': '£995',
        r'\$60/hr': '£45/hr',
        r'\$50/hr': '£40/hr',
        # 大额金额
        r'\$3,444': '£2,899',
        r'\$3,468': '£2,919',
        r'\$6,000': '£5,050',
        r'\$7,200': '£6,060',
        r'\$7,890': '£6,640',
        r'\$8,388': '£7,060',
        r'\$15': '£12.50',
        r'\$20': '£16.50',
        r'\$23\.59': '£19.99',
        r'\$497\.59': '£418',
    }
    
    for usd_pattern, gbp_value in currency_conversions.items():
        content = re.sub(usd_pattern, gbp_value, content)
    
    # 通用USD到GBP符号替换（保留其他数字）
    # content = content.replace('$', '£')  # 太广泛，先不用
    
    # 8. 银行: 美国银行 → 英国银行
    us_banks_to_uk = {
        'Chase Bank': 'Barclays',
        'Chase': 'Barclays',
        'Bank of America': 'Lloyds Bank',
        'BofA': 'Lloyds',
        'Wells Fargo': 'HSBC UK',
        'Citibank': 'NatWest',
        'Citi': 'NatWest',
        'US Bank': 'Santander UK',
        'TD Bank': 'Nationwide',
        'PNC Bank': 'TSB Bank',
        'Capital One': 'Metro Bank',
        'Truist Bank': 'Co-operative Bank',
        'Fifth Third Bank': 'Yorkshire Bank',
        '50+ US banks': '100+ UK banks',
        'US banks': 'UK banks',
        'US bank': 'UK bank',
        'American banks': 'British banks',
        'JPMorgan Chase': 'Barclays',
    }
    
    for us_bank, uk_bank in us_banks_to_uk.items():
        content = content.replace(us_bank, uk_bank)
    
    # 9. 支付方式: 美国 → 英国
    payment_conversions = {
        'ACH/Wire/Check/Zelle/Venmo': 'Direct Debit/Standing Order/BACS/Faster Payments',
        'ACH/Zelle/Venmo': 'Direct Debit/BACS/Faster Payments',
        'ACH/Wire/Check': 'Direct Debit/Standing Order/BACS',
        'ACH transfer': 'BACS transfer',
        'ACH': 'BACS',
        'Zelle': 'Faster Payments',
        'Venmo': 'PayPal',
        'wire transfer': 'bank transfer',
        'check number': 'cheque number',
        'check': 'cheque',
    }
    
    for us_payment, uk_payment in payment_conversions.items():
        content = content.replace(us_payment, uk_payment)
    
    # 10. 地点: 美国 → 英国
    us_locations_to_uk = {
        'United States': 'United Kingdom',
        'US ': 'UK ',
        'U.S.': 'U.K.',
        'American': 'British',
        'America': 'Britain',
        'New York': 'London',
        'Manhattan': 'Central London',
        'Los Angeles': 'Manchester',
        'LA': 'Manchester',
        'Chicago': 'Birmingham',
        'San Francisco': 'Leeds',
        'Boston': 'Glasgow',
        'Seattle': 'Edinburgh',
        'Miami': 'Bristol',
        'US timezone': 'UK timezone',
        'EST/PST': 'GMT/BST',
        '9am-6pm EST/PST': '9am-5pm GMT',
    }
    
    for us_location, uk_location in us_locations_to_uk.items():
        content = content.replace(us_location, uk_location)
    
    # 11. 法规: 美国 → 英国
    regulation_conversions = {
        'IRS compliant': 'HMRC compliant',
        'IRS': 'HMRC',
        'SOC2 certified': 'FCA regulated',
        'SOC2': 'FCA',
        'US GAAP': 'UK GAAP',
        'GAAP': 'UK GAAP',
        'FDIC-insured': 'FCA-regulated',
        'FDIC': 'FSCS',
        'US regulatory': 'UK regulatory',
        'federal': 'national',
        'Internal Revenue Service': 'HM Revenue & Customs',
    }
    
    for us_reg, uk_reg in regulation_conversions.items():
        content = content.replace(us_reg, uk_reg)
    
    # 添加UK特定法规提及
    if 'Companies House' not in content and 'HMRC' in content:
        content = re.sub(
            r'(HMRC compliant)',
            r'\1, Companies House registered',
            content,
            count=1
        )
    
    # 12. 术语: CPA → Chartered Accountant
    terminology_conversions = {
        'CPA firm': 'accounting firm',
        'CPA': 'chartered accountant',
        'CPAs': 'chartered accountants',
        'Certified Public Accountant': 'Chartered Accountant',
        'accounting professional': 'accountant',
    }
    
    for us_term, uk_term in terminology_conversions.items():
        content = content.replace(us_term, uk_term)
    
    # 13. 案例研究本地化
    case_study_conversions = {
        'Manhattan CPA Firm': 'Central London Accounting Firm',
        'New York CPA firm': 'London accounting firm',
        'Los Angeles restaurant': 'Manchester restaurant',
        'Chicago restaurant': 'Birmingham restaurant',
        'San Francisco': 'Leeds',
    }
    
    for us_case, uk_case in case_study_conversions.items():
        content = content.replace(us_case, uk_case)
    
    # 14. Open Graph locale
    content = re.sub(
        r'<meta property="og:locale" content="en_US">',
        '<meta property="og:locale" content="en_GB">',
        content
    )
    if 'og:locale' not in content:
        content = re.sub(
            r'(<meta property="og:image".*?>)',
            r'\1\n    <meta property="og:locale" content="en_GB">',
            content
        )
    
    # 15. Schema标记 - 更新inLanguage
    content = re.sub(
        r'"inLanguage": "en-US"',
        '"inLanguage": "en-GB"',
        content
    )
    if '"dateModified"' in content and '"inLanguage"' not in content:
        content = content.replace(
            '"dateModified": "2025-12-28"',
            '"dateModified": "2025-12-28",\n        "inLanguage": "en-GB"'
        )
    
    # 16. Footer更新
    content = re.sub(
        r'AI-powered document processing platform for US businesses.*?IRS compliant, SOC2 certified\.',
        'AI-powered document processing platform for UK businesses. 90% cheaper than competitors, 200x faster, specialized for UK banks (Barclays, Lloyds, HSBC UK, NatWest). 3-second processing, 98% accuracy. HMRC compliant, FCA regulated.',
        content
    )
    
    # 17. 标题更新
    def update_h1_uk(m):
        title = m.group(1)
        title = title.replace(' for US Businesses', ' for UK Businesses')
        title = title.replace(' (US)', ' (UK)')
        title = title.replace(' for American', ' for British')
        if 'UK' not in title and 'British' not in title and '?' in title:
            return f'<h1>{title} for UK Businesses?</h1>'
        return f'<h1>{title}</h1>'
    
    content = re.sub(
        r'<h1>(.*?)</h1>',
        update_h1_uk,
        content
    )
    
    # 18. 银行代码系统
    bank_code_conversions = {
        'routing number': 'sort code',
        'Routing Number': 'Sort Code',
        'account number': 'account number',  # 保持不变
        'Account Number': 'Account Number',
    }
    
    for us_code, uk_code in bank_code_conversions.items():
        content = content.replace(us_code, uk_code)
    
    # 添加Sort Code说明
    if 'Sort Code' in content and 'XX-XX-XX' not in content:
        content = re.sub(
            r'(Sort Code)',
            r'\1 (XX-XX-XX format)',
            content,
            count=1
        )
    
    # 19. 日期格式提及
    if 'MM/DD/YYYY' in content:
        content = content.replace('MM/DD/YYYY', 'DD/MM/YYYY')
    
    # 20. 拼写: 美式英语 → 英式英语
    spelling_conversions = {
        'specialized': 'specialised',
        'optimize': 'optimise',
        'optimized': 'optimised',
        'organization': 'organisation',
        'organizations': 'organisations',
        'recognize': 'recognise',
        'recognized': 'recognised',
        'analyze': 'analyse',
        'analyzed': 'analysed',
        'center': 'centre',
        'color': 'colour',
        'labor': 'labour',
        'favor': 'favour',
    }
    
    for us_spelling, uk_spelling in spelling_conversions.items():
        # 使用单词边界避免部分匹配
        content = re.sub(r'\b' + us_spelling + r'\b', uk_spelling, content, flags=re.IGNORECASE)
    
    # 21. 添加UK特定提及
    if 'UK banks' in content and 'Sort Code' not in content:
        content = re.sub(
            r'(UK banks.*?)',
            r'\1 Supporting UK-specific formats including Sort Code and account number validation.',
            content,
            count=1
        )
    
    return content

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    en_blog_dir = os.path.join(base_dir, 'en', 'blog')
    en_gb_blog_dir = os.path.join(base_dir, 'en-gb', 'blog')
    
    # 确保目标目录存在
    os.makedirs(en_gb_blog_dir, exist_ok=True)
    
    # 要处理的文件列表
    files_to_process = [
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
    print("🇬🇧 批量创建英国版SEO文章")
    print("=" * 70)
    print(f"📂 源目录: {en_blog_dir}")
    print(f"📂 目标目录: {en_gb_blog_dir}")
    print(f"📝 待处理文章: {len(files_to_process)}")
    print("=" * 70)
    
    success_count = 0
    error_count = 0
    
    for filename in files_to_process:
        try:
            source_file = os.path.join(en_blog_dir, filename)
            target_file = os.path.join(en_gb_blog_dir, filename)
            
            # 检查源文件是否存在
            if not os.path.exists(source_file):
                print(f"⚠️  {filename} - 源文件不存在，跳过")
                error_count += 1
                continue
            
            # 读取源文件
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 本地化内容
            localized_content = localize_to_gb(content, filename)
            
            # 写入目标文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(localized_content)
            
            print(f"✅ {filename} - 创建成功")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {filename} - 错误: {str(e)}")
            error_count += 1
    
    print("=" * 70)
    print("📊 处理完成统计")
    print("=" * 70)
    print(f"✅ 成功: {success_count}/{len(files_to_process)}")
    print(f"❌ 失败: {error_count}/{len(files_to_process)}")
    print("=" * 70)
    
    if success_count > 0:
        print("\n🎉 英国版SEO文章创建完成！")
        print("\n📝 关键本地化修改:")
        print("   ✅ HTML lang: en/en-US → en-GB")
        print("   ✅ 货币: USD ($5.59) → GBP (£4.99)")
        print("   ✅ 银行: Chase/BofA/Wells Fargo → Barclays/Lloyds/HSBC UK/NatWest")
        print("   ✅ 地点: New York/LA → London/Manchester/Birmingham")
        print("   ✅ 法规: IRS/SOC2 → HMRC/FCA/Companies House")
        print("   ✅ 支付: ACH/Zelle/Venmo → BACS/Faster Payments/PayPal")
        print("   ✅ 术语: CPA → Chartered Accountant")
        print("   ✅ 银行代码: Routing Number → Sort Code (XX-XX-XX)")
        print("   ✅ 日期: MM/DD/YYYY → DD/MM/YYYY")
        print("   ✅ 拼写: 美式英语 → 英式英语")
        print("   ✅ 劳动成本: $60/hr → £45/hr")
        print("   ✅ 案例: 美国案例 → 英国案例")
    
    if error_count > 0:
        print(f"\n⚠️  {error_count} 个文件处理失败，请检查错误信息")
    
    return success_count, error_count

if __name__ == "__main__":
    success, errors = main()
    exit(0 if errors == 0 else 1)

