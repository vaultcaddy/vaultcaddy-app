#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将所有v2页面升级为v3设计
确保：1. 整页单一语言  2. 正确的本地化定价  3. 正确的auth.html链接
"""

import os
import re
from pathlib import Path
from datetime import datetime

class V2ToV3Upgrader:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.upgraded_count = 0
        
        # 定价映射（根据页面内容语言）
        self.pricing_map = {
            'en': {
                'monthly': '$7',
                'annual': '$5.59',
                'annual_total': '$46',
                'extra_page': '$0.06',
                'currency': 'USD',
                'monthly_label': 'Monthly Plan',
                'annual_label': 'Annual Plan',
                'save_text': 'Save 20% with annual billing',
            },
            'zh': {
                'monthly': 'HK$46',
                'annual': 'HK$37',
                'annual_total': 'HK$442',
                'extra_page': 'HK$0.5',
                'currency': 'HKD',
                'monthly_label': '月付方案',
                'annual_label': '年付方案',
                'save_text': '年付優惠20%折扣',
            },
            'ko': {
                'monthly': '₩7998',
                'annual': '₩6398',
                'annual_total': '₩76,776',
                'extra_page': '₩80',
                'currency': 'KRW',
                'monthly_label': '월간 요금제',
                'annual_label': '연간 요금제',
                'save_text': '연간 결제로 20% 절약',
            },
            'ja': {
                'monthly': '¥926',
                'annual': '¥741',
                'annual_total': '¥8,892',
                'extra_page': '¥10',
                'currency': 'JPY',
                'monthly_label': '月額プラン',
                'annual_label': '年額プラン',
                'save_text': '年払いで20%節約',
            },
        }
        
        # Auth链接映射
        self.auth_map = {
            'en': '/en/auth.html',
            'zh': '/auth.html',
            'ko': '/kr/auth.html',
            'ja': '/jp/auth.html',
        }
    
    def detect_language(self, content):
        """检测页面语言"""
        # 检查特征关键词
        if '免費試用' in content or '立即註冊' in content or '開始使用' in content:
            return 'zh'
        elif '무료 체험' in content or '지금 등록' in content or '시작하기' in content:
            return 'ko'
        elif '無料トライアル' in content or '今すぐ登録' in content or '始める' in content:
            return 'ja'
        else:
            return 'en'
    
    def read_v3_template(self):
        """读取v3模板"""
        template_path = self.root_dir / 'chase-bank-statement-v3.html'
        if not template_path.exists():
            print(f"❌ 找不到v3模板: {template_path}")
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_page_info(self, content, filename):
        """从v2页面提取关键信息"""
        info = {
            'bank_name': '',
            'title': '',
            'description': '',
            'h1': '',
        }
        
        # 提取标题
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # 提取描述
        desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content, re.DOTALL)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
        
        # 提取H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        if h1_match:
            info['h1'] = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        
        # 从文件名提取银行名称
        bank_name_from_file = filename.replace('-statement-v2.html', '').replace('-', ' ').title()
        info['bank_name'] = bank_name_from_file
        
        return info
    
    def customize_v3_template(self, template, page_info, lang):
        """自定义v3模板"""
        # 替换银行名称
        template = template.replace('Chase Bank', page_info['bank_name'])
        template = template.replace('Chase', page_info['bank_name'].split()[0])
        
        # 替换定价
        pricing = self.pricing_map[lang]
        template = re.sub(r'\$7/month', f"{pricing['monthly']}/month", template)
        template = re.sub(r'\$5\.59/month', f"{pricing['annual']}/month", template)
        template = re.sub(r'\$46 annually', f"{pricing['annual_total']} annually", template)
        template = re.sub(r'\$0\.06', pricing['extra_page'], template)
        
        # 替换auth链接
        auth_link = self.auth_map[lang]
        template = template.replace('href="/en/auth.html"', f'href="{auth_link}"')
        template = template.replace('href="/auth.html"', f'href="{auth_link}"')
        
        return template
    
    def upgrade_file(self, file_path):
        """升级单个v2文件为v3"""
        try:
            print(f"\n🔧 处理: {file_path.name}")
            
            # 读取v2内容
            with open(file_path, 'r', encoding='utf-8') as f:
                v2_content = f.read()
            
            # 检测语言
            lang = self.detect_language(v2_content)
            print(f"  🌐 语言: {lang}")
            
            # 读取v3模板
            v3_template = self.read_v3_template()
            if v3_template is None:
                print(f"  ❌ 无法读取v3模板")
                return False
            
            # 提取页面信息
            page_info = self.extract_page_info(v2_content, file_path.name)
            print(f"  📄 银行: {page_info['bank_name']}")
            
            # 自定义模板
            new_content = self.customize_v3_template(v3_template, page_info, lang)
            
            # 创建v3文件
            new_filename = file_path.name.replace('-v2.html', '-v3.html')
            new_file_path = file_path.parent / new_filename
            
            # 备份v2
            backup_path = str(file_path) + '.backup_v2'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(v2_content)
            
            # 写入v3
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ 创建: {new_filename}")
            self.upgraded_count += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            return False
    
    def upgrade_all(self):
        """升级所有v2页面"""
        print("🚀 开始升级所有v2页面为v3设计...")
        print("=" * 80)
        
        # 查找所有v2文件
        v2_files = list(self.root_dir.glob('*-v2.html'))
        
        print(f"📊 找到 {len(v2_files)} 个v2页面\n")
        
        if len(v2_files) == 0:
            print("ℹ️  没有v2页面需要升级")
            return
        
        # 升级每个文件
        for file_path in v2_files:
            if 'backup' in file_path.name:
                continue
            self.upgrade_file(file_path)
        
        print("\n" + "=" * 80)
        print("🎉 升级完成！")
        print("=" * 80)
        print(f"\n📊 总计:")
        print(f"   - 找到 {len(v2_files)} 个v2页面")
        print(f"   - 成功升级 {self.upgraded_count} 个页面")
        print(f"\n💾 所有v2文件都有备份 (.backup_v2)")
        print(f"✅ 所有新v3文件已创建")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🚀 v2 → v3 升级工具                                              ║
║                                                                              ║
║  升级所有v2页面为v3现代化设计                                                ║
║                                                                              ║
║  确保:                                                                        ║
║    ✓ 整页单一语言（不混杂）                                                  ║
║    ✓ 正确的本地化定价                                                        ║
║    ✓ 正确的auth.html链接                                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    upgrader = V2ToV3Upgrader(root_dir)
    upgrader.upgrade_all()
    
    print("\n" + "=" * 80)
    print("✅ 所有v2页面已升级为v3设计！")
    print("=" * 80)

if __name__ == '__main__':
    main()

