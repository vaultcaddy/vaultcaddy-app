# Prompt 优化总结 - 列对齐和横向扫描规则

**更新时间：** 2026-02-04  
**问题来源：** 用户反馈恒生银行 7 Mar 行数据提取不完整

---

## 🔍 问题诊断

### 实际问题
用户上传的恒生银行对账单（7 Mar 行）：

**PDF 原始内容：**
```
7 Mar | QUICK CHEQUE DEPOSIT (07MAR25) | 78,649.00 | 80,145.59
```

**AI 提取结果（问题）：**
```json
{
  "date": "7 Mar",
  "description": "—",           // ❌ 遗漏
  "credit": 0.00,                // ❌ 遗漏
  "balance": 80145.59            // ✅ 正确
}
```

**应该的提取结果：**
```json
{
  "date": "7 Mar",
  "description": "QUICK CHEQUE DEPOSIT (07MAR25)",
  "credit": 78649.00,
  "balance": 80145.59
}
```

---

## 🧠 根因分析

### AI 的错误行为
AI 在读取表格时，虽然能看到 `7 Mar` 和 `80,145.59`，但**没有正确识别中间列的边界**，导致：

1. ✅ 识别到 `Date` 列的 `7 Mar`
2. ❌ **跳过** `Description` 列
3. ❌ **跳过** `Credit` 列
4. ✅ 跳到 `Balance` 列的 `80,145.59`
5. ❌ 把被跳过的内容错误地归类到下一行

### 原有 Prompt 的缺陷
- ✅ AI 知道要提取 `date`, `description`, `credit`, `debit`, `balance`
- ❌ AI **不知道**这些字段必须来自 **同一视觉行**
- ❌ AI **不知道**要从左到右**完整读取**该行的所有列
- ❌ AI **不知道**跳过列会导致数据丢失

---

## ✅ 解决方案：3 个新规则

### 1️⃣ ROW INTEGRITY RULE（行完整性规则）

```
⚠️ CRITICAL ROW INTEGRITY RULE:
ALL fields (date, description, credit, debit, balance) for ONE transaction 
MUST come from the SAME VISUAL ROW in the table.
```

**作用：**
- 强制 AI 从同一视觉行提取所有字段
- 禁止跨行提取
- 禁止把某行的字段和另一行的字段混合

---

### 2️⃣ EXTRACTION ORDER（横向扫描指令）

```
📍 EXTRACTION ORDER (left-to-right, DO NOT skip columns):
For EACH ROW:
1. Read Date column (leftmost) → extract "date"
2. Read Description column (middle) → extract "description" (ALL visible text in this column)
3. Read Credit/Deposit column → extract "credit"
4. Read Debit/Withdrawal column → extract "debit"
5. Read Balance column (rightmost) → extract "balance"
6. Move to NEXT ROW and repeat

❗ NEVER read Date → skip middle columns → jump to Balance. This causes data loss.
```

**作用：**
- 明确从左到右的扫描顺序
- 禁止跳过中间列
- 确保每一列都被读取

---

### 3️⃣ VALIDATION CHECK（验证检查）

```
✅ VALIDATION CHECK before outputting each transaction:
- IF "date" is NOT empty AND "balance" is NOT null
  → "description" MUST NOT be empty/blank
  → "credit" OR "debit" MUST have a value (at least one must be > 0)
- IF above check fails → RE-READ that visual row from left to right completely
```

**作用：**
- 在输出前进行逻辑验证
- 如果有日期和余额，必须有描述和金额
- 如果验证失败，要求 AI 重新读取该行

---

## 📊 更新对比

### 更新前的 Prompt（简化版）
```
✂️ FIELD EXTRACTION RULES (NON-NEGOTIABLE):
| JSON Field | Source Column | Action                                  |
|------------|---------------|-----------------------------------------|
| balance    | 餘額          | COPY EXACT NUMBER (remove commas)       |
| debit      | 借項          | COPY number or 0                        |
| credit     | 貸項          | COPY number or 0                        |

❗ ABSOLUTE COMMANDS:
- IF number unclear → output null (NEVER guess/calculate)
- REMOVE all commas from numbers before outputting
```

**问题：**
- 没有明确"同一行"的概念
- 没有规定读取顺序
- 没有验证机制

---

