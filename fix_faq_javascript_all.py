#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复所有FAQ的JavaScript功能（支持button和div两种结构）
"""

import os
import re
from pathlib import Path

def fix_faq_js(file_path):
    """修复单个文件的FAQ JavaScript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找并替换旧的FAQ JavaScript
        old_faq_js_pattern = r'// FAQ Toggle Functionality\s+document\.querySelectorAll\(\'\.faq-question\'\)\.forEach\(question => \{[\s\S]*?\}\);'
        
        new_faq_js = '''// FAQ Toggle Functionality - 支持所有FAQ结构
        document.addEventListener('DOMContentLoaded', function() {
            // 处理所有 .faq-question 元素（无论是button还是div）
            document.querySelectorAll('.faq-question').forEach(question => {
                question.addEventListener('click', function() {
                    const faqItem = this.closest('.faq-item');
                    if (!faqItem) return;
                    
                    // 查找答案元素（可能是nextElementSibling或者在同一个faq-item下）
                    let answer = this.nextElementSibling;
                    if (!answer || !answer.classList.contains('faq-answer')) {
                        answer = faqItem.querySelector('.faq-answer');
                    }
                    
                    // 查找图标元素（可能是div或span）
                    let icon = this.querySelector('.faq-icon');
                    
                    if (answer) {
                        const isHidden = answer.style.display === 'none' || answer.style.display === '' || 
                                       window.getComputedStyle(answer).display === 'none';
                        
                        if (isHidden) {
                            answer.style.display = 'block';
                            if (icon) {
                                icon.textContent = '−';
                                icon.style.transform = 'rotate(180deg)';
                            }
                        } else {
                            answer.style.display = 'none';
                            if (icon) {
                                icon.textContent = '+';
                                icon.style.transform = 'rotate(0deg)';
                            }
                        }
                    }
                });
            });
        });'''
        
        # 替换旧的JavaScript
        content = re.sub(old_faq_js_pattern, new_faq_js, content)
        
        # 如果找不到旧的JavaScript，直接在</body>前添加新的
        if '// FAQ Toggle Functionality' not in content:
            new_script = f'''
    <script>
        {new_faq_js}
    </script>
</body>'''
            content = content.replace('</body>', new_script)
        
        # 只有在内容改变时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 失败: {file_path.name} - {e}")
        return False

def main():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    print("🔧 开始修复所有FAQ的JavaScript功能...")
    print("=" * 80)
    
    languages = {
        'zh-TW': '台湾',
        'zh-HK': '香港',
        'ja-JP': '日本',
        'ko-KR': '韩国'
    }
    
    for lang_code, lang_name in languages.items():
        print(f"\n{'='*80}")
        print(f"修复 {lang_name} 版本 ({lang_code})...")
        print(f"{'='*80}")
        
        lang_dir = root_dir / lang_code
        if not lang_dir.exists():
            print(f"  ⚠️ 目录不存在: {lang_dir}")
            continue
        
        lang_files = list(lang_dir.glob('*-v3.html'))
        lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
        
        print(f"  找到 {len(lang_files)} 个页面")
        
        fixed_count = 0
        for i, file_path in enumerate(lang_files, 1):
            if fix_faq_js(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
    
    print("\n" + "=" * 80)
    print("🎉 所有FAQ的JavaScript功能修复完成！")
    print("=" * 80)
    print("\n请刷新浏览器并测试FAQ展开/收起功能！")

if __name__ == '__main__':
    main()

