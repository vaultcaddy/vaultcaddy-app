#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bing特定SEO优化：为Bing搜索引擎优化4个语言版本
Bing Specific SEO Optimization: Optimize for Bing search engine
"""

import os
from pathlib import Path

def optimize_for_bing():
    """为Bing优化所有语言版本的首页"""
    
    files_to_optimize = {
        'index.html': {
            'lang': 'zh-TW',
            'region': 'HK',
            'bing_specific': {
                'ms.country': 'HK',
                'ms.topic': 'Business, Accounting, Banking',
            }
        },
        'en/index.html': {
            'lang': 'en',
            'region': 'GB-US-AU-CA-NZ',  # 扩展到所有英语国家
            'bing_specific': {
                'ms.country': 'GB;US;AU;CA;NZ',
                'ms.topic': 'Business, Accounting, Banking',
            }
        },
        'jp/index.html': {
            'lang': 'ja',
            'region': 'JP',
            'bing_specific': {
                'ms.country': 'JP',
                'ms.topic': 'Business, Accounting, Banking',
            }
        },
        'kr/index.html': {
            'lang': 'ko',
            'region': 'KR',
            'bing_specific': {
                'ms.country': 'KR',
                'ms.topic': 'Business, Accounting, Banking',
            }
        }
    }
    
    for file_path, config in files_to_optimize.items():
        print(f"\n🔧 优化 {file_path} for Bing...")
        
        if not os.path.exists(file_path):
            print(f"  ⚠️  文件不存在，跳过")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有Bing特定标签
        if 'ms.country' in content:
            print(f"  ℹ️  已包含Bing标签")
            continue
        
        # 构建Bing特定meta标签
        bing_meta_tags = f'''
    <!-- Bing Webmaster优化 -->
    <meta name="ms.country" content="{config['bing_specific']['ms.country']}">
    <meta name="ms.topic" content="{config['bing_specific']['ms.topic']}">
    <meta name="ms.category" content="Banking, Accounting, Finance, OCR, AI">
    <meta name="ms.locale" content="{config['lang']}">
'''
        
        # 在</head>前插入
        if '</head>' in content:
            content = content.replace('</head>', bing_meta_tags + '\n</head>')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Bing优化完成")
        else:
            print(f"  ❌ 无法找到</head>标签")
    
    print("\n" + "="*70)
    print("📊 Bing SEO优化总结:")
    print(f"  ✅ 添加 ms.country 标签（指定目标国家）")
    print(f"  ✅ 添加 ms.topic 标签（指定主题分类）")
    print(f"  ✅ 添加 ms.category 标签（指定行业类别）")
    print(f"  ✅ 英文版扩展到5个英语国家（GB, US, AU, CA, NZ）")
    print("="*70)

if __name__ == '__main__':
    print("🎯 Bing特定SEO优化")
    print("="*70)
    optimize_for_bing()
    print("\n✅ 优化完成！")

