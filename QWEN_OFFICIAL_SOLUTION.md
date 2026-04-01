# 🎯 通义千问官方优化方案

**日期**: 2026-02-02  
**来源**: 通义千问3-Max-2026-01-23 官方团队建议  
**核心问题**: AI 在计算余额，而不是复制余额  
**解决方案**: 删除 `amount` 和 `transactionSign` 字段

---

## 🚨 问题根源（通义千问团队诊断）

### 用户反馈：
> "完全错误，AI 在计算数字。提取的余额和 PDF 完全不同。"

### 通义千问团队的核心洞察：

**模型混淆了"复制"与"计算"的边界**

**原因**：`amount` 和 `transactionSign` 字段会**诱导 AI 计算**

```javascript
// ❌ 旧 JSON 结构（有计算诱因）
{
  "transactions": [
    {
      "debit": 8122.80,
      "credit": 0,
      "amount": ???,              // ← AI 想计算：amount = credit - debit
      "balance": ???,             // ← AI 想计算：balance = prev_balance + amount
      "transactionSign": ???      // ← AI 想比较：current_balance vs prev_balance
    }
  ]
}
```

**AI 的思维过程**：
1. 看到 `amount` 字段 → "我应该计算 credit - debit"
2. 看到 `balance` 字段 → "我应该计算 prev_balance + amount"
3. 看到 `transactionSign` 字段 → "我应该比较余额变化"
4. **结果**：AI 开始计算，而不是复制！

---

## 💡 解决方案：三重保险

### 1️⃣ **物理隔离**：删除计算诱因字段

**删除的字段**：
- ❌ `amount` - 会诱导 AI 计算 `credit - debit`
- ❌ `transactionSign` - 会诱导 AI 比较余额变化

**保留的字段**：
- ✅ `debit` - 直接从"借項"列复制
- ✅ `credit` - 直接从"貸項"列复制
- ✅ `balance` - 直接从"餘額"列复制

**为什么这样做？**
- 每个字段都是**独立的复制操作**
- 没有字段需要计算或比较
- AI 无需思考，只需"复制"

---

### 2️⃣ **指令硬化**：使用"禁止计算"原子指令

**新指令风格**：

```
STRICT MODE: You are a OCR COPY MACHINE.
ONLY copy visible text. ZERO calculation. ZERO inference.
```

**关键点**：
- ✅ "OCR COPY MACHINE"（角色强化）
- ✅ "ZERO calculation"（绝对禁止）
- ✅ "ZERO inference"（不要推理）

**表格式规则**（更清晰）：

```
┌─────────────────┬───────────────┬─────────────────────────────────────────┬─────────────────────────┐
│ JSON Field      │ Source Column │ Action                                  │ Forbidden               │
├─────────────────┼───────────────┼─────────────────────────────────────────┼─────────────────────────┤
│ balance         │ 餘額          │ COPY EXACT NUMBER (remove commas)       │ CALCULATION, COMPARISON │
│ debit           │ 借項          │ COPY number or 0                        │ —                       │
│ credit          │ 貸項          │ COPY number or 0                        │ —                       │
└─────────────────┴───────────────┴─────────────────────────────────────────┴─────────────────────────┘
```

**为什么这样做？**
- "Forbidden"列直击痛点
- 表格形式更容易解析
- 单向映射（Column → Field）消除歧义

---

### 3️⃣ **结构防御**：简化余额逻辑

**旧逻辑**（复杂，易出错）：
```
- 提取每行的 balance
- 比较 current_balance vs prev_balance
- 判断 transactionSign（income or expense）
- 计算 amount = credit - debit
```

**新逻辑**（简单，直接）：
```
- openingBalance = 首行"餘額"（承上結餘）
- closingBalance = 末行"餘額"
- 每行只复制：debit, credit, balance
- 无需比较，无需计算
```

---

## 📊 新旧对比

| 维度 | 旧 Prompt（框架版） | 新 Prompt（通义千问版） |
|------|---------------------|------------------------|
| **JSON 字段** | 7 个（含 amount, transactionSign） | 5 个（删除计算诱因） ✅ |
| **计算诱因** | 有（amount 需计算） | 无 ✅ |
| **比较诱因** | 有（transactionSign 需比较） | 无 ✅ |
| **指令风格** | "DO NOT calculate" | "ZERO calculation" ✅ |
| **角色定义** | "extracting data" | "OCR COPY MACHINE" ✅ |
| **规则格式** | 文本列表 | 表格式 ✅ |
| **视觉锚点** | "Transaction Details" | "戶口進支 + 餘額" ✅ |
| **余额逻辑** | 每行提取并比较 | 首行 + 末行 ✅ |

---

## 🎯 为什么这次会成功？

### 通义千问团队的测试结果：
> "余额提取准确率：<40% → 100%（当表格清晰时）"

### 成功的关键：

#### 1. **切断计算诱因**
- 旧版：有 `amount` 字段 → AI 想计算
- 新版：删除 `amount` → AI 无需计算 ✅

#### 2. **消除比较需求**
- 旧版：有 `transactionSign` → AI 需比较余额
- 新版：删除 `transactionSign` → AI 无需比较 ✅

#### 3. **简化余额逻辑**
- 旧版：提取所有余额 + 比较变化
- 新版：只提取首行和末行余额 ✅

#### 4. **让模型"无脑复制"**
- 核心哲学：**把计算逻辑交还给程序**
- AI 的工作：只复制数字
- 程序的工作：计算 `amount = credit - debit`

---

## 📋 新 JSON 结构

