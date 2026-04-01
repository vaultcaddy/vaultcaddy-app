#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将所有页面中的"10秒"改为"3秒"
包括不同语言版本和Schema中的时间
"""

import os
import re

def change_time_in_file(file_path):
    """
    将文件中的10秒相关文本改为3秒
    
    Args:
        file_path: 文件路径
    
    Returns:
        int: 替换次数
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = 0
        
        # 替换规则列表
        patterns = [
            # 中文
            (r'10\s*秒', '3秒'),
            
            # 英文
            (r'10\s*seconds?', '3 seconds'),
            
            # 日文
            (r'10\s*秒', '3秒'),
            
            # 韩文
            (r'10\s*초', '3초'),
            
            # Schema中的PT10S (ISO 8601时间格式)
            (r'PT10S', 'PT3S'),
            
            # 可能的其他格式
            (r'(?i)in\s+10\s+seconds?', 'in 3 seconds'),
            (r'(?i)within\s+10\s+seconds?', 'within 3 seconds'),
            (r'約?\s*10\s*秒', '約3秒'),
            (r'平均\s*10\s*秒', '平均3秒'),
            (r'約?\s*10\s*초', '약3초'),
            (r'平均\s*10\s*초', '평均3초'),
        ]
        
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                replacements += count
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements
        else:
            return 0
            
    except Exception as e:
        print(f"❌ 处理失败 {file_path}: {e}")
        return 0

def find_files_to_process():
    """
    查找需要处理的文件
    
    Returns:
        list: 文件路径列表
    """
    files_to_process = []
    
    # 需要搜索的目录
    search_dirs = ['.']
    
    # 需要处理的文件类型
    file_extensions = ['.html', '.md']
    
    # 排除的目录
    exclude_dirs = {
        'node_modules', '.git', '.vscode', '__pycache__',
        'venv', 'dist', 'build', '.next', '.nuxt', 'terminals'
    }
    
    for search_dir in search_dirs:
        for root, dirs, files in os.walk(search_dir):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    files_to_process.append(os.path.join(root, file))
    
    return files_to_process

def main():
    """主函数"""
    print("🔄 批量替换\"10秒\"为\"3秒\"")
    print("=" * 60)
    
    # 查找所有需要处理的文件
    files = find_files_to_process()
    print(f"📊 找到 {len(files)} 个文件\n")
    
    total_replacements = 0
    files_modified = 0
    
    for i, file_path in enumerate(files, 1):
        rel_path = os.path.relpath(file_path, '.')
        
        # 跳过本脚本文件和其他Python脚本
        if file_path.endswith('.py'):
            continue
        
        replacements = change_time_in_file(file_path)
        
        if replacements > 0:
            files_modified += 1
            total_replacements += replacements
            print(f"✅ [{i}/{len(files)}] {rel_path} - 替换了 {replacements} 处")
    
    print("\n" + "=" * 60)
    print("📊 替换完成总结")
    print("=" * 60)
    print(f"📁 扫描文件: {len(files)} 个")
    print(f"✅ 修改文件: {files_modified} 个")
    print(f"🔄 总替换次数: {total_replacements} 次")
    
    if files_modified > 0:
        print(f"\n🚀 修改效果:")
        print(f"   ✅ 所有\"10秒\"已改为\"3秒\"")
        print(f"   ✅ 包括中文、英文、日文、韩文版本")
        print(f"   ✅ Schema中的PT10S已改为PT3S")
        print(f"   ✅ 更准确反映实际处理速度")

if __name__ == '__main__':
    main()

