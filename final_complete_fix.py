#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 最终完整修复：所有遗漏的英文文本
"""

import os
import re
from pathlib import Path

def get_all_replacements(lang):
    """获取所有需要替换的文本（包括之前遗漏的）"""
    
    if lang == 'zh-TW' or lang == 'zh-HK':
        return {
            # ===== 图1: Hero Section =====
            'CTBC Bank statements are converted to Excel in seconds': 'CTBC銀行對帳單在幾秒內轉換為Excel',
            'Scotiabank statements are converted to Excel in seconds': 'Scotiabank對帳單在幾秒內轉換為Excel',
            'U.S. Bank statements are converted to Excel in seconds': '美國銀行對帳單在幾秒內轉換為Excel',
            'are converted to Excel in seconds': '在幾秒內轉換為Excel',
            
            # ===== 图2 & 图3: Features卡片 =====
            '否 waiting, no queues, no manual work. Batch upload supported.': '無需等待、無需排隊、無需手動工作。支援批量上傳。',
            'Pre-格式化的，可直接導入您的會計軟件。': '預先格式化，可直接導入您的會計軟件。',
            'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-': 'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-',  # 将被下面的完整替换
            
            # ===== 图3: How It Works步骤 =====
            'Our AI engine, specifically trained on CTBC Bank formats, automatically extracts all transactions, dates, amounts, and descriptions 準確率達98% in just 3秒.': '我們的AI引擎專門針對CTBC銀行格式進行訓練，自動提取所有交易、日期、金額和描述，準確率達98%，只需3秒。',
            'Our AI engine, specifically trained on Scotiabank formats, automatically extracts all transactions, dates, amounts, and descriptions 準確率達98% in just 3秒.': '我們的AI引擎專門針對Scotiabank格式進行訓練，自動提取所有交易、日期、金額和描述，準確率達98%，只需3秒。',
            'Our AI engine, specifically trained on U.S. Bank formats, automatically extracts all transactions, dates, amounts, and descriptions 準確率達98% in just 3秒.': '我們的AI引擎專門針對美國銀行格式進行訓練，自動提取所有交易、日期、金額和描述，準確率達98%，只需3秒。',
            
            'formatted and ready to import without any manual adjustments.': '格式化，無需任何手動調整即可導入。',
            'Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files auto-delete after 24 hours.': '在我們的儀表板中查看提取的數據。進行任何必要的調整，然後下載或直接同步到您的會計軟件。所有文件24小時後自動刪除。',
            
            # ===== 定价部分 =====
            'with annual billing': '年付優惠',
            'Billed $46 annually (save 20%)': '年付NT$148（節省20%）',
            'Billed $92 annually (save 20%)': '年付NT$296（節省20%）',
            'Billed annually (save 20%)': '年付優惠（節省20%）',
            'Certified secure': '認證安全',
            
            # ===== 图5: FAQ答案（最重要！）=====
            'VaultCaddy achieves 98%+ accuracy for CTBC Bank statements using advanced AI specifically trained on CTBC formats. Our system recognizes all CTBC account types and handles various statement layouts with industry-leading precision.': 'VaultCaddy使用專門針對CTBC格式訓練的先進AI，對CTBC銀行對帳單達到98%以上的準確率。我們的系統可識別所有CTBC帳戶類型，並以行業領先的精度處理各種對帳單佈局。',
            
            'VaultCaddy supports all CTBC Bank account types: CTBC Total Checking, CTBC Savings, CTBC Business Complete Banking, CTBC Credit Cards (Sapphire, Freedom, Ink), CTBC Private Client accounts, and CTBC First Banking.': 'VaultCaddy支援所有CTBC銀行帳戶類型：CTBC完全支票、CTBC儲蓄、CTBC商業完整銀行業務、CTBC信用卡（Sapphire、Freedom、Ink）、CTBC私人客戶帳戶和CTBC First Banking。',
            
            'After uploading your CTBC Bank statement, simply select "QuickBooks (QBO)" as your export format. VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop. 否 manual formatting required.': '上傳CTBC銀行對帳單後，只需選擇"QuickBooks (QBO)"作為您的匯出格式。VaultCaddy生成格式正確的QBO文件，您可以直接導入QuickBooks Online或桌面版。無需手動格式化。',
            
            '是. We use bank-level AES-256 encryption for all data. VaultCaddy is SOC 2 Type II certified and GDPR compliant. Your CTBC Bank statements are automatically deleted after 24 hours. We\'ve had zero data breaches in 3+ years of operation.': '是的。我們對所有數據使用銀行級AES-256加密。VaultCaddy已獲得SOC 2 Type II認證並符合GDPR。您的CTBC銀行對帳單24小時後自動刪除。我們在3年多的運營中零數據洩露。',
            
            '是! VaultCaddy supports unlimited batch processing. Upload 10, 50, or 100+ CTBC Bank statements simultaneously. Each file is processed independently in 3-5 seconds. Perfect for accounting firms or businesses with multiple accounts.': '是的！VaultCaddy支援無限批量處理。同時上傳10、50或100+份CTBC銀行對帳單。每個文件在3-5秒內獨立處理。非常適合會計事務所或擁有多個帳戶的企業。',
            
            # 其他银行的FAQ（通用）
            'VaultCaddy achieves 98%+ accuracy': 'VaultCaddy達到98%以上的準確率',
            'using advanced AI specifically trained on': '使用專門針對',
            'formats. Our system recognizes all': '格式訓練的先進AI。我們的系統可識別所有',
            'account types and handles various statement layouts with industry-leading precision.': '帳戶類型，並以行業領先的精度處理各種對帳單佈局。',
            
            'VaultCaddy supports all': 'VaultCaddy支援所有',
            'Bank account types:': '銀行帳戶類型：',
            
            'After uploading your': '上傳您的',
            'Bank statement, simply select "QuickBooks (QBO)" as your export format.': '銀行對帳單後，只需選擇"QuickBooks (QBO)"作為匯出格式。',
            'VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop.': 'VaultCaddy生成格式正確的QBO文件，您可以直接導入QuickBooks Online或桌面版。',
            '否 manual formatting required.': '無需手動格式化。',
            'No manual formatting required.': '無需手動格式化。',
            
            'We use bank-level AES-256 encryption for all data.': '我們對所有數據使用銀行級AES-256加密。',
            'is SOC 2 Type II certified and GDPR compliant.': '已獲得SOC 2 Type II認證並符合GDPR。',
            'Your': '您的',
            'Bank statements are automatically deleted after 24 hours.': '銀行對帳單24小時後自動刪除。',
            "We\'ve had zero data breaches in 3+ years of operation.": '我們在3年多的運營中零數據洩露。',
            
            'VaultCaddy supports unlimited batch processing.': 'VaultCaddy支援無限批量處理。',
            'Upload 10, 50, or 100+': '上傳10、50或100+份',
            'Bank statements simultaneously.': '銀行對帳單。',
            'Each file is processed independently in 3-5 seconds.': '每個文件在3-5秒內獨立處理。',
            'Perfect for accounting firms or businesses with multiple accounts.': '非常適合會計事務所或擁有多個帳戶的企業。',
        }
    
    elif lang == 'ja-JP':
        return {
            # Hero Section
            'CTBC Bank statements are converted to Excel in seconds': 'CTBC銀行明細書が数秒でExcelに変換されます',
            'Scotiabank statements are converted to Excel in seconds': 'Scotiabank明細書が数秒でExcelに変換されます',
            'are converted to Excel in seconds': 'が数秒でExcelに変換されます',
            'the USA': '米国',
            
            # Features
            'Built specifically for Scotiabank statements': 'Scotiabank明細書専用に設計',
            'Built specifically for CTBC Bank statements': 'CTBC銀行明細書専用に設計',
            'Our AI is specifically trained on': '当社のAIは',
            'Bank formats.': '銀行形式で特別に訓練されています。',
            'Handles checking, savings, credit cards, and business accounts with industry-leading precision.': '当座預金、普通預金、クレジットカード、ビジネスアカウントを業界最高の精度で処理します。',
            
            # FAQ (最重要！)
            'VaultCaddy achieves 98%+ accuracy for': 'VaultCaddyは',
            'using advanced AI specifically trained on': 'の形式で特別に訓練された高度なAIを使用して98%以上の精度を達成します。',
            'formats. Our system recognizes all': '当社のシステムはすべての',
            'account types and handles various statement layouts with industry-leading precision.': 'アカウントタイプを認識し、業界最高の精度でさまざまな明細書レイアウトを処理します。',
            
            'After uploading your': 'アップロード後、',
            'Bank statement, simply select "QuickBooks (QBO)" as your export format.': '銀行明細書で「QuickBooks（QBO）」をエクスポート形式として選択するだけです。',
            'VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop.': 'VaultCaddyは適切にフォーマットされたQBOファイルを生成し、QuickBooks OnlineまたはDesktopに直接インポートできます。',
            'No manual formatting required.': '手動フォーマット不要。',
            
            'We use bank-level AES-256 encryption for all data.': 'すべてのデータに銀行レベルのAES-256暗号化を使用しています。',
            'is SOC 2 Type II certified and GDPR compliant.': 'はSOC 2 Type II認証を取得しており、GDPRに準拠しています。',
            'Bank statements are automatically deleted after 24 hours.': '銀行明細書は24時間後に自動削除されます。',
            "We\'ve had zero data breaches in 3+ years of operation.": '3年以上の運営でデータ侵害はゼロです。',
            
            'VaultCaddy supports unlimited batch processing.': 'VaultCaddyは無制限のバッチ処理をサポートしています。',
            'Upload 10, 50, or 100+': '10、50、または100以上の',
            'Bank statements simultaneously.': '銀行明細書を同時にアップロードできます。',
            'Each file is processed independently in 3-5 seconds.': '各ファイルは3〜5秒で独立して処理されます。',
            'Perfect for accounting firms or businesses with multiple accounts.': '会計事務所や複数のアカウントを持つ企業に最適です。',
        }
    
    elif lang == 'ko-KR':
        return {
            # Hero Section
            'CTBC Bank statements are converted to Excel in seconds': 'CTBC 은행 명세서가 몇 초 만에 Excel로 변환됩니다',
            'Scotiabank statements are converted to Excel in seconds': 'Scotiabank 명세서가 몇 초 만에 Excel로 변환됩니다',
            'are converted to Excel in seconds': '가 몇 초 만에 Excel로 변환됩니다',
            'the USA': '미국',
            
            # Features
            'Built specifically for Scotiabank statements': 'Scotiabank 명세서 전용 설계',
            'Built specifically for CTBC Bank statements': 'CTBC 은행 명세서 전용 설계',
            
            # FAQ
            'VaultCaddy achieves 98%+ accuracy for': 'VaultCaddy는',
            'using advanced AI specifically trained on': '형식으로 특별히 훈련된 고급 AI를 사용하여 98% 이상의 정확도를 달성합니다.',
            'formats. Our system recognizes all': '당사 시스템은 모든',
            'account types and handles various statement layouts with industry-leading precision.': '계정 유형을 인식하고 업계 최고의 정밀도로 다양한 명세서 레이아웃을 처리합니다.',
            
            'After uploading your': '업로드 후',
            'Bank statement, simply select "QuickBooks (QBO)" as your export format.': '은행 명세서에서 "QuickBooks (QBO)"를 내보내기 형식으로 선택하기만 하면 됩니다.',
            'VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop.': 'VaultCaddy는 QuickBooks Online 또는 Desktop으로 직접 가져올 수 있는 올바른 형식의 QBO 파일을 생성합니다.',
            'No manual formatting required.': '수동 형식 지정이 필요하지 않습니다.',
            
            'We use bank-level AES-256 encryption for all data.': '모든 데이터에 은행 수준의 AES-256 암호화를 사용합니다.',
            'is SOC 2 Type II certified and GDPR compliant.': '는 SOC 2 Type II 인증을 받았으며 GDPR을 준수합니다.',
            'Bank statements are automatically deleted after 24 hours.': '은행 명세서는 24시간 후 자동으로 삭제됩니다.',
            "We\'ve had zero data breaches in 3+ years of operation.": '3년 이상의 운영에서 데이터 침해가 없습니다.',
            
            'VaultCaddy supports unlimited batch processing.': 'VaultCaddy는 무제한 배치 처리를 지원합니다.',
            'Upload 10, 50, or 100+': '10, 50 또는 100개 이상의',
            'Bank statements simultaneously.': '은행 명세서를 동시에 업로드할 수 있습니다.',
            'Each file is processed independently in 3-5 seconds.': '각 파일은 3-5초 내에 독립적으로 처리됩니다.',
            'Perfect for accounting firms or businesses with multiple accounts.': '회계 사무소 또는 여러 계정을 가진 기업에 적합합니다.',
        }
    
    return {}

def fix_file(file_path, lang):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = get_all_replacements(lang)
        
        # 逐个替换
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # 写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 失败: {file_path.name} - {e}")
        return False

def main():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    print("🔥 最终完整修复开始...")
    print("=" * 80)
    
    languages = {
        'zh-TW': '台湾',
        'zh-HK': '香港',
        'ja-JP': '日本',
        'ko-KR': '韩国'
    }
    
    for lang_code, lang_name in languages.items():
        print(f"\n{'='*80}")
        print(f"修复 {lang_name} 版本 ({lang_code})...")
        print(f"{'='*80}")
        
        lang_dir = root_dir / lang_code
        if not lang_dir.exists():
            print(f"  ⚠️ 目录不存在: {lang_dir}")
            continue
        
        lang_files = list(lang_dir.glob('*-v3.html'))
        lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
        
        print(f"  找到 {len(lang_files)} 个页面")
        
        fixed_count = 0
        for i, file_path in enumerate(lang_files, 1):
            if fix_file(file_path, lang_code):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
    
    print("\n" + "=" * 80)
    print("🎉 最终完整修复完成！")
    print("=" * 80)
    print("\n请刷新浏览器并验证：")
    print("  - https://vaultcaddy.com/zh-TW/ctbc-bank-statement-v3.html")
    print("  - https://vaultcaddy.com/ja-JP/scotiabank-statement-v3.html")

if __name__ == '__main__':
    main()

