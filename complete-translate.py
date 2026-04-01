#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译系统 - VaultCaddy Index.html
Complete Translation System for Index.html
"""

import json
import re
from pathlib import Path

def load_complete_translations():
    """加载完整翻译数据"""
    with open('complete-translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def safe_replace(content, old_text, new_text, context=""):
    """安全地替换文本，避免误替换"""
    count = 0
    
    # 方法1: 在标签之间替换 >old_text<
    pattern1 = f'>{re.escape(old_text)}<'
    replacement1 = f'>{new_text}<'
    new_content, n1 = re.subn(pattern1, replacement1, content)
    count += n1
    content = new_content
    
    # 方法2: 在属性中替换 "old_text"
    pattern2 = f'"{re.escape(old_text)}"'
    replacement2 = f'"{new_text}"'
    new_content, n2 = re.subn(pattern2, replacement2, content)
    count += n2
    content = new_content
    
    # 方法3: 在按钮/链接文本中替换（考虑空格）
    pattern3 = f'>{re.escape(old_text)}\\s*<'
    replacement3 = f'>{new_text}<'
    new_content, n3 = re.subn(pattern3, replacement3, content)
    count += n3
    content = new_content
    
    if count > 0 and context:
        print(f"    ✓ {context}: 替换{count}处")
    
    return content

def translate_index_complete(lang_code):
    """完整翻译index.html"""
    print(f"\n{'='*60}")
    print(f"🌍 开始完整翻译 index.html → {lang_code}")
    print(f"{'='*60}")
    
    # 加载翻译数据
    translations = load_complete_translations()
    lang_trans = translations['index_complete'][lang_code]
    zh_trans = translations['index_complete']['zh']
    
    # 读取原始文件
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建目标目录
    target_dir = Path(lang_code)
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir / 'index.html'
    
    # 翻译计数器
    sections_translated = 0
    
    # 1. Meta标签
    print("\n📋 第1步: 翻译Meta标签")
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{lang_trans.get("meta_title", zh_trans["nav_home"])}</title>',
        content,
        flags=re.DOTALL
    )
    
    # 修改lang属性
    lang_attr = {'en': 'en', 'jp': 'ja', 'kr': 'ko'}.get(lang_code, lang_code)
    content = content.replace('<html lang="zh-TW">', f'<html lang="{lang_attr}">')
    sections_translated += 1
    print("  ✅ Meta标签完成")
    
    # 2. 导航栏
    print("\n📋 第2步: 翻译导航栏")
    nav_items = [
        ('nav_home', '首頁'),
        ('nav_features', '功能'),
        ('nav_pricing', '價格'),
        ('nav_blog', '學習中心'),
        ('nav_dashboard', '儀表板'),
        ('nav_login', '登入'),
        ('nav_account', '帳戶'),
        ('nav_billing', '計費'),
        ('nav_logout', '登出'),
        ('nav_privacy', '隱私政策'),
        ('nav_terms', '服務條款')
    ]
    
    for key, zh_text in nav_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 导航栏完成")
    
    # 3. Hero区域
    print("\n📋 第3步: 翻译Hero区域")
    hero_items = [
        ('hero_title', '針對香港銀行對帳單處理'),
        ('hero_subtitle', '低至 HKD 0.5/頁'),
        ('hero_trust', '超過 200+ 企業信賴'),
        ('hero_desc', '專為會計師及小型公司設計的 AI 文檔處理平台'),
        ('hero_features', '自動轉換 Excel/CSV/QuickBooks/Xero'),
        ('hero_stats', '• 準確率 98% • 節省 90% 時間'),
        ('cta_free', '免費試用 20 頁'),
        ('cta_no_signup', '無需預約')
    ]
    
    for key, zh_text in hero_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ Hero区域完成")
    
    # 4. 统计数据
    print("\n📋 第4步: 翻译统计数据")
    stat_items = [
        ('stat_time', '平均處理時間'),
        ('stat_accuracy', '數據準確率'),
        ('stat_clients', '企業客戶')
    ]
    
    for key, zh_text in stat_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 统计数据完成")
    
    # 5. 功能区域
    print("\n📋 第5步: 翻译功能区域")
    feature_items = [
        ('features_title', '強大功能'),
        ('features_subtitle', '一站式 AI 文檔處理平台'),
        ('features_desc', '支援發票、收據、銀行對賬單等多種財務文檔'),
        ('section1_badge', '智能發票收據處理'),
        ('section1_feature1_title', 'OCR 光學辨識技術'),
        ('section1_feature1_desc', '準確擷取商家、日期、金額、稅項等關鍵資料'),
        ('section1_feature2_title', '智能分類歸檔'),
        ('section1_feature2_desc', '自動識別發票類型並歸類到對應會計科目'),
        ('section1_feature3_title', '即時同步到會計軟件'),
        ('section1_feature3_desc', '一鍵匯出QuickBooks、Xero 等主流平台格式'),
        ('section2_badge', '銀行對賬單智能分析'),
        ('section2_feature1_title', '智能交易分類'),
        ('section2_feature1_desc', '自動識別收入、支出、轉賬類別並歸類'),
        ('section2_feature2_title', '精準數據提取'),
        ('section2_feature2_desc', '準確擷取日期、對方賬戶、金額等關鍵資料'),
        ('section2_feature3_title', '多格式匯出'),
        ('section2_feature3_desc', '支援匯出到 Excel、CSV、QuickBooks、Xero 等')
    ]
    
    for key, zh_text in feature_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 功能区域完成")
    
    # 6. 价值主张
    print("\n📋 第6步: 翻译价值主张")
    value_items = [
        ('why_title', '為什麼選擇 VaultCaddy'),
        ('why_subtitle', '專為香港會計師打造'),
        ('why_desc', '提升效率，降低成本，讓您專注於更有價值的工作'),
        ('value1_title', '極速處理'),
        ('value2_title', '超高準確率'),
        ('value3_title', '性價比最高')
    ]
    
    for key, zh_text in value_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 价值主张完成")
    
    # 7. 定价区域
    print("\n📋 第7步: 翻译定价区域")
    pricing_items = [
        ('pricing_title', '輕鬆處理銀行對帳單'),
        ('pricing_monthly', '月付'),
        ('pricing_yearly', '年付'),
        ('pricing_save', '節省 20%'),
        ('pricing_per_month', '/月'),
        ('pricing_monthly_credits', '每月 100 Credits'),
        ('pricing_overage', '超出後每頁 HKD $0.5'),
        ('pricing_cta', '開始使用'),
        ('pricing_feature1', '發票/收據處理'),
        ('pricing_feature2', '銀行對賬單處理'),
        ('pricing_feature3', 'Excel/CSV 匯出'),
        ('pricing_feature4', 'QuickBooks 格式'),
        ('pricing_feature5', 'Xero 格式'),
        ('pricing_feature8', 'OCR 文字辨識'),
        ('pricing_feature9', '批量處理'),
        ('pricing_feature10', '雲端儲存'),
        ('pricing_feature11', '安全加密'),
        ('pricing_feature12', '優先支援')
    ]
    
    for key, zh_text in pricing_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 定价区域完成")
    
    # 8. 博客/学习中心
    print("\n📋 第8步: 翻译学习中心")
    blog_items = [
        ('blog_title', '學習中心'),
        ('blog_subtitle', '實用指南與最佳實踐'),
        ('blog_cta', '閱讀文章')
    ]
    
    for key, zh_text in blog_items:
        content = safe_replace(content, zh_text, lang_trans[key], key)
    sections_translated += 1
    print("  ✅ 学习中心完成")
    
    # 9. 调整脚本路径（针对blog目录）
    print("\n📋 第9步: 调整资源路径")
    if lang_code != 'zh':
        # 语言选择器脚本路径保持不变（已在根目录）
        pass
    print("  ✅ 路径调整完成")
    sections_translated += 1
    
    # 10. 保存文件
    print("\n📋 第10步: 保存文件")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  💾 文件已保存: {target_file}")
    print(f"  📊 文件大小: {target_file.stat().st_size / 1024:.1f} KB")
    
    # 完成总结
    print(f"\n{'='*60}")
    print(f"✅ {lang_code.upper()} 版本翻译完成!")
    print(f"📊 翻译区域: {sections_translated}/10")
    print(f"📁 输出文件: {target_file}")
    print(f"{'='*60}")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("🌍 VaultCaddy 完整翻译系统 v2.0")
    print("="*60)
    print("\n📋 翻译计划:")
    print("  1. 英文版 (en/)")
    print("  2. 日文版 (jp/)")
    print("  3. 韩文版 (kr/)")
    print()
    
    # 翻译3种语言
    languages = [
        ('en', '英文'),
        ('jp', '日文'),
        ('kr', '韩文')
    ]
    
    for lang_code, lang_name in languages:
        try:
            translate_index_complete(lang_code)
        except Exception as e:
            print(f"\n❌ {lang_name}翻译失败: {e}")
            continue
    
    # 最终总结
    print("\n" + "="*60)
    print("🎉 所有语言翻译完成！")
    print("="*60)
    print("\n📁 生成的文件:")
    print("  ✓ en/index.html")
    print("  ✓ jp/index.html")
    print("  ✓ kr/index.html")
    print("\n🚀 下一步:")
    print("  1. 在浏览器中测试: python3 -m http.server 8000")
    print("  2. 访问: http://localhost:8000/en/index.html")
    print("  3. 测试语言切换功能")
    print("  4. 人工校对翻译质量")
    print("  5. 继续翻译auth.html和dashboard.html")
    print("\n💡 提示: 翻译后的文件保留了所有HTML结构和样式")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

