#!/usr/bin/env python3
"""
修复Firstproject页面的翻译问题

作用：
1. 在translations.js中添加firstproject相关翻译键
2. 修复firstproject.html中的混乱文本
3. 为关键元素添加data-translate属性
"""

import os
import re

# Firstproject相关的翻译键
FIRSTPROJECT_TRANSLATIONS = {
    'en': {
        'select_document_type': 'Select Document Type',
        'bank_statement': 'Bank Statement',
        'bank_statement_desc': 'Convert bank statements to Excel and CSV format',
        'invoice': 'Invoice',
        'invoice_desc': 'Extract number, date, project details, price and supplier information',
        'drag_drop_files': 'Drag and drop files here or click to upload',
        'file_format_support': 'Supports PDF, JPG, PNG formats (Max 10MB) | ✨ Batch upload supported',
        'file_upload': 'File Upload',
        'ai_analysis': 'AI Analysis',
        'data_extraction': 'Data Extraction',
        'cloud_storage': 'Cloud Storage',
        'processing_progress': 'Processing Progress',
        'date_filter': 'Date Filter',
        'date_range': 'Date Range',
        'upload_date_range': 'Upload Date Range',
        'clear_filter': 'Clear Filter',
        'document_name': 'Document Name',
        'type': 'Type',
        'status': 'Status',
        'supplier_source_bank': 'Supplier/Source/Bank',
        'amount': 'Amount',
        'date': 'Date',
        'upload_date': 'Upload Date',
        'no_results': 'No results.',
        'total': 'Total',
        'invoices': 'invoices',
        'rows_per_page': 'Rows per page',
        'page': 'Page',
        'of': 'of',
        'to': 'to',
    },
    'zh-TW': {
        'select_document_type': '選擇文檔類型',
        'bank_statement': '銀行對帳單',
        'bank_statement_desc': '將銀行對帳單轉換為 Excel 和 CSV 格式',
        'invoice': '發票',
        'invoice_desc': '提取編號、日期、項目明細、價格及供應商信息',
        'drag_drop_files': '將文件拖放到此處或點擊上傳',
        'file_format_support': '支持 PDF、JPG、PNG 格式（最大 10MB）| ✨ 支持批量上傳',
        'file_upload': '文件上傳',
        'ai_analysis': 'AI 分析',
        'data_extraction': '數據提取',
        'cloud_storage': '雲端存儲',
        'processing_progress': '處理進度',
        'date_filter': '日期篩選',
        'date_range': '日期範圍',
        'upload_date_range': '上傳日期範圍',
        'clear_filter': '清除篩選',
        'document_name': '文檔名稱',
        'type': '類型',
        'status': '狀態',
        'supplier_source_bank': '供應商/來源/銀行',
        'amount': '金額',
        'date': '日期',
        'upload_date': '上傳日期',
        'no_results': '無結果。',
        'total': '共',
        'invoices': '張發票',
        'rows_per_page': '每頁行數',
        'page': '第',
        'of': '頁，共',
        'to': '至',
    },
    'ja': {
        'select_document_type': '文書タイプを選択',
        'bank_statement': '銀行取引明細書',
        'bank_statement_desc': '銀行取引明細書を Excel と CSV 形式に変換',
        'invoice': '請求書',
        'invoice_desc': '番号、日付、プロジェクト明細、価格、サプライヤー情報を抽出',
        'drag_drop_files': 'ここにファイルをドラッグ＆ドロップするかクリックしてアップロード',
        'file_format_support': 'PDF、JPG、PNG形式対応（最大10MB）| ✨ バッチアップロード対応',
        'file_upload': 'ファイルアップロード',
        'ai_analysis': 'AI分析',
        'data_extraction': 'データ抽出',
        'cloud_storage': 'クラウドストレージ',
        'processing_progress': '処理進捗',
        'date_filter': '日付フィルター',
        'date_range': '日付範囲',
        'upload_date_range': 'アップロード日範囲',
        'clear_filter': 'フィルターをクリア',
        'document_name': '文書名',
        'type': 'タイプ',
        'status': 'ステータス',
        'supplier_source_bank': 'サプライヤー/ソース/銀行',
        'amount': '金額',
        'date': '日付',
        'upload_date': 'アップロード日',
        'no_results': '結果がありません。',
        'total': '合計',
        'invoices': '件の請求書',
        'rows_per_page': 'ページあたりの行数',
        'page': 'ページ',
        'of': '/',
        'to': '〜',
    },
    'ko': {
        'select_document_type': '문서 유형 선택',
        'bank_statement': '은행 명세서',
        'bank_statement_desc': '은행 명세서를 Excel 및 CSV 형식으로 변환',
        'invoice': '송장',
        'invoice_desc': '번호, 날짜, 프로젝트 명세, 가격 및 공급업체 정보 추출',
        'drag_drop_files': '파일을 여기에 드래그 앤 드롭하거나 클릭하여 업로드',
        'file_format_support': 'PDF, JPG, PNG 형식 지원 (최대 10MB) | ✨ 배치 업로드 지원',
        'file_upload': '파일 업로드',
        'ai_analysis': 'AI 분석',
        'data_extraction': '데이터 추출',
        'cloud_storage': '클라우드 스토리지',
        'processing_progress': '처리 진행률',
        'date_filter': '날짜 필터',
        'date_range': '날짜 범위',
        'upload_date_range': '업로드 날짜 범위',
        'clear_filter': '필터 지우기',
        'document_name': '문서 이름',
        'type': '유형',
        'status': '상태',
        'supplier_source_bank': '공급업체/출처/은행',
        'amount': '금액',
        'date': '날짜',
        'upload_date': '업로드 날짜',
        'no_results': '결과가 없습니다.',
        'total': '총',
        'invoices': '개의 송장',
        'rows_per_page': '페이지당 행 수',
        'page': '페이지',
        'of': '/',
        'to': '~',
    }
}

