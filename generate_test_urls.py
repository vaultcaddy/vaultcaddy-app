#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""随机生成测试页面URL"""

import random
from pathlib import Path

# 获取所有v3页面
root = Path('/Users/cavlinyeung/ai-bank-parser')
base_url = 'https://vaultcaddy.com'

# 收集所有v3页面
all_pages = {
    'en': [],
    'zh-TW': [],
    'zh-HK': [],
    'ja-JP': [],
    'ko-KR': []
}

# 英文版（根目录）
for file in root.glob('*-v3.html'):
    if 'test' not in file.name and 'backup' not in file.name:
        all_pages['en'].append(f"{base_url}/{file.name}")

# 其他语言版本
for lang_dir in ['zh-TW', 'zh-HK', 'ja-JP', 'ko-KR']:
    lang_path = root / lang_dir
    if lang_path.exists():
        for file in lang_path.glob('*-v3.html'):
            if 'test' not in file.name and 'backup' not in file.name:
                all_pages[lang_dir].append(f"{base_url}/{lang_dir}/{file.name}")

# 从每个语言随机选择3-4个
test_urls = []
for lang, urls in all_pages.items():
    if urls:
        count = 4 if lang in ['en', 'zh-TW', 'zh-HK'] else 3
        selected = random.sample(urls, min(count, len(urls)))
        test_urls.extend(selected)

# 打乱顺序
random.shuffle(test_urls)

# 输出前15个
print("🔍 随机选择的15个测试页面：\n")
for i, url in enumerate(test_urls[:15], 1):
    # 提取语言标识
    if '/zh-TW/' in url:
        lang_flag = '🇹🇼'
    elif '/zh-HK/' in url:
        lang_flag = '🇭🇰'
    elif '/ja-JP/' in url:
        lang_flag = '🇯🇵'
    elif '/ko-KR/' in url:
        lang_flag = '🇰🇷'
    else:
        lang_flag = '🇺🇸'
    
    print(f"{i}. {lang_flag} {url}")

# 保存到文件供Chrome MCP使用
with open('/Users/cavlinyeung/ai-bank-parser/test_urls.txt', 'w') as f:
    for url in test_urls[:15]:
        f.write(url + '\n')

print(f"\n✅ 已保存到 test_urls.txt")
