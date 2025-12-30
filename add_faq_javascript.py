#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有v3页面添加FAQ的JavaScript交互功能
使"+"号可以点击展开/收起FAQ
"""

import os
import re
from pathlib import Path

class FAQJavaScriptAdder:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        
        # FAQ JavaScript代码
        self.faq_javascript = '''
        // FAQ 交互功能
        document.addEventListener('DOMContentLoaded', function() {
            const faqQuestions = document.querySelectorAll('.faq-question');
            
            faqQuestions.forEach(function(question) {
                question.addEventListener('click', function() {
                    const faqItem = this.parentElement;
                    const answer = faqItem.querySelector('.faq-answer');
                    const icon = this.querySelector('.faq-icon');
                    
                    // 切换展开/收起
                    const isActive = faqItem.classList.contains('active');
                    
                    if (isActive) {
                        faqItem.classList.remove('active');
                        answer.style.maxHeight = '0';
                        icon.textContent = '+';
                    } else {
                        faqItem.classList.add('active');
                        answer.style.maxHeight = answer.scrollHeight + 'px';
                        icon.textContent = '−';
                    }
                });
            });
        });'''
    
    def add_faq_javascript(self, file_path):
        """为单个文件添加FAQ JavaScript"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有FAQ JavaScript
            if 'FAQ 交互功能' in content or 'faq-question.*addEventListener' in content:
                return False
            
            original_content = content
            
            # 在</script>标签之后，</body>之前插入FAQ JavaScript
            # 查找最后一个</script>标签
            last_script_match = None
            for match in re.finditer(r'</script>', content):
                last_script_match = match
            
            if last_script_match:
                # 在最后一个</script>之后插入新的script
                insert_pos = last_script_match.end()
                new_script = f'\n\n        <script>{self.faq_javascript}\n        </script>'
                content = content[:insert_pos] + new_script + content[insert_pos:]
            else:
                # 如果没有找到</script>，在</body>之前插入
                body_match = re.search(r'</body>', content)
                if body_match:
                    insert_pos = body_match.start()
                    new_script = f'\n        <script>{self.faq_javascript}\n        </script>\n'
                    content = content[:insert_pos] + new_script + content[insert_pos:]
            
            # 检查是否有变化
            if content != original_content:
                # 备份
                backup_path = str(file_path) + '.backup_faq_js'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 添加失败: {e}")
            return False
    
    def process_directory(self, dir_name):
        """处理目录中的所有v3文件"""
        dir_path = self.root_dir / dir_name
        
        if not dir_path.exists():
            return
        
        print(f"\n🔧 处理: {dir_name}/")
        
        # 只处理v3文件
        html_files = list(dir_path.glob('*-v3.html'))
        
        fixed_in_dir = 0
        for file_path in html_files:
            if 'backup' in file_path.name:
                continue
            
            if self.add_faq_javascript(file_path):
                fixed_in_dir += 1
                self.fixed_count += 1
                print(f"  ✅ {file_path.name}")
        
        if fixed_in_dir > 0:
            print(f"  📊 添加了 {fixed_in_dir} 个文件")
        else:
            print(f"  ℹ️  没有需要添加的文件")
    
    def add_to_all(self):
        """为所有语言目录添加FAQ JavaScript"""
        print("⚡ 为所有v3页面添加FAQ交互功能...")
        print("=" * 80)
        
        # 处理所有语言目录
        lang_dirs = ['zh-TW', 'zh-HK', 'ko-KR', 'ja-JP', 'en-US', 'en-UK', 'en-AU', 'en-CA']
        
        for lang_dir in lang_dirs:
            self.process_directory(lang_dir)
        
        print("\n" + "=" * 80)
        print("🎉 FAQ JavaScript添加完成！")
        print("=" * 80)
        print(f"\n📊 总计添加了 {self.fixed_count} 个文件")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FAQ JavaScript添加工具                                      ║
║                                                                              ║
║  此工具将为所有v3页面添加FAQ交互功能                                          ║
║                                                                              ║
║  功能:                                                                        ║
║    ✓ 点击"+"号展开FAQ                                                         ║
║    ✓ 再次点击收起FAQ                                                          ║
║    ✓ "+"变成"−"                                                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    adder = FAQJavaScriptAdder(root_dir)
    adder.add_to_all()
    
    print("\n" + "=" * 80)
    print("✅ FAQ交互功能添加完成！")
    print("=" * 80)
    print("\n请刷新浏览器，现在"+"号应该可以点击了！")

if __name__ == '__main__':
    main()

