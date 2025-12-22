#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三阶段：翻译HTML注释、Alt标签、CSS注释中的中文
"""

import re

def fix_en_index_phase3():
    """修复HTML注释和Alt标签中的所有中文"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 3: 翻译HTML注释、Alt标签、CSS...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # HTML 注释翻译
    # ============================================
    print("🔄 翻译HTML注释...")
    
    html_comment_translations = {
        '價格區域': 'Pricing Section',
        '月付和年付並列顯示': 'Monthly and Annual plans displayed side by side',
        '月付方案': 'Monthly Plan',
        '🔥 標題和價格橫向排列': '🔥 Title and price horizontally arranged',
        'CTA 按鈕': 'CTA Button',
        '年付方案': 'Annual Plan',
        '客戶評價區域（BankGPT 風格）': 'Customer Reviews Section (BankGPT Style)',
        '標題': 'Title',
        '6張評價卡片 3x2 網格（桌面版）/ 輪播（手機版）': '6 review cards 3x2 grid (desktop) / carousel (mobile)',
        '評價卡片 1': 'Review Card 1',
        '評價卡片 2': 'Review Card 2',
        '評價卡片 3': 'Review Card 3',
        '評價卡片 4': 'Review Card 4',
        '評價卡片 5': 'Review Card 5',
        '評價卡片 6': 'Review Card 6',
        'SEO 文章引導區域': 'SEO Article Guide Section',
        '文章 1': 'Article 1',
        '文章 2': 'Article 2',
        'CTA 卡片': 'CTA Card',
        '頁尾': 'Footer',
        'Footer 內容': 'Footer Content',
        'Logo 和描述': 'Logo and Description',
        'Footer 底部': 'Footer Bottom',
        'Footer 鏈接 Hover 效果': 'Footer Link Hover Effect',
        '響應式設計': 'Responsive Design',
        '手机版Hero区域向上移动消除白色空白': 'Move Hero section up on mobile to eliminate white space',
        '導航欄': 'Navigation Bar',
        '顯示漢堡菜單按鈕': 'Show hamburger menu button',
        '手機版顯示 logo, 隱藏文字': 'Show logo on mobile, hide text',
        '✅ 顯示 V 圖標': '✅ Show V icon',
        '✅ 隱藏 "VaultCaddy" 文字': '✅ Hide "VaultCaddy" text',
        '隱藏導航欄中的文字鏈接': 'Hide text links in navigation bar',
        'User dropdown menu位置': 'User dropdown menu position',
        '💡 手機版：確保用戶菜單按鈕和頭像正確顯示': '💡 Mobile: Ensure user menu button and avatar display correctly',
        '🔥 通用：減少所有容器的左右內距': '🔥 General: Reduce left and right padding of all containers',
        '🔥 功能卡片內距優化': '🔥 Feature card padding optimization',
        '🔥 智能發票/銀行對賬單徽章置中（提高優先級）': '🔥 Center Smart Invoice/Bank Statement badges (increase priority)',
        '🔥 標題也置中（提高優先級）': '🔥 Center title too (increase priority)',
        '🔥 功能區內的所有 flex 容器間距減少': '🔥 Reduce spacing of all flex containers in feature section',
        '🔥 描述段落間距進一步減少（總共 30pt）': '🔥 Further reduce description paragraph spacing (total 30pt)',
    }
    
    for chinese, english in html_comment_translations.items():
        content = content.replace(chinese, english)
    
    # ============================================
    # Alt 标签翻译
    # ============================================
    print("🔄 翻译Alt标签...")
    
    alt_translations = {
        'VaultCaddy用戶John M. - 香港會計師 - 使用VaultCaddy處理銀行對帳單': 'VaultCaddy user John M. - Hong Kong Accountant - Using VaultCaddy for bank statement processing',
        'VaultCaddy用戶Sarah T. - 簿記員 - 推薦VaultCaddy銀行對帳單AI處理工具': 'VaultCaddy user Sarah T. - Bookkeeper - Recommends VaultCaddy AI bank statement processing tool',
        'VaultCaddy用戶David L. - 公司老闆 - VaultCaddy節省90%記帳時間': 'VaultCaddy user David L. - Business Owner - VaultCaddy saves 90% bookkeeping time',
        'VaultCaddy用戶Emily R. - 財務經理 - VaultCaddy QuickBooks整合專家': 'VaultCaddy user Emily R. - Finance Manager - VaultCaddy QuickBooks integration expert',
        'VaultCaddy用戶Michael K. - 自由工作者 - VaultCaddy低成本記帳解決方案': 'VaultCaddy user Michael K. - Freelancer - VaultCaddy low-cost bookkeeping solution',
        'VaultCaddy用戶Sophia W. - 小店老闆 - VaultCaddy自動化對帳單處理': 'VaultCaddy user Sophia W. - Small Shop Owner - VaultCaddy automated statement processing',
    }
    
    for chinese, english in alt_translations.items():
        content = content.replace(chinese, english)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 3 翻译进度:")
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
        print(f"🎉 Phase 3 完成！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase3()
    print(f"\n{'='*60}")
    if remaining > 0:
        print(f"🔄 需要Phase 4继续翻译...")
    else:
        print(f"✅ 所有HTML和Alt标签翻译完成！")

