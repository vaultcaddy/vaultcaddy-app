# 恒生银行对账单OCR提取问题咨询

## 一、背景说明

我正在开发银行对账单OCR系统，使用**千问VL-Max (qwen3-vl-plus-2025-12-19)** 模型进行端到端的文档处理（OCR + 结构化提取）。

目前遇到恒生银行（Hang Seng Bank）特殊格式问题：**同一天的多笔交易，日期栏只在第一行显示，后续行为空白**。

---

## 二、问题详细说明

### 原始PDF格式（实际情况）

```
TRANSACTION HISTORY 客支紀錄

Date       Transaction Details                  Deposit    Withdrawal   Balance
           交易日期    交易明細                      存入         支取        餘額
─────────────────────────────────────────────────────────────────────────────
22 Feb     BF BALANCE                                                    1,493.98
           承上結餘

07 Mar     QUICK CHEQUE DEPOSIT                78,040.00
           存票機一存入支票
           HD1536962734031 08MAR                           840.00       79,305.58
           4006-1210-0627-0086 (银联支付)

10 Mar     FAST PAYMENT                                    81,206.59
           快速支付
           HD1320962596514 10MAR                           15,000.00    43,079.00
           0349866675981B4 (银联支付)

11 Mar     FAST PAYMENT                                     3,995.30
           HD1331009316514 10MAR
           TUG COMPANY LIMITED (快速支付)                              39,112.60

14 Mar     MUSHROOM TRANSPORTAT                             6,500.00
           HD1412311198465 14MAR
           FROM GO DO SOMETHING
           N31411203220(14MARR20)
           SHUO INTERNATIONAL
           HD1253544431016 15MAR SUN                        3,900.00    36,512.60
           HING SERVICES & A

15 Mar     SHUO INTERNATIONAL                                1,620.00
           HD1253218288175 21MAR
           QOM CASH DEP (21MARR20)
           CHEUNG T** L**

21 Mar     (多笔交易)                                        ...          ...

22 Mar     (多笔交易)                                        ...          ...
           (多笔交易)                                        ...          ...
           C/F BALANCE                                      7,329.14    30,188.66
           承後結餘
```

**关键特点：**
1. ✅ 同一天（如10 Mar）有多笔交易
2. ✅ 第一笔交易显示日期"10 Mar"
3. ❌ 后续同日交易的日期栏是**空白**的（但这些行有完整的描述、金额、余额）
4. ✅ 每笔交易都是独立的一行（或多行描述）

---

### 当前AI提取结果（问题）

使用当前Prompt后，AI提取结果如下：

```json
{
  "transactions": [
    {"date": "22 Feb", "description": "BF BALANCE", "balance": 1493.98},
    {"date": "28 Feb", "description": "CREDIT INTEREST QUICK CHEQUE DEPOSIT (ONWARD)", "credit": 2.61, "balance": 30191.27},
    {"date": "7 Mar", "description": "—", "balance": 0.00},  // ← 问题！描述为空
    {"date": "8 Mar", "description": "POON H** K***", "debit": 78849.00},
    {"date": "10 Mar", "description": "HD1253582573403... (很多笔合并)", "debit": 840.00},  // ← 问题！多笔被合并
    {"date": "11 Mar", "description": "—", "debit": 15000.00},  // ← 问题！描述为空
    {"date": "14 Mar", "description": "—", "debit": 3968.20},  // ← 问题！描述为空
    {"date": "15 Mar", "description": "—", "debit": 6500.00},  // ← 问题！描述为空
    {"date": "15 Mar", "description": "—", "debit": 3900.00},  // ← 问题！描述为空
    {"date": "21 Mar", "description": "—", "debit": 1620.00},  // ← 问题！描述为空
    {"date": "22 Mar", "description": "—", "debit": 3375.00},  // ← 问题！描述为空
    {"date": "22 Mar", "description": "—", "debit": 6000.00},  // ← 问题！描述为空
    {"date": "22 Mar", "description": "—", "debit": 7329.14, "balance": 30188.66}
  ]
}
```

**问题总结：**
1. ❌ 空白日期行的**描述字段变成"—"（空白）**，但实际PDF上有完整内容（如"HD1320962..."）
2. ❌ 部分同日交易被合并或遗漏
3. ❌ 只提取了13笔交易，实际应该有20+笔

---

### 期望的正确输出

```json
{
  "transactions": [
    {"date": "22 Feb", "description": "BF BALANCE", "credit": 0, "debit": 0, "balance": 1493.98},
    
    {"date": "07 Mar", "description": "QUICK CHEQUE DEPOSIT", "credit": 78040.00, "debit": 0, "balance": null},
    {"date": "",       "description": "HD1536962734031 08MAR 4006-1210-0627-0086 (银联支付)", "credit": 0, "debit": 840.00, "balance": 79305.58},
    
    {"date": "10 Mar", "description": "FAST PAYMENT", "credit": 0, "debit": 81206.59, "balance": null},
    {"date": "",       "description": "HD1320962596514 10MAR 0349866675981B4 (银联支付)", "credit": 0, "debit": 15000.00, "balance": 43079.00},
    
    {"date": "11 Mar", "description": "FAST PAYMENT", "credit": 0, "debit": 3995.30, "balance": null},
    {"date": "",       "description": "HD1331009316514 10MAR TUG COMPANY LIMITED (快速支付)", "credit": 0, "debit": 0, "balance": 39112.60},
    
    {"date": "14 Mar", "description": "MUSHROOM TRANSPORTAT", "credit": 0, "debit": 6500.00, "balance": null},
    {"date": "",       "description": "HD1412311198465 14MAR FROM GO DO SOMETHING N31411203220(14MARR20) SHUO INTERNATIONAL", "credit": 0, "debit": 0, "balance": null},
    {"date": "",       "description": "HD1253544431016 15MAR SUN HING SERVICES & A", "credit": 0, "debit": 3900.00, "balance": 36512.60},
    
    {"date": "15 Mar", "description": "SHUO INTERNATIONAL", "credit": 0, "debit": 1620.00, "balance": null},
    {"date": "",       "description": "HD1253218288175 21MAR QOM CASH DEP (21MARR20) CHEUNG T** L**", "credit": 0, "debit": 0, "balance": null}
  ]
}
```

