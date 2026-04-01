#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新博客頁面的價格信息
- VaultCaddy: $15/月起 → HKD$0.5/頁
- 所有美金價格 → 港幣
- 更新處理時間統計
"""

import re
from pathlib import Path

# 博客文件列表
BLOG_FILES = [
    'blog/automate-financial-documents.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/how-to-convert-pdf-bank-statement-to-excel.html'
]

# 價格替換規則
PRICE_REPLACEMENTS = [
    # VaultCaddy 價格
    (r'<strong>價格：</strong>\$15/月起', '<strong>價格：</strong>低至 HKD $0.5/頁'),
    (r'<strong>價格：</strong>hkd\$78/月起', '<strong>價格：</strong>低至 HKD $0.5/頁'),
    (r'價格：\$15/月起', '價格：低至 HKD $0.5/頁'),
    (r'價格：hkd\$78/月起', '價格：低至 HKD $0.5/頁'),
    
    # ABBYY FineReader
    (r'<strong>價格：</strong>\$199（一次性購買）', '<strong>價格：</strong>USD $199（一次性購買）'),
    (r'價格：\$199（一次性購買）', '價格：USD $199（一次性購買）'),
    
    # Adobe Acrobat Pro DC
    (r'<strong>價格：</strong>\$19\.99/月', '<strong>價格：</strong>USD $19.99/月'),
    (r'價格：\$19\.99/月', '價格：USD $19.99/月'),
    
    # Smallpdf
    (r'<strong>價格：</strong>\$12/月或免費版（有限制）', '<strong>價格：</strong>USD $12/月或免費版（有限制）'),
    (r'價格：\$12/月或免費版（有限制）', '價格：USD $12/月或免費版（有限制）'),
    
    # PDFelement
    (r'<strong>價格：</strong>\$79\.99/年', '<strong>價格：</strong>USD $79.99/年'),
    (r'價格：\$79\.99/年', '價格：USD $79.99/年'),
    
    # Nitro Pro
    (r'<strong>價格：</strong>\$179\.99/年', '<strong>價格：</strong>USD $179.99/年'),
    (r'價格：\$179\.99/年', '價格：USD $179.99/年'),
    
    # Able2Extract Professional
    (r'<strong>價格：</strong>\$149\.95（一次性購買）', '<strong>價格：</strong>USD $149.95（一次性購買）'),
    (r'價格：\$149\.95（一次性購買）', '價格：USD $149.95（一次性購買）'),
    
    # Zamzar
    (r'<strong>價格：</strong>\$9/月或免費版（有限制）', '<strong>價格：</strong>USD $9/月或免費版（有限制）'),
    (r'價格：\$9/月或免費版（有限制）', '價格：USD $9/月或免費版（有限制）'),
]

# 統計數據替換
STATS_REPLACEMENTS = [
    # AI 發票處理指南
    (r'3 分鐘\s*</div>\s*<div[^>]*>\s*處理一張發票', '10 秒</div>\n                <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">處理一張發票'),
    (r'處理時間\s*</td>\s*<td[^>]*>5-10 分鐘/張</td>\s*<td[^>]*>30 秒/張', '處理時間</td>\n                        <td style="padding: 1rem; text-align: left; border-bottom: 1px solid #e5e7eb;">5-10 分鐘/張</td>\n                        <td style="padding: 1rem; text-align: left; border-bottom: 1px solid #e5e7eb; color: #10b981; font-weight: 600;">10 秒/張'),
]

def update_file(file_path):
    """更新單個文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 應用價格替換
        for pattern, replacement in PRICE_REPLACEMENTS:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made.append(f"  ✅ 替換: {pattern[:50]}...")
        
        # 應用統計數據替換
        for pattern, replacement in STATS_REPLACEMENTS:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                changes_made.append(f"  ✅ 替換統計數據")
        
        # 如果有變更，寫入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✅ 更新: {file_path}")
            for change in changes_made:
                print(change)
            return True
        else:
            print(f"\n⏭️  跳過: {file_path} (無需更新)")
            return False
            
    except Exception as e:
        print(f"\n❌ 錯誤: {file_path}")
        print(f"   {str(e)}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始更新博客頁面價格信息...")
    print("=" * 60)
    
    updated_count = 0
    
    for file_path in BLOG_FILES:
        if update_file(file_path):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共更新 {updated_count}/{len(BLOG_FILES)} 個文件")
    print("=" * 60)

if __name__ == '__main__':
    main()

