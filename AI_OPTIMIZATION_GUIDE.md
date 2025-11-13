# 🤖 AI 成本優化完整指南

## 📊 當前成本分析

### 問題：AI 成本占總成本 95%

```
DeepSeek API：  $4,375/月（95.4%）
其他 Firebase：  $209/月  （4.6%）
────────────────────────────────
總成本：       $4,584/月
```

**單頁成本：**
```
Vision OCR：$0.00148/頁
DeepSeek AI：$0.035/頁
────────────────────────────────
總計：      $0.03648/頁
```

**目標：將單頁成本降低 67% → $0.012/頁**

---

## 🎯 Part 1: 優化 AI 提示詞（立即執行）

### 1.1 減少輸入 Token

#### ❌ 當前提示詞（低效）

```javascript
const prompt = `
請從以下 OCR 文本中提取發票信息：

OCR 文本：
${fullOcrText}  // ← 包含大量無用內容！

請提取以下信息：
1. 供應商名稱
2. 發票號碼
3. 發票日期
4. 總金額
5. 稅額
6. 明細項目
... 還有 20+ 個字段

輸出格式：
請以 JSON 格式輸出，包含所有字段，每個字段都要有詳細說明...
... 還有 500+ 字的格式說明
`;
```

**問題：**
- OCR 文本包含大量空白、重複、無關內容
- 提示詞冗長，重複說明
- 每次都發送完整格式要求

**成本：**
```
OCR 文本：2,000-3,000 tokens
提示詞：  500-800 tokens
────────────────────────────────
總輸入：  2,500-3,800 tokens × $0.01/1K = $0.025-0.038
```

---

#### ✅ 優化後提示詞（高效）

```javascript
// 1. 預處理 OCR 文本
function cleanOcrText(rawText) {
    return rawText
        .replace(/\s+/g, ' ')           // 合併多個空格
        .replace(/(\r\n|\n|\r){3,}/g, '\n\n')  // 移除多餘換行
        .trim()
        .slice(0, 3000);                // 限制最大長度
}

// 2. 簡化提示詞（移除冗余）
const optimizedPrompt = `Extract from OCR:
${cleanOcrText(rawText)}

Output JSON: {vendor, invoiceNo, date, total, tax, items}`;
```

**節省：**
```
優化後輸入：600-1,200 tokens（減少 60-70%）
成本：      $0.006-0.012（節省 $0.019-0.026）
```

---

### 1.2 減少輸出 Token

#### ❌ 當前輸出（低效）

```json
{
  "vendor": "ABC Company Limited",
  "vendorAddress": "123 Main Street, Hong Kong",
  "vendorPhone": "+852 1234 5678",
  "vendorEmail": "info@abc.com",
  "vendorTaxId": "12345678",
  "invoiceNumber": "INV-2025-001",
  "invoiceDate": "2025-01-12",
  "dueDate": "2025-02-12",
  "purchaseOrder": "PO-12345",
  "customerName": "XYZ Corp",
  "customerAddress": "456 Market St",
  ... 還有 20+ 個字段
  "items": [
    {
      "itemNumber": 1,
      "productCode": "PRD-001",
      "description": "Product A with very long description...",
      "quantity": 10,
      "unit": "pcs",
      "unitPrice": 100.50,
      "subtotal": 1005.00,
      "tax": 80.40,
      "total": 1085.40
    }
  ],
  "notes": "Additional notes and comments...",
  "metadata": {
    "extractedAt": "2025-01-12T10:30:00Z",
    "confidence": 0.95,
    "model": "deepseek-chat"
  }
}
```

**成本：**
```
輸出：800-1,200 tokens × $0.03/1K = $0.024-0.036
```

---

#### ✅ 優化後輸出（精簡）

```javascript
// 只要求必要字段
const optimizedPrompt = `Extract minimal data:
${cleanText}

Return compact JSON:
{v:vendor,n:invoiceNo,d:date,t:total,tx:tax,i:[{d:desc,q:qty,p:price}]}`;
```

**輸出示例：**
```json
{
  "v": "ABC Co",
  "n": "INV-001",
  "d": "2025-01-12",
  "t": 1085.40,
  "tx": 80.40,
  "i": [{"d": "Prod A", "q": 10, "p": 100.50}]
}
```

**節省：**
```
優化後輸出：200-400 tokens（減少 70-75%）
成本：      $0.006-0.012（節省 $0.018-0.024）
```

---

### 1.3 使用更便宜的模型

| 模型 | 輸入成本 | 輸出成本 | 適用場景 |
|------|---------|---------|---------|
| DeepSeek Chat | $0.01/1K | $0.03/1K | 複雜發票 |
| GPT-4 Turbo | $0.01/1K | $0.03/1K | 複雜發票 |
| **GPT-3.5 Turbo** | **$0.0005/1K** | **$0.0015/1K** | **簡單發票** ✅ |
| Claude Haiku | $0.00025/1K | $0.00125/1K | 簡單發票 ✅ |

