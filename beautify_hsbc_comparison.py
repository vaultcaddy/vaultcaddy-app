#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为hsbc-vs-manual.html添加视觉设计，美化大段文字内容"""

from bs4 import BeautifulSoup
import re

print("=" * 70)
print("开始美化 hsbc-vs-manual.html 的文字内容")
print("=" * 70)
print()

with open('hsbc-vs-manual.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('hsbc-vs-manual.html.backup_beautify', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已创建备份：hsbc-vs-manual.html.backup_beautify")
print()

# 添加新的CSS样式
new_css = """
    /* ====== 对比页面专用样式 ====== */
    
    /* 场景卡片 */
    .scenario-card {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border-left: 4px solid #667eea;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }
    
    .scenario-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    .scenario-card h4 {
        color: #667eea;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .scenario-card ul {
        list-style: none;
        padding: 0;
    }
    
    .scenario-card li {
        padding: 0.75rem 0;
        border-bottom: 1px solid #e5e7eb;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    .scenario-card li:last-child {
        border-bottom: none;
    }
    
    /* 对比结果框 */
    .comparison-result {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
    }
    
    .comparison-result h4 {
        color: white;
        font-size: 1.6rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .comparison-result ul {
        list-style: none;
        padding: 0;
    }
    
    .comparison-result li {
        padding: 0.75rem 0 0.75rem 2rem;
        position: relative;
        font-size: 1.15rem;
        line-height: 1.9;
    }
    
    .comparison-result li:before {
        content: '✅';
        position: absolute;
        left: 0;
        font-size: 1.3rem;
    }
    
    /* 案例引用框 */
    .case-quote {
        background: #f9fafb;
        border-left: 5px solid #fbbf24;
        padding: 2rem;
        margin: 2.5rem 0;
        border-radius: 8px;
        font-style: italic;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .case-quote p {
        font-size: 1.15rem;
        line-height: 2;
        color: #1f2937;
        margin-bottom: 1.5rem;
    }
    
    .case-quote cite {
        display: block;
        text-align: right;
        font-style: normal;
        font-weight: 700;
        color: #667eea;
        font-size: 1.1rem;
        margin-top: 1.5rem;
    }
    
    /* 功能对比框 */
    .feature-comparison {
        background: white;
        border: 2px solid #e5e7eb;
        padding: 2.5rem;
        margin: 2.5rem 0;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    
    .feature-comparison h4 {
        color: #1f2937;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* 价格对比卡片 */
    .price-comparison-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2.5rem 0;
    }
    
    .price-card {
        background: white;
        border: 2px solid #e5e7eb;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .price-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .price-card.featured {
        border: 3px solid #10b981;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    }
    
    .price-card h5 {
        font-size: 1.3rem;
        color: #1f2937;
        margin-bottom: 1.5rem;
    }
    
    .price-card .price {
        font-size: 2.5rem;
        font-weight: 900;
        color: #667eea;
        margin: 1.5rem 0;
    }
    
    .price-card.featured .price {
        color: #10b981;
    }
    
    /* 关键发现框 */
    .key-findings {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin: 2.5rem 0;
        border: 2px solid #fbbf24;
    }
    
    .key-findings h4 {
        color: #92400e;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .key-findings ul {
        list-style: none;
        padding: 0;
    }
    
    .key-findings li {
        padding: 1rem 0 1rem 2.5rem;
        position: relative;
        font-size: 1.15rem;
        line-height: 1.9;
        color: #78350f;
        font-weight: 500;
    }
    
    .key-findings li:before {
        content: '💡';
        position: absolute;
        left: 0;
        font-size: 1.5rem;
    }
    
    /* 真实案例卡片 */
    .real-case-card {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin: 2.5rem 0;
        border: 2px solid #8b5cf6;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.15);
    }
    
    .real-case-card h4 {
        color: #6b21a8;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    .real-case-card .case-details {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .real-case-card .case-result {
        background: #10b981;
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        font-weight: 600;
    }
    
    /* 场景对比网格 */
    .scenario-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2.5rem 0;
    }
    
    .scenario-item {
        background: white;
        border: 2px solid #e5e7eb;
        padding: 2rem;
        border-radius: 12px;
        transition: all 0.3s;
    }
    
    .scenario-item:hover {
        border-color: #667eea;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
    }
    
    .scenario-item h5 {
        color: #667eea;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .scenario-item .result {
        margin-top: 1.5rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .scenario-item .result.success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .scenario-item .result.fail {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* 响应式优化 */
    @media (max-width: 768px) {
        .scenario-card,
        .comparison-result,
        .feature-comparison,
        .key-findings,
        .real-case-card {
            padding: 1.5rem;
        }
        
        .price-comparison-cards {
            grid-template-columns: 1fr;
        }
        
        .scenario-grid {
            grid-template-columns: 1fr;
        }
    }
"""

# 在</style>标签前插入新CSS
content = content.replace('</style>', new_css + '\n    </style>')

print("✅ 已添加新的CSS样式")
print()

# 保存修改后的内容
with open('hsbc-vs-manual.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 70)
print("✅ CSS样式添加完成！")
print("=" * 70)
print()
print("📊 添加的新样式：")
print("   1. ✅ 场景卡片（scenario-card）")
print("   2. ✅ 对比结果框（comparison-result）")
print("   3. ✅ 案例引用框（case-quote）")
print("   4. ✅ 功能对比框（feature-comparison）")
print("   5. ✅ 价格对比卡片（price-comparison-cards）")
print("   6. ✅ 关键发现框（key-findings）")
print("   7. ✅ 真实案例卡片（real-case-card）")
print("   8. ✅ 场景对比网格（scenario-grid）")
print()
print("💡 下一步：")
print("   需要手动应用这些CSS类到HTML内容中")
print("   或者运行第二个脚本自动添加这些类")
print("=" * 70)

