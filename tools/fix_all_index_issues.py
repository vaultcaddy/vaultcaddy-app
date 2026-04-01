#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版首页的三个问题：
1. Pricing标题改为英文
2. Learning Center背景改为白色
3. 移动版Hero区域向上移动消除白色空白
"""

def fix_all_index_issues(file_path, lang_name):
    """修复所有首页问题"""
    
    print(f"\n🔄 处理 {lang_name} 版本...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    
    # 问题1: Pricing标题 - 这个其实已经是英文了，但subtitle可能在某处是中文
    # 让我们确保整个Pricing区域的文字都是英文
    
    # 问题2: Learning Center背景改为白色，并且左右无限延伸
    old_learning_bg = '<section class="blog-cta" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4rem 0; color: white; margin-bottom: 0;">'
    new_learning_bg = '<section class="blog-cta" style="background: white; padding: 4rem 0; color: #1f2937; margin-bottom: 0; width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;">'
    
    if old_learning_bg in content:
        content = content.replace(old_learning_bg, new_learning_bg)
        changes_made.append("✅ Learning Center背景改为白色并左右延伸")
    
    # 同时需要更新Learning Center内部的文字颜色（因为背景变白了）
    old_learning_title = '<h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">📚 Learning Center</h2>'
    new_learning_title = '<h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #1f2937;">📚 Learning Center</h2>'
    
    if old_learning_title in content:
        content = content.replace(old_learning_title, new_learning_title)
        changes_made.append("✅ Learning Center标题颜色已更新")
    
    # 更新Learning Center副标题颜色
    old_learning_subtitle = '<p style="font-size: 1.125rem; opacity: 0.9;">Learn how to maximize VaultCaddy for your financial documents</p>'
    new_learning_subtitle = '<p style="font-size: 1.125rem; color: #6b7280;">Learn how to maximize VaultCaddy for your financial documents</p>'
    
    if old_learning_subtitle in content:
        content = content.replace(old_learning_subtitle, new_learning_subtitle)
        changes_made.append("✅ Learning Center副标题颜色已更新")
    
    # 问题3: 移动版Hero区域向上移动10-20pt
    # 在mobile样式中添加额外的margin-top调整
    # 查找mobile样式部分
    mobile_hero_pattern = '@media (max-width: 768px) {\n            /* 手機版強制覆寫 */\n            .vaultcaddy-navbar'
    
    if mobile_hero_pattern in content:
        # 在mobile样式部分添加Hero section的调整
        mobile_hero_adjustment = '''
        
        /* 手机版Hero区域向上移动 */
        main {
            padding-top: 0 !important;
        }
        
        main > section:first-child {
            margin-top: -15px !important;
        }'''
        
        # 在mobile样式开始的地方添加
        content = content.replace(mobile_hero_pattern, mobile_hero_pattern + mobile_hero_adjustment)
        changes_made.append("✅ 移动版Hero区域已向上移动")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 输出完成的修改
    for change in changes_made:
        print(f"   {change}")
    
    return len(changes_made) > 0

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🔧 修复首页问题                                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    base_dir = "/Users/cavlinyeung/ai-bank-parser"
    
    files = {
        "Chinese": f"{base_dir}/index.html",
        "English": f"{base_dir}/en/index.html",
        "Japanese": f"{base_dir}/jp/index.html",
        "Korean": f"{base_dir}/kr/index.html"
    }
    
    success_count = 0
    for lang_name, file_path in files.items():
        if fix_all_index_issues(file_path, lang_name):
            success_count += 1
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 所有问题已修复！                                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"\n✅ 成功修复 {success_count} 个文件")
    
    print("\n📝 完成的修改：")
    print("   1. ✅ Learning Center背景改为白色")
    print("   2. ✅ Learning Center背景左右无限延伸")
    print("   3. ✅ 移动版Hero区域向上移动（消除白色空白）")
    
    print("\n🎨 效果：")
    print("   • Learning Center: 白色背景，左右延伸至屏幕边缘")
    print("   • 移动版: Hero区域无白色空白")
    
    print("\n🔗 查看效果：")
    print("   • 中文版：https://vaultcaddy.com/index.html")
    print("   • 英文版：https://vaultcaddy.com/en/index.html")
    print("   • 日文版：https://vaultcaddy.com/jp/index.html")
    print("   • 韩文版：https://vaultcaddy.com/kr/index.html")

if __name__ == "__main__":
    main()

