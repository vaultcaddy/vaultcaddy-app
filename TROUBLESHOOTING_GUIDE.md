# 文檔處理失敗排查指南

## 問題：銀行對帳單處理失敗

### 可能的原因

#### 1. **API 密鑰問題**
- DeepSeek API 密鑰無效或過期
- API 配額已用完
- API 請求被限流

**檢查方法：**
```javascript
// 在瀏覽器控制台中檢查
console.log('API Key:', window.DEEPSEEK_API_KEY);
```

**解決方案：**
- 檢查 `config.js` 中的 API 密鑰
- 前往 DeepSeek 控制台檢查配額
- 等待限流解除（通常 1 分鐘）

---

#### 2. **文件格式問題**
- PDF 文件損壞
- 文件過大（超過 10MB）
- 文件包含受保護的內容

**檢查方法：**
```javascript
// 檢查文件信息
console.log('File size:', file.size / 1024 / 1024, 'MB');
console.log('File type:', file.type);
```

**解決方案：**
- 確保 PDF 文件完整且未損壞
- 壓縮大文件或分割成多個文件
- 移除 PDF 保護

---

#### 3. **網絡連接問題**
- 網絡不穩定
- 請求超時
- CORS 錯誤

**檢查方法：**
- 打開瀏覽器開發者工具（F12）
- 查看 Network 標籤
- 查看是否有失敗的請求

**解決方案：**
- 檢查網絡連接
- 重試上傳
- 清除瀏覽器緩存

---

#### 4. **AI 處理器未載入**
- `hybrid-vision-deepseek.js` 未正確載入
- 處理器初始化失敗

**檢查方法：**
```javascript
// 在瀏覽器控制台中檢查
console.log('Processor loaded:', !!window.HybridVisionDeepSeekProcessor);
```

**解決方案：**
- 刷新頁面
- 清除瀏覽器緩存
- 檢查控制台錯誤信息

---

## 調試步驟

### 步驟 1：打開瀏覽器開發者工具
1. 按 `F12` 或右鍵點擊頁面 → 「檢查」
2. 切換到「Console」標籤

### 步驟 2：查看錯誤信息
上傳文件後，查看控制台中的錯誤信息：

```
✅ 正常流程：
🤖 開始 AI 處理: filename.pdf (3 頁)
✅ 文檔狀態已更新

❌ 失敗流程：
🤖 開始 AI 處理: filename.pdf (3 頁)
❌ AI 處理失敗: [錯誤信息]
✅ 已退回 3 Credits
```

### 步驟 3：檢查 Network 請求
1. 切換到「Network」標籤
2. 上傳文件
3. 查找失敗的請求（紅色）
4. 點擊查看詳細錯誤信息

### 步驟 4：檢查 Firestore 數據
1. 前往 [Firebase Console](https://console.firebase.google.com/)
2. 選擇您的項目
3. 點擊「Firestore Database」
4. 查看文檔的 `status` 和 `error` 欄位

---

## Credits 退款驗證

### 檢查 Credits 是否正確退回

#### 方法 1：查看 UI 顯示
- 處理失敗後，右上角的 Credits 應該立即增加
- 例如：79997 → 80000（退回 3 Credits）

#### 方法 2：查看 Firestore
1. 前往 Firebase Console → Firestore Database
2. 找到 `users/{userId}` 文檔
3. 檢查 `currentCredits` 欄位的值
4. 查看 `creditsHistory` 子集合
5. 應該看到一條 `type: 'refund'` 的記錄

#### 方法 3：查看控制台日誌
```
✅ Credits 已退回: 3 頁，新餘額: 80000
```

---

## 常見錯誤和解決方案

### 錯誤 1：「AI 處理器未載入」
**原因：** `hybrid-vision-deepseek.js` 未正確載入

**解決方案：**
1. 刷新頁面
2. 檢查文件路徑是否正確
3. 查看控制台是否有 404 錯誤

### 錯誤 2：「API 請求失敗」
**原因：** DeepSeek API 密鑰無效或配額用完

**解決方案：**
1. 檢查 `config.js` 中的 API 密鑰
2. 前往 DeepSeek 控制台檢查配額
3. 更新 API 密鑰

### 錯誤 3：「Credits 不足」
**原因：** 用戶 Credits 餘額不足

**解決方案：**
1. 前往 `billing.html` 購買 Credits
2. 或使用管理員權限添加 Credits

### 錯誤 4：「文件上傳失敗」
**原因：** Firebase Storage 配置問題或文件過大

**解決方案：**
1. 檢查 Firebase Storage 規則
2. 確認文件大小不超過限制
3. 檢查網絡連接

---

## 手動退回 Credits

如果自動退款失敗，可以手動退回 Credits：

### 方法 1：使用 Firebase Console
1. 前往 Firestore Database
2. 找到 `users/{userId}` 文檔
3. 編輯 `currentCredits` 欄位
4. 增加相應的 Credits 數量

### 方法 2：使用腳本
```javascript
// 在瀏覽器控制台中執行
const userId = 'USER_ID';
const refundAmount = 3;

firebase.firestore().collection('users').doc(userId).update({
    currentCredits: firebase.firestore.FieldValue.increment(refundAmount),
    credits: firebase.firestore.FieldValue.increment(refundAmount)
}).then(() => {
    console.log('✅ Credits 已手動退回');
}).catch(error => {
    console.error('❌ 退回失敗:', error);
});
```

---

## 預防措施

### 1. 定期檢查 API 配額
- 監控 DeepSeek API 使用量
- 設置配額警告
- 準備備用 API 密鑰

### 2. 文件驗證
- 上傳前檢查文件大小
- 驗證文件格式
- 提供文件預覽

### 3. 錯誤監控
- 記錄所有處理失敗的文檔
- 定期檢查錯誤日誌
- 分析失敗原因

### 4. 用戶通知
- 處理失敗時顯示清晰的錯誤信息
- 提供重試選項
- 確認 Credits 已退回

---

## 聯繫支援

如果問題仍未解決：

1. **收集信息：**
   - 瀏覽器控制台截圖
   - 錯誤信息
   - 文件類型和大小
   - 用戶 ID

2. **檢查文檔：**
   - `EMAIL_VERIFICATION_SETUP.md`
   - `CREDITS_UPDATE_GUIDE.md`
   - `IMPLEMENTATION_SUMMARY.md`

3. **測試環境：**
   - 使用不同的瀏覽器
   - 嘗試不同的文件
   - 檢查網絡連接

---

**記住：所有 Credits 操作都會記錄到 `creditsHistory`，可以隨時查看和審計。** ✅
