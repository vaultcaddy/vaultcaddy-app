#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版：处理所有语言版本的银行页面
1. 移动客户案例到FAQ之后
2. 强化收据关键词
"""

import os
import re
import glob

def process_file_v2(file_path):
    """处理单个HTML文件（优化版）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # ==================================================
        # 任务1：移动客户案例section到最后一个FAQ section之后
        # ==================================================
        
        # 查找所有独立的section标签
        sections = list(re.finditer(r'<section[^>]*>[\s\S]*?</section>', content))
        
        # 找到包含"案例/Case/事例/사례"的section
        case_study_section = None
        case_study_keywords = ['香港中小企業真實案例', 'Real Business Success Stories', 
                              '導入事例', '도입 사례', 'Success Stories']
        
        for section in sections:
            section_text = section.group(0)
            if any(keyword in section_text for keyword in case_study_keywords):
                # 确保这是一个独立的section（不在其他section内）
                # 通过检查是否包含完整的案例结构
                if ('案例' in section_text or 'Case' in section_text or 
                    '事例' in section_text or '사례' in section_text) and \
                   len(section_text) > 500:  # 确保是完整的section
                    case_study_section = section
                    break
        
        # 找到最后一个FAQ section
        faq_section = None
        faq_keywords = ['FAQ', '常見問題', 'Frequently Asked Questions', 
                       'よくある質問', '자주 묻는 질문']
        
        for section in reversed(sections):
            section_text = section.group(0)
            if any(keyword in section_text for keyword in faq_keywords):
                if '<details' in section_text:  # 确保是FAQ section
                    faq_section = section
                    break
        
        # 执行移动
        if case_study_section and faq_section:
            case_content = case_study_section.group(0)
            
            # 移除原位置
            content = content.replace(case_content, '', 1)
            
            # 在FAQ之后插入
            faq_end = faq_section.end()
            # 需要在新的content中重新查找FAQ位置
            new_faq_match = None
            for section in re.finditer(r'<section[^>]*>[\s\S]*?</section>', content):
                section_text = section.group(0)
                if any(keyword in section_text for keyword in faq_keywords):
                    if '<details' in section_text:
                        new_faq_match = section
                        break
            
            if new_faq_match:
                insert_pos = new_faq_match.end()
                content = (
                    content[:insert_pos] + 
                    '\n\n' + case_content + 
                    content[insert_pos:]
                )
                changes_made.append('移动案例')
        
        # ==================================================
        # 任务2：强化收据关键词
        # ==================================================
        
        # 检测语言
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path or '/ko/' in file_path:
            lang = 'kr'
        
        # 更新title
        if lang == 'zh':
            if re.search(r'<title>.*?對帳單(?!及收據).*?AI處理', content):
                content = re.sub(
                    r'(<title>.*?)對帳單(.*?AI處理)',
                    r'\1對帳單及收據\2',
                    content
                )
                changes_made.append('title')
        elif lang == 'en':
            if re.search(r'<title>.*?Statement(?! & Receipt).*?AI Processing', content):
                content = re.sub(
                    r'(<title>.*?)Statement(.*?AI Processing)',
                    r'\1Statement & Receipt\2',
                    content
                )
                changes_made.append('title')
        elif lang == 'ja':
            if re.search(r'<title>.*?明細(?!・領収書).*?AI', content):
                content = re.sub(
                    r'(<title>.*?)明細(.*?AI)',
                    r'\1明細・領収書\2',
                    content
                )
                changes_made.append('title')
        elif lang == 'kr':
            if re.search(r'<title>.*?명세서(?! 및 영수증).*?AI', content):
                content = re.sub(
                    r'(<title>.*?)명세서(.*?AI)',
                    r'\1명세서 및 영수증\2',
                    content
                )
                changes_made.append('title')
        
        # 更新meta description
        if lang == 'zh':
            if re.search(r'<meta name="description".*?對帳單(?!及收據).*?AI', content):
                content = re.sub(
                    r'(<meta name="description"[^>]*?對帳單)(.*?AI)',
                    r'\1及收據\2',
                    content
                )
                changes_made.append('description')
        elif lang == 'en':
            if re.search(r'<meta name="description".*?Statement(?! and Receipt).*?AI', content):
                content = re.sub(
                    r'(<meta name="description"[^>]*?Statement)(.*?AI)',
                    r'\1 and Receipt\2',
                    content
                )
                changes_made.append('description')
        elif lang == 'ja':
            if re.search(r'<meta name="description".*?明細(?!と領収書).*?AI', content):
                content = re.sub(
                    r'(<meta name="description"[^>]*?明細)(.*?AI)',
                    r'\1と領収書\2',
                    content
                )
                changes_made.append('description')
        elif lang == 'kr':
            if re.search(r'<meta name="description".*?명세서(?! 및 영수증).*?AI', content):
                content = re.sub(
                    r'(<meta name="description"[^>]*?명세서)(.*?AI)',
                    r'\1 및 영수증\2',
                    content
                )
                changes_made.append('description')
        
        # 更新keywords
        keywords_to_add = {
            'zh': ',銀行收據處理,收據AI處理,receipt processing',
            'en': ',receipt processing,invoice processing,receipt AI',
            'ja': ',領収書処理,レシート処理,receipt processing',
            'kr': ',영수증 처리,receipt processing,영수증 AI'
        }
        
        keywords_pattern = r'(<meta name="keywords" content="[^"]*)"'
        keywords_match = re.search(keywords_pattern, content)
        if keywords_match:
            original_kw = keywords_match.group(0)
            add_kw = keywords_to_add.get(lang, '')
            if add_kw and add_kw not in original_kw:
                content = content.replace(
                    original_kw,
                    original_kw[:-1] + add_kw + '"'
                )
                changes_made.append('keywords')
        
        # 更新OG title
        if lang == 'zh':
            if re.search(r'<meta property="og:title".*?對帳單(?!及收據).*?AI', content):
                content = re.sub(
                    r'(<meta property="og:title"[^>]*?對帳單)(.*?AI)',
                    r'\1及收據\2',
                    content
                )
                changes_made.append('og:title')
        
        # ==================================================
        # 保存修改
        # ==================================================
        
        if content != original_content:
            # 创建备份
            backup_path = file_path + '.backup_receipt_v2'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # 写入新内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes_made
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
print("🔧 优化版：调整银行页面结构 + 强化收据关键词")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个银行页面待处理")
print()

processed = 0
total_changes = 0

for i, file_path in enumerate(all_files, 1):
    success, changes = process_file_v2(file_path)
    
    if success:
        processed += 1
        total_changes += len(changes)
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   修改: {', '.join(changes)}")
    else:
        if changes:
            print(f"❌ [{i}/{len(all_files)}] {file_path} - {changes[0]}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"🔧 总修改：{total_changes} 处")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("=" * 70)
print("🎉 所有语言版本银行页面优化完成！")
print("=" * 70)

