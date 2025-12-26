#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试版本 - 只处理3个文件
"""

import os
import re
from localized_content_library import get_localized_content

def detect_language_from_path(file_path):
    """从文件路径检测语言"""
    if '/ja/' in file_path or file_path.startswith('ja/'):
        return 'ja'
    elif '/ko/' in file_path or '/kr/' in file_path or file_path.startswith('kr/') or file_path.startswith('ko/'):
        return 'ko'
    elif '/en/' in file_path or file_path.startswith('en/'):
        return 'en'
    else:
        return 'zh'

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

def insert_content_between_images(html_content, language):
    """在图片之间插入本地化内容"""
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
            content_types = ['bank_case_study_1', 'bank_security', 'integration_guide']
            content_type = content_types[inserted_count % 3]
            localized_content = get_localized_content(language, content_type)
            
            insertions.append({
                'position': img1.end(),
                'content': localized_content
            })
            inserted_count += 1
    
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
        
        language = detect_language_from_path(file_path)
        new_content, inserted_count = insert_content_between_images(content, language)
        
        if inserted_count > 0:
            # 创建备份
            backup_path = file_path + '.backup_before_image_spacing'
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

# 测试3个文件
test_files = [
    'ja/hsbc-bank-statement.html',
    'kr/hsbc-bank-statement.html',
    'en/hsbc-bank-statement.html'
]

print("=" * 70)
print("🧪 测试模式 - 处理3个文件")
print("=" * 70)
print()

for file_path in test_files:
    if os.path.exists(file_path):
        success, result = process_file(file_path)
        if success:
            print(f"✅ {file_path} - 插入 {result} 段内容")
        else:
            print(f"❌ {file_path} - 错误: {result}")
    else:
        print(f"⏭️  {file_path} - 文件不存在")

print()
print("✅ 测试完成！请验证这3个文件的显示效果")

