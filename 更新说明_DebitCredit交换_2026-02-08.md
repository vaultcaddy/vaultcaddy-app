# Debit/Credit 交换功能更新

**更新日期：** 2026-02-08  
**更新类型：** 功能增强 + 后端验证  
**Git Commit：** cc568b92

---

## 📋 更新需求

### **需求 1：前端交换功能 ✅**
用户点击金额左侧的 `+/-` 按钮时：
- ✅ 按钮符号切换（`+` ↔ `-`）
- ✅ **Credit 与 Debit 值互换**
- ✅ 余额（Balance）保持不变

### **需求 2：后端自动验证 ✅**
基于余额变化自动修正 debit/credit 分类：
- ✅ 余额减少（上一列 > 本列）→ **Debit（支出）**
- ✅ 余额增加（上一列 < 本列）→ **Credit（存入）**
- ✅ **只交换值，不改变数值本身**

---

## 🔍 会计术语说明

### **Debit vs Credit**

| 术语 | 中文 | 含义 | 余额变化 |
|------|------|------|---------|
| **Debit** | 借项/支出 | 从账户扣除的钱 | 余额**减少** ⬇️ |
| **Credit** | 贷项/存入 | 存入账户的钱 | 余额**增加** ⬆️ |

### **验证逻辑示例**

**场景 1：支出识别错误**
```json
// 原始数据（AI 识别错误）
{
  "date": "2022/02/07",
  "description": "SCR OCTOPUS CARDS LTD",
  "debit": 0,
  "credit": 29193.00,  // ❌ 错误：应该是支出
  "balance": 2971.09
}

// 上一笔交易的余额：32164.09
// 本笔交易的余额：2971.09
// 32164.09 > 2971.09 → 余额减少 → 应该是支出（debit）

// 后端自动修正后
{
  "date": "2022/02/07",
  "description": "SCR OCTOPUS CARDS LTD",
  "debit": 29193.00,   // ✅ 修正：移到 debit
  "credit": 0,         // ✅ 修正：归零
  "balance": 2971.09
}
```

**场景 2：存入识别错误**
```json
// 原始数据（AI 识别错误）
{
  "date": "2022/02/08",
  "description": "FPS Transfer",
  "debit": 1000.00,    // ❌ 错误：应该是存入
  "credit": 0,
  "balance": 3971.09
}

// 上一笔交易的余额：2971.09
// 本笔交易的余额：3971.09
// 2971.09 < 3971.09 → 余额增加 → 应该是存入（credit）

// 后端自动修正后
{
  "date": "2022/02/08",
  "description": "FPS Transfer",
  "debit": 0,          // ✅ 修正：归零
  "credit": 1000.00,   // ✅ 修正：移到 credit
  "balance": 3971.09
}
```

---

## 🛠️ 技术实现

### **1. 前端更新（document-detail-new.js）**

**文件位置：** `document-detail-new.js`  
**函数：** `toggleTransactionType(index)`

**更新前：**
```javascript
function toggleTransactionType(index) {
    // ❌ 只切换显示标记，不交换 debit/credit
    transaction.transactionSign = transaction.transactionSign === 'income' ? 'expense' : 'income';
    
    // 重新渲染
    displayDocumentContent();
    markAsChanged();
}
```

**更新后：**
```javascript
function toggleTransactionType(index) {
    console.log(`🔄 切換交易 ${index} 的類型標記並交換 debit/credit`);
    
    // ✅ 1. 切換顯示標記
    transaction.transactionSign = transaction.transactionSign === 'income' ? 'expense' : 'income';
    
    // ✅ 2. 交換 debit 和 credit 的值
    const tempDebit = transaction.debit;
    transaction.debit = transaction.credit;
    transaction.credit = tempDebit;
    
    console.log(`✅ 交易 ${index} 已切換:`);
    console.log(`   - 標記: ${transaction.transactionSign}`);
    console.log(`   - Debit: ${transaction.debit}`);
    console.log(`   - Credit: ${transaction.credit}`);
    console.log(`   - Balance: ${transaction.balance} (余額保持不變)`);
    
    // 更新 UI
    displayDocumentContent();
    markAsChanged();
}
```

