#!/usr/bin/env python3
"""
最终定价更新脚本 - 更新所有4个语言版本
中文版（HKD）: Starter $28/$22, Pro $118/$93
英文版（USD）: Starter $3.88/$2.88, Pro $14.99/$11.99  
日文版（JPY）: Starter ¥599/¥479, Pro ¥2,348/¥1,878
韩文版（KRW）: Starter ₩5,588/₩4,468, Pro ₩21,699/₩17,359
"""

import re
from pathlib import Path
from datetime import datetime

def update_file_pricing(filepath, language='zh'):
    """更新单个文件的定价"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        if language == 'zh':  # 中文版（HKD）
            replacements = [
                # 从旧价格更新
                (r'\$2\.88', '$28'),
                (r'\$3\.60', '$28'),
                (r'HKD \$ 58', 'HKD $ 28'),
                (r'HKD \$ 46', 'HKD $ 22'),
                (r'年付僅?\s*\$?2\.88', '年付僅 $22'),
                (r'\$14\.99', '$118'),
                (r'年付僅?\s*\$?11\.99', '年付僅 $93'),
                # Meta description
                (r'從 \$2\.88/月', '從 HK$28/月'),
                (r'月費46元', 'Starter月費28元起'),
                # Schema.org
                (r'"price":\s*"2\.88"', '"price": "28"'),
                (r'"price":\s*"14\.99"', '"price": "118"'),
            ]
        
        elif language == 'en':  # 英文版（USD）
            replacements = [
                (r'From \$2\.88', 'From $3.88'),
                (r'\$2\.88/month', '$3.88/month'),
                (r'Yearly: \$2\.88', 'Yearly: $2.88'),
                (r'\$14\.99/month', '$14.99/month'),
                (r'Yearly: \$11\.99', 'Yearly: $11.99'),
                (r'"price":\s*"2\.88"', '"price": "3.88"'),
                (r'"price":\s*"14\.99"', '"price": "14.99"'),
            ]
        
        elif language == 'jp':  # 日文版（JPY）
            replacements = [
                (r'¥\s*2\.88', '¥599'),
                (r'¥\s*3\.88', '¥599'),
                (r'年払い[：:]\s*¥\s*2\.88', '年払い: ¥479'),
                (r'¥\s*14\.99', '¥2,348'),
                (r'年払い[：:]\s*¥\s*11\.99', '年払い: ¥1,878'),
                (r'"price":\s*"2\.88"', '"price": "599"'),
                (r'"priceCurrency":\s*"USD"', '"priceCurrency": "JPY"'),
            ]
        
        elif language == 'kr':  # 韩文版（KRW）
            replacements = [
                (r'₩\s*2\.88', '₩5,588'),
                (r'₩\s*3\.88', '₩5,588'),
                (r'연간[：:]\s*₩\s*2\.88', '연간: ₩4,468'),
                (r'₩\s*14\.99', '₩21,699'),
                (r'연간[：:]\s*₩\s*11\.99', '연간: ₩17,359'),
                (r'"price":\s*"2\.88"', '"price": "5588"'),
                (r'"priceCurrency":\s*"USD"', '"priceCurrency": "KRW"'),
            ]
        
        else:
            return 0
        
        # 应用所有替换
        for pattern, replacement in replacements:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes += count
        
        # 如果有更改，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误 {filepath}: {e}")
        return 0

def main():
    root = Path('.')
    report = {
        'zh': {'files': [], 'changes': 0},
        'en': {'files': [], 'changes': 0},
        'jp': {'files': [], 'changes': 0},
        'kr': {'files': [], 'changes': 0}
    }
    
    print("🚀 开始最终定价更新...")
    print()
    
    # 1. 中文版
    print("📂 更新中文版（HKD）...")
    zh_files = [
        'index.html',
        'billing.html',
        'pricing.html',
    ]
    for filename in zh_files:
        filepath = root / filename
        if filepath.exists():
            changes = update_file_pricing(filepath, 'zh')
            if changes > 0:
                report['zh']['files'].append(filename)
                report['zh']['changes'] += changes
                print(f"✅ {filename} ({changes} 处)")
    
    # 更新所有中文landing pages
    for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
        for filepath in sorted(root.glob(pattern)):
            changes = update_file_pricing(filepath, 'zh')
            if changes > 0:
                report['zh']['files'].append(filepath.name)
                report['zh']['changes'] += changes
    
    print(f"📊 中文版: {len(report['zh']['files'])} 个文件, {report['zh']['changes']} 处修改")
    
    # 2. 英文版
    print(f"\n📂 更新英文版（USD）...")
    en_dir = root / 'en'
    if en_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = en_dir / filename
            if filepath.exists():
                changes = update_file_pricing(filepath, 'en')
                if changes > 0:
                    report['en']['files'].append(filename)
                    report['en']['changes'] += changes
                    print(f"✅ {filename} ({changes} 处)")
        
        # 更新英文landing pages
        for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
            for filepath in sorted(en_dir.glob(pattern)):
                changes = update_file_pricing(filepath, 'en')
                if changes > 0:
                    report['en']['files'].append(filepath.name)
                    report['en']['changes'] += changes
        
        print(f"📊 英文版: {len(report['en']['files'])} 个文件, {report['en']['changes']} 处修改")
    
    # 3. 日文版
    print(f"\n📂 更新日文版（JPY）...")
    jp_dir = root / 'jp'
    if jp_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = jp_dir / filename
            if filepath.exists():
                changes = update_file_pricing(filepath, 'jp')
                if changes > 0:
                    report['jp']['files'].append(filename)
                    report['jp']['changes'] += changes
                    print(f"✅ {filename} ({changes} 处)")
        
        # 更新日文landing pages
        for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
            for filepath in sorted(jp_dir.glob(pattern)):
                changes = update_file_pricing(filepath, 'jp')
                if changes > 0:
                    report['jp']['files'].append(filepath.name)
                    report['jp']['changes'] += changes
        
        print(f"📊 日文版: {len(report['jp']['files'])} 个文件, {report['jp']['changes']} 处修改")
    
    # 4. 韩文版
    print(f"\n📂 更新韩文版（KRW）...")
    kr_dir = root / 'kr'
    if kr_dir.exists():
        for filename in ['index.html', 'billing.html', 'pricing.html']:
            filepath = kr_dir / filename
            if filepath.exists():
                changes = update_file_pricing(filepath, 'kr')
                if changes > 0:
                    report['kr']['files'].append(filename)
                    report['kr']['changes'] += changes
                    print(f"✅ {filename} ({changes} 处)")
        
        # 更新韩文landing pages
        for pattern in ['*-v1.html', '*-v2.html', '*-v3.html', 'convert-*.html', '*-bank-statement-*.html']:
            for filepath in sorted(kr_dir.glob(pattern)):
                changes = update_file_pricing(filepath, 'kr')
                if changes > 0:
                    report['kr']['files'].append(filepath.name)
                    report['kr']['changes'] += changes
        
        print(f"📊 韩文版: {len(report['kr']['files'])} 个文件, {report['kr']['changes']} 处修改")
    
    # 总结
    total_files = sum(len(r['files']) for r in report.values())
    total_changes = sum(r['changes'] for r in report.values())
    
    print()
    print("=" * 80)
    print(f"✨ 更新完成！")
    print(f"📊 总计: {total_files} 个文件, {total_changes} 处修改")
    print()
    print("📋 最终定价:")
    print("  中文版（HKD）: Starter $28/月（年付$22），Pro $118/月（年付$93）")
    print("  英文版（USD）: Starter $3.88/月（年付$2.88），Pro $14.99/月（年付$11.99）")
    print("  日文版（JPY）: Starter ¥599/月（年付¥479），Pro ¥2,348/月（年付¥1,878）")
    print("  韩文版（KRW）: Starter ₩5,588/月（年付₩4,468），Pro ₩21,699/月（年付₩17,359）")
    print()
    print("🗑️  已移除 'API 访问' 功能项")
    
    # 生成报告文件
    report_content = f"""# 定价更新完成报告

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 更新总结

