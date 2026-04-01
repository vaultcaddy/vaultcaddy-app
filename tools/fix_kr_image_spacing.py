#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修复kr/目录的图片间距
"""

import os
import re
import glob
from localized_content_library import get_localized_content

def count_text_between_images(html_content, img1_pos, img2_pos):
    """计算两张图片之间的文字数量"""
    between_content = html_content[img1_pos:img2_pos]
    text_only = re.sub(r'<[^>]+>', '', between_content)
    text_only = re.sub(r'\s+', '', text_only)
    return len(text_only)

def find_image_positions(html_content):
    """找到所有图片的位置"""
    img_pattern = r'<img[^>]*>'
    matches = list(re.finditer(img_pattern, html_content, re.IGNORECASE))
    return matches

def insert_content_between_images(html_content):
    """在图片之间插入韩国本地化内容"""
    img_matches = find_image_positions(html_content)
    
    if len(img_matches) < 2:
        return html_content, 0
    
    insertions = []
    inserted_count = 0
    
    for i in range(len(img_matches) - 1):
        img1 = img_matches[i]
        img2 = img_matches[i + 1]
        
        text_count = count_text_between_images(html_content, img1.end(), img2.start())
        
        if text_count < 1000:
            # 循环使用3种韩国本地化内容
            content_types = ['bank_case_study_1', 'bank_security', 'integration_guide']
            content_type = content_types[inserted_count % 3]
            
            # 获取韩国本地化内容
            localized_content = get_localized_content('ko', content_type)
            
            insertions.append({
                'position': img1.end(),
                'content': localized_content
            })
            inserted_count += 1
    
    # 从后往前插入
    insertions.reverse()
    for insertion in insertions:
        html_content = (
            html_content[:insertion['position']] + 
            '\n' + insertion['content'] + '\n' + 
            html_content[insertion['position']:]
        )
    
    return html_content, inserted_count

def process_file(file_path):
    """处理单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, inserted_count = insert_content_between_images(content)
        
        if inserted_count > 0:
            # 创建备份
            backup_path = file_path + '.backup_kr_spacing'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入新内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, inserted_count
        else:
            return False, 0
            
    except Exception as e:
        return False, str(e)

# 获取所有kr/目录的文件
patterns = [
    'kr/*-bank-statement.html',
    'kr/solutions/*/index.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))

print("=" * 70)
print("🔧 修复kr/目录图片间距")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个文件待处理")
print()

processed = 0
skipped = 0
errors = 0
total_insertions = 0

for i, file_path in enumerate(all_files, 1):
    success, result = process_file(file_path)
    
    if success:
        processed += 1
        total_insertions += result
        print(f"✅ [{i}/{len(all_files)}] {file_path} - 插入 {result} 段内容")
    elif result == 0:
        skipped += 1
    else:
        errors += 1
        print(f"❌ [{i}/{len(all_files)}] {file_path} - 错误: {result}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"📝 插入内容：{total_insertions} 段")
print(f"⏭️  无需处理：{skipped} 个文件")
print(f"❌ 错误：{errors} 个文件")
print()
print("=" * 70)
print("🎉 kr/目录图片间距修复完成！")
print("=" * 70)

