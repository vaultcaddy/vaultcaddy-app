#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时移除非英文页面的GIF，避免语言和价格不一致
"""

import os
import re
from pathlib import Path
from datetime import datetime

class GIFRemover:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.removed_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.non_english_dirs = ['ko-KR', 'ja-JP', 'zh-HK', 'zh-TW', 'kr', 'jp', 'ja']
        self.processed_files = []
        
    def remove_gif_section(self, file_path):
        """从HTML文件中移除GIF section"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含GIF
            if 'chase-bank-demo.gif' not in content:
                self.skipped_count += 1
                return False
            
            original_content = content
            
            # 方法1: 移除整个包含GIF的section（最常见的结构）
            # 查找包含GIF的section标签
            pattern1 = r'<section[^>]*>(?:(?!</section>).)*chase-bank-demo\.gif(?:(?!</section>).)*</section>'
            new_content = re.sub(pattern1, '', content, flags=re.DOTALL)
            
            # 方法2: 如果是在其他容器中，尝试移除包含GIF的div
            if new_content == content:
                pattern2 = r'<div[^>]*>(?:(?!</div>).)*chase-bank-demo\.gif(?:(?!</div>).)*</div>'
                new_content = re.sub(pattern2, '', content, flags=re.DOTALL)
            
            if new_content != original_content:
                # 备份原文件
                backup_path = str(file_path) + '.backup_gif_removal'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 写入新内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✅ 已移除GIF: {file_path.name}")
                self.processed_files.append(file_path)
                return True
            else:
                print(f"  ⚠️  未找到可移除的GIF section: {file_path.name}")
                self.skipped_count += 1
                return False
                
        except Exception as e:
            print(f"  ❌ 处理失败 {file_path.name}: {e}")
            self.error_count += 1
            return False
    
    def process_directory(self, dir_name):
        """处理一个语言目录"""
        dir_path = self.root_dir / dir_name
        
        if not dir_path.exists():
            print(f"⚠️  目录不存在: {dir_name}")
            return
        
        print(f"\n📁 处理目录: {dir_name}")
        
        # 查找所有HTML文件
        html_files = list(dir_path.glob('**/*.html'))
        
        if not html_files:
            print(f"  ℹ️  没有找到HTML文件")
            return
        
        removed_in_dir = 0
        for file_path in html_files:
            # 跳过backup文件
            if 'backup' in file_path.name:
                continue
            
            if self.remove_gif_section(file_path):
                removed_in_dir += 1
                self.removed_count += 1
        
        print(f"  📊 {dir_name}: 移除了 {removed_in_dir} 个GIF")
    
    def execute(self):
        """执行移除操作"""
        print("🚀 开始移除非英文页面的GIF...")
        print("=" * 80)
        print(f"目标语言目录: {', '.join(self.non_english_dirs)}")
        print(f"原因: 避免英文GIF在非英文页面造成语言和价格混淆")
        print("=" * 80)
        
        for dir_name in self.non_english_dirs:
            self.process_directory(dir_name)
        
        print("\n" + "=" * 80)
        print(f"🎉 处理完成！")
        print(f"📊 统计:")
        print(f"   - 成功移除: {self.removed_count} 个GIF")
        print(f"   - 跳过（无GIF）: {self.skipped_count} 个文件")
        print(f"   - 错误: {self.error_count} 个")
        print("=" * 80)
        
        if self.removed_count > 0:
            print("\n💾 备份说明:")
            print("   所有修改的文件都有备份（.backup_gif_removal）")
            print("   如需恢复，可以从备份文件恢复")
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成报告"""
        report = f"""# ✅ GIF临时移除完成报告

**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 统计结果

| 指标 | 数量 |
|------|------|
| **成功移除** | {self.removed_count} |
| **跳过（无GIF）** | {self.skipped_count} |
| **错误** | {self.error_count} |
| **总计处理** | {self.removed_count + self.skipped_count + self.error_count} |

---

## 🎯 执行原因

当前所有语言版本都使用同一个英文GIF (`chase-bank-demo.gif`)，导致：

❌ **问题**:
- 韩文页面显示英文界面 + 美元价格
- 日文页面显示英文界面 + 美元价格  
- 中文页面显示英文界面 + 美元价格

