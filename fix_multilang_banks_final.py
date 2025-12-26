#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复多语言银行页面：移除重复案例，将案例移到FAQ之后"""

import glob
import re

def fix_bank_page(file_path):
    """修复银行页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 识别语言 ==========
        if '/en/' in file_path:
            lang = 'en'
            case_title = 'Real Business Success Stories'
            faq_marker = 'Frequently Asked Questions'
        elif '/ja/' in file_path:
            lang = 'ja'
            case_title = '実例紹介|成功事例|香港中小企業真實案例'
            faq_marker = 'よくある質問|FAQ'
        elif '/kr/' in file_path:
            lang = 'kr'
            case_title = '홍콩 중소기업 사례|성공 사례|실제 사례|Real Business Success Stories'
            faq_marker = '자주 묻는 질문|FAQ'
        else:
            lang = 'zh'
            case_title = '香港中小企業真實案例'
            faq_marker = '常見問題'
        
        # ========== 2. 查找FAQ位置 ==========
        faq_match = re.search(faq_marker, content, re.IGNORECASE)
        if not faq_match:
            return False, ['未找到FAQ']
        faq_pos = faq_match.start()
        
        # ========== 3. 查找所有案例sections ==========
        # 使用更灵活的pattern：查找h2标题包含案例关键词的section
        case_pattern = rf'<h2[^>]*>(?:[^<]*)?(?:{case_title})(?:[^<]*)?</h2>'
        case_matches = list(re.finditer(case_pattern, content, re.IGNORECASE | re.DOTALL))
        
        if not case_matches:
            return False, ['未找到案例section']
        
        # ========== 4. 提取最完整的案例section ==========
        # 查找每个案例标题所在的section
        best_case_section = None
        best_case_length = 0
        case_sections_to_remove = []
        
        for case_match in case_matches:
            # 向前查找最近的<section标签
            before = content[:case_match.start()]
            section_start_matches = list(re.finditer(r'<section[^>]*>', before))
            if section_start_matches:
                section_start_pos = section_start_matches[-1].start()
            else:
                continue
            
            # 向后查找对应的</section>
            after = content[case_match.end():]
            section_end_match = re.search(r'</section>', after)
            if section_end_match:
                section_end_pos = case_match.end() + section_end_match.end()
            else:
                continue
            
            section_content = content[section_start_pos:section_end_pos]
            section_length = len(section_content)
            
            # 记录这个section
            case_sections_to_remove.append((section_start_pos, section_end_pos, section_content))
            
            # 找最长的作为最佳案例
            if section_length > best_case_length:
                best_case_length = section_length
                best_case_section = section_content
        
        if not best_case_section:
            return False, ['无法提取完整案例section']
        
        # ========== 5. 检查是否需要移动 ==========
        cases_after_faq = [cs for cs in case_sections_to_remove if cs[0] > faq_pos]
        cases_before_faq = [cs for cs in case_sections_to_remove if cs[0] < faq_pos]
        
        if len(cases_after_faq) == 1 and len(cases_before_faq) == 0:
            return False, ['案例已在FAQ之后，无需修改']
        
        # ========== 6. 移除所有案例sections ==========
        for start, end, _ in sorted(case_sections_to_remove, reverse=True):
            content = content[:start] + '\n' + content[end:]
            changes.append(f'移除案例@{start}')
        
        # ========== 7. 查找FAQ section的结束 ==========
        faq_match = re.search(faq_marker, content, re.IGNORECASE)
        faq_pos = faq_match.start()
        
        # 查找FAQ所在section的结束
        after_faq = content[faq_pos:]
        faq_section_end = re.search(r'</section>', after_faq)
        if faq_section_end:
            insert_pos = faq_pos + faq_section_end.end()
        else:
            # 如果找不到，就在FAQ之后1000个字符处插入
            insert_pos = faq_pos + 1000
        
        # ========== 8. 插入案例section ==========
        content = (
            content[:insert_pos] +
            '\n\n    <!-- Success Stories Section -->\n' +
            '    ' + best_case_section + '\n\n' +
            content[insert_pos:]
        )
        changes.append('在FAQ后插入案例')
        
        # ========== 保存 ==========
        with open(file_path + '.backup_final', 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, changes
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
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
print("🔧 修复多语言银行页面（移除重复，移到FAQ后）")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个多语言银行页面")
print()

processed = 0
by_lang = {'en': 0, 'ja': 0, 'kr': 0}

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_bank_page(file_path)
    
    lang = 'en' if '/en/' in file_path else ('ja' if '/ja/' in file_path else 'kr')
    
    if success:
        processed += 1
        by_lang[lang] += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"   英文版：{by_lang['en']} 个")
print(f"   日文版：{by_lang['ja']} 个")
print(f"   韩文版：{by_lang['kr']} 个")
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("🎉 完成！")

