#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 深度修复：所有语言混合问题
更强力的文本替换，确保100%语言一致性
"""

import os
import re
from pathlib import Path

def fix_file_deep(file_path, replacements):
    """深度修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
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
    
    # 日文页面替换
    ja_replacements = {
        '真實客戶評價': 'お客様の声',
        '每月節省': '月間節約',
        '針對日本市場的專業解答': '日本市場向けの専門的な回答',
        '節省20%': '20%割引',
        'Start Free Trial': '無料トライアルを開始',
        'See How It Works': '使い方を見る',
        'AUTO PLAYING': '自動再生中',
        'LIVE DEMONSTRATION': 'ライブデモンストレーション',
        'MOST POPULAR': '最も人気',
        'Monthly Plan': '月払いプラン',
        'Annual Plan': '年払いプラン',
        'per month': '月額',
        'per additional page': '追加ページごと',
        '所有匯出格式': 'すべての出力形式',
        '電郵支援': 'メールサポート',
        '優先電郵支援': '優先メールサポート',
        'Cancel anytime': 'いつでもキャンセル可能',
        'pages included': 'ページ含む',
        '24h auto-delete': '24時間自動削除',
    }
    
    # 繁体中文页面替换（台湾和香港）
    zh_replacements = {
        'Start Free Trial': '開始免費試用',
        'See How It Works': '查看運作方式',
        'AUTO PLAYING': '自動播放',
        'LIVE DEMONSTRATION': '實時演示',
        'MOST POPULAR': '最受歡迎',
        'Monthly Plan': '月付方案',
        'Annual Plan': '年付方案',
        'per month': '每月',
        'per additional page': '每頁額外費用',
        'pages included': '頁面包含',
        'Cancel anytime': '隨時取消',
        'All export formats': '所有匯出格式',
        'Email Support': '電郵支援',
        'Priority email support': '優先電郵支援',
        '24h auto-delete': '24小時自動刪除',
    }
    
    # 韩文页面替换
    ko_replacements = {
        'Start Free Trial': '무료 체험 시작',
        'See How It Works': '작동 방식 보기',
        'AUTO PLAYING': '자동 재생 중',
        'LIVE DEMONSTRATION': '라이브 데모',
        'MOST POPULAR': '가장 인기 있는',
        'Monthly Plan': '월간 플랜',
        'Annual Plan': '연간 플랜',
        'per month': '월',
        'per additional page': '추가 페이지당',
        'pages included': '페이지 포함',
        'Cancel anytime': '언제든지 취소',
        'All export formats': '모든 내보내기 형식',
        'Email Support': '이메일 지원',
        'Priority email support': '우선 이메일 지원',
        '24h auto-delete': '24시간 자동 삭제',
    }
    
    print("🔥 开始深度修复...")
    print("=" * 80)
    
    # 修复日文页面
    ja_dir = root_dir / 'ja-JP'
    if ja_dir.exists():
        print("\n修复日文页面...")
        ja_files = list(ja_dir.glob('*-v3.html'))
        ja_files = [f for f in ja_files if 'test' not in f.name and 'backup' not in f.name]
        fixed_count = 0
        for file_path in ja_files:
            if fix_file_deep(file_path, ja_replacements):
                fixed_count += 1
        print(f"  ✅ 修复了 {fixed_count} 个日文页面")
    
    # 修复台湾繁体页面
    tw_dir = root_dir / 'zh-TW'
    if tw_dir.exists():
        print("\n修复台湾繁体页面...")
        tw_files = list(tw_dir.glob('*-v3.html'))
        tw_files = [f for f in tw_files if 'test' not in f.name and 'backup' not in f.name]
        fixed_count = 0
        for file_path in tw_files:
            if fix_file_deep(file_path, zh_replacements):
                fixed_count += 1
        print(f"  ✅ 修复了 {fixed_count} 个台湾页面")
    
    # 修复香港繁体页面
    hk_dir = root_dir / 'zh-HK'
    if hk_dir.exists():
        print("\n修复香港繁体页面...")
        hk_files = list(hk_dir.glob('*-v3.html'))
        hk_files = [f for f in hk_files if 'test' not in f.name and 'backup' not in f.name]
        fixed_count = 0
        for file_path in hk_files:
            if fix_file_deep(file_path, zh_replacements):
                fixed_count += 1
        print(f"  ✅ 修复了 {fixed_count} 个香港页面")
    
    # 修复韩文页面
    ko_dir = root_dir / 'ko-KR'
    if ko_dir.exists():
        print("\n修复韩文页面...")
        ko_files = list(ko_dir.glob('*-v3.html'))
        ko_files = [f for f in ko_files if 'test' not in f.name and 'backup' not in f.name]
        fixed_count = 0
        for file_path in ko_files:
            if fix_file_deep(file_path, ko_replacements):
                fixed_count += 1
        print(f"  ✅ 修复了 {fixed_count} 个韩文页面")
    
    print("\n" + "=" * 80)
    print("🎉 深度修复完成！")
    print("=" * 80)

if __name__ == '__main__':
    main()