✅ **解决**:
- 暂时移除非英文页面的GIF
- 避免用户混淆
- 等待本地化GIF版本创建完成

---

## 🌍 处理的语言目录

"""
        for dir_name in self.non_english_dirs:
            status = "✅" if (self.root_dir / dir_name).exists() else "⚠️ "
            report += f"- {status} `{dir_name}/`\n"
        
        report += f"""

---

## 📝 处理的文件

"""
        if self.processed_files:
            for file_path in self.processed_files[:20]:  # 只显示前20个
                report += f"- {file_path.relative_to(self.root_dir)}\n"
            
            if len(self.processed_files) > 20:
                report += f"\n... 还有 {len(self.processed_files) - 20} 个文件\n"
        else:
            report += "（无文件被处理）\n"
        
        report += f"""

---

## 💾 备份信息

所有修改的文件都创建了备份：
- 备份文件名: `原文件名.backup_gif_removal`
- 位置: 与原文件相同目录

恢复方法（如需要）:
```bash
# 恢复单个文件
mv 文件名.backup_gif_removal 文件名

# 恢复所有文件
find . -name "*.backup_gif_removal" -exec sh -c 'mv "$1" "${{1%.backup_gif_removal}}"' _ {{}} \;
```

---

## ⏭️ 下一步行动

### 立即完成 ✅

- [x] 移除非英文页面的英文GIF
- [x] 避免语言和价格不一致

### 本周完成 🎯

□ 录制韩文版GIF
  - 语言: 한국어
  - 价格: ₩7998/월 (100페이지)
  - 保存为: `/video/chase-bank-demo-ko.gif`

□ 录制日文版GIF
  - 语言: 日本語
  - 价格: ¥926/月 (100ページ)
  - 保存为: `/video/chase-bank-demo-ja.gif`

□ 录制香港繁体中文版GIF
  - 语言: 繁體中文（香港）
  - 价格: HK$46/月（100頁）
  - 保存为: `/video/chase-bank-demo-zh-hk.gif`

□ 录制台湾繁体中文版GIF
  - 语言: 繁體中文（台灣）
  - 价格: NT$195/月（100頁）
  - 保存为: `/video/chase-bank-demo-zh-tw.gif`

□ 重命名现有英文GIF
  - 从: `/video/chase-bank-demo.gif`
  - 到: `/video/chase-bank-demo-en.gif`

□ 运行更新脚本
  - 更新所有页面使用对应语言的GIF
  - 验证所有语言版本

---

## 📈 预期效果

### 当前状态（临时方案）

✅ **优点**:
- 消除了语言和价格不一致
- 避免用户混淆
- 保持页面其他内容正常

⚠️ **缺点**:
- 失去了动态演示
- 可能略微降低转化率

### 最终状态（本地化完成后）

✅ **优点**:
- 完美的语言一致性
- 价格完全本地化
- 专业品牌形象
- 预计转化率提升 2-4倍

---

## 🎉 总结

**问题**: 英文GIF在非英文页面造成混淆

**临时方案**: ✅ 已完成 - 移除非英文页面的GIF

**永久方案**: 🔄 进行中 - 创建本地化GIF版本

**预期完成**: 本周内

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        report_file = self.root_dir / '✅_GIF临时移除报告.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 详细报告已保存: {report_file.name}")

def main():
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   GIF 本地化临时修复工具                                      ║
║                                                                              ║
║  此工具将暂时移除非英文页面的英文GIF，避免语言和价格不一致                  ║
║                                                                              ║
║  处理的目录: ko-KR, ja-JP, zh-HK, zh-TW, kr, jp, ja                          ║
║  保留的目录: en-US, en-UK, en-AU, en-CA (英文版本保持不变)                   ║
║                                                                              ║
║  所有修改的文件都会创建备份 (.backup_gif_removal)                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    input_text = input("按 Enter 继续，或输入 'n' 取消: ")
    if input_text.lower() == 'n':
        print("❌ 已取消")
        return
    
    remover = GIFRemover(root_dir)
    remover.execute()
    
    print("\n" + "=" * 80)
    print("✅ 完成！非英文页面的GIF已移除")
    print("📄 详细报告: ✅_GIF临时移除报告.md")
    print("=" * 80)

if __name__ == '__main__':
    main()

