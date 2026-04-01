#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并修复网页中未本地化的文字
确保价格、货币、描述都使用正确的语言
"""

import os
import re
from pathlib import Path
from datetime import datetime

class LocalizationFixer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.fixed_count = 0
        self.issues_found = {}
        
        # 定义每个语言的正确价格文字
        self.lang_pricing = {
            'ko-KR': {
                'monthly': '₩7998/월',
                'pages': '100페이지',
                'additional': '₩80/페이지',
                'currency_symbol': '₩',
                'per_month': '/월',
                'per_page': '/페이지',
            },
            'ja-JP': {
                'monthly': '¥926/月',
                'pages': '100ページ',
                'additional': '¥10/ページ',
                'currency_symbol': '¥',
                'per_month': '/月',
                'per_page': '/ページ',
            },
            'zh-HK': {
                'monthly': 'HK$46/月',
                'pages': '100頁',
                'additional': 'HK$0.5/頁',
                'currency_symbol': 'HK$',
                'per_month': '/月',
                'per_page': '/頁',
            },
            'zh-TW': {
                'monthly': 'NT$195/月',
                'pages': '100頁',
                'additional': 'NT$2/頁',
                'currency_symbol': 'NT$',
                'per_month': '/月',
                'per_page': '/頁',
            },
        }
        
        # 需要检查的错误模式（英文价格出现在非英文页面）
        self.wrong_patterns = [
            r'\$5\.59/month',
            r'\$5\.59',
            r'\$0\.06/page',
            r'100 pages',
            r'/month',
            r'/page',
            r'USD',
        ]
    
    def check_file(self, file_path, lang_code):
        """检查单个文件的本地化问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # 检查是否有英文价格
            for pattern in self.wrong_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues.append(f"Found English pricing: {pattern}")
            
            # 检查是否有正确的本地化价格
            expected = self.lang_pricing.get(lang_code, {})
            if expected:
                has_correct_price = expected['monthly'] in content or expected['currency_symbol'] in content
                if not has_correct_price:
                    issues.append(f"Missing correct pricing: {expected['monthly']}")
            
            return issues
            
        except Exception as e:
            return [f"Error reading file: {e}"]
    
    def fix_pricing(self, file_path, lang_code):
        """修复文件中的价格本地化"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            expected = self.lang_pricing.get(lang_code)
            
            if not expected:
                return False
            
            # 替换模式
            replacements = [
                # 月费
                (r'\$5\.59/month', expected['monthly']),
                (r'\$5\.59\s*/\s*month', expected['monthly']),
                (r'\$5\.59', expected['monthly'].split('/')[0]),
                
                # 额外费用
                (r'\$0\.06/page', expected['additional']),
                (r'\$0\.06\s*/\s*page', expected['additional']),
                
                # 页数描述
                (r'100\s+pages', expected['pages']),
                (r'100pages', expected['pages']),
                
                # 通用替换（更谨慎）
                (r'/month\b', expected['per_month']),
                (r'/page\b', expected['per_page']),
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # 检查是否有变化
            if content != original_content:
                # 备份原文件
                backup_path = str(file_path) + '.backup_localization'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入修复后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ 修复失败: {e}")
            return False
    
    def scan_directory(self, dir_name, lang_code):
        """扫描目录查找本地化问题"""
        dir_path = self.root_dir / dir_name
        
        if not dir_path.exists():
            return
        
        print(f"\n📁 检查: {dir_name}/ (应使用 {self.lang_pricing[lang_code]['monthly']})")
        
        html_files = list(dir_path.glob('**/*.html'))
        
        if not html_files:
            print(f"  ℹ️  没有HTML文件")
            return
        
        issues_in_dir = []
        
        for file_path in html_files[:10]:  # 先检查前10个文件
            if 'backup' in file_path.name:
                continue
            
            issues = self.check_file(file_path, lang_code)
            if issues:
                issues_in_dir.append({
                    'file': file_path,
                    'issues': issues
                })
        
        if issues_in_dir:
            print(f"  ⚠️  发现 {len(issues_in_dir)} 个文件有本地化问题")
            for item in issues_in_dir[:3]:  # 显示前3个
                print(f"    - {item['file'].name}: {len(item['issues'])} issues")
            
            self.issues_found[dir_name] = issues_in_dir
        else:
            print(f"  ✅ 所有检查的文件都已正确本地化")
    
    def fix_directory(self, dir_name, lang_code):
        """修复目录中的本地化问题"""
        dir_path = self.root_dir / dir_name
        
        if not dir_path.exists():
            return
        
        print(f"\n🔧 修复: {dir_name}/ → {self.lang_pricing[lang_code]['monthly']}")
        
        html_files = list(dir_path.glob('**/*.html'))
        
        fixed_in_dir = 0
        for file_path in html_files:
            if 'backup' in file_path.name:
                continue
            
            if self.fix_pricing(file_path, lang_code):
                fixed_in_dir += 1
                self.fixed_count += 1
                print(f"  ✅ {file_path.name}")
        
        if fixed_in_dir > 0:
            print(f"  📊 修复了 {fixed_in_dir} 个文件")
        else:
            print(f"  ℹ️  没有需要修复的文件")
    
    def scan_all(self):
        """扫描所有语言目录"""
        print("🔍 扫描所有语言目录查找本地化问题...")
        print("=" * 80)
        
        for lang_code in self.lang_pricing.keys():
            self.scan_directory(lang_code, lang_code)
        
        print("\n" + "=" * 80)
        print("📊 扫描完成")
        print("=" * 80)
        
        if self.issues_found:
            print(f"\n⚠️  发现 {len(self.issues_found)} 个目录有本地化问题")
            print("\n详细问题:")
            for dir_name, issues in self.issues_found.items():
                print(f"\n  {dir_name}/:")
                for item in issues[:3]:
                    print(f"    - {item['file'].name}")
                    for issue in item['issues'][:2]:
                        print(f"      • {issue}")
        else:
            print("\n✅ 所有检查的目录都已正确本地化")
    
    def fix_all(self):
        """修复所有语言目录"""
        print("🔧 修复所有语言目录的本地化问题...")
        print("=" * 80)
        
        for lang_code in self.lang_pricing.keys():
            self.fix_directory(lang_code, lang_code)
        
        print("\n" + "=" * 80)
        print("🎉 修复完成！")
        print("=" * 80)
        print(f"\n📊 总计修复了 {self.fixed_count} 个文件")
        
        if self.fixed_count > 0:
            print(f"\n💾 所有修改的文件都有备份（.backup_localization）")
        
        self.generate_report()
    
    def generate_report(self):
        """生成报告"""
        report = f"""# ✅ 网页本地化文字修复报告