### 更新后的 Prompt（优化版）
```
⚠️ CRITICAL ROW INTEGRITY RULE:
ALL fields (date, description, credit, debit, balance) for ONE transaction 
MUST come from the SAME VISUAL ROW in the table.

📍 EXTRACTION ORDER (left-to-right, DO NOT skip columns):
For EACH ROW:
1. Read Date column (leftmost) → extract "date"
2. Read Description column (middle) → extract "description" (ALL visible text)
3. Read Credit/Deposit column → extract "credit"
4. Read Debit/Withdrawal column → extract "debit"
5. Read Balance column (rightmost) → extract "balance"
6. Move to NEXT ROW and repeat

❗ NEVER read Date → skip middle columns → jump to Balance. This causes data loss.

✂️ FIELD EXTRACTION RULES (NON-NEGOTIABLE):
| JSON Field      | Source Column | Action                                  | Forbidden               |
|-----------------|---------------|-----------------------------------------|-------------------------|
| date            | 日期          | COPY RAW text. If empty → ""            | —                       |
| description     | 戶口進支/摘要  | COPY ALL visible text from THIS row     | Skipping, merging       |
| credit          | 貸項/存入      | COPY number or 0. Remove commas         | —                       |
| debit           | 借項/支出      | COPY number or 0. Remove commas         | —                       |
| balance         | 餘額          | COPY number (remove commas). If blank/"—"/"N/A" → null | —   |

✅ VALIDATION CHECK before outputting each transaction:
- IF "date" is NOT empty AND "balance" is NOT null
  → "description" MUST NOT be empty/blank
  → "credit" OR "debit" MUST have a value (at least one must be > 0)
- IF above check fails → RE-READ that visual row from left to right completely
```

**改进：**
- ✅ 明确"同一视觉行"概念
- ✅ 规定从左到右的读取顺序
- ✅ 禁止跳过列
- ✅ 添加输出前验证
- ✅ 添加错误自我修正机制

---

## 🎯 预期效果

### 1. 解决恒生银行列对齐问题
**之前：**
```json
{
  "date": "7 Mar",
  "description": "—",
  "credit": 0.00,
  "balance": 80145.59
}
```

**现在：**
```json
{
  "date": "7 Mar",
  "description": "QUICK CHEQUE DEPOSIT (07MAR25)",
  "credit": 78649.00,
  "balance": 80145.59
}
```

### 2. 保持 ICBC 兼容性
- ✅ 原有的 "OCR COPY MACHINE" 模式不变
- ✅ 原有的字段提取规则不变
- ✅ 只是增加了"行完整性"和"横向扫描"的约束

### 3. 提高多行描述合并的准确性
对于 10 Mar 的多行描述（用户之前提到的问题）：
```
10 Mar  4006-1210-0627-0086
        N31098558858(10MAR25)  21,226.59
```

**新的 Prompt 会：**
- 识别到第一行（10 Mar）没有金额，会自动合并描述
- 识别到第二行有金额（21,226.59），标记为交易结束
- 输出合并后的结果：
```json
{
  "date": "10 Mar",
  "description": "4006-1210-0627-0086 N31098558858(10MAR25)",
  "debit": 21226.59,
  "balance": null
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
✅ 优化Prompt：添加列对齐和横向扫描规则

问题诊断：
- 用户发现 7 Mar 行的提取结果：
  ✅ AI能看到 '7 Mar' 和 '80,145.59'
  ❌ 但遗漏中间的 'QUICK CHEQUE DEPOSIT' 和 '78,649.00'
  ❌ 说明 AI 跳过了中间列，直接从日期跳到余额

核心优化（3个新规则）：

1️⃣ ROW INTEGRITY RULE（行完整性）
- 强制 AI 从同一视觉行提取所有字段
- 禁止跨行提取

2️⃣ EXTRACTION ORDER（横向扫描）
- 明确从左到右顺序：Date → Description → Credit → Debit → Balance
- 禁止跳过中间列（NEVER skip columns）

3️⃣ VALIDATION CHECK（验证检查）
- 如果有 date 和 balance，必须有 description
- 如果验证失败，要求 RE-READ 该行
```

---

## 🧪 测试建议

### 1. 恒生银行对账单测试
- ✅ 重新上传之前有问题的 PDF
- ✅ 检查 7 Mar 行是否完整提取
- ✅ 检查 10 Mar 的多行描述是否正确合并

### 2. ICBC 对账单回归测试
- ✅ 确保之前正确的 ICBC 提取仍然正确
- ✅ 确保新规则不会破坏原有逻辑

### 3. 边缘情况测试
- ✅ 同一天多笔交易（日期为空）
- ✅ 描述为空的交易
- ✅ 余额为 null 的交易

---

## 📚 相关文档

- `/Users/cavlinyeung/ai-bank-parser/CURRENT_WORKFLOW_EXPLANATION.md` - 完整工作流程
- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_金额判断.md` - 之前的 Prompt 优化（已回退）
- `/Users/cavlinyeung/ai-bank-parser/SAME_DATE_SOLUTION.md` - 同日多交易问题分析

---

## ✅ 总结

这次优化的核心是**解决 AI 的列对齐问题**，通过添加 3 个新规则：
1. **行完整性规则** - 确保所有字段来自同一行
2. **横向扫描指令** - 确保从左到右不跳过列
3. **验证检查** - 确保输出的逻辑一致性

这些规则不改变原有的 "OCR COPY MACHINE" 哲学，只是增加了**空间约束**（同一行）和**顺序约束**（从左到右），使 AI 更像人类一样阅读表格。

**预期结果：**
- ✅ 解决恒生银行 7 Mar 行的数据丢失问题
- ✅ 保持 ICBC 对账单的提取准确性
- ✅ 提高多行描述合并的准确性
