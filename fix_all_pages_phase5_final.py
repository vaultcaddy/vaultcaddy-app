#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 5: 翻译剩余的2-4字常见词
⚠️ 只翻译文本，不改变任何结构
"""

import re
import os

# Phase 5 - 短词和常见术语
PHASE5_TRANSLATIONS = {
    'en': {
        # 2-4字常见词（按频率排序）
        '格式': 'Format',
        '菜單': 'Menu',
        '按鈕': 'Button',
        '更新': 'Update',
        '表格': 'Table',
        '處理': 'Process',
        '轉換': 'Convert',
        '移除': 'Remove',
        '載入': 'Load',
        '元素': 'Element',
        '明細': 'Details',
        '文件': 'File',
        '檢查': 'Check',
        '樣式': 'Style',
        '獲取': 'Get',
        '名稱': 'Name',
        '圖片': 'Image',
        '生成': 'Generate',
        '等待': 'Wait',
        '專用': 'Dedicated',
        '打開': 'Open',
        '上傳': 'Upload',
        '退回': 'Return',
        '合併': 'Merge',
        '內容': 'Content',
        '文字': 'Text',
        '標題': 'Title',
        '遮罩': 'Mask',
        '使用': 'Use',
        '切換': 'Switch',
        '選擇': 'Select',
        '批量': 'Batch',
        '沒有': 'None',
        '渲染': 'Render',
        '支持': 'Support',
        '最多': 'Maximum',
        '隊列': 'Queue',
        '方案': 'Plan',
        '其他': 'Other',
        '總數': 'Total',
        
        # 完整短语（结合上下文）
        '處理器': 'Handler',
        '處理和': 'Handle and',
        '管理器修复时序问题': 'Manager fixes timing issue',
        '白色主題樣式': 'White theme style',
        '電腦版上移': 'Desktop move up',
        '距離和': 'Distance and',
        '從減少到': 'Reduced from to',
        '減少內容距離': 'Reduce content distance',
        '只需要導航欄高度': 'Only navbar height needed',
        '只有的距離': 'Only distance',
        '確保表格最小寬度觸發水平滾動': 'Ensure table min-width triggers horizontal scroll',
        '防止標題文字': 'Prevent title text',
        '防止單元格內容': 'Prevent cell content',
        '頁面保護立即內容等待檢查': 'Page protection immediate content wait check',
        '安全隐藏控制台日志不删除代码': 'Safe hide console log do not delete code',
        
        # 更多技术词汇
        '狀態': 'Status',
        '類型': 'Type',
        '數據': 'Data',
        '信息': 'Info',
        '錯誤': 'Error',
        '警告': 'Warning',
        '成功': 'Success',
        '列表': 'List',
        '項目': 'Item',
        '對象': 'Object',
        '數組': 'Array',
        '字符串': 'String',
        '數字': 'Number',
        '布爾': 'Boolean',
        '空值': 'Null',
        '未定義': 'Undefined',
        '函數': 'Function',
        '方法': 'Method',
        '屬性': 'Property',
        '事件': 'Event',
        '監聽': 'Listen',
        '觸發': 'Trigger',
        '回調': 'Callback',
        '異步': 'Async',
        '同步': 'Sync',
        '加載': 'Load',
        '卸載': 'Unload',
        '初始': 'Initial',
        '完成': 'Complete',
        '失敗': 'Fail',
        '成功': 'Success',
        '進度': 'Progress',
        '百分比': 'Percentage',
        '計數': 'Count',
        '索引': 'Index',
        '鍵': 'Key',
        '值': 'Value',
        '對': 'Pair',
        '映射': 'Map',
        '集合': 'Set',
        '隊列': 'Queue',
        '棧': 'Stack',
        '樹': 'Tree',
        '節點': 'Node',
        '根': 'Root',
        '葉子': 'Leaf',
        '父': 'Parent',
        '子': 'Child',
        '兄弟': 'Sibling',
        '深度': 'Depth',
        '寬度': 'Width',
        '高度': 'Height',
        '長度': 'Length',
        '大小': 'Size',
        '數量': 'Quantity',
        '總計': 'Total',
        '平均': 'Average',
        '最大': 'Maximum',
        '最小': 'Minimum',
        '中間': 'Middle',
        '開始': 'Start',
        '結束': 'End',
        '範圍': 'Range',
        '區間': 'Interval',
        '步長': 'Step',
        '增量': 'Increment',
        '減量': 'Decrement',
        '乘法': 'Multiply',
        '除法': 'Divide',
        '求和': 'Sum',
        '求差': 'Difference',
        '求積': 'Product',
        '求商': 'Quotient',
        '求餘': 'Remainder',
        '取整': 'Round',
        '向上': 'Ceil',
        '向下': 'Floor',
        '絕對值': 'Absolute',
        '正數': 'Positive',
        '負數': 'Negative',
        '零': 'Zero',
        '非零': 'Non-zero',
        '真': 'True',
        '假': 'False',
        '是': 'Yes',
        '否': 'No',
        '有': 'Has',
        '無': 'None',
        '存在': 'Exists',
        '不存在': 'Not exists',
        '包含': 'Contains',
        '不包含': 'Not contains',
        '等於': 'Equals',
        '不等於': 'Not equals',
        '大於': 'Greater than',
        '小於': 'Less than',
        '大於等於': 'Greater or equal',
        '小於等於': 'Less or equal',
        '在之間': 'Between',
        '在之外': 'Outside',
        '在之前': 'Before',
        '在之後': 'After',
        '並且': 'And',
        '或者': 'Or',
        '非': 'Not',
        '如果': 'If',
        '否則': 'Else',
        '當': 'When',
        '直到': 'Until',
        '為止': 'Until',
        '遍歷': 'Iterate',
        '循環': 'Loop',
        '跳出': 'Break',
        '繼續': 'Continue',
        '返回': 'Return',
        '拋出': 'Throw',
        '捕獲': 'Catch',
        '最終': 'Finally',
        '嘗試': 'Try',
    },
    'jp': {
        '格式': 'フォーマット',
        '菜單': 'メニュー',
        '按鈕': 'ボタン',
        '更新': '更新',
        '表格': 'テーブル',
        '處理': '処理',
        '轉換': '変換',
        '移除': '削除',
        '載入': '読み込み',
        '元素': '要素',
        '明細': '明細',
        '文件': 'ファイル',
        '檢查': 'チェック',
        '樣式': 'スタイル',
        '獲取': '取得',
        '名稱': '名前',
        '圖片': '画像',
        '生成': '生成',
        '等待': '待機',
        '專用': '専用',
        '打開': '開く',
        '上傳': 'アップロード',
        '退回': '戻る',
        '合併': 'マージ',
        '內容': 'コンテンツ',
        '文字': 'テキスト',
        '標題': 'タイトル',
        '遮罩': 'マスク',
        '使用': '使用',
        '切換': '切り替え',
        '選擇': '選択',
        '批量': 'バッチ',
        '沒有': 'なし',
        '渲染': 'レンダリング',
        '支持': 'サポート',
        '最多': '最大',
        '隊列': 'キュー',
        '方案': 'プラン',
        '其他': 'その他',
        '總數': '合計',
    },
    'kr': {
        '格式': '포맷',
        '菜單': '메뉴',
        '按鈕': '버튼',
        '更新': '업데이트',
        '表格': '표',
        '處理': '처리',
        '轉換': '변환',
        '移除': '제거',
        '載入': '로드',
        '元素': '요소',
        '明細': '명세',
        '文件': '파일',
        '檢查': '확인',
        '樣式': '스타일',
        '獲取': '가져오기',
        '名稱': '이름',
        '圖片': '이미지',
        '生成': '생성',
        '等待': '대기',
        '專用': '전용',
        '打開': '열기',
        '上傳': '업로드',
        '退回': '돌아가기',
        '合併': '병합',
        '內容': '내용',
        '文字': '텍스트',
        '標題': '제목',
        '遮罩': '마스크',
        '使用': '사용',
        '切換': '전환',
        '選擇': '선택',
        '批量': '일괄',
        '沒有': '없음',
        '渲染': '렌더링',
        '支持': '지원',
        '最多': '최대',
        '隊列': '큐',
        '方案': '방안',
        '其他': '기타',
        '總數': '총계',
    }
}

def translate_file_phase5(file_path, lang_code):
    """Phase 5 翻译"""
    
    if not os.path.exists(file_path):
        return 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE5_TRANSLATIONS.get(lang_code, {})
    # 按长度排序，先替换长的
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
    print("🚀 Phase 5: 最终翻译...")
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
            before, after, replaced = translate_file_phase5(file_path, lang_code)
            
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
    print(f"Phase 5 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有设计保持不变")

if __name__ == '__main__':
    main()

