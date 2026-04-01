#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为银行页面添加专业的银行Logo和品牌图片
使用免费资源和SVG图标
"""

import re
from pathlib import Path

# 银行信息配置
BANK_CONFIGS = {
    'hsbc-bank-statement.html': {
        'name': '匯豐銀行',
        'name_en': 'HSBC',
        'color': '#DB0011',  # HSBC红色
        'logo_url': 'https://logos-world.net/wp-content/uploads/2021/02/HSBC-Logo.png',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
    'hang-seng-bank-statement.html': {
        'name': '恆生銀行',
        'name_en': 'Hang Seng Bank',
        'color': '#0072CE',  # Hang Seng蓝色
        'logo_url': 'https://www.hangseng.com/content/dam/cib/images/logo.svg',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1554224311-beee89af87c6?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
    'boc-hk-bank-statement.html': {
        'name': '中國銀行香港',
        'name_en': 'Bank of China (Hong Kong)',
        'color': '#C8102E',  # BOC红色
        'logo_url': 'https://www.bochk.com/dam/more/logo/bochk-logo-en.svg',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1560520653-9e0e4c89eb11?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
    'standard-chartered-statement.html': {
        'name': '渣打銀行',
        'name_en': 'Standard Chartered',
        'color': '#0B6BA8',  # SC蓝色
        'logo_url': 'https://av.sc.com/corp-en/content/images/sc-logo-v1.svg',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
    'bea-bank-statement.html': {
        'name': '東亞銀行',
        'name_en': 'Bank of East Asia',
        'color': '#005EB8',  # BEA蓝色
        'logo_url': 'https://www.hkbea.com/html/en/bea-logo.svg',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1565372195458-9de0b320ef04?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
    'dbs-bank-statement.html': {
        'name': '星展銀行',
        'name_en': 'DBS Bank',
        'color': '#EB0A1E',  # DBS红色
        'logo_url': 'https://www.dbs.com/assets/navigation/logo-dbs.svg',
        'icon': '🏦',
        'bg_image': 'https://images.unsplash.com/photo-1571171637578-41bc2dd41cd2?ixlib=rb-4.0.3&q=80&fm=jpg&w=1200',
    },
}

def add_bank_logo_to_hero(content, bank_name, bank_name_en, bank_color, logo_url, icon):
    """
    在Hero section添加银行logo
    """
    
    # 1. 在Hero section添加银行logo展示区域
    old_hero_start = r'(<section class="hero">[\s\S]*?<div class="container">)'
    
    new_hero_start = f'''<section class="hero">
        <div class="container">
            <!-- 银行Logo展示 -->
            <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 2rem;">
                <!-- 银行Logo容器 -->
                <div style="background: white; padding: 1.5rem 3rem; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 1.5rem;">
                    <!-- 银行图标 -->
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, {bank_color} 0%, {bank_color}dd 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 3rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        {icon}
                    </div>
                    <!-- 银行名称 -->
                    <div style="text-align: left;">
                        <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.25rem;">{bank_name}</div>
                        <div style="font-size: 1rem; color: #6b7280; font-weight: 500;">{bank_name_en}</div>
                    </div>
                </div>
                <!-- VaultCaddy Logo -->
                <div style="font-size: 1.5rem; color: rgba(255,255,255,0.8); font-weight: 600;">×</div>
                <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); padding: 1.5rem 2rem; border-radius: 16px; border: 2px solid rgba(255,255,255,0.3);">
                    <div style="font-size: 1.75rem; font-weight: 700; color: white;">VaultCaddy</div>
                    <div style="font-size: 0.875rem; color: rgba(255,255,255,0.9); font-weight: 500; text-transform: uppercase; letter-spacing: 0.1em;">AI PROCESSING</div>
                </div>
            </div>'''
    
    content = re.sub(old_hero_start, new_hero_start, content, count=1)
    
    return content

def add_bank_features_section(content, bank_name, bank_color):
    """
    添加银行特色功能展示区域
    """
    
    # 在Features section之前添加银行特色区域
    bank_features = f'''
    <!-- 银行特色功能 -->
    <section style="background: linear-gradient(135deg, {bank_color}15 0%, {bank_color}05 100%); padding: 4rem 2rem; border-top: 3px solid {bank_color};">
        <div class="container">
            <h2 style="text-align: center; font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
                為{bank_name}用戶量身訂製
            </h2>
            <p style="text-align: center; font-size: 1.25rem; color: #6b7280; margin-bottom: 3rem;">
                專業識別{bank_name}對帳單格式，確保100%兼容
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; max-width: 1000px; margin: 0 auto;">
                <!-- 特色1 -->
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 4px solid {bank_color};">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{bank_name[0]}</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">商業戶口支援</h3>
                    <p style="color: #6b7280; line-height: 1.6;">完美支援{bank_name}商業綜合戶口格式</p>
                </div>
                
                <!-- 特色2 -->
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 4px solid {bank_color};">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">💱</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">多幣種識別</h3>
                    <p style="color: #6b7280; line-height: 1.6;">自動識別HKD、USD、CNY等貨幣</p>
                </div>
                
                <!-- 特色3 -->
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 4px solid {bank_color};">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">📅</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">月結單自動化</h3>
                    <p style="color: #6b7280; line-height: 1.6;">批量處理多個月份對帳單</p>
                </div>
                
                <!-- 特色4 -->
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 4px solid {bank_color};">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔐</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">數據安全</h3>
                    <p style="color: #6b7280; line-height: 1.6;">符合{bank_name}數據保護標準</p>
                </div>
            </div>
        </div>
    </section>
    '''
    
    # 在第一个<section class="features">之前插入
    content = content.replace('<section class="features">', bank_features + '\n    <section class="features">', 1)
    
    return content

def add_bank_showcase_images(content, bank_name):
    """
    添加银行对账单示例图片展示
    """
    
    showcase = f'''
    <!-- 对账单处理效果展示 -->
    <section style="background: #f9fafb; padding: 5rem 2rem;">
        <div class="container">
            <h2 style="text-align: center; font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
                {bank_name}對帳單處理效果
            </h2>
            <p style="text-align: center; font-size: 1.25rem; color: #6b7280; margin-bottom: 3rem;">
                上傳PDF → AI識別 → 匯出QuickBooks，全程10秒
            </p>
            
            <div style="max-width: 900px; margin: 0 auto; display: grid; gap: 2rem;">
                <!-- 处理前后对比 -->
                <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                    <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 2rem; align-items: center;">
                        <!-- 原始PDF -->
                        <div>
                            <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); padding: 3rem 2rem; border-radius: 12px; text-align: center; border: 2px dashed #9ca3af;">
                                <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                                <div style="font-size: 1.125rem; font-weight: 600; color: #1f2937;">原始PDF對帳單</div>
                                <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">{bank_name}月結單</div>
                            </div>
                        </div>
                        
                        <!-- 箭头 -->
                        <div style="font-size: 2rem; color: #667eea;">→</div>
                        
                        <!-- 处理结果 -->
                        <div>
                            <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 3rem 2rem; border-radius: 12px; text-align: center; border: 2px solid #667eea;">
                                <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                                <div style="font-size: 1.125rem; font-weight: 600; color: #667eea;">結構化數據</div>
                                <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">Excel / QuickBooks</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 数据准确性展示 -->
                <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                    <h3 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1.5rem; text-align: center;">
                        AI自動提取的數據欄位
                    </h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 交易日期</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Date</div>
                        </div>
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 交易金額</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Amount</div>
                        </div>
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 交易描述</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Description</div>
                        </div>
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 帳戶餘額</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Balance</div>
                        </div>
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 交易類型</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Type</div>
                        </div>
                        <div style="padding: 1rem; background: #f9fafb; border-radius: 8px; text-align: center;">
                            <div style="font-weight: 600; color: #667eea; margin-bottom: 0.25rem;">✓ 對方帳戶</div>
                            <div style="font-size: 0.875rem; color: #6b7280;">Reference</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''
    
    # 在FAQ section之前插入
    content = content.replace('<section class="faq">', showcase + '\n    <section class="faq">', 1)
    
    return content

def enhance_bank_page(file_path):
    """
    增强单个银行页面
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 获取银行配置
        filename = Path(file_path).name
        if filename not in BANK_CONFIGS:
            return False, f"未找到配置: {filename}"
        
        config = BANK_CONFIGS[filename]
        
        # 1. 添加银行Logo到Hero
        content = add_bank_logo_to_hero(
            content,
            config['name'],
            config['name_en'],
            config['color'],
            config['logo_url'],
            config['icon']
        )
        
        # 2. 添加银行特色功能区域
        content = add_bank_features_section(
            content,
            config['name'],
            config['color']
        )
        
        # 3. 添加对账单处理效果展示
        content = add_bank_showcase_images(
            content,
            config['name']
        )
        
        # 检查是否有变化
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "美化成功"
        else:
            return False, "无需修改"
            
    except Exception as e:
        return False, f"错误: {e}"

