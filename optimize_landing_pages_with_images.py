#!/usr/bin/env python3
"""
Landing Page圖片優化工具
作用: 為所有Landing Page添加5張必備圖片和優化內容
"""

import os
import re
from pathlib import Path

# 銀行頁面列表
BANK_PAGES = {
    'hsbc': {
        'file': 'hsbc-bank-statement.html',
        'name_zh': '匯豐銀行',
        'name_en': 'HSBC',
        'color': '#DB0011',
        'logo': 'hsbc-logo.png'
    },
    'hangseng': {
        'file': 'hangseng-bank-statement.html',
        'name_zh': '恆生銀行',
        'name_en': 'Hang Seng',
        'color': '#00857D',
        'logo': 'hangseng-logo.png'
    },
    'bochk': {
        'file': 'boc-hk-bank-statement.html',
        'name_zh': '中國銀行(香港)',
        'name_en': 'BOC Hong Kong',
        'color': '#CC092F',
        'logo': 'bochk-logo.png'
    },
    'sc': {
        'file': 'sc-bank-statement.html',
        'name_zh': '渣打銀行',
        'name_en': 'Standard Chartered',
        'color': '#00843D',
        'logo': 'sc-logo.png'
    },
    'dbs': {
        'file': 'dbs-bank-statement.html',
        'name_zh': '星展銀行',
        'name_en': 'DBS',
        'color': '#D0262D',
        'logo': 'dbs-logo.png'
    },
    'bea': {
        'file': 'bea-bank-statement.html',
        'name_zh': '東亞銀行',
        'name_en': 'Bank of East Asia',
        'color': '#007A33',
        'logo': 'bea-logo.png'
    },
    'citibank': {
        'file': 'citibank-bank-statement.html',
        'name_zh': '花旗銀行',
        'name_en': 'Citibank',
        'color': '#0072CE',
        'logo': 'citibank-logo.png'
    },
    'dahsing': {
        'file': 'dahsing-bank-statement.html',
        'name_zh': '大新銀行',
        'name_en': 'Dah Sing Bank',
        'color': '#003A70',
        'logo': 'dahsing-logo.png'
    },
    'citic': {
        'file': 'citic-bank-statement.html',
        'name_zh': '中信銀行國際',
        'name_en': 'CITIC Bank',
        'color': '#C8102E',
        'logo': 'citic-logo.png'
    },
    'bankcomm': {
        'file': 'bankcomm-bank-statement.html',
        'name_zh': '交通銀行',
        'name_en': 'Bank of Communications',
        'color': '#004B8D',
        'logo': 'bankcomm-logo.png'
    }
}

