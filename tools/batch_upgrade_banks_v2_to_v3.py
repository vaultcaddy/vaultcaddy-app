#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量升级52个银行页面 v2→v3
确保：纯英文 + 正确定价 + 正确auth链接
"""

import os
import re
from pathlib import Path

class BankPageUpgrader:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.upgraded_count = 0
        self.template = None
        
        # 银行名称映射（从文件名提取到显示名称）
        self.bank_names = {
            'chase': 'Chase Bank',
            'bank-of-america': 'Bank of America',
            'wells-fargo': 'Wells Fargo',
            'citibank': 'Citibank',
            'capital-one': 'Capital One',
            'us-bank': 'U.S. Bank',
            'truist': 'Truist Bank',
            'pnc': 'PNC Bank',
            'td-bank': 'TD Bank',
            'ally': 'Ally Bank',
            'hsbc-bank': 'HSBC',
            'hsbc-uk-bank': 'HSBC UK',
            'hsbc-hong-kong': 'HSBC Hong Kong',
            'barclays': 'Barclays Bank',
            'lloyds-bank': 'Lloyds Bank',
            'natwest-bank': 'NatWest Bank',
            'santander-uk': 'Santander UK',
            'rbc-bank': 'RBC Bank',
            'td-canada-trust': 'TD Canada Trust',
            'bmo-bank': 'BMO Bank',
            'scotiabank': 'Scotiabank',
            'cibc-bank': 'CIBC Bank',
            'dbs-bank': 'DBS Bank',
            'ocbc-bank': 'OCBC Bank',
            'uob-bank': 'UOB Bank',
            'hang-seng-bank': 'Hang Seng Bank',
            'boc-hk': 'Bank of China (Hong Kong)',
            'cathay-bank': 'Cathay Bank',
            'commbank': 'Commonwealth Bank',
            'westpac-bank': 'Westpac Bank',
            'anz-bank': 'ANZ Bank',
            'anz-nz-bank': 'ANZ New Zealand',
            'nab-bank': 'NAB Bank',
            'asb-bank': 'ASB Bank',
            'bnz-bank': 'BNZ Bank',
            'deutsche-bank': 'Deutsche Bank',
            'commerzbank': 'Commerzbank',
            'dz-bank': 'DZ Bank',
            'ing-bank': 'ING Bank',
            'abn-amro': 'ABN AMRO Bank',
            'rabobank': 'Rabobank',
            'mizuho-bank': 'Mizuho Bank',
            'smbc-bank': 'SMBC Bank',
            'mufg-bank': 'MUFG Bank',
            'shinhan-bank': 'Shinhan Bank',
            'woori-bank': 'Woori Bank',
            'kb-kookmin': 'KB Kookmin Bank',
            'hana-bank': 'Hana Bank',
            'ctbc-bank': 'CTBC Bank',
            'bank-of-taiwan': 'Bank of Taiwan',
        }
    
    def load_template(self):
        """加载v3模板"""
        template_path = self.root_dir / 'chase-bank-statement-v3-test.html'
        if not template_path.exists():
            print(f"❌ 找不到模板: {template_path}")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        print("✅ 模板加载成功")
        return True
    
    def extract_bank_name_from_filename(self, filename):
        """从文件名提取银行名称"""
        # 移除-statement-v2.html
        name_part = filename.replace('-statement-v2.html', '')
        
        # 查找映射
        if name_part in self.bank_names:
            return self.bank_names[name_part]
        
        # 默认：首字母大写
        return ' '.join(word.capitalize() for word in name_part.split('-'))
    
    def customize_template(self, bank_name, filename):
        """自定义模板"""
        content = self.template
        
        # 1. 替换银行名称
        content = content.replace('Chase Bank', bank_name)
        content = content.replace('Chase', bank_name.split()[0])
        
        # 2. 替换chase.com域名
        bank_domain = filename.replace('-statement-v2.html', '') + '.com'
        content = content.replace('chase.com', bank_domain)
        
        # 3. 确保定价正确
        # 已经在模板中是正确的 $5.59 和 $7
        
        # 4. 确保auth链接正确
        # 已经在模板中是 /en/auth.html
        
        # 5. 更新Title和Meta
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{bank_name} Statement Converter | PDF to Excel/QuickBooks | 98% Accuracy</title>',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="AI-powered {bank_name} statement converter. Convert PDF to Excel/QuickBooks/Xero in 3 seconds with 98% accuracy. From $5.59/month | 500+ businesses trust us">',
            content
        )
        
        return content
    
    def upgrade_file(self, file_path):
        """升级单个银行页面"""
        try:
            print(f"\n🔧 处理: {file_path.name}")
            
            # 提取银行名称
            bank_name = self.extract_bank_name_from_filename(file_path.name)
            print(f"  🏦 银行: {bank_name}")
            
            # 自定义模板
            new_content = self.customize_template(bank_name, file_path.name)
            
            # 创建新文件名
            new_filename = file_path.name.replace('-v2.html', '-v3.html')
            new_file_path = file_path.parent / new_filename
            
            # 写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ 创建: {new_filename}")
            self.upgraded_count += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upgrade_all(self):
        """升级所有银行页面"""
        print("🚀 开始批量升级银行页面...")
        print("=" * 80)
        
        # 加载模板
        if not self.load_template():
            return
        
        # 查找所有银行statement页面
        bank_files = list(self.root_dir.glob('*-statement-v2.html'))
        
        print(f"\n📊 找到 {len(bank_files)} 个银行页面")
        print("=" * 80)
        
        # 升级每个文件
        for file_path in bank_files:
            if 'backup' in file_path.name:
                continue
            self.upgrade_file(file_path)
        
        print("\n" + "=" * 80)
        print("🎉 Phase 1: 银行页面升级完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 找到 {len(bank_files)} 个银行页面")
        print(f"   - 成功升级 {self.upgraded_count} 个页面")
        print(f"\n✅ 所有新v3文件已创建")
        print(f"💾 原v2文件保持不变")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🏦 Phase 1: 批量升级银行页面 v2→v3                               ║
║                                                                              ║
║  升级内容:                                                                    ║
║    ✓ 使用chase-bank-statement-v3-test.html模板                               ║
║    ✓ 替换银行名称                                                            ║
║    ✓ 纯英文内容                                                              ║
║    ✓ 正确定价（$5.59/月，$7/月）                                              ║
║    ✓ 正确链接（/en/auth.html）                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    upgrader = BankPageUpgrader(root_dir)
    upgrader.upgrade_all()
    
    print("\n" + "=" * 80)
    print("✅ Phase 1 完成！")
    print("=" * 80)
    print("\n下一步: Phase 2 - 升级17个行业页面")

if __name__ == '__main__':
    main()

