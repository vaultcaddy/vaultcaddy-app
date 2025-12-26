#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""灵活版：强制添加收据关键词"""

import glob
import re

def add_receipt_flexible(file_path):
    """使用更灵活的匹配规则"""
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
        
        # ========== Title ==========
        if lang == 'zh':
            # 查找title中的"对账单"，在其后添加"及收据"
            if '<title>' in content and '對帳單' in content and '收據' not in content[:500]:
                content = re.sub(
                    r'(<title>[^<]*?)對帳單([^<]*</title>)',
                    r'\1對帳單及收據\2',
                    content,
                    count=1
                )
                changes.append('title')
        
        elif lang == 'en':
            # Statement -> Statement & Receipt
            if '<title>' in content and 'Statement' in content and 'Receipt' not in content[:500]:
                content = re.sub(
                    r'(<title>[^<]*?)Statement([^<]*?</title>)',
                    r'\1Statement & Receipt\2',
                    content,
                    count=1
                )
                changes.append('title')
        
        elif lang == 'ja':
            # 明細 -> 明細・領収書
            if '<title>' in content and '明細' in content and '領収書' not in content[:500]:
                content = re.sub(
                    r'(<title>[^<]*?)明細([^<]*?</title>)',
                    r'\1明細・領収書\2',
                    content,
                    count=1
                )
                changes.append('title')
        
        elif lang == 'kr':
            # 명세서 -> 명세서 및 영수증
            if '<title>' in content and '명세서' in content and '영수증' not in content[:500]:
                content = re.sub(
                    r'(<title>[^<]*?)명세서([^<]*?</title>)',
                    r'\1명세서 및 영수증\2',
                    content,
                    count=1
                )
                changes.append('title')
        
        # ========== Description ==========
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
        if desc_match:
            desc_content = desc_match.group(1)
            new_desc = desc_content
            
            if lang == 'zh' and '對帳單' in desc_content and '收據' not in desc_content:
                new_desc = desc_content.replace('對帳單', '對帳單及收據', 1)
                changes.append('description')
            
            elif lang == 'en' and 'statement' in desc_content.lower() and 'receipt' not in desc_content.lower():
                # 找到"statement"的位置，在其后添加" and receipt"
                new_desc = re.sub(
                    r'(bank\s+statement)',
                    r'bank statement and receipt',
                    desc_content,
                    count=1,
                    flags=re.IGNORECASE
                )
                if new_desc == desc_content:
                    new_desc = re.sub(
                        r'(Statement)',
                        r'Statement and Receipt',
                        desc_content,
                        count=1
                    )
                if new_desc != desc_content:
                    changes.append('description')
            
            elif lang == 'ja' and '明細' in desc_content and '領収書' not in desc_content:
                new_desc = desc_content.replace('明細', '明細と領収書', 1)
                changes.append('description')
            
            elif lang == 'kr' and '명세서' in desc_content and '영수증' not in desc_content:
                new_desc = desc_content.replace('명세서', '명세서 및 영수증', 1)
                changes.append('description')
            
            if new_desc != desc_content:
                content = content.replace(
                    f'<meta name="description" content="{desc_content}"',
                    f'<meta name="description" content="{new_desc}"'
                )
        
        # ========== Keywords ==========
        keywords_to_add = {
            'zh': ',銀行收據處理,收據AI處理,發票處理',
            'en': ',receipt processing,invoice processing,bank receipt',
            'ja': ',領収書処理,レシート処理,請求書処理',
            'kr': ',영수증 처리,은행 영수증,영수증 AI'
        }
        
        kw_match = re.search(r'<meta name="keywords" content="([^"]*)"', content)
        if kw_match:
            current_kw = kw_match.group(1)
            add_kw = keywords_to_add.get(lang, '')
            
            # 检查是否需要添加
            receipt_kw = {'zh': '收據', 'en': 'receipt', 'ja': '領収書', 'kr': '영수증'}
            if receipt_kw.get(lang, '') not in current_kw:
                new_kw = current_kw + add_kw
                content = content.replace(
                    f'<meta name="keywords" content="{current_kw}"',
                    f'<meta name="keywords" content="{new_kw}"'
                )
                changes.append('keywords')
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_flex', 'w', encoding='utf-8') as f:
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
print("🔧 灵活版：强制添加收据关键词")
print("=" * 70)
print()

processed = 0
by_lang = {'zh': 0, 'en': 0, 'ja': 0, 'kr': 0}

for i, file_path in enumerate(all_files, 1):
    success, changes = add_receipt_flexible(file_path)
    
    if success:
        processed += 1
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path:
            lang = 'kr'
        by_lang[lang] += 1
        
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   更新: {', '.join(changes)}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 总处理：{processed} 个文件")
print(f"   中文版：{by_lang['zh']} 个")
print(f"   英文版：{by_lang['en']} 个")
print(f"   日文版：{by_lang['ja']} 个")
print(f"   韩文版：{by_lang['kr']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 灵活版更新完成！")
print("=" * 70)

