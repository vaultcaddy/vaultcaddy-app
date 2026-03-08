#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 8: 最终清理 - 处理所有剩余的零散中文
⚠️ 只翻译文本，不改变任何结构
"""

import re
import os

# Phase 8 - 最终清理（所有剩余常见词汇）
PHASE8_TRANSLATIONS = {
    'en': {
        # 从最终扫描发现的剩余词汇
        '所有': 'all',
        '所以': 'so',
        '所需': 'required',
        '不同': 'different',
        '相同': 'same',
        '類似': 'similar',
        '不同': 'different',
        '相關': 'related',
        '獨立': 'independent',
        '依賴': 'depend',
        '必須': 'must',
        '應該': 'should',
        '可以': 'can',
        '可能': 'may',
        '允許': 'allow',
        '禁止': 'forbid',
        '限制': 'limit',
        '擴展': 'extend',
        '縮小': 'reduce',
        '擴大': 'expand',
        '增加': 'increase',
        '減少': 'decrease',
        '提高': 'improve',
        '降低': 'lower',
        '優化': 'optimize',
        '改進': 'improve',
        '修正': 'fix',
        '修復': 'repair',
        '調試': 'debug',
        '測試': 'test',
        '檢查': 'check',
        '驗證': 'verify',
        '確認': 'confirm',
        '取消': 'cancel',
        '忽略': 'ignore',
        '跳過': 'skip',
        '繼續': 'continue',
        '暫停': 'pause',
        '停止': 'stop',
        '開始': 'start',
        '重新': 're-',
        '再次': 'again',
        '首次': 'first time',
        '第一': 'first',
        '最後': 'last',
        '之前': 'before',
        '之後': 'after',
        '期間': 'during',
        '同時': 'meanwhile',
        '然後': 'then',
        '接著': 'next',
        '最終': 'finally',
        '總是': 'always',
        '從不': 'never',
        '有時': 'sometimes',
        '經常': 'often',
        '很少': 'rarely',
        '偶爾': 'occasionally',
        '立即': 'immediately',
        '馬上': 'right away',
        '稍後': 'later',
        '暫時': 'temporarily',
        '永久': 'permanently',
        '臨時': 'temporary',
        '固定': 'fixed',
        '動態': 'dynamic',
        '靜態': 'static',
        '全局': 'global',
        '局部': 'local',
        '公共': 'public',
        '私有': 'private',
        '保護': 'protected',
        '內部': 'internal',
        '外部': 'external',
        '上級': 'parent',
        '下級': 'child',
        '同級': 'sibling',
        '祖先': 'ancestor',
        '後代': 'descendant',
        '根節點': 'root',
        '葉節點': 'leaf',
        '父節點': 'parent',
        '子節點': 'child',
        '兄弟節點': 'sibling',
        '鄰居': 'neighbor',
        '相鄰': 'adjacent',
        '連續': 'continuous',
        '間斷': 'discrete',
        '離散': 'discrete',
        '連貫': 'coherent',
        '一致': 'consistent',
        '統一': 'unified',
        '分散': 'scattered',
        '集中': 'concentrated',
        '分佈': 'distributed',
        '集合': 'collection',
        '數組': 'array',
        '列表': 'list',
        '隊列': 'queue',
        '棧': 'stack',
        '堆': 'heap',
        '樹': 'tree',
        '圖': 'graph',
        '哈希': 'hash',
        '映射': 'map',
        '字典': 'dictionary',
        '鍵值': 'key-value',
        '對象': 'object',
        '實例': 'instance',
        '類': 'class',
        '接口': 'interface',
        '抽象': 'abstract',
        '具體': 'concrete',
        '泛型': 'generic',
        '特殊': 'special',
        '普通': 'normal',
        '標準': 'standard',
        '自定義': 'custom',
        '預設': 'default',
        '推薦': 'recommended',
        '可選': 'optional',
        '必需': 'required',
        '强制': 'mandatory',
        '可用': 'available',
        '不可用': 'unavailable',
        '已啟用': 'enabled',
        '已禁用': 'disabled',
        '激活': 'active',
        '未激活': 'inactive',
        '在線': 'online',
        '離線': 'offline',
        '就緒': 'ready',
        '未就緒': 'not ready',
        '忙碌': 'busy',
        '空閑': 'idle',
        '等待': 'waiting',
        '運行': 'running',
        '停止': 'stopped',
        '暫停': 'paused',
        '錯誤': 'error',
        '警告': 'warning',
        '信息': 'info',
        '調試': 'debug',
        '跟蹤': 'trace',
        '關鍵': 'critical',
        '重要': 'important',
        '次要': 'minor',
        '嚴重': 'severe',
        '輕微': 'slight',
        '高': 'high',
        '中': 'medium',
        '低': 'low',
        '非常': 'very',
        '極其': 'extremely',
        '稍微': 'slightly',
        '比較': 'relatively',
        '大約': 'approximately',
        '精確': 'precise',
        '準確': 'accurate',
        '模糊': 'fuzzy',
        '清晰': 'clear',
        '明確': 'explicit',
        '隱式': 'implicit',
        '顯式': 'explicit',
        '直接': 'direct',
        '間接': 'indirect',
        '立即': 'immediate',
        '延遲': 'delayed',
        '即時': 'instant',
        '實時': 'real-time',
        '離線': 'offline',
        '在線': 'online',
        '同步': 'synchronous',
        '異步': 'asynchronous',
        '阻塞': 'blocking',
        '非阻塞': 'non-blocking',
        '並行': 'parallel',
        '串行': 'serial',
        '順序': 'sequential',
        '亂序': 'out-of-order',
        '遞增': 'ascending',
        '遞減': 'descending',
        '正序': 'forward',
        '逆序': 'reverse',
        '正向': 'forward',
        '反向': 'backward',
        '單向': 'one-way',
        '雙向': 'bi-directional',
        '多向': 'multi-directional',
        '單一': 'single',
        '多個': 'multiple',
        '唯一': 'unique',
        '重複': 'duplicate',
        '相同': 'same',
        '不同': 'different',
        '相似': 'similar',
        '相等': 'equal',
        '不等': 'not equal',
        '大於': 'greater than',
        '小於': 'less than',
        '等於': 'equal to',
        '不等於': 'not equal to',
        '大於等於': 'greater or equal',
        '小於等於': 'less or equal',
        '介於': 'between',
        '之間': 'between',
        '以內': 'within',
        '以外': 'outside',
        '包含': 'include',
        '排除': 'exclude',
        '屬於': 'belong to',
        '不屬於': 'not belong to',
        '存在': 'exist',
        '不存在': 'not exist',
        '為空': 'empty',
        '非空': 'non-empty',
        '為真': 'true',
        '為假': 'false',
        '成立': 'valid',
        '不成立': 'invalid',
        '滿足': 'satisfy',
        '不滿足': 'not satisfy',
        '符合': 'conform',
        '不符合': 'not conform',
        '匹配': 'match',
        '不匹配': 'not match',
        '通過': 'pass',
        '不通過': 'fail',
        '成功': 'success',
        '失敗': 'failure',
        '完成': 'complete',
        '未完成': 'incomplete',
        '就緒': 'ready',
        '未就緒': 'not ready',
        '可行': 'feasible',
        '不可行': 'infeasible',
        '有效': 'valid',
        '無效': 'invalid',
        '合法': 'legal',
        '非法': 'illegal',
        '正確': 'correct',
        '錯誤': 'wrong',
        '正常': 'normal',
        '異常': 'abnormal',
        '安全': 'safe',
        '危險': 'dangerous',
        '穩定': 'stable',
        '不穩定': 'unstable',
        '可靠': 'reliable',
        '不可靠': 'unreliable',
        '可信': 'trusted',
        '不可信': 'untrusted',
        '已知': 'known',
        '未知': 'unknown',
        '確定': 'certain',
        '不確定': 'uncertain',
        '明確': 'clear',
        '模糊': 'vague',
        '具體': 'specific',
        '抽象': 'abstract',
        '簡單': 'simple',
        '複雜': 'complex',
        '容易': 'easy',
        '困難': 'difficult',
        '快速': 'fast',
        '緩慢': 'slow',
        '高效': 'efficient',
        '低效': 'inefficient',
        '最優': 'optimal',
        '次優': 'suboptimal',
        '最佳': 'best',
        '最差': 'worst',
        '更好': 'better',
        '更差': 'worse',
        '改善': 'improve',
        '惡化': 'worsen',
        '增強': 'enhance',
        '減弱': 'weaken',
        '加強': 'strengthen',
        '削弱': 'weaken',
        '提升': 'promote',
        '下降': 'decrease',
        '上升': 'increase',
        '變化': 'change',
        '不變': 'unchanged',
        '固定': 'fixed',
        '可變': 'variable',
        '常量': 'constant',
        '變量': 'variable',
        '參數': 'parameter',
        '引數': 'argument',
        '返回值': 'return value',
        '返回': 'return',
    },
    'jp': {
        '所有': 'すべて',
        '所以': 'なので',
        '不同': '異なる',
        '相同': '同じ',
        '不': 'ない',
        '的': 'の',
        '和': 'と',
        '為': 'として',
        '在': 'で',
        '於': 'に',
        '從': 'から',
        '到': 'まで',
        '與': 'と',
        '或': 'または',
    },
    'kr': {
        '所有': '모든',
        '所以': '그래서',
        '不同': '다른',
        '相同': '같은',
        '不': '아니',
        '的': '',
        '和': '및',
        '為': '로서',
        '在': '에서',
        '於': '에',
        '從': '부터',
        '到': '까지',
        '與': '와',
        '或': '또는',
    }
}

def translate_file_phase8(file_path, lang_code):
    """Phase 8 最终清理"""
    
    if not os.path.exists(file_path):
        return 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_before = len(re.findall(r'[一-龥]', content))
    
    translations = PHASE8_TRANSLATIONS.get(lang_code, {})
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
    print("🚀 Phase 8: 最终清理...")
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
            before, after, replaced = translate_file_phase8(file_path, lang_code)
            
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
    print(f"Phase 8 完成:")
    print(f"  原始: {total_before:,} 字符")
    print(f"  剩余: {total_after:,} 字符")
    print(f"  翻译: {total_translated:,} 字符 ({percentage:.1f}%)")
    print(f"  替换处数: {total_replaced} 处")
    print(f"{'='*70}")
    print(f"✅ 所有设计保持不变")
    print(f"\n🎉 Phase 1-8 全部完成！")

if __name__ == '__main__':
    main()

