# 向通义千问提问：银行对账单提取错误问题

## 问题描述
我使用 Qwen-VL-Max 模型提取银行对账单数据，遇到了**"看错行/看错表格"**的问题。

---

## PDF 文件实际结构（恒生银行对账单）

### 第1页：账户信息
- 银行名称：HANG SENG BANK (恒生银行)
- 账户号码：766-450064-882
- 对账日期：22 Mar 2025

### 第2页：包含两个表格

#### 表格1：ACCOUNT SUMMARY（账户摘要）- 位于页面顶部
```
Deposit Services        Account Number   Balance (HKD)
综合户口                766-450064-882   30,188.66
HKD Statement Savings                    30,188.66
Sub-total                                30,188.66
Total                                    30,188.66

Credit Facilities       Account Number   Loan Balance  HKD Equivalent
其他户口                996-667688-164   119,986.00DR  119,986.00DR
Personal Loan                            119,986.00DR  119,986.00DR
Sub-total                                119,986.00DR  119,986.00DR

Card Types              Account Number   Credit Limit  Balance (HKD)
VISA Platinum Card      4006 1210 0627   279,000.00    19,906.81DR
```

#### 表格2：TRANSACTION HISTORY（交易历史）- 位于页面底部
```
Integrated Account Statement Savings (综合户口－儲蓄戶口)

Date    Transaction Details                     Deposit      Withdrawal   Balance (HKD)
22 Feb  BF BALANCE                                                        1,493.98
28 Feb  CREDIT INTEREST QUICK                   2.61                      1,496.59
        CHEQUE DEPOSIT (DTMAND)
7 Mar   存入現金                                78,649.00                 80,145.59
        POON H** K***
8 Mar   (繳費項目)                                           840.00       79,305.59
10 Mar  HD1253582573401 08MAR                                            (省略后续交易)
        4006-1210 0627-0086
...（继续列出所有交易，直到最后一行）
22 Mar  C/F BALANCE                                                       30,188.66
```

### 第3页：只包含最后两笔交易
```
Date    Transaction Details                     Deposit      Withdrawal   Balance (HKD)
...
22 Mar  期初現金存款(利息計息戶口)              88,561.61    93,856.85
        Credit Interest Account
```

---

## AI 提取的错误结果

```json
{
  "openingBalance": 30718.39,   // ❌ 错误！应该是 1,493.98
  "transactions": [
    {
      "date": "22 Feb",
      "description": "承上結餘",
      "debit": 0,
      "credit": 0,
      "balance": 30718.39        // ❌ 错误！应该是 1,493.98
    },
    {
      "date": "28 Feb",
      "description": "CREDIT INTEREST QUICK CHEQUE DEPOSIT (DTMAND)",
      "debit": 0,
      "credit": 2.61,
      "balance": 1493.98
    },
    {
      "date": "7 Mar",
      "description": "存入現金",
      "debit": 0,
      "credit": 76849.00,        // ❌ 错误！应该是 78,649.00
      "balance": 1496.59
    }
  ]
}
```

---

## 期望的正确结果

```json
{
  "openingBalance": 1493.98,     // ✅ 正确
  "transactions": [
    {
      "date": "22 Feb",
      "description": "BF BALANCE",
      "debit": 0,
      "credit": 0,
      "balance": 1493.98         // ✅ 正确
    },
    {
      "date": "28 Feb",
      "description": "CREDIT INTEREST QUICK CHEQUE DEPOSIT (DTMAND)",
      "debit": 0,
      "credit": 2.61,
      "balance": 1496.59
    },
    {
      "date": "7 Mar",
      "description": "存入現金",
      "debit": 0,
      "credit": 78649.00,        // ✅ 正确
      "balance": 80145.59
    }
  ]
}
```

---

## 当前使用的 Prompt

