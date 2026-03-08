#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量优化行业解决方案Landing Page脚本
为所有行业页面添加5个内容区域 + 手机版响应式优化
"""

import os
import re
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent

# 手机版响应式CSS
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

# 餐厅页面的5个优化区域（从已完成的restaurant-accounting-solution.html提取）
# 注意：这里我会使用占位符 {INDUSTRY_NAME}，在应用时替换成具体行业

def get_industry_sections(industry_name, industry_emoji):
    """生成行业特定的5个内容区域"""
    
    # 这里返回5个section的HTML模板
    # 由于内容很长，我会从restaurant页面复制并适配
    
    sections = f'''
<!-- 新增区域1：{industry_name}財務管理完整流程 -->
<section style="padding: 5rem 0; background: white;">
    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
            {industry_emoji} {industry_name}財務管理的完整解決方案
        </h2>
        <p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
            從日常收據到月度對帳，VaultCaddy為香港{industry_name}提供一站式財務管理工具
        </p>

        <!-- 场景图片 -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <img alt="香港{industry_name}使用VaultCaddy處理收據和對帳單" loading="lazy" src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
        </div>

        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 16px; color: white;">
            <h3 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 1.5rem; text-align: center;">📊 VaultCaddy如何幫助{industry_name}？</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; text-align: center;">
                <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</div>
                    <div style="font-size: 2rem; font-weight: 900; margin-bottom: 0.5rem;">3秒</div>
                    <div style="font-size: 1rem; opacity: 0.9;">處理速度</div>
                    <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">vs 人工30分鐘</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">✓</div>
                    <div style="font-size: 2rem; font-weight: 900; margin-bottom: 0.5rem;">98%</div>
                    <div style="font-size: 1rem; opacity: 0.9;">準確率</div>
                    <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">vs 人工85%</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
                    <div style="font-size: 2rem; font-weight: 900; margin-bottom: 0.5rem;">90%</div>
                    <div style="font-size: 1rem; opacity: 0.9;">時間節省</div>
                    <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">每月省10+小時</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 新增区域2：成本控制策略 -->
<section style="padding: 5rem 0; background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);">
    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
            💰 {industry_name}成本控制的黃金法則
        </h2>
        <p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
            利用VaultCaddy的數據分析功能，幫助{industry_name}實現精準成本控制
        </p>

        <!-- 成本控制图片 -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <img alt="{industry_name}成本控制與利潤分析" loading="lazy" src="https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 1rem;">支出追蹤</h3>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #4b5563;">自動分類所有支出項目，實時監控成本變化</p>
            </div>
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 1rem;">收入分析</h3>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #4b5563;">追蹤每月收入趨勢，識別淡旺季規律</p>
            </div>
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💵</div>
                <h3 style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 1rem;">利潤優化</h3>
                <p style="font-size: 0.95rem; line-height: 1.6; color: #4b5563;">發現隱藏成本，提升整體利潤率</p>
            </div>
        </div>
    </div>
</section>

<!-- 新增区域3：報稅與合規 -->
<section style="padding: 5rem 0; background: white;">
    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
            📋 {industry_name}報稅與會計合規
        </h2>
        <p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
            香港{industry_name}必須遵守的稅務規定，VaultCaddy幫您輕鬆合規
        </p>

        <!-- 报税合规图片 -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <img alt="{industry_name}報稅與會計合規管理" loading="lazy" src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;">
            <div style="text-align: center; padding: 2rem 1rem; background: #f0f9ff; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                <h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">利得稅</h3>
                <p style="font-size: 0.85rem; color: #6b7280;">自動計算應繳稅額</p>
            </div>
            <div style="text-align: center; padding: 2rem 1rem; background: #f0fdf4; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
                <h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">發票管理</h3>
                <p style="font-size: 0.85rem; color: #6b7280;">365天雲端保存</p>
            </div>
            <div style="text-align: center; padding: 2rem 1rem; background: #fef3c7; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
                <h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">強積金</h3>
                <p style="font-size: 0.85rem; color: #6b7280;">自動計算供款</p>
            </div>
            <div style="text-align: center; padding: 2rem 1rem; background: #fce7f3; border-radius: 12px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                <h3 style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">合規報告</h3>
                <p style="font-size: 0.85rem; color: #6b7280;">一鍵生成</p>
            </div>
        </div>
    </div>
</section>

<!-- 新增区域4：數碼化轉型 -->
<section style="padding: 5rem 0; background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);">
    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
            🚀 {industry_name}數碼化轉型路線圖
        </h2>
        <p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
            從傳統記賬到數碼化管理，VaultCaddy陪伴您的轉型之旅
        </p>

        <!-- 数码化转型图片 -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <img alt="{industry_name}數碼化轉型與智能管理" loading="lazy" src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem;">
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">1️⃣</div>
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem;">第1個月</h3>
                <p style="font-size: 0.9rem; color: #6b7280;">開始記錄日常收據</p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">2️⃣</div>
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #10b981; margin-bottom: 0.5rem;">第2-3個月</h3>
                <p style="font-size: 0.9rem; color: #6b7280;">流程優化自動化</p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">3️⃣</div>
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">第4-6個月</h3>
                <p style="font-size: 0.9rem; color: #6b7280;">數據驅動決策</p>
            </div>
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">4️⃣</div>
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #8b5cf6; margin-bottom: 0.5rem;">6個月後</h3>
                <p style="font-size: 0.9rem; color: #6b7280;">全面智能化</p>
            </div>
        </div>
    </div>
</section>

<!-- 新增区域5：VaultCaddy vs 競爭對手 -->
<section style="padding: 5rem 0; background: white;">
    <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1.5rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f2937;">
            🏆 為什麼選擇VaultCaddy？
        </h2>
        <p style="text-align: center; font-size: 1.2rem; color: #6b7280; max-width: 800px; margin: 0 auto 3rem;">
            專為香港{industry_name}設計的財務管理解決方案
        </p>

        <!-- 对比图片 -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <img alt="VaultCaddy與競爭對手功能對比" loading="lazy" src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1200&h=600&fit=crop" style="max-width: 100%; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);"/>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3rem;">
            <div style="text-align: center; padding: 2rem; background: #f0f9ff; border-radius: 16px;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">💰</div>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">價格親民</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #667eea; margin-bottom: 0.5rem;">HK$46/月</div>
                <p style="font-size: 0.9rem; color: #6b7280;">比Dext便宜83%</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: #f0fdf4; border-radius: 16px;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">極速處理</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #10b981; margin-bottom: 0.5rem;">3秒</div>
                <p style="font-size: 0.9rem; color: #6b7280;">vs 競品15-20秒</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: #fef3c7; border-radius: 16px;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🇭🇰</div>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">本地化</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #f59e0b; margin-bottom: 0.5rem;">100%</div>
                <p style="font-size: 0.9rem; color: #6b7280;">香港銀行+廣東話支援</p>
            </div>
        </div>

        <div style="text-align: center; background: #f9fafb; padding: 2rem; border-radius: 12px;">
            <p style="font-size: 1.1rem; color: #4b5563; margin-bottom: 1.5rem;">
                <strong style="color: #667eea;">超過200+香港{industry_name}的選擇</strong>
            </p>
            <a href="https://vaultcaddy.com/auth.html" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                免費試用20頁 →
            </a>
            <p style="margin-top: 1rem; color: #6b7280; font-size: 0.9rem;">無需信用卡 | 3秒看到效果</p>
        </div>
    </div>
</section>
'''
    
    return sections

# 行业名称和emoji映射
INDUSTRY_INFO = {
    'restaurant': ('餐廳', '🍽️'),
    'retail': ('零售店', '🛍️'),
    'beauty': ('美容院', '💄'),
    'cleaning': ('清潔服務', '🧹'),
    'pet': ('寵物服務', '🐾'),
    'travel': ('旅行社', '✈️'),
    'event': ('活動策劃', '🎉'),
    'coworking': ('共享辦公', '🏢'),
    'property': ('物業管理', '🏘️'),
    'delivery': ('配送服務', '🚗'),
    'healthcare': ('醫療保健', '🏥'),
    'accountant': ('會計師事務所', '📊'),
    'lawyer': ('律師事務所', '⚖️'),
    'consultant': ('顧問服務', '💡'),
    'marketing': ('營銷機構', '📱'),
    'realestate': ('房地產', '🏠'),
    'designer': ('設計師', '🎨'),
    'developer': ('開發者', '💻'),
    'photographer': ('攝影師', '📸'),
    'tutor': ('補習老師', '📚'),
    'fitness': ('健身教練', '💪'),
    'artist': ('藝術家', '🎭'),
    'musician': ('音樂家', '🎵'),
    'freelancer': ('自由職業者', '🌟'),
    'contractor': ('承包商', '🔨'),
    'smallbiz': ('小型企業', '🏢'),
    'startup': ('創業公司', '🚀'),
    'ecommerce': ('電商企業', '🛒'),
    'finance': ('個人理財', '💰'),
    'nonprofit': ('非營利組織', '❤️'),
    'education': ('教育機構', '🎓'),
}

def get_industry_name(filename):
    """从文件名提取行业信息"""
    filename_lower = filename.lower()
    for key, (name, emoji) in INDUSTRY_INFO.items():
        if key in filename_lower:
            return name, emoji
    return '企業', '🏢'

def optimize_industry_page(file_path):
    """优化单个行业页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经优化过
        if '<!-- 新增区域1：' in content and '財務管理完整流程 -->' in content:
            print(f"  ⏭️  已优化，跳过: {file_path.name}")
            return False
        
        # 获取行业信息
        industry_name, industry_emoji = get_industry_name(file_path.name)
        
        # 生成5个内容区域
        sections = get_industry_sections(industry_name, industry_emoji)
        
        # 查找插入位置
        inserted = False
        
        # 尝试在FAQ前插入
        faq_patterns = [
            r'(<section[^>]*class="faq-section")',
            r'(<section[^>]*style="[^"]*padding:[^"]*background:\s*#f9fafb[^"]*">.*?<h2[^>]*>.*?常見問題)',
            r'(<section[^>]*style="[^"]*padding:[^"]*background:\s*#f9fafb[^"]*">.*?<h2[^>]*>.*?FAQ)',
        ]
        
        for faq_pattern in faq_patterns:
            if re.search(faq_pattern, content, re.DOTALL | re.IGNORECASE):
                content = re.sub(
                    faq_pattern,
                    sections + '\n' + r'\1',
                    content,
                    count=1,
                    flags=re.DOTALL | re.IGNORECASE
                )
                inserted = True
                break
        
        # 尝试在CTA section前插入
        if not inserted:
            cta_pattern = r'(<section[^>]*class="cta-section")'
            if re.search(cta_pattern, content):
                content = re.sub(
                    cta_pattern,
                    sections + '\n' + r'\1',
                    content,
                    count=1
                )
                inserted = True
        
        # 在</body>前插入（兜底）
        if not inserted:
            body_pattern = r'(</body>)'
            if re.search(body_pattern, content, re.IGNORECASE):
                content = re.sub(
                    body_pattern,
                    sections + '\n' + r'\1',
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
        
        print(f"  ✅ 优化完成: {file_path.name} ({industry_name})")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误 {file_path.name}: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量优化行业Landing Page...")
    print("📱 包含手机版响应式优化")
    print("=" * 60)
    
    # 统计
    total = 0
    success = 0
    skipped = 0
    failed = 0
    
    # 优化中文版行业页面
    print("\n📄 处理中文版行业页面...")
    industry_files = list(BASE_DIR.glob('*-accounting-solution.html'))
    for file_path in sorted(industry_files):
        total += 1
        result = optimize_industry_page(file_path)
        if result:
            success += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1
    
    # 优化多语言版行业页面
    for lang in ['en', 'kr', 'jp']:
        lang_dir = BASE_DIR / lang
        if lang_dir.exists():
            print(f"\n📄 处理{lang}版行业页面...")
            industry_files = list(lang_dir.glob('*-accounting-solution.html'))
            for file_path in sorted(industry_files):
                total += 1
                result = optimize_industry_page(file_path)
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

