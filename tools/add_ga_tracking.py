#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加Google Analytics事件跟踪到所有页面
"""

import os
import re
from pathlib import Path

class GATrackingAdder:
    """GA跟踪添加器"""
    
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.stats = {
            'total': 0,
            'added': 0,
            'skipped': 0,
            'errors': []
        }
    
    def add_tracking_to_page(self, filepath):
        """添加GA跟踪到单个页面"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经添加过
            if 'ga-event-tracking.js' in content:
                print(f"  ℹ️  已存在GA跟踪: {filepath.name}")
                self.stats['skipped'] += 1
                return False
            
            # 在</body>前添加GA跟踪脚本
            tracking_script = '''
    <!-- Google Analytics 事件跟踪 -->
    <script src="/ga-event-tracking.js"></script>
'''
            
            body_close = content.rfind('</body>')
            if body_close == -1:
                print(f"  ⚠️  未找到</body>标签: {filepath.name}")
                self.stats['errors'].append(f"{filepath.name}: 未找到</body>标签")
                return False
            
            # 插入GA跟踪脚本
            content = content[:body_close] + tracking_script + content[body_close:]
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 已添加GA跟踪: {filepath.name}")
            self.stats['added'] += 1
            return True
            
        except Exception as e:
            error_msg = f"{filepath.name}: {str(e)}"
            print(f"  ❌ 错误: {error_msg}")
            self.stats['errors'].append(error_msg)
            return False
    
    def add_tracking_to_all_pages(self):
        """添加GA跟踪到所有页面"""
        print("🚀 开始添加Google Analytics事件跟踪...")
        print("=" * 60)
        
        # 收集所有HTML页面
        pages = []
        
        # 主页
        index_file = self.root_dir / 'index.html'
        if index_file.exists():
            pages.append(index_file)
        
        # 所有landing pages（v3, v2, simple）
        for file in self.root_dir.glob('*.html'):
            if file.name not in ['index.html'] and not file.name.startswith('.'):
                pages.append(file)
        
        # 子目录中的页面
        for lang_dir in ['zh-HK', 'zh-TW', 'ja-JP', 'ko-KR', 'en', 'kr', 'jp']:
            lang_path = self.root_dir / lang_dir
            if lang_path.exists():
                for file in lang_path.glob('*.html'):
                    pages.append(file)
        
        # 其他重要页面
        for page_name in ['signup.html', 'login.html', 'pricing.html', 'firstproject.html', 'document-detail.html']:
            page_file = self.root_dir / page_name
            if page_file.exists() and page_file not in pages:
                pages.append(page_file)
            
            # 检查多语言版本
            for lang_dir in ['en', 'kr', 'jp']:
                lang_page = self.root_dir / lang_dir / page_name
                if lang_page.exists() and lang_page not in pages:
                    pages.append(lang_page)
        
        self.stats['total'] = len(pages)
        
        print(f"📊 找到 {self.stats['total']} 个页面需要添加GA跟踪")
        print("=" * 60)
        
        # 添加GA跟踪到每个页面
        for page in pages:
            self.add_tracking_to_page(page)
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成报告"""
        report = f"""
# ✅ Google Analytics事件跟踪添加完成

**完成时间**: {os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}

---

## 📊 添加统计

| 指标 | 数量 |
|------|------|
| **总页面数** | {self.stats['total']} |
| **成功添加** | {self.stats['added']} |
| **已存在跳过** | {self.stats['skipped']} |
| **错误数** | {len(self.stats['errors'])} |
| **成功率** | {((self.stats['added'] + self.stats['skipped']) / self.stats['total'] * 100):.1f}% |

---

## 🎯 跟踪功能

本次添加的GA事件跟踪包括:

1. ✅ **GIF演示观看跟踪**
   - 当GIF进入视口50%时触发
   - 记录页面路径

2. ✅ **PDF上传跟踪**
   - 记录文件数量
   - 记录文件类型和大小

3. ✅ **转换完成跟踪**
   - 记录处理时间
   - 记录页面数量

4. ✅ **CTA点击跟踪**
   - 跟踪所有注册/登录按钮
   - 记录按钮文本和链接

5. ✅ **Free Trial Banner点击跟踪**
   - 专门跟踪Sticky Banner点击
   - 记录页面路径

