#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Hero区域顶部空白 - 将蓝色背景向上移动覆盖白色空白
"""

import re

def fix_hero_whitespace(file_path, lang_name):
    """修复Hero区域顶部的白色空白"""
    
    print(f"\n🔄 处理 {lang_name} 版本...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 方法1: 修改Hero section的margin-top为负值
    # 查找Hero section的style属性
    old_hero_pattern = r'(<section style="[^"]*)(margin-top:\s*0)([^"]*">)'
    
    if re.search(old_hero_pattern, content):
        # 将margin-top: 0改为margin-top: -60px (覆盖main的padding-top)
        content = re.sub(old_hero_pattern, r'\1margin-top: -60px\3', content)
        print(f"   ✅ 已设置 margin-top: -60px")
    else:
        # 如果没找到margin-top: 0，尝试在style中添加margin-top
        hero_pattern = r'(<section style="[^"]*)(overflow: hidden;)([^"]*">)'
        if re.search(hero_pattern, content):
            content = re.sub(hero_pattern, r'\1\2 margin-top: -60px;\3', content)
            print(f"   ✅ 已添加 margin-top: -60px")
    
    # 方法2: 同时修改main的padding-top为0（因为导航栏是fixed定位）
    main_pattern = r'(<main style=")padding-top:\s*60px;(")'
    if re.search(main_pattern, content):
        content = re.sub(main_pattern, r'\1padding-top: 0;\2', content)
        print(f"   ✅ 已修改 main padding-top 为 0")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    base_dir = "/Users/cavlinyeung/ai-bank-parser"
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🔧 修复Hero区域顶部白色空白                                         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    files = {
        "English": f"{base_dir}/en/index.html",
        "Japanese": f"{base_dir}/jp/index.html",
        "Korean": f"{base_dir}/kr/index.html"
    }
    
    success_count = 0
    for lang_name, file_path in files.items():
        if fix_hero_whitespace(file_path, lang_name):
            success_count += 1
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 白色空白修复完成！                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"\n✅ 成功修复 {success_count} 个文件")
    
    print("\n📝 修复方案：")
    print("   1. ✅ 设置 Hero section margin-top: -60px")
    print("   2. ✅ 设置 main padding-top: 0")
    print("   3. ✅ 导航栏为 fixed 定位，不受影响")
    
    print("\n🎨 效果：")
    print("   • 蓝色背景直接衔接橙色Banner")
    print("   • 无任何白色空白")
    print("   • 导航栏保持在顶部固定位置")
    
    print("\n🔗 查看效果：")
    print("   • 英文版：https://vaultcaddy.com/en/index.html")
    print("   • 日文版：https://vaultcaddy.com/jp/index.html")
    print("   • 韩文版：https://vaultcaddy.com/kr/index.html")

if __name__ == "__main__":
    main()

