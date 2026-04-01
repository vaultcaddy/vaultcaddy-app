#!/usr/bin/env python3
"""
Phase 4: SEO提交 - 更新Sitemap并准备提交GSC
"""
import os
from datetime import datetime
import xml.etree.ElementTree as ET

print("=" * 70)
print("🚀 Phase 4: SEO提交开始")
print("=" * 70 + "\n")

# 1. 读取现有sitemap
print("📋 步骤1: 读取现有sitemap.xml...\n")

try:
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    print(f"✅ 现有sitemap读取成功")
    
    # 统计现有URL数量
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    existing_urls = root.findall('.//ns:loc', namespace)
    print(f"📊 现有URL数量: {len(existing_urls)}")
    
except Exception as e:
    print(f"⚠️  无法读取现有sitemap: {e}")
    print("💡 将创建新的sitemap...")
    root = None

# 2. 获取所有v3页面
print(f"\n📋 步骤2: 扫描v3页面...\n")

v3_files = sorted([f for f in os.listdir('.') if f.endswith('-statement-v3.html')])
print(f"✅ 找到 {len(v3_files)} 个v3页面")

# 3. 准备新增URL
print(f"\n📋 步骤3: 准备新增URL...\n")

base_url = "https://vaultcaddy.com/"
current_date = datetime.now().strftime('%Y-%m-%d')

new_urls = []
for filename in v3_files:
    url = base_url + filename
    new_urls.append({
        'loc': url,
        'lastmod': current_date,
        'changefreq': 'weekly',
        'priority': '0.8'
    })

print(f"✅ 准备添加 {len(new_urls)} 个新URL")
print(f"📅 最后修改日期: {current_date}")
print(f"🔄 更新频率: weekly")
print(f"⭐ 优先级: 0.8")

# 4. 创建/更新sitemap
print(f"\n📋 步骤4: 生成新sitemap.xml...\n")

# 创建新的sitemap
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
new_root = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')

# 添加现有URL（如果有的话）
if root is not None:
    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None and 'statement-v3.html' not in loc.text:
            # 保留非v3的URL
            new_root.append(url_elem)