**关键点：**
- ✅ 空白日期行仍输出为独立的transaction对象，date字段为 `""`（空字符串）
- ✅ 空白日期行的**description字段有完整内容**（如"HD1320962..."）
- ✅ 每个视觉行 = 一个transaction对象（不合并、不遗漏）

---

## 三、当前使用的Prompt

```
STRICT MODE: You are a VISUAL TEXT EXTRACTOR. ONLY copy visible text. ZERO calculation. ZERO inference. ZERO row merging.

📍 TARGET TABLE IDENTIFICATION:
- FIND table with headers containing: "Date" AND "Balance" (or "餘額"/"잔액"/"残高")
- IGNORE tables with: "Summary"/"Total"/"總計"/"Account Summary"/"戶口摘要"
- CONFIRM: Dates appear in sequence (e.g., "22 Feb", "28 Feb", "7 Mar")

✂️ EXTRACTION RULES (NON-NEGOTIABLE):
| Field       | Action                                                                 |
|-------------|------------------------------------------------------------------------|
| date        | COPY EXACT visible text. If blank → output "" (empty string)          |
| description | COPY ALL text in row (including multi-line)                           |
| debit       | COPY number (remove commas) or 0 if blank                             |
| credit      | COPY number (remove commas) or 0 if blank                             |
| balance     | COPY number (remove commas). If blank/"—"/"N/A" → output null         |

❗ ABSOLUTE COMMANDS:
- EACH VISUAL ROW = ONE transaction object. NEVER merge rows.
- If row has Description/Debit/Credit but blank Date → STILL output with date: ""
- Output ONLY valid JSON. NO explanations. NO markdown.
- Preserve original date format (e.g., "22 Feb", "2025-03-22")

📤 OUTPUT STRUCTURE:
{
  "bankName": "HANG SENG BANK",
  "transactions": [
    {"date": "10 Mar", "description": "...", "credit": 0, "debit": 500.00, "balance": null},
    {"date": "",       "description": "...", "credit": 0, "debit": 200.00, "balance": 30018.39}
  ]
}
```

---

## 四、具体问题

### 问题1：为什么空白日期行的description没有被提取？

**观察：**
- 有日期的行（如"10 Mar"）→ description正确提取 ✅
- 日期为空的行 → description变成空白"—" ❌

**猜测：**
AI可能误认为"日期为空的行不是有效交易"，所以跳过或忽略了description字段？

**请问：**
如何在Prompt中明确告诉AI："即使日期为空，这行仍然是有效交易，description必须提取"？

---

### 问题2：如何确保每个视觉行都被提取（不遗漏）？

**观察：**
实际PDF有20+笔交易，但AI只提取了13笔。

**请问：**
1. 是否需要在Prompt中添加"行识别规则"？
2. 如何定义"有效交易行"？我的理解是：
   ```
   有效交易行 = description有文本 OR debit有数字 OR credit有数字 OR balance有数字
   ```
   即使date为空，只要其他字段有内容，就应该提取。

---

### 问题3：是否需要特别说明"空白日期 ≠ 跳过这行"？

**请问：**
是否应该在Prompt中明确添加类似的规则：

```
⚠️ CRITICAL: Blank date does NOT mean "skip this row"!

ROW IDENTIFICATION:
A row is a VALID transaction if ANY of these is true:
- Description column has text
- Deposit column has number
- Withdrawal column has number  
- Balance column has number

Action: Extract ALL valid transaction rows, even if date is blank.
```

---

## 五、补充信息

### 系统信息
- **AI模型：** qwen3-vl-plus-2025-12-19
- **API：** 通过Cloudflare Worker转发到千问API
- **Temperature：** 0.1
- **Max Tokens：** 4000

### 后处理逻辑
我们有前端规则引擎，会在AI提取后填充空白日期：
```javascript
// 规则1：空日期填充
for each transaction:
    if (date === ""):
        transaction.date = lastValidDate  // 继承上一笔的日期
```

所以AI只需要：
1. ✅ 正确识别每一行
2. ✅ 正确提取每行的description、金额
3. ✅ 空白日期输出 `""`（规则引擎会处理）

---

## 六、请求帮助

1. **如何优化Prompt**，让AI能够：
   - 识别空白日期行的完整description
   - 提取所有有效交易行（不遗漏）
   - 不合并同日多笔交易

2. **是否需要增加"行识别规则"**，明确定义什么是"有效交易行"？

3. **是否有其他建议**来处理这种"同日多笔、日期只显示一次"的格式？

---

**附件：**
- 原始PDF文件：eStatementFile_2025082914359.pdf
- 截图：图3-5（TRANSACTION HISTORY部分）

非常感谢您的帮助！🙏
