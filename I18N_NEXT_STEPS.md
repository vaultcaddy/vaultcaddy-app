# 🌐 語言切換 - 下一步工作指南

**更新時間**: 2025-11-21 下午 4:30

---

## ✅ 今天已完成

### 1️⃣ Export 功能統一 ✅
- ✅ 統一 `document-detail.html` Export 菜單
- ✅ 添加所有導出格式支持
- ✅ 引用 `bank-statement-export.js` 和 `invoice-export.js`

### 2️⃣ UI 優化 ✅
- ✅ 首頁演示動畫內容更新
- ✅ billing.html pricing.description 恢復
- ✅ account.html 購買記錄滾動 + 限制10個
- ✅ Export 按鈕數字樣式

---

## ⚪ 語言切換剩餘工作（40 分鐘）

### 方法 1: 快速批量更新（推薦）

使用查找替換批量添加 `data-i18n` 標記：

#### 步驟 1: 更新 language-manager.js（10 分鐘）

添加以下翻譯 keys：

```javascript
// Demo 演示動畫
'demo.hk_restaurant': {
    'zh': '香港茶餐廳',
    'en': 'Hong Kong Tea Restaurant'
},
'demo.invoice_number': {
    'zh': 'INV-2025-001',
    'en': 'INV-2025-001'
},
'demo.egg_tart': {
    'zh': '蛋撻',
    'en': 'Egg Tart'
},
'demo.milk_tea': {
    'zh': '鴛鴦奶茶',
    'en': 'Yuenyeung Milk Tea'
},
'demo.pineapple_bun': {
    'zh': '菠蘿包',
    'en': 'Pineapple Bun'
},
'demo.subtotal': {
    'zh': '小計:',
    'en': 'Subtotal:'
},
'demo.tax': {
    'zh': '稅額:',
    'en': 'Tax:'
},
'demo.boc_hk': {
    'zh': '中國銀行（香港）',
    'en': 'Bank of China (Hong Kong)'
},
'demo.customer_payment': {
    'zh': '客戶收款',
    'en': 'Customer Payment'
},
'demo.staff_salary': {
    'zh': '員工薪酬',
    'en': 'Staff Salary'
},
'demo.office_supplies': {
    'zh': '辦公用品',
    'en': 'Office Supplies'
},
'demo.bank_fee': {
    'zh': '銀行手續費',
    'en': 'Bank Fee'
},
'demo.month_balance': {
    'zh': '月結餘額:',
    'en': 'Month Balance:'
},

// Pricing 卡片
'pricing.monthly': {
    'zh': '月費',
    'en': 'Monthly'
},
'pricing.yearly': {
    'zh': '年費',
    'en': 'Yearly'
},
'pricing.suitable_for': {
    'zh': '適合會計師、企業和個人用戶',
    'en': 'For accountants, businesses and individuals'
},
'pricing.includes': {
    'zh': '頁面包含',
    'en': 'Includes'
},
'pricing.monthly_credits': {
    'zh': '每月 100 Credits',
    'en': '100 Credits per month'
},
'pricing.yearly_credits': {
    'zh': '每年 1,200 Credits',
    'en': '1,200 Credits per year'
},
'pricing.overage': {
    'zh': '超出後每頁 HKD $0.5',
    'en': 'HKD $0.5 per page after'
},
'pricing.batch_processing': {
    'zh': '批次處理無限制文件',
    'en': 'Unlimited batch processing'
},
'pricing.one_click_convert': {
    'zh': '一鍵轉換所有文件',
    'en': 'One-click conversion'
},
'pricing.excel_csv': {
    'zh': 'Excel/CSV 匯出',
    'en': 'Excel/CSV Export'
},
'pricing.quickbooks': {
    'zh': 'QuickBooks 整合',
    'en': 'QuickBooks Integration'
},
'pricing.ai_processing': {
    'zh': '複合式 AI 處理',
    'en': 'Hybrid AI Processing'
},
'pricing.8_languages': {
    'zh': '8 種語言支援',
    'en': '8 Languages Support'
},
'pricing.email_support': {
    'zh': '電子郵件支援',
    'en': 'Email Support'
},
'pricing.secure_upload': {
    'zh': '安全文件上傳',
    'en': 'Secure File Upload'
},
'pricing.365_retention': {
    'zh': '365 天數據保留',
    'en': '365-day Data Retention'
},
'pricing.30_retention': {
    'zh': '30 天圖片保留',
    'en': '30-day Image Retention'
},
'pricing.start_now': {
    'zh': '立即開始',
    'en': 'Get Started'
},
'pricing.save_20': {
    'zh': '節省 20%',
    'en': 'Save 20%'
},
```

#### 步驟 2: 更新 index.html（15 分鐘）

批量添加 `data-i18n` 到以下區塊：

1. **演示動畫**（Lines 348-432）
2. **Pricing 卡片**（Lines 625-710）
3. **Benefits 區塊**（Lines 470-580）

#### 步驟 3: 測試（5 分鐘）

```bash
# 訪問 https://vaultcaddy.com/
# 點擊「繁體中文」切換為「English」
# 確認所有區塊翻譯正確
```

