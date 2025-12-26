#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重组银行页面结构：背景图片在顶部，案例在FAQ之后"""

import glob
import re

def reorganize_bank_page(file_path):
    """重组单个银行页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 查找并提取背景图片section ==========
        # 查找类似这样的section：
        # <section class="hero">
        #     <img src="..." alt="Banking Background" class="hero-background" ...>
        # </section>
        bg_pattern = r'<section class="hero">[\s\S]*?<img[^>]+class="hero-background"[^>]+>[\s\S]*?</section>'
        bg_match = re.search(bg_pattern, content)
        
        if bg_match:
            bg_section = bg_match.group(0)
            # 移除原位置的背景section
            content = content.replace(bg_section, '', 1)
            changes.append('移除背景图片')
        else:
            bg_section = None
        
        # ========== 2. 查找优惠横幅的位置，在其后插入背景图片 ==========
        if bg_section:
            # 查找优惠横幅
            promo_pattern = r'(<!-- 优惠横幅 -->[\s\S]*?</div>\s*)'
            promo_match = re.search(promo_pattern, content)
            
            if promo_match:
                insert_pos = promo_match.end()
                # 在优惠横幅后插入背景图片
                content = (
                    content[:insert_pos] +
                    '\n\n    <!-- 视觉背景图片 -->\n' +
                    '    ' + bg_section + '\n\n' +
                    content[insert_pos:]
                )
                changes.append('背景图片移到顶部')
        
        # ========== 3. 清理案例section周围的多余背景 ==========
        # 查找案例section前的空section或重复的hero section
        case_pattern = r'(<section[^>]*>\s*<div class="container">\s*<h2[^>]*>香港中小企業真實案例</h2>)'
        case_match = re.search(case_pattern, content)
        
        if case_match:
            # 检查案例section之前是否有多余的section标签
            before_case = content[:case_match.start()]
            # 查找最后一个section标签（可能是空的或只有图片的）
            last_section_pattern = r'<section[^>]*>\s*(?:<img[^>]*>)?\s*$'
            if re.search(last_section_pattern, before_case):
                # 有多余的section，移除它
                content = re.sub(last_section_pattern, '', before_case) + content[case_match.start():]
                changes.append('清理多余section')
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_reorg', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    '*-bank-statement.html',
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
print("🔧 重组银行页面结构")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个银行页面")
print()

processed = 0
by_lang = {'zh': 0, 'en': 0, 'ja': 0, 'kr': 0}

for i, file_path in enumerate(all_files, 1):
    success, changes = reorganize_bank_page(file_path)
    
    if success:
        processed += 1
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path:
            lang = 'kr'
        by_lang[lang] += 1
        
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   修改: {', '.join(changes)}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"   中文版：{by_lang['zh']} 个")
print(f"   英文版：{by_lang['en']} 个")
print(f"   日文版：{by_lang['ja']} 个")
print(f"   韩文版：{by_lang['kr']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 重组完成！")
print("=" * 70)
print()
print("新结构：")
print("  1. 优惠横幅")
print("  2. 视觉背景图片 ← 移到顶部")
print("  3. Hero内容")
print("  4. ... 其他内容 ...")
print("  5. FAQ")
print("  6. 香港中小企業真實案例 ← 保持在FAQ之后")