```
STRICT MODE: You are a OCR COPY MACHINE. ONLY copy visible text. ZERO calculation. ZERO inference.

📍 TARGET TABLE IDENTIFICATION (CRITICAL):
- FIND table with header containing BOTH: "戶口進支" AND "餘額"
- IGNORE any section with "戶口摘要" / "Account Summary" / "總計" / "TOTAL"
- FIRST row of target table MUST be "承上結餘" (Brought Forward) → this row's "餘額" = openingBalance
- LAST row's "餘額" = closingBalance

✂️ FIELD EXTRACTION RULES (NON-NEGOTIABLE):
| JSON Field      | Source Column | Action                                  | Forbidden               |
|-----------------|---------------|-----------------------------------------|-------------------------|
| balance         | 餘額          | COPY EXACT NUMBER (remove commas)       | CALCULATION, COMPARISON |
| debit           | 借項          | COPY number or 0                        | —                       |
| credit          | 貸項          | COPY number or 0                        | —                       |
| amount          | (REMOVE)      | ⚠️ FIELD DELETED - DO NOT OUTPUT        | —                       |
| transactionSign | (REMOVE)      | ⚠️ FIELD DELETED - DO NOT OUTPUT        | —                       |

❗ ABSOLUTE COMMANDS:
- IF "餘額" column value = "30,718.39" → output balance: 30718.39 (NO EXCEPTIONS)
- IF number unclear → output null (NEVER guess/calculate)
- REMOVE all commas from numbers before outputting
- Date format: Convert to YYYY-MM-DD ONLY if unambiguous; else output original string
- Output ONLY valid JSON. NO explanations. NO markdown. NO comments.

📤 OUTPUT STRUCTURE (REDUCED):
{
  "bankName": "...",
  "accountNumber": "...",
  "accountHolder": "...",
  "currency": "...",
  "statementPeriod": "...",
  "openingBalance": 30718.39,  // FROM FIRST ROW'S "餘額"
  "closingBalance": ...,        // FROM LAST ROW'S "餘額"
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "...",
      "debit": 0,
      "credit": 1500.00,
      "balance": 32218.39  // COPIED DIRECTLY FROM "餘額" COLUMN OF THIS ROW
    }
  ]
}

⚠️ CRITICAL: Extract EVERY row from "戶口進支" table (including "承上結餘"). DO NOT skip. DO NOT combine.
```

---

## 问题分析

### 我的猜测：
1. **AI 读取了错误的表格**：可能读取了顶部的 ACCOUNT SUMMARY（30,188.66），而不是底部的 TRANSACTION HISTORY（1,493.98）
2. **行对齐错误**：7 Mar 的存入金额从 78,649.00 变成了 76,849.00，可能是读取了其他行的数字

### 关键问题：
- 银行对账单通常有多个表格（账户摘要表、交易历史表）
- 不同表格的数字容易混淆
- 如何让 AI 精准定位到 "TRANSACTION HISTORY" 表格？
- 如何确保 AI 从同一行读取所有字段（日期、描述、金额、余额）？

---

## 我的提问

**请帮我优化这个 Prompt，解决以下问题：**

1. **如何让 AI 准确识别 TRANSACTION HISTORY 表格**，而不是 ACCOUNT SUMMARY？
   - 提示：TRANSACTION HISTORY 有 Date 列，且日期是连续的（22 Feb, 28 Feb, 7 Mar...）
   - ACCOUNT SUMMARY 没有 Date 列

2. **如何确保 AI 从同一行读取所有字段**，避免行对齐错误？
   - 例如：7 Mar 这行的所有字段（日期、描述、存款、余额）必须都来自这一行

3. **如何处理多页文档**？
   - 第2页有完整的交易记录
   - 第3页只有最后几笔交易
   - 如何确保 AI 不会重复提取或遗漏？

**期望的优化方向：**
- 添加更明确的表格识别规则（通过列名、日期格式等特征）
- 强调"横向扫描"规则（同一行的所有字段必须一起提取）
- 添加验证机制（例如：首行余额应该是最小的，末行余额应该是最大的）

---

## 技术背景
- **模型**：Qwen-VL-Max (qwen3-vl-plus-2025-12-19)
- **输入**：多页 PDF 转换的图片（Base64）
- **输出**：JSON 格式的结构化数据
- **语言**：中英文混合（香港银行对账单）

