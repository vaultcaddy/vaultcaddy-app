#!/usr/bin/env python3
"""
批量升级所有-v2.html页面到完整SEO优化模板
添加：Schema.org、Open Graph、详细meta标签、FAQ结构化数据
"""

import os
import re
from pathlib import Path

def has_full_seo(content):
    """检查页面是否已有完整SEO优化"""
    return ('schema.org/SoftwareApplication' in content and 
            'og:title' in content and 
            'schema.org/FAQPage' in content)

def get_page_info(filename):
    """从文件名提取页面信息"""
    name = filename.replace('-v2.html', '').replace('-', ' ').title()
    
    # 银行页面
    banks = {
        'chase-bank': ('Chase Bank', 'chase', 'Chase Bank USA'),
        'bank-of-america': ('Bank of America', 'bofa', 'Bank of America USA'),
        'wells-fargo': ('Wells Fargo', 'wellsfargo', 'Wells Fargo Bank'),
        'citibank': ('Citibank', 'citi', 'Citibank USA'),
        'capital-one': ('Capital One', 'capitalone', 'Capital One Bank'),
        'us-bank': ('US Bank', 'usbank', 'US Bank USA'),
        'pnc-bank': ('PNC Bank', 'pnc', 'PNC Bank USA'),
        'td-bank': ('TD Bank', 'tdbank', 'TD Bank USA'),
        'truist-bank': ('Truist Bank', 'truist', 'Truist Bank USA'),
        'ally-bank': ('Ally Bank', 'ally', 'Ally Bank USA'),
        'hsbc-bank': ('HSBC Bank', 'hsbc', 'HSBC Hong Kong'),
        'hsbc-uk-bank': ('HSBC UK', 'hsbc-uk', 'HSBC UK Bank'),
        'barclays-bank': ('Barclays', 'barclays', 'Barclays Bank UK'),
        'lloyds-bank': ('Lloyds', 'lloyds', 'Lloyds Bank UK'),
        'natwest-bank': ('NatWest', 'natwest', 'NatWest Bank UK'),
        'santander-uk': ('Santander UK', 'santander-uk', 'Santander UK Bank'),
        'rbc-bank': ('RBC', 'rbc', 'Royal Bank of Canada'),
        'td-canada-trust': ('TD Canada Trust', 'td-canada', 'TD Canada Trust Bank'),
        'scotiabank': ('Scotiabank', 'scotiabank', 'Scotiabank Canada'),
        'bmo-bank': ('BMO', 'bmo', 'Bank of Montreal'),
        'cibc-bank': ('CIBC', 'cibc', 'CIBC Bank Canada'),
        'commbank': ('Commonwealth Bank', 'commbank', 'Commonwealth Bank Australia'),
        'westpac-bank': ('Westpac', 'westpac', 'Westpac Bank Australia'),
        'anz-bank': ('ANZ', 'anz', 'ANZ Bank Australia'),
        'nab-bank': ('NAB', 'nab', 'National Australia Bank'),
        'anz-nz-bank': ('ANZ NZ', 'anz-nz', 'ANZ New Zealand'),
        'asb-bank': ('ASB', 'asb', 'ASB Bank New Zealand'),
        'westpac-nz': ('Westpac NZ', 'westpac-nz', 'Westpac New Zealand'),
        'bnz-bank': ('BNZ', 'bnz', 'Bank of New Zealand'),
        'dbs-bank': ('DBS', 'dbs', 'DBS Bank Singapore'),
        'ocbc-bank': ('OCBC', 'ocbc', 'OCBC Bank Singapore'),
        'uob-bank': ('UOB', 'uob', 'UOB Bank Singapore'),
    }
    
    for key, value in banks.items():
        if key in filename:
            return {
                'name': value[0],
                'slug': value[1],
                'full_name': value[2],
                'type': 'bank'
            }
    
    # 行业页面
    if 'restaurant' in filename:
        return {'name': 'Restaurant', 'slug': 'restaurant', 'full_name': 'Restaurant Accounting', 'type': 'industry'}
    elif 'ecommerce' in filename:
        return {'name': 'E-commerce', 'slug': 'ecommerce', 'full_name': 'E-commerce Accounting', 'type': 'industry'}
    elif 'real-estate' in filename:
        return {'name': 'Real Estate', 'slug': 'real-estate', 'full_name': 'Real Estate Accounting', 'type': 'industry'}
    elif 'small-business' in filename:
        return {'name': 'Small Business', 'slug': 'small-business', 'full_name': 'Small Business Accounting', 'type': 'industry'}
    elif 'freelancer' in filename:
        return {'name': 'Freelancer', 'slug': 'freelancer', 'full_name': 'Freelancer Accounting', 'type': 'industry'}
    elif 'construction' in filename:
        return {'name': 'Construction', 'slug': 'construction', 'full_name': 'Construction Accounting', 'type': 'industry'}
    elif 'healthcare' in filename:
        return {'name': 'Healthcare', 'slug': 'healthcare', 'full_name': 'Healthcare Accounting', 'type': 'industry'}
    elif 'law-firm' in filename:
        return {'name': 'Law Firm', 'slug': 'law-firm', 'full_name': 'Law Firm Accounting', 'type': 'industry'}
    elif 'nonprofit' in filename or 'non-profit' in filename:
        return {'name': 'Non-profit', 'slug': 'nonprofit', 'full_name': 'Non-profit Accounting', 'type': 'industry'}
    elif 'consulting' in filename:
        return {'name': 'Consulting', 'slug': 'consulting', 'full_name': 'Consulting Firm Accounting', 'type': 'industry'}
    elif 'insurance' in filename:
        return {'name': 'Insurance', 'slug': 'insurance', 'full_name': 'Insurance Agency Accounting', 'type': 'industry'}
    elif 'travel-agency' in filename:
        return {'name': 'Travel Agency', 'slug': 'travel', 'full_name': 'Travel Agency Accounting', 'type': 'industry'}
    elif 'manufacturing' in filename:
        return {'name': 'Manufacturing', 'slug': 'manufacturing', 'full_name': 'Manufacturing Accounting', 'type': 'industry'}
    elif 'logistics' in filename:
        return {'name': 'Logistics', 'slug': 'logistics', 'full_name': 'Logistics & Shipping Accounting', 'type': 'industry'}
    elif 'retail' in filename:
        return {'name': 'Retail', 'slug': 'retail', 'full_name': 'Retail Store Accounting', 'type': 'industry'}
    elif 'professional-services' in filename:
        return {'name': 'Professional Services', 'slug': 'professional', 'full_name': 'Professional Services Accounting', 'type': 'industry'}
    elif 'agriculture' in filename or 'farming' in filename:
        return {'name': 'Agriculture', 'slug': 'agriculture', 'full_name': 'Agriculture & Farming Accounting', 'type': 'industry'}
    
    # 对比页面
    elif 'vs-manual' in filename:
        return {'name': 'vs Manual', 'slug': 'vs-manual', 'full_name': 'VaultCaddy vs Manual Processing', 'type': 'comparison'}
    elif 'vs-excel' in filename:
        return {'name': 'vs Excel', 'slug': 'vs-excel', 'full_name': 'VaultCaddy vs Excel', 'type': 'comparison'}
    elif 'vs-competitors' in filename:
        return {'name': 'vs Competitors', 'slug': 'vs-competitors', 'full_name': 'VaultCaddy vs Competitors', 'type': 'comparison'}
    elif 'vs-nanonets' in filename:
        return {'name': 'vs Nanonets', 'slug': 'vs-nanonets', 'full_name': 'VaultCaddy vs Nanonets', 'type': 'comparison'}
    elif 'vs-formx' in filename:
        return {'name': 'vs FormX', 'slug': 'vs-formx', 'full_name': 'VaultCaddy vs FormX', 'type': 'comparison'}
    
    # 功能页面
    elif 'api-integration-guide' in filename:
        return {'name': 'API Integration', 'slug': 'api-guide', 'full_name': 'API Integration Guide', 'type': 'feature'}
    elif 'api-integration' in filename:
        return {'name': 'API Integration', 'slug': 'api', 'full_name': 'API Integration Solution', 'type': 'feature'}
    elif 'batch-processing' in filename:
        return {'name': 'Batch Processing', 'slug': 'batch', 'full_name': 'Batch Processing Solution', 'type': 'feature'}
    elif 'bulk-processing' in filename:
        return {'name': 'Bulk Processing', 'slug': 'bulk', 'full_name': 'Bulk Processing Solution', 'type': 'feature'}
    elif 'multi-currency' in filename:
        return {'name': 'Multi-Currency', 'slug': 'multi-currency', 'full_name': 'Multi-Currency Support', 'type': 'feature'}
    elif 'ocr' in filename:
        return {'name': 'OCR Technology', 'slug': 'ocr', 'full_name': 'OCR Bank Statement Technology', 'type': 'feature'}
    elif 'mobile-app' in filename:
        return {'name': 'Mobile App', 'slug': 'mobile', 'full_name': 'Mobile App Bank Statement Scanner', 'type': 'feature'}
    elif 'data-security' in filename:
        return {'name': 'Data Security', 'slug': 'security', 'full_name': 'Bank Statement Data Security', 'type': 'feature'}
    elif 'automated-reconciliation' in filename or 'reconciliation' in filename:
        return {'name': 'Reconciliation', 'slug': 'reconciliation', 'full_name': 'Automated Bank Reconciliation', 'type': 'feature'}
    elif 'white-label' in filename:
        return {'name': 'White Label', 'slug': 'white-label', 'full_name': 'White Label Solution', 'type': 'feature'}
    elif 'custom-report' in filename:
        return {'name': 'Custom Reports', 'slug': 'custom-reports', 'full_name': 'Custom Report Builder', 'type': 'feature'}
    elif 'webhook' in filename:
        return {'name': 'Webhook', 'slug': 'webhook', 'full_name': 'Webhook Integration', 'type': 'feature'}
    elif 'multi-company' in filename:
        return {'name': 'Multi-Company', 'slug': 'multi-company', 'full_name': 'Multi-Company Management', 'type': 'feature'}
    
    return {'name': name, 'slug': filename.replace('.html', ''), 'full_name': name, 'type': 'other'}

