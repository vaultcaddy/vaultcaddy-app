#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在4个版本的index.html的Hero区域添加简洁口号
"""

import os
import re

# 工作目录
BASE_DIR = "/Users/cavlinyeung/ai-bank-parser"

# 4个版本的index.html及其口号
INDEX_FILES = {
    "index.html": {
        "slogan": "只保留您需要的功能，拒絕為不必要支付"
    },
    "en/index.html": {
        "slogan": "Only What You Need, Refuse to Pay for Unnecessary"
    },
    "jp/index.html": {
        "slogan": "必要な機能だけ、不要なものにお金を払わない"
    },
    "kr/index.html": {
        "slogan": "필요한 것만, 불필요한 것에 비용 지불 거부"
    }
}

def add_slogan_to_index(file_path, slogan):
    """在index.html的Hero副标题后添加口号"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找插入点：Hero副标题之后
    # 查找 <p id="hero-subtitle" ... 之后的第一个 </p>
    pattern = r'(<p id="hero-subtitle"[^>]*>.*?</p>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"❌ 未找到插入点：{file_path}")
        return False
    
    subtitle_end_pos = match.end()
    
    # 构建口号HTML
    slogan_html = f'''
        <div style="text-align: center; margin: 2rem auto 1rem; max-width: 800px;">
            <p style="font-size: 1.3rem; font-weight: 600; color: #667eea; background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%); padding: 1rem 2rem; border-radius: 50px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2); border: 2px solid rgba(102, 126, 234, 0.3); display: inline-block;">
                💡 {slogan}
            </p>
        </div>'''
    
    # 插入口号
    new_content = content[:subtitle_end_pos] + slogan_html + content[subtitle_end_pos:]
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("\n" + "="*80)
    print("🚀 开始在4个版本的index.html中添加简洁口号")
    print("="*80 + "\n")
    
    success_count = 0
    
    for file_name, config in INDEX_FILES.items():
        file_path = os.path.join(BASE_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在：{file_path}")
            continue
        
        print(f"📝 处理：{file_name}")
        print(f"   口号：{config['slogan']}")
        
        if add_slogan_to_index(file_path, config['slogan']):
            print(f"   ✅ 成功添加口号\n")
            success_count += 1
        else:
            print(f"   ❌ 添加失败\n")
    
    print("="*80)
    print(f"✅ 完成！成功添加：{success_count}/{len(INDEX_FILES)} 页")
    print("="*80)
    
    # 显示添加的口号
    print("\n📋 添加的口号：\n")
    for file_name, config in INDEX_FILES.items():
        print(f"   {file_name}:")
        print(f"   💡 {config['slogan']}\n")

if __name__ == "__main__":
    main()

