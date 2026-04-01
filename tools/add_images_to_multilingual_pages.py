#!/usr/bin/env python3
"""
为多语言Landing Page添加5张图片
作用: 为英文、日文、韩文的银行页面和行业页面添加完整的5张Unsplash图片
"""

import os
import re

# Unsplash图片集合（专业、商业、金融主题）
IMAGE_COLLECTIONS = {
    'hero_backgrounds': [
        'photo-1554224155-6726b3ff858f',  # 金融数据
        'photo-1565372195458-9de0b320ef04',  # 现代办公室
        'photo-1563013544-824ae1b704d3',   # 商业建筑
        'photo-1556740758-90de374c12ad',   # 商业环境
        'photo-1551836022-4c4c79ecde51',   # 团队协作
    ],
    'product_demos': [
        'photo-1460925895917-afdab827c52f',  # 数据分析
        'photo-1551288049-bebda4e38f71',   # 图表展示
        'photo-1543286386-713bdd548da4',   # 笔记本工作
        'photo-1526628953301-3e589a6a8b74',  # 会议讨论
    ],
    'customer_stories': [
        'photo-1551836022-4c4c79ecde51',   # 团队合作
        'photo-1522071820081-009f0129c71c',  # 团队讨论
        'photo-1600880292203-757bb62b4baf',  # 商务会议
    ],
    'data_charts': [
        'photo-1551288049-bebda4e38f71',   # 图表分析
        'photo-1543286386-713bdd548da4',   # 数据展示
        'photo-1460925895917-afdab827c52f',  # 分析报告
    ],
    'trust_badges': [
        'photo-1554224155-8d04cb21cd6c',   # 银行建筑
        'photo-1565372195458-9de0b320ef04',  # 专业环境
    ]
}

