#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面SEO审计 - 检查缺失的内容和SEO优化机会
"""

import os
from pathlib import Path
import json

def seo_audit():
    """进行全面SEO审计"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              🔍 VaultCaddy 全面SEO审计                                ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    issues = []
    recommendations = []
    
    # 1. 检查收据相关内容
    print("\n1️⃣  检查收据相关内容")
    print("="*70)
    
    receipt_files = {
        'zh': 'receipt-scanner.html',
        'en': 'en/receipt-scanner.html',
        'jp': 'jp/receipt-scanner.html',
        'kr': 'kr/receipt-scanner.html'
    }
    
    missing_receipt = []
    for lang, file in receipt_files.items():
        if os.path.exists(file):
            print(f"   ✅ {lang.upper()}: {file}")
        else:
            print(f"   ❌ {lang.upper()}: {file} - 缺失")
            missing_receipt.append((lang, file))
    
    if missing_receipt:
        issues.append({
            'category': '收据页面',
            'severity': 'HIGH',
            'issue': f'缺少 {len(missing_receipt)} 个语言版本的收据扫描页面',
            'missing': missing_receipt
        })
    
    # 2. 检查收据博客文章
    print("\n2️⃣  检查收据博客文章")
    print("="*70)
    
    receipt_blog_topics = [
        'receipt-scanning-guide',
        'receipt-management-best-practices',
        'expense-tracking-with-receipts',
        'receipt-ocr-technology',
        'digital-receipt-management'
    ]
    
    for lang in ['en', 'jp', 'kr']:
        blog_dir = Path(f'{lang}/blog')
        if blog_dir.exists():
            existing = list(blog_dir.glob('*receipt*.html'))
            print(f"   {lang.upper()}: {len(existing)} 个收据相关文章")
            if len(existing) == 0:
                issues.append({
                    'category': '收据博客',
                    'severity': 'MEDIUM',
                    'issue': f'{lang.upper()} 缺少收据相关博客文章',
                    'recommendation': '创建至少2-3篇收据相关文章'
                })
    
    # 3. 检查Landing Pages
    print("\n3️⃣  检查收据相关Landing Pages")
    print("="*70)
    
    for lang in ['en', 'jp', 'kr']:
        solutions_dir = Path(f'{lang}/solutions')
        if solutions_dir.exists():
            receipt_pages = list(solutions_dir.glob('*receipt*'))
            print(f"   {lang.upper()}: {len(receipt_pages)} 个收据相关landing page")
    
    # 4. 检查robots.txt
    print("\n4️⃣  检查robots.txt")
    print("="*70)
    
    if os.path.exists('robots.txt'):
        with open('robots.txt', 'r') as f:
            content = f.read()
            print(f"   ✅ robots.txt 存在")
            if 'Sitemap:' in content:
                print(f"   ✅ 包含Sitemap引用")
            else:
                issues.append({
                    'category': 'robots.txt',
                    'severity': 'MEDIUM',
                    'issue': 'robots.txt缺少Sitemap引用'
                })
    else:
        issues.append({
            'category': 'robots.txt',
            'severity': 'HIGH',
            'issue': 'robots.txt文件不存在'
        })
    
    # 5. 检查Open Graph图片
    print("\n5️⃣  检查Open Graph图片")
    print("="*70)
    
    og_images = Path('images').glob('og-*.png') if Path('images').exists() else []
    og_images = list(og_images)
    print(f"   找到 {len(og_images)} 个OG图片")
    
    if len(og_images) == 0:
        recommendations.append({
            'category': 'Open Graph',
            'priority': 'MEDIUM',
            'recommendation': '创建Open Graph图片（1200x630）用于社交媒体分享'
        })
    
    # 6. 检查Schema.org标记
    print("\n6️⃣  检查Schema.org结构化数据")
    print("="*70)
    
    pages_to_check = [
        'index.html',
        'en/index.html',
        'jp/index.html',
        'kr/index.html'
    ]
    
    missing_schema = []
    for page in pages_to_check:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'application/ld+json' in content:
                    print(f"   ✅ {page}: 有Schema")
                else:
                    print(f"   ❌ {page}: 缺少Schema")
                    missing_schema.append(page)
    
    if missing_schema:
        issues.append({
            'category': 'Schema.org',
            'severity': 'MEDIUM',
            'issue': f'{len(missing_schema)} 个主页缺少结构化数据',
            'pages': missing_schema
        })
    
    # 7. 检查内部链接
    print("\n7️⃣  检查内部链接优化")
    print("="*70)
    
    recommendations.append({
        'category': '内部链接',
        'priority': 'HIGH',
        'recommendation': '在博客文章之间添加相关文章链接'
    })
    
    recommendations.append({
        'category': '内部链接',
        'priority': 'MEDIUM',
        'recommendation': '在Landing Pages添加指向博客文章的链接'
    })
    
    # 8. 检查H1标签
    print("\n8️⃣  检查H1标签优化")
    print("="*70)
    
    recommendations.append({
        'category': 'H1标签',
        'priority': 'LOW',
        'recommendation': '确保每个页面只有一个H1标签，包含主要关键词'
    })
    
    # 9. 检查移动端友好性
    print("\n9️⃣  移动端友好性")
    print("="*70)
    
    recommendations.append({
        'category': '移动端',
        'priority': 'MEDIUM',
        'recommendation': '在Google Search Console中检查移动端可用性'
    })
    
    # 10. 检查页面加载速度
    print("\n🔟 页面加载速度")
    print("="*70)
    
    recommendations.append({
        'category': '页面速度',
        'priority': 'HIGH',
        'recommendation': '使用Google PageSpeed Insights检查所有主要页面'
    })
    
    # 生成报告
    print("\n" + "="*70)
    print("📊 审计结果总结")
    print("="*70)
    
    print(f"\n🚨 发现问题：{len(issues)} 个")
    for i, issue in enumerate(issues, 1):
        print(f"\n   {i}. [{issue['severity']}] {issue['category']}")
        print(f"      问题：{issue['issue']}")
        if 'recommendation' in issue:
            print(f"      建议：{issue['recommendation']}")
    
    print(f"\n💡 改进建议：{len(recommendations)} 个")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n   {i}. [{rec['priority']}] {rec['category']}")
        print(f"      建议：{rec['recommendation']}")
    
    # 保存详细报告
    report = {
        'issues': issues,
        'recommendations': recommendations,
        'summary': {
            'total_issues': len(issues),
            'high_severity': len([i for i in issues if i['severity'] == 'HIGH']),
            'medium_severity': len([i for i in issues if i['severity'] == 'MEDIUM']),
            'total_recommendations': len(recommendations)
        }
    }
    
    with open('seo_audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细报告已保存到：seo_audit_report.json")
    
    return issues, recommendations

if __name__ == '__main__':
    seo_audit()

