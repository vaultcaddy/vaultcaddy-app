#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正日本和韩国版本的价格
日本：¥10/枚
韩国：₩80/페이지
"""

import re

def fix_jp_pricing():
    """修正日文版价格为¥10"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/jp/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修正所有¥8相关的价格为¥10
    # 1. 标题中的价格
    content = re.sub(r'1枚¥8', '1枚¥10', content)
    content = re.sub(r'¥8/枚', '¥10/枚', content)
    content = re.sub(r'1枚¥8から', '1枚¥10から', content)
    
    # 2. 描述中的价格
    content = re.sub(r'月額¥900', '月額¥1,158', content)
    
    # 3. Schema.org中的价格
    content = re.sub(r'"price": "900"', '"price": "1158"', content)
    content = re.sub(r'"price": "8"', '"price": "10"', content)
    
    # 4. 页面显示的价格（如果有）
    content = re.sub(r'低至 ¥9/頁', '低至 ¥10/頁', content)
    content = re.sub(r'起价为 ¥9', '起价为 ¥10', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 日文版价格已修正为 ¥10/枚")

def fix_kr_pricing():
    """确认韩文版价格为₩80（可能需要微调其他地方）"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/kr/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查并修正所有价格为₩80
    content = re.sub(r'페이지당 ₩85', '페이지당 ₩80', content)
    content = re.sub(r'₩85/페이지', '₩80/페이지', content)
    
    # 修正月费（₩9,000 应该是对的，对应20倍汇率）
    # 确认显示的价格
    content = re.sub(r'低至 ₩950/頁', '低至 ₩80/頁', content)
    content = re.sub(r'起价为 ₩950', '起价为 ₩80', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 韩文版价格已确认为 ₩80/페이지")

def update_seo_report():
    """更新SEO报告中的价格"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/SEO_Optimization_Master_Report.md'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修正日文价格
    content = content.replace('¥8/枚', '¥10/枚')
    content = content.replace('1枚¥8', '1枚¥10')
    content = content.replace('月額¥900', '月額¥1,158')
    content = content.replace('¥8 | ¥900', '¥10 | ¥1,158')
    
    # 确认韩文价格
    content = content.replace('페이지당 ₩85', '페이지당 ₩80')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SEO报告价格已更新")

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 修正日本和韩国版本价格")
    print("=" * 60)
    print()
    print("正确价格：")
    print("🇯🇵 日本：¥10/枚（月费 ¥1,158）")
    print("🇰🇷 韩国：₩80/페이지（月费 ₩9,000）")
    print()
    print("=" * 60)
    print()
    
    # 1. 修正日文版
    fix_jp_pricing()
    
    # 2. 修正韩文版
    fix_kr_pricing()
    
    # 3. 更新SEO报告
    update_seo_report()
    
    print()
    print("=" * 60)
    print("✅ 所有价格已修正完成！")
    print("=" * 60)
    print()
    print("修正总结：")
    print("📝 日文版：¥8/枚 → ¥10/枚")
    print("📝 韩文版：确认为 ₩80/페이지")
    print("📝 SEO报告已更新")

