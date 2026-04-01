#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第七阶段（最终清理）：处理所有剩余的中英混合内容
"""

import re

def fix_en_index_phase7_final_cleanup():
    """最终清理：处理所有剩余的中英混合内容"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 7 (Final Cleanup): 最终清理所有中文...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # 最后的中英混合内容翻译
    # ============================================
    print("🔄 最终清理所有中英混合内容...")
    
    final_cleanup_translations = {
        # Console.log中的中英混合
        'cannot find漢堡menubutton': 'cannot find hamburger menu button',
        'Mobile自動輪播（僅在Mobileenabled）': 'Mobile auto carousel (only when mobile enabled)',
        '評價輪播': 'Reviews carousel',
        '每4sToggle': 'Toggle every 4s',
        'Learning Center輪播': 'Learning Center carousel',
        '每5sToggle': 'Toggle every 5s',
        '🔥 即時從 SimpleDataManager 獲取最新 Credits': '🔥 Get latest credits from SimpleDataManager immediately',
        '✅ 即時獲取 Credits': '✅ Immediately get credits',
        '❌ 無法獲取 Credits': '❌ Cannot get credits',
        '🔍 Found': '🔍 Found',
        '個示例Card': ' demo cards',
        '✅ Card': '✅ Card',
        '上移 20pt': 'move up 20pt',
        '✅ MobileStyle強制應用': '✅ Mobile style force applied',
        'Window大小改變時重新check': 'Re-check when window size changes',
        
        # HTML注释中的中英混合
        '主要ContentSection': 'Main Content Section',
        '🎨 全新 Hero Section': '🎨 Brand new Hero Section',
        '动态Background装饰': 'Dynamic background decoration',
        'Background裝飾': 'Background decoration',
        '主Title': 'Main title',
        '信任標籤（移到Title下方）': 'Trust label (moved below title)',
        '副Title': 'Subtitle',
        
        # 更多细节翻译
        '漢堡': 'hamburger',
        '輪播': 'carousel',
        '僅在': 'only when',
        'enabled': 'enabled',
        '即時': 'immediately',
        '獲取': 'get',
        '無法': 'cannot',
        '示例': 'demo',
        'Card': 'card',
        '上移': 'move up',
        'Style': 'style',
        '強制': 'force',
        '應用': 'applied',
        '大小': 'size',
        '改變': 'change',
        '時': 'when',
        '重新': 're-',
        'check': 'check',
        '主要': 'main',
        'Content': 'content',
        'Section': 'section',
        '全新': 'brand new',
        'Hero': 'hero',
        '动态': 'dynamic',
        'Background': 'background',
        '装饰': 'decoration',
        '裝飾': 'decoration',
        'Title': 'title',
        '主': 'main',
        '信任': 'trust',
        '標籤': 'label',
        '移到': 'moved to',
        '下方': 'below',
        '副': 'sub',
        
        # 数字和单位
        's': 's',
        'pt': 'pt',
        '每': 'every',
        '個': '',  # 空字符串，表示删除
    }
    
    print(f"🔄 处理 {len(final_cleanup_translations)} 个最终词组...")
    
    # 按长度排序，先替换长的
    sorted_translations = sorted(final_cleanup_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        if english:
            content = content.replace(chinese, english)
        else:
            content = content.replace(chinese, '')
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 7 (Final Cleanup) 进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已清理: {chinese_chars_before - chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if chinese_chars_after > 20:
        print(f"⚠️  还有 {chinese_chars_after} 个中文字符")
        # 打印剩余内容
        print("\n📍 剩余中文内容:")
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.strip().split('\n')
        for line in lines[:10]:
            print(f"  {line}")
        if len(lines) > 10:
            print(f"  ... 还有 {len(lines) - 10} 行")
        return chinese_chars_after
    elif chinese_chars_after > 0:
        print(f"✅✅✅ 几乎完美！剩余 {chinese_chars_after} 个字符（可能是必要的或嵌入在代码中的）")
        # 显示剩余内容
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        print("\n📍 剩余的 {chinese_chars_after} 个字符位置:")
        print(result.stdout)
        return chinese_chars_after
    else:
        print(f"🎉🎉🎉 完美！0个中文字符！英文版首页100%完成！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase7_final_cleanup()
    print(f"\n{'='*70}")
    print(f"\n📊 英文版首页翻译总结:")
    print(f"  原始中文字符: 2,854 个")
    if remaining == 0:
        print(f"  剩余中文字符: 0 个")
        print(f"  完成度: 100% ✅✅✅")
        print(f"\n🎉🎉🎉 英文版首页完美完成！所有中文已翻译！")
    elif remaining <= 20:
        print(f"  剩余中文字符: {remaining} 个")
        print(f"  完成度: {((2854 - remaining) / 2854 * 100):.1f}% ✅✅")
        print(f"\n✅✅ 英文版首页几乎完成！剩余少量字符可能是必要的中文或不影响显示")
    else:
        print(f"  剩余中文字符: {remaining} 个")
        print(f"  完成度: {((2854 - remaining) / 2854 * 100):.1f}% ✅")

