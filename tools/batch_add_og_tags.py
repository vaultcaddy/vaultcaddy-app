#!/usr/bin/env python3
"""
批量为 VaultCaddy Landing Pages 添加 Open Graph 和 SEO 优化标签

作用：
1. 提升搜索结果点击率（CTR）
2. 社交媒体分享时显示漂亮的预览卡片
3. 增加曝光和新用户

使用方法：
    python3 batch_add_og_tags.py
"""

import os
import re
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "optimized_pages"
OUTPUT_DIR.mkdir(exist_ok=True)

# OG 图片配置（需要创建这些图片！）
OG_IMAGES = {
    'zh': 'https://vaultcaddy.com/images/og-preview-zh.jpg',
    'en': 'https://vaultcaddy.com/images/og-preview-en.jpg',
    'ja': 'https://vaultcaddy.com/images/og-preview-ja.jpg',
    'ko': 'https://vaultcaddy.com/images/og-preview-ko.jpg',
}

# SEO 配置（针对不同语言）
SEO_CONFIG = {
    'zh': {
        'title_template': '{bank}银行对账单转Excel｜3秒完成｜准确率98%｜月费$46起 - VaultCaddy',
        'title_default': '银行对账单转Excel｜3秒完成｜准确率98%｜月费$46起 - VaultCaddy',
        'description_template': 'VaultCaddy AI自动处理{bank}银行对账单，3秒转成Excel/CSV。比人工便宜95%，比Dext便宜70%，准确率98%。月费HK$46起，免费试用20页。立即体验！',
        'description_default': 'VaultCaddy AI自动处理银行对账单、发票，3秒转成Excel/CSV。比人工便宜95%，比Dext便宜70%，准确率98%。支持恒生、汇丰、中银等所有香港银行。月费HK$46起，免费试用20页。',
        'og_title_template': '{bank}银行对账单转Excel，3秒完成｜月费$46起',
        'og_title_default': '银行对账单转Excel，3秒完成｜月费$46起',
        'og_description': '拍照上传对账单，AI自动转成Excel。比人工便宜95%，比Dext便宜70%。支持所有香港银行，免费试用20页。',
        'locale': 'zh_TW',
    },
    'en': {
        'title_template': '{bank} Bank Statement to Excel | 3 Seconds | 98% Accurate | From $46/month - VaultCaddy',
        'title_default': 'Bank Statement to Excel in 3 Seconds | 98% Accurate | From $46/month - VaultCaddy',
        'description_template': 'VaultCaddy AI processes {bank} bank statements to Excel/CSV in 3 seconds. 95% cheaper than manual, 70% cheaper than Dext, 98% accuracy. From HK$46/month, 20 pages free trial.',
        'description_default': 'VaultCaddy AI processes bank statements & invoices to Excel/CSV in 3 seconds. 95% cheaper than manual, 70% cheaper than Dext. Supports all HK banks. From $46/month, free trial.',
        'og_title_template': '{bank} Bank Statement to Excel in 3 Seconds | From $46/month',
        'og_title_default': 'Bank Statement to Excel in 3 Seconds | From $46/month',
        'og_description': 'Upload bank statements, AI converts to Excel automatically. 95% cheaper than manual, 70% cheaper than Dext. Free 20-page trial.',
        'locale': 'en',
    },
    'ja': {
        'title_template': '{bank}銀行明細書→Excel変換｜3秒完了｜正確率98%｜月額$46〜 - VaultCaddy',
        'title_default': '銀行明細書→Excel変換｜3秒完了｜正確率98%｜月額$46〜 - VaultCaddy',
        'description_template': 'VaultCaddy AIが{bank}銀行明細書を3秒でExcel/CSV変換。手作業より95%安く、Dextより70%安い、正確率98%。月額$46〜、20ページ無料トライアル。',
        'description_default': 'VaultCaddy AIが銀行明細書・請求書を3秒でExcel/CSV変換。手作業より95%安く、Dextより70%安い。香港全銀行対応。月額$46〜、無料トライアル。',
        'og_title_template': '{bank}銀行明細書→Excel変換、3秒完了｜月額$46〜',
        'og_title_default': '銀行明細書→Excel変換、3秒完了｜月額$46〜',
        'og_description': '明細書を撮影してアップロード、AIが自動的にExcelに変換。手作業より95%安く、Dextより70%安い。20ページ無料トライアル。',
        'locale': 'ja',
    },
    'ko': {
        'title_template': '{bank}은행 명세서→Excel 변환｜3초 완료｜정확도98%｜월$46부터 - VaultCaddy',
        'title_default': '은행 명세서→Excel 변환｜3초 완료｜정확도98%｜월$46부터 - VaultCaddy',
        'description_template': 'VaultCaddy AI가 {bank}은행 명세서를 3초 만에 Excel/CSV로 변환. 수동보다 95% 저렴, Dext보다 70% 저렴, 정확도 98%. 월$46부터, 20페이지 무료 체험.',
        'description_default': 'VaultCaddy AI가 은행 명세서와 송장을 3초 만에 Excel/CSV로 변환. 수동보다 95% 저렴, Dext보다 70% 저렴. 홍콩 모든 은행 지원. 월$46부터, 무료 체험.',
        'og_title_template': '{bank}은행 명세서→Excel 변환, 3초 완료｜월$46부터',
        'og_title_default': '은행 명세서→Excel 변환, 3초 완료｜월$46부터',
        'og_description': '명세서 촬영 업로드, AI가 자동으로 Excel로 변환. 수동보다 95% 저렴, Dext보다 70% 저렴. 20페이지 무료 체험.',
        'locale': 'ko',
    },
}

