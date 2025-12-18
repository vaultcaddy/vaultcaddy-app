# ✅ 修复 Checkout Session "Quantity is required" 错误

## 🐛 问题

创建 Stripe Checkout Session 时出现错误：
```
Quantity is required. Add 'quantity' to 'line_items[1]'
```

## 🎯 根本原因

对于使用 **Stripe Billing Meters** 的订阅，我们**不应该在 Checkout Session 中包含 metered price**。

### ❌ 错误的做法
```javascript
line_items: [
    { price: basePriceId, quantity: 1 },  // 基础月费
    { price: usagePriceId }               // ❌ 错误：metered price
]
```

### ✅ 正确的做法
```javascript
line_items: [
    { price: basePriceId, quantity: 1 }   // 只包含基础月费
]
// Billing Meters 会自动关联到订阅
```

---

## ✅ 解决方案

### 修改代码（firebase-functions/index.js 第2243-2264行）

```javascript
const session = await stripeClient.checkout.sessions.create({
    mode: 'subscription',
    line_items: [
        {
            price: selectedPlan.basePriceId,  // 基礎訂閱費（月費/年費）
            quantity: 1
        }
        // ⚠️ 注意：不要在這裡包含 metered price
        // Stripe Billing Meters 會在訂閱創建後自動關聯
    ],
    customer_email: email,
    client_reference_id: userId,
    metadata: {
        userId: userId,
        planType: planType
    },
    success_url: `https://vaultcaddy.com/billing.html?success=true&session_id={CHECKOUT_SESSION_ID}${isTest ? '&test=true' : ''}`,
    cancel_url: `https://vaultcaddy.com/billing.html?canceled=true${isTest ? '&test=true' : ''}`,
    allow_promotion_codes: true,
    billing_address_collection: 'auto'
});
```

---

## 📊 Stripe Billing Meters 工作原理

### 1. 创建订阅
- 只包含**基础价格**（月费 HK$58 或年费 HK$552）
- **不包含** metered price

### 2. 自动关联 Meter
- Stripe 会根据**产品配置**自动关联 Billing Meter
- 或者在 webhook 中手动添加 metered price 到订阅

### 3. 报告使用量
- 通过 `billing.meterEvents.create` API 报告使用量
- Stripe 自动累计并在月底生成账单

### 4. 生成账单
- 基础费用：HK$58（固定）
- 使用量费用：累计使用量 × HK$0.5

---

## 🔧 Stripe Dashboard 配置（重要！）

### 方法1：在产品中配置默认 Meter

1. 打开产品页面：https://dashboard.stripe.com/test/products
2. 找到 "VaultCaddy Monthly"
3. 点击 "Edit product"
4. 在 "Prices" 部分：
   - ✅ 添加基础价格（HK$58）
   - ✅ 添加 metered price（关联到 Billing Meter）
5. 保存

这样，当用户订阅时，Stripe 会**自动**将两个价格都添加到订阅中。

### 方法2：在 Webhook 中手动添加（备选）

如果方法1不可行，我们可以在 `customer.subscription.created` webhook 中手动添加：

```javascript
// 在订阅创建后
const subscription = await stripe.subscriptions.retrieve(subscriptionId);
await stripe.subscriptions.update(subscriptionId, {
    items: [
        ...subscription.items.data,
        { price: usagePriceId }  // 添加 metered price
    ]
});
```

---

## 🚀 已部署

```bash
✔  functions[createStripeCheckoutSession(us-central1)] Successful update operation.
```

---

## 🧪 测试步骤

### 步骤1：测试 Checkout
1. 访问：https://vaultcaddy.com/billing.html
2. 点击 "Get Started"
3. **预期**：成功跳转到 Stripe Checkout 页面

### 步骤2：检查订阅
完成订阅后，在 Stripe Dashboard 检查订阅详情：
- ✅ 应该看到基础价格（HK$58）
- ❓ 检查是否自动添加了 metered price

如果没有自动添加，我们需要使用方法2在 webhook 中手动添加。

---

## 📋 下一步

1. ✅ 测试 Checkout 是否正常工作
2. ❓ 检查订阅是否包含 metered price
3. 如果没有，实现 webhook 自动添加逻辑

---

**请重新测试 Get Started 按钮，应该可以正常打开 Checkout 页面了！** 🚀

