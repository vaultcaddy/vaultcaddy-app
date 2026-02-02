# 千问 AI 优化建议 - 已实施总结

## 📊 千问 AI 的核心发现

### 问题本质
> **多模态大模型无法可靠执行"跨行状态继承"逻辑**  
> 不是能力不足，而是架构限制 —— 模型按单张图片/单个视觉区域做独立推理，不维护行间状态变量

### 实测数据
- ❌ 尝试让 AI 填充日期：错误率从 **12% 升至 37%**
- ✅ 使用后端确定性填充：错误率 **< 1%**（仅 OCR 误识别）

### 核心建议
**两阶段处理：**
1. **AI 专注 OCR**：只负责"抄录"，不做"推理"
2. **后端确定性填充**：用简单代码处理空白日期（100% 可靠）

---

## ✅ 我们的实施方案

### 1. **后端填充逻辑（已实施）** ✓

**位置：** `qwen-vl-max-processor.js` → `postProcessTransactions()` 方法

**功能：**
```javascript
// 遍历所有交易，自动填充空白日期
let lastValidDate = null;
for (const tx of transactions) {
    if (tx.date && tx.date.trim() !== '') {
        lastValidDate = tx.date;  // 更新最后有效日期
    } else {
        tx.date = lastValidDate || 'Unknown';  // 使用上一笔的日期
    }
}
```

**优势：**
- ✅ 100% 确定性（不依赖 AI 推理）
- ✅ 易于调试（可加日志）
- ✅ 可扩展（支持日期重置检测）

---

### 2. **Prompt 优化（已实施）** ✓

**按照千问建议，修改了 2 处关键指令：**

#### **修改 1：明确空白日期的处理**

**修改前（模糊）：**
```
• "date": copy RAW text from Date column → keep as-is. Never convert.
```

**修改后（明确）：**
```
• "date": copy RAW text from Date column. 
         If empty / blank / whitespace-only → output "" (empty string). 
         NEVER fill or infer.
```

**效果：**
- ✅ AI 不再尝试"猜测"空白日期
- ✅ 明确输出 `"date": ""`，方便后端识别和填充

---

#### **修改 2：添加同日多笔交易示例**

**新增输出示例：**
```json
{
  "transactions": [
    {
      "date": "10 Mar",
      "description": "ATM WITHDRAWAL",
      "credit": 0,
      "debit": 500.00,
      "balance": null
    },
    {
      "date": "",  // ← INTENTIONALLY EMPTY — backend will fill
      "description": "ONLINE TRANSFER",
      "credit": 0,
      "debit": 200.00,
      "balance": null
    },
    {
      "date": "",
      "description": "POS PURCHASE",
      "credit": 0,
      "debit": 150.00,
      "balance": 30018.39
    }
  ]
}
```

**效果：**
- ✅ AI 看到具体示例，明白空白日期是正常的
- ✅ 注释 `// backend will fill` 强化了"AI 不负责填充"的概念

---

### 3. **处理流程（完整）** ✓

```
┌─────────────┐
│ 1. PDF 上传  │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ 2. Qwen-VL-Max OCR   │ ← AI 只负责"抄录"
│    输出原始 JSON      │
└──────┬───────────────┘
       │ {
       │   "date": "10 Mar", "debit": 500, "balance": null
       │ },
       │ {
       │   "date": "",       "debit": 200, "balance": null  ← 空白日期
       │ }
       ▼
┌──────────────────────────┐
│ 3. postProcessTransactions() │ ← 后端确定性填充
│    填充空白日期               │
└──────┬───────────────────────┘
       │ {
       │   "date": "10 Mar", "debit": 500, "balance": null
       │ },
       │ {
       │   "date": "10 Mar", "debit": 200, "balance": null  ← 已填充
       │ }
       ▼
┌─────────────────┐
│ 4. 保存到 Firestore │
└─────────────────┘
```

---

## 📊 对比分析

| 方案 | AI 填充日期 | 后端填充日期（我们的方案） |
|------|------------|---------------------------|
| **可靠性** | 63% (千问实测) | 99%+ |
| **错误来源** | AI 误判"previous row" | 仅 OCR 误识别 |
| **调试难度** | 高（AI 黑盒） | 低（纯逻辑代码） |
| **维护成本** | 高（需反复调 Prompt） | 低（10行代码） |
| **扩展性** | 差（无法加日志） | 好（可加检测/验证） |

---

## 🧪 测试用例

### 输入（AI 提取结果）
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "ATM", "debit": 500, "balance": null },
    { "date": "", "description": "POS", "debit": 200, "balance": null },
    { "date": "", "description": "Transfer", "debit": 150, "balance": 30018.39 }
  ]
}
```

### 输出（后端填充后）
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "ATM", "debit": 500, "balance": null },
    { "date": "10 Mar", "description": "POS", "debit": 200, "balance": null },
    { "date": "10 Mar", "description": "Transfer", "debit": 150, "balance": 30018.39 }
  ]
}
```

✅ **所有日期已填充，数据完整！**

---

## 🎯 千问 AI 的其他建议

### 可选实施：后端填充余额

**目的：** 为前端显示提供完整的余额数据

**代码示例（千问提供）：**
```javascript
function fillCumulativeBalance(transactions, openingBalance) {
    let balance = openingBalance;
    for (const tx of transactions) {
        if (tx.balance !== null) {
            balance = tx.balance;  // 使用银行的官方余额
        } else {
            balance = balance + tx.credit - tx.debit;  // 累加计算
        }
        tx.balanceDisplay = balance;  // 新增字段用于显示
    }
    return transactions;
}
```

**建议：**
- ⏳ 暂不实施（当前前端已能处理 `balance: null`）
- 📌 如果未来需要"实时余额预览"功能，可以添加

---

## ✅ 总结

### 千问 AI 的价值
1. ✅ **验证了我们的方案是正确的**（两阶段处理）
2. ✅ **提供了实测数据**（AI 填充错误率 37%）
3. ✅ **给出了明确的 Prompt 优化建议**（2 处关键修改）
4. ✅ **解释了问题的本质**（架构限制，非能力不足）

### 我们的实施
- ✅ **后端填充**：`postProcessTransactions()` 已完整实现
- ✅ **Prompt 优化**：已按千问建议修改（明确空白日期 + 添加示例）
- ✅ **完整流程**：AI OCR → 后端填充 → 保存数据

### 下一步
- 🧪 **测试恒生银行对账单**（之前出现问题的样本）
- 📊 **监控提取准确率**（预期 > 99%）
- 📝 **收集更多银行格式**（确保通用性）

---

## 📚 相关文档

- `QWEN_QUESTION_SAME_DATE.md` - 向千问 AI 的咨询问题（详细版）
- `QWEN_QUESTION_SAME_DATE_SHORT.txt` - 向千问 AI 的咨询问题（简洁版）
- `SAME_DATE_SOLUTION.md` - 同日多笔交易问题的完整解决方案
- `qwen-vl-max-processor.js` - 核心处理代码（包含后端填充逻辑）

**最后更新：** 2026-02-02

