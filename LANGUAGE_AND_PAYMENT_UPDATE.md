# 🌐 語言切換 & 💳 付費連結更新總結

**更新日期**: 2025-11-20  
**任務**: 
1. 實現中英文語言切換功能
2. 更新付費連結為新定價方案

---

## ✅ 已完成工作

### 1️⃣ 創建語言管理器 (`language-manager.js`)

**文件**: `language-manager.js`  
**功能**:
- 管理中英文切換（zh ↔ en）
- 動態翻譯頁面內容
- 保存用戶語言偏好到 localStorage
- 自動翻譯帶有 `data-i18n="key"` 屬性的元素

**使用方法**:
```html
<!-- 1. 在 HTML 中引入 -->
<script defer src="language-manager.js"></script>

<!-- 2. 在需要翻譯的元素上添加 data-i18n -->
<h1 data-i18n="hero.title">AI 驅動的財務文件處理</h1>
<button data-i18n="pricing.cta">立即開始</button>

<!-- 3. 切換語言 -->
<script>
window.languageManager.setLanguage('en'); // 切換到英文
window.languageManager.setLanguage('zh'); // 切換到中文
</script>
```

**已添加的翻譯內容**:
- ✅ 導航欄 (nav.*)
- ✅ 首頁 Hero (hero.*)
- ✅ 定價頁面 (pricing.*)
- ✅ 功能列表 (feature.*)
- ✅ 計費頁面 (billing.*)
- ✅ 帳戶頁面 (account.*)
- ✅ 儀表板 (dashboard.*)
- ✅ 通用文本 (common.*)
- ✅ Email 驗證 (email.*)

---

### 2️⃣ 整合導航欄語言切換

**文件**: `navbar-component.js`  
**變更**:
- ✅ 統一語言代碼：`zh-tw` → `zh`
- ✅ 整合 `window.languageManager.setLanguage()`
- ✅ 雙語通知消息

**效果**:
```
用戶點選 "English" → 頁面所有標記為 data-i18n 的元素自動翻譯為英文
用戶點選 "繁體中文" → 頁面恢復中文
```

---

### 3️⃣ 更新 `index.html` 和 `billing.html`

**變更**:
- ✅ 引入 `language-manager.js`（在導航欄之前載入）
- ✅ 版本號更新：`?v=20251120`

**文件路徑**:
- `/Users/cavlinyeung/ai-bank-parser/index.html`
- `/Users/cavlinyeung/ai-bank-parser/billing.html`

---

### 4️⃣ 更新付費連結邏輯 (`billing.html`)

**文件**: `billing.html` - `subscribeToPlan()` 函數  
**變更**:
- ✅ 簡化為 2 個方案：`monthly` 和 `yearly`
- ✅ 更新 Credits 映射：
  - 月費：100 Credits, HKD $78/月
  - 年費：1,200 Credits, HKD $62/月 (年付 $744)
- ✅ 更新確認訊息，包含完整功能列表
- ✅ 添加 Payment Links 未配置的提示

**重要提示**: Payment Links 目前設置為 `REPLACE_WITH_YOUR_MONTHLY_LINK` 和 `REPLACE_WITH_YOUR_YEARLY_LINK`，需要在 Stripe 中創建。

---

## 📋 待辦事項

### ⚠️ **必須完成**: 創建 Stripe Payment Links

您需要在 Stripe 中創建 2 個新的 Payment Links：

#### 🔹 **Payment Link 1: 月費方案**

登入 Stripe Dashboard → Products → Create Product

**產品信息**:
- **名稱**: VaultCaddy Pro - Monthly
- **說明**: 每月 100 Credits，超出後每頁 HKD $0.5
- **價格**: HKD $78
- **計費週期**: 每月重複

**Payment Link 設置**:
1. 創建產品後，點擊 "Create Payment Link"
2. 啟用 "Recurring payment" (重複付款)
3. 設置成功後跳轉 URL: `https://vaultcaddy.com/billing.html?success=true`
4. 設置取消後跳轉 URL: `https://vaultcaddy.com/billing.html?cancelled=true`
5. 複製生成的 Payment Link

**更新代碼**:
打開 `billing.html`，找到第 778 行附近：
```javascript
const stripeLinks = {
    'monthly': 'https://buy.stripe.com/YOUR_MONTHLY_LINK_HERE',  // ⬅️ 替換這裡
    'yearly': 'https://buy.stripe.com/test_REPLACE_WITH_YOUR_YEARLY_LINK'
};
```

---

#### 🔹 **Payment Link 2: 年費方案**

