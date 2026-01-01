#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 完整修复：所有英文文本和FAQ功能
"""

import os
import re
from pathlib import Path

def fix_complete(file_path, replacements, lang_code):
    """完整修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 替换所有文本
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        # 2. 确保FAQ JavaScript存在并正确
        if 'faq-question' in content:
            # 检查是否有FAQ JavaScript
            if 'FAQ Toggle Functionality' not in content and 'faq-question' in content:
                # 添加FAQ JavaScript
                faq_script = '''
    <script>
        // FAQ Toggle Functionality
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.faq-question').forEach(question => {
                question.addEventListener('click', () => {
                    const answer = question.nextElementSibling;
                    const icon = question.querySelector('.faq-icon');
                    
                    if (answer && answer.classList.contains('faq-answer')) {
                        if (answer.style.display === 'none' || answer.style.display === '') {
                            answer.style.display = 'block';
                            if (icon) {
                                icon.textContent = '−';
                                icon.style.transform = 'rotate(180deg)';
                            }
                        } else {
                            answer.style.display = 'none';
                            if (icon) {
                                icon.textContent = '+';
                                icon.style.transform = 'rotate(0deg)';
                            }
                        }
                    }
                });
            });
        });
    </script>
'''
                # 在</body>之前插入
                content = content.replace('</body>', faq_script + '\n</body>')
        
        # 只有在内容改变时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 失败: {file_path.name} - {e}")
        return False

