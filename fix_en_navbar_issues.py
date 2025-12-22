#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版博客和Dashboard的导航栏问题
1. 博客导航栏：删除Home，Dashboard不要框样式，修正Dashboard链接
2. Dashboard侧边栏：转为英文
"""

import re

print("╔══════════════════════════════════════════════════════════════════════╗")
print("║          修复英文版导航栏和侧边栏                                       ║")
print("╚══════════════════════════════════════════════════════════════════════╝")
print()

changes = []

# 1. 修复博客页面导航栏
print("1️⃣  修复博客页面导航栏...")
blog_file = 'en/blog/index.html'

with open(blog_file, 'r', encoding='utf-8') as f:
    blog_content = f.read()

# 删除Home链接（桌面版）
old_desktop_nav = '''        <div style="display: flex; gap: 2rem; align-items: center;" class="desktop-menu">
            <a href="/en/index.html" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Home</a>
            <a href="/en/index.html#features" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Features</a>
            <a href="/en/index.html#pricing" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Pricing</a>
            <a href="/en/blog/" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Learning Center</a>
            <a href="/dashboard.html" style="padding: 0.5rem 1rem; background: #f3f4f6; color: #1f2937; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.3s;">Dashboard</a>
            <a href="/auth.html" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.3s;">Login</a>
        </div>'''

new_desktop_nav = '''        <div style="display: flex; gap: 2rem; align-items: center;" class="desktop-menu">
            <a href="/en/index.html#features" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Features</a>
            <a href="/en/index.html#pricing" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Pricing</a>
            <a href="/en/blog/" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Learning Center</a>
            <a href="/en/dashboard.html" style="color: #4b5563; text-decoration: none; font-weight: 500; transition: color 0.3s;">Dashboard</a>
            <a href="/auth.html" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.3s;">Login</a>
        </div>'''

if old_desktop_nav in blog_content:
    blog_content = blog_content.replace(old_desktop_nav, new_desktop_nav)
    changes.append("✅ 博客桌面导航栏：删除Home，移除Dashboard框样式，修正链接")

# 删除Home链接（移动版）
old_mobile_nav = '''    <div id="mobile-menu" style="display: none; position: fixed; top: 60px; left: 0; right: 0; bottom: 0; background: white; z-index: 999; padding: 2rem; flex-direction: column; gap: 1.5rem;">
        <a href="/en/index.html" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Home</a>
        <a href="/en/index.html#features" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Features</a>
        <a href="/en/index.html#pricing" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Pricing</a>
        <a href="/en/blog/" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Learning Center</a>
        <a href="/dashboard.html" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Dashboard</a>
        <a href="/auth.html" style="display: inline-block; padding: 0.75rem 1.5rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 500;">Login</a>
    </div>'''

new_mobile_nav = '''    <div id="mobile-menu" style="display: none; position: fixed; top: 60px; left: 0; right: 0; bottom: 0; background: white; z-index: 999; padding: 2rem; flex-direction: column; gap: 1.5rem;">
        <a href="/en/index.html#features" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Features</a>
        <a href="/en/index.html#pricing" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Pricing</a>
        <a href="/en/blog/" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Learning Center</a>
        <a href="/en/dashboard.html" style="color: #1f2937; text-decoration: none; font-size: 1.125rem; font-weight: 500;">Dashboard</a>
        <a href="/auth.html" style="display: inline-block; padding: 0.75rem 1.5rem; background: #8b5cf6; color: white; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 500;">Login</a>
    </div>'''

if old_mobile_nav in blog_content:
    blog_content = blog_content.replace(old_mobile_nav, new_mobile_nav)
    changes.append("✅ 博客移动导航栏：删除Home，修正Dashboard链接")

with open(blog_file, 'w', encoding='utf-8') as f:
    f.write(blog_content)

print("   ✅ 博客导航栏修复完成")

# 2. 修复Dashboard页面侧边栏
print("\n2️⃣  修复Dashboard页面侧边栏...")
dashboard_file = 'en/dashboard.html'

with open(dashboard_file, 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

# 修复移动侧边栏中文
replacements = {
    '<span>首頁</span>': '<span>Home</span>',
}

for old, new in replacements.items():
    if old in dashboard_content:
        dashboard_content = dashboard_content.replace(old, new)
        changes.append(f"✅ Dashboard侧边栏：{old} → {new}")

with open(dashboard_file, 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

print("   ✅ Dashboard侧边栏修复完成")

# 总结
print("\n" + "="*70)
print("🎉 完成！")
print("="*70)
print()

if changes:
    print("📊 修复项目：")
    for change in changes:
        print(f"   {change}")
else:
    print("ℹ️  没有需要修复的项目")

print()
print("🌐 验证链接：")
print("   https://vaultcaddy.com/en/blog/")
print("   https://vaultcaddy.com/en/dashboard.html")
print()
print("✨ 修复完成！")


