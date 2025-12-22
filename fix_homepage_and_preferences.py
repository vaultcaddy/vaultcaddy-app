#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复3个问题：
1. 恢复英文版首页缺失的"Why Choose"和"Pricing"部分
2. 删除4个版本account.html中的Preferences部分
"""

import re

print("🔧 开始修复...")
print("="*70)

# ============================================================
# 任务1: 恢复英文版首页缺失的内容
# ============================================================
print("\n📝 任务1: 检查英文版首页缺失内容...")

with open('en/index.html', 'r', encoding='utf-8') as f:
    en_content = f.read()

# 检查是否缺少"Why Choose"部分
has_why_choose = 'Why Choose VaultCaddy' in en_content or 'id="why-choose"' in en_content
has_pricing = 'FAIR AND AFFORDABLE' in en_content or 'Fair and Affordable' in en_content

if not has_why_choose or not has_pricing:
    print("  ❌ 发现英文版首页缺少内容")
    print(f"     Why Choose section: {'✓' if has_why_choose else '✗ 缺失'}")
    print(f"     Pricing section: {'✓' if has_pricing else '✗ 缺失'}")
    
    # 读取中文版的完整内容作为参考
    with open('index.html', 'r', encoding='utf-8') as f:
        zh_content = f.read()
    
    # 提取"Why Choose"部分（从SECTION_2_START到pricing section）
    why_choose_match = re.search(
        r'<!-- 🎨 SECTION_2_START 為什麼選擇 VaultCaddy -->.*?</section>',
        zh_content,
        re.DOTALL
    )
    
    # 提取Pricing部分（从pricing section到用户评价）
    pricing_match = re.search(
        r'<!-- 價格區域 -->.*?</section>\s*<!-- 客戶評價區域',
        zh_content,
        re.DOTALL
    )
    
    if why_choose_match and pricing_match:
        why_choose_html = why_choose_match.group(0)
        pricing_html = pricing_match.group(0).replace('<!-- 客戶評價區域', '')
        
        # 翻译为英文版本
        # Why Choose部分
        why_choose_en = why_choose_html
        why_choose_en = why_choose_en.replace('為什麼選擇 VaultCaddy', 'Why Choose VaultCaddy')
        why_choose_en = why_choose_en.replace('專為香港會計師打造', 'Built for Accountants')
        why_choose_en = why_choose_en.replace('提升效率，降低成本，讓您專注於更有價值的工作', 'Increase efficiency, reduce costs, focus on more valuable work')
        why_choose_en = why_choose_en.replace('極速處理', 'Ultra-Fast Processing')
        why_choose_en = why_choose_en.replace('平均 <strong style="color: #10b981;">10 秒</strong>完成一份文檔', 'Average <strong style="color: #10b981;">10s</strong> to complete one document')
        why_choose_en = why_choose_en.replace('批量處理更快更省時', 'Batch processing faster and more time-saving')
        why_choose_en = why_choose_en.replace('節省 <strong style="color: #10b981;">90% 人工輸入</strong>時間', 'Save <strong style="color: #10b981;">90%</strong> manual input time')
        why_choose_en = why_choose_en.replace('超高準確率', 'Highest Accuracy')
        why_choose_en = why_choose_en.replace('AI 辨識準確率達 <strong style="color: #667eea;">98%</strong>', 'AI recognition accuracy reaches <strong style="color: #667eea;">98%</strong>')
        why_choose_en = why_choose_en.replace('自動驗證和校正錯誤', 'Automatic verification and error correction')
        why_choose_en = why_choose_en.replace('大幅降低人為失誤風險', 'Greatly reduce human error risk')
        why_choose_en = why_choose_en.replace('性價比最高', 'Fair and Affordable')
        why_choose_en = why_choose_en.replace('每頁低至 <strong style="color: #f59e0b;">HKD 0.5</strong>', 'From <strong style="color: #f59e0b;">$0.06</strong> per page')
        why_choose_en = why_choose_en.replace('無隱藏收費', 'No hidden fees')
        why_choose_en = why_choose_en.replace('用多少付多少最靈活', 'Pay only for what you use')
        
        # Pricing部分
        pricing_en = pricing_html
        pricing_en = pricing_en.replace('合理且實惠的價格', 'FAIR AND AFFORDABLE PRICING')
        pricing_en = pricing_en.replace('輕鬆處理銀行對帳單', 'Easy Bank Statement Processing')
        pricing_en = pricing_en.replace('與數千家企業一起，節省財務數據錄入的時間。無隱藏費用，隨時取消。', 'Join thousands of businesses saving time on financial data entry. No hidden fees, cancel anytime.')
        pricing_en = pricing_en.replace('月付', 'Monthly')
        pricing_en = pricing_en.replace('年付', 'Yearly')
        pricing_en = pricing_en.replace('HKD $58', 'USD $ 6.99')
        pricing_en = pricing_en.replace('HKD $46', 'USD $ 5.59')
        pricing_en = pricing_en.replace('/月', '/month')
        pricing_en = pricing_en.replace('頁面包含', "What's Included")
        pricing_en = pricing_en.replace('每月 100 Credits', '100 Credits per month')
        pricing_en = pricing_en.replace('每年 1,200 Credits', '1,200 Credits per year')
        pricing_en = pricing_en.replace('超出後每頁 HKD $0.5', 'Then USD $0.06 per page')
        pricing_en = pricing_en.replace('批次處理無限制文件', 'Unlimited Batch Processing')
        pricing_en = pricing_en.replace('一鍵轉換所有文件', 'One-Click Convert All')
        pricing_en = pricing_en.replace('複合式 AI 處理', 'Hybrid AI Processing')
        pricing_en = pricing_en.replace('8 種語言支援', '8 Languages Support')
        pricing_en = pricing_en.replace('電子郵件支援', 'Email Support')
        pricing_en = pricing_en.replace('安全文件上傳', 'Secure File Upload')
        pricing_en = pricing_en.replace('365 天數據保留', 'Data Retention')
        pricing_en = pricing_en.replace('30 天圖片保留', 'Image Backup')
        pricing_en = pricing_en.replace('開始使用', 'Get Started')
        pricing_en = pricing_en.replace('節省 20%', 'Save 20%')
        pricing_en = pricing_en.replace('billing.html', '../auth.html')
        
        # 找到插入位置（在"All-in-One"部分之后）
        insert_pos = en_content.find('<!-- 客戶評價區域')
        if insert_pos == -1:
            insert_pos = en_content.find('<section style="padding: 4rem 0; background: #f9fafb;">')
        
        if insert_pos != -1:
            # 插入内容
            new_content = (
                en_content[:insert_pos] +
                why_choose_en + '\n\n' +
                pricing_en + '\n\n        ' +
                en_content[insert_pos:]
            )
            
            with open('en/index.html', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("  ✅ 已恢复英文版首页缺失内容")
        else:
            print("  ⚠️  无法找到插入位置")
    else:
        print("  ⚠️  无法从中文版提取内容")
else:
    print("  ✓ 英文版首页内容完整")

# ============================================================
# 任务2: 删除4个版本account.html中的Preferences部分
# ============================================================
print("\n📝 任务2: 删除4个版本account.html中的Preferences部分...")

account_files = [
    'account.html',
    'en/account.html',
    'jp/account.html',
    'kr/account.html'
]

for file_path in account_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找Preferences部分（从<div class="account-section">到</div>）
    # 匹配包含"Preferences"或"偏好设置"等标题的section
    pattern = r'<div class="account-section"[^>]*>\s*<h2[^>]*>(?:Preferences|偏好設定|環境設定|設定|preferences|preference).*?</div>\s*</div>\s*</div>'
    
    if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        # 删除Preferences部分
        new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ {file_path} - 已删除Preferences部分")
    else:
        print(f"  ℹ️  {file_path} - 未找到Preferences部分")

print("\n" + "="*70)
print("🎉 修复完成！")
print("\n修改总结:")
print("  1. ✅ 恢复英文版首页缺失内容（Why Choose + Pricing）")
print("  2. ✅ 删除4个版本account.html中的Preferences部分")