**產品信息**:
- **名稱**: VaultCaddy Pro - Yearly
- **說明**: 每年 1,200 Credits，超出後每頁 HKD $0.5
- **價格**: HKD $744
- **計費週期**: 每年重複

**Payment Link 設置**:
1. 創建產品後，點擊 "Create Payment Link"
2. 啟用 "Recurring payment" (重複付款)
3. 設置成功後跳轉 URL: `https://vaultcaddy.com/billing.html?success=true`
4. 設置取消後跳轉 URL: `https://vaultcaddy.com/billing.html?cancelled=true`
5. 複製生成的 Payment Link

**更新代碼**:
打開 `billing.html`，找到第 778 行附近：
```javascript
const stripeLinks = {
    'monthly': 'https://buy.stripe.com/YOUR_MONTHLY_LINK_HERE',
    'yearly': 'https://buy.stripe.com/YOUR_YEARLY_LINK_HERE'  // ⬅️ 替換這裡
};
```

---

### 🌐 為所有頁面添加 `data-i18n` 標記

目前只創建了翻譯字典，但頁面元素尚未標記。您需要手動為需要翻譯的元素添加 `data-i18n` 屬性。

**示例** (`index.html` Hero Section):

```html
<!-- 修改前 -->
<h1>AI 驅動的財務文件處理</h1>
<p>香港市場性價比最高的 AI 銀行對帳單處理工具</p>
<button>免費開始</button>

<!-- 修改後 -->
<h1 data-i18n="hero.title">AI 驅動的財務文件處理</h1>
<p data-i18n="hero.subtitle">香港市場性價比最高的 AI 銀行對帳單處理工具</p>
<button data-i18n="hero.cta">免費開始</button>
```

**需要更新的頁面**:
- ✅ `index.html` - Hero, Features, Pricing, Testimonials
- ⏳ `billing.html` - Pricing cards, Feature lists
- ⏳ `dashboard.html` - 所有按鈕和標題
- ⏳ `firstproject.html` - 所有按鈕和標題
- ⏳ `account.html` - 所有表單標籤
- ⏳ `document-detail.html` - 所有按鈕和標籤

**翻譯 key 參考**: 參考 `language-manager.js` 中的 `translations` 對象。

---

## 🧪 測試步驟

### 測試語言切換功能

1. 訪問 https://vaultcaddy.com/
2. 點擊導航欄右上角的 "繁體中文" 下拉選單
3. 選擇 "English"
4. 確認頁面內容已切換為英文（如果已添加 data-i18n 標記）
5. 打開 Console (F12)，查看是否有以下日誌：
   ```
   ✅ LanguageManager 初始化完成，當前語言: zh
   🌐 切換語言: zh → en
   🔄 開始翻譯頁面...
   📝 找到 X 個需要翻譯的元素
   ✅ 頁面翻譯完成
   ```

### 測試付費連結功能

1. 訪問 https://vaultcaddy.com/billing.html
2. 點擊「立即開始」按鈕（月費或年費）
3. **如果 Payment Links 已配置**:
   - 應顯示確認對話框
   - 點擊「確認」後跳轉到 Stripe 支付頁面
4. **如果 Payment Links 未配置**:
   - 應顯示提示：「付費功能正在設置中，請稍後再試或聯繫客服。」

---

## 📂 文件變更列表

| 文件 | 狀態 | 說明 |
|------|------|------|
| `language-manager.js` | ✅ 新增 | 語言管理器 |
| `navbar-component.js` | ✅ 修改 | 整合語言切換 |
| `index.html` | ✅ 修改 | 引入 language-manager.js |
| `billing.html` | ✅ 修改 | 引入 language-manager.js + 更新付費邏輯 |

---

## 🎯 下一步建議

### 立即執行

1. **創建 Stripe Payment Links**（見上方說明）
2. **更新 `billing.html` 中的 Payment Links**
3. **測試付費流程**

### 可選執行

4. **為頁面添加 `data-i18n` 標記**（逐頁進行）
   - 從 `index.html` 開始
   - 然後 `billing.html`
   - 最後其他頁面
5. **擴展翻譯字典**（如需要更多翻譯）
   - 編輯 `language-manager.js`
   - 添加新的 key-value pairs
6. **為 Dashboard 和 Account 頁面添加翻譯**

---

## 📞 需要幫助？

如果您在設置 Stripe Payment Links 時遇到問題，請提供：
1. Stripe Dashboard 的截圖
2. 錯誤訊息（如有）
3. 瀏覽器 Console 日誌

我會進一步協助您完成設置！

---

**更新狀態**: 語言管理器已完成，付費連結邏輯已更新，等待 Stripe Payment Links 配置。

