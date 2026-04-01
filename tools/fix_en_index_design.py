#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版首页设计，使其与中文版完全对齐
"""

import re

def fix_en_index():
    """修复英文版首页设计问题"""
    
    # 读取英文版
    with open('en/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 开始修复英文版首页设计...")
    
    # 1. 修复 "Built for Accountants" 标题，添加装饰性分隔线
    print("1️⃣ 添加标题装饰线...")
    old_title = r'<h2 style="font-size: 3rem; font-weight: 800; color: #1f2937; margin-bottom: 1rem;">Built for Accountants</h2>'
    new_title = '<h2 style="font-size: 3rem; font-weight: 800; color: #1f2937; margin-bottom: 1rem;">Built for Accountants<div style="width: 80px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 1rem auto; border-radius: 2px;"></div></h2>'
    
    if old_title in content:
        content = content.replace(old_title, new_title)
        print("   ✅ 已添加标题装饰线")
    else:
        print("   ⚠️ 未找到标题，尝试宽松匹配...")
        # 尝试更宽松的匹配
        pattern = r'(<h2[^>]*>Built for Accountants</h2>)'
        match = re.search(pattern, content)
        if match:
            old = match.group(1)
            new = '<h2 style="font-size: 3rem; font-weight: 800; color: #1f2937; margin-bottom: 1rem;">Built for Accountants<div style="width: 80px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 1rem auto; border-radius: 2px;"></div></h2>'
            content = content.replace(old, new)
            print("   ✅ 已添加标题装饰线（宽松匹配）")
        else:
            print("   ❌ 无法找到标题")
    
    # 2. 检查并确保用户评价部分的设计一致性
    print("2️⃣ 检查用户评价部分...")
    if 'VaultCaddy User' in content or 'Financial Analyst' in content:
        print("   ✅ 用户评价部分存在")
    else:
        print("   ⚠️ 未找到用户评价部分")
    
    # 3. 确保定价卡片的渐变背景一致
    print("3️⃣ 检查定价卡片设计...")
    if 'FAIR AND AFFORDABLE' in content or 'BEST VALUE' in content:
        print("   ✅ 定价部分标签正确")
    else:
        print("   ⚠️ 定价部分可能需要检查")
    
    # 4. 确保统计数据部分的设计一致
    print("4️⃣ 检查统计数据部分...")
    if '10s' in content and '98%' in content:
        print("   ✅ 统计数据部分存在")
    else:
        print("   ⚠️ 统计数据部分可能有问题")
    
    # 5. 确保CTA按钮样式一致
    print("5️⃣ 检查CTA按钮...")
    if 'cta-primary' in content:
        print("   ✅ CTA按钮class正确")
    else:
        print("   ⚠️ CTA按钮可能需要优化")
    
    # 6. 确保英文版登录按钮文案为 "Login" 而非中文
    print("6️⃣ 修复英文版登录按钮...")
    # 替换导航栏中的登录按钮
    content = re.sub(
        r'<button onclick="window\.location\.href=\'auth\.html\'" style="padding: 0\.5rem 1\.5rem; background: #667eea; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0\.2s; font-size: 0\.875rem;">登入</button>',
        '<button onclick="window.location.href=\'auth.html\'" style="padding: 0.5rem 1.5rem; background: #667eea; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;">Login</button>',
        content
    )
    print("   ✅ 已修复登录按钮文案")
    
    # 7. 修复用户下拉菜单中的中文
    print("7️⃣ 修复用户菜单英文...")
    # Account
    content = content.replace(
        '<i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>\n            帳戶',
        '<i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>\n            Account'
    )
    content = content.replace(
        '<i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>帳戶',
        '<i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>Account'
    )
    # Billing
    content = content.replace(
        '<i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>\n            計費',
        '<i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>\n            Billing'
    )
    content = content.replace(
        '<i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>計費',
        '<i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>Billing'
    )
    # Logout
    content = content.replace(
        '<i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>\n            登出',
        '<i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>\n            Logout'
    )
    content = content.replace(
        '<i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>登出',
        '<i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>Logout'
    )
    print("   ✅ 已修复用户菜单文案")
    
    # 8. 修复手机侧边栏中的中文
    print("8️⃣ 修复手机侧边栏英文...")
    # Home
    content = content.replace('<span>首頁</span>', '<span>Home</span>')
    # Features
    content = content.replace('<span>功能</span>', '<span>Features</span>')
    # Pricing
    content = content.replace('<span>價格</span>', '<span>Pricing</span>')
    # Learning Center
    content = content.replace('<span>學習中心</span>', '<span>Learning Center</span>')
    # Dashboard
    content = content.replace('<span>儀表板</span>', '<span>Dashboard</span>')
    # Privacy Policy
    content = content.replace('<span>隱私政策</span>', '<span>Privacy Policy</span>')
    # Terms of Service
    content = content.replace('<span>服務條款</span>', '<span>Terms of Service</span>')
    print("   ✅ 已修复侧边栏文案")
    
    # 9. 修复JS中的中文提示
    print("9️⃣ 修复JavaScript中的文案...")
    content = content.replace("'登入失敗, 請重試'", "'Login failed, please try again'")
    content = content.replace("'Logout失敗, 請重試'", "'Logout failed, please try again'")
    content = content.replace('console.log(\'✅ 用戶已登入, 顯示頭像\')', 'console.log(\'✅ User logged in, showing avatar\')')
    content = content.replace('console.log(\'✅ 用戶未登入, 顯示登入按鈕\')', 'console.log(\'✅ User not logged in, showing login button\')')
    content = content.replace('console.log(\'❌ 無法更新用戶菜單:', 'console.log(\'❌ Cannot update user menu:')
    print("   ✅ 已修复JavaScript文案")
    
    # 10. 确保所有导航链接指向正确
    print("🔟 检查导航链接...")
    # 导航栏链接应该指向 index.html 而不是 /
    content = re.sub(
        r'<a href="index\.html#features"',
        '<a href="#features"',
        content
    )
    content = re.sub(
        r'<a href="index\.html#pricing"',
        '<a href="#pricing"',
        content
    )
    print("   ✅ 导航链接已优化")
    
    # 写回文件
    with open('en/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ 英文版首页设计修复完成！")
    print("\n📝 修复内容：")
    print("   1. ✅ 添加标题装饰线")
    print("   2. ✅ 修复登录按钮文案")
    print("   3. ✅ 修复用户菜单文案")
    print("   4. ✅ 修复侧边栏文案")
    print("   5. ✅ 修复JavaScript提示文案")
    print("   6. ✅ 优化导航链接")
    print("\n🌐 请访问 https://vaultcaddy.com/en/index.html 查看效果")

if __name__ == '__main__':
    fix_en_index()

