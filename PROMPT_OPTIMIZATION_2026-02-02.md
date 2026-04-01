# Prompt 优化记录 - 2026-02-02

## 📊 问题背景

### 恒生银行对账单提取错误
- **错误**：承上结余 30,718.39 → **正确**：1,493.98
- **错误**：7 Mar 存入 76,849.00 → **正确**：78,649.00

### 根本原因
1. **看错表格**：AI 读取了 ACCOUNT SUMMARY 而非 TRANSACTION HISTORY
2. **行对齐错误**：从不同行提取了数据

---

## 🔧 优化方案（来自通义千问）

### 1. **更严格的表格识别规则**

**之前：**
```
- FIND table with header containing BOTH: "戶口進支" AND "餘額"
- IGNORE any section with "戶口摘要" / "Account Summary"
```

**优化后：**
```
📍 STEP 1: LOCATE THE TRANSACTION TABLE (NON-NEGOTIABLE)
Find the table that satisfies ALL of these visual conditions:
• Contains a column with header containing ANY of: "Date", "DATE", "日期"
• Contains a column with header containing ANY of: "Balance", "BALANCE", "餘額"
• Contains AT LEAST ONE of: "Deposit", "DEPOSIT", "存入", "Credit"
• Contains AT LEAST ONE of: "Withdrawal", "WITHDRAWAL", "支出", "Debit"
• Has ≥ 3 rows with visible dates in chronological order
• Is NOT inside any box/section titled: "Account Summary", "戶口摘要", "TOTAL"

❗ If multiple tables match, choose the one with MOST date rows AND located LOWEST on the page.
```

**改进点：**
- ✅ 明确要求必须有 Date 列（ACCOUNT SUMMARY 没有）
- ✅ 明确要求 ≥3 行日期且按时间顺序
- ✅ 如果有多个表格，选择日期行最多且位置最低的

---

### 2. **更详细的字段提取规则**

**之前：**
```
| balance  | 餘額 | COPY EXACT NUMBER |
| debit    | 借項 | COPY number or 0  |
| credit   | 貸項 | COPY number or 0  |
```

**优化后：**
```
📍 STEP 2: EXTRACT FIELDS — STRICTLY FROM SAME ROW
For EACH ROW in the identified table:
• "date": copy RAW text (e.g., "22 Feb") → keep as-is. Never convert.
• "description": copy ALL visible text (e.g., "BF BALANCE", "ATM WITHDRAWAL")
• "credit": copy number from Deposit/Credit column. If empty → 0. Remove commas. Keep decimals.
• "debit": copy number from Withdrawal/Debit column. If empty → 0. Remove commas. Keep decimals.
• "balance": copy number from Balance column. Remove commas. If value is "—" → null.
```

**改进点：**
- ✅ 明确每个字段的来源列
- ✅ 详细说明如何处理空值、逗号、"DR" 标记
- ✅ 强调所有字段必须来自同一行

---

### 3. **明确的期初/期末余额规则**

**之前：**
```
- FIRST row = "承上結餘" → openingBalance
- LAST row = "結轉結餘" → closingBalance
```

**优化后：**
```
📍 STEP 3: DETERMINE OPENING & CLOSING
• "openingBalance" = "balance" value from FIRST row of this table  
• "closingBalance" = "balance" value from LAST row of this table  
• DO NOT use any other section (e.g., Account Summary) for these values.
```

**改进点：**
- ✅ 明确禁止使用 Account Summary 的值
- ✅ 简化规则，直接取首行和末行

---

### 4. **更强的禁止规则**

**之前：**
```
- NEVER calculate
- IF number unclear → null
```

**优化后：**
```
❗ ABSOLUTE RULES:
• NEVER calculate balance. NEVER compare rows. NEVER infer meaning of "DR"/"CR".
• If a number has comma → remove it before output (e.g., "30,718.39" → 30718.39).
• If field is occluded, blurred, or ambiguous → output null (NOT 0, NOT guess).
• Output ONLY valid JSON. NO explanations. NO markdown. NO comments. NO extra keys.
```

**改进点：**
- ✅ 禁止比较行（避免推断）
- ✅ 禁止推断 DR/CR 含义（直接复制）
- ✅ 明确"不清楚"应输出 null 而非 0

---

## 📈 预期效果

### 解决的问题：
1. ✅ **看错表格**：通过 Date 列验证，确保找到 TRANSACTION HISTORY
2. ✅ **行对齐错误**：明确所有字段必须来自同一行
3. ✅ **数值错误**：详细的数字处理规则（逗号、DR、空值）

### 测试用例：
- 恒生银行对账单（多表格，容易混淆）
- 中国工商银行对账单（之前成功的案例）
- 其他香港本地银行对账单

---

## 📝 技术细节

### Prompt 长度变化：
- **之前**：~70 行
- **优化后**：~60 行（更简洁但更精确）

### 关键改进点：
1. **视觉特征识别**：通过列标题（Date, Balance, Deposit, Withdrawal）
2. **位置规则**：选择日期行最多且位置最低的表格
3. **数据验证**：日期必须按时间顺序（≥3 行）
4. **严格禁止**：禁止计算、比较、推断

---

## 🚀 下一步

1. **重新上传恒生银行对账单测试**
2. **验证其他银行对账单**
3. **如果仍有错误，提供新的案例**

---

## 📌 备注

- 这个 Prompt 是基于通义千问 AI 的专业建议优化的
- 核心思想：从"通用规则"改为"视觉特征识别"
- 重点：AI 应该像人一样"看"表格（找 Date 列、看位置、数日期行）

