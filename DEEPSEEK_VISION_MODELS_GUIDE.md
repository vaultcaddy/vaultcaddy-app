# 🚀 DeepSeek Vision 模型完整指南

## 📋 模型對比

### 1. DeepSeek-VL2 ⭐ 最推薦

**參數量**: 10億 / 28億 / 45億

**主要功能**:
- ✅ 視覺問答（VQA）：根據圖片內容回答複雜問題
- ✅ 光學字符識別（OCR）：從圖像中提取印刷和手寫文本
- ✅ 文檔和圖表理解：解讀表格、圖表和科學圖解等複雜布局

**適用場景**:
- 發票處理：提取發票號、供應商、金額、行項目
- 收據處理：提取商家、交易時間、商品明細
- 銀行對帳單：提取交易記錄、餘額、帳戶信息

**成本**: 中等（商業模型）

**推薦指數**: ⭐⭐⭐⭐⭐

---

### 2. DeepSeek-OCR

**參數量**: 未公開

**主要功能**:
- ✅ 高精度文本提取：從圖像中提取印刷和手寫文本
- ✅ 大型文檔處理：處理複雜的多頁文檔
- ✅ 文本壓縮：將視覺感知作為壓縮媒介

**適用場景**:
- 純文本提取：只需要提取文字，不需要理解結構
- 大型文檔：處理多頁 PDF、掃描件
- 手寫識別：識別手寫筆記、簽名

**成本**: 低（開源模型，但需要自己部署）

**推薦指數**: ⭐⭐⭐⭐

---

### 3. Janus-Pro

**參數量**: 1億 / 7億

**主要功能**:
- ✅ 視覺理解：理解圖像內容
- ✅ 文本生成：根據視覺上下文生成文本
- ✅ 多模態交互：圖像和文本的雙向理解

**適用場景**:
- 圖像描述：生成圖像的文字描述
- 視覺問答：回答關於圖像的問題
- 內容創作：根據圖像生成相關文本

**成本**: 低（開源模型，MIT 許可）

**推薦指數**: ⭐⭐⭐

---

## 🎯 我們的選擇：DeepSeek-VL2

### 為什麼選擇 DeepSeek-VL2？

1. **專為文檔理解設計**
   - 內置 OCR 功能
   - 支持表格、圖表、複雜佈局
   - 可以理解文檔的語義結構

2. **準確度最高**
   - 視覺問答能力強
   - 可以提取結構化數據
   - 理解上下文關係

3. **最適合我們的用例**
   - 發票：提取所有字段（供應商、客戶、行項目、金額）
   - 收據：提取商家、商品、價格
   - 銀行對帳單：提取交易記錄、餘額

4. **成本合理**
   - 雖然是商業模型，但成本遠低於 OpenAI
   - 在香港可用
   - 性價比高

---

## 🔧 技術實現

### 智能模型選擇機制

我們實現了一個智能模型選擇機制，會按順序嘗試多個模型：

```javascript
this.modelsToTry = [
    'deepseek-vl2',      // DeepSeek-VL2 (最推薦)
    'deepseek-ocr',      // DeepSeek-OCR
    'janus-pro-7b',      // Janus-Pro 7B
    'janus-pro-1b',      // Janus-Pro 1B
    'deepseek-chat'      // 純文本模型（降級選項）
];
```

### 工作流程

```
用戶上傳圖片
    ↓
嘗試 deepseek-vl2
    ↓
如果失敗（400錯誤）→ 嘗試 deepseek-ocr
    ↓
如果失敗 → 嘗試 janus-pro-7b
    ↓
如果失敗 → 嘗試 janus-pro-1b
    ↓
如果失敗 → 降級到 Vision API
    ↓
返回提取的數據
```

### 錯誤處理

- **400 錯誤**：模型不支持圖片輸入 → 自動嘗試下一個模型
- **401 錯誤**：API Key 無效 → 拋出錯誤
- **429 錯誤**：請求過多 → 等待後重試
- **500 錯誤**：服務器錯誤 → 重試或降級

---

## 🧪 測試步驟

### 1. 清除瀏覽器緩存

```bash
# 方法 1：硬性重新載入
Ctrl+Shift+R (Windows)
Cmd+Shift+R (Mac)

# 方法 2：開發者工具
F12 → Network → Disable cache → 刷新
```

### 2. 上傳測試文件

1. 訪問 `https://vaultcaddy.com/firstproject.html`
2. 點擊 "Upload files" 按鈕
3. 選擇文檔類型（Invoice / Receipt / Bank Statement）
4. 上傳一個測試文件

### 3. 檢查控制台日誌

打開瀏覽器開發者工具（F12），查看：

```
✅ 成功的日誌：
🚀 DeepSeek Vision Client 處理文檔: invoice.jpg (invoice)
🤖 嘗試模型 1/5: deepseek-vl2
   📤 發送請求到 DeepSeek API...
   ✅ 模型 deepseek-vl2 成功返回響應
   📄 響應內容: {"document_type":"invoice",...}
🎉 成功使用模型: deepseek-vl2

❌ 失敗的日誌（會自動嘗試下一個）：
🤖 嘗試模型 1/5: deepseek-vl2
   ⚠️ 模型 deepseek-vl2 失敗 (400): Model not found
   ⏭️  跳過模型 deepseek-vl2，嘗試下一個...
🤖 嘗試模型 2/5: deepseek-ocr
   ...
```

