#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用版：为所有页面添加收据关键词（无需匹配特定词）"""

import glob
import re

def universal_add_receipt(file_path):
    """通用添加收据关键词"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # 检测语言
        lang = 'zh'
        if '/en/' in file_path or file_path.startswith('en/'):
            lang = 'en'
        elif '/ja/' in file_path or file_path.startswith('ja/'):
            lang = 'ja'
        elif '/kr/' in file_path or file_path.startswith('kr/'):
            lang = 'kr'
        
        # ========== Description - 直接在开头添加收据关键词 ==========
        desc_pattern = r'(<meta[^>]*name="description"[^>]*content=")([^"]*)"'
        desc_match = re.search(desc_pattern, content)
        
        if desc_match:
            desc_prefix = desc_match.group(1)
            desc_content = desc_match.group(2)
            new_desc = desc_content
            
            # 检查是否已包含收据关键词
            if lang == 'zh' and '收據' not in desc_content:
                # 在description开头添加收据相关描述
                new_desc = f"支援銀行對帳單及收據AI處理。{desc_content}"
                changes.append('description')
            
            elif lang == 'en' and 'receipt' not in desc_content.lower():
                new_desc = f"Support bank statement and receipt AI processing. {desc_content}"
                changes.append('description')
            
            elif lang == 'ja' and '領収書' not in desc_content:
                new_desc = f"銀行明細と領収書のAI処理に対応。{desc_content}"
                changes.append('description')
            
            elif lang == 'kr' and '영수증' not in desc_content:
                new_desc = f"은행 명세서 및 영수증 AI 처리 지원. {desc_content}"
                changes.append('description')
            
            if new_desc != desc_content:
                content = content.replace(
                    f'{desc_prefix}{desc_content}"',
                    f'{desc_prefix}{new_desc}"'
                )
        
        # ========== Keywords ==========
        kw_pattern = r'(<meta[^>]*name="keywords"[^>]*content=")([^"]*)"'
        kw_match = re.search(kw_pattern, content)
        
        if kw_match:
            kw_prefix = kw_match.group(1)
            keywords = kw_match.group(2)
            
            keywords_to_add = {
                'zh': ',收據處理,收據AI,發票處理',
                'en': ',receipt processing,invoice AI,receipt automation',
                'ja': ',領収書処理,レシート処理,請求書AI',
                'kr': ',영수증 처리,영수증 AI,송장 처리'
            }
            
            receipt_check = {'zh': '收據', 'en': 'receipt', 'ja': '領収書', 'kr': '영수증'}
            
            if receipt_check.get(lang, '') not in keywords:
                new_keywords = keywords + keywords_to_add.get(lang, '')
                content = content.replace(
                    f'{kw_prefix}{keywords}"',
                    f'{kw_prefix}{new_keywords}"'
                )
                changes.append('keywords')
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_universal', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有需要处理的页面
patterns = [
    'resources.html',
    'solutions/*/index.html',
    'en/resources.html',
    'en/solutions/*/index.html',
    'ja/resources.html',
    'ja/solutions/*/index.html',
    'kr/resources.html',
    'kr/solutions/*/index.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 通用版：为所有页面Description添加收据关键词")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个文件待处理")
print()

processed = 0
by_type = {'description': 0, 'keywords': 0}

for i, file_path in enumerate(all_files, 1):
    success, changes = universal_add_receipt(file_path)
    
    if success:
        processed += 1
        for change in changes:
            by_type[change] = by_type.get(change, 0) + 1
        
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   更新: {', '.join(changes)}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"   Description更新：{by_type['description']} 个")
print(f"   Keywords更新：{by_type['keywords']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 通用版更新完成！")
print("=" * 70)

