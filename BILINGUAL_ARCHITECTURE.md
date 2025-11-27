# VaultCaddy 雙語架構方案

## 📅 更新時間
2025年11月27日 下午 4:50

---

## 🎯 最終決定：方案 B

### 架構設計

```
vaultcaddy.com/
├── index.html          (繁體中文首頁)
├── dashboard.html      (繁體中文)
├── firstproject.html   (繁體中文)
├── account.html        (繁體中文)
├── billing.html        (繁體中文)
├── privacy.html        (繁體中文)
├── terms.html          (繁體中文)
└── en/
    ├── home.html       (英文首頁)
    ├── dashboard.html  (英文)
    ├── firstproject.html (英文)
    ├── account.html    (英文)
    ├── billing.html    (英文)
    ├── privacy.html    (英文)
    └── terms.html      (英文)
```

---

## ❌ 為什麼不用 /tc/ 目錄？

### 問題
1. **瀏覽器緩存混淆**：即使文件內容相同，瀏覽器顯示不一致
2. **路徑複雜**：/tc/home.html vs index.html 容易混淆
3. **不必要**：VaultCaddy 主要服務香港，繁體中文是主要語言

### 嘗試過的方案
- ✅ 創建 /tc/ 目錄
- ✅ 複製所有文件
- ✅ 更新 107 個鏈接
- ❌ 但瀏覽器顯示不一致

### 最終決定
- **刪除 /tc/ 目錄**
- **根目錄 = 繁體中文**（主要版本）
- **創建 /en/ 目錄**（英文版本）

---

## ✅ 方案 B 的優勢

### 1. 簡單清晰
```
繁體中文：https://vaultcaddy.com/
英文：https://vaultcaddy.com/en/
```

### 2. SEO 友好
- 根目錄為主要市場（香港）
- `/en/` 清楚標示英文版本

### 3. 用戶體驗
- 預設繁體中文（香港用戶）
- 可選擇切換到英文

### 4. 維護簡單
- 只有兩個版本
- 不會混淆路徑

---

## 📋 下一步計劃

### 1. 創建英文版本 (/en/)
**任務**：
- [ ] 創建 `/en/` 目錄
- [ ] 複製根目錄所有文件到 `/en/`
- [ ] 翻譯所有內容為英文
- [ ] 更新所有鏈接為 `/en/` 路徑

**頁面清單**：
1. home.html (原 index.html)
2. dashboard.html
3. firstproject.html
4. account.html
5. billing.html
6. privacy.html
7. terms.html

### 2. 添加語言切換器
**位置**：導航欄右上角

**功能**：
- 繁體中文 ⇄ English
- 保持當前頁面位置
  - index.html ↔ /en/home.html
  - dashboard.html ↔ /en/dashboard.html
  - 等等...

### 3. 語言偏好保存
- 使用 localStorage 保存用戶選擇
- 下次訪問時自動切換到偏好語言

### 4. 首次訪問語言選擇
**選項 A**：根據瀏覽器語言自動選擇
```javascript
if (navigator.language.startsWith('en')) {
    // 重定向到 /en/
}
```

**選項 B**：始終顯示繁體中文（推薦）
- 繁體中文為預設
- 用戶可手動切換

---

## 🛠️ 技術實現

### 語言切換器 HTML
```html
<div class="language-switcher">
    <button onclick="switchLanguage('tc')" class="lang-btn active">
        繁體中文
    </button>
    <button onclick="switchLanguage('en')" class="lang-btn">
        English
    </button>
</div>
```

### 語言切換 JavaScript
```javascript
function switchLanguage(lang) {
    const currentPath = window.location.pathname;
    
    if (lang === 'en') {
        // 繁體中文 → 英文
        if (currentPath === '/' || currentPath === '/index.html') {
            window.location.href = '/en/home.html';
        } else {
            const filename = currentPath.split('/').pop();
            window.location.href = '/en/' + filename;
        }
    } else {
        // 英文 → 繁體中文
        const filename = currentPath.split('/').pop();
        if (filename === 'home.html') {
            window.location.href = '/index.html';
        } else {
            window.location.href = '/' + filename;
        }
    }
    
    // 保存偏好
    localStorage.setItem('preferredLanguage', lang);
}
```

---

## 📊 當前狀態

### 完成
- ✅ 根目錄繁體中文版本（最新）
- ✅ 所有內容更新
  - 年費：HKD 744
  - 服務說明：PDF/JPG/PNG
  - UI 調整：向上 10pt
- ✅ 刪除 /tc/ 目錄
- ✅ 清理相關文件

### 待完成
- [ ] 創建 /en/ 目錄
- [ ] 翻譯所有內容
- [ ] 添加語言切換器
- [ ] 測試語言切換功能

---

## 🎉 優勢總結

| 項目 | 方案 A (/tc/ + /en/) | 方案 B (根目錄 + /en/) |
|------|---------------------|----------------------|
| URL 簡潔 | ❌ /tc/home.html | ✅ / 或 /index.html |
| SEO | 🟡 需要額外配置 | ✅ 根目錄最佳 |
| 維護 | 🟡 三個版本 | ✅ 兩個版本 |
| 用戶體驗 | 🟡 需要選擇 | ✅ 預設繁體 |
| 瀏覽器緩存 | ❌ 容易混淆 | ✅ 清楚分離 |

---

**決定**：✅ 方案 B（根目錄 + /en/）  
**原因**：簡單、清晰、SEO 友好、用戶體驗佳  
**下一步**：創建 /en/ 英文版本 🚀

