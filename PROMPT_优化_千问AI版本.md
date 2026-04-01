# Prompt 优化 - 千问AI版本（基于真实PDF分析）

**更新时间：** 2026-02-04  
**来源：** 千问AI基于真实ICBC和恒生银行PDF的分析

---

## 📊 问题背景

### **之前遇到的问题：**

#### ICBC（工商银行亚洲）：
- ❌ 日期提取错误（2023年被识别为2022年）
- ❌ 交易顺序混乱
- ❌ 金额对不上
- ❌ 部分交易被遗漏或重复

#### 恒生银行（Hang Seng Bank）：
- ❌ 同一天多笔交易时，日期只显示一次（其他行为空）
- ❌ 同一天多笔交易时，只有最后一笔有余额
- ❌ AI无法理解"空白日期=继承上一行的日期"
- ❌ AI无法理解"一个日期对应多笔交易"

---

## 🔍 千问AI的格式分析

### **ICBC（标准清晰型）**
- 表头：日期 | 摘要 | 貨幣 | 支出 | 存入 | 結餘
- 特点：
  - ✅ 每行独立完整
  - ✅ 每笔交易都有日期、金额、余额
  - ✅ 无空白字段
  - ✅ 余额逐笔更新
- **这是最标准的表格格式，适合直接OCR提取**

### **恒生银行（复杂排版型）**
- 表头：Date | Transaction Details | Deposit | Withdrawal | Balance
- 特点：
  - ⚠️ 同日多笔交易共享日期（仅第一行有日期）
  - ⚠️ 余额只出现在最后一笔
  - ⚠️ 描述可能跨行
  - ⚠️ 存在视觉合并（多个交易堆叠）
- **这是高难度格式，AI容易将多行合并为一行**

---

## ✨ 千问AI的关键改进

### **1. 更详细的列识别规则**

**之前：**
```
| debit  | 借項 | COPY number or 0 |
| credit | 貸項 | COPY number or 0 |
```

**现在：**
```
✂️ COLUMN IDENTIFICATION RULES:
- "Date" / "日期": First column in transaction history section
- "Description" / "摘要" / "Transaction Details": Second column
- "Debit" / "借項" / "Withdrawal" / "支出": Column with outflow values
- "Credit" / "貸項" / "Deposit" / "存入": Column with inflow values
- "Balance" / "餘額" / "結餘": Last numeric column
```

**改进：**
- ✅ 支持多语言变体（中文/英文/繁体/简体）
- ✅ 明确每列的位置（第一列、第二列、最后一列）
- ✅ 提供列的语义描述（outflow、inflow）

---

### **2. 基于金额的行验证规则（核心创新）**

**之前：**
- 没有明确的"什么是有效交易"的定义
- 依赖AI自己判断

**现在：**
```
✂️ ROW VALIDATION RULE (CRITICAL):
A row is a VALID TRANSACTION if ANY of the following is TRUE:
- "Description" has non-empty text
- "Debit" or "Credit" contains a number
- "Balance" contains a number
→ IF valid, extract as ONE transaction object — EVEN IF "Date" is blank.
```

**改进：**
- ✅ 明确定义"有效交易"的判断标准
- ✅ 只要有金额（debit/credit/balance），就提取
- ✅ 即使日期为空，也要提取
- ✅ 解决恒生银行"空白日期"问题

---

### **3. 禁止合并行**

**新增规则：**
```
❗ ABSOLUTE COMMANDS:
- EACH PHYSICAL LINE IN THE TABLE = ONE transaction object. 
- NEVER combine multiple lines.
```

**作用：**
- ✅ 防止AI将多行描述合并成一个交易
- ✅ 确保每一行都被独立提取
- ✅ 解决恒生银行多行描述的问题

---

### **4. 允许空日期**

**新增规则：**
```
| date | COPY EXACT visible text. If blank → output "" |
```

**配合后端处理：**
```javascript
// 已有的 postProcessTransactions 函数会自动填充空日期
let lastValidDate = null;
for (const tx of transactions) {
    if (tx.date === "") {
        tx.date = lastValidDate;
    } else {
        lastValidDate = tx.date;
    }
}
```

**作用：**
- ✅ AI输出 `date: ""`（不是null）
- ✅ 后端自动填充上一笔交易的日期
- ✅ 解决恒生银行"同日多交易"问题

---

### **5. 强制提取description**

**新增规则：**
```
| description | COPY ALL text from "Description" column of THIS row ONLY. 
               NEVER merge across rows. |
```

**作用：**
- ✅ 即使日期为空，也要提取描述
- ✅ 只提取当前行的描述，不跨行合并
- ✅ 确保每笔交易的描述完整

---

## 📤 新的输出示例

### **恒生银行（同日多交易）**

**PDF内容：**
```
10 Mar | HD1253... | 840.00 |  | 79,305.59
       | N31088... | 21,226.59 |  | 58,077.00
       | HD1253... | 15,000.00 |  | 43,079.00
```

