#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第六阶段（彻底完成）：翻译所有剩余的console.log中的中文
"""

import re

def fix_en_index_phase6_complete():
    """彻底完成：翻译所有剩余的console.log"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 6 (Complete All): 翻译所有剩余console.log...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # 剩余的Console.log 翻译
    # ============================================
    print("🔄 翻译剩余的所有console.log...")
    
    remaining_console_translations = {
        # 用户相关
        '獲取用戶首字母': 'Get user initial',
        '優先使用 displayName 的第一個字母': 'Priority use first letter of displayName',
        '否則使用 email 的第一個字母': 'Otherwise use first letter of email',
        
        # 汉堡菜单相关
        '🔥 漢堡Menu功能（立即執行, 不等待 DOMContentLoaded）': '🔥 Hamburger menu function (execute immediately, no wait for DOMContentLoaded)',
        '🔵 初始化漢堡Menu...': '🔵 Initializing hamburger menu...',
        'Open側邊欄': 'Open sidebar',
        '🔵 openMobileSidebar 被調用': '🔵 openMobileSidebar called',
        '❌ 找不到側邊欄或遮罩元素': '❌ Cannot find sidebar or overlay elements',
        'Close側邊欄': 'Close sidebar',
        '🔵 closeMobileSidebar 被調用': '🔵 closeMobileSidebar called',
        '確保漢堡MenuButton綁定（多重綁定策略）': 'Ensure hamburger menu button binding (multiple binding strategy)',
        '✅ Found漢堡MenuButton, 開始綁定事件': '✅ Found hamburger menu button, start binding events',
        '創建統一的處理函數': 'Create unified handler function',
        '🔵 MenuButton被Trigger': '🔵 Menu button triggered',
        'Click 事件（滑鼠和一般觸摸）': 'Click event (mouse and general touch)',
        'Touchend 事件（iOS Safari 更可靠）': 'Touchend event (more reliable on iOS Safari)',
        '🔥 3. 只在MobileSettings可見（不影響Desktop）': '🔥 3. Only when mobile visible (does not affect desktop)',
        'Mobile：漢堡Menu已啟用': 'Mobile: Hamburger menu enabled',
        'Desktop：漢堡Menu保持Hide': 'Desktop: Hamburger menu stays hidden',
        '✅ 漢堡Menu功能已綁定（click + touchend）': '✅ Hamburger menu function bound (click + touchend)',
        '⚠️ 找不到漢堡MenuButton': '⚠️ Cannot find hamburger menu button',
        '👍 用戶Menu初始化調用成功': '👍 User menu initialization call successful',
        '❌ 用戶Menu初始化失敗': '❌ User menu initialization failed',
        '🔥 設置漢堡Menu和遮罩的Click處理器': '🔥 Set hamburger menu and overlay click handlers',
        '✅ 遮罩和側邊欄鏈接Click處理器已設置': '✅ Overlay and sidebar link click handlers set',
        '⚠️ 找不到遮罩或側邊欄': '⚠️ Cannot find overlay or sidebar',
        '🔥 手機版漢堡Menu多重檢查（確保不會失效）': '🔥 Mobile hamburger menu multiple checks (ensure no failure)',
        '✅ 第一次檢查：漢堡Menu已就緒': '✅ First check: Hamburger menu ready',
        '⏳ 第一次檢查：Menu未就緒, 將重試...': '⏳ First check: Menu not ready, will retry...',
        '✅ 第二次檢查：漢堡Menu已就緒': '✅ Second check: Hamburger menu ready',
        '⏳ 第二次檢查：Menu未就緒, 將重試...': '⏳ Second check: Menu not ready, will retry...',
        '✅ 第三次檢查：漢堡Menu已就緒': '✅ Third check: Hamburger menu ready',
        '❌ 第三次檢查失敗：漢堡Menu仍未就緒': '❌ Third check failed: Hamburger menu still not ready',
        
        # 更多通用翻译
        '被調用': 'called',
        '被Trigger': 'triggered',
        '已就緒': 'ready',
        '未就緒': 'not ready',
        '將重試': 'will retry',
        '重試': 'retry',
        '檢查': 'check',
        '確保': 'ensure',
        '處理器': 'handler',
        '處理函數': 'handler function',
        '綁定': 'bind',
        '已綁定': 'bound',
        '已設置': 'set',
        '啟用': 'enabled',
        '停用': 'disabled',
        '可見': 'visible',
        '隱藏': 'hidden',
        '保持': 'stay',
        '影響': 'affect',
        '不影響': 'does not affect',
        '找不到': 'cannot find',
        '找到': 'found',
        'Found': 'Found',
        '開始': 'start',
        '完成': 'complete',
        '成功': 'successful',
        '失敗': 'failed',
        '錯誤': 'error',
        '警告': 'warning',
        '信息': 'info',
        '調試': 'debug',
        '初始化': 'initialization',
        '調用': 'call',
        '功能': 'function',
        '事件': 'event',
        '元素': 'element',
        '按鈕': 'button',
        'Button': 'button',
        'Menu': 'menu',
        '側邊欄': 'sidebar',
        '遮罩': 'overlay',
        '鏈接': 'link',
        '用戶': 'user',
        '首字母': 'initial',
        '第一個': 'first',
        '字母': 'letter',
        '使用': 'use',
        '優先': 'priority',
        '否則': 'otherwise',
        '立即': 'immediately',
        '執行': 'execute',
        '等待': 'wait',
        '多重': 'multiple',
        '策略': 'strategy',
        '統一': 'unified',
        '創建': 'create',
        '設置': 'set',
        '確認': 'confirm',
        '檢測': 'detect',
        '監測': 'monitor',
        '只在': 'only when',
        '所有': 'all',
        '任何': 'any',
        '或': 'or',
        '和': 'and',
        '與': 'and',
        '的': '',  # 这个不翻译，直接删除
        '已': '',  # 这个不翻译，直接删除
        '了': '',  # 这个不翻译，直接删除
    }
    
    print(f"🔄 翻译 {len(remaining_console_translations)} 个剩余词组...")
    
    # 按长度排序，先替换长的，避免部分匹配
    sorted_translations = sorted(remaining_console_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        if english:  # 如果英文不为空
            content = content.replace(chinese, english)
        else:  # 如果英文为空，表示删除中文
            content = content.replace(chinese, '')
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 6 (Complete All) 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if chinese_chars_after > 50:
        print(f"⚠️  还有 {chinese_chars_after} 个中文字符")
        # 打印出剩余的中文内容
        print("\n📍 剩余中文内容（前20行）:")
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.strip().split('\n')
        for line in lines[:20]:
            print(f"  {line}")
        if len(lines) > 20:
            print(f"  ... 还有 {len(lines) - 20} 行")
        return chinese_chars_after
    elif chinese_chars_after > 0:
        print(f"✅ 几乎完成！剩余 {chinese_chars_after} 个字符（可能是不可避免的中文内容）")
        return chinese_chars_after
    else:
        print(f"🎉🎉🎉 完全完成！0个中文字符！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase6_complete()
    print(f"\n{'='*70}")
    if remaining > 50:
        print(f"⚠️  还需要继续处理 {remaining} 个中文字符")
    elif remaining > 0:
        print(f"✅✅✅ 英文版首页基本完成！剩余 {remaining} 个字符可能是必要的中文或注释")
    else:
        print(f"🎉🎉🎉 英文版首页100%完成！所有中文已翻译！")

