#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4: 翻译技术注释和CSS/JS中的短语
⚠️ 只翻译文本，不改变任何结构
"""

import re
import os

# Phase 4 - 技术注释和UI短语
PHASE4_TRANSLATIONS = {
    'en': {
        '選擇要': 'Select to',
        '格式化': 'Format',
        '最高優先級': 'Highest priority',
        '菜單在': 'Menu at',
        '確保菜單所有部分都是白色': 'Ensure all menu parts are white',
        '菜單背景遮罩': 'Menu background mask',
        '菜單項更大觸控區域': 'Menu items larger touch area',
        '輸入框': 'Input box',
        '部分列': 'Column section',
        '按鈕組': 'Button group',
        '個字符': ' characters',
        '統一靜態導航欄': 'Unified static navbar',
        '立即執行': 'Execute immediately',
        '首字母': 'First letter',
        '的第一個字母': 'First letter of',
        '已打開': 'Opened',
        '秒切換': 'Second toggle',
        '下拉菜單': 'Dropdown menu',
        '右上角': 'Top right corner',
        '提取編號': 'Extract number',
        '和供應商': 'And supplier',
        '動態生成': 'Dynamically generated',
        '獨立一行': 'Separate line',
        '全白色': 'All white',
        '無陰影': 'No shadow',
        '折疊按鈕': 'Collapse button',
        '已改為': 'Changed to',
        '全局變量': 'Global variable',
        '過濾列表': 'Filter list',
        '如果有': 'If any',
        
        # 更多技术术语
        '左側': 'Left side',
        '右側': 'Right side',
        '頂部': 'Top',
        '底部': 'Bottom',
        '中間': 'Middle',
        '左上': 'Top left',
        '右上': 'Top right',
        '左下': 'Bottom left',
        '右下': 'Bottom right',
        '內邊距': 'Padding',
        '外邊距': 'Margin',
        '邊框': 'Border',
        '圓角': 'Border radius',
        '陰影': 'Shadow',
        '透明度': 'Opacity',
        '層級': 'Z-index',
        '定位': 'Position',
        '浮動': 'Float',
        '清除浮動': 'Clear float',
        '溢出': 'Overflow',
        '顯示方式': 'Display',
        '可見性': 'Visibility',
        '指針': 'Cursor',
        '字體': 'Font',
        '字號': 'Font size',
        '字重': 'Font weight',
        '行高': 'Line height',
        '字間距': 'Letter spacing',
        '詞間距': 'Word spacing',
        '文本對齊': 'Text align',
        '文本裝飾': 'Text decoration',
        '文本轉換': 'Text transform',
        '垂直對齊': 'Vertical align',
        '水平對齊': 'Horizontal align',
        '背景色': 'Background color',
        '前景色': 'Foreground color',
        '背景圖': 'Background image',
        '背景位置': 'Background position',
        '背景大小': 'Background size',
        '背景重複': 'Background repeat',
        '漸變': 'Gradient',
        '過渡': 'Transition',
        '動畫': 'Animation',
        '變換': 'Transform',
        '旋轉': 'Rotate',
        '縮放': 'Scale',
        '傾斜': 'Skew',
        '位移': 'Translate',
        '持續時間': 'Duration',
        '延遲': 'Delay',
        '緩動': 'Easing',
        '幀': 'Frame',
        '關鍵幀': 'Keyframe',
        '媒體查詢': 'Media query',
        '斷點': 'Breakpoint',
        '響應式': 'Responsive',
        '自適應': 'Adaptive',
        '彈性盒': 'Flexbox',
        '網格': 'Grid',
        '容器': 'Container',
        '項目': 'Item',
        '主軸': 'Main axis',
        '交叉軸': 'Cross axis',
        '換行': 'Wrap',
        '對齊': 'Align',
        '分配': 'Justify',
        '伸展': 'Stretch',
        '收縮': 'Shrink',
        '基準': 'Basis',
        '順序': 'Order',
        '跨度': 'Span',
        '間隙': 'Gap',
        '行間隙': 'Row gap',
        '列間隙': 'Column gap',
        '模板': 'Template',
        '區域': 'Area',
    },
    'jp': {
        '選擇要': '選択',
        '格式化': 'フォーマット',
        '最高優先級': '最優先',
        '菜單在': 'メニュー位置',
        '確保菜單所有部分都是白色': 'メニュー全体を白色に',
        '菜單背景遮罩': 'メニュー背景マスク',
        '菜單項更大觸控區域': 'メニュー項目のタッチ領域拡大',
        '輸入框': '入力ボックス',
        '部分列': '列セクション',
        '按鈕組': 'ボタングループ',
        '個字符': '文字',
        '統一靜態導航欄': '統一された静的ナビゲーションバー',
        '立即執行': '即座に実行',
        '首字母': '頭文字',
        '的第一個字母': 'の最初の文字',
        '已打開': '開いた',
        '秒切換': '秒切り替え',
        '下拉菜單': 'ドロップダウンメニュー',
        '右上角': '右上隅',
        '提取編號': '番号抽出',
        '和供應商': 'とサプライヤー',
        '動態生成': '動的生成',
        '獨立一行': '独立した行',
        '全白色': '全て白色',
        '無陰影': '影なし',
        '折疊按鈕': '折りたたみボタン',
        '已改為': '変更済み',
        '全局變量': 'グローバル変数',
        '過濾列表': 'フィルターリスト',
        '如果有': 'もしあれば',
    },
    'kr': {
        '選擇要': '선택',
        '格式化': '포맷',
        '最高優先級': '최우선',
        '菜單在': '메뉴 위치',
        '確保菜單所有部分都是白色': '메뉴 전체를 흰색으로',
        '菜單背景遮罩': '메뉴 배경 마스크',
        '菜單項更大觸控區域': '메뉴 항목 터치 영역 확대',
        '輸入框': '입력 상자',
        '部分列': '열 섹션',
        '按鈕組': '버튼 그룹',
        '個字符': '자',
        '統一靜態導航欄': '통일된 정적 네비게이션 바',
        '立即執行': '즉시 실행',
        '首字母': '첫 글자',
        '的第一個字母': '의 첫 글자',
        '已打開': '열림',
        '秒切換': '초 전환',
        '下拉菜單': '드롭다운 메뉴',
        '右上角': '오른쪽 상단',
        '提取編號': '번호 추출',
        '和供應商': '및 공급업체',
        '動態生成': '동적 생성',
        '獨立一行': '독립된 줄',
        '全白色': '전체 흰색',
        '無陰影': '그림자 없음',
        '折疊按鈕': '접기 버튼',
        '已改為': '변경됨',
        '全局變量': '전역 변수',
        '過濾列表': '필터 목록',
        '如果有': '있다면',
    }
}

def translate_file_phase4(file_path, lang_code):
    """Phase 4 翻译"""
    
    if not os.path.exists(file_path):
        return 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE4_TRANSLATIONS.get(lang_code, {})
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    replaced_count = 0
    for chinese, target in sorted_trans:
        if chinese in content:
            content = content.replace(chinese, target)
            replaced_count += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    chinese_after = len(re.findall(r'[一-龥]', content))
    
    return chinese_before, chinese_after, replaced_count

def main():
    print("🚀 Phase 4: 翻译技术注释...")
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
            before, after, replaced = translate_file_phase4(file_path, lang_code)
            
            if before > 0 and replaced > 0:
                translated = before - after
                total_before += before
                total_after += after
                total_replaced += replaced
                
                print(f"{lang_name} {page}: 替换{replaced}处, -{translated}字")
    
    total_translated = total_before - total_after
    percentage = (total_translated / total_before * 100) if total_before > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"Phase 4 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有设计保持不变")

if __name__ == '__main__':
    main()