---

### 方法 2: AI 輔助批量更新（更快）

使用 Cursor 的 AI 功能批量添加：

```
Prompt:
為 index.html 中以下區塊的所有中文文字添加 data-i18n 標記：
1. Lines 348-432（演示動畫）
2. Lines 625-710（Pricing 卡片）
3. Lines 470-580（Benefits 區塊）

要求：
- 使用 language-manager.js 中已存在的 keys
- 如果 key 不存在，添加到 language-manager.js
- 保持原有 HTML 結構不變
```

---

## 📋 快速 Checklist

### index.html 剩餘區塊

- [ ] 演示動畫（Lines 348-432）
  - [ ] 香港茶餐廳
  - [ ] 蛋撻、鴛鴦奶茶、菠蘿包
  - [ ] 中國銀行（香港）
  - [ ] 客戶收款、員工薪酬等

- [ ] Pricing 卡片（Lines 625-710）
  - [ ] 月費、年費標題
  - [ ] 適合會計師、企業和個人用戶
  - [ ] 頁面包含
  - [ ] 所有功能列表（12個）
  - [ ] 立即開始按鈕

- [ ] Benefits 區塊（Lines 470-580）
  - [ ] 標題和描述
  - [ ] 5個 benefit 卡片

---

## 🎯 預期成果

### 完成後效果

#### 中文版（默認）
```
演示動畫：
- 香港茶餐廳 ｜ INV-2025-001
- 蛋撻 x5 @ $12 = $60
- 中國銀行（香港） ｜ 2025-03

Pricing：
- 月費 / 年費
- 適合會計師、企業和個人用戶
- HKD $78 /月
- 包含 100 Credits
```

#### 英文版（切換後）
```
Demo Animation:
- Hong Kong Tea Restaurant ｜ INV-2025-001
- Egg Tart x5 @ $12 = $60
- Bank of China (Hong Kong) ｜ 2025-03

Pricing:
- Monthly / Yearly
- For accountants, businesses and individuals
- HKD $78 /month
- 100 Credits included
```

---

## 🔧 實用命令

### 查找未添加 data-i18n 的中文文字

```bash
# 查找包含中文但沒有 data-i18n 的行
grep -n "[\u4e00-\u9fa5]" index.html | grep -v "data-i18n"
```

### 統計 data-i18n 使用情況

```bash
# 統計已添加 data-i18n 的元素數量
grep -o "data-i18n" index.html | wc -l
```

### 檢查翻譯 key 是否存在

```bash
# 檢查某個 key 是否在 language-manager.js 中
grep "demo.hk_restaurant" language-manager.js
```

---

## 📝 注意事項

### 1️⃣ 保持 HTML 結構不變
- 只添加 `data-i18n` 屬性
- 不修改原有的 inline styles
- 不改變元素層級

### 2️⃣ 使用一致的 key 命名
- `demo.*` - 演示動畫
- `pricing.*` - 定價相關
- `feature.*` - 功能相關
- `benefit.*` - 優勢相關

### 3️⃣ 測試切換效果
- 切換語言後立即生效
- 無需刷新頁面
- 語言偏好保存在 localStorage

---

## 💡 常見問題

### Q: 如果某些文字不需要翻譯？

**A**: 跳過即可，例如：
- 價格數字（$78, $62）
- 圖標（✅, ❌）
- 品牌名稱（VaultCaddy）

### Q: 翻譯 key 太多，如何組織？

**A**: 使用命名空間：
```javascript
'demo.invoice.restaurant': '香港茶餐廳'
'demo.bank.name': '中國銀行（香港）'
```

### Q: 如何批量測試所有翻譯？

**A**: 使用瀏覽器開發者工具：
```javascript
// 切換為英文並檢查
window.languageManager.setLanguage('en');
document.querySelectorAll('[data-i18n]').forEach(el => {
    if (el.textContent.match(/[\u4e00-\u9fa5]/)) {
        console.warn('未翻譯:', el.getAttribute('data-i18n'), el.textContent);
    }
});
```

---

## 🎯 下次會話開始時

### 1️⃣ 檢查當前進度

```bash
cd /Users/cavlinyeung/ai-bank-parser
git log --oneline -5
```

### 2️⃣ 繼續剩餘工作

- [ ] 完成 index.html（40 分鐘）
- [ ] 更新 dashboard.html（20 分鐘）
- [ ] 更新 account.html（15 分鐘）
- [ ] 更新 billing.html（15 分鐘）

### 3️⃣ 測試和部署

- [ ] 測試所有頁面語言切換
- [ ] 檢查翻譯質量
- [ ] 提交最終代碼
- [ ] 部署到生產環境

---

**總結**: 今天完成了 Export 功能統一和 UI 優化，語言切換的基礎架構已完成，剩餘工作是批量添加 `data-i18n` 標記，預計 40 分鐘完成。🎉

**建議**: 使用 Cursor 的 AI 功能批量添加 `data-i18n`，可以將 40 分鐘縮短到 15 分鐘。✨

