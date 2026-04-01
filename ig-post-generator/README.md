# 📱 VaultCaddy IG Post 自動生成器

## 🎯 **功能**

一鍵生成 5 張 IG 帖子圖片，包括：

1. **第 1 張**：痛點展示（"你的時間值幾多錢？"）
2. **第 2 張**：免費試用優惠
3. **第 3 張**：成本對比（人手 vs AI）
4. **第 4 張**：準確率對比
5. **第 5 張**：CTA 行動呼籲（品牌展示 + QR Code）

**同時自動生成**：
- ✅ 貼文文案（caption.txt）
- ✅ 標籤（30個精選標籤）
- ✅ 生成報告（generation_report.json）

---

## 🚀 **快速開始**

### **步驟 1：安裝依賴**

```bash
cd /Users/cavlinyeung/ai-bank-parser/ig-post-generator
pip3 install -r requirements.txt
```

### **步驟 2：一鍵生成**

```bash
python3 generator.py
```

### **步驟 3：查看結果**

```bash
open ig-posts/
```

---

## 📊 **輸出結構**

```
ig-posts/
├── 01_痛點展示.png          (1080x1080)
├── 02_免費試用優惠.png      (1080x1080)
├── 03_成本對比.png          (1080x1080)
├── 04_準確率對比.png        (1080x1080)
├── 05_CTA行動呼籲.png       (1080x1080)
├── caption.txt             (貼文文案)
└── generation_report.json  (生成報告)
```

---

## 🎨 **設計規格**

### **尺寸**
- 寬度：1080px
- 高度：1080px
- 格式：PNG
- 品質：95%

### **配色方案**
- **主紫色**：#6B5FCF
- **淺紫色**：#9B87E8
- **黃色強調**：#FFC107
- **綠色成功**：#10B981
- **米色背景**：#F5F3EF

### **字體**
- 使用系統字體：PingFang（macOS）
- 自動降級到默認字體（其他系統）

---

## 📝 **自定義內容**

### **修改圖片內容**

編輯 `generator.py`，找到對應函數：

```python
def generate_post_1_intro(self):
    # 修改這裡的文字內容
    lines=['你的時間', '值幾多錢？']
```

### **修改配色**

```python
self.colors = {
    'primary': '#6B5FCF',      # 改為你的品牌色
    'bg_beige': '#F5F3EF'      # 改為你的背景色
}
```

### **修改文案**

編輯 `generate_caption_and_tags()` 函數中的文案

---

## 🔧 **進階功能**

### **添加 QR Code（TODO）**

```bash
pip3 install qrcode[pil]
```

在 `generator.py` 中添加：

```python
import qrcode

def add_qr_code(self, img, url, position):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='white', back_color='transparent')
    qr_img = qr_img.resize((200, 200))
    img.paste(qr_img, position)
    return img
```

### **添加 Logo 圖片**

```python
logo = Image.open('logo.png')
logo = logo.resize((150, 150))
img.paste(logo, (465, 80), logo)  # 如果 logo 有透明度
```

---

## 🎬 **發帖流程**

### **步驟 1：生成圖片**
```bash
python3 generator.py
```

### **步驟 2：檢查輸出**
```bash
open ig-posts/
```

### **步驟 3：調整（如需要）**
- 修改 `generator.py`
- 重新運行

### **步驟 4：上傳到 IG**
1. 將 5 張圖片傳到手機
2. 打開 Instagram App
3. 創建 Carousel 帖子（多圖輪播）
4. 添加圖片（順序：01 → 05）
5. 複製 `caption.txt` 的內容作為文案
6. 發布！

---

## 📈 **最佳實踐**

### **發帖時間**
- ⏰ 早上 8-9AM（上班途中）
- ⏰ 中午 12-1PM（午餐時間）
- ⏰ 晚上 7-9PM（下班後）

### **發帖頻率**
- 📅 每週 2-3 次
- 📅 週二至週四效果最好

### **互動策略**
- 💬 及時回覆評論（1小時內）
- ❤️ 與類似帳號互動
- 📊 追蹤數據分析

---

## 🛠️ **故障排查**

### **問題 1：找不到字體**
```
解決：自動降級到默認字體，或下載 PingFang 字體
```

### **問題 2：圖片模糊**
```python
# 增加圖片品質
img.save(output_path, quality=100)
```

### **問題 3：顏色不準確**
```python
# 確保使用正確的 HEX 值
self.hex_to_rgb('#6B5FCF')
```

---

## 🎨 **未來改進**

- [ ] 添加 QR Code 生成
- [ ] 支持自定義字體
- [ ] 添加圖片濾鏡效果
- [ ] 支持視頻生成（IG Reels）
- [ ] AI 自動生成文案變體
- [ ] 批量生成多套方案

---

## 📞 **需要幫助？**

- 📧 Email: support@vaultcaddy.com
- 💬 IG: @vaultcaddy.hk

---

**生成器版本**: 1.0.0  
**最後更新**: 2025-12-13

