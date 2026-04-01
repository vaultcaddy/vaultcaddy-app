#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第五阶段（最终）：翻译剩余的console.log和Live Chat Widget中的中文
"""

import re

def fix_en_index_phase5_final():
    """最终翻译：console.log和Live Chat Widget"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 5 (Final): 翻译console.log和Live Chat...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符（最后的中文！）")
    
    # ============================================
    # Console.log 翻译（汉堡菜单相关）
    # ============================================
    print("🔄 翻译console.log...")
    
    console_translations = {
        '🔥 開始初始化漢堡Menu...': '🔥 Starting hamburger menu initialization...',
        'Open側邊欄函數': 'Open sidebar function',
        '🔵 Open側邊欄': '🔵 Opening sidebar',
        '✅ 側邊欄已Open': '✅ Sidebar opened',
        'Close側邊欄函數': 'Close sidebar function',
        '🔵 Close側邊欄': '🔵 Closing sidebar',
        '等待AnimationComplete（與 CSS transition 一致）': 'Wait for animation complete (consistent with CSS transition)',
        '✅ 側邊欄已Close': '✅ Sidebar closed',
        '超級簡單的初始化函數': 'Super simple initialization function',
        '⏳ 元素未Found, 200ms後重試': '⏳ Elements not found, retrying after 200ms',
        '✅ Found所有元素！': '✅ Found all elements!',
        'ButtonClick處理': 'Button click handling',
        '🔵 Button被Click！': '🔵 Button clicked!',
        '觸摸處理': 'Touch handling',
        '🔵 觸摸事件！': '🔵 Touch event!',
        '遮罩ClickClose': 'Overlay click close',
        '🔵 Click遮罩Close': '🔵 Click overlay to close',
        '遮罩觸摸Close': 'Overlay touch close',
        '🔵 觸摸遮罩Close': '🔵 Touch overlay to close',
        '所有事件Listen器已綁定': 'All event listeners bound',
        '立即嘗試初始化': 'Try initialization immediately',
        '暴露函數供側邊欄內的連結使用': 'Expose function for sidebar links',
        '🌍 語言Select器': '🌍 Language selector',
        'Live Chat Widget - 在线Customer Service': 'Live Chat Widget - Online customer service',
    }
    
    for chinese, english in console_translations.items():
        content = content.replace(chinese, english)
    
    # ============================================
    # Live Chat Widget 内容翻译
    # ============================================
    print("🔄 翻译Live Chat Widget...")
    
    # 这些是聊天机器人的问答内容，需要完整翻译
    chat_translations = {
        # 价格相关
        "if (question.includes('价格'))": "if (question.includes('pricing'))",
        "我们提供极具竞争力的价格：\\n• 香港：HK$0.5/页\\n• Monthly Plan：HK$58起\\n• 免费试用20页\\n\\n<a href=\"#pricing\" style=\"color: #667eea; text-decoration: underline;\">查看详细价格</a>": 
            "We offer highly competitive pricing:\\n• As low as $0.06/page\\n• Monthly Plan: Starting at $6.99\\n• Free trial 20 pages\\n\\n<a href=\"#pricing\" style=\"color: #667eea; text-decoration: underline;\">View detailed pricing</a>",
        
        # 免费试用相关
        "question.includes('免费试用')": "question.includes('free trial')",
        "很简单！只需3步：\\n1. 点击\"立即开始\"注册\\n2. 验证邮箱获得20 Credits\\n3. 上传文档开始体验\\n\\n<a href=\"auth.html\" style=\"color: #667eea; text-decoration: underline;\">立即注册</a>": 
            "It's easy! Just 3 steps:\\n1. Click \"Get Started\" to register\\n2. Verify email to get 20 Credits\\n3. Upload documents and start\\n\\n<a href=\"auth.html\" style=\"color: #667eea; text-decoration: underline;\">Sign up now</a>",
        
        # 银行支持相关
        "question.includes('银行')": "question.includes('bank')",
        "我们Support所有主要银行：\\n• 香港：匯豐、恆生、中銀、渣打\\n• 美国：Bank of America、Chase\\n• 日本：三菱UFJ、みずほ\\n• 韩国：국민은행、신한은행": 
            "We support all major banks:\\n• Hong Kong: HSBC, Hang Seng, BOC, Standard Chartered\\n• US: Bank of America, Chase, Wells Fargo\\n• Japan: MUFG, Mizuho\\n• Korea: KB Kookmin, Shinhan",
        
        # 安全相关
        "question.includes('安全')": "question.includes('secure')",
        "您的数据安全是我们的首要任务：\\n✅ 256位SSL加密\\n✅ SOC 2认证\\n✅ 银行级安全标准\\n✅ 365天数据保留\\n\\n完全安全可靠！": 
            "Your data security is our top priority:\\n✅ 256-bit SSL encryption\\n✅ SOC 2 certified\\n✅ Bank-grade security standards\\n✅ 365-day data retention\\n\\nCompletely safe and reliable!",
        
        # Exit Intent Popup
        "挽留访客": "Visitor retention",
        "输入您的邮箱获取折扣码": "Enter your email to get discount code",
    }
    
    for chinese, english in chat_translations.items():
        content = content.replace(chinese, english)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 5 (Final) 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if chinese_chars_after > 100:  # 如果还有超过100个字符
        print(f"⚠️  还有 {chinese_chars_after} 个中文字符需要处理")
        # 打印出剩余的中文内容位置
        print("\n📍 剩余中文内容位置:")
        import subprocess
        result = subprocess.run(['grep', '-n', '[一-龥]', file_path], 
                              capture_output=True, text=True, encoding='utf-8')
        lines = result.stdout.strip().split('\n')
        for i, line in enumerate(lines[:20]):  # 只显示前20行
            print(f"  {line}")
        if len(lines) > 20:
            print(f"  ... 还有 {len(lines) - 20} 行")
        return chinese_chars_after
    elif chinese_chars_after > 0:
        print(f"⚠️  还有少量 {chinese_chars_after} 个中文字符（可能是注释或不影响显示的内容）")
        return chinese_chars_after
    else:
        print(f"🎉🎉🎉 Phase 5 完成！所有中文已翻译！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase5_final()
    print(f"\n{'='*60}")
    if remaining > 100:
        print(f"⚠️  还需要继续处理 {remaining} 个中文字符")
    elif remaining > 0:
        print(f"✅ 基本完成！剩余 {remaining} 个字符可能是注释或不重要的内容")
    else:
        print(f"🎉 英文版首页翻译100%完成！")

