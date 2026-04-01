#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在首页中突出"拍照/上传照片"功能
在Hero区域的描述中添加这个关键功能
"""

import os
import re

def add_photo_upload_highlight(file_path, lang='zh'):
    """
    添加拍照/上传照片功能的突出介绍
    
    Args:
        file_path: 文件路径
        lang: 语言代码 ('zh', 'en', 'ja', 'ko')
    
    Returns:
        bool: 是否成功修改
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据语言定义新的描述文本
        descriptions = {
            'zh': {
                'hero_addition': '📱 手機拍照即可 • 自動提取數據',
                'meta_addition': ' 📱 手機拍照秒傳QuickBooks',
                'feature_title': '手機拍照秒上傳',
                'feature_desc': '<span>📱 手機直接拍照上傳</span><br/><span>無需掃描器或電腦</span><br/><span>隨時隨地處理文檔</span>'
            },
            'en': {
                'hero_addition': '📱 Just Take a Photo • Instant Data Extraction',
                'meta_addition': ' 📱 Photo Upload to QuickBooks in Seconds',
                'feature_title': 'Mobile Photo Upload',
                'feature_desc': '<span>📱 Upload via Phone Camera</span><br/><span>No Scanner or Computer Required</span><br/><span>Process Documents Anywhere</span>'
            },
            'ja': {
                'hero_addition': '📱 写真撮影だけで • 自動データ抽出',
                'meta_addition': ' 📱 スマホ撮影でQuickBooksへ',
                'feature_title': 'スマホ撮影アップロード',
                'feature_desc': '<span>📱 スマートフォンで直接撮影</span><br/><span>スキャナー不要</span><br/><span>いつでもどこでも処理</span>'
            },
            'ko': {
                'hero_addition': '📱 사진만 찍으면 OK • 자동 데이터 추출',
                'meta_addition': ' 📱 스마트폰 촬영으로 QuickBooks에',
                'feature_title': '모바일 사진 업로드',
                'feature_desc': '<span>📱 스마트폰으로 바로 촬영</span><br/><span>스캐너나 컴퓨터 불필요</span><br/><span>언제 어디서나 문서 처리</span>'
            }
        }
        
        desc = descriptions.get(lang, descriptions['zh'])
        modified = False
        
        # 1. 在Hero区域的"自動轉換"后面添加拍照功能
        hero_patterns = {
            'zh': r'(\*\*自動轉換 Excel/CSV/QuickBooks/Xero\*\*)',
            'en': r'(\*\*Automatic Conversion to Excel/CSV/QuickBooks/Xero\*\*)',
            'ja': r'(\*\*自動変換 Excel/CSV/QuickBooks/Xero\*\*)',
            'ko': r'(\*\*자동 변환 Excel/CSV/QuickBooks/Xero\*\*)'
        }
        
        pattern = hero_patterns.get(lang, hero_patterns['zh'])
        replacement = r'\1<br/>' + desc['hero_addition']
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
        
        # 2. 在meta description中添加拍照功能
        if lang == 'zh':
            meta_pattern = r'(3秒轉QuickBooks/Excel)'
            meta_replacement = r'\1' + desc['meta_addition']
        elif lang == 'en':
            meta_pattern = r'(Export to QuickBooks in 3 seconds)'
            meta_replacement = r'\1' + desc['meta_addition']
        elif lang == 'ja':
            meta_pattern = r'(3秒でQuickBooks/Excelへ)'
            meta_replacement = r'\1' + desc['meta_addition']
        elif lang == 'ko':
            meta_pattern = r'(3초로 QuickBooks/Excel 전환)'
            meta_replacement = r'\1' + desc['meta_addition']
        
        if re.search(meta_pattern, content):
            content = re.sub(meta_pattern, meta_replacement, content, count=1)
            modified = True
        
        # 3. 添加一个新的功能卡片（在"极速处理"卡片前面）
        # 找到"极速处理"卡片的位置
        speed_card_patterns = {
            'zh': r'(<h3[^>]*>極速處理</h3>)',
            'en': r'(<h3[^>]*>Ultra Fast</h3>)',
            'ja': r'(<h3[^>]*>超高速処理</h3>)',
            'ko': r'(<h3[^>]*>초고속 처리</h3>)'
        }
        
        speed_pattern = speed_card_patterns.get(lang, speed_card_patterns['zh'])
        
        # 新的功能卡片HTML
        new_card_html = f'''<!-- 卡片 0: 手機拍照功能 -->
<div class="fade-in-up" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 40px rgba(0,0,0,0.08)'" onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 20px 50px rgba(0,0,0,0.12)'" style="background: white; border-radius: 20px; padding: 2.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.08); border: 2px solid #e5e7eb; text-align: center; transition: all 0.3s ease;">
<div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);">
<i class="fas fa-camera" style="color: white; font-size: 2.5rem;"></i>
</div>
<h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">{desc['feature_title']}</h3>
<p style="color: #6b7280; line-height: 1.8; font-size: 1rem;">{desc['feature_desc']}</p>
</div>
<!-- 原有卡片 1 -->
<div class="fade-in-up delay-1" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 40px rgba(0,0,0,0.08)'" onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 20px 50px rgba(0,0,0,0.12)'" style="background: white; border-radius: 20px; padding: 2.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.08); border: 2px solid #e5e7eb; text-align: center; transition: all 0.3s ease;">
<div style="width: 80px; height: 80px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);">
<i class="fas fa-bolt" style="color: white; font-size: 2.5rem;"></i>
</div>
'''
        
        # 查找"极速处理"卡片的开始位置
        # 需要往前找到包含该卡片的div容器
        if re.search(speed_pattern, content):
            # 查找卡片容器的开始
            # 向前查找包含 "fade-in-up delay-1" 的div
            container_pattern = r'(<div class="fade-in-up delay-1"[^>]*>.*?<div style="width: 80px; height: 80px;[^>]*?linear-gradient\(135deg, #10b981 0%, #059669 100%\)[^>]*>.*?<i class="fas fa-bolt")'
            
            if re.search(container_pattern, content, re.DOTALL):
                content = re.sub(
                    container_pattern,
                    new_card_html + r'\1',
                    content,
                    count=1,
                    flags=re.DOTALL
                )
                modified = True
                
                # 修改grid-template-columns从3列改为4列
                grid_pattern = r'(grid-template-columns:\s*repeat\()3(,\s*1fr\))'
                if re.search(grid_pattern, content):
                    content = re.sub(grid_pattern, r'\g<1>4\2', content)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 处理失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("📱 突出\"拍照/上传照片\"功能")
    print("=" * 60)
    
    # 4个版本的首页
    index_files = [
        ('index.html', 'zh'),
        ('en/index.html', 'en'),
        ('jp/index.html', 'ja'),
        ('kr/index.html', 'ko')
    ]
    
    success_count = 0
    
    for file_path, lang in index_files:
        if not os.path.exists(file_path):
            print(f"⏭️  文件不存在: {file_path}")
            continue
        
        print(f"🔄 处理 {file_path}...", end=' ')
        
        if add_photo_upload_highlight(file_path, lang):
            success_count += 1
            print("✅ 完成")
        else:
            print("⏭️  跳过（已有或无法修改）")
    
    print("\n" + "=" * 60)
    print("📊 修改完成总结")
    print("=" * 60)
    print(f"✅ 成功修改: {success_count}/{len(index_files)} 个文件")
    
    if success_count > 0:
        print(f"\n🚀 修改效果:")
        print(f"   ✅ Hero区域突出手机拍照功能")
        print(f"   ✅ Meta描述中添加拍照关键词")
        print(f"   ✅ 新增\"手机拍照上传\"功能卡片")
        print(f"   ✅ 4个语言版本同步更新")

if __name__ == '__main__':
    main()

