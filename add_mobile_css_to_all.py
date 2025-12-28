#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有Landing Page添加手机版响应式CSS
"""

import os
import re
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent

# 手机版响应式CSS
MOBILE_CSS = '''
    <!-- 手機版響應式優化 -->
    <style>
    @media (max-width: 768px) {
        /* 新增区域响应式样式 */
        section h2 {
            font-size: 1.8rem !important;
        }
        
        section h3 {
            font-size: 1.3rem !important;
        }
        
        section h4 {
            font-size: 1.1rem !important;
        }
        
        section p {
            font-size: 0.95rem !important;
        }
        
        /* 网格布局改为单列 */
        section div[style*="display: grid"][style*="grid-template-columns: 1fr 1fr"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(2, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(3, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(4, 1fr)"] {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        
        /* 表格滚动 */
        table {
            font-size: 0.85rem !important;
        }
        
        table th,
        table td {
            padding: 0.5rem !important;
        }
        
        /* 容器内边距 */
        .container {
            padding: 0 1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        section h2 {
            font-size: 1.5rem !important;
        }
        
        section h3 {
            font-size: 1.2rem !important;
        }
        
        section h4 {
            font-size: 1rem !important;
        }
        
        section p, section li {
            font-size: 0.9rem !important;
        }
        
        /* 4列网格在小屏幕改为1列 */
        section div[style*="display: grid"][style*="grid-template-columns: repeat(4, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        /* 图片边距 */
        img {
            margin-bottom: 2rem !important;
        }
        
        /* 内边距优化 */
        section {
            padding: 3rem 0 !important;
        }
        
        section > div {
            padding: 0 0.75rem !important;
        }
    }
    </style>
'''

def add_mobile_css(file_path):
    """为单个页面添加手机版CSS"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有手机版CSS
        if '<!-- 手機版響應式優化 -->' in content:
            return False  # 已经有了，跳过
        
        # 在</head>前添加CSS
        head_pattern = r'(</head>)'
        if re.search(head_pattern, content, re.IGNORECASE):
            content = re.sub(
                head_pattern,
                MOBILE_CSS + '\n' + r'\1',
                content,
                count=1,
                flags=re.IGNORECASE
            )
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        else:
            return None  # 找不到</head>
        
    except Exception as e:
        print(f"  ❌ 错误 {file_path.name}: {str(e)}")
        return None

def main():
    """主函数"""
    print("🚀 为所有Landing Page添加手机版响应式CSS...")
    print("=" * 60)
    
    # 统计
    total = 0
    success = 0
    skipped = 0
    failed = 0
    
    # 处理银行页面
    print("\n📱 处理银行页面...")
    
    # 中文版
    bank_files = list(BASE_DIR.glob('*-bank-statement.html'))
    for file_path in sorted(bank_files):
        total += 1
        result = add_mobile_css(file_path)
        if result:
            success += 1
            print(f"  ✅ 添加CSS: {file_path.name}")
        elif result is False:
            skipped += 1
        else:
            failed += 1
    
    # 多语言版
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            bank_files = list(lang_dir.glob('*-bank-statement.html'))
            for file_path in sorted(bank_files):
                total += 1
                result = add_mobile_css(file_path)
                if result:
                    success += 1
                    print(f"  ✅ 添加CSS: {lang}/{file_path.name}")
                elif result is False:
                    skipped += 1
                else:
                    failed += 1
    
    # 处理行业页面
    print("\n📱 处理行业页面...")
    
    # 中文版
    industry_files = list(BASE_DIR.glob('*-accounting-solution.html'))
    for file_path in sorted(industry_files):
        total += 1
        result = add_mobile_css(file_path)
        if result:
            success += 1
            print(f"  ✅ 添加CSS: {file_path.name}")
        elif result is False:
            skipped += 1
        else:
            failed += 1
    
    # 多语言版
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            industry_files = list(lang_dir.glob('*-accounting-solution.html'))
            for file_path in sorted(industry_files):
                total += 1
                result = add_mobile_css(file_path)
                if result:
                    success += 1
                    print(f"  ✅ 添加CSS: {lang}/{file_path.name}")
                elif result is False:
                    skipped += 1
                else:
                    failed += 1
    
    # 打印统计
    print("\n" + "=" * 60)
    print("📊 处理统计:")
    print(f"  总计: {total} 个文件")
    print(f"  ✅ 成功添加: {success} 个")
    print(f"  ⏭️  已有CSS: {skipped} 个")
    print(f"  ❌ 失败: {failed} 个")
    print("=" * 60)
    print("\n✨ 手机版CSS添加完成！")

if __name__ == '__main__':
    main()

