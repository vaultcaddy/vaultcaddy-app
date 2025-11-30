#!/usr/bin/env python3
"""
修復所有頁面中的用戶 Logo 邏輯，統一為 'YC'
"""

import re
import os

# 要修復的文件列表
files_to_fix = [
    'index.html',
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html',
    'blog/how-to-convert-pdf-bank-statement-to-excel.html'
]

def fix_file(filename):
    """修復單個文件"""
    try:
        if not os.path.exists(filename):
            print(f"⚠️  {filename} - 文件不存在，跳過")
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修復 getUserInitial 函數 - 直接返回 'YC'
        # 模式 1: return userEmail ? userEmail.charAt(0).toUpperCase() : 'U';
        content = re.sub(
            r'return userEmail \? userEmail\.charAt\(0\)\.toUpperCase\(\) : [\'"]U[\'"];',
            "return 'YC';",
            content
        )
        
        # 模式 2: user.email.charAt(0).toUpperCase()
        content = re.sub(
            r'user\.email\.charAt\(0\)\.toUpperCase\(\)',
            "'YC'",
            content
        )
        
        # 模式 3: avatarText = user.email.charAt(0).toUpperCase();
        content = re.sub(
            r'avatarText\s*=\s*user\.email\.charAt\(0\)\.toUpperCase\(\);',
            "avatarText = 'YC';",
            content
        )
        
        # 模式 4: 任何 email.charAt(0) 相關的
        content = re.sub(
            r'email\.charAt\(0\)\.toUpperCase\(\)',
            "'YC'",
            content
        )
        
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} - 已修復 Logo 邏輯")
            return True
        else:
            print(f"⏭️  {filename} - 無需修改")
            return False
    except Exception as e:
        print(f"❌ {filename} - 錯誤: {e}")
        return False

def main():
    print("=" * 70)
    print("修復所有頁面的用戶 Logo 邏輯為 'YC'...")
    print("=" * 70)
    
    fixed_count = 0
    for filename in files_to_fix:
        if fix_file(filename):
            fixed_count += 1
    
    print("=" * 70)
    print(f"✅ 完成！成功修復: {fixed_count}/{len(files_to_fix)} 個文件")
    print("=" * 70)

if __name__ == "__main__":
    main()

