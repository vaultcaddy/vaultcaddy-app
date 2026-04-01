# Google Ads 轉換追蹤設定指南

**日期**: 2026-02-13  
**狀態**: ✅ 代碼已添加，等待 Google Ads 配置

---

## 📊 當前狀況

### 已完成的步驟
- ✅ 已創建轉換追蹤腳本 (`google-ads-conversion-tracking.js`)
- ✅ 已在 `dashboard.html` 添加轉換追蹤
- ✅ 已在 `firstproject.html` 添加轉換追蹤
- ✅ 已配置 Google Analytics (G-LWPEKNC7RQ)

### 待完成的步驟
- ⏳ 在 Google Ads 中設定轉換動作
- ⏳ 驗證轉換追蹤是否正常工作

---

## 🎯 轉換事件說明

### 觸發條件
當用戶訪問以下頁面時，會自動觸發轉換事件：

1. **Dashboard 頁面**
   - URL: `https://vaultcaddy.com/dashboard.html`
   - 事件標籤: `dashboard_visit`
   - 觸發條件: 用戶已登入並訪問儀表板

2. **First Project 頁面**
   - URL: `https://vaultcaddy.com/firstproject.html?project=xxx`
   - 事件標籤: `firstproject_visit`
   - 觸發條件: 用戶已登入並訪問項目頁面

### 發送的事件
轉換追蹤腳本會發送以下事件：

1. **`manual_event_PURCHASE`** (主要轉換事件)
   - 用於 Google Ads 轉換追蹤
   - 事件類別: `conversion`
   - 值: 1
   - 貨幣: HKD

2. **`page_view_conversion`** (GA4 事件)
   - 用於 Google Analytics 分析
   - 事件類別: `conversion`

3. **`sign_up`** (僅 dashboard_visit 時)
   - 標準 GA4 事件
   - 用於分析用戶註冊行為

---

## 🔧 Google Ads 設定步驟

### 步驟 1: 創建轉換動作

1. **登入 Google Ads**
   - 訪問: https://ads.google.com
   - 選擇帳戶: `675-939-0205 Vaultcaddy AI`

2. **進入轉換設定**
   - 點擊左側選單「工具和設定」→「轉換」
   - 或直接訪問: `https://ads.google.com/aw/conversions`

3. **新增轉換動作**
   - 點擊「+」按鈕
   - 選擇「網站」

4. **設定轉換動作**
   ```
   轉換類別: 其他
   轉換名稱: Dashboard 訪問
   價值: 不設定價值（或設定為 1）
   計算方式: 每次
   歸因模式: 資料驅動歸因（推薦）
   ```

5. **選擇追蹤方式**
   - 選擇「使用 Google Analytics (GA4) 事件」
   - 事件名稱: `manual_event_PURCHASE`
   - 事件參數: 
     - `event_label` = `dashboard_visit` 或 `firstproject_visit`

### 步驟 2: 設定轉換動作（方法 2 - 使用自訂事件）

如果方法 1 不適用，可以使用自訂事件：

1. **創建轉換動作**
   ```
   轉換類別: 其他
   轉換名稱: 用戶訪問儀表板
   價值: 不設定價值
   計算方式: 每次
   ```

2. **選擇追蹤方式**
   - 選擇「使用 Google Analytics (GA4) 事件」
   - 事件名稱: `page_view_conversion`
   - 條件: `event_label` 等於 `dashboard_visit` 或 `firstproject_visit`

### 步驟 3: 驗證轉換追蹤

1. **測試轉換事件**
   - 清除瀏覽器緩存
   - 訪問 `https://vaultcaddy.com/dashboard.html`
   - 登入帳戶
   - 打開開發者工具 (F12) → Console
   - 查看是否有以下日誌：
     ```
     📊 開始發送 Google Ads 轉換事件: dashboard_visit
     ✅ 轉換事件已發送到 dataLayer: manual_event_PURCHASE
     ✅ GA4 事件已發送到 dataLayer: page_view_conversion
     ✅ 轉換追蹤完成: dashboard_visit
     ```

2. **在 Google Analytics 中驗證**
   - 訪問 Google Analytics
   - 進入「即時」報告
   - 查看是否有 `manual_event_PURCHASE` 或 `page_view_conversion` 事件

3. **在 Google Ads 中驗證**
   - 等待 24-48 小時
   - 檢查轉換動作是否有數據
   - 或在「診斷」中查看轉換追蹤狀態

