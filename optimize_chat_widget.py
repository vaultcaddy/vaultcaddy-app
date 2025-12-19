#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化客服小部件
1. 删除contact-widget.js引用
2. 将客服小部件内容改为繁体中文
"""

import re

def optimize_chat_widget():
    filepath = '/Users/cavlinyeung/ai-bank-parser/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 70)
    print("🔧 优化客服小部件")
    print("=" * 70)
    print()
    
    # 1. 删除contact-widget.js引用
    print("📝 步骤 1：删除contact-widget.js引用...")
    content = re.sub(
        r'<script src="contact-widget\.js\?v=\d+"></script>\s*\n',
        '',
        content
    )
    print("  ✅ 已删除contact-widget.js引用")
    print()
    
    # 2. 将客服小部件内容改为繁体中文
    print("📝 步骤 2：将客服小部件内容改为繁体中文...")
    
    # 简体到繁体的映射
    translations = {
        # 注释
        '<!-- Live Chat Widget - 在线客服 -->': '<!-- Live Chat Widget - 線上客服 -->',
        
        # 标题和副标题
        'VaultCaddy 客服': 'VaultCaddy 客服',  # 保持不变
        '通常在1分钟内回复': '通常在1分鐘內回覆',
        
        # 欢迎消息
        '👋 您好！我是VaultCaddy客服助手。': '👋 您好！我是VaultCaddy客服助手。',
        '我可以帮您：': '我可以幫您：',
        '了解产品功能': '了解產品功能',
        '查看定价方案': '查看定價方案',
        '解答技术问题': '解答技術問題',
        '有什么可以帮您的吗？': '有什麼可以幫您的嗎？',
        
        # 快速问题按钮
        '价格是多少？': '價格是多少？',
        '如何开始免费试用？': '如何開始免費試用？',
        '支持哪些银行？': '支持哪些銀行？',
        '数据安全吗？': '數據安全嗎？',
        
        # 输入框和按钮
        '输入您的问题...': '輸入您的問題...',
        '发送': '發送',
        
        # 回复内容 - 价格
        '我们提供极具竞争力的价格：': '我們提供極具競爭力的價格：',
        '• 香港：HK\\$0\\.5/页': '• 香港：HK$0.5/頁',
        '• 月付方案：HK\\$58起': '• 月付方案：HK$58起',
        '• 免费试用20页': '• 免費試用20頁',
        '查看详细价格': '查看詳細價格',
        
        # 回复内容 - 免费试用
        '很简单！只需3步：': '很簡單！只需3步：',
        '点击"立即开始"注册': '點擊「立即開始」註冊',
        '验证邮箱获得20 Credits': '驗證郵箱獲得20 Credits',
        '上传文档开始体验': '上傳文檔開始體驗',
        '立即注册': '立即註冊',
        
        # 回复内容 - 银行支持
        '我们支持所有主要银行：': '我們支持所有主要銀行：',
        '• 香港：匯豐、恆生、中銀、渣打': '• 香港：匯豐、恆生、中銀、渣打',
        '• 美国：Bank of America、Chase': '• 美國：Bank of America、Chase',
        '• 日本：三菱UFJ、みずほ': '• 日本：三菱UFJ、みずほ',
        '• 韩国：국민은행、신한은행': '• 韓國：국민은행、신한은행',
        
        # 回复内容 - 数据安全
        '您的数据安全是我们的首要任务：': '您的數據安全是我們的首要任務：',
        '✅ 256位SSL加密': '✅ 256位SSL加密',
        '✅ SOC 2认证': '✅ SOC 2認證',
        '✅ 银行级安全标准': '✅ 銀行級安全標準',
        '✅ 365天数据保留': '✅ 365天數據保留',
        '完全安全可靠！': '完全安全可靠！',
        
        # 默认回复
        '感谢您的提问！我们的客服团队会尽快回复。您也可以：': '感謝您的提問！我們的客服團隊會盡快回覆。您也可以：',
        '注册免费试用': '註冊免費試用',
        '查看帮助文档': '查看幫助文檔',
        '发送邮件至 support@vaultcaddy.com': '發送郵件至 support@vaultcaddy.com',
    }
    
    # 执行替换
    for old_text, new_text in translations.items():
        content = content.replace(old_text, new_text)
    
    # 特殊处理JavaScript代码中的繁体转换
    # 处理question.includes检查
    content = content.replace("question.includes('价格')", "question.includes('價格')")
    content = content.replace("question.includes('免费试用')", "question.includes('免費試用')")
    content = content.replace("question.includes('银行')", "question.includes('銀行')")
    content = content.replace("question.includes('安全')", "question.includes('安全')")
    
    print("  ✅ 已将客服小部件内容改为繁体中文")
    print()
    
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 70)
    print("✅ 优化完成！")
    print("=" * 70)
    print()
    print("完成的修改：")
    print("  1. ✅ 已删除contact-widget.js引用（图2的联繫我们表单）")
    print("  2. ✅ 已将客服小部件内容改为繁体中文（图1优化）")
    print()
    print("现在只有一个客服小部件，内容已全部改为繁体中文！")

if __name__ == '__main__':
    optimize_chat_widget()

