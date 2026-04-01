# Prompt 重大优化 - TABLE-AS-EXCEL 模式

**更新时间：** 2026-02-04  
**问题来源：** 用户反馈（基于实际提取结果）

---

## 🚨 用户反馈的问题

用户上传了两个银行对账单：
- **图1图2（恒生银行）** - 部分有金额的行被遗漏
- **图3图4（ICBC）** - "借項"和"貸項"还是混淆

**用户的关键提问：**
> "所以有什麼更好的方法要求他完成？**假設他是excel？**你有什麼建議？"

---

## 💡 核心洞察：从 OCR 模式 → EXCEL 模式

### 之前的方法（OCR 模式）
- AI 被当作"文本阅读器"
- 需要 AI 自己判断哪一列是"貸項"，哪一列是"借項"
- 容易混淆，因为不同银行的列顺序不同

### 新方法（EXCEL 模式）
- AI 被当作"Excel 数据处理器"
- **先读取表头**，确定列映射关系
- **再逐行提取**，按列索引读取数据
- 就像人类使用 Excel 一样：先看列名，再读数据

---

## 🎯 新方案：3步骤流程

### STEP 1: LOCATE TABLE（定位表格）
```
- FIND table with header row containing BOTH: "戶口進支" AND "餘額"
- IGNORE any section with: "戶口摘要" / "Account Summary" / "總計" / "TOTAL"
```

**作用：** 找到正确的交易明细表

---

### STEP 2: READ HEADER ROW（读取表头）
```
READ each column header from left to right and determine:
- Which column contains: "Date" / "日期" → Column A (date)
- Which column contains: "Transaction Details" / "戶口進支" → Column B (description)
- Which column contains: "Deposit" / "貸項" / "Credit" → Column C or D (THIS IS CREDIT)
- Which column contains: "Withdrawal" / "借項" / "Debit" → Column C or D (THIS IS DEBIT)
- Which column contains: "Balance" / "餘額" → Column E (balance)

⚠️ CRITICAL COLUMN MAPPING:
You MUST determine the EXACT position of Credit and Debit columns:
- If header row shows: "日期 | 戶口進支 | 貸項 | 借項 | 餘額"
  → Column mapping: A=date, B=description, C=credit, D=debit, E=balance
- If header row shows: "Date | Particulars | Withdrawal | Deposit | Balance"
  → Column mapping: A=date, B=description, C=debit, D=credit, E=balance
```

**作用：** 
- 像 Excel 一样，先确定每一列的含义
- 明确哪一列是 credit，哪一列是 debit
- 防止混淆

---

### STEP 3: PROCESS LIKE EXCEL（像 Excel 一样处理）
```
Starting from the FIRST data row (after header), process EACH row like reading an Excel spreadsheet:

FOR EACH ROW (Row 2, Row 3, Row 4, ...):
  1. Read cell in Column A (Date column) → extract "date"
  2. Read cell in Column B (Description column) → extract "description"
  3. Read cell in Column C:
     - IF Column C header = "貸項"/"Deposit"/"Credit" → extract to "credit"
     - IF Column C header = "借項"/"Withdrawal"/"Debit" → extract to "debit"
  4. Read cell in Column D:
     - IF Column D header = "貸項"/"Deposit"/"Credit" → extract to "credit"
     - IF Column D header = "借項"/"Withdrawal"/"Debit" → extract to "debit"
  5. Read cell in Column E (Balance column) → extract "balance"
  
  6. TRANSACTION VALIDATION:
     - IF "credit" > 0 OR "debit" > 0 → OUTPUT this row as a transaction
     - IF both "credit" = 0 AND "debit" = 0 → SKIP (not a transaction)
```

**作用：**
- 逐行读取，像 Excel 一样
- 根据 STEP 2 的列映射，正确提取 credit 和 debit
- 有金额就提取，无金额就跳过

---

## 📊 与之前方法的对比

