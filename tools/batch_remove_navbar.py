#!/usr/bin/env python3
"""
批量移除所有 landing page 的导航栏
移除 <nav class="navbar">...</nav> 部分
"""

from pathlib import Path
import re

def remove_navbar(file_path):
    """移除页面中的导航栏"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 检查是否有导航栏
        if '<nav class="navbar">' not in html_content and '<nav class="navbar"' not in html_content:
            return False, "没有导航栏"
        
        # 使用正则表达式移除整个导航栏区域
        # 匹配从 <!-- Navigation --> 或 <nav 到 </nav>
        pattern = r'(<!-- Navigation -->.*?)?<nav class="navbar".*?</nav>\s*'
        
        new_html = re.sub(pattern, '', html_content, flags=re.DOTALL)
        
        # 检查是否有变化
        if new_html == html_content:
            return False, "未找到匹配的导航栏"
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True, "成功"
    
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("🗑️  开始批量移除导航栏...")
    print("=" * 70)
    print()
    
    # 统计
    total_processed = 0
    total_success = 0
    total_skip = 0
    total_error = 0
    
    # 读取生成的页面列表
    pages_files = [
        'phase2_generated_pages.txt',
        'phase2_generated_remaining_204_pages.txt'
    ]
    
    all_pages = []
    for pages_file in pages_files:
        if Path(pages_file).exists():
            with open(pages_file, 'r', encoding='utf-8') as f:
                all_pages.extend([line.strip() for line in f if line.strip()])
    
    print(f"📄 找到 {len(all_pages)} 个页面")
    print()
    print("🗑️  移除导航栏...")
    print("-" * 70)
    
    for page_path in all_pages:
        if not Path(page_path).exists():
            continue
        
        total_processed += 1
        
        success, message = remove_navbar(page_path)
        
        if success:
            total_success += 1
            if total_success % 20 == 0:
                print(f"✅ 已完成 {total_success}/{len(all_pages)} 页...")
        elif "没有导航栏" in message:
            total_skip += 1
        else:
            total_error += 1
            if total_error <= 5:  # 只显示前5个错误
                print(f"❌ {page_path}: {message}")
    
    print()
    print("=" * 70)
    print("🎉 批量移除完成！")
    print()
    print("📊 统计：")
    print(f"   - 处理: {total_processed} 页")
    print(f"   - 成功: {total_success} 页")
    print(f"   - 跳过: {total_skip} 页（没有导航栏）")
    print(f"   - 错误: {total_error} 页")
    print()
    print("✅ 已移除内容：")
    print("   - 导航栏（功能 定價 資源 立即試用）")
    print()
    print("📋 页面结构（更新后）：")
    print("   1. <head> - SEO 标签")
    print("   2. 【简化优势 Hero】- 为什么功能更少？")
    print("   3. 【痛点分析】- 3 个痛点")
    print("   4. 【客户案例】- 真实故事")
    print("   5. 【使用指南】- 3 步骤")
    print("   6. 【FAQ】- 8 个问题")
    print("   7. 【行动呼籲】- CTA")

if __name__ == '__main__':
    # 确认执行
    print()
    print("⚠️  重要提示：")
    print("   此操作将从 292 个页面移除导航栏")
    print("   移除的内容：VaultCaddy | 功能 | 定價 | 資源 | 立即試用")
    print()
    
    response = input("是否继续？(yes/no): ").strip().lower()
    
    if response in ['yes', 'y', '是']:
        main()
    else:
        print("❌ 操作已取消")

