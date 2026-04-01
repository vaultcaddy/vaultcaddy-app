#!/usr/bin/env python3
"""
实施第 1 阶段上线策略：
- 选择 56 个高价值页面上线（index）
- 其他 236 个页面暂时不索引（noindex）
"""

import re
from pathlib import Path

# 第 1 阶段：香港 12 家主要银行 + 2 个核心行业
PHASE1_BANKS = [
    'hsbc', 'hangseng', 'bochk', 'sc', 'dbs', 'bea',
    'citibank', 'dahsing', 'citic', 'bankcomm', 'fubon', 'ocbc'
]

PHASE1_INDUSTRIES = [
    'accountant',  # 会计师
    'smallbiz'     # 小型企业
]

def should_index_in_phase1(filename):
    """判断页面是否应该在第 1 阶段索引"""
    
    # 检查是否是银行页面
    for bank in PHASE1_BANKS:
        if f"{bank}-bank-statement-simple" in filename:
            return True
    
    # 检查是否是行业页面
    for industry in PHASE1_INDUSTRIES:
        if f"{industry}-accounting-solution" in filename:
            return True
    
    return False

def set_robots_meta(file_path, should_index=True):
    """设置页面的 robots meta 标签"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if should_index:
        # 允许索引
        new_robots = '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">'
    else:
        # 不允许索引（但允许爬取链接）
        new_robots = '<meta name="robots" content="noindex, follow">'
    
    # 替换现有的 robots meta 标签
    if 'name="robots"' in content:
        content = re.sub(
            r'<meta name="robots" content="[^"]*">',
            new_robots,
            content
        )
    else:
        # 如果没有 robots 标签，在 </head> 之前添加
        insert_point = content.rfind('</head>')
        if insert_point != -1:
            content = (
                content[:insert_point] +
                f'    {new_robots}\n' +
                content[insert_point:]
            )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return should_index

def main():
    """主函数"""
    
    print("🚀 实施第 1 阶段上线策略...")
    print("=" * 70)
    print()
    print("📋 策略说明：")
    print("   - ✅ 56 个高价值页面：index（允许 Google 索引）")
    print("   - ⏸️  236 个其他页面：noindex（暂不索引，保留质量）")
    print()
    print("📝 第 1 阶段页面：")
    print("   - 香港 12 家主要银行（48 页）")
    print("   - 2 个核心行业：会计师、小型企业（8 页）")
    print()
    print("=" * 70)
    print()
    
    # 读取所有生成的页面
    pages_files = [
        'phase2_generated_pages.txt',
        'phase2_generated_remaining_204_pages.txt'
    ]
    
    all_pages = []
    for pages_file in pages_files:
        if Path(pages_file).exists():
            with open(pages_file, 'r', encoding='utf-8') as f:
                all_pages.extend([line.strip() for line in f if line.strip()])
    
    # 统计
    phase1_count = 0
    phase2_count = 0
    
    # 处理每个页面
    for page_path in all_pages:
        if not Path(page_path).exists():
            continue
        
        filename = Path(page_path).name
        should_index = should_index_in_phase1(filename)
        
        try:
            set_robots_meta(page_path, should_index)
            
            if should_index:
                phase1_count += 1
                print(f"✅ [Phase 1] {page_path}")
            else:
                phase2_count += 1
                if phase2_count % 50 == 0:
                    print(f"⏸️  已设置 {phase2_count} 个页面为 noindex...")
        
        except Exception as e:
            print(f"❌ {page_path}: {e}")
    
    print()
    print("=" * 70)
    print("🎉 第 1 阶段上线策略实施完成！")
    print()
    print("📊 统计：")
    print(f"   - ✅ Phase 1（index）：{phase1_count} 页")
    print(f"   - ⏸️  Phase 2+（noindex）：{phase2_count} 页")
    print(f"   - 📈 总计：{phase1_count + phase2_count} 页")
    print()
    print("🎯 第 1 阶段页面列表：")
    print()
    print("**银行页面（48 页）：**")
    for bank in PHASE1_BANKS:
        bank_name = {
            'hsbc': '滙豐銀行',
            'hangseng': '恒生銀行',
            'bochk': '中國銀行（香港）',
            'sc': '渣打銀行',
            'dbs': '星展銀行',
            'bea': '東亞銀行',
            'citibank': '花旗銀行',
            'dahsing': '大新銀行',
            'citic': '中信銀行',
            'bankcomm': '交通銀行',
            'fubon': '富邦銀行',
            'ocbc': 'OCBC'
        }.get(bank, bank)
        print(f"   - {bank_name} (4 語言)")
    print()
    print("**行業頁面（8 頁）：**")
    for industry in PHASE1_INDUSTRIES:
        industry_name = {
            'accountant': '會計師',
            'smallbiz': '小型企業'
        }.get(industry, industry)
        print(f"   - {industry_name} (4 語言)")
    print()
    print("=" * 70)
    print()
    print("✅ 下一步：")
    print("   1. 提交 Sitemap 到 Google Search Console")
    print("   2. 監控索引狀態（1-2 週）")
    print("   3. 根據數據決定是否進入第 2 階段")
    print()
    print("📈 預期效果（1-4 週）：")
    print("   - Google 索引 40-50 個頁面")
    print("   - SEO 流量增長 30-50%")
    print("   - 無任何警告或懲罰")

if __name__ == '__main__':
    # 询问用户确认
    print()
    print("⚠️  重要提示：")
    print("   此操作将为 236 个页面添加 noindex 标签")
    print("   这些页面暂时不会被 Google 索引")
    print()
    
    response = input("是否继续？(yes/no): ").strip().lower()
    
    if response in ['yes', 'y', '是']:
        main()
    else:
        print("❌ 操作已取消")

