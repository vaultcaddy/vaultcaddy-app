#!/usr/bin/env python3
"""
修復博客頁面左側欄樣式
添加 sidebar-link 和 sidebar-nav 的 CSS
"""

import re
import os

blog_pages = [
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html'
]

def add_sidebar_css(content):
    """添加 sidebar-nav 和 sidebar-link 的 CSS"""
    
    # 查找 .article-list a.active 的位置
    pattern = r'(\.article-list a\.active \{[^}]+\})'
    
    if not re.search(pattern, content):
        print('  ⚠ 找不到 .article-list a.active')
        return content
    
    # 在 .article-list a.active 後面添加新的 CSS
    sidebar_css = '''
        
        /* 側邊欄導航樣式 */
        .sidebar-nav {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .sidebar-link {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            color: #6b7280;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.2s;
            font-size: 0.9rem;
        }
        
        .sidebar-link:hover {
            background: #f3f4f6;
            color: #667eea;
        }
        
        .sidebar-link.active {
            background: #eff6ff;
            color: #667eea;
            font-weight: 600;
        }
        
        .sidebar-link i {
            width: 20px;
            text-align: center;
            color: #667eea;
            font-size: 1rem;
        }
        
        .sidebar-link span {
            flex: 1;
        }'''
    
    replacement = r'\1' + sidebar_css
    content = re.sub(pattern, replacement, content)
    print('  ✓ 添加 sidebar CSS')
    
    return content

def remove_emoji_from_title(content):
    """移除標題中的 emoji"""
    # 移除 📚 emoji
    content = content.replace('<h3>📚 文章導航</h3>', '<h3>文章導航</h3>')
    content = content.replace('<h4 style="margin-bottom: 0.5rem; font-size: 1.125rem;">💡 需要幫助？</h4>', 
                            '<h4 style="margin-bottom: 0.5rem; font-size: 1.125rem;">需要幫助？</h4>')
    print('  ✓ 移除 emoji')
    return content

def process_file(filepath):
    """處理單個文件"""
    print(f'\n處理: {filepath}')
    
    if not os.path.exists(filepath):
        print(f'  ⚠ 文件不存在')
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 添加 sidebar CSS
        content = add_sidebar_css(content)
        
        # 2. 移除 emoji
        content = remove_emoji_from_title(content)
        
        # 只在內容有變化時寫入
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  ✅ 更新完成')
            return True
        else:
            print(f'  ⏭️  無需更新')
            return False
    except Exception as e:
        print(f'  ❌ 處理時出錯: {e}')
        return False

def main():
    print('🚀 開始修復博客頁面左側欄...\n')
    
    success_count = 0
    for page in blog_pages:
        if process_file(page):
            success_count += 1
    
    print(f'\n✅ 完成！成功更新 {success_count}/{len(blog_pages)} 個文件')

if __name__ == '__main__':
    main()

