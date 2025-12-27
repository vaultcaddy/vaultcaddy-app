#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动为hsbc-vs-manual.html的内容添加CSS类"""

from bs4 import BeautifulSoup
import re

print("=" * 70)
print("开始为内容添加CSS类")
print("=" * 70)
print()

with open('hsbc-vs-manual.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 找到主要内容区域
content_div = soup.find('div', class_='content')
if not content_div:
    print("❌ 未找到内容区域")
    exit(1)

# 统计修改
modifications = {
    'key_findings': 0,
    'case_quotes': 0,
    'scenario_cards': 0,
    'comparison_results': 0
}

# 1. 为"关键发现"添加key-findings类
for element in content_div.find_all(['p', 'div']):
    text = element.get_text()
    if '**关键发现**' in text or '关键发现：' in text:
        # 查找包含关键发现的完整段落
        parent = element.parent
        if parent and parent.name in ['div', 'section']:
            parent['class'] = parent.get('class', []) + ['key-findings']
            modifications['key_findings'] += 1
        else:
            # 创建一个新的div包裹
            new_div = soup.new_tag('div', **{'class': 'key-findings'})
            element.wrap(new_div)
            modifications['key_findings'] += 1

# 2. 为引用（blockquote）添加case-quote类
for blockquote in content_div.find_all('blockquote'):
    blockquote['class'] = blockquote.get('class', []) + ['case-quote']
    modifications['case_quotes'] += 1

# 3. 为场景描述添加scenario-card类
# 查找包含"场景1"、"场景2"等的段落
for element in content_div.find_all(['p', 'div', 'ul']):
    text = element.get_text()
    if re.search(r'\*\*场景\d+', text) or re.search(r'场景\d+：', text):
        # 创建scenario-card包裹
        if element.name == 'ul':
            # 如果是列表，包裹整个列表
            new_div = soup.new_tag('div', **{'class': 'scenario-card'})
            element.wrap(new_div)
            modifications['scenario_cards'] += 1
        elif element.parent.name != 'div' or 'scenario-card' not in element.parent.get('class', []):
            # 如果不是已经在scenario-card中，创建新的
            new_div = soup.new_tag('div', **{'class': 'scenario-card'})
            element.wrap(new_div)
            modifications['scenario_cards'] += 1

# 4. 为对比结果添加comparison-result类
for element in content_div.find_all(['p', 'div']):
    text = element.get_text()
    if '**节省对比**' in text or '节省对比：' in text:
        parent = element.parent
        if parent and parent.name in ['div', 'section']:
            parent['class'] = parent.get('class', []) + ['comparison-result']
            modifications['comparison_results'] += 1

# 保存修改
with open('hsbc-vs-manual.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("✅ 已应用CSS类到内容")
print()
print("=" * 70)
print("📊 修改统计：")
print("=" * 70)
print(f"   关键发现框：{modifications['key_findings']} 个")
print(f"   案例引用框：{modifications['case_quotes']} 个")
print(f"   场景卡片：{modifications['scenario_cards']} 个")
print(f"   对比结果框：{modifications['comparison_results']} 个")
print()
print("=" * 70)
print("✅ 内容美化完成！")
print("=" * 70)
print()
print("💡 下一步：")
print("   1. 上传修复后的文件到服务器")
print("   2. 清除浏览器缓存")
print("   3. 验证视觉效果")
print("=" * 70)

