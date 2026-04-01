#!/usr/bin/env python3
"""
重建 privacy.html 和 terms.html
- 保留內容部分
- 從 index.html 複製導航欄和 footer
- 添加必要的 scripts 和 styles
"""

from bs4 import BeautifulSoup
import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 讀取 index.html
print("讀取 index.html...")
index_html = read_file('index.html')

# 提取導航欄（從 <nav> 到 </nav> 和相關元素）
nav_pattern = r'(<!-- ✅ 統一靜態導航欄.*?</nav>)'
nav_match = re.search(nav_pattern, index_html, re.DOTALL)
nav_html = nav_match.group(1) if nav_match else ''

# 提取手機側邊欄
sidebar_pattern = r'(<!-- 手機側邊欄菜單 -->.*?</div>\s*<!-- 側邊欄遮罩 -->.*?</div>)'
sidebar_match = re.search(sidebar_pattern, index_html, re.DOTALL)
sidebar_html = sidebar_match.group(1) if sidebar_match else ''

# 提取用戶下拉菜單
dropdown_pattern = r'(<div id="user-dropdown".*?</div>\s*</div>\s*</div>)'
dropdown_match = re.search(dropdown_pattern, index_html, re.DOTALL)
dropdown_html = dropdown_match.group(1) if dropdown_match else ''

# 提取 footer
footer_pattern = r'(<!-- 頁尾 -->.*?</footer>)'
footer_match = re.search(footer_pattern, index_html, re.DOTALL)
footer_html = footer_match.group(1) if footer_match else ''

# 提取響應式 CSS 和 JavaScript
style_js_pattern = r'(<style>.*?footer a:hover.*?</style>.*?<script>.*?openMobileSidebar.*?</script>)'
style_js_match = re.search(style_js_pattern, index_html, re.DOTALL)
style_js_html = style_js_match.group(1) if style_js_match else ''

print(f"✅ 提取導航欄: {len(nav_html)} 字符")
print(f"✅ 提取側邊欄: {len(sidebar_html)} 字符")
print(f"✅ 提取下拉菜單: {len(dropdown_html)} 字符")
print(f"✅ 提取 Footer: {len(footer_html)} 字符")
print(f"✅ 提取樣式和JS: {len(style_js_html)} 字符")

# ========== 處理 privacy.html ==========
print("\n處理 privacy.html...")
privacy_html = read_file('privacy.html')
privacy_soup = BeautifulSoup(privacy_html, 'html.parser')

# 提取隱私政策的內容部分
privacy_content = privacy_soup.find('div', {'class': 'content'})
if not privacy_content:
    print("❌ 找不到 privacy.html 的內容")
    exit(1)

# 創建新的 privacy.html
new_privacy = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>隱私政策 - VaultCaddy</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- Firebase SDK（CDN 版本 - compat）-->
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    
    <!-- Firebase 配置和數據管理器 -->
    <script defer src="firebase-config.js?v=20251105"></script>
    <!-- 🔥 新的簡化系統 -->
    <script defer src="simple-auth.js?v=20251105-force-init"></script>
    <script defer src="simple-data-manager.js?v=20251105-force-init"></script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            min-height: 100vh;
            color: #1f2937;
            padding-top: 60px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            overflow: hidden;
            margin-bottom: 2rem;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2.5rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
        }}
        
        .header .date {{
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
        }}
        
        .content {{
            padding: 3rem 2.5rem;
        }}
        
        .section {{
            margin-bottom: 2.5rem;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .section-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.125rem;
        }}
        
        .section p {{
            color: #475569;
            line-height: 1.8;
            margin-bottom: 1rem;
        }}
        
        .section ul {{
            margin: 1rem 0 1rem 1.5rem;
        }}
        
        .section li {{
            color: #475569;
            line-height: 1.8;
            margin-bottom: 0.75rem;
        }}
        
        .section strong {{
            color: #1e293b;
            font-weight: 600;
        }}
        
        .highlight-box {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
        }}
        
        .contact-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 2.5rem;
            border-radius: 16px;
            text-align: center;
            border: 2px solid #e2e8f0;
        }}
        
        .contact-card h3 {{
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #1e293b;
        }}
        
        .contact-card p {{
            color: #64748b;
            margin-bottom: 1.5rem;
        }}
        
        .contact-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 0.5rem;
        }}
        
        .contact-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
    </style>
</head>
<body>
    {nav_html}
    
    {sidebar_html}
    
    {dropdown_html}
    
    <div class="container">
        {str(privacy_soup.find('div', {'class': 'card'})) if privacy_soup.find('div', {'class': 'card'}) else ''}
    </div>
    
    {footer_html}
    
    {style_js_html}
    
    <!-- 右下角對話按鈕 -->
    <script src="contact-widget.js?v=20251125"></script>
</body>
</html>'''

write_file('privacy.html', new_privacy)
print("✅ privacy.html 已重建")

# ========== 處理 terms.html ==========
print("\n處理 terms.html...")
terms_html = read_file('terms.html')
terms_soup = BeautifulSoup(terms_html, 'html.parser')

# 提取服務條款的內容部分
terms_card = terms_soup.find('div', {'class': 'card'})
if not terms_card:
    print("❌ 找不到 terms.html 的內容")
    exit(1)

# 創建新的 terms.html
new_terms = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>服務條款 - VaultCaddy</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- Firebase SDK（CDN 版本 - compat）-->
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    
    <!-- Firebase 配置和數據管理器 -->
    <script defer src="firebase-config.js?v=20251105"></script>
    <!-- 🔥 新的簡化系統 -->
    <script defer src="simple-auth.js?v=20251105-force-init"></script>
    <script defer src="simple-data-manager.js?v=20251105-force-init"></script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            min-height: 100vh;
            color: #1f2937;
            padding-top: 60px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            overflow: hidden;
            margin-bottom: 2rem;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2.5rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
        }}
        
        .header .date {{
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
        }}
        
        .content {{
            padding: 3rem 2.5rem;
        }}
        
        .section {{
            margin-bottom: 2.5rem;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .section-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.125rem;
        }}
        
        .section p {{
            color: #475569;
            line-height: 1.8;
            margin-bottom: 1rem;
        }}
        
        .section ul {{
            margin: 1rem 0 1rem 1.5rem;
        }}
        
        .section li {{
            color: #475569;
            line-height: 1.8;
            margin-bottom: 0.75rem;
        }}
        
        .section strong {{
            color: #1e293b;
            font-weight: 600;
        }}
        
        .highlight-box {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
        }}
        
        .contact-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 2.5rem;
            border-radius: 16px;
            text-align: center;
            border: 2px solid #e2e8f0;
        }}
        
        .contact-card h3 {{
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #1e293b;
        }}
        
        .contact-card p {{
            color: #64748b;
            margin-bottom: 1.5rem;
        }}
        
        .contact-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 0.5rem;
        }}
        
        .contact-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
    </style>
</head>
<body>
    {nav_html}
    
    {sidebar_html}
    
    {dropdown_html}
    
    <div class="container">
        {str(terms_card)}
    </div>
    
    {footer_html}
    
    {style_js_html}
    
    <!-- 右下角對話按鈕 -->
    <script src="contact-widget.js?v=20251125"></script>
</body>
</html>'''

write_file('terms.html', new_terms)
print("✅ terms.html 已重建")

print("\n✅ 完成！兩個文件都已重建")
print("\n檢查結果：")
print(f"- privacy.html: {len(new_privacy)} 字符")
print(f"- terms.html: {len(new_terms)} 字符")

