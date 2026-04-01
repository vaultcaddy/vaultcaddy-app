#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复日文版和韩文版首页设计，使其与中文版完全对齐
"""

import re

def fix_index(file_path, language_name, title_text, divider_needed=True):
    """
    修复首页设计
    Args:
        file_path: 文件路径
        language_name: 语言名称（用于日志）
        title_text: 标题文本（如"專為香港會計師打造"）
        divider_needed: 是否需要添加分隔线
    """
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n🔧 开始修复{language_name}版首页设计...")
    
    # 1. 如果需要，添加标题装饰线
    if divider_needed:
        print(f"1️⃣ 检查标题装饰线...")
        # 检查是否已经有装饰线
        if f'>{title_text}<div style="width: 80px; height: 4px;' in content:
            print(f"   ℹ️  标题装饰线已存在")
        else:
            # 尝试添加装饰线
            old_pattern = f'>{title_text}</h2>'
            new_replacement = f'>{title_text}<div style="width: 80px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 1rem auto; border-radius: 2px;"></div></h2>'
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_replacement)
                print(f"   ✅ 已添加标题装饰线")
            else:
                print(f"   ⚠️  未找到标题：{title_text}")
    
    # 2. 确保定价卡片的标签一致
    print(f"2️⃣ 检查定价卡片...")
    if 'Save 20%' in content or '節省 20%' in content or '節約 20%' in content or '20% 절약' in content:
        print(f"   ✅ 定价标签存在")
    else:
        print(f"   ⚠️  定价标签可能缺失")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {language_name}版首页设计修复完成！")

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║            修复日文版和韩文版首页设计对齐工具                          ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    # 修复日文版
    fix_index(
        file_path='jp/index.html',
        language_name='日文',
        title_text='香港の会計士のために構築',
        divider_needed=True
    )
    
    # 修复韩文版
    fix_index(
        file_path='kr/index.html',
        language_name='韩文',
        title_text='홍콩 회계사를 위해 구축됨',
        divider_needed=True
    )
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║                        ✅ 全部修复完成！                                ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print("\n📝 修复内容：")
    print("   ✅ 检查并添加标题装饰线")
    print("   ✅ 检查定价卡片标签")
    print("\n🌐 请访问以下页面查看效果：")
    print("   - https://vaultcaddy.com/jp/index.html")
    print("   - https://vaultcaddy.com/kr/index.html")

if __name__ == '__main__':
    main()

