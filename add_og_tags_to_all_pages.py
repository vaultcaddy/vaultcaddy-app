#!/usr/bin/env python3
"""
批量为所有页面添加 OG 标签 - 使用 SEO 优化的图片名称

作用：
1. 自动为每个页面添加对应的 OG 图片标签
2. 使用 SEO 优化的文件名
3. 包含完整的 OG 元数据

使用方法：
    python3 add_og_tags_to_all_pages.py
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

# 配置
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / f"backup_before_og_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
BACKUP_DIR.mkdir(exist_ok=True)

# 页面和对应的 OG 图片映射（SEO 优化文件名）
PAGE_OG_MAPPING = {
    # 中文版
    "index.html": {
        "og_image": "vaultcaddy-bank-statement-receipt-invoice-ai-hong-kong-og-image.jpg",
        "og_title": "对账单+收据+发票AI识别转Excel｜3秒完成｜月费$46起 - VaultCaddy",
        "og_description": "告别手工录入！VaultCaddy AI自动处理银行对账单、收据、发票，3秒转成Excel。支持所有香港银行和商户。",
        "og_url": "https://vaultcaddy.com/"
    },
    "ai-vs-manual-comparison.html": {
        "og_image": "ai-vs-manual-dext-autoentry-comparison-hong-kong-2025-og-image.jpg",
        "og_title": "VaultCaddy vs 人工 vs Dext vs AutoEntry 完整对比 2025｜年省35,000港币",
        "og_description": "人工处理对账单每月花30小时？VaultCaddy AI 3秒搞定，比人工便宜95%，比Dext便宜70%。",
        "og_url": "https://vaultcaddy.com/ai-vs-manual-comparison.html"
    },
    "vaultcaddy-vs-dext.html": {
        "og_image": "vaultcaddy-vs-dext-receipt-bank-price-comparison-hk-og-image.jpg",
        "og_title": "VaultCaddy vs Dext 价格对比｜年费便宜70%｜月费$46 vs $273",
        "og_description": "Dext太贵？VaultCaddy年费仅$552，便宜70%！相同功能，更适合香港。",
        "og_url": "https://vaultcaddy.com/vaultcaddy-vs-dext.html"
    },
    "vaultcaddy-vs-autoentry.html": {
        "og_image": "vaultcaddy-vs-autoentry-bookkeeping-automation-hk-og-image.jpg",
        "og_title": "VaultCaddy vs AutoEntry 对比｜年费便宜85%｜月费$46 vs $325",
        "og_description": "AutoEntry太贵？VaultCaddy年费仅$552，便宜85%！全中文界面，24/7中文客服。",
        "og_url": "https://vaultcaddy.com/vaultcaddy-vs-autoentry.html"
    },
    "vaultcaddy-vs-receiptbank.html": {
        "og_image": "vaultcaddy-vs-receipt-bank-accounting-software-hk-og-image.jpg",
        "og_title": "VaultCaddy vs Receipt Bank 对比｜年费便宜70%",
        "og_description": "Receipt Bank（现Dext）太贵？VaultCaddy提供相同功能，价格便宜70%。",
        "og_url": "https://vaultcaddy.com/vaultcaddy-vs-receiptbank.html"
    },
    "hsbc-bank-statement.html": {
        "og_image": "hsbc-bank-statement-to-excel-converter-hong-kong-og-image.jpg",
        "og_title": "汇丰银行对账单转Excel｜3秒处理｜支持HSBC网银PDF",
        "og_description": "汇丰对账单手工录入太慢？VaultCaddy AI自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/hsbc-bank-statement.html"
    },
    "hangseng-bank-statement.html": {
        "og_image": "hang-seng-bank-statement-pdf-to-excel-hk-og-image.jpg",
        "og_title": "恒生银行对账单转Excel｜3秒处理｜支持Hang Seng网银PDF",
        "og_description": "恒生对账单自动识别，3秒转成Excel，准确率98%。月费$46起。",
        "og_url": "https://vaultcaddy.com/hangseng-bank-statement.html"
    },
    "bochk-bank-statement.html": {
        "og_image": "bank-of-china-hk-statement-ocr-converter-og-image.jpg",
        "og_title": "中国银行（香港）对账单转Excel｜3秒处理｜支持BOCHK网银PDF",
        "og_description": "中银对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/bochk-bank-statement.html"
    },
    "citibank-bank-statement.html": {
        "og_image": "citibank-hong-kong-statement-excel-converter-og-image.jpg",
        "og_title": "花旗银行对账单转Excel｜3秒处理｜支持Citibank网银PDF",
        "og_description": "花旗对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/citibank-bank-statement.html"
    },
    "sc-bank-statement.html": {
        "og_image": "standard-chartered-hk-bank-statement-automation-og-image.jpg",
        "og_title": "渣打银行对账单转Excel｜3秒处理｜支持Standard Chartered网银PDF",
        "og_description": "渣打对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/sc-bank-statement.html"
    },
    "dbs-bank-statement.html": {
        "og_image": "dbs-bank-hong-kong-statement-processing-tool-og-image.jpg",
        "og_title": "星展银行对账单转Excel｜3秒处理｜支持DBS网银PDF",
        "og_description": "星展对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/dbs-bank-statement.html"
    },
    "bea-bank-statement.html": {
        "og_image": "bank-of-east-asia-statement-to-excel-hk-og-image.jpg",
        "og_title": "东亚银行对账单转Excel｜3秒处理｜支持BEA网银PDF",
        "og_description": "东亚对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/bea-bank-statement.html"
    },
    "dahsing-bank-statement.html": {
        "og_image": "dah-sing-bank-statement-converter-hong-kong-og-image.jpg",
        "og_title": "大新银行对账单转Excel｜3秒处理｜支持Dah Sing网银PDF",
        "og_description": "大新对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/dahsing-bank-statement.html"
    },
    "citic-bank-statement.html": {
        "og_image": "citic-bank-hong-kong-statement-ocr-tool-og-image.jpg",
        "og_title": "中信银行对账单转Excel｜3秒处理｜支持CITIC网银PDF",
        "og_description": "中信对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/citic-bank-statement.html"
    },
    "bankcomm-bank-statement.html": {
        "og_image": "bank-of-communications-hk-statement-automation-og-image.jpg",
        "og_title": "交通银行对账单转Excel｜3秒处理｜支持BankComm网银PDF",
        "og_description": "交通银行对账单自动识别，3秒转成Excel，准确率98%。",
        "og_url": "https://vaultcaddy.com/bankcomm-bank-statement.html"
    },
    # 英文版
    "en/index.html": {
        "og_image": "bank-statement-receipt-invoice-ai-ocr-hong-kong-en-og-image.jpg",
        "og_title": "Bank Statements+Receipts+Invoices AI OCR to Excel | From $46/month - VaultCaddy",
        "og_description": "Stop manual data entry! VaultCaddy AI processes bank statements, receipts, and invoices to Excel in 3 seconds. 98% accuracy, 95% cheaper.",
        "og_url": "https://vaultcaddy.com/en/"
    },
    "en/ai-vs-manual-comparison.html": {
        "og_image": "ai-vs-manual-bookkeeping-comparison-hong-kong-2025-en-og-image.jpg",
        "og_title": "VaultCaddy vs Manual vs Dext vs AutoEntry Comparison 2025 | Save HK$35,000/year",
        "og_description": "Manual bookkeeping takes 30 hours/month? VaultCaddy AI does it in 3 seconds, 95% cheaper than manual, 70% cheaper than Dext.",
        "og_url": "https://vaultcaddy.com/en/ai-vs-manual-comparison.html"
    },
    "en/vaultcaddy-vs-dext.html": {
        "og_image": "vaultcaddy-vs-dext-receipt-bank-comparison-en-og-image.jpg",
        "og_title": "VaultCaddy vs Dext Comparison | 70% Cheaper | $46/month vs $273/month",
        "og_description": "Dext too expensive? VaultCaddy offers same features at $552/year vs Dext $3,276/year. 70% cheaper!",
        "og_url": "https://vaultcaddy.com/en/vaultcaddy-vs-dext.html"
    },
    # 日文版
    "jp/index.html": {
        "og_image": "bank-statement-ai-converter-hong-kong-japanese-og-image.jpg",
        "og_title": "銀行明細書+領収書+請求書AI変換｜3秒でExcelに｜月額$46〜 - VaultCaddy",
        "og_description": "手作業入力にさようなら！VaultCaddy AIで銀行明細書、領収書、請求書を3秒でExcel変換。正確率98%。",
        "og_url": "https://vaultcaddy.com/jp/"
    },
    # 韩文版
    "kr/index.html": {
        "og_image": "bank-statement-ai-converter-hong-kong-korean-og-image.jpg",
        "og_title": "은행 명세서+영수증+청구서 AI 변환｜3초에 Excel로｜월$46부터 - VaultCaddy",
        "og_description": "수동 입력 안녕！VaultCaddy AI로 은행 명세서, 영수증, 청구서를 3초 만에 Excel로 변환. 정확도 98%.",
        "og_url": "https://vaultcaddy.com/kr/"
    },
}


def create_og_tags(page_info):
    """生成 OG 标签 HTML"""
    og_tags = f'''
    <!-- Open Graph 标签 - SEO 优化 -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{page_info['og_url']}">
    <meta property="og:title" content="{page_info['og_title']}">
    <meta property="og:description" content="{page_info['og_description']}">
    <meta property="og:image" content="https://vaultcaddy.com/images/og/{page_info['og_image']}">
    <meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/{page_info['og_image']}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{page_info['og_title']}">
    
    <!-- Twitter Card 标签 -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{page_info['og_url']}">
    <meta name="twitter:title" content="{page_info['og_title']}">
    <meta name="twitter:description" content="{page_info['og_description']}">
    <meta name="twitter:image" content="https://vaultcaddy.com/images/og/{page_info['og_image']}">'''
    
    return og_tags


def add_og_tags_to_file(file_path, page_info):
    """为单个文件添加 OG 标签"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份
        backup_path = BACKUP_DIR / file_path.name
        shutil.copy2(file_path, backup_path)
        
        # 检查是否已有 OG 标签
        if 'property="og:image"' in content:
            print(f"  ⏭️  已有 OG 标签，跳过")
            return False
        
        # 生成 OG 标签
        og_tags = create_og_tags(page_info)
        
        # 在 </head> 前插入
        if '</head>' in content:
            content = content.replace('</head>', f'{og_tags}\n</head>')
            print(f"  ✅ 已添加 OG 标签")
        else:
            print(f"  ❌ 未找到 </head> 标签")
            return False
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False


