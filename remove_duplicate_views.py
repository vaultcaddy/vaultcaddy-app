#!/usr/bin/env python3
"""
删除 firstproject.html 中的重复视图，只保留 team-project-view

作用：
1. 删除 document-list-view（图1）
2. 删除 bank-statement-view（图3）
3. 只保留 team-project-view（图2）

使用方法：
python3 remove_duplicate_views.py
"""

import re
import shutil
from datetime import datetime

def remove_duplicate_views():
    input_file = 'firstproject.html'
    backup_file = f'{input_file}.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    print(f'📁 读取文件: {input_file}')
    
    # 备份原文件
    shutil.copy2(input_file, backup_file)
    print(f'✅ 已备份到: {backup_file}')
    
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'\n🔍 原文件大小: {len(content)} 字符')
    
    # 删除 document-list-view（图1）
    print(f'\n🗑️  删除 document-list-view（图1）...')
    
    # 找到 document-list-view 的开始和结束
    # 开始: <div id="document-list-view" class="view-container" style="display: none;">
    # 结束: 下一个 </div> 之前（在 team-project-view 之前）
    
    # 使用正则表达式匹配整个 document-list-view div
    pattern1 = r'<!-- 文檔列表視圖 -->\s*<div id="document-list-view"[^>]*>.*?</div>\s*(?=<!-- Team Project 視圖 -->)'
    
    match1 = re.search(pattern1, content, re.DOTALL)
    if match1:
        print(f'   找到 document-list-view，长度: {len(match1.group(0))} 字符')
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        print(f'   ✅ 已删除 document-list-view')
    else:
        print(f'   ⚠️  未找到 document-list-view')
    
    # 删除 bank-statement-view（图3）
    print(f'\n🗑️  删除 bank-statement-view（图3）...')
    
    # 使用正则表达式匹配整个 bank-statement-view div
    pattern2 = r'<!-- 銀行對帳單視圖 -->\s*<div id="bank-statement-view"[^>]*>.*?</div>\s*(?=</main>)'
    
    match2 = re.search(pattern2, content, re.DOTALL)
    if match2:
        print(f'   找到 bank-statement-view，长度: {len(match2.group(0))} 字符')
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        print(f'   ✅ 已删除 bank-statement-view')
    else:
        print(f'   ⚠️  未找到 bank-statement-view')
    
    print(f'\n📊 新文件大小: {len(content)} 字符')
    
    # 计算减少的字符数
    with open(input_file, 'r', encoding='utf-8') as f:
        original_size = len(f.read())
    reduced_size = original_size - len(content)
    print(f'   减少了: {reduced_size} 字符')
    
    # 写回文件
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n✅ 修复完成！')
    print(f'   - 原文件: {input_file}')
    print(f'   - 备份文件: {backup_file}')
    print(f'\n📝 现在只保留 team-project-view（图2）')
    print(f'   请刷新浏览器查看效果')

if __name__ == '__main__':
    try:
        remove_duplicate_views()
    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()

