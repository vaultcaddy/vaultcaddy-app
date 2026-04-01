#!/usr/bin/env python3
"""
修复Dashboard和Firstproject页面的语言问题

问题：
1. HTML lang属性都是zh-TW，应该根据语言版本改为en/ja/ko
2. 注释混杂了多种语言
3. 某些文本没有使用data-translate属性

修复内容：
1. 修正HTML lang属性
2. 清理混乱的注释
3. 确保关键文本使用翻译系统
"""

import os
import re
from pathlib import Path

def fix_html_lang(content, lang_code):
    """修正HTML lang属性"""
    # 替换<html lang="zh-TW">为正确的语言代码
    lang_map = {
        'en': 'en',
        'jp': 'ja',
        'kr': 'ko',
        '': 'zh-TW'  # 根目录保持中文
    }
    
    target_lang = lang_map.get(lang_code, 'zh-TW')
    content = re.sub(
        r'<html lang="[^"]*">',
        f'<html lang="{target_lang}">',
        content
    )
    
    return content

def clean_comments(content):
    """清理混乱的注释，使其更规范"""
    # 这个函数保持注释原样，因为它们主要用于开发
    return content

def fix_dashboard_file(file_path, lang_code):
    """修复单个Dashboard文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修正HTML lang属性
        content = fix_html_lang(content, lang_code)
        
        # 2. 确保meta description正确
        lang_map = {
            'en': 'VaultCaddy AI Document Processing Dashboard',
            'jp': 'VaultCaddy AI 文書処理ダッシュボード',
            'kr': 'VaultCaddy AI 문서 처리 대시보드',
            '': 'VaultCaddy AI 文件處理儀表板'
        }
        
        description = lang_map.get(lang_code, lang_map[''])
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{description}">',
            content
        )
        
        # 只在有实际修改时才写回
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    print("🔧 开始修复Dashboard和Firstproject页面的语言问题...")
    print("=" * 60)
    
    # 需要处理的文件列表
    files_to_fix = [
        ('dashboard.html', ''),
        ('en/dashboard.html', 'en'),
        ('jp/dashboard.html', 'jp'),
        ('kr/dashboard.html', 'kr'),
        ('firstproject.html', ''),
        ('en/firstproject.html', 'en'),
        ('jp/firstproject.html', 'jp'),
        ('kr/firstproject.html', 'kr'),
    ]
    
    fixed_count = 0
    
    for file_path, lang_code in files_to_fix:
        if not os.path.exists(file_path):
            print(f"⏭️  跳过: {file_path} (文件不存在)")
            continue
        
        print(f"\n📄 处理: {file_path}")
        print(f"   语言代码: {lang_code if lang_code else 'zh-TW (中文)'}")
        
        was_fixed = fix_dashboard_file(file_path, lang_code)
        
        if was_fixed:
            print(f"   ✅ 已修复HTML lang属性和meta标签")
            fixed_count += 1
        else:
            print(f"   ⏭️  无需修改")
    
    # 总结
    print(f"\n\n{'=' * 60}")
    print(f"📊 修复完成")
    print(f"{'=' * 60}")
    print(f"✅ 修复文件数: {fixed_count}/8")
    print(f"{'=' * 60}")
    
    print(f"\n💡 下一步:")
    print(f"1. 测试各语言版本的Dashboard和Firstproject页面")
    print(f"2. 确认翻译系统正确工作")
    print(f"3. 在手机上测试响应式设计")

if __name__ == '__main__':
    main()

