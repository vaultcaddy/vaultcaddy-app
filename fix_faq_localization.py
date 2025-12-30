#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复FAQ部分的完整本地化
包括：FAQ问题和答案的完整翻译
"""

import os
import re
from pathlib import Path

class FAQLocalizer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        
        # FAQ翻译映射
        self.faq_translations = {
            'zh-TW': {
                # FAQ标题
                '常見問題': '常見問題',
                '關於 Chase Bank 對帳單 conversion': '關於 Chase Bank 對帳單轉換',
                
                # FAQ问题
                'VaultCaddy對於 Chase Bank 對帳單設計?': 'VaultCaddy 對 Chase Bank 對帳單的設計如何？',
                '支援哪些 Chase Bank account types are supported?': '支援哪些 Chase Bank 帳戶類型？',
                '如何將 Chase Bank 對帳單設計 to QuickBooks?': '如何將 Chase Bank 對帳單匯入 QuickBooks？',
                '我的 Chase Bank data secure with VaultCaddy?': '我的 Chase Bank 資料在 VaultCaddy 是否安全？',
                '我可以批次處理多份 Chase Bank 對帳單設計?': '我可以批次處理多份 Chase Bank 對帳單嗎？',
                
                # FAQ答案
                'VaultCaddy supports all Chase Bank account types: Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking.':
                'VaultCaddy 支援所有 Chase Bank 帳戶類型：Chase Total Checking、Chase Savings、Chase Business Complete Banking、Chase 信用卡（Sapphire、Freedom、Ink）、Chase Private Client 帳戶和 Chase First Banking。',
                
                'Yes! VaultCaddy includes direct QuickBooks export. After processing your Chase statement, select QuickBooks (QBO) format, and the file is ready to import into your QuickBooks account without any manual adjustments.':
                '是的！VaultCaddy 包含直接匯出至 QuickBooks 的功能。處理完您的 Chase 對帳單後，選擇 QuickBooks (QBO) 格式，檔案即可直接匯入您的 QuickBooks 帳戶，無需手動調整。',
                
                'Absolutely. VaultCaddy uses bank-level encryption (256-bit SSL) and is SOC 2 compliant. Your Chase Bank data is processed securely, and all files are automatically deleted after 24 hours.':
                '絕對安全。VaultCaddy 使用銀行級加密（256位元 SSL）並符合 SOC 2 標準。您的 Chase Bank 資料會被安全處理，所有檔案會在 24 小時後自動刪除。',
                
                'Yes! You can upload multiple Chase Bank statements at once. VaultCaddy will process all files in parallel, and you can download all results in a single batch, saving you significant time.':
                '可以！您可以一次上傳多份 Chase Bank 對帳單。VaultCaddy 會並行處理所有檔案，您可以一次性下載所有結果，大幅節省時間。',
            },
            'zh-HK': {
                # FAQ标题
                '常見問題': '常見問題',
                '關於 Chase Bank 對帳單 conversion': '關於 Chase Bank 對賬單轉換',
                
                # FAQ问题
                'VaultCaddy對於 Chase Bank 對帳單設計?': 'VaultCaddy 對 Chase Bank 對賬單的設計如何？',
                '支援哪些 Chase Bank account types are supported?': '支援哪些 Chase Bank 帳戶類型？',
                '如何將 Chase Bank 對帳單設計 to QuickBooks?': '如何將 Chase Bank 對賬單匯入 QuickBooks？',
                '我的 Chase Bank data secure with VaultCaddy?': '我的 Chase Bank 資料在 VaultCaddy 是否安全？',
                '我可以批次處理多份 Chase Bank 對帳單設計?': '我可以批次處理多份 Chase Bank 對賬單嗎？',
                
                # FAQ答案
                'VaultCaddy supports all Chase Bank account types: Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking.':
                'VaultCaddy 支援所有 Chase Bank 帳戶類型：Chase Total Checking、Chase Savings、Chase Business Complete Banking、Chase 信用卡（Sapphire、Freedom、Ink）、Chase Private Client 帳戶和 Chase First Banking。',
                
                'Yes! VaultCaddy includes direct QuickBooks export. After processing your Chase statement, select QuickBooks (QBO) format, and the file is ready to import into your QuickBooks account without any manual adjustments.':
                '是的！VaultCaddy 包含直接匯出至 QuickBooks 的功能。處理完您的 Chase 對賬單後，選擇 QuickBooks (QBO) 格式，檔案即可直接匯入您的 QuickBooks 帳戶，無需手動調整。',
                
                'Absolutely. VaultCaddy uses bank-level encryption (256-bit SSL) and is SOC 2 compliant. Your Chase Bank data is processed securely, and all files are automatically deleted after 24 hours.':
                '絕對安全。VaultCaddy 使用銀行級加密（256位元 SSL）並符合 SOC 2 標準。您的 Chase Bank 資料會被安全處理，所有檔案會在 24 小時後自動刪除。',
                
                'Yes! You can upload multiple Chase Bank statements at once. VaultCaddy will process all files in parallel, and you can download all results in a single batch, saving you significant time.':
                '可以！您可以一次上傳多份 Chase Bank 對賬單。VaultCaddy 會並行處理所有檔案，您可以一次性下載所有結果，大幅節省時間。',
            },
            'ko-KR': {
                # FAQ标题
                '常見問題': '자주 묻는 질문',
                '關於 Chase Bank 對帳單 conversion': 'Chase Bank 명세서 변환 정보',
                
                # FAQ问题
                'VaultCaddy對於 Chase Bank 對帳單設計?': 'VaultCaddy는 Chase Bank 명세서를 어떻게 처리하나요?',
                '支援哪些 Chase Bank account types are supported?': '어떤 Chase Bank 계정 유형을 지원하나요?',
                '如何將 Chase Bank 對帳單設計 to QuickBooks?': 'Chase Bank 명세서를 QuickBooks로 가져오는 방법은?',
                '我的 Chase Bank data secure with VaultCaddy?': 'VaultCaddy에서 내 Chase Bank 데이터는 안전한가요?',
                '我可以批次處理多份 Chase Bank 對帳單設計?': '여러 Chase Bank 명세서를 일괄 처리할 수 있나요?',
                
                # FAQ答案
                'VaultCaddy supports all Chase Bank account types: Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking.':
                'VaultCaddy는 모든 Chase Bank 계정 유형을 지원합니다: Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase 신용카드(Sapphire, Freedom, Ink), Chase Private Client 계정, Chase First Banking.',
                
                'Yes! VaultCaddy includes direct QuickBooks export. After processing your Chase statement, select QuickBooks (QBO) format, and the file is ready to import into your QuickBooks account without any manual adjustments.':
                '네! VaultCaddy는 QuickBooks로 직접 내보내기를 포함합니다. Chase 명세서를 처리한 후 QuickBooks (QBO) 형식을 선택하면 수동 조정 없이 QuickBooks 계정으로 바로 가져올 수 있습니다.',
                
                'Absolutely. VaultCaddy uses bank-level encryption (256-bit SSL) and is SOC 2 compliant. Your Chase Bank data is processed securely, and all files are automatically deleted after 24 hours.':
                '물론입니다. VaultCaddy는 은행급 암호화(256비트 SSL)를 사용하며 SOC 2를 준수합니다. Chase Bank 데이터는 안전하게 처리되며 모든 파일은 24시간 후 자동으로 삭제됩니다.',
                
                'Yes! You can upload multiple Chase Bank statements at once. VaultCaddy will process all files in parallel, and you can download all results in a single batch, saving you significant time.':
                '네! 여러 Chase Bank 명세서를 한 번에 업로드할 수 있습니다. VaultCaddy는 모든 파일을 병렬로 처리하며, 모든 결과를 한 번에 다운로드할 수 있어 시간을 크게 절약할 수 있습니다.',
            },
            'ja-JP': {
                # FAQ标题
                '常見問題': 'よくある質問',
                '關於 Chase Bank 對帳單 conversion': 'Chase Bank明細書の変換について',
                
                # FAQ问题
                'VaultCaddy對於 Chase Bank 對帳單設計?': 'VaultCaddyはChase Bank明細書をどのように処理しますか？',
                '支援哪些 Chase Bank account types are supported?': 'どのChase Bankアカウントタイプをサポートしていますか？',
                '如何將 Chase Bank 對帳單設計 to QuickBooks?': 'Chase Bank明細書をQuickBooksにインポートする方法は？',
                '我的 Chase Bank data secure with VaultCaddy?': 'VaultCaddyで私のChase Bankデータは安全ですか？',
                '我可以批次處理多份 Chase Bank 對帳單設計?': '複数のChase Bank明細書を一括処理できますか？',
                
                # FAQ答案
                'VaultCaddy supports all Chase Bank account types: Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking.':
                'VaultCaddyはすべてのChase Bankアカウントタイプをサポートしています：Chase Total Checking、Chase Savings、Chase Business Complete Banking、Chaseクレジットカード（Sapphire、Freedom、Ink）、Chase Private Clientアカウント、Chase First Banking。',
                
                'Yes! VaultCaddy includes direct QuickBooks export. After processing your Chase statement, select QuickBooks (QBO) format, and the file is ready to import into your QuickBooks account without any manual adjustments.':
                'はい！VaultCaddyはQuickBooksへの直接エクスポートを含みます。Chase明細書を処理した後、QuickBooks（QBO）形式を選択すると、手動調整なしでQuickBooksアカウントにすぐにインポートできます。',
                
                'Absolutely. VaultCaddy uses bank-level encryption (256-bit SSL) and is SOC 2 compliant. Your Chase Bank data is processed securely, and all files are automatically deleted after 24 hours.':
                'もちろんです。VaultCaddyは銀行レベルの暗号化（256ビットSSL）を使用し、SOC 2に準拠しています。Chase Bankデータは安全に処理され、すべてのファイルは24時間後に自動的に削除されます。',
                
                'Yes! You can upload multiple Chase Bank statements at once. VaultCaddy will process all files in parallel, and you can download all results in a single batch, saving you significant time.':
                'はい！複数のChase Bank明細書を一度にアップロードできます。VaultCaddyはすべてのファイルを並列処理し、すべての結果を一括でダウンロードできるため、大幅に時間を節約できます。',
            },
        }
    
    def fix_file(self, file_path, lang_code):
        """修复单个文件的FAQ本地化"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            translations = self.faq_translations.get(lang_code)
            
            if not translations:
                return False
            
            # 替换所有FAQ内容
            for english, localized in translations.items():
                content = content.replace(english, localized)
            
            # 检查是否有变化
            if content != original_content:
                # 备份
                backup_path = str(file_path) + '.backup_faq_loc'
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
        
        print(f"\n🔧 修复: {dir_name}/ → FAQ本地化")
        
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
        print("❓ 修复所有FAQ的本地化...")
        print("=" * 80)
        
        for lang_code in self.faq_translations.keys():
            self.fix_directory(lang_code, lang_code)
        
        print("\n" + "=" * 80)
        print("🎉 FAQ本地化完成！")
        print("=" * 80)
        print(f"\n📊 总计修复了 {self.fixed_count} 个文件")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FAQ本地化修复工具                                            ║
║                                                                              ║
║  此工具将修复FAQ部分的所有英文                                                ║
║                                                                              ║
║  修复范围:                                                                    ║
║    ✓ FAQ问题                                                                  ║
║    ✓ FAQ答案                                                                  ║
║    ✓ FAQ标题                                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    localizer = FAQLocalizer(root_dir)
    localizer.fix_all()
    
    print("\n" + "=" * 80)
    print("✅ FAQ本地化完成！")
    print("=" * 80)
    print("\n请刷新浏览器测试！")

if __name__ == '__main__':
    main()

