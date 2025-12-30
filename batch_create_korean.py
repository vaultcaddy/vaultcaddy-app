#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建韩文版本的v3银行页面
Phase 3: 韩文（ko-KR）
"""

import os
import re

# 核心翻译字典（英文 -> 韩文）
TRANSLATIONS_KO_KR = {
    # SEO和Hero
    "Statement Converter": "명세서 변환기",
    "PDF to Excel/QuickBooks": "PDF를 Excel/QuickBooks로",
    "98% Accuracy": "98% 정확도",
    "Trusted by 500+ businesses": "500개 이상의 기업이 신뢰",
    "Convert": "변환",
    "Statements in Seconds": "명세서를 몇 초 안에",
    "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy": "98% 정확도의 AI 기반 PDF를 Excel/QuickBooks로 변환기",
    "No manual data entry. No templates. Just fast, accurate results.": "수동 데이터 입력 불필요. 템플릿 불필요. 빠르고 정확한 결과만.",
    
    # 統計數據
    "Accuracy": "정확도",
    "Processing": "처리 속도",
    "Per Month": "월간",
    
    # CTA按鈕
    "Start Free Trial": "무료 체험 시작",
    "See How It Works": "작동 방식 보기",
    
    # Features Section
    "Why Choose VaultCaddy?": "VaultCaddy를 선택하는 이유",
    "Built specifically for": "전용으로 구축",
    "statements": "명세서",
    
    "98% AI Accuracy": "98% AI 정확도",
    "Our AI is specifically trained on": "당사의 AI는 전문적으로 훈련되었습니다",
    "formats. Handles checking, savings, credit cards, and business accounts with industry-leading precision.": "형식. 당좌 예금, 저축, 신용 카드 및 비즈니스 계정을 업계 최고의 정밀도로 처리합니다.",
    
    "3-Second Processing": "3초 처리",
    "Convert your": "귀하의",
    "PDF to Excel/QuickBooks in just 3 seconds. No waiting, no queues, no manual work. Batch upload supported.": "PDF를 단 3초 만에 Excel/QuickBooks로 변환. 대기 없음, 대기열 없음, 수동 작업 없음. 일괄 업로드 지원.",
    
    "Multiple Export Formats": "다중 내보내기 형식",
    "Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.": "Excel, CSV, QuickBooks(QBO) 또는 Xero로 내보내기. 사전 포맷되어 회계 소프트웨어로 바로 가져올 수 있습니다.",
    
    "Bank-Level Security": "은행 수준 보안",
    "AES-256 encryption, SOC 2 Type II certified, GDPR compliant. Files auto-delete after 24 hours. Zero data breaches in 3+ years.": "AES-256 암호화, SOC 2 Type II 인증, GDPR 준수. 파일은 24시간 후 자동 삭제. 3년 이상 데이터 침해 제로.",
    
    "Batch Processing": "일괄 처리",
    "Upload 10, 50, or 100+ statements at once. Process all your": "한 번에 10, 50 또는 100개 이상의 명세서 업로드. 모든",
    "accounts in minutes instead of hours.": "계정을 몇 시간이 아닌 몇 분 안에 처리.",
    
    "Expert Support": "전문가 지원",
    "Professional accounting automation team. Email support included in all plans. Priority support for annual subscribers.": "전문 회계 자동화 팀. 모든 플랜에 이메일 지원 포함. 연간 구독자에게는 우선 지원.",
    
    # How It Works
    "How It Works": "작동 방식",
    "statements in 4 simple steps": "명세서를 4가지 간단한 단계로",
    
    "Upload Your": "업로드",
    "Statement": "명세서",
    "Drag and drop your PDF, JPG, or PNG files. We support all": "PDF, JPG 또는 PNG 파일을 드래그 앤 드롭. 모든",
    "account types including checking, savings, credit cards, and business accounts. Batch upload available.": "계정 유형 지원(당좌 예금, 저축, 신용 카드, 비즈니스 계정). 일괄 업로드 가능.",
    
    "AI Processing": "AI 처리",
    "Our AI engine, specifically trained on": "당사의 AI 엔진은 전문적으로 훈련되었습니다",
    "formats, automatically extracts all transactions, dates, amounts, and descriptions with 98% accuracy in just 3 seconds.": "형식으로, 단 3초 만에 98% 정확도로 모든 거래, 날짜, 금액 및 설명을 자동 추출합니다.",
    
    "Export to Your System": "시스템으로 내보내기",
    "Choose your preferred format: Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.": "선호하는 형식 선택: Excel(XLSX), CSV, QuickBooks(QBO) 또는 Xero. 내보내기는 사전 포맷되어 수동 조정 없이 바로 가져올 수 있습니다.",
    
    "Verify & Save": "확인 및 저장",
    "Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files auto-delete after 24 hours.": "대시보드에서 추출된 데이터 검토. 필요한 조정을 하고 다운로드하거나 회계 소프트웨어에 직접 동기화. 모든 파일은 24시간 후 자동 삭제됩니다.",
    
    # Comparison Table
    "See how we compare to manual entry and competitors": "수동 입력 및 경쟁사와의 비교를 확인하세요",
    "Feature": "기능",
    "Manual Entry": "수동 입력",
    "Competitors": "경쟁사",
    "Processing Speed": "처리 속도",
    "seconds": "초",
    "minutes": "분",
    "Accuracy Rate": "정확도",
    "Unlimited": "무제한",
    "Manual only": "수동만",
    "Limited": "제한적",
    "Bank-Specific AI": "은행 전용 AI",
    "Yes": "예",
    "No": "아니오",
    "formats": "형식",
    "format": "형식",
    "Low cost": "저렴한 비용",
    "Your time": "귀하의 시간",
    "Monthly Cost": "월 비용",
    
    # Testimonials
    "Trusted by 2,500+ Users Worldwide": "전 세계 2,500명 이상의 사용자가 신뢰",
    "See what our customers say about VaultCaddy": "VaultCaddy에 대한 고객의 의견을 확인하세요",
    
    "VaultCaddy saves me 10+ hours every month. The accuracy is incredible and it handles all my bank statements perfectly.": "VaultCaddy는 매달 10시간 이상 절약해줍니다. 정확도가 놀랍고 모든 은행 명세서를 완벽하게 처리합니다.",
    "Small Business Owner, USA": "중소기업 소유주, 미국",
    
    "Best investment for my accounting practice. Processes 50+ bank statements in minutes instead of hours.": "회계 사무소를 위한 최고의 투자. 50개 이상의 은행 명세서를 몇 시간이 아닌 몇 분 만에 처리합니다.",
    "CPA, New York": "공인회계사, 뉴욕",
    
    "Incredibly accurate. No more manual data entry errors. My clients love the fast turnaround time.": "놀라울 정도로 정확합니다. 더 이상 수동 데이터 입력 오류가 없습니다. 고객들은 빠른 처리 시간을 좋아합니다.",
    "Bookkeeper, California": "경리 담당자, 캘리포니아",
    
    # Use Cases
    "Perfect For Every Business": "모든 비즈니스에 완벽",
    "See how different professionals use VaultCaddy": "다양한 전문가들이 VaultCaddy를 어떻게 사용하는지 확인하세요",
    
    "Accountants & CPAs": "회계사 및 공인회계사",
    "Batch process 50+ client statements in minutes. Free up time for advisory services.": "몇 분 안에 50개 이상의 고객 명세서 일괄 처리. 자문 서비스에 시간을 할애하세요.",
    
    "Small Business Owners": "중소기업 소유주",
    "Reconcile accounts monthly in seconds. Focus on growing your business, not data entry.": "매월 몇 초 안에 계정 조정. 데이터 입력이 아닌 비즈니스 성장에 집중.",
    
    "Freelancers": "프리랜서",
    "Organize expenses and receipts for tax time. Export directly to your accounting software.": "세무 시기를 위한 경비 및 영수증 정리. 회계 소프트웨어로 직접 내보내기.",
    
    "Retail & E-commerce": "소매 및 전자상거래",
    "Manage multiple payment accounts and platforms. Keep perfect records for inventory management.": "여러 결제 계정 및 플랫폼 관리. 재고 관리를 위한 완벽한 기록 유지.",
    
    # Pricing
    "Simple, Transparent Pricing": "간단하고 투명한 가격",
    "Save 20% with annual billing": "연간 청구로 20% 절약",
    
    "Monthly Plan": "월간 플랜",
    "Annual Plan": "연간 플랜",
    "month": "월",
    "Billed": "청구",
    "annually": "연간",
    "save 20%": "20% 절약",
    "pages included": "100페이지 포함",
    "per additional page": "추가 페이지당",
    "All export formats": "모든 내보내기 형식",
    "Email support": "이메일 지원",
    "auto-delete": "자동 삭제",
    "Priority email support": "우선 이메일 지원",
    "Get Started": "시작하기",
    
    # FAQ
    "Frequently Asked Questions": "자주 묻는 질문",
    "Everything you need to know about": "에 대해 알아야 할 모든 것",
    "bank statement conversion": "은행 명세서 변환",
    
    "How accurate is VaultCaddy for": "VaultCaddy의 정확도는",
    "bank statements?": "은행 명세서에 대해 얼마나 됩니까?",
    "VaultCaddy achieves 98%+ accuracy for": "VaultCaddy는 98% 이상의 정확도를 달성합니다",
    "bank statements using advanced AI specifically trained on": "은행 명세서에서 전문적으로 훈련된 고급 AI를 사용",
    "formats. Our system recognizes all": "형식. 당사 시스템은 모든",
    "account types and handles various statement layouts with industry-leading precision.": "계정 유형을 인식하고 업계 최고의 정밀도로 다양한 명세서 레이아웃을 처리합니다.",
    
    "What": "어떤",
    "account types are supported?": "계정 유형이 지원됩니까?",
    
    "How do I export": "어떻게 내보내나요",
    "statements to QuickBooks?": "명세서를 QuickBooks로?",
    "After uploading your": "업로드 후",
    "statement, simply select": "명세서, 단순히 선택",
    "as your export format. VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop. No manual formatting required.": "내보내기 형식으로. VaultCaddy는 QuickBooks Online 또는 Desktop으로 직접 가져올 수 있는 적절하게 포맷된 QBO 파일을 생성합니다. 수동 포맷 불필요.",
    
    "Is my": "제",
    "data secure with VaultCaddy?": "데이터는 VaultCaddy에서 안전합니까?",
    "Yes. We use bank-level AES-256 encryption for all data. VaultCaddy is SOC 2 Type II certified and GDPR compliant. Your": "예. 모든 데이터에 은행 수준의 AES-256 암호화를 사용합니다. VaultCaddy는 SOC 2 Type II 인증 및 GDPR 준수. 귀하의",
    "statements are automatically deleted after 24 hours. We've had zero data breaches in 3+ years of operation.": "명세서는 24시간 후 자동 삭제됩니다. 3년 이상의 운영에서 데이터 침해가 없었습니다.",
    
    "Can I batch process multiple": "여러",
    "statements?": "명세서를 일괄 처리할 수 있습니까?",
    "Yes! VaultCaddy supports unlimited batch processing. Upload 10, 50, or 100+": "예! VaultCaddy는 무제한 일괄 처리를 지원합니다. 10, 50 또는 100개 이상의",
    "statements simultaneously. Each file is processed independently in 3-5 seconds. Perfect for accounting firms or businesses with multiple accounts.": "명세서를 동시에 업로드. 각 파일은 3-5초 내에 독립적으로 처리됩니다. 회계 사무소 또는 여러 계정이 있는 비즈니스에 완벽.",
    
    # Trust Badges
    "AES-256 Encrypted": "AES-256 암호화",
    "Bank-level security": "은행 수준 보안",
    "SOC 2 Type II": "SOC 2 Type II",
    "Certified secure": "인증된 보안",
    "GDPR Compliant": "GDPR 준수",
    "Data protected": "데이터 보호",
    "4.8/5 Rating": "4.8/5 평점",
    "500+ reviews": "500개 이상 리뷰",
}

def translate_content(content, translations):
    """翻译内容"""
    for english, korean in translations.items():
        content = re.sub(r'\b' + re.escape(english) + r'\b', korean, content, flags=re.IGNORECASE)
    return content

def create_ko_kr_version(source_file, target_dir="ko-KR"):
    """创建韩文版本"""
    try:
        os.makedirs(target_dir, exist_ok=True)
        
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        translated_content = translate_content(content, TRANSLATIONS_KO_KR)
        
        # 更新语言标签
        translated_content = translated_content.replace('lang="en-US"', 'lang="ko-KR"')
        translated_content = translated_content.replace('lang="en"', 'lang="ko-KR"')
        
        # 更新价格为韩元
        translated_content = translated_content.replace('$7/month', '₩9,998/월')
        translated_content = translated_content.replace('$5.59/month', '₩7,998/월')
        translated_content = translated_content.replace('$67', '₩95,976')
        translated_content = translated_content.replace('$0.06/page', '₩80/페이지')
        
        target_file = os.path.join(target_dir, os.path.basename(source_file))
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return True, "Success"
        
    except Exception as e:
        return False, str(e)

def batch_create_ko_kr():
    """批量创建韩文版本"""
    print("🇰🇷 開始創建韓文版本...")
    print("=" * 70)
    
    v3_files = [f for f in os.listdir('.') if f.endswith('-v3.html') and not f.startswith(('zh-', 'ja-', 'ko-'))]
    
    success_count = 0
    error_count = 0
    
    for i, file_name in enumerate(sorted(v3_files), 1):
        bank_name = file_name.replace('-statement-v3.html', '').replace('-', ' ').title()
        
        success, message = create_ko_kr_version(file_name)
        
        if success:
            print(f"✅ {i}/50 - {bank_name}")
            success_count += 1
        else:
            print(f"❌ {i}/50 - {bank_name} - 오류: {message}")
            error_count += 1
    
    print("=" * 70)
    print(f"\n🎉 생성 완료!")
    print(f"✅ 성공: {success_count}/50")
    print(f"❌ 실패: {error_count}/50")
    
    if success_count > 0:
        print(f"\n📁 생성된 파일:")
        print(f"   디렉토리: ko-KR/")
        print(f"   파일 수: {success_count}개")
        
        print(f"\n📈 예상 효과:")
        print(f"   대상 시장: 한국")
        print(f"   잠재 사용자: 80,000+")
        print(f"   예상 전환: 800명/년")
        print(f"   연간 수익: ~₩64,000,000 (~US$57,600)")

if __name__ == '__main__':
    batch_create_ko_kr()

