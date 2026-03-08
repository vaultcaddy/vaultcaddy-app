#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第八阶段（绝对最终）：翻译所有剩余的HTML注释中的繁体中文
"""

import re

def fix_en_index_phase8_absolute_final():
    """绝对最终：翻译所有剩余的HTML注释"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 8 (Absolute Final): 翻译最后的HTML注释...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符（最后的！）")
    
    # ============================================
    # 最后的HTML注释翻译
    # ============================================
    print("🔄 翻译最后的HTML注释...")
    
    absolute_final_translations = {
        # CTA和数据相关
        'CTA button組（向move up10pt）': 'CTA button group (move up 10pt)',
        '關鍵數據': 'Key data',
        
        # 功能展示相关
        '🎨 核心function展示section': '🎨 Core function showcase section',
        'function組1：Smart Invoice & Receipt Processing': 'Function group 1: Smart Invoice & Receipt Processing',
        '模擬發票 - 茶餐廳（直接复制银行card代码, 只改内容）': 'Mock invoice - Tea restaurant (directly copy bank card code, only change content)',
        'AI 處理label': 'AI processing label',
        'function組2：銀行月結單分析': 'Function group 2: Bank statement analysis',
        '模擬銀行對賬單圖示': 'Mock bank statement illustration',
        '價值main張card': 'Value main cards',
        
        # 更细粒度的翻译
        'button組': 'button group',
        '向': '',  # 删除
        'move up': 'move up',
        '10pt': '10pt',
        '關鍵': 'key',
        '數據': 'data',
        '核心': 'core',
        'function': 'function',
        '展示': 'showcase',
        'section': 'section',
        'function組': 'function group',
        '模擬': 'mock',
        '發票': 'invoice',
        '茶餐廳': 'tea restaurant',
        '直接': 'directly',
        '复制': 'copy',
        '銀行': 'bank',
        'card': 'card',
        '代码': 'code',
        '只': 'only',
        '改': 'change',
        '内容': 'content',
        'AI': 'AI',
        '處理': 'processing',
        'label': 'label',
        '月結單': 'statement',
        '分析': 'analysis',
        '對賬單': 'statement',
        '圖示': 'illustration',
        '價值': 'value',
        'main': 'main',
        '張': '',  # 删除
    }
    
    print(f"🔄 处理 {len(absolute_final_translations)} 个最终HTML注释...")
    
    # 按长度排序
    sorted_translations = sorted(absolute_final_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        if english:
            content = content.replace(chinese, english)
        else:
            content = content.replace(chinese, '')
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 8 (Absolute Final) 进度:")
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
    print(f"📊 英文版首页翻译最终总结:")
    print(f"  原始中文字符数: {total_original} 个")
    print(f"  剩余中文字符数: {chinese_chars_after} 个")
    print(f"  翻译字符数: {total_original - chinese_chars_after} 个")
    print(f"  完成度: {completion_rate:.1f}%")
    
    if chinese_chars_after == 0:
        print(f"\n🎉🎉🎉 完美！100%完成！英文版首页所有中文已翻译！")
        return 0
    elif chinese_chars_after <= 10:
        print(f"\n✅✅✅ 几乎完美！剩余 {chinese_chars_after} 个字符")
        print(f"（这些可能是嵌入在代码中或必要的中文内容）")
        # 显示剩余内容
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(f"\n📍 剩余内容位置:")
            print(result.stdout)
        return chinese_chars_after
    else:
        print(f"\n✅✅ 接近完成！剩余 {chinese_chars_after} 个字符")
        # 显示前10行剩余内容
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            print(f"\n📍 剩余内容（前10行）:")
            for line in lines[:10]:
                print(f"  {line}")
            if len(lines) > 10:
                print(f"  ... 还有 {len(lines) - 10} 行")
        return chinese_chars_after

if __name__ == '__main__':
    remaining = fix_en_index_phase8_absolute_final()
    print(f"\n{'='*70}")
    if remaining == 0:
        print(f"🎉🎉🎉 英文版首页翻译100%完成！可以继续修复日文和韩文版！")
    elif remaining <= 10:
        print(f"✅✅ 英文版首页基本完成！可以继续修复日文和韩文版！")
    else:
        print(f"✅ 英文版首页大部分完成（{((2854 - remaining) / 2854 * 100):.1f}%）")