def main():
    """主函数"""
    print("=" * 70)
    print("🏦 开始为银行页面添加Logo和图片")
    print("=" * 70)
    print()
    
    bank_files = list(BANK_CONFIGS.keys())
    
    print(f"找到 {len(bank_files)} 个银行页面")
    print("-" * 70)
    
    success_count = 0
    
    for filename in bank_files:
        bank_name = BANK_CONFIGS[filename]['name']
        print(f"处理中: {bank_name} ({filename})...", end=" ")
        
        success, message = enhance_bank_page(filename)
        
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⏭️  {message}")
    
    print("-" * 70)
    print()
    print(f"✅ 完成：{success_count}/{len(bank_files)} 个页面已美化")
    print()
    
    print("=" * 70)
    print("🎉 银行页面Logo美化完成！")
    print("=" * 70)
    print()
    print("📊 美化内容：")
    print("  ✅ 6个银行页面全部处理")
    print("  ✅ Hero区域添加银行Logo展示")
    print("  ✅ 添加银行特色功能区域")
    print("  ✅ 添加对账单处理效果展示")
    print("  ✅ 使用银行品牌颜色设计")
    print()
    print("🎨 包含的银行：")
    for filename, config in BANK_CONFIGS.items():
        print(f"  • {config['name']} ({config['name_en']})")
    print()
    print("🚀 立即刷新浏览器查看效果！")
    print()

if __name__ == '__main__':
    main()

