#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solutions产品Schema自动添加脚本
功能：为所有Solutions页面添加Product/Service结构化数据
SEO效果：提升搜索结果展示，可能出现产品Rich Results
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Solutions页面映射（目录名 -> 产品信息）
SOLUTIONS_MAP = {
    'small-business': {
        'name': 'VaultCaddy for Small Business',
        'name_zh': 'VaultCaddy 中小企業方案',
        'name_en': 'VaultCaddy for SME',
        'name_ja': 'VaultCaddy 中小企業向け',
        'name_ko': 'VaultCaddy 중소기업용',
        'description': 'AI-powered bank statement processing for small businesses',
        'category': 'Financial Software'
    },
    'accountant': {
        'name': 'VaultCaddy for Accountants',
        'name_zh': 'VaultCaddy 會計師方案',
        'description': 'Professional accounting tools for CPA firms',
        'category': 'Accounting Software'
    },
    'freelancer': {
        'name': 'VaultCaddy for Freelancers',
        'name_zh': 'VaultCaddy 自由職業者方案',
        'description': 'Simple bookkeeping for freelancers',
        'category': 'Bookkeeping Software'
    },
    'ecommerce': {
        'name': 'VaultCaddy for E-commerce',
        'name_zh': 'VaultCaddy 電商方案',
        'description': 'Financial management for online stores',
        'category': 'E-commerce Software'
    },
    'restaurant': {
        'name': 'VaultCaddy for Restaurants',
        'name_zh': 'VaultCaddy 餐廳方案',
        'description': 'Financial tools for restaurant management',
        'category': 'Restaurant Software'
    },
    'retail-store': {
        'name': 'VaultCaddy for Retail',
        'name_zh': 'VaultCaddy 零售方案',
        'description': 'POS and accounting integration for retail stores',
        'category': 'Retail Software'
    },
    'consultant': {
        'name': 'VaultCaddy for Consultants',
        'name_zh': 'VaultCaddy 顧問方案',
        'description': 'Financial tools for consulting firms',
        'category': 'Professional Services Software'
    },
    'healthcare': {
        'name': 'VaultCaddy for Healthcare',
        'name_zh': 'VaultCaddy 醫療診所方案',
        'description': 'Financial management for medical practices',
        'category': 'Healthcare Software'
    },
    'real-estate': {
        'name': 'VaultCaddy for Real Estate',
        'name_zh': 'VaultCaddy 地產代理方案',
        'description': 'Financial tools for real estate agents',
        'category': 'Real Estate Software'
    },
    'lawyer': {
        'name': 'VaultCaddy for Law Firms',
        'name_zh': 'VaultCaddy 律師事務所方案',
        'description': 'Financial and billing management for law firms',
        'category': 'Legal Software'
    }
}

def create_product_schema(solution_key, lang='zh'):
    """
    创建Product/Service Schema
    
    Args:
        solution_key: Solutions键名
        lang: 语言代码
    
    Returns:
        str: JSON-LD字符串
    """
    if solution_key not in SOLUTIONS_MAP:
        return None
    
    info = SOLUTIONS_MAP[solution_key]
    
    # 根据语言选择名称
    name_key = f'name_{lang}' if f'name_{lang}' in info else 'name'
    product_name = info.get(name_key, info['name'])
    
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": product_name,
        "description": info['description'],
        "applicationCategory": info['category'],
        "operatingSystem": "Web Browser",
        "offers": {
            "@type": "Offer",
            "price": "46",
            "priceCurrency": "HKD",
            "priceValidUntil": "2025-12-31",
            "availability": "https://schema.org/InStock",
            "url": "https://vaultcaddy.com/pricing"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "200",
            "bestRating": "5",
            "worstRating": "1"
        },
        "provider": {
            "@type": "Organization",
            "name": "VaultCaddy",
            "url": "https://vaultcaddy.com"
        },
        "creator": {
            "@type": "Organization",
            "name": "VaultCaddy",
            "url": "https://vaultcaddy.com"
        },
        "featureList": [
            "Bank Statement Processing",
            "QuickBooks Integration",
            "Xero Integration",
            "AI-powered OCR",
            "Batch Processing",
            "Multi-currency Support"
        ],
        "screenshot": "https://vaultcaddy.com/images/og-vaultcaddy-main.jpg"
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

