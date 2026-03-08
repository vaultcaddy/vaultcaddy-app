#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有450个v3页面添加hreflang标签
确保搜索引擎正确理解多语言版本关系
"""

import os
import re
from pathlib import Path

class HreflangAdder:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.updated_count = {'en': 0, 'zh-TW': 0, 'zh-HK': 0, 'ja-JP': 0, 'ko-KR': 0}
        
        # 语言配置
        self.lang_config = {
            'en': {'dir': '', 'hreflang': 'en'},
            'zh-TW': {'dir': 'zh-TW', 'hreflang': 'zh-TW'},
            'zh-HK': {'dir': 'zh-HK', 'hreflang': 'zh-HK'},
            'ja-JP': {'dir': 'ja-JP', 'hreflang': 'ja'},
            'ko-KR': {'dir': 'ko-KR', 'hreflang': 'ko'}
        }
        
        self.base_url = 'https://vaultcaddy.com'
    
    def generate_hreflang_tags(self, filename):
        """生成完整的hreflang标签集合"""
        tags = []
        
        # 为每种语言生成标签
        for lang, config in self.lang_config.items():
            if config['dir']:
                url = f"{self.base_url}/{config['dir']}/{filename}"
            else:
                url = f"{self.base_url}/{filename}"
            
            tag = f'    <link rel="alternate" hreflang="{config["hreflang"]}" href="{url}" />'
            tags.append(tag)
        
        # 添加x-default标签（指向英文版）
        default_tag = f'    <link rel="alternate" hreflang="x-default" href="{self.base_url}/{filename}" />'
        tags.append(default_tag)
        
        return '\n'.join(tags)
    
    def add_hreflang_to_file(self, file_path, lang_key):
        """为单个文件添加hreflang标签"""
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有hreflang标签
            if 'rel="alternate" hreflang=' in content:
                # 如果已存在，先删除旧的
                content = re.sub(
                    r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n?',
                    '',
                    content
                )
            
            # 生成hreflang标签
            filename = file_path.name
            hreflang_tags = self.generate_hreflang_tags(filename)
            
            # 在</head>之前插入hreflang标签
            if '</head>' in content:
                # 添加注释和标签
                hreflang_section = f'\n    <!-- Hreflang Tags for Multilingual SEO -->\n{hreflang_tags}\n'
                content = content.replace('</head>', f'{hreflang_section}</head>')
            else:
                print(f"  ⚠️ 找不到</head>标签: {file_path.name}")
                return False
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.updated_count[lang_key] += 1
            return True
            
        except Exception as e:
            print(f"  ❌ 失败: {file_path.name} - {e}")
            return False
    
    def process_all_files(self):
        """处理所有v3文件"""
        print("🚀 开始添加Hreflang标签...")
        print("=" * 80)
        
        # 处理英文版（根目录）
        print(f"\n{'='*80}")
        print("处理英文版 (en)...")
        print(f"{'='*80}")
        
        en_files = list(self.root_dir.glob('*-v3.html'))
        en_files = [f for f in en_files if 'test' not in f.name and 'backup' not in f.name]
        
        for i, file_path in enumerate(en_files, 1):
            if i % 10 == 0:
                print(f"  进度: {i}/{len(en_files)}")
            self.add_hreflang_to_file(file_path, 'en')
        
        print(f"  ✅ 完成: {self.updated_count['en']}个页面")
        
        # 处理其他语言版本
        for lang_key, config in self.lang_config.items():
            if lang_key == 'en':
                continue
            
            print(f"\n{'='*80}")
            print(f"处理{lang_key}版本...")
            print(f"{'='*80}")
            
            lang_dir = self.root_dir / config['dir']
            if not lang_dir.exists():
                print(f"  ⚠️ 目录不存在: {lang_dir}")
                continue
            
            lang_files = list(lang_dir.glob('*-v3.html'))
            lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
            
            for i, file_path in enumerate(lang_files, 1):
                if i % 10 == 0:
                    print(f"  进度: {i}/{len(lang_files)}")
                self.add_hreflang_to_file(file_path, lang_key)
            
            print(f"  ✅ 完成: {self.updated_count[lang_key]}个页面")
        
        print("\n" + "=" * 80)
        print("🎉 Hreflang标签添加完成！")
        print("=" * 80)
        print(f"\n📊 统计:")
        for lang, count in self.updated_count.items():
            print(f"   {lang}: {count}个页面")
        print(f"\n总计: {sum(self.updated_count.values())} 个页面已添加hreflang标签")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🌍 Hreflang标签批量添加                                    ║
║                                                                              ║
║  添加内容:                                                                   ║
║    ✓ 英文版 (en) - hreflang="en"                                             ║
║    ✓ 台湾版 (zh-TW) - hreflang="zh-TW"                                       ║
║    ✓ 香港版 (zh-HK) - hreflang="zh-HK"                                       ║
║    ✓ 日文版 (ja-JP) - hreflang="ja"                                          ║
║    ✓ 韩文版 (ko-KR) - hreflang="ko"                                          ║
║    ✓ 默认版 - hreflang="x-default" → 英文版                                  ║
║                                                                              ║
║  SEO效果:                                                                    ║
║    ✓ 告诉搜索引擎不同语言版本的关系                                          ║
║    ✓ 避免重复内容惩罚                                                        ║
║    ✓ 正确的地理定位                                                          ║
║    ✓ 提高本地搜索排名                                                        ║
║                                                                              ║
║  目标: 450个页面                                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    adder = HreflangAdder(root_dir)
    adder.process_all_files()
    
    print("\n" + "=" * 80)
    print("✅ 所有页面的hreflang标签添加完成！")
    print("=" * 80)
    print("\n下一步: 批量添加更多本地化内容")

if __name__ == '__main__':
    main()