def generate_seo_head(info, filename):
    """生成完整的SEO优化head部分"""
    name = info['name']
    full_name = info['full_name']
    page_type = info['type']
    
    # 生成标题和描述
    if page_type == 'bank':
        title = f"{full_name} Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy"
        description = f"AI-powered {full_name} statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month | 500+ businesses trust us"
        keywords = f"{name} bank statement,{name} PDF converter,{name} to Excel,{name} to QuickBooks,bank statement automation"
    elif page_type == 'industry':
        title = f"{full_name} Solution | Bank Statement Automation | VaultCaddy"
        description = f"AI-powered {full_name} solution. Automate bank reconciliation in seconds. From $5.59/month | 500+ businesses"
        keywords = f"{full_name},{name} accounting software,{name} bank reconciliation,automated accounting"
    elif page_type == 'comparison':
        title = f"{full_name} | Best Bank Statement Converter 2025"
        description = f"See why 500+ businesses choose VaultCaddy. Better pricing, faster processing, higher accuracy. From $5.59/month"
        keywords = f"VaultCaddy comparison,bank statement converter comparison,best accounting software"
    else:  # feature
        title = f"{full_name} | Bank Statement Processing | VaultCaddy"
        description = f"{full_name} for bank statement processing. Enterprise-grade solution from $5.59/month"
        keywords = f"{full_name},bank statement processing,accounting automation"
    
    canonical = f"https://vaultcaddy.com/en/{filename}"
    
    seo_html = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Optimization -->
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{name} - VaultCaddy">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://vaultcaddy.com/images/{info['slug']}-og-image.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    
    <!-- Component Library CSS -->
    <link rel="stylesheet" href="../components/design-system.css">
    <link rel="stylesheet" href="../components/additional-components.css">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Fix FAQ double plus icon -->
    <style>
        .faq-question::after {{
            display: none !important;
        }}
        
        /* Mobile responsive */
        @media (max-width: 768px) {{
            .pricing-grid {{
                grid-template-columns: 1fr !important;
            }}
            .feature-grid {{
                grid-template-columns: 1fr !important;
            }}
        }}
    </style>
    
    <!-- Structured Data - SoftwareApplication -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "VaultCaddy - {full_name}",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Web, iOS, Android",
      "offers": {{
        "@type": "Offer",
        "price": "5.59",
        "priceCurrency": "USD",
        "priceValidUntil": "2026-12-31"
      }},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "127",
        "bestRating": "5",
        "worstRating": "1"
      }},
      "description": "{description}"
    }}
    </script>
    
    <!-- Structured Data - FAQ -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "How accurate is VaultCaddy?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "VaultCaddy achieves 98% accuracy using advanced AI trained on millions of bank statements. Our system is continuously improving."
          }}
        }},
        {{
          "@type": "Question",
          "name": "What file formats are supported?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "We support PDF, JPG, PNG, and other image formats. Export to Excel, CSV, QuickBooks, or Xero."
          }}
        }},
        {{
          "@type": "Question",
          "name": "How long does processing take?",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "Most bank statements are processed in 3-5 seconds. Batch uploads are supported for multiple months."
          }}
        }}
      ]
    }}
    </script>