def generate_image_list():
    """生成圖片需求清單"""
    
    print("=" * 80)
    print("📸 Landing Page 圖片需求清單")
    print("=" * 80)
    print()
    
    # 為每個銀行生成圖片清單
    for bank_id, bank_info in BANK_PAGES.items():
        bank_name_zh = bank_info['name_zh']
        bank_name_en = bank_info['name_en']
        
        print(f"\n### {bank_name_zh} ({bank_name_en})")
        print(f"檔案: {bank_info['file']}")
        print(f"品牌色: {bank_info['color']}")
        print()
        
        images = [
            {
                'num': 1,
                'type': 'Hero Banner',
                'size': '1920x800px',
                'format': 'WebP + JPG',
                'filename': f"{bank_id}-hero-banner",
                'description': f"{bank_name_zh}品牌色背景,左側標題文字,右側銀行對帳單mockup",
                'alt': f"{bank_name_zh}({bank_name_en})對帳單AI處理 - 3秒轉QuickBooks - VaultCaddy"
            },
            {
                'num': 2,
                'type': '上傳截圖',
                'size': '1200x800px',
                'format': 'WebP + PNG',
                'filename': f"{bank_id}-upload-interface",
                'description': f"VaultCaddy上傳界面截圖,標註支援{bank_name_zh}格式",
                'alt': f"{bank_name_zh}對帳單上傳界面 - 支援PDF和手機拍照 - VaultCaddy"
            },
            {
                'num': 3,
                'type': 'AI結果截圖',
                'size': '1200x800px',
                'format': 'WebP + PNG',
                'filename': f"{bank_id}-ai-result",
                'description': f"顯示{bank_name_zh}對帳單AI識別結果表格,標註98%準確率",
                'alt': f"{bank_name_zh}對帳單AI識別結果 - 98%準確率 - VaultCaddy"
            },
            {
                'num': 4,
                'type': '流程圖',
                'size': '1000x600px',
                'format': 'SVG/WebP',
                'filename': f"{bank_id}-workflow-diagram",
                'description': f"3步驟處理{bank_name_zh}對帳單: 上傳→AI處理→匯出",
                'alt': f"{bank_name_zh}對帳單處理流程 - 3步驟完成 - VaultCaddy"
            },
            {
                'num': 5,
                'type': '數據對比圖',
                'size': '800x600px',
                'format': 'WebP + PNG',
                'filename': f"{bank_id}-savings-comparison",
                'description': f"手動vs AI處理{bank_name_zh}對帳單的時間/成本對比",
                'alt': f"{bank_name_zh}對帳單手動vs AI處理對比 - 節省時間和金錢 - VaultCaddy"
            }
        ]
        
        for img in images:
            print(f"  [{img['num']}] {img['type']}")
            print(f"      檔名: {img['filename']}.webp / {img['filename']}.jpg")
            print(f"      尺寸: {img['size']}")
            print(f"      格式: {img['format']}")
            print(f"      內容: {img['description']}")
            print(f"      Alt: {img['alt']}")
            print()
    
    # 統計
    total_images = len(BANK_PAGES) * 5
    print("\n" + "=" * 80)
    print(f"總計: {len(BANK_PAGES)}個銀行 × 5張圖片 = {total_images}張圖片")
    print("=" * 80)
    
    # 生成檔案夾結構建議
    print("\n\n📁 建議的圖片檔案夾結構:")
    print("""
images/
├── banks/
│   ├── logos/
│   │   ├── hsbc-logo.png
│   │   ├── hangseng-logo.png
│   │   └── ... (其他銀行Logo)
│   ├── hero/
│   │   ├── hsbc-hero-banner.webp
│   │   ├── hsbc-hero-banner.jpg
│   │   └── ... (其他銀行Hero)
│   ├── screenshots/
│   │   ├── hsbc-upload-interface.webp
│   │   ├── hsbc-ai-result.webp
│   │   └── ... (其他銀行截圖)
│   ├── diagrams/
│   │   ├── hsbc-workflow-diagram.svg
│   │   └── ... (其他銀行流程圖)
│   └── charts/
│       ├── hsbc-savings-comparison.webp
│       └── ... (其他銀行圖表)
""")

