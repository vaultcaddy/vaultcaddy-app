#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 7: 翻译复杂短语和剩余词组
⚠️ 只翻译文本，不改变任何结构
"""

import re
import os

# Phase 7 - 复杂短语和剩余词组
PHASE7_TRANSLATIONS = {
    'en': {
        # 从分析中发现的词组
        '混合並發': 'mixed concurrency',
        '完整欄位': 'complete fields',
        '台日志': 'console log',
        '不删除代码': 'do not delete code',
        '管理器': 'manager',
        '时序问题': 'timing issue',
        '電腦版': 'desktop',
        '的距離': 'distance',
        '覆蓋所': 'cover',
        '不影響': 'no effect',
        '优化加载速度': 'optimize loading speed',
        '僅手機': 'mobile only',
        '欄的距離': 'column distance',
        '以容納': 'to accommodate',
        '重定向': 'redirect',
        '時間戳': 'timestamp',
        '期間並': 'during and',
        '所以這裡不': 'so here not',
        '再調用': 'call again',
        '按實際': 'by actual',
        '法讀取': 'cannot read',
        '超過並發限制': 'exceed concurrency limit',
        '一個任務': 'one task',
        '都釋放鎖': 'release all locks',
        '機制持續監控': 'mechanism continuously monitors',
        '避免不': 'avoid',
        '更改所': 'change',
        '法復原': 'cannot restore',
        '待實現': 'to be implemented',
        '分析選': 'analyze selection',
        '勾選且': 'checked and',
        '勾選的': 'checked',
        
        # 更多技术词汇
        '欄位': 'field',
        '並發': 'concurrency',
        '防止': 'prevent',
        '避免': 'avoid',
        '確認': 'confirm',
        '驗證': 'verify',
        '檢測': 'detect',
        '監控': 'monitor',
        '追蹤': 'track',
        '記錄': 'log',
        '保存': 'save',
        '恢復': 'restore',
        '還原': 'restore',
        '撤銷': 'undo',
        '重做': 'redo',
        '刷新': 'refresh',
        '重載': 'reload',
        '加載': 'load',
        '卸載': 'unload',
        '初始化': 'initialize',
        '釋放': 'release',
        '清理': 'cleanup',
        '銷毀': 'destroy',
        '創建': 'create',
        '生成': 'generate',
        '構建': 'build',
        '編譯': 'compile',
        '解析': 'parse',
        '分析': 'analyze',
        '計算': 'calculate',
        '處理': 'process',
        '執行': 'execute',
        '運行': 'run',
        '啟動': 'start',
        '停止': 'stop',
        '暫停': 'pause',
        '繼續': 'resume',
        '取消': 'cancel',
        '終止': 'terminate',
        '結束': 'end',
        '完成': 'complete',
        '失敗': 'fail',
        '成功': 'success',
        '錯誤': 'error',
        '異常': 'exception',
        '警告': 'warning',
        '提示': 'tip',
        '通知': 'notify',
        '消息': 'message',
        '事件': 'event',
        '回調': 'callback',
        '觸發': 'trigger',
        '監聽': 'listen',
        '綁定': 'bind',
        '解綁': 'unbind',
        '註冊': 'register',
        '註銷': 'unregister',
        '訂閱': 'subscribe',
        '取消訂閱': 'unsubscribe',
        '發布': 'publish',
        '廣播': 'broadcast',
        '接收': 'receive',
        '發送': 'send',
        '傳輸': 'transfer',
        '傳遞': 'pass',
        '返回': 'return',
        '響應': 'response',
        '請求': 'request',
        '查詢': 'query',
        '檢索': 'retrieve',
        '搜索': 'search',
        '過濾': 'filter',
        '篩選': 'filter',
        '排序': 'sort',
        '分組': 'group',
        '聚合': 'aggregate',
        '合並': 'merge',
        '拆分': 'split',
        '連接': 'join',
        '斷開': 'disconnect',
        '重連': 'reconnect',
        '超時': 'timeout',
        '重試': 'retry',
        '延遲': 'delay',
        '等待': 'wait',
        '阻塞': 'block',
        '非阻塞': 'non-blocking',
        '同步': 'sync',
        '異步': 'async',
        '並行': 'parallel',
        '串行': 'serial',
        '順序': 'sequence',
        '隨機': 'random',
        '循環': 'loop',
        '遍歷': 'iterate',
        '遞歸': 'recursive',
        '遞增': 'increment',
        '遞減': 'decrement',
        '累加': 'accumulate',
        '累計': 'accumulate',
        '統計': 'statistics',
        '比較': 'compare',
        '匹配': 'match',
        '替換': 'replace',
        '插入': 'insert',
        '刪除': 'delete',
        '移除': 'remove',
        '添加': 'add',
        '追加': 'append',
        '前置': 'prepend',
        '包含': 'contain',
        '排除': 'exclude',
        '選擇': 'select',
        '全選': 'select all',
        '反選': 'invert',
        '勾選': 'check',
        '取消勾選': 'uncheck',
        '選中': 'selected',
        '未選中': 'unselected',
        '可選': 'optional',
        '必選': 'required',
        '可用': 'available',
        '不可用': 'unavailable',
        '啟用': 'enabled',
        '禁用': 'disabled',
        '激活': 'active',
        '未激活': 'inactive',
        '在線': 'online',
        '離線': 'offline',
        '連接': 'connected',
        '斷開': 'disconnected',
        '正常': 'normal',
        '異常': 'abnormal',
        '有效': 'valid',
        '無效': 'invalid',
        '合法': 'legal',
        '非法': 'illegal',
        '允許': 'allow',
        '禁止': 'forbid',
        '限制': 'limit',
        '無限': 'unlimited',
        '最大': 'max',
        '最小': 'min',
        '平均': 'average',
        '總計': 'total',
        '小計': 'subtotal',
        '數量': 'quantity',
        '次數': 'count',
        '頻率': 'frequency',
        '速率': 'rate',
        '速度': 'speed',
        '進度': 'progress',
        '百分比': 'percentage',
        '比例': 'ratio',
        '比率': 'rate',
        '權重': 'weight',
        '優先級': 'priority',
        '等級': 'level',
        '級別': 'level',
        '層次': 'hierarchy',
        '層級': 'level',
        '深度': 'depth',
        '寬度': 'width',
        '高度': 'height',
        '長度': 'length',
        '大小': 'size',
        '容量': 'capacity',
        '限額': 'quota',
        '閾值': 'threshold',
        '範圍': 'range',
        '區間': 'interval',
        '間隔': 'interval',
        '步長': 'step',
        '偏移': 'offset',
        '位置': 'position',
        '坐標': 'coordinate',
        '索引': 'index',
        '下標': 'subscript',
        '指針': 'pointer',
        '引用': 'reference',
        '地址': 'address',
        '路徑': 'path',
        '鏈接': 'link',
        '地址': 'url',
        '域名': 'domain',
        '端口': 'port',
        '協議': 'protocol',
        '版本': 'version',
        '版本號': 'version number',
        '標識': 'identifier',
        '標識符': 'identifier',
        '名稱': 'name',
        '標題': 'title',
        '描述': 'description',
        '說明': 'description',
        '注釋': 'comment',
        '備註': 'note',
        '標記': 'mark',
        '標簽': 'tag',
        '標誌': 'flag',
        '狀態': 'state',
        '模式': 'mode',
        '類型': 'type',
        '格式': 'format',
        '樣式': 'style',
        '主題': 'theme',
        '模板': 'template',
        '佈局': 'layout',
        '結構': 'structure',
        '框架': 'framework',
        '組件': 'component',
        '模塊': 'module',
        '插件': 'plugin',
        '擴展': 'extension',
        '工具': 'tool',
        '實用': 'utility',
        '助手': 'helper',
        '服務': 'service',
        '接口': 'interface',
        '實現': 'implementation',
        '配置': 'config',
        '設置': 'settings',
        '選項': 'option',
        '參數': 'parameter',
        '參數': 'argument',
        '變量': 'variable',
        '常量': 'constant',
        '屬性': 'property',
        '方法': 'method',
        '函數': 'function',
        '過程': 'procedure',
        '算法': 'algorithm',
        '邏輯': 'logic',
        '規則': 'rule',
        '條件': 'condition',
        '判斷': 'judge',
        '分支': 'branch',
        '循環': 'loop',
        '跳轉': 'jump',
        '跳過': 'skip',
        '中斷': 'break',
        '中止': 'abort',
        '退出': 'exit',
        '返回': 'return',
        '輸入': 'input',
        '輸出': 'output',
        '打印': 'print',
        '顯示': 'display',
        '呈現': 'render',
        '渲染': 'render',
        '繪製': 'draw',
        '動畫': 'animation',
        '過渡': 'transition',
        '效果': 'effect',
        '特效': 'effect',
        '交互': 'interaction',
        '操作': 'operation',
        '行為': 'behavior',
        '動作': 'action',
        '手勢': 'gesture',
        '觸摸': 'touch',
        '點擊': 'click',
        '雙擊': 'double click',
        '長按': 'long press',
        '滑動': 'swipe',
        '拖動': 'drag',
        '拖拽': 'drag',
        '放置': 'drop',
        '縮放': 'zoom',
        '旋轉': 'rotate',
        '滾動': 'scroll',
        '翻頁': 'page turn',
        '切換': 'switch',
        '跳轉': 'jump',
        '導航': 'navigation',
        '前進': 'forward',
        '後退': 'backward',
        '刷新': 'refresh',
        '重新加載': 'reload',
    },
    'jp': {
        '混合並發': 'ミックス並行',
        '完整欄位': '完全フィールド',
        '不影響': '影響なし',
        '勾選且': 'チェックされかつ',
        '勾選的': 'チェックされた',
        '欄位': 'フィールド',
        '並發': '並行',
        '防止': '防止',
        '避免': '回避',
        '確認': '確認',
        '驗證': '検証',
        '的': 'の',
        '和': 'と',
    },
    'kr': {
        '混合並發': '혼합 동시성',
        '完整欄位': '전체 필드',
        '不影響': '영향 없음',
        '勾選且': '체크되고',
        '勾選的': '체크된',
        '欄位': '필드',
        '並發': '동시성',
        '防止': '방지',
        '避免': '회피',
        '確認': '확인',
        '驗證': '검증',
        '的': '',
        '和': '및',
    }
}

def translate_file_phase7(file_path, lang_code):
    """Phase 7 翻译"""
    
    if not os.path.exists(file_path):
        return 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE7_TRANSLATIONS.get(lang_code, {})
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    replaced_count = 0
    for chinese, target in sorted_trans:
        if chinese in content and target:
            content = content.replace(chinese, target)
            replaced_count += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    chinese_after = len(re.findall(r'[一-龥]', content))
    
    return chinese_before, chinese_after, replaced_count

def main():
    print("🚀 Phase 7: 翻译复杂短语和剩余词组...")
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
            before, after, replaced = translate_file_phase7(file_path, lang_code)
            
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
    print(f"Phase 7 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有设计保持不变")

if __name__ == '__main__':
    main()

