#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""强制添加收据关键词到所有银行页面"""

import glob
import re

def force_add_receipt(file_path):
    """强制添加收据关键词"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # 检测语言
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path:
            lang = 'kr'
        
        # ========== 1. 修复Title ==========
        if lang == 'zh':
            # 对账单 -> 对账单及收据
            title_patterns = [
                (r'(<title>.*?)對帳單(.*?AI.*?</title>)', r'\1對帳單及收據\2'),
                (r'(<title>.*?)银行明细(.*?AI.*?</title>)', r'\1银行明细及收据\2'),
            ]
        elif lang == 'en':
            title_patterns = [
                (r'(<title>.*?)Statement(.*?AI.*?</title>)', r'\1Statement & Receipt\2'),
                (r'(<title>.*?)Bank Statement(.*?</title>)', r'\1Bank Statement & Receipt\2'),
            ]
        elif lang == 'ja':
            title_patterns = [
                (r'(<title>.*?)明細(.*?AI.*?</title>)', r'\1明細・領収書\2'),
                (r'(<title>.*?)明細書(.*?AI.*?</title>)', r'\1明細書・領収書\2'),
            ]
        elif lang == 'kr':
            title_patterns = [
                (r'(<title>.*?)명세서(.*?AI.*?</title>)', r'\1명세서 및 영수증\2'),
            ]
        
        for pattern, replacement in title_patterns:
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content, count=1)
                if new_content != content:
                    content = new_content
                    changes.append('title')
                    break
        
        # ========== 2. 修复Description ==========
        if lang == 'zh':
            desc_patterns = [
                (r'(<meta name="description" content=".*?)對帳單(.*?AI.*?")', r'\1對帳單及收據\2'),
                (r'(<meta name="description" content=".*?)银行明细(.*?AI.*?")', r'\1银行明细及收据\2'),
            ]
        elif lang == 'en':
            desc_patterns = [
                (r'(<meta name="description" content=".*?)Statement(.*?AI.*?")', r'\1Statement and Receipt\2'),
                (r'(<meta name="description" content=".*?)Bank Statement(.*?")', r'\1Bank Statement and Receipt\2'),
            ]
        elif lang == 'ja':
            desc_patterns = [
                (r'(<meta name="description" content=".*?)明細(.*?AI.*?")', r'\1明細と領収書\2'),
                (r'(<meta name="description" content=".*?)明細書(.*?AI.*?")', r'\1明細書と領収書\2'),
            ]
        elif lang == 'kr':
            desc_patterns = [
                (r'(<meta name="description" content=".*?)명세서(.*?AI.*?")', r'\1명세서 및 영수증\2'),
            ]
        
        for pattern, replacement in desc_patterns:
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content, count=1)
                if new_content != content:
                    content = new_content
                    changes.append('description')
                    break
        
        # ========== 3. 添加Keywords ==========
        keywords_to_add = {
            'zh': ',銀行收據處理,收據AI處理,發票處理,receipt processing',
            'en': ',receipt processing,invoice processing,receipt AI,bank receipt',
            'ja': ',領収書処理,レシート処理,請求書処理,receipt processing',
            'kr': ',영수증 처리,receipt processing,영수증 AI,은행 영수증'
        }
        
        kw_match = re.search(r'<meta name="keywords" content="([^"]*)"', content)
        if kw_match:
            current_kw = kw_match.group(1)
            add_kw = keywords_to_add.get(lang, '')
            
            # 检查是否需要添加
            need_add = False
            if lang == 'zh' and '收據' not in current_kw:
                need_add = True
            elif lang == 'en' and 'receipt' not in current_kw.lower():
                need_add = True
            elif lang == 'ja' and '領収書' not in current_kw:
                need_add = True
            elif lang == 'kr' and '영수증' not in current_kw:
                need_add = True
            
            if need_add and add_kw:
                new_kw = current_kw + add_kw
                content = content.replace(
                    f'<meta name="keywords" content="{current_kw}"',
                    f'<meta name="keywords" content="{new_kw}"'
                )
                changes.append('keywords')
        
        # ========== 4. OG Title ==========
        if lang == 'zh':
            og_pattern = r'(<meta property="og:title" content=".*?)對帳單(.*?")'
            if re.search(og_pattern, content):
                content = re.sub(og_pattern, r'\1對帳單及收據\2', content, count=1)
                changes.append('og:title')
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_force_receipt', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    '*-bank-statement.html',
    'en/*-bank-statement.html',
    'ja/*-bank-statement.html',
    'kr/*-bank-statement.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 强制添加收据关键词到所有银行页面")
print("=" * 70)
print()

processed = 0
total_changes = 0

for i, file_path in enumerate(all_files, 1):
    success, changes = force_add_receipt(file_path)
    
    if success:
        processed += 1
        total_changes += len(changes)
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   更新: {', '.join(changes)}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"🔧 总更新：{total_changes} 处")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 强制更新完成！")
print("=" * 70)

