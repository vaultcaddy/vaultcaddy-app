# 📊 会计软件 CSV 格式对比分析

## 目的
分析主流会计软件的 CSV 导入格式要求，评估"通用 CSV"的可行性。

---

## 🔍 各软件 CSV 格式要求

### 1️⃣ QuickBooks Online (QBO)

**推荐格式**: QBO 文件（专有格式）  
**CSV 支持**: 有限支持

**CSV 格式**:
```csv
Date,Description,Amount
01/07/2021,Payment received,100.00
01/07/2021,Office supplies,-50.00
```

**要求**:
- **日期格式**: `MM/DD/YYYY` (美国格式)
- **金额格式**: 正数为收入，负数为支出
- **必填字段**: Date, Description, Amount
- **可选字段**: Check Number, Payee

**问题**: 
- ❌ CSV 功能有限，推荐使用 QBO 文件
- ❌ 不支持复杂的交易类型
- ❌ 不支持余额字段

---

### 2️⃣ Xero

**推荐格式**: CSV（直接支持）  
**CSV 支持**: ✅ 完整支持

**CSV 格式**:
```csv
*Date,*Amount,Payee,Description,Reference,Check Number
2021-07-01,100.00,ABC Company,Payment received,INV-001,
2021-07-01,-50.00,Office Depot,Office supplies,REF-002,1234
```

**要求**:
- **日期格式**: `YYYY-MM-DD` (ISO 8601)
- **金额格式**: 正数为收入，负数为支出
- **必填字段**: `*Date`, `*Amount` (带 `*` 标记)
- **可选字段**: Payee, Description, Reference, Check Number
- **列顺序**: 必须严格按照模板顺序

**问题**: 
- ⚠️ 字段名称必须精确匹配（区分大小写）
- ⚠️ 必须使用 `*` 标记必填字段

---

### 3️⃣ Wave Accounting

**推荐格式**: CSV（直接支持）  
**CSV 支持**: ✅ 完整支持

**CSV 格式**:
```csv
Transaction Date,Description,Amount,Currency,Account Name
07/01/2021,Payment received,100.00,USD,Checking Account
07/01/2021,Office supplies,-50.00,USD,Checking Account
```

**要求**:
- **日期格式**: `MM/DD/YYYY` (美国格式)
- **金额格式**: 正数为收入，负数为支出
- **必填字段**: Transaction Date, Amount
- **可选字段**: Description, Currency, Account Name
- **货币**: 必须指定货币代码 (USD, HKD, GBP 等)

**问题**: 
- ⚠️ 字段名称不同于 Xero
- ⚠️ 需要货币字段
- ⚠️ 日期格式不同

---

### 4️⃣ Sage (Sage 50 / Sage Accounting)

**推荐格式**: CSV（支持）  
**CSV 支持**: ✅ 支持

**CSV 格式**:
```csv
Date,Type,Account Ref,Description,Debit,Credit,Reference
01/07/2021,BP,1200,Payment received,100.00,0.00,INV-001
01/07/2021,BR,1200,Office supplies,0.00,50.00,REF-002
```

**要求**:
- **日期格式**: `DD/MM/YYYY` (英国格式)
- **金额格式**: 分开 Debit（借方）和 Credit（贷方）
- **必填字段**: Date, Type, Account Ref, Debit, Credit
- **交易类型代码**: BP (Bank Payment), BR (Bank Receipt) 等

**问题**: 
- ❌ 完全不同的格式！使用借贷分离
- ❌ 需要交易类型代码
- ❌ 需要账户参考号

---

### 5️⃣ FreshBooks

**推荐格式**: CSV（有限支持）  
**CSV 支持**: ⚠️ 有限

**CSV 格式**:
```csv
Date,Description,Amount,Client
2021-07-01,Payment received,100.00,ABC Company
2021-07-01,Office supplies,-50.00,
```

**要求**:
- **日期格式**: `YYYY-MM-DD`
- **金额格式**: 正数为收入，负数为支出
- **必填字段**: Date, Amount
- **可选字段**: Description, Client

**问题**: 
- ⚠️ CSV 导入功能有限
- ⚠️ 推荐使用 API 或手动输入

---

### 6️⃣ MYOB (Mind Your Own Business)

**推荐格式**: TXT/CSV  
**CSV 支持**: ✅ 支持

**CSV 格式**:
```csv
Date,Amount,Description,Memo,Cheque Number
01/07/2021,100.00,Payment received,Invoice INV-001,
01/07/2021,-50.00,Office supplies,Receipt,1234
```

**要求**:
- **日期格式**: `DD/MM/YYYY` (澳洲格式)
- **金额格式**: 正数为收入，负数为支出
- **必填字段**: Date, Amount
- **可选字段**: Description, Memo, Cheque Number

**问题**: 
- ⚠️ 字段名称不同（Cheque vs Check）
- ⚠️ 日期格式不同

---

### 7️⃣ Zoho Books

**推荐格式**: CSV（支持）  
**CSV 支持**: ✅ 支持

**CSV 格式**:
```csv
Date,Description,Reference,Debit,Credit
01/07/2021,Payment received,INV-001,100.00,
01/07/2021,Office supplies,REF-002,,50.00
```

**要求**:
- **日期格式**: `DD/MM/YYYY`
- **金额格式**: 分开 Debit 和 Credit
- **必填字段**: Date, Debit OR Credit
- **可选字段**: Description, Reference

