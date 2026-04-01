#!/usr/bin/env python3
"""
批量更新所有页面的最终定价信息
- 中文版：HKD 28/22 (Starter), HKD 118/93 (Pro)
- 英文版：USD 3.88/2.88 (Starter), USD 14.99/11.99 (Pro)  
- 日文版：JPY 599/479 (Starter), JPY 2348/1878 (Pro)
- 韩文版：KRW 5588/4468 (Starter), KRW 21699/17359 (Pro)
"""

import os
import re
from pathlib import Path

# 定义替换规则 - 中文版（HKD）
REPLACEMENTS_ZH = [
    # 从 USD $2.88 更新为 HKD $28
    (r'\$2\.88', '$28'),
    (r'\$3\.60', '$28'),
    
    # Starter 年付价格
    (r'年付僅?\s*\$?2\.88', '年付僅 $22'),
    (r'年付[：:]\s*\$?2\.88', '年付: $22'),
    
    # Pro 价格
    (r'\$14\.99', '$118'),
    (r'年付僅?\s*\$?11\.99', '年付僅 $93'),
    
    # Schema.org 更新
    (r'"price":\s*"2\.88"', '"price": "28"'),
    (r'"price":\s*"14\.99"', '"price": "118"'),
    
    # index.html pricing section - 月付
    (r'HKD\s*\$\s*58\s*/月', 'HKD $ 28 /月'),
    (r'HKD\s*\$\s*46\s*/月', 'HKD $ 22 /月'),
    
    # 超出费用（保持原样或调整）
    (r'HKD\s*\$0\.5', 'HKD $0.5'),
    
    # Credits
    (r'每月\s*100\s*Credits', '每月 100 Credits'),
    (r'每年\s*1,?200\s*Credits', '每年 1,200 Credits'),
]

# 英文版（USD）
REPLACEMENTS_EN = [
    # Starter 价格
    (r'From \$2\.88', 'From $3.88'),
    (r'\$3\.88/month', '$3.88/month'),  # 已经是正确的
    (r'Yearly: \$2\.88', 'Yearly: $2.88'),  # 已经是正确的
    
    # Pro 价格
    (r'\$14\.99/month', '$14.99/month'),  # 已经是正确的
    (r'Yearly: \$11\.99', 'Yearly: $11.99'),  # 已经是正确的
    
    # Schema.org
    (r'"price":\s*"2\.88"', '"price": "3.88"'),
    (r'"price":\s*"14\.99"', '"price": "14.99"'),
]

# 日文版（JPY）
REPLACEMENTS_JP = [
    # Starter 价格
    (r'¥\s*2\.88', '¥599'),
    (r'¥\s*3\.88', '¥599'),
    (r'年払い[：:]\s*¥\s*2\.88', '年払い: ¥479'),
    
    # Pro 价格
    (r'¥\s*14\.99', '¥2,348'),
    (r'年払い[：:]\s*¥\s*11\.99', '年払い: ¥1,878'),
    
    # Schema.org
    (r'"price":\s*"2\.88"', '"price": "599"'),
    (r'"priceCurrency":\s*"USD"', '"priceCurrency": "JPY"'),
]

# 韩文版（KRW）
REPLACEMENTS_KR = [
    # Starter 价格
    (r'₩\s*2\.88', '₩5,588'),
    (r'₩\s*3\.88', '₩5,588'),
    (r'연간[：:]\s*₩\s*2\.88', '연간: ₩4,468'),
    
    # Pro 价格
    (r'₩\s*14\.99', '₩21,699'),
    (r'연간[：:]\s*₩\s*11\.99', '연간: ₩17,359'),
    
    # Schema.org
    (r'"price":\s*"2\.88"', '"price": "5588"'),
    (r'"priceCurrency":\s*"USD"', '"priceCurrency": "KRW"'),
]

# 移除 "API 访问" 功能项
REMOVE_API_FEATURE = [
    (r'<li>.*?API\s*访?問.*?</li>\s*', ''),
    (r'<li>.*?API\s*access.*?</li>\s*', ''),
    (r'<li>.*?API\s*アクセス.*?</li>\s*', ''),
    (r'✓\s*API\s*访?問.*?\n', ''),
    (r'✓\s*API\s*access.*?\n', ''),
]

