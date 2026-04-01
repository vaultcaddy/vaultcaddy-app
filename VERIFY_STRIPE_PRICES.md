# 🔍 Stripe 價格驗證指南

## ✅ 快速驗證步驟

### 1️⃣ 驗證年付產品價格

**訪問**: https://dashboard.stripe.com/products/prod_Tb2443GvCbe4Pp

**應該看到以下 4 個新價格**:

- ✅ **HKD $336/年** - `price_1SuruEJmiQ31C0GTWqMAZeuM`
  - 元數據: `credits: 1200`, `monthly_credits: 100`, `plan_type: starter_yearly`

- ✅ **USD $42.96/年** - `price_1SuruEJmiQ31C0GTBVhLSAtA`
  - 元數據: `credits: 1200`, `monthly_credits: 100`, `plan_type: starter_yearly`

- ✅ **JPY ¥7056/年** - `price_1SuruEJmiQ31C0GTde3o97rx`
  - 元數據: `credits: 1200`, `monthly_credits: 100`, `plan_type: starter_yearly`

- ✅ **KRW ₩62,256/年** - `price_1SuruFJmiQ31C0GTUL0Yxltm`
  - 元數據: `credits: 1200`, `monthly_credits: 100`, `plan_type: starter_yearly`

---

### 2️⃣ 驗證月付產品價格

**訪問**: https://dashboard.stripe.com/products/prod_Tb24SiE4usHRDS

**應該看到以下 4 個新價格**:

- ✅ **HKD $38/月** - `price_1SuruFJmiQ31C0GTdJxUaknj`
  - 元數據: `credits: 100`, `monthly_credits: 100`, `plan_type: starter_monthly`

- ✅ **USD $4.88/月** - `price_1SuruGJmiQ31C0GThdoiTbTM`
  - 元數據: `credits: 100`, `monthly_credits: 100`, `plan_type: starter_monthly`

- ✅ **JPY ¥788/月** - `price_1SuruGJmiQ31C0GTGQVpiEuP`
  - 元數據: `credits: 100`, `monthly_credits: 100`, `plan_type: starter_monthly`

- ✅ **KRW ₩6,988/月** - `price_1SuruGJmiQ31C0GTpBz3jbMo`
  - 元數據: `credits: 100`, `monthly_credits: 100`, `plan_type: starter_monthly`

---

## 📋 驗證檢查清單

### Stripe Dashboard 檢查:
- [ ] 所有 8 個價格都已創建
- [ ] 每個價格的金額正確
- [ ] 每個價格的元數據（metadata）正確
- [ ] 計費週期正確（年付/月付）
- [ ] 幣種正確

### 代碼檢查:
- [x] `stripe-manager.js` 已更新所有 Price ID
- [x] 多幣種支持已實現
- [x] 語言自動檢測已實現
- [ ] 前端頁面測試（`billing.html`）

---

## 🧪 測試支付流程（可選）

### 使用 Stripe 測試卡:

**測試卡號**: `4242 4242 4242 4242`  
**到期日**: 任何未來日期 (如 `12/28`)  
**CVC**: 任何 3 位數字 (如 `123`)  
**郵編**: 任何 5 位數字 (如 `12345`)

### 測試步驟:

1. 在網站上選擇訂閱計劃（月付或年付）
2. 選擇幣種（根據語言版本）
3. 點擊「訂閱」按鈕
4. 在 Stripe Checkout 頁面輸入測試卡信息
5. 完成支付
6. 驗證用戶 Credits 是否正確增加
7. 驗證訂閱狀態是否正確更新

---

## ⚠️ 常見問題

### Q: 價格創建後多久生效？
**A**: 立即生效，可以馬上使用。

### Q: 如何停用舊價格？
**A**: 在 Stripe Dashboard 中找到舊價格，點擊「Archive」即可。

### Q: 元數據 (metadata) 有什麼用？
**A**: 用於在 Webhook 中識別訂閱類型和 Credits 數量，自動更新用戶帳戶。

### Q: 可以修改已創建的價格嗎？
**A**: 不可以。Stripe 價格一旦創建就不可修改，只能創建新價格。

---

## 📞 如有問題

請訪問 Stripe Dashboard 查看詳細信息：
- 產品頁面: https://dashboard.stripe.com/products
- 價格頁面: https://dashboard.stripe.com/prices
- API 日誌: https://dashboard.stripe.com/logs

---

**最後更新**: 2026-01-29  
**狀態**: ✅ 所有價格已創建並配置完成

