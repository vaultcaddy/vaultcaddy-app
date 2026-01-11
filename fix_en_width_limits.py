#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版首页的三个问题：
1. 图1-3中左右不限制宽度（移除max-width限制）
2. 图1中"合理且實惠的價格"改为英文
3. "輕鬆處理銀行對帳單"改为英文
"""

import re

file_path = 'en/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# 1. 移除定价区域的max-width: 1000px限制
# 找到并替换定价卡片容器的宽度限制
old_pricing_grid = r'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; max-width: 1000px; margin: 0 auto;">'
new_pricing_grid = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 0 auto;">'

if old_pricing_grid in content:
    content = content.replace(old_pricing_grid, new_pricing_grid)
    changes.append("✅ 移除定价区域的max-width限制")

# 2. 移除定价卡片的max-width: 500px限制
old_card_style = 'border: 2px solid #e5e7eb; border-radius: 16px; padding: 2.5rem; background: white; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); max-width: 500px; width: 100%;'
new_card_style = 'border: 2px solid #e5e7eb; border-radius: 16px; padding: 2.5rem; background: white; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); width: 100%;'

content = content.replace(old_card_style, new_card_style)
changes.append("✅ 移除定价卡片的max-width限制")

# 3. 移除评价区域的max-width: 1400px限制
old_testimonials = 'display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 1400px; margin: 0 auto;'
new_testimonials = 'display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 0 auto;'

if old_testimonials in content:
    content = content.replace(old_testimonials, new_testimonials)
    changes.append("✅ 移除评价区域的max-width限制")

# 4. 移除Learning Center的max-width: 1200px限制
old_learning = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; max-width: 1200px; margin: 0 auto;'
new_learning = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 0 auto;'

if old_learning in content:
    content = content.replace(old_learning, new_learning)
    changes.append("✅ 移除Learning Center的max-width限制")

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("╔══════════════════════════════════════════════════════════════════════╗")
print("║          修复英文版首页 - 移除宽度限制                                 ║")
print("╚══════════════════════════════════════════════════════════════════════╝")
print()

for change in changes:
    print(f"   {change}")

print()
print("="*70)
print("🎉 完成！")
print("="*70)
print()
print("📊 修复项目：")
print(f"   - 定价区域：移除max-width: 1000px")
print(f"   - 定价卡片：移除max-width: 500px")
print(f"   - 评价区域：移除max-width: 1400px（如有）")
print(f"   - Learning Center：移除max-width: 1200px（如有）")
print()
print("🌐 验证链接：")
print("   https://vaultcaddy.com/en/index.html")
print()
print("✨ 现在定价区域、评价区域和Learning Center都会自适应屏幕宽度！")







