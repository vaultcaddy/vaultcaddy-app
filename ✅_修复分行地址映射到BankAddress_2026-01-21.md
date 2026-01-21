# ✅ 修复分行地址映射到 Excel BankAddress 列

## 📋 问题描述
- **图1（Excel）**: `BankAddress` 列（D列）应该显示分行地址
- **图2（网页）**: "分行地址"字段的内容没有正确映射到Excel的 `BankAddress` 列

---

## 🔍 问题根源

### 字段名称不匹配
**网页端**:
- 字段标签: "分行地址"
- 数据字段名: `branchName`

**Excel导出**:
- 列名: `BankAddress`
- 数据来源: `data.bankAddress` 或 `data.bank_address`

**问题**: 网页上的 `branchName` 字段没有被Excel导出代码识别。

---

## ✅ 已完成的修复

### 修改文件
`document-detail.html`

### 修改位置
第 3002-3007 行（Excel导出部分）

### 修改内容

#### **修改前**:
```javascript
// 提取基本信息
const customerName = data.accountHolder || data.account_holder || data.customerName || '';
const accountNumber = data.accountNumber || data.account_number || '';
const accountType = data.accountType || 'Integrated Account';
const bankName = data.bankName || data.bank_name || data.bank || '';
const bankAddress = data.bankAddress || data.bank_address || '';
```

#### **修改后**:
```javascript
// 提取基本信息
const customerName = data.accountHolder || data.account_holder || data.customerName || '';
const accountNumber = data.accountNumber || data.account_number || '';
const accountType = data.accountType || 'Integrated Account';
const bankName = data.bankName || data.bank_name || data.bank || '';
// 🔥 分行地址：优先使用 branchName (页面上的"分行地址"字段)
const bankAddress = data.branchName || data.branch_name || data.bankAddress || data.bank_address || '';
```

---

## 📊 字段映射关系

### 完整映射表
| 网页字段（中文） | 网页数据字段名 | Excel列名 | 映射优先级 |
|---------------|--------------|-----------|-----------|
| 銀行名稱 | `bankName` | `BankName` | 1️⃣ `bankName` → 2️⃣ `bank_name` → 3️⃣ `bank` |
| 銀行代碼 | `bankCode` | - | - |
| 帳戶號碼 | `accountNumber` | `AccountNumber` | 1️⃣ `accountNumber` → 2️⃣ `account_number` |
| **分行地址** | `branchName` | `BankAddress` | 1️⃣ `branchName` → 2️⃣ `branch_name` → 3️⃣ `bankAddress` → 4️⃣ `bank_address` |
| 帳戶持有人 | `accountHolder` | `CustomerName` | 1️⃣ `accountHolder` → 2️⃣ `account_holder` → 3️⃣ `customerName` |

### 为什么使用多个备选字段？
**向后兼容**: 支持不同版本的数据格式
- `branchName`: 新版本（页面表单）
- `branch_name`: 下划线格式
- `bankAddress`: 旧版本
- `bank_address`: 旧版本下划线格式

---

## 🧪 测试步骤

### 步骤 1: 在网页中填写分行地址
1. 打开: `https://vaultcaddy.com/document-detail.html?project=SJJkhY7CFdqh8zyVAM6B&id=vPwfbEF32mLC72EsZsDW`
2. 找到"分行地址"字段
3. 填写地址，例如: `香港中環花園道33樓`
4. 保存（自动保存）

### 步骤 2: 导出Excel
1. 点击 **Export** 按钮
2. 选择 **Excel (.xlsx)**
3. 打开下载的文件

### 步骤 3: 验证 BankAddress 列
打开Excel文件，检查 **D列 (BankAddress)**:

**预期结果**:
- ✅ 每一行的 `BankAddress` 列应该显示: `香港中環花園道33樓`
- ✅ 不再是空白或旧的默认值

### 步骤 4: 对比验证
| 项目 | 网页显示 | Excel显示 | 状态 |
|-----|---------|-----------|------|
| 分行地址 | `香港中環花園道33樓` | D列: `香港中環花園道33樓` | ✅ 一致 |

---

## 📝 示例数据

### 网页版（图2）:
```
銀行名稱: 中國工商銀行（亞洲）有限公司
銀行代碼: 024, 004
帳戶號碼: 861-512-08367-3
分行地址: 香港中環花園道33樓  ← 这个字段
帳戶持有人: TUG COMPANY LIMITED
```

### Excel版（图1）对应列:
```
Column A: CustomerName = TUG COMPANY LIMITED
Column B: AccountNumber = 861-512-08367-3
Column C: AccountType = Integrated Account
Column D: BankName = 中國工商銀行（亞洲）有限公司
Column E: BankAddress = 香港中環花園道33樓  ← 应该填充这里
```

---

## 🔧 技术细节

### JavaScript 短路求值（||）
```javascript
const bankAddress = data.branchName || data.branch_name || data.bankAddress || data.bank_address || '';
```

**执行逻辑**:
1. 如果 `data.branchName` 存在且非空 → 使用它
2. 否则，如果 `data.branch_name` 存在 → 使用它
3. 否则，如果 `data.bankAddress` 存在 → 使用它
4. 否则，如果 `data.bank_address` 存在 → 使用它
5. 否则 → 使用空字符串 `''`

### 优先级顺序
1️⃣ **最高**: `branchName` (新版本，页面表单)
2️⃣ **次高**: `branch_name` (下划线格式)
3️⃣ **备用**: `bankAddress` (旧版本)
4️⃣ **备用**: `bank_address` (旧版本下划线)

---

## 📁 文件更改总结

| 文件 | 更改内容 | 行数 |
|-----|---------|------|
| `document-detail.html` | 添加 `branchName` 到 `bankAddress` 映射 | ~3007 |
| `document-detail.html` | 添加注释说明优先级 | ~3007 |

---

## 🎯 下一步

1. **立即测试**: 刷新页面，填写分行地址
2. **导出验证**: 导出Excel，检查BankAddress列
3. **数据完整性**: 确认所有14列都正确填充

---

## ✅ 完成状态

| 任务 | 状态 |
|-----|------|
| 识别字段映射问题 | ✅ 完成 |
| 添加 branchName 映射 | ✅ 完成 |
| 添加向后兼容性 | ✅ 完成 |
| 测试文档 | ✅ 完成 |

---

## 🔗 相关文档
- `✅_Excel导出和字段名称修复_2026-01-21.md` - Excel导出格式说明
- `✅_账户信息和按钮布局优化_2026-01-16.md` - 分行地址字段添加

---

**创建时间**: 2026-01-21  
**作者**: VaultCaddy AI Assistant  
**相关文件**: `document-detail.html`
