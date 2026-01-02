# 📊 Google Sheet反向链接追踪模板

**如何使用**: 复制下面的内容，粘贴到Google Sheet

---

## 方法1: 直接复制粘贴到Google Sheet

### 步骤：
1. 打开Google Sheets (sheets.google.com)
2. 创建新表格，命名为 "VaultCaddy反向链接追踪"
3. 复制下面的表格内容（从"日期"开始）
4. 在Google Sheet的A1单元格粘贴
5. 格式化：选择第1行 → 加粗 → 背景颜色（蓝色）

---

## 表格模板（复制下面的内容）

```
日期	平台	类型	URL	标题/描述	Domain Authority	状态	预估流量	备注
01/02/2025	Quora	Q&A回答	https://quora.com/...	"Best way to convert bank statements"	DA 90	✅ Live	5-10	使用对比型模板
01/03/2025	Reddit	主帖	https://reddit.com/r/Accounting/...	"I automated bank reconciliation"	DA 95	✅ Live	20-30	142 upvotes
01/04/2025	Medium	文章	https://medium.com/@vaultcaddy/...	"Bank Statement Automation Guide"	DA 95	✅ Live	50-100	发布在The Startup
01/05/2025	LinkedIn	文章	https://linkedin.com/pulse/...	"CFO Guide to Automation"	DA 98	✅ Live	30-50	127 likes
01/06/2025	HK88DB	目录	https://hk88db.com/...	VaultCaddy商业目录	DA 35	✅ Live	2-5	香港本地目录
01/07/2025	Product Hunt	产品	https://producthunt.com/posts/...	VaultCaddy Launch	DA 92	⏳ 审核中	100-200	等待审核
01/08/2025	G2	评论	https://g2.com/products/vaultcaddy	VaultCaddy Reviews	DA 85	✅ Live	20-40	5 reviews
01/09/2025	Capterra	目录	https://capterra.com/p/vaultcaddy	VaultCaddy Listing	DA 82	✅ Live	15-25	Accounting Software分类
01/10/2025	Quora	Q&A回答	https://quora.com/...	"QuickBooks import methods"	DA 90	✅ Live	8-12	使用问题解决型模板
01/11/2025	Reddit	评论	https://reddit.com/r/SmallBusiness/...	帮助用户解决问题	DA 95	✅ Live	5-10	32 upvotes
```

---

## 方法2: 使用预设公式的高级模板

### 在Google Sheet中创建以下工作表：

**Sheet 1: 反向链接追踪**

| 列 | 说明 | 格式 |
|---|---|---|
| A | 日期 | 日期格式 (MM/DD/YYYY) |
| B | 平台 | 文本 |
| C | 类型 | 下拉选单（Q&A, 主帖, 评论, 目录, 文章, 产品） |
| D | URL | 超链接 |
| E | 标题/描述 | 文本 |
| F | Domain Authority | 数字 (0-100) |
| G | 状态 | 下拉选单（✅ Live, ⏳ 审核中, ❌ 被拒, 🔄 待跟进） |
| H | 预估流量/月 | 数字 |
| I | 备注 | 文本 |

---

**Sheet 2: 统计仪表板**

复制以下公式到相应单元格：

```
总链接数:
=COUNTA(反向链接追踪!A:A)-1

Live链接数:
=COUNTIF(反向链接追踪!G:G,"✅ Live")

审核中:
=COUNTIF(反向链接追踪!G:G,"⏳ 审核中")

预估总流量:
=SUM(反向链接追踪!H:H)

平均DA:
=AVERAGE(反向链接追踪!F:F)

高质量链接 (DA 50+):
=COUNTIFS(反向链接追踪!F:F,">=50",反向链接追踪!G:G,"✅ Live")

中等质量链接 (DA 30-50):
=COUNTIFS(反向链接追踪!F:F,">=30",反向链接追踪!F:F,"<50",反向链接追踪!G:G,"✅ Live")

基础链接 (DA <30):
=COUNTIFS(反向链接追踪!F:F,"<30",反向链接追踪!G:G,"✅ Live")
```

---

## 方法3: 按平台分类追踪

### 创建多个Sheet页签：

**Sheet: Quora追踪**
```
日期	问题URL	回答URL	问题标题	Upvotes	Views	预估流量	备注
01/02	https://...	https://...	"Best way to convert bank statements"	15	127	5-10	使用对比型模板
01/05	https://...	https://...	"QuickBooks import methods"	8	89	3-5	使用问题解决型
```