### 之前的 OCR 模式（有问题）

**Prompt 结构：**
```
1. 找到表格
2. 识别列（通过关键词："貸項" = credit, "借項" = debit）
3. 逐行提取
```

**问题：**
- ❌ AI 在提取时，可能不记得哪一列是什么
- ❌ 不同银行列顺序不同，AI 容易混淆
- ❌ 没有明确的"先读表头，再读数据"流程

**例子（ICBC）：**
```
表头：日期 | 戶口進支 | 貸項 | 借項 | 餘額
数据：2022/02/04 | SCR OCTOPUS | 8,122.80 | 0 | 38,841.19
```

**AI 的错误行为：**
- 看到 8,122.80，但不确定这是在"貸項"列还是"借項"列
- 可能把 8,122.80 错误地映射到 debit

---

### 现在的 EXCEL 模式（优化版）

**Prompt 结构：**
```
STEP 1: 找到表格
STEP 2: 读取表头，确定列映射
  - Column A = 日期
  - Column B = 戶口進支
  - Column C = 貸項（THIS IS CREDIT）
  - Column D = 借項（THIS IS DEBIT）
  - Column E = 餘額
STEP 3: 逐行提取，按列索引读取
  - Row 2, Column C = 8,122.80 → credit (因为 Column C = 貸項)
```

**优点：**
- ✅ AI 明确知道 Column C 是 credit，Column D 是 debit
- ✅ 提取时按列索引读取，不会混淆
- ✅ 像人类使用 Excel 一样：先看列名，再读数据

**例子（ICBC）：**
```
STEP 2: 读取表头
- Column C header = "貸項" → Column C = credit
- Column D header = "借項" → Column D = debit

STEP 3: 读取数据
- Row 2, Column C = 8,122.80 → credit = 8122.80
- Row 2, Column D = 0 → debit = 0
```

---

## 🎯 关键改进

### 1. **明确的列映射流程**
**之前：** 在提取时判断列
**现在：** 先读表头，确定列映射，再提取数据

### 2. **EXCEL 思维模式**
**之前：** "读取'貸項'列的值"（模糊）
**现在：** "读取 Column C 的值，Column C = credit"（明确）

### 3. **防止混淆的机制**
```
❗ BEFORE extracting ANY data, you MUST know:
- "貸項" is in column ___ → THIS IS CREDIT (money IN)
- "借項" is in column ___ → THIS IS DEBIT (money OUT)
```

### 4. **逐行扫描，有金额就提取**
```
FOR EACH ROW:
  IF "credit" > 0 OR "debit" > 0 → OUTPUT
  IF both = 0 → SKIP
```

---

## 🔧 实际例子

### 例子 1：ICBC（列顺序：貸項 → 借項）

**表头：**
```
| 日期       | 戶口進支             | 貸項     | 借項   | 餘額      |
```

**STEP 2（列映射）：**
```
- Column A = 日期
- Column B = 戶口進支
- Column C = 貸項 → THIS IS CREDIT
- Column D = 借項 → THIS IS DEBIT
- Column E = 餘額
```

**STEP 3（数据行）：**
```
| 2022/02/04 | SCR OCTOPUS CARDS LTD | 8,122.80 | 0 | 38,841.19 |
```

**提取结果：**
```json
{
  "date": "2022/02/04",
  "description": "SCR OCTOPUS CARDS LTD",
  "credit": 8122.80,  // ← 从 Column C 提取
  "debit": 0,         // ← 从 Column D 提取
  "balance": 38841.19
}
```

---

### 例子 2：恒生银行（列顺序：Withdrawal → Deposit）

**表头：**
```
| Date  | Transaction Details         | Withdrawal | Deposit | Balance     |
```

**STEP 2（列映射）：**
```
- Column A = Date
- Column B = Transaction Details
- Column C = Withdrawal → THIS IS DEBIT
- Column D = Deposit → THIS IS CREDIT
- Column E = Balance
```

