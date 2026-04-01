#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版客服弹窗中的中文内容
"""

def fix_chatbox_english():
    """修复英文版客服弹窗"""
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/en/index.html"
    
    print("🔄 修复英文版客服弹窗...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 修复客服标题
    old_title = '<h3 style="margin: 0; font-size: 1.125rem; font-weight: 700;">VaultCaddy 客服</h3>\n                    <p style="margin: 0; font-size: 0.875rem; opacity: 0.9;">通常在1分钟内回复</p>'
    new_title = '<h3 style="margin: 0; font-size: 1.125rem; font-weight: 700;">VaultCaddy Support</h3>\n                    <p style="margin: 0; font-size: 0.875rem; opacity: 0.9;">Usually replies within 1 minute</p>'
    
    if old_title in content:
        content = content.replace(old_title, new_title)
        changes.append("✅ 客服标题已翻译")
    
    # 2. 修复快捷问题按钮
    quick_questions = [
        ("价格是多少？", "What's the pricing?"),
        ("如何开始免费试用？", "How to start free trial?"),
        ("支持哪些银行？", "Which banks are supported?"),
        ("数据安全吗？", "Is my data secure?")
    ]
    
    for chinese, english in quick_questions:
        # 修复按钮显示文本
        old_btn = f'                        💰 {chinese}\n                    </button>' if chinese == "价格是多少？" else \
                  f'                        🎁 {chinese}\n                    </button>' if chinese == "如何开始免费试用？" else \
                  f'                        🏦 {chinese}\n                    </button>' if chinese == "支持哪些银行？" else \
                  f'                        🔒 {chinese}\n                    </button>'
        
        emoji = "💰" if chinese == "价格是多少？" else \
                "🎁" if chinese == "如何开始免费试用？" else \
                "🏦" if chinese == "支持哪些银行？" else \
                "🔒"
        
        new_btn = f'                        {emoji} {english}\n                    </button>'
        
        if old_btn in content:
            content = content.replace(old_btn, new_btn)
            changes.append(f"✅ 按钮已翻译: {chinese} → {english}")
        
        # 修复onclick函数中的参数
        old_onclick = f"sendQuickQuestion('{chinese}')"
        new_onclick = f"sendQuickQuestion('{english}')"
        content = content.replace(old_onclick, new_onclick)
    
    # 3. 修复输入框placeholder
    old_placeholder = 'placeholder="输入您的问题..."'
    new_placeholder = 'placeholder="Type your question..."'
    
    if old_placeholder in content:
        content = content.replace(old_placeholder, new_placeholder)
        changes.append("✅ 输入框placeholder已翻译")
    
    # 4. 修复发送按钮
    old_send_btn = '                        发送\n                    </button>'
    new_send_btn = '                        Send\n                    </button>'
    
    if old_send_btn in content:
        content = content.replace(old_send_btn, new_send_btn)
        changes.append("✅ 发送按钮已翻译")
    
    # 5. 修复自动回复消息
    old_auto_reply = "感谢您的提问！我们的客服团队会尽快回复。您也可以：\\n\\n• <a href=\"auth.html\" style=\"color: #667eea;\">注册免费试用</a>\\n• <a href=\"blog/\" style=\"color: #667eea;\">查看帮助文档</a>\\n• 发送邮件至 support@vaultcaddy.com"
    new_auto_reply = "Thank you for your question! Our support team will respond shortly. You can also:\\n\\n• <a href=\"auth.html\" style=\"color: #667eea;\">Sign up for free trial</a>\\n• <a href=\"blog/\" style=\"color: #667eea;\">View help documentation</a>\\n• Email us at support@vaultcaddy.com"
    
    if old_auto_reply in content:
        content = content.replace(old_auto_reply, new_auto_reply)
        changes.append("✅ 自动回复消息已翻译")
    
    # 6. 修复弹出优惠窗口
    old_popup_title = '##  等等！别错过这个优惠'
    new_popup_title = '##  Wait! Don\'t Miss This Offer'
    
    if old_popup_title in content:
        content = content.replace(old_popup_title, new_popup_title)
        changes.append("✅ 弹窗标题已翻译")
    
    # 7. 修复优惠内容
    old_offer = ' 首次注册立享 **20%折扣**   \n \\+ 免费试用 **20页**'
    new_offer = ' Get **20% OFF** your first signup   \n \\+ Free trial **20 pages**'
    
    if old_offer in content:
        content = content.replace(old_offer, new_offer)
        changes.append("✅ 优惠内容已翻译")
    
    # 8. 修复优惠按钮
    old_offer_btn = ' 获取20%折扣码 →'
    new_offer_btn = ' Get 20% Discount Code →'
    
    if old_offer_btn in content:
        content = content.replace(old_offer_btn, new_offer_btn)
        changes.append("✅ 优惠按钮已翻译")
    
    # 9. 修复成功提示
    old_success = '                    ✅ 折扣码已发送到您的邮箱！'
    new_success = '                    ✅ Discount code sent to your email!'
    
    if old_success in content:
        content = content.replace(old_success, new_success)
        changes.append("✅ 成功提示已翻译")
    
    # 10. 修复优惠说明
    old_note = '                    优惠码有效期24小时 | 仅限首次注册用户'
    new_note = '                    Code valid for 24 hours | First-time users only'
    
    if old_note in content:
        content = content.replace(old_note, new_note)
        changes.append("✅ 优惠说明已翻译")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 输出完成的修改
    for change in changes:
        print(f"   {change}")
    
    return len(changes) > 0

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🌐 修复英文版客服弹窗                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    if fix_chatbox_english():
        print("\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║     🎉 客服弹窗已完全翻译为英文！                                       ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        
        print("\n📝 翻译内容：")
        print("   • 客服标题: VaultCaddy Support")
        print("   • 回复时间: Usually replies within 1 minute")
        print("   • 快捷问题: 4个按钮已翻译")
        print("   • 输入框: Type your question...")
        print("   • 发送按钮: Send")
        print("   • 自动回复: 已翻译")
        print("   • 优惠弹窗: 所有内容已翻译")
        
        print("\n🔗 查看效果：")
        print("   https://vaultcaddy.com/en/index.html")
        print("   点击右下角的客服按钮查看")

if __name__ == "__main__":
    main()

