# 🎯 创建 Meter 价格配置指南

## 背景
现在我们已经创建了 Billing Meter (`mtr_test_61TnAddrAuQxlRy7p41JmiQ31C`)，需要创建一个新的价格配置，关联到这个 Meter。

---

## 第2步：创建新的价格配置

### 方法1：在产品页面添加新价格（推荐）

1. **打开产品页面**
   👉 https://dashboard.stripe.com/test/products/prod_RljqP7IVFKJmWc
   
2. **点击 "Add another price"（添加另一个价格）**

3. **配置价格**

#### 3.1 Pricing model（定价模式）
选择：**Usage is metered（按使用量计费）**

#### 3.2 Billing meter（计费表）
选择：**VaultCaddy Credits 使用量** (`vaultcaddy_credit_usage`)

⚠️ 这就是我们刚创建的 Meter！

#### 3.3 Price（价格）
选择：**Graduated pricing（梯度定价）**

配置层级：
```
第1层（Tier 1）:
- Up to: 100
- Unit price: HK$0.00

第2层（Tier 2）:
- Up to: Infinity（无限）
- Unit price: HK$0.50
```

💡 这意味着：
- 前100个 Credits：免费（月费包含）
- 第101个开始：每个 HK$0.50

#### 3.4 Billing period（计费周期）
选择：**Monthly（每月）**

#### 3.5 Currency（货币）
选择：**HKD（港币）**

---

### 方法2：创建全新的产品+价格

如果你想创建一个全新的产品（而不是在现有产品上添加价格），可以：

1. 打开：https://dashboard.stripe.com/test/products/create
2. 配置产品名称：`VaultCaddy Pro（新版）`
3. 然后按照上面的步骤配置价格

⚠️ **建议**：使用方法1，保持现有产品不变

---

## 创建后需要的信息

创建完成后，请记录：

1. **Price ID**（类似 `price_xxxxx`）
   - 这是新创建的价格 ID
   - 需要更新到 `billing.html` 中

2. **订阅配置**
   - 月费部分：保持现有的固定价格 `price_1SeCWBJmiQ31C0GTmZ1gxqXa`（HK$58）
   - 超额部分：新的 Meter 价格 ID

---

## ⚠️ 重要配置说明

### 现有订阅架构
```
订阅包含2个订阅项：
1. 固定月费项（HK$58/月，包含100 Credits）
   - Price ID: price_1SeCWBJmiQ31C0GTmZ1gxqXa
   
2. 超额计费项（新）
   - Price ID: 待创建（基于 Meter）
   - 前100个：HK$0（因为已包含在月费中）
   - 第101+个：HK$0.50/个
```

### 新订阅创建时的配置
在 `billing.html` 中，我们需要修改 Stripe Checkout 配置：

```javascript
lineItems: [
  {
    price: 'price_1SeCWBJmiQ31C0GTmZ1gxqXa', // 固定月费
    quantity: 1
  },
  {
    price: 'price_NEW_METER_PRICE_ID', // 新的 Meter 价格
    // 不需要 quantity，因为是按使用量计费
  }
]
```

---

## 测试计划

创建价格后，我们会：

1. ✅ 创建测试订阅
2. ✅ 上传文档（扣除 Credits）
3. ✅ 验证 Meter Events 已发送到 Stripe
4. ✅ 模拟超额使用（修改 Firestore 数据）
5. ✅ 触发计费，确认发票金额正确
6. ✅ 测试订阅取消，确认超额费用已收取

---

## 下一步

请在 Stripe Dashboard 中：
1. 点击 "Add another price"
2. 按照上面的配置填写
3. 创建完成后，告诉我新的 **Price ID**

我会立即更新代码配置！



