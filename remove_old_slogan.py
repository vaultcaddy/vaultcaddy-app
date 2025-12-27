#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从4个版本的index.html中移除旧口号
"""

import os
import re

# 工作目录
BASE_DIR = "/Users/cavlinyeung/ai-bank-parser"

# 4个版本的index.html
INDEX_FILES = [
    "index.html",
    "en/index.html",
    "jp/index.html",
    "kr/index.html"
]

def remove_slogan(file_path):
    """移除index.html中的旧口号"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并删除口号div（包括前后的换行）
    pattern = r'\n\s*<div style="text-align: center; margin: 2rem auto 1rem; max-width: 800px;">.*?</div>'
    
    # 使用DOTALL标志让.匹配换行符
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("\n" + "="*80)
    print("🗑️  开始移除旧口号")
    print("="*80 + "\n")
    
    success_count = 0
    
    for file_name in INDEX_FILES:
        file_path = os.path.join(BASE_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在：{file_path}")
            continue
        
        print(f"📝 处理：{file_name}")
        
        if remove_slogan(file_path):
            print(f"   ✅ 成功移除旧口号\n")
            success_count += 1
        else:
            print(f"   ❌ 移除失败\n")
    
    print("="*80)
    print(f"✅ 完成！成功移除：{success_count}/{len(INDEX_FILES)} 页")
    print("="*80)

if __name__ == "__main__":
    main()