def get_replacements(lang):
    """获取对应语言的替换字典"""
    
    base_replacements = {
        # Hero section英文
        'AI-powered PDF轉Excel/QuickBooks converter 準確率達98%.': '',
        'No manual data entry. No templates. Just fast, accurate results.': '',
        
        # 对比表格
        'See how we compare to manual entry and competitors': '',
        'Feature': '',
        'Manual Entry': '',
        'Competitors': '',
        '處理 Speed': '',
        '3 seconds': '',
        '30-60 minutes': '',
        '10-30 seconds': '',
        'Unlimited': '',
        'Manual only': '',
        'Limited': '',
        'Bank-Specific AI': '',
        'Yes': '',
        'No': '',
        'Export Formats': '',
        '4 formats': '',
        '1 format': '',
        '2-3 formats': '',
        'Monthly Cost': '',
        'Low cost': '',
        'Your time': '',
        '$20-50+': '',
        
        # How it works步骤
        'Drag and drop your PDF, JPG, or PNG files. We support all CTBC account types including checking, savings, credit cards, and business accounts. Batch upload available.': '',
        'Our AI engine, specifically trained on CTBC Bank formats, automatically extracts all transactions, dates, amounts, and descriptions 準確率達98% in just 3 seconds.': '',
        'Choose your preferred format: Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-': '',
        'formatted and ready to import into your accounting software.': '',
        
        # FAQ问题
        'Everything you need to know about CTBC Bank statement conversion': '',
        'How accurate is VaultCaddy for CTBC Bank statements?': '',
        'What CTBC Bank account types are supported?': '',
        'How do I export CTBC Bank statements to QuickBooks?': '',
        'Is my CTBC Bank data secure with VaultCaddy?': '',
        'Can I batch process multiple CTBC Bank statements?': '',
        
        # 其他关键功能描述
        'Our AI is specifically trained on CTBC Bank formats. Handles checking, savings, credit cards, and business accounts with industry-leading precision.': '',
        '轉換 your CTBC Bank PDF轉 Excel/QuickBooks in just 3 seconds. No waiting, no queues, no manual work. Batch upload supported.': '',
        'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.': '',
        'AES-256 encryption, SOC 2 Type II certified, GDPR compliant. Files auto-delete after 24 hours. Zero data breaches in 3+ years.': '',
        'Upload 10, 50, or 100+ statements at once. Process all your CTBC Bank accounts in minutes instead of hours.': '',
        'Professional accounting automation team. 電子郵件支援 included in all plans. 優先支援 for annual subscribers.': '',
        '轉換 CTBC Bank statements in 4 simple steps': '',
        'Built specifically for CTBC Bank statements': '',
    }
    
    if lang == 'zh-TW' or lang == 'zh-HK':
        return {
            **base_replacements,
            'AI-powered PDF轉Excel/QuickBooks converter 準確率達98%.': 'AI驅動的PDF轉Excel/QuickBooks轉換器，準確率達98%。',
            'No manual data entry. No templates. Just fast, accurate results.': '無需手動輸入數據。無需模板。只需快速、準確的結果。',
            'See how we compare to manual entry and competitors': '查看我們與手動輸入和競爭對手的比較',
            'Feature': '功能',
            'Manual Entry': '手動輸入',
            'Competitors': '競爭對手',
            '處理 Speed': '處理速度',
            '3 seconds': '3秒',
            '30-60 minutes': '30-60分鐘',
            '10-30 seconds': '10-30秒',
            'Unlimited': '無限',
            'Manual only': '僅手動',
            'Limited': '有限',
            'Bank-Specific AI': '銀行專用AI',
            'Yes': '是',
            'No': '否',
            'Export Formats': '匯出格式',
            '4 formats': '4種格式',
            '1 format': '1種格式',
            '2-3 formats': '2-3種格式',
            'Monthly Cost': '月費',
            'Low cost': '低成本',
            'Your time': '您的時間',
            '$20-50+': '$20-50+',
            'Drag and drop your PDF, JPG, or PNG files. We support all CTBC account types including checking, savings, credit cards, and business accounts. Batch upload available.': '拖放您的PDF、JPG或PNG文件。我們支援所有CTBC帳戶類型，包括支票、儲蓄、信用卡和商業帳戶。支援批量上傳。',
            'Our AI engine, specifically trained on CTBC Bank formats, automatically extracts all transactions, dates, amounts, and descriptions 準確率達98% in just 3 seconds.': '我們的AI引擎專門針對CTBC銀行格式進行訓練，自動提取所有交易、日期、金額和描述，準確率達98%，只需3秒。',
            'Choose your preferred format: Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-': '選擇您喜歡的格式：Excel (XLSX)、CSV、QuickBooks (QBO) 或 Xero。我們的匯出是預先',
            'formatted and ready to import into your accounting software.': '格式化的，可直接導入您的會計軟件。',
            'Everything you need to know about CTBC Bank statement conversion': '關於CTBC銀行對帳單轉換您需要知道的一切',
            'How accurate is VaultCaddy for CTBC Bank statements?': 'VaultCaddy對CTBC銀行對帳單的準確率如何？',
            'What CTBC Bank account types are supported?': '支援哪些CTBC銀行帳戶類型？',
            'How do I export CTBC Bank statements to QuickBooks?': '如何將CTBC銀行對帳單匯出到QuickBooks？',
            'Is my CTBC Bank data secure with VaultCaddy?': '我的CTBC銀行數據在VaultCaddy上安全嗎？',
            'Can I batch process multiple CTBC Bank statements?': '我可以批量處理多個CTBC銀行對帳單嗎？',
            'Our AI is specifically trained on CTBC Bank formats. Handles checking, savings, credit cards, and business accounts with industry-leading precision.': '我們的AI專門針對CTBC銀行格式進行訓練。以行業領先的精度處理支票、儲蓄、信用卡和商業帳戶。',
            '轉換 your CTBC Bank PDF轉 Excel/QuickBooks in just 3 seconds. No waiting, no queues, no manual work. Batch upload supported.': '只需3秒即可轉換您的CTBC銀行PDF到Excel/QuickBooks。無需等待、無需排隊、無需手動工作。支援批量上傳。',
            'Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.': '匯出到Excel、CSV、QuickBooks (QBO) 或 Xero。預先格式化，可直接導入您的會計軟件。',
            'AES-256 encryption, SOC 2 Type II certified, GDPR compliant. Files auto-delete after 24 hours. Zero data breaches in 3+ years.': 'AES-256加密，SOC 2 Type II認證，符合GDPR。文件24小時後自動刪除。3年以上零數據洩露。',
            'Upload 10, 50, or 100+ statements at once. Process all your CTBC Bank accounts in minutes instead of hours.': '一次上傳10、50或100+份對帳單。在幾分鐘內處理所有CTBC銀行帳戶，而不是幾小時。',
            'Professional accounting automation team. 電子郵件支援 included in all plans. 優先支援 for annual subscribers.': '專業會計自動化團隊。所有計劃均包含電郵支援。年度訂閱者享有優先支援。',
            '轉換 CTBC Bank statements in 4 simple steps': '4個簡單步驟轉換CTBC銀行對帳單',
            'Built specifically for CTBC Bank statements': '專為CTBC銀行對帳單設計',
        }
    
    elif lang == 'ja-JP':
        return {
            **base_replacements,
            'AI-powered PDF轉Excel/QuickBooks converter 準確率達98%.': 'AI搭載のPDFからExcel/QuickBooksへのコンバーター、精度98%。',
            'No manual data entry. No templates. Just fast, accurate results.': '手動データ入力不要。テンプレート不要。高速で正確な結果のみ。',
            'See how we compare to manual entry and competitors': '手動入力や競合他社との比較を見る',
            'Feature': '機能',
            'Manual Entry': '手動入力',
            'Competitors': '競合他社',
            '處理 Speed': '処理速度',
            '3 seconds': '3秒',
            '30-60 minutes': '30-60分',
            '10-30 seconds': '10-30秒',
            'Unlimited': '無制限',
            'Manual only': '手動のみ',
            'Limited': '制限あり',
            'Bank-Specific AI': '銀行専用AI',
            'Yes': 'はい',
            'No': 'いいえ',
            'Export Formats': 'エクスポート形式',
            '4 formats': '4形式',
            '1 format': '1形式',
            '2-3 formats': '2-3形式',
            'Monthly Cost': '月額費用',
            'Low cost': '低コスト',
            'Your time': 'あなたの時間',
            '$20-50+': '$20-50+',
            'Everything you need to know about CTBC Bank statement conversion': 'CTBC銀行明細書変換について知っておくべきすべて',
            'How accurate is VaultCaddy for CTBC Bank statements?': 'VaultCaddyのCTBC銀行明細書の精度は？',
            'What CTBC Bank account types are supported?': 'どのCTBC銀行口座タイプがサポートされていますか？',
            'How do I export CTBC Bank statements to QuickBooks?': 'CTBC銀行明細書をQuickBooksにエクスポートする方法は？',
            'Is my CTBC Bank data secure with VaultCaddy?': 'VaultCaddyでCTBC銀行データは安全ですか？',
            'Can I batch process multiple CTBC Bank statements?': '複数のCTBC銀行明細書を一括処理できますか？',
        }
    
    elif lang == 'ko-KR':
        return {
            **base_replacements,
            'AI-powered PDF轉Excel/QuickBooks converter 準確率達98%.': 'AI 기반 PDF에서 Excel/QuickBooks로 변환, 정확도 98%.',
            'No manual data entry. No templates. Just fast, accurate results.': '수동 데이터 입력 불필요. 템플릿 불필요. 빠르고 정확한 결과만.',
            'See how we compare to manual entry and competitors': '수동 입력 및 경쟁사와의 비교',
            'Feature': '기능',
            'Manual Entry': '수동 입력',
            'Competitors': '경쟁사',
            '處理 Speed': '처리 속도',
            '3 seconds': '3초',
            '30-60 minutes': '30-60분',
            '10-30 seconds': '10-30초',
            'Unlimited': '무제한',
            'Manual only': '수동만',
            'Limited': '제한됨',
            'Bank-Specific AI': '은행 전용 AI',
            'Yes': '예',
            'No': '아니오',
            'Export Formats': '내보내기 형식',
            '4 formats': '4가지 형식',
            '1 format': '1가지 형식',
            '2-3 formats': '2-3가지 형식',
            'Monthly Cost': '월 비용',
            'Low cost': '저비용',
            'Your time': '당신의 시간',
            '$20-50+': '$20-50+',
            'Everything you need to know about CTBC Bank statement conversion': 'CTBC 은행 명세서 변환에 대해 알아야 할 모든 것',
            'How accurate is VaultCaddy for CTBC Bank statements?': 'VaultCaddy의 CTBC 은행 명세서 정확도는?',
            'What CTBC Bank account types are supported?': '어떤 CTBC 은행 계좌 유형이 지원됩니까?',
            'How do I export CTBC Bank statements to QuickBooks?': 'CTBC 은행 명세서를 QuickBooks로 내보내는 방법은?',
            'Is my CTBC Bank data secure with VaultCaddy?': 'VaultCaddy에서 CTBC 은행 데이터가 안전합니까?',
            'Can I batch process multiple CTBC Bank statements?': '여러 CTBC 은행 명세서를 일괄 처리할 수 있습니까?',
        }
    
    return {}

def main():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    print("🔥 开始完整修复所有文本...")
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
        
        replacements = get_replacements(lang_code)
        fixed_count = 0
        
        for i, file_path in enumerate(lang_files, 1):
            if fix_complete(file_path, replacements, lang_code):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
    
    print("\n" + "=" * 80)
    print("🎉 完整修复完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

