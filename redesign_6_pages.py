#!/usr/bin/env python3
"""
重新设计6个页面，采用HSBC完整设计标准
"""

import os
import re

# 页面配置
PAGES_CONFIG = {
    'chase-bank-statement-v2.html': {
        'type': 'bank',
        'name': 'Chase Bank',
        'full_name': 'Chase Bank USA',
        'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Chase_logo.svg/200px-Chase_logo.svg.png',
        'brand_color_start': '#0047BB',
        'brand_color_end': '#005EB8',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'US',
        'businesses': '500+',
        'hero_tagline': '🎁 20% OFF Limited Time - New Users Get 20 Free Credits',
        'hero_title': 'Chase Bank Statement<br>AI Converter',
        'hero_description': 'Convert Chase PDF to Excel/QuickBooks/Xero in 3 seconds<br>98% Accuracy • All Formats • Bank-Level Security',
        'stats_count': '500+'
    },
    'restaurant-accounting-v2.html': {
        'type': 'industry',
        'name': 'Restaurant',
        'full_name': 'Restaurant Accounting',
        'logo_icon': '🍽️',
        'brand_color_start': '#f59e0b',
        'brand_color_end': '#d97706',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'Global',
        'businesses': '150+',
        'hero_tagline': '🎁 20% OFF for Restaurants - Start Free Trial Today',
        'hero_title': 'Restaurant Accounting<br>AI Automation',
        'hero_description': 'Automate bank reconciliation for restaurants in seconds<br>98% Accuracy • Multi-Location • Real-Time Reports',
        'stats_count': '150+'
    },
    'vaultcaddy-vs-manual-v2.html': {
        'type': 'comparison',
        'name': 'VaultCaddy vs Manual',
        'full_name': 'VaultCaddy vs Manual Processing',
        'logo_icon': '⚡',
        'brand_color_start': '#8b5cf6',
        'brand_color_end': '#6d28d9',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'Global',
        'businesses': '500+',
        'hero_tagline': '⚡ 95% Faster Than Manual Data Entry',
        'hero_title': 'VaultCaddy vs<br>Manual Processing',
        'hero_description': 'Save 20 hours per month with AI automation<br>98% Accuracy • Zero Training • Instant Setup',
        'stats_count': '500+'
    },
    'us-bank-statement-v2.html': {
        'type': 'bank',
        'name': 'US Bank',
        'full_name': 'US Bank USA',
        'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/US_Bank_logo.svg/200px-US_Bank_logo.svg.png',
        'brand_color_start': '#002B5C',
        'brand_color_end': '#003D7C',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'US',
        'businesses': '500+',
        'hero_tagline': '🎁 20% OFF Limited Time - New Users Get 20 Free Credits',
        'hero_title': 'US Bank Statement<br>AI Converter',
        'hero_description': 'Convert US Bank PDF to Excel/QuickBooks/Xero in 3 seconds<br>98% Accuracy • All Formats • Bank-Level Security',
        'stats_count': '500+'
    },
    'vaultcaddy-vs-nanonets-v2.html': {
        'type': 'comparison',
        'name': 'VaultCaddy vs Nanonets',
        'full_name': 'VaultCaddy vs Nanonets',
        'logo_icon': '🆚',
        'brand_color_start': '#3b82f6',
        'brand_color_end': '#2563eb',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'Global',
        'businesses': '500+',
        'hero_tagline': '💰 10x More Affordable Than Nanonets',
        'hero_title': 'VaultCaddy vs<br>Nanonets',
        'hero_description': 'Better pricing, faster processing, higher accuracy<br>98% Accuracy • $5.59/month vs $299/month • No Training Required',
        'stats_count': '500+'
    },
    'ecommerce-accounting-v2.html': {
        'type': 'industry',
        'name': 'E-commerce',
        'full_name': 'E-commerce Accounting',
        'logo_icon': '🛒',
        'brand_color_start': '#10b981',
        'brand_color_end': '#059669',
        'currency': 'USD',
        'monthly_price': '$5.59',
        'annual_price': '$67.08',
        'extra_page': '$0.06',
        'market': 'Global',
        'businesses': '200+',
        'hero_tagline': '🎁 20% OFF for E-commerce - Start Free Trial Today',
        'hero_title': 'E-commerce Accounting<br>AI Automation',
        'hero_description': 'Automate bank reconciliation for online stores in seconds<br>98% Accuracy • Multi-Currency • Real-Time Sync',
        'stats_count': '200+'
    },
}

