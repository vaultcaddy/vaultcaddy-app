# 千问 AI 优化咨询：同一天多笔交易的提取问题

## 📋 问题背景

我们使用 Qwen-VL-Max 提取银行对账单，遇到一个**银行格式特性**导致的提取难题。

---

## 🔍 问题描述

### 实际银行对账单格式（以恒生银行为例）

银行对账单中，**同一天的多笔交易**有以下格式特点：

```
日期       描述                    借项(支出)  贷项(存入)  餘額
10 Mar    ATM WITHDRAWAL          500.00                  (空白)
          ONLINE TRANSFER         200.00                  (空白)
          POS PURCHASE            150.00                  30,018.39
11 Mar    SALARY                              15,000.00   45,018.39
```

**关键特性：**
1. ✅ 同一天的第1笔交易：显示日期
2. ❌ 同一天的第2/3/...笔交易：**日期列为空**（或显示为空格）
3. ❌ 同一天的前N-1笔交易：**余额列为空**（或显示为"—"）
4. ✅ 同一天的最后1笔交易：显示**当天最终余额**

---

## ❌ 当前 Prompt 的问题

我们目前的提取规则：

```
✂️ FIELD EXTRACTION RULES (NON-NEGOTIABLE):
| JSON Field | Source Column | Action                                  |
|------------|---------------|-----------------------------------------|
| date       | 日期          | COPY RAW text, never convert            |
| balance    | 餘額          | COPY number; if "—"/"N/A"/blank → null  |
```

**导致的问题：**
- AI 看到空白的日期列，不知道应该使用哪个日期
- AI 看到空白的余额列，输出 `balance: null`，但实际上应该如何处理？

**示例输出（错误）：**
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": null },
    { "date": "", "description": "ONLINE TRANSFER", "debit": 200.00, "balance": null },
    { "date": "", "description": "POS PURCHASE", "debit": 150.00, "balance": 30018.39 }
  ]
}
```

**期望输出（正确）：**
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": null },
    { "date": "10 Mar", "description": "ONLINE TRANSFER", "debit": 200.00, "balance": null },
    { "date": "10 Mar", "description": "POS PURCHASE", "debit": 150.00, "balance": 30018.39 }
  ]
}
```

---

## 🎯 需要优化的规则

### 1️⃣ 日期填充规则

**新增规则：**
```
📅 DATE HANDLING (SAME-DATE TRANSACTIONS):
- IF current row's Date column is EMPTY/BLANK:
  → Use the date from the PREVIOUS row (carry forward)
- NEVER skip rows with empty dates
- NEVER merge multiple rows into one transaction
```

### 2️⃣ 余额处理规则

**需要明确：**
```
💰 BALANCE HANDLING (MULTI-TRANSACTION DAYS):
- IF current row's Balance column is EMPTY/BLANK/"—":
  → Output balance: null (backend will calculate cumulative balance)
- IF current row's Balance column has a number:
  → Copy that number (this is the final balance for that date)
```

---

## ❓ 向千问 AI 的提问

**我们的问题：**

> 您好，我们在使用 Qwen-VL-Max 提取银行对账单时，遇到一个格式特性问题：
> 
> **场景：** 同一天有多笔交易时，银行只在第1笔显示日期，后续交易的日期列为空；只在最后1笔显示余额，前面的余额列为空。
> 
> **当前问题：** AI 提取时，空白的日期列被输出为 `"date": ""`，导致我们无法判断这笔交易的实际日期。
> 
> **请问：**
> 1. 如何在 Prompt 中明确告诉 AI："如果日期列为空，使用上一行的日期"？
> 2. 这种"向上查找/填充"的逻辑，AI 是否能理解？还是需要特殊的指令格式？
> 3. 是否有更好的表达方式，让 AI 理解"同一组交易"的概念？
> 
> **当前 Prompt 片段：**
> ```
> • "date": copy RAW text from Date column (e.g., "22 Feb", "2025-02-22") → keep as-is. Never convert.
> • "balance": copy number from Balance column. If value is "—", "N/A", blank → null.
> ```
> 
> **期望优化后的规则：**
> - 能够自动填充空白日期列（使用上一笔交易的日期）
> - 明确区分"余额为空"（同日多笔交易的中间行）和"余额缺失"（数据损坏）的情况

---

## 📌 补充信息

### 1. 这是全球银行的通用格式
这不是单一银行的特例，**全球多数银行**都采用这种"日期只显示一次"的紧凑格式，包括：
- 香港：恒生银行、汇丰银行、中国银行
- 中国大陆：工商银行、建设银行
- 欧美：HSBC、Citibank、Bank of America

### 2. 我们的处理策略
- **前端提取：** 尽可能还原完整数据（日期填充）
- **后端计算：** 对于空白余额，通过 `openingBalance + credit - debit` 累加计算

### 3. 输出格式要求
```json
{
  "transactions": [
    { "date": "10 Mar", "description": "...", "debit": 500, "credit": 0, "balance": null },
    { "date": "10 Mar", "description": "...", "debit": 200, "credit": 0, "balance": null },
    { "date": "10 Mar", "description": "...", "debit": 150, "credit": 0, "balance": 30018.39 }
  ]
}
```

**关键点：**
- `date` 必须填充完整（不能为空字符串）
- `balance` 为 `null` 是可接受的（中间交易）
- 每笔交易必须独立一行（不能合并）

---

## 🤔 我们的疑问

1. **Qwen-VL-Max 是否支持"上下文填充"逻辑？**  
   例如："如果当前行的字段为空，使用前一行的值"

2. **应该如何在 Prompt 中表达？**  
   - 使用"IF...THEN..."条件句？
   - 使用"COPY from previous row if current is blank"？
   - 还是需要提供具体示例？

3. **是否建议在 Prompt 中加入示例？**  
   例如：
   ```
   ✅ CORRECT EXAMPLE:
   Row 1: [10 Mar, ATM, 500, 0, null]
   Row 2: [     , POS, 200, 0, 30018.39]  ← Date is blank
   Output: [10 Mar, POS, 200, 0, 30018.39]  ← Use date from Row 1
   ```

---

## 📤 期待的回复

请帮助我们：
1. 提供优化后的 Prompt 规则（完整片段）
2. 说明 AI 是否能理解这种"填充"逻辑
3. 如果不行，建议替代方案（例如：后处理脚本）

非常感谢！🙏