def generate_image_insertion_code(bank_id, bank_info):
    """為指定銀行生成圖片插入代碼"""
    
    bank_name_zh = bank_info['name_zh']
    bank_name_en = bank_info['name_en']
    brand_color = bank_info['color']
    
    code = f"""
<!-- ============================================ -->
<!-- 圖片優化 - {bank_name_zh}({bank_name_en}) -->
<!-- ============================================ -->

<!-- 圖片1: Hero Banner -->
<section class="hero" style="background: linear-gradient(135deg, {brand_color} 0%, #555 100%); position: relative; overflow: hidden;">
    <picture>
        <source srcset="/images/banks/hero/{bank_id}-hero-banner.webp" type="image/webp">
        <img src="/images/banks/hero/{bank_id}-hero-banner.jpg" 
             alt="{bank_name_zh}({bank_name_en})對帳單AI處理 - 3秒轉QuickBooks - VaultCaddy"
             loading="eager"
             width="1920"
             height="800"
             style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.2;">
    </picture>
    
    <div class="hero-content" style="position: relative; z-index: 1; padding: 5rem 2rem; max-width: 1200px; margin: 0 auto;">
        <h1>{bank_name_zh}({bank_name_en})對帳單AI自動處理</h1>
        <p class="hero-subtitle">3秒轉QuickBooks/Excel | 98%準確率 | HK$30/月起</p>
        <a href="#signup" class="cta-button">免費試用20頁 →</a>
    </div>
</section>

<!-- 圖片2: 上傳界面截圖 -->
<section class="how-it-works" style="padding: 5rem 2rem; background: #f9fafb;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;">
            如何使用VaultCaddy處理{bank_name_zh}對帳單？
        </h2>
        
        <div class="step" style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; margin-bottom: 4rem;">
            <div class="step-image">
                <picture>
                    <source srcset="/images/banks/screenshots/{bank_id}-upload-interface.webp" type="image/webp">
                    <img src="/images/banks/screenshots/{bank_id}-upload-interface.png" 
                         alt="{bank_name_zh}對帳單上傳界面 - 支援PDF和手機拍照 - VaultCaddy"
                         loading="lazy"
                         width="1200"
                         height="800"
                         style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                </picture>
            </div>
            
            <div class="step-text">
                <div class="step-number" style="background: {brand_color}; color: white; width: 3rem; height: 3rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">1</div>
                <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">上傳{bank_name_zh}對帳單</h3>
                <ul style="font-size: 1.1rem; line-height: 2;">
                    <li>✅ 從{bank_name_zh}網上銀行下載PDF</li>
                    <li>✅ 或用手機拍攝紙質對帳單</li>
                    <li>✅ 支援多頁對帳單</li>
                    <li>✅ 拖放或點擊上傳</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- 圖片3: AI識別結果截圖 -->
<section class="ai-results" style="padding: 5rem 2rem;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;">
            AI自動識別{bank_name_zh}對帳單
        </h2>
        
        <div class="result-showcase" style="position: relative;">
            <picture>
                <source srcset="/images/banks/screenshots/{bank_id}-ai-result.webp" type="image/webp">
                <img src="/images/banks/screenshots/{bank_id}-ai-result.png" 
                     alt="{bank_name_zh}對帳單AI識別結果 - 98%準確率 - VaultCaddy"
                     loading="lazy"
                     width="1200"
                     height="800"
                     style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            </picture>
            
            <div class="result-highlights" style="display: flex; justify-content: space-around; margin-top: 2rem;">
                <div class="highlight" style="text-align: center;">
                    <span class="icon" style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">⚡</span>
                    <span class="text" style="font-size: 1.1rem; font-weight: 600;">3秒完成處理</span>
                </div>
                <div class="highlight" style="text-align: center;">
                    <span class="icon" style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">✓</span>
                    <span class="text" style="font-size: 1.1rem; font-weight: 600;">98%識別準確率</span>
                </div>
                <div class="highlight" style="text-align: center;">
                    <span class="icon" style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">✎</span>
                    <span class="text" style="font-size: 1.1rem; font-weight: 600;">可人工編輯修正</span>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 圖片4: 流程圖 -->
<section class="workflow" style="padding: 5rem 2rem; background: #f9fafb;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;">
            3步驟完成{bank_name_zh}對帳單處理
        </h2>
        
        <div class="workflow-diagram" style="text-align: center; margin-bottom: 3rem;">
            <picture>
                <source srcset="/images/banks/diagrams/{bank_id}-workflow-diagram.webp" type="image/webp">
                <img src="/images/banks/diagrams/{bank_id}-workflow-diagram.svg" 
                     alt="{bank_name_zh}對帳單處理流程 - 3步驟完成 - VaultCaddy"
                     loading="lazy"
                     width="1000"
                     height="600"
                     style="max-width: 100%; height: auto;">
            </picture>
        </div>
        
        <!-- 備用: HTML實現的流程圖 -->
        <div class="workflow-steps" style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 1rem; align-items: center;">
            <div class="workflow-step" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="step-icon" style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                <div class="step-number" style="background: {brand_color}; color: white; width: 2.5rem; height: 2.5rem; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; margin-bottom: 1rem;">1</div>
                <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">上傳{bank_name_zh}對帳單</h3>
                <p style="color: #666; margin-bottom: 1rem;">支援PDF/拍照</p>
                <span class="step-time" style="background: #fef3c7; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">30秒</span>
            </div>
            
            <div class="workflow-arrow" style="font-size: 2rem; color: {brand_color};">→</div>
            
            <div class="workflow-step" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="step-icon" style="font-size: 4rem; margin-bottom: 1rem;">🤖</div>
                <div class="step-number" style="background: {brand_color}; color: white; width: 2.5rem; height: 2.5rem; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; margin-bottom: 1rem;">2</div>
                <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">AI自動識別</h3>
                <p style="color: #666; margin-bottom: 1rem;">提取所有交易</p>
                <span class="step-time" style="background: #d1fae5; color: #065f46; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">3秒</span>
            </div>
            
            <div class="workflow-arrow" style="font-size: 2rem; color: {brand_color};">→</div>
            
            <div class="workflow-step" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="step-icon" style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <div class="step-number" style="background: {brand_color}; color: white; width: 2.5rem; height: 2.5rem; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; margin-bottom: 1rem;">3</div>
                <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem;">一鍵匯出</h3>
                <p style="color: #666; margin-bottom: 1rem;">QuickBooks/Excel</p>
                <span class="step-time" style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">5秒</span>
            </div>
        </div>
    </div>
</section>

<!-- 圖片5: 數據對比圖 -->
<section class="savings" style="padding: 5rem 2rem;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem;">
            使用VaultCaddy處理{bank_name_zh}對帳單能節省多少？
        </h2>
        
        <div class="comparison-chart" style="text-align: center; margin-bottom: 3rem;">
            <picture>
                <source srcset="/images/banks/charts/{bank_id}-savings-comparison.webp" type="image/webp">
                <img src="/images/banks/charts/{bank_id}-savings-comparison.png" 
                     alt="{bank_name_zh}對帳單手動vs AI處理對比 - 節省時間和金錢 - VaultCaddy"
                     loading="lazy"
                     width="800"
                     height="600"
                     style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            </picture>
        </div>
        
        <!-- 補充數據卡片 -->
        <div class="savings-cards" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
            <div class="card" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="card-icon" style="font-size: 3rem; margin-bottom: 1rem;">⏱️</div>
                <div class="card-value" style="font-size: 1.8rem; font-weight: 700; color: {brand_color}; margin-bottom: 0.5rem;">2小時 → 3秒</div>
                <div class="card-label" style="color: #666;">處理時間節省</div>
            </div>
            
            <div class="card" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="card-icon" style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
                <div class="card-value" style="font-size: 1.8rem; font-weight: 700; color: {brand_color}; margin-bottom: 0.5rem;">HK$170/月</div>
                <div class="card-label" style="color: #666;">成本節省</div>
            </div>
            
            <div class="card" style="background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div class="card-icon" style="font-size: 3rem; margin-bottom: 1rem;">✓</div>
                <div class="card-value" style="font-size: 1.8rem; font-weight: 700; color: {brand_color}; margin-bottom: 0.5rem;">98% vs 85%</div>
                <div class="card-label" style="color: #666;">準確率提升</div>
            </div>
        </div>
    </div>
</section>

<!-- ============================================ -->
<!-- 圖片優化結束 -->
<!-- ============================================ -->
"""
    
    return code

