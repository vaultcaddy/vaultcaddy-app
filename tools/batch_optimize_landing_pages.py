#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量优化Landing Page脚本
为所有银行和行业页面添加图片和内容区域
"""

import os
import re
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent

# 手机版响应式CSS（与行业页面相同）
MOBILE_CSS = '''
    <!-- 手機版響應式優化 -->
    <style>
    @media (max-width: 768px) {
        /* 新增区域响应式样式 */
        section h2 {
            font-size: 1.8rem !important;
        }
        
        section h3 {
            font-size: 1.3rem !important;
        }
        
        section h4 {
            font-size: 1.1rem !important;
        }
        
        section p {
            font-size: 0.95rem !important;
        }
        
        /* 网格布局改为单列 */
        section div[style*="display: grid"][style*="grid-template-columns: 1fr 1fr"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(2, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(3, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        section div[style*="display: grid"][style*="grid-template-columns: repeat(4, 1fr)"] {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        
        /* 表格滚动 */
        table {
            font-size: 0.85rem !important;
        }
        
        table th,
        table td {
            padding: 0.5rem !important;
        }
        
        /* 容器内边距 */
        .container {
            padding: 0 1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        section h2 {
            font-size: 1.5rem !important;
        }
        
        section h3 {
            font-size: 1.2rem !important;
        }
        
        section h4 {
            font-size: 1rem !important;
        }
        
        section p, section li {
            font-size: 0.9rem !important;
        }
        
        /* 4列网格在小屏幕改为1列 */
        section div[style*="display: grid"][style*="grid-template-columns: repeat(4, 1fr)"] {
            grid-template-columns: 1fr !important;
        }
        
        /* 图片边距 */
        img {
            margin-bottom: 2rem !important;
        }
        
        /* 内边距优化 */
        section {
            padding: 3rem 0 !important;
        }
        
        section > div {
            padding: 0 0.75rem !important;
        }
    }
    </style>
'''

# HSBC页面的优化内容模板（简洁版）
BANK_SECTION_1 = '''
<!-- 新增区域1：銀行對帳單3大應用場景 -->
<section style="padding: 5rem 0; background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);">
<div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
<h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: {BANK_COLOR};">
📊 誰在使用VaultCaddy處理{BANK_NAME}對帳單？
</h2>
<p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
香港200+企業的選擇，節省90%處理時間
</p>

<!-- 场景图片 -->
<div style="text-align: center; margin-bottom: 3rem;">
<img alt="香港企業使用{BANK_NAME}對帳單處理系統" loading="lazy" src="https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
</div>

<!-- 三大场景卡片 -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3rem;">
<!-- 场景1 -->
<div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
<div style="font-size: 4rem; margin-bottom: 1rem;">🏪</div>
<h3 style="font-size: 1.3rem; font-weight: 700; color: {BANK_COLOR}; margin-bottom: 1rem;">中小企業</h3>
<div style="background: #fef2f2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
<div style="font-size: 2rem; font-weight: 900; color: {BANK_COLOR};">500+</div>
<div style="font-size: 0.9rem; color: #6b7280;">月均交易筆數</div>
</div>
<ul style="text-align: left; font-size: 0.95rem; line-height: 1.8; color: #4b5563; list-style: none; padding: 0;">
<li>✓ 3分鐘完成月度對帳</li>
<li>✓ 節省HK$2,000/月</li>
<li>✓ 準確率98%</li>
</ul>
</div>

<!-- 场景2 -->
<div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
<div style="font-size: 4rem; margin-bottom: 1rem;">💼</div>
<h3 style="font-size: 1.3rem; font-weight: 700; color: {BANK_COLOR}; margin-bottom: 1rem;">會計師事務所</h3>
<div style="background: #fef2f2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
<div style="font-size: 2rem; font-weight: 900; color: {BANK_COLOR};">60份</div>
<div style="font-size: 0.9rem; color: #6b7280;">月處理對帳單數</div>
</div>
<ul style="text-align: left; font-size: 0.95rem; line-height: 1.8; color: #4b5563; list-style: none; padding: 0;">
<li>✓ 批量上傳一次完成</li>
<li>✓ 節省1週工作時間</li>
<li>✓ 自動標記異常</li>
</ul>
</div>

<!-- 场景3 -->
<div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
<div style="font-size: 4rem; margin-bottom: 1rem;">🏢</div>
<h3 style="font-size: 1.3rem; font-weight: 700; color: {BANK_COLOR}; margin-bottom: 1rem;">大型企業</h3>
<div style="background: #fef2f2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
<div style="font-size: 2rem; font-weight: 900; color: {BANK_COLOR};">多部門</div>
<div style="font-size: 0.9rem; color: #6b7280;">集中管理</div>
</div>
<ul style="text-align: left; font-size: 0.95rem; line-height: 1.8; color: #4b5563; list-style: none; padding: 0;">
<li>✓ 多用戶權限管理</li>
<li>✓ 雲端集中存儲</li>
<li>✓ 完整審計記錄</li>
</ul>
</div>
</div>

<!-- 对比数据 -->
<div style="background: linear-gradient(135deg, {BANK_COLOR} 0%, {BANK_COLOR_DARK} 100%); padding: 3rem; border-radius: 16px; color: white; margin-bottom: 2rem;">
<h3 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">⚡ 效率對比</h3>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
<div>
<div style="font-size: 3rem; font-weight: 900; margin-bottom: 0.5rem;">3秒</div>
<div style="font-size: 1rem; opacity: 0.9;">AI處理速度</div>
<div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">vs 人工30-60分鐘</div>
</div>
<div>
<div style="font-size: 3rem; font-weight: 900; margin-bottom: 0.5rem;">98%</div>
<div style="font-size: 1rem; opacity: 0.9;">識別準確率</div>
<div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">vs 人工85-90%</div>
</div>
<div>
<div style="font-size: 3rem; font-weight: 900; margin-bottom: 0.5rem;">90%</div>
<div style="font-size: 1rem; opacity: 0.9;">時間節省</div>
<div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">每月省10-15小時</div>
</div>
</div>
</div>

<div style="text-align: center;">
<a href="https://vaultcaddy.com/auth.html" style="display: inline-block; background: linear-gradient(135deg, {BANK_COLOR} 0%, {BANK_COLOR_DARK} 100%); color: white; padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); transition: all 0.3s ease;">
免費試用20頁 →
</a>
<p style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">無需信用卡 | 3秒看到效果</p>
</div>
</div>
</section>
'''

BANK_SECTION_2 = '''
<!-- 新增区域2：數據安全保障 -->
<section style="padding: 5rem 0; background: white;">
<div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
<h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
🔒 銀行級數據安全保護
</h2>
<p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
符合香港PDPO條例，保護您的{BANK_NAME}對帳單數據
</p>

<!-- 安全图片 -->
<div style="text-align: center; margin-bottom: 3rem;">
<img alt="銀行級數據加密與安全保護" loading="lazy" src="https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
</div>

<!-- 4大安全保障 -->
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 3rem;">
<div style="text-align: center; padding: 2rem 1rem; background: #f0f9ff; border-radius: 12px;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
<h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">AES-256加密</h3>
<p style="font-size: 0.85rem; color: #6b7280;">銀行級別加密傳輸</p>
</div>
<div style="text-align: center; padding: 2rem 1rem; background: #f0fdf4; border-radius: 12px;">
<div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
<h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">PDPO合規</h3>
<p style="font-size: 0.85rem; color: #6b7280;">香港私隱條例認證</p>
</div>
<div style="text-align: center; padding: 2rem 1rem; background: #fef3c7; border-radius: 12px;">
<div style="font-size: 3rem; margin-bottom: 1rem;">☁️</div>
<h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Google Cloud</h3>
<p style="font-size: 0.85rem; color: #6b7280;">企業級雲端架構</p>
</div>
<div style="text-align: center; padding: 2rem 1rem; background: #fce7f3; border-radius: 12px;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🗑️</div>
<h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">隨時刪除</h3>
<p style="font-size: 0.85rem; color: #6b7280;">完全控制您的數據</p>
</div>
</div>

<!-- 安全对比表 -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 16px; color: white; margin-bottom: 3rem;">
<h3 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">🛡️ 多層安全防護</h3>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
<div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
<div style="font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem;">上傳前</div>
<div style="font-size: 1rem; opacity: 0.9; margin-bottom: 1rem;">本地加密</div>
<div style="font-size: 0.85rem; opacity: 0.8;">設備端預加密處理</div>
</div>
<div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
<div style="font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem;">傳輸中</div>
<div style="font-size: 1rem; opacity: 0.9; margin-bottom: 1rem;">SSL/TLS</div>
<div style="font-size: 0.85rem; opacity: 0.8;">銀行級傳輸協議</div>
</div>
<div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
<div style="font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem;">存儲後</div>
<div style="font-size: 1rem; opacity: 0.9; margin-bottom: 1rem;">二次加密</div>
<div style="font-size: 0.85rem; opacity: 0.8;">雲端AES-256加密</div>
</div>
</div>
</div>

<!-- 常见问题简化版 -->
<div style="background: #f9fafb; padding: 2.5rem; border-radius: 12px; border-left: 4px solid #667eea;">
<h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1.5rem;">❓ 安全相關常見問題</h3>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
<div>
<h4 style="font-size: 1rem; font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">✓ 員工能看到我的數據嗎？</h4>
<p style="font-size: 0.9rem; line-height: 1.6; color: #4b5563;">不能。所有數據加密存儲，未經授權無法查看。</p>
</div>
<div>
<h4 style="font-size: 1rem; font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">✓ 取消訂閱後數據會怎樣？</h4>
<p style="font-size: 0.9rem; line-height: 1.6; color: #4b5563;">可隨時導出並永久刪除，30天內完全清除。</p>
</div>
<div>
<h4 style="font-size: 1rem; font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">✓ 會分享給銀行或第三方嗎？</h4>
<p style="font-size: 0.9rem; line-height: 1.6; color: #4b5563;">絕不。我們是獨立服務商，無數據共享協議。</p>
</div>
<div>
<h4 style="font-size: 1rem; font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">✓ 數據存儲在哪裡？</h4>
<p style="font-size: 0.9rem; line-height: 1.6; color: #4b5563;">亞太地區數據中心，受香港法律保護。</p>
</div>
</div>
</div>
</div>
</section>
'''

# 银行颜色映射
BANK_COLORS = {
    'hsbc': ('#DB0011', '#8B0008'),
    'hangseng': ('#00685E', '#004D45'),
    'bochk': ('#C8102E', '#8B0000'),
    'sc': ('#0072BC', '#005A9C'),
    'dbs': ('#E30613', '#B00510'),
    'bea': ('#006EB6', '#005A9C'),
    'citibank': ('#003DA5', '#002B73'),
    'dahsing': ('#003DA5', '#002B73'),
    'citic': ('#C8102E', '#8B0000'),
    'bankcomm': ('#004EA2', '#003B7A'),
    'default': ('#667eea', '#764ba2')
}

def get_bank_color(filename):
    """根据文件名获取银行品牌色"""
    for bank_key in BANK_COLORS.keys():
        if bank_key in filename.lower():
            return BANK_COLORS[bank_key]
    return BANK_COLORS['default']

def get_bank_name(filename):
    """从文件名提取银行名称"""
    bank_names = {
        'hsbc': '滙豐銀行',
        'hangseng': '恒生銀行',
        'hang-seng': '恒生銀行',
        'bochk': '中銀香港',
        'boc-hk': '中銀香港',
        'sc': '渣打銀行',
        'dbs': '星展銀行',
        'bea': '東亞銀行',
        'citibank': '花旗銀行',
        'dahsing': '大新銀行',
        'citic': '中信銀行',
        'bankcomm': '交通銀行'
    }
    
    filename_lower = filename.lower()
    for key, name in bank_names.items():
        if key in filename_lower:
            return name
    return '銀行'

def optimize_bank_page(file_path):
    """优化单个银行页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经优化过
        if '<!-- 新增区域1：銀行對帳單3大應用場景 -->' in content:
            print(f"  ⏭️  已优化，跳过: {file_path.name}")
            return False
        
        # 获取银行信息
        bank_name = get_bank_name(file_path.name)
        bank_color, bank_color_dark = get_bank_color(file_path.name)
        
        # 替换模板变量
        section1 = BANK_SECTION_1.replace('{BANK_NAME}', bank_name)
        section1 = section1.replace('{BANK_COLOR}', bank_color)
        section1 = section1.replace('{BANK_COLOR_DARK}', bank_color_dark)
        
        section2 = BANK_SECTION_2.replace('{BANK_NAME}', bank_name)
        
        # 查找插入位置 - 尝试多种模式
        inserted = False
        
        # 模式1: 在comparison-section后插入
        pattern1 = r'(</section>\s*(?:<!--[^>]*-->)?\s*<section[^>]*class="comparison-section"[^>]*>.*?</section>)'
        if re.search(pattern1, content, re.DOTALL):
            content = re.sub(
                pattern1,
                r'\1\n' + section1 + '\n' + section2,
                content,
                count=1,
                flags=re.DOTALL
            )
            inserted = True
        
        # 模式2: 在FAQ section前插入
        if not inserted:
            faq_patterns = [
                r'(<!-- FAQ -->)',
                r'(<section[^>]*class="faq-section")',
                r'(<section[^>]*style="[^"]*padding:[^"]*background:\s*white[^"]*">.*?<h2[^>]*>.*?常見問題)',
                r'(<section[^>]*style="[^"]*padding:[^"]*background:\s*white[^"]*">.*?<h2[^>]*>.*?FAQ)',
            ]
            
            for faq_pattern in faq_patterns:
                if re.search(faq_pattern, content, re.DOTALL | re.IGNORECASE):
                    content = re.sub(
                        faq_pattern,
                        section1 + '\n' + section2 + '\n' + r'\1',
                        content,
                        count=1,
                        flags=re.DOTALL | re.IGNORECASE
                    )
                    inserted = True
                    break
        
        # 模式3: 在related-banks-section前插入
        if not inserted:
            related_pattern = r'(<section[^>]*class="related-banks-section")'
            if re.search(related_pattern, content):
                content = re.sub(
                    related_pattern,
                    section1 + '\n' + section2 + '\n' + r'\1',
                    content,
                    count=1
                )
                inserted = True
        
        # 模式4: 在final-cta-section前插入
        if not inserted:
            cta_pattern = r'(<section[^>]*class="final-cta-section")'
            if re.search(cta_pattern, content):
                content = re.sub(
                    cta_pattern,
                    section1 + '\n' + section2 + '\n' + r'\1',
                    content,
                    count=1
                )
                inserted = True
        
        # 模式5: 在footer前插入（最后的兜底方案）
        if not inserted:
            footer_pattern = r'(<!-- Footer -->|<footer)'
            if re.search(footer_pattern, content, re.IGNORECASE):
                content = re.sub(
                    footer_pattern,
                    section1 + '\n' + section2 + '\n' + r'\1',
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
                inserted = True
        
        # 模式6: 在</body>前插入（绝对兜底）
        if not inserted:
            body_pattern = r'(</body>)'
            if re.search(body_pattern, content, re.IGNORECASE):
                content = re.sub(
                    body_pattern,
                    section1 + '\n' + section2 + '\n' + r'\1',
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
                inserted = True
        
        if not inserted:
            print(f"  ⚠️  找不到插入位置: {file_path.name}")
            return False
        
        # 添加手机版响应式CSS（在</head>前）
        if MOBILE_CSS not in content:
            head_pattern = r'(</head>)'
            if re.search(head_pattern, content, re.IGNORECASE):
                content = re.sub(
                    head_pattern,
                    MOBILE_CSS + '\n' + r'\1',
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 优化完成: {file_path.name} (含手机版CSS)")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误 {file_path.name}: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量优化银行Landing Page...")
    print("📱 包含手机版响应式优化")
    print("=" * 60)
    
    # 统计
    total = 0
    success = 0
    skipped = 0
    failed = 0
    
    # 优化中文版银行页面
    print("\n📄 处理中文版银行页面...")
    bank_files = list(BASE_DIR.glob('*-bank-statement.html'))
    for file_path in sorted(bank_files):
        total += 1
        result = optimize_bank_page(file_path)
        if result:
            success += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1
    
    # 优化多语言版银行页面
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            print(f"\n📄 处理{lang}版银行页面...")
            bank_files = list(lang_dir.glob('*-bank-statement.html'))
            for file_path in sorted(bank_files):
                total += 1
                result = optimize_bank_page(file_path)
                if result:
                    success += 1
                elif result is False:
                    skipped += 1
                else:
                    failed += 1
    
    # 打印统计
    print("\n" + "=" * 60)
    print("📊 优化统计:")
    print(f"  总计: {total} 个文件")
    print(f"  ✅ 成功: {success} 个")
    print(f"  ⏭️  跳过: {skipped} 个（已优化）")
    print(f"  ❌ 失败: {failed} 个")
    print("=" * 60)
    print("\n✨ 批量优化完成！包含手机版响应式CSS")

if __name__ == '__main__':
    main()

