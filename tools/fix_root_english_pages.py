#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复根目录英文页面的auth.html链接
英文页面应该跳转到 /en/auth.html，而不是 /auth.html
"""

import os
import re
from pathlib import Path

class RootEnglishPageFixer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        self.total_replacements = 0
    
    def is_english_page(self, file_path):
        """检查页面是否为英文页面"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含英文特征内容
            english_indicators = [
                'Start Free Trial',
                'See How It Works',
                'No credit card required',
                'Why Choose VaultCaddy?',
                'Convert Chase Bank',
                'AI-powered PDF to Excel',
            ]
            
            # 检查是否包含中文特征内容
            chinese_indicators = [
                '免費試用',
                '立即註冊',
                '開始使用',
                '為什麼選擇',
                '專為',
            ]
            
            # 计算英文和中文指示词的出现次数
            english_count = sum(1 for indicator in english_indicators if indicator in content)
            chinese_count = sum(1 for indicator in chinese_indicators if indicator in content)
            
            # 如果英文指示词更多，判定为英文页面
            return english_count > chinese_count and english_count >= 3
            
        except Exception as e:
            print(f"  ⚠️ 无法读取文件: {e}")
            return False
    
    def fix_file(self, file_path):
        """修复单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含 /auth.html
            if 'href="/auth.html"' not in content:
                return False
            
            original_content = content
            
            # 计算替换次数
            count_before = content.count('href="/auth.html"')
            
            # 替换 /auth.html 为 /en/auth.html
            content = content.replace('href="/auth.html"', 'href="/en/auth.html"')
            
            # 检查是否有变化
            if content != original_content:
                # 备份
                backup_path = str(file_path) + '.backup_en_auth'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.total_replacements += count_before
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 修复失败: {e}")
            return False
    
    def fix_root_english_pages(self):
        """修复根目录中的所有英文页面"""
        print("🔧 修复根目录英文页面的auth.html链接...")
        print("=" * 80)
        
        # 查找根目录下的所有HTML文件
        html_files = [f for f in self.root_dir.glob('*.html') if not f.name.startswith('.')]
        
        print(f"📊 在根目录找到 {len(html_files)} 个HTML文件\n")
        
        english_files = []
        
        # 先识别哪些是英文页面
        print("🔍 识别英文页面...\n")
        for file_path in html_files:
            if 'backup' in file_path.name:
                continue
            
            if self.is_english_page(file_path):
                english_files.append(file_path)
                print(f"  ✅ {file_path.name} - 英文页面")
        
        print(f"\n📊 找到 {len(english_files)} 个英文页面\n")
        
        if len(english_files) == 0:
            print("ℹ️  根目录没有英文页面需要修复")
            return
        
        print("🔧 开始修复...\n")
        
        # 修复英文页面
        for file_path in english_files:
            if self.fix_file(file_path):
                self.fixed_count += 1
                print(f"  ✅ 修复: {file_path.name}")
        
        print("\n" + "=" * 80)
        print("🎉 修复完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 识别了 {len(english_files)} 个英文页面")
        print(f"   - 修复了 {self.fixed_count} 个文件")
        print(f"   - 替换了 {self.total_replacements} 个链接")
        print(f"\n💾 所有修改的文件都有备份 (.backup_en_auth)")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           🔧 修复根目录英文页面的auth.html链接                                 ║
║                                                                              ║
║  问题: 根目录的英文页面跳转到了中文的 /auth.html                              ║
║                                                                              ║
║  修复方案:                                                                    ║
║    ✓ 自动识别根目录中的英文页面                                               ║
║    ✓ 将 /auth.html 改为 /en/auth.html                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    fixer = RootEnglishPageFixer(root_dir)
    fixer.fix_root_english_pages()
    
    print("\n" + "=" * 80)
    print("✅ 根目录英文页面的auth.html链接已修复！")
    print("=" * 80)
    print("\n请刷新浏览器测试：")
    print("  🔗 https://vaultcaddy.com/chase-bank-statement-v3.html")
    print("  ✅ 应该跳转到: https://vaultcaddy.com/en/auth.html")

if __name__ == '__main__':
    main()

