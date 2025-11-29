#!/usr/bin/env python3
"""
批量更新博客頁面
1. 更新收費信息（HKD$0.5, 20頁免費, 10秒處理）
2. 統一左側欄導航
3. 修復右上角登入邏輯
"""

import re
import os

# 博客頁面列表
blog_pages = [
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html'
]

def update_pricing_info(content):
    """更新收費信息"""
    # 更新 HKD 0.5
    content = re.sub(
        r'低至\s*HKD\s*\$?\s*[\d.]+\s*/\s*頁',
        '低至 HKD 0.5/頁',
        content,
        flags=re.IGNORECASE
    )
    
    # 更新免費頁數
    content = re.sub(
        r'免費(試用|獲得|轉換)?\s*\d+\s*頁',
        '免費試用 20 頁',
        content,
        flags=re.IGNORECASE
    )
    
    # 更新處理時間
    content = re.sub(
        r'(平均|約|大約)?\s*\d+\s*(秒|分鐘)\s*(完成|處理)',
        '平均 10 秒處理',
        content,
        flags=re.IGNORECASE
    )
    
    # 特定替換
    replacements = [
        ('每天免費轉換 3 頁', '免費試用 20 頁'),
        ('3 分鐘內完成', '平均 10 秒處理'),
        ('3 分鐘完成', '平均 10 秒處理'),
        ('200 頁轉換額度', '20 頁免費試用'),
        ('免費獲得 200 頁', '免費試用 20 頁'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    return content

def add_unified_auth_script(content):
    """添加統一認證腳本"""
    # 檢查是否已經有 unified-auth.js
    if 'unified-auth.js' in content:
        print('  ✓ unified-auth.js 已存在')
        return content
    
    # 在 simple-data-manager.js 之後添加
    pattern = r'(<script[^>]*src="[^"]*simple-data-manager\.js[^"]*"[^>]*></script>)'
    replacement = r'\1\n    <script defer src="../unified-auth.js?v=20251129"></script>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print('  ✓ 添加 unified-auth.js')
    else:
        print('  ⚠ 找不到 simple-data-manager.js，嘗試其他位置')
        # 嘗試在 </head> 之前添加
        pattern = r'(</head>)'
        replacement = r'    <script defer src="../unified-auth.js?v=20251129"></script>\n\1'
        content = re.sub(pattern, replacement, content)
        print('  ✓ 在 </head> 前添加 unified-auth.js')
    
    return content

def update_sidebar_navigation(content):
    """統一左側欄導航"""
    sidebar_html = '''        <!-- 左側欄 -->
        <aside class="blog-sidebar">
            <h3>📚 文章導航</h3>
            <nav class="sidebar-nav">
                <a href="/blog/how-to-convert-pdf-bank-statement-to-excel.html" class="sidebar-link">
                    <i class="fas fa-file-excel"></i>
                    <span>PDF 銀行對帳單轉 Excel</span>
                </a>
                <a href="/blog/ai-invoice-processing-guide.html" class="sidebar-link">
                    <i class="fas fa-file-invoice"></i>
                    <span>AI 發票處理完整指南</span>
                </a>
                <a href="/blog/best-pdf-to-excel-converter.html" class="sidebar-link">
                    <i class="fas fa-star"></i>
                    <span>最佳 PDF 轉 Excel 工具</span>
                </a>
                <a href="/blog/ocr-technology-for-accountants.html" class="sidebar-link">
                    <i class="fas fa-search"></i>
                    <span>會計師的 OCR 技術指南</span>
                </a>
                <a href="/blog/automate-financial-documents.html" class="sidebar-link">
                    <i class="fas fa-robot"></i>
                    <span>自動化財務文檔處理</span>
                </a>
            </nav>
            
            <div class="sidebar-cta" style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; text-align: center;">
                <h4 style="margin-bottom: 0.5rem; font-size: 1.125rem;">💡 需要幫助？</h4>
                <p style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 1rem;">立即試用 VaultCaddy，體驗 AI 文檔處理的強大功能</p>
                <a href="/" style="display: inline-block; background: white; color: #667eea; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    開始使用
                </a>
            </div>
        </aside>'''
    
    # 查找並替換左側欄
    pattern = r'<aside class="blog-sidebar">.*?</aside>'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, sidebar_html, content, flags=re.DOTALL)
        print('  ✓ 更新左側欄導航')
    else:
        print('  ⚠ 找不到左側欄')
    
    return content

def remove_old_auth_logic(content):
    """移除舊的認證邏輯"""
    # 移除舊的 updateUserMenu 函數定義（如果在 HTML 中）
    # 保留對 updateUserMenu() 的調用，因為 unified-auth.js 會提供
    
    # 移除重複的 auth-state-changed 監聽器
    pattern = r'window\.addEventListener\([\'"]auth-state-changed[\'"].*?\}\);'
    matches = re.findall(pattern, content, re.DOTALL)
    if len(matches) > 1:
        print(f'  ⚠ 發現 {len(matches)} 個 auth-state-changed 監聽器，保留第一個')
        # 只保留第一個
        for i, match in enumerate(matches[1:], 1):
            content = content.replace(match, f'// 已移除重複的 auth-state-changed 監聽器 #{i+1}')
    
    return content

def process_file(filepath):
    """處理單個文件"""
    print(f'\n處理: {filepath}')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 更新收費信息
        content = update_pricing_info(content)
        
        # 2. 統一左側欄
        content = update_sidebar_navigation(content)
        
        # 3. 添加統一認證腳本
        content = add_unified_auth_script(content)
        
        # 4. 移除舊的認證邏輯
        content = remove_old_auth_logic(content)
        
        # 只在內容有變化時寫入
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ {filepath} 更新完成')
        else:
            print(f'⏭️  {filepath} 無需更新')
        
        return True
    except Exception as e:
        print(f'❌ 處理 {filepath} 時出錯: {e}')
        return False

def main():
    print('🚀 開始批量更新博客頁面...\n')
    
    success_count = 0
    for page in blog_pages:
        if os.path.exists(page):
            if process_file(page):
                success_count += 1
        else:
            print(f'⚠️  文件不存在: {page}')
    
    print(f'\n✅ 完成！成功更新 {success_count}/{len(blog_pages)} 個文件')

if __name__ == '__main__':
    main()