**Sheet: Reddit追踪**
```
日期	Subreddit	帖子类型	URL	标题	Upvotes	Comments	预估流量	备注
01/03	r/Accounting	主帖	https://...	"I automated bank reconciliation"	142	28	20-30	很多正面评论
01/07	r/SmallBusiness	评论	https://...	帮助用户	32	5	5-10	建立信任
```

**Sheet: 目录追踪**
```
日期	目录名称	类别	URL	DA	状态	审核时间	备注
01/06	HK88DB	电脑软件	https://...	35	✅ Live	1天	香港本地
01/08	G2	Accounting	https://...	85	✅ Live	3天	需要5个评论
01/09	Capterra	Accounting	https://...	82	⏳ 审核中	pending	提交1周
```

**Sheet: Guest Post追踪**
```
日期	网站	Outreach状态	回复	文章标题	DA	发布日期	URL	备注
01/10	AccountingWEB	已发送	等待中	"AI in Bank Reconciliation"	72	-	-	1周无回复，跟进
01/11	Small Business Trends	已发送	拒绝	"5 Ways to Cut Costs"	68	-	-	不接受外部文章
01/12	Tech in Asia	草稿中	-	"Hong Kong Fintech"	78	-	-	准备pitch
```

---

## 数据可视化建议

### 在Google Sheet中创建图表：

**图表1: 每周新增链接趋势**
- 类型: 折线图
- X轴: 日期（按周分组）
- Y轴: 新增链接数
- 数据: 反向链接追踪!A:A

**图表2: 平台分布饼图**
- 类型: 饼图
- 数据: 反向链接追踪!B:B（平台列）
- 显示: 各平台占比

**图表3: DA分布柱状图**
- 类型: 柱状图
- 分类: <30, 30-50, 50+
- Y轴: 链接数量

**图表4: 预估流量增长**
- 类型: 面积图
- X轴: 日期
- Y轴: 累计预估流量
- 公式: 累加H列

---

## 每周检查清单（在Sheet中添加）

**Sheet: 每周任务**

```
Week	任务	目标	完成	备注
Week 1 (01/02-01/08)	商业目录注册	15个	12	✅ 完成80%
Week 1	Quora回答	5个	7	✅ 超额完成
Week 1	Reddit参与	评论15次	18	✅ 建立karma
Week 2 (01/09-01/15)	Medium文章	2篇	⏳	进行中
Week 2	LinkedIn文章	1篇	⏳	待开始
Week 2	Guest Post outreach	5封邮件	⏳	待开始
Week 3 (01/16-01/22)	Quora持续	3个/周	⏳	待开始
Week 3	Reddit主帖	1个	⏳	待开始
Week 3	论坛参与	10次	⏳	待开始
Week 4 (01/23-01/29)	Guest Post跟进	所有outreach	⏳	待开始
Week 4	目录审核跟进	检查所有审核中	⏳	待开始
Week 4	月度总结	报告	⏳	待开始
```

---

## Domain Authority参考

常见平台的DA值（供填写参考）：

| 平台 | DA |
|---|---|
| Quora | 90 |
| Reddit | 95 |
| Medium | 95 |
| LinkedIn | 98 |
| YouTube | 100 |
| Facebook | 96 |
| Twitter | 94 |
| Product Hunt | 92 |
| G2 | 85 |
| Capterra | 82 |
| Yelp | 93 |
| Google My Business | 100 |
| Tech in Asia | 78 |
| AccountingWEB | 72 |
| HK88DB | 35 |
| Discuss.com.hk | 42 |
| 地区商业目录 | 20-40 |
| 个人博客 | 10-30 |

---

## 自动化建议

### 使用Google Sheets公式自动化：

**1. 自动计算链接年龄**
```
=TODAY()-A2
```
（在"天数"列，计算从发布到现在多少天）

**2. 条件格式化**
- DA >= 70: 绿色背景
- DA 50-69: 黄色背景
- DA < 50: 白色背景

**3. 自动提醒**
使用Google Sheets的通知功能：
- 当"状态"列从"⏳ 审核中"变为"✅ Live"时发送email通知

