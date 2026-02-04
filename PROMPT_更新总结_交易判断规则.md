# Prompt 优化总结 - 列识别和交易判断规则

**更新时间：** 2026-02-04  
**问题来源：** 用户反馈（基于实际提取结果）

---

## 📊 用户反馈的问题

### 背景
用户上传了两个银行对账单：
- **图2（ICBC）** → 转换后的内容显示在图1和图6
- **图5（恒生银行）** → 转换后的内容显示在图3和图4

**总体评价：** "这个更新效果不错"

**但有以下问题需要优化：**

### 问题 1：支出/存入判断错误
> "支出／存入时对时错，要仔细一点说明，我们横向扫描后要查看分类"

**分析：**
- AI 在提取时，可能混淆了"支出"列和"存入"列
- 虽然 Prompt 已经有"横向扫描"规则，但**没有明确的列识别规则**
- 需要添加多语言关键词表格，帮助 AI 正确识别"Credit"和"Debit"列

---

### 问题 2：交易判断规则不够清晰
> "只要在支出／收入有数据就是一列，就算没有餘额和日期"

**分析：**
- 当前的验证规则是：`IF date不空 AND balance不空 → 才验证`
- 但实际应该是：**只要有金额（credit 或 debit > 0），就是一笔交易**
- 即使 `date = ""` 和 `balance = null`，也应该提取

**原有规则（有问题）：**
```
✅ VALIDATION CHECK:
- IF "date" is NOT empty AND "balance" is NOT null
  → "description" MUST NOT be empty
  → "credit" OR "debit" MUST have a value
```

**应该的规则：**
```
⚠️ TRANSACTION EXTRACTION RULE:
- IF "credit" > 0 OR "debit" > 0 → 立即提取
- EVEN IF "date" = "" AND "balance" = null
```

---

## ✅ 优化方案

### 1️⃣ **COLUMN IDENTIFICATION（列识别规则）**

添加一个**多语言关键词表格**，帮助 AI 正确识别每一列：

```
🔍 COLUMN IDENTIFICATION (Multi-language Keywords):
Carefully identify each column by its header keywords:

| Column Type | Keywords (ANY of these) | Maps to JSON Field |
|-------------|------------------------|-------------------|
| Date        | "Date", "DATE", "日期", "交易日期", "發生日期", "날짜" | date |
| Description | "Transaction Details", "Particulars", "戶口進支", "摘要", "交易明細", "说明", "적요" | description |
| **CREDIT (存入)** | "Deposit", "DEPOSIT", "Credit", "CREDIT", "貸項", "存入", "收入", "입금" | credit |
| **DEBIT (支出)** | "Withdrawal", "WITHDRAWAL", "Debit", "DEBIT", "借項", "支出", "費用", "지출" | debit |
| Balance     | "Balance", "BALANCE", "餘額", "結餘", "余额", "잔액" | balance |

❗ CRITICAL: 
- "貸項"/"Deposit"/"Credit" → ALWAYS map to "credit" (money IN)
- "借項"/"Withdrawal"/"Debit" → ALWAYS map to "debit" (money OUT)
- DO NOT confuse them. Check column header carefully before extracting.
```

**作用：**
- 明确列出所有可能的列标题关键词（中文、英文、繁体、简体、韩文）
- 明确 "貸項" → credit（存入），"借項" → debit（支出）
- 警告 AI 不要混淆，提取前仔细检查列标题

---

### 2️⃣ **TRANSACTION EXTRACTION RULE（交易提取规则）**

替换原有的验证规则，改为**基于金额的提取规则**：

```
⚠️ TRANSACTION EXTRACTION RULE (MOST CRITICAL):
A row is a VALID TRANSACTION if:
- "credit" > 0 OR "debit" > 0 (at least one has a number)

EVEN IF "date" is empty ("") AND "balance" is null, you MUST extract it as a transaction.

Example:
- Row: "" | "ONLINE TRANSFER" | 200.00 | 0 | null
  → VALID transaction (credit > 0)
- Row: "10 Mar" | "ATM WITHDRAWAL" | 0 | 0 | 79305.59
  → INVALID transaction (no credit or debit) → SKIP

✅ VALIDATION CHECK before outputting each transaction:
- IF "credit" > 0 OR "debit" > 0 → EXTRACT as transaction
- IF both "credit" = 0 AND "debit" = 0 → SKIP (not a transaction)
```