# 银行名称映射
BANK_NAMES = {
    'hsbc': {'zh': '汇丰', 'en': 'HSBC', 'ja': 'HSBC', 'ko': 'HSBC'},
    'hangseng': {'zh': '恒生', 'en': 'Hang Seng', 'ja': 'ハンセン', 'ko': '항셍'},
    'bochk': {'zh': '中国银行（香港）', 'en': 'Bank of China (HK)', 'ja': '中国銀行（香港）', 'ko': '중국은행(홍콩)'},
    'citibank': {'zh': '花旗', 'en': 'Citibank', 'ja': 'シティバンク', 'ko': '씨티은행'},
    'sc': {'zh': '渣打', 'en': 'Standard Chartered', 'ja': 'スタンダードチャータード', 'ko': 'SC제일은행'},
    'dbs': {'zh': '星展', 'en': 'DBS', 'ja': 'DBS', 'ko': 'DBS'},
    'bea': {'zh': '东亚', 'en': 'BEA', 'ja': '東亜', 'ko': 'BEA'},
    'dahsing': {'zh': '大新', 'en': 'Dah Sing', 'ja': '大新', 'ko': '다싱'},
    'citic': {'zh': '中信', 'en': 'CITIC', 'ja': '中信', 'ko': '중신'},
    'bankcomm': {'zh': '交通', 'en': 'Bank of Communications', 'ja': '交通', 'ko': '교통'},
}


def detect_language(file_path):
    """检测文件语言"""
    path_str = str(file_path)
    if '/en/' in path_str or path_str.startswith('en/'):
        return 'en'
    elif '/ja/' in path_str or path_str.startswith('ja/') or '/jp/' in path_str or path_str.startswith('jp/'):
        return 'ja'
    elif '/ko/' in path_str or path_str.startswith('ko/') or '/kr/' in path_str or path_str.startswith('kr/'):
        return 'ko'
    else:
        return 'zh'


def detect_bank(file_path):
    """从文件名检测银行"""
    filename = Path(file_path).stem.lower()
    for bank_code, bank_names in BANK_NAMES.items():
        if bank_code in filename:
            return bank_code
    return None


