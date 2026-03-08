#!/usr/bin/env python3
"""
更新 sitemap.xml，添加阶段2生成的所有 204 个新页面
"""

from datetime import datetime

# 读取生成的页面列表
with open('phase2_generated_remaining_204_pages.txt', 'r', encoding='utf-8') as f:
    new_pages = [line.strip() for line in f if line.strip()]

# 生成sitemap条目
today = datetime.now().strftime('%Y-%m-%d')

sitemap_entries = []
for page in new_pages:
    url = f"https://vaultcaddy.com/{page}"
    # 银行页面优先级稍高
    priority = "0.85" if "bank-statement" in page else "0.80"
    entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>'''
    sitemap_entries.append(entry)

# 读取现有sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

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
print()
print("🔗 新增的页面类型：")

# 统计
bank_pages = sum(1 for p in new_pages if 'bank-statement' in p)
industry_pages = sum(1 for p in new_pages if 'accounting-solution' in p)

print(f"   - {bank_pages} 个银行专属页面（优先级 0.85）")
print(f"   - {industry_pages} 个行业专属页面（优先级 0.80）")
print()
print("📊 总计sitemap中的页面数：")

# 计算总页面数
with open('sitemap.xml', 'r') as f:
    total_urls = f.read().count('<url>')
print(f"   🌐 {total_urls} 个页面")

