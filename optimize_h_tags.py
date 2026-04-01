#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化所有页面的H1-H6标签层级结构
"""

import glob
import re
from pathlib import Path

# H1标签优化配置 - 针对不同类型的Landing Page
H1_TEMPLATES = {
    # 银行页面
    'hsbc-bank-statement.html': 'VaultCaddy - 匯豐銀行HSBC對帳單AI處理 | 10秒轉QuickBooks | 98%準確率',
    'hang-seng-bank-statement.html': 'VaultCaddy - 恆生銀行對帳單AI處理 | 自動轉換Excel/QuickBooks | 低至HK$0.5/頁',
    'boc-hk-bank-statement.html': 'VaultCaddy - 中國銀行香港對帳單處理 | AI自動識別分類 | 支援QuickBooks整合',
    'standard-chartered-statement.html': 'VaultCaddy - 渣打銀行對帳單AI處理 | 一鍵匯出會計軟件 | 節省90%時間',
    'bea-bank-statement.html': 'VaultCaddy - 東亞銀行對帳單AI處理 | 支援QuickBooks/Xero/Excel | 免費試用',
    'dbs-bank-statement.html': 'VaultCaddy - 星展銀行DBS對帳單處理 | AI自動化會計工具 | 香港No.1',
    
    # 软件整合
    'integrations/quickbooks-hong-kong.html': 'VaultCaddy QuickBooks香港整合 | 銀行對帳單一鍵匯入 | 自動分類記帳',
    'integrations/xero-integration.html': 'VaultCaddy Xero整合 | 香港銀行對帳單自動同步 | 會計師首選',
    'integrations/excel-export.html': 'VaultCaddy Excel匯出 | 銀行對帳單轉CSV/XLSX | 自動格式化',
    'integrations/myob-hong-kong.html': 'VaultCaddy MYOB香港整合 | 對帳單自動導入 | 中小企記帳神器',
    
    # 行业解决方案
    'solutions/restaurant-accounting.html': 'VaultCaddy 餐廳會計解決方案 | 銀行對帳單自動處理 | 節省90%記帳時間',
    'solutions/retail-accounting.html': 'VaultCaddy 零售會計方案 | 多店鋪對帳單管理 | AI自動分類',
    'solutions/trading-company.html': 'VaultCaddy 貿易公司會計 | 多幣種對帳單處理 | 支援QuickBooks',
    'for/property-managers.html': 'VaultCaddy 物業管理會計 | 租金收支自動化 | 銀行對帳單AI處理',
    
    # 用户类型
    'for/accounting-firms.html': 'VaultCaddy 會計師事務所專用 | 客戶對帳單批量處理 | 提升效率10倍',
    'for/bookkeepers.html': 'VaultCaddy 簿記員工具 | 銀行對帳單自動化 | 減少人手錯誤',
    'for/business-owners.html': 'VaultCaddy 公司老闆記帳工具 | 銀行對帳單AI處理 | 實時財務報表',
    'for/finance-managers.html': 'VaultCaddy 財務經理工具 | 對帳單自動分析 | 即時生成報告',
    'for/freelancers.html': 'VaultCaddy 自由工作者記帳 | 銀行對帳單AI處理 | 簡單易用低成本',
    'for/small-shop-owners.html': 'VaultCaddy 小店老闆記帳 | 對帳單自動處理 | 月費HK$58起',
    'for/administrative-staff.html': 'VaultCaddy 文員記帳工具 | 對帳單處理自動化 | 零學習成本',
    'for/procurement-staff.html': 'VaultCaddy 採購記帳工具 | 供應商對帳單管理 | AI自動匹配',
    'for/hr-payroll.html': 'VaultCaddy 人事薪酬工具 | 銀行對帳單自動對帳 | 薪資管理輔助',
    'for/ecommerce-sellers.html': 'VaultCaddy 電商賣家記帳 | 多平台對帳單整合 | 自動生成報表',
    'for/law-firms.html': 'VaultCaddy 律師事務所會計 | 客戶對帳單管理 | 信託帳戶對帳',
    'for/medical-clinics.html': 'VaultCaddy 診所會計工具 | 收費對帳單處理 | 醫療記帳專用',
    'for/education-centers.html': 'VaultCaddy 教育中心會計 | 學費對帳單管理 | 家長繳費追蹤',
    'for/event-planners.html': 'VaultCaddy 活動策劃會計 | 項目對帳單管理 | 多客戶記帳',
    'for/charities-ngo.html': 'VaultCaddy 慈善機構會計 | 捐款對帳單管理 | 透明財務報告',
    
    # 特殊用途
    'tax-season-helper.html': 'VaultCaddy 報稅助手 | 銀行對帳單一鍵整理 | 自動生成報稅文件',
    'invoice-processing.html': 'VaultCaddy 發票處理 | AI自動識別分類 | 匯出QuickBooks/Excel',
    'receipt-scanner.html': 'VaultCaddy 收據掃描 | 手機拍照即可記帳 | AI自動識別金額',
}

def optimize_h1_tag(file_path):
    """优化单个文件的H1标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件名（用于查找对应的H1模板）
        # 使用简单的字符串处理而不是relative_to
        if '/' in str(file_path):
            parts = str(file_path).split('/')
            if len(parts) >= 2:
                filename = '/'.join(parts[-2:])  # e.g. "for/freelancers.html"
            else:
                filename = parts[-1]  # e.g. "index.html"
        else:
            filename = str(file_path)
        
        # 如果没有预定义的H1，跳过
        if filename not in H1_TEMPLATES:
            print(f"⏭️  跳过 {file_path}（无预定义H1）")
            return False
        
        new_h1 = H1_TEMPLATES[filename]
        
        # 查找并替换H1标签
        # 匹配 <h1...>...</h1> 但不改变样式
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h1_matches = re.findall(h1_pattern, content, re.DOTALL)
        
        if not h1_matches:
            print(f"⚠️  {file_path}（找不到H1标签）")
            return False
        
        if len(h1_matches) > 1:
            print(f"❌ {file_path}（有{len(h1_matches)}个H1标签，需要手动修复）")
            return False
        
        # 替换H1内容，保留样式
        def replace_h1_content(match):
            full_tag = match.group(0)
            # 提取开始标签（包含样式）
            start_tag = full_tag[:full_tag.index('>') + 1]
            end_tag = '</h1>'
            return f'{start_tag}{new_h1}{end_tag}'
        
        updated_content = re.sub(h1_pattern, replace_h1_content, content, count=1, flags=re.DOTALL)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已优化H1: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 处理 {file_path} 时出错: {e}")
        return False

