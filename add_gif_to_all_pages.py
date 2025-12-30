#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有非v3银行页面添加GIF演示
作用：在Hero Section后添加GIF演示，统一用户体验
"""

import os
import re
from pathlib import Path

# GIF 演示 HTML 代码（与v3相同）
GIF_DEMO_HTML = '''
    <!-- 🎬 Demo GIF Section -->
    <section style="padding: 80px 24px; background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);">
        <div style="max-width: 1200px; margin: 0 auto;">
            <!-- 标题 -->
            <div style="text-align: center; margin-bottom: 60px;">
                <div style="display: inline-block; background: rgba(99, 102, 241, 0.1); border: 2px solid rgba(99, 102, 241, 0.3); padding: 12px 32px; border-radius: 50px; margin-bottom: 24px;">
                    <span style="color: #6366f1; font-weight: 700; font-size: 14px; letter-spacing: 1px;">
                        🎬 LIVE DEMONSTRATION
                    </span>
                </div>
                <h2 style="font-size: 48px; font-weight: 800; color: white; margin-bottom: 20px; line-height: 1.2;">
                    See VaultCaddy in Action
                </h2>
                <p style="font-size: 20px; color: #94a3b8; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                    Watch how bank statements are converted to Excel in seconds with 98% accuracy
                </p>
            </div>
            
            <!-- GIF 容器 -->
            <div style="position: relative; max-width: 900px; margin: 0 auto; border-radius: 20px; overflow: hidden; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 100px rgba(99, 102, 241, 0.3); background: #000;">
                <!-- GIF 动图 - 自动播放循环 -->
                <img 
                    src="/video/chase-bank-demo.gif" 
                    alt="Bank Statement Conversion Demo"
                    style="width: 100%; height: auto; display: block; border-radius: 20px;"
                    loading="lazy"
                >
                
                <!-- 自动播放标签 -->
                <div style="position: absolute; top: 20px; right: 20px; background: rgba(16, 185, 129, 0.95); backdrop-filter: blur(10px); padding: 8px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);">
                    <div style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: pulse 1.5s ease-in-out infinite;"></div>
                    <span style="color: white; font-weight: 600; font-size: 13px;">AUTO PLAYING</span>
                </div>
            </div>
            
            <!-- GIF 下方特点 -->
            <div style="margin-top: 60px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 900px; margin-left: auto; margin-right: auto;">
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">⚡</div>
                    <div style="font-size: 32px; font-weight: 800; color: #10b981; margin-bottom: 8px;">3s</div>
                    <div style="font-size: 16px; color: #94a3b8;">Average Processing</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">🎯</div>
                    <div style="font-size: 32px; font-weight: 800; color: #6366f1; margin-bottom: 8px;">98%</div>
                    <div style="font-size: 16px; color: #94a3b8;">Accuracy Rate</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">💰</div>
                    <div style="font-size: 32px; font-weight: 800; color: #ec4899; margin-bottom: 8px;">$5.59</div>
                    <div style="font-size: 16px; color: #94a3b8;">Starting From/Month</div>
                </div>
            </div>
            
            <!-- CTA 按钮 -->
            <div style="text-align: center; margin-top: 50px;">
                <a href="/signup.html" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 20px 50px; border-radius: 50px; font-weight: 700; font-size: 18px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 15px 40px rgba(102, 126, 234, 0.5)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(102, 126, 234, 0.4)';">
                    🎁 Start Free Trial - 20 Pages Free
                </a>
                <p style="margin-top: 16px; color: #94a3b8; font-size: 14px;">No credit card required • Cancel anytime</p>
            </div>
        </div>
    </section>
    
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    @media (max-width: 768px) {
        h2 { font-size: 36px !important; }
        p { font-size: 16px !important; }
    }
    </style>

'''

def add_gif_to_page(file_path):
    """为单个页面添加GIF演示"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加过GIF
        if '<!-- 🎬 Demo GIF Section -->' in content or 'chase-bank-demo.gif' in content:
            return 'skip', '已存在GIF'
        
        # 多种插入策略
        inserted = False
        
        # 策略1: 查找第一个 </section> 后插入（通常是Hero section）
        pattern1 = r'(</section>\s*)\n(\s*<section)'
        if re.search(pattern1, content):
            new_content = re.sub(
                pattern1,
                r'\1' + GIF_DEMO_HTML + r'\2',
                content,
                count=1
            )
            inserted = True
        
        # 策略2: 如果没找到，尝试在第一个section后插入
        if not inserted:
            pattern2 = r'(</section>)'
            if re.search(pattern2, content):
                new_content = re.sub(
                    pattern2,
                    r'\1' + GIF_DEMO_HTML,
                    content,
                    count=1
                )
                inserted = True
        
        if not inserted:
            return 'error', '未找到插入位置'
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 'success', '已添加'
    
    except Exception as e:
        return 'error', str(e)

def main():
    print("🎬 开始为所有非v3页面添加GIF演示...")
    print("=" * 80)
    
    # 查找所有银行相关页面
    all_pages = []
    
    # 1. 根目录的页面
    root_patterns = [
        '*-statement-v2.html',
        '*-statement-simple.html',
        '*-statement.html'
    ]
    
    for pattern in root_patterns:
        pages = list(Path('.').glob(pattern))
        all_pages.extend(pages)
    
    # 2. 排除v3页面
    all_pages = [p for p in all_pages if 'v3.html' not in str(p)]
    
    # 3. 排除blog等目录
    all_pages = [p for p in all_pages if '/blog/' not in str(p) and '/en-' not in str(p)]
    
    print(f"📊 找到 {len(all_pages)} 个需要添加GIF的页面")
    print()
    
    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    
    # 处理每个页面
    for page_path in all_pages:
        status, message = add_gif_to_page(str(page_path))
        
        if status == 'success':
            print(f"✅ {page_path}")
            success_count += 1
        elif status == 'skip':
            # print(f"⏭️  {page_path} - {message}")
            skip_count += 1
        else:
            print(f"❌ {page_path} - {message}")
            error_count += 1
    
    print()
    print("=" * 80)
    print(f"🎉 根目录页面完成！")
    print(f"✅ 成功添加: {success_count}")
    print(f"⏭️  已存在跳过: {skip_count}")
    print(f"❌ 失败: {error_count}")
    print(f"📊 总计: {len(all_pages)}")
    print()
    print("📋 GIF 演示特点:")
    print("  ✅ 自动播放（无需点击）")
    print("  ✅ 循环播放（停留1秒）")
    print("  ✅ 100%兼容性")
    print("  ✅ AUTO PLAYING 标签")
    print("  ✅ 响应式设计")
    print("  ✅ 与v3页面相同的设计")

if __name__ == '__main__':
    main()

