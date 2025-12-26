#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复多语言银行页面背景图片位置"""

import glob
import re

def fix_bg_position(file_path):
    """修复背景图片位置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # ========== 1. 查找 promo-banner 的结束位置 ==========
        promo_pattern = r'(<div class="promo-banner">.*?</div>\s*)'
        promo_match = re.search(promo_pattern, content, re.DOTALL)
        
        if not promo_match:
            return False, ['未找到promo-banner']
        
        insert_pos = promo_match.end()
        
        # ========== 2. 检查是否已经有视觉背景图片 ==========
        after_promo = content[insert_pos:insert_pos+500]
        if '<!-- 视觉背景图片 -->' in after_promo or '<!-- Visual Background -->' in after_promo:
            return False, ['背景图片已在正确位置']
        
        # ========== 3. 查找并提取背景图片section ==========
        bg_pattern = r'<section class="hero">[\s\S]*?<img[^>]+class="hero-background"[^>]+>[\s\S]*?</section>'
        bg_match = re.search(bg_pattern, content)
        
        if not bg_match:
            return False, ['未找到背景图片section']
        
        bg_section = bg_match.group(0)
        bg_pos = bg_match.start()
        
        # 检查背景图片是否已经在promo之后
        if bg_pos < insert_pos + 100:  # 已经很接近promo了
            return False, ['背景图片已在正确位置']
        
        # ========== 4. 移除原位置的背景 ==========
        content = content[:bg_match.start()] + content[bg_match.end():]
        
        # ========== 5. 在promo后插入背景 ==========
        # 重新查找promo位置（因为content已改变）
        promo_match = re.search(promo_pattern, content, re.DOTALL)
        insert_pos = promo_match.end()
        
        # 根据语言选择注释
        if '/en/' in file_path:
            comment = '    <!-- Visual Background -->'
        elif '/ja/' in file_path:
            comment = '    <!-- ビジュアル背景 -->'
        elif '/kr/' in file_path:
            comment = '    <!-- 시각적 배경 -->'
        else:
            comment = '    <!-- 视觉背景图片 -->'
        
        content = (
            content[:insert_pos] +
            '\n\n' + comment + '\n' +
            '    ' + bg_section + '\n\n' +
            content[insert_pos:]
        )
        
        # ========== 保存 ==========
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, ['移动背景图片到顶部']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    'en/*-bank-statement.html',
    'ja/*-bank-statement.html',
    'kr/*-bank-statement.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 修复多语言银行页面背景位置")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个多语言银行页面")
print()

processed = 0
by_lang = {'en': 0, 'ja': 0, 'kr': 0}

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_bg_position(file_path)
    
    lang = 'en' if '/en/' in file_path else ('ja' if '/ja/' in file_path else 'kr')
    
    if success:
        processed += 1
        by_lang[lang] += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
    else:
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"   英文版：{by_lang['en']} 个")
print(f"   日文版：{by_lang['ja']} 个")
print(f"   韩文版：{by_lang['kr']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("🎉 完成！")

