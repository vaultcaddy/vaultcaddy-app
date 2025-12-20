#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复博客分类标签的格式问题
"""

import re

# 分类标签翻译
CATEGORY_LABELS = {
    'en': {
        'all': 'All Articles',
        'freelancer': 'Freelancers',
        'smb': 'Small Business',
        'accountant': 'Accounting Firms'
    },
    'jp': {
        'all': '全記事',
        'freelancer': '個人/フリーランサー',
        'smb': '中小企業',
        'accountant': '会計事務所'
    },
    'kr': {
        'all': '모든 글',
        'freelancer': '개인/프리랜서',
        'smb': '중소기업',
        'accountant': '회계 사무소'
    }
}

def fix_blog_categories(file_path, language):
    """修复博客分类标签"""
    
    print(f"\n🔧 修复 {language.upper()} 版博客...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 修复错误的data-category格式
    # 从: class="blog-card data-category="xxx"
    # 到: class="blog-card" data-category="xxx"
    pattern = r'class="blog-card\s+data-category="([^"]+)"'
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(
            r'class="blog-card\s+data-category="([^"]+)"',
            r'class="blog-card" data-category="\1"',
            content
        )
        changes.append(f"✅ 修复 {len(matches)} 个data-category格式")
    
    # 2. 检查是否需要添加分类标签HTML
    if 'blog-categories' not in content or 'category-tag' not in content:
        # 查找 </section> 后面的 <div class="blog-grid">
        if '</section>\n    \n    <div class="blog-grid">' in content:
            old_html = '</section>\n    \n    <div class="blog-grid">'
            new_html = f'''</section>
    
    <div class="blog-categories">
        <div class="category-tag active" data-category="all">{CATEGORY_LABELS[language]['all']}</div>
        <div class="category-tag" data-category="freelancer">{CATEGORY_LABELS[language]['freelancer']}</div>
        <div class="category-tag" data-category="smb">{CATEGORY_LABELS[language]['smb']}</div>
        <div class="category-tag" data-category="accountant">{CATEGORY_LABELS[language]['accountant']}</div>
    </div>
    
    <div class="blog-grid">'''
            content = content.replace(old_html, new_html)
            changes.append("✅ 添加分类标签HTML")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if changes:
        for change in changes:
            print(f"   {change}")
    else:
        print("   ℹ️  格式正确，无需修复")
    
    print(f"✅ {language.upper()} 版博客修复完成")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              修复博客分类标签格式问题                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    total_changes = 0
    
    # 英文版
    print("\n" + "="*70)
    print("📝 English (en)")
    print("="*70)
    total_changes += fix_blog_categories('en/blog/index.html', 'en')
    
    # 日文版
    print("\n" + "="*70)
    print("📝 Japanese (jp)")
    print("="*70)
    total_changes += fix_blog_categories('jp/blog/index.html', 'jp')
    
    # 韩文版
    print("\n" + "="*70)
    print("📝 Korean (kr)")
    print("="*70)
    total_changes += fix_blog_categories('kr/blog/index.html', 'kr')
    
    # 总结
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   总修复项: {total_changes} 处")
    print(f"\n🌐 请访问以下页面验证效果：")
    print(f"   - https://vaultcaddy.com/en/blog/")
    print(f"   - https://vaultcaddy.com/jp/blog/")
    print(f"   - https://vaultcaddy.com/kr/blog/")

if __name__ == '__main__':
    main()

