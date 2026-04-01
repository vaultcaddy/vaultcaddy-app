#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""替换content-section的内容为新设计"""

print("=" * 70)
print("🎨 替换内容区域为全新设计")
print("=" * 70)
print()

with open('hsbc-vs-manual.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('hsbc-vs-manual.html.backup_content_replace', 'w', encoding='utf-8') as f:
    f.write(content)

# 读取新的设计内容
with open('create_demo_content.html', 'r', encoding='utf-8') as f:
    new_content = f.read()

# 查找 content-section 的开始和结束
import re

# 查找 <div class="content-section"> 到下一个 </div> 之前的内容
# 这里需要找到匹配的结束标签
pattern = r'(<div class="content-section">)(.*?)(以上详细对比表格共约.*?</div>\s*</div>)'

# 创建替换内容
replacement = r'\1\n' + new_content + r'\n\3'

# 执行替换
new_html = re.sub(pattern, replacement, content, flags=re.DOTALL)

if new_html == content:
    print("⚠️  未找到匹配的内容，尝试另一种模式...")
    # 尝试更简单的替换：找到 ## 📊 VaultCaddy vs 人工处理：全面对比 开始的部分
    pattern2 = r'(## 📊 VaultCaddy vs 人工处理：全面对比.*?)(以上详细对比表格共约)'
    replacement2 = new_content + '\n\n'
    new_html = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# 保存
with open('hsbc-vs-manual.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

if new_html != content:
    print("✅ 已成功替换内容区域！")
else:
    print("❌ 替换失败，请手动检查")

print()
print("=" * 70)
print("✅ 内容替换完成！")
print("=" * 70)
print()
print("💡 下一步：")
print("   1. 上传修复后的文件到服务器")
print("   2. 清除浏览器缓存")
print("   3. 验证新设计效果")
print("=" * 70)

