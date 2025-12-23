#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化页面关键词密度
分析并优化主要关键词在页面中的出现频率
目标：关键词密度控制在2-5%之间
"""

import os
import re
from bs4 import BeautifulSoup
from collections import Counter

# 目标关键词（每个语言的核心关键词）
TARGET_KEYWORDS = {
    'zh': [
        '銀行對帳单', 'QuickBooks', 'AI', '會計', '對帳', 
        '轉換', 'Excel', '處理', '自動化', '香港'
    ],
    'en': [
        'bank statement', 'QuickBooks', 'AI', 'accounting', 'reconciliation',
        'convert', 'Excel', 'processing', 'automation', 'software'
    ],
    'ja': [
        '銀行明細', 'QuickBooks', 'AI', '会計', '照合',
        '変換', 'Excel', '処理', '自動化', 'ソフト'
    ],
    'ko': [
        '은행 명세서', 'QuickBooks', 'AI', '회계', '조회',
        '변환', 'Excel', '처리', '자동화', '소프트웨어'
    ]
}

def analyze_keyword_density(file_path, lang):
    """
    分析页面关键词密度
    
    Args:
        file_path: HTML文件路径
        lang: 语言代码
    
    Returns:
        dict: 关键词分析结果
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 移除script和style标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取所有文本
        text = soup.get_text()
        
        # 计算总词数
        words = text.split()
        total_words = len(words)
        
        # 统计目标关键词出现次数
        keywords = TARGET_KEYWORDS[lang]
        keyword_counts = {}
        
        for keyword in keywords:
            # 不区分大小写搜索
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
            density = (count / total_words * 100) if total_words > 0 else 0
            keyword_counts[keyword] = {
                'count': count,
                'density': density,
                'status': '✅' if 2 <= density <= 5 else ('⚠️' if density > 5 else '❌')
            }
        
        return {
            'total_words': total_words,
            'keywords': keyword_counts
        }
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None

def generate_keyword_report(file_path, lang, name):
    """
    生成关键词密度报告
    
    Args:
        file_path: HTML文件路径
        lang: 语言代码
        name: 版本名称
    
    Returns:
        dict: 分析结果
    """
    print(f"\n{'='*60}")
    print(f"📊 {name} 关键词密度分析")
    print(f"{'='*60}")
    
    result = analyze_keyword_density(file_path, lang)
    
    if not result:
        print("❌ 分析失败")
        return None
    
    print(f"📝 总词数: {result['total_words']:,} 个")
    print(f"\n🔑 核心关键词密度:")
    print(f"{'关键词':<20} {'出现次数':<12} {'密度':<12} {'状态':<8}")
    print("-" * 60)
    
    for keyword, data in result['keywords'].items():
        print(f"{keyword:<20} {data['count']:<12} {data['density']:.2f}%{'':<8} {data['status']}")
    
    # 统计状态
    statuses = [data['status'] for data in result['keywords'].values()]
    good_count = statuses.count('✅')
    warning_count = statuses.count('⚠️')
    bad_count = statuses.count('❌')
    
    print(f"\n📈 密度分布:")
    print(f"  ✅ 理想范围(2-5%): {good_count} 个")
    print(f"  ⚠️  过高(>5%): {warning_count} 个")
    print(f"  ❌ 过低(<2%): {bad_count} 个")
    
    # 给出优化建议
    print(f"\n💡 优化建议:")
    for keyword, data in result['keywords'].items():
        if data['status'] == '❌':
            print(f"  • 增加'{keyword}'的出现频率（当前{data['density']:.2f}%，建议2-3%）")
        elif data['status'] == '⚠️':
            print(f"  • 减少'{keyword}'的出现频率（当前{data['density']:.2f}%，建议3-4%）")
    
    return result

def main():
    """主函数"""
    print("🎯 第5周任务3：优化页面关键词密度")
    print("=" * 60)
    print("📋 目标：确保核心关键词密度在2-5%范围内")
    print("-" * 60)
    
    # 4个版本的首页
    index_files = [
        ('index.html', 'zh', '中文版'),
        ('en/index.html', 'en', '英文版'),
        ('jp/index.html', 'ja', '日文版'),
        ('kr/index.html', 'ko', '韩文版')
    ]
    
    all_results = {}
    
    for file_path, lang, name in index_files:
        if not os.path.exists(file_path):
            print(f"\n⏭️  {name}: 文件不存在")
            continue
        
        result = generate_keyword_report(file_path, lang, name)
        if result:
            all_results[name] = result
    
    # 总体评估
    print(f"\n{'='*60}")
    print("🎯 总体评估")
    print(f"{'='*60}")
    
    total_good = 0
    total_warning = 0
    total_bad = 0
    
    for name, result in all_results.items():
        statuses = [data['status'] for data in result['keywords'].values()]
        total_good += statuses.count('✅')
        total_warning += statuses.count('⚠️')
        total_bad += statuses.count('❌')
    
    total_keywords = total_good + total_warning + total_bad
    
    print(f"📊 4个版本总计:")
    print(f"  ✅ 理想范围: {total_good}/{total_keywords} ({total_good/total_keywords*100:.1f}%)")
    print(f"  ⚠️  需要微调: {total_warning}/{total_keywords} ({total_warning/total_keywords*100:.1f}%)")
    print(f"  ❌ 需要增强: {total_bad}/{total_keywords} ({total_bad/total_keywords*100:.1f}%)")
    
    print(f"\n🚀 SEO优化建议:")
    print(f"  1. 在Hero区域自然融入关键词")
    print(f"  2. 在功能说明中重复核心关键词")
    print(f"  3. 在FAQ中使用长尾关键词")
    print(f"  4. 确保关键词分布均匀，避免堆砌")
    print(f"  5. 优先优化密度<2%的关键词")
    
    print(f"\n📈 预期效果:")
    print(f"  ✅ 提升搜索引擎对页面主题的理解")
    print(f"  ✅ 改善相关关键词排名")
    print(f"  ✅ 提高自然流量转化率")
    print(f"  ✅ 预期排名提升 +2-4位")

if __name__ == '__main__':
    main()

