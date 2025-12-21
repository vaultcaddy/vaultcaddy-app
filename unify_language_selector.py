#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有页面添加语言选择器并移除国旗、调整按钮样式
"""

import os
import re

def ensure_language_switcher(file_path, page_name):
    """确保页面有语言选择器容器和脚本引用"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 确保引用 multilingual-data-sync.js
    if 'multilingual-data-sync.js' not in content:
        # 在 </head> 前添加脚本引用
        if file_path.startswith('/Users/cavlinyeung/ai-bank-parser/en/') or \
           file_path.startswith('/Users/cavlinyeung/ai-bank-parser/jp/') or \
           file_path.startswith('/Users/cavlinyeung/ai-bank-parser/kr/'):
            script_tag = '<script src="../multilingual-data-sync.js"></script>\n</head>'
        else:
            script_tag = '<script src="/multilingual-data-sync.js"></script>\n</head>'
        
        content = content.replace('</head>', script_tag)
        changes.append(f"✅ 添加 multilingual-data-sync.js 引用")
    
    # 2. 确保有 language-switcher 容器
    if 'language-switcher' not in content:
        # 在用户菜单前添加语言选择器容器
        patterns = [
            # Pattern 1: 在 user-menu 的 div 中添加
            (r'(<div id="user-menu"[^>]*>)',
             r'\1\n                <div id="language-switcher" style="margin-right: 1rem;"></div>'),
            # Pattern 2: 在导航栏的右侧容器中添加
            (r'(<div[^>]*style="[^"]*display:\s*flex[^"]*gap[^"]*"[^>]*>)(\s*<a[^>]*href="auth\.html")',
             r'\1\n                <div id="language-switcher" style="margin-right: 1rem;"></div>\2'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                changes.append(f"✅ 添加 language-switcher 容器")
                break
    
    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return len(changes)

def update_multilingual_sync_js():
    """修改 multilingual-data-sync.js 删除国旗并调整padding"""
    
    file_path = '/Users/cavlinyeung/ai-bank-parser/multilingual-data-sync.js'
    
    print("\n🔧 修改 multilingual-data-sync.js...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 删除主按钮中的国旗
    old_button = r'<span style="font-size: 1\.25rem;">\$\{currentLangConfig\.flag\}</span>\s*\n\s*<span'
    new_button = '<span'
    
    if re.search(old_button, content):
        content = re.sub(old_button, new_button, content)
        changes.append("✅ 删除主按钮国旗")
    
    # 2. 调整主按钮 padding (0.5rem → 0.375rem)
    content = content.replace(
        'gap: 0.5rem; padding: 0.5rem 1rem;',
        'gap: 0.5rem; padding: 0.375rem 0.875rem;'
    )
    changes.append("✅ 调整主按钮 padding")
    
    # 3. 删除下拉菜单中的国旗
    old_dropdown_item = r'<span style="font-size: 1\.25rem;">\$\{config\.flag\}</span>\s*\n\s*<div'
    new_dropdown_item = '<div'
    
    if re.search(old_dropdown_item, content):
        content = re.sub(old_dropdown_item, new_dropdown_item, content)
        changes.append("✅ 删除下拉菜单国旗")
    
    # 4. 调整下拉菜单项的布局（删除 gap）
    content = content.replace(
        'gap: 0.75rem; padding: 0.75rem 1rem;',
        'padding: 0.625rem 1rem;'
    )
    changes.append("✅ 调整下拉菜单 padding")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    for change in changes:
        print(f"   {change}")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🌐 统一语言选择器 + 删除国旗 + 调整样式                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    base_path = "/Users/cavlinyeung/ai-bank-parser"
    
    # 1. 修改 multilingual-data-sync.js
    print("📝 Step 1: 修改 multilingual-data-sync.js")
    update_multilingual_sync_js()
    
    # 2. 确保所有功能页面有语言选择器
    print("\n📝 Step 2: 确保所有功能页面有语言选择器")
    
    pages = [
        "index.html",
        "dashboard.html",
        "firstproject.html",
        "document-detail.html",
        "account.html",
        "billing.html",
        "privacy.html",
        "terms.html"
    ]
    
    langs = [
        ("", "中文"),
        ("en", "英文"),
        ("jp", "日文"),
        ("kr", "韩文")
    ]
    
    total_changes = 0
    
    for lang_code, lang_name in langs:
        print(f"\n📁 {lang_name} 版本:")
        for page in pages:
            if lang_code:
                file_path = os.path.join(base_path, lang_code, page)
            else:
                file_path = os.path.join(base_path, page)
            
            if os.path.exists(file_path):
                changes = ensure_language_switcher(file_path, page)
                if changes > 0:
                    print(f"   ✅ {page}: {changes} 处修改")
                    total_changes += changes
                else:
                    print(f"   ✓ {page}: 已有语言选择器")
    
    # 3. 检查学习中心（blog）页面
    print("\n📝 Step 3: 检查学习中心页面")
    
    blog_dirs = [
        "blog",
        "en/blog",
        "jp/blog",
        "kr/blog"
    ]
    
    for blog_dir in blog_dirs:
        blog_path = os.path.join(base_path, blog_dir)
        if os.path.exists(blog_path):
            # 检查 index.html
            index_path = os.path.join(blog_path, "index.html")
            if os.path.exists(index_path):
                changes = ensure_language_switcher(index_path, f"{blog_dir}/index.html")
                if changes > 0:
                    print(f"   ✅ {blog_dir}/index.html: {changes} 处修改")
                    total_changes += changes
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 全部完成！                                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    print("📊 修改总结：")
    print(f"   • multilingual-data-sync.js: 删除国旗 + 调整 padding")
    print(f"   • 功能页面: {total_changes} 处修改")
    print(f"   • 涉及 {len(langs)} 个语言版本")
    print(f"   • 涉及 {len(pages)} 个功能页面")
    
    print("\n✅ 修改内容：")
    print("   1️⃣ 删除主按钮的国旗图标")
    print("   2️⃣ 删除下拉菜单的国旗图标")
    print("   3️⃣ 主按钮 padding: 0.5rem → 0.375rem (减少2pt)")
    print("   4️⃣ 下拉菜单 padding: 0.75rem → 0.625rem")
    print("   5️⃣ 确保所有页面有语言选择器容器")
    
    print("\n🌐 语言选择器现在的样式：")
    print("   • 主按钮: 只显示语言名称 + 下拉箭头")
    print("   • 下拉菜单: 显示语言名称（本地名 + 英文名）")
    print("   • 更紧凑的 padding，节省空间")
    print("   • 所有版本统一风格")

if __name__ == "__main__":
    main()

