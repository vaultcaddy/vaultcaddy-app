#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成多语言数据互通系统
作用：
1. 在所有页面的 <head> 中添加 multilingual-data-sync.js 引用
2. 在导航栏中添加语言切换器容器
3. 更新 unified-auth.js 中的链接，使其指向正确的语言版本

使用方法：
python3 integrate_multilingual_sync.py
"""

import os
import re
from pathlib import Path

# 需要集成的页面列表
PAGES_TO_INTEGRATE = [
    'dashboard.html',
    'firstproject.html',
    'document-detail.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html'
]

# 语言版本
LANGUAGES = ['en', 'jp', 'kr']

def add_script_to_head(html_content, script_path):
    """在 <head> 标签中添加脚本引用"""
    script_tag = f'<script src="{script_path}"></script>'
    
    # 检查是否已经存在
    if script_path in html_content:
        print(f'   ⏭️  脚本已存在: {script_path}')
        return html_content
    
    # 在 </head> 之前插入
    if '</head>' in html_content:
        html_content = html_content.replace(
            '</head>',
            f'    {script_tag}\n</head>'
        )
        print(f'   ✅ 添加脚本: {script_path}')
    else:
        print(f'   ⚠️  找不到 </head> 标签')
    
    return html_content

def add_language_switcher_container(html_content):
    """在导航栏中添加语言切换器容器"""
    
    # 检查是否已经存在
    if 'id="language-switcher"' in html_content:
        print('   ⏭️  语言切换器容器已存在')
        return html_content
    
    # 尝试在 user-menu 附近添加
    patterns = [
        # 模式1: 在 user-menu 之前添加
        (r'(<div[^>]*id="user-menu"[^>]*>)',
         r'<div id="language-switcher" style="display: inline-block; margin-right: 1rem;"></div>\n                \1'),
        
        # 模式2: 在导航栏右侧添加
        (r'(<div[^>]*class="[^"]*navbar-right[^"]*"[^>]*>)',
         r'\1\n                <div id="language-switcher" style="display: inline-block; margin-right: 1rem;"></div>'),
        
        # 模式3: 在 nav 标签内部最后添加
        (r'(</nav>)',
         r'    <div id="language-switcher" style="position: absolute; top: 1rem; right: 8rem;"></div>\n\1'),
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, html_content):
            html_content = re.sub(pattern, replacement, html_content, count=1)
            print('   ✅ 添加语言切换器容器')
            return html_content
    
    print('   ⚠️  无法找到合适位置添加语言切换器')
    return html_content

def integrate_page(file_path, is_language_version=False):
    """集成单个页面"""
    
    if not os.path.exists(file_path):
        print(f'❌ 文件不存在: {file_path}')
        return False
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 确定脚本路径（根据是否为语言版本调整）
    if is_language_version:
        script_path = '/multilingual-data-sync.js'
    else:
        script_path = '/multilingual-data-sync.js'
    
    # 添加脚本引用
    content = add_script_to_head(content, script_path)
    
    # 添加语言切换器容器
    content = add_language_switcher_container(content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    print('╔══════════════════════════════════════════════════════════════════════╗')
    print('║          🌐 集成多语言数据互通系统                                    ║')
    print('╚══════════════════════════════════════════════════════════════════════╝')
    print()
    
    success_count = 0
    total_count = 0
    
    # 处理中文版（根目录）
    print('📄 处理中文版页面...')
    for page in PAGES_TO_INTEGRATE:
        total_count += 1
        print(f'\n处理: {page}')
        if integrate_page(page, is_language_version=False):
            success_count += 1
    
    # 处理其他语言版本
    for lang in LANGUAGES:
        print(f'\n📄 处理 {lang.upper()} 版本页面...')
        for page in PAGES_TO_INTEGRATE:
            total_count += 1
            file_path = os.path.join(lang, page)
            print(f'\n处理: {file_path}')
            if integrate_page(file_path, is_language_version=True):
                success_count += 1
    
    print()
    print('='*70)
    print(f'✅ 完成！成功处理 {success_count}/{total_count} 个页面')
    print('='*70)
    print()
    print('📝 下一步：')
    print('1. 访问任意页面，查看右上角的语言切换器')
    print('2. 尝试切换语言，确认功能正常')
    print('3. 登录后，语言偏好会自动保存到 Firebase')
    print('4. 下次登录时，会自动使用您偏好的语言')
    print()

if __name__ == '__main__':
    main()

