#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VaultCaddy 多语言同步大师系统
作用：
1. 自动检测中文版页面的内容
2. 翻译并同步到英文、日文、韩文版本
3. 支持增量更新（只更新改动部分）
4. 维护翻译字典（避免重复翻译）

使用方法：
python3 multilingual_sync_master.py [页面名称]
例如：python3 multilingual_sync_master.py dashboard
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 翻译字典（核心术语）
TRANSLATION_DICT = {
    # 通用UI
    '正在驗證身份...': {
        'en': 'Verifying identity...',
        'jp': '本人確認中...',
        'kr': '신원 확인 중...'
    },
    '功能': {
        'en': 'Features',
        'jp': '機能',
        'kr': '기능'
    },
    '價格': {
        'en': 'Pricing',
        'jp': '価格',
        'kr': '가격'
    },
    '學習中心': {
        'en': 'Learning Center',
        'jp': '学習センター',
        'kr': '학습 센터'
    },
    '儀表板': {
        'en': 'Dashboard',
        'jp': 'ダッシュボード',
        'kr': '대시보드'
    },
    '首頁': {
        'en': 'Home',
        'jp': 'ホーム',
        'kr': '홈'
    },
    '登入': {
        'en': 'Login',
        'jp': 'ログイン',
        'kr': '로그인'
    },
    '登出': {
        'en': 'Logout',
        'jp': 'ログアウト',
        'kr': '로그아웃'
    },
    '帳戶': {
        'en': 'Account',
        'jp': 'アカウント',
        'kr': '계정'
    },
    '計費': {
        'en': 'Billing',
        'jp': '請求',
        'kr': '청구'
    },
    
    # Dashboard专用
    '項目': {
        'en': 'Project',
        'jp': 'プロジェクト',
        'kr': '프로젝트'
    },
    '創建': {
        'en': 'Create',
        'jp': '作成',
        'kr': '생성'
    },
    '刪除': {
        'en': 'Delete',
        'jp': '削除',
        'kr': '삭제'
    },
    '取消': {
        'en': 'Cancel',
        'jp': 'キャンセル',
        'kr': '취소'
    },
    '操作': {
        'en': 'Actions',
        'jp': '操作',
        'kr': '작업'
    },
    '上傳日期': {
        'en': 'Upload Date',
        'jp': 'アップロード日',
        'kr': '업로드 날짜'
    },
    '文檔名稱': {
        'en': 'Document Name',
        'jp': '文書名',
        'kr': '문서 이름'
    },
    '類型': {
        'en': 'Type',
        'jp': 'タイプ',
        'kr': '유형'
    },
    '狀態': {
        'en': 'Status',
        'jp': 'ステータス',
        'kr': '상태'
    },
    '金額': {
        'en': 'Amount',
        'jp': '金額',
        'kr': '금액'
    },
    '日期': {
        'en': 'Date',
        'jp': '日付',
        'kr': '날짜'
    },
    
    # Email验证
    '立即驗證您的 email 即送 20 Credits 試用！': {
        'en': 'Verify your email now and get 20 Credits free trial!',
        'jp': 'メールを今すぐ確認して20クレジットの無料トライアルを獲得！',
        'kr': '지금 이메일을 인증하고 20 크레딧 무료 평가판을 받으세요!'
    },
    '立即驗證': {
        'en': 'Verify Now',
        'jp': '今すぐ確認',
        'kr': '지금 인증'
    },
    
    # 项目管理
    '創建新項目': {
        'en': 'Create New Project',
        'jp': '新規プロジェクト作成',
        'kr': '새 프로젝트 만들기'
    },
    '項目名稱': {
        'en': 'Project Name',
        'jp': 'プロジェクト名',
        'kr': '프로젝트 이름'
    },
    '輸入項目名稱以創建新的文檔項目': {
        'en': 'Enter project name to create a new document project',
        'jp': '新しいドキュメントプロジェクトを作成するにはプロジェクト名を入力してください',
        'kr': '새 문서 프로젝트를 만들려면 프로젝트 이름을 입력하세요'
    },
    '刪除項目': {
        'en': 'Delete Project',
        'jp': 'プロジェクト削除',
        'kr': '프로젝트 삭제'
    },
    
    # Account页面
    '帳戶設定': {
        'en': 'Account Settings',
        'jp': 'アカウント設定',
        'kr': '계정 설정'
    },
    '管理您的個人資料和帳戶偏好設定': {
        'en': 'Manage your profile and account preferences',
        'jp': 'プロフィールとアカウントの設定を管理',
        'kr': '프로필 및 계정 기본 설정 관리'
    },
    '個人資料': {
        'en': 'Profile',
        'jp': 'プロフィール',
        'kr': '프로필'
    },
    '目前計劃': {
        'en': 'Current Plan',
        'jp': '現在のプラン',
        'kr': '현재 플랜'
    },
    '下次計費：': {
        'en': 'Next Billing:',
        'jp': '次回請求:',
        'kr': '다음 청구:'
    },
    '管理訂閱': {
        'en': 'Manage Subscription',
        'jp': 'サブスクリプション管理',
        'kr': '구독 관리'
    },
    '升級計劃': {
        'en': 'Upgrade Plan',
        'jp': 'プランをアップグレード',
        'kr': '플랜 업그레이드'
    },
    'Credits 使用情況': {
        'en': 'Credits Usage',
        'jp': 'クレジット使用状況',
        'kr': '크레딧 사용 현황'
    },
    '每處理 1 頁文檔消耗 1 個 Credit': {
        'en': '1 Credit is consumed per page processed',
        'jp': '1ページ処理ごとに1クレジット消費',
        'kr': '페이지당 1크레딧 소비'
    },
    '重置日期：': {
        'en': 'Reset Date:',
        'jp': 'リセット日:',
        'kr': '리셋 날짜:'
    },
    '購買 Credits': {
        'en': 'Purchase Credits',
        'jp': 'クレジット購入',
        'kr': '크레딧 구매'
    },
    '查看記錄': {
        'en': 'View History',
        'jp': '履歴を表示',
        'kr': '기록 보기'
    },
    '密碼': {
        'en': 'Password',
        'jp': 'パスワード',
        'kr': '비밀번호'
    },
    '目前密碼': {
        'en': 'Current Password',
        'jp': '現在のパスワード',
        'kr': '현재 비밀번호'
    },
    '新密碼': {
        'en': 'New Password',
        'jp': '新しいパスワード',
        'kr': '새 비밀번호'
    },
    '確認新密碼': {
        'en': 'Confirm New Password',
        'jp': '新しいパスワードを確認',
        'kr': '새 비밀번호 확인'
    },
    '密碼至少需要 8 個字元': {
        'en': 'Password must be at least 8 characters',
        'jp': 'パスワードは8文字以上必要です',
        'kr': '비밀번호는 최소 8자 이상이어야 합니다'
    },
    '更新密碼': {
        'en': 'Update Password',
        'jp': 'パスワード更新',
        'kr': '비밀번호 업데이트'
    },
    '偏好設定': {
        'en': 'Preferences',
        'jp': '設定',
        'kr': '환경설정'
    },
    '語言': {
        'en': 'Language',
        'jp': '言語',
        'kr': '언어'
    },
    '時區': {
        'en': 'Timezone',
        'jp': 'タイムゾーン',
        'kr': '시간대'
    },
    '儲存偏好設定': {
        'en': 'Save Preferences',
        'jp': '設定を保存',
        'kr': '환경설정 저장'
    },
    '購買記錄': {
        'en': 'Purchase History',
        'jp': '購入履歴',
        'kr': '구매 내역'
    },
    '危險區域': {
        'en': 'Danger Zone',
        'jp': '危険エリア',
        'kr': '위험 구역'
    },
    '刪除您的帳戶將永久移除所有資料，包括項目、文檔和設定。此操作無法復原。': {
        'en': 'Deleting your account will permanently remove all data, including projects, documents and settings. This action cannot be undone.',
        'jp': 'アカウントを削除すると、プロジェクト、ドキュメント、設定を含むすべてのデータが完全に削除されます。この操作は元に戻せません。',
        'kr': '계정을 삭제하면 프로젝트, 문서 및 설정을 포함한 모든 데이터가 영구적으로 제거됩니다. 이 작업은 취소할 수 없습니다.'
    },
    '刪除帳戶': {
        'en': 'Delete Account',
        'jp': 'アカウント削除',
        'kr': '계정 삭제'
    },
    
    # Billing页面
    '無隱藏費用，安全可靠': {
        'en': 'No hidden fees, safe and reliable',
        'jp': '隠れた費用なし、安全で信頼できる',
        'kr': '숨겨진 비용 없이 안전하고 신뢰할 수 있습니다'
    },
    '與數千家企業一起，節省財務數據錄入的時間。': {
        'en': 'Join thousands of businesses saving time on financial data entry.',
        'jp': '数千の企業とともに、財務データ入力の時間を節約しましょう。',
        'kr': '수천 개의 기업과 함께 재무 데이터 입력 시간을 절약하세요.'
    },
    '月付': {
        'en': 'Monthly',
        'jp': '月払い',
        'kr': '월간'
    },
    '年付': {
        'en': 'Yearly',
        'jp': '年払い',
        'kr': '연간'
    },
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
    '超出後每頁 HKD $0.5': {
        'en': 'Then USD $0.06 per page',
        'jp': '超過後1ページ¥8',
        'kr': '초과 시 페이지당 ₩80'
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
    '開始使用': {
        'en': 'Get Started',
        'jp': '始める',
        'kr': '시작하기'
    },
    '節省 21%': {
        'en': 'Save 20%',
        'jp': '21%節約',
        'kr': '21% 절약'
    },
    
    # 隐私政策
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
    '最後更新：': {
        'en': 'Last Updated:',
        'jp': '最終更新:',
        'kr': '최종 업데이트:'
    },
    
    # 文档处理
    '選擇文檔類型': {
        'en': 'Select Document Type',
        'jp': '文書タイプを選択',
        'kr': '문서 유형 선택'
    },
    '銀行對帳單': {
        'en': 'Bank Statement',
        'jp': '銀行取引明細書',
        'kr': '은행 명세서'
    },
    '將銀行對帳單轉換為 Excel 和 CSV 格式': {
        'en': 'Convert bank statements to Excel and CSV format',
        'jp': '銀行取引明細書をExcelとCSV形式に変換',
        'kr': '은행 명세서를 Excel 및 CSV 형식으로 변환'
    },
    '發票': {
        'en': 'Invoice',
        'jp': '請求書',
        'kr': '송장'
    },
    '提取編號、日期、項目明細、價格和供應商信息': {
        'en': 'Extract number, date, line items, price and supplier information',
        'jp': '番号、日付、品目明細、価格、サプライヤー情報を抽出',
        'kr': '번호, 날짜, 품목 명세, 가격 및 공급업체 정보 추출'
    },
    '拖放文件到此處或點擊上傳': {
        'en': 'Drag and drop files here or click to upload',
        'jp': 'ここにファイルをドラッグ＆ドロップするかクリックしてアップロード',
        'kr': '파일을 여기에 드래그 앤 드롭하거나 클릭하여 업로드'
    },
    '支援 PDF、JPG、PNG 格式 (最大 10MB)｜✨ 支持批量上傳': {
        'en': 'Supports PDF, JPG, PNG formats (Max 10MB) | ✨ Batch upload supported',
        'jp': 'PDF、JPG、PNG形式対応（最大10MB）| ✨ バッチアップロード対応',
        'kr': 'PDF, JPG, PNG 형식 지원 (최대 10MB) | ✨ 배치 업로드 지원'
    },
    '文件上傳': {
        'en': 'File Upload',
        'jp': 'ファイルアップロード',
        'kr': '파일 업로드'
    },
    'AI 分析': {
        'en': 'AI Analysis',
        'jp': 'AI分析',
        'kr': 'AI 분석'
    },
    '數據提取': {
        'en': 'Data Extraction',
        'jp': 'データ抽出',
        'kr': '데이터 추출'
    },
    '雲端存儲': {
        'en': 'Cloud Storage',
        'jp': 'クラウドストレージ',
        'kr': '클라우드 스토리지'
    },
    '處理進度': {
        'en': 'Processing Progress',
        'jp': '処理進捗',
        'kr': '처리 진행률'
    },
    '上傳文件': {
        'en': 'Upload Files',
        'jp': 'ファイルをアップロード',
        'kr': '파일 업로드'
    },
    '匯出': {
        'en': 'Export',
        'jp': 'エクスポート',
        'kr': '내보내기'
    },
    '日期篩選': {
        'en': 'Date Filter',
        'jp': '日付フィルター',
        'kr': '날짜 필터'
    },
    '日期範圍': {
        'en': 'Date Range',
        'jp': '日付範囲',
        'kr': '날짜 범위'
    },
    '至': {
        'en': 'to',
        'jp': '〜',
        'kr': '~'
    },
    '上傳日期範圍': {
        'en': 'Upload Date Range',
        'jp': 'アップロード日付範囲',
        'kr': '업로드 날짜 범위'
    },
    '清除篩選': {
        'en': 'Clear Filter',
        'jp': 'フィルターをクリア',
        'kr': '필터 지우기'
    },
    '供應商/來源/銀行': {
        'en': 'Supplier/Source/Bank',
        'jp': 'サプライヤー/ソース/銀行',
        'kr': '공급업체/출처/은행'
    },
    '共 0 張發票': {
        'en': '0 invoices total',
        'jp': '合計0件の請求書',
        'kr': '총 0개 송장'
    },
    '所有記錄': {
        'en': 'All Records',
        'jp': '全記録',
        'kr': '모든 기록'
    },
    '載入記錄中...': {
        'en': 'Loading records...',
        'jp': '記録を読み込み中...',
        'kr': '기록 로드 중...'
    },
    '描述': {
        'en': 'Description',
        'jp': '説明',
        'kr': '설명'
    },
    
    # 文档详情页面
    '返回儀表板': {
        'en': 'Back to Dashboard',
        'jp': 'ダッシュボードに戻る',
        'kr': '대시보드로 돌아가기'
    },
    '載入中...': {
        'en': 'Loading...',
        'jp': '読み込み中...',
        'kr': '로드 중...'
    },
    '已儲存': {
        'en': 'Saved',
        'jp': '保存済み',
        'kr': '저장됨'
    },
    '載入文檔中...': {
        'en': 'Loading document...',
        'jp': 'ドキュメントを読み込み中...',
        'kr': '문서 로드 중...'
    },
    '載入交易記錄中...': {
        'en': 'Loading transactions...',
        'jp': '取引を読み込み中...',
        'kr': '거래 로드 중...'
    },
    '餘額': {
        'en': 'Balance',
        'jp': '残高',
        'kr': '잔액'
    },
    '顯示未對帳': {
        'en': 'Show Unreconciled',
        'jp': '未照合を表示',
        'kr': '미조정 표시'
    },
    '全選': {
        'en': 'Toggle All',
        'jp': '全選択',
        'kr': '모두 선택'
    },
    '新增項目': {
        'en': 'Add Item',
        'jp': '項目を追加',
        'kr': '항목 추가'
    },
    '上一頁': {
        'en': 'Previous',
        'jp': '前へ',
        'kr': '이전'
    },
    '下一頁': {
        'en': 'Next',
        'jp': '次へ',
        'kr': '다음'
    },
}

# 页面配置
PAGES_TO_SYNC = {
    'dashboard': {
        'source': 'dashboard.html',
        'description': 'Dashboard主页面',
        'priority': 'HIGH'
    },
    'firstproject': {
        'source': 'firstproject.html',
        'description': '项目页面',
        'priority': 'HIGH'
    },
    'document-detail': {
        'source': 'document-detail.html',
        'description': '文档详情页面',
        'priority': 'HIGH'
    },
    'account': {
        'source': 'account.html',
        'description': '账户设置页面',
        'priority': 'HIGH'
    },
    'billing': {
        'source': 'billing.html',
        'description': '计费页面',
        'priority': 'HIGH'
    },
    'privacy': {
        'source': 'privacy.html',
        'description': '隐私政策页面',
        'priority': 'MEDIUM'
    },
    'terms': {
        'source': 'terms.html',
        'description': '服务条款页面',
        'priority': 'MEDIUM'
    }
}

def translate_content(content, target_lang):
    """翻译内容"""
    
    translated = content
    translation_count = 0
    
    # 遍历翻译字典
    for zh_text, translations in TRANSLATION_DICT.items():
        if zh_text in translated and target_lang in translations:
            translated = translated.replace(zh_text, translations[target_lang])
            translation_count += 1
    
    return translated, translation_count

def sync_page(page_name, dry_run=False):
    """同步单个页面到其他语言版本"""
    
    if page_name not in PAGES_TO_SYNC:
        print(f"❌ 未知页面: {page_name}")
        return False
    
    config = PAGES_TO_SYNC[page_name]
    source_file = config['source']
    
    if not os.path.exists(source_file):
        print(f"❌ 源文件不存在: {source_file}")
        return False
    
    print(f"\n{'='*70}")
    print(f"📄 同步页面: {page_name}")
    print(f"   描述: {config['description']}")
    print(f"   优先级: {config['priority']}")
    print(f"{'='*70}\n")
    
    # 读取中文版源文件
    with open(source_file, 'r', encoding='utf-8') as f:
        zh_content = f.read()
    
    print(f"✅ 读取中文版: {source_file} ({len(zh_content)} 字符)")
    
    # 为每个语言创建版本
    for lang in ['en', 'jp', 'kr']:
        print(f"\n🌐 处理 {lang.upper()} 版本...")
        
        # 翻译内容
        translated_content, count = translate_content(zh_content, lang)
        
        print(f"   翻译项数: {count}")
        
        # 确定目标文件路径
        target_dir = Path(lang)
        target_dir.mkdir(exist_ok=True)
        target_file = target_dir / source_file
        
        if dry_run:
            print(f"   [DRY RUN] 将写入: {target_file}")
        else:
            # 写入文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            print(f"   ✅ 已写入: {target_file}")
    
    return True

def generate_sync_report():
    """生成同步报告"""
    
    report = []
    report.append("# 🌐 VaultCaddy 多语言同步系统")
    report.append(f"\n**生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    report.append("\n---\n")
    
    report.append("## 📋 需要同步的页面\n")
    
    for page_name, config in PAGES_TO_SYNC.items():
        status = "✅" if os.path.exists(config['source']) else "❌"
        report.append(f"### {page_name}")
        report.append(f"- **状态：** {status}")
        report.append(f"- **源文件：** `{config['source']}`")
        report.append(f"- **描述：** {config['description']}")
        report.append(f"- **优先级：** {config['priority']}")
        report.append("")
    
    report.append("\n---\n")
    report.append("## 📊 翻译字典统计\n")
    report.append(f"- **术语总数：** {len(TRANSLATION_DICT)}")
    report.append(f"- **支持语言：** 英文(EN)、日文(JP)、韩文(KR)")
    report.append("")
    
    report.append("\n---\n")
    report.append("## 🚀 使用方法\n")
    report.append("```bash")
    report.append("# 同步单个页面")
    report.append("python3 multilingual_sync_master.py dashboard")
    report.append("")
    report.append("# 同步所有页面")
    report.append("python3 multilingual_sync_master.py all")
    report.append("")
    report.append("# 预览模式（不实际写入）")
    report.append("python3 multilingual_sync_master.py dashboard --dry-run")
    report.append("```")
    
    report.append("\n---\n")
    report.append("## 💡 工作流程\n")
    report.append("1. 修改中文版页面（dashboard.html等）")
    report.append("2. 运行同步脚本")
    report.append("3. 自动翻译并创建/更新其他语言版本")
    report.append("4. 验证各语言版本")
    
    return '\n'.join(report)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          🌐 VaultCaddy 多语言同步大师系统                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print("📝 系统说明：")
    print("   - 自动检测中文版内容")
    print("   - 翻译并同步到英文、日文、韩文")
    print("   - 维护统一的翻译术语")
    print("   - 支持增量更新")
    print()
    
    # 生成同步报告
    report = generate_sync_report()
    with open('🌐_多语言同步系统说明.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 已生成系统说明文档：🌐_多语言同步系统说明.md")
    print()
    print("📊 统计：")
    print(f"   - 支持页面：{len(PAGES_TO_SYNC)} 个")
    print(f"   - 翻译术语：{len(TRANSLATION_DICT)} 个")
    print(f"   - 目标语言：3 种（EN, JP, KR）")
    print()
    print("🚀 下一步：")
    print("   1. 查看生成的说明文档")
    print("   2. 使用脚本同步特定页面")
    print("   3. 验证翻译效果")
    print()
    print("💡 使用示例：")
    print("   python3 multilingual_sync_master.py dashboard")
    print("   python3 multilingual_sync_master.py all")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        page = sys.argv[1]
        dry_run = '--dry-run' in sys.argv
        
        if page == 'all':
            print("\n🔄 同步所有页面...")
            for page_name in PAGES_TO_SYNC.keys():
                sync_page(page_name, dry_run)
        else:
            sync_page(page, dry_run)
    else:
        main()