def generate_hero_section(config):
    """生成Hero Section"""
    logo_html = ''
    if 'logo_url' in config:
        logo_html = f'''
                                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, {config['brand_color_start']} 0%, {config['brand_color_end']} 100%); border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-xl);">
                                    <img src="{config['logo_url']}" alt="{config['name']}" style="width: 50px; height: auto;">
                                </div>'''
    else:
        logo_html = f'''
                                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, {config['brand_color_start']} 0%, {config['brand_color_end']} 100%); border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--font-bold); font-size: var(--text-2xl);">
                                    {config['logo_icon']}
                                </div>'''
    
    return f'''    <!-- ============================================================
         HERO SECTION - 渐变背景 + 插图
         ============================================================ -->
    
    <section style="background: linear-gradient(135deg, {config['brand_color_start']} 0%, {config['brand_color_end']} 100%); color: var(--white); padding: var(--space-20) 0; position: relative; overflow: hidden;">
        <!-- 背景装饰 -->
        <div style="position: absolute; top: 0; right: 0; width: 50%; height: 100%; background: url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2240%22 fill=%22rgba(255,255,255,0.05)%22/></svg>'); opacity: 0.5;"></div>
        
        <div class="container" style="position: relative; z-index: 1; max-width: 1200px; margin: 0 auto; padding: 0 var(--space-6);">
            <div class="grid grid-cols-2" style="display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: var(--space-12);">
                <!-- 左侧内容 -->
                <div class="hero-content">
                    <span class="badge" style="background: rgba(255,255,255,0.2); color: var(--white); margin-bottom: var(--space-4); font-size: var(--text-sm); display: inline-block; padding: var(--space-2) var(--space-4); border-radius: var(--radius-full);">
                        {config['hero_tagline']}
                    </span>
                    
                    <h1 style="color: var(--white); font-size: var(--text-5xl); margin-bottom: var(--space-4); line-height: var(--leading-tight); font-weight: var(--font-black);">
                        {config['hero_title']}
                    </h1>
                    
                    <p class="lead" style="color: rgba(255,255,255,0.95); margin-bottom: var(--space-8); font-size: var(--text-xl); line-height: var(--leading-relaxed);">
                        {config['hero_description']}
                    </p>
                    
                    <div class="flex gap-4" style="display: flex; gap: var(--space-4); margin-bottom: var(--space-8); flex-wrap: wrap;">
                        <button class="btn btn-lg" style="background: var(--white); color: {config['brand_color_start']}; padding: var(--space-4) var(--space-8); border-radius: var(--radius-full); font-weight: var(--font-bold); font-size: var(--text-lg); border: none; cursor: pointer; box-shadow: var(--shadow-xl);" onclick="window.location.href='../firstproject.html'">
                            <i class="fas fa-rocket" style="margin-right: var(--space-2);"></i>
                            Start Free Trial
                        </button>
                        <button class="btn btn-lg" style="background: transparent; border: 2px solid var(--white); color: var(--white); padding: var(--space-4) var(--space-8); border-radius: var(--radius-full); font-weight: var(--font-bold); font-size: var(--text-lg); cursor: pointer;" onclick="window.scrollTo({{top: document.getElementById('pricing').offsetTop, behavior: 'smooth'}})">
                            <i class="fas fa-dollar-sign" style="margin-right: var(--space-2);"></i>
                            View Pricing
                        </button>
                    </div>
                    
                    <!-- 信任指标 -->
                    <div class="flex gap-6" style="display: flex; gap: var(--space-6); font-size: var(--text-sm); flex-wrap: wrap; opacity: 0.95;">
                        <span style="display: flex; align-items: center;">
                            <i class="fas fa-check-circle" style="margin-right: var(--space-2); color: #22c55e;"></i>
                            SOC2 Certified
                        </span>
                        <span style="display: flex; align-items: center;">
                            <i class="fas fa-shield-alt" style="margin-right: var(--space-2); color: #22c55e;"></i>
                            Bank-Level Security
                        </span>
                        <span style="display: flex; align-items: center;">
                            <i class="fas fa-users" style="margin-right: var(--space-2); color: #22c55e;"></i>
                            {config['businesses']} Businesses
                        </span>
                        <span style="display: flex; align-items: center;">
                            <i class="fas fa-star" style="margin-right: var(--space-2); color: #fbbf24;"></i>
                            4.9/5.0 Rating
                        </span>
                    </div>
                </div>
                
                <!-- 右侧视觉 -->
                <div class="hero-visual hidden-mobile">
                    <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); border-radius: var(--radius-2xl); padding: var(--space-12); box-shadow: var(--shadow-2xl); border: 1px solid rgba(255,255,255,0.2);">
                        <!-- 模拟银行对账单界面 -->
                        <div style="background: var(--white); border-radius: var(--radius-xl); padding: var(--space-8); color: var(--gray-900);">
                            <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-6);">
{logo_html}
                                <div>
                                    <div style="font-weight: var(--font-bold); font-size: var(--text-lg);">{config['name']}</div>
                                    <div style="color: var(--gray-500); font-size: var(--text-sm);">{'Business Account' if config['type'] == 'bank' else config['type'].title()}</div>
                                </div>
                            </div>
                            
                            <div style="border-top: 2px solid var(--gray-200); padding-top: var(--space-4); margin-bottom: var(--space-4);">
                                <div style="display: flex; justify-content: space-between; margin-bottom: var(--space-3); font-size: var(--text-sm);">
                                    <span style="color: var(--gray-600);">Opening Balance</span>
                                    <span style="font-weight: var(--font-semibold);">{config['currency']}{'$' if config['currency'] != 'USD' else ''}125,680.50</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: var(--space-3); font-size: var(--text-sm);">
                                    <span style="color: var(--gray-600);">Total Income</span>
                                    <span style="color: var(--success); font-weight: var(--font-semibold);">+{config['currency']}{'$' if config['currency'] != 'USD' else ''}89,500.00</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: var(--space-3); font-size: var(--text-sm);">
                                    <span style="color: var(--gray-600);">Total Expenses</span>
                                    <span style="color: var(--error); font-weight: var(--font-semibold);">-{config['currency']}{'$' if config['currency'] != 'USD' else ''}45,230.25</span>
                                </div>
                            </div>
                            
                            <div style="border-top: 2px solid var(--gray-200); padding-top: var(--space-4);">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-weight: var(--font-bold); font-size: var(--text-lg);">Closing Balance</span>
                                    <span style="font-weight: var(--font-bold); font-size: var(--text-2xl); color: {config['brand_color_start']};">{config['currency']}{'$' if config['currency'] != 'USD' else ''}169,950.25</span>
                                </div>
                            </div>
                            
                            <!-- AI处理标识 -->
                            <div style="margin-top: var(--space-6); padding: var(--space-4); background: rgba(59, 130, 246, 0.1); border-radius: var(--radius-lg); text-align: center;">
                                <i class="fas fa-robot" style="font-size: var(--text-3xl); color: {config['brand_color_start']}; margin-bottom: var(--space-2);"></i>
                                <div style="font-weight: var(--font-semibold); color: {config['brand_color_start']};">AI Processed • 3 Seconds</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ============================================================
         STATS SECTION - 数据展示
         ============================================================ -->
    
    <section class="stats-section" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: var(--white); padding: var(--space-16) 0;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 var(--space-6);">
            <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-8);">
                <div class="stat-card" style="text-align: center; animation: floatUp 0.6s ease-out;">
                    <div class="stat-icon" style="font-size: 48px; margin-bottom: var(--space-3);">⚡</div>
                    <div class="stat-number" style="font-size: var(--text-5xl); font-weight: var(--font-bold); margin-bottom: var(--space-2);">3 sec</div>
                    <div class="stat-label" style="font-size: var(--text-base); opacity: 0.9;">Average Processing</div>
                </div>
                
                <div class="stat-card" style="text-align: center; animation: floatUp 0.6s ease-out 0.1s;">
                    <div class="stat-icon" style="font-size: 48px; margin-bottom: var(--space-3);">🎯</div>
                    <div class="stat-number" style="font-size: var(--text-5xl); font-weight: var(--font-bold); margin-bottom: var(--space-2);">98%</div>
                    <div class="stat-label" style="font-size: var(--text-base); opacity: 0.9;">Accuracy Rate</div>
                </div>
                
                <div class="stat-card" style="text-align: center; animation: floatUp 0.6s ease-out 0.2s;">
                    <div class="stat-icon" style="font-size: 48px; margin-bottom: var(--space-3);">🏢</div>
                    <div class="stat-number" style="font-size: var(--text-5xl); font-weight: var(--font-bold); margin-bottom: var(--space-2);">{config['stats_count']}</div>
                    <div class="stat-label" style="font-size: var(--text-base); opacity: 0.9;">Businesses Using</div>
                </div>
                
                <div class="stat-card" style="text-align: center; animation: floatUp 0.6s ease-out 0.3s;">
                    <div class="stat-icon" style="font-size: 48px; margin-bottom: var(--space-3);">💰</div>
                    <div class="stat-number" style="font-size: var(--text-5xl); font-weight: var(--font-bold); margin-bottom: var(--space-2);">{config['monthly_price']}</div>
                    <div class="stat-label" style="font-size: var(--text-base); opacity: 0.9);">per month (annual)</div>
                </div>
            </div>
        </div>
    </section>

    <style>
        @keyframes floatUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @media (max-width: 768px) {{
            .grid.grid-cols-2 {{
                grid-template-columns: 1fr !important;
            }}
            .hidden-mobile {{
                display: none !important;
            }}
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr) !important;
            }}
            h1 {{
                font-size: var(--text-3xl) !important;
            }}
        }}
    </style>'''

