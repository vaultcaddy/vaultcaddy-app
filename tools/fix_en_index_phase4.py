#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第四阶段：翻译CSS注释和剩余的JavaScript注释中的中文
"""

import re

def fix_en_index_phase4():
    """修复CSS注释中的所有中文"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 4: 翻译CSS注释和剩余内容...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # CSS 注释翻译
    # ============================================
    print("🔄 翻译CSS注释...")
    
    css_comment_translations = {
        # 响应式相关
        '總共上移 60pt': 'Total move up 60pt',
        '內層容器': 'Inner container',
        '文字大小適配': 'Text size adaptation',
        '✅ PRICING - 使用真實版設計（顯示詳細功能列表）': '✅ PRICING - Use real version design (display detailed feature list)',
        '🔥 定價區塊：手機版改為單列, 卡片居中': '🔥 Pricing section: Change to single column on mobile, center cards',
        '🔥 卡片間距減少': '🔥 Card spacing reduced',
        '🔥 定價卡片：收窄並居中, 減少內距': '🔥 Pricing cards: Narrow and center, reduce padding',
        '🔥 內距減少': '🔥 Padding reduced',
        '🔥 定價卡片': '🔥 Pricing card',
        '🔥 Title and price horizontally arranged區域': '🔥 Title and price horizontally arranged area',
        '🔥 定價卡片Title': '🔥 Pricing card title',
        '🔥 價格數字': '🔥 Price number',
        '🔥 功能列表容器': '🔥 Feature list container',
        "🔥 What's IncludedTitle - 放大到Title大小": "🔥 What's Included Title - Enlarge to title size",
        '🔥 功能列表：改為 2 列布局': '🔥 Feature list: Change to 2-column layout',
        '🔥 功能列表項目 - 放大到Title大小': '🔥 Feature list item - Enlarge to title size',
        '🔥 功能列表勾選圖標 - 放大': '🔥 Feature list checkmark icon - Enlarge',
        '🔥 CTA Button': '🔥 CTA Button',
        '🔥 CTA Button：減少內距': '🔥 CTA Button: Reduce padding',
        '🔥 Save 20% 標籤：放大到Title大小': '🔥 Save 20% label: Enlarge to title size',
        '🔥 放大到Title大小': '🔥 Enlarge to title size',
        '✅ TESTIMONIALS - 使用真實版設計（Sarah T. 有邊框）': '✅ TESTIMONIALS - Use real version design (Sarah T. has border)',
        '✅ FEATURES - 使用真實版設計（已在 HTML 中有打勾圖標, 不需要 ::before）': '✅ FEATURES - Use real version design (checkmark icon already in HTML, no need for ::before)',
        '🔥 再減半（從 0.35rem → 0.175rem）': '🔥 Reduce by half again (from 0.35rem → 0.175rem)',
        '🔥 功能文字段落間空白再減半（從 0.5rem → 0.25rem）': '🔥 Feature text paragraph spacing reduce by half again (from 0.5rem → 0.25rem)',
        '🔥 功能Title下方間距再減半': '🔥 Feature title bottom margin reduce by half again',
        '🔥 功能徽章下方間距再減半': '🔥 Feature badge bottom margin reduce by half again',
        '🔥 價值卡片（Ultra-Fast Processing/超高準確率/性價比最高）- 強制收窄底部空白': '🔥 Value cards (Ultra-Fast Processing/Highest Accuracy/Best Cost Performance) - Force narrow bottom spacing',
        '🔥 進一步縮小': '🔥 Further reduce',
        '🔥 價值卡片Title間距': '🔥 Value card title spacing',
        '🔥 價值卡片圖標容器間距': '🔥 Value card icon container spacing',
        '🔥 價值卡片描述最後一行底部間距移除': '🔥 Value card description last line bottom margin removed',
        '🔥 Hero 區域：信任標籤置中': '🔥 Hero section: Center trust label',
        '🔥 Hero 區域：副Title分行顯示': '🔥 Hero section: Subtitle line break display',
        '🔥 CTA Button向上移 10pt': '🔥 CTA Button move up 10pt',
        '🔥 統計數據向上移 20pt': '🔥 Statistics move up 20pt',
        '🔥 確保藍色標籤保持圓角膠囊形狀': '🔥 Ensure blue label maintains rounded pill shape',
        '圓角膠囊': 'Rounded pill',
        '🔥 確保圓形圖標容器顯示（圖3/4 - 超高準確率等圖標）': '🔥 Ensure round icon container displays (Figure 3/4 - Highest Accuracy icons etc.)',
        '🔥 確保圖標內的 Font Awesome 圖標顯示': '🔥 Ensure Font Awesome icons inside icon display',
        '🔥 手機版啟用動畫特效（與電腦版相同）': '🔥 Enable animation effects on mobile (same as desktop)',
        '移除了強制立即顯示的規則, 讓 Intersection Observer 自然觸發動畫': 'Removed forced immediate display rules, let Intersection Observer naturally trigger animations',
        '小屏幕手機優化 (iPhone SE 等)': 'Small screen mobile optimization (iPhone SE etc.)',
        
        # JavaScript相关
        '數字滾動動畫腳本': 'Number scrolling animation script',
        '數字滾動動畫函數': 'Number scrolling animation function',
        '使用 easeOutQuart 緩動函數': 'Use easeOutQuart easing function',
        '頁面加載後啟動數字動畫': 'Start number animation after page load',
        '延遲 300ms 開始動畫': 'Delay 300ms before starting animation',
        '🔥 漢堡菜單超級簡單修復方案': '🔥 Hamburger menu super simple fix',
        
        # 更多通用翻译
        '圖標': 'Icon',
        '容器': 'Container',
        '標題': 'Title',
        '副標題': 'Subtitle',
        '按鈕': 'Button',
        '卡片': 'Card',
        '區域': 'Section',
        '列表': 'List',
        '項目': 'Item',
        '內容': 'Content',
        '間距': 'Spacing',
        '邊距': 'Margin',
        '內距': 'Padding',
        '寬度': 'Width',
        '高度': 'Height',
        '顏色': 'Color',
        '背景': 'Background',
        '邊框': 'Border',
        '陰影': 'Shadow',
        '動畫': 'Animation',
        '過渡': 'Transition',
        '效果': 'Effect',
        '樣式': 'Style',
        '布局': 'Layout',
        '對齊': 'Alignment',
        '置中': 'Center',
        '左對齊': 'Left align',
        '右對齊': 'Right align',
        '水平': 'Horizontal',
        '垂直': 'Vertical',
        '隱藏': 'Hide',
        '顯示': 'Show',
        '收起': 'Collapse',
        '展開': 'Expand',
        '切換': 'Toggle',
        '滾動': 'Scroll',
        '點擊': 'Click',
        '懸停': 'Hover',
        '焦點': 'Focus',
        '載入': 'Load',
        '延遲': 'Delay',
        '觸發': 'Trigger',
        '監聽': 'Listen',
        '響應式': 'Responsive',
        '手機版': 'Mobile',
        '桌面版': 'Desktop',
        '平板': 'Tablet',
        '小屏幕': 'Small screen',
        '大屏幕': 'Large screen',
        '優化': 'Optimization',
        '性能': 'Performance',
        '加載': 'Loading',
        '緩存': 'Cache',
        '壓縮': 'Compression',
        '最小化': 'Minimize',
        '最大化': 'Maximize',
        '全屏': 'Fullscreen',
        '窗口': 'Window',
        '彈窗': 'Popup',
        '提示': 'Tooltip',
        '通知': 'Notification',
        '警告': 'Alert',
        '錯誤': 'Error',
        '成功': 'Success',
        '信息': 'Info',
        '調試': 'Debug',
        '日誌': 'Log',
        '輸出': 'Output',
        '輸入': 'Input',
        '表單': 'Form',
        '字段': 'Field',
        '驗證': 'Validation',
        '提交': 'Submit',
        '重置': 'Reset',
        '搜索': 'Search',
        '篩選': 'Filter',
        '排序': 'Sort',
        '分頁': 'Pagination',
        '跳轉': 'Jump',
        '鏈接': 'Link',
        '路由': 'Route',
        '導航': 'Navigation',
        '菜單': 'Menu',
        '子菜單': 'Submenu',
        '下拉': 'Dropdown',
        '選項': 'Option',
        '選擇': 'Select',
        '複選': 'Checkbox',
        '單選': 'Radio',
        '開關': 'Switch',
        '滑塊': 'Slider',
        '進度': 'Progress',
        '加載中': 'Loading',
        '完成': 'Complete',
        '失敗': 'Failed',
        '成功': 'Success',
        '取消': 'Cancel',
        '確認': 'Confirm',
        '關閉': 'Close',
        '打開': 'Open',
        '保存': 'Save',
        '刪除': 'Delete',
        '編輯': 'Edit',
        '新增': 'Add',
        '更新': 'Update',
        '刷新': 'Refresh',
        '返回': 'Back',
        '前進': 'Forward',
        '上一步': 'Previous',
        '下一步': 'Next',
        '首頁': 'Home',
        '末頁': 'Last',
        '跳過': 'Skip',
        '繼續': 'Continue',
        '暫停': 'Pause',
        '播放': 'Play',
        '停止': 'Stop',
        '重播': 'Replay',
        '分享': 'Share',
        '收藏': 'Favorite',
        '點讚': 'Like',
        '評論': 'Comment',
        '轉發': 'Forward',
        '舉報': 'Report',
        '屏蔽': 'Block',
        '關注': 'Follow',
        '取消關注': 'Unfollow',
        '訂閱': 'Subscribe',
        '取消訂閱': 'Unsubscribe',
        '登入': 'Login',
        '登出': 'Logout',
        '註冊': 'Register',
        '找回密碼': 'Recover Password',
        '修改密碼': 'Change Password',
        '個人中心': 'Profile',
        '設置': 'Settings',
        '幫助': 'Help',
        '反饋': 'Feedback',
        '關於': 'About',
        '版本': 'Version',
        '更新日誌': 'Changelog',
        '使用條款': 'Terms of Service',
        '隱私政策': 'Privacy Policy',
        '聯繫我們': 'Contact Us',
        '客服': 'Customer Service',
        '支持': 'Support',
        '常見問題': 'FAQ',
        '教程': 'Tutorial',
        '指南': 'Guide',
        '文檔': 'Documentation',
        '演示': 'Demo',
        '下載': 'Download',
        '上傳': 'Upload',
        '導出': 'Export',
        '導入': 'Import',
        '打印': 'Print',
        '複製': 'Copy',
        '粘貼': 'Paste',
        '剪切': 'Cut',
        '撤銷': 'Undo',
        '重做': 'Redo',
        '全選': 'Select All',
        '清空': 'Clear',
        '刷新': 'Refresh',
    }
    
    print(f"🔄 翻译 {len(css_comment_translations)} 个CSS和JavaScript词组...")
    
    # 按长度排序，先替换长的，避免部分匹配
    sorted_translations = sorted(css_comment_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        content = content.replace(chinese, english)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 4 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if chinese_chars_after > 0:
        print(f"⚠️  还需要继续翻译剩余的 {chinese_chars_after} 个中文字符")
        return chinese_chars_after
    else:
        print(f"🎉 Phase 4 完成！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase4()
    print(f"\n{'='*60}")
    if remaining > 0:
        print(f"🔄 需要Phase 5继续翻译...")
    else:
        print(f"✅ 所有CSS注释翻译完成！")

