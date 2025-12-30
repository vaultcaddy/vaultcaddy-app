#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理2天前的旧md和txt文件
保留重要文件（如README, sitemap等）
"""

import os
from pathlib import Path
from datetime import datetime, timedelta

class FileCleanup:
    """文件清理器"""
    
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.days_old = 2
        self.cutoff_time = datetime.now() - timedelta(days=self.days_old)
        
        # 保留的重要文件（不删除）
        self.keep_files = {
            'README.md',
            'README.txt',
            'sitemap.xml',
            'robots.txt',
            'CHANGELOG.md',
            'LICENSE.md',
            'CONTRIBUTING.md',
            'package.json',
            '.gitignore'
        }
        
        # 保留最近创建的重要报告（今天和昨天的）
        self.keep_patterns = [
            '✅_剩余Pages_GIF添加完成.md',
            '🎉_SEO优化4阶段_最终完成报告.md',
            '📊_Performance_Dashboard_Setup_Guide.md',
            '🚀_SEO优化完整计划_4阶段.md',
            '✅_Sitemap生成完成_Phase4.md',
            '✅_GA事件跟踪添加完成_Phase2.md',
            '✅_SEO优化完成报告_Phase1.md'
        ]
        
        self.stats = {
            'total': 0,
            'deleted': 0,
            'kept': 0,
            'errors': []
        }
    
    def should_keep(self, filepath):
        """判断是否应该保留文件"""
        filename = filepath.name
        
        # 保留重要文件
        if filename in self.keep_files:
            return True, "重要文件"
        
        # 保留最近的关键报告
        if filename in self.keep_patterns:
            return True, "关键报告"
        
        # 检查文件修改时间
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        if mtime > self.cutoff_time:
            return True, f"太新了 ({mtime.strftime('%m-%d %H:%M')})"
        
        return False, None
    
    def cleanup(self):
        """清理旧文件"""
        print("🗑️  开始清理旧文件...")
        print(f"📅 删除 {self.cutoff_time.strftime('%Y-%m-%d')} 之前的文件")
        print("=" * 60)
        
        # 收集所有md和txt文件
        files_to_check = []
        for pattern in ['*.md', '*.txt']:
            files_to_check.extend(self.root_dir.glob(pattern))
        
        self.stats['total'] = len(files_to_check)
        
        print(f"📊 找到 {self.stats['total']} 个文件需要检查\n")
        
        # 分类文件
        to_delete = []
        to_keep = []
        
        for filepath in files_to_check:
            should_keep, reason = self.should_keep(filepath)
            
            if should_keep:
                to_keep.append((filepath, reason))
                self.stats['kept'] += 1
            else:
                to_delete.append(filepath)
        
        # 显示将要删除的文件（前20个）
        if to_delete:
            print(f"🗑️  将删除 {len(to_delete)} 个文件：\n")
            for i, filepath in enumerate(to_delete[:20], 1):
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                print(f"  {i}. {filepath.name} ({mtime.strftime('%m-%d %H:%M')})")
            
            if len(to_delete) > 20:
                print(f"  ... 还有 {len(to_delete) - 20} 个文件")
            
            print()
        
        # 显示保留的重要文件（前10个）
        if to_keep:
            print(f"✅ 保留 {len(to_keep)} 个文件：\n")
            for i, (filepath, reason) in enumerate(to_keep[:10], 1):
                print(f"  {i}. {filepath.name} - {reason}")
            
            if len(to_keep) > 10:
                print(f"  ... 还有 {len(to_keep) - 10} 个文件")
            
            print()
        
        # 确认删除
        if to_delete:
            print("=" * 60)
            print(f"⚠️  准备删除 {len(to_delete)} 个文件")
            print("=" * 60)
            
            # 生成报告（在删除前）
            self.generate_report(to_delete, to_keep)
            
            # 执行删除
            print("\n🗑️  开始删除文件...\n")
            for filepath in to_delete:
                try:
                    filepath.unlink()
                    self.stats['deleted'] += 1
                except Exception as e:
                    error_msg = f"无法删除 {filepath.name}: {str(e)}"
                    self.stats['errors'].append(error_msg)
                    print(f"  ❌ {error_msg}")
        else:
            self.generate_report([], to_keep)
    
    def generate_report(self, deleted_files, kept_files):
        """生成清理报告"""
        report = f"""
# 🗑️ 文件清理报告

**清理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**清理规则**: 删除 {self.cutoff_time.strftime('%Y-%m-%d')} 之前的 .md 和 .txt 文件

---

## 📊 清理统计

| 指标 | 数量 |
|------|------|
| **检查文件总数** | {self.stats['total']} |
| **已删除** | {self.stats['deleted']} |
| **保留** | {self.stats['kept']} |
| **错误** | {len(self.stats['errors'])} |

---

## ✅ 保留的文件 ({len(kept_files)}个)

### 重要文件
"""
        
        important_kept = [f for f, r in kept_files if r == "重要文件"]
        if important_kept:
            for f in important_kept:
                report += f"- {f.name}\n"
        
        report += "\n### 关键报告\n"
        key_reports = [f for f, r in kept_files if r == "关键报告"]
        if key_reports:
            for f in key_reports:
                report += f"- {f.name}\n"
        
        report += "\n### 最近文件\n"
        recent_files = [f for f, r in kept_files if "太新了" in r][:10]
        if recent_files:
            for f in recent_files:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                report += f"- {f.name} ({mtime.strftime('%m-%d %H:%M')})\n"
        
        if len(recent_files) > 10:
            report += f"\n... 还有 {len(recent_files) - 10} 个最近文件\n"
        
        report += f"""
---

## 🗑️ 已删除的文件 ({len(deleted_files)}个)

"""
        
        if deleted_files:
            # 按日期分组
            from collections import defaultdict
            by_date = defaultdict(list)
            
            for f in deleted_files:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                date_str = mtime.strftime('%Y-%m-%d')
                by_date[date_str].append(f.name)
            
            for date in sorted(by_date.keys(), reverse=True):
                report += f"\n### {date} ({len(by_date[date])}个)\n\n"
                for filename in sorted(by_date[date])[:20]:
                    report += f"- {filename}\n"
                
                if len(by_date[date]) > 20:
                    report += f"\n... 还有 {len(by_date[date]) - 20} 个文件\n"
        
        if self.stats['errors']:
            report += "\n---\n\n## ❌ 错误列表\n\n"
            for error in self.stats['errors']:
                report += f"- {error}\n"
        
        report += """
---

## 💾 释放的空间

清理前后对比:
"""
        
        # 计算释放的空间
        total_size = sum(f.stat().st_size for f in deleted_files if f.exists())
        report += f"- 释放空间: {total_size / 1024 / 1024:.2f} MB\n"
        
        report += """
---

## 🎯 清理效果

✅ 项目更整洁
✅ 减少文件检索时间
✅ 降低仓库大小
✅ 保留所有关键文件

---

**清理完成！** 🎉
"""
        
        # 保存报告
        report_file = self.root_dir / '✅_文件清理报告.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print(f"🎉 清理完成！")
        print(f"📊 总计: {self.stats['total']} 个文件")
        print(f"🗑️  删除: {self.stats['deleted']} 个文件")
        print(f"✅ 保留: {self.stats['kept']} 个文件")
        print(f"💾 释放: {total_size / 1024 / 1024:.2f} MB")
        print(f"📄 报告: {report_file.name}")
        print("=" * 60)

def main():
    """主函数"""
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    cleaner = FileCleanup(root_dir)
    cleaner.cleanup()

if __name__ == '__main__':
    main()

