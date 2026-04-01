# 银行单提取实验 Prompt 方案集

**目标银行：** 恒生银行（Hang Seng）+ 工商银行亚洲（ICBC）  
**核心规则：** 只要有支出/收入就是1个交易，不进行任何计算  
**创建日期：** 2026-02-06

---

## 方案一：EXCEL TABLE MODE（表格读取模式）

### 🎯 核心思路

把银行单当作 Excel 表格来处理：
1. 第一步：识别表格列标题（Header Row）
2. 第二步：建立列索引映射（Column Index Mapping）
3. 第三步：逐行读取，严格按列位置提取数据

### 📜 完整 Prompt

```
🔷 EXCEL TABLE EXTRACTION MODE

You are an Excel table reader. Your job is to extract transaction data from a bank statement table AS IF it were an Excel spreadsheet.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 STEP 1: LOCATE THE TRANSACTION TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Find the table that contains transaction history. It must have:
• A header row with column names
• At least 3 of these keywords: ["Date"|"日期"], ["Description"|"摘要"|"Transaction Details"], ["Debit"|"支出"|"Withdrawal"], ["Credit"|"存入"|"Deposit"], ["Balance"|"結存"|"餘額"]

Skip any section titled: "Summary", "Total", "摘要", "總計"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 STEP 2: MAP COLUMN INDICES (LIKE EXCEL COLUMNS A, B, C...)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Identify the column position for each field. Example:

| Column A | Column B              | Column C | Column D   | Column E  | Column F |
|----------|-----------------------|----------|------------|-----------|----------|
| Date     | Transaction Details   | Currency | Deposit    | Withdrawal| Balance  |
| 日期     | 摘要                  | 货币     | 存入       | 支出      | 結存     |

Create a mental map:
- dateColumn = Column A
- descriptionColumn = Column B
- currencyColumn = Column C (if exists)
- creditColumn = Column D
- debitColumn = Column E
- balanceColumn = Column F

⚠️ CRITICAL: Different banks may have different column orders. Map columns based on header text, NOT position.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 STEP 3: ROW-BY-ROW EXTRACTION (LIKE READING EXCEL ROWS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For EACH row in the table (starting from row below header):

1. Read Cell in dateColumn → "date"
2. Read Cell in descriptionColumn → "description"
3. Read Cell in creditColumn → "credit"
4. Read Cell in debitColumn → "debit"
5. Read Cell in balanceColumn → "balance"

🎯 TRANSACTION RULE (CRITICAL):
A row is a valid transaction IF:
• creditColumn has a number (e.g., 1500.00, 78649, 2.61)
  OR
• debitColumn has a number (e.g., 500.00, 21226.59)

→ Extract this row as ONE transaction object

Skip row ONLY IF:
• Both creditColumn = blank/0 AND debitColumn = blank/0
• Row contains "TOTAL", "SUMMARY", "承上結餘", "結轉下頁"

🔄 DATE INHERITANCE RULE:
• Track the last valid date as you process rows
• If current row's dateColumn is blank → use the last valid date
• Update lastValidDate whenever you see a non-blank date in dateColumn

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️ EXTRACTION RULES (NON-NEGOTIABLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Field       | Action                                                                 |
|-------------|------------------------------------------------------------------------|
| date        | Copy text from dateColumn. If blank → use PREVIOUS transaction's date |
| description | Copy ALL text from descriptionColumn of THIS ROW ONLY                  |
| credit      | Copy number from creditColumn (remove commas). If blank → 0            |
| debit       | Copy number from debitColumn (remove commas). If blank → 0             |
| balance     | Copy number from balanceColumn (remove commas). If blank/"—" → null    |

❗ ABSOLUTE RULES:
- EACH PHYSICAL ROW = ONE transaction object (if credit OR debit has value)
- NEVER merge rows (even if date is blank)
- NEVER skip a row because date column is empty
- NEVER calculate balance (ONLY copy visible numbers)
- If date is blank, inherit date from PREVIOUS transaction in your output
- Remove ALL commas from numbers before outputting (e.g., "1,500.00" → 1500.00)
- Date format: Output original string UNCHANGED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 OUTPUT STRUCTURE (STRICT JSON)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{
  "bankName": "string (exact bank name from document)",
  "accountNumber": "string (exact account number)",
  "accountHolder": "string (account holder name or \"\")",
  "currency": "string (HKD/USD/CNY/etc.)",
  "statementPeriod": "string (statement period or date)",
  "openingBalance": number (first row's balance if available, else null),
  "closingBalance": number (last row's balance if available, else null),
  "transactions": [
    {
      "date": "string (original format or \"\")",
      "description": "string (full text from description column)",
      "debit": number (0 if blank),
      "credit": number (0 if blank),
      "balance": number (null if blank)
    }
  ]
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXAMPLE MAPPING: ICBC ASIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Header Row:
| 日期       | 摘要                | 货币 | 支出      | 存入      | 結存      |
|------------|---------------------|------|-----------|-----------|-----------|
| Column A   | Column B            | Col C| Column D  | Column E  | Column F  |

Data Row:
| 2023/07/15 | SCR OCTOPUS CARDS   | HKD  | 184.30    |           | 8,349.45  |

Extraction:
{
  "date": "2023/07/15",
  "description": "SCR OCTOPUS CARDS",
  "debit": 184.30,
  "credit": 0,
  "balance": 8349.45
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXAMPLE MAPPING: HANG SENG BANK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Header Row:
| Date       | Transaction Details           | Deposit   | Withdrawal | Balance   |
|------------|-------------------------------|-----------|------------|-----------|
| Column A   | Column B                      | Column C  | Column D   | Column E  |

Data Row 1:
| 7 Mar      | BF BALANCE                    | 2.61      |            | 1,493.98  |
           
Data Row 2:
|            | CREDIT INTEREST               |           |            |           |

Data Row 3:
|            | QUICK CHEQUE DEPOSIT (DTMAND) | 78,649.00 |            | 80,145.59 |

Extraction Process:

Row 1: | 7 Mar | BF BALANCE | 2.61 | | 1,493.98 |
→ Has credit (2.61) → Extract
→ Date = "7 Mar" → Store as lastDate = "7 Mar"

Row 2: | | CREDIT INTEREST | | | |
→ No credit AND no debit → SKIP (no money movement)

Row 3: | | QUICK CHEQUE DEPOSIT (DTMAND) | 78,649.00 | | 80,145.59 |
→ Has credit (78,649.00) → Extract
→ Date is blank → Use lastDate = "7 Mar"

Final Output (2 transactions):
{
  "date": "7 Mar",
  "description": "BF BALANCE",
  "debit": 0,
  "credit": 2.61,
  "balance": 1493.98
},
{
  "date": "7 Mar",  // ← Inherited from previous transaction
  "description": "QUICK CHEQUE DEPOSIT (DTMAND)",
  "debit": 0,
  "credit": 78649.00,
  "balance": 80145.59
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ FINAL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Track the last valid date as you process rows (for date inheritance)
- NEVER calculate balance (ONLY copy visible numbers)
- Output ONLY valid JSON
- NO explanations, NO markdown code blocks, NO comments
- If unclear/ambiguous → output null for that field ONLY
- Process EXACTLY like reading an Excel file: header → column mapping → row-by-row extraction
```