**作用：**
- 明确交易的判断标准：**有金额就提取**
- 支持同日多交易（日期为空的情况）
- 跳过没有金额的行（如小计、总计、标题行）

---

## 📊 更新对比

### 更新前的 Prompt（问题版）

```
✂️ FIELD EXTRACTION RULES:
| date            | 日期          | COPY RAW text. If empty → ""            |
| description     | 戶口進支/摘要  | COPY ALL visible text from THIS row     |
| credit          | 貸項/存入      | COPY number or 0. Remove commas         |
| debit           | 借項/支出      | COPY number or 0. Remove commas         |
| balance         | 餘額          | COPY number (remove commas). If blank → null |

✅ VALIDATION CHECK:
- IF "date" is NOT empty AND "balance" is NOT null
  → "description" MUST NOT be empty/blank
  → "credit" OR "debit" MUST have a value
```

**问题：**
- ❌ 没有列识别规则（AI可能混淆"支出"和"存入"）
- ❌ 验证规则基于 `date` 和 `balance`，而不是 `credit` 和 `debit`
- ❌ 可能跳过有金额但无日期的行

---

### 更新后的 Prompt（优化版）

```
🔍 COLUMN IDENTIFICATION (Multi-language Keywords):
| Column Type | Keywords (ANY of these) | Maps to JSON Field |
|-------------|------------------------|-------------------|
| **CREDIT (存入)** | "Deposit", "DEPOSIT", "Credit", "CREDIT", "貸項", "存入", "收入" | credit |
| **DEBIT (支出)** | "Withdrawal", "WITHDRAWAL", "Debit", "DEBIT", "借項", "支出", "費用" | debit |

❗ CRITICAL: 
- "貸項"/"Deposit"/"Credit" → ALWAYS map to "credit" (money IN)
- "借項"/"Withdrawal"/"Debit" → ALWAYS map to "debit" (money OUT)

✂️ FIELD EXTRACTION RULES:
(same as before)

⚠️ TRANSACTION EXTRACTION RULE (MOST CRITICAL):
A row is a VALID TRANSACTION if:
- "credit" > 0 OR "debit" > 0 (at least one has a number)

EVEN IF "date" is empty ("") AND "balance" is null, you MUST extract it as a transaction.

✅ VALIDATION CHECK:
- IF "credit" > 0 OR "debit" > 0 → EXTRACT as transaction
- IF both "credit" = 0 AND "debit" = 0 → SKIP (not a transaction)
```

**改进：**
- ✅ 添加列识别规则（多语言关键词表格）
- ✅ 明确 "貸項" = credit，"借項" = debit
- ✅ 验证规则基于 `credit` 和 `debit`（有金额就提取）
- ✅ 支持无日期和无余额的行

---

## 🎯 预期效果

### 1. 解决支出/存入混淆问题

**场景：** ICBC 对账单，列标题为"借項"和"貸項"

**之前：** AI 可能混淆，把"借項"当作 credit
**现在：** AI 会查看列标题，正确识别：
- "借項" → debit（支出）
- "貸項" → credit（存入）

---

### 2. 正确提取所有有金额的行

**场景：** 同一天有多笔交易，日期只显示一次

**PDF 内容：**
```
10 Mar | ATM WITHDRAWAL | 500.00 | 79,305.59
       | ONLINE TRANSFER | 200.00 | 79,105.59
       | POS PURCHASE | 150.00 | 78,955.59
```

**之前（错误）：**
```json
{
  "transactions": [
    {"date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": 79305.59}
    // ❌ 后两笔被跳过（因为没有 date 和 balance）
  ]
}
```

