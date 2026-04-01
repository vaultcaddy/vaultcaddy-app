#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单方法：直接在HTML中查找并包裹特定内容"""

import re

print("=" * 70)
print("开始为文字内容添加视觉设计")
print("=" * 70)
print()

with open('hsbc-vs-manual.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('hsbc-vs-manual.html.backup_wrap', 'w', encoding='utf-8') as f:
    f.write(content)

modifications = 0

# 1. 为"关键发现"段落添加样式
pattern1 = r'(\*\*关键发现\*\*：\s*\n)((?:[-\d\.].*\n?)+)'
def wrap_key_findings(match):
    global modifications
    modifications += 1
    return f'<div class="key-findings">\n\n{match.group(0)}\n</div>\n'

content = re.sub(pattern1, wrap_key_findings, content)

# 2. 为用户场景添加样式
pattern2 = r'(\*\*场景\d+：[^\n]+\*\*\n)((?:[-\*].*\n?)+)'
def wrap_scenario(match):
    global modifications
    modifications += 1
    return f'<div class="scenario-card">\n\n{match.group(0)}\n</div>\n'

content = re.sub(pattern2, wrap_scenario, content)

# 3. 为真实案例添加样式（blockquote后面的署名）
pattern3 = r'(>\s*"[^"]+"\s*\n>\s*\n>\s*—\s*[^\n]+)'
def wrap_case_quote(match):
    global modifications
    modifications += 1
    # blockquote已经存在，只需要添加class
    return match.group(0)  # 保持原样，因为blockquote本身就有样式

content = re.sub(pattern3, wrap_case_quote, content)

# 保存
with open('hsbc-vs-manual.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已添加 {modifications} 处视觉设计包裹")
print()
print("=" * 70)
print("✅ 内容包裹完成！")
print("=" * 70)
print()
print("💡 实际上，让我们采用更直接的方法...")
print("   直接修改CSS样式，让现有内容自动获得更好的视觉效果")
print("=" * 70)

