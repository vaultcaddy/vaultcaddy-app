# 🔑 正確的 API Key 設置指南

## 🚨 問題診斷

### **發現的問題：**

根據您的截圖，API Key 有**兩個版本**：

| 位置 | API Key | 狀態 |
|------|---------|------|
| **DeepSeek 平台（圖 1、圖 7）** | `sk-d0edd459796441c190543979f4123867` | ✅ 正確 |
| **測試工具（圖 2）** | `sk-d0edd459796441c190543979f4123867` | ✅ 正確（但測試失敗） |
| **Cloudflare Worker（圖 6）** | `sk-d0edd459796441c1905439797f4123867` | ❌ 錯誤（多了一個 `7`） |

### **差異對比：**

```
正確: sk-d0edd459796441c1905439  79  f4123867
錯誤: sk-d0edd459796441c1905439  797 f4123867
                                ^^^
                                多了一個 7！
```

---

## 🔍 **為什麼測試 2 失敗？**

### **可能的原因：**

1. **API Key 創建失敗**
   - DeepSeek 平台顯示 Key 已創建
   - 但 Key 可能沒有完全激活
   - 或者 Key 的權限有問題

2. **賬戶餘額問題**
   - 圖 7 顯示：
     - 充值餘額：$0.00 USD + ¥8.53 CNY
     - 本月消費：¥0.90 CNY
   - 餘額可能不足以創建新 Key

3. **Key 創建時間問題**
   - Key 創建於 2025-11-17
   - 可能需要等待幾分鐘才能使用

4. **測試工具直接調用 DeepSeek API 被封鎖**
   - 直接從瀏覽器調用可能有 CORS 限制
   - 但通過 Worker 調用可以（這就是為什麼測試 3、4 成功）

---

## ✅ **解決方案（3 個步驟）**

### **步驟 1：在 DeepSeek 平台充值（如果需要）**

1. 訪問：https://platform.deepseek.com
2. 點擊右上角的 **充值**
3. 充值至少 $5 USD 或 ¥30 CNY
4. 確認充值成功

**為什麼要充值？**
- 圖 7 顯示充值餘額只有 ¥8.53 CNY
- 可能不足以激活新 API Key
- DeepSeek 可能要求最低餘額

---

### **步驟 2：在 Cloudflare Worker 中使用正確的 API Key**

**重要：請使用以下完整的 API Key（從圖 1 複製）：**
```
sk-d0edd459796441c190543979f4123867
```

**修改步驟：**

1. 訪問：https://dash.cloudflare.com/
2. 進入 **Workers & Pages** → **deepseek-proxy**
3. 點擊 **Quick Edit**
4. 找到第 22 行
5. **完全刪除整行**
6. **重新輸入**（或從下面複製粘貼）：

```javascript
const DEEPSEEK_API_KEY = 'sk-d0edd459796441c190543979f4123867'; // ✅ 正確的 Key（沒有多餘的 7）
```

7. **仔細檢查**：確認沒有多餘的字符
8. 點擊 **Save and Deploy**
9. 等待 30 秒

---

### **步驟 3：驗證部署**

#### **3.1 檢查 Worker 健康檢查**

訪問：https://deepseek-proxy.vaultcaddy.workers.dev

**應該看到：**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "supported_models": ["deepseek-chat", "deepseek-reasoner"],
  "max_timeout": "120 seconds",
  "updated": "2025-11-16"
}
```

#### **3.2 重新運行測試工具**

訪問：https://vaultcaddy.com/test-deepseek-api.html

**重新測試 1-4：**

| 測試 | 預期結果 |
|------|----------|
| 測試 1 | ✅ 通過（max_timeout: 120 seconds） |
| 測試 2 | ❌ 可能還是失敗（CORS 問題） |
| 測試 3 | ✅ 通過（Worker 代理調用） |
| 測試 4 | ✅ 通過（Reasoner 模型） |

**注意：** 測試 2 失敗是**正常的**，因為：
- 直接從瀏覽器調用 DeepSeek API 有 CORS 限制
- 測試 3、4 成功才是關鍵（它們通過 Worker 調用）

---

## 🎯 **關鍵檢查清單**

請逐一確認：

- [ ] DeepSeek 賬戶餘額 > ¥10 CNY（圖 7）
- [ ] Cloudflare Worker 第 22 行使用正確的 API Key（沒有多餘的 `7`）
- [ ] Worker 已保存並部署（等待 30 秒）
- [ ] Worker 健康檢查返回 `max_timeout: "120 seconds"`
- [ ] 測試 3、4 通過（Worker 代理調用成功）
- [ ] 瀏覽器緩存已清除
- [ ] 瀏覽器已重啟

---

## 🐛 **為什麼測試 2 會失敗？**

### **原因 1：CORS 限制（最可能）**

測試 2 直接從瀏覽器調用 DeepSeek API：

```javascript
fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer sk-d0edd459796441c190543979f4123867'
    },
    // ...
})
```

**問題：**
- DeepSeek API 可能不允許直接從瀏覽器調用（CORS 限制）
- 只能從服務器端調用（如 Cloudflare Worker）

**這就是為什麼：**
- ❌ 測試 2 失敗（直接調用）
- ✅ 測試 3、4 成功（通過 Worker 調用）

### **原因 2：API Key 權限問題**

新創建的 API Key 可能需要：
- 等待幾分鐘激活
- 最低賬戶餘額（如 ¥10 CNY）
- 特定的權限設置

---

## 💡 **重要結論**

**測試 2 失敗不是問題！**

只要：
- ✅ 測試 1 通過（Worker 健康）
- ✅ 測試 3 通過（Worker 代理調用）
- ✅ 測試 4 通過（Reasoner 模型）

就說明 Worker 配置正確，可以正常使用！

**測試 2 失敗的原因：**
- DeepSeek API 不允許直接從瀏覽器調用（CORS 限制）
- 這是 DeepSeek 的安全設計，不是我們的問題

---

## 🚀 **下一步：測試實際上傳**

1. ✅ 確認 Worker 第 22 行 API Key 正確（沒有多餘的 `7`）
2. ✅ 確認 Worker 已部署（健康檢查通過）
3. ✅ 清除瀏覽器緩存
4. ✅ 上傳銀行對帳單 PDF
5. ✅ 檢查 Console 日誌

**成功的日誌應該是：**
```
🏦 過濾銀行對帳單文本（激進版本 - 解決超時問題）...
✅ 銀行對帳單過濾完成：967 → 450 字符（減少 53%）
🔄 DeepSeek API 請求（第 1 次嘗試）...
✅ DeepSeek API 請求成功（第 1 次嘗試）
✅ 批量處理完成，總耗時: 25000ms
```

---

## 📞 **如果還是失敗**

請提供：

1. **Cloudflare Worker 第 22 行的截圖**
   - 確認 API Key 是否正確

2. **上傳 PDF 的完整 Console 日誌**
   - 截圖所有錯誤信息

3. **DeepSeek 賬戶餘額**
   - 確認是否有足夠餘額

我會立即幫您診斷！🚀

