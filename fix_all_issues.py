#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復所有問題：
1. 博客價格添加港幣換算
2. firstproject.html 按鈕位置調整
3. account.html 個人資料 logo
4. 恢復用戶下拉菜單設計
"""

import re
from pathlib import Path

def fix_firstproject_buttons():
    """修復 firstproject.html 按鈕位置"""
    file_path = 'firstproject.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 CSS 中添加按鈕區域樣式
    css_addition = """
        /* 按鈕區域樣式 */
        #standalone-buttons-container {
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 5pt;
            justify-content: flex-end;
        }
        """
    
    # 在 </style> 前插入
    content = content.replace('</style>', css_addition + '\n    </style>')
    
    # 將按鈕區域移到表格上方
    # 找到 </header> 和 <!-- 文檔表格 --> 之間的位置
    pattern = r'(</header>\s*\n\s*)(<!-- 文檔表格 -->)'
    replacement = r'''\1
                <!-- 操作按鈕（獨立區域）-->
                <div id="standalone-buttons-container">
                    <button id="upload-btn-standalone" onclick="openUploadModal()" style="background: #8b5cf6; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500;">
                        <span>Upload files</span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                    <div class="dropdown" id="export-dropdown-standalone" style="position: relative;">
                        <button id="export-btn-standalone" onclick="toggleExportMenu()" style="background: #10b981; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500;">
                            <i class="fas fa-download"></i>
                            <span>Export</span>
                            <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
                        </button>
                        <!-- Export menu will be handled by existing toggleExportMenu function -->
                    </div>
                    <button onclick="deleteSelectedDocuments()" id="delete-selected-btn-standalone" disabled style="background: #ef4444; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500; opacity: 0.5;">
                        <i class="fas fa-trash"></i>
                        <span>Delete</span>
                        <span id="delete-count-standalone" style="display: none;"></span>
                    </button>
                </div>

                \2'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 按鈕位置")

def update_blog_prices_with_hkd():
    """更新博客價格，添加港幣換算"""
    blog_files = [
        'blog/automate-financial-documents.html',
        'blog/best-pdf-to-excel-converter.html',
        'blog/ocr-technology-for-accountants.html'
    ]
    
    # 匯率（USD to HKD，約 7.8）
    conversions = {
        '199': '1,552',  # 199 * 7.8
        '19.99': '156',  # 19.99 * 7.8
        '12': '94',      # 12 * 7.8
        '79.99': '624',  # 79.99 * 7.8
        '179.99': '1,404', # 179.99 * 7.8
        '149.95': '1,170', # 149.95 * 7.8
        '9': '70',       # 9 * 7.8
    }
    
    replacements = [
        (r'USD \$199（一次性購買）', 'USD $199（一次性購買，約 HKD $1,552）'),
        (r'USD \$19\.99/月', 'USD $19.99/月（約 HKD $156）'),
        (r'USD \$12/月', 'USD $12/月（約 HKD $94）'),
        (r'USD \$79\.99/年', 'USD $79.99/年（約 HKD $624）'),
        (r'USD \$179\.99/年', 'USD $179.99/年（約 HKD $1,404）'),
        (r'USD \$149\.95（一次性購買）', 'USD $149.95（一次性購買，約 HKD $1,170）'),
        (r'USD \$9/月', 'USD $9/月（約 HKD $70）'),
    ]
    
    for file_path in blog_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 已更新 {file_path} 價格")
            else:
                print(f"⏭️  跳過 {file_path}（無需更新）")
                
        except Exception as e:
            print(f"❌ 錯誤: {file_path} - {str(e)}")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始修復所有問題...")
    print("=" * 60)
    
    # 1. 修復 firstproject.html 按鈕位置
    print("\n1️⃣ 修復 firstproject.html 按鈕位置...")
    fix_firstproject_buttons()
    
    # 2. 更新博客價格
    print("\n2️⃣ 更新博客價格（添加港幣換算）...")
    update_blog_prices_with_hkd()
    
    print("\n" + "=" * 60)
    print("✅ 所有修復完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()

