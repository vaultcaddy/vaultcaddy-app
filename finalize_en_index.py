#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完成 en/index.html 的最终英文化修改
"""

import re

def finalize_en_index():
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 图2: 餐厅部分 - 改为美国常见餐厅和食品
    content = content.replace(
        '<span>Hong Kong Restaurant</span>',
        '<span>Restaurant</span>'
    )
    
    # 替换食品项目为美国常见的
    # Egg Tarts x5 $60 -> Burger x2 $18
    content = re.sub(
        r'<span style="color: #6b7280;">Egg Tarts x5</span>.*?<span style="font-weight: 600; color: #1f2937;">\$60</span>',
        '<span style="color: #6b7280;">Burger x2</span>\n                                            <span style="font-weight: 600; color: #1f2937;">$18</span>',
        content,
        flags=re.DOTALL
    )
    
    # Milk Tea x3 $54 -> Fries x3 $12
    content = re.sub(
        r'<span style="color: #6b7280;">Milk Tea x3</span>.*?<span style="font-weight: 600; color: #1f2937;">\$54</span>',
        '<span style="color: #6b7280;">Fries x3</span>\n                                            <span style="font-weight: 600; color: #1f2937;">$12</span>',
        content,
        flags=re.DOTALL
    )
    
    # Pineapple Buns x4 $32 -> Soft Drink x4 $8
    content = re.sub(
        r'<span style="color: #6b7280;">Pineapple Buns x4</span>.*?<span style="font-weight: 600; color: #1f2937;">\$32</span>',
        '<span style="color: #6b7280;">Soft Drink x4</span>\n                                            <span style="font-weight: 600; color: #1f2937;">$8</span>',
        content,
        flags=re.DOTALL
    )
    
    # 更新总价 $146 -> $38
    content = re.sub(
        r'(<div style="display: flex; justify-content: space-between; padding-top: 1rem; border-top: 2px solid #e5e7eb; margin-top: 1rem;">.*?<span style="font-weight: 700; font-size: 1\.25rem; color: #1f2937;">Total</span>.*?<span style="font-weight: 700; font-size: 1\.25rem; color: #667eea;">)\$146(</span>)',
        r'\1$38\2',
        content,
        flags=re.DOTALL
    )
    
    # 图3: 银行部分 - 改为美国常见银行
    content = content.replace(
        'Bank of China (Hong Kong)2025-03',
        'Bank of America 2025-03'
    )
    
    # Save 90% 輸入時間 -> Save 90% Input Time
    content = content.replace(
        'Save 90% 輸入時間',
        'Save 90% Input Time'
    )
    
    # 图4: Built for Hong Kong Accountants -> Built for Accountants
    content = content.replace(
        'Built for Hong Kong Accountants',
        'Built for Accountants'
    )
    
    # 图5: Ultra-Fast Processing 部分
    # 10s完成一份文檔 -> to complete one document
    content = content.replace(
        '<strong style="color: #10b981;">10s</strong>完成一份文檔',
        '<strong style="color: #10b981;">10s</strong> to complete one document'
    )
    
    # 90% 人工輸入時間 -> manual input time
    content = content.replace(
        '<strong style="color: #10b981;">90% 人工輸入</strong>時間',
        '<strong style="color: #10b981;">90%</strong> manual input time'
    )
    
    # HKD 0.5 -> USD 0.06
    content = content.replace(
        '<strong style="color: #f59e0b;">HKD 0.5</strong>',
        '<strong style="color: #f59e0b;">USD 0.06</strong>'
    )
    
    # 图6: 定价部分的中文
    content = content.replace(
        '與數千家企業一起, Save財務數據錄入的時間. 無隱藏費用, 隨時取消. ',
        'Join thousands of businesses saving time on financial data entry. No hidden fees, cancel anytime.'
    )
    
    # 图7: 用户评价部分
    reviews = {
        '"VaultCaddy 完全改變了我處理銀行對賬單的方式. 以往需要數小時的人工輸入, 現在只需幾分鐘, 且準確度遠勝其他工具. "':
            '"VaultCaddy completely transformed how I handle bank statements. What used to take hours of manual input now takes just minutes, with accuracy that far surpasses other tools."',
        
        '"我們事務所每月需處理數百張發票. 使用 VaultCaddy, 我們將處理時間減少了 70% 以上. 它首發、可靠, 幫我們團隊省去大量時間. "':
            '"Our firm processes hundreds of invoices monthly. With VaultCaddy, we\'ve reduced processing time by over 70%. It\'s fast, reliable, and saves our team tremendous amounts of time."',
        
        '"VaultCaddy 是我們唯一找到能安全擴展至數千份文件的解決方案. 銀行等級的合規功能讓我們能安心在多部門使用. "':
            '"VaultCaddy is the only solution we found that can securely scale to thousands of documents. Bank-grade compliance features let us confidently use it across multiple departments."',
        
        '"身為企業主, 我沒有時間手動整理收據與發票. VaultCaddy 自動擷取並分類所有資料, 讓記帳與報稅輕鬆許多. "':
            '"As a business owner, I don\'t have time to manually organize receipts and invoices. VaultCaddy automatically extracts and categorizes all data, making bookkeeping and tax filing much easier."',
        
        '"在稽核過程中, 一致性與準確度至關重要. VaultCaddy 提供乾淨、結構化的輸出, 讓合規檢查更快、更輕鬆, 我強烈推薦給稽核合規團隊. "':
            '"In the audit process, consistency and accuracy are paramount. VaultCaddy provides clean, structured output that makes compliance checks faster and easier. I highly recommend it to audit and compliance teams."',
        
        '"審閱申請人的銀行對帳單過去需要數小時. 使用 VaultCaddy, 我能在幾分鐘內分析大筆記錄, 讓貸款審批流程更快、更有效率. "':
            '"Reviewing applicants\' bank statements used to take hours. With VaultCaddy, I can analyze large volumes of records in minutes, making the loan approval process faster and more efficient."'
    }
    
    for chinese, english in reviews.items():
        content = content.replace(chinese, english)
    
    # 图8: 学习中心和 CTA 部分
    content = content.replace(
        '深入分析隱藏成本, 了解如何每月Save 40+ 小時, 將重複工作轉化為業務增長. ',
        'In-depth analysis of hidden costs, learn how to save 40+ hours per month and transform repetitive work into business growth.'
    )
    
    content = content.replace(
        '立即上傳您的第一份文檔, 體驗 AI 的Powerful Features',
        'Upload your first document now and experience the powerful features of AI'
    )
    
    # FAQ 部分 - 也更新银行名称
    content = content.replace(
        'VaultCaddy supports all major Hong Kong banks, including HSBC, Hang Seng Bank, Bank of China (Hong Kong), Standard Chartered, Bank of East Asia, Citibank, and more.',
        'VaultCaddy supports all major banks, including Bank of America, Chase, Wells Fargo, Citibank, US Bank, PNC, and more.'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/index.html 英文化修改完成！")
    print("\n主要修改：")
    print("✓ 餐厅名称：Hong Kong Restaurant → Restaurant")
    print("✓ 食品：Egg Tarts/Milk Tea/Pineapple Buns → Burger/Fries/Soft Drink")
    print("✓ 银行：Bank of China (Hong Kong) → Bank of America")
    print("✓ 标题：Built for Hong Kong Accountants → Built for Accountants")
    print("✓ 价格：HKD 0.5 → USD 0.06")
    print("✓ 所有中文内容翻译成英文")

if __name__ == '__main__':
    finalize_en_index()

