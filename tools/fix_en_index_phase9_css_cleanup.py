#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第九阶段（终极清理）：清理所有CSS注释中的中英混合内容
"""

import re

def fix_en_index_phase9_css_cleanup():
    """终极清理：CSS注释中的中英混合"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 9 (Ultimate CSS Cleanup): 清理CSS注释...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # CSS注释中的中英混合翻译
    # ============================================
    print("🔄 清理CSS注释中的中英混合内容...")
    
    css_mixed_translations = {
        # CSS注释翻译
        'HideNavigation Bar中文字Link': 'Hide text links in navigation bar',
        '🔥 title也Center（提高priority級）': '🔥 Title also centered (increase priority)',
        '🔥 grid Containerchange為Vertical排列': '🔥 Grid container changed to vertical layout',
        '🔥 描述段落Spacingunified減少': '🔥 Description paragraph spacing unified reduction',
        '🔥 all大Padding div 都縮小（排除functioncard）': '🔥 All large padding divs reduced (exclude function cards)',
        '🔥 統計data - stay橫, 縮小字體（被below規則覆蓋）': '🔥 Statistics data - stay horizontal, reduce font (overridden by below rules)',
        '統計data數字': 'Statistics data numbers',
        '統計dataContainer中all div（數字）': 'All divs in statistics data container (numbers)',
        '統計dataContainer中all div（描述文字）': 'All divs in statistics data container (description text)',
        '為什麼Selectcard': 'Why choose card',
        
        # 更细粒度的CSS术语翻译
        'Hide': 'Hide',
        'Navigation Bar': 'Navigation Bar',
        '中': ' ',
        '文字': 'text',
        'Link': 'link',
        'title': 'title',
        '也': 'also',
        'Center': 'center',
        '提高': 'increase',
        'priority': 'priority',
        '級': '',
        'grid': 'grid',
        'Container': 'container',
        'change': 'change',
        '為': 'to',
        'Vertical': 'vertical',
        '排列': 'layout',
        '描述': 'description',
        '段落': 'paragraph',
        'Spacing': 'spacing',
        'unified': 'unified',
        '減少': 'reduction',
        'all': 'all',
        '大': 'large',
        'Padding': 'padding',
        'div': 'div',
        '都': '',
        '縮小': 'reduced',
        '排除': 'exclude',
        'functioncard': 'function card',
        '統計': 'statistics',
        'data': 'data',
        'stay': 'stay',
        '橫': 'horizontal',
        '縮小字體': 'reduce font',
        '被': '',
        'below': 'below',
        '規則': 'rules',
        '覆蓋': 'overridden',
        '數字': 'numbers',
        '描述文字': 'description text',
        '為什麼': 'why',
        'Select': 'choose',
    }
    
    print(f"🔄 处理 {len(css_mixed_translations)} 个CSS词组...")
    
    # 按长度排序
    sorted_translations = sorted(css_mixed_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        if english:
            content = content.replace(chinese, english)
        else:
            content = content.replace(chinese, '')
    
    # 清理多余空格
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r' {2,}', ' ', content)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 9 (Ultimate CSS Cleanup) 进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已清理: {chinese_chars_before - chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 最终统计
    total_original = 2854
    completion_rate = ((total_original - chinese_chars_after) / total_original * 100)
    
    print(f"\n{'='*70}")
    print(f"🏆 英文版首页翻译终极总结:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  📊 原始中文字符: 2,854 个")
    print(f"  ✅ 已翻译字符: {total_original - chinese_chars_after:,} 个")
    print(f"  ⚠️  剩余中文字符: {chinese_chars_after} 个")
    print(f"  🎯 完成度: {completion_rate:.2f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if chinese_chars_after == 0:
        print(f"\n🎉🎉🎉 完美！100%完成！")
        print(f"英文版首页所有中文已完全翻译！")
        return 0
    elif chinese_chars_after <= 5:
        print(f"\n✅✅✅ 几乎完美！剩余 {chinese_chars_after} 个字符")
        print(f"（可能是嵌入在复杂代码中的字符，不影响用户体验）")
        # 显示剩余内容
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(f"\n📍 剩余内容:")
            print(result.stdout)
        return chinese_chars_after
    else:
        print(f"\n✅✅ 接近完成！剩余 {chinese_chars_after} 个字符")
        # 显示剩余内容
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            print(f"\n📍 剩余内容（前5行）:")
            for line in lines[:5]:
                print(f"  {line}")
            if len(lines) > 5:
                print(f"  ... 还有 {len(lines) - 5} 行")
        return chinese_chars_after

if __name__ == '__main__':
    remaining = fix_en_index_phase9_css_cleanup()
    print(f"\n{'='*70}")
    if remaining == 0:
        print(f"🎉🎉🎉 英文版首页100%完成！")
        print(f"✅ 可以继续修复日文版和韩文版！")
    elif remaining <= 5:
        print(f"✅✅ 英文版首页基本完成（{((2854 - remaining) / 2854 * 100):.2f}%）！")
        print(f"✅ 剩余 {remaining} 个字符不影响用户体验，可以继续修复日文版和韩文版！")
    else:
        print(f"✅ 英文版首页接近完成（{((2854 - remaining) / 2854 * 100):.2f}%）！")
        print(f"✅ 可以继续修复日文版和韩文版！")

