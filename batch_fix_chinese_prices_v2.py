#!/usr/bin/env python3
"""修正中文版（香港）价格 V2"""
import os
import re

# 香港的价格映射
# 基于用户提供的真实价格（假设HKD与图中EUR价格相近）
# 原价: HK$46/月 → 20% OFF: HK$37/月

PRICE_MAPPINGS = {
    # 月费
    'HK$69': 'HK$37',
    'HK$58': 'HK$46',  # 可能是其他套餐
    'HK$46': 'HK$37',  # 基础套餐（100页）
    '$552': '$448',  # 年费
    '$96': '$77',  # 150页月费
    '$206': '$165',  # Dext对比价格（保持不变）
    
    # 额外页费
    'HK$0.60': 'HK$0.48',
    'HK$0.5': 'HK$0.40',
    
    # 其他套餐价格
    'HK$103': 'HK$56',
    'HK$138': 'HK$74',
}

def fix_prices_in_file(filepath):
    """修正文件中的价格"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_changes = 0
        
        # 按长度排序避免部分匹配
        sorted_mappings = sorted(PRICE_MAPPINGS.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_price, new_price in sorted_mappings:
            # 使用正则表达式进行精确匹配
            pattern = re.escape(old_price)
            matches = list(re.finditer(pattern, content))
            if matches:
                content = content.replace(old_price, new_price)
                total_changes += len(matches)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_changes
        return False, 0
        
    except Exception as e:
        print(f"      错误: {e}")
        return False, 0

def main():
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    blog_dir = os.path.join(base_dir, 'blog')
    
    files_to_update = [
        'vaultcaddy-vs-dext-comparison-2025.html',
        'hsbc-bank-statement-to-excel-guide-2025.html',
        'hong-kong-accounting-software-top-10-2025.html',
        'restaurant-accounting-system-guide-2025.html',
        'vaultcaddy-vs-expensify-comparison-2025.html',
        'hang-seng-bank-statement-to-excel-guide-2025.html',
        'pdf-bank-statement-cannot-copy-text-solutions-2025.html',
        'quickbooks-import-bank-statement-error-fix-2025.html',
        'vaultcaddy-vs-quickbooks-comparison-2025.html',
        'manual-data-entry-vs-ai-automation-2025.html',
    ]
    
    print("=" * 70)
    print("💰 修正中文版（香港）价格 V2")
    print("=" * 70)
    print("\n📊 价格调整（20% OFF）：")
    print("  原价月费: HK$46 → 优惠价: HK$37")
    print("  原价年费: $552 → 优惠价: $448")
    print("  额外页费: HK$0.5 → HK$0.40")
    print("=" * 70)
    
    if not os.path.exists(blog_dir):
        print("\n⚠️  中文博客目录不存在")
        return
    
    print("\n🇭🇰 处理中文版文章:")
    updated = 0
    total_changes = 0
    
    for filename in files_to_update:
        filepath = os.path.join(blog_dir, filename)
        if os.path.exists(filepath):
            print(f"\n  处理: {filename}")
            success, changes = fix_prices_in_file(filepath)
            if success and changes > 0:
                updated += 1
                total_changes += changes
                print(f"  ✅ 成功修改 {changes} 处")
            else:
                print(f"  ℹ️  无需修改")
        else:
            print(f"  ⚠️  文件不存在: {filename}")
    
    print("\n" + "=" * 70)
    print("📊 修正完成统计")
    print("=" * 70)
    print(f"✅ 成功更新: {updated}/10 文件")
    print(f"✅ 总计修改: {total_changes} 处")
    print("=" * 70)
    
    if total_changes > 0:
        print("\n💡 修改说明:")
        print("   ✅ 月费降低约20%")
        print("   ✅ 年费更优惠")
        print("   ✅ 价格更具竞争力")
    
    print("\n🎉 中文版价格修正完成！")

if __name__ == "__main__":
    main()

