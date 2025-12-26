#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复图片间距脚本
确保图片与图片之间有≥1000字的本地化内容
"""

import os
import re
from bs4 import BeautifulSoup
import glob

# 导入本地化内容库
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
    # 移除HTML标签
    text_only = re.sub(r'<[^>]+>', '', between_content)
    # 移除空白字符
    text_only = re.sub(r'\s+', '', text_only)
    return len(text_only)

def find_image_positions(html_content):
    """找到所有图片的位置"""
    img_pattern = r'<img[^>]*>'
    matches = list(re.finditer(img_pattern, html_content, re.IGNORECASE))
    return matches

def insert_content_between_images(html_content, language, page_type='bank'):
    """在图片之间插入本地化内容"""
    
    # 找到所有图片位置
    img_matches = find_image_positions(html_content)
    
    if len(img_matches) < 2:
        return html_content, 0  # 少于2张图片，无需处理
    
    insertions = []
    inserted_count = 0
    
    # 检查每对相邻图片
    for i in range(len(img_matches) - 1):
        img1 = img_matches[i]
        img2 = img_matches[i + 1]
        
        # 计算两张图片之间的文字数
        text_count = count_text_between_images(html_content, img1.end(), img2.start())
        
        # 如果文字少于1000字，插入内容
        if text_count < 1000:
            # 循环使用3种内容类型
            content_types = ['bank_case_study_1', 'bank_security', 'integration_guide']
            content_type = content_types[inserted_count % 3]
            
            # 获取本地化内容
            localized_content = get_localized_content(language, content_type)
            
            # 记录插入位置和内容
            insertions.append({
                'position': img1.end(),
                'content': localized_content
            })
            inserted_count += 1
    
    # 从后往前插入，避免位置偏移
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
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测语言
        language = detect_language_from_path(file_path)
        
        # 插入内容
        new_content, inserted_count = insert_content_between_images(content, language)
        
        if inserted_count > 0:
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, inserted_count
        else:
            return False, 0
            
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("🔧 自动修复Landing Page图片间距")
    print("=" * 70)
    print()
    
    # 要处理的文件模式
    patterns = [
        # 银行页面
        'ja/*-bank-statement.html',
        'ko/*-bank-statement.html',
        'kr/*-bank-statement.html',
        'en/*-bank-statement.html',
        '*-bank-statement.html',
        
        # 行业解决方案
        'ja/solutions/*/index.html',
        'ko/solutions/*/index.html',
        'kr/solutions/*/index.html',
        'en/solutions/*/index.html',
        'solutions/*/index.html',
        
        # 博客文章
        'ja/blog/*.html',
        'ko/blog/*.html',
        'kr/blog/*.html',
        'en/blog/*.html',
        'blog/*.html',
    ]
    
    all_files = []
    for pattern in patterns:
        all_files.extend(glob.glob(pattern))
    
    # 去重
    all_files = list(set(all_files))
    # 排除备份文件
    all_files = [f for f in all_files if 'backup' not in f and '.bak' not in f]
    
    print(f"📝 找到 {len(all_files)} 个文件待处理")
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
            # print(f"⏭️  [{i}/{len(all_files)}] {file_path} - 无需处理")
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
    
    if processed > 0:
        print("=" * 70)
        print("🎉 修复完成！")
        print("=" * 70)
        print()
        print("下一步：")
        print("1. 验证几个页面的显示效果")
        print("2. 确认内容本地化正确")
        print("3. 检查页面加载速度")
        print("4. 上传到服务器测试")
        print()

if __name__ == '__main__':
    main()