**现在（正确）：**
```json
{
  "transactions": [
    {"date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": 79305.59},
    {"date": "", "description": "ONLINE TRANSFER", "debit": 200.00, "balance": 79105.59},
    {"date": "", "description": "POS PURCHASE", "debit": 150.00, "balance": 78955.59}
  ]
}
```

然后 `postProcessTransactions` 会填充空白日期：
```json
{
  "transactions": [
    {"date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": 79305.59},
    {"date": "10 Mar", "description": "ONLINE TRANSFER", "debit": 200.00, "balance": 79105.59},
    {"date": "10 Mar", "description": "POS PURCHASE", "debit": 150.00, "balance": 78955.59}
  ]
}
```

---

### 3. 自动跳过无金额的行

**场景：** 表格中有小计、总计、空行

**PDF 内容：**
```
10 Mar | ATM WITHDRAWAL | 500.00 | 79,305.59
       | --- Sub-total --- |  |  
11 Mar | CREDIT INTEREST | 2.61 | 79,308.20
```

**提取结果：**
```json
{
  "transactions": [
    {"date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500.00, "balance": 79305.59},
    // ✅ "Sub-total" 被跳过（credit=0, debit=0）
    {"date": "11 Mar", "description": "CREDIT INTEREST", "credit": 2.61, "balance": 79308.20}
  ]
}
```

---

## 📝 技术细节

### 更新的文件
- `/Users/cavlinyeung/ai-bank-parser/qwen-vl-max-processor.js`
  - `generatePrompt(documentType)` - 单页 Prompt
  - `generateMultiPagePrompt(documentType, pageCount)` - 多页 Prompt

### Git Commit
```
✅ 优化Prompt：列识别和交易判断规则

用户反馈优化点：
1. 支出/存入判断错误 → 需要更明确的列识别规则
2. 交易判断规则不清晰 → 应该是"有金额就提取"

核心优化（2个新规则）：

1️⃣ COLUMN IDENTIFICATION（列识别规则）
- 添加多语言关键词表格
- 明确 "貸項"→credit, "借項"→debit

2️⃣ TRANSACTION EXTRACTION RULE（交易提取规则）
- IF credit > 0 OR debit > 0 → 立即提取
- EVEN IF date="" AND balance=null
```

---

## 🧪 测试建议

### 1. ICBC 对账单（图2）
- ✅ 检查"借項"是否正确映射到 debit
- ✅ 检查"貸項"是否正确映射到 credit
- ✅ 检查所有有金额的行是否都被提取

### 2. 恒生银行对账单（图5）
- ✅ 检查同日多交易是否全部提取
- ✅ 检查日期为空的行是否被提取
- ✅ 检查余额为空的行是否被提取

### 3. 边缘情况
- ✅ 小计行（credit=0, debit=0）是否被跳过
- ✅ 空行是否被跳过
- ✅ 标题行是否被跳过

---

## 🔗 相关文档

- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_列对齐优化.md` - 上一次优化（列对齐和横向扫描）
- `/Users/cavlinyeung/ai-bank-parser/CURRENT_WORKFLOW_EXPLANATION.md` - 完整工作流程

---

## ✅ 总结

这次优化的核心是**基于金额的交易判断**，而不是基于日期和余额：

### 关键变化
1. **列识别规则** - 添加多语言关键词表格，明确"支出"和"存入"的映射
2. **交易判断规则** - 从"有 date 和 balance 才验证"改为"有金额就提取"

### 预期结果
- ✅ 解决支出/存入混淆问题
- ✅ 确保所有有金额的交易都被提取
- ✅ 支持同日多交易（日期为空的情况）
- ✅ 自动跳过无金额的行（小计、总计、空行）

### 与上一次优化的关系
- **上一次（列对齐优化）：** 解决 AI 跳过中间列的问题（横向扫描）
- **这一次（交易判断优化）：** 解决 AI 判断哪些行是交易的问题（基于金额）

两者结合，形成完整的提取逻辑：
1. **横向扫描** - 确保从左到右读取所有列
2. **基于金额判断** - 确保所有有金额的行都被提取
