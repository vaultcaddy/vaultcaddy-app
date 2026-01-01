#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户报告的4个页面问题
1. hsbc-bank-statement.html - 删除重复内容
2. ally-bank-statement-v2.html - 确保图标显示
3. chase-bank-statement-v3.html - Trust Badges背景改为白色
4. zh-HK/hsbc-bank-statement-v3.html - FAQ翻译为中文
"""

import os
import re

def fix_hsbc_original(filepath):
    """修复hsbc-bank-statement.html的重复内容"""
    print("\n修复 1/4: hsbc-bank-statement.html")
    print("=" * 80)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找重复的FAQ section
    # 保留第一个FAQ部分，删除后续重复的
    faq_sections = list(re.finditer(r'<!-- FAQ.*?-->.*?<section[^>]*class="faq"[^>]*>.*?</section>', content, re.DOTALL))
    
    if len(faq_sections) > 1:
        print(f"  找到 {len(faq_sections)} 个FAQ部分，保留第1个，删除其余{len(faq_sections)-1}个")
        # 从后往前删除，避免索引变化
        for i in range(len(faq_sections) - 1, 0, -1):
            start, end = faq_sections[i].span()
            content = content[:start] + content[end:]
        print("  ✅ 已删除重复的FAQ部分")
    else:
        print("  ℹ️ 未发现重复的FAQ部分")
    
    # 检查是否有其他重复的section
    # 查找重复的feature sections
    feature_sections = list(re.finditer(r'<!-- Features.*?-->.*?<section.*?</section>', content, re.DOTALL))
    if len(feature_sections) > 1:
        print(f"  找到 {len(feature_sections)} 个Features部分")
        # 这里只是统计，不删除，因为可能是不同的features section
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✅ 完成")

def fix_ally_v2_icons(filepath):
    """修复ally-bank-statement-v2.html的图标显示"""
    print("\n修复 2/4: ally-bank-statement-v2.html")
    print("=" * 80)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 确保Font Awesome已加载
    if 'font-awesome' in content or 'fontawesome' in content:
        print("  ✅ Font Awesome已加载")
    else:
        print("  ⚠️ Font Awesome未加载，正在添加...")
        # 在head中添加Font Awesome
        head_end = content.find('</head>')
        fa_link = '\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">\n'
        content = content[:head_end] + fa_link + content[head_end:]
        print("  ✅ 已添加Font Awesome链接")
    
    # 检查图标是否存在
    icon_count = len(re.findall(r'<i class="fas fa-', content))
    print(f"  找到 {icon_count} 个Font Awesome图标")
    
    # 如果图标数量少，添加更明显的图标样式
    if 'AI-Powered Recognition' in content:
        # 增加图标的可见性
        content = re.sub(
            r'(<i class="fas fa-robot"></i>)',
            r'<i class="fas fa-robot" style="font-size: 24px;"></i>',
            content
        )
        content = re.sub(
            r'(<i class="fas fa-bolt"></i>)',
            r'<i class="fas fa-bolt" style="font-size: 24px;"></i>',
            content
        )
        content = re.sub(
            r'(<i class="fas fa-file-export"></i>)',
            r'<i class="fas fa-file-export" style="font-size: 24px;"></i>',
            content
        )
        print("  ✅ 已增强图标显示样式")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✅ 完成")

def fix_chase_v3_trust_section(filepath):
    """修复chase-bank-statement-v3.html的Trust Badges部分背景"""
    print("\n修复 3/4: chase-bank-statement-v3.html")
    print("=" * 80)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找Trust & Security Section
    trust_section_match = re.search(
        r'<!-- Trust & Security Section.*?-->(.*?)</section>',
        content,
        re.DOTALL
    )
    
    if trust_section_match:
        trust_section = trust_section_match.group(0)
        
        # 确保section背景是白色
        if 'background: white' in trust_section or 'background:#ffffff' in trust_section or 'background: #ffffff' in trust_section:
            print("  ✅ Trust Badges背景已经是白色")
        else:
            # 修改背景为白色
            trust_section = re.sub(
                r'<section style="([^"]*?)">',
                lambda m: f'<section style="{m.group(1)}; background: #ffffff;">',
                trust_section
            )
            content = content.replace(trust_section_match.group(0), trust_section)
            print("  ✅ 已将Trust Badges背景改为白色")
        
        # 检查是否有黑色边框或分隔线
        if 'border-top' in trust_section and ('#0f172a' in trust_section or 'black' in trust_section or '#000' in trust_section):
            trust_section = re.sub(
                r'border-top:\s*[^;]*#0f172a[^;]*;',
                'border-top: none;',
                trust_section
            )
            trust_section = re.sub(
                r'border-top:\s*[^;]*black[^;]*;',
                'border-top: none;',
                trust_section
            )
            content = content.replace(trust_section_match.group(0), trust_section)
            print("  ✅ 已删除黑色边框")
    else:
        print("  ⚠️ 未找到Trust & Security Section")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✅ 完成")

def fix_hk_faq_english(filepath):
    """修复zh-HK/hsbc-bank-statement-v3.html的FAQ英文问题"""
    print("\n修复 4/4: zh-HK/hsbc-bank-statement-v3.html")
    print("=" * 80)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = {
        # FAQ描述
        'Everything you need to know about HSBC statement conversion': '關於滙豐銀行對帳單轉換的所有資訊',
        
        # FAQ问题
        'How accurate is VaultCaddy for HSBC statements?': 'VaultCaddy處理滙豐銀行對帳單的準確度如何？',
        'What HSBC account types are supported?': '支援哪些滙豐銀行帳戶類型？',
        'How do I export HSBC statements to QuickBooks?': '如何將滙豐銀行對帳單匯出到QuickBooks？',
        'Is my HSBC data secure with VaultCaddy?': '我的滙豐銀行數據在VaultCaddy中安全嗎？',
        'Can I batch process multiple HSBC statements?': '可以批量處理多個滙豐銀行對帳單嗎？',
        
        # FAQ答案中的英文片段
        'VaultCaddy達到98%以上的準確率 for HSBC statements 使用專門針對 HSBC 格式訓練的先進AI': 'VaultCaddy使用專門針對滙豐銀行格式訓練的先進AI，達到98%以上的準確率',
        'for HSBC statements': '處理滙豐銀行對帳單',
        'HSBC Total Checking, HSBC Savings, HSBC Business Complete Banking, HSBC Credit Cards (Sapphire, Freedom, Ink), HSBC Private Client accounts, and HSBC First Banking': '滙豐支票帳戶、滙豐儲蓄帳戶、滙豐商業帳戶、滙豐信用卡、滙豐優越理財帳戶、滙豐卓越理財帳戶',
        'HSBC account types': '滙豐銀行帳戶類型',
        'HSBC statement': '滙豐銀行對帳單',
        'simply select "QuickBooks (QBO)" as your export format': '只需選擇「QuickBooks (QBO)」作為匯出格式',
        'VaultCaddy生成格式正確的QBO文件': 'VaultCaddy會生成格式正確的QBO文件',
    }
    
    fixed_count = 0
    for old_text, new_text in replacements.items():
        if old_text in content:
            content = content.replace(old_text, new_text)
            fixed_count += 1
    
    print(f"  ✅ 已翻译 {fixed_count} 个英文文本")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✅ 完成")

def main():
    print("\n🔧 开始修复4个页面的问题")
    print("=" * 80)
    
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    # 1. 修复hsbc-bank-statement.html
    fix_hsbc_original(os.path.join(base_dir, 'hsbc-bank-statement.html'))
    
    # 2. 修复ally-bank-statement-v2.html
    fix_ally_v2_icons(os.path.join(base_dir, 'ally-bank-statement-v2.html'))
    
    # 3. 修复chase-bank-statement-v3.html
    fix_chase_v3_trust_section(os.path.join(base_dir, 'chase-bank-statement-v3.html'))
    
    # 4. 修复zh-HK/hsbc-bank-statement-v3.html
    fix_hk_faq_english(os.path.join(base_dir, 'zh-HK/hsbc-bank-statement-v3.html'))
    
    print("\n" + "=" * 80)
    print("🎉 所有4个页面问题已修复完成！")
    print("=" * 80)
    print("\n请刷新浏览器查看修复效果！")

if __name__ == '__main__':
    main()

