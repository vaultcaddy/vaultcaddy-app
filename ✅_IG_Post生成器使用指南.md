# ✅ IG Post 生成器使用指南

## 🎉 **已成功创建！**

### **生成的内容**

✅ **5 张 IG 图片**（1080x1080px）
1. 痛点展示 - "你的時間值幾多錢？"
2. 免费试用优惠 - "立即免費試用"
3. 成本对比 - "人手處理 vs AI 自動化"
4. 准确率对比 - "錯誤率對比"
5. CTA 行动呼吁 - "VaultCaddy 品牌展示"（紫色渐变）

✅ **贴文文案**（caption.txt）
- 包含完整文案
- 30个精选标签
- 直接复制使用

---

## 🚀 **一键生成（30秒）**

### **方法 1：使用命令行（推荐）**

```bash
cd /Users/cavlinyeung/ai-bank-parser/ig-post-generator
./run.sh
```

### **方法 2：直接运行 Python**

```bash
cd /Users/cavlinyeung/ai-bank-parser/ig-post-generator
python3 generator.py
```

### **输出位置**

```
ig-post-generator/ig-posts/
├── 01_痛點展示.png
├── 02_免費試用優惠.png
├── 03_成本對比.png
├── 04_準確率對比.png
├── 05_CTA行動呼籲.png
├── caption.txt
└── generation_report.json
```

---

## 📱 **发布到 Instagram**

### **步骤 1：传输到手机**

#### **方法 A：AirDrop（推荐）**
1. 在 Mac 上打开 `ig-posts` 文件夹
2. 选中 5 张图片
3. 右键 → 共享 → AirDrop → 选择你的 iPhone

#### **方法 B：iCloud**
1. 将图片拖到 iCloud Drive
2. 在 iPhone 上打开文件 App
3. 保存图片到相册

#### **方法 C：Email/WhatsApp**
1. 将图片发送给自己
2. 在手机上保存

---

### **步骤 2：创建 Instagram Carousel**

1. **打开 Instagram App**
2. **点击 "+"** 创建新帖子
3. **选择 "帖子"**
4. **点击多选图标**（右上角）
5. **按顺序选择 5 张图片**：
   ```
   01_痛點展示.png
   02_免費試用優惠.png
   03_成本對比.png
   04_準確率對比.png
   05_CTA行動呼籲.png
   ```
6. **点击 "下一步"**

---

### **步骤 3：添加文案**

1. **复制 caption.txt 的内容**
   - 在 Mac 上打开 `caption.txt`
   - 全选并复制

2. **粘贴到 Instagram**
   - 在 "撰写说明..." 区域粘贴
   - 检查标签是否正确（应该自动变蓝）

3. **添加地理位置**（可选）
   - 搜索 "香港" 或 "Hong Kong"
   - 选择一个地点

---

### **步骤 4：发布设置**

1. **标记其他账号**（可选）
   - 可以标记合作伙伴或客户

2. **设置为商业帖子**（如果有商业账号）
   - 点击 "高级设置"
   - 启用 "将此帖子设为商业帖子"

3. **发布时间**
   - **立即发布**: 直接点击 "分享"
   - **定时发布**: 需要商业账号 + Meta Business Suite

---

## ⏰ **最佳发布时间**

### **推荐时间（香港时区）**
- 🌅 **早上 8-9AM**（上班途中）
- 🍽️ **中午 12-1PM**（午餐时间）
- 🌆 **晚上 7-9PM**（下班后）

### **推荐日期**
- 📅 **週二至週四**（工作日参与度最高）
- ❌ 避免週末（B2B 产品）

---

## 🎨 **自定义内容**

### **修改图片内容**

编辑 `generator.py`：

```python
def generate_post_1_intro(self):
    # 修改这里的文字
    lines=['你的新标题', '第二行']
```

### **修改配色**

```python
self.colors = {
    'primary': '#你的品牌色',
    'bg_beige': '#你的背景色'
}
```

### **修改文案**

编辑 `generate_caption_and_tags()` 函数中的文案

### **重新生成**

```bash
cd /Users/cavlinyeung/ai-bank-parser/ig-post-generator
python3 generator.py
```

---

## 📊 **内容策略建议**

### **第 1 周**
- **帖子 1**：品牌介绍（使用当前生成的 5 张图）
- **Story**：behind-the-scenes（团队介绍）

### **第 2 周**
- **帖子 2**：客户案例（如果有）
- **帖子 3**：使用教程（3 步开始使用）

### **第 3 周**
- **帖子 4**：行业洞察（会计自动化趋势）
- **帖子 5**：FAQ（常见问题）

### **第 4 周**
- **帖子 6**：成功故事（客户反馈）
- **帖子 7**：优惠活动（限时折扣）

---

## 📈 **追踪数据**

### **关键指标**
- 👁️ **触及人数**（Reach）
- ❤️ **互动率**（Engagement Rate）
- 💬 **评论数**（Comments）
- 🔗 **链接点击**（Link Clicks）
- 👤 **新追踪者**（New Followers）

### **使用 Instagram Insights**
1. 打开帖子
2. 点击 "查看数据分析"
3. 查看详细数据

---

## 🔄 **持续优化**

### **如果触及率低**
- 调整发帖时间
- 增加标签数量
- 与其他账号互动

### **如果互动率低**
- 强化痛点描述
- 优化 CTA 设计
- 添加问题引导评论

### **如果转换率低**
- 简化注册流程
- 强调免费试用
- 添加社会证明

---

## 💡 **进阶功能（未来）**

### **TODO：添加 QR Code**

```bash
pip3 install qrcode[pil]
```

在 `generator.py` 中：

```python
import qrcode

qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data('https://vaultcaddy.com')
qr.make(fit=True)
qr_img = qr.make_image(fill_color='white', back_color=(107, 95, 207))
```

### **TODO：批量生成不同主题**

- 系列 A：成本节省
- 系列 B：时间管理
- 系列 C：客户案例
- 系列 D：行业洞察

---

## ✅ **测试超额计费（方法 C）**

### **现在 billing.html 已添加测试按钮**

1. 访问 https://vaultcaddy.com/billing.html
2. 点击"🧪 測試模式（測試超額計費）"
3. 使用测试卡：4242 4242 4242 4242
4. 完成订阅（获得 100 测试 Credits）
5. 在 Firebase 中修改 Credits 为 2
6. 上传 5 页文档测试超额

**详细步骤**: 见 `🧪_测试超额计费指南.md`

---

## 📋 **快速检查清单**

### **发布前**
- [ ] 5 张图片已生成
- [ ] 在手机上预览效果
- [ ] 文案已复制
- [ ] 标签已检查
- [ ] 选择发布时间
- [ ] 添加地理位置

### **发布后**
- [ ] 监控前 2 小时的数据
- [ ] 及时回复评论
- [ ] 分享到 Story
- [ ] 固定到个人资料（如果效果好）

---

## 🎯 **总结**

### **✅ 已完成**
1. IG Post 自动生成器（Python 工具）
2. 5 张高质量图片（1080x1080）
3. 完整贴文文案和标签
4. 临时测试按钮（测试超额计费）
5. 使用文档和指南

### **⏳ 下一步**
1. 将图片传到手机
2. 发布到 Instagram
3. 测试超额计费功能
4. 监控帖子数据

---

**工具位置**: `/Users/cavlinyeung/ai-bank-parser/ig-post-generator/`  
**一键运行**: `./run.sh`  
**输出位置**: `ig-posts/`

---

**🎨 图片已生成并且中文显示正常！**  
**📱 可以开始准备发布了！** 🚀


