#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Schema.org结构化数据添加到所有Landing Page
"""

import re
import glob
from pathlib import Path

# Schema模板（FAQ + WebSite + BreadcrumbList）
SCHEMA_TEMPLATE = '''
    <!-- ============================================ -->
    <!-- 增强型 Schema.org 结构化数据 - SEO优化 -->
    <!-- ============================================ -->
    
    <!-- FAQ Schema - 常见问题（会在Google搜索结果展示） -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "VaultCaddy 支援哪些銀行？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 支援香港所有主要銀行，包括匯豐銀行(HSBC)、恆生銀行(Hang Seng)、中國銀行香港(BOC HK)、渣打銀行(Standard Chartered)、東亞銀行(BEA)、星展銀行(DBS)等。支援商業戶口和個人戶口的對帳單。"
          }
        },
        {
          "@type": "Question",
          "name": "VaultCaddy 的收費是多少？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 提供兩種方案：月付方案 HK$58/月，包含100頁免費處理，超出後每頁HK$0.5；年付方案 HK$552/年（相當於HK$46/月），同樣包含100頁免費處理。新用戶可免費試用20頁。使用優惠碼SAVE20可享首月8折優惠。"
          }
        },
        {
          "@type": "Question",
          "name": "VaultCaddy 的準確率如何？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 使用專門訓練的AI模型，對香港銀行對帳單的識別準確率達98%以上。系統可自動識別日期、金額、交易描述、餘額等所有欄位，並支援人工修正。"
          }
        },
        {
          "@type": "Question",
          "name": "VaultCaddy 支援哪些會計軟件？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 支援QuickBooks、Xero、MYOB等主流會計軟件，也可匯出Excel (.xlsx)、CSV等通用格式。系統會自動將交易分類，方便直接匯入會計軟件。"
          }
        },
        {
          "@type": "Question",
          "name": "處理一份對帳單需要多久？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 平均處理一份銀行對帳單只需10秒，包括上傳、AI識別、分類和匯出。人工手動輸入同樣的對帳單平均需要2小時，VaultCaddy 可節省99.9%的時間。"
          }
        },
        {
          "@type": "Question",
          "name": "VaultCaddy 的數據安全嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "VaultCaddy 採用銀行級256位元加密技術，符合香港私隱條例。所有數據儲存在香港本地數據中心，並通過SOC 2安全認證。用戶可隨時刪除數據，我們不會將數據用於其他用途。"
          }
        }
      ]
    }
    </script>

    <!-- WebSite Schema - 网站搜索功能 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "VaultCaddy",
      "url": "https://vaultcaddy.com",
      "description": "AI銀行對帳單處理平台 - 香港專業版",
      "inLanguage": ["zh-HK", "en", "ja", "ko"],
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://vaultcaddy.com/?s={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>

    <!-- BreadcrumbList Schema - 面包屑导航 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "首頁",
          "item": "https://vaultcaddy.com"
        }{{BREADCRUMB_ITEMS}}
      ]
    }
    </script>
'''

# Landing Page的面包屑配置
BREADCRUMB_CONFIG = {
    # 银行页面
    'hsbc-bank-statement.html': ('銀行對帳單處理', '匯豐銀行對帳單處理'),
    'hang-seng-bank-statement.html': ('銀行對帳單處理', '恆生銀行對帳單處理'),
    'boc-hk-bank-statement.html': ('銀行對帳單處理', '中國銀行香港對帳單處理'),
    'standard-chartered-statement.html': ('銀行對帳單處理', '渣打銀行對帳單處理'),
    'bea-bank-statement.html': ('銀行對帳單處理', '東亞銀行對帳單處理'),
    'dbs-bank-statement.html': ('銀行對帳單處理', '星展銀行對帳單處理'),
    
    # 软件整合
    'integrations/quickbooks-hong-kong.html': ('軟體整合', 'QuickBooks 香港整合'),
    'integrations/xero-integration.html': ('軟體整合', 'Xero 整合'),
    'integrations/excel-export.html': ('軟體整合', 'Excel 匯出'),
    'integrations/myob-hong-kong.html': ('軟體整合', 'MYOB 香港整合'),
    
    # 行业解决方案
    'solutions/restaurant-accounting.html': ('解決方案', '餐廳會計'),
    'solutions/retail-accounting.html': ('解決方案', '零售會計'),
    'solutions/trading-company.html': ('解決方案', '貿易公司'),
    'for/property-managers.html': ('解決方案', '物業管理'),
    
    # 用户类型
    'for/accounting-firms.html': ('目標用戶', '會計師事務所'),
    'for/business-owners.html': ('目標用戶', '公司老闆'),
    'for/bookkeepers.html': ('目標用戶', '簿記員'),
    'for/finance-managers.html': ('目標用戶', '財務經理'),
    'for/freelancers.html': ('目標用戶', '自由工作者'),
    'for/small-shop-owners.html': ('目標用戶', '小店老闆'),
    'for/administrative-staff.html': ('目標用戶', '文員'),
    'for/procurement-staff.html': ('目標用戶', '採購員'),
    'for/hr-payroll.html': ('目標用戶', '人事薪酬'),
    'for/ecommerce-sellers.html': ('目標用戶', '電商賣家'),
    'for/law-firms.html': ('專業服務', '律師事務所'),
    'for/medical-clinics.html': ('專業服務', '診所'),
    'for/education-centers.html': ('專業服務', '教育中心'),
    'for/event-planners.html': ('專業服務', '活動策劃'),
    'for/charities-ngo.html': ('專業服務', '慈善機構'),
    
    # 特殊用途
    'tax-season-helper.html': ('特殊用途', '報稅助手'),
    'invoice-processing.html': ('特殊用途', '發票處理'),
    'receipt-scanner.html': ('特殊用途', '收據掃描'),
}

def generate_breadcrumb(filename):
    """生成面包屑导航项"""
    if filename not in BREADCRUMB_CONFIG:
        return ""
    
    category, page_title = BREADCRUMB_CONFIG[filename]
    full_url = f"https://vaultcaddy.com/{filename}"
    
    return f''',
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{category}",
          "item": "https://vaultcaddy.com/#solutions"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{page_title}",
          "item": "{full_url}"
        }}'''

def add_schema_to_file(file_path):
    """添加Schema到单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有Schema（避免重复添加）
        if '<!-- 增强型 Schema.org 结构化数据 - SEO优化 -->' in content:
            print(f"⏭️  跳过 {file_path}（已有Schema）")
            return False
        
        # 查找</head>标签
        if '</head>' not in content:
            print(f"❌ 跳过 {file_path}（找不到</head>标签）")
            return False
        
        # 生成面包屑导航
        # 使用文件名而不是相对路径
        if '/' in file_path:
            filename = '/'.join(file_path.split('/')[-2:]) if file_path.count('/') >= 2 else file_path.split('/')[-1]
        else:
            filename = file_path
        breadcrumb_items = generate_breadcrumb(filename)
        schema_code = SCHEMA_TEMPLATE.replace('{{BREADCRUMB_ITEMS}}', breadcrumb_items)
        
        # 在</head>前添加Schema
        updated_content = content.replace('</head>', f'{schema_code}\n</head>')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已添加Schema到 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 处理 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 开始添加Schema.org结构化数据到所有Landing Page")
    print("=" * 70)
    print()
    
    # 所有需要添加Schema的文件
    files_to_process = []
    
    # 1. 多语言主页（跳过index.html因为已手动添加）
    files_to_process.extend([
        'en/index.html',
        'jp/index.html',
        'kr/index.html',
    ])
    
    # 2. 所有Landing Page
    landing_pages = list(glob.glob('*-statement.html'))  # 银行页面
    landing_pages.extend(glob.glob('for/*.html'))  # 用户类型页面
    landing_pages.extend(glob.glob('solutions/*.html'))  # 解决方案页面
    landing_pages.extend(glob.glob('integrations/*.html'))  # 软件整合页面
    landing_pages.extend([
        'tax-season-helper.html',
        'invoice-processing.html',
        'receipt-scanner.html',
    ])  # 特殊用途页面
    
    files_to_process.extend(landing_pages)
    
    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in files_to_process:
        if Path(file_path).exists():
            result = add_schema_to_file(file_path)
            if result:
                success_count += 1
            elif result is False:
                skip_count += 1
        else:
            print(f"⚠️  文件不存在: {file_path}")
            error_count += 1
    
    print()
    print("=" * 70)
    print("📊 执行结果统计")
    print("=" * 70)
    print(f"✅ 成功添加Schema: {success_count} 个文件")
    print(f"⏭️  跳过（已有Schema）: {skip_count} 个文件")
    print(f"❌ 错误/不存在: {error_count} 个文件")
    print(f"📝 总计处理: {len(files_to_process)} 个文件")
    print()
    print("🎉 所有Landing Page的Schema.org结构化数据已添加完成！")
    print()
    print("📋 下一步:")
    print("1. 使用 Google Rich Results Test 验证:")
    print("   https://search.google.com/test/rich-results")
    print("2. 输入任意页面URL测试")
    print("3. 确认FAQ、Breadcrumb、Organization等Schema正常显示")
    print()

if __name__ == '__main__':
    main()