</head>'''
    
    return seo_html

def upgrade_page(filepath):
    """升级单个页面"""
    filename = os.path.basename(filepath)
    
    print(f"📄 处理: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有完整SEO
    if has_full_seo(content):
        print(f"   ✅ 已有完整SEO，跳过")
        return False
    
    # 获取页面信息
    info = get_page_info(filename)
    
    # 生成新的head部分
    new_head = generate_seo_head(info, filename)
    
    # 替换head部分
    # 找到</head>的位置
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"   ❌ 未找到</head>标签")
        return False
    
    # 找到<body>的位置
    body_start = content.find('<body')
    if body_start == -1:
        print(f"   ❌ 未找到<body>标签")
        return False
    
    # 保留body及之后的内容
    new_content = new_head + '\n' + content[body_start:]
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✅ SEO升级完成: {info['type']} - {info['name']}")
    return True

def main():
    print("🚀 开始批量升级所有页面到完整SEO模板\n")
    
    # 获取所有-v2.html文件
    files = sorted(Path('.').glob('*-v2.html'))
    
    upgraded = 0
    skipped = 0
    
    for filepath in files:
        if upgrade_page(str(filepath)):
            upgraded += 1
        else:
            skipped += 1
        print()
    
    print(f"\n{'='*60}")
    print(f"📊 升级完成统计:")
    print(f"   ✅ 已升级: {upgraded} 个页面")
    print(f"   ⏭️  已跳过: {skipped} 个页面（已有完整SEO）")
    print(f"   📦 总计: {upgraded + skipped} 个页面")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()

