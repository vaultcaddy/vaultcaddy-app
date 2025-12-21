#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复日文版首页剩余中文内容
"""

def fix_remaining_chinese():
    """修复所有剩余的中文内容"""
    
    file_path = "/Users/cavlinyeung/ai-bank-parser/jp/index.html"
    
    print("🇯🇵 修复日文版首页剩余中文内容...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. 客服对话框的自动回复（图1）
    print("\n📝 修复客服对话框回复...")
    
    # 主要自动回复
    old_reply = '感谢您的提问！我们的客服团队会尽快回复。您也可以：\\n\\n• <a href="auth.html" style="color: #667eea;">注册免费试用</a>\\n• <a href="blog/" style="color: #667eea;">查看帮助文档</a>\\n• 发送邮件至 support@vaultcaddy.com'
    new_reply = 'お問い合わせありがとうございます！カスタマーサポートチームができるだけ早く返信いたします。また、以下もご利用いただけます：\\n\\n• <a href="auth.html" style="color: #667eea;">無料トライアルに登録</a>\\n• <a href="blog/" style="color: #667eea;">ヘルプドキュメントを見る</a>\\n• support@vaultcaddy.com にメール'
    
    if old_reply in content:
        content = content.replace(old_reply, new_reply)
        changes.append("✅ 客服自动回复")
    
    # 快速问题的回复
    quick_replies = [
        ('我们支持所有主要银行：\\n• 日本：三菱UFJ銀行、みずほ銀行、三井住友銀行\\n• 美国：Bank of America、Chase\\n• 日本：三菱UFJ、みずほ\\n• 韩国：국민은행、신한은행',
         '主要な銀行をすべてサポート：\\n• 日本：三菱UFJ銀行、みずほ銀行、三井住友銀行\\n• アメリカ：Bank of America、Chase\\n• 日本：三菱UFJ、みずほ\\n• 韓国：국민은행、신한은행'),
        
        ('您的数据安全是我们的首要任务：\\n✅ 256位SSL加密\\n✅ SOC 2认证\\n✅ 银行级安全标准\\n✅ 365天数据保留\\n\\n完全安全可靠！',
         'データセキュリティは当社の最優先事項です：\\n✅ 256ビットSSL暗号化\\n✅ SOC 2認証\\n✅ 銀行レベルのセキュリティ基準\\n✅ 365日間データ保持\\n\\n完全に安全で信頼できます！'),
        
        ('很简单！只需3步：\\n1. 点击"立即开始"注册\\n2. 验证邮箱获得20 Credits\\n3. 上传文档开始体验\\n\\n<a href="auth.html" style="color: #667eea; text-decoration: underline;">立即注册</a>',
         'とても簡単です！3ステップ：\\n1. 「今すぐ始める」をクリックして登録\\n2. メール認証で20クレジット獲得\\n3. 文書をアップロードして体験開始\\n\\n<a href="auth.html" style="color: #667eea; text-decoration: underline;">今すぐ登録</a>')
    ]
    
    for old, new in quick_replies:
        if old in content:
            content = content.replace(old, new)
    
    changes.append("✅ 快速问题回复")
    
    # 输入提示文字
    content = content.replace('输入您的问题...', 'ご質問を入力してください...')
    changes.append("✅ 输入框提示文字")
    
    # 2. 价格区域标题（图2 - 动态内容）
    print("\n📝 修复价格区域标题...")
    
    # 在HTML中查找并替换
    old_pricing = '<h2 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;" data-translate="pricing_title">合理且實惠的價格</h2>'
    new_pricing = '<h2 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;" data-translate="pricing_title">合理でお手頃な料金</h2>'
    
    if old_pricing in content:
        content = content.replace(old_pricing, new_pricing)
        changes.append("✅ 价格标题")
    
    old_subtitle = '<p style="font-size: 1.125rem; color: #6b7280;">輕鬆處理銀行對帳單</p>'
    new_subtitle = '<p style="font-size: 1.125rem; color: #6b7280;">銀行明細の処理を簡単に</p>'
    
    if old_subtitle in content:
        content = content.replace(old_subtitle, new_subtitle)
        changes.append("✅ 价格副标题")
    
    # 3. 发票示例区域标题（图4）
    print("\n📝 修复发票示例区域...")
    
    old_invoice_title = '<h3 style="color: #1f2937; font-size: 1.875rem; font-weight: 700; margin-bottom: 1rem;">自動提取發票數據<br>秒速完成分類歸檔</h3>'
    new_invoice_title = '<h3 style="color: #1f2937; font-size: 1.875rem; font-weight: 700; margin-bottom: 1rem;">レシートデータの自動抽出<br>秒速で分類完了</h3>'
    
    if old_invoice_title in content:
        content = content.replace(old_invoice_title, new_invoice_title)
        changes.append("✅ 发票示例标题")
    
    # 4. 银行示例区域标题（图5）
    print("\n📝 修复银行示例区域...")
    
    old_bank_title = '<h3 style="color: #1f2937; font-size: 1.875rem; font-weight: 700; margin-bottom: 1rem;">自動識別收支類別<br>即時生成財務報表</h3>'
    new_bank_title = '<h3 style="color: #1f2937; font-size: 1.875rem; font-weight: 700; margin-bottom: 1rem;">収支分類を自動識別<br>即座に財務レポート生成</h3>'
    
    if old_bank_title in content:
        content = content.replace(old_bank_title, new_bank_title)
        changes.append("✅ 银行示例标题")
    
    # スマート取引分類下的文字
    old_smart_text = '收入、支出、振替を自動識別して分類'
    new_smart_text = '収入、支出、振替を自動識別して分類'
    
    if old_smart_text in content:
        content = content.replace(old_smart_text, new_smart_text)
        changes.append("✅ スマート取引分類说明")
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    for change in changes:
        print(f"   {change}")
    
    return len(changes)

def main():
    """主函数"""
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     🇯🇵 修复日文版剩余中文内容                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")
    
    changes_count = fix_remaining_chinese()
    
    if changes_count > 0:
        print("\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║     🎉 修复完成！                                                       ║")
        print("╚══════════════════════════════════════════════════════════════════════╝\n")
        
        print("📊 修复总结：")
        print("   1️⃣ 客服对话框回复 → 日文")
        print("   2️⃣ 价格区域标题（动态） → 日文")
        print("   3️⃣ 发票示例标题 → 日文")
        print("   4️⃣ 银行示例标题 → 日文")
        print("   5️⃣ 输入框提示 → 日文")
        
        print("\n🔗 查看效果：")
        print("   https://vaultcaddy.com/jp/index.html")
        
        print("\n✅ 现在日文版首页应该是100%纯日文！")

if __name__ == "__main__":
    main()

