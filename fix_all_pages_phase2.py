#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2: 翻译剩余的技术术语和UI元素
"""

import re
import os

# Phase 2 翻译字典 - 技术术语和UI元素
PHASE2_TRANSLATIONS = {
    'en': {
        '導出模塊未載入': 'Export module not loaded',
        '漢堡菜單': 'Hamburger menu',
        '居中顯示': 'Center display',
        '全白色設計': 'All white design',
        '無邊框': 'No border',
        '選擇器': 'Selector',
        '和供應商中間': 'Between supplier',
        '模態框': 'Modal',
        '被調用': 'Called',
        '上傳模態框': 'Upload modal',
        '轉換為': 'Convert to',
        '篩選器': 'Filter',
        '重新渲染': 'Re-render',
        '個文件': ' files',
        '防止重複退回': 'Prevent duplicate return',
        '當前運行': 'Currently running',
        '多頁結果': 'Multi-page results',
        '確定要': 'Confirm to',
        '獲取選中的': 'Get selected',
        '請刷新頁面後': 'Please refresh page',
        '重新嘗試': 'Retry',
        '識別中': 'Recognizing',
        '類型': 'Type',
        '大小': 'Size',
        '日期': 'Date',
        '操作': 'Actions',
        '搜索': 'Search',
        '篩選': 'Filter',
        '排序': 'Sort',
        '分頁': 'Pagination',
        '每頁顯示': 'Items per page',
        '頁碼': 'Page number',
        '跳轉': 'Jump to',
        '全選': 'Select all',
        '反選': 'Deselect',
        '批量操作': 'Batch operations',
        '批量刪除': 'Batch delete',
        '批量下載': 'Batch download',
        '導出': 'Export',
        '導入': 'Import',
        '打印': 'Print',
        '分享': 'Share',
        '復制': 'Copy',
        '粘貼': 'Paste',
        '剪切': 'Cut',
        '撤銷': 'Undo',
        '重做': 'Redo',
        '刷新': 'Refresh',
        '重載': 'Reload',
        '關閉': 'Close',
        '最小化': 'Minimize',
        '最大化': 'Maximize',
        '全屏': 'Fullscreen',
        '退出全屏': 'Exit fullscreen',
        '縮放': 'Zoom',
        '放大': 'Zoom in',
        '縮小': 'Zoom out',
        '適應屏幕': 'Fit to screen',
        '實際大小': 'Actual size',
        '預覽': 'Preview',
        '詳情': 'Details',
        '設置': 'Settings',
        '選項': 'Options',
        '高級': 'Advanced',
        '基本': 'Basic',
        '簡單': 'Simple',
        '標準': 'Standard',
        '自定義': 'Custom',
        '推薦': 'Recommended',
        '默認': 'Default',
        '應用': 'Apply',
        '重置': 'Reset',
        '恢復': 'Restore',
        '清空': 'Clear',
        '清除': 'Remove',
        '添加': 'Add',
        '新建': 'New',
        '創建': 'Create',
        '複製': 'Duplicate',
        '移動': 'Move',
        '重命名': 'Rename',
        '屬性': 'Properties',
        '信息': 'Information',
        '提示': 'Tips',
        '警告': 'Warning',
        '錯誤': 'Error',
        '成功': 'Success',
        '通知': 'Notification',
        '消息': 'Message',
        '確認操作': 'Confirm action',
        '您確定': 'Are you sure',
        '無法撤銷': 'Cannot be undone',
        '將會': 'Will',
        '請確認': 'Please confirm',
        '是否繼續': 'Continue?',
    },
    'jp': {
        '導出模塊未載入': 'エクスポートモジュール未読み込み',
        '漢堡菜單': 'ハンバーガーメニュー',
        '居中顯示': '中央表示',
        '全白色設計': '全白デザイン',
        '無邊框': '枠なし',
        '選擇器': 'セレクタ',
        '和供應商中間': 'サプライヤー間',
        '模態框': 'モーダル',
        '被調用': '呼び出された',
        '上傳模態框': 'アップロードモーダル',
        '轉換為': '変換',
        '篩選器': 'フィルター',
        '重新渲染': '再レンダリング',
        '個文件': '個のファイル',
        '防止重複退回': '重複返却を防止',
        '當前運行': '現在実行中',
        '多頁結果': '複数ページの結果',
        '確定要': '確認',
        '獲取選中的': '選択されたものを取得',
        '請刷新頁面後': 'ページを更新してください',
        '重新嘗試': '再試行',
        '識別中': '認識中',
    },
    'kr': {
        '導出模塊未載入': '내보내기 모듈 로드 안 됨',
        '漢堡菜單': '햄버거 메뉴',
        '居中顯示': '중앙 표시',
        '全白色設計': '전체 흰색 디자인',
        '無邊框': '테두리 없음',
        '選擇器': '선택기',
        '和供應商中間': '공급업체 사이',
        '模態框': '모달',
        '被調用': '호출됨',
        '上傳模態框': '업로드 모달',
        '轉換為': '변환',
        '篩選器': '필터',
        '重新渲染': '재렌더링',
        '個文件': '개 파일',
        '防止重複退回': '중복 반환 방지',
        '當前運行': '현재 실행 중',
        '多頁結果': '다중 페이지 결과',
        '確定要': '확인',
        '獲取選中的': '선택된 항목 가져오기',
        '請刷新頁面後': '페이지를 새로고침하세요',
        '重新嘗試': '다시 시도',
        '識別中': '인식 중',
    }
}

def translate_file_phase2(file_path, lang_code):
    """Phase 2 翻译"""
    
    if not os.path.exists(file_path):
        return 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE2_TRANSLATIONS.get(lang_code, {})
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, target in sorted_trans:
        if chinese in content:
            content = content.replace(chinese, target)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    chinese_after = len(re.findall(r'[一-龥]', content))
    
    return chinese_before, chinese_after

def main():
    print("🚀 Phase 2: 翻译技术术语...")
    print("="*70)
    
    pages = [
        'firstproject.html',
        'account.html',
        'billing.html',
        'dashboard.html',
        'document-detail.html',
        'terms.html',
        'privacy.html',
    ]
    
    languages = {'en': '🇬🇧英文', 'jp': '🇯🇵日文', 'kr': '🇰🇷韩文'}
    
    total_before = 0
    total_after = 0
    
    for page in pages:
        for lang_code, lang_name in languages.items():
            file_path = f"{lang_code}/{page}"
            before, after = translate_file_phase2(file_path, lang_code)
            
            if before > 0:
                translated = before - after
                total_before += before
                total_after += after
                
                if translated > 0:
                    print(f"{lang_name} {page}: -{translated}字")
    
    total_translated = total_before - total_after
    percentage = (total_translated / total_before * 100) if total_before > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"Phase 2 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