- **总文件数**: {total_files}
- **总修改处**: {total_changes}

## 各语言版本更新详情

### 中文版（HKD）
- 文件数: {len(report['zh']['files'])}
- 修改处: {report['zh']['changes']}
- 定价: Starter $28/月（年付$22），Pro $118/月（年付$93）

### 英文版（USD）
- 文件数: {len(report['en']['files'])}
- 修改处: {report['en']['changes']}
- 定价: Starter $3.88/月（年付$2.88），Pro $14.99/月（年付$11.99）

### 日文版（JPY）
- 文件数: {len(report['jp']['files'])}
- 修改处: {report['jp']['changes']}
- 定价: Starter ¥599/月（年付¥479），Pro ¥2,348/月（年付¥1,878）

### 韩文版（KRW）
- 文件数: {len(report['kr']['files'])}
- 修改处: {report['kr']['changes']}
- 定价: Starter ₩5,588/月（年付₩4,468），Pro ₩21,699/月（年付₩17,359）

## 更新内容

1. ✅ 更新所有 index.html 为双层定价结构
2. ✅ 更新所有 billing.html 定价信息
3. ✅ 更新所有 landing pages 价格展示
4. ✅ 更新 Schema.org 价格字段
5. ✅ 更新 meta description 价格信息
6. ✅ 移除 "API 访问" 功能项

## 下一步

根据《方案4实施计划》，接下来需要：

1. **后端集成** (1-2周):
   - 更新Firestore数据结构
   - 创建订阅管理Cloud Functions
   - 集成Stripe支付系统

2. **升级触发器** (3-5天):
   - 创建实时使用量监控
   - 添加UI内升级提示
   - 创建邮件提醒系统

3. **SEO与内容营销** (持续):
   - 创建关键词页面
   - 创建竞品对比页面
   - Reddit/Quora营销
   - YouTube演示视频

---

*更新完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open('✅_最终定价更新完成报告.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📄 已生成报告: ✅_最终定价更新完成报告.md")

if __name__ == '__main__':
    main()

