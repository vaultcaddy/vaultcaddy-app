#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客SEO批量优化工具
Batch Blog SEO Optimizer
"""

import re
from pathlib import Path

# 17篇博客文章的SEO数据
BLOG_SEO_DATA = {
    "manual-vs-ai-cost-analysis.html": {
        "title": "人手處理 vs AI 自動化：真實成本對比與時間解放指南 | VaultCaddy",
        "description": "深入分析人手處理財務文檔的隱藏成本。了解如何透過 AI 自動化每月節省 40+ 小時，將重複工作時間轉化為業務增長和個人休息時間。針對香港文件，價格低至HKD $0.5/頁。",
        "keywords": "財務文檔處理成本,人手 vs AI,時間成本分析,會計自動化,提升生產力,香港會計師,財務管理效率,AI OCR,香港文件處理",
        "og_image": "/images/blog/manual-vs-ai-cover.jpg"
    },
    "personal-bookkeeping-best-practices.html": {
        "title": "個人記賬的 7 個最佳實踐：用 AI 工具實現財務自由 | VaultCaddy",
        "description": "掌握7個經過驗證的個人記賬最佳實踐，結合AI工具自動化財務管理。從每日記錄到月度分析，學習如何輕鬆管理個人財務。針對香港用戶，低至HKD $0.5/頁。",
        "keywords": "個人記賬,財務自由,AI記賬工具,財務管理,預算管理,支出追蹤,香港理財,自動化記賬,發票管理",
        "og_image": "/images/blog/personal-bookkeeping-cover.jpg"
    },
    "ai-invoice-processing-guide.html": {
        "title": "AI 發票處理完整指南：從上傳到入賬的自動化流程 | VaultCaddy",
        "description": "全面了解 AI 發票處理技術。學習如何使用 OCR 和機器學習自動提取發票數據、驗證準確性。針對香港發票格式優化，98%準確率，低至HKD $0.5/頁。",
        "keywords": "AI 發票處理,OCR 技術,發票自動化,會計軟件,發票數據提取,QuickBooks,Xero,香港發票,財務自動化",
        "og_image": "/images/blog/ai-invoice-guide-cover.jpg"
    },
    "freelancer-invoice-management.html": {
        "title": "自由工作者如何輕鬆管理發票和收據 | VaultCaddy",
        "description": "5個實用技巧幫助自由工作者使用 AI 技術輕鬆管理財務文檔，節省時間專注核心業務。支持香港所有銀行文件，安全可靠，低至HKD $0.5/頁。",
        "keywords": "自由工作者,Freelancer,發票管理,收據管理,財務文檔,AI自動化,香港自由職業,記賬工具,報稅準備",
        "og_image": "/images/blog/freelancer-invoice-cover.jpg"
    },
    "freelancer-tax-preparation-guide.html": {
        "title": "自由工作者報稅指南：香港稅務完整準備 | VaultCaddy",
        "description": "完整的香港自由工作者報稅準備指南，教您如何整理財務文檔、最大化扣稅、避免常見錯誤。AI自動整理，安全加密，低至HKD $0.5/頁。",
        "keywords": "香港報稅,自由工作者稅務,稅務準備,扣稅項目,IRR表格,利得稅,個人入息稅,財務文檔整理,香港稅務局",
        "og_image": "/images/blog/tax-preparation-cover.jpg"
    },
    "small-business-document-management.html": {
        "title": "小型企業文檔管理完全指南 | VaultCaddy",
        "description": "如何使用 AI 工具高效管理發票、收據、合同等業務文檔，提高團隊效率，降低運營成本。針對香港中小企，安全合規，低至HKD $0.5/頁。",
        "keywords": "小型企業,文檔管理,業務文檔,發票管理,合同管理,香港中小企,運營效率,AI自動化,數碼轉型",
        "og_image": "/images/blog/small-business-cover.jpg"
    },
    "ai-invoice-processing-for-smb.html": {
        "title": "AI 發票處理如何幫助香港小型企業節省成本 | VaultCaddy",
        "description": "深入分析 AI 自動化發票處理的 ROI，實際案例展示香港小型企業如何每月節省數千元成本。98%準確率，支持所有香港銀行，低至HKD $0.5/頁。",
        "keywords": "AI 發票處理,中小企業,成本節省,ROI分析,財務自動化,香港小型企業,會計自動化,發票掃描,OCR技術",
        "og_image": "/images/blog/ai-invoice-smb-cover.jpg"
    },
    "quickbooks-integration-guide.html": {
        "title": "QuickBooks 整合指南：實現香港會計流程自動化 | VaultCaddy",
        "description": "詳細教程：如何將 VaultCaddy 與 QuickBooks 整合，實現香港會計流程完全自動化。支持港幣交易，安全可靠，低至HKD $0.5/頁。",
        "keywords": "QuickBooks,會計軟件整合,QuickBooks香港,會計自動化,財務軟件,發票導出,銀行對賬,API整合,港幣記賬",
        "og_image": "/images/blog/quickbooks-cover.jpg"
    },
    "accounting-firm-automation.html": {
        "title": "香港會計事務所如何使用 AI 提高效率 | VaultCaddy",
        "description": "探索 AI 技術如何幫助香港會計事務所自動化重複性工作，讓會計師專注於高價值服務。支持所有香港銀行文件，安全加密，低至HKD $0.5/頁。",
        "keywords": "會計事務所,香港會計師,AI自動化,會計效率,事務所管理,客戶服務,財務自動化,香港HKICPA,執業會計師",
        "og_image": "/images/blog/accounting-firm-cover.jpg"
    },
    "client-document-management-for-accountants.html": {
        "title": "香港會計師的客戶文檔管理最佳實踐 | VaultCaddy",
        "description": "如何高效管理多個客戶的財務文檔，確保數據安全、合規，提升客戶滿意度。符合香港PDPO規定，銀行級加密，低至HKD $0.5/頁。",
        "keywords": "客戶文檔管理,香港會計師,數據安全,PDPO合規,文檔整理,客戶服務,會計事務所,檔案管理,雲端儲存",
        "og_image": "/images/blog/client-document-cover.jpg"
    },
    "ocr-accuracy-for-accounting.html": {
        "title": "OCR 技術在香港會計行業的應用與準確率 | VaultCaddy",
        "description": "深入分析 OCR 和 AI 文檔識別技術的準確率、限制和最佳應用場景。針對香港文件優化，98%準確率，支持繁體中文，低至HKD $0.5/頁。",
        "keywords": "OCR技術,文檔識別,AI識別,準確率,香港會計,繁體中文OCR,發票識別,銀行對賬單,機器學習",
        "og_image": "/images/blog/ocr-accuracy-cover.jpg"
    },
    "accounting-workflow-optimization.html": {
        "title": "優化香港會計工作流程：端到端自動化指南 | VaultCaddy",
        "description": "完整的香港會計工作流程優化指南，從文檔接收到報表生成的端到端自動化解決方案。符合香港會計準則，安全可靠，低至HKD $0.5/頁。",
        "keywords": "會計工作流程,流程優化,端到端自動化,香港會計準則,HKFRS,工作效率,數碼轉型,會計自動化,報表生成",
        "og_image": "/images/blog/workflow-optimization-cover.jpg"
    },
    "how-to-convert-pdf-bank-statement-to-excel.html": {
        "title": "如何將 PDF 銀行對賬單轉換為 Excel | VaultCaddy",
        "description": "3步驟快速將香港所有銀行的 PDF 對賬單轉換為 Excel，支持滙豐、恆生、中銀等所有主要銀行。98%準確率，安全加密，低至HKD $0.5/頁。",
        "keywords": "PDF轉Excel,銀行對賬單,PDF轉換,Excel導出,香港銀行,滙豐銀行,恆生銀行,中銀香港,財務報表",
        "og_image": "/images/blog/pdf-to-excel-cover.jpg"
    },
    "best-pdf-to-excel-converter.html": {
        "title": "2025年最佳 PDF 轉 Excel 轉換器推薦 | VaultCaddy",
        "description": "評測市面上最好的 PDF 轉 Excel 工具，針對香港用戶需求。VaultCaddy 支持繁體中文，針對香港銀行優化，98%準確率，低至HKD $0.5/頁。",
        "keywords": "PDF轉Excel工具,PDF轉換器,最佳轉換器,文檔轉換,香港工具,繁體中文支持,銀行文件,財務文檔,OCR轉換",
        "og_image": "/images/blog/best-converter-cover.jpg"
    },
    "ocr-technology-for-accountants.html": {
        "title": "香港會計師必知的 OCR 技術指南 | VaultCaddy",
        "description": "全面了解 OCR 技術如何革新香港會計行業，提升工作效率。支持繁體中文，針對香港文件格式優化，98%準確率，低至HKD $0.5/頁。",
        "keywords": "OCR技術,香港會計師,文檔識別,AI技術,會計自動化,繁體中文,香港文件,發票掃描,銀行對賬",
        "og_image": "/images/blog/ocr-technology-cover.jpg"
    },
    "automate-financial-documents.html": {
        "title": "自動化處理香港財務文檔的完整指南 | VaultCaddy",
        "description": "學習如何使用 AI 工具自動化處理發票、收據、銀行對賬單等財務文檔。針對香港文件格式，支持所有銀行，安全合規，低至HKD $0.5/頁。",
        "keywords": "財務文檔自動化,文檔處理,AI自動化,香港財務,發票處理,銀行對賬,收據管理,會計自動化,數碼轉型",
        "og_image": "/images/blog/automate-documents-cover.jpg"
    },
    "index.html": {
        "title": "VaultCaddy 博客 - AI 文檔處理專業指南",
        "description": "VaultCaddy 博客：AI 文檔處理、財務管理、會計自動化的最佳實踐和專業指南。針對香港文件和銀行優化，98%準確率，低至HKD $0.5/頁，安全可靠。",
        "keywords": "AI 文檔處理,財務管理,會計自動化,發票管理,收據整理,香港會計,銀行對賬單,OCR技術,VaultCaddy",
        "og_image": "/images/blog/blog-cover.jpg"
    }
}

def add_seo_tags(filepath, seo_data):
    """为HTML文件添加完整的SEO标签"""
    print(f"\n处理: {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有完整SEO（避免重复添加）
        if 'property="og:title"' in content and 'application/ld+json' in content:
            print(f"  ℹ️ SEO标签已存在，跳过")
            return False
        
        # 1. 更新或添加基本meta标签
        # Title
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{seo_data["title"]}</title>',
            content,
            flags=re.DOTALL
        )
        
        # Description
        if 'name="description"' in content:
            content = re.sub(
                r'<meta name="description"[^>]*>',
                f'<meta name="description" content="{seo_data["description"]}">',
                content
            )
        else:
            # 在title后添加
            content = content.replace(
                '</title>',
                f'</title>\n    <meta name="description" content="{seo_data["description"]}">'
            )
        
        # Keywords
        if 'name="keywords"' in content:
            content = re.sub(
                r'<meta name="keywords"[^>]*>',
                f'<meta name="keywords" content="{seo_data["keywords"]}">',
                content
            )
        else:
            content = content.replace(
                'name="description"',
                f'name="description"\n    <meta name="keywords" content="{seo_data["keywords"]}"'
            )
        
        # 2. 添加Open Graph标签（如果不存在）
        if 'property="og:' not in content:
            og_tags = f'''
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://vaultcaddy.com/blog/{filepath.name}">
    <meta property="og:title" content="{seo_data["title"]}">
    <meta property="og:description" content="{seo_data["description"]}">
    <meta property="og:image" content="https://vaultcaddy.com{seo_data["og_image"]}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://vaultcaddy.com/blog/{filepath.name}">
    <meta property="twitter:title" content="{seo_data["title"]}">
    <meta property="twitter:description" content="{seo_data["description"]}">
    <meta property="twitter:image" content="https://vaultcaddy.com{seo_data["og_image"]}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://vaultcaddy.com/blog/{filepath.name}">'''
            
            # 在</head>前添加
            content = content.replace('</head>', og_tags + '\n</head>')
        
        # 3. 添加结构化数据（JSON-LD）
        if 'application/ld+json' not in content:
            structured_data = f'''
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{seo_data["title"].replace(' | VaultCaddy', '')}",
      "description": "{seo_data["description"]}",
      "image": "https://vaultcaddy.com{seo_data["og_image"]}",
      "author": {{
        "@type": "Organization",
        "name": "VaultCaddy"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "VaultCaddy",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://vaultcaddy.com/logo.png"
        }}
      }},
      "datePublished": "2025-12-05",
      "dateModified": "2025-12-05"
    }}
    </script>'''
            
            # 在</head>前添加
            content = content.replace('</head>', structured_data + '\n</head>')
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ SEO优化完成")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("🚀 博客SEO批量优化")
    print("="*60)
    print()
    
    blog_dir = Path('blog')
    if not blog_dir.exists():
        print("❌ blog/ 目录不存在")
        return
    
    print(f"📁 找到 {len(BLOG_SEO_DATA)} 篇文章需要优化")
    print()
    
    updated_count = 0
    skipped_count = 0
    
    for filename, seo_data in BLOG_SEO_DATA.items():
        filepath = blog_dir / filename
        if filepath.exists():
            if add_seo_tags(filepath, seo_data):
                updated_count += 1
            else:
                skipped_count += 1
        else:
            print(f"\n⚠️ 文件不存在: {filename}")
            skipped_count += 1
    
    # 总结
    print()
    print("="*60)
    print("✅ SEO优化完成！")
    print("="*60)
    print(f"总文章数: {len(BLOG_SEO_DATA)}")
    print(f"已优化: {updated_count}")
    print(f"跳过: {skipped_count}")
    print()
    print("🎯 优化内容:")
    print("  ✅ Meta Title (针对香港用户)")
    print("  ✅ Meta Description (包含竞争优势)")
    print("  ✅ Meta Keywords (香港本地化)")
    print("  ✅ Open Graph Tags (社交媒体)")
    print("  ✅ Twitter Cards")
    print("  ✅ Canonical URLs")
    print("  ✅ Structured Data (JSON-LD)")
    print()
    print("💡 所有SEO标签已针对香港市场优化：")
    print("  • 强调香港文件和银行支持")
    print("  • 突出价格优势 (HKD $0.5/页)")
    print("  • 强调安全性和98%准确率")
    print()

if __name__ == '__main__':
    main()

