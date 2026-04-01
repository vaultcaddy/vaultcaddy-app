# Prompt 更新总结 - 金额判断逻辑（关键突破）

> **更新日期：** 2026-02-03  
> **版本：** 3.0（金额判断版）  
> **状态：** ✅ 已实施到代码

---

## 🔥 核心突破：从"日期判断"改为"金额判断"

### 旧版逻辑（问题）

```
判断交易行的依据：日期栏是否有内容

问题：
❌ 恒生银行同日多笔交易，日期栏为空 → 可能被跳过
❌ AI可能误认为"无日期 = 非交易"
❌ 导致description为空或交易被忽略
```

### 新版逻辑（解决方案）✅

```
判断交易行的依据：金额栏是否有数字

优势：
✅ 金额是交易的本质 - 没有金额就不是交易
✅ 适用于所有银行 - 无论日期怎么显示
✅ 解决空白日期问题 - 不再依赖日期判断
```

---

## 📊 更新内容对比

### 1. ROW VALIDATION RULE（新增）

**旧版：** 没有明确的行验证规则

**新版：**
```
✂️ ROW VALIDATION RULE (CRITICAL - AMOUNT-BASED):
⚠️ A row is a VALID TRANSACTION if ANY of the following is TRUE:
1. "Withdrawal"/"借項"/"支取"/"Debit" column contains a number
2. "Deposit"/"貸項"/"存入"/"Credit" column contains a number
3. "Balance"/"餘額"/"结余" column contains a number
4. "Transaction Details"/"交易明細"/"描述" column contains non-empty text

→ IF ANY of these is true, extract as ONE transaction object — EVEN IF "Date" is blank.

❗ CRITICAL: DO NOT use "Date" to decide if a row is a transaction. Use AMOUNT columns instead.
```

**关键改进：**
- 🔥 **以金额判断** - 核心逻辑转变
- 🔥 **四个条件** - 只要满足一个就是有效交易
- 🔥 **明确禁止** - "DO NOT use Date to decide"

---

### 2. AI定位升级

**旧版：** `You are a OCR COPY MACHINE.`

**新版：** `You are a VISUAL TEXT EXTRACTOR.`

**原因：** 千问AI专业建议，更精准的职责定位

---

### 3. 表格识别增强（通用性）

**旧版：**
```
- FIND table with header containing BOTH: "戶口進支" AND "餘額"
```
❌ 只适用恒生银行

**新版：**
```
- FIND table with headers containing keywords:
  * Date: "Date"/"日期"/"交易日期"
  * Balance: "Balance"/"餘額"/"结余"/"잔액"/"残高"
  * Transaction: "Transaction"/"交易"/"明細"/"Details"/"戶口進支"
```
✅ 支持多家银行、多语言

---

### 4. 详细例子（新增）

**旧版：** 简单的3笔交易示例

**新版：** 恒生银行7笔交易完整示例
```
Visual table in PDF:
Date       Transaction Details              Credit    Debit      Balance
10 Mar     FAST PAYMENT                               81,206.59
           HD1320962734031 08MAR (银联)               15,000.00  43,079.00  ← 日期空白
11 Mar     FAST PAYMENT                                3,995.30
           TUG COMPANY LIMITED                                   39,112.60  ← 日期空白
14 Mar     MUSHROOM TRANSPORTAT                        6,500.00
           HD1412311198465 14MAR                                            ← 日期空白
           N31411203220(14MARR20)                      3,900.00  36,512.60  ← 日期空白

Expected output (7 separate transaction objects):
[所有7笔都被提取，包括空白日期的行]
```

**重点说明：**
- ✅ 视觉化展示"空白日期但仍提取"
- ✅ 明确"7行 = 7个对象"（不合并）
- ✅ 空白日期行的description完整

---

### 5. EXTRACTION RULES优化

**旧版：**
```
For EACH ROW in the identified table:
• "date": copy RAW text...
```

**新版：**
```
| Field       | Action                                                                 |
|-------------|------------------------------------------------------------------------|
| date        | COPY EXACT visible text in Date column. If blank/empty → output ""    |
| description | COPY ALL visible text from Transaction Details column of THIS ROW ONLY. NEVER merge with other rows. |
| debit       | COPY number from Withdrawal/借項/支取 (remove commas). If blank → 0    |
| credit      | COPY number from Deposit/貸項/存入 (remove commas). If blank → 0       |
| balance     | COPY number from Balance/餘額 (remove commas). If blank/"—"/"N/A" → null |
```

**改进：**
- ✅ 表格化呈现（更清晰）
- ✅ **"of THIS ROW ONLY"** - 防止合并
- ✅ **"NEVER merge with other rows"** - 再次强调

---

