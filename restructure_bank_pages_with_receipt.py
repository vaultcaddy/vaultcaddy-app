#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 将"中小企業真實案例"移到FAQ之后
2. 强化"收据"关键词在SEO中的显示
"""

import os
import re
import glob
from bs4 import BeautifulSoup

# 语言配置
LANGUAGE_CONFIG = {
    '': {  # 中文
        'case_study_title': '香港中小企業真實案例',
        'faq_title': '常見問題 FAQ',
        'meta_add_receipt': '及收據',
        'title_add_receipt': '及收據',
        'keywords_add': ',銀行收據處理,收據AI處理,receipt processing'
    },
    'en/': {  # 英文
        'case_study_title': 'Real Success Stories',
        'faq_title': 'FAQ',
        'meta_add_receipt': ' and Receipt',
        'title_add_receipt': ' & Receipt',
        'keywords_add': ',receipt processing,invoice processing,receipt AI'
    },
    'jp/': {  # 日文
        'case_study_title': '導入事例',
        'faq_title': 'よくある質問',
        'meta_add_receipt': 'と領収書',
        'title_add_receipt': '・領収書',
        'keywords_add': ',領収書処理,レシート処理,receipt processing'
    },
    'kr/': {  # 韩文
        'case_study_title': '도입 사례',
        'faq_title': '자주 묻는 질문',
        'meta_add_receipt': ' 및 영수증',
        'title_add_receipt': ' 및 영수증',
        'keywords_add': ',영수증 처리,receipt processing,영수증 AI'
    }
}

def move_case_study_after_faq(html_content, lang_key):
    """将客户案例移到FAQ之后"""
    config = LANGUAGE_CONFIG[lang_key]
    
    # 查找客户案例section（使用更灵活的匹配）
    case_study_pattern = r'<section[^>]*>[\s\S]*?' + re.escape(config['case_study_title']) + r'[\s\S]*?</section>'
    case_study_match = re.search(case_study_pattern, html_content)
    
    if not case_study_match:
        return html_content, False
    
    case_study_section = case_study_match.group(0)
    
    # 查找FAQ section的结束标签
    faq_pattern = r'<section[^>]*>[\s\S]*?' + re.escape(config['faq_title']) + r'[\s\S]*?</section>'
    faq_matches = list(re.finditer(faq_pattern, html_content))
    
    if not faq_matches:
        return html_content, False
    
    # 使用最后一个FAQ section
    last_faq = faq_matches[-1]
    
    # 移除原位置的客户案例
    html_content = html_content.replace(case_study_section, '')
    
    # 在最后一个FAQ section之后插入
    insert_position = last_faq.end()
    html_content = (
        html_content[:insert_position] + 
        '\n\n' + case_study_section + 
        html_content[insert_position:]
    )
    
    return html_content, True

def add_receipt_to_seo(html_content, lang_key):
    """在SEO标签中添加"收据"关键词"""
    config = LANGUAGE_CONFIG[lang_key]
    changes = 0
    
    # 1. 更新title标签（在"对账单"后添加"及收据"）
    if lang_key == '':  # 中文
        title_pattern = r'(<title>.*?銀行.*?)對帳單(.*?AI處理.*?</title>)'
        if re.search(title_pattern, html_content):
            html_content = re.sub(
                title_pattern,
                r'\1對帳單及收據\2',
                html_content
            )
            changes += 1
    elif lang_key == 'en/':  # 英文
        title_pattern = r'(<title>.*?Bank.*?)Statement(.*?AI Processing.*?</title>)'
        if re.search(title_pattern, html_content):
            html_content = re.sub(
                title_pattern,
                r'\1Statement & Receipt\2',
                html_content
            )
            changes += 1
    elif lang_key == 'jp/':  # 日文
        title_pattern = r'(<title>.*?銀行.*?)明細(.*?AI.*?</title>)'
        if re.search(title_pattern, html_content):
            html_content = re.sub(
                title_pattern,
                r'\1明細・領収書\2',
                html_content
            )
            changes += 1
    elif lang_key == 'kr/':  # 韩文
        title_pattern = r'(<title>.*?은행.*?)명세서(.*?AI.*?</title>)'
        if re.search(title_pattern, html_content):
            html_content = re.sub(
                title_pattern,
                r'\1명세서 및 영수증\2',
                html_content
            )
            changes += 1
    
    # 2. 更新meta description（在"对账单"后添加"及收据"）
    if lang_key == '':  # 中文
        desc_pattern = r'(<meta name="description" content=".*?銀行.*?)對帳單(.*?AI.*?)"'
        if re.search(desc_pattern, html_content):
            html_content = re.sub(
                desc_pattern,
                r'\1對帳單及收據\2',
                html_content
            )
            changes += 1
    elif lang_key == 'en/':  # 英文
        desc_pattern = r'(<meta name="description" content=".*?Bank.*?)Statement(.*?AI.*?)"'
        if re.search(desc_pattern, html_content):
            html_content = re.sub(
                desc_pattern,
                r'\1Statement and Receipt\2',
                html_content
            )
            changes += 1
    elif lang_key == 'jp/':  # 日文
        desc_pattern = r'(<meta name="description" content=".*?銀行.*?)明細(.*?AI.*?)"'
        if re.search(desc_pattern, html_content):
            html_content = re.sub(
                desc_pattern,
                r'\1明細と領収書\2',
                html_content
            )
            changes += 1
    elif lang_key == 'kr/':  # 韩文
        desc_pattern = r'(<meta name="description" content=".*?은행.*?)명세서(.*?AI.*?)"'
        if re.search(desc_pattern, html_content):
            html_content = re.sub(
                desc_pattern,
                r'\1명세서 및 영수증\2',
                html_content
            )
            changes += 1
    
    # 3. 更新keywords（添加收据相关关键词）
    keywords_pattern = r'(<meta name="keywords" content="[^"]*)"'
    keywords_match = re.search(keywords_pattern, html_content)
    if keywords_match:
        original_keywords = keywords_match.group(0)
        if config['keywords_add'] not in original_keywords:
            html_content = html_content.replace(
                original_keywords,
                original_keywords[:-1] + config['keywords_add'] + '"'
            )
            changes += 1
    
    # 4. 更新Open Graph标签
    og_title_pattern = r'(<meta property="og:title" content=".*?銀行.*?)對帳單(.*?)"'
    if lang_key == '' and re.search(og_title_pattern, html_content):
        html_content = re.sub(
            og_title_pattern,
            r'\1對帳單及收據\2',
            html_content
        )
        changes += 1
    
    return html_content, changes

def process_file(file_path):
    """处理单个HTML文件"""
    # 确定语言
    lang_key = ''
    if '/en/' in file_path:
        lang_key = 'en/'
    elif '/jp/' in file_path or '/ja/' in file_path:
        lang_key = 'jp/'
    elif '/kr/' in file_path or '/ko/' in file_path:
        lang_key = 'kr/'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 任务1：移动客户案例到FAQ之后
        new_content, moved = move_case_study_after_faq(content, lang_key)
        
        # 任务2：添加收据关键词到SEO
        new_content, seo_changes = add_receipt_to_seo(new_content, lang_key)
        
        if moved or seo_changes > 0:
            # 创建备份
            backup_path = file_path + '.backup_receipt_restructure'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入新内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, moved, seo_changes
        else:
            return False, False, 0
            
    except Exception as e:
        return False, False, str(e)

# 获取所有银行页面
patterns = [
    '*-bank-statement.html',
    'en/*-bank-statement.html',
    'jp/*-bank-statement.html',
    'ja/*-bank-statement.html',
    'kr/*-bank-statement.html',
    'ko/*-bank-statement.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))

print("=" * 70)
print("🔧 调整银行页面结构 + 强化收据关键词")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个银行页面待处理")
print()

processed = 0
moved_count = 0
seo_updated_count = 0
errors = 0

for i, file_path in enumerate(all_files, 1):
    success, moved, seo_changes = process_file(file_path)
    
    if success:
        processed += 1
        if moved:
            moved_count += 1
        if seo_changes > 0:
            seo_updated_count += 1
        
        status = []
        if moved:
            status.append("✅ 移动案例")
        if seo_changes > 0:
            status.append(f"✅ SEO更新({seo_changes}处)")
        
        print(f"[{i}/{len(all_files)}] {file_path}")
        print(f"         {' | '.join(status)}")
    elif seo_changes == 0 and not moved:
        # 无需处理
        pass
    else:
        errors += 1
        print(f"❌ [{i}/{len(all_files)}] {file_path} - 错误")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"📦 移动案例：{moved_count} 个文件")
print(f"🔍 SEO更新：{seo_updated_count} 个文件")
print(f"⏭️  无需处理：{len(all_files) - processed - errors} 个文件")
print(f"❌ 错误：{errors} 个文件")
print()
print("=" * 70)
print("🎉 银行页面结构调整 + 收据关键词强化完成！")
print("=" * 70)

