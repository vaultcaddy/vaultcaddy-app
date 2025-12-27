#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彻底重新设计对比页面 - 采用卡片式、数据可视化的现代设计"""

import re

print("=" * 70)
print("🎨 设计大师模式：彻底重新设计对比页面")
print("=" * 70)
print()

with open('hsbc-vs-manual.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('hsbc-vs-manual.html.backup_redesign', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已创建备份：hsbc-vs-manual.html.backup_redesign")
print()

# 新的设计方案：创建全新的CSS
new_design_css = """
    /* ====== 全新设计系统 ====== */
    
    /* 价格对比大卡片 */
    .price-comparison-hero {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 2rem;
        margin: 4rem 0;
        align-items: stretch;
    }
    
    .price-card-large {
        background: white;
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.12);
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s;
    }
    
    .price-card-large:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.18);
    }
    
    .price-card-large.winner {
        border: 4px solid #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 50%);
    }
    
    .price-card-large.winner::before {
        content: '✨ 推薦方案';
        position: absolute;
        top: 0;
        right: 0;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 0 0 0 24px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .price-card-large .card-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 2rem;
    }
    
    .price-card-large.winner .card-title {
        color: #10b981;
    }
    
    .price-card-large .price-amount {
        font-size: 4rem;
        font-weight: 900;
        color: #667eea;
        margin: 2rem 0;
        line-height: 1;
    }
    
    .price-card-large.winner .price-amount {
        color: #10b981;
    }
    
    .price-card-large .price-period {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    .price-card-large .features-list {
        list-style: none;
        padding: 0;
        margin: 2rem 0;
        text-align: left;
    }
    
    .price-card-large .features-list li {
        padding: 1rem 0;
        border-bottom: 1px solid #e5e7eb;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .price-card-large .features-list li:last-child {
        border-bottom: none;
    }
    
    .price-card-large .features-list li.positive::before {
        content: '✓';
        display: inline-block;
        width: 28px;
        height: 28px;
        background: #10b981;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-weight: 900;
        flex-shrink: 0;
    }
    
    .price-card-large .features-list li.negative::before {
        content: '✗';
        display: inline-block;
        width: 28px;
        height: 28px;
        background: #ef4444;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-weight: 900;
        flex-shrink: 0;
    }
    
    .vs-divider {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .vs-divider .vs-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 900;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    /* 数据可视化卡片 */
    .data-viz-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    }
    
    .data-viz-card .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .data-viz-card .card-icon {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .data-viz-card .card-header h3 {
        font-size: 1.8rem;
        color: #1f2937;
        margin: 0;
        border: none;
        padding: 0;
    }
    
    /* 对比表格 - 现代设计 */
    .modern-comparison-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 2rem 0;
        overflow: hidden;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .modern-comparison-table thead {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: white;
    }
    
    .modern-comparison-table thead th {
        padding: 1.5rem;
        font-size: 1.15rem;
        font-weight: 700;
        text-align: left;
        border: none;
    }
    
    .modern-comparison-table thead th:first-child {
        border-radius: 16px 0 0 0;
    }
    
    .modern-comparison-table thead th:last-child {
        border-radius: 0 16px 0 0;
    }
    
    .modern-comparison-table tbody tr {
        background: white;
        transition: all 0.3s;
    }
    
    .modern-comparison-table tbody tr:nth-child(even) {
        background: #f9fafb;
    }
    
    .modern-comparison-table tbody tr:hover {
        background: #f3f4f6;
        transform: scale(1.01);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .modern-comparison-table tbody td {
        padding: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        font-size: 1.05rem;
        vertical-align: middle;
    }
    
    .modern-comparison-table tbody tr:last-child td {
        border-bottom: none;
    }
    
    .modern-comparison-table tbody tr:last-child td:first-child {
        border-radius: 0 0 0 16px;
    }
    
    .modern-comparison-table tbody tr:last-child td:last-child {
        border-radius: 0 0 16px 0;
    }
    
    .modern-comparison-table .highlight-cell {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        font-weight: 700;
        color: #065f46;
    }
    
    /* 节省金额大数字展示 */
    .savings-showcase {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 24px;
        padding: 4rem;
        text-align: center;
        color: white;
        margin: 4rem 0;
        box-shadow: 0 12px 48px rgba(16, 185, 129, 0.3);
    }
    
    .savings-showcase h3 {
        font-size: 2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        border: none;
        color: white;
        padding: 0;
    }
    
    .savings-showcase .big-number {
        font-size: 5rem;
        font-weight: 900;
        margin: 2rem 0;
        line-height: 1;
        text-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .savings-showcase .subtitle {
        font-size: 1.5rem;
        opacity: 0.9;
        margin-top: 1rem;
    }
    
    /* 进度条对比 */
    .progress-comparison {
        margin: 3rem 0;
    }
    
    .progress-item {
        margin: 2rem 0;
    }
    
    .progress-item .label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .progress-bar-bg {
        background: #e5e7eb;
        height: 40px;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        padding-left: 1rem;
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        transition: width 1s ease-out;
    }
    
    .progress-bar-fill.winner {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
    }
    
    /* 场景卡片网格 */
    .scenario-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .scenario-card-modern {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    
    .scenario-card-modern:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 36px rgba(0,0,0,0.12);
    }
    
    .scenario-card-modern .scenario-number {
        display: inline-block;
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        text-align: center;
        line-height: 48px;
        font-size: 1.5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
    }
    
    .scenario-card-modern h4 {
        font-size: 1.5rem;
        color: #1f2937;
        margin-bottom: 1.5rem;
        border: none;
        padding: 0;
    }
    
    .scenario-card-modern .steps {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .scenario-card-modern .steps li {
        padding: 1rem 0;
        border-bottom: 1px dashed #e5e7eb;
        font-size: 1.05rem;
        line-height: 1.8;
        background: none;
        border-left: none;
        border-radius: 0;
        margin: 0;
    }
    
    .scenario-card-modern .steps li:last-child {
        border-bottom: none;
    }
    
    .scenario-card-modern .result {
        margin-top: 1.5rem;
        padding: 1.25rem;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-radius: 12px;
        font-weight: 700;
        color: #065f46;
        text-align: center;
        font-size: 1.15rem;
    }
    
    /* 响应式设计 */
    @media (max-width: 1024px) {
        .price-comparison-hero {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        .vs-divider {
            transform: rotate(90deg);
        }
        
        .scenario-grid {
            grid-template-columns: 1fr;
        }
    }
    
    @media (max-width: 768px) {
        .price-card-large .price-amount {
            font-size: 3rem;
        }
        
        .savings-showcase .big-number {
            font-size: 3rem;
        }
        
        .modern-comparison-table {
            font-size: 0.9rem;
        }
        
        .modern-comparison-table thead th,
        .modern-comparison-table tbody td {
            padding: 1rem 0.75rem;
        }
    }
"""

# 在现有CSS后添加新的设计CSS
# 查找</style>标签，在其前面插入
content = content.replace('</style>', new_design_css + '\n    </style>')

print("✅ 已添加全新的设计CSS系统")
print()

# 保存
with open('hsbc-vs-manual.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 70)
print("✅ 新设计CSS已添加！")
print("=" * 70)
print()
print("📊 新增设计组件：")
print("   1. ✅ 价格对比大卡片（price-comparison-hero）")
print("   2. ✅ 数据可视化卡片（data-viz-card）")
print("   3. ✅ 现代对比表格（modern-comparison-table）")
print("   4. ✅ 节省金额展示（savings-showcase）")
print("   5. ✅ 进度条对比（progress-comparison）")
print("   6. ✅ 场景卡片网格（scenario-grid）")
print()
print("💡 下一步：创建示例HTML，展示如何使用这些组件")
print("=" * 70)

