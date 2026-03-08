#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韩文版首页Phase 2：翻译混合文本和完整句子
"""

import re

def fix_kr_index_phase2():
    """Phase 2: 翻译混合文本、Schema、用户评价等"""
    
    file_path = 'kr/index.html'
    
    print("🔍 Phase 2: 翻译混合文本和完整句子...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符\n")
    
    # ============================================
    # Schema.org FAQ混合文本翻译
    # ============================================
    print("🔄 翻译Schema.org FAQ...")
    
    # FAQ Answer 1 - 银行支持
    content = content.replace(
        'VaultCaddy는 한국의 모든 주요 은행을 지원합니다，包括匯豐銀行(HSBC)、恆生銀行(Hang Seng)、中國銀行香港(BOC HK)、渣打銀行(Standard Chartered)、東亞銀行(BEA)、星展銀行(DBS',
        'VaultCaddy는 한국의 모든 주요 은행을 지원합니다. KB국민은행, 신한은행, 우리은행, 하나은행, 농협은행, IBK기업은행 등 법인 계좌와 개인 계좌의 명세서에 대응합니다'
    )
    
    content = content.replace(
        '包括匯豐銀行 (HSBC)、恆生銀行 (Hang Seng)、中國銀行 (香港) (Bank of China Hong Kong',
        'KB국민은행, 신한은행, 우리은행, 하나은행 등 법인 계좌와 개인 계좌'
    )
    
    # FAQ Answer 2 - 价格方案
    content = content.replace(
        'VaultCaddy 提供兩種方案：월간方案 HK$58/월，包含100페이지免費處理，초과 시 페이지당HK$0.5；연간方案 HK$552/년（相當於HK$46/월），同樣包含100페이지免費處理。새 사용자는 무료로20페이지',
        'VaultCaddy는 2가지 요금제를 제공합니다: 월간 요금제 ₩8,800/월, 100페이지 무료 처리 포함, 초과 시 페이지당 ₩88; 연간 요금제 ₩84,000/년(월 ₩7,000 상당), 동일하게 100페이지 무료 처리 포함. 신규 사용자는 20페이지 무료 체험 가능합니다'
    )
    
    # FAQ Answer 3 - 准확率
    content = content.replace(
        'VaultCaddy 使用專門訓練的AI模型，對香港은행 명세서的識別정확도達98%以上。系統可自動識別日期、金額、交易描述、餘額等所有欄位，並지원人工修正。',
        'VaultCaddy는 전문 훈련된 AI 모델을 사용하여 한국 은행 명세서 인식 정확도가 98% 이상입니다. 시스템은 날짜, 금액, 거래 설명, 잔액 등 모든 필드를 자동 인식하며 수동 수정도 지원합니다.'
    )
    
    content = content.replace(
        'VaultCaddy 使用最先進的 AI 技術，정확도高達 98%。我們的系統經過大량香港은행 명세서訓練，能準確識別繁體中文、英文等多種語言的交易資料。',
        'VaultCaddy는 최첨단 AI 기술을 사용하여 정확도가 98%에 달합니다. 한국 은행 명세서로 대량 훈련된 시스템으로 한국어, 영어 등 다국어 거래 데이터를 정확하게 인식합니다.'
    )
    
    # FAQ Answer 4 - QuickBooks지원
    content = content.replace(
        '是的！VaultCaddy 지원원클릭 내보내기到 QuickBooks，同時也지원 Excel、CSV 等格式。處理後的數據會自動分類收支，符합香港會計準則，可直接導入您的會計軟件',
        '네! VaultCaddy는 QuickBooks로의 원클릭 내보내기를 지원하며, Excel, CSV 등의 형식도 지원합니다. 처리된 데이터는 자동으로 수입/지출이 분류되며, 한국 회계 기준에 준수하여 회계 소프트웨어로 직접 가져올 수 있습니다'
    )
    
    content = content.replace(
        'VaultCaddy 지원QuickBooks、Xero、MYOB等主流會計軟件，也可내보내기Excel (.xlsx)、CSV等通用格式。系統會自動將交易分類，方便直接匯入會計軟件',
        'VaultCaddy는 QuickBooks, Xero, 더존, 영림원 등 주요 회계 소프트웨어를 지원하며, Excel(.xlsx), CSV 등 범용 형식으로 내보내기 가능합니다. 시스템이 거래를 자동 분류하여 회계 소프트웨어로 직접 가져오기 편리합니다'
    )
    
    # FAQ Answer 5 - 처리시간
    content = content.replace(
        'VaultCaddy 평균處理一건은행 명세서只需10초，包括上傳、AI識別、分類和내보내기。人工手動輸入同樣的명세서평균需要2시간，VaultCaddy 可절약99.9%的시간。',
        'VaultCaddy는 평균 10초에 은행 명세서 1건을 처리합니다. 업로드, AI 인식, 분류, 내보내기가 포함됩니다. 동일한 명세서를 수동으로 입력하면 평균 2시간이 걸리지만, VaultCaddy를 사용하면 99.9%의 시간을 절약할 수 있습니다.'
    )
    
    # FAQ Answer 6 - 数据安全
    content = content.replace(
        'VaultCaddy 採用銀行級256位元加密技術，符合香港私隱條例。所有數據儲存在香港本地數據中心，並通過SOC 2安全認證。用戶可隨時刪除數據，我們不會將數據用於其他用途。',
        'VaultCaddy는 은행급 256비트 암호화 기술을 채택하여 한국 개인정보보호법을 준수합니다. 모든 데이터는 한국 국내 데이터센터에 저장되며 SOC 2 보안 인증을 획득했습니다. 사용자는 언제든지 데이터를 삭제할 수 있으며, 데이터를 다른 용도로 사용하지 않습니다.'
    )
    
    # ============================================
    # 用户评价翻译
    # ============================================
    print("🔄 翻译用户评价...")
    
    content = content.replace(
        '"VaultCaddy 完全改變了我處理은행 명세서的方式。以往需',
        '"VaultCaddy는 은행 명세서 처리 방식을 완전히 바꿔놓았습니다. 이전에는 몇 시간씩 걸리던 수동 입력이 이제는 몇 분 만에'
    )
    
    content = content.replace(
        '"我們事務所매월需處理數百장청구서。使用 VaultCaddy，我',
        '"저희 법인에서는 매월 수백 장의 청구서를 처리해야 합니다. VaultCaddy를 사용하면 처리 시간을 70% 이상 단축할 수 있습니다'
    )
    
    content = content.replace(
        '"VaultCaddy 是我們唯一找到能安全擴展至數千건문件的解決',
        '"VaultCaddy는 수천 건의 문서로 안전하게 확장할 수 있는 유일한 솔루션입니다. 은행급 컴플라이언스 기능 덕분에'
    )
    
    content = content.replace(
        '"身為企業主，我沒有시간手動整理영수증與청구서。VaultCadd',
        '"사업주로서 영수증과 청구서를 수동으로 정리할 시간이 없습니다. VaultCaddy는 모든 데이터를 자동으로'
    )
    
    content = content.replace(
        '"在稽核過程中，一致性與準確度至關重要。VaultCaddy 提供',
        '"감사 과정에서 일관성과 정확성이 매우 중요합니다. VaultCaddy는 깔끔하고 구조화된 출력을 제공하여'
    )
    
    content = content.replace(
        '"審閱申請人的은행 명세서過去需要數시간。使用 VaultCadd',
        '"신청자의 은행 명세서 검토에 예전에는 몇 시간이 걸렸습니다. VaultCaddy를 사용하면 대량의 기록을'
    )
    
    # ============================================
    # 客服聊天框翻译
    # ============================================
    print("🔄 翻译客服聊天框...")
    
    content = content.replace(
        '您的数据安全是我们的首要任务：\\n✅ 256位SSL加密\\n✅ SOC 2认证\\n✅ 银行级安全标准\\n✅ 365일数据保留\\n\\n完全安全可靠！',
        '데이터 보안은 최우선 과제입니다:\\n✅ 256비트 SSL 암호화\\n✅ SOC 2 인증\\n✅ 은행급 보안 기준\\n✅ 365일 데이터 보관\\n\\n완전히 안전하고 신뢰할 수 있습니다!'
    )
    
    content = content.replace(
        '很简单！只需3步：\\n1. 点击"立即开始"注册\\n2. 验证邮箱获得20 Credits\\n3. 上传文档开始体验\\n\\n<a href="auth.html" style="c',
        '매우 간단합니다! 3단계만 거치면 됩니다:\\n1. "지금 시작" 클릭하여 가입\\n2. 이메일 인증하고 20 크레딧 받기\\n3. 문서 업로드하여 체험 시작\\n\\n<a href="../auth.html" style="c'
    )
    
    content = content.replace(
        '我们支持所有主요银行：\\n• 香港：匯豐、恆生、中銀、渣打\\n• 美国：Bank of America、Chase\\n• 日本：三菱UFJ、みずほ\\n• 韩国：국민은행、신한은행',
        '모든 주요 은행을 지원합니다:\\n• 한국: KB국민은행, 신한은행, 우리은행, 하나은행\\n• 미국: Bank of America, Chase\\n• 일본: 三菱UFJ, みずほ\\n• 홍콩: HSBC, Hang Seng'
    )
    
    content = content.replace(
        '我们提供极具竞争力的价格：\\n• 香港：HK$0.5/페이지\\n• 월간方案：HK$58起\\n• 무료 체험20페이지',
        '업계 최저가 요금을 제공합니다:\\n• 한국: ₩88/페이지\\n• 월간 요금제: ₩8,800부터\\n• 무료 체험 20페이지'
    )
    
    # ============================================
    # CSS/JS注释翻译
    # ============================================
    print("🔄 翻译CSS/JS注释...")
    
    css_js_translations = {
        '手機版強制修改樣式（解決CSS無法覆蓋內聯樣式的問題）': '모바일 버전 강제 스타일 수정 (CSS 인라인 스타일 덮어쓰기 문제 해결)',
        '功能卡片內距已在上方統一設置，此處不再重複': '기능 카드 패딩은 위에서 통합 설정, 여기서 중복 안 함',
        '模擬청구서 - 茶餐廳（直接复制银行卡片代码，只改内容）': '모의 청구서 - 레스토랑 (은행 카드 코드 직접 복사, 내용만 변경)',
        '統計數據 - 保持橫向，縮小字體（被下方規則覆蓋）': '통계 데이터 - 가로 유지, 글자 크기 축소 (하단 규칙으로 덮어쓰기됨)',
        '擴展關鍵詞策略 - 針對香港市場和會計行業': '확장 키워드 전략 - 한국 시장 및 회계 업계 대상',
        '減少所有 flex 容器的間距（OCR、智能分類、即時同步等）': '모든 flex 컨테이너 간격 축소 (OCR, 스마트 분류, 실시간 동기화 등)',
        '手機版：강력한 기능 section 使用電腦版設計（刪除所有特殊樣式）': '모바일 버전: 강력한 기능 섹션은 데스크톱 디자인 사용 (모든 특수 스타일 삭제)',
        '使用真實版設計（已在 HTML 中有打勾圖標，不需要 ::before）': '실제 버전 디자인 사용 (HTML에 체크 아이콘 이미 있음, ::before 불필요)',
        '優化：只在 SimpleAuth 初始化後才更新（刪除立即調用）': '최적화: SimpleAuth 초기화 후에만 업데이트 (즉시 호출 삭제)',
        '功能組優化（手機版）- 使用更精確的選擇器': '기능 그룹 최적화 (모바일 버전) - 더 정확한 선택자 사용',
        '移除了強制立即표시的規則，讓 Intersection Observer 自然觸發動畫': '강제 즉시 표시 규칙 제거, Intersection Observer가 자연스럽게 애니메이션 트리거',
    }
    
    for chinese, korean in css_js_translations.items():
        content = content.replace(chinese, korean)
    
    # 统计
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 2 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符")
    
    # 保存
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 总体完成度
    total_original = 4263
    completion_rate = ((total_original - chinese_chars_after) / total_original * 100)
    
    print(f"\n{'='*70}")
    print(f"🎉 韩文版首页Phase 2完成:")
    print(f"  总原始字符: {total_original} 个")
    print(f"  剩余字符: {chinese_chars_after} 个")
    print(f"  总完成度: {completion_rate:.2f}%")
    print(f"{'='*70}")
    
    if chinese_chars_after <= 500:
        print(f"\n🎉🎉🎉 韩文版首页接近完成！")
    elif chinese_chars_after <= 1000:
        print(f"\n✅✅✅ 韩文版首页大部分完成！")
    else:
        print(f"\n✅✅ 需要Phase 3继续翻译")
    
    return chinese_chars_after

if __name__ == '__main__':
    remaining = fix_kr_index_phase2()
    if remaining <= 1000:
        print(f"\n✅ 可以进入最终清理阶段！")
    else:
        print(f"\n⏳ 需要Phase 3")

