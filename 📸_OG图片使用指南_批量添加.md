# 📸 OG 图片使用指南 - 批量添加到网页

**状态**：✅ 已成功生成 6 个 OG 图片！  
**位置**：`/Users/cavlinyeung/ai-bank-parser/images/og/`  
**下一步**：将图片上传到网站并更新 HTML

---

## ✅ 已生成的 OG 图片

| 文件名 | 大小 | 用于页面 | 状态 |
|--------|------|---------|------|
| `og-index.jpg` | 17KB | index.html | ✅ 已生成 |
| `og-ai-vs-manual-comparison.jpg` | 76KB | ai-vs-manual-comparison.html | ✅ 已生成 |
| `og-vaultcaddy-vs-dext.jpg` | 82KB | vaultcaddy-vs-dext.html | ✅ 已生成 |
| `og-vaultcaddy-vs-autoentry.jpg` | 78KB | vaultcaddy-vs-autoentry.html | ✅ 已生成 |
| `og-hsbc-bank-statement.jpg` | 66KB | hsbc-bank-statement.html | ✅ 已生成 |
| `og-hangseng-bank-statement.jpg` | 64KB | hangseng-bank-statement.html | ✅ 已生成 |

**总计**：6 个图片，所有图片尺寸：1200 x 630 px ✓

---

## 🚀 快速使用步骤

### Step 1: 上传图片到网站

将 `images/og/` 目录中的所有图片上传到网站的 `/images/og/` 目录：

```bash
# 如果使用 FTP/SFTP
上传到：https://vaultcaddy.com/images/og/

# 如果使用 Git
git add images/og/*.jpg
git commit -m "Add OG preview images"
git push
```

### Step 2: 在 HTML 中添加 OG 标签

在每个页面的 `<head>` 部分添加以下代码：

---

## 📄 各页面的 OG 标签代码

### 1️⃣ 首页（index.html）

在 `<head>` 部分添加：

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vaultcaddy.com/">
<meta property="og:title" content="银行对账单转Excel｜3秒完成｜月费$46起｜比Dext便宜70% - VaultCaddy">
<meta property="og:description" content="告别30小时手工对账！VaultCaddy AI让您3秒将银行对账单转成Excel，准确率98%，比人工便宜95%，比Dext便宜70%。支持汇丰、恒生等所有香港银行。月费$46起，免费试用20页。">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-index.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-index.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VaultCaddy - 银行对账单转Excel工具">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/">
<meta name="twitter:title" content="银行对账单转Excel｜3秒完成｜月费$46起">
<meta name="twitter:description" content="告别30小时手工对账！VaultCaddy AI让您3秒将银行对账单转成Excel，准确率98%。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-index.jpg">
```

---

### 2️⃣ AI vs 人工对比页（ai-vs-manual-comparison.html）

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://vaultcaddy.com/ai-vs-manual-comparison.html">
<meta property="og:title" content="VaultCaddy vs 人工处理 vs Dext vs AutoEntry｜香港对账单AI处理完整对比 2025">
<meta property="og:description" content="人工处理对账单每月花30小时？年费3万港币？VaultCaddy AI 3秒搞定，年费仅$552，比人工便宜95%，比Dext便宜70%。查看完整对比表→">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-ai-vs-manual-comparison.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-ai-vs-manual-comparison.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VaultCaddy vs 人工处理 vs Dext vs AutoEntry 完整对比">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/ai-vs-manual-comparison.html">
<meta name="twitter:title" content="VaultCaddy vs 人工 vs Dext vs AutoEntry 完整对比 2025">
<meta name="twitter:description" content="年省35,000港币！VaultCaddy AI 3秒处理对账单，比人工便宜95%，比Dext便宜70%。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-ai-vs-manual-comparison.jpg">
```

---

### 3️⃣ VaultCaddy vs Dext（vaultcaddy-vs-dext.html）

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://vaultcaddy.com/vaultcaddy-vs-dext.html">
<meta property="og:title" content="VaultCaddy vs Dext（原Receipt Bank）对比｜年费便宜70%｜月费$46 vs $273">
<meta property="og:description" content="Dext太贵？年费$3,276？VaultCaddy提供相同功能，年费仅$552，便宜70%！更适合香港银行。1,000+企业从Dext转到VaultCaddy。">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-dext.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-dext.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VaultCaddy vs Dext 价格和功能对比">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/vaultcaddy-vs-dext.html">
<meta name="twitter:title" content="VaultCaddy vs Dext 对比｜年费便宜70%">
<meta name="twitter:description" content="相同功能，价格便宜70%！VaultCaddy年费$552 vs Dext年费$3,276。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-dext.jpg">
```

---

### 4️⃣ VaultCaddy vs AutoEntry（vaultcaddy-vs-autoentry.html）

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://vaultcaddy.com/vaultcaddy-vs-autoentry.html">
<meta property="og:title" content="VaultCaddy vs AutoEntry 对比｜年费便宜85%｜月费$46 vs $325">
<meta property="og:description" content="AutoEntry太贵？年费$3,900？VaultCaddy年费仅$552，便宜85%！更适合香港银行，全中文界面，24/7中文客服。">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-autoentry.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-autoentry.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VaultCaddy vs AutoEntry 价格和功能对比">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/vaultcaddy-vs-autoentry.html">
<meta name="twitter:title" content="VaultCaddy vs AutoEntry 对比｜年费便宜85%">
<meta name="twitter:description" content="相同功能，价格便宜85%！VaultCaddy年费$552 vs AutoEntry年费$3,900。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-vaultcaddy-vs-autoentry.jpg">
```

---

