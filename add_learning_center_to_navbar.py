#!/usr/bin/env python3
"""
為所有頁面的導航欄添加「學習中心」鏈接
位置：價格和儀表板之間
"""

import os
import re

# 要更新的文件列表
files_to_update = [
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html',
    'document-detail.html',
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html',
]

def add_learning_center_to_desktop_nav(content):
    """在桌面版導航欄中添加學習中心"""
    # 匹配：價格鏈接 + 儀表板鏈接
    pattern = r'(<a href="(?:index\.html#pricing|#pricing)"[^>]*>價格</a>)\s*(<a href="(?:\.\./)?dashboard\.html"[^>]*>儀表板</a>)'
    
    # 替換：在中間插入學習中心鏈接
    replacement = r'\1\n                <a href="/blog/" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">學習中心</a>\n                \2'
    
    new_content = re.sub(pattern, replacement, content)
    return new_content

def add_learning_center_to_mobile_nav(content):
    """在手機版側邊欄中添加學習中心"""
    # 匹配：價格鏈接（包含<span>價格</span>）
    pattern = r'(<a href="(?:index\.html#pricing|#pricing)"[^>]*>\s*<i class="fas fa-dollar-sign"[^>]*></i>\s*<span>價格</span>\s*</a>)'
    
    # 替換：在後面插入學習中心鏈接
    replacement = r'''\1
                <a href="/blog/" style="padding: 0.875rem 1rem; color: #374151; text-decoration: none; border-radius: 8px; transition: background 0.2s; display: flex; align-items: center; gap: 0.75rem;" onclick="closeMobileSidebar()">
                    <i class="fas fa-graduation-cap" style="width: 20px; color: #667eea;"></i>
                    <span>學習中心</span>
                </a>'''
    
    new_content = re.sub(pattern, replacement, content)
    return new_content

def update_file(filepath):
    """更新單個文件"""
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在：{filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已經有學習中心鏈接
        if '學習中心' in content and '/blog/' in content:
            print(f"✅ {filepath} 已包含學習中心鏈接，跳過")
            return True
        
        original_content = content
        
        # 添加到桌面版導航欄
        content = add_learning_center_to_desktop_nav(content)
        
        # 添加到手機版側邊欄
        content = add_learning_center_to_mobile_nav(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新：{filepath}")
            return True
        else:
            print(f"⚠️  未找到匹配模式：{filepath}")
            return False
            
    except Exception as e:
        print(f"❌ 更新 {filepath} 時出錯：{str(e)}")
        return False

def main():
    print("🚀 開始為所有頁面添加「學習中心」鏈接...\n")
    
    success_count = 0
    for filepath in files_to_update:
        if update_file(filepath):
            success_count += 1
    
    print(f"\n✨ 完成！成功更新 {success_count}/{len(files_to_update)} 個文件")

if __name__ == '__main__':
    main()

