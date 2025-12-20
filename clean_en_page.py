#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 en/index.html 页面内容并优化SEO
"""

import re

# 读取文件
with open('/Users/cavlinyeung/ai-bank-parser/en/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔧 开始修改 en/index.html...")

# 1. 修改第一个横幅（中文改为英文）
content = re.sub(
    r'⚡ 限時優惠：本月註冊立享 8 折！<span[^>]*>優惠碼：SAVE20</span> 已有 <span[^>]*>237</span> 位香港會計師加入',
    '⚡ Limited Offer: 20% OFF This Month! <span style="background: white; color: #f59e0b; padding: 0.25rem 1rem; border-radius: 20px; margin-left: 1rem; font-weight: 700;">Code: SAVE20</span> Join <span style="font-size: 1.125rem; font-weight: 700;">237</span> accounting professionals worldwide',
    content
)
print("✅ 1. 第一个优惠横幅已改为英文")

# 2. 删除第二个横幅
content = re.sub(
    r'<!-- Urgency Banner -->\s*<div[^>]*>\s*⚡ Limited Offer: Get 20%[^<]*<[^>]*>180\+</span>[^<]*</div>\s*',
    '',
    content,
    flags=re.DOTALL
)
print("✅ 2. 第二个优惠横幅已删除")

# 3. 删除整个 "Trusted by CPAs Across America" section
# 找到这个section的开始和结束
pattern = r'<h3[^>]*>\s*Trusted by CPAs Across America\s*</h3>.*?(?=<section|<div class="container"|<!-- 準備好開始了嗎？ -->)'
content = re.sub(pattern, '', content, flags=re.DOTALL)
print("✅ 3. Trusted by CPAs Across America 部分已删除")

# 4. 将 "合理且實惠的價格" 和 "輕鬆處理銀行對帳單" 改为英文
content = content.replace('合理且實惠的價格', 'Fair and Affordable Pricing')
content = content.replace('輕鬆處理銀行對帳單', 'Easy Bank Statement Processing')
print("✅ 4. 价格标题已改为英文")

# 5. 删除任何可能残留的测试 API keys（如果存在）
# 搜索常见的 Stripe key 格式并替换
content = re.sub(r'sk_(test|live)_[A-Za-z0-9]{99,}', 'REDACTED_API_KEY', content)
print("✅ 5. API keys 已移除（如有）")

# 保存文件
with open('/Users/cavlinyeung/ai-bank-parser/en/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 所有修改完成！")
print("\n修改摘要：")
print("1. ✅ 第一个横幅改为英文")
print("2. ✅ 删除第二个冗余横幅")
print("3. ✅ 删除美国CPA见证部分")
print("4. ✅ 价格标题改为英文")
print("5. ✅ 清理API keys")

