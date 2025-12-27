#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复Hero Section的容器结构"""

import glob
import re

def fix_hero_container(file_path):
    """修复Hero Section的容器结构"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 查找并修复Hero Section结构 ==========
        # 查找Hero Section
        hero_pattern = r'(<section class="hero">[\s\S]*?<img[^>]+class="hero-background"[^>]*>\s*)'
        hero_match = re.search(hero_pattern, content)
        
        if not hero_match:
            return False, ['未找到Hero Section']
        
        hero_section_start = hero_match.group(0)
        hero_end_pos = hero_match.end()
        
        # 查找bank-logo到Hero Section结束的所有内容
        after_hero_bg = content[hero_end_pos:]
        
        # 检查是否有<div class="container hero-content">
        if '<div class="container hero-content">' not in after_hero_bg[:500]:
            # 没有container，需要添加
            
            # 查找bank-logo的位置
            bank_logo_pattern = r'(\s*<!-- 银行Logo占位 -->)'
            bank_logo_match = re.search(bank_logo_pattern, after_hero_bg)
            
            if bank_logo_match:
                # 在bank-logo前插入container开始标签
                insert_pos = hero_end_pos + bank_logo_match.start()
                content = (
                    content[:insert_pos] +
                    '\n        <div class="container hero-content">\n' +
                    content[insert_pos:]
                )
                changes.append('添加container hero-content开始标签')
        
        # ========== 2. 确保Hero Section有正确的结束标签 ==========
        # 重新查找内容（因为content已改变）
        # 查找"免費試用"按钮和trust badges后的位置
        hero_content_end_pattern = r'(<div class="trust-badges">[\s\S]*?</div>\s*</div>\s*<a[^>]*>立即免費試用[^<]*</a>[\s\S]*?</div>\s*)'
        hero_content_end_match = re.search(hero_content_end_pattern, content)
        
        if hero_content_end_match:
            insert_pos = hero_content_end_match.end()
            # 检查后面是否已经有</section>
            after_text = content[insert_pos:insert_pos+50]
            if '</section>' not in after_text[:30]:
                # 添加</section>标签
                content = content[:insert_pos] + '\n    </section>\n\n' + content[insert_pos:]
                changes.append('添加hero section结束标签')
        
        # ========== 保存 ==========
        if content != original:
            with open(file_path + '.backup_hero_v2', 'w', encoding='utf-8') as f:
                f.write(original)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, ['无需修改']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    'bochk-bank-statement.html',
    'hsbc-bank-statement.html',
    'hangseng-bank-statement.html',
    'dbs-bank-statement.html',
    'sc-bank-statement.html',
]

all_files = patterns

print("=" * 70)
print("🔧 修复Hero Section容器结构")
print("=" * 70)
print()
print(f"处理 {len(all_files)} 个文件")
print()

processed = 0

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_hero_container(file_path)
    
    if success:
        processed += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print(f"✅ 已处理：{processed}/{len(all_files)} 个文件")
print("🎉 完成！")

