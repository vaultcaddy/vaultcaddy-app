#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇯🇵 专门修复日本版本的语言混合问题
"""

import os
import re
from pathlib import Path

def fix_jp_file(file_path):
    """修复单个日文文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 日文版本：所有中文和英文替换为日文
        replacements = {
            # 中文标题替换为日文
            '真實客戶評價': 'お客様の声',
            '每月節省': '月間節約',
            '針對日本市場的專業解答': '日本市場向けの専門的な回答',
            '節省20%': '20%割引',
            '所有匯出格式': 'すべての出力形式',
            '電郵支援': 'メールサポート',
            '優先電郵支援': '優先メールサポート',
            
            # 英文替换为日文
            'Start Free Trial': '無料トライアルを開始',
            'See How It Works': '使い方を見る',
            'FREE: Try 20 pages': '無料：20ページお試し',
            'No credit card required': 'クレジットカード不要',
            'AUTO PLAYING': '自動再生中',
            'LIVE DEMONSTRATION': 'ライブデモンストレーション',
            'MOST POPULAR': '最も人気',
            'Monthly Plan': '月払いプラン',
            'Annual Plan': '年払いプラン',
            'per month': '月額',
            'per additional page': '追加ページごと',
            'pages included': 'ページ含む',
            'All export formats': 'すべての出力形式',
            'Email Support': 'メールサポート',
            'Priority email support': '優先メールサポート',
            '24h auto-delete': '24時間自動削除',
            'Cancel anytime': 'いつでもキャンセル可能',
            'Start': '開始',
            'Billed annually': '年間請求',
            
            # 标题和大文本
            'Convert': '変換',
            'Statements in Seconds': '明細書を数秒で',
            'Made Simple': 'シンプルに',
            'Automate': '自動化',
            'Save 10+ hours per week': '週10時間以上を節約',
            'on manual data entry': '手動データ入力で',
            
            # 统计数字标签
            'Hours Saved/Week': '週間節約時間',
            'Accuracy': '精度',
            'Processing': '処理',
            'Per Month': '月額',
            
            # 视频和演示
            'Watch how': '見る方法',
            'are processed in seconds': '数秒で処理',
            'with 98% accuracy': '98%の精度で',
            'Average processing time': '平均処理時間',
            'Starting From/Month': '月額〜',
            
            # 常见问题和挑战
            'Common': '一般的な',
            'Challenges': '課題',
            'How VaultCaddy Solves These Problems': 'VaultCaddyがこれらの問題を解決する方法',
            'Specific Features': '専用機能',
            'Built for the unique needs': 'ユニークなニーズに対応',
            'Built for': '専用設計',
            'designed specifically for': '専用に設計',
            
            # 行业特定功能
            'Supplier Invoice Processing': '仕入先請求書処理',
            'Delivery Platform Reports': '配送プラットフォームレポート',
            'POS System Export': 'POSシステムエクスポート',
            'Cash Flow Tracking': 'キャッシュフロー追跡',
            'Cost Analysis': 'コスト分析',
            'Fund Accounting': '資金会計',
            'Grant Expense Tracking': '助成金経費追跡',
            'Donor Reporting': '寄付者報告',
            'Manual tracking': '手動追跡',
            'weekly': '毎週',
            'Ensuring': '確保',
            'Creating': '作成',
            'Gathering data': 'データ収集',
            
            # 解决方案文本
            'AI-powered automation': 'AI駆動の自動化',
            'Automated': '自動化された',
            'Real-time': 'リアルタイム',
            'One-click': 'ワンクリック',
            'Always prepared': '常に準備完了',
            
            # 功能描述
            'Automatic': '自動',
            'Extract': '抽出',
            'Reconcile': '照合',
            'Track': '追跡',
            'Compare': '比較',
            'Identify': '特定',
            
            # 其他常见文本
            'How It Works': '使い方',
            'Why Choose VaultCaddy?': 'なぜVaultCaddy？',
            'Simple, Transparent Pricing': 'シンプルで透明な料金',
            'in Seconds': '数秒で',
            'Upload Your': 'アップロード',
            'AI Processing': 'AI処理',
            'Export to Your System': 'システムへエクスポート',
            'Verify & Save': '確認して保存',
            'Ready to Save': '節約の準備',
            'Join 500+': '500+に参加',
            'using VaultCaddy': 'VaultCaddyを使用',
            
            # 信任标志
            'AES-256 Encrypted': 'AES-256暗号化',
            'Bank-level security': '銀行レベルのセキュリティ',
            'SOC 2 Type II Certified': 'SOC 2 Type II認証',
            'GDPR Compliant': 'GDPR準拠',
            'Data protected': 'データ保護',
            'Rating': '評価',
            'reviews': 'レビュー',
            'Trusted by': '信頼されている',
            'businesses in': '企業',
            
            # 特定行业文本
            'nonprofit organizations': '非営利組織',
            'nonprofit organization businesses': '非営利組織ビジネス',
            'nonprofit organization invoices': '非営利組織請求書',
            'Nonprofit Organization Accounting': '非営利組織会計',
            'Nonprofit Organization Invoice Processing Demo': '非営利組織請求書処理デモ',
            'Nonprofit Organization-Specific Features': '非営利組織専用機能',
            'food service businesses': '飲食サービス業',
        }
        
        # 逐个精确替换
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
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
    jp_dir = root_dir / 'ja-JP'
    
    print("🇯🇵 开始修复日本版本...")
    print("=" * 80)
    
    if not jp_dir.exists():
        print(f"  ⚠️ 目录不存在: {jp_dir}")
        return
    
    jp_files = list(jp_dir.glob('*-v3.html'))
    jp_files = [f for f in jp_files if 'test' not in f.name and 'backup' not in f.name]
    
    print(f"  找到 {len(jp_files)} 个日本页面")
    
    fixed_count = 0
    for i, file_path in enumerate(jp_files, 1):
        if fix_jp_file(file_path):
            fixed_count += 1
        if i % 10 == 0:
            print(f"  进度: {i}/{len(jp_files)} (已修复: {fixed_count})")
    
    print("\n" + "=" * 80)
    print(f"✅ 日本版本修复完成！")
    print(f"   修复了 {fixed_count} 个页面")
    print("=" * 80)

if __name__ == '__main__':
    main()

