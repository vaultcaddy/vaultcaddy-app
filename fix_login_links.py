#!/usr/bin/env python3
"""
批量修复所有HTML文件中的login.html链接为en/auth.html

这个脚本会：
1. 扫描所有HTML文件
2. 查找并替换 href="login.html" 为 href="en/auth.html"
3. 生成修复报告
"""

import os
import re
from pathlib import Path

def fix_login_links(file_path):
    """修复单个HTML文件中的login.html链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算修改前的匹配数
        original_count = len(re.findall(r'href="login\.html"', content))
        
        if original_count == 0:
            return 0, 0  # 没有需要修复的链接
        
        # 替换 href="login.html" 为 href="en/auth.html"
        new_content = re.sub(r'href="login\.html"', r'href="en/auth.html"', content)
        
        # 计算修改后还剩多少（应该为0）
        remaining_count = len(re.findall(r'href="login\.html"', new_content))
        
        # 如果有修改，写回文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return original_count, remaining_count
        
    except Exception as e:
        print(f"❌ 错误处理 {file_path}: {e}")
        return 0, 0

def main():
    """主函数：扫描并修复所有HTML文件"""
    base_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    # 统计变量
    total_files = 0
    fixed_files = 0
    total_fixes = 0
    skipped_files = 0
    
    # 需要排除的目录
    exclude_dirs = {
        'node_modules', '.git', 'dist', 'build', '__pycache__',
        '.pytest_cache', '.mypy_cache', 'venv', 'env'
    }
    
    print("🔍 开始扫描HTML文件...")
    print(f"📂 基础目录: {base_dir}")
    print("=" * 80)
    
    # 扫描所有HTML文件
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # 排除特定目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    total_files = len(html_files)
    print(f"📄 找到 {total_files} 个HTML文件\n")
    
    # 处理每个文件
    fixed_files_list = []
    
    for file_path in html_files:
        original_count, remaining_count = fix_login_links(file_path)
        
        if original_count > 0:
            fixed_count = original_count - remaining_count
            total_fixes += fixed_count
            fixed_files += 1
            
            # 相对路径
            rel_path = file_path.relative_to(base_dir)
            fixed_files_list.append((str(rel_path), original_count, fixed_count))
            
            status = "✅" if remaining_count == 0 else "⚠️"
            print(f"{status} {rel_path}: 修复 {fixed_count}/{original_count} 处")
        else:
            skipped_files += 1
    
    # 打印总结
    print("\n" + "=" * 80)
    print("📊 修复总结")
    print("=" * 80)
    print(f"✅ 总扫描文件: {total_files}")
    print(f"✅ 修复的文件: {fixed_files}")
    print(f"✅ 跳过的文件（无需修复）: {skipped_files}")
    print(f"✅ 总修复链接数: {total_fixes}")
    print("=" * 80)
    
    # 显示前20个修复的文件
    if fixed_files_list:
        print("\n📋 修复详情（前20个文件）:")
        for i, (file, original, fixed) in enumerate(fixed_files_list[:20], 1):
            print(f"{i:2d}. {file}: {fixed} 处")
    
    print("\n🎉 批量修复完成！")
    
    # 生成修复报告
    report_path = base_dir / 'fix_login_links_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("Login.html 链接批量修复报告\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"总扫描文件: {total_files}\n")
        f.write(f"修复的文件: {fixed_files}\n")
        f.write(f"跳过的文件: {skipped_files}\n")
        f.write(f"总修复链接数: {total_fixes}\n\n")
        f.write("=" * 80 + "\n")
        f.write("修复详情:\n")
        f.write("=" * 80 + "\n\n")
        for i, (file, original, fixed) in enumerate(fixed_files_list, 1):
            f.write(f"{i:3d}. {file}: {fixed}/{original} 处\n")
    
    print(f"\n📄 详细报告已保存到: {report_path}")

if __name__ == "__main__":
    main()

