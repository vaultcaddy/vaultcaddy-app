# 📝 文本分段處理策略

## 問題重新分析

### **DeepSeek-Chat 實際限制：**
- **上下文長度：** 128K tokens（約 85,000 中文字符）
- **輸出長度：** 默認 4K，最大 8K tokens
- **2521 字符：** 完全不會超過限制 ✅

### **真正的超時原因：**
1. **處理速度慢：** 複雜文本需要更長時間
2. **網絡不穩定：** Cloudflare Worker → DeepSeek
3. **API 繁忙：** 高峰時段響應變慢

---

## 🎯 **分段處理方案**

### **策略：**
- 如果文本 > 2000 字符，分段處理
- 每段 ≤ 2000 字符
- 分段數 = Math.ceil(總字符數 / 2000)

### **示例：**

| 總字符數 | 分段數 | 每段字符數 |
|----------|--------|------------|
| 2521 | 2 | 1260, 1261 |
| 5000 | 3 | 1666, 1667, 1667 |
| 10000 | 5 | 2000 × 5 |

---

## 🔧 **實現邏輯**

### **步驟 1：檢查文本長度**

```javascript
const MAX_CHUNK_SIZE = 2000; // 每段最大字符數

if (filteredText.length > MAX_CHUNK_SIZE) {
    console.log(`📝 文本過長（${filteredText.length} 字符），開始分段處理...`);
    
    // 計算分段數
    const numChunks = Math.ceil(filteredText.length / MAX_CHUNK_SIZE);
    console.log(`   將分為 ${numChunks} 段處理`);
    
    // 分段處理
    const results = [];
    for (let i = 0; i < numChunks; i++) {
        const start = i * MAX_CHUNK_SIZE;
        const end = Math.min(start + MAX_CHUNK_SIZE, filteredText.length);
        const chunk = filteredText.substring(start, end);
        
        console.log(`   處理第 ${i + 1}/${numChunks} 段（${chunk.length} 字符）...`);
        
        const result = await analyzeTextWithDeepSeek(chunk, documentType);
        results.push(result);
    }
    
    // 合併結果
    const mergedResult = mergeChunkedResults(results, documentType);
    return mergedResult;
}
```

---

### **步驟 2：合併分段結果**

**銀行對帳單：**
```javascript
function mergeChunkedResults(results, documentType) {
    if (documentType === 'bank_statement') {
        return {
            bankName: results[0].bankName || '',
            accountNumber: results[0].accountNumber || '',
            statementDate: results[0].statementDate || '',
            openingBalance: results[0].openingBalance || 0,
            closingBalance: results[results.length - 1].closingBalance || 0,
            transactions: results.flatMap(r => r.transactions || [])
        };
    }
    
    // 發票/收據：只取第一段（通常所有信息在第一段）
    if (documentType === 'invoice' || documentType === 'receipt') {
        return results[0];
    }
    
    // 通用文檔：合併所有文本
    return {
        content: results.map(r => r.content).join('\n\n')
    };
}
```

---

## 📊 **優勢分析**

### **方案對比：**

| 方案 | 優勢 | 劣勢 |
|------|------|------|
| **不分段（當前）** | 簡單，一次調用 | 超時風險高 |
| **分段處理** | 穩定，不超時 | 多次調用，成本稍高 |
| **智能過濾** | 減少字符數 | 可能丟失信息 |

### **建議：** 結合「智能過濾 + 分段處理」

1. **先過濾：** 2521 → 1600 字符（減少 35%）
2. **再檢查：** 如果仍 > 2000，分段處理
3. **最終：** 穩定性 ↑，成本 ↓

---

## 🎯 **實施計劃**

### **優先級 1：實現分段邏輯**
- 修改 `analyzeTextWithDeepSeek` 方法
- 添加分段檢查
- 實現合併邏輯

### **優先級 2：測試**
- 測試 2521 字符（分 2 段）
- 測試 5000 字符（分 3 段）
- 確認結果準確性

### **優先級 3：優化**
- 智能分段（按行分段，避免截斷交易記錄）
- 並行處理（同時處理多段，節省時間）

---

## 💰 **成本分析**

### **2521 字符銀行對帳單：**

**方案 A：不分段（當前）**
- DeepSeek 調用：1 次
- 成本：¥0.0003
- 風險：超時 ❌

**方案 B：分段（2 段）**
- DeepSeek 調用：2 次
- 成本：¥0.0006（2 倍）
- 風險：穩定 ✅

**方案 C：過濾 + 分段**
- 過濾：2521 → 1600 字符
- 分段：不需要（< 2000）
- DeepSeek 調用：1 次
- 成本：¥0.0003
- 風險：穩定 ✅

**結論：** 方案 C 最優（成本低 + 穩定）

---

## 🚀 **立即行動**

1. **保留智能過濾**（已實現）
2. **添加分段邏輯**（作為備用）
3. **測試 3 頁 PDF**

如果過濾後仍超時，分段邏輯會自動啟動！

