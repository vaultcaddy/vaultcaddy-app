#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改英文版首页的标题和客服文案
"""

def fix_english_index():
    """修复英文版首页"""
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/en/index.html"
    
    print("🔄 修改英文版首页...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修改Hero区域的主标题
    old_title = '<span>Free Bank Statement OCR & PDF to QuickBooks Converter</span><br>\n                        <span>98% Accuracy</span> | <span style="background: linear-gradient(120deg, #ffd700, #ffed4e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4.5rem;">From $0.06/<span>page</span></span>'
    
    new_title = '<span>VaultCaddy - Bank Statement & Receipt AI Processing Expert | QuickBooks Integration</span><br>\n                        <span>From</span> <span style="background: linear-gradient(120deg, #ffd700, #ffed4e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4.5rem;">$0.06/<span>page</span></span>'
    
    if old_title in content:
        content = content.replace(old_title, new_title)
        print("   ✅ 已更新Hero标题")
    else:
        print("   ⚠️  未找到Hero标题")
    
    # 2. 修改Pricing部分的标题 - "Fair and Affordable Pricing"
    old_pricing_title = '<p style="font-size: 0.875rem; font-weight: 600; color: #8b5cf6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem; text-align: center;" data-translate="pricing_badge">Fair and Affordable Pricing</p>\n                <h2 data-translate="pricing_title" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Easy Bank Statement Processing</h2>'
    
    new_pricing_title = '<p style="font-size: 0.875rem; font-weight: 600; color: #8b5cf6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem; text-align: center;" data-translate="pricing_badge">FAIR AND AFFORDABLE PRICING</p>\n                <h2 data-translate="pricing_title" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Easy Bank Statement Processing</h2>'
    
    if old_pricing_title in content:
        content = content.replace(old_pricing_title, new_pricing_title)
        print("   ✅ 已更新Pricing标题")
    
    # 3. 修改客服弹窗的中文内容为英文
    old_chatbox_content = '''                        <p style="margin: 0; color: #1f2937; font-size: 0.9375rem;">
                            👋 您好！我是VaultCaddy客服助手。
                            <br><br>
                            我可以帮您：
                            <br>• 了解产品功能
                            <br>• 查看定价方案
                            <br>• 解答技术问题
                            <br><br>
                            有什么可以帮您的吗？
                        </p>'''
    
    new_chatbox_content = '''                        <p style="margin: 0; color: #1f2937; font-size: 0.9375rem;">
                            👋 Hi! I'm VaultCaddy Support Assistant.
                            <br><br>
                            I can help you with:
                            <br>• Product features
                            <br>• Pricing plans
                            <br>• Technical questions
                            <br><br>
                            How can I assist you today?
                        </p>'''
    
    if old_chatbox_content in content:
        content = content.replace(old_chatbox_content, new_chatbox_content)
        print("   ✅ 已更新客服弹窗内容")
    
    # 4. 修改客服弹窗的快捷问题按钮
    old_quick_buttons = '''                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        💰 价格是多少？
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🎁 如何开始免费试用？
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🏦 支持哪些银行？
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🔒 数据安全吗？
                    </button>'''
    
    new_quick_buttons = '''                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        💰 What's the pricing?
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🎁 How to start free trial?
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🏦 Which banks supported?
                    </button>
                    <button style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: white; color: #1f2937; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 0.5rem;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">
                        🔒 Is my data secure?
                    </button>'''
    
    if old_quick_buttons in content:
        content = content.replace(old_quick_buttons, new_quick_buttons)
        print("   ✅ 已更新客服快捷按钮")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     📝 修改英文版首页内容                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    if fix_english_index():
        print("\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║     🎉 英文版首页修改完成！                                             ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        
        print("\n📝 完成的修改：")
        print("   1. ✅ Hero标题改为: VaultCaddy - Bank Statement & Receipt AI Processing Expert")
        print("   2. ✅ Pricing标题改为大写: FAIR AND AFFORDABLE PRICING")
        print("   3. ✅ 客服弹窗内容改为英文")
        print("   4. ✅ 客服快捷按钮改为英文")
        
        print("\n🔗 查看效果：")
        print("   https://vaultcaddy.com/en/index.html")

if __name__ == "__main__":
    main()

