#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复博客页面的三个问题：
1. 蓝色背景改为白色
2. 导航栏改为对应语言
3. 导航栏链接对应语言版本
"""

import os
import re
from pathlib import Path

# 多语言导航栏配置
NAVBAR_CONFIGS = {
    'en': {
        'home': 'Home',
        'features': 'Features',
        'pricing': 'Pricing',
        'learning': 'Learning Center',
        'dashboard': 'Dashboard',
        'login': 'Login',
        'home_link': '/en/index.html',
        'features_link': '/en/index.html#features',
        'pricing_link': '/en/index.html#pricing',
        'learning_link': '/en/blog/',
        'dashboard_link': '/dashboard.html',
        'login_link': '/auth.html'
    },
    'jp': {
        'home': 'ホーム',
        'features': '機能',
        'pricing': '価格',
        'learning': '学習センター',
        'dashboard': 'ダッシュボード',
        'login': 'ログイン',
        'home_link': '/jp/index.html',
        'features_link': '/jp/index.html#features',
        'pricing_link': '/jp/index.html#pricing',
        'learning_link': '/jp/blog/',
        'dashboard_link': '/dashboard.html',
        'login_link': '/auth.html'
    },
    'kr': {
        'home': '홈',
        'features': '기능',
        'pricing': '가격',
        'learning': '학습 센터',
        'dashboard': '대시보드',
        'login': '로그인',
        'home_link': '/kr/index.html',
        'features_link': '/kr/index.html#features',
        'pricing_link': '/kr/index.html#pricing',
        'learning_link': '/kr/blog/',
        'dashboard_link': '/dashboard.html',
        'login_link': '/auth.html'
    }
}

def generate_inline_navbar(lang):
    """生成内联导航栏HTML"""
    
    config = NAVBAR_CONFIGS[lang]
    
    navbar_html = f'''    <!-- 多语言导航栏 ({lang.upper()}) -->
    <nav style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;">
        <a href="{config['home_link']}" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600; font-size: 1.125rem;">
            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem;">V</div>
            <span>VaultCaddy</span>
        </a>
        
        <!-- Desktop Menu -->
        <div style="display: flex; gap: 2rem; align-items: center;" class="desktop-menu">
            <a href="{config['home_link']}" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">{config['home']}</a>
            <a href="{config['features_link']}" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">{config['features']}</a>
            <a href="{config['pricing_link']}" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">{config['pricing']}</a>
            <a href="{config['learning_link']}" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">{config['learning']}</a>
            <a href="{config['dashboard_link']}" style="padding: 0.5rem 1rem; background: #f3f4f6; color: #1f2937; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.3s;">{config['dashboard']}</a>
            <a href="{config['login_link']}" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.3s;">{config['login']}</a>
        </div>
        
        <!-- Mobile Menu Button -->
        <button id="mobile-menu-btn" style="display: none; background: none; border: none; cursor: pointer; padding: 0.5rem;" class="mobile-menu-btn">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
        </button>
    </nav>
    
    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu" style="display: none; position: fixed; top: 60px; left: 0; right: 0; bottom: 0; background: white; z-index: 999; padding: 2rem; flex-direction: column; gap: 1.5rem;">
        <a href="{config['home_link']}" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">{config['home']}</a>
        <a href="{config['features_link']}" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">{config['features']}</a>
        <a href="{config['pricing_link']}" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">{config['pricing']}</a>
        <a href="{config['learning_link']}" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">{config['learning']}</a>
        <a href="{config['dashboard_link']}" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">{config['dashboard']}</a>
        <a href="{config['login_link']}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 500;">{config['login']}</a>
    </div>
    
    <style>
        @media (max-width: 768px) {{
            .desktop-menu {{ display: none !important; }}
            .mobile-menu-btn {{ display: block !important; }}
        }}
    </style>
    
    <script>
        // Mobile menu toggle
        document.getElementById('mobile-menu-btn')?.addEventListener('click', function() {{
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileMenu.style.display === 'none' || mobileMenu.style.display === '') {{
                mobileMenu.style.display = 'flex';
            }} else {{
                mobileMenu.style.display = 'none';
            }}
        }});
    </script>'''
    
    return navbar_html

def fix_blog_index(file_path, lang):
    """修复博客索引页"""
    
    print(f"\n🔧 修复: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 修改背景色：蓝紫色渐变 → 白色
    if 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)' in content:
        content = content.replace(
            'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);',
            'background: #ffffff; border-bottom: 1px solid #e5e7eb;'
        )
        # 文字颜色也要改
        content = content.replace(
            '.blog-hero {\n            background: #ffffff; border-bottom: 1px solid #e5e7eb;\n            color: white;',
            '.blog-hero {\n            background: #ffffff; border-bottom: 1px solid #e5e7eb;\n            color: #1f2937;'
        )
        changes.append("✅ 背景色：蓝紫色 → 白色")
    
    # 2. 移除动态导航栏加载，替换为内联导航栏
    # 找到 <div id="navbar-container"></div> 并替换
    navbar_html = generate_inline_navbar(lang)
    
    if '<div id="navbar-container">' in content:
        content = re.sub(
            r'<div id="navbar-container">\s*</div>',
            navbar_html,
            content
        )
        changes.append(f"✅ 添加{lang.upper()}语言导航栏")
    
    # 3. 移除 load-unified-navbar.js 的引用
    if 'load-unified-navbar.js' in content:
        content = re.sub(
            r'<script src="[^"]*load-unified-navbar\.js">\s*</script>',
            '<!-- 已使用内联多语言导航栏 -->',
            content
        )
        changes.append("✅ 移除旧导航栏加载脚本")
    
    # 写回文件
    if changes:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        for change in changes:
            print(f"   {change}")
    else:
        print("   ℹ️  无需修改")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          修复博客页面（背景+导航栏+链接）                              ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    blog_pages = [
        ('en/blog/index.html', 'en'),
        ('jp/blog/index.html', 'jp'),
        ('kr/blog/index.html', 'kr'),
    ]
    
    total_changes = 0
    
    for file_path, lang in blog_pages:
        if os.path.exists(file_path):
            total_changes += fix_blog_index(file_path, lang)
        else:
            print(f"\n⚠️  文件不存在: {file_path}")
    
    # 总结
    print("\n" + "="*70)
    print("🎉 完成！")
    print("="*70)
    print(f"\n📊 统计：")
    print(f"   处理文件数: {len(blog_pages)}")
    print(f"   总修改项: {total_changes}")
    print(f"\n✨ 完成的修复：")
    print(f"   ✅ 背景色：蓝紫色渐变 → 白色")
    print(f"   ✅ 导航栏：改为对应语言")
    print(f"   ✅ 导航链接：指向对应语言版本")
    print(f"\n🌐 验证链接：")
    print(f"   https://vaultcaddy.com/en/blog/")
    print(f"   https://vaultcaddy.com/jp/blog/")
    print(f"   https://vaultcaddy.com/kr/blog/")

if __name__ == '__main__':
    main()

