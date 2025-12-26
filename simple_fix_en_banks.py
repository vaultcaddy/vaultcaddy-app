#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单直接地修复英文银行页面"""

import glob
import re

def simple_fix(file_path):
    """简单修复：移除所有案例section，在FAQ后添加一个"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 1. 查找FAQ位置
        faq_match = re.search(r'(<!-- FAQ Section -->)', content)
        if not faq_match:
            return False, ['未找到FAQ Section']
        
        # 2. 查找FAQ section的结束
        faq_start = faq_match.start()
        after_faq = content[faq_start:]
        faq_section_end_match = re.search(r'</section>', after_faq)
        if not faq_section_end_match:
            return False, ['无法找到FAQ section结束']
        
        faq_end_pos = faq_start + faq_section_end_match.end()
        
        # 3. 查找所有"Real Business Success Stories" section并移除
        # 使用更简单的方法：查找h2标题，然后向前向后找section边界
        case_pattern = r'<h2[^>]*>Real Business Success Stories</h2>'
        removed_count = 0
        
        # 重复查找并移除，直到没有更多
        while True:
            case_match = re.search(case_pattern, content, re.IGNORECASE)
            if not case_match:
                break
            
            # 向前查找最近的<section
            before = content[:case_match.start()]
            section_starts = list(re.finditer(r'<section[^>]*>', before))
            if section_starts:
                section_start = section_starts[-1].start()
            else:
                # 如果找不到，就跳过这个
                break
            
            # 向后查找对应的</section>
            after = content[case_match.end():]
            section_end_match = re.search(r'</section>', after)
            if section_end_match:
                section_end = case_match.end() + section_end_match.end()
            else:
                break
            
            # 移除这个section
            content = content[:section_start] + '\n' + content[section_end:]
            removed_count += 1
        
        if removed_count == 0:
            return False, ['未找到案例section']
        
        # 4. 创建一个新的案例section
        case_section = '''
    <!-- Success Stories Section -->
    <section style="padding: 3rem 0; background: white;">
        <div class="container">
            <h2 style="font-size: 2rem; color: #667eea; margin-bottom: 2rem;">Real Business Success Stories</h2>
            
            <div style="background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">📊 Case Study: NYC Accounting Firm</h3>
                <p style="line-height: 1.8; color: #4b5563;">
                    Smith & Associates, a mid-sized accounting firm in Manhattan, serves over 65 small businesses.
                    They process 280+ bank statements monthly from various institutions including Chase, Bank of America,
                    Citibank, and Wells Fargo. Previously, their team of 4 bookkeepers spent an entire week
                    manually entering data from PDF statements.
                </p>
                <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                    After implementing VaultCaddy, processing time dropped from 40 hours to just 2 hours per month.
                    Accuracy improved from 85% to 98%. The firm now saves $18,000 per month in labor costs,
                    equivalent to $216,000 annually. More importantly, their CPAs can now focus on high-value
                    tax planning and advisory services instead of data entry.
                </p>
            </div>
            
            <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
                <h3 style="color: #1f2937; margin-bottom: 1rem;">🍽️ Case Study: Multi-location Restaurant Chain</h3>
                <p style="line-height: 1.8; color: #4b5563;">
                    "Taste of Home" restaurant group operates 8 locations across California.
                    Each location maintains separate bank accounts with Chase, Bank of America, and Wells Fargo.
                    CFO Sarah Martinez previously spent 3 days each month consolidating cash flow data
                    from all locations to create unified financial reports.
                </p>
                <p style="line-height: 1.8; color: #4b5563; margin-top: 1rem;">
                    Manual data entry led to frequent discrepancies between locations. With VaultCaddy,
                    restaurant managers simply photograph statements with their phones and upload.
                    Report compilation time decreased from 3 days to 4 hours with virtually zero errors.
                    Real-time cash flow visibility enables optimized purchasing and staffing decisions.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                    <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">98%</div>
                    <div style="color: #6b7280;">Accuracy Rate</div>
                    <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">Supports all major banks</div>
                </div>
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                    <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">3sec</div>
                    <div style="color: #6b7280;">Processing Speed</div>
                    <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">Photo upload & done</div>
                </div>
                <div style="background: white; border: 2px solid #e5e7eb; padding: 1.5rem; border-radius: 8px;">
                    <div style="font-size: 2.5rem; color: #667eea; font-weight: 800;">$46</div>
                    <div style="color: #6b7280;">Monthly Plan</div>
                    <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">300x cheaper than manual</div>
                </div>
            </div>
        </div>
    </section>
'''
        
        # 5. 重新查找FAQ结束位置（因为content已改变）
        faq_match = re.search(r'(<!-- FAQ Section -->)', content)
        faq_start = faq_match.start()
        after_faq = content[faq_start:]
        faq_section_end_match = re.search(r'</section>', after_faq)
        faq_end_pos = faq_start + faq_section_end_match.end()
        
        # 6. 在FAQ后插入
        content = content[:faq_end_pos] + '\n' + case_section + '\n' + content[faq_end_pos:]
        
        # 保存
        with open(file_path + '.backup_simple', 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, [f'移除{removed_count}个重复案例', '在FAQ后添加案例']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取英文银行页面
files = glob.glob('en/*-bank-statement.html')
files.sort()

print("=" * 70)
print("🔧 修复英文银行页面（简单直接法）")
print("=" * 70)
print()
print(f"找到 {len(files)} 个英文银行页面")
print()

processed = 0
for i, file_path in enumerate(files, 1):
    success, messages = simple_fix(file_path)
    
    if success:
        processed += 1
        print(f"✅ [{i}/{len(files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        print(f"⏭️  [{i}/{len(files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print(f"✅ 已处理：{processed}/{len(files)} 个文件")
print("🎉 完成！")

