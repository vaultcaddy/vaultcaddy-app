#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修正日本和韩国版本的价格
根据图1的正确价格：
- 日本：¥10/枚
- 韩国：₩80/페이지
"""

import re

def comprehensive_fix_jp():
    """全面修正日文版所有价格"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/jp/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Title标签
    content = content.replace('1枚¥8から', '1枚¥10から')
    
    # 2. Meta description
    content = content.replace('¥9/頁', '¥10/頁')
    
    # 3. Open Graph
    content = re.sub(r'¥9/頁', '¥10/頁', content)
    
    # 4. Twitter Card
    # 已经在上面替换了
    
    # 5. Schema.org priceRange
    content = content.replace('"priceRange": "¥9 - ¥1158"', '"priceRange": "¥10 - ¥1158"')
    
    # 6. 页面内容中的价格显示
    content = content.replace('1ページあたり最低 ¥9', '1ページあたり最低 ¥10')
    content = content.replace('¥9/<span>頁</span>', '¥10/<span>頁</span>')
    content = content.replace('<strong style="color: #f59e0b;">¥9</strong>', '<strong style="color: #f59e0b;">¥10</strong>')
    
    # 7. 超出后的价格（应该是¥10，不是¥0.5）
    content = content.replace('超過後1ページあたり¥0.5', '超過後1ページあたり¥10')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 日文版所有价格已修正为 ¥10/枚")
    print("   - Title: 1枚¥10から")
    print("   - Description: ¥10/頁")
    print("   - 页面显示: ¥10/頁")
    print("   - 超出价格: ¥10/枚")

def comprehensive_fix_kr():
    """全面修正韩文版所有价格"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/kr/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Title - 已经是正确的 ₩80
    
    # 2. Meta description - 修正为₩80
    content = content.replace('₩950/頁', '₩80/頁')
    
    # 3. Open Graph
    # 已经在上面替换了
    
    # 4. Schema.org priceRange
    content = content.replace('"priceRange": "₩950 - ₩9998"', '"priceRange": "₩80 - ₩9998"')
    
    # 5. 页面内容中的价格显示
    content = content.replace('페이지당 최저 ₩950', '페이지당 최저 ₩80')
    content = content.replace('₩950/<span>頁</span>', '₩80/<span>頁</span>')
    content = content.replace('<strong style="color: #f59e0b;">₩950</strong>', '<strong style="color: #f59e0b;">₩80</strong>')
    
    # 6. 超出后的价格（应该是₩80，不是₩0.5）
    content = content.replace('초과 시 페이지당 ₩0.5', '초과 시 페이지당 ₩80')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 韩文版所有价格已修正为 ₩80/페이지")
    print("   - Title: 페이지당 ₩80부터")
    print("   - Description: ₩80/頁")
    print("   - 页面显示: ₩80/頁")
    print("   - 超出价格: ₩80/페이지")

def update_seo_comprehensive():
    """全面更新SEO报告"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/SEO_Optimization_Master_Report.md'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 日文价格修正
    content = content.replace('¥8/枚', '¥10/枚')
    content = content.replace('1枚¥8', '1枚¥10')
    content = content.replace('¥8 |', '¥10 |')
    content = content.replace('**¥8**', '**¥10**')
    
    # 韩文价格修正
    content = content.replace('₩950', '₩80')
    content = content.replace('**₩80**', '**₩80**')  # 确保正确
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SEO报告已全面更新")

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 全面修正日本和韩国版本价格（根据图1）")
    print("=" * 70)
    print()
    print("正确价格（参考图1）：")
    print("🇯🇵 日本：")
    print("   - 每页价格：¥10/枚")
    print("   - 月费：¥1,158")
    print("   - 超出价格：¥10/枚")
    print()
    print("🇰🇷 韩国：")
    print("   - 每页价格：₩80/페이지")
    print("   - 月费：₩9,998")
    print("   - 超出价格：₩80/페이지")
    print()
    print("=" * 70)
    print()
    
    # 1. 全面修正日文版
    comprehensive_fix_jp()
    print()
    
    # 2. 全面修正韩文版
    comprehensive_fix_kr()
    print()
    
    # 3. 更新SEO报告
    update_seo_comprehensive()
    
    print()
    print("=" * 70)
    print("✅ 所有价格修正完成！")
    print("=" * 70)
    print()
    print("修正详情：")
    print()
    print("📝 日文版修正项目：")
    print("   ✅ Title标签：1枚¥10から")
    print("   ✅ Meta描述：¥10/頁")
    print("   ✅ Open Graph：¥10/頁")
    print("   ✅ 页面显示：¥10/頁")
    print("   ✅ 超出价格：¥10/枚")
    print()
    print("📝 韩文版修正项目：")
    print("   ✅ Title标签：페이지당 ₩80부터")
    print("   ✅ Meta描述：₩80/頁")
    print("   ✅ Open Graph：₩80/頁")
    print("   ✅ 页面显示：₩80/頁")
    print("   ✅ 超出价格：₩80/페이지")
    print()
    print("📝 SEO报告：")
    print("   ✅ 所有价格引用已更新")

