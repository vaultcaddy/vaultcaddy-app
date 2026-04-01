#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整重组所有银行页面：背景在顶部，案例在FAQ之后"""

import glob
import re

def restructure_page(file_path):
    """重组页面结构"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 识别语言和关键词 ==========
        if '/en/' in file_path:
            lang = 'en'
            case_title_patterns = [
                r'<h2[^>]*>(?:Real Case Studies?|Success Stories?|Hong Kong SME Case Studies?)</h2>',
                r'<section[^>]*>[\s\S]*?<h3[^>]*>📊 Case Study:',
            ]
            faq_pattern = r'<!-- FAQ Section -->|💬 Frequently Asked Questions'
        elif '/ja/' in file_path:
            lang = 'ja'
            case_title_patterns = [
                r'<h2[^>]*>(?:香港中小企業真實案例|実例紹介|成功事例)</h2>',
                r'<section[^>]*>[\s\S]*?<h3[^>]*>📊 (?:実例|ケーススタディ):',
            ]
            faq_pattern = r'<!-- FAQ|よくある質問'
        elif '/kr/' in file_path:
            lang = 'kr'
            case_title_patterns = [
                r'<h2[^>]*>(?:홍콩 중소기업 사례|성공 사례|실제 사례)</h2>',
                r'<section[^>]*>[\s\S]*?<h3[^>]*>📊 (?:사례|케이스 스터디):',
            ]
            faq_pattern = r'<!-- FAQ|자주 묻는 질문'
        else:
            lang = 'zh'
            case_title_patterns = [
                r'<h2[^>]*>香港中小企業真實案例</h2>',
                r'<section[^>]*>[\s\S]*?<h3[^>]*>📊 案例：',
            ]
            faq_pattern = r'<!-- FAQ|常見問題|💬 常見問題'
        
        # ========== 2. 查找FAQ位置 ==========
        faq_match = re.search(faq_pattern, content)
        if not faq_match:
            return False, ['未找到FAQ section']
        faq_pos = faq_match.start()
        
        # ========== 3. 查找并提取所有案例sections ==========
        case_sections = []
        for pattern in case_title_patterns:
            # 查找完整的案例section
            full_pattern = r'<section[^>]*>[\s\S]*?' + pattern + r'[\s\S]*?</section>'
            for match in re.finditer(full_pattern, content):
                case_sections.append((match.start(), match.end(), match.group(0)))
        
        # 按位置排序并去重
        case_sections = sorted(set(case_sections), key=lambda x: x[0])
        
        if not case_sections:
            return False, ['未找到案例section']
        
        # ========== 4. 检查案例是否在FAQ之后 ==========
        cases_after_faq = [cs for cs in case_sections if cs[0] > faq_pos]
        cases_before_faq = [cs for cs in case_sections if cs[0] < faq_pos]
        
        if len(cases_after_faq) == 1 and len(cases_before_faq) == 0:
            return False, ['案例已在FAQ之后，无需修改']
        
        # ========== 5. 移除所有案例sections ==========
        # 从后往前删除，避免位置变化
        for start, end, _ in sorted(case_sections, reverse=True):
            content = content[:start] + content[end:]
            changes.append(f'移除案例@{start}')
        
        # ========== 6. 找到最好的案例section（通常是最完整的一个） ==========
        best_case = max(case_sections, key=lambda x: len(x[2]))
        case_content = best_case[2]
        
        # ========== 7. 重新查找FAQ的结束位置（content已改变） ==========
        faq_match = re.search(faq_pattern, content)
        faq_pos = faq_match.start()
        
        # 查找FAQ section的结束
        after_faq = content[faq_pos:]
        faq_end_match = re.search(r'</section>\s*(?:\n|$)', after_faq)
        if faq_end_match:
            faq_end_pos = faq_pos + faq_end_match.end()
        else:
            faq_end_pos = faq_pos + 5000  # 估计值
        
        # ========== 8. 在FAQ后插入案例 ==========
        content = (
            content[:faq_end_pos] +
            '\n\n    <!-- Success Stories Section -->\n' +
            '    ' + case_content + '\n\n' +
            content[faq_end_pos:]
        )
        changes.append('在FAQ后插入案例')
        
        # ========== 保存 ==========
        with open(file_path + '.backup_restructure', 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, changes
        
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
print("🔧 完整重组所有银行页面")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个银行页面")
print()

processed = 0
by_lang = {'zh': 0, 'en': 0, 'ja': 0, 'kr': 0}
skipped = []

for i, file_path in enumerate(all_files, 1):
    success, messages = restructure_page(file_path)
    
    lang = 'zh'
    if '/en/' in file_path:
        lang = 'en'
    elif '/ja/' in file_path:
        lang = 'ja'
    elif '/kr/' in file_path:
        lang = 'kr'
    
    if success:
        processed += 1
        by_lang[lang] += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        skipped.append((file_path, messages[0]))
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print("📊 处理统计")
print("=" * 70)
print(f"✅ 已处理：{processed} 个文件")
print(f"   中文版：{by_lang['zh']} 个")
print(f"   英文版：{by_lang['en']} 个")
print(f"   日文版：{by_lang['ja']} 个")
print(f"   韩文版：{by_lang['kr']} 个")
print(f"⏭️  无需处理：{len(skipped)} 个文件")
print()
print("=" * 70)
print("🎉 重组完成！")
print("=" * 70)
print()
print("新结构：")
print("  1. 优惠横幅")
print("  2. Hero内容")
print("  3. ... 其他内容 ...")
print("  4. FAQ ← FAQ section")
print("  5. 香港中小企業真實案例 ← 移到这里（只有一个）")
print("  6. Final CTA")

