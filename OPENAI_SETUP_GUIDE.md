# 🚀 OpenAI GPT-4 Vision 完整設置指南

## 📊 **成本分析**

### **OpenAI 官方定價**
- **GPT-4 Vision**: $0.01 USD / 1,000 tokens (約 $0.078 HKD)
- 一張發票圖片 ≈ 1,500-2,000 tokens
- **每張發票成本**: 約 $0.015-0.02 USD (約 $0.12-0.16 HKD)

### **與你的定價對比**

**Basic Plan ($15/月, 200 頁)**:
- 你的成本: 200 × $0.02 = **$4 USD/月**
- 你的利潤: $15 - $4 = **$11 USD/月**
- **利潤率: 73%** ✅

**Pro Plan ($31/月, 500 頁)**:
- 你的成本: 500 × $0.02 = **$10 USD/月**
- 你的利潤: $31 - $10 = **$21 USD/月**
- **利潤率: 68%** ✅

### **結論**
✅ **定價非常合理！** 你的利潤率在 68-73% 之間，這是非常健康的 SaaS 利潤率。

---

## 💰 **收入計算**

### **100 個付費用戶的收入**

假設用戶分佈：
- 60% 選擇 Basic ($15/月)
- 40% 選擇 Pro ($31/月)

**月收入**:
- Basic: 60 × $15 = $900 USD
- Pro: 40 × $31 = $1,240 USD
- **總計: $2,140 USD/月 ≈ $16,692 HKD/月**

**年收入**:
- **$25,680 USD ≈ $200,304 HKD**

**扣除成本後**:
- AI 成本: 約 $600 USD/月
- 服務器成本: 約 $50 USD/月
- **淨收入: $1,490 USD/月 ≈ $11,622 HKD/月**

### **養活你需要多少用戶？**

**你的月薪**: $25,000 HKD

**計算**:
- 每個用戶平均收入: $16,692 / 100 = $167 HKD/月
- 扣除成本後: 約 $116 HKD/月/用戶

**需要用戶數**:
- $25,000 / $116 = **約 216 個付費用戶**

**更保守的估計（包含其他成本）**:
- **約 250-300 個付費用戶** 可以養活你

---

## 💼 **香港會計師使用的軟件**

### **主流軟件（按使用率排序）**

1. **QuickBooks** ⭐⭐⭐⭐⭐ (40-50%)
   - 中小企業最愛
   - 價格: $30-200 USD/月

2. **Xero** ⭐⭐⭐⭐ (25-30%)
   - 雲端會計軟件
   - 價格: $20-70 USD/月

3. **MYOB** ⭐⭐⭐ (15-20%)
   - 傳統軟件
   - 價格: $25-100 USD/月

4. **Sage** ⭐⭐ (5-10%)
   - 大型企業
   - 價格: $50-300 USD/月

5. **Excel** ⭐⭐⭐⭐⭐ (幾乎所有人)
   - 作為輔助工具

### **你們的機會**
✅ **與 QuickBooks/Xero 整合**是關鍵！
✅ **CSV 導出**是必須功能！

---

## 📝 **OpenAI 帳戶註冊與 API Key 獲取指南**

### **Step 1: 註冊 OpenAI 帳戶**

1. **訪問 OpenAI 註冊頁面**：https://platform.openai.com/signup
2. **選擇註冊方式**：
   - 使用 Google 帳戶（推薦，最快）
   - 使用 Microsoft 帳戶
   - 使用電子郵件註冊

3. **完成驗證**：
   - 驗證電子郵件地址
   - 驗證手機號碼（需要香港手機號碼）

### **Step 2: 設置付款方式**

1. **訪問 Billing 頁面**：https://platform.openai.com/account/billing/overview
2. **添加付款方式**：
   - 點擊 "Add payment method"
   - 輸入信用卡信息（支持 Visa、Mastercard、American Express）
   - **建議設置使用限額**：例如 $50 USD/月，避免超支

3. **選擇付款計劃**：
   - **Pay as you go**（按使用量付費，推薦）
   - 無需月費，只按實際使用量計費

### **Step 3: 創建 API Key**

1. **訪問 API Keys 頁面**：https://platform.openai.com/api-keys
2. **創建新的 API Key**：
   - 點擊 "Create new secret key"
   - 輸入 Key 名稱（例如：`VaultCaddy-Production`）
   - **重要**：立即複製並保存 API Key，因為它只會顯示一次！

