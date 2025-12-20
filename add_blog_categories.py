#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为多语言博客页面添加分类标签功能
参考中文版：https://vaultcaddy.com/blog/
"""

import re

# 文章分类映射
ARTICLE_CATEGORIES = {
    'manual-vs-ai-cost-analysis': 'all',  # 精选文章
    'personal-bookkeeping-best-practices': 'freelancer',
    'freelancer-invoice-management': 'freelancer',
    'freelancer-tax-preparation': 'freelancer',
    'ai-invoice-processing-guide': 'smb',
    'ai-invoice-processing-small-business': 'smb',
    'accounting-firm-automation': 'accountant',
    'accounting-workflow-optimization': 'accountant',
    'automate-financial-documents': 'smb',
    'best-pdf-to-excel-converter': 'smb',
    'client-document-management': 'accountant',
    'how-to-convert-pdf-bank-statement': 'smb',
    'ocr-accuracy-for-accounting': 'accountant',
    'ocr-technology-for-accountants': 'accountant',
    'quickbooks-integration-guide': 'smb',
    'small-business-document-management': 'smb',
}

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

# 分类标签CSS
CATEGORY_CSS = """
        .blog-categories {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }
        .category-tag {
            padding: 0.5rem 1.5rem;
            border-radius: 24px;
            background: #f3f4f6;
            color: #4b5563;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.938rem;
            font-weight: 500;
        }
        .category-tag:hover, .category-tag.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
"""

# 分类标签JavaScript
CATEGORY_JS = """
    <script>
        // 分類篩選功能
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.category-tag').forEach(tag => {
                tag.addEventListener('click', function() {
                    // 更新活動標籤
                    document.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                    this.classList.add('active');

                    const category = this.dataset.category;
                    
                    // 篩選文章
                    document.querySelectorAll('.blog-card').forEach(card => {
                        if (category === 'all' || card.dataset.category === category || card.dataset.category === 'all') {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });
        });
    </script>
"""

def add_categories_to_blog(file_path, language):
    """为博客索引页添加分类标签功能"""
    
    print(f"\n🔧 处理 {language.upper()} 版博客...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 检查是否已经有分类CSS
    if '.blog-categories' not in content:
        # 在</style>前添加分类CSS
        style_end = content.rfind('</style>')
        if style_end != -1:
            content = content[:style_end] + CATEGORY_CSS + '\n    ' + content[style_end:]
            changes.append("✅ 添加分类CSS")
    
    # 2. 添加分类标签HTML
    if 'blog-categories' not in content and 'category-tag' not in content:
        # 查找blog-hero section之后的位置
        search_str = '</section>\n    \n    <div class="blog-grid">'
        
        if search_str in content:
            categories_html = f'''</section>
    
    <div class="blog-categories">
        <div class="category-tag active" data-category="all">{CATEGORY_LABELS[language]['all']}</div>
        <div class="category-tag" data-category="freelancer">{CATEGORY_LABELS[language]['freelancer']}</div>
        <div class="category-tag" data-category="smb">{CATEGORY_LABELS[language]['smb']}</div>
        <div class="category-tag" data-category="accountant">{CATEGORY_LABELS[language]['accountant']}</div>
    </div>
    
    <div class="blog-grid">'''
            
            content = content.replace(search_str, categories_html)
            changes.append("✅ 添加分类标签HTML")
    
    # 3. 为每个博客卡片添加data-category属性
    added_categories = 0
    for article_slug, category in ARTICLE_CATEGORIES.items():
        # 查找href包含该文章的blog-card
        pattern = f'<a href="{article_slug}.html" class="blog-card"'
        if pattern in content:
            replacement = f'<a href="{article_slug}.html" class="blog-card" data-category="{category}"'
            new_content = content.replace(pattern, replacement)
            if new_content != content:
                content = new_content
                added_categories += 1
    
    if added_categories > 0:
        changes.append(f"✅ 为 {added_categories} 篇文章添加分类标签")
    
    # 4. 添加JavaScript筛选功能
    if '分類篩選功能' not in content and '分类筛选功能' not in content and 'Category filter' not in content:
        # 在</body>前添加JavaScript
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + '\n' + CATEGORY_JS + '\n' + content[body_end:]
            changes.append("✅ 添加筛选JavaScript")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if changes:
        for change in changes:
            print(f"   {change}")
    else:
        print("   ℹ️  无需更改（已存在分类功能）")
    
    print(f"✅ {language.upper()} 版博客处理完成")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              为多语言博客添加分类标签功能                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    total_changes = 0
    
    # 英文版
    print("\n" + "="*70)
    print("📝 English (en)")
    print("="*70)
    total_changes += add_categories_to_blog('en/blog/index.html', 'en')
    
    # 日文版
    print("\n" + "="*70)
    print("📝 Japanese (jp)")
    print("="*70)
    total_changes += add_categories_to_blog('jp/blog/index.html', 'jp')
    
    # 韩文版
    print("\n" + "="*70)
    print("📝 Korean (kr)")
    print("="*70)
    total_changes += add_categories_to_blog('kr/blog/index.html', 'kr')
    
    # 总结
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   总修改项: {total_changes} 处")
    print(f"\n✨ 新增功能：")
    print(f"   ✅ 分类标签（全部文章、个人/自由职业者、小型企业、会计事务所）")
    print(f"   ✅ 点击标签筛选文章")
    print(f"   ✅ 美观的交互效果")
    print(f"\n🌐 请访问以下页面验证效果：")
    print(f"   - https://vaultcaddy.com/en/blog/")
    print(f"   - https://vaultcaddy.com/jp/blog/")
    print(f"   - https://vaultcaddy.com/kr/blog/")
    print(f"   - https://vaultcaddy.com/blog/ (参考)")

if __name__ == '__main__':
    main()

