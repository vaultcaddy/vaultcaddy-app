#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的首页智能同步系统
作用：彻底清除其他语言版本中的中文内容
"""

import os
import re
import json

# 完整翻译字典
FULL_TRANSLATIONS = {
    # === SEO和标题 ===
    '動態 SEO 優化標題 - 針對香港會計師和中小企業': {
        'en': 'Dynamic SEO Optimized Title - For US Accountants and SMEs',
        'jp': 'ダイナミックSEO最適化タイトル - 日本の会計士および中小企業向け',
        'kr': '동적 SEO 최적화 제목 - 한국 회계사 및 중소기업 대상'
    },
    '增強型描述 - 強調目標用戶痛點': {
        'en': 'Enhanced Description - Highlight Target User Pain Points',
        'jp': '強化された説明 - ターゲットユーザーの課題を強調',
        'kr': '강화된 설명 - 대상 사용자의 주요 문제점 강조'
    },
    '擴展關鍵詞策略 - 針對香港市場和會計行業': {
        'en': 'Extended Keyword Strategy - For US Market and Accounting Industry',
        'jp': 'キーワード戦略の拡張 - 日本市場および会計業界向け',
        'kr': '확장 키워드 전략 - 한국 시장 및 회계 업계 대상'
    },
    '搜索引擎優化': {
        'en': 'Search Engine Optimization',
        'jp': '検索エンジン最適化',
        'kr': '검색 엔진 최적화'
    },
    
    # === 主要标题和描述 ===
    '香港銀行對帳單處理專家': {
        'en': 'US Bank Statement Processing Expert',
        'jp': '日本の銀行明細処理の専門家',
        'kr': '한국 은행 명세서 처리 전문가'
    },
    '支援匯豐恆生中銀': {
        'en': 'Support Major US Banks',
        'jp': '日本の主要銀行対応',
        'kr': '한국 주요 은행 지원'
    },
    '專為會計師及小型公司設計的 AI 文檔處理平台': {
        'en': 'AI Document Processing Platform Designed for Accountants and Small Businesses',
        'jp': '会計士および中小企業向けに設計されたAI文書処理プラットフォーム',
        'kr': '회계사 및 중소기업을 위해 설계된 AI 문서 처리 플랫폼'
    },
    '自動轉換 Excel/CSV/QuickBooks/Xero': {
        'en': 'Auto Convert to Excel/CSV/QuickBooks/Xero',
        'jp': 'Excel/CSV/QuickBooks/Xeroへの自動変換',
        'kr': 'Excel/CSV/QuickBooks/Xero로 자동 변환'
    },
    '98% 準確率': {
        'en': '98% Accuracy',
        'jp': '98%の精度',
        'kr': '98% 정확도'
    },
    '節省 90% 時間': {
        'en': 'Save 90% Time',
        'jp': '90%の時間を節約',
        'kr': '90% 시간 절약'
    },
    
    # === 按钮和行动号召 ===
    '立即免費試用': {
        'en': 'Try Free Now',
        'jp': '今すぐ無料で試す',
        'kr': '지금 무료로 체험'
    },
    '開始使用': {
        'en': 'Get Started',
        'jp': '始める',
        'kr': '시작하기'
    },
    '無需信用卡': {
        'en': 'No Credit Card Required',
        'jp': 'クレジットカード不要',
        'kr': '신용카드 불필요'
    },
    '免費試用 20 頁': {
        'en': 'Try 20 Pages Free',
        'jp': '20ページ無料トライアル',
        'kr': '20페이지 무료 체험'
    },
    
    # === 统计数据 ===
    '平均處理時間': {
        'en': 'Average Processing Time',
        'jp': '平均処理時間',
        'kr': '평균 처리 시간'
    },
    '數據準確率': {
        'en': 'Data Accuracy',
        'jp': 'データ精度',
        'kr': '데이터 정확도'
    },
    '企業客戶': {
        'en': 'Business Clients',
        'jp': '法人顧客',
        'kr': '기업 고객'
    },
    '超過': {
        'en': 'Over',
        'jp': '以上',
        'kr': '이상'
    },
    '企業信賴': {
        'en': 'businesses trust',
        'jp': '企業が信頼',
        'kr': '기업이 신뢰'
    },
    
    # === 功能描述 ===
    '強大的功能': {
        'en': 'Powerful Features',
        'jp': '強力な機能',
        'kr': '강력한 기능'
    },
    '一站式 AI 文檔處理平台': {
        'en': 'All-in-One AI Document Processing Platform',
        'jp': 'オールインワンAI文書処理プラットフォーム',
        'kr': '올인원 AI 문서 처리 플랫폼'
    },
    '支援發票、收據、銀行對帳單等多種財務文檔': {
        'en': 'Support invoices, receipts, bank statements and various financial documents',
        'jp': '請求書、領収書、銀行取引明細書などの様々な財務文書に対応',
        'kr': '송장, 영수증, 은행 명세서 및 다양한 재무 문서 지원'
    },
    
    # === 智能发票处理 ===
    '智能發票與收據處理': {
        'en': 'Smart Invoice & Receipt Processing',
        'jp': 'スマート請求書＆領収書処理',
        'kr': '스마트 송장 및 영수증 처리'
    },
    '自動提取發票數據，秒速完成分類歸檔': {
        'en': 'Auto Extract Invoice Data, Complete Classification in Seconds',
        'jp': '請求書データを自動抽出、分類を秒速で完了',
        'kr': '송장 데이터 자동 추출, 초 단위 분류 완료'
    },
    'OCR 光學識別技術': {
        'en': 'OCR Optical Recognition Technology',
        'jp': 'OCR光学認識技術',
        'kr': 'OCR 광학 인식 기술'
    },
    '精準擷取商家、日期、金額、稅額等關鍵資訊': {
        'en': 'Precisely extract key information such as merchant, date, amount, tax',
        'jp': '商店、日付、金額、税額などの主要情報を正確に抽出',
        'kr': '상점, 날짜, 금액, 세금 등 주요 정보를 정확하게 추출'
    },
    '智能分類': {
        'en': 'Smart Categorization',
        'jp': 'スマート分類',
        'kr': '지능형 분류'
    },
    '自動辨識發票類型並歸類至對應會計科目': {
        'en': 'Auto identify invoice types and categorize to corresponding accounting accounts',
        'jp': '請求書タイプを自動識別し、対応する会計科目に分類',
        'kr': '송장 유형을 자동으로 식별하고 해당 회계 계정으로 분류'
    },
    '即時同步會計軟體': {
        'en': 'Real-time Sync to Accounting Software',
        'jp': '会計ソフトへのリアルタイム同期',
        'kr': '회계 소프트웨어에 실시간 동기화'
    },
    '一鍵匯出至 QuickBooks、Xero 等主流平台': {
        'en': 'One-click export to QuickBooks, Xero and other major platforms',
        'jp': 'QuickBooks、Xeroなどの主要プラットフォームにワンクリックでエクスポート',
        'kr': 'QuickBooks, Xero 등 주요 플랫폼으로 원클릭 내보내기'
    },
    
    # === 银行对账单处理 ===
    '銀行對帳單智能分析': {
        'en': 'Smart Bank Statement Analysis',
        'jp': 'スマート銀行明細分析',
        'kr': '은행 명세서 지능형 분석'
    },
    '自動識別收支類別，即時生成財務報表': {
        'en': 'Auto identify income/expense categories, generate financial reports instantly',
        'jp': '収支カテゴリを自動識別、財務レポートを即座に生成',
        'kr': '수입 지출 범주 자동 식별, 즉시 재무 보고서 생성'
    },
    '智能交易分類': {
        'en': 'Smart Transaction Categorization',
        'jp': 'スマート取引分類',
        'kr': '스마트 거래 분류'
    },
    '自動識別收入、支出、轉帳並進行分類': {
        'en': 'Auto identify and categorize income, expenses, transfers',
        'jp': '収入、支出、振替を自動識別して分類',
        'kr': '수입, 지출, 이체를 자동으로 식별하고 분류'
    },
    '精準數據提取': {
        'en': 'Precise Data Extraction',
        'jp': '精密なデータ抽出',
        'kr': '정밀 데이터 추출'
    },
    '準確擷取日期、對方帳戶、金額等關鍵數據': {
        'en': 'Accurately extract key data such as date, payee account, amount',
        'jp': '日付、相手口座、金額などの主要データを正確に抽出',
        'kr': '날짜, 상대방 계정, 금액 등 주요 데이터를 정확하게 추출'
    },
    '多格式匯出': {
        'en': 'Multiple Format Export',
        'jp': '複数形式でエクスポート',
        'kr': '다중 형식 내보내기'
    },
    '支援匯出為 Excel、CSV、QuickBooks、Xero 等格式': {
        'en': 'Support export to Excel, CSV, QuickBooks, Xero and more',
        'jp': 'Excel、CSV、QuickBooks、Xeroなどの形式でエクスポート対応',
        'kr': 'Excel, CSV, QuickBooks, Xero 등으로 내보내기 지원'
    },
    
    # === 为什么选择 ===
    '為什麼選擇 VaultCaddy': {
        'en': 'Why Choose VaultCaddy',
        'jp': 'VaultCaddyを選ぶ理由',
        'kr': 'VaultCaddy를 선택하는 이유'
    },
    '專為香港會計師打造': {
        'en': 'Built for US Accountants',
        'jp': '日本の会計士のために構築',
        'kr': '한국 회계사를 위해 구축'
    },
    '提升效率，降低成本，讓您專注於更有價值的工作': {
        'en': 'Boost efficiency, reduce costs, let you focus on more valuable work',
        'jp': '効率を向上させ、コストを削減し、より価値のある仕事に集中できます',
        'kr': '효율성을 높이고 비용을 절감하며 더 가치 있는 작업에 집중하세요'
    },
    
    # === 三大优势 ===
    '極速處理': {
        'en': 'Ultra-Fast Processing',
        'jp': '超高速処理',
        'kr': '초고속 처리'
    },
    '平均 10 秒完成一份文檔': {
        'en': 'Average 10 seconds to complete one document',
        'jp': '平均10秒で1つの文書を完了',
        'kr': '평균 10초로 문서 1개 완료'
    },
    '批量處理更快更省時': {
        'en': 'Batch processing is faster and saves more time',
        'jp': 'バッチ処理でさらに速く時間を節約',
        'kr': '배치 처리로 더 빠르고 시간 절약'
    },
    '節省 90% 人工輸入時間': {
        'en': 'Save 90% manual input time',
        'jp': '90%の手動入力時間を節約',
        'kr': '90% 수동 입력 시간 절약'
    },
    
    '極致準確': {
        'en': 'Maximum Accuracy',
        'jp': '最高精度',
        'kr': '최고 정확도'
    },
    'AI 辨識準確率達 98%': {
        'en': 'AI recognition accuracy reaches 98%',
        'jp': 'AI認識精度は98%に達する',
        'kr': 'AI 인식 정확도 98% 달성'
    },
    '自動驗證和校正錯誤': {
        'en': 'Auto verify and correct errors',
        'jp': '自動検証とエラー修正',
        'kr': '자동 검증 및 오류 수정'
    },
    '大幅降低人為失誤風險': {
        'en': 'Significantly reduce human error risk',
        'jp': 'ヒューマンエラーのリスクを大幅に削減',
        'kr': '인적 오류 위험 대폭 감소'
    },
    
    '性價比最高': {
        'en': 'Best Value',
        'jp': '最高のコストパフォーマンス',
        'kr': '최고의 가성비'
    },
    '無隱藏收費': {
        'en': 'No hidden fees',
        'jp': '隠れた費用なし',
        'kr': '숨겨진 비용 없음'
    },
    '用多少付多少最靈活': {
        'en': 'Pay as you go, most flexible',
        'jp': '使った分だけ支払い、最も柔軟',
        'kr': '사용한 만큼만 지불, 가장 유연함'
    },
    
    # === 定价 ===
    '合理且實惠的價格': {
        'en': 'Fair and Affordable Pricing',
        'jp': '合理で手頃な価格',
        'kr': '합리적이고 저렴한 가격'
    },
    '輕鬆處理銀行對帳單': {
        'en': 'Easy Bank Statement Processing',
        'jp': '銀行明細を簡単に処理',
        'kr': '간편한 은행 명세서 처리'
    },
    '與數千家企業一起，節省財務數據錄入的時間': {
        'en': 'Join thousands of businesses saving time on financial data entry',
        'jp': '数千の企業とともに、財務データ入力の時間を節約',
        'kr': '수천 개의 기업과 함께 재무 데이터 입력 시간 절약'
    },
    '無隱藏費用，隨時取消': {
        'en': 'No hidden fees, cancel anytime',
        'jp': '隠れた費用なし、いつでもキャンセル可能',
        'kr': '숨겨진 비용 없음, 언제든 취소 가능'
    },
    
    '月付': {'en': 'Monthly', 'jp': '月払い', 'kr': '월간'},
    '年付': {'en': 'Yearly', 'jp': '年払い', 'kr': '연간'},
    '每月': {'en': '/month', 'jp': '/月', 'kr': '/월'},
    '每年': {'en': '/year', 'jp': '/年', 'kr': '/년'},
    
    '頁面包含': {
        'en': "What's Included",
        'jp': '含まれる内容',
        'kr': '포함 사항'
    },
    '每月 100 Credits': {
        'en': '100 Credits per month',
        'jp': '月間100クレジット',
        'kr': '월 100 크레딧'
    },
    '每年 1,200 Credits': {
        'en': '1,200 Credits per year',
        'jp': '年間1,200クレジット',
        'kr': '연간 1,200 크레딧'
    },
    '超出後每頁': {
        'en': 'Then',
        'jp': '超過後1ページ',
        'kr': '초과 시 페이지당'
    },
    '批次處理無限制文件': {
        'en': 'Unlimited Batch Processing',
        'jp': 'バッチ処理無制限',
        'kr': '무제한 배치 처리'
    },
    '一鍵轉換所有文件': {
        'en': 'One-Click Convert All',
        'jp': 'ワンクリック一括変換',
        'kr': '원클릭 일괄 변환'
    },
    'Excel/CSV 匯出': {
        'en': 'Excel/CSV Export',
        'jp': 'Excel/CSVエクスポート',
        'kr': 'Excel/CSV 내보내기'
    },
    'QuickBooks 整合': {
        'en': 'QuickBooks Integration',
        'jp': 'QuickBooks統合',
        'kr': 'QuickBooks 통합'
    },
    '複合式 AI 處理': {
        'en': 'Hybrid AI Processing',
        'jp': 'ハイブリッドAI処理',
        'kr': '하이브리드 AI 처리'
    },
    '8 種語言支援': {
        'en': '8 Languages Support',
        'jp': '8言語サポート',
        'kr': '8개 언어 지원'
    },
    '電子郵件支援': {
        'en': 'Email Support',
        'jp': 'メールサポート',
        'kr': '이메일 지원'
    },
    '安全文件上傳': {
        'en': 'Secure File Upload',
        'jp': '安全なファイルアップロード',
        'kr': '안전한 파일 업로드'
    },
    '365 天數據保留': {
        'en': '365-day Data Retention',
        'jp': '365日データ保持',
        'kr': '365일 데이터 보관'
    },
    '30 天圖片保留': {
        'en': '30-day Image Backup',
        'jp': '30日画像保持',
        'kr': '30일 이미지 백업'
    },
    '節省 20%': {
        'en': 'Save 20%',
        'jp': '20%節約',
        'kr': '20% 절약'
    },
    
    # === 用户评价 ===
    'VaultCaddy 使用者評價': {
        'en': 'VaultCaddy User Reviews',
        'jp': 'VaultCaddyユーザーレビュー',
        'kr': 'VaultCaddy 사용자 리뷰'
    },
    
    # === 学习中心 ===
    '學習中心': {
        'en': 'Learning Center',
        'jp': '学習センター',
        'kr': '학습 센터'
    },
    '了解如何最大化利用 VaultCaddy 處理您的財務文檔': {
        'en': 'Learn how to maximize VaultCaddy for your financial documents',
        'jp': 'VaultCaddyを最大限に活用して財務文書を処理する方法を学ぶ',
        'kr': 'VaultCaddy를 최대한 활용하여 재무 문서를 처리하는 방법 알아보기'
    },
    '閱讀文章': {
        'en': 'Read Article',
        'jp': '記事を読む',
        'kr': '기사 읽기'
    },
    
    # === 页脚 ===
    '專為會計師及小型公司設計的 AI 文檔處理平台，讓財務文檔管理變得簡單高效': {
        'en': 'AI document processing platform designed for accountants and small businesses, making financial document management simple and efficient',
        'jp': '会計士および中小企業向けに設計されたAI文書処理プラットフォーム、財務文書管理をシンプルかつ効率的に',
        'kr': '회계사 및 중소기업을 위해 설계된 AI 문서 처리 플랫폼, 재무 문서 관리를 간단하고 효율적으로'
    },
    '快速連結': {
        'en': 'Quick Links',
        'jp': 'クイックリンク',
        'kr': '빠른 링크'
    },
    '功能介紹': {
        'en': 'Features',
        'jp': '機能紹介',
        'kr': '기능 소개'
    },
    '價格方案': {
        'en': 'Pricing',
        'jp': '料金プラン',
        'kr': '가격 계획'
    },
    '法律政策': {
        'en': 'Legal',
        'jp': '法的情報',
        'kr': '법률 정책'
    },
    '隱私政策': {
        'en': 'Privacy Policy',
        'jp': 'プライバシーポリシー',
        'kr': '개인정보 처리방침'
    },
    '服務條款': {
        'en': 'Terms of Service',
        'jp': '利用規約',
        'kr': '서비스 약관'
    },
    '版權所有': {
        'en': 'All rights reserved',
        'jp': '全著作権所有',
        'kr': '저작권 소유'
    },
    '聯繫我們': {
        'en': 'Contact Us',
        'jp': 'お問い合わせ',
        'kr': '문의하기'
    },
    
    # === 限时优惠横幅 ===
    '限時優惠：本月註冊立享 8 折！': {
        'en': 'Limited Offer: Register this month and get 20% off!',
        'jp': '期間限定：今月の登録で20%オフ！',
        'kr': '한정 특가: 이번 달 가입 시 20% 할인!'
    },
    '優惠碼：': {
        'en': 'Code:',
        'jp': 'コード:',
        'kr': '코드:'
    },
    '已有': {
        'en': 'Already',
        'jp': 'すでに',
        'kr': '이미'
    },
    '位香港會計師加入': {
        'en': 'US accountants joined',
        'jp': '名の日本の会計士が参加',
        'kr': '명 이상의 한국 회계사가 가입'
    },
}

def main():
    print('開始同步首頁...\n')
    
    # 讀取中文版
    with open('index.html', 'r', encoding='utf-8') as f:
        zh_content = f.read()
    
    for lang in ['en', 'jp', 'kr']:
        print(f'處理 {lang} 版本...')
        content = zh_content
        
        # 翻譯所有文本
        for zh_text, translations in FULL_TRANSLATIONS.items():
            if lang in translations:
                content = content.replace(zh_text, translations[lang])
        
        # 寫入文件
        os.makedirs(lang, exist_ok=True)
        with open(f'{lang}/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✅ {lang}/index.html 已更新\n')
    
    print('🎉 同步完成！')

if __name__ == '__main__':
    main()