3. **保存 API Key**：
   ```
   sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### **Step 4: 設置使用限額（重要！）**

1. **訪問 Usage limits 頁面**：https://platform.openai.com/account/limits
2. **設置月度限額**：
   - Hard limit: $50 USD（硬限制，達到後 API 會停止工作）
   - Email alerts: $40 USD（達到後發送警告郵件）

---

## 🔧 **整合 OpenAI GPT-4 Vision 到 VaultCaddy**

### **Step 1: 填入 API Key**

打開 `firstproject.html` 文件，找到以下代碼：

```javascript
// ⚠️ 請在這裡填入你的 OpenAI API Key
const openaiApiKey = 'YOUR_OPENAI_API_KEY_HERE'; // ⚠️ 請替換為你的 API Key
```

將 `YOUR_OPENAI_API_KEY_HERE` 替換為你的 OpenAI API Key：

```javascript
// ✅ 已填入 API Key
const openaiApiKey = 'sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
```

### **Step 2: 測試 OpenAI Vision**

1. **訪問** `https://vaultcaddy.com/firstproject.html`
2. **打開瀏覽器控制台**（按 F12）
3. **查看日誌**，應該看到：
   ```
   ✅ OpenAI Vision Client 已初始化
   Model: gpt-4-vision-preview
   ```

4. **上傳一張發票**
5. **查看控制台日誌**，應該看到：
   ```
   🔄 OpenAI Vision 開始處理文檔...
   ✅ 圖片已轉換為 Base64
   📤 發送請求到 OpenAI API
   📥 收到 OpenAI 響應
   ✅ 數據提取成功
   ✅ 處理器 openaiVision 成功處理文檔
   ```

---

## 🎯 **下一步建議**

### **1. 立即完成（今天）**
- ✅ 註冊 OpenAI 帳戶
- ✅ 創建 API Key
- ✅ 填入 API Key 到 `firstproject.html`
- ✅ 測試上傳發票，確保 OpenAI Vision 正常工作

### **2. 短期優化（本週）**
- 優化 OpenAI Vision 的提示詞，提高提取準確度
- 實現 CSV 導出功能（QuickBooks/Xero 整合）
- 添加手動修正功能，讓用戶可以修改提取的數據

### **3. 中期目標（本月）**
- 實現 Bank Statement 提取功能
- 實現 Receipt 提取功能
- 優化 UI/UX，讓用戶體驗更好

### **4. 長期目標（下個月）**
- 實現 QuickBooks/Xero 直接整合（IIF/QBO 格式）
- 實現批量處理功能
- 實現 Smart Reconciliation 功能

---

## 🤔 **常見問題**

### **Q1: OpenAI API Key 安全嗎？**
**A**: 目前 API Key 是直接寫在前端代碼中的，這**不安全**。建議：
1. 短期：設置 OpenAI API Key 的使用限額（$50 USD/月）
2. 長期：將 API Key 移到後端（例如 Cloudflare Workers），前端只調用後端 API

### **Q2: 如果 OpenAI API 失敗怎麼辦？**
**A**: 系統已經實現了備用機制：
1. 優先使用 OpenAI GPT-4 Vision（準確度最高）
2. 如果失敗，自動切換到 Gemini AI（備用1）
3. 如果還失敗，自動切換到 Vision AI（備用2）

### **Q3: 如何監控 OpenAI API 使用量？**
**A**: 訪問 https://platform.openai.com/usage 查看實時使用量和成本。

### **Q4: 如何降低成本？**
**A**: 
1. 使用更小的圖片（降低 token 數量）
2. 優化提示詞（減少輸出 token）
3. 實現緩存機制（避免重複處理相同文檔）

---

## 📞 **需要幫助？**

如果你在設置過程中遇到任何問題，請：
1. 檢查瀏覽器控制台（F12）的錯誤日誌
2. 確認 OpenAI API Key 是否正確
3. 確認 OpenAI 帳戶是否有足夠的餘額
4. 確認網絡連接是否正常

---

## ✅ **完成檢查清單**

- [ ] 註冊 OpenAI 帳戶
- [ ] 驗證電子郵件和手機號碼
- [ ] 添加付款方式
- [ ] 創建 API Key
- [ ] 設置使用限額
- [ ] 填入 API Key 到 `firstproject.html`
- [ ] 測試上傳發票
- [ ] 確認 OpenAI Vision 正常工作
- [ ] 檢查提取的數據是否準確

---

**祝你成功！** 🎉

