#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专门为Solutions和资源页添加收据关键词（无AI限制）"""

import glob
import re

def add_receipt_no_ai_check(file_path):
    """添加收据关键词（无需AI检查）"""
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
        
        # ========== Title（无AI限制） ==========
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            new_title = title
            
            if lang == 'zh' and '收據' not in title:
                # 在title末尾或|前添加"及收據"
                if '|' in title:
                    new_title = re.sub(r'(\s*\|)', r' 及收據\1', title, count=1)
                else:
                    new_title = title + ' 及收據'
                changes.append('title')
            
            elif lang == 'en' and 'Receipt' not in title and 'receipt' not in title:
                # 在title末尾或|前添加"& Receipt"
                if '|' in title:
                    new_title = re.sub(r'(\s*\|)', r' & Receipt\1', title, count=1)
                else:
                    new_title = title + ' & Receipt'
                changes.append('title')
            
            elif lang == 'ja' and '領収書' not in title:
                # 在title末尾或|前添加"・領収書"
                if '|' in title:
                    new_title = re.sub(r'(\s*\|)', r'・領収書\1', title, count=1)
                else:
                    new_title = title + '・領収書'
                changes.append('title')
            
            elif lang == 'kr' and '영수증' not in title:
                # 在title末尾或|前添加" 및 영수증"
                if '|' in title:
                    new_title = re.sub(r'(\s*\|)', r' 및 영수증\1', title, count=1)
                else:
                    new_title = title + ' 및 영수증'
                changes.append('title')
            
            if new_title != title:
                content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
        
        # ========== Description（直接添加） ==========
        desc_pattern = r'(<meta[^>]*name="description"[^>]*content=")([^"]*)"'
        desc_match = re.search(desc_pattern, content)
        
        if desc_match:
            desc_prefix = desc_match.group(1)
            desc_content = desc_match.group(2)
            new_desc = desc_content
            
            if lang == 'zh' and '收據' not in desc_content:
                new_desc = f"{desc_content}。支援銀行對帳單及收據AI處理"
                changes.append('description')
            
            elif lang == 'en' and 'receipt' not in desc_content.lower():
                new_desc = f"{desc_content}. Support bank statement and receipt AI processing"
                changes.append('description')
            
            elif lang == 'ja' and '領収書' not in desc_content:
                new_desc = f"{desc_content}。銀行明細と領収書のAI処理に対応"
                changes.append('description')
            
            elif lang == 'kr' and '영수증' not in desc_content:
                new_desc = f"{desc_content}. 은행 명세서 및 영수증 AI 처리 지원"
                changes.append('description')
            
            if new_desc != desc_content:
                content = content.replace(
                    f'{desc_prefix}{desc_content}"',
                    f'{desc_prefix}{new_desc}"'
                )
        
        # ========== 保存 ==========
        if content != original:
            # 备份
            with open(file_path + '.backup_final', 'w', encoding='utf-8') as f:
                f.write(original)
            
            # 保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有Solutions和资源页
patterns = [
    'resources.html',
    'solutions/*/index.html',
    'en/resources.html',
    'en/solutions/*/index.html',
    'ja/resources.html',
    'kr/resources.html',
    'kr/solutions/*/index.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔧 最终版：为Solutions和资源页添加收据关键词（无AI限制）")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个文件待处理")
print()

processed = 0
by_type = {'title': 0, 'description': 0}

for i, file_path in enumerate(all_files, 1):
    success, changes = add_receipt_no_ai_check(file_path)
    
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
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 最终版更新完成！")
print("=" * 70)

