#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强 HSBC 优化页面的手机版视觉效果
添加渐变、动画、图标、卡片效果等
"""

from pathlib import Path

# 读取现有文件
html_file = Path("/Users/cavlinyeung/ai-bank-parser/hsbc-bank-statement-optimized.html")
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 增强的手机版CSS
enhanced_mobile_css = """
        /* ==================== 手机版视觉增强 ==================== */
        @media (max-width: 768px) {
            /* Hero 区域增强 */
            .hero {
                padding: 60px 16px;
                position: relative;
                overflow: hidden;
            }
            
            /* 添加动态背景装饰 */
            .hero::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -20%;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                border-radius: 50%;
                animation: float 6s ease-in-out infinite;
            }
            
            .hero::after {
                content: '';
                position: absolute;
                bottom: -30%;
                left: -10%;
                width: 250px;
                height: 250px;
                background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
                border-radius: 50%;
                animation: float 8s ease-in-out infinite reverse;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .hero h1 {
                font-size: 32px;
                line-height: 1.3;
                position: relative;
                z-index: 1;
            }
            
            .hero-subtitle {
                font-size: 18px;
                position: relative;
                z-index: 1;
            }
            
            .hero-badge {
                animation: pulse 2s ease-in-out infinite;
                position: relative;
                z-index: 1;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .cta-button {
                width: 100%;
                max-width: 400px;
                padding: 16px 32px;
                font-size: 16px;
                min-height: 54px;
                position: relative;
                z-index: 1;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            }
            
            /* 内容区域增强 */
            .content-section {
                padding: 48px 16px;
            }
            
            .section-title {
                font-size: 28px;
                margin-bottom: 16px;
                position: relative;
                padding-left: 16px;
            }
            
            /* 为标题添加彩色边框 */
            .section-title::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px;
            }
            
            .section-subtitle {
                font-size: 16px;
                margin-bottom: 40px;
            }
            
            .content-text {
                font-size: 16px;
                line-height: 1.8;
                margin-bottom: 20px;
            }
            
            /* 图片增强 */
            .content-image {
                border-radius: 12px;
                margin: 40px auto;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
                transition: transform 0.3s ease;
            }
            
            /* 特性卡片增强 */
            .features-grid {
                grid-template-columns: 1fr;
                gap: 20px;
                margin: 40px 0;
            }
            
            .feature-card {
                padding: 24px;
                background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
                border-left: 4px solid #667eea;
                position: relative;
                overflow: hidden;
            }
            
            .feature-card::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200px;
                height: 200px;
                background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
                border-radius: 50%;
            }
            
            .feature-icon {
                font-size: 36px;
                filter: drop-shadow(0 4px 6px rgba(102, 126, 234, 0.3));
            }
            
            .feature-title {
                font-size: 20px;
                color: #667eea;
            }
            
            .feature-description {
                font-size: 15px;
            }
            
            /* 统计数据增强 */
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 32px;
                margin: 40px 0;
            }
            
            .stats-grid > div {
                background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
                padding: 24px;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .stats-grid > div:active {
                transform: translateY(-4px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            }
            
            .stat-number {
                font-size: 48px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .stat-label {
                font-size: 16px;
                color: #6b7280;
                font-weight: 600;
            }
            
            /* FAQ 增强 */
            .faq-item {
                padding: 24px;
                margin-bottom: 16px;
                border-left: 4px solid #10b981;
                background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
                transition: transform 0.3s ease;
            }
            
            .faq-item:active {
                transform: translateX(4px);
            }
            
            .faq-question {
                font-size: 18px;
                color: #10b981;
                position: relative;
                padding-left: 28px;
            }
            
            .faq-question::before {
                content: '💡';
                position: absolute;
                left: 0;
                top: 0;
            }
            
            .faq-answer {
                font-size: 15px;
                padding-left: 28px;
            }
            
            /* 客户评价增强 */
            .testimonial {
                padding: 24px;
                background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
                border-left: 4px solid #3b82f6;
                margin-bottom: 24px;
            }
            
            .testimonial-text {
                font-size: 16px;
                line-height: 1.8;
                font-style: italic;
                position: relative;
                padding-left: 20px;
            }
            
            .testimonial-text::before {
                content: '"';
                position: absolute;
                left: 0;
                top: -10px;
                font-size: 48px;
                color: #3b82f6;
                opacity: 0.3;
                font-family: Georgia, serif;
            }
            
            .author-avatar {
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 20px;
            }
            
            .author-name {
                font-size: 16px;
                font-weight: 700;
                color: #1f2937;
            }
            
            .author-title {
                font-size: 13px;
                color: #6b7280;
            }
            
            /* CTA 区域增强 */
            .cta-section {
                padding: 60px 16px;
                position: relative;
                overflow: hidden;
            }
            
            .cta-section::before {
                content: '';
                position: absolute;
                top: -100px;
                left: -100px;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                border-radius: 50%;
            }
            
            .cta-section h2 {
                font-size: 28px;
                position: relative;
                z-index: 1;
            }
            
            .cta-section p {
                font-size: 16px;
                position: relative;
                z-index: 1;
            }
            
            /* 添加内容淡入动画 */
            .content-text {
                animation: fadeInUp 0.6s ease-out;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        }
        
        @media (max-width: 480px) {
            .hero h1 {
                font-size: 26px;
            }
            
            .section-title {
                font-size: 24px;
            }
            
            .stat-number {
                font-size: 40px;
            }
        }
"""

# 找到现有的手机版CSS位置并替换
import re

# 查找 @media (max-width: 768px) 的位置
pattern = r'(@media \(max-width: 768px\) \{[^}]*\}.*?@media \(max-width: 480px\) \{[^}]*\})'
match = re.search(pattern, content, re.DOTALL)

if match:
    # 替换现有的手机版CSS
    content = content.replace(match.group(0), enhanced_mobile_css.strip())
else:
    # 如果找不到，在 </style> 前添加
    content = content.replace('</style>', enhanced_mobile_css + '\n    </style>')

# 保存增强后的文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 手机版视觉效果已增强！")
print()
print("增强内容：")
print("  ✅ Hero区域动态背景装饰")
print("  ✅ 脉冲动画效果")
print("  ✅ 彩色标题边框")
print("  ✅ 渐变卡片背景")
print("  ✅ 悬停/点击动画")
print("  ✅ 统计数据渐变色")
print("  ✅ FAQ问答图标")
print("  ✅ 评价引号装饰")
print("  ✅ 淡入动画效果")
print()
print("请刷新页面查看效果！")