**策略：智能路由**
```javascript
function selectModel(documentComplexity) {
    if (documentComplexity === 'simple') {
        return 'gpt-3.5-turbo';  // 便宜 20 倍！
    } else {
        return 'deepseek-chat';  // 複雜才用
    }
}
```

**節省：**
```
假設 70% 文檔是簡單的：
簡單文檔成本：$0.002/頁（使用 GPT-3.5）
複雜文檔成本：$0.035/頁（使用 DeepSeek）

平均成本：0.7 × $0.002 + 0.3 × $0.035 = $0.0119/頁
節省：    $0.035 - $0.0119 = $0.0231/頁（66%）
```

---

## 🔄 Part 2: 實施緩存機制（中期執行）

### 2.1 識別重複文檔

```javascript
// 計算文檔指紋
function getDocumentFingerprint(ocrText) {
    const normalized = ocrText.replace(/\s+/g, '').toLowerCase();
    return CryptoJS.SHA256(normalized).toString();
}

// 檢查緩存
async function processWithCache(file, ocrText) {
    const fingerprint = getDocumentFingerprint(ocrText);
    
    // 查詢緩存
    const cached = await db.collection('extractionCache')
        .doc(fingerprint)
        .get();
    
    if (cached.exists) {
        console.log('✅ 使用緩存結果');
        return cached.data().extractedData;
    }
    
    // 沒有緩存，調用 AI
    const result = await callDeepSeekAPI(ocrText);
    
    // 保存到緩存
    await db.collection('extractionCache').doc(fingerprint).set({
        extractedData: result,
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 天
    });
    
    return result;
}
```

**節省：**
```
假設 20% 文檔是重複的：
節省：0.2 × $4,375 = $875/月
```

---

### 2.2 模板匹配

```javascript
// 識別常見供應商模板
const vendorTemplates = {
    'HW海運達': {
        vendor: { regex: /HW.{0,10}海運達/, confidence: 0.95 },
        invoiceNo: { regex: /INV-\d{6}/, position: 'top-right' },
        total: { regex: /總額[:：]\s*\$?([\d,]+\.?\d*)/, group: 1 }
    },
    // ... 其他供應商
};

// 先嘗試模板匹配
function tryTemplateMatch(ocrText, vendor) {
    const template = vendorTemplates[vendor];
    if (!template) return null;
    
    // 嘗試提取所有字段
    const extracted = {};
    for (const [field, rule] of Object.entries(template)) {
        const match = ocrText.match(rule.regex);
        if (match) {
            extracted[field] = match[rule.group || 0];
        }
    }
    
    // 如果提取了 80% 以上字段，使用模板結果
    const extractionRate = Object.keys(extracted).length / Object.keys(template).length;
    if (extractionRate >= 0.8) {
        console.log('✅ 使用模板匹配，跳過 AI');
        return extracted;
    }
    
    return null;  // 需要 AI
}
```

**節省：**
```
假設 30% 文檔可以用模板：
節省：0.3 × $4,375 = $1,312.5/月
```

---

## 🚀 Part 3: 批次處理（立即執行）

### 3.1 合併多個文檔

```javascript
// ❌ 當前：逐個處理
for (const file of files) {
    const result = await processDocument(file);  // 每次單獨調用 API
}

// ✅ 優化：批次處理
async function batchProcess(files) {
    // 合併多個文檔到一個請求
    const batchPrompt = files.map((file, i) => 
        `Document ${i+1}:\n${cleanOcrText(file.ocrText)}\n---`
    ).join('\n');
    
    const prompt = `Extract from ${files.length} documents:
${batchPrompt}

Return array of JSON objects.`;
    
    const results = await callDeepSeekAPI(prompt);
    return results;
}
```

**節省：**
```
批次處理 5 個文檔：
- 減少 API 調用開銷
- 共享提示詞前綴
- 節省：約 15-20%
```

---

## 📊 Part 4: 總體優化效果

### 優化前後對比

| 優化措施 | 節省比例 | 節省金額 |
|---------|---------|---------|
| **提示詞優化** | 40-50% | $1,750-2,188/月 |
| **緩存機制** | 15-20% | $656-875/月 |
| **模板匹配** | 20-30% | $875-1,312/月 |
| **批次處理** | 10-15% | $438-656/月 |
| **智能路由** | 50-70% | $2,188-3,063/月 |

**總節省（組合使用）：**
```
保守估計：$2,000-2,500/月（45-57%）
樂觀估計：$3,000-3,500/月（68-80%）
```

**優化後成本：**
```
當前：$4,584/月
優化後：$1,000-1,500/月
節省：約 70%
```

---

## 💻 Part 5: 實施代碼示例

### 完整優化流程