**问题**: 
- ❌ 使用借贷分离格式
- ⚠️ 字段名称不同

---

## 📊 对比总结表

| 软件 | 日期格式 | 金额格式 | 必填字段 | 特殊要求 | 通用性 |
|------|---------|---------|---------|---------|--------|
| **QuickBooks** | MM/DD/YYYY | 正负号 | Date, Amount | 推荐 QBO | ❌ |
| **Xero** | YYYY-MM-DD | 正负号 | *Date, *Amount | 必须用 `*` | ⚠️ |
| **Wave** | MM/DD/YYYY | 正负号 | Date, Amount | 需要 Currency | ⚠️ |
| **Sage** | DD/MM/YYYY | Debit/Credit | Date, Type, Debit, Credit | 需要交易代码 | ❌ |
| **FreshBooks** | YYYY-MM-DD | 正负号 | Date, Amount | CSV 功能有限 | ⚠️ |
| **MYOB** | DD/MM/YYYY | 正负号 | Date, Amount | Cheque 拼写 | ✅ |
| **Zoho Books** | DD/MM/YYYY | Debit/Credit | Date, Debit/Credit | 借贷分离 | ❌ |

**图例**:
- ✅ 高兼容性
- ⚠️ 中等兼容性（需要小调整）
- ❌ 低兼容性（需要大改）

---

## 🎯 结论

### ❌ 无法创建完全通用的 CSV 格式

**原因**:
1. **日期格式不同**: 3种不同格式
2. **金额格式不同**: 正负号 vs 借贷分离
3. **字段名称不同**: 每个软件都不同
4. **必填字段不同**: 要求不一致
5. **特殊要求**: Sage 需要交易代码，Xero 需要 `*` 标记

---

## 💡 推荐方案

### 方案A: 提供多种 CSV 格式（推荐）⭐⭐⭐⭐⭐

**为每个软件提供专用 CSV 格式**:
- `标准 CSV` (VaultCaddy 格式 - 最详细)
- `Xero CSV` (ISO 日期，正负号格式，`*` 标记)
- `QuickBooks CSV` (美国日期，简单格式)
- `Wave CSV` (美国日期，包含货币)
- `Sage CSV` (英国日期，借贷分离)
- `MYOB CSV` (澳洲日期，Cheque 拼写)
- `Zoho Books CSV` (印度格式，借贷分离)

**优点**: ✅ 100% 兼容  
**缺点**: ❌ 需要维护多个导出格式

---

### 方案B: "通用 CSV" + 软件特定格式

**提供2个选项**:
1. **"通用 CSV"** (标准格式，适用于大多数软件，用户可能需要手动调整)
   - 使用 `YYYY-MM-DD` 日期格式（最通用）
   - 使用正负号格式
   - 包含所有字段
   - 添加说明："适用于 Xero, Wave, MYOB 等，可能需要调整列名"

2. **软件特定格式** (针对要求严格的软件)
   - `Sage CSV` (借贷格式)
   - `Zoho Books CSV` (借贷格式)

**优点**: ✅ 简化 UI，覆盖大部分需求  
**缺点**: ⚠️ 用户可能需要手动调整

---

### 方案C: "智能 CSV" (动态字段映射)

**提供1个 CSV + 映射指南**:
- 导出标准 CSV
- 提供在线工具：用户选择目标软件，自动转换字段

**优点**: ✅ 最佳用户体验  
**缺点**: ❌ 需要额外开发

---

## 📋 推荐实施方案

### 推荐: 方案B（通用 + 特定）

**导出菜单**:
```
📥 导出选项
├─ 📄 标准 CSV (VaultCaddy 格式 - 最详细)
├─ 📄 通用 CSV (适用于 Xero, Wave, QuickBooks, MYOB)
├─ 📄 Sage CSV (借贷格式)
├─ 📄 Zoho Books CSV (借贷格式)
├─ 📊 Excel (.xlsx)
└─ 💼 QBO (QuickBooks 专用)
```

**"通用 CSV" 格式**:
```csv
Date,Type,Description,Payee,Reference,Amount,Balance
2021-07-01,Deposit,Payment received,ABC Company,INV-001,100.00,1000.00
2021-07-01,Withdrawal,Office supplies,Office Depot,REF-002,-50.00,950.00
```

**说明文字**:
> 📌 **通用 CSV**: 使用国际标准格式（ISO 8601 日期），适用于 Xero, Wave, QuickBooks, MYOB 等会计软件。导入时可能需要调整列名以匹配软件要求。

---

## ⏱️ 工作量评估

| 任务 | 时间 |
|------|------|
| 实现"通用 CSV"格式 | 15分钟 |
| 实现 Sage CSV 格式 | 30分钟 |
| 实现 Zoho Books CSV 格式 | 30分钟 |
| 更新 UI 和说明文字 | 15分钟 |
| 测试所有格式 | 30分钟 |
| **总计** | **2小时** |

---

## 🎯 下一步行动

1. ✅ 确认方案B
2. ✅ 实现"通用 CSV"格式
3. ✅ 实现 Sage CSV 和 Zoho Books CSV
4. ✅ 更新导出菜单 UI
5. ✅ 添加格式说明
6. ✅ 测试所有格式

---

**创建时间**: 2026-01-07  
**作者**: AI Assistant  
**用途**: 评估会计软件 CSV 格式兼容性


