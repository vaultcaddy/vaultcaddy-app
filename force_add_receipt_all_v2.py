#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""强力版：为所有页面添加收据关键词"""

import glob
import re
import os

def add_receipt_to_page(file_path):
    """为单个页面添加收据关键词"""
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
        
        # ========== Title ==========
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if title_match:
            title = title_match.group(1)
            new_title = title
            
            if lang == 'zh' and 'AI' in title and '收據' not in title:
                # 在"AI"前添加"及收據"
                if '對帳單' in title:
                    new_title = title.replace('對帳單', '對帳單及收據', 1)
                elif '银行' in title and 'AI' in title:
                    new_title = re.sub(r'(银行[^A]*?)(AI)', r'\1及收據\2', title)
                
                if new_title != title:
                    content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    changes.append('title')
            
            elif lang == 'en' and 'AI' in title and 'Receipt' not in title and 'receipt' not in title:
                if 'Statement' in title:
                    new_title = title.replace('Statement', 'Statement & Receipt', 1)
                elif 'Bank' in title and 'AI' in title:
                    new_title = re.sub(r'(Bank[^A]*?)(AI)', r'\1& Receipt \2', title)
                
                if new_title != title:
                    content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    changes.append('title')
            
            elif lang == 'ja' and 'AI' in title and '領収書' not in title:
                if '明細' in title:
                    new_title = title.replace('明細', '明細・領収書', 1)
                
                if new_title != title:
                    content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    changes.append('title')
            
            elif lang == 'kr' and 'AI' in title and '영수증' not in title:
                if '명세서' in title:
                    new_title = title.replace('명세서', '명세서 및 영수증', 1)
                
                if new_title != title:
                    content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                    changes.append('title')
        
        # ========== Description ==========
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
        if desc_match:
            desc = desc_match.group(1)
            new_desc = desc
            
            if lang == 'zh' and 'AI' in desc and '收據' not in desc:
                if '對帳單' in desc:
                    new_desc = desc.replace('對帳單', '對帳單及收據', 1)
                
                if new_desc != desc:
                    content = content.replace(
                        f'content="{desc}"',
                        f'content="{new_desc}"'
                    )
                    changes.append('description')
            
            elif lang == 'en' and 'AI' in desc.lower() and 'receipt' not in desc.lower():
                if 'statement' in desc.lower():
                    new_desc = re.sub(r'(bank\s+statement)', r'bank statement and receipt', desc, count=1, flags=re.IGNORECASE)
                
                if new_desc != desc:
                    content = content.replace(
                        f'content="{desc}"',
                        f'content="{new_desc}"'
                    )
                    changes.append('description')
            
            elif lang == 'ja' and 'AI' in desc and '領収書' not in desc:
                if '明細' in desc:
                    new_desc = desc.replace('明細', '明細と領収書', 1)
                
                if new_desc != desc:
                    content = content.replace(
                        f'content="{desc}"',
                        f'content="{new_desc}"'
                    )
                    changes.append('description')
            
            elif lang == 'kr' and 'AI' in desc and '영수증' not in desc:
                if '명세서' in desc:
                    new_desc = desc.replace('명세서', '명세서 및 영수증', 1)
                
                if new_desc != desc:
                    content = content.replace(
                        f'content="{desc}"',
                        f'content="{new_desc}"'
                    )
                    changes.append('description')
        
        # ========== Keywords ==========
        kw_match = re.search(r'<meta[^>]*name="keywords"[^>]*content="([^"]*)"', content)
        if kw_match:
            keywords = kw_match.group(1)
            
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
                    f'content="{keywords}"',
                    f'content="{new_keywords}"'
                )
                changes.append('keywords')
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_v2', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有landing page
patterns = [
    'index.html',
    'resources.html',
    'solutions/*/index.html',
    'en/index.html',
    'en/resources.html',
    'en/solutions/*/index.html',
    'ja/resources.html',
    'ja/solutions/*/index.html',
    'kr/index.html',
    'kr/resources.html',
    'kr/solutions/*/index.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 强力版：为所有Landing Page添加收据关键词")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个文件待处理")
print()

processed = 0
by_type = {'title': 0, 'description': 0, 'keywords': 0}

for i, file_path in enumerate(all_files, 1):
    success, changes = add_receipt_to_page(file_path)
    
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
print(f"   Title更新：{by_type['title']} 个")
print(f"   Description更新：{by_type['description']} 个")
print(f"   Keywords更新：{by_type['keywords']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 强力更新完成！")
print("=" * 70)

