#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复JavaScript语法错误 - 删除多余的闭合括号
"""

import os
import re
from pathlib import Path

def fix_js_syntax(file_path):
    """修复JavaScript语法错误"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找并修复多余的闭合括号
        # 正确的结构应该是：
        # });
        # </script>
        # 而不是：
        # });
        # });
        # });
        # </script>
        
        # 使用正则表达式修复
        pattern = r'(\s+\}\);\s+)\}\);\s+\}\);\s+</script>'
        replacement = r'\1    </script>'
        
        content = re.sub(pattern, replacement, content)
        
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
    
    print("🔧 开始修复JavaScript语法错误...")
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
            if fix_js_syntax(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 JavaScript语法错误修复完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n请刷新本地文件并测试FAQ功能！")

if __name__ == '__main__':
    main()

