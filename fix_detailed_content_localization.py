#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有详细内容的本地化
包括：卡片描述、段落文字、长文本等
"""

import os
import re
from pathlib import Path
from datetime import datetime

class DetailedContentLocalizer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        
        # 完整的详细内容翻译
        self.detailed_translations = {
            'zh-TW': {
                # 大标题
                'Why Choose VaultCaddy?': '為什麼選擇 VaultCaddy？',
                'See VaultCaddy in Action': '查看 VaultCaddy 實際運作',
                
                # 卡片标题
                '98% AI 準確率': '98% AI 準確率',
                '3-Second 處理速度': '3秒 處理速度',
                'Batch 處理速度': '批量 處理速度',
                '多種匯出格式': '多種匯出格式',
                '銀行級安全': '銀行級安全',
                '專家支援': '專家支援',
                
                # 卡片内容 - AI准确率
                'Handles checking, savings, credit cards, and business accounts with industry-leading precision.': 
                '處理支票、儲蓄、信用卡和商業帳戶，具備業界領先的精確度。',
                
                'We support all Chase account types including checking, savings, credit cards, and business accounts.':
                '我們支援所有 Chase 帳戶類型，包括支票、儲蓄、信用卡和商業帳戶。',
                
                # 卡片内容 - 处理速度
                'Batch upload supported.': '支援批量上傳。',
                
                'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.':
                '匯出至 Excel、CSV、QuickBooks (QBO) 或 Xero。預先格式化，可直接匯入您的會計軟體。',
                
                # AI处理速度详细描述
                'automatically extracts all transactions, dates, amounts, and descriptions with':
                '自動提取所有交易、日期、金額和描述，準確率達',
                
                'in just': '僅需',
                
                # 匯出格式详细描述
                'Choose your preferred': '選擇您偏好的',
                
                'Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.':
                'Excel (XLSX)、CSV、QuickBooks (QBO) 或 Xero。我們的匯出檔案已預先格式化，無需手動調整即可匯入。',
                
                # 验证和储存
                'Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files':
                '在我們的儀表板中查看提取的數據。進行必要的調整，然後下載或直接同步至您的會計軟體。所有檔案將在',
                
                'after 24 hours.': '24小時後自動刪除。',
                
                # 其他常见短语
                'Try 20 pages': '試用20頁',
                '無需信用卡': '無需信用卡',
            },
            'zh-HK': {
                # 大标题
                'Why Choose VaultCaddy?': '為什麼選擇 VaultCaddy？',
                'See VaultCaddy in Action': '查看 VaultCaddy 實際運作',
                
                # 卡片标题
                '98% AI 準確率': '98% AI 準確率',
                '3-Second 處理速度': '3秒 處理速度',
                'Batch 處理速度': '批量 處理速度',
                '多種匯出格式': '多種匯出格式',
                '銀行級安全': '銀行級安全',
                '專家支援': '專家支援',
                
                # 卡片内容
                'Handles checking, savings, credit cards, and business accounts with industry-leading precision.':
                '處理支票、儲蓄、信用卡和商業帳戶，具備業界領先的精確度。',
                
                'We support all Chase account types including checking, savings, credit cards, and business accounts.':
                '我們支援所有 Chase 帳戶類型，包括支票、儲蓄、信用卡和商業帳戶。',
                
                'Batch upload supported.': '支援批量上傳。',
                
                'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.':
                '匯出至 Excel、CSV、QuickBooks (QBO) 或 Xero。預先格式化，可直接匯入您的會計軟件。',
                
                'automatically extracts all transactions, dates, amounts, and descriptions with':
                '自動提取所有交易、日期、金額和描述，準確率達',
                
                'in just': '僅需',
                
                'Choose your preferred': '選擇您偏好的',
                
                'Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.':
                'Excel (XLSX)、CSV、QuickBooks (QBO) 或 Xero。我們的匯出檔案已預先格式化，無需手動調整即可匯入。',
                
                'Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files':
                '在我們的儀表板中查看提取的數據。進行必要的調整，然後下載或直接同步至您的會計軟件。所有檔案將在',
                
                'after 24 hours.': '24小時後自動刪除。',
            },
            'ko-KR': {
                # 大标题
                'Why Choose VaultCaddy?': 'VaultCaddy를 선택하는 이유?',
                'See VaultCaddy in Action': 'VaultCaddy 실제 작동 보기',
                
                # 卡片标题
                '98% AI 準確率': '98% AI 정확도',
                '3-Second 處理速度': '3초 처리 속도',
                'Batch 處理速度': '일괄 처리 속도',
                '多種匯出格式': '다양한 내보내기 형식',
                '銀行級安全': '은행급 보안',
                '專家支援': '전문가 지원',
                
                # 卡片内容
                'Handles checking, savings, credit cards, and business accounts with industry-leading precision.':
                '업계 최고의 정확도로 당좌, 저축, 신용카드 및 비즈니스 계정을 처리합니다.',
                
                'We support all Chase account types including checking, savings, credit cards, and business accounts.':
                '당좌, 저축, 신용카드 및 비즈니스 계정을 포함한 모든 Chase 계정 유형을 지원합니다.',
                
                'Batch upload supported.': '일괄 업로드 지원.',
                
                'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.':
                'Excel, CSV, QuickBooks (QBO) 또는 Xero로 내보내기. 사전 포맷되어 회계 소프트웨어로 바로 가져올 수 있습니다.',
                
                'automatically extracts all transactions, dates, amounts, and descriptions with':
                '모든 거래, 날짜, 금액 및 설명을 자동으로 추출하며 정확도는',
                
                'in just': '단',
                
                'Choose your preferred': '원하는',
                
                'Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.':
                'Excel (XLSX), CSV, QuickBooks (QBO) 또는 Xero를 선택하세요. 수동 조정 없이 바로 가져올 수 있도록 사전 포맷되어 있습니다.',
                
                'Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files':
                '대시보드에서 추출된 데이터를 검토하세요. 필요한 조정을 한 후 다운로드하거나 회계 소프트웨어와 직접 동기화하세요. 모든 파일은',
                
                'after 24 hours.': '24시간 후 자동 삭제됩니다.',
            },
            'ja-JP': {
                # 大标题
                'Why Choose VaultCaddy?': 'VaultCaddyを選ぶ理由？',
                'See VaultCaddy in Action': 'VaultCaddyの実際の動作を見る',
                
                # 卡片标题
                '98% AI 準確率': '98% AI 精度',
                '3-Second 處理速度': '3秒 処理速度',
                'Batch 處理速度': 'バッチ 処理速度',
                '多種匯出格式': '複数のエクスポート形式',
                '銀行級安全': '銀行レベルのセキュリティ',
                '專家支援': '専門家サポート',
                
                # 卡片内容
                'Handles checking, savings, credit cards, and business accounts with industry-leading precision.':
                '業界最高レベルの精度で当座預金、普通預金、クレジットカード、ビジネスアカウントを処理します。',
                
                'We support all Chase account types including checking, savings, credit cards, and business accounts.':
                '当座預金、普通預金、クレジットカード、ビジネスアカウントを含むすべてのChaseアカウントタイプをサポートしています。',
                
                'Batch upload supported.': 'バッチアップロードに対応。',
                
                'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.':
                'Excel、CSV、QuickBooks（QBO）、またはXeroにエクスポート。事前にフォーマットされており、会計ソフトウェアにすぐにインポートできます。',
                
                'automatically extracts all transactions, dates, amounts, and descriptions with':
                'すべての取引、日付、金額、説明を自動的に抽出し、精度は',
                
                'in just': 'わずか',
                
                'Choose your preferred': 'お好みの',
                
                'Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.':
                'Excel（XLSX）、CSV、QuickBooks（QBO）、またはXeroを選択してください。手動調整なしですぐにインポートできるよう事前にフォーマットされています。',
                
                'Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files':
                'ダッシュボードで抽出されたデータを確認してください。必要な調整を行った後、ダウンロードするか、会計ソフトウェアと直接同期してください。すべてのファイルは',
                
                'after 24 hours.': '24時間後に自動削除されます。',
            },
        }
    
    def fix_file(self, file_path, lang_code):
        """修复单个文件的详细内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            translations = self.detailed_translations.get(lang_code)
            
            if not translations:
                return False
            
            # 替换所有详细内容
            for english, localized in translations.items():
                # 使用更灵活的匹配
                content = content.replace(english, localized)
                # 同时尝试匹配可能有额外空格的版本
                content = re.sub(re.escape(english), localized, content, flags=re.IGNORECASE)
            
            # 检查是否有变化
            if content != original_content:
                # 备份
                backup_path = str(file_path) + '.backup_detailed_loc'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 修复失败: {e}")
            return False
    
    def fix_directory(self, dir_name, lang_code):
        """修复目录中的所有文件"""
        dir_path = self.root_dir / dir_name
        
        if not dir_path.exists():
            return
        
        print(f"\n🔧 修复: {dir_name}/ → 详细内容本地化")
        
        html_files = list(dir_path.glob('**/*.html'))
        
        fixed_in_dir = 0
        for file_path in html_files:
            if 'backup' in file_path.name:
                continue
            
            if self.fix_file(file_path, lang_code):
                fixed_in_dir += 1
                self.fixed_count += 1
                print(f"  ✅ {file_path.name}")
        
        if fixed_in_dir > 0:
            print(f"  📊 修复了 {fixed_in_dir} 个文件")
        else:
            print(f"  ℹ️  没有需要修复的文件")
    
    def fix_all(self):
        """修复所有语言目录"""
        print("📝 修复所有详细内容的本地化...")
        print("=" * 80)
        print("包括: 卡片描述、段落文字、长句等所有详细内容")
        print("=" * 80)
        
        for lang_code in self.detailed_translations.keys():
            self.fix_directory(lang_code, lang_code)
        
        print("\n" + "=" * 80)
        print("🎉 详细内容本地化完成！")
        print("=" * 80)
        print(f"\n📊 总计修复了 {self.fixed_count} 个文件")
        
        if self.fixed_count > 0:
            print(f"\n💾 所有修改的文件都有备份（.backup_detailed_loc）")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   详细内容本地化修复工具                                       ║
║                                                                              ║
║  此工具将修复所有详细内容的英文                                               ║
║                                                                              ║
║  修复范围:                                                                    ║
║    ✓ 卡片标题和描述                                                           ║
║    ✓ 段落文字                                                                 ║
║    ✓ 长句和详细说明                                                           ║
║    ✓ 所有剩余的英文内容                                                       ║
║                                                                              ║
║  所有修改的文件都会创建备份 (.backup_detailed_loc)                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    localizer = DetailedContentLocalizer(root_dir)
    localizer.fix_all()
    
    print("\n" + "=" * 80)
    print("✅ 详细内容本地化完成！")
    print("=" * 80)
    print("\n请刷新浏览器测试！")

if __name__ == '__main__':
    main()