**AI输出（新Prompt）：**
```json
{
  "transactions": [
    {
      "date": "10 Mar",
      "description": "HD1253...",
      "debit": 840.00,
      "credit": 0,
      "balance": 79305.59
    },
    {
      "date": "",  // ← AI输出空字符串
      "description": "N31088...",
      "debit": 21226.59,
      "credit": 0,
      "balance": 58077.00
    },
    {
      "date": "",  // ← AI输出空字符串
      "description": "HD1253...",
      "debit": 15000.00,
      "credit": 0,
      "balance": 43079.00
    }
  ]
}
```

**后端处理后：**
```json
{
  "transactions": [
    {
      "date": "10 Mar",
      "description": "HD1253...",
      "debit": 840.00,
      "credit": 0,
      "balance": 79305.59
    },
    {
      "date": "10 Mar",  // ← 后端自动填充
      "description": "N31088...",
      "debit": 21226.59,
      "credit": 0,
      "balance": 58077.00
    },
    {
      "date": "10 Mar",  // ← 后端自动填充
      "description": "HD1253...",
      "debit": 15000.00,
      "credit": 0,
      "balance": 43079.00
    }
  ]
}
```

---

## 🎯 预期改进效果

### **ICBC（工商银行）：**
- ✅ 日期识别更准确（2023不会被误读为2022）
- ✅ 交易顺序正确（按表格顺序提取）
- ✅ 金额准确（明确的列识别规则）
- ✅ 不遗漏、不重复（基于金额的行验证）

### **恒生银行：**
- ✅ 空白日期被提取为 `""`（后端填充）
- ✅ 每一行都被独立提取（不合并）
- ✅ 同日多交易正确处理
- ✅ 描述完整（不跨行合并）

---

## 📊 与之前版本的对比

### **版本1：OCR COPY MACHINE（最简版）**
- 优点：简单、直接
- 缺点：缺少明确规则，AI容易混淆

### **版本2：TABLE-AS-EXCEL（EXCEL模式）**
- 优点：结构化思维
- 缺点：过于复杂，AI反而混乱

### **版本3：千问AI优化版（当前版）**
- 优点：
  - ✅ 明确的列识别规则
  - ✅ 明确的行验证规则
  - ✅ 明确的提取规则
  - ✅ 支持多语言和多格式
  - ✅ 禁止合并行
  - ✅ 允许空日期（配合后端）
- 缺点：
  - ⚠️ 稍微复杂（但每条规则都有明确目的）

---

## 🧪 测试建议

### **立即测试：**
1. **重新上传之前失败的ICBC对账单**
   - 检查日期是否正确（2023不应变成2022）
   - 检查交易顺序是否正确
   - 检查金额是否准确

2. **重新上传恒生银行对账单**
   - 检查"10 Mar"那天的多笔交易是否都被提取
   - 检查空白日期是否变成 `""`
   - 检查后端是否正确填充日期

3. **测试其他银行**
   - 中银香港
   - 汇丰银行
   - 渣打银行

---

## 🔄 如果还有问题

### **可能需要进一步优化的地方：**

1. **如果日期仍然识别错误：**
   - 可能需要添加日期格式的明确示例
   - 可能需要禁止AI"纠正"年份

2. **如果行仍然被合并：**
   - 可能需要更强的"禁止合并"警告
   - 可能需要添加行分隔符的识别规则

3. **如果金额仍然错误：**
   - 可能需要更详细的列边界识别规则
   - 可能需要添加OCR错误纠正规则

---

## 💡 关键收获

1. **基于真实PDF的分析比理论假设更有效**
   - 千问AI看到真实PDF后，提供了更准确的建议

2. **明确的规则比模糊的指令更有效**
   - "ROW VALIDATION RULE" 明确定义了"什么是有效交易"
   - "EACH PHYSICAL LINE = ONE transaction" 明确禁止合并行

3. **前后端配合比单纯依赖AI更可靠**
   - AI输出 `date: ""`
   - 后端填充空日期
   - 职责分离，更可靠

---

## 🚀 下一步

1. **测试新Prompt**（本周内）
2. **收集测试结果**（成功率、错误类型）
3. **根据结果决定：**
   - 如果成功率 > 85%：准备推出
   - 如果成功率 < 85%：继续优化或考虑其他方案

---

## 📚 相关文档

- `/Users/cavlinyeung/ai-bank-parser/CURRENT_WORKFLOW_EXPLANATION.md` - 完整工作流程
- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_列对齐优化.md` - 第一次优化
- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_交易判断规则.md` - 第二次优化
- `/Users/cavlinyeung/ai-bank-parser/PROMPT_更新总结_TABLE_AS_EXCEL模式.md` - 第三次优化（已回退）

---

## ✅ 总结

这次优化基于千问AI对真实PDF的分析，提供了更明确、更详细的规则。

**核心改进：**
1. 明确的列识别规则
2. 基于金额的行验证规则
3. 禁止合并行
4. 允许空日期（配合后端填充）

**预期效果：**
- 解决ICBC的日期和顺序问题
- 解决恒生银行的空白日期和同日多交易问题

**现在需要：真实测试来验证效果。**