---

### **2. 后端验证（qwen-vl-max-processor.js）**

**文件位置：** `qwen-vl-max-processor.js`  
**函数：** `postProcessTransactions(extractedData)`

**新增逻辑：**
```javascript
// 步骤 2：验证并修正 debit/credit（基于余额变化）
console.log('🔍 开始验证 debit/credit 分类...');
let correctionCount = 0;

for (let i = 1; i < extractedData.transactions.length; i++) {
    const prevTx = extractedData.transactions[i - 1];
    const currTx = extractedData.transactions[i];
    
    // 解析余额值
    const prevBalance = parseFloat(prevTx.balance);
    const currBalance = parseFloat(currTx.balance);
    const debit = parseFloat(currTx.debit) || 0;
    const credit = parseFloat(currTx.credit) || 0;
    
    // 跳过无法比较的行（余额缺失或无效）
    if (isNaN(prevBalance) || isNaN(currBalance)) {
        continue;
    }
    
    // 规则 1：余额减少 = 支出（应该是 debit，不是 credit）
    if (prevBalance > currBalance && credit > 0 && debit === 0) {
        console.log(`⚠️ 交易 ${i} 修正：余额从 ${prevBalance} 减少到 ${currBalance}，应为支出（debit）`);
        currTx.debit = currTx.credit;  // 将 credit 的值移到 debit
        currTx.credit = 0;              // credit 归零
        correctionCount++;
    }
    
    // 规则 2：余额增加 = 存入（应该是 credit，不是 debit）
    if (prevBalance < currBalance && debit > 0 && credit === 0) {
        console.log(`⚠️ 交易 ${i} 修正：余额从 ${prevBalance} 增加到 ${currBalance}，应为存入（credit）`);
        currTx.credit = currTx.debit;   // 将 debit 的值移到 credit
        currTx.debit = 0;               // debit 归零
        correctionCount++;
    }
}

if (correctionCount > 0) {
    console.log(`✅ 共修正 ${correctionCount} 笔交易的 debit/credit 分类`);
} else {
    console.log('✅ 所有交易的 debit/credit 分类正确，无需修正');
}
```

---

## 🎯 验证规则详解

### **规则 1：余额减少 → Debit（支出）**

**触发条件：**
```javascript
prevBalance > currBalance && credit > 0 && debit === 0
```

**含义：**
- 上一笔余额 **大于** 本笔余额（余额减少了）
- 但 AI 识别为 `credit > 0`（存入）
- `debit = 0`（支出为零）

**修正动作：**
```javascript
currTx.debit = currTx.credit;  // 将 credit 的值移到 debit
currTx.credit = 0;              // credit 归零
```

**示例：**
- 原始：`debit: 0, credit: 1000`
- 修正：`debit: 1000, credit: 0`

---

### **规则 2：余额增加 → Credit（存入）**

**触发条件：**
```javascript
prevBalance < currBalance && debit > 0 && credit === 0
```

**含义：**
- 上一笔余额 **小于** 本笔余额（余额增加了）
- 但 AI 识别为 `debit > 0`（支出）
- `credit = 0`（存入为零）

**修正动作：**
```javascript
currTx.credit = currTx.debit;   // 将 debit 的值移到 credit
currTx.debit = 0;               // debit 归零
```

**示例：**
- 原始：`debit: 1000, credit: 0`
- 修正：`debit: 0, credit: 1000`

---

## ✅ 优势分析

### **为什么选择后端验证？**

| 方案 | 优势 | 劣势 |
|------|------|------|
| **Prompt 验证** | 实时修正 | ❌ 增加 Token 消耗<br>❌ 增加 AI 出错概率<br>❌ 难以调试 |
| **前端验证** | 用户可见修正 | ❌ 仅在显示时修正<br>❌ 数据不一致 |
| **后端验证** ⭐ | ✅ 100% 确定性逻辑<br>✅ 可调试<br>✅ 不增加 Token 消耗<br>✅ 保持数据一致性 | 无 |