---

## 📋 轉換動作設定建議

### 建議創建兩個轉換動作

#### 轉換動作 1: Dashboard 訪問
```
名稱: Dashboard 訪問
事件: manual_event_PURCHASE
條件: event_label = 'dashboard_visit'
價值: 不設定
計算方式: 每次
```

#### 轉換動作 2: First Project 訪問
```
名稱: First Project 訪問
事件: manual_event_PURCHASE
條件: event_label = 'firstproject_visit'
價值: 不設定
計算方式: 每次
```

或者創建一個合併的轉換動作：

#### 轉換動作: 用戶訪問（合併）
```
名稱: 用戶訪問儀表板或項目
事件: manual_event_PURCHASE
條件: event_label 包含 'dashboard_visit' 或 'firstproject_visit'
價值: 不設定
計算方式: 每次
```

---

## 🔍 故障排查

### 問題 1: 轉換事件未觸發

**檢查項目**:
1. 確認用戶已登入
2. 檢查 Console 是否有錯誤
3. 確認 `google-ads-conversion-tracking.js` 已正確加載
4. 檢查 `dataLayer` 是否存在

**解決方法**:
```javascript
// 在 Console 中手動測試
window.dataLayer.push({
    'event': 'manual_event_PURCHASE',
    'event_category': 'conversion',
    'event_label': 'dashboard_visit',
    'value': 1,
    'currency': 'HKD'
});
```

### 問題 2: Google Ads 未記錄轉換

**可能原因**:
1. 轉換動作設定錯誤
2. 事件名稱不匹配
3. 歸因窗口未過期（轉換有 24-48 小時延遲）

**解決方法**:
1. 檢查轉換動作中的事件名稱是否為 `manual_event_PURCHASE`
2. 確認條件設定正確
3. 等待 24-48 小時後再檢查

### 問題 3: 重複觸發轉換

**原因**: 用戶刷新頁面或多次訪問

**解決方法**: 
- 已使用 `sessionStorage` 防止重複觸發（僅對 `dashboard_visit`）
- 如需更嚴格控制，可以改用 `localStorage` 或服務器端追蹤

---

## ✅ 驗證清單

### 代碼部署
- [x] 轉換追蹤腳本已創建
- [x] dashboard.html 已添加腳本引用
- [x] firstproject.html 已添加腳本引用
- [ ] 代碼已部署到生產環境

### Google Ads 設定
- [ ] 已創建轉換動作
- [ ] 事件名稱設定為 `manual_event_PURCHASE`
- [ ] 條件設定正確（event_label）
- [ ] 轉換動作已啟用

### 測試驗證
- [ ] 測試訪問 dashboard.html
- [ ] 檢查 Console 日誌
- [ ] 在 GA4 中驗證事件
- [ ] 等待 24-48 小時後檢查 Google Ads

---

## 📊 預期結果

### 24 小時內
- Google Analytics 應該顯示轉換事件
- 可以在「即時」報告中看到事件

### 48 小時內
- Google Ads 應該開始顯示轉換數據
- 轉換次數應該與實際訪問次數接近

### 1 週內
- 轉換數據應該穩定
- 可以計算真實的 CPA（每次轉換成本）

---

## 🎯 下一步行動

1. **立即執行**
   - [ ] 部署代碼到生產環境
   - [ ] 在 Google Ads 中創建轉換動作
   - [ ] 測試轉換追蹤

2. **24 小時內**
   - [ ] 檢查 Google Analytics 事件
   - [ ] 驗證轉換追蹤是否正常工作

3. **48 小時內**
   - [ ] 檢查 Google Ads 轉換數據
   - [ ] 分析轉換率

---

## 📝 技術細節

### 事件發送順序
1. 檢查頁面是否為目標頁面
2. 等待 Firebase Auth 初始化（最多 5 秒）
3. 檢查用戶是否已登入
4. 發送轉換事件到 `dataLayer`
5. 如果 `gtag` 已加載，也發送到 `gtag`

### 防重複機制
- 使用 `sessionStorage` 標記已追蹤的轉換
- 同一會話中不會重複觸發 `sign_up` 事件

### 兼容性
- 支持 `dataLayer`（即使 gtag 未加載也能工作）
- 支持 `gtag`（如果已加載）
- 支持動態路由變化

---

**最後更新**: 2026-02-13
