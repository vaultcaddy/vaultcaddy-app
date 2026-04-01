# Prompt 更新总结 - AB类通用版

**日期：** 2026-02-06  
**目标：** 建立一个同时适用于A类和B类银行对账单的通用Prompt

---

## 📋 背景：用户的核心理解

用户通过实际案例（图1-7）明确了银行对账单的两种类型：

### **A类银行单**（图1-4：ICBC 工商银行）
- ✅ 所有交易都有：**日期、名称、支出/存入、余额**
- 特点：完整、标准、清晰

### **B类银行单**（图5-7：Hang Seng 恒生银行）
- ✅ 所有交易都有：**名称、支出/存入**
- ⚠️ **日期和余额可能空白**
- 特点：复杂、不规则

### 🔑 **用户的核心理解：**
1. **只要有支出/存入 = 一单交易记录**
2. 日期和余额可以是空白
3. 我们只是数据抄写员，**不用计算**
4. 目标：全球所有银行单合用（中文、英文、韩文、日文）

---

## 🎯 关键修改

### 1. **简化交易判定规则**

**之前（复杂，4个条件）：**
```
A row is a VALID TRANSACTION if ANY of the following is TRUE:
- "description" column contains non-whitespace text
- "debit" column contains a visible number
- "credit" column contains a visible number
- "balance" column contains a visible number
```

**现在（简单，1个核心）：**
```
CORE: Extract a row as transaction IF debit OR credit has a number
Skip ONLY IF: Both debit=0 AND credit=0 (no money movement)
```

✅ **为什么更好：**
- 符合用户的理解："只要有支出/存入就是一单交易"
- 更简洁，AI更容易遵循
- 直接适用于AB两类

---

### 2. **明确定义AB两类**

新增：
```
You are a DATA COPY CLERK. Two bank statement types exist:
• TYPE A (ICBC 工商银行): All transactions have date, description, debit/credit, balance
• TYPE B (Hang Seng 恒生银行): Transactions have description+debit/credit, but date/balance may be blank
```

✅ **作用：**
- 让AI理解两种类型的存在
- 明确B类的空白字段是正常现象
- 避免AI因为空白字段而跳过交易

---

### 3. **添加实际例子**

新增：
```
💡 EXAMPLES - TYPE A vs TYPE B:
TYPE A (ICBC - 所有字段都有):
{"date":"2023/07/07","description":"SIC ALIPAY HK LTD","debit":21.62,"credit":0,"balance":35667.34}

TYPE B (Hang Seng - 日期和余额可能空白):
{"date":"","description":"QUICK CHEQUE DEPOSIT","debit":0,"credit":78649.00,"balance":null}
{"date":"10 Mar","description":"ATM WITHDRAWAL","debit":500.00,"credit":0,"balance":79405.09}
```

✅ **作用：**
- 清楚展示TYPE A和TYPE B的差异
- 明确展示空白字段的正确处理方式
- 用实际例子强化AI的理解

---

### 4. **强调数据抄写员角色**

修改标题：
```
🎯 TRANSACTION RULE (CRITICAL - AB Types Compatible):
You are a DATA COPY CLERK.
```

✅ **作用：**
- 强调"抄写员"角色，不是"计算器"
- 符合用户的理解："我们只是数据抄写员，不用计算"
- 避免AI过度推理或计算

---

## 📊 Prompt结构对比

| 部分 | 之前 | 现在 | 改进 |
|------|------|------|------|
| 角色定义 | VISUAL TEXT EXTRACTOR | DATA COPY CLERK | ✅ 更明确"抄写"角色 |
| 交易判定 | 4个条件（description/debit/credit/balance） | 1个核心（debit OR credit） | ✅ 更简洁清晰 |
| AB类说明 | 无 | 明确定义TYPE A和TYPE B | ✅ 让AI理解两类差异 |
| 实际例子 | 无 | ICBC vs Hang Seng对比例子 | ✅ 强化理解 |
| 空值处理 | 已有 | 强调date=""和balance=null | ✅ 更清晰 |

---

## 🧪 测试计划

### 测试1：TYPE A（ICBC 工商银行）
**预期结果：**
- ✅ 所有交易都有完整的date、description、debit/credit、balance
- ✅ 日期格式保持原样（如 "2023/07/07"）
- ✅ 金额正确，去除逗号
- ✅ 交易顺序正确