**STEP 3（数据行）：**
```
| 7 Mar | QUICK CHEQUE DEPOSIT (07MAR25) | 0 | 78,649.00 | 80,145.59 |
```

**提取结果：**
```json
{
  "date": "7 Mar",
  "description": "QUICK CHEQUE DEPOSIT (07MAR25)",
  "credit": 78649.00,  // ← 从 Column D 提取（因为 Column D = Deposit）
  "debit": 0,          // ← 从 Column C 提取（因为 Column C = Withdrawal）
  "balance": 80145.59
}
```

---

## ✅ 预期效果

### 1. 解决 ICBC 的"貸項"和"借項"混淆问题
- **之前：** AI 不确定 8,122.80 是在哪一列
- **现在：** AI 先读表头，知道 Column C = "貸項" = credit，所以 8,122.80 → credit

### 2. 确保所有有金额的行都被提取
- **之前：** AI 可能跳过某些行
- **现在：** 逐行扫描，只要 credit > 0 或 debit > 0，就提取

### 3. 更像人类使用 Excel 的思维
- **Step 1:** 找到表格
- **Step 2:** 看表头，知道每一列是什么
- **Step 3:** 逐行读取数据

---

## 📝 技术细节

### 更新的文件
- `/Users/cavlinyeung/ai-bank-parser/qwen-vl-max-processor.js`
  - `generatePrompt(documentType)` - 单页 Prompt
  - `generateMultiPagePrompt(documentType, pageCount)` - 多页 Prompt

### Git Commit
```
🔥 重大优化：TABLE-AS-EXCEL 模式

核心改变：从 OCR 模式 → EXCEL 模式

STEP 1: LOCATE TABLE（定位表格）
STEP 2: READ HEADER ROW（读取表头，确定列映射）
STEP 3: PROCESS LIKE EXCEL（像 Excel 一样逐行处理）

预期效果：
- ✅ ICBC 的"貸項"和"借項"不会混淆（因为先读表头）
- ✅ 所有有金额的行都会被提取（因为逐行扫描）
```

---

## 🧪 测试建议

### 1. ICBC 对账单（图3图4）
- ✅ 检查"貸項"是否正确映射到 credit
- ✅ 检查"借項"是否正确映射到 debit
- ✅ 检查金额是否准确

### 2. 恒生银行对账单（图1图2）
- ✅ 检查所有有金额的行是否都被提取
- ✅ 检查"Withdrawal"是否正确映射到 debit
- ✅ 检查"Deposit"是否正确映射到 credit

### 3. 同日多交易
- ✅ 检查日期为空的行是否被提取
- ✅ 检查 `postProcessTransactions` 是否正确填充日期

---

## 📚 相关文档

- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_交易判断规则.md` - 上一次优化（交易判断规则）
- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_列对齐优化.md` - 列对齐和横向扫描
- `/Users/cavlinyeung/ai-bank-parser/CURRENT_WORKFLOW_EXPLANATION.md` - 完整工作流程

---

## ✅ 总结

这次优化的核心是 **"假设他是 Excel"**（用户的建议）：

### 关键变化
1. **从 OCR 模式 → EXCEL 模式**
2. **3步骤流程：** 定位表格 → 读取表头 → 逐行处理
3. **先确定列映射，再提取数据**

### 预期结果
- ✅ 解决 ICBC 的"貸項"和"借項"混淆问题
- ✅ 确保所有有金额的行都被提取
- ✅ 更像人类使用 Excel 的思维方式

### 与之前优化的关系
- **第1次（列对齐优化）：** 解决 AI 跳过中间列的问题
- **第2次（交易判断优化）：** 解决 AI 判断哪些行是交易的问题
- **第3次（TABLE-AS-EXCEL）：** 解决 AI 混淆列映射的问题 ← 当前

三次优化，层层递进，最终形成完整的 EXCEL 模式提取逻辑。
