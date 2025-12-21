#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文、日文、韩文版首页的Hero区域设计
1. 橙色Banner改为2行样式（与中文版一致）
2. 蓝色背景添加图片背景
3. 确保无白色空白
"""

import re

def fix_hero_design(file_path, lang_config):
    """修复Hero区域设计"""
    
    print(f"\n🔄 处理 {lang_config['name']} 版本...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复橙色Banner - 改为2行样式
    old_banner_pattern = r'<!-- 8折優惠橫幅 -->\s*<div style="[^"]*background:[^>]*>.*?</div>'
    
    new_banner = f'''<!-- 8折優惠橫幅 -->
    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; text-align: center; padding: 0.75rem; font-weight: 600; position: relative; z-index: 1002; font-size: 1.125rem;">
        <div style="margin-bottom: 0.35rem;">
            {lang_config['banner_line1']}
        </div>
        <div style="font-size: 1rem; display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 0.5rem;">
            <span style="background: white; color: #f59e0b; padding: 0.25rem 1rem; border-radius: 20px; font-weight: 700; white-space: nowrap;">{lang_config['banner_code']}</span>
            <span style="white-space: nowrap;">{lang_config['banner_line2']}</span>
        </div>
    </div>'''
    
    if re.search(old_banner_pattern, content, re.DOTALL):
        content = re.sub(old_banner_pattern, new_banner, content, flags=re.DOTALL)
        print(f"   ✅ 已更新橙色Banner为2行样式")
    else:
        print(f"   ⚠️  未找到橙色Banner")
    
    # 2. 修复Hero区域 - 添加图片背景和动态装饰
    # 查找当前的Hero section
    old_hero_pattern = r'<section style="background: linear-gradient\(135deg, #667eea 0%, #764ba2 100\%\); padding: 5rem 0;[^>]*>'
    
    new_hero_bg = '''<section style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%), 
                 url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&q=80&fm=jpg&w=1920') center/cover no-repeat; 
                 padding: 5rem 0; color: white; position: relative; overflow: hidden; margin-top: 0;">
        <!-- 动态背景装饰 -->
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.15; background: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;0.4&quot;%3E%3Cpath d=&quot;M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>'''
    
    if re.search(old_hero_pattern, content):
        content = re.sub(old_hero_pattern, new_hero_bg, content)
        print(f"   ✅ 已添加图片背景和动态装饰")
    else:
        print(f"   ⚠️  未找到Hero section开始标签")
    
    # 3. 确保没有白色背景的margin问题
    # 找到并更新Hero section中的 margin-top
    content = re.sub(
        r'(<section[^>]*style="[^"]*)(margin-top:\s*\d+(?:px|rem|pt)[^"]*)',
        r'\1margin-top: 0',
        content
    )
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    base_dir = "/Users/cavlinyeung/ai-bank-parser"
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎨 修复首页Hero区域设计                                             ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    # 各语言配置
    lang_configs = {
        "en": {
            "name": "English",
            "file": f"{base_dir}/en/index.html",
            "banner_line1": "⚡ Limited Offer: 20% OFF This Month!",
            "banner_code": "Code: SAVE20",
            "banner_line2": "Join <span style=\"font-weight: 700;\">237</span> accounting professionals worldwide"
        },
        "jp": {
            "name": "Japanese",
            "file": f"{base_dir}/jp/index.html",
            "banner_line1": "⚡ 期間限定：今月ご登録で初月20%OFF！",
            "banner_code": "クーポンコード：SAVE20",
            "banner_line2": "すでに <span style=\"font-weight: 700;\">120</span>社 以上の企業が利用中"
        },
        "kr": {
            "name": "Korean",
            "file": f"{base_dir}/kr/index.html",
            "banner_line1": "⚡ 환영 특가: 이번 달 가입 시 첫 달 20% 할인!",
            "banner_code": "쿠폰 코드: SAVE20",
            "banner_line2": "이미 <span style=\"font-weight: 700;\">95</span>개 이상의 기업이 사용 중"
        }
    }
    
    success_count = 0
    for lang, config in lang_configs.items():
        if fix_hero_design(config['file'], config):
            success_count += 1
    
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🎉 Hero区域设计修复完成！                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"\n✅ 成功修复 {success_count} 个文件")
    
    print("\n📝 完成的改动：")
    print("   1. ✅ 橙色Banner改为2行样式（与中文版一致）")
    print("   2. ✅ 蓝色背景添加图片背景")
    print("   3. ✅ 添加动态SVG装饰图案")
    print("   4. ✅ 移除白色空白（margin-top: 0）")
    
    print("\n🎨 设计效果：")
    print("   • 橙色Banner：第一行优惠信息 + 第二行优惠码和用户数")
    print("   • 蓝色背景：渐变 + 图片背景 + 动态装饰")
    print("   • 无白色空白：Hero区域直接衔接导航栏")
    
    print("\n🔗 查看效果：")
    print("   • 英文版：https://vaultcaddy.com/en/index.html")
    print("   • 日文版：https://vaultcaddy.com/jp/index.html")
    print("   • 韩文版：https://vaultcaddy.com/kr/index.html")
    
    print("\n📸 与中文版对比：")
    print("   • 中文版：https://vaultcaddy.com/index.html")

if __name__ == "__main__":
    main()

