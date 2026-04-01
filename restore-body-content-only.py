#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只恢复body内容（导航栏、banner、页面设计），保留SEO标签
"""

import re
from pathlib import Path

def extract_body_content(html_content):
    """提取<body>...</body>之间的内容"""
    pattern = r'<body[^>]*>(.*?)</body>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def replace_body_content(current_html, backup_body_content):
    """替换当前HTML的body内容，保留head中的SEO标签"""
    # 提取当前的head部分
    head_pattern = r'(<head>.*?</head>)'
    head_match = re.search(head_pattern, current_html, re.DOTALL)
    
    if not head_match:
        print("  ❌ 无法找到<head>标签")
        return None
    
    current_head = head_match.group(1)
    
    # 提取当前的body标签属性（如果有）
    body_tag_pattern = r'<body([^>]*)>'
    body_tag_match = re.search(body_tag_pattern, current_html)
    body_attributes = body_tag_match.group(1) if body_tag_match else ''
    
    # 构建新的HTML（保留当前head，使用backup的body）
    new_html = f'''<!DOCTYPE html>
<html lang="zh-TW">
{current_head}
<body{body_attributes}>
{backup_body_content}
</body>
</html>'''
    
    return new_html

def process_file(current_file, backup_file, language='zh'):
    """处理单个文件：保留SEO，恢复body内容"""
    print(f'\n处理: {current_file}')
    
    try:
        # 读取当前文件
        with open(current_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # 读取备份文件
        if not Path(backup_file).exists():
            print(f'  ⚠️  备份文件不存在: {backup_file}')
            return False
            
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        # 提取备份的body内容
        print('  - 提取备份的body内容...')
        backup_body = extract_body_content(backup_content)
        
        if not backup_body:
            print('  ❌ 无法提取备份的body内容')
            return False
        
        # 替换body内容
        print('  - 保留当前SEO标签...')
        print('  - 恢复导航栏和页面设计...')
        new_content = replace_body_content(current_content, backup_body)
        
        if not new_content:
            return False
        
        # 写回文件
        with open(current_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'  ✅ 完成！SEO已保留，设计已恢复')
        
        return True
        
    except Exception as e:
        print(f'  ❌ 错误: {e}')
        return False

def main():
    """主函数"""
    print('='*60)
    print('🔄 只恢复设计内容，保留SEO标签')
    print('='*60)
    print('\n📋 恢复内容:')
    print('  ✅ 导航栏（navigation bar）')
    print('  ✅ 橙色banner（如有）')
    print('  ✅ 页面设计和布局')
    print('  ✅ 文字内容')
    print('\n📋 保留内容:')
    print('  ✅ <title>标签')
    print('  ✅ <meta>标签（description, keywords等）')
    print('  ✅ Open Graph标签')
    print('  ✅ Twitter Card标签')
    print('  ✅ Structured Data (JSON-LD)')
    print('')
    
    # 定义要处理的文件
    files_to_process = [
        ('index.html', 'backup_latest/index.html', 'zh'),
        ('en/index.html', 'backup_before_restore/en_index.html', 'en'),
        ('jp/index.html', 'backup_before_restore/jp_index.html', 'jp'),
        ('kr/index.html', 'backup_before_restore/kr_index.html', 'kr'),
    ]
    
    success_count = 0
    fail_count = 0
    
    for current_file, backup_file, language in files_to_process:
        if Path(current_file).exists():
            if process_file(current_file, backup_file, language):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f'\n⚠️  当前文件不存在: {current_file}')
            fail_count += 1
    
    print('\n' + '='*60)
    print(f'✅ 处理完成: {success_count}个文件成功, {fail_count}个失败')
    print('='*60)
    
    print('\n✨ 恢复结果:')
    print('  ✅ 导航栏已恢复到之前的设计')
    print('  ✅ 橙色banner（如有）已恢复')
    print('  ✅ 页面设计已恢复')
    print('  ✅ SEO标签（title、meta等）保持不变')

if __name__ == '__main__':
    main()

