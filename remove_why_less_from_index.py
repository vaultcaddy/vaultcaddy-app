#!/usr/bin/env python3
"""
从 4 个版本的 index.html 中移除"为什么功能更少？"Hero 区域
"""

from pathlib import Path
import re

def remove_why_less_section(file_path):
    """移除"为什么功能更少？"区域"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 查找并移除整个"简化优势 Hero 区域"
        # 匹配从 <section class="why-less-is-more" 或类似的开始标记到对应的 </section>
        
        # 方法1: 匹配明确的注释标记
        pattern1 = r'<!-- 簡化優勢 Hero 區域 -->.*?</section>\s*'
        
        # 方法2: 匹配以 style 属性开始的 section（包含 "为什么功能更少"）
        pattern2 = r'<section[^>]*style="background: linear-gradient\(135deg, rgba\(102, 126, 234[^>]*>.*?</section>\s*(?=\s*<main|<section)'
        
        # 方法3: 匹配包含特定内容的 section
        pattern3 = r'<section[^>]*>.*?為什麼 VaultCaddy 功能更少\?.*?</section>\s*'
        pattern4 = r'<section[^>]*>.*?Why does VaultCaddy have fewer features\?.*?</section>\s*'
        pattern5 = r'<section[^>]*>.*?なぜVaultCaddyは機能が少ないのか\?.*?</section>\s*'
        pattern6 = r'<section[^>]*>.*?왜 VaultCaddy는 기능이 적은가\?.*?</section>\s*'
        
        # 尝试所有模式
        new_html = html_content
        for pattern in [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6]:
            temp_html = re.sub(pattern, '', new_html, flags=re.DOTALL)
            if temp_html != new_html:
                new_html = temp_html
                break
        
        # 检查是否有变化
        if new_html == html_content:
            # 尝试更宽松的匹配
            # 查找包含 "Dext" 和 "60+ 功能" 的 section
            pattern_loose = r'<section[^>]*>.*?Dext.*?60\+.*?</section>\s*'
            new_html = re.sub(pattern_loose, '', html_content, flags=re.DOTALL)
        
        if new_html == html_content:
            return False, "未找到匹配的内容"
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True, "成功"
    
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("🗑️  开始从 index.html 移除简化优势区域...")
    print("=" * 70)
    print()
    
    # 4 个版本的 index.html
    index_files = [
        'index.html',           # 繁体中文
        'en/index.html',        # 英文
        'jp/index.html',        # 日文
        'kr/index.html'         # 韩文
    ]
    
    total_success = 0
    total_error = 0
    
    for file_path in index_files:
        if not Path(file_path).exists():
            print(f"⚠️  文件不存在：{file_path}")
            total_error += 1
            continue
        
        print(f"处理：{file_path}...")
        success, message = remove_why_less_section(file_path)
        
        if success:
            print(f"✅ {file_path}: {message}")
            total_success += 1
        else:
            print(f"❌ {file_path}: {message}")
            total_error += 1
    
    print()
    print("=" * 70)
    print("🎉 处理完成！")
    print()
    print("📊 统计：")
    print(f"   - 成功：{total_success}/4 页")
    print(f"   - 错误：{total_error}/4 页")
    print()
    print("✅ 已移除内容：")
    print("   - 💡 為什麼選擇 VaultCaddy？")
    print("   - 為什麼 VaultCaddy 功能更少？")
    print("   - Dext 60+ 功能 vs VaultCaddy 12 功能对比")
    print("   - 更少 = 更簡單 = 更快 = 更便宜")
    print("   - 优势标签（便宜83%、3秒上手、繁體中文）")
    print()
    print("📋 index.html 页面结构（更新后）：")
    print("   1. <head> - SEO 标签")
    print("   2. <nav> - 导航栏（保留）")
    print("   3. <main> - 主要内容区域")
    print("      - Hero 区域")
    print("      - 核心功能")
    print("      - 使用场景")
    print("      - 客户评价")
    print("      - 等等...")

if __name__ == '__main__':
    # 确认执行
    print()
    print("⚠️  重要提示：")
    print("   此操作将从 4 个版本的 index.html 移除简化优势区域")
    print("   文件：index.html, en/index.html, jp/index.html, kr/index.html")
    print()
    
    response = input("是否继续？(yes/no): ").strip().lower()
    
    if response in ['yes', 'y', '是']:
        main()
    else:
        print("❌ 操作已取消")