### **双重保障机制**

1. **前端按钮交换** → 用户手动修正
2. **后端自动验证** → 系统自动修正

**流程：**
```
AI 提取数据
    ↓
后端验证 + 自动修正 ✅
    ↓
前端显示
    ↓
用户点击按钮手动调整（如需要）✅
```

---

## 🧪 测试场景

### **场景 1：AI 识别完全正确**
```javascript
// 交易 1
{ debit: 0, credit: 1000, balance: 31000 }  // 上一笔余额: 30000

// 后端验证
30000 < 31000 && debit=0 && credit=1000  // ✅ 正确，无需修正
```

### **场景 2：AI 识别错误（支出标记为存入）**
```javascript
// 交易 1
{ debit: 0, credit: 500, balance: 29500 }  // 上一笔余额: 30000

// 后端验证
30000 > 29500 && credit=500 && debit=0  // ❌ 错误，自动修正
// 修正后
{ debit: 500, credit: 0, balance: 29500 }  // ✅
```

### **场景 3：用户点击按钮手动调整**
```javascript
// 初始状态
{ debit: 500, credit: 0, balance: 29500 }

// 用户点击 +/- 按钮
toggleTransactionType(index)

// 前端交换后
{ debit: 0, credit: 500, balance: 29500 }  // ✅ 余额保持不变
```

---

## 📊 日志输出示例

### **后端验证日志**

```
🔍 开始验证 debit/credit 分类...
⚠️ 交易 3 修正：余额从 32164.09 减少到 2971.09，应为支出（debit）
⚠️ 交易 7 修正：余额从 2971.09 增加到 3971.09，应为存入（credit）
✅ 共修正 2 笔交易的 debit/credit 分类
```

### **前端交换日志**

```
🔄 切換交易 3 的類型標記並交換 debit/credit
✅ 交易 3 已切換:
   - 標記: expense
   - Debit: 29193.00
   - Credit: 0
   - Balance: 2971.09 (余額保持不變)
```

---

## 🚀 部署步骤

### **已完成 ✅**
1. ✅ 前端代码更新（`document-detail-new.js`）
2. ✅ 后端代码更新（`qwen-vl-max-processor.js`）
3. ✅ Git 提交（cc568b92）

### **测试建议**
1. 上传包含 debit/credit 错误的银行单
2. 检查后端日志，确认自动修正
3. 测试前端 +/- 按钮交换功能
4. 验证余额保持不变

---

## 📚 相关文档

- 📄 **精简版 Prompt 文档**：`PROMPT_简化版_ICBC专用_2026-02-06.md`
- 📄 **测试指南**：`测试指南_精简版Prompt_2026-02-06.md`
- 📄 **统一模型方案**：`统一模型方案_qwen3-vl-plus_标准模式_2026-02-06.md`

---

## ⚠️ 注意事项

### **验证逻辑的限制**

1. **需要余额数据**
   - 如果 PDF 中没有余额列，验证无法进行
   - 解决：保持 AI 原始识别

2. **第一笔交易**
   - 第一笔交易没有"上一笔余额"，无法比较
   - 解决：跳过第一笔，从第二笔开始验证

3. **余额不变的交易**
   - 如果余额不变（`prevBalance == currBalance`）
   - 解决：保持 AI 原始识别，不做修正

### **数值保持不变原则 ⭐**

**重要：** 后端验证**只交换分类**，不改变数值本身！

```javascript
// ✅ 正确：只交换 debit/credit
currTx.debit = currTx.credit;  // 移动值
currTx.credit = 0;              // 归零

// ❌ 错误：不要修改数值本身
currTx.debit = Math.abs(currTx.balance - prevTx.balance);  // ❌ 计算
```

---

**✅ 更新完成！现在可以立即测试！** 🎉