def add_firstproject_translations(file_path):
    """在translations.js中添加firstproject翻译键"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # 为每个语言添加翻译键
        for lang_code, translations in FIRSTPROJECT_TRANSLATIONS.items():
            # 检查是否已经存在select_document_type
            lang_section_pattern = rf"'{lang_code}':\s*\{{[^}}]*'select_document_type':"
            
            if re.search(lang_section_pattern, content, re.DOTALL):
                print(f"  ⏭️  {lang_code}: Firstproject翻译键已存在")
                continue
            
            # 找到该语言的TRANSLATIONS对象
            pattern = rf"('{lang_code}':\s*\{{[^}}]*?)(\s*\}})"
            
            # 构建要添加的翻译文本
            trans_lines = []
            for key, value in translations.items():
                # 转义单引号
                escaped_value = value.replace("'", "\\'")
                trans_lines.append(f"        '{key}': '{escaped_value}'")
            
            trans_text = ',\n' + ',\n'.join(trans_lines)
            
            # 在语言对象的最后一个属性后添加
            def replacer(match):
                return match.group(1) + trans_text + match.group(2)
            
            content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
            print(f"  ✅ {lang_code}: 已添加 {len(translations)} 个Firstproject翻译键")
            modified = True
        
        # 如果有修改才写回
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return modified
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def fix_firstproject_html(file_path, lang_code):
    """修复firstproject.html中的混乱文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复混杂的文本 - 根据网页内容中看到的问题
        
        # 1. 修复"SelectDocumentType"
        content = re.sub(
            r'SelectDocumentType',
            '<span data-translate="select_document_type">Select Document Type</span>',
            content
        )
        
        # 2. 修复"willBank StatementConvert to"等混乱文本
        content = re.sub(
            r'willBank StatementConvert to Excel and CSV Format',
            '<span data-translate="bank_statement_desc">Convert bank statements to Excel and CSV format</span>',
            content
        )
        
        content = re.sub(
            r'할은행 명세서변환 Excel 및 CSV 포맷',
            '<span data-translate="bank_statement_desc">은행 명세서를 Excel 및 CSV 형식으로 변환</span>',
            content
        )
        
        content = re.sub(
            r'將銀行取引明細書変換 Excel と CSV フォーマット',
            '<span data-translate="bank_statement_desc">銀行取引明細書を Excel と CSV 形式に変換</span>',
            content
        )
        
        # 3. 修复"Extract number、Date、ProjectDetails"等
        content = re.sub(
            r'Extract number、Date、ProjectDetails、PricingAnd supplierInformation',
            '<span data-translate="invoice_desc">Extract number, date, project details, price and supplier information</span>',
            content
        )
        
        content = re.sub(
            r'번호 추출、날짜、프로젝트명세、가격및 공급업체정보',
            '<span data-translate="invoice_desc">번호, 날짜, 프로젝트 명세, 가격 및 공급업체 정보 추출</span>',
            content
        )
        
        content = re.sub(
            r'番号抽出、日付、プロジェクト明細、価格とサプライヤー信息',
            '<span data-translate="invoice_desc">番号、日付、プロジェクト明細、価格、サプライヤー情報を抽出</span>',
            content
        )
        
        # 4. 修复"共 0 張송장" / "共 0 張請求書" / "total 0 sheetInvoice"
        content = re.sub(
            r'total 0 sheetInvoice',
            '<span data-translate="total">Total</span> 0 <span data-translate="invoices">invoices</span>',
            content
        )
        
        content = re.sub(
            r'共 0 張송장',
            '<span data-translate="total">총</span> 0 <span data-translate="invoices">개의 송장</span>',
            content
        )
        
        content = re.sub(
            r'共 0 張請求書',
            '<span data-translate="total">合計</span> 0 <span data-translate="invoices">件の請求書</span>',
            content
        )
        
        # 5. 修复"inputProjectNametoCreatenew的DocumentProject"等
        content = re.sub(
            r'inputProjectNametoCreatenew的DocumentProject',
            '<span data-translate="project_name_placeholder">Enter project name to create a new document project</span>',
            content
        )
        
        content = re.sub(
            r'입력프로젝트이름以생성새로운的문서프로젝트',
            '<span data-translate="project_name_placeholder">프로젝트 이름을 입력하여 새 문서 프로젝트 생성</span>',
            content
        )
        
        content = re.sub(
            r'輸入プロジェクト名前以作成新の文書プロジェクト',
            '<span data-translate="project_name_placeholder">プロジェクト名を入力して新しいドキュメントプロジェクトを作成</span>',
            content
        )
        
        # 6. 修复"CreatenewProject" / "생성새로운프로젝트" / "作成新プロジェクト"
        content = re.sub(
            r'CreatenewProject',
            '<span data-translate="create_new_project">Create New Project</span>',
            content
        )
        
        content = re.sub(
            r'생성새로운프로젝트',
            '<span data-translate="create_new_project">새 프로젝트 생성</span>',
            content
        )
        
        content = re.sub(
            r'作成新プロジェクト',
            '<span data-translate="create_new_project">新しいプロジェクトを作成</span>',
            content
        )
        
        # 只在有实际修改时才写回
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    print("🔧 开始修复Firstproject页面翻译问题...")
    print("=" * 60)
    
    # 第一步：添加翻译键到translations.js
    print("\n📝 步骤1: 添加Firstproject翻译键到translations.js")
    print("-" * 60)
    
    if os.path.exists('translations.js'):
        add_firstproject_translations('translations.js')
    else:
        print("  ❌ translations.js 不存在")
    
    # 第二步：修复firstproject.html文件
    print("\n📝 步骤2: 修复firstproject.html文件")
    print("-" * 60)
    
    files_to_fix = [
        ('firstproject.html', ''),
        ('en/firstproject.html', 'en'),
        ('jp/firstproject.html', 'jp'),
        ('kr/firstproject.html', 'kr'),
    ]
    
    fixed_count = 0
    
    for file_path, lang_code in files_to_fix:
        if not os.path.exists(file_path):
            print(f"⏭️  跳过: {file_path} (不存在)")
            continue
        
        print(f"\n📄 处理: {file_path}")
        
        was_fixed = fix_firstproject_html(file_path, lang_code)
        
        if was_fixed:
            print(f"   ✅ 已修复混乱文本并添加翻译标记")
            fixed_count += 1
        else:
            print(f"   ⏭️  无需修改")
    
    # 总结
    print(f"\n\n{'=' * 60}")
    print(f"📊 修复完成")
    print(f"{'=' * 60}")
    print(f"✅ translations.js: 已添加Firstproject翻译键")
    print(f"✅ 修复的firstproject.html文件: {fixed_count}/4")
    print(f"{'=' * 60}")
    
    print(f"\n💡 测试链接:")
    print(f"- 英文: https://vaultcaddy.com/en/firstproject.html?project=V3UX1IvpVbHLsW2fXZ45")
    print(f"- 日文: https://vaultcaddy.com/jp/firstproject.html?project=V3UX1IvpVbHLsW2fXZ45")
    print(f"- 韩文: https://vaultcaddy.com/kr/firstproject.html?project=V3UX1IvpVbHLsW2fXZ45")

if __name__ == '__main__':
    main()

