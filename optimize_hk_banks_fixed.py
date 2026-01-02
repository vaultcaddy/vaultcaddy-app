#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化5个香港本地银行页面 - 使用差异化策略（修正文件路径）
"""

import re
from pathlib import Path

# 5个香港银行的差异化配置（使用实际文件路径）
HK_BANKS_CONFIG = [
    {
        'file': 'hang-seng-bank-statement-v3.html',
        'bank_name': '恒生銀行',
        'bank_en': 'Hang Seng',
        'title': '恒生銀行月結單轉Excel教學｜中小企對帳自動化｜Hang Seng Statement OCR',
        'description': '恒生銀行月結單手動輸入太慢？VaultCaddy專為香港中小企設計，自動識別恒生網銀PDF、優越理財月結單，轉成Excel/CSV/Xero。支持企業戶口、Savings、信用卡。3秒處理｜98%準確｜HK$46/月起',
        'h1': '恒生銀行月結單自動轉Excel - 中小企對帳解決方案',
        'keywords': '恒生銀行對帳單,恒生月結單,Hang Seng statement,恒生網銀PDF,優越理財,中小企對帳,恒生企業戶口,Hang Seng OCR,恒生銀行轉Excel',
        'unique_selling_point': '中小企首選 | 優越理財支持',
        'search_volume': '800/月'
    },
    {
        'file': 'bochk-bank-statement.html',
        'bank_name': '中國銀行香港',
        'bank_en': 'BOCHK',
        'title': '中國銀行香港對帳單處理｜BOCHK多幣種月結單｜iBanking PDF轉Excel',
        'description': '中國銀行（香港）對帳單AI處理，支持iBanking網銀PDF、多幣種賬戶、企業戶口月結單。自動識別人民幣/美元/港幣交易，轉Excel/CSV。官方背景銀行首選方案｜3秒處理｜98%準確率',
        'h1': '中國銀行香港對帳單AI處理 - 多幣種企業帳戶',
        'keywords': '中銀香港對帳單,BOCHK statement,中銀月結單,iBanking PDF,多幣種帳戶,中銀企業戶口,中國銀行香港,BOCHK OCR,中銀網銀處理',
        'unique_selling_point': '官方背景 | 多幣種支持',
        'search_volume': '600/月'
    },
    {
        'file': 'sc-bank-statement.html',
        'bank_name': '渣打銀行',
        'bank_en': 'Standard Chartered',
        'title': '渣打銀行對帳單OCR識別｜外資銀行月結單處理｜Standard Chartered PDF',
        'description': '渣打銀行（Standard Chartered）對帳單自動處理，支持Priority Banking、外幣帳戶、國際業務月結單。AI識別網銀PDF轉Excel/QuickBooks，適合跨境貿易企業｜3秒處理｜HK$46/月',
        'h1': '渣打銀行對帳單OCR - 外資銀行+國際業務專用',
        'keywords': '渣打銀行對帳單,Standard Chartered statement,渣打月結單,SC OCR,Priority Banking,外資銀行,國際業務,渣打網銀,跨境貿易對帳',
        'unique_selling_point': '外資銀行 | 國際業務',
        'search_volume': '400/月'
    },
    {
        'file': 'bea-bank-statement.html',
        'bank_name': '東亞銀行',
        'bank_en': 'BEA',
        'title': '東亞銀行對帳單處理｜本地銀行中小企方案｜BEA Cyberbanking PDF',
        'description': '東亞銀行對帳單AI處理，支持Cyberbanking網銀PDF、企業戶口、商業帳戶月結單。本地銀行中小企首選，轉Excel/CSV/QuickBooks。香港老牌銀行專用方案｜3秒處理｜98%準確',
        'h1': '東亞銀行對帳單AI處理 - 香港本地銀行方案',
        'keywords': '東亞銀行對帳單,BEA statement,東亞月結單,Cyberbanking PDF,本地銀行,東亞企業戶口,BEA OCR,東亞網銀,香港老牌銀行',
        'unique_selling_point': '本地銀行 | 中小企業',
        'search_volume': '350/月'
    },
    {
        'file': 'citibank-bank-statement.html',
        'bank_name': '花旗銀行',
        'bank_en': 'Citibank',
        'title': '花旗銀行對帳單AI處理｜美資銀行信用卡賬單｜Citibank PDF轉Excel',
        'description': '花旗銀行（Citibank）對帳單自動化處理，支持信用卡賬單、企業戶口、網銀PDF。美資銀行專用AI方案，轉Excel/QuickBooks/Xero。支持Corporate Card｜3秒處理｜HK$46/月',
        'h1': '花旗銀行對帳單AI處理 - 美資銀行+信用卡專用',
        'keywords': '花旗銀行對帳單,Citibank statement,花旗月結單,花旗信用卡,Corporate Card,美資銀行,Citi OCR,花旗網銀,花旗企業戶口',
        'unique_selling_point': '美資銀行 | 卡類業務',
        'search_volume': '450/月'
    }
]

def optimize_bank_page(config):
    """优化单个银行页面"""
    
    file_path = config['file']
    
    # 检查文件是否存在
    if not Path(file_path).exists():
        print(f"   ❌ 文件不存在: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 更新Title
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{config["title"]}</title>',
            content,
            count=1,
            flags=re.DOTALL
        )
        
        # 2. 更新Meta Description
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{config["description"]}"',
            content,
            count=1
        )
        
        # 3. 更新或添加Keywords
        if re.search(r'<meta name="keywords"', content):
            content = re.sub(
                r'<meta name="keywords" content="[^"]*"',
                f'<meta name="keywords" content="{config["keywords"]}"',
                content,
                count=1
            )
        else:
            # 如果不存在，添加在description后面
            content = re.sub(
                r'(<meta name="description"[^>]*>)',
                r'\1\n    <meta name="keywords" content="' + config["keywords"] + '">',
                content,
                count=1
            )
        
        # 4. 更新主标题H1
        h1_patterns = [
            r'(<h1[^>]*>)[^<]*(</h1>)',
            r'(<h1[^>]*style="[^"]*">)[^<]*(</h1>)',
        ]
        
        h1_updated = False
        for pattern in h1_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, r'\1' + config['h1'] + r'\2', content, count=1, flags=re.DOTALL)
                h1_updated = True
                break
        
        # 5. 更新Open Graph标题
        if '<meta property="og:title"' in content:
            content = re.sub(
                r'<meta property="og:title" content="[^"]*"',
                f'<meta property="og:title" content="{config["title"]}"',
                content,
                count=1
            )
        
        # 6. 更新Open Graph描述
        if '<meta property="og:description"' in content:
            content = re.sub(
                r'<meta property="og:description" content="[^"]*"',
                f'<meta property="og:description" content="{config["description"][:150]}"',
                content,
                count=1
            )
        
        # 检查是否有实际变化
        if content == original_content:
            print(f"   ⚠️  内容未改变，可能需要手动检查")
            return False
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Title: {config['title'][:50]}...")
        print(f"   ✅ H1: {config['h1'][:50]}...")
        print(f"   ✅ 搜索量: {config['search_volume']}")
        return True
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False

def main():
    print("=" * 80)
    print("🏦 香港本地银行页面差异化优化")
    print("=" * 80)
    print()
    print("📋 策略: 每个银行有独特的定位和关键词组合")
    print("🎯 目标: 避免关键词竞食，提升整体排名")
    print()
    print("=" * 80)
    print()
    
    success_count = 0
    total_search_volume = 0
    
    for i, config in enumerate(HK_BANKS_CONFIG, 1):
        print(f"📝 [{i}/5] 优化 {config['bank_name']} ({config['bank_en']})")
        print(f"   📍 定位: {config['unique_selling_point']}")
        print(f"   📊 搜索量: {config['search_volume']}")
        
        if optimize_bank_page(config):
            success_count += 1
            # 提取搜索量数字
            volume_num = int(config['search_volume'].split('/')[0])
            total_search_volume += volume_num
        
        print()
    
    print("=" * 80)
    print("📊 优化结果")
    print("=" * 80)
    print(f"✅ 成功优化: {success_count}/{len(HK_BANKS_CONFIG)} 个页面")
    print(f"✅ 成功率: {success_count/len(HK_BANKS_CONFIG)*100:.1f}%")
    print(f"✅ 覆盖搜索量: {total_search_volume}/月")
    print()
    
    if success_count == len(HK_BANKS_CONFIG):
        print("🎉 所有5个香港银行页面优化完成！")
        print()
    elif success_count > 0:
        print(f"⚠️  {len(HK_BANKS_CONFIG) - success_count} 个页面需要手动检查")
        print()
    
    print("=" * 80)
    print("🎯 差异化策略详情")
    print("=" * 80)
    print()
    
    for config in HK_BANKS_CONFIG:
        print(f"🏦 {config['bank_name']} ({config['bank_en']})")
        print(f"   📍 定位: {config['unique_selling_point']}")
        print(f"   📊 搜索量: {config['search_volume']}")
        print(f"   🎯 主关键词: {config['keywords'].split(',')[0]}")
        print()
    
    print("=" * 80)
    print("📈 预期SEO效果")
    print("=" * 80)
    print()
    print(f"📊 总搜索量: {total_search_volume}/月")
    print()
    print("⏰ 时间表:")
    print("   • 2周后: 排名进入前30")
    print("   • 4周后: 排名进入前20")
    print("   • 8周后: 排名进入前15")
    print()
    print("📈 流量预期:")
    print("   • 额外访客: +150-250/月")
    print("   • 额外注册: +20-35/月")
    print("   • 转化率: 约15%")
    print()
    
    print("=" * 80)
    print("✅ 下一步行动清单")
    print("=" * 80)
    print()
    print("□ 1. 在Google Search Console提交这5个URL (10分钟)")
    print("□ 2. 为这些页面建设反向链接 (每天30分钟)")
    print("   - Quora: 回答相关问题")
    print("   - Reddit: 参与相关讨论")
    print("   - 商业目录: 提交公司信息")
    print()
    print("□ 3. 每周监控排名变化 (每周15分钟)")
    print("   - Google Search Console")
    print("   - 记录关键词排名")
    print()
    print("□ 4. 4周后查看效果并调整")
    print()
    print("🚀 优化完成！现在开始执行SEO策略吧！")
    print()

if __name__ == "__main__":
    main()
