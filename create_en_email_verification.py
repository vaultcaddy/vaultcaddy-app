#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为英文版Dashboard创建英文版的email验证提示
"""

import shutil

print("╔══════════════════════════════════════════════════════════════════════╗")
print("║          创建英文版Email验证模块                                        ║")
print("╚══════════════════════════════════════════════════════════════════════╝")
print()

# 读取现有的中文版
with open('email-verification-check.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换中文文本为英文
translations = {
    '立即驗證您的 email 即送 20 Credits 試用！': 'Verify your email now and get 20 Credits free trial!',
    '立即驗證': 'Verify Now',
    '請先驗證您的 email 才能使用此功能': 'Please verify your email to use this feature',
}

en_content = content
for zh, en in translations.items():
    en_content = en_content.replace(zh, en)

# 保存英文版
with open('email-verification-check-en.js', 'w', encoding='utf-8') as f:
    f.write(en_content)

print("✅ 创建英文版：email-verification-check-en.js")

# 更新Dashboard引用
with open('en/dashboard.html', 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

# 替换引用
old_script = '<script defer src="../email-verification-check.js"></script>'
new_script = '<script defer src="../email-verification-check-en.js"></script>'

if old_script in dashboard_content:
    dashboard_content = dashboard_content.replace(old_script, new_script)
    print("✅ 更新Dashboard引用为英文版")
else:
    print("⚠️  Dashboard中未找到email-verification-check.js引用")

# 保存Dashboard
with open('en/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

print()
print("="*70)
print("🎉 完成！")
print("="*70)
print()
print("📊 创建的文件：")
print("   ✅ email-verification-check-en.js（英文版验证模块）")
print()
print("🌐 验证：")
print("   未登录时访问：https://vaultcaddy.com/en/dashboard.html")
print("   应该看到英文提示：'Verify your email now and get 20 Credits free trial!'")








