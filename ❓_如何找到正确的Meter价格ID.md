# ❓ 如何找到正确的 Meter 价格 ID

## 🎯 我们需要的价格

### ✅ 正确的价格特征：
- **类型**：基于用量（Usage-based / Metered）
- **关联的计费表**：VaultCaddy Credits 使用量 (`vaultcaddy_credit_usage`)
- **梯度定价**：
  - 第1层：0-100 → HK$0.00
  - 第2层：101+ → HK$0.50
- **描述**：超额 Credits 按量计费

### ❌ 不是这个（固定月费）：
- Price ID: `price_1Sdn7oJmiQ31C0GT8BSefS3u`
- 类型：固定价格
- 金额：HK$58/月
- 描述：月费基础价格

---

## 📋 在 Stripe Dashboard 中查找

### 步骤1：打开产品页面
访问：https://dashboard.stripe.com/test/products/prod_RljqP7IVFKJmWc

### 步骤2：查看价格列表
在"价格"部分，你应该看到**多个价格**：

```
价格列表：
├── HK$58.00 / 月                    ← 这是固定月费（不是我们要的）
│   Price ID: price_1Sdn7oJmiQ31C0GT8BSefS3u
│
└── 超价为HK$0.00 每 1 单位 / 每 1 个月   ← 这是 Meter 计费（我们要的！）
    Price ID: price_xxxxxxxxxxxxxxxx  ← 需要这个！
    类型：基于用量
    计费表：VaultCaddy Credits 使用量
```

### 步骤3：复制 Meter 价格的 ID
1. 找到显示"基于用量"或"超价为HK$0.00"的那一行
2. 点击该价格
3. 在详情页右上角复制完整的 Price ID

---

## 🔍 如何区分两种价格

| 特征 | 固定月费 | Meter 计费（我们要的）|
|------|----------|---------------------|
| **显示金额** | HK$58.00 / 月 | 超价为HK$0.00 / 单位 |
| **类型** | 固定 (Fixed) | 基于用量 (Metered) |
| **计费表** | 无 | VaultCaddy Credits 使用量 |
| **梯度定价** | 无 | 有（0-100, 101+） |

---

## ❓ 如果找不到 Meter 价格

**可能原因**：还没有创建基于 Meter 的价格

**解决方案**：
1. 在产品页面点击"Add another price"（添加另一个价格）
2. 选择"Usage is metered"（按使用量计费）
3. 选择计费表："VaultCaddy Credits 使用量"
4. 配置梯度定价：
   - 第1层：0-100 → HK$0.00
   - 第2层：101+ → HK$0.50
5. 点击"Create price"
6. 复制新创建的 Price ID

---

## 📸 如何确认是正确的价格

正确的 Meter 价格详情页应该显示：

```
类型：基于用量
计费表：VaultCaddy Credits 使用量
事件名称：vaultcaddy_credit_usage
Meter ID：mtr_test_61TnAddrAuQxlRy7p41JmiQ31C0GTJwG

价格：
第一个单位        最后一个单位      每单位          固定费用
0               100            HK$ 0.00        HK$ 0
101             ∞              HK$ 0.50        HK$ 0
```

如果看到这些信息，说明你找对了！复制页面右上角的 Price ID 即可。