**4. 每周自动报告**
设置Google Apps Script，每周五自动发送：
- 本周新增链接数
- 累计链接总数
- 预估流量增长
- 待跟进任务

---

## 导出和分享

### 如何分享Google Sheet：

1. **与团队共享**:
   - 点击右上角"共享"
   - 输入团队成员email
   - 设置权限（查看者/评论者/编辑者）

2. **定期导出**:
   - File → Download → Excel (.xlsx)
   - 每月备份一次

3. **创建报告**:
   - File → Download → PDF
   - 用于月度总结报告

---

## 移动端使用

**Google Sheets App (iOS/Android):**
- 随时随地更新
- 扫描二维码直接添加URL
- 拍照保存截图作为备注

**快速添加新链接（手机）:**
1. 打开Google Sheets App
2. 点击"+"
3. 选择"反向链接追踪"表格
4. 添加新行
5. 填写必填字段（日期、平台、URL、状态）

---

## 示例：完整的第一周数据

复制粘贴到你的Google Sheet开始使用：

```
日期	平台	类型	URL	标题/描述	Domain Authority	状态	预估流量/月	备注
01/02/2025	Quora	Q&A回答	https://quora.com/answer1	Best way to convert bank statements	90	✅ Live	5-10	127 views, 15 upvotes
01/02/2025	Quora	Q&A回答	https://quora.com/answer2	How to import to QuickBooks	90	✅ Live	3-5	89 views, 8 upvotes
01/03/2025	Reddit	主帖	https://reddit.com/r/Accounting/post1	I automated bank reconciliation	95	✅ Live	20-30	142 upvotes, 28 comments
01/03/2025	Reddit	评论	https://reddit.com/r/SmallBusiness/comment1	帮助用户解决CSV问题	95	✅ Live	2-3	建立信任
01/03/2025	Reddit	评论	https://reddit.com/r/Bookkeeping/comment2	分享经验	95	✅ Live	2-3	12 upvotes
01/04/2025	Medium	文章	https://medium.com/@vaultcaddy/automation	Bank Statement Automation Guide	95	✅ Live	50-100	发布在The Startup, 243 claps
01/05/2025	LinkedIn	文章	https://linkedin.com/pulse/cfo-guide	CFO Guide to Automation	98	✅ Live	30-50	127 likes, 45 comments
01/06/2025	HK88DB	目录	https://hk88db.com/vaultcaddy	VaultCaddy商业目录	35	✅ Live	2-5	香港本地目录
01/06/2025	GoHere.hk	目录	https://gohere.hk/vaultcaddy	IT服务目录	28	⏳ 审核中	1-2	等待审核1周
01/07/2025	Product Hunt	产品	https://producthunt.com/posts/vaultcaddy	VaultCaddy Launch	92	⏳ 审核中	100-200	计划01/15发布
01/08/2025	G2	评论	https://g2.com/products/vaultcaddy	VaultCaddy Reviews	85	✅ Live	20-40	需要5个评论才能排名
01/09/2025	Capterra	目录	https://capterra.com/p/vaultcaddy	VaultCaddy Listing	82	✅ Live	15-25	Accounting Software分类
01/09/2025	GetApp	目录	https://getapp.com/vaultcaddy	VaultCaddy Profile	78	⏳ 审核中	10-15	等待审核
01/10/2025	Quora	Q&A回答	https://quora.com/answer3	Best accounting software	90	✅ Live	8-12	使用个人故事型模板
01/10/2025	Trustpilot	评论	https://trustpilot.com/vaultcaddy	Company Profile	82	✅ Live	5-8	需要客户评论
```

---

## 总结统计（第一周）

基于上面的示例数据：

```
总链接数: 15
✅ Live: 11
⏳ 审核中: 4

平台分布:
- Quora: 3个
- Reddit: 3个
- Medium: 1个
- LinkedIn: 1个
- 商业目录: 7个

DA分布:
- 高质量 (50+): 9个 (60%)
- 中等质量 (30-50): 2个 (13.3%)
- 基础 (<30): 0个 (0%)

预估总流量: 279-518访客/月

下周目标:
- 继续Quora (5个新回答)
- Reddit主帖 (1个)
- Medium文章 (1个)
- Guest Post outreach (5个)
```

---

**准备好了吗？立即创建你的反向链接追踪表！** 📊

复制上面的模板到Google Sheets，开始追踪你的SEO进度！
