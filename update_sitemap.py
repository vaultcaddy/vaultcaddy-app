#!/usr/bin/env python3
"""
更新 sitemap.xml，添加阶段2生成的88个银行专属页面
"""

from datetime import datetime

# 读取生成的页面列表
with open('phase2_generated_pages_localized.txt', 'r', encoding='utf-8') as f:
    new_pages = [line.strip() for line in f if line.strip()]

# 生成sitemap条目
today = datetime.now().strftime('%Y-%m-%d')

sitemap_entries = []
for page in new_pages:
    url = f"https://vaultcaddy.com/{page}"
    entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>'''
    sitemap_entries.append(entry)

# 读取现有sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

# 检查是否已经包含新页面（避免重复添加）
if 'hsbc-bank-statement-simple.html' in sitemap_content:
    print("⚠️  Sitemap 中已包含银行专属页面，先移除旧条目...")
    # 移除所有 bank-statement-simple.html 的旧条目
    lines = sitemap_content.split('\n')
    filtered_lines = []
    skip_next_lines = 0
    for line in lines:
        if skip_next_lines > 0:
            skip_next_lines -= 1
            continue
        if '-bank-statement-simple.html' in line:
            # 跳过这个条目的5行（<url>到</url>）
            skip_next_lines = 4  # 还需要跳过接下来的4行
            # 移除当前行前的 <url> 标签
            if filtered_lines and '<url>' in filtered_lines[-1]:
                filtered_lines.pop()
            continue
        filtered_lines.append(line)
    
    sitemap_content = '\n'.join(filtered_lines)

# 在 </urlset> 之前插入新条目
insertion_point = sitemap_content.rfind('</urlset>')
if insertion_point == -1:
    print("❌ 错误：找不到 </urlset> 标签")
    exit(1)

new_sitemap = (
    sitemap_content[:insertion_point] +
    '\n'.join(sitemap_entries) + '\n' +
    sitemap_content[insertion_point:]
)

# 写入新sitemap
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(new_sitemap)

print(f"✅ Sitemap 已更新！")
print(f"📝 添加了 {len(sitemap_entries)} 个新页面")
print(f"📅 最后修改日期：{today}")
print(f"🎯 优先级：0.85（银行专属页面）")
print()
print("🔗 新增的页面类型：")
print("   - 22 个中文银行专属页面")
print("   - 22 个英文银行专属页面")
print("   - 22 个日文银行专属页面")
print("   - 22 个韩文银行专属页面")

