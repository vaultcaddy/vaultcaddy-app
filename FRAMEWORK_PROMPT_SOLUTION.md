# 🎯 框架式 Prompt - 最终解决方案

**日期**: 2026-02-02  
**核心问题**: AI 在计算数字，而不是复制数字  
**用户洞察**: "需要给 AI 一定的框架"  
**解决方案**: 明确告诉 AI 从哪里提取、如何提取

---

## 🚨 问题回顾

### 用户反馈：
> "我只可以說完全錯誤，最主要是 ai 在計數。我們要有一定的框架給他。"

### 失败的尝试（按时间顺序）：

| 尝试 | 方法 | 结果 |
|------|------|------|
| 1 | 极端强化 - 多次强调"不要计算" | ❌ AI 还是计算 |
| 2 | 删除具体例子 - 避免过拟合 | ❌ AI 还是计算 |
| 3 | 彻底重构 - "数据搬运工"哲学 | ❌ AI 还是计算 |
| 4 | 极简 Prompt - 只要求核心字段 | ❌ AI 还是计算 |
| 5 | 恢复原始中文 Prompt | ❌ AI 还是计算 |
| 6 | 极简通用 Prompt（英文） | ❌ AI 还是计算 |

### 核心问题：
**AI 不知道从哪里提取余额！**
- 银行对账单有 2 个区域：Account Summary 和 Transaction Details
- Account Summary 显示的是计算后的总数
- Transaction Details 才是真正的交易表格
- **AI 可能从 Account Summary 提取，或者自己计算余额**

---

## 💡 解决方案：框架式 Prompt

### 核心思想：
不仅告诉 AI "做什么"，还要告诉 AI：
1. **从哪里**提取
2. **不从哪里**提取
3. **如何**提取（逐步指导）

---

## 📋 新 Prompt 结构

### 1️⃣ 开头：定义任务和警告
```javascript
You are extracting data from a bank statement.
Your job: COPY numbers from the table to JSON. DO NOT calculate anything.
```

**设计原则**：
- ✅ 清晰的任务定义
- ✅ 强调"COPY"而不是"EXTRACT"
- ✅ 立即警告"DO NOT calculate"

---

### 2️⃣ 关键框架：2 个区域（最重要！）
```javascript
Bank statements have 2 sections:
1. Account Summary (戶口摘要) - Shows totals only, SKIP THIS
2. Transaction Details (戶口進支/交易明細) - This is the TABLE you need
```

**设计原则**：
- ✅ **明确区分 2 个区域**（之前的 Prompt 都没有这个）
- ✅ 明确说"SKIP THIS"（Account Summary）
- ✅ 明确说"This is the TABLE you need"（Transaction Details）
- ✅ 中英文双语（帮助 AI 识别中文对账单）

**为什么这是关键？**
- 这是之前所有 Prompt 缺失的部分
- AI 不知道从哪里提取，所以可能从 Account Summary 提取（那里是总数）
- 或者 AI 看到多个数字，自己计算余额

---

### 3️⃣ JSON 结构（简洁版）
```javascript
📋 What to extract:

{
  "bankName": "Bank name",
  "transactions": [...]
}
```

**设计原则**：
- ✅ 用 emoji 📋 增加视觉识别
- ✅ 保持简洁，只列字段名

---

### 4️⃣ 核心：4 步提取流程（框架！）
```javascript
🎯 HOW to extract transactions:

Step 1: Find the Transaction Details TABLE (戶口進支/交易明細)
Step 2: Each ROW in the table = ONE transaction
Step 3: For each row, COPY these columns:
   - Date column → "date" (format: YYYY-MM-DD)
   - Description column → "description" 
   - Debit/Withdrawal column → "debit" (0 if empty)
   - Credit/Deposit column → "credit" (0 if empty)
   - Amount column → "amount"
   - Balance column → "balance" (COPY this number, DO NOT calculate!)

Step 4: Determine "transactionSign":
   - Compare current row balance with previous row balance
   - If balance INCREASED → "income"
   - If balance DECREASED → "expense"
```

**设计原则**：
- ✅ **明确的 4 步流程**（框架！）
- ✅ Step 1: 找到正确的表格
- ✅ Step 2: 每行 = 一个交易
- ✅ Step 3: 逐列说明如何复制（最详细）
- ✅ Step 4: 唯一需要"判断"的部分（income/expense）
- ✅ **Balance column 特别强调：COPY, DO NOT calculate**

---

### 5️⃣ 结尾：关键警告
```javascript
⚠️ CRITICAL:
- Extract EVERY row from the transaction table (including "承上結餘/Brought Forward")
- DO NOT skip any rows
- DO NOT combine rows
- Balance: COPY the number from Balance column, DO NOT calculate
- If you cannot see a number, set to null
```

**设计原则**：
- ✅ 用 ⚠️ 符号引起注意
- ✅ 再次强调 Balance 的处理方式
- ✅ 包含"承上結餘"（开头结余）的提取

---

## 📊 新旧对比

