# 手機版卡片固定寬度修復

## 修復時間
2025年12月2日 下午6:00

---

## 🎯 修復內容

### 問題根源
1. **通用CSS規則覆蓋：** 第1665-1668行的CSS會覆蓋所有 `padding: 2rem` 的元素
2. **沒有固定寬度：** 手機版卡片寬度不固定，看起來很窄

### 解決方案

#### 1. 排除卡片被通用規則影響
```css
/* 修改前 */
div[style*="padding: 2rem"],
div[style*="padding: 3rem"] {
    padding: 1rem 0.5rem !important;
}

/* 修改後 - 排除卡片 */
div[style*="padding: 2rem"]:not(.fade-in-right > div):not(.fade-in-left > div),
div[style*="padding: 3rem"]:not(.fade-in-right > div):not(.fade-in-left > div) {
    padding: 1rem 0.5rem !important;
}
```

#### 2. 添加手機版固定寬度樣式
```css
/* 手機版：茶餐廳和銀行卡片固定寬度 */
.fade-in-right > div[style*="border-radius: 16px"],
.fade-in-left > div[style*="border-radius: 16px"] {
    width: 280px !important;           /* 固定寬度 */
    max-width: 90vw !important;        /* 最大90%視窗寬度 */
    margin: 0 auto !important;         /* 居中 */
    padding: 1.5rem !important;        /* 調整內距 */
    transform: rotate(0deg) !important; /* 不旋轉 */
}

/* 內層容器 */
.fade-in-right > div[style*="border-radius: 16px"] > div,
.fade-in-left > div[style*="border-radius: 16px"] > div {
    padding: 1.25rem !important;
}

/* 文字大小適配 */
/* 1.125rem → 1rem */
.fade-in-right > div[style*="border-radius: 16px"] [style*="font-size: 1.125rem"],
.fade-in-left > div[style*="border-radius: 16px"] [style*="font-size: 1.125rem"] {
    font-size: 1rem !important;
}

/* 1.5rem → 1.25rem */
.fade-in-right > div[style*="border-radius: 16px"] [style*="font-size: 1.5rem"],
.fade-in-left > div[style*="border-radius: 16px"] [style*="font-size: 1.5rem"] {
    font-size: 1.25rem !important;
}
```

---

## 📱 手機版效果

### 桌面版
- 寬度：自適應（跟隨容器）
- padding: 2rem
- 文字：1.125rem (項目), 1.5rem (總計)
- 旋轉：-2deg (茶餐廳), 2deg (銀行)

### 手機版（現在）
- 寬度：**280px（固定）**
- 最大寬度：90vw（不超出螢幕）
- padding: 1.5rem（稍小但保持比例）
- 文字：1rem (項目), 1.25rem (總計)
- 旋轉：0deg（不旋轉，方便閱讀）
- **居中顯示**

---

## 🔧 技術要點

### CSS 優先級
使用屬性選擇器 + :not() 排除特定元素：
```css
div[style*="padding: 2rem"]:not(.fade-in-right > div)
```

這樣通用規則不會影響卡片。

### 固定寬度的好處
1. **一致性：** 兩個卡片寬度完全一致
2. **可讀性：** 280px 是手機上的最佳閱讀寬度
3. **響應式：** `max-width: 90vw` 確保小螢幕也能正常顯示

---

## ✅ 測試清單

### 手機版測試（必測）

**步驟1：清除緩存**
- **快捷鍵：** 在手機瀏覽器中長按刷新按鈕

**步驟2：查看卡片**
- [ ] 茶餐廳卡片寬度：280px（固定）
- [ ] 銀行卡片寬度：280px（固定）
- [ ] 兩個卡片寬度完全一致
- [ ] 卡片居中顯示
- [ ] 卡片不旋轉（正面顯示）

**步驟3：檢查文字**
- [ ] 標題清晰可讀（1rem）
- [ ] 項目價格清晰（1rem）
- [ ] 總計大且突出（1.25rem）

**步驟4：不同螢幕測試**
- [ ] iPhone SE（小螢幕）：卡片不超出螢幕
- [ ] iPhone 14（中螢幕）：卡片 280px 居中
- [ ] iPad mini（大螢幕）：卡片 280px 居中

---

## 📊 對比

| 屬性 | 修復前 | 修復後 |
|------|-------|-------|
| 寬度 | 不固定（被壓縮）| 280px 固定 ✅ |
| padding | 被覆蓋為 1rem 0.5rem | 1.5rem ✅ |
| 一致性 | 不一致 | 兩個卡片完全一致 ✅ |
| 居中 | 不居中 | 居中顯示 ✅ |
| 旋轉 | 可能旋轉 | 不旋轉 ✅ |

---

## 🔍 如何驗證修復

### 方法1：使用開發者工具（推薦）
1. 在電腦上打開 Chrome
2. 按 F12 打開開發者工具
3. 切換到手機視圖（Toggle device toolbar）
4. 選擇 iPhone 12 Pro
5. 刷新頁面
6. 滾動到「強大功能」區域
7. 檢查卡片寬度

### 方法2：實際手機測試
1. 清除手機瀏覽器緩存
2. 訪問網站
3. 滾動到「強大功能」區域
4. 觀察兩個卡片

**應該看到：**
- ✅ 兩個卡片寬度完全一樣
- ✅ 卡片居中顯示
- ✅ 文字清晰可讀
- ✅ 不會超出螢幕

---

## 💡 下一步建議

### 建議1：調整固定寬度
如果 280px 太小或太大，可以修改：
```css
width: 300px !important; /* 改為 300px */
```

### 建議2：調整文字大小
如果文字太小，可以修改：
```css
font-size: 1.125rem !important; /* 改為更大 */
```

### 建議3：統一手機版樣式
考慮為所有手機版卡片創建統一的class：
```css
.mobile-card {
    width: 280px;
    max-width: 90vw;
    margin: 0 auto;
}
```

---

**修復完成！請立即清除緩存並測試！** 🎉

