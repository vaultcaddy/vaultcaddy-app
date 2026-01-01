#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 正确修复FAQ功能 - 使用max-height而不是display
"""

import os
import re
from pathlib import Path

def fix_faq_correct(file_path):
    """正确修复FAQ功能"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找并替换FAQ JavaScript
        old_pattern = r'// FAQ Toggle Functionality[\s\S]*?document\.addEventListener\(\'DOMContentLoaded\'[\s\S]*?\}\);[\s\S]*?\}\);'
        
        new_js = '''// FAQ Toggle Functionality - 正确版本
        document.addEventListener('DOMContentLoaded', function() {
            // 处理所有 .faq-question 元素（button和div都支持）
            document.querySelectorAll('.faq-question').forEach(question => {
                question.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const faqItem = this.closest('.faq-item');
                    if (!faqItem) return;
                    
                    // 查找答案元素
                    let answer = this.nextElementSibling;
                    if (!answer || !answer.classList.contains('faq-answer')) {
                        answer = faqItem.querySelector('.faq-answer');
                    }
                    
                    // 查找图标元素
                    let icon = this.querySelector('.faq-icon');
                    
                    if (answer) {
                        const isOpen = answer.style.maxHeight && answer.style.maxHeight !== '0px';
                        
                        if (isOpen) {
                            // 关闭
                            answer.style.maxHeight = '0';
                            answer.style.paddingTop = '0';
                            answer.style.paddingBottom = '0';
                            if (icon) {
                                icon.textContent = '+';
                                icon.style.transform = 'rotate(0deg)';
                            }
                        } else {
                            // 打开
                            answer.style.maxHeight = answer.scrollHeight + 100 + 'px';
                            answer.style.paddingTop = '15px';
                            answer.style.paddingBottom = '0';
                            if (icon) {
                                icon.textContent = '−';
                                icon.style.transform = 'rotate(180deg)';
                            }
                        }
                    }
                });
            });
        });'''
        
        # 替换JavaScript
        content = re.sub(old_pattern, new_js, content)
        
        # 如果正则没匹配到，尝试简单替换
        if content == original_content:
            if '// FAQ Toggle Functionality' in content:
                # 找到开始位置
                start_pos = content.find('// FAQ Toggle Functionality')
                # 找到对应的结束位置（两个闭合的});）
                temp = content[start_pos:]
                count = 0
                end_pos = start_pos
                for i, char in enumerate(temp):
                    if char == '{':
                        count += 1
                    elif char == '}':
                        count -= 1
                        if count == 0 and i > 50:  # 确保找到完整的代码块
                            end_pos = start_pos + i + 2  # +2 包括 });
                            break
                
                if end_pos > start_pos:
                    content = content[:start_pos] + new_js + content[end_pos:]
        
        # 写入文件
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
    
    print("🔧 开始正确修复FAQ功能...")
    print("=" * 80)
    
    languages = {
        'zh-TW': '台湾',
        'zh-HK': '香港',
        'ja-JP': '日本',
        'ko-KR': '韩国'
    }
    
    total_fixed = 0
    
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
            if fix_faq_correct(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 FAQ功能正确修复完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n请刷新本地文件并测试FAQ功能！")

if __name__ == '__main__':
    main()

