#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇰🇷 专门修复韩国版本的语言混合问题
"""

import os
import re
from pathlib import Path

def fix_ko_file(file_path):
    """修复单个韩文文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 韩文版本：所有英文替换为韩文
        replacements = {
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
            'pages included': '페이지 포함',
            'All export formats': '모든 내보내기 형식',
            'Email Support': '이메일 지원',
            'Priority email support': '우선 이메일 지원',
            '24h auto-delete': '24시간 자동 삭제',
            'Cancel anytime': '언제든지 취소',
            'Start': '시작',
            'Billed annually': '연간 청구',
            
            # 标题和大文本
            'Convert': '변환',
            'Statements in Seconds': '명세서를 몇 초 만에',
            'Made Simple': '간단하게',
            'Automate': '자동화',
            'Save 10+ hours per week': '주당 10시간 이상 절약',
            'on manual data entry': '수동 데이터 입력',
            
            # 统计数字标签
            'Hours Saved/Week': '주당 절약 시간',
            'Accuracy': '정확도',
            'Processing': '처리',
            'Per Month': '월',
            
            # 视频和演示
            'Watch how': '방법 보기',
            'are processed in seconds': '몇 초 만에 처리',
            'with 98% accuracy': '98% 정확도',
            'Average processing time': '평균 처리 시간',
            'Starting From/Month': '월 시작',
            
            # 常见问题和挑战
            'Common': '일반적인',
            'Challenges': '과제',
            'How VaultCaddy Solves These Problems': 'VaultCaddy가 이러한 문제를 해결하는 방법',
            'Specific Features': '전용 기능',
            'Built for the unique needs': '고유한 요구 사항에 맞게 설계',
            'Built for': '전용 설계',
            'designed specifically for': '전용 설계',
            
            # 行业特定功能
            'Supplier Invoice Processing': '공급업체 송장 처리',
            'Delivery Platform Reports': '배달 플랫폼 보고서',
            'POS System Export': 'POS 시스템 내보내기',
            'Cash Flow Tracking': '현금 흐름 추적',
            'Cost Analysis': '비용 분석',
            'Fund Accounting': '기금 회계',
            'Grant Expense Tracking': '보조금 비용 추적',
            'Donor Reporting': '기부자 보고',
            'Manual tracking': '수동 추적',
            'weekly': '매주',
            'Ensuring': '보장',
            'Creating': '생성',
            'Gathering data': '데이터 수집',
            
            # 解决方案文本
            'AI-powered automation': 'AI 기반 자동화',
            'Automated': '자동화된',
            'Real-time': '실시간',
            'One-click': '원클릭',
            'Always prepared': '항상 준비',
            
            # 功能描述
            'Automatic': '자동',
            'Extract': '추출',
            'Reconcile': '조정',
            'Track': '추적',
            'Compare': '비교',
            'Identify': '식별',
            
            # 其他常见文本
            'How It Works': '작동 방식',
            'Why Choose VaultCaddy?': 'VaultCaddy를 선택하는 이유는?',
            'Simple, Transparent Pricing': '간단하고 투명한 가격',
            'in Seconds': '몇 초 만에',
            'Upload Your': '업로드',
            'AI Processing': 'AI 처리',
            'Export to Your System': '시스템으로 내보내기',
            'Verify & Save': '확인 및 저장',
            'Ready to Save': '절약 준비',
            'Join 500+': '500+ 가입',
            'using VaultCaddy': 'VaultCaddy 사용',
            
            # 信任标志
            'AES-256 Encrypted': 'AES-256 암호화',
            'Bank-level security': '은행 수준 보안',
            'SOC 2 Type II Certified': 'SOC 2 Type II 인증',
            'GDPR Compliant': 'GDPR 준수',
            'Data protected': '데이터 보호',
            'Rating': '평점',
            'reviews': '리뷰',
            'Trusted by': '신뢰받는',
            'businesses in': '기업',
            
            # 特定行业文本
            'nonprofit organizations': '비영리 조직',
            'nonprofit organization businesses': '비영리 조직 비즈니스',
            'nonprofit organization invoices': '비영리 조직 송장',
            'Nonprofit Organization Accounting': '비영리 조직 회계',
            'Nonprofit Organization Invoice Processing Demo': '비영리 조직 송장 처리 데모',
            'Nonprofit Organization-Specific Features': '비영리 조직 전용 기능',
            'food service businesses': '식품 서비스 비즈니스',
        }
        
        # 逐个精确替换
        for english, korean in replacements.items():
            content = content.replace(english, korean)
        
        # 只有在内容改变时才写入
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
    ko_dir = root_dir / 'ko-KR'
    
    print("🇰🇷 开始修复韩国版本...")
    print("=" * 80)
    
    if not ko_dir.exists():
        print(f"  ⚠️ 目录不存在: {ko_dir}")
        return
    
    ko_files = list(ko_dir.glob('*-v3.html'))
    ko_files = [f for f in ko_files if 'test' not in f.name and 'backup' not in f.name]
    
    print(f"  找到 {len(ko_files)} 个韩国页面")
    
    fixed_count = 0
    for i, file_path in enumerate(ko_files, 1):
        if fix_ko_file(file_path):
            fixed_count += 1
        if i % 10 == 0:
            print(f"  进度: {i}/{len(ko_files)} (已修复: {fixed_count})")
    
    print("\n" + "=" * 80)
    print(f"✅ 韩国版本修复完成！")
    print(f"   修复了 {fixed_count} 个页面")
    print("=" * 80)

if __name__ == '__main__':
    main()

