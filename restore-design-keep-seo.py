#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只恢复body内容（导航栏、banner、页面设计），保留当前的SEO标签
"""

import re
from pathlib import Path

def extract_section(html_content, tag_name):
    """提取指定标签的内容"""
    # 匹配开始和结束标签（包括属性）
    pattern = rf'<{tag_name}[^>]*>(.*?)</{tag_name}>'
    match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0)  # 返回完整的标签及内容
    return None

def main():
    """主函数"""
    print('='*60)
    print('🔄 只恢复设计内容，保留当前SEO标签')
    print('='*60)
    print('\n📋 保留（不变）:')
    print('  ✅ <title>标签')
    print('  ✅ <meta>标签（description, keywords等）')
    print('  ✅ Open Graph标签')
    print('  ✅ Twitter Card标签')
    print('  ✅ Structured Data (JSON-LD)')
    print('')
    print('📋 恢复（从backup）:')
    print('  ✅ 导航栏（navigation bar）')
    print('  ✅ 橙色banner（如有）')
    print('  ✅ 页面设计和布局')
    print('  ✅ 文字内容')
    print('')
    
    # 定义要处理的文件
    files_to_process = [
        ('index.html', 'backup_latest/index.html', 'zh-TW'),
    ]
    
    success_count = 0
    fail_count = 0
    
    for current_file, backup_file, lang in files_to_process:
        print(f'\n处理: {current_file}')
        
        try:
            # 1. 读取当前文件
            if not Path(current_file).exists():
                print(f'  ❌ 当前文件不存在: {current_file}')
                fail_count += 1
                continue
                
            with open(current_file, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # 2. 读取备份文件
            if not Path(backup_file).exists():
                print(f'  ❌ 备份文件不存在: {backup_file}')
                fail_count += 1
                continue
                
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            # 3. 提取当前的head部分（保留SEO）
            print('  - 提取当前的<head>标签（保留SEO）...')
            current_head = extract_section(current_content, 'head')
            if not current_head:
                print('  ❌ 无法提取当前的<head>标签')
                fail_count += 1
                continue
            
            # 4. 提取备份的body部分（恢复设计）
            print('  - 提取备份的<body>标签（恢复设计）...')
            backup_body = extract_section(backup_content, 'body')
            if not backup_body:
                print('  ❌ 无法提取备份的<body>标签')
                fail_count += 1
                continue
            
            # 5. 构建新的HTML
            print('  - 合并内容（保留SEO + 恢复设计）...')
            new_html = f'''<!DOCTYPE html>
<html lang="{lang}">
{current_head}
{backup_body}
</html>'''
            
            # 6. 写回文件
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f'  ✅ 完成！')
            print(f'     - SEO标签：保持不变（当前版本）')
            print(f'     - 页面设计：已恢复（备份版本）')
            
            success_count += 1
            
        except Exception as e:
            print(f'  ❌ 错误: {e}')
            fail_count += 1
    
    print('\n' + '='*60)
    print(f'✅ 处理完成: {success_count}个文件成功, {fail_count}个失败')
    print('='*60)
    
    if success_count > 0:
        print('\n✨ 恢复结果:')
        print('  ✅ 导航栏已恢复')
        print('  ✅ 页面设计已恢复')
        print('  ✅ SEO标签（title、meta等）保持不变')

if __name__ == '__main__':
    main()