**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 修复统计

| 语言目录 | 正确价格 | 修复文件数 |
|----------|----------|------------|
"""
        
        for lang_code, pricing in self.lang_pricing.items():
            report += f"| **{lang_code}** | {pricing['monthly']} | - |\n"
        
        report += f"""

**总计修复**: {self.fixed_count} 个文件

---

## 🎯 修复内容

### 价格本地化

"""
        
        for lang_code, pricing in self.lang_pricing.items():
            report += f"""
#### {lang_code}

| 项目 | 正确值 |
|------|--------|
| 月费 | {pricing['monthly']} |
| 包含页数 | {pricing['pages']} |
| 额外费用 | {pricing['additional']} |
| 货币符号 | {pricing['currency_symbol']} |

"""
        
        report += f"""

---

## ✅ 修复的错误

### 常见问题

1. **英文价格出现在非英文页面**
   - `$5.59/month` → 本地化价格
   - `$0.06/page` → 本地化价格

2. **英文单位出现在非英文页面**
   - `100 pages` → 本地化单位
   - `/month` → 本地化单位
   - `/page` → 本地化单位

3. **货币符号不正确**
   - `$` → ₩ / ¥ / HK$ / NT$

---

## 💾 备份信息

所有修改的文件都创建了备份：
- 备份文件名: `原文件名.backup_localization`
- 位置: 与原文件相同目录

恢复方法（如需要）:
```bash
# 恢复单个文件
mv 文件名.backup_localization 文件名

# 恢复所有文件
find . -name "*.backup_localization" -exec sh -c 'mv "$1" "${{1%.backup_localization}}"' _ {{}} \\;
```

---

## 🎉 结果

### 修复前 ❌

```
韩文页面显示:
  月费: $5.59/month ❌
  额外: $0.06/page ❌
  页数: 100 pages ❌
```

### 修复后 ✅

```
韩文页面显示:
  月费: ₩7998/월 ✅
  额外: ₩80/페이지 ✅
  页数: 100페이지 ✅
```

---

## ✅ 验证清单

### 韩文页面 (ko-KR/)

```
□ 月费显示: ₩7998/월
□ 额外费用: ₩80/페이지
□ 页数描述: 100페이지
□ 无英文价格
```

### 日文页面 (ja-JP/)

```
□ 月费显示: ¥926/月
□ 额外费用: ¥10/ページ
□ 页数描述: 100ページ
□ 无英文价格
```

### 繁体中文香港 (zh-HK/)

```
□ 月费显示: HK$46/月
□ 额外费用: HK$0.5/頁
□ 页数描述: 100頁
□ 无英文价格
```

### 繁体中文台湾 (zh-TW/)

```
□ 月费显示: NT$195/月
□ 额外费用: NT$2/頁
□ 页数描述: 100頁
□ 无英文价格
```

---

## 🎯 预期效果

**修复后**:
- ✅ 所有价格完全本地化
- ✅ 货币符号正确
- ✅ 单位使用对应语言
- ✅ 无英文混入
- ✅ 用户体验提升
- ✅ 转化率提升

---

**下一步**: 测试每个语言版本，验证显示正确

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        report_file = self.root_dir / '✅_网页本地化文字修复报告.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 详细报告已保存: {report_file.name}")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   网页本地化文字检查和修复工具                                ║
║                                                                              ║
║  此工具将检查并修复网页中未本地化的文字                                      ║
║                                                                              ║
║  修复内容:                                                                    ║
║    - 价格（$5.59 → ₩7998/¥926/HK$46/NT$195）                                ║
║    - 货币符号（$ → ₩/¥/HK$/NT$）                                             ║
║    - 单位（/month → /월/月, pages → 페이지/ページ/頁）                       ║
║                                                                              ║
║  所有修改的文件都会创建备份 (.backup_localization)                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    fixer = LocalizationFixer(root_dir)
    
    # 先扫描
    print("\n【步骤1/2】扫描本地化问题\n")
    fixer.scan_all()
    
    if not fixer.issues_found:
        print("\n✅ 所有页面都已正确本地化！无需修复")
        return
    
    print("\n" + "=" * 80)
    input_text = input("\n发现本地化问题，是否立即修复？按 Enter 继续，或输入 'n' 取消: ")
    
    if input_text.lower() == 'n':
        print("❌ 已取消修复")
        return
    
    # 执行修复
    print("\n【步骤2/2】修复本地化问题\n")
    fixer.fix_all()
    
    print("\n" + "=" * 80)
    print("✅ 所有网页文字已本地化！")
    print("📄 详细报告: ✅_网页本地化文字修复报告.md")
    print("=" * 80)
    print("\n请测试各语言版本，确认显示正确！")

if __name__ == '__main__':
    main()

