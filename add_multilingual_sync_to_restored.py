#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将数据互通功能集成到已恢复的英文、日文、韩文版本
"""

import re

def integrate_multilingual_sync_to_restored(file_path, lang):
    """将数据互通脚本集成到恢复后的文件"""
    
    print(f"\n🔄 处理 {lang.upper()} 版本...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经集成
    if 'multilingual-data-sync.js' in content:
        print(f"   ⏭️  已经集成过了")
        return False
    
    # 1. 在 </head> 标签前添加脚本引用
    script_tag = '\n    <!-- 🌐 多语言数据互通系统 -->\n    <script src="../multilingual-data-sync.js" defer></script>'
    
    if '</head>' in content:
        content = content.replace('</head>', script_tag + '\n</head>', 1)
        print(f"   ✅ 已添加脚本引用")
    else:
        print(f"   ⚠️  找不到 </head> 标签")
        return False
    
    # 2. 在用户菜单前添加语言切换器容器
    # 查找用户菜单的位置
    user_menu_pattern = r'(<div id="user-menu"[^>]*>)'
    
    if re.search(user_menu_pattern, content):
        # 在用户菜单前添加语言切换器
        language_switcher = r'<div id="language-switcher" style="margin-right: 1rem;"></div>\n                \1'
        content = re.sub(user_menu_pattern, language_switcher, content, count=1)
        print(f"   ✅ 已添加语言切换器容器")
    else:
        print(f"   ⚠️  找不到用户菜单位置")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    base_dir = "/Users/cavlinyeung/ai-bank-parser"
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🌐 重新集成数据互通功能                                             ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    files = {
        "en": f"{base_dir}/en/index.html",
        "jp": f"{base_dir}/jp/index.html",
        "kr": f"{base_dir}/kr/index.html"
    }
    
    success_count = 0
    for lang, file_path in files.items():
        if integrate_multilingual_sync_to_restored(file_path, lang):
            success_count += 1
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 数据互通功能集成完成！                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"\n✅ 成功集成 {success_count} 个文件")
    
    print("\n📚 数据互通系统功能：")
    print("   1. ✅ 所有语言版本使用相同的 Firebase 数据库")
    print("   2. ✅ 用户语言偏好保存到 Firebase 和 LocalStorage")
    print("   3. ✅ 在页面右上角添加语言切换器（用户菜单旁边）")
    print("   4. ✅ 切换语言时保持在相同页面")
    print("   5. ✅ 所有语言版本访问相同的用户数据、项目和文档")
    
    print("\n🔧 语言切换器 UI：")
    print("   🇨🇳 中文    ▼")
    print("   ├── 🇨🇳 中文 (Chinese)      ✓")
    print("   ├── 🇺🇸 English (English)")
    print("   ├── 🇯🇵 日本語 (Japanese)")
    print("   └── 🇰🇷 한국어 (Korean)")
    
    print("\n🧪 测试方法：")
    print("   1. 访问英文版：https://vaultcaddy.com/en/index.html")
    print("   2. 右上角应该显示语言切换器（在用户菜单旁边）")
    print("   3. 点击切换器选择其他语言，应该跳转到对应版本")
    print("   4. 在任何版本登录，切换语言后应该保持登录状态")
    print("   5. 创建的项目和数据在所有语言版本都能看到")

if __name__ == "__main__":
    main()

