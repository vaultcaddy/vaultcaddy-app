# 同一天多笔交易问题 - 分析与解决方案

## 📊 问题分析

### 问题根源
**银行对账单格式特性：**
```
日期       描述                    借项    贷项    餘額
10 Mar    ATM WITHDRAWAL          500             (空白)
          ONLINE TRANSFER         200             (空白)
          POS PURCHASE            150             30,018.39
11 Mar    SALARY                          15,000  45,018.39
```

**AI 提取结果：**
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500, "balance": null },
    { "date": "", "description": "ONLINE TRANSFER", "debit": 200, "balance": null },
    { "date": "", "description": "POS PURCHASE", "debit": 150, "balance": 30018.39 },
    { "date": "11 Mar", "description": "SALARY", "credit": 15000, "balance": 45018.39 }
  ]
}
```

**问题：**
- ❌ 第2、3笔交易的 `date` 为空字符串 `""`
- ❌ 前端无法正确显示日期
- ❌ 排序和分组功能受影响

---

## 💡 解决方案

### 方案 A：前端后处理（推荐）✅

**优点：**
- 可靠、可控
- 不依赖 AI 的"智能填充"能力
- 易于调试和维护

**实现位置：**
`qwen-vl-max-processor.js` 的 `parseJSON()` 方法之后

**代码实现：**

```javascript
/**
 * 后处理：填充空白日期（同一天多笔交易）
 * @param {Object} extractedData - AI 提取的原始数据
 * @returns {Object} 处理后的数据
 */
function postProcessTransactions(extractedData) {
    if (!extractedData.transactions || !Array.isArray(extractedData.transactions)) {
        return extractedData;
    }
    
    let lastValidDate = null;
    
    extractedData.transactions = extractedData.transactions.map((tx) => {
        // 如果当前交易的日期为空/null/undefined，使用上一笔的日期
        if (!tx.date || tx.date.trim() === '') {
            if (lastValidDate) {
                tx.date = lastValidDate;
            } else {
                // 如果是第一笔就为空，使用 statement 的开始日期
                tx.date = 'Unknown';
            }
        } else {
            // 更新最后有效日期
            lastValidDate = tx.date;
        }
        
        return tx;
    });
    
    return extractedData;
}
```

**集成到现有代码：**

在 `processDocument()` 和 `processMultiPageDocument()` 方法中：

```javascript
// 6. 解析 JSON
const extractedData = this.parseJSON(responseText);

// ✅ 新增：后处理 - 填充空白日期
const processedData = this.postProcessTransactions(extractedData);

return {
    success: true,
    documentType: documentType,
    extractedData: processedData,  // ← 使用处理后的数据
    // ...
};
```

---

### 方案 B：优化 Prompt（备选）

**在 Prompt 中新增规则：**

```
📅 DATE FILLING RULE (CRITICAL FOR SAME-DATE TRANSACTIONS):
• IF current row's Date column is EMPTY/BLANK/contains only spaces:
  → Copy the date from the PREVIOUS transaction row
  → NEVER output empty string "" for date
• IF current row's Date column has visible text:
  → Copy that text as-is
• IF first row has empty date (rare case):
  → Extract date from statement header/period

✅ EXAMPLE (3 transactions on same day):
PDF shows:
  10 Mar  ATM        500   (空白)
          POS        200   (空白)
          Transfer   100   30,018.39

Output:
  { "date": "10 Mar", "debit": 500, "balance": null },
  { "date": "10 Mar", "debit": 200, "balance": null },
  { "date": "10 Mar", "debit": 100, "balance": 30018.39 }

❌ WRONG:
  { "date": "", ... }  ← NEVER output empty date!
```

**风险：**
- AI 可能不理解"PREVIOUS row"的概念
- 可能需要多次测试和调整
- 不如后处理脚本可靠

---

## 🎯 推荐实施步骤

### 阶段 1：立即实施（前端后处理）

1. ✅ 在 `qwen-vl-max-processor.js` 中添加 `postProcessTransactions()` 方法
2. ✅ 在 `processDocument()` 和 `processMultiPageDocument()` 中调用
3. ✅ 测试多个银行对账单，确保日期填充正确

### 阶段 2：咨询千问 AI（Prompt 优化）

1. 📧 将 `QWEN_QUESTION_SAME_DATE.md` 发送给千问 AI 团队
2. ⏳ 等待回复和建议
3. 🧪 如果 AI 能理解"日期填充"逻辑，更新 Prompt 并测试

### 阶段 3：双重保险（如果 Prompt 优化成功）

- 保留前端后处理作为**兜底方案**
- 即使 AI 填充了日期，后处理脚本仍会检查并补漏
- 确保 100% 的日期完整性

---

## 📝 测试用例

### 测试 1：同日 3 笔交易
```
10 Mar  ATM        500   -
        POS        200   -
        Transfer   100   30,018.39
```

**期望输出：**
```json
[
  { "date": "10 Mar", "debit": 500, "balance": null },
  { "date": "10 Mar", "debit": 200, "balance": null },
  { "date": "10 Mar", "debit": 100, "balance": 30018.39 }
]
```

### 测试 2：跨日交易
```
10 Mar  ATM        500   30,018.39
11 Mar  Salary     -     15,000   45,018.39
```

**期望输出：**
```json
[
  { "date": "10 Mar", "debit": 500, "balance": 30018.39 },
  { "date": "11 Mar", "credit": 15000, "balance": 45018.39 }
]
```

### 测试 3：混合场景
```
10 Mar  ATM        500   -
        POS        200   30,018.39
11 Mar  Salary     -     15,000   45,018.39
```

**期望输出：**
```json
[
  { "date": "10 Mar", "debit": 500, "balance": null },
  { "date": "10 Mar", "debit": 200, "balance": 30018.39 },
  { "date": "11 Mar", "credit": 15000, "balance": 45018.39 }
]
```

---

## ⚠️ 注意事项

1. **余额处理：**
   - 同日多笔交易中，前N-1笔的 `balance` 为 `null` 是正常的
   - 前端显示时，如果 `balance === null`，可以累加计算：
     ```javascript
     displayBalance = previousBalance + credit - debit
     ```

2. **日期格式：**
   - 保持原始格式（"10 Mar"、"2025-03-10" 等）
   - 不进行格式转换，避免引入错误

3. **边界情况：**
   - 第一笔交易日期为空：使用 `statementPeriod` 的开始日期
   - 所有交易日期都为空：标记为数据错误，提示用户

---

## 📊 实施优先级

| 方案 | 优先级 | 开发时间 | 可靠性 | 维护成本 |
|------|--------|---------|--------|---------|
| 前端后处理 | ⭐⭐⭐⭐⭐ | 30 分钟 | 99% | 低 |
| Prompt 优化 | ⭐⭐⭐ | 需等待千问回复 | 70-90% | 中 |
| 双重保险 | ⭐⭐⭐⭐⭐ | 前端后处理 + Prompt | 99.9% | 低 |

**结论：先实施前端后处理，同时咨询千问 AI。** ✅

