#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇰 专门修复香港版本的语言混合问题
"""

import os
import re
from pathlib import Path

def fix_hk_file(file_path):
    """修复单个香港文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 香港版本：所有英文替换为繁体中文
        replacements = {
            # 标题和大文本
            'Convert': '轉換',
            'Statements in Seconds': '對帳單，只需幾秒',
            'Made Simple': '變得簡單',
            'Automate': '自動化',
            'Save 10+ hours per week': '每週節省10+小時',
            'on manual data entry': '在手動數據輸入上',
            
            # 按钮和CTA
            'Start Free Trial': '開始免費試用',
            'See How It Works': '查看運作方式',
            'FREE: Try 20 pages': '免費試用20頁',
            '無需信用卡': '無需信用卡',
            'No credit card required': '無需信用卡',
            'AUTO PLAYING': '自動播放',
            'LIVE DEMONSTRATION': '實時演示',
            
            # 统计数字标签
            'Hours Saved/Week': '每週節省小時',
            'Accuracy': '準確率',
            'Processing': '處理',
            'Per Month': '每月',
            
            # 定价部分
            'MOST POPULAR': '最受歡迎',
            'Monthly Plan': '月付方案',
            'Annual Plan': '年付方案',
            'per month': '每月',
            'per additional page': '每頁額外費用',
            'pages included': '頁面包含',
            'All export formats': '所有匯出格式',
            'Email Support': '電郵支援',
            'Priority email support': '優先電郵支援',
            '24h auto-delete': '24小時自動刪除',
            'Cancel anytime': '隨時取消',
            'Start': '開始',
            'Billed annually': '按年計費',
            
            # 视频和演示部分
            'Watch how': '觀看如何',
            'are processed in seconds': '在幾秒內處理',
            'with 98% accuracy': '準確率達98%',
            'Average processing time': '平均處理時間',
            'Starting From/Month': '起價/月',
            
            # 常见问题和挑战
            'Common': '常見',
            'Challenges': '挑戰',
            'How VaultCaddy Solves These Problems': 'VaultCaddy如何解決這些問題',
            'Specific Features': '專屬功能',
            'Built for the unique needs': '專為獨特需求而設計',
            'Built for': '專為',
            'designed specifically for': '專為設計',
            
            # 行业特定功能
            'Supplier Invoice Processing': '供應商發票處理',
            'Delivery Platform Reports': '配送平台報告',
            'POS System Export': 'POS系統匯出',
            'Cash Flow Tracking': '現金流追蹤',
            'Cost Analysis': '成本分析',
            'Fund Accounting': '基金會計',
            'Grant Expense Tracking': '資助費用追蹤',
            'Donor Reporting': '捐贈者報告',
            'Manual tracking': '手動追蹤',
            'weekly': '每週',
            'Ensuring': '確保',
            'expenses comply with': '費用符合',
            'grant requirements': '資助要求',
            'Creating': '創建',
            'custom reports': '自訂報告',
            'for different donor requirements': '針對不同捐贈者要求',
            'Gathering data': '收集數據',
            'for annual filing': '用於年度申報',
            
            # 解决方案文本
            'AI-powered automation': 'AI驅動的自動化',
            'Automated': '自動化',
            'AI assigns transactions': 'AI分配交易',
            'to correct funds': '到正確的基金',
            'Real-time': '實時',
            'budget vs. actual by grant': '預算與實際按資助',
            'One-click': '一鍵',
            'donor impact statements': '捐贈者影響聲明',
            'Always prepared': '隨時準備',
            
            # 功能描述
            'Automatic item-level extraction': '自動項目級提取',
            'with prices and quantities': '包含價格和數量',
            'Extract orders, fees': '提取訂單、費用',
            'and net deposits automatically': '並自動淨存款',
            'Reconcile sales, tips': '對帳銷售、小費',
            'and payment methods automatically': '並自動支付方式',
            'Track alcohol costs': '追蹤酒精成本',
            'separately for liquor license compliance': '單獨用於酒牌合規',
            'Daily cash register reconciliation': '每日收銀機對帳',
            'Track cash deposits': '追蹤現金存款',
            'petty cash': '零用現金',
            'and employee meal deductions automatically': '並自動員工餐扣除',
            'Food cost percentage calculations': '食品成本百分比計算',
            'Compare actual costs': '比較實際成本',
            'vs. theoretical costs': '與理論成本',
            'Identify inventory shrinkage': '識別庫存縮減',
            'and waste': '和浪費',
            
            # 其他常见文本
            'How It Works': '運作方式',
            'Why Choose VaultCaddy?': '為什麼選擇VaultCaddy？',
            'Simple, Transparent Pricing': '簡單透明的定價',
            'in Seconds': '只需幾秒',
            'Upload Your': '上傳您的',
            'AI Processing': 'AI處理',
            'Export to Your System': '匯出到您的系統',
            'Verify & Save': '驗證並保存',
            'Ready to Save': '準備節省',
            'Join 500+': '加入500+',
            'using VaultCaddy': '使用VaultCaddy',
            'for automated accounting': '進行自動化會計',
            
            # 信任标志
            'AES-256 Encrypted': 'AES-256加密',
            'Bank-level security': '銀行級安全',
            'SOC 2 Type II Certified': 'SOC 2 Type II認證',
            'GDPR Compliant': '符合GDPR',
            'Data protected': '數據保護',
            'Rating': '評分',
            'reviews': '評價',
            'Trusted by': '受信賴於',
            'businesses in': '企業在',
            'the USA': '美國',
            
            # 特定行业文本
            'nonprofit organizations': '非營利組織',
            'nonprofit organization businesses': '非營利組織業務',
            'nonprofit organization invoices': '非營利組織發票',
            'Nonprofit Organization Accounting': '非營利組織會計',
            'Nonprofit Organization Invoice Processing Demo': '非營利組織發票處理演示',
            'Nonprofit Organization-Specific Features': '非營利組織專屬功能',
            'food service businesses': '餐飲服務業務',
        }
        
        # 逐个精确替换
        for english, chinese in replacements.items():
            content = content.replace(english, chinese)
        
        # 只有在内容改变时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 失败: {file_path.name} - {e}")
        return False

def main():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    hk_dir = root_dir / 'zh-HK'
    
    print("🇭🇰 开始修复香港版本...")
    print("=" * 80)
    
    if not hk_dir.exists():
        print(f"  ⚠️ 目录不存在: {hk_dir}")
        return
    
    hk_files = list(hk_dir.glob('*-v3.html'))
    hk_files = [f for f in hk_files if 'test' not in f.name and 'backup' not in f.name]
    
    print(f"  找到 {len(hk_files)} 个香港页面")
    
    fixed_count = 0
    for i, file_path in enumerate(hk_files, 1):
        if fix_hk_file(file_path):
            fixed_count += 1
        if i % 10 == 0:
            print(f"  进度: {i}/{len(hk_files)} (已修复: {fixed_count})")
    
    print("\n" + "=" * 80)
    print(f"✅ 香港版本修复完成！")
    print(f"   修复了 {fixed_count} 个页面")
    print("=" * 80)

if __name__ == '__main__':
    main()

