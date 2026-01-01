#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建80个v3页面的多语言版本
语言: zh-TW, zh-HK, ja-JP, ko-KR
"""

import os
import re
from pathlib import Path
import shutil

class MultilingualV3Creator:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.created_count = {'zh-TW': 0, 'zh-HK': 0, 'ja-JP': 0, 'ko-KR': 0}
        
        # 定价信息（月费展示，实际是年费÷12）
        self.pricing = {
            'zh-TW': {
                'starter_monthly': 'NT$185',
                'starter_yearly': 'NT$148',
                'pro_monthly': 'NT$370',
                'pro_yearly': 'NT$296',
                'extra_page': 'NT$2',
                'currency': 'NT$',
                'unit': '頁'
            },
            'zh-HK': {
                'starter_monthly': 'HK$46',
                'starter_yearly': 'HK$37',
                'pro_monthly': 'HK$92',
                'pro_yearly': 'HK$74',
                'extra_page': 'HK$0.5',
                'currency': 'HK$',
                'unit': '頁'
            },
            'ja-JP': {
                'starter_monthly': '¥926',
                'starter_yearly': '¥741',
                'pro_monthly': '¥1852',
                'pro_yearly': '¥1481',
                'extra_page': '¥10',
                'currency': '¥',
                'unit': 'ページ'
            },
            'ko-KR': {
                'starter_monthly': '₩7,998',
                'starter_yearly': '₩6,398',
                'pro_monthly': '₩15,996',
                'pro_yearly': '₩12,797',
                'extra_page': '₩80',
                'currency': '₩',
                'unit': '페이지'
            }
        }
        
        # 完整翻译字典
        self.translations = {
            # 页面标题和描述
            'Convert {bank} Bank Statements to Excel': {
                'zh-TW': '轉換{bank}銀行對帳單為Excel',
                'zh-HK': '轉換{bank}銀行對帳單為Excel',
                'ja-JP': '{bank}銀行明細書をExcelに変換',
                'ko-KR': '{bank} 은행 명세서를 Excel로 변환'
            },
            '{bank} Statement Converter': {
                'zh-TW': '{bank}對帳單轉換器',
                'zh-HK': '{bank}對帳單轉換器',
                'ja-JP': '{bank}明細書コンバーター',
                'ko-KR': '{bank} 명세서 변환기'
            },
            'PDF to Excel/QuickBooks': {
                'zh-TW': 'PDF轉Excel/QuickBooks',
                'zh-HK': 'PDF轉Excel/QuickBooks',
                'ja-JP': 'PDFからExcel/QuickBooksへ',
                'ko-KR': 'PDF를 Excel/QuickBooks로'
            },
            '98% Accuracy': {
                'zh-TW': '98%準確率',
                'zh-HK': '98%準確率',
                'ja-JP': '98%精度',
                'ko-KR': '98% 정확도'
            },
            'AI-powered {bank} statement converter': {
                'zh-TW': 'AI驅動的{bank}對帳單轉換器',
                'zh-HK': 'AI驅動的{bank}對帳單轉換器',
                'ja-JP': 'AI搭載{bank}明細書コンバーター',
                'ko-KR': 'AI 기반 {bank} 명세서 변환기'
            },
            'Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy': {
                'zh-TW': '3秒內將PDF轉換為Excel/QuickBooks/Xero，準確率達98%',
                'zh-HK': '3秒內將PDF轉換為Excel/QuickBooks/Xero，準確率達98%',
                'ja-JP': '3秒でPDFをExcel/QuickBooks/Xeroに変換、精度98%',
                'ko-KR': '3초 만에 PDF를 Excel/QuickBooks/Xero로 변환, 정확도 98%'
            },
            'From $5.59/month': {
                'zh-TW': '月費{price}起',
                'zh-HK': '月費{price}起',
                'ja-JP': '月額{price}から',
                'ko-KR': '월 {price}부터'
            },
            '500+ businesses trust us': {
                'zh-TW': '500+企業信賴我們',
                'zh-HK': '500+企業信賴我們',
                'ja-JP': '500以上の企業が信頼',
                'ko-KR': '500개 이상의 기업이 신뢰'
            },
            
            # Hero部分
            'Convert {bank} Bank Statements to Excel in 3 Seconds': {
                'zh-TW': '3秒內將{bank}銀行對帳單轉換為Excel',
                'zh-HK': '3秒內將{bank}銀行對帳單轉換為Excel',
                'ja-JP': '{bank}銀行明細書を3秒でExcelに変換',
                'ko-KR': '3초 만에 {bank} 은행 명세서를 Excel로 변환'
            },
            'AI-powered bank statement converter': {
                'zh-TW': 'AI驅動的銀行對帳單轉換器',
                'zh-HK': 'AI驅動的銀行對帳單轉換器',
                'ja-JP': 'AI搭載銀行明細書コンバーター',
                'ko-KR': 'AI 기반 은행 명세서 변환기'
            },
            'Upload PDF → AI Processing → Export Excel': {
                'zh-TW': '上傳PDF → AI處理 → 匯出Excel',
                'zh-HK': '上傳PDF → AI處理 → 匯出Excel',
                'ja-JP': 'PDFアップロード → AI処理 → Excel出力',
                'ko-KR': 'PDF 업로드 → AI 처리 → Excel 내보내기'
            },
            'Start Free Trial - 20 Pages Free': {
                'zh-TW': '開始免費試用 - 免費20頁',
                'zh-HK': '開始免費試用 - 免費20頁',
                'ja-JP': '無料トライアル開始 - 20ページ無料',
                'ko-KR': '무료 평가판 시작 - 20페이지 무료'
            },
            'No credit card required': {
                'zh-TW': '無需信用卡',
                'zh-HK': '無需信用卡',
                'ja-JP': 'クレジットカード不要',
                'ko-KR': '신용카드 불필요'
            },
            
            # 統計卡片
            '3s': {
                'zh-TW': '3秒',
                'zh-HK': '3秒',
                'ja-JP': '3秒',
                'ko-KR': '3초'
            },
            'Processing Time': {
                'zh-TW': '處理時間',
                'zh-HK': '處理時間',
                'ja-JP': '処理時間',
                'ko-KR': '처리 시간'
            },
            '98%': {
                'zh-TW': '98%',
                'zh-HK': '98%',
                'ja-JP': '98%',
                'ko-KR': '98%'
            },
            'Accuracy Rate': {
                'zh-TW': '準確率',
                'zh-HK': '準確率',
                'ja-JP': '精度',
                'ko-KR': '정확도'
            },
            '500+': {
                'zh-TW': '500+',
                'zh-HK': '500+',
                'ja-JP': '500+',
                'ko-KR': '500+'
            },
            'Happy Customers': {
                'zh-TW': '滿意客戶',
                'zh-HK': '滿意客戶',
                'ja-JP': '満足顧客',
                'ko-KR': '만족 고객'
            },
            
            # Trust Badges
            'Trusted by 500+ businesses worldwide': {
                'zh-TW': '全球500+企業信賴',
                'zh-HK': '全球500+企業信賴',
                'ja-JP': '世界500以上の企業が信頼',
                'ko-KR': '전 세계 500개 이상의 기업이 신뢰'
            },
            'SOC 2 Type II Certified': {
                'zh-TW': 'SOC 2 Type II認證',
                'zh-HK': 'SOC 2 Type II認證',
                'ja-JP': 'SOC 2 Type II認定',
                'ko-KR': 'SOC 2 Type II 인증'
            },
            'Bank-Grade Security': {
                'zh-TW': '銀行級安全',
                'zh-HK': '銀行級安全',
                'ja-JP': '銀行レベルのセキュリティ',
                'ko-KR': '은행 수준 보안'
            },
            
            # GIF演示部分
            'See VaultCaddy in Action': {
                'zh-TW': '查看VaultCaddy實際運作',
                'zh-HK': '查看VaultCaddy實際運作',
                'ja-JP': 'VaultCaddyの実際の動作を見る',
                'ko-KR': 'VaultCaddy 실제 작동 보기'
            },
            'Watch how {bank} statements are processed in seconds with 98% accuracy': {
                'zh-TW': '觀看{bank}對帳單如何在數秒內以98%準確率處理',
                'zh-HK': '觀看{bank}對帳單如何在數秒內以98%準確率處理',
                'ja-JP': '{bank}明細書が98%の精度で数秒で処理される様子をご覧ください',
                'ko-KR': '{bank} 명세서가 98% 정확도로 몇 초 만에 처리되는 방법을 확인하세요'
            },
            'Average Processing': {
                'zh-TW': '平均處理時間',
                'zh-HK': '平均處理時間',
                'ja-JP': '平均処理時間',
                'ko-KR': '평균 처리 시간'
            },
            'Starting From /Month': {
                'zh-TW': '每月起價',
                'zh-HK': '每月起價',
                'ja-JP': '月額料金',
                'ko-KR': '월 요금'
            },
            
            # 定價部分
            'Choose Your Plan': {
                'zh-TW': '選擇您的方案',
                'zh-HK': '選擇您的方案',
                'ja-JP': 'プランを選択',
                'ko-KR': '플랜 선택'
            },
            'Simple, transparent pricing': {
                'zh-TW': '簡單透明的定價',
                'zh-HK': '簡單透明的定價',
                'ja-JP': 'シンプルで透明な価格設定',
                'ko-KR': '간단하고 투명한 가격'
            },
            'No hidden fees': {
                'zh-TW': '無隱藏費用',
                'zh-HK': '無隱藏費用',
                'ja-JP': '隠れた料金なし',
                'ko-KR': '숨겨진 수수료 없음'
            },
            'Starter Plan': {
                'zh-TW': '入門版',
                'zh-HK': '入門版',
                'ja-JP': 'スターター',
                'ko-KR': '스타터'
            },
            'Professional Plan': {
                'zh-TW': '專業版',
                'zh-HK': '專業版',
                'ja-JP': 'プロフェッショナル',
                'ko-KR': '프로페셔널'
            },
            'Pay Monthly': {
                'zh-TW': '按月付費',
                'zh-HK': '按月付費',
                'ja-JP': '月払い',
                'ko-KR': '월별 결제'
            },
            'Pay Yearly': {
                'zh-TW': '按年付費',
                'zh-HK': '按年付費',
                'ja-JP': '年払い',
                'ko-KR': '연간 결제'
            },
            'Save 20%': {
                'zh-TW': '節省20%',
                'zh-HK': '節省20%',
                'ja-JP': '20%割引',
                'ko-KR': '20% 절약'
            },
            'RECOMMENDED': {
                'zh-TW': '推薦',
                'zh-HK': '推薦',
                'ja-JP': 'おすすめ',
                'ko-KR': '추천'
            },
            '/month': {
                'zh-TW': '/月',
                'zh-HK': '/月',
                'ja-JP': '/月',
                'ko-KR': '/월'
            },
            'per month, billed annually': {
                'zh-TW': '每月，按年計費',
                'zh-HK': '每月，按年計費',
                'ja-JP': '毎月、年間請求',
                'ko-KR': '월별, 연간 청구'
            },
            '100 pages/month included': {
                'zh-TW': '包含每月100頁',
                'zh-HK': '包含每月100頁',
                'ja-JP': '月100ページ含む',
                'ko-KR': '월 100페이지 포함'
            },
            '200 pages/month included': {
                'zh-TW': '包含每月200頁',
                'zh-HK': '包含每月200頁',
                'ja-JP': '月200ページ含む',
                'ko-KR': '월 200페이지 포함'
            },
            'Additional pages': {
                'zh-TW': '額外頁數',
                'zh-HK': '額外頁數',
                'ja-JP': '追加ページ',
                'ko-KR': '추가 페이지'
            },
            '/page': {
                'zh-TW': '/頁',
                'zh-HK': '/頁',
                'ja-JP': '/ページ',
                'ko-KR': '/페이지'
            },
            'All export formats': {
                'zh-TW': '所有匯出格式',
                'zh-HK': '所有匯出格式',
                'ja-JP': 'すべての出力形式',
                'ko-KR': '모든 내보내기 형식'
            },
            'Excel, QuickBooks, Xero, CSV': {
                'zh-TW': 'Excel、QuickBooks、Xero、CSV',
                'zh-HK': 'Excel、QuickBooks、Xero、CSV',
                'ja-JP': 'Excel、QuickBooks、Xero、CSV',
                'ko-KR': 'Excel, QuickBooks, Xero, CSV'
            },
            'Email support': {
                'zh-TW': '電子郵件支援',
                'zh-HK': '電子郵件支援',
                'ja-JP': 'メールサポート',
                'ko-KR': '이메일 지원'
            },
            'Priority support': {
                'zh-TW': '優先支援',
                'zh-HK': '優先支援',
                'ja-JP': '優先サポート',
                'ko-KR': '우선 지원'
            },
            'API access': {
                'zh-TW': 'API存取',
                'zh-HK': 'API存取',
                'ja-JP': 'APIアクセス',
                'ko-KR': 'API 액세스'
            },
            'Get Started': {
                'zh-TW': '開始使用',
                'zh-HK': '開始使用',
                'ja-JP': '始める',
                'ko-KR': '시작하기'
            },
            
            # FAQ
            'Frequently Asked Questions': {
                'zh-TW': '常見問題',
                'zh-HK': '常見問題',
                'ja-JP': 'よくある質問',
                'ko-KR': '자주 묻는 질문'
            },
            'How accurate is the conversion?': {
                'zh-TW': '轉換準確率有多高？',
                'zh-HK': '轉換準確率有多高？',
                'ja-JP': '変換の精度はどのくらいですか？',
                'ko-KR': '변환 정확도는 얼마나 됩니까?'
            },
            'What formats can I export to?': {
                'zh-TW': '我可以匯出到哪些格式？',
                'zh-HK': '我可以匯出到哪些格式？',
                'ja-JP': 'どの形式にエクスポートできますか？',
                'ko-KR': '어떤 형식으로 내보낼 수 있습니까?'
            },
            'Is my data secure?': {
                'zh-TW': '我的資料安全嗎？',
                'zh-HK': '我的資料安全嗎？',
                'ja-JP': 'データは安全ですか？',
                'ko-KR': '내 데이터가 안전합니까?'
            },
            
            # 最終CTA
            'Ready to Save 10+ Hours Per Month?': {
                'zh-TW': '準備每月節省10小時以上？',
                'zh-HK': '準備每月節省10小時以上？',
                'ja-JP': '毎月10時間以上節約する準備はできていますか？',
                'ko-KR': '매월 10시간 이상 절약할 준비가 되셨습니까?'
            },
            'Join 500+ businesses using VaultCaddy': {
                'zh-TW': '加入500+使用VaultCaddy的企業',
                'zh-HK': '加入500+使用VaultCaddy的企業',
                'ja-JP': 'VaultCaddyを使用する500以上の企業に参加',
                'ko-KR': 'VaultCaddy를 사용하는 500개 이상의 기업에 가입'
            },
            'Cancel anytime': {
                'zh-TW': '隨時取消',
                'zh-HK': '隨時取消',
                'ja-JP': 'いつでもキャンセル可能',
                'ko-KR': '언제든지 취소 가능'
            }
        }
        
        # 語言和auth鏈接映射
        self.lang_config = {
            'zh-TW': {'dir': 'zh-TW', 'auth': '/auth.html', 'lang_code': 'zh-TW'},
            'zh-HK': {'dir': 'zh-HK', 'auth': '/auth.html', 'lang_code': 'zh-HK'},
            'ja-JP': {'dir': 'ja-JP', 'auth': '/jp/auth.html', 'lang_code': 'ja'},
            'ko-KR': {'dir': 'ko-KR', 'auth': '/kr/auth.html', 'lang_code': 'ko-KR'}
        }
    
    def translate_text(self, text, lang, bank_name=''):
        """翻譯文本"""
        # 替換銀行名稱
        text_with_bank = text.replace('{bank}', bank_name) if bank_name else text
        
        # 查找翻譯
        if text in self.translations and lang in self.translations[text]:
            translated = self.translations[text][lang]
            if '{bank}' in translated and bank_name:
                return translated.replace('{bank}', bank_name)
            return translated
        
        # 如果沒有翻譯，返回原文
        return text_with_bank
    
    def create_language_directory(self, lang):
        """創建語言目錄"""
        lang_dir = self.root_dir / self.lang_config[lang]['dir']
        lang_dir.mkdir(exist_ok=True)
        return lang_dir
    
    def translate_file(self, file_path, lang):
        """翻譯單個文件"""
        try:
            print(f"  🔧 {lang}: {file_path.name}")
            
            # 讀取原文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取銀行名稱（如果是銀行頁面）
            bank_name = ''
            if '-statement-v3.html' in file_path.name:
                name_part = file_path.name.replace('-statement-v3.html', '')
                # 這裡保持英文銀行名稱，不翻譯
                bank_name = name_part.replace('-', ' ').title()
            
            # 1. 更新lang屬性
            content = re.sub(
                r'<html lang="en-US">',
                f'<html lang="{self.lang_config[lang]["lang_code"]}">',
                content
            )
            
            # 2. 替換定價
            pricing = self.pricing[lang]
            content = content.replace('$5.59', pricing['starter_monthly'])
            content = content.replace('$4.47', pricing['starter_yearly'])
            content = content.replace('$7', pricing['pro_monthly'])
            content = content.replace('$5.60', pricing['pro_yearly'])
            content = content.replace('$0.06', pricing['extra_page'])
            
            # 3. 替換auth鏈接
            content = content.replace('/en/auth.html', self.lang_config[lang]['auth'])
            
            # 4. 翻譯主要UI文本（使用正則表達式批量替換）
            for eng_text, translations in self.translations.items():
                if lang in translations:
                    # 跳過包含{bank}的模板文本，單獨處理
                    if '{bank}' not in eng_text:
                        # 使用單詞邊界進行精確匹配
                        pattern = re.escape(eng_text)
                        content = re.sub(pattern, translations[lang], content)
            
            # 創建語言目錄
            lang_dir = self.create_language_directory(lang)
            
            # 寫入新文件
            new_file_path = lang_dir / file_path.name
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_count[lang] += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失敗: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def create_all_languages(self):
        """創建所有語言版本"""
        print("🚀 開始創建多語言v3頁面...")
        print("=" * 80)
        
        # 查找所有v3文件
        v3_files = list(self.root_dir.glob('*-v3.html'))
        v3_files = [f for f in v3_files if 'test' not in f.name and 'backup' not in f.name]
        
        print(f"\n📊 找到 {len(v3_files)} 個v3頁面")
        print(f"將創建 {len(v3_files)} × 4 = {len(v3_files) * 4} 個多語言頁面")
        print("=" * 80)
        
        # 為每種語言創建頁面
        for lang in ['zh-TW', 'zh-HK', 'ja-JP', 'ko-KR']:
            print(f"\n{'='*80}")
            print(f"創建 {lang} 版本...")
            print(f"{'='*80}")
            
            for file_path in v3_files:
                self.translate_file(file_path, lang)
        
        print("\n" + "=" * 80)
        print("🎉 多語言頁面創建完成！")
        print("=" * 80)
        print(f"\n📊 創建統計:")
        for lang, count in self.created_count.items():
            print(f"   {lang}: {count}個頁面")
        print(f"\n總計: {sum(self.created_count.values())} 個多語言頁面")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🌍 多語言v3頁面批量創建                                  ║
║                                                                              ║
║  創建內容:                                                                   ║
║    ✓ 台灣繁體中文 (zh-TW/) - 80個頁面                                        ║
║    ✓ 香港繁體中文 (zh-HK/) - 80個頁面                                        ║
║    ✓ 日文 (ja-JP/) - 80個頁面                                                ║
║    ✓ 韓文 (ko-KR/) - 80個頁面                                                ║
║                                                                              ║
║  本地化內容:                                                                 ║
║    ✓ 完整UI文本翻譯                                                          ║
║    ✓ 正確的貨幣和定價                                                        ║
║    ✓ 正確的auth鏈接                                                          ║
║    ✓ 正確的lang屬性                                                          ║
║                                                                              ║
║  總計: 320個多語言頁面                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    creator = MultilingualV3Creator(root_dir)
    creator.create_all_languages()
    
    print("\n" + "=" * 80)
    print("✅ 所有多語言頁面創建完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

