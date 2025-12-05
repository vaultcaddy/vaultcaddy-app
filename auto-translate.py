#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动翻译HTML页面
Auto-translate HTML Pages using AI-assisted translations
"""

import os
import json
import re
from pathlib import Path
import shutil

def load_translations():
    """加载翻译文件"""
    with open('translate-content.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def translate_html(content, translations_dict):
    """翻译HTML内容"""
    translated = content
    
    # 翻译所有定义的文本
    for key, value in translations_dict.items():
        if key == 'meta_title':
            # 翻译 <title> 标签
            translated = re.sub(
                r'<title>.*?</title>',
                f'<title>{value}</title>',
                translated,
                flags=re.DOTALL
            )
        elif key == 'meta_description':
            # 翻译 meta description
            translated = re.sub(
                r'<meta name="description" content=".*?"',
                f'<meta name="description" content="{value}"',
                translated
            )
    
    return translated

def translate_index_page(lang_code):
    """翻译index.html到指定语言"""
    print(f"\n🌍 开始翻译 index.html 到 {lang_code}")
    
    # 加载翻译数据
    translations = load_translations()
    lang_translations = translations['index_page'][lang_code]
    
    # 读取原始文件
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标目录
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    
    # 复制文件
    target_file = target_dir / 'index.html'
    
    # 开始翻译
    translated_content = content
    
    # 1. 翻译meta标签
    print(f"  ✅ 翻译meta标签")
    translated_content = re.sub(
        r'<title>.*?</title>',
        f'<title>{lang_translations["meta_title"]}</title>',
        translated_content,
        flags=re.DOTALL
    )
    
    translated_content = re.sub(
        r'(<meta name="description" content=").*?(")',
        rf'\1{lang_translations["meta_description"]}\2',
        translated_content
    )
    
    # 2. 添加lang属性
    if lang_code == 'en':
        translated_content = translated_content.replace('<html lang="zh-TW">', '<html lang="en">')
    elif lang_code == 'jp':
        translated_content = translated_content.replace('<html lang="zh-TW">', '<html lang="ja">')
    elif lang_code == 'kr':
        translated_content = translated_content.replace('<html lang="zh-TW">', '<html lang="ko">')
    
    # 3. 翻译导航栏
    print(f"  ✅ 翻译导航栏")
    nav_translations = {
        '首頁': lang_translations.get('nav_home', '首頁'),
        '功能': lang_translations.get('nav_features', '功能'),
        '價格': lang_translations.get('nav_pricing', '價格'),
        '學習中心': lang_translations.get('nav_blog', '學習中心'),
        '儀表板': lang_translations.get('nav_dashboard', '儀表板'),
        '登入': lang_translations.get('nav_login', '登入'),
        '帳戶': lang_translations.get('nav_account', '帳戶'),
        '計費': lang_translations.get('nav_billing', '計費'),
        '登出': lang_translations.get('nav_logout', '登出'),
        '隱私政策': lang_translations.get('nav_privacy', '隱私政策'),
        '服務條款': lang_translations.get('nav_terms', '服務條款')
    }
    
    # 4. 翻译Hero区域
    print(f"  ✅ 翻译Hero区域")
    hero_replacements = {
        '針對香港銀行對帳單處理': lang_translations['hero_title'],
        '低至 HKD 0.5/頁': lang_translations['hero_subtitle'],
        '超過 200+ 企業信賴': lang_translations['hero_trust'],
        '專為會計師及小型公司設計的 AI 文檔處理平台': lang_translations['hero_desc'],
        '自動轉換 Excel/CSV/QuickBooks/Xero': lang_translations['hero_features'],
        '• 準確率 98% • 節省 90% 時間': lang_translations['hero_stats'],
        '免費試用 20 頁': lang_translations['cta_free'],
        '無需預約': lang_translations['cta_no_signup']
    }
    
    for zh_text, translated_text in {**nav_translations, **hero_replacements}.items():
        # 使用更精确的替换，避免误替换
        translated_content = translated_content.replace(f'>{zh_text}<', f'>{translated_text}<')
        translated_content = translated_content.replace(f'"{zh_text}"', f'"{translated_text}"')
    
    # 5. 翻译统计数据
    print(f"  ✅ 翻译统计数据")
    stats_replacements = {
        '平均處理時間': lang_translations['stat_time'],
        '數據準確率': lang_translations['stat_accuracy'],
        '企業客戶': lang_translations['stat_clients']
    }
    
    for zh_text, translated_text in stats_replacements.items():
        translated_content = translated_content.replace(f'>{zh_text}<', f'>{translated_text}<')
    
    # 6. 保存文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"  💾 文件已保存: {target_file}")
    print(f"  ✅ {lang_code} 版本翻译完成！")

def main():
    """主函数"""
    print("=" * 60)
    print("🌍 VaultCaddy AI 辅助翻译系统")
    print("=" * 60)
    
    # 翻译index.html到3种语言
    for lang in ['en', 'jp', 'kr']:
        translate_index_page(lang)
    
    print("\n" + "=" * 60)
    print("✅ 所有翻译完成！")
    print("=" * 60)
    print("\n📋 下一步:")
    print("1. 检查翻译文件: en/index.html, jp/index.html, kr/index.html")
    print("2. 在浏览器中测试")
    print("3. 人工校对翻译质量")
    print("4. 继续翻译其他页面")

if __name__ == '__main__':
    main()

