#!/usr/bin/env python3
"""
🔥 最终修复：清理 i18n 对象的所有格式问题
"""

import os
import re

def fix_indentation_in_i18n():
    """修复 i18n 对象中的缩进问题"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找并修复缩进问题
    fixed_lines = []
    in_i18n = False
    i18n_depth = 0
    
    for i, line in enumerate(lines):
        # 检测是否在 i18n 对象内
        if 'const i18n = {' in line:
            in_i18n = True
        
        if in_i18n:
            # 修复多余的缩进（8个空格变成正常缩进）
            if line.startswith('                no_transactions:'):
                line = line.replace('                no_transactions:', '        no_transactions:')
            if line.startswith('                no_transactions: '):
                line = line.replace('                ', '        ')
            
            # 检测 i18n 对象结束
            if line.strip() == '};' and i18n_depth == 0:
                in_i18n = False
        
        fixed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("✅ 修复了缩进问题")

def main():
    print("🔥 修复 i18n 格式问题...\n")
    
    fix_indentation_in_i18n()
    
    print("\n✅ 完成！")
    print("\n请清除缓存并刷新页面测试")

if __name__ == '__main__':
    main()