| 维度 | 旧 Prompt（极简版） | 新 Prompt（框架版） |
|------|---------------------|---------------------|
| **区域说明** | ❌ 无 | ✅ 明确 2 个区域 |
| **提取位置** | ❌ 不明确 | ✅ "Transaction Details TABLE" |
| **跳过位置** | ❌ 不明确 | ✅ "SKIP Account Summary" |
| **提取流程** | ❌ 无框架 | ✅ 4 步明确流程 |
| **Balance 处理** | "Extract balance" | ✅ "COPY from Balance column" |
| **逐列说明** | ❌ 无 | ✅ Step 3 逐列说明 |
| **中文关键词** | ❌ 无 | ✅ 戶口進支/交易明細 |

---

## 🎯 为什么这次会成功？

### 1. **明确的空间框架**
- 旧版：只说"提取交易"
- 新版：明确"从 Transaction Details TABLE 提取"
- **AI 知道在哪里找数据**

### 2. **明确的操作指令**
- 旧版：只说"不要计算"
- 新版：说"COPY the number from Balance column"
- **AI 知道如何操作**

### 3. **逐步的提取流程**
- 旧版：没有流程，AI 自由发挥
- 新版：4 步流程，AI 按步骤执行
- **AI 有清晰的执行路径**

### 4. **双语关键词**
- 英文 Prompt + 中文关键词（戶口進支/交易明細）
- 帮助 AI 识别中文对账单的特定区域
- **适用全球，但优化了中文识别**

---

## 🔍 与用户需求的对应

### 用户的核心要求：
1. **提取数据 + 放在对的位置**
   - ✅ 新 Prompt：明确从 Transaction Details TABLE 提取
   - ✅ 4 步流程确保数据放在对的位置

2. **不改变任何数字**
   - ✅ 新 Prompt：多次强调 COPY，不是 calculate
   - ✅ Balance: "COPY the number from Balance column"

3. **只改变分类（income/expense）**
   - ✅ 新 Prompt：Step 4 专门说明如何判断
   - ✅ 通过余额比较判断

4. **需要框架**
   - ✅ 新 Prompt：4 步提取流程就是框架
   - ✅ 告诉 AI "从哪里" "如何" 提取

---

## 📈 预期效果

### 旧版问题：
- 🔴 承上結餘错误（例如 59,417.89，应该是 30,718.39）
- 🔴 很多余额错误
- 🔴 AI 在计算数字

### 新版预期：
- 🟢 **承上結餘准确**：从 Balance column 直接复制
- 🟢 **所有余额准确**：逐行从 Balance column 复制
- 🟢 **不计算**：AI 知道从哪个列复制，不需要计算
- 🟢 **每行独立提取**：Step 2 明确说明
- 🟢 **不遗漏**：包括"承上結餘"

---

## 🏆 关键洞察

### 之前为什么失败？
1. **过度强调"不要做"，没说"要做什么"**
   - 说了 20+ 次"不要计算"
   - 但没说"从 Balance column 复制"

2. **没有空间框架**
   - 没说从哪里提取（Transaction Details）
   - 没说不从哪里提取（Account Summary）
   - AI 可能从错误的地方提取

3. **没有操作流程**
   - 只说"提取交易"
   - AI 不知道如何逐步执行

### 为什么这次会成功？
1. **有明确的空间框架**
   - 2 个区域：哪里提取，哪里跳过

2. **有明确的操作流程**
   - 4 步流程：找表格 → 识别行 → 复制列 → 判断分类

3. **有具体的操作指令**
   - 不是"不要计算"
   - 而是"COPY from Balance column"

---

## 📝 核心原则

### 1️⃣ 给 AI 框架，而不是自由
- ❌ "提取所有交易"（太抽象）
- ✅ "Step 1: Find the TABLE, Step 2: Each ROW..."（具体框架）

### 2️⃣ 告诉 AI "在哪里"，而不只是"做什么"
- ❌ "提取余额"（AI 不知道从哪里提取）
- ✅ "COPY from Balance column"（AI 知道在哪里）

### 3️⃣ 正面指令 > 负面指令
- ❌ "不要计算"（AI 不知道要做什么）
- ✅ "COPY this number"（AI 知道要做什么）

### 4️⃣ 流程 > 规则
- ❌ 8 个规则（AI 可能忘记）
- ✅ 4 步流程（AI 按步骤执行）

---

## 🎯 测试要点

重新上传之前失败的 PDF，验证：
1. ✅ **承上結餘是否正确**（这是关键）
2. ✅ **所有余额是否正确**（逐行检查）
3. ✅ **日期和金额是否准确**
4. ✅ **transactionSign 是否正确**（income/expense）
5. ✅ **是否提取了所有行**（不遗漏）

---

## 🏆 结论

### 用户是对的：
> "我們要有一定的框架給他"

### 关键发现：
- AI 需要**明确的空间框架**（从哪里提取）
- AI 需要**明确的操作流程**（如何提取）
- AI 需要**具体的指令**（COPY，不是 calculate）

### 最终方案：
**框架式 Prompt**：
1. 明确 2 个区域（哪里提取，哪里跳过）
2. 4 步提取流程（找 → 识别 → 复制 → 判断）
3. 逐列说明（Date → Description → ... → Balance）
4. 具体指令（COPY from Balance column）

---

**文件**: `qwen-vl-max-processor.js`  
**函数**: `generatePrompt()`, `generateMultiPagePrompt()`  
**修改类型**: 框架式 Prompt（4 步流程 + 2 区域说明）  
**影响范围**: 所有银行对账单提取  
**核心哲学**: 给 AI 框架，而不是自由