def redesign_page(filename):
    """重新设计单个页面"""
    if filename not in PAGES_CONFIG:
        print(f"跳过: {filename}")
        return False
    
    print(f"🎨 重新设计: {filename}")
    config = PAGES_CONFIG[filename]
    
    filepath = filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到<body>标签
    body_match = re.search(r'<body[^>]*>', content, re.DOTALL)
    if not body_match:
        print(f"   ❌ 未找到<body>标签")
        return False
    
    body_start = body_match.end()
    
    # 生成新的body内容
    new_hero = generate_hero_section(config)
    
    # 保留现有的其他sections（pricing, FAQ等），只替换Hero和Stats
    # 找到第一个section结束后的内容
    remaining_content_match = re.search(r'</section>\s*</section>', content[body_start:], re.DOTALL)
    if remaining_content_match:
        # 找到前两个section之后的内容
        remaining_start = body_start + remaining_content_match.end()
        remaining_content = content[remaining_start:]
    else:
        # 如果找不到，保留所有body之后的内容
        remaining_content = content[body_start:]
    
    # 构建新内容
    new_content = content[:body_start] + '\n' + new_hero + '\n' + remaining_content
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✅ 重新设计完成: {config['name']}")
    return True

def main():
    print("🎨 开始重新设计6个页面\n")
    print("=" * 60)
    
    redesigned = 0
    for filename in PAGES_CONFIG.keys():
        if redesign_page(filename):
            redesigned += 1
        print()
    
    print("=" * 60)
    print(f"\n✅ 重新设计完成: {redesigned}/6 个页面")
    print("\n🎉 所有页面已升级到HSBC完整设计标准！")

if __name__ == '__main__':
    main()