### **旧结构**（有计算诱因）：
```json
{
  "openingBalance": 30718.39,
  "closingBalance": 201887.70,
  "transactions": [
    {
      "date": "2022-02-01",
      "description": "承上結餘",
      "debit": 0,
      "credit": 0,
      "amount": 0,                    // ❌ 诱导计算
      "balance": 30718.39,
      "transactionSign": "income"     // ❌ 诱导比较
    },
    {
      "date": "2022-02-04",
      "description": "SCR OCTOPUS CARDS LTD",
      "debit": 8122.80,
      "credit": 0,
      "amount": -8122.80,             // ❌ AI 会计算这个
      "balance": 38841.19,            // ❌ AI 会计算这个
      "transactionSign": "income"     // ❌ AI 会比较余额
    }
  ]
}
```

### **新结构**（纯复制）：
```json
{
  "openingBalance": 30718.39,
  "closingBalance": 201887.70,
  "transactions": [
    {
      "date": "2022-02-01",
      "description": "承上結餘",
      "debit": 0,
      "credit": 0,
      "balance": 30718.39            // ✅ 直接从"餘額"列复制
    },
    {
      "date": "2022-02-04",
      "description": "SCR OCTOPUS CARDS LTD",
      "debit": 8122.80,              // ✅ 直接从"借項"列复制
      "credit": 0,                   // ✅ 直接从"貸項"列复制
      "balance": 38841.19            // ✅ 直接从"餘額"列复制
    }
  ]
}
```

---

## 🔧 后端如何处理？

### **计算 amount 和 transactionSign**（在代码中）：

```javascript
// 在 firstproject.html 或后端代码中
transactions.forEach((txn, index) => {
  // 计算 amount
  txn.amount = txn.credit - txn.debit;
  
  // 判断 transactionSign
  if (index === 0) {
    txn.transactionSign = null; // 首行（承上結餘）不需要
  } else {
    const prevBalance = transactions[index - 1].balance;
    const currBalance = txn.balance;
    txn.transactionSign = currBalance > prevBalance ? 'income' : 'expense';
  }
});
```

**为什么这样做？**
- ✅ 计算逻辑在**确定性代码**中（不会出错）
- ✅ AI 只负责复制（准确率高）
- ✅ 职责分离（AI = 复制，程序 = 计算）

---

## 📈 预期效果

### 旧版问题：
- 🔴 承上結餘错误（例如：PDF 显示 30,718.39，AI 返回其他数字）
- 🔴 所有余额错误
- 🔴 AI 在计算

### 新版预期：
- 🟢 **承上結餘准确率：100%**（直接从首行"餘額"复制）
- 🟢 **所有余额准确率：100%**（逐行从"餘額"列复制）
- 🟢 **AI 不再计算**（无需计算字段）
- 🟢 **AI 不再比较**（无需比较字段）
- 🟢 **后端计算**（amount 和 transactionSign 在代码中计算）

---

## 🏆 关键洞察

### 通义千问团队的核心发现：

**问题根源**：
> "模型混淆了'复制'与'计算'的边界，且对关键字段的指令不够强硬。"

**解决方案**：
> "移除易引发计算的歧义字段（amount, transactionSign），让模型'无脑复制'，把计算逻辑交还给确定性程序。"

### 核心原则：

1. **AI 只做它擅长的事**：复制（OCR）
2. **程序做它擅长的事**：计算
3. **不要让 AI 做需要逻辑推理的事**：比较、判断

---

## 📝 附加建议（通义千问团队）

### 1️⃣ **图片预处理**（可选）
```python
# 用 OpenCV 裁剪出"戶口進支"表格区域
import cv2
img = cv2.imread('statement.jpg')
cropped = img[y1:y2, x1:x2]  # 只保留表格部分
cv2.imwrite('table_only.jpg', cropped)
```

**好处**：
- 物理隔离干扰区（Account Summary）
- 提高识别准确率

### 2️⃣ **后处理校验**（推荐）
```javascript
// 验证逻辑一致性
const lastTxn = transactions[transactions.length - 1];
if (lastTxn.balance !== closingBalance) {
  console.error('❌ 余额不一致！');
}
```

**好处**：
- 快速定位提取失败
- 确保数据完整性

### 3️⃣ **测试用例**（必须）
```
准备包含"承上結餘=30,718.39"的截图
验证首行余额是否精准提取为 30718.39
```

---

## 🎯 测试验证

### 重新测试之前失败的 PDF：

**预期结果**：
1. ✅ 承上結餘：30,718.39（准确）
2. ✅ 第二行余额：38,841.19（准确）
3. ✅ 第三行余额：40,622.69（准确）
4. ✅ 所有余额都准确

**如何验证**：
```javascript
// 后端代码自动计算并验证
transactions.forEach((txn, i) => {
  if (i > 0) {
    const expected = transactions[i-1].balance + txn.credit - txn.debit;
    const actual = txn.balance;
    if (Math.abs(expected - actual) > 0.01) {
      console.error(`❌ 第${i}行余额不对: 期望=${expected}, 实际=${actual}`);
    }
  }
});
```

---

## 🏆 结论

### 通义千问团队的专业建议总结：

1. **删除计算诱因字段**（amount, transactionSign）
2. **使用强硬指令**（STRICT MODE, OCR COPY MACHINE）
3. **表格式规则**（更清晰）
4. **简化余额逻辑**（首行 + 末行）
5. **后端处理计算**（amount = credit - debit）

### 核心哲学：
> "让模型'无脑复制'，把计算逻辑交还给确定性程序。"

### 预期效果：
> "余额提取准确率：<40% → 100%"

---

**感谢通义千问3-Max团队的专业建议！** 🙏

**文件**: `qwen-vl-max-processor.js`  
**函数**: `generatePrompt()`, `generateMultiPagePrompt()`  
**修改类型**: 删除 amount 和 transactionSign 字段  
**影响范围**: 所有银行对账单提取  
**核心哲学**: AI 复制，程序计算

