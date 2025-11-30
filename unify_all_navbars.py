#!/usr/bin/env python3
"""
統一所有頁面的導航欄到 index.html 的版本
包括主要頁面和博客頁面
"""

import re
import os

# 主要頁面列表
main_pages = [
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html'
]

# 博客頁面列表
blog_pages = [
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html'
]

def extract_navbar_from_index():
    """從 index.html 提取導航欄模板"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 <nav> 到 </nav>
    nav_match = re.search(
        r'<nav[^>]*class="vaultcaddy-navbar"[^>]*>.*?</nav>',
        content,
        flags=re.DOTALL
    )
    
    if not nav_match:
        print("❌ 無法從 index.html 提取導航欄")
        return None
    
    navbar_html = nav_match.group(0)
    
    # 提取手機側邊欄（從 <!-- 手機側邊欄菜單 --> 到第一個完整的 </div></div>）
    mobile_match = re.search(
        r'<!-- 手機側邊欄菜單 -->.*?</div>\s*</div>',
        content,
        flags=re.DOTALL
    )
    
    mobile_sidebar_html = mobile_match.group(0) if mobile_match else ""
    
    return navbar_html, mobile_sidebar_html

def replace_navbar(filename, navbar_html, mobile_sidebar_html):
    """替換單個文件的導航欄"""
    try:
        if not os.path.exists(filename):
            print(f"⚠️  {filename} - 文件不存在，跳過")
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換導航欄
        content = re.sub(
            r'<nav[^>]*class="vaultcaddy-navbar"[^>]*>.*?</nav>',
            navbar_html,
            content,
            flags=re.DOTALL,
            count=1
        )
        
        # 替換手機側邊欄
        if mobile_sidebar_html:
            content = re.sub(
                r'<!-- 手機側邊欄菜單 -->.*?</div>\s*</div>',
                mobile_sidebar_html,
                content,
                flags=re.DOTALL,
                count=1
            )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename} - 導航欄已更新")
        return True
    except Exception as e:
        print(f"❌ {filename} - 錯誤: {e}")
        return False

def main():
    print("=" * 70)
    print("從 index.html 提取導航欄模板並統一到所有頁面...")
    print("=" * 70)
    
    # 提取模板
    result = extract_navbar_from_index()
    if not result:
        return
    
    navbar_html, mobile_sidebar_html = result
    print(f"✅ 已提取導航欄模板 ({len(navbar_html)} 字符)")
    print(f"✅ 已提取手機側邊欄模板 ({len(mobile_sidebar_html)} 字符)")
    print()
    
    # 更新主要頁面
    print("更新主要頁面...")
    main_success = 0
    for page in main_pages:
        if replace_navbar(page, navbar_html, mobile_sidebar_html):
            main_success += 1
    
    print(f"\n主要頁面: {main_success}/{len(main_pages)} 成功")
    
    # 更新博客頁面
    print("\n更新博客頁面...")
    blog_success = 0
    for page in blog_pages:
        if replace_navbar(page, navbar_html, mobile_sidebar_html):
            blog_success += 1
    
    print(f"\n博客頁面: {blog_success}/{len(blog_pages)} 成功")
    
    print("=" * 70)
    print(f"✅ 完成！總共成功: {main_success + blog_success}/{len(main_pages) + len(blog_pages)}")
    print("=" * 70)

if __name__ == "__main__":
    main()

