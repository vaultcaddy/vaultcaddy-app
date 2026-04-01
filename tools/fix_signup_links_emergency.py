#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 紧急修复：所有signup.html链接改为正确的auth.html
根据页面语言自动使用正确的路径
"""

import os
import re
from pathlib import Path

class SignupLinkFixer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        self.total_replacements = 0
        
        # 语言到auth路径的映射
        self.lang_to_auth_path = {
            'zh-TW': '/auth.html',
            'zh-HK': '/auth.html',
            'ko-KR': '/kr/auth.html',
            'ja-JP': '/jp/auth.html',
            'en': '/en/auth.html',
            'en-US': '/en/auth.html',
            'en-UK': '/en/auth.html',
            'en-AU': '/en/auth.html',
            'en-CA': '/en/auth.html',
            'en-NZ': '/en/auth.html',
            'en-SG': '/en/auth.html',
            'en-IE': '/en/auth.html',
            'jp': '/jp/auth.html',
            'kr': '/kr/auth.html',
            'ja': '/jp/auth.html',  # 备用
            'root': '/auth.html',  # 根目录
        }
    
    def get_correct_auth_path(self, file_path):
        """根据文件路径确定正确的auth.html路径"""
        path_str = str(file_path)
        
        # 检查文件在哪个语言目录下
        for lang_dir, auth_path in self.lang_to_auth_path.items():
            if lang_dir == 'root':
                continue
            if f'/{lang_dir}/' in path_str or path_str.startswith(f'{lang_dir}/'):
                return auth_path
        
        # 默认返回根目录的auth.html
        return '/auth.html'
    
    def fix_file(self, file_path):
        """修复单个文件中的所有signup.html链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含signup.html
            if '/signup.html' not in content:
                return False
            
            original_content = content
            
            # 获取正确的auth路径
            correct_auth_path = self.get_correct_auth_path(file_path)
            
            # 计算替换次数
            count_before = content.count('/signup.html')
            
            # 替换所有的/signup.html为正确的auth.html
            content = content.replace('/signup.html', correct_auth_path)
            
            count_after = content.count(correct_auth_path) - (original_content.count(correct_auth_path) if correct_auth_path in original_content else 0)
            
            # 检查是否有变化
            if content != original_content:
                # 备份
                backup_path = str(file_path) + '.backup_signup_fix'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.total_replacements += count_before
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 修复失败 {file_path.name}: {e}")
            return False
    
    def fix_all_html_files(self):
        """修复所有HTML文件"""
        print("🚨 紧急修复所有signup.html链接...")
        print("=" * 80)
        
        # 查找所有HTML文件
        html_files = list(self.root_dir.glob('**/*.html'))
        
        print(f"📊 找到 {len(html_files)} 个HTML文件\n")
        
        # 按目录分组统计
        dir_stats = {}
        
        for file_path in html_files:
            if 'backup' in file_path.name:
                continue
            
            # 获取目录
            relative_path = file_path.relative_to(self.root_dir)
            dir_name = str(relative_path.parent) if relative_path.parent != Path('.') else 'root'
            
            if self.fix_file(file_path):
                self.fixed_count += 1
                
                if dir_name not in dir_stats:
                    dir_stats[dir_name] = {
                        'count': 0,
                        'auth_path': self.get_correct_auth_path(file_path)
                    }
                dir_stats[dir_name]['count'] += 1
        
        # 显示统计
        print("\n" + "=" * 80)
        print("📊 修复统计 (按目录)")
        print("=" * 80)
        
        for dir_name, stats in sorted(dir_stats.items()):
            print(f"\n📁 {dir_name}/")
            print(f"   ✅ 修复了 {stats['count']} 个文件")
            print(f"   🔗 使用链接: {stats['auth_path']}")
        
        print("\n" + "=" * 80)
        print("🎉 紧急修复完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 修复了 {self.fixed_count} 个文件")
        print(f"   - 替换了 {self.total_replacements} 个错误链接")
        print(f"\n💾 所有修改的文件都有备份 (.backup_signup_fix)")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🚨 紧急修复：Signup链接错误                                      ║
║                                                                              ║
║  问题: 所有页面的注册链接都指向错误的 /signup.html                            ║
║                                                                              ║
║  修复方案:                                                                    ║
║    ✓ 中文版 (zh-TW, zh-HK) → /auth.html                                      ║
║    ✓ 英文版 (en-*) → /en/auth.html                                           ║
║    ✓ 日文版 (ja-JP, jp) → /jp/auth.html                                      ║
║    ✓ 韩文版 (ko-KR, kr) → /kr/auth.html                                      ║
║    ✓ 根目录 → /auth.html                                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    fixer = SignupLinkFixer(root_dir)
    fixer.fix_all_html_files()
    
    print("\n" + "=" * 80)
    print("✅ 所有signup.html链接已修复为正确的auth.html！")
    print("=" * 80)
    print("\n请刷新浏览器测试所有注册链接！")

if __name__ == '__main__':
    main()