def main():
    """主函數"""
    
    print("\n" + "=" * 80)
    print("🎨 VaultCaddy Landing Page 圖片優化工具")
    print("=" * 80)
    print()
    
    # 選單
    print("請選擇操作:")
    print("1. 生成圖片需求清單")
    print("2. 生成圖片插入代碼(單個銀行)")
    print("3. 生成圖片插入代碼(所有銀行)")
    print()
    
    choice = input("請輸入選項(1-3): ").strip()
    
    if choice == '1':
        generate_image_list()
        
    elif choice == '2':
        print("\n可選銀行:")
        for i, (bank_id, bank_info) in enumerate(BANK_PAGES.items(), 1):
            print(f"{i}. {bank_info['name_zh']} ({bank_id})")
        
        bank_num = int(input("\n請選擇銀行編號: ").strip())
        bank_id = list(BANK_PAGES.keys())[bank_num - 1]
        bank_info = BANK_PAGES[bank_id]
        
        code = generate_image_insertion_code(bank_id, bank_info)
        
        # 保存到檔案
        output_file = f"image_code_{bank_id}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"\n✅ 已生成圖片插入代碼: {output_file}")
        print(f"請將代碼複製到 {bank_info['file']} 中")
        
    elif choice == '3':
        # 為所有銀行生成代碼
        for bank_id, bank_info in BANK_PAGES.items():
            code = generate_image_insertion_code(bank_id, bank_info)
            
            output_file = f"image_code_{bank_id}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"✅ 已生成: {output_file} ({bank_info['name_zh']})")
        
        print(f"\n✅ 已為 {len(BANK_PAGES)} 個銀行生成圖片插入代碼")
    
    else:
        print("❌ 無效選項")

if __name__ == '__main__':
    main()

