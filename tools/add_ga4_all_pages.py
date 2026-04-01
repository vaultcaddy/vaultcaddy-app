#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Google Analytics 4代码添加到所有页面
测量ID: G-LWPEKNC7RQ
"""

import glob
from pathlib import Path

# GA4代码模板
GA4_CODE = '''
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-LWPEKNC7RQ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-LWPEKNC7RQ');
    </script>
'''

def add_ga4_to_file(file_path):
    """添加GA4代码到单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有GA4代码（避免重复添加）
        if 'G-LWPEKNC7RQ' in content or 'Google Analytics 4' in content:
            print(f"⏭️  跳过 {file_path}（已有GA4代码）")
            return False
        
        # 查找</head>标签
        if '</head>' not in content:
            print(f"❌ 跳过 {file_path}（找不到</head>标签）")
            return False
        
        # 在</head>前添加GA4代码
        updated_content = content.replace('</head>', f'{GA4_CODE}\n</head>')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已添加GA4到 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 处理 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 开始添加Google Analytics 4到所有页面")
    print("=" * 70)
    print(f"测量ID: G-LWPEKNC7RQ")
    print()
    
    # 所有需要添加GA4的文件
    files_to_process = []
    
    # 1. 主页（4个语言版本）
    files_to_process.extend([
        'index.html',
        'en/index.html',
        'jp/index.html',
        'kr/index.html',
    ])
    
    # 2. Blog页面（4个语言版本）
    files_to_process.extend([
        'blog/index.html',
        'en/blog/index.html',
        'jp/blog/index.html',
        'kr/blog/index.html',
    ])
    
    # 3. 用户页面（4个语言版本）
    for lang in ['', 'en/', 'jp/', 'kr/']:
        files_to_process.extend([
            f'{lang}auth.html',
            f'{lang}dashboard.html',
            f'{lang}billing.html',
            f'{lang}account.html',
            f'{lang}firstproject.html',
            f'{lang}document-detail.html',
        ])
    
    # 4. 所有Landing Page
    landing_pages = list(glob.glob('*-statement.html'))  # 银行页面
    landing_pages.extend(glob.glob('for/*.html'))  # 用户类型页面
    landing_pages.extend(glob.glob('solutions/*.html'))  # 解决方案页面
    landing_pages.extend(glob.glob('integrations/*.html'))  # 软件整合页面
    landing_pages.extend([
        'tax-season-helper.html',
        'invoice-processing.html',
        'receipt-scanner.html',
    ])  # 特殊用途页面
    
    files_to_process.extend(landing_pages)
    
    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in files_to_process:
        if Path(file_path).exists():
            result = add_ga4_to_file(file_path)
            if result:
                success_count += 1
            elif result is False:
                skip_count += 1
        else:
            # 不打印不存在的文件（有些页面可能不存在）
            error_count += 1
    
    print()
    print("=" * 70)
    print("📊 执行结果统计")
    print("=" * 70)
    print(f"✅ 成功添加GA4: {success_count} 个文件")
    print(f"⏭️  跳过（已有GA4）: {skip_count} 个文件")
    print(f"⚠️  文件不存在: {error_count} 个文件")
    print(f"📝 总计处理: {len(files_to_process)} 个文件")
    print()
    print("🎉 Google Analytics 4已添加到所有重要页面！")
    print()
    print("📋 下一步:")
    print("1. 等待10-15分钟，让GA4开始收集数据")
    print("2. 访问 https://analytics.google.com")
    print("3. 查看实时报告，确认GA4正常工作")
    print("4. 打开网站任意页面，应该会在实时报告中看到访问")
    print()
    print("🎯 恭喜！VaultCaddy现在可以追踪所有流量数据了！")
    print()

if __name__ == '__main__':
    main()