6. ✅ **滚动深度跟踪**
   - 跟踪25%, 50%, 75%, 90%, 100%
   - 优化内容布局参考

7. ✅ **页面停留时间跟踪**
   - 记录用户在页面的时间
   - 分析内容吸引力

8. ✅ **出站链接跟踪**
   - 跟踪外部链接点击
   - 分析用户流向

9. ✅ **表单交互跟踪**
   - 跟踪表单开始和提交
   - 优化转化漏斗

10. ✅ **视频播放跟踪**
    - 跟踪视频播放和完成
    - 分析内容有效性

---

## 📊 如何查看数据

### Google Analytics 4 (GA4)

1. **实时数据**:
   - 登录 GA4
   - 转到"实时" → "事件"
   - 查看正在发生的事件

2. **事件报告**:
   - 转到"报告" → "参与度" → "事件"
   - 查看所有跟踪的事件
   - 按事件名称筛选

3. **转化漏斗**:
   - 转到"探索" → "漏斗探索"
   - 创建自定义漏斗:
     ```
     页面访问 → gif_view → cta_click → form_submit
     ```

4. **自定义报告**:
   - 使用"探索"功能
   - 创建自定义维度和指标
   - 分析用户行为路径

---

## 🎯 关键指标监控

### 优先监控指标:

1. **GIF观看率**
   - 公式: gif_view事件 / 总页面浏览量
   - 目标: > 80%

2. **CTA点击率**
   - 公式: cta_click事件 / 总页面浏览量
   - 目标: > 5%

3. **转换完成率**
   - 公式: conversion_complete事件 / pdf_upload事件
   - 目标: > 90%

4. **平均处理时间**
   - 查看conversion_complete事件的processing_time_seconds参数
   - 目标: < 3秒

5. **滚动深度**
   - 查看有多少用户滚动到75%+
   - 目标: > 40%

---

## 🚀 下一步操作

### 立即执行:

1. ✅ **部署更新**
   - 清除CDN缓存
   - 确保ga-event-tracking.js可访问
   - 测试几个页面的事件触发

2. ✅ **GA4设置**
   - 确认GA4代码已安装
   - 设置关键事件为转化
   - 创建自定义报告

3. ✅ **测试验证**
   - 打开Chrome DevTools
   - 切换到Network标签
   - 筛选"analytics"或"collect"
   - 执行各种操作，查看事件是否发送

### 本周执行:

4. ✅ **创建Dashboard**
   - 在GA4中创建自定义Dashboard
   - 添加关键指标卡片
   - 设置定期邮件报告

5. ✅ **设置告警**
   - 转化率突然下降 > 20%
   - 错误率突然上升 > 10%
   - 流量异常波动

---

## 🐛 调试信息

事件跟踪脚本会在浏览器控制台输出调试信息:

```
🔍 GA Event Tracking initialized
✅ GIF观看跟踪已启用
✅ PDF上传跟踪已启用
✅ CTA点击跟踪已启用 (15个按钮)
...
🎉 所有GA事件跟踪已初始化完成
```

当事件触发时:
```
✅ GA Event: gif_view {{event_category: "engagement", ...}}
✅ GA Event: cta_click {{event_category: "engagement", ...}}
```

---

## ❌ 错误列表

"""
        
        if self.stats['errors']:
            for error in self.stats['errors']:
                report += f"- {error}\n"
        else:
            report += "无错误 ✅\n"
        
        report += """
---

**Phase 2 完成！** ✅

**准备开始 Phase 3: 创建性能监控Dashboard吗？** 📊
"""
        
        # 保存报告
        report_file = self.root_dir / '✅_GA事件跟踪添加完成_Phase2.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print(f"✅ GA跟踪添加完成！")
        print(f"📊 总计: {self.stats['total']} 个页面")
        print(f"✅ 成功: {self.stats['added']} 个页面")
        print(f"ℹ️  跳过: {self.stats['skipped']} 个页面")
        print(f"❌ 错误: {len(self.stats['errors'])} 个")
        print(f"📄 报告已生成: {report_file.name}")
        print("=" * 60)

def main():
    """主函数"""
    root_dir = '/Users/cavlinyeung/ai-bank-parser'
    adder = GATrackingAdder(root_dir)
    adder.add_tracking_to_all_pages()

if __name__ == '__main__':
    main()

