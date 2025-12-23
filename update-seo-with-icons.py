#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有index页面、landing pages和学习中心的SEO标题
加入 📱拍照上传 💰价格 ⚡速度 元素
"""

import re
from pathlib import Path

# 定义4个版本的新SEO内容
SEO_UPDATES = {
    'index.html': {
        'title': 'VaultCaddy 銀行對帳單AI處理 | 📱拍照上傳 💰46元/月 ⚡3秒完成',
        'description': '📱 拍照上傳即可！💰 年費低至HK$46/月！⚡ 只需3秒處理完成！VaultCaddy是香港最簡單易用的銀行對帳單AI處理工具。支援匯豐、恆生、中銀、渣打等所有香港銀行，一鍵匯出QuickBooks/Excel，98%準確率，已服務200+企業。立即免費試用20頁！',
        'og_title': 'VaultCaddy 銀行對帳單AI處理 | 📱拍照上傳 💰46元/月 ⚡3秒完成',
        'og_description': '📱 拍照上傳即可！💰 年費低至HK$46/月！⚡ 只需3秒處理完成！支援所有香港銀行，一鍵匯出QuickBooks/Excel，98%準確率',
        'twitter_title': 'VaultCaddy 銀行對帳單AI處理 | 📱拍照上傳 💰46元/月 ⚡3秒完成',
        'twitter_description': '📱 拍照上傳即可！💰 年費低至HK$46/月！⚡ 只需3秒處理完成！支援所有香港銀行，一鍵匯出QuickBooks/Excel',
    },
    'en/index.html': {
        'title': 'VaultCaddy Bank Statement AI | 📱Photo Upload 💰$46/mo ⚡3sec Done',
        'description': '📱 Just take a photo! 💰 From HK$46/month! ⚡ Done in 3 seconds! VaultCaddy is Hong Kong\'s simplest bank statement AI tool. Support all HK banks (HSBC, Hang Seng, BOC, Standard Chartered), one-click export to QuickBooks/Excel, 98% accuracy, serving 200+ businesses. Try 20 pages free!',
        'og_title': 'VaultCaddy Bank Statement AI | 📱Photo Upload 💰$46/mo ⚡3sec Done',
        'og_description': '📱 Just take a photo! 💰 From HK$46/month! ⚡ Done in 3 seconds! Support all HK banks, one-click QuickBooks/Excel export, 98% accuracy',
        'twitter_title': 'VaultCaddy Bank Statement AI | 📱Photo Upload 💰$46/mo ⚡3sec Done',
        'twitter_description': '📱 Just take a photo! 💰 From HK$46/month! ⚡ Done in 3 seconds! Support all HK banks, QuickBooks/Excel export',
    },
    'jp/index.html': {
        'title': 'VaultCaddy 銀行明細AI処理 | 📱写真アップ 💰46元/月 ⚡3秒完了',
        'description': '📱 写真を撮るだけ！💰 年額HK$46/月から！⚡ わずか3秒で処理完了！VaultCaddyは香港で最も使いやすい銀行明細AI処理ツールです。HSBC、ハンセン、中国銀行、スタンダードチャータードなど香港の全銀行に対応、QuickBooks/Excelへワンクリック出力、98%の精度、200社以上にご利用いただいています。今すぐ20ページ無料お試し！',
        'og_title': 'VaultCaddy 銀行明細AI処理 | 📱写真アップ 💰46元/月 ⚡3秒完了',
        'og_description': '📱 写真を撮るだけ！💰 年額HK$46/月から！⚡ わずか3秒で処理完了！香港の全銀行対応、QuickBooks/Excelへワンクリック出力、98%精度',
        'twitter_title': 'VaultCaddy 銀行明細AI処理 | 📱写真アップ 💰46元/月 ⚡3秒完了',
        'twitter_description': '📱 写真を撮るだけ！💰 年額HK$46/月から！⚡ わずか3秒で処理完了！香港の全銀行対応、QuickBooks/Excel出力',
    },
    'kr/index.html': {
        'title': 'VaultCaddy 은행명세서AI처리 | 📱사진업로드 💰46원/월 ⚡3초완료',
        'description': '📱 사진만 찍으면 됩니다！💰 연회비 HK$46/월부터！⚡ 단 3초면 처리 완료！VaultCaddy는 홍콩에서 가장 사용하기 쉬운 은행명세서 AI 처리 도구입니다. HSBC, 항셍, 중국은행, 스탠다드차타드 등 홍콩의 모든 은행 지원, QuickBooks/Excel로 원클릭 내보내기, 98% 정확도, 200개 이상 기업이 사용 중. 지금 20페이지 무료 체험！',
        'og_title': 'VaultCaddy 은행명세서AI처리 | 📱사진업로드 💰46원/월 ⚡3초완료',
        'og_description': '📱 사진만 찍으면 됩니다！💰 연회비 HK$46/월부터！⚡ 단 3초면 처리 완료！홍콩의 모든 은행 지원, QuickBooks/Excel 원클릭 내보내기, 98% 정확도',
        'twitter_title': 'VaultCaddy 은행명세서AI처리 | 📱사진업로드 💰46원/월 ⚡3초완료',
        'twitter_description': '📱 사진만 찍으면 됩니다！💰 연회비 HK$46/월부터！⚡ 단 3초면 처리 완료！홍콩의 모든 은행 지원, QuickBooks/Excel 내보내기',
    }
}

def update_meta_tag(content, tag_pattern, new_value):
    """更新meta标签的content值"""
    pattern = rf'(<meta\s+[^>]*{tag_pattern}[^>]*content=")[^"]*("[^>]*>)'
    replacement = rf'\g<1>{new_value}\g<2>'
    return re.sub(pattern, replacement, content, flags=re.IGNORECASE)

def update_title_tag(content, new_title):
    """更新title标签"""
    pattern = r'<title>[^<]*</title>'
    replacement = f'<title>{new_title}</title>'
    return re.sub(pattern, replacement, content, flags=re.IGNORECASE)

def update_index_file(file_path, seo_data):
    """更新单个index文件的SEO标签"""
    print(f'\n处理: {file_path}')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新title
        print('  - 更新<title>标签...')
        content = update_title_tag(content, seo_data['title'])
        
        # 更新meta description
        print('  - 更新<meta name="description">...')
        content = update_meta_tag(content, r'name=["\']description["\']', seo_data['description'])
        
        # 更新Open Graph title
        print('  - 更新og:title...')
        content = update_meta_tag(content, r'property=["\']og:title["\']', seo_data['og_title'])
        
        # 更新Open Graph description
        print('  - 更新og:description...')
        content = update_meta_tag(content, r'property=["\']og:description["\']', seo_data['og_description'])
        
        # 更新Twitter title
        print('  - 更新twitter:title...')
        content = update_meta_tag(content, r'name=["\']twitter:title["\']', seo_data['twitter_title'])
        
        # 更新Twitter description
        print('  - 更新twitter:description...')
        content = update_meta_tag(content, r'name=["\']twitter:description["\']', seo_data['twitter_description'])
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'  ✅ 完成！')
        return True
        
    except Exception as e:
        print(f'  ❌ 错误: {e}')
        return False

def main():
    """主函数"""
    print('='*60)
    print('🔄 更新所有index页面的SEO标签')
    print('='*60)
    print('\n📋 更新内容:')
    print('  ✅ <title>标签 - 加入📱💰⚡元素')
    print('  ✅ <meta name="description"> - 加入核心卖点')
    print('  ✅ Open Graph标签 (og:title, og:description)')
    print('  ✅ Twitter Card标签 (twitter:title, twitter:description)')
    print('')
    
    success_count = 0
    fail_count = 0
    
    # 更新4个版本的index.html
    for file_path, seo_data in SEO_UPDATES.items():
        if Path(file_path).exists():
            if update_index_file(file_path, seo_data):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f'\n⚠️  文件不存在: {file_path}')
            fail_count += 1
    
    print('\n' + '='*60)
    print(f'✅ Index页面处理完成: {success_count}个成功, {fail_count}个失败')
    print('='*60)
    
    if success_count > 0:
        print('\n✨ 更新结果:')
        print('  ✅ 所有index页面的SEO标签已更新')
        print('  ✅ 标题包含: 📱拍照上传 💰价格 ⚡速度')
        print('  ✅ 描述突出核心卖点')

if __name__ == '__main__':
    main()

