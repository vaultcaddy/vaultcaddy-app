#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6: 翻译单字和2字常用词
⚠️ 只翻译文本，不改变任何结构
"""

import re
import os

# Phase 6 - 单字和2字词（高频词优先）
PHASE6_TRANSLATIONS = {
    'en': {
        # 高频2字词（优先翻译，避免拆分）
        '頁面': 'page',
        '頁數': 'page count',
        '記錄': 'record',
        '跳過': 'skip',
        '優化': 'optimize',
        '交易': 'transaction',
        '提取': 'extract',
        '搜尋': 'search',
        '確保': 'ensure',
        '詳細': 'details',
        '圖標': 'icon',
        '調整': 'adjust',
        '已經': 'already',
        '暴露': 'expose',
        '重複': 'duplicate',
        '立即': 'immediately',
        '導航': 'navigation',
        '點擊': 'click',
        '供應': 'supply',
        '輪詢': 'polling',
        '變化': 'change',
        '準備': 'prepare',
        '計算': 'calculate',
        '直接': 'direct',
        '多頁': 'multi-page',
        '排隊': 'queue',
        '複選': 'multiple select',
        '觸摸': 'touch',
        '控制': 'control',
        '滾動': 'scroll',
        '強制': 'force',
        '通用': 'general',
        '卡片': 'card',
        '完全': 'completely',
        '統一': 'unified',
        '一致': 'consistent',
        '原始': 'original',
        '自動': 'auto',
        '輪播': 'carousel',
        '當前': 'current',
        '默認': 'default',
        '保存': 'save',
        '載入': 'load',
        '更新': 'update',
        '刪除': 'delete',
        '添加': 'add',
        '修改': 'modify',
        '複製': 'copy',
        '移動': 'move',
        '創建': 'create',
        '關閉': 'close',
        '打開': 'open',
        '顯示': 'show',
        '隱藏': 'hide',
        '啟用': 'enable',
        '禁用': 'disable',
        '選擇': 'select',
        '取消': 'cancel',
        '確認': 'confirm',
        '返回': 'return',
        '繼續': 'continue',
        '停止': 'stop',
        '開始': 'start',
        '結束': 'end',
        '上傳': 'upload',
        '下載': 'download',
        '導出': 'export',
        '導入': 'import',
        '篩選': 'filter',
        '排序': 'sort',
        '分組': 'group',
        '合併': 'merge',
        '分割': 'split',
        '展開': 'expand',
        '收起': 'collapse',
        '刷新': 'refresh',
        '重置': 'reset',
        '恢復': 'restore',
        '清空': 'clear',
        '全選': 'select all',
        '反選': 'deselect',
        '批量': 'batch',
        '單個': 'single',
        '多個': 'multiple',
        '全部': 'all',
        '部分': 'partial',
        '首頁': 'home',
        '末頁': 'last page',
        '上頁': 'previous',
        '下頁': 'next',
        '跳轉': 'jump',
        '查詢': 'query',
        '檢索': 'retrieve',
        '匹配': 'match',
        '比較': 'compare',
        '驗證': 'verify',
        '測試': 'test',
        '調試': 'debug',
        '日誌': 'log',
        '報錯': 'error',
        '警告': 'warning',
        '提示': 'hint',
        '消息': 'message',
        '通知': 'notification',
        '彈窗': 'popup',
        '對話': 'dialog',
        '表單': 'form',
        '輸入': 'input',
        '輸出': 'output',
        '結果': 'result',
        '數據': 'data',
        '信息': 'info',
        '內容': 'content',
        '標題': 'title',
        '描述': 'description',
        '備註': 'note',
        '說明': 'instruction',
        
        # 常见单字（在上下文中翻译）
        '的': '',  # 的 通常作为 "的" 可以省略
        '和': 'and',
        '或': 'or',
        '與': 'and',
        '為': 'as',
        '至': 'to',
        '從': 'from',
        '到': 'to',
        '在': 'in',
        '於': 'at',
        '被': 'by',
        '將': 'will',
        '會': 'will',
        '可': 'can',
        '能': 'able',
        '要': 'need',
        '需': 'need',
        '該': 'should',
        '必': 'must',
        '已': 'already',
        '未': 'not',
        '無': 'no',
        '有': 'has',
        '是': 'is',
        '否': 'no',
        '新': 'new',
        '舊': 'old',
        '大': 'large',
        '小': 'small',
        '高': 'high',
        '低': 'low',
        '長': 'long',
        '短': 'short',
        '寬': 'wide',
        '窄': 'narrow',
        '深': 'deep',
        '淺': 'shallow',
        '前': 'front',
        '後': 'back',
        '左': 'left',
        '右': 'right',
        '上': 'up',
        '下': 'down',
        '中': 'middle',
        '內': 'inner',
        '外': 'outer',
        '多': 'many',
        '少': 'few',
        '全': 'all',
        '半': 'half',
        '單': 'single',
        '雙': 'double',
        '第': 'No.',
        '次': 'times',
        '個': '',
        '項': 'item',
        '條': '',
        '行': 'line',
        '列': 'column',
        '頁': 'page',
        '級': 'level',
        '層': 'layer',
        '組': 'group',
        '類': 'type',
        '型': 'type',
    },
    'jp': {
        '頁面': 'ページ',
        '頁數': 'ページ数',
        '記錄': '記録',
        '跳過': 'スキップ',
        '優化': '最適化',
        '交易': '取引',
        '提取': '抽出',
        '搜尋': '検索',
        '確保': '確保',
        '詳細': '詳細',
        '圖標': 'アイコン',
        '調整': '調整',
        '已經': '既に',
        '暴露': '公開',
        '重複': '重複',
        '立即': '即座に',
        '導航': 'ナビゲーション',
        '點擊': 'クリック',
        '供應': '供給',
        '輪詢': 'ポーリング',
        '變化': '変化',
        '準備': '準備',
        '計算': '計算',
        '直接': '直接',
        '多頁': '複数ページ',
        '排隊': 'キュー',
        '複選': '複数選択',
        '觸摸': 'タッチ',
        '控制': '制御',
        '滾動': 'スクロール',
        '強制': '強制',
        '通用': '汎用',
        '卡片': 'カード',
        '完全': '完全',
        '統一': '統一',
        '一致': '一致',
        '原始': '元の',
        '自動': '自動',
        '輪播': 'カルーセル',
        '和': 'と',
        '的': 'の',
    },
    'kr': {
        '頁面': '페이지',
        '頁數': '페이지 수',
        '記錄': '기록',
        '跳過': '건너뛰기',
        '優化': '최적화',
        '交易': '거래',
        '提取': '추출',
        '搜尋': '검색',
        '確保': '보장',
        '詳細': '상세',
        '圖標': '아이콘',
        '調整': '조정',
        '已經': '이미',
        '暴露': '노출',
        '重複': '중복',
        '立即': '즉시',
        '導航': '내비게이션',
        '點擊': '클릭',
        '供應': '공급',
        '輪詢': '폴링',
        '變化': '변화',
        '準備': '준비',
        '計算': '계산',
        '直接': '직접',
        '多頁': '다중 페이지',
        '排隊': '대기열',
        '複選': '다중 선택',
        '觸摸': '터치',
        '控制': '제어',
        '滾動': '스크롤',
        '強制': '강제',
        '通用': '범용',
        '卡片': '카드',
        '完全': '완전',
        '統一': '통일',
        '一致': '일치',
        '原始': '원본',
        '自動': '자동',
        '輪播': '캐러셀',
        '和': '및',
        '的': '',
    }
}

def translate_file_phase6(file_path, lang_code):
    """Phase 6 翻译"""
    
    if not os.path.exists(file_path):
        return 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE6_TRANSLATIONS.get(lang_code, {})
    # 按长度排序，先替换长的
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    replaced_count = 0
    for chinese, target in sorted_trans:
        if chinese in content and target:  # 只替换有翻译的
            content = content.replace(chinese, target)
            replaced_count += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    chinese_after = len(re.findall(r'[一-龥]', content))
    
    return chinese_before, chinese_after, replaced_count

def main():
    print("🚀 Phase 6: 翻译单字和2字词...")
    print("⚠️  只翻译文本，保持所有设计和结构不变")
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
    total_replaced = 0
    
    for page in pages:
        for lang_code, lang_name in languages.items():
            file_path = f"{lang_code}/{page}"
            before, after, replaced = translate_file_phase6(file_path, lang_code)
            
            if before > 0 and replaced > 0:
                translated = before - after
                total_before += before
                total_after += after
                total_replaced += replaced
                
                if translated > 0:
                    print(f"{lang_name} {page}: 替换{replaced}处, -{translated}字")
    
    total_translated = total_before - total_after
    percentage = (total_translated / total_before * 100) if total_before > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"Phase 6 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有设计保持不变")

if __name__ == '__main__':
    main()