---

## 方案二：VISUAL ROW SCANNER（推荐方案 - 视觉行扫描）

### 🎯 核心思路

基于视觉识别，逐行扫描，以"金额存在性"作为交易判定标准：
1. 视觉定位交易表格
2. 逐行从左到右扫描
3. 如果该行有金额（支出或收入），提取为交易
4. 不依赖日期和余额的存在性

### 📜 完整 Prompt

```
🔷 VISUAL ROW SCANNER MODE (RECOMMENDED)

You are a bank statement scanner. Your job is to scan each visual row and extract transaction data based on AMOUNT PRESENCE (not date presence).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CORE PRINCIPLE: "FOLLOW THE MONEY"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A transaction exists WHERE MONEY MOVES.

✅ Extract a row as transaction IF:
• Debit/Withdrawal/支出 column has a number (e.g., 500.00, 21226.59)
  OR
• Credit/Deposit/存入 column has a number (e.g., 2.61, 78649.00)

❌ Skip a row ONLY IF:
• Both Debit = blank/0 AND Credit = blank/0 (no money movement)
• Row contains: "TOTAL", "SUMMARY", "承上結餘", "Account Summary"

🔄 DATE INHERITANCE RULE:
• Track the last valid date as you process rows
• If current row's date is blank → use the last valid date
• Update lastValidDate whenever you see a non-blank date

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 STEP 1: LOCATE TRANSACTION TABLE (MULTILINGUAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Find the table with transaction history. It must contain:
• Date column: ["日期", "Date", "取引日", "거래일"]
• Amount columns: ["支出", "存入", "Withdrawal", "Deposit", "Debit", "Credit", "借項", "貸項"]
• Balance column: ["餘額", "結存", "Balance", "残高", "잔액"]

Ignore sections with: ["Summary", "摘要", "Total", "總計", "Account Summary"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 STEP 2: SCAN ROW BY ROW (LEFT TO RIGHT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For EACH visual row in the table:

1. Scan from LEFT → RIGHT
2. Check Debit/Withdrawal column: has number?
3. Check Credit/Deposit column: has number?
4. IF either has a number → Extract this row as ONE transaction

⚠️ CRITICAL RULES:
• NEVER merge multiple rows into one transaction
• NEVER skip a row because date is blank
• NEVER combine description from previous/next row
• Extract ONLY what is visible in THIS SINGLE ROW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️ EXTRACTION RULES (FIELD BY FIELD)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Field       | How to Extract                                                         |
|-------------|------------------------------------------------------------------------|
| date        | Copy exact text from Date column. If blank → use PREVIOUS transaction's date |
| description | Copy ALL visible text from Description column of THIS ROW ONLY         |
| debit       | Copy number from Withdrawal/Debit/支出 column (remove commas). Blank → 0 |
| credit      | Copy number from Deposit/Credit/存入 column (remove commas). Blank → 0   |
| balance     | Copy number from Balance/餘額 column (remove commas). If blank/"—" → null |

🎯 KEY POINTS:
• Remove ALL commas from numbers (e.g., "1,500.00" → 1500.00)
• Date format: Output original string AS IS (no conversion)
• Date inheritance: If current row's date is blank, use the date from PREVIOUS extracted transaction
• Description: Copy exact text, do NOT merge with other rows
• Balance: NEVER calculate, ONLY copy visible numbers (if blank → null)
• If field is unclear → output null (for numbers) or "" (for text)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 OUTPUT JSON STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{
  "bankName": "string (copy from document header)",
  "accountNumber": "string (copy from document)",
  "accountHolder": "string (copy from document or \"\")",
  "currency": "string (HKD/USD/CNY/JPY/KRW/etc.)",
  "statementPeriod": "string (copy statement period/date)",
  "openingBalance": number (first transaction's balance if available, else null),
  "closingBalance": number (last transaction's balance if available, else null),
  "transactions": [
    {
      "date": "string (original format or \"\" if blank)",
      "description": "string (complete description from this row)",
      "debit": number (0 if blank),
      "credit": number (0 if blank),
      "balance": number (null if blank)
    }
  ]
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXAMPLE: a bank STATEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Visual Row:
| 2023/07/15 | SCR OCTOPUS CARDS LTD | HKD | 184.30 | | 8,349.45 |

Scan Result:
- Date column: "2023/07/15" ✅
- Description: "SCR OCTOPUS CARDS LTD" ✅
- Debit: 184.30 ✅ (has number → valid transaction!)
- Credit: blank → 0
- Balance: 8,349.45 ✅

Output:
{
  "date": "2023/07/15",
  "description": "SCR OCTOPUS CARDS LTD",
  "debit": 184.30,
  "credit": 0,
  "balance": 8349.45
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXAMPLE: b BANK STATEMENT (COMPLEX CASE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Visual Row 1:
| 7 Mar | CREDIT INTEREST | 2.61 | | 1,496.59 |

Scan Result:
- Date: "7 Mar" ✅
- Description: "CREDIT INTEREST" ✅
- Credit: 2.61 ✅ (has number → valid transaction!)
- Debit: blank → 0
- Balance: 1,496.59 ✅

Output:
{
  "date": "7 Mar",
  "description": "CREDIT INTEREST",
  "debit": 0,
  "credit": 2.61,
  "balance": 1496.59
}

---

Visual Row 2:
| | QUICK CHEQUE DEPOSIT (DTMAND) | 78,649.00 | | 80,145.59 |

Scan Result:
- Date: blank → inherit from previous transaction = "7 Mar"
- Description: "QUICK CHEQUE DEPOSIT (DTMAND)" ✅
- Credit: 78,649.00 ✅ (has number → valid transaction!)
- Debit: blank → 0
- Balance: 80,145.59 ✅

Output:
{
  "date": "7 Mar",  // ← Inherited from previous transaction
  "description": "QUICK CHEQUE DEPOSIT (DTMAND)",
  "debit": 0,
  "credit": 78649.00,
  "balance": 80145.59
}

⚠️ Note: Even though date is blank in the PDF, we inherit "7 Mar" from the previous transaction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 WHY THIS METHOD WORKS BETTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ Date inheritance handled by AI
   - Some banks (HSBC, Hang Seng) leave date blank for same-day transactions
   - AI automatically inherits date from previous transaction
   - No need for backend post-processing!

2. ✅ No row merging confusion
   - Each visual row = one potential transaction
   - Clear rule: has money = extract, no money = skip

3. ✅ Works for all bank formats
   - ICBC: All fields complete
   - Hang Seng: Date/balance may be blank
   - Both work with same rule!

4. ✅ No balance calculation
   - NEVER calculate or infer balance
   - ONLY copy visible numbers
   - If blank → output null

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ FINAL OUTPUT REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Track the last valid date as you process rows (for date inheritance)
- NEVER calculate balance (ONLY copy visible numbers from Balance column)
- Output ONLY valid JSON
- NO explanations before/after JSON
- NO markdown code blocks (```)
- NO comments inside JSON
- If any field is unclear → null (numbers) or "" (text)
- Process systematically: row 1 → row 2 → row 3 → ... → last row
```

---

## 🎯 两个方案对比

| 特性 | 方案一：Excel Table Mode | 方案二：Visual Row Scanner ⭐ |
|------|-------------------------|---------------------------|
| **核心思路** | 先识别列标题，建立列索引映射 | 逐行扫描，基于金额存在性提取 |
| **优势** | 更接近人类读表格的方式 | 简单直接，不依赖列顺序 |
| **劣势** | 需要模型理解"列映射"概念 | 可能遗漏无金额的描述行 |
| **适用场景** | 格式规整的银行单（ICBC） | 所有银行单，尤其复杂格式（HSBC） |
| **准确率预期** | 85% - 90% | 90% - 95% |
| **Token 消耗** | 中等（多一步列映射） | 较低（直接扫描） |
| **推荐指数** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔬 测试建议

### 测试步骤：

1. **分别测试两个 Prompt**
   - 使用恒生银行单测试方案一和方案二
   - 使用 ICBC 银行单测试方案一和方案二

2. **对比结果**
   - 交易数量是否正确
   - 日期、金额、余额是否准确
   - 是否有遗漏或多余的交易

3. **记录问题**
   - 哪些交易被错误提取
   - 哪些字段识别错误
   - Token 消耗对比

### 预期结果：

| 银行 | 方案一 | 方案二 |
|------|-------|-------|
| ICBC | ✅ 准确率高 | ✅ 准确率高 |
| 恒生 | ⚠️ 可能遗漏空日期行 | ✅ 准确率高 |

---

## 📝 后端配合（已简化）

✅ **日期继承已由 AI 处理，无需后端填充！**

两个 Prompt 都已内置日期继承逻辑：
- 如果日期为空，AI 自动使用上一个交易的日期
- 直接输出完整数据，无需后端再处理

~~之前需要的后端代码（已废弃）：~~
```javascript
// ❌ 不再需要！AI 已在 Prompt 中处理
// function fillMissingDates(transactions) { ... }
```

**现在只需要：**
1. 接收 AI 输出的 JSON
2. 直接显示在 UI 上
3. 验证数据完整性（可选）

---

## 🎯 推荐使用

**我强烈推荐使用方案二：Visual Row Scanner**

理由：
1. ✅ 更符合 Vision-Language Model 的工作原理（视觉扫描）
2. ✅ 规则简单明确："有金额 = 提取，无金额 = 跳过"
3. ✅ 不依赖列顺序或格式（适配全球银行）
4. ✅ AI 自动处理日期继承（无需后端代码）
5. ✅ 不计算 balance（只复制可见数字，避免错误）
6. ✅ 配合 `extra_body` 深度思考模式效果更好

---

**下一步：** 使用恒生和 ICBC 银行单测试这两个 Prompt，记录准确率和问题！