def update_file(filepath, replacements, lang='zh'):
    """更新单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # 应用所有替换规则
        for pattern, replacement in replacements:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes += count
        
        # 移除API功能项
        for pattern, replacement in REMOVE_API_FEATURE:
            new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
            if count > 0:
                content = new_content
                changes += count
        
        # 如果有更改，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
    except Exception as e:
        print(f"❌ 更新失败 {filepath}: {e}")
        return 0

def main():
    """主函数"""
    root = Path('.')
    updated_files = []
    total_changes = 0
    
    print("🚀 开始更新所有定价信息...")
    print()
    
    # 中文版文件（根目录）
    print("📂 更新中文版（HKD）...")
    zh_files = [
        'index.html',
        'billing.html',
        'pricing.html',
    ]
    
    for filename in zh_files:
        filepath = root / filename
        if filepath.exists():
            changes = update_file(filepath, REPLACEMENTS_ZH, 'zh')
            if changes > 0:
                updated_files.append((str(filepath), changes))
                total_changes += changes
                print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    # 更新所有landing page（中文）
    for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
        for filepath in sorted(root.glob(pattern)):
            changes = update_file(filepath, REPLACEMENTS_ZH, 'zh')
            if changes > 0:
                updated_files.append((str(filepath), changes))
                total_changes += changes
                print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    # 英文版
    print(f"\n📂 更新英文版（USD）...")
    en_dir = root / 'en'
    if en_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = en_dir / filename
            if filepath.exists():
                changes = update_file(filepath, REPLACEMENTS_EN, 'en')
                if changes > 0:
                    updated_files.append((str(filepath), changes))
                    total_changes += changes
                    print(f"✅ 已更新: {filepath} ({changes} 处修改)")
        
        # 英文landing pages
        for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
            for filepath in sorted(en_dir.glob(pattern)):
                changes = update_file(filepath, REPLACEMENTS_EN, 'en')
                if changes > 0:
                    updated_files.append((str(filepath), changes))
                    total_changes += changes
                    print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    # 日文版
    print(f"\n📂 更新日文版（JPY）...")
    jp_dir = root / 'jp'
    if jp_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = jp_dir / filename
            if filepath.exists():
                changes = update_file(filepath, REPLACEMENTS_JP, 'jp')
                if changes > 0:
                    updated_files.append((str(filepath), changes))
                    total_changes += changes
                    print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    # 韩文版
    print(f"\n📂 更新韩文版（KRW）...")
    kr_dir = root / 'kr'
    if kr_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = kr_dir / filename
            if filepath.exists():
                changes = update_file(filepath, REPLACEMENTS_KR, 'kr')
                if changes > 0:
                    updated_files.append((str(filepath), changes))
                    total_changes += changes
                    print(f"✅ 已更新: {filepath} ({changes} 处修改)")
    
    print()
    print("=" * 80)
    print(f"📊 更新总结:")
    print(f"✅ 已更新 {len(updated_files)} 个文件")
    print(f"🔢 总共 {total_changes} 处修改")
    print()
    
    if updated_files:
        print(f"📋 详细列表:")
        for filepath, changes in updated_files[:20]:  # 只显示前20个
            print(f"  - {filepath}: {changes} 处修改")
        if len(updated_files) > 20:
            print(f"  ... 还有 {len(updated_files) - 20} 个文件")
    else:
        print("⚠️  未找到需要更新的文件")
    
    print()
    print("✨ 更新完成！")
    print()
    print("📋 定价总结:")
    print("中文版（HKD）:")
    print("  - Starter: $28/月（年付$22）")
    print("  - Pro: $118/月（年付$93）")
    print()
    print("英文版（USD）:")
    print("  - Starter: $3.88/月（年付$2.88）")
    print("  - Pro: $14.99/月（年付$11.99）")
    print()
    print("日文版（JPY）:")
    print("  - Starter: ¥599/月（年付¥479）")
    print("  - Pro: ¥2,348/月（年付¥1,878）")
    print()
    print("韩文版（KRW）:")
    print("  - Starter: ₩5,588/月（年付₩4,468）")
    print("  - Pro: ₩21,699/月（年付₩17,359）")
    print()
    print("🗑️  已移除 'API 访问' 功能项")

if __name__ == '__main__':
    main()

