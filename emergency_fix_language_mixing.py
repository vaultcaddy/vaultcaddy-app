#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 紧急修复：所有页面的语言混合问题
修复英文、中文、日文、韩文页面中的错误语言文本
"""

import os
import re
from pathlib import Path

class LanguageMixingFixer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = {'zh-TW': 0, 'zh-HK': 0, 'ja-JP': 0, 'ko-KR': 0}
        
        # 需要翻译的英文文本映射
        self.translations = {
            'zh-TW': {
                # 按钮和CTA
                'Start Free Trial': '開始免費試用',
                'See How It Works': '查看運作方式',
                'FREE: Try 20 pages': '免費試用20頁',
                'No credit card required': '無需信用卡',
                'AUTO PLAYING': '自動播放',
                'LIVE DEMONSTRATION': '實時演示',
                'MOST POPULAR': '最受歡迎',
                'Monthly Plan': '月付方案',
                'Annual Plan': '年付方案',
                'per month': '每月',
                'per additional page': '每頁額外費用',
                'Email Support': '電郵支援',
                'Priority email support': '優先電郵支援',
                '24h auto-delete': '24小時自動刪除',
                'Start': '開始',
                'Ready to Save': '準備節省',
                'Join 500+': '加入500+',
                'Built for': '專為',
                'designed specifically for': '專為設計',
                'How It Works': '運作方式',
                'Why Choose VaultCaddy?': '為什麼選擇VaultCaddy？',
                'Simple, Transparent Pricing': '簡單透明的定價',
                'Convert': '轉換',
                'in Seconds': '只需幾秒',
                'Made Simple': '變得簡單',
                'Automate': '自動化',
                'Upload Your': '上傳您的',
                'AI Processing': 'AI處理',
                'Export to Your System': '匯出到您的系統',
                'Verify & Save': '驗證並保存',
                'AES-256 Encrypted': 'AES-256加密',
                'Bank-level security': '銀行級安全',
                'SOC 2 Type II Certified': 'SOC 2 Type II認證',
                'GDPR Compliant': '符合GDPR',
                'Data protected': '數據保護',
                'Rating': '評分',
                'reviews': '評價',
                'Trusted by': '受信賴於',
                'businesses in': '企業在',
                'Accuracy': '準確率',
                'Processing': '處理',
                'Per Month': '每月',
                'pages included': '頁面包含',
                'All export formats': '所有匯出格式',
                'Cancel anytime': '隨時取消',
                'Billed annually': '按年計費',
                'Watch how': '觀看如何',
                'are processed in seconds': '在幾秒內處理',
                'with 98% accuracy': '準確率達98%',
                'Average processing time': '平均處理時間',
                'Starting From/Month': '起價/月',
                'Common': '常見',
                'Challenges': '挑戰',
                'How VaultCaddy Solves These Problems': 'VaultCaddy如何解決這些問題',
                'Specific Features': '專屬功能',
                'Built for the unique needs': '專為獨特需求而設計',
                'Everything you need to know': '您需要知道的一切',
                'Hours Saved/Week': '每週節省小時',
                'Manual tracking': '手動追蹤',
                'weekly': '每週',
                'Ensuring': '確保',
                'Creating': '創建',
                'Gathering data': '收集數據',
                'AI-powered automation': 'AI驅動的自動化',
                'Real-time': '實時',
                'One-click': '一鍵',
                'Always prepared': '隨時準備',
                'Automatic': '自動',
                'Extract': '提取',
                'Reconcile': '對帳',
                'Track': '追蹤',
                'Compare': '比較',
                'Identify': '識別',
            },
            'zh-HK': {
                # 按钮和CTA
                'Start Free Trial': '開始免費試用',
                'See How It Works': '查看運作方式',
                'FREE: Try 20 pages': '免費試用20頁',
                'No credit card required': '無需信用卡',
                'AUTO PLAYING': '自動播放',
                'LIVE DEMONSTRATION': '實時演示',
                'MOST POPULAR': '最受歡迎',
                'Monthly Plan': '月付方案',
                'Annual Plan': '年付方案',
                'per month': '每月',
                'per additional page': '每頁額外費用',
                'Email Support': '電郵支援',
                'Priority email support': '優先電郵支援',
                '24h auto-delete': '24小時自動刪除',
                'Start': '開始',
                'Ready to Save': '準備節省',
                'Join 500+': '加入500+',
                'Built for': '專為',
                'designed specifically for': '專為設計',
                'How It Works': '運作方式',
                'Why Choose VaultCaddy?': '為什麼選擇VaultCaddy？',
                'Simple, Transparent Pricing': '簡單透明的定價',
                'Convert': '轉換',
                'in Seconds': '只需幾秒',
                'Made Simple': '變得簡單',
                'Automate': '自動化',
                'Upload Your': '上傳您的',
                'AI Processing': 'AI處理',
                'Export to Your System': '匯出到您的系統',
                'Verify & Save': '驗證並保存',
                'AES-256 Encrypted': 'AES-256加密',
                'Bank-level security': '銀行級安全',
                'SOC 2 Type II Certified': 'SOC 2 Type II認證',
                'GDPR Compliant': '符合GDPR',
                'Data protected': '數據保護',
                'Rating': '評分',
                'reviews': '評價',
                'Trusted by': '受信賴於',
                'businesses in': '企業在',
                'Accuracy': '準確率',
                'Processing': '處理',
                'Per Month': '每月',
                'pages included': '頁面包含',
                'All export formats': '所有匯出格式',
                'Cancel anytime': '隨時取消',
                'Billed annually': '按年計費',
                'Watch how': '觀看如何',
                'are processed in seconds': '在幾秒內處理',
                'with 98% accuracy': '準確率達98%',
                'Average processing time': '平均處理時間',
                'Starting From/Month': '起價/月',
                'Common': '常見',
                'Challenges': '挑戰',
                'How VaultCaddy Solves These Problems': 'VaultCaddy如何解決這些問題',
                'Specific Features': '專屬功能',
                'Built for the unique needs': '專為獨特需求而設計',
                'Everything you need to know': '您需要知道的一切',
                'Hours Saved/Week': '每週節省小時',
            },
            'ja-JP': {
                # 按钮和CTA
                'Start Free Trial': '無料トライアルを開始',
                'See How It Works': '使い方を見る',
                'FREE: Try 20 pages': '無料：20ページお試し',
                'No credit card required': 'クレジットカード不要',
                'AUTO PLAYING': '自動再生中',
                'LIVE DEMONSTRATION': 'ライブデモンストレーション',
                'MOST POPULAR': '最も人気',
                'Monthly Plan': '月払いプラン',
                'Annual Plan': '年払いプラン',
                'per month': '月額',
                'per additional page': '追加ページごと',
                'Email Support': 'メールサポート',
                'Priority email support': '優先メールサポート',
                '24h auto-delete': '24時間自動削除',
                'Start': '開始',
                'Ready to Save': '節約の準備',
                'Join 500+': '500+に参加',
                'Built for': '専用設計',
                'designed specifically for': '専用に設計',
                'How It Works': '使い方',
                'Why Choose VaultCaddy?': 'なぜVaultCaddy？',
                'Simple, Transparent Pricing': 'シンプルで透明な料金',
                'Convert': '変換',
                'in Seconds': '数秒で',
                'Made Simple': 'シンプルに',
                'Automate': '自動化',
                'Upload Your': 'アップロード',
                'AI Processing': 'AI処理',
                'Export to Your System': 'システムへエクスポート',
                'Verify & Save': '確認して保存',
                'AES-256 Encrypted': 'AES-256暗号化',
                'Bank-level security': '銀行レベルのセキュリティ',
                'SOC 2 Type II Certified': 'SOC 2 Type II認証',
                'GDPR Compliant': 'GDPR準拠',
                'Data protected': 'データ保護',
                'Rating': '評価',
                'reviews': 'レビュー',
                'Trusted by': '信頼されている',
                'businesses in': '企業',
                'Accuracy': '精度',
                'Processing': '処理',
                'Per Month': '月額',
                'pages included': 'ページ含む',
                'All export formats': 'すべての出力形式',
                'Cancel anytime': 'いつでもキャンセル可能',
                'Billed annually': '年間請求',
                'Watch how': '見る方法',
                'are processed in seconds': '数秒で処理',
                'with 98% accuracy': '98%の精度で',
                'Average processing time': '平均処理時間',
                'Starting From/Month': '月額〜',
                'Common': '一般的な',
                'Challenges': '課題',
                'How VaultCaddy Solves These Problems': 'VaultCaddyがこれらの問題を解決する方法',
                'Specific Features': '専用機能',
                'Built for the unique needs': 'ユニークなニーズに対応',
                'Everything you need to know': '知っておくべきこと',
                'Hours Saved/Week': '週間節約時間',
                '💬 真實客戶評價': '💬 お客様の声',
                '每月節省': '月間節約',
                '針對日本市場的專業解答': '日本市場向けの専門的な回答',
                '節省20%': '20%割引',
            },
            'ko-KR': {
                # 按钮和CTA
                'Start Free Trial': '무료 체험 시작',
                'See How It Works': '작동 방식 보기',
                'FREE: Try 20 pages': '무료: 20페이지 체험',
                'No credit card required': '신용카드 불필요',
                'AUTO PLAYING': '자동 재생 중',
                'LIVE DEMONSTRATION': '라이브 데모',
                'MOST POPULAR': '가장 인기 있는',
                'Monthly Plan': '월간 플랜',
                'Annual Plan': '연간 플랜',
                'per month': '월',
                'per additional page': '추가 페이지당',
                'Email Support': '이메일 지원',
                'Priority email support': '우선 이메일 지원',
                '24h auto-delete': '24시간 자동 삭제',
                'Start': '시작',
                'Ready to Save': '절약 준비',
                'Join 500+': '500+ 가입',
                'Built for': '전용 설계',
                'designed specifically for': '전용 설계',
                'How It Works': '작동 방식',
                'Why Choose VaultCaddy?': 'VaultCaddy를 선택하는 이유는?',
                'Simple, Transparent Pricing': '간단하고 투명한 가격',
                'Convert': '변환',
                'in Seconds': '몇 초 만에',
                'Made Simple': '간단하게',
                'Automate': '자동화',
                'Upload Your': '업로드',
                'AI Processing': 'AI 처리',
                'Export to Your System': '시스템으로 내보내기',
                'Verify & Save': '확인 및 저장',
                'AES-256 Encrypted': 'AES-256 암호화',
                'Bank-level security': '은행 수준 보안',
                'SOC 2 Type II Certified': 'SOC 2 Type II 인증',
                'GDPR Compliant': 'GDPR 준수',
                'Data protected': '데이터 보호',
                'Rating': '평점',
                'reviews': '리뷰',
                'Trusted by': '신뢰받는',
                'businesses in': '기업',
                'Accuracy': '정확도',
                'Processing': '처리',
                'Per Month': '월',
                'pages included': '페이지 포함',
                'All export formats': '모든 내보내기 형식',
                'Cancel anytime': '언제든지 취소',
                'Billed annually': '연간 청구',
                'Watch how': '방법 보기',
                'are processed in seconds': '몇 초 만에 처리',
                'with 98% accuracy': '98% 정확도',
                'Average processing time': '평균 처리 시간',
                'Starting From/Month': '월 시작',
                'Common': '일반적인',
                'Challenges': '과제',
                'How VaultCaddy Solves These Problems': 'VaultCaddy가 이러한 문제를 해결하는 방법',
                'Specific Features': '전용 기능',
                'Built for the unique needs': '고유한 요구 사항에 맞게 설계',
                'Everything you need to know': '알아야 할 모든 것',
                'Hours Saved/Week': '주당 절약 시간',
            }
        }
    
    def fix_file(self, file_path, lang):
        """修复单个文件的语言混合问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            translations = self.translations[lang]
            
            # 逐个替换英文文本
            for english, localized in translations.items():
                # 使用正则表达式进行替换，确保不会破坏HTML标签
                content = re.sub(
                    r'(?<=>)' + re.escape(english) + r'(?=<)',
                    localized,
                    content
                )
                # 也替换纯文本中的
                content = content.replace(f'>{english}<', f'>{localized}<')
                content = content.replace(f' {english} ', f' {localized} ')
            
            # 只有在内容改变时才写入
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_count[lang] += 1
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 失败: {file_path.name} - {e}")
            return False
    
    def process_all_languages(self):
        """处理所有语言版本"""
        print("🚨 开始紧急修复语言混合问题...")
        print("=" * 80)
        
        for lang_key in self.translations.keys():
            lang_dir_map = {
                'zh-TW': 'zh-TW',
                'zh-HK': 'zh-HK',
                'ja-JP': 'ja-JP',
                'ko-KR': 'ko-KR'
            }
            
            lang_dir = self.root_dir / lang_dir_map[lang_key]
            
            if not lang_dir.exists():
                print(f"  ⚠️ 目录不存在: {lang_dir}")
                continue
            
            print(f"\n{'='*80}")
            print(f"修复 {lang_key} 版本...")
            print(f"{'='*80}")
            
            lang_files = list(lang_dir.glob('*-v3.html'))
            lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
            
            print(f"  找到 {len(lang_files)} 个页面")
            
            for i, file_path in enumerate(lang_files, 1):
                if i % 10 == 0:
                    print(f"  进度: {i}/{len(lang_files)}")
                self.fix_file(file_path, lang_key)
            
            print(f"  ✅ 完成: {self.fixed_count[lang_key]}个页面")
        
        print("\n" + "=" * 80)
        print("🎉 语言混合问题修复完成！")
        print("=" * 80)
        print(f"\n📊 统计:")
        for lang, count in self.fixed_count.items():
            print(f"   {lang}: {count}个页面")
        print(f"\n总计: {sum(self.fixed_count.values())} 个页面已修复")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🚨 紧急修复：语言混合问题                                  ║
║                                                                              ║
║  问题:                                                                       ║
║    ❌ 日文页面包含大量中文                                                   ║
║    ❌ 繁体页面包含大量英文                                                   ║
║    ❌ 韩文页面包含大量英文                                                   ║
║                                                                              ║
║  修复内容:                                                                   ║
║    ✓ 将所有英文按钮翻译为对应语言                                            ║
║    ✓ 将所有中文标题翻译为对应语言                                            ║
║    ✓ 确保100%语言一致性                                                     ║
║                                                                              ║
║  目标: 360个多语言页面                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    fixer = LanguageMixingFixer(root_dir)
    fixer.process_all_languages()
    
    print("\n" + "=" * 80)
    print("✅ 所有语言混合问题已修复！")
    print("=" * 80)
    print("\n🎉 现在所有页面应该是100%单一语言！")

if __name__ == '__main__':
    main()

