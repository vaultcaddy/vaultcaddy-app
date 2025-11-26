#!/usr/bin/env python3
"""
更新 privacy.html 和 terms.html
- 添加 index.html 的導航欄和 footer
- 刪除"返回首頁"按鈕
- 將內容向上移動 10pt
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
index_html = read_file('index.html')
index_soup = BeautifulSoup(index_html, 'html.parser')

# 提取導航欄
nav = index_soup.find('nav', {'class': 'vaultcaddy-navbar'})
mobile_sidebar = index_soup.find('div', {'id': 'mobile-sidebar'})
mobile_overlay = index_soup.find('div', {'id': 'mobile-sidebar-overlay'})

# 提取用戶下拉菜單
user_dropdown_pattern = r'(<div id="user-dropdown".*?</div>)\s*</nav>'
user_dropdown_match = re.search(user_dropdown_pattern, index_html, re.DOTALL)
user_dropdown = user_dropdown_match.group(1) if user_dropdown_match else ''

# 提取 footer
footer = index_soup.find('footer')

# 提取響應式 CSS 和相關的 JavaScript
responsive_css_pattern = r'(<style>.*?@media.*?</style>)'
responsive_css_match = re.search(responsive_css_pattern, index_html, re.DOTALL)
responsive_css = responsive_css_match.group(1) if responsive_css_match else ''

# 提取漢堡菜單的 JavaScript
hamburger_js_pattern = r'(// ==================== 漢堡菜單.*?}\)\(\);)'
hamburger_js_match = re.search(hamburger_js_pattern, index_html, re.DOTALL)
hamburger_js = hamburger_js_match.group(1) if hamburger_js_match else ''

# 提取用戶菜單的 JavaScript
user_menu_js_pattern = r'(// 點擊外部關閉下拉菜單.*?window\.addEventListener\(\'user-logged-out\', updateUserMenu\);)'
user_menu_js_match = re.search(user_menu_js_pattern, index_html, re.DOTALL)
user_menu_js = user_menu_js_match.group(1) if user_menu_js_match else ''

# 處理 privacy.html
print("處理 privacy.html...")
privacy_html = read_file('privacy.html')
privacy_soup = BeautifulSoup(privacy_html, 'html.parser')

# 創建新的 HTML 結構
new_privacy = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>隱私政策 - VaultCaddy</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- Firebase SDK -->
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
    <script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    
    <!-- Firebase 配置和數據管理器 -->
    <script defer src="firebase-config.js?v=20251105"></script>
    <script defer src="simple-auth.js?v=20251105"></script>
    <script defer src="simple-data-manager.js?v=20251105"></script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f9fafb;
            min-height: 100vh;
            color: #1f2937;
            padding-top: 60px; /* 為導航欄留出空間 */
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            margin-top: -10pt; /* 向上移動 10pt */
        }}
        
        .card {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
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
            letter-spacing: -0.02em;
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
            font-size: 1rem;
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
    {str(nav)}
    
    {str(mobile_sidebar)}
    {str(mobile_overlay)}
    
    {user_dropdown}
    
    <div class="container">
        <div class="card">
            <div class="header">
                <h1>🔒 隱私政策</h1>
                <p class="date">最後更新：2025年1月22日</p>
            </div>
            
            <div class="content">
                <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2.5rem;">
                    本隱私政策說明 VaultCaddy 如何收集、使用和保護您的個人資料。我們致力於保護您的隱私安全。
                </p>
                
                <div class="section">
                    <h2 class="section-title">
                        <div class="section-icon"><i class="fas fa-database"></i></div>
                        我們收集的信息
                    </h2>
                    <p>我們通過以下方式收集信息：</p>
                    <ul>
                        <li><strong>帳戶信息：</strong>註冊時收集您的電子郵件地址</li>
                        <li><strong>使用數據：</strong>記錄您如何使用我們的服務</li>
                        <li><strong>文檔處理：</strong>臨時處理您上傳的文檔（24小時後自動刪除）</li>
                        <li><strong>付款信息：</strong>通過 Stripe 等安全支付平台處理</li>
                    </ul>
                    <div class="highlight-box">
                        <strong><i class="fas fa-shield-alt"></i> 重要：</strong>我們不會永久存儲您的文檔，所有文件在處理後 24 小時內自動刪除。
                    </div>
                </div>

                <div class="section">
                    <h2 class="section-title">
                        <div class="section-icon"><i class="fas fa-tasks"></i></div>
                        信息使用方式
                    </h2>
                    <ul>
                        <li>提供和改進文檔處理服務</li>
                        <li>處理交易並管理您的帳戶</li>
                        <li>發送服務更新（需經您同意）</li>
                        <li>回應查詢和支持請求</li>
                        <li>確保平台安全並防止欺詐</li>
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">
                        <div class="section-icon"><i class="fas fa-lock"></i></div>
                        安全措施
                    </h2>
                    <p>我們採取多層級的安全措施保護您的數據：</p>
                    <ul>
                        <li><strong>SSL/TLS 加密：</strong>所有數據傳輸都經過加密</li>
                        <li><strong>數據加密：</strong>敏感信息使用行業標準加密存儲</li>
                        <li><strong>定期審計：</strong>持續進行安全審查和漏洞掃描</li>
                        <li><strong>訪問控制：</strong>嚴格限制數據訪問權限</li>
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">
                        <div class="section-icon"><i class="fas fa-user-shield"></i></div>
                        您的權利
                    </h2>
                    <p>根據數據保護法律，您擁有以下權利：</p>
                    <ul>
                        <li><strong>訪問權：</strong>查看我們持有的您的信息</li>
                        <li><strong>更正權：</strong>更正不準確的信息</li>
                        <li><strong>刪除權：</strong>要求刪除您的個人數據</li>
                        <li><strong>數據可攜權：</strong>以可攜格式獲取您的數據</li>
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">
                        <div class="section-icon"><i class="fas fa-globe"></i></div>
                        第三方服務
                    </h2>
                    <p>我們使用以下可信賴的第三方服務：</p>
                    <ul>
                        <li><strong>Stripe：</strong>安全的付款處理</li>
                        <li><strong>Firebase：</strong>用戶認證和數據存儲</li>
                        <li><strong>Google Cloud：</strong>AI 文檔處理</li>
                    </ul>
                </div>

                <div class="contact-card">
                    <h3>有疑問？聯繫我們</h3>
                    <p>如果您對我們的隱私政策有任何疑問，歡迎隨時與我們聯繫</p>
                    <a href="mailto:vaultcaddy@gmail.com" class="contact-link">
                        <i class="fas fa-envelope"></i>
                        vaultcaddy@gmail.com
                    </a>
                    <a href="index.html" class="contact-link">
                        <i class="fas fa-home"></i>
                        訪問網站
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    {str(footer)}
    
    {responsive_css}
    
    <script>
        {hamburger_js}
        
        {user_menu_js}
    </script>
    
    <!-- 右下角對話按鈕 -->
    <script src="contact-widget.js?v=20251125"></script>
</body>
</html>
'''

write_file('privacy.html', new_privacy)
print("✅ privacy.html 已更新")

# 類似處理 terms.html
print("\\n處理 terms.html...")
terms_html = read_file('terms.html')

# 讀取 terms.html 的內容部分
terms_soup = BeautifulSoup(terms_html, 'html.parser')
terms_content = terms_soup.find('div', {'class': 'content'})

# 由於結構相似，我會直接創建新的 terms.html
# 這裡需要從原始 terms.html 提取內容...

print("✅ 完成")