### 6. ABSOLUTE COMMANDS强化

**新增命令：**
```
- EACH VISUAL ROW = ONE transaction object. NEVER combine multiple rows into one.
- NEVER skip a row if it has content in debit/credit/balance columns.
- A blank date does NOT mean "not a transaction" — check amount columns instead.
```

**三次强调"不依赖日期"：**
1. ROW VALIDATION: "DO NOT use Date to decide"
2. EXTRACTION RULES: "If blank/empty → output ''"
3. ABSOLUTE COMMANDS: "A blank date does NOT mean not a transaction"

---

## 🎯 预期解决的问题

### 问题1：空白日期行的description为空 ✅

**原因：** AI误认为"无日期 = 非交易"，忽略了description

**解决：** 新逻辑以金额判断，只要有debit/credit/balance就提取

---

### 问题2：交易被遗漏 ✅

**原因：** 空白日期行被跳过

**解决：** "NEVER skip a row if it has content in amount columns"

---

### 问题3：同日多笔被合并 ✅

**原因：** AI可能自作聪明地合并

**解决：** "EACH VISUAL ROW = ONE transaction object. NEVER combine"

---

## 📝 实施范围

### 已更新的函数

1. **`generatePrompt(documentType)`** - 单页处理
   - 行数：244-368
   - 银行对账单Prompt已完全更新

2. **`generateMultiPagePrompt(documentType, pageCount)`** - 多页处理
   - 行数：370-428
   - 银行对账单Prompt已完全更新

3. **发票Prompt** - 保持不变 ✅
   - 发票处理逻辑无需修改

---

## 🧪 测试建议

### 测试重点

1. **恒生银行对账单**（您提供的图片）
   - ✅ 是否提取了所有交易（20+笔）？
   - ✅ 空白日期行的description是否完整？
   - ✅ 是否没有合并同日多笔？

2. **其他银行对账单**
   - 工商银行（之前已正确）
   - 汇丰银行
   - 其他国际银行

### 测试步骤

```javascript
// 1. 上传恒生银行对账单
// 2. 打开浏览器控制台
// 3. 查看AI原始响应
const docs = await window.simpleDataManager.getDocuments(currentProjectId);
console.log('AI原始响应:', docs[0].rawText);
console.log('交易数量:', docs[0].processedData.transactions.length);

// 4. 检查空白日期行
const emptyDateRows = docs[0].processedData.transactions.filter(tx => tx.date === "");
console.log('空白日期行数量:', emptyDateRows.length);
console.log('空白日期行内容:', emptyDateRows);

// 5. 验证description是否完整
emptyDateRows.forEach((tx, i) => {
    console.log(`空白日期行 ${i+1}:`, tx.description);
});
```

---

## 📊 版本历史

| 版本 | 日期 | 核心特点 | 问题 |
|------|------|----------|------|
| 1.0 | 2026-01-xx | "OCR COPY MACHINE" | 恒生银行问题 |
| 2.0 | 2026-02-03 | "VISUAL TEXT EXTRACTOR"（千问AI建议） | 仍有遗漏 |
| **3.0** | **2026-02-03** | **金额判断逻辑** | **预期解决** ✅ |

---

## 🎯 关键创新点

### 1. 判断逻辑的本质转变 🔥

```
从"表象"（日期是否存在）
    ↓
转为"本质"（金额是否存在）
```

这是解决问题的**核心突破**！

### 2. 三重保险机制

```
1. ROW VALIDATION RULE - 明确告诉AI判断标准
2. EXTRACTION RULES - 规定如何提取每个字段
3. ABSOLUTE COMMANDS - 三次强调不依赖日期
```

### 3. 实例驱动学习

通过7笔交易的详细示例，让AI"看到"正确的处理方式。

---

## 💡 如果问题仍存在

### 可能的原因

1. **AI视觉识别问题**
   - 表格结构识别错误
   - 列对齐出现偏差

2. **Prompt理解问题**
   - AI未能正确理解"金额判断"规则
   - 需要进一步简化或重组

3. **前端后处理问题**
   - `postProcessTransactions()`有bug
   - 规则引擎未正确执行

### 下一步诊断

如果测试后问题仍存在，请提供：
1. AI原始响应（rawText）
2. 处理后数据（processedData）
3. 具体哪些交易被遗漏或错误

---

## ✅ Git提交信息

```
Commit: c841f8df
Message: 🔥 更新Prompt - 金额判断逻辑（关键突破）

文件: qwen-vl-max-processor.js
修改: 106 insertions(+), 74 deletions(-)
```

---

**文档版本：** 1.0  
**创建日期：** 2026-02-03  
**维护者：** AI助手  
**下一步：** 测试验证 → 反馈调整
