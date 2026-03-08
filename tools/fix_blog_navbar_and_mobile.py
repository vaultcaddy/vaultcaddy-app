#!/usr/bin/env python3
"""
修復博客頁面的導航欄和添加手機版支持
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

def extract_navbar_from_index():
    """從 index.html 提取完整的導航欄（包括靜態 HTML 和手機側邊欄）"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取從 <nav 到 手機側邊欄結束的所有內容
    # 包括: <nav>...</nav> + <!-- 手機側邊欄菜單 --> ... </div>
    
    # 找到 <body> 標籤後的第一個 <nav>
    body_match = re.search(r'<body>(.*)', content, flags=re.DOTALL)
    if not body_match:
        return None
    
    body_content = body_match.group(1)
    
    # 提取 <nav> 到 手機側邊欄結束
    navbar_match = re.search(
        r'(<nav[^>]*class="vaultcaddy-navbar"[^>]*>.*?</nav>\s*<!-- 手機側邊欄菜單 -->.*?</div>\s*</div>)',
        body_content,
        flags=re.DOTALL
    )
    
    if navbar_match:
        return navbar_match.group(1)
    
    return None

def fix_blog_page(filename, navbar_html):
    """修復單個博客頁面"""
    try:
        if not os.path.exists(filename):
            print(f"⚠️  {filename} - 文件不存在")
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除舊的導航欄容器
        content = re.sub(
            r'<!-- 統一導航欄容器 -->\s*<div id="navbar-container"></div>\s*<div id="sidebar-container"></div>',
            '',
            content
        )
        
        # 移除任何可能存在的舊導航欄
        content = re.sub(
            r'<!-- 統一靜態導航欄 -->',
            '',
            content
        )
        
        # 在 <body> 後插入新的導航欄
        content = re.sub(
            r'(<body>)',
            r'\1\n    ' + navbar_html + '\n',
            content
        )
        
        # 添加手機版 CSS（如果沒有的話）
        if '@media (max-width: 768px)' not in content or 'mobile-menu-btn' not in content:
            mobile_css = '''
        /* 手機版導航欄 */
        @media (max-width: 768px) {
            #mobile-menu-btn {
                display: block !important;
            }
            
            .desktop-logo-text {
                display: none !important;
            }
            
            nav .desktop-logo + div {
                display: none !important;
            }
            
            nav > div:last-child > div:first-child {
                display: none !important;
            }
            
            .blog-sidebar {
                display: none !important;
            }
            
            .blog-container {
                margin-left: 0 !important;
                padding: 1rem !important;
            }
        }'''
            
            # 在 </style> 前插入
            content = re.sub(
                r'(</style>)',
                mobile_css + r'\n    \1',
                content,
                count=1
            )
        
        # 添加手機側邊欄開關函數（如果沒有的話）
        if 'function openMobileSidebar' not in content:
            mobile_js = '''
    <script>
        function openMobileSidebar() {
            const sidebar = document.getElementById('mobile-sidebar');
            if (sidebar) {
                sidebar.style.left = '0';
            }
        }
        
        function closeMobileSidebar() {
            const sidebar = document.getElementById('mobile-sidebar');
            if (sidebar) {
                sidebar.style.left = '-100%';
            }
        }
    </script>'''
            
            # 在 </body> 前插入
            content = re.sub(
                r'(</body>)',
                mobile_js + r'\n\1',
                content
            )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename} - 已更新導航欄和手機版")
        return True
    except Exception as e:
        print(f"❌ {filename} - 錯誤: {e}")
        return False

def main():
    print("=" * 70)
    print("修復博客頁面導航欄並添加手機版支持...")
    print("=" * 70)
    
    # 提取 index.html 的導航欄
    navbar_html = extract_navbar_from_index()
    if not navbar_html:
        print("❌ 無法從 index.html 提取導航欄")
        return
    
    print(f"✅ 已提取導航欄模板 ({len(navbar_html)} 字符)")
    print()
    
    # 修復所有博客頁面
    success_count = 0
    for page in blog_pages:
        if fix_blog_page(page, navbar_html):
            success_count += 1
    
    print("=" * 70)
    print(f"✅ 完成！成功: {success_count}/{len(blog_pages)}")
    print("=" * 70)

if __name__ == "__main__":
    main()

