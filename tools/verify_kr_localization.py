#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证kr/目录的本地化和图片间距
"""

import os
import re
from bs4 import BeautifulSoup

def check_file(filepath):
    """检查单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含韩国关键词
        korean_keywords = ['서울', '부산', 'KB국민은행', '신한은행', '하나은행', 
                          '금융감독원', '개인정보보호법', '더존 SmartA']
        korean_count = sum(1 for kw in korean_keywords if kw in content)
        
        # 查找图片
        img_pattern = r'<img[^>]*>'
        images = list(re.finditer(img_pattern, content, re.IGNORECASE))
        
        # 检查相邻图片间距
        issues = []
        for i in range(len(images) - 1):
            img1 = images[i]
            img2 = images[i + 1]
            between = content[img1.end():img2.start()]
            text_only = re.sub(r'<[^>]+>', '', between)
            text_only = re.sub(r'\s+', '', text_only)
            text_len = len(text_only)
            
            if text_len < 1000:
                issues.append(f"图片 {i+1} 和 {i+2} 之间只有 {text_len} 字")
        
        return {
            'korean_keywords': korean_count,
            'images': len(images),
            'issues': issues,
            'has_korean': korean_count > 0
        }
    except Exception as e:
        return {'error': str(e)}

# 检查关键文件
files_to_check = [
    'kr/resources.html',
    'kr/hsbc-bank-statement.html',
    'kr/solutions/restaurant/index.html',
    'kr/solutions/accountant/index.html'
]

print("=" * 70)
print("🔍 验证kr/目录本地化和图片间距")
print("=" * 70)
print()

for filepath in files_to_check:
    if os.path.exists(filepath):
        result = check_file(filepath)
        print(f"📄 {filepath}")
        print(f"   韩国关键词: {result.get('korean_keywords', 0)} 个")
        print(f"   图片数量: {result.get('images', 0)} 个")
        
        issues = result.get('issues', [])
        if issues:
            print(f"   ⚠️  间距问题: {len(issues)} 处")
            for issue in issues[:3]:  # 只显示前3个
                print(f"      - {issue}")
        else:
            print(f"   ✅ 图片间距: 全部符合要求")
        
        if result.get('has_korean'):
            print(f"   ✅ 本地化: 已韩国化")
        else:
            print(f"   ❌ 本地化: 未韩国化")
        print()
    else:
        print(f"❌ {filepath} - 文件不存在")
        print()

print("=" * 70)
print("验证完成")
print("=" * 70)

