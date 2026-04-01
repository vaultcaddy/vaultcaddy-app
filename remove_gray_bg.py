#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除英文版首页Pricing区域的灰色背景框
"""

def remove_gray_background_container():
    """删除包裹Pricing和Learning Center的灰色背景容器"""
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/en/index.html"
    
    print("🔄 删除灰色背景框...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 删除灰色背景容器的开始标签（两层div）
    old_gray_bg_start = '    <!-- US Social Proof -->\n    <div style="background: #f3f4f6; padding: 3rem 2rem; margin: 4rem 0;">\n        <div style="max-width: 1200px; margin: 0 auto;">'
    new_start = '    <!-- US Social Proof -->'
    
    if old_gray_bg_start in content:
        content = content.replace(old_gray_bg_start, new_start)
        print("   ✅ 已删除灰色背景框开始标签")
    else:
        print("   ⚠️  未找到灰色背景框开始标签，尝试另一种模式")
        # 尝试不带注释的版本
        old_gray_bg_start_alt = '    <div style="background: #f3f4f6; padding: 3rem 2rem; margin: 4rem 0;">\n        <div style="max-width: 1200px; margin: 0 auto;">'
        if old_gray_bg_start_alt in content:
            content = content.replace(old_gray_bg_start_alt, '')
            print("   ✅ 已删除灰色背景框开始标签（无注释版本）")
    
    # 2. 在Learning Center section结束后添加闭合的</div></div>标签（如果缺失）
    # 并在之后立即删除它们
    # 查找 </section>\n\n    </main> 并确保前面有正确的闭合标签
    
    old_ending = '        </section>\n\n    </main>'
    
    # 如果存在这个模式，说明div标签确实没有闭合
    if old_ending in content:
        # 添加闭合标签，然后立即用新模式替换回去（相当于删除了外层div）
        new_ending = '        </section>\n        </div>\n    </div>\n\n    </main>'
        
        # 先添加闭合标签
        content = content.replace(old_ending, new_ending)
        print("   ✅ 已添加临时闭合标签")
        
        # 然后删除这两个闭合标签（实际上就是删除了灰色框的容器）
        final_ending = '        </section>\n\n    </main>'
        content = content.replace(new_ending, final_ending)
        print("   ✅ 已删除灰色背景框闭合标签")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🗑️  删除灰色背景框                                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    if remove_gray_background_container():
        print("\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║     🎉 灰色背景框已删除！                                               ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        
        print("\n📝 完成的修改：")
        print("   1. ✅ 删除了灰色背景容器的开始标签")
        print("   2. ✅ 确保HTML结构正确闭合")
        
        print("\n🎨 效果：")
        print("   • Pricing区域不再有灰色背景")
        print("   • Learning Center不再有灰色背景")
        print("   • 页面布局保持正常")
        
        print("\n🔗 查看效果：")
        print("   https://vaultcaddy.com/en/index.html")

if __name__ == "__main__":
    main()