### 测试2：TYPE B（Hang Seng 恒生银行）
**预期结果：**
- ✅ 提取所有有支出/存入的行（即使date=""）
- ✅ 空白日期输出为 `"date": ""`
- ✅ 空白余额输出为 `"balance": null`
- ✅ 不跳过任何有金额的交易
- ✅ 后端的 `postProcessTransactions` 正确填充空白日期

### 测试3：多语言银行单（如有）
**预期结果：**
- ✅ 正确识别日文/韩文表头
- ✅ 提取逻辑与中英文一致

---

## 📈 成功标准

| 指标 | 目标 |
|------|------|
| **TYPE A准确率** | ≥90% |
| **TYPE B准确率** | ≥85% |
| **空白日期处理** | 100%（frontend自动填充） |
| **交易遗漏率** | <5% |
| **误判率** | <5% |

---

## 🚀 下一步行动

### ✅ 已完成
1. ✅ 更新 `qwen-vl-max-processor.js` 中的 `generatePrompt()` 和 `generateMultiPagePrompt()`
2. ✅ 添加AB类定义和实际例子
3. ✅ 简化交易判定规则
4. ✅ 强调数据抄写员角色

### 🔜 待执行
1. **立即测试 ICBC 对账单**（图1-4）
   - 上传完整的4页PDF
   - 检查提取结果的准确性
   - 特别注意日期格式和金额

2. **立即测试 Hang Seng 对账单**（图5-7）
   - 上传完整的PDF
   - 检查空白日期是否正确输出为 `""`
   - 检查空白余额是否正确输出为 `null`
   - 验证前端 `postProcessTransactions` 是否正确填充日期

3. **对比分析**
   - 记录TYPE A和TYPE B的准确率
   - 识别仍然存在的问题

4. **决定推出**
   - 如果准确率≥85% → 立即准备产品落地页和广告
   - 如果准确率75-84% → 加"人工辅助验证"功能后推出
   - 如果准确率<75% → 重新评估AI模型选择

---

## 💡 关键洞察

### ✅ 为什么这次更新很重要？

1. **基于真实案例**
   - 用户通过实际的ICBC和Hang Seng对账单明确了需求
   - 不是理论推测，而是真实问题

2. **符合用户的理解模型**
   - "只要有支出/存入就是一单交易"
   - "我们只是数据抄写员"
   - 这些是用户的原话，最贴近实际需求

3. **AB类通用性**
   - 不需要为每种银行写不同的Prompt
   - 一个Prompt覆盖全球标准型和复杂型银行单

4. **简洁但完整**
   - 简化了交易判定规则（4条→1条）
   - 但保留了所有必要的细节（多语言、空值处理、格式保持）

---

## ⚠️ 注意事项

1. **后端日期填充仍然必需**
   - Prompt让AI输出 `"date": ""`
   - `postProcessTransactions()` 在前端填充空白日期
   - 这是正确的架构（AI做视觉，后端做逻辑）

2. **保持Prompt稳定**
   - 这次更新基于用户的核心理解
   - 除非测试发现重大问题，否则不要频繁修改
   - 过度优化会导致混乱

3. **测试优先**
   - 不要猜测效果
   - 立即用实际PDF测试
   - 用数据说话

---

## 📝 文件更新记录

| 文件 | 修改内容 | 行号 |
|------|----------|------|
| `qwen-vl-max-processor.js` | `generatePrompt()` - 单页Prompt | 244-315 |
| `qwen-vl-max-processor.js` | `generateMultiPagePrompt()` - 多页Prompt | 317-420 |
| `PROMPT_AB类通用版.md` | 新建 - Prompt文档 | 全部 |
| `PROMPT_更新总结_AB类通用版.md` | 新建 - 本文档 | 全部 |

---

## 🎯 终极目标

**这个Prompt的目标是：**
- ✅ 让AI能准确提取A类和B类银行对账单
- ✅ 不需要为每种银行写专门的规则
- ✅ 适用于全球主要银行（中英日韩四语）
- ✅ 配合后端日期填充，达到90%+准确率
- ✅ 让你能自信地推出产品并开始销售

**现在该行动了：测试 → 验证 → 推出！** 🚀