```javascript
// hybrid-vision-deepseek.js

class OptimizedProcessor {
    constructor() {
        this.cache = new Map();
        this.templates = this.loadTemplates();
    }
    
    async process(file, documentType) {
        // 1. 檢查緩存
        const fingerprint = this.getFingerprint(file);
        if (this.cache.has(fingerprint)) {
            console.log('✅ 使用緩存');
            return this.cache.get(fingerprint);
        }
        
        // 2. OCR 提取
        const ocrText = await this.runVisionOCR(file);
        const cleanText = this.cleanText(ocrText);
        
        // 3. 嘗試模板匹配
        const templateResult = this.tryTemplate(cleanText, documentType);
        if (templateResult && templateResult.confidence > 0.85) {
            console.log('✅ 使用模板');
            return templateResult.data;
        }
        
        // 4. 評估複雜度
        const complexity = this.assessComplexity(cleanText);
        
        // 5. 選擇模型
        const model = complexity === 'simple' ? 'gpt-3.5-turbo' : 'deepseek-chat';
        
        // 6. 構建精簡提示詞
        const prompt = this.buildOptimizedPrompt(cleanText, documentType);
        
        // 7. 調用 AI
        const result = await this.callAI(model, prompt);
        
        // 8. 保存緩存
        this.cache.set(fingerprint, result);
        await this.saveToFirestoreCache(fingerprint, result);
        
        return result;
    }
    
    cleanText(rawText) {
        return rawText
            .replace(/\s+/g, ' ')
            .replace(/(\r\n|\n|\r){3,}/g, '\n\n')
            .trim()
            .slice(0, 3000);
    }
    
    assessComplexity(text) {
        // 簡單：單頁、少項目、清晰格式
        if (text.length < 500 && text.split('\n').length < 30) {
            return 'simple';
        }
        // 複雜：多頁、多項目、混亂格式
        return 'complex';
    }
    
    buildOptimizedPrompt(text, type) {
        const templates = {
            invoice: 'Extract: {v:vendor,n:no,d:date,t:total,i:items}',
            receipt: 'Extract: {v:merchant,d:date,t:total,i:items}',
            statement: 'Extract: {b:bank,p:period,txs:transactions}'
        };
        
        return `${templates[type]}\n${text}`;
    }
    
    async callAI(model, prompt) {
        const tokens = this.estimateTokens(prompt);
        console.log(`📊 使用 ${model}，預估 ${tokens} tokens`);
        
        // 調用 API...
    }
}
```

---

## 📈 Part 6: 監控和調整

### 實施監控

```javascript
// 記錄每次處理的成本
class CostTracker {
    async trackProcessing(documentId, details) {
        await db.collection('processingCosts').add({
            documentId,
            model: details.model,
            inputTokens: details.inputTokens,
            outputTokens: details.outputTokens,
            cost: details.cost,
            cacheHit: details.cacheHit,
            templateUsed: details.templateUsed,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
        });
    }
    
    async getMonthlyStats() {
        const snapshot = await db.collection('processingCosts')
            .where('timestamp', '>=', startOfMonth())
            .get();
        
        const stats = {
            totalCost: 0,
            cacheHitRate: 0,
            templateRate: 0,
            avgCostPerDoc: 0
        };
        
        // 計算統計...
        return stats;
    }
}
```

---

## 🎯 實施計劃

### 第一週（立即執行）

**目標：節省 30-40%**

- [x] 優化提示詞（減少 token）
- [x] 清理 OCR 文本
- [x] 精簡輸出格式
- [x] 部署更新

**預估節省：$1,300-1,750/月**

---

### 第二-四週（中期執行）

**目標：額外節省 20-30%**

- [ ] 實施緩存機制
- [ ] 建立供應商模板庫
- [ ] 實施批次處理
- [ ] 添加成本監控

**預估額外節省：$875-1,312/月**

---

### 第五-八週（長期優化）

**目標：總節省 70%**

- [ ] 智能模型路由
- [ ] 完善模板庫（覆蓋 50% 文檔）
- [ ] 優化緩存策略
- [ ] 考慮自建簡單模型

**預估總節省：$3,000-3,500/月**

---

## 💰 ROI 計算

### 投入成本

```
開發時間：40-60 小時
開發成本：假設 $0（自己做）
測試時間：10-20 小時
────────────────────────────────
總投入：  50-80 小時工作
```

### 回報

```
月節省：  $2,000-3,500
年節省：  $24,000-42,000
ROI：     無限（因為開發成本為 $0）
回收期：  立即
```

---

## 📝 總結

### 優先級排序

**🔴 高優先級（立即執行）：**
1. ✅ 優化提示詞（2-3 天）
2. ✅ 清理 OCR 文本（1 天）
3. ✅ 精簡輸出（1 天）

**🟡 中優先級（1-2 週）：**
4. ⚠️ 實施緩存（3-5 天）
5. ⚠️ 批次處理（2-3 天）

**🟢 低優先級（1-2 個月）：**
6. ⏳ 模板匹配（1-2 週）
7. ⏳ 智能路由（1 週）
8. ⏳ 成本監控（1 週）

---

**下一步：開始實施提示詞優化！** 🚀