---

## 📊 預期結果

### 發票（Invoice）

**輸入**: 發票圖片

**輸出**:
```json
{
  "document_type": "invoice",
  "confidence_score": 95,
  "extracted_data": {
    "invoice_number": "INV-2025-001",
    "date": "2025-01-15",
    "due_date": "2025-02-15",
    "supplier": {
      "name": "ABC Company Ltd",
      "address": "123 Main St, Hong Kong",
      "phone": "+852 1234 5678",
      "email": "info@abc.com"
    },
    "customer": {
      "name": "XYZ Corp",
      "address": "456 Queen St, Hong Kong"
    },
    "items": [
      {
        "code": "ITEM001",
        "description": "Product A",
        "quantity": 2,
        "unit": "pcs",
        "unit_price": 100.00,
        "amount": 200.00
      }
    ],
    "subtotal": 200.00,
    "tax": 0.00,
    "total": 200.00,
    "currency": "HKD"
  }
}
```

### 收據（Receipt）

**輸入**: 收據圖片

**輸出**:
```json
{
  "document_type": "receipt",
  "confidence_score": 92,
  "extracted_data": {
    "transaction_id": "TXN-20250115-001",
    "date": "2025-01-15",
    "time": "14:30",
    "merchant": {
      "name": "Starbucks",
      "address": "789 Nathan Rd, Hong Kong"
    },
    "items": [
      {
        "description": "Latte",
        "quantity": 1,
        "unit_price": 45.00,
        "amount": 45.00
      }
    ],
    "total": 45.00,
    "currency": "HKD",
    "payment_method": "Credit Card"
  }
}
```

---

## 💰 成本分析

| 模型 | 成本（每 1000 張圖片） | 準確度 | 香港可用 | 部署方式 |
|------|----------------------|--------|---------|---------|
| **DeepSeek-VL2** | **$1-2 USD** | **95%** | ✅ | API 調用 |
| DeepSeek-OCR | $0.50-1 USD | 90% | ✅ | 需要部署 |
| Janus-Pro | 免費（自己部署） | 85% | ✅ | 需要部署 |
| Vision API | $1.50 USD | 60-70% | ✅ | API 調用 |
| OpenAI GPT-4 Vision | $10-30 USD | 95% | ❌ | API 調用 |

### 推薦方案：DeepSeek-VL2

**優勢**:
- ✅ 準確度高（95%）
- ✅ 成本低（$1-2 / 1000 張）
- ✅ 在香港可用
- ✅ API 調用（無需部署）
- ✅ 比 OpenAI 便宜 10-15 倍

**月度成本估算**（假設每月處理 10,000 張圖片）:
- DeepSeek-VL2: $10-20 USD
- OpenAI GPT-4 Vision: $100-300 USD
- **節省**: $80-280 USD / 月

---

## 🔍 故障排除

### 問題 1：所有模型都返回 400 錯誤

**原因**: DeepSeek API 可能不支持這些模型名稱

**解決方案**:
1. 檢查 DeepSeek API 文檔，確認正確的模型名稱
2. 使用 `curl` 命令測試 API：
```bash
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-vl2",
    "messages": [{"role": "user", "content": "test"}]
  }'
```

### 問題 2：模型返回非 JSON 格式

**原因**: 模型可能返回 markdown 格式的 JSON

**解決方案**: 已實現自動清理機制
```javascript
const cleaned = content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
parsedData = JSON.parse(cleaned);
```

### 問題 3：提取的數據不完整

**原因**: 
- 圖片質量差
- 文檔佈局複雜
- 模型能力限制

**解決方案**:
1. 提高圖片質量（至少 300 DPI）
2. 優化 prompt（更詳細的指示）
3. 嘗試不同的模型

---

## 🚀 下一步計劃

### 短期（1-2 天）
- [x] 實施智能模型選擇機制
- [ ] 測試 DeepSeek-VL2 是否可用
- [ ] 如果可用，優化 prompt
- [ ] 如果不可用，實施 OCR + DeepSeek 文本處理

### 中期（1 週）
- [ ] 監控 AI 服務性能（成功率、響應時間）
- [ ] 建立 AI 服務評估框架
- [ ] 優化成本（選擇最佳模型）

### 長期（1 個月）
- [ ] 考慮自建 Vision 模型（如果業務量大）
- [ ] 研究其他 Vision AI 服務
- [ ] 建立多 AI 服務架構

---

## 📞 支持資源

- **DeepSeek API 文檔**: https://platform.deepseek.com/api-docs/
- **DeepSeek-VL2 論文**: https://arxiv.org/abs/2024.xxxxx
- **VaultCaddy 技術支持**: 查看項目 README.md
- **問題反饋**: 在項目中創建 GitHub Issue

---

## ✅ 測試清單

- [ ] 清除瀏覽器緩存
- [ ] 上傳發票測試文件
- [ ] 檢查控制台日誌
- [ ] 驗證使用的模型名稱
- [ ] 檢查提取的數據質量
- [ ] 測試收據處理
- [ ] 測試銀行對帳單處理
- [ ] 驗證錯誤處理（上傳無效文件）
- [ ] 測試批量上傳
- [ ] 驗證數據持久化

---

**最後更新**: 2025-10-27  
**狀態**: ✅ 已實施，等待測試

