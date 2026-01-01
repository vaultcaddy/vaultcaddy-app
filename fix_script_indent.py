#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复</script>标签的缩进
"""

import os
from pathlib import Path

def fix_indent(file_path):
    """修复缩进"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复缩进
        content = content.replace('        });\n            </script>', '        });\n    </script>')
        
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
    
    print("🔧 修复</script>缩进...")
    
    languages = ['zh-TW', 'zh-HK', 'ja-JP', 'ko-KR']
    total_fixed = 0
    
    for lang_code in languages:
        lang_dir = root_dir / lang_code
        if not lang_dir.exists():
            continue
        
        lang_files = list(lang_dir.glob('*-v3.html'))
        lang_files = [f for f in lang_files if 'test' not in f.name]
        
        for file_path in lang_files:
            if fix_indent(file_path):
                total_fixed += 1
    
    print(f"✅ 完成！修复了 {total_fixed} 个页面")

if __name__ == '__main__':
    main()

