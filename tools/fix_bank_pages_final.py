#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复所有银行页面：将案例section移到FAQ之后，优化银行名称排版"""

import glob
import re

def fix_single_bank_page(file_path):
    """修复单个银行页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 1. 优化银行名称排版 ==========
        # 查找并修复 "BOC Hong Kong 中國銀行(香港)" 类型的文字
        bank_name_patterns = [
            (r'BOC Hong Kong 中國銀行\(香港\)', '中國銀行(香港)<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">BOC Hong Kong</span>'),
            (r'HSBC 滙豐銀行', '滙豐銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">HSBC</span>'),
            (r'Hang Seng 恒生銀行', '恒生銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Hang Seng Bank</span>'),
            (r'Standard Chartered 渣打銀行', '渣打銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Standard Chartered</span>'),
            (r'DBS 星展銀行', '星展銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">DBS Bank</span>'),
            (r'BEA 東亞銀行', '東亞銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Bank of East Asia</span>'),
            (r'Citibank 花旗銀行', '花旗銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Citibank</span>'),
            (r'Dah Sing 大新銀行', '大新銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Dah Sing Bank</span>'),
            (r'CITIC 中信銀行', '中信銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">CITIC Bank</span>'),
            (r'Bank of Communications 交通銀行', '交通銀行<br><span style="font-size: 0.7em; font-weight: 400; color: #999;">Bank of Communications</span>'),
        ]
        
        # 只在 bank-logo 区域内替换
        bank_logo_pattern = r'(<div class="bank-logo"[^>]*>[\s\S]*?<strong[^>]*>)([^<]+)(</strong>)'
        
        def replace_bank_name(match):
            prefix = match.group(1)
            bank_name = match.group(2).strip()
            suffix = match.group(3)
            
            # 检查是否匹配任何银行名称模式
            for pattern, replacement in bank_name_patterns:
                if re.search(pattern, bank_name):
                    return prefix + replacement + suffix
            
            # 如果没有匹配，保持原样
            return match.group(0)
        
        content = re.sub(bank_logo_pattern, replace_bank_name, content)
        if content != original:
            changes.append('优化银行名称排版')
        
        # ========== 2. 查找案例section ==========
        # 查找 "香港中小企業真實案例" section
        case_pattern = r'<section[^>]*>[\s\S]*?<h2[^>]*>香港中小企業真實案例</h2>[\s\S]*?</section>'
        case_match = re.search(case_pattern, content)
        
        if not case_match:
            if changes:
                # 有银行名称排版优化，但没有案例section
                with open(file_path + '.backup_namefix', 'w', encoding='utf-8') as f:
                    f.write(original)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes
            else:
                return False, ['未找到案例section']
        
        case_section = case_match.group(0)
        case_pos = case_match.start()
        
        # ========== 3. 查找FAQ section ==========
        faq_pattern = r'<!-- FAQ Section -->\s*<section[\s\S]*?</section>'
        faq_match = re.search(faq_pattern, content)
        
        if not faq_match:
            if changes:
                with open(file_path + '.backup_namefix', 'w', encoding='utf-8') as f:
                    f.write(original)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes
            else:
                return False, ['未找到FAQ section']
        
        faq_end_pos = faq_match.end()
        
        # ========== 4. 检查案例是否已在FAQ之后 ==========
        if case_pos > faq_end_pos:
            # 案例已在FAQ之后，无需移动
            if changes:
                with open(file_path + '.backup_namefix', 'w', encoding='utf-8') as f:
                    f.write(original)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes
            else:
                return False, ['案例已在FAQ之后']
        
        # ========== 5. 移动案例section到FAQ之后 ==========
        # 移除原位置的案例section
        content = content[:case_match.start()] + content[case_match.end():]
        changes.append('移除原位置案例')
        
        # 重新查找FAQ section的结束位置（因为content已改变）
        faq_match = re.search(faq_pattern, content)
        faq_end_pos = faq_match.end()
        
        # 在FAQ后插入案例section
        content = (
            content[:faq_end_pos] +
            '\n\n    <!-- 案例 Section -->\n' +
            '    ' + case_section + '\n\n' +
            content[faq_end_pos:]
        )
        changes.append('在FAQ后插入案例')
        
        # ========== 6. 保存 ==========
        with open(file_path + '.backup_namefix', 'w', encoding='utf-8') as f:
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
print("🔧 修复所有银行页面（案例移到FAQ后 + 优化银行名称）")
print("=" * 70)
print()
print(f"找到 {len(all_files)} 个银行页面")
print()

processed = 0
by_lang = {'zh': 0, 'en': 0, 'ja': 0, 'kr': 0}

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_single_bank_page(file_path)
    
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
print(f"⏭️  无需处理：{len(all_files) - processed} 个文件")
print()
print("🎉 完成！")

