#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复多语言 Dashboard 的 JavaScript 路径问题
问题：en/jp/kr 的 dashboard 在子目录中，但引用的是相对路径，导致找不到 JS 文件
解决：将所有相对路径改为绝对路径（从根目录开始）
"""

def fix_dashboard_paths(file_path, lang_name):
    """修复单个 dashboard 文件的路径"""
    
    print(f"\n🔧 修复 {lang_name} Dashboard 路径...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 需要修复的相对路径 JS/CSS 文件
    path_fixes = [
        ('src="config.js"', 'src="../config.js"'),
        ('src="translations.js', 'src="../translations.js'),
        ('src="navbar-component.js', 'src="../navbar-component.js'),
        ('src="sidebar-component.js', 'src="../sidebar-component.js'),
        ('src="firebase-config.js', 'src="../firebase-config.js'),
        ('src="simple-auth.js', 'src="../simple-auth.js'),
        ('src="user-profile-manager.js', 'src="../user-profile-manager.js'),
        ('src="simple-data-manager.js', 'src="../simple-data-manager.js'),
        ('src="email-verification-check.js', 'src="../email-verification-check.js'),
        ('src="navbar-interactions.js', 'src="../navbar-interactions.js'),
        ('src="disable-console-safe.js', 'src="../disable-console-safe.js'),
        ('href="styles.css"', 'href="../styles.css"'),
        ('href="dashboard.css"', 'href="../dashboard.css"'),
    ]
    
    for old, new in path_fixes:
        if old in content:
            content = content.replace(old, new)
            changes.append(f"   ✅ {old} → {new}")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    for change in changes:
        print(change)
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🔧 修复多语言 Dashboard JavaScript 路径问题                         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    dashboards = [
        ("/Users/cavlinyeung/ai-bank-parser/en/dashboard.html", "英文"),
        ("/Users/cavlinyeung/ai-bank-parser/jp/dashboard.html", "日文"),
        ("/Users/cavlinyeung/ai-bank-parser/kr/dashboard.html", "韩文"),
    ]
    
    total_changes = 0
    
    for file_path, lang_name in dashboards:
        changes = fix_dashboard_paths(file_path, lang_name)
        total_changes += changes
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 修复完成！                                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    print("📊 修复总结：")
    print(f"   • 修复了 {total_changes} 个路径引用")
    print("   • 所有 JS/CSS 文件现在使用正确的相对路径（../）")
    
    print("\n🔍 问题原因：")
    print("   • Dashboard 文件在子目录中（en/, jp/, kr/）")
    print("   • 但使用的是相对路径（config.js）")
    print("   • 浏览器尝试从子目录加载文件（en/config.js）❌")
    print("   • 应该从根目录加载（../config.js）✅")
    
    print("\n✅ 现在测试：")
    print("   1. 在中文版登录")
    print("   2. 访问 https://vaultcaddy.com/en/dashboard.html")
    print("   3. 访问 https://vaultcaddy.com/jp/dashboard.html")
    print("   4. 访问 https://vaultcaddy.com/kr/dashboard.html")
    print("   5. 应该能成功进入并看到相同的数据！")
    
    print("\n💡 数据互通说明：")
    print("   • 所有版本使用同一个 Firebase 项目")
    print("   • 认证状态跨语言共享")
    print("   • 用户数据、项目、文档完全同步")

if __name__ == "__main__":
    main()