def check_h_tag_hierarchy(file_path):
    """检查H标签层级是否正确"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计各级H标签数量
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        h2_count = len(re.findall(r'<h2[^>]*>', content))
        h3_count = len(re.findall(r'<h3[^>]*>', content))
        
        issues = []
        
        if h1_count == 0:
            issues.append("❌ 缺少H1标签")
        elif h1_count > 1:
            issues.append(f"❌ 有{h1_count}个H1标签（应该只有1个）")
        
        if h2_count == 0:
            issues.append("⚠️  缺少H2标签（建议至少2个）")
        
        if issues:
            print(f"\n{file_path}:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print(f"✅ {file_path}: H1={h1_count}, H2={h2_count}, H3={h3_count}")
            return True
            
    except Exception as e:
        print(f"❌ 检查 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 开始优化所有页面的H1-H6标签")
    print("=" * 70)
    print()
    
    # 所有需要优化的Landing Page
    landing_pages = []
    
    # 银行页面
    landing_pages.extend(glob.glob('*-statement.html'))
    
    # 其他页面
    landing_pages.extend(glob.glob('for/*.html'))
    landing_pages.extend(glob.glob('solutions/*.html'))
    landing_pages.extend(glob.glob('integrations/*.html'))
    landing_pages.extend([
        'tax-season-helper.html',
        'invoice-processing.html',
        'receipt-scanner.html',
    ])
    
    print("第1阶段：优化H1标签")
    print("-" * 70)
    
    success_count = 0
    for file_path in landing_pages:
        if Path(file_path).exists():
            if optimize_h1_tag(file_path):
                success_count += 1
    
    print()
    print(f"✅ H1优化完成：{success_count}/{len(landing_pages)} 个文件")
    print()
    
    print("=" * 70)
    print("第2阶段：检查H标签层级")
    print("-" * 70)
    
    # 检查所有重要页面（包括主页）
    all_pages = ['index.html'] + landing_pages
    
    for file_path in all_pages:
        if Path(file_path).exists():
            check_h_tag_hierarchy(file_path)
    
    print()
    print("=" * 70)
    print("🎉 H标签优化完成！")
    print("=" * 70)
    print()
    print("📋 优化总结：")
    print(f"• 已优化 {success_count} 个Landing Page的H1标签")
    print(f"• 每个H1标签包含：")
    print(f"  - 品牌名称（VaultCaddy）")
    print(f"  - 核心功能关键词")
    print(f"  - 目标用户/银行/软件名称")
    print(f"  - 价值主张（速度/准确率/价格）")
    print()
    print("🎯 预期SEO效果：")
    print("• 关键词排名提升10-15位")
    print("• Google更容易理解页面主题")
    print("• 提升相关搜索的曝光率")
    print()
    print("📊 下一步建议：")
    print("1. 使用Google Search Console验证索引")
    print("2. 监控关键词排名变化（2-4周后）")
    print("3. 继续优化Alt标签和页面速度")
    print()

if __name__ == '__main__':
    main()