def main():
    """主函数"""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 批量添加 OG 标签（SEO 优化版）")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"📂 备份目录: {BACKUP_DIR}")
    print(f"📋 需要处理: {len(PAGE_OG_MAPPING)} 个页面\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for page_path, page_info in PAGE_OG_MAPPING.items():
        file_path = BASE_DIR / page_path
        
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📄 {page_path}")
        print(f"  🖼️  OG 图片: {page_info['og_image']}")
        
        if not file_path.exists():
            print(f"  ⚠️  文件不存在，跳过")
            skip_count += 1
            continue
        
        result = add_og_tags_to_file(file_path, page_info)
        if result:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 完成统计：")
    print(f"✅ 成功添加：{success_count} 个")
    print(f"⏭️  已存在跳过：{skip_count} 个")
    print(f"❌ 错误：{error_count} 个")
    print(f"📂 备份位置：{BACKUP_DIR}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print("🎯 下一步：")
    print("1. 检查修改的文件")
    print("2. 测试 OG 预览：")
    print("   • Facebook Debugger: https://developers.facebook.com/tools/debug/")
    print("   • WhatsApp: 发送链接测试")
    print("3. 提交更改：")
    print("   git add *.html")
    print('   git commit -m "Add OG tags to all pages"')
    print("   git push")


if __name__ == '__main__':
    main()