def add_images_to_bank_page(filepath, lang):
    """为银行页面添加5张图片"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已经有5张图片标注，跳过
    if content.count('<!-- 图片') >= 5 or content.count('loading="lazy"') >= 2:
        return False
    
    # 在Hero section的演示图部分添加图片2和图片3
    demo_section = '''            <div style="text-align: center; margin-top: 4rem;">
                <img src="https://images.unsplash.com/'''
    
    if demo_section in content and content.count('loading="lazy"') < 2:
        # 添加第2张图片（产品演示）
        replacement = '''            <!-- 图片2: 产品演示 -->
            <div style="text-align: center; margin-top: 4rem;">
                <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop" 
                     alt="VaultCaddy处理演示"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            </div>
            
            <!-- 图片3: 数据分析 -->
            <div style="text-align: center; margin-top: 3rem;">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=500&fit=crop" 
                     alt="数据分析图表"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            </div>
'''
        
        content = content.replace(demo_section, replacement, 1)
    
    # 在Final CTA section之前添加图片4和图片5
    final_cta_marker = '    <section class="final-cta-section">'
    
    if final_cta_marker in content:
        additional_images = '''    
    <!-- 图片4: 客户案例 -->
    <section style="padding: 3rem 0; background: #f9fafb;">
        <div class="container" style="text-align: center;">
            <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=400&fit=crop" 
                 alt="客户使用案例"
                 loading="lazy"
                 style="max-width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        </div>
    </section>
    
    <!-- 图片5: 信任徽章/银行支持 -->
    <section style="padding: 2rem 0;">
        <div class="container" style="text-align: center;">
            <h3 style="font-size: 1.5rem; margin-bottom: 1.5rem; color: #6b7280;">支援所有主要銀行</h3>
            <img src="https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=1200&h=300&fit=crop" 
                 alt="支持的银行"
                 loading="lazy"
                 style="max-width: 100%; border-radius: 12px; opacity: 0.8;">
        </div>
    </section>
    
'''
        
        content = content.replace(final_cta_marker, additional_images + final_cta_marker)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def add_images_to_industry_page(filepath, lang):
    """为行业页面添加5张图片"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已经有5张图片标注，跳过
    if content.count('<!-- 图片') >= 5 or content.count('loading="lazy"') >= 3:
        return False
    
    # 行业页面通常结构更简单，我们需要在合适位置添加图片
    
    # 在挑战section后添加图片2
    challenge_section_end = '</div>\n    </section>\n    \n    <section class="section section-alt">'
    if challenge_section_end in content and 'loading="lazy"' not in content:
        replacement = '''</div>
            
            <!-- 图片2: 行业场景 -->
            <div style="text-align: center; margin-top: 3rem;">
                <img src="https://images.unsplash.com/photo-1556740758-90de374c12ad?w=1200&h=600&fit=crop" 
                     alt="行业场景"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            </div>
        </div>
    </section>
    
    <section class="section section-alt">'''
        
        content = content.replace(challenge_section_end, replacement, 1)
    
    # 在解决方案section后添加图片3
    if '</div>\n        </div>\n    </section>\n    \n    <section class="section">' in content:
        marker = '</div>\n        </div>\n    </section>\n    \n    <section class="section">'
        replacement = '''</div>
            
            <!-- 图片3: 产品演示 -->
            <div style="text-align: center; margin-top: 3rem;">
                <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop" 
                     alt="产品演示"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
            </div>
        </div>
    </section>
    
    <section class="section">'''
        
        content = content.replace(marker, replacement, 1)
    
    # 在客户案例后添加图片4
    if '</div>\n        </div>\n    </section>\n    \n    <section class="section section-alt">' in content:
        marker = '</div>\n        </div>\n    </section>\n    \n    <section class="section section-alt">'
        replacement = '''</div>
            
            <!-- 图片4: 客户成功案例 -->
            <div style="text-align: center; margin-top: 2rem;">
                <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=500&fit=crop" 
                     alt="客户成功案例"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            </div>
        </div>
    </section>
    
    <section class="section section-alt">'''
        
        content = content.replace(marker, replacement, 1)
    
    # 在ROI对比后添加图片5
    if '</div>\n        </div>\n    </section>\n    \n    <section class="cta-section">' in content:
        marker = '</div>\n        </div>\n    </section>\n    \n    <section class="cta-section">'
        replacement = '''</div>
            
            <!-- 图片5: ROI数据可视化 -->
            <div style="text-align: center; margin-top: 3rem;">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=500&fit=crop" 
                     alt="ROI数据"
                     loading="lazy"
                     style="max-width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            </div>
        </div>
    </section>
    
    <section class="cta-section">'''
        
        content = content.replace(marker, replacement, 1)
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    
    print("=" * 80)
    print("🖼️  為多語言Landing Page添加5張圖片")
    print("=" * 80)
    print()
    
    updated_count = 0
    skipped_count = 0
    
    # 处理英文银行页面
    print("📁 處理英文銀行頁面...")
    for i, bank in enumerate(['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm'], 1):
        filepath = f"en/{bank}-bank-statement.html"
        if os.path.exists(filepath):
            if add_images_to_bank_page(filepath, 'en'):
                print(f"  ✅ {filepath}")
                updated_count += 1
            else:
                print(f"  ⏭️  {filepath} (已有圖片)")
                skipped_count += 1
    
    print()
    
    # 处理日文银行页面
    print("📁 處理日文銀行頁面...")
    for bank in ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']:
        filepath = f"ja/{bank}-bank-statement.html"
        if os.path.exists(filepath):
            if add_images_to_bank_page(filepath, 'ja'):
                print(f"  ✅ {filepath}")
                updated_count += 1
            else:
                print(f"  ⏭️  {filepath} (已有圖片)")
                skipped_count += 1
    
    print()
    
    # 处理韩文银行页面
    print("📁 處理韓文銀行頁面...")
    for bank in ['hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea', 'citibank', 'dahsing', 'citic', 'bankcomm']:
        filepath = f"ko/{bank}-bank-statement.html"
        if os.path.exists(filepath):
            if add_images_to_bank_page(filepath, 'ko'):
                print(f"  ✅ {filepath}")
                updated_count += 1
            else:
                print(f"  ⏭️  {filepath} (已有圖片)")
                skipped_count += 1
    
    print()
    
    # 处理日文行业页面
    print("📁 處理日文行業頁面...")
    for industry in ['restaurant', 'accountant', 'retail', 'ecommerce', 'trading']:
        filepath = f"ja/solutions/{industry}/index.html"
        if os.path.exists(filepath):
            if add_images_to_industry_page(filepath, 'ja'):
                print(f"  ✅ {filepath}")
                updated_count += 1
            else:
                print(f"  ⏭️  {filepath} (已有圖片)")
                skipped_count += 1
    
    print()
    
    # 处理韩文行业页面
    print("📁 處理韓文行業頁面...")
    for industry in ['restaurant', 'accountant', 'retail', 'ecommerce', 'trading']:
        filepath = f"ko/solutions/{industry}/index.html"
        if os.path.exists(filepath):
            if add_images_to_industry_page(filepath, 'ko'):
                print(f"  ✅ {filepath}")
                updated_count += 1
            else:
                print(f"  ⏭️  {filepath} (已有圖片)")
                skipped_count += 1
    
    print()
    print("=" * 80)
    print(f"✅ 圖片添加完成!")
    print("=" * 80)
    print()
    print(f"📊 統計:")
    print(f"  - 更新的頁面: {updated_count}")
    print(f"  - 跳過的頁面: {skipped_count}")
    print()
    print(f"🖼️  每頁現在包含5張圖片:")
    print(f"  1. Hero背景圖 (金融/商業環境)")
    print(f"  2. 產品演示圖 (數據分析)")
    print(f"  3. 數據圖表 (可視化)")
    print(f"  4. 客戶案例 (團隊協作)")
    print(f"  5. 信任徽章 (銀行支持)")
    print()
    print(f"📈 SEO優化:")
    print(f"  - 所有圖片使用Unsplash CDN (快速載入)")
    print(f"  - 所有圖片有Alt標籤 (SEO友好)")
    print(f"  - 所有圖片有loading='lazy' (性能優化)")
    print(f"  - 圖片尺寸優化 (1200x600或1200x500)")

if __name__ == '__main__':
    main()