def generate_og_tags(file_path, base_url='https://vaultcaddy.com'):
    """生成 Open Graph 和 SEO 标签"""
    
    # 检测语言和银行
    lang = detect_language(file_path)
    bank_code = detect_bank(file_path)
    seo = SEO_CONFIG[lang]
    
    # 生成标题和描述
    if bank_code and bank_code in BANK_NAMES:
        bank_name = BANK_NAMES[bank_code][lang]
        title = seo['title_template'].format(bank=bank_name)
        description = seo['description_template'].format(bank=bank_name)
        og_title = seo['og_title_template'].format(bank=bank_name)
    else:
        title = seo['title_default']
        description = seo['description_default']
        og_title = seo['og_title_default']
    
    # 生成URL
    url = f"{base_url}/{file_path.relative_to(BASE_DIR)}"
    
    # 获取 OG 图片
    og_image = OG_IMAGES.get(lang, OG_IMAGES['zh'])
    
    # 生成标签HTML
    tags = f'''<!-- ✅ SEO 优化标签 -->
<title>{title}</title>
<meta name="description" content="{description}">

<!-- ✅ Open Graph 标签（社交媒体预览）-->
<meta property="og:type" content="website">
<meta property="og:site_name" content="VaultCaddy">
<meta property="og:locale" content="{seo['locale']}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{seo['og_description']}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:secure_url" content="{og_image}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_title}">

<!-- ✅ Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{seo['og_description']}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{og_title}">

<!-- ✅ 规范链接 -->
<link rel="canonical" href="{url}">
'''
    
    return tags


def process_html_file(file_path):
    """处理单个HTML文件"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有 OG 标签
        if 'property="og:title"' in content:
            print(f"⏭️  跳过（已有OG标签）: {file_path.name}")
            return False
        
        # 生成新标签
        new_tags = generate_og_tags(file_path)
        
        # 查找插入位置（在 <head> 标签之后）
        head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
        if not head_match:
            print(f"❌ 未找到 <head> 标签: {file_path.name}")
            return False
        
        # 插入新标签
        insert_pos = head_match.end()
        new_content = content[:insert_pos] + '\n' + new_tags + '\n' + content[insert_pos:]
        
        # 保存到输出目录
        output_path = OUTPUT_DIR / file_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已优化: {file_path.name} → {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ 错误处理 {file_path.name}: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始批量添加 Open Graph 和 SEO 标签...\n")
    
    # 查找所有需要处理的HTML文件
    html_files = []
    
    # 主目录的 landing pages
    for pattern in ['*-bank-statement.html', 'ai-vs-*.html', 'vaultcaddy-vs-*.html', 'index.html']:
        html_files.extend(BASE_DIR.glob(pattern))
    
    # 子目录的 landing pages
    for lang_dir in ['en', 'ja', 'jp', 'ko', 'kr']:
        lang_path = BASE_DIR / lang_dir
        if lang_path.exists():
            for pattern in ['*-bank-statement.html', 'ai-vs-*.html', 'vaultcaddy-vs-*.html', 'index.html']:
                html_files.extend(lang_path.glob(pattern))
    
    # 去重
    html_files = list(set(html_files))
    
    print(f"📁 找到 {len(html_files)} 个HTML文件\n")
    
    # 处理文件
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in html_files:
        result = process_html_file(file_path)
        if result is True:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
    
    # 输出统计
    print(f"\n{'='*60}")
    print(f"📊 处理完成统计：")
    print(f"✅ 成功优化：{success_count} 个文件")
    print(f"⏭️  跳过：{skip_count} 个文件（已有OG标签）")
    print(f"❌ 错误：{error_count} 个文件")
    print(f"{'='*60}\n")
    
    print(f"📂 优化后的文件保存在：{OUTPUT_DIR}")
    print(f"\n⚠️  重要：请检查优化后的文件，确认无误后再替换原文件！")
    print(f"\n📝 下一步：")
    print(f"1. 创建 OG 预览图（1200x630px）")
    print(f"2. 上传图片到 /images/ 目录")
    print(f"3. 测试社交媒体预览")
    print(f"4. 提交 Google Search Console 重新抓取")


if __name__ == '__main__':
    main()

