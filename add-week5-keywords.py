#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第5周：关键词深化与扩展
为4个语言版本添加60个新关键词（问题词+商业词+长尾词）
"""

import os
import re

# 新增关键词策略
NEW_KEYWORDS = {
    'zh': {
        # 问题词（用户痛点）- 20个
        'problem': [
            '銀行對帳單處理太慢怎麼辦',
            '手動錄入銀行對帳單錯誤多',
            '會計做帳太費時',
            '月結單人工輸入出錯',
            '銀行對帳對不上',
            '會計人手不足',
            '記帳效率低下',
            '發票整理太亂',
            '收據管理混亂',
            '財務報表延遲',
            '對帳時間太長',
            '重複輸入銀行資料',
            'QuickBooks匯入失敗',
            'Excel對帳錯誤',
            '會計軟件太貴',
            '銀行月結單看不懂',
            '跨行對帳困難',
            '多幣種對帳複雜',
            '年度結帳壓力大',
            '審計資料準備慢'
        ],
        # 商業詞（購買意圖）- 20個
        'commercial': [
            '銀行對帳單軟件價格',
            '會計軟件月費比較',
            'QuickBooks自動化方案',
            '香港最便宜記帳軟件',
            '會計SaaS訂閱',
            '企業記帳系統報價',
            'AI會計軟件購買',
            '銀行對帳服務收費',
            '會計外包vs軟件',
            '記帳軟件試用',
            '會計工具免費試用',
            '中小企會計解決方案',
            '創業公司記帳工具',
            '會計師推薦軟件',
            'CFO工具推薦',
            '財務總監必備工具',
            '會計事務所軟件',
            '香港持牌會計師工具',
            '上市公司財務軟件',
            '集團公司對帳系統'
        ],
        # 長尾詞（具體場景）- 20個
        'long_tail': [
            '匯豐銀行對帳單轉QuickBooks教學',
            '恆生銀行PDF轉Excel步驟',
            '中銀香港月結單自動處理',
            '渣打銀行對帳單OCR識別',
            '多銀行對帳單合併處理',
            '跨境收款對帳方法',
            '外幣銀行對帳單處理',
            '電商平台收款對帳',
            '餐廳銀行對帳單整理',
            '零售店收款記錄',
            '網店財務自動化',
            '自由職業者記帳',
            '小型工作室財務管理',
            '初創企業財務工具',
            '會計師事務所批量處理',
            'MPF強積金對帳',
            '香港稅務報表準備',
            '年度審計資料整理',
            '季度財務報告生成',
            '月度管理報表自動化'
        ]
    },
    'en': {
        'problem': [
            'bank statement processing too slow',
            'manual data entry errors',
            'bookkeeping takes too much time',
            'bank reconciliation mistakes',
            'accounting staff shortage',
            'inefficient record keeping',
            'invoice organization chaos',
            'receipt management problems',
            'financial report delays',
            'reconciliation time consuming',
            'duplicate bank data entry',
            'QuickBooks import issues',
            'Excel reconciliation errors',
            'accounting software too expensive',
            'bank statement hard to read',
            'multi-bank reconciliation difficult',
            'multi-currency accounting complex',
            'year-end closing pressure',
            'audit preparation slow',
            'cash flow tracking hard'
        ],
        'commercial': [
            'bank statement software pricing',
            'accounting software cost comparison',
            'QuickBooks automation solution',
            'cheapest bookkeeping software',
            'accounting SaaS subscription',
            'business accounting system quote',
            'AI accounting software purchase',
            'bank reconciliation service fee',
            'accounting outsourcing vs software',
            'bookkeeping software trial',
            'accounting tool free trial',
            'SME accounting solution',
            'startup bookkeeping tool',
            'accountant recommended software',
            'CFO tool recommendation',
            'finance director essential tool',
            'accounting firm software',
            'CPA practice management',
            'enterprise financial software',
            'group company reconciliation system'
        ],
        'long_tail': [
            'HSBC statement to QuickBooks tutorial',
            'Chase bank PDF to Excel steps',
            'Wells Fargo statement auto processing',
            'DBS bank statement OCR recognition',
            'multi-bank statement consolidation',
            'cross-border payment reconciliation',
            'foreign currency statement processing',
            'ecommerce platform payment reconciliation',
            'restaurant bank statement organization',
            'retail store payment records',
            'online shop financial automation',
            'freelancer bookkeeping guide',
            'small studio financial management',
            'startup financial tools',
            'accounting firm batch processing',
            '401k retirement account reconciliation',
            'US tax return preparation',
            'annual audit document preparation',
            'quarterly financial report generation',
            'monthly management report automation'
        ]
    },
    'ja': {
        'problem': [
            '銀行明細処理が遅すぎる',
            '手動入力ミスが多い',
            '経理作業に時間がかかる',
            '銀行照合が合わない',
            '経理人手不足',
            '記帳効率が低い',
            '請求書整理が乱雑',
            '領収書管理が混乱',
            '財務報告が遅延',
            '照合時間が長い',
            '銀行データ重複入力',
            'QuickBooks取込失敗',
            'Excel照合エラー',
            '会計ソフトが高すぎる',
            '銀行明細が読みにくい',
            '複数銀行照合が困難',
            '多通貨会計が複雑',
            '決算期プレッシャー',
            '監査資料準備が遅い',
            'キャッシュフロー追跡困難'
        ],
        'commercial': [
            '銀行明細ソフト価格',
            '会計ソフト料金比較',
            'QuickBooks自動化ソリューション',
            '最安記帳ソフト',
            '会計SaaSサブスクリプション',
            '企業会計システム見積',
            'AI会計ソフト購入',
            '銀行照合サービス料金',
            '経理アウトソーシングvsソフト',
            '記帳ソフト試用',
            '会計ツール無料トライアル',
            '中小企業会計ソリューション',
            'スタートアップ記帳ツール',
            '税理士推奨ソフト',
            'CFOツール推薦',
            '財務部長必須ツール',
            '会計事務所ソフト',
            '公認会計士業務管理',
            '上場企業財務ソフト',
            'グループ会社照合システム'
        ],
        'long_tail': [
            'みずほ銀行明細QuickBooks取込',
            '三菱UFJ銀行PDF Excel変換',
            'ゆうちょ銀行明細自動処理',
            'りそな銀行明細OCR認識',
            '複数銀行明細統合処理',
            '海外送金照合方法',
            '外貨銀行明細処理',
            'EC決済照合',
            '飲食店銀行明細整理',
            '小売店入金記録',
            'ネットショップ財務自動化',
            'フリーランス記帳',
            '小規模事業所財務管理',
            'スタートアップ財務ツール',
            '会計事務所一括処理',
            '厚生年金照合',
            '確定申告資料準備',
            '年度監査資料整理',
            '四半期財務報告生成',
            '月次管理レポート自動化'
        ]
    },
    'ko': {
        'problem': [
            '은행 명세서 처리 너무 느림',
            '수동 입력 오류가 많음',
            '경리 작업 시간 소요',
            '은행 조회 불일치',
            '경리 인력 부족',
            '장부 기록 효율 낮음',
            '청구서 정리 혼란',
            '영수증 관리 복잡',
            '재무 보고 지연',
            '조회 시간 오래 걸림',
            '은행 데이터 중복 입력',
            'QuickBooks 가져오기 실패',
            'Excel 조회 오류',
            '회계 소프트웨어 너무 비쌈',
            '은행 명세서 읽기 어려움',
            '다중 은행 조회 어려움',
            '다중 통화 회계 복잡',
            '결산 압박',
            '감사 자료 준비 느림',
            '현금 흐름 추적 어려움'
        ],
        'commercial': [
            '은행 명세서 소프트웨어 가격',
            '회계 소프트웨어 비용 비교',
            'QuickBooks 자동화 솔루션',
            '가장 저렴한 장부 소프트웨어',
            '회계 SaaS 구독',
            '기업 회계 시스템 견적',
            'AI 회계 소프트웨어 구매',
            '은행 조회 서비스 요금',
            '경리 아웃소싱 vs 소프트웨어',
            '장부 소프트웨어 체험',
            '회계 도구 무료 체험',
            '중소기업 회계 솔루션',
            '스타트업 장부 도구',
            '세무사 추천 소프트웨어',
            'CFO 도구 추천',
            '재무 이사 필수 도구',
            '회계 사무소 소프트웨어',
            '공인회계사 업무 관리',
            '상장 기업 재무 소프트웨어',
            '그룹사 조회 시스템'
        ],
        'long_tail': [
            'KB국민은행 명세서 QuickBooks 가져오기',
            '신한은행 PDF Excel 변환',
            '하나은행 명세서 자동 처리',
            '우리은행 명세서 OCR 인식',
            '다중 은행 명세서 통합',
            '해외 송금 조회 방법',
            '외환 은행 명세서 처리',
            '전자상거래 결제 조회',
            '식당 은행 명세서 정리',
            '소매점 입금 기록',
            '온라인 쇼핑몰 재무 자동화',
            '프리랜서 장부 기록',
            '소규모 스튜디오 재무 관리',
            '스타트업 재무 도구',
            '회계 사무소 일괄 처리',
            '국민연금 조회',
            '세금 신고 자료 준비',
            '연간 감사 자료 정리',
            '분기별 재무 보고서 생성',
            '월간 관리 보고서 자동화'
        ]
    }
}

def add_keywords_to_file(file_path, lang):
    """
    为指定文件添加新关键词
    
    Args:
        file_path: HTML文件路径
        lang: 语言代码
    
    Returns:
        bool: 是否成功修改
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找现有的keywords meta标签
        keywords_pattern = r'<meta\s+content="([^"]+)"\s+name="keywords"\s*/>'
        match = re.search(keywords_pattern, content)
        
        if not match:
            print(f"  ⚠️  未找到keywords标签")
            return False
        
        existing_keywords = match.group(1)
        
        # 合并新关键词
        new_keywords = NEW_KEYWORDS[lang]
        all_new_keywords = (
            new_keywords['problem'] + 
            new_keywords['commercial'] + 
            new_keywords['long_tail']
        )
        
        # 将新关键词添加到现有关键词后面
        updated_keywords = existing_keywords + ',' + ','.join(all_new_keywords)
        
        # 替换内容
        new_meta = f'<meta content="{updated_keywords}" name="keywords"/>'
        content = re.sub(keywords_pattern, new_meta, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")
        return False

def main():
    """主函数"""
    print("🔥 第5周：关键词深化与扩展")
    print("=" * 60)
    print("📋 任务：为4个语言版本各添加60个新关键词")
    print("-" * 60)
    
    # 4个版本的首页
    index_files = [
        ('index.html', 'zh', '中文版'),
        ('en/index.html', 'en', '英文版'),
        ('jp/index.html', 'ja', '日文版'),
        ('kr/index.html', 'ko', '韩文版')
    ]
    
    success_count = 0
    total_keywords_added = 0
    
    for file_path, lang, name in index_files:
        if not os.path.exists(file_path):
            print(f"⏭️  {name}: 文件不存在")
            continue
        
        print(f"\n🔄 处理 {name} ({file_path})...")
        
        if add_keywords_to_file(file_path, lang):
            keywords_count = len(NEW_KEYWORDS[lang]['problem']) + \
                           len(NEW_KEYWORDS[lang]['commercial']) + \
                           len(NEW_KEYWORDS[lang]['long_tail'])
            success_count += 1
            total_keywords_added += keywords_count
            print(f"  ✅ 成功添加 {keywords_count} 个新关键词")
            print(f"     - 问题词: {len(NEW_KEYWORDS[lang]['problem'])} 个")
            print(f"     - 商业词: {len(NEW_KEYWORDS[lang]['commercial'])} 个")
            print(f"     - 长尾词: {len(NEW_KEYWORDS[lang]['long_tail'])} 个")
        else:
            print(f"  ❌ 添加失败")
    
    print("\n" + "=" * 60)
    print("📊 添加完成总结")
    print("=" * 60)
    print(f"✅ 成功处理: {success_count}/4 个版本")
    print(f"🔑 总共添加: {total_keywords_added} 个新关键词")
    print(f"📈 平均每版本: {total_keywords_added // success_count if success_count > 0 else 0} 个")
    
    print(f"\n🚀 预期SEO效果:")
    print(f"   ✅ 覆盖更多用户搜索意图")
    print(f"   ✅ 问题词：吸引有痛点的用户")
    print(f"   ✅ 商业词：吸引购买意向用户")
    print(f"   ✅ 长尾词：覆盖具体使用场景")
    print(f"   ✅ 预期自然流量提升 +30-40%")

if __name__ == '__main__':
    main()