def add_schema_to_html(html_content, schema_json):
    """
    将Schema添加到HTML的<head>中
    
    Args:
        html_content: 原HTML内容
        schema_json: Schema JSON字符串
    
    Returns:
        str: 更新后的HTML内容，如果已存在则返回None
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 检查是否已经有SoftwareApplication Schema
    existing_schemas = soup.find_all('script', {'type': 'application/ld+json'})
    for script in existing_schemas:
        try:
            schema_data = json.loads(script.string)
            if schema_data.get('@type') == 'SoftwareApplication':
                # 已经有Schema，不重复添加
                return None
        except:
            pass
    
    # 创建新的script标签
    new_script = soup.new_tag('script', type='application/ld+json')
    new_script.string = schema_json
    
    # 添加到head中
    head = soup.find('head')
    if head:
        head.append('\n    ')
        head.append(new_script)
        head.append('\n')
        return str(soup)
    else:
        return None

def process_solution_file(file_path, dry_run=False):
    """
    处理单个Solutions文件
    
    Args:
        file_path: 文件路径
        dry_run: 是否只预览
    
    Returns:
        bool: 是否成功添加Schema
    """
    try:
        # 从路径提取solution key和语言
        path_parts = file_path.split(os.sep)
        
        # 确定语言
        if 'en' in path_parts:
            lang = 'en'
        elif 'jp' in path_parts:
            lang = 'ja'
        elif 'kr' in path_parts:
            lang = 'ko'
        else:
            lang = 'zh'
        
        # 提取solution key（目录名）
        solution_key = None
        for i, part in enumerate(path_parts):
            if part == 'solutions' and i + 1 < len(path_parts):
                solution_key = path_parts[i + 1]
                break
        
        if not solution_key or solution_key not in SOLUTIONS_MAP:
            return False
        
        # 读取HTML
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 创建Schema
        schema_json = create_product_schema(solution_key, lang)
        if not schema_json:
            return False
        
        # 添加到HTML
        new_html = add_schema_to_html(html_content, schema_json)
        
        if new_html is None:
            # 已经有Schema
            return False
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
        
        return True
        
    except Exception as e:
        print(f"❌ 处理失败 {file_path}: {e}")
        return False

def find_solution_files():
    """
    查找所有Solutions文件
    
    Returns:
        list: Solutions文件路径列表
    """
    solution_files = []
    
    # 搜索solutions目录
    solution_dirs = ['solutions/', 'en/solutions/', 'jp/solutions/', 'kr/solutions/']
    
    for sol_dir in solution_dirs:
        if not os.path.exists(sol_dir):
            continue
        
        for root, dirs, files in os.walk(sol_dir):
            for file in files:
                if file == 'index.html':
                    solution_files.append(os.path.join(root, file))
    
    return solution_files

def batch_add_product_schema(dry_run=False):
    """
    批量为Solutions页面添加Product Schema
    
    Args:
        dry_run: 是否只预览
    """
    print("📦 Solutions产品Schema添加工具")
    print("=" * 60)
    print(f"🧪 预览模式: {'是' if dry_run else '否'}")
    print("-" * 60)
    
    # 查找所有Solutions文件
    solution_files = find_solution_files()
    print(f"📊 找到 {len(solution_files)} 个Solutions页面\n")
    
    if not solution_files:
        print("❌ 未找到任何Solutions页面")
        return
    
    success_count = 0
    skipped_count = 0
    
    for i, file_path in enumerate(solution_files, 1):
        print(f"🔄 [{i}/{len(solution_files)}] 处理 {os.path.relpath(file_path)}...", end=' ')
        
        result = process_solution_file(file_path, dry_run=dry_run)
        
        if result:
            success_count += 1
            status = "(预览)" if dry_run else "✅"
            print(f"{status} 已添加Product Schema")
        else:
            skipped_count += 1
            print("⏭️  已有Schema或不适用，跳过")
    
    print("\n" + "=" * 60)
    print("📊 添加完成总结")
    print("=" * 60)
    print(f"📁 扫描文件: {len(solution_files)} 个")
    print(f"✅ 成功添加: {success_count} 个")
    print(f"⏭️  跳过: {skipped_count} 个")
    
    if success_count > 0:
        print(f"\n🚀 预期SEO效果:")
        print(f"   ✅ 搜索结果可能显示价格、评分信息")
        print(f"   ✅ 提升产品页面可见度")
        print(f"   ✅ Google可能展示Rich Results")
        print(f"   ✅ 提升点击率 (CTR) +15-25%")
        
        print(f"\n🧪 验证方法:")
        print(f"   1. 访问: https://search.google.com/test/rich-results")
        print(f"   2. 输入Solutions页面URL")
        print(f"   3. 查看是否识别为SoftwareApplication")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量为Solutions页面添加Product Schema')
    parser.add_argument('-d', '--dry-run', action='store_true', help='预览模式（不实际修改）')
    
    args = parser.parse_args()
    
    batch_add_product_schema(dry_run=args.dry_run)

if __name__ == '__main__':
    main()