### 5️⃣ HSBC 银行页面（hsbc-bank-statement.html）

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vaultcaddy.com/hsbc-bank-statement.html">
<meta property="og:title" content="汇丰银行对账单转Excel｜3秒处理｜支持HSBC网银PDF｜月费$46起">
<meta property="og:description" content="汇丰银行（HSBC）对账单手工录入太慢？VaultCaddy AI自动识别汇丰网银PDF，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页。">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-hsbc-bank-statement.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-hsbc-bank-statement.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="汇丰银行对账单自动转Excel">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/hsbc-bank-statement.html">
<meta name="twitter:title" content="汇丰银行对账单转Excel｜3秒处理">
<meta name="twitter:description" content="汇丰对账单自动识别，3秒转成Excel，准确率98%。月费$46起。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-hsbc-bank-statement.jpg">
```

---

### 6️⃣ 恒生银行页面（hangseng-bank-statement.html）

```html
<!-- Open Graph 标签 -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vaultcaddy.com/hangseng-bank-statement.html">
<meta property="og:title" content="恒生银行对账单转Excel｜3秒处理｜支持Hang Seng网银PDF｜月费$46起">
<meta property="og:description" content="恒生银行对账单手工录入太慢？VaultCaddy AI自动识别恒生网银PDF，3秒转成Excel/CSV，准确率98%。月费$46起，免费试用20页。">
<meta property="og:image" content="https://vaultcaddy.com/images/og/og-hangseng-bank-statement.jpg">
<meta property="og:image:secure_url" content="https://vaultcaddy.com/images/og/og-hangseng-bank-statement.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="恒生银行对账单自动转Excel">

<!-- Twitter Card 标签 -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://vaultcaddy.com/hangseng-bank-statement.html">
<meta name="twitter:title" content="恒生银行对账单转Excel｜3秒处理">
<meta name="twitter:description" content="恒生对账单自动识别，3秒转成Excel，准确率98%。月费$46起。">
<meta name="twitter:image" content="https://vaultcaddy.com/images/og/og-hangseng-bank-statement.jpg">
```

---

## 🧪 Step 3: 测试预览效果

### 方法 1: Facebook Debugger（推荐）

1. 访问：https://developers.facebook.com/tools/debug/
2. 输入页面 URL（例如：`https://vaultcaddy.com/`）
3. 点击 "Fetch new information"
4. 查看预览效果

**如果图片不显示**：
- 点击 "Scrape Again" 按钮
- 等待 24-48 小时让 Facebook 缓存更新

### 方法 2: WhatsApp 测试

1. 打开 WhatsApp
2. 给自己或朋友发送页面链接
3. 查看预览卡片

### 方法 3: LinkedIn Post Inspector

1. 访问：https://www.linkedin.com/post-inspector/
2. 输入页面 URL
3. 查看预览效果

### 方法 4: Twitter Card Validator

1. 访问：https://cards-dev.twitter.com/validator
2. 输入页面 URL
3. 查看预览效果

---

## 📊 预期效果

### 优化前（没有 OG 图片）：

```
WhatsApp/Facebook 分享：
┌─────────────────────────────────┐
│ https://vaultcaddy.com/         │
│                                 │
│ VaultCaddy - AI Document...    │
└─────────────────────────────────┘
```
😐 纯文字链接，无吸引力

### 优化后（有 OG 图片）：

```
WhatsApp/Facebook 分享：
┌─────────────────────────────────┐
│ [预览图：紫色渐变+核心卖点]      │
│                                 │
│ VaultCaddy vs 人工處理 vs Dext │
│ 月費HK$46起 | 比人工便宜95%     │
│                                 │
│ vaultcaddy.com                  │
└─────────────────────────────────┘
```
😍 专业预览卡片，点击率提升 3-10 倍！

---

## 🔄 批量更新脚本（可选）

如果您想自动为所有页面添加 OG 标签，可以使用以下 Python 脚本：

```python
# batch_add_og_tags.py
# 批量为所有页面添加 OG 标签

# （详细脚本见 batch_add_og_tags.py 文件）
```

---

## ✅ 完成检查清单

- [ ] 上传所有 OG 图片到网站 `/images/og/` 目录
- [ ] 为首页添加 OG 标签
- [ ] 为 AI vs 人工对比页添加 OG 标签
- [ ] 为 vs Dext 页面添加 OG 标签
- [ ] 为 vs AutoEntry 页面添加 OG 标签
- [ ] 为 HSBC 页面添加 OG 标签
- [ ] 为恒生页面添加 OG 标签
- [ ] 使用 Facebook Debugger 测试所有页面
- [ ] WhatsApp 测试分享效果
- [ ] 监控社交媒体分享数据

---

## 📞 需要帮助？

### 常见问题：

**Q: 图片不显示怎么办？**
A: 
1. 确认图片 URL 可以通过 HTTPS 访问
2. 使用 Facebook Debugger 清除缓存
3. 等待 24-48 小时

**Q: 需要为所有页面生成 OG 图片吗？**
A: 
- **必须**：首页、主要对比页、热门银行页
- **推荐**：所有 landing pages
- **可选**：博客文章、帮助页面

**Q: 图片可以用其他尺寸吗？**
A: 
- **推荐**：1200 x 630 px（Facebook/WhatsApp 标准）
- **最小**：600 x 315 px
- **最大**：不超过 5 MB

---

## 🎯 下一步

1. **今天**：上传图片，为前3个页面添加 OG 标签
2. **本周**：完成所有6个页面的 OG 标签
3. **下周**：为其他重要页面生成 OG 图片
4. **持续**：监控社交媒体分享数据

---

**记住**：OG 图片是提升社交媒体分享率的关键！  
**立即开始添加 OG 标签！** 🚀