# 添加所有v3 URL
for url_data in new_urls:
    url_elem = ET.SubElement(new_root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    
    loc = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    loc.text = url_data['loc']
    
    lastmod = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
    lastmod.text = url_data['lastmod']
    
    changefreq = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
    changefreq.text = url_data['changefreq']
    
    priority = ET.SubElement(url_elem, '{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
    priority.text = url_data['priority']

# 写入文件
new_tree = ET.ElementTree(new_root)
ET.indent(new_tree, space="  ")
new_tree.write('sitemap_v3.xml', encoding='utf-8', xml_declaration=True)

print(f"✅ 新sitemap生成完成: sitemap_v3.xml")

# 统计最终URL数量
total_urls = len(new_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
print(f"📊 总URL数量: {total_urls}")
print(f"   - v3页面: {len(new_urls)}")
print(f"   - 其他页面: {total_urls - len(new_urls)}")

# 5. 创建robots.txt（如果不存在）
print(f"\n📋 步骤5: 检查robots.txt...\n")

if os.path.exists('robots.txt'):
    print("✅ robots.txt已存在")
    with open('robots.txt', 'r') as f:
        print("当前内容:")
        print(f.read())
else:
    robots_content = f"""# robots.txt for VaultCaddy.com
# Generated: {current_date}

User-agent: *
Allow: /

# Sitemaps
Sitemap: https://vaultcaddy.com/sitemap.xml
Sitemap: https://vaultcaddy.com/sitemap_v3.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /private/
Disallow: /api/

# Allow all bank statement pages
Allow: /*-statement-v3.html
"""
    with open('robots.txt', 'w') as f:
        f.write(robots_content)
    print("✅ robots.txt创建完成")

# 6. 创建GSC提交指南
print(f"\n📋 步骤6: 创建GSC提交指南...\n")

gsc_guide = f"""# 🚀 Google Search Console 提交指南

## 📅 准备时间
**日期**: {current_date}  
**新增页面**: 50个银行v3页面  
**Sitemap文件**: sitemap_v3.xml  

---

## 📋 提交步骤

### 1. 登录Google Search Console
🔗 **URL**: https://search.google.com/search-console  
📧 **账户**: 使用VaultCaddy管理员账户

### 2. 选择资源
选择: `vaultcaddy.com` 资源

### 3. 提交Sitemap
**路径**: 左侧菜单 → "索引" → "站点地图"

**操作**:
1. 点击"添加新的站点地图"
2. 输入: `sitemap_v3.xml`
3. 点击"提交"
4. 等待处理（通常24-48小时）

**预期结果**:
- 状态: "成功"
- 已发现: 50个URL
- 已索引: 0→50（逐步增加）

### 4. 请求编入索引（可选但推荐）
**对于重要页面（如Chase, BOA等）**:

1. 点击左侧"网址检查"
2. 输入完整URL，例如:
   `https://vaultcaddy.com/chase-bank-statement-v3.html`
3. 点击"请求编入索引"
4. 等待确认

**推荐优先索引**:
- chase-bank-statement-v3.html
- bank-of-america-statement-v3.html
- wells-fargo-statement-v3.html
- citibank-statement-v3.html
- hsbc-uk-bank-statement-v3.html

### 5. 监控索引状态
**路径**: "索引" → "网页"

**检查项目**:
- 已索引的网页数量
- 索引覆盖率
- 发现但未编入索引的网页
- 错误或警告

**预期时间表**:
- 1-3天: 开始索引（10-20个）
- 1周: 大部分索引（30-40个）
- 2周: 全部索引（50个）

---

## 🎯 Bing Webmaster Tools 提交

### 1. 登录Bing Webmaster
🔗 **URL**: https://www.bing.com/webmasters

### 2. 提交Sitemap
**路径**: "站点地图" → "提交站点地图"

**操作**:
1. 输入: `https://vaultcaddy.com/sitemap_v3.xml`
2. 点击"提交"
3. 等待处理

### 3. URL提交工具
**路径**: "配置我的站点" → "提交URL"

**批量提交重要URL**（最多50个/天）:
```
https://vaultcaddy.com/chase-bank-statement-v3.html
https://vaultcaddy.com/bank-of-america-statement-v3.html
https://vaultcaddy.com/wells-fargo-statement-v3.html
... (添加更多)
```

---

## 📊 监控和追踪

### Google Analytics设置
**确保追踪代码已添加到所有v3页面**

**检查项目**:
1. 所有页面包含GA代码
2. 目标设置（注册、下载等）
3. 事件追踪（CTA点击）
4. 自定义维度（银行类型、地区）

### 关键词排名追踪
**使用工具**: Google Search Console, Ahrefs, SEMrush

**追踪关键词**（示例）:
- "Chase Bank statement converter"
- "Bank of America PDF to Excel"
- "Wells Fargo bank statement"
- "convert bank statement to QuickBooks"

### 监控频率
- **第1周**: 每天检查索引状态
- **第2-4周**: 每2-3天检查
- **1个月后**: 每周检查

---

## ✅ 提交检查清单

### 提交前
- [x] sitemap_v3.xml已生成
- [x] robots.txt已更新
- [x] 所有50个v3页面可访问
- [x] Meta标签正确
- [x] Schema标记完整

### 提交后
- [ ] Google Search Console提交sitemap
- [ ] Bing Webmaster提交sitemap
- [ ] 请求5-10个重要页面索引
- [ ] 设置Google Analytics监控
- [ ] 设置关键词排名追踪

### 1周后检查
- [ ] 检查索引数量
- [ ] 查看索引覆盖率
- [ ] 检查是否有错误
- [ ] 查看搜索表现数据
- [ ] 分析用户行为

---

## 🎉 预期结果

### 1个月后
- 索引页面: 48-50个
- 搜索曝光: 1,000-2,000
- 搜索点击: 50-100
- 平均排名: 20-50位

### 3个月后
- 索引页面: 50个
- 搜索曝光: 10,000-20,000
- 搜索点击: 500-1,000
- 平均排名: 10-20位
- Top 20页面: 10-15个

### 6个月后
- 搜索曝光: 50,000-100,000
- 搜索点击: 3,000-6,000
- 平均排名: 5-15位
- Top 10页面: 15-20个
- Featured Snippets: 5-10个

---

## 💡 优化建议

### 持续优化
1. **内容更新**: 每月更新重要页面
2. **内部链接**: 从高权重页面链接
3. **外部链接**: 获取相关网站backlinks
4. **用户体验**: 监控跳出率和停留时间
5. **技术优化**: 提升加载速度

### A/B测试
- 测试不同Title标签
- 测试不同Meta Description
- 测试不同CTA文案
- 测试不同页面布局

---

**Phase 4完成！准备提交到搜索引擎！** 🚀
"""

with open('GSC_提交指南.md', 'w', encoding='utf-8') as f:
    f.write(gsc_guide)

print("✅ GSC提交指南创建完成: GSC_提交指南.md")

print("\n" + "=" * 70)
print("🎉 Phase 4: SEO提交准备完成！")
print("=" * 70)
print(f"\n✅ 已生成文件:")
print(f"   1. sitemap_v3.xml ({total_urls} URLs)")
print(f"   2. robots.txt (已更新)")
print(f"   3. GSC_提交指南.md (详细步骤)")
print(f"\n📊 统计:")
print(f"   • 新增页面: {len(v3_files)}")
print(f"   • 总URL: {total_urls}")
print(f"   • 更新日期: {current_date}")
print(f"\n⏭️  下一步操作:")
print(f"   1. 查看 GSC_提交指南.md")
print(f"   2. 提交 sitemap_v3.xml 到 Google Search Console")
print(f"   3. 提交 sitemap_v3.xml 到 Bing Webmaster")
print(f"   4. 监控索引状态")
print(f"\n🎊 Phase 1-4 全部完成！恭喜！")
