# 🔧 billing.html 配置更新指南

## 📋 需要更新的文件
- `billing.html`
- `account.html`（如果也有 Stripe Checkout 配置）

---

## 🎯 等待用户提供的信息

### 新的 Price ID
创建完 Meter 价格后，Stripe 会生成一个新的 Price ID，格式类似：
```
price_xxxxxxxxxxxxxxxxxxxxx
```

**示例**：`price_1SeXXXJmiQ31C0GTxxxxxxxx`

---

## 🔧 修改步骤

### 1. 打开 `billing.html`

在文件中找到 Stripe Checkout 配置（大约在行800-900）：

```javascript
const sessionResponse = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: headers,
    body: new URLSearchParams({
        'line_items[0][price]': 'price_1SeCWBJmiQ31C0GTmZ1gxqXa',
        'line_items[0][quantity]': '1',
        // ... 其他参数
    })
});
```

---

### 2. 修改为双订阅项配置

**旧配置**（单一价格）：
```javascript
body: new URLSearchParams({
    'line_items[0][price]': 'price_1SeCWBJmiQ31C0GTmZ1gxqXa',
    'line_items[0][quantity]': '1',
    // ...
})
```

**新配置**（固定月费 + Meter 计费）：
```javascript
body: new URLSearchParams({
    // 订阅项 1：固定月费（HK$58，包含100 Credits）
    'line_items[0][price]': 'price_1SeCWBJmiQ31C0GTmZ1gxqXa',
    'line_items[0][quantity]': '1',
    
    // 订阅项 2：超额计费（基于 Billing Meter）
    'line_items[1][price]': 'price_NEW_METER_PRICE_ID', // 🔥 替换为新的 Price ID
    
    // ... 其他参数保持不变
})
```

---

### 3. 完整示例（待替换 Price ID）

```javascript
async function createCheckoutSession(planType, isTestMode) {
    const stripe_key = isTestMode ? 
        'sk_test_51S6Qv3JmiQ31C0GTbiGaoNjEugsCskHfhma2MAZChrenTpiag7WEsxkbjwPmLwEamsWdYdUGr05uagoLVEnq9g5N00RQU4012q' :
        'sk_live_YOUR_LIVE_KEY';
    
    const headers = {
        'Authorization': `Bearer ${stripe_key}`,
        'Content-Type': 'application/x-www-form-urlencoded'
    };
    
    const user = firebase.auth().currentUser;
    if (!user || !user.email) {
        throw new Error('请先登录');
    }
    
    const sessionResponse = await fetch('https://api.stripe.com/v1/checkout/sessions', {
        method: 'POST',
        headers: headers,
        body: new URLSearchParams({
            'mode': 'subscription',
            'customer_email': user.email,
            
            // 🔥 订阅项 1：固定月费
            'line_items[0][price]': 'price_1SeCWBJmiQ31C0GTmZ1gxqXa',
            'line_items[0][quantity]': '1',
            
            // 🔥 订阅项 2：Meter 计费（超额部分）
            'line_items[1][price]': 'price_NEW_METER_PRICE_ID', // ← 替换这里！
            
            'success_url': 'https://vaultcaddy.com/billing.html?session_id={CHECKOUT_SESSION_ID}&success=true',
            'cancel_url': 'https://vaultcaddy.com/billing.html?canceled=true',
            'metadata[userId]': user.uid,
            'metadata[planType]': planType,
            'metadata[isTestMode]': isTestMode.toString(),
            
            // 允许促销代码
            'allow_promotion_codes': 'true',
            
            // 订阅数据
            'subscription_data[metadata][userId]': user.uid,
            'subscription_data[metadata][planType]': planType
        })
    });
    
    const sessionData = await sessionResponse.json();
    
    if (!sessionResponse.ok) {
        console.error('创建 Stripe Session 失败:', sessionData);
        throw new Error(sessionData.error?.message || 'Failed to create checkout session');
    }
    
    return sessionData;
}
```

---

## 🎯 完整替换步骤

### 步骤 1：获取新的 Price ID
在 Stripe Dashboard 中创建完 Meter 价格后：
1. 点击新创建的价格
2. 复制 Price ID（格式：`price_xxxxx`）

### 步骤 2：全局搜索替换
在项目中搜索所有 Stripe Checkout 配置，替换为新的双订阅项配置。

**需要检查的文件**：
- `billing.html`
- `account.html`
- 其他可能包含 Stripe Checkout 的页面

### 步骤 3：测试模式 vs 生产模式

⚠️ **重要**：测试模式和生产模式需要不同的 Price ID！

**测试模式 Price ID**：
```javascript
const TEST_METER_PRICE_ID = 'price_test_xxxxx'; // 从测试模式获取
```

**生产模式 Price ID**（稍后创建）：
```javascript
const LIVE_METER_PRICE_ID = 'price_live_xxxxx'; // 从生产模式获取
```

**动态选择**：
```javascript
const meterPriceId = isTestMode ? TEST_METER_PRICE_ID : LIVE_METER_PRICE_ID;

body: new URLSearchParams({
    'line_items[0][price]': 'price_1SeCWBJmiQ31C0GTmZ1gxqXa',
    'line_items[0][quantity]': '1',
    'line_items[1][price]': meterPriceId, // 动态选择
    // ...
})
```

---

## 📝 检查清单

- [ ] 用户已提供测试模式的 Meter Price ID
- [ ] 已在 `billing.html` 中添加第二个订阅项配置
- [ ] 已使用正确的 Price ID 替换 `price_NEW_METER_PRICE_ID`
- [ ] 已测试 Stripe Checkout 流程
- [ ] 已确认订阅创建成功
- [ ] 已在 Stripe Dashboard 确认订阅包含两个订阅项
- [ ] 稍后在生产模式中创建相同配置的 Meter 和 Price

---

## 🆘 如果遇到问题

### 问题1：Checkout 失败
**可能原因**：Price ID 不正确或不存在

**解决方案**：
1. 在 Stripe Dashboard 中验证 Price ID
2. 确认 Price ID 是否属于正确的模式（测试 vs 生产）

### 问题2：订阅只包含固定月费
**可能原因**：第二个订阅项配置不正确

**解决方案**：
1. 检查 `line_items[1][price]` 是否正确设置
2. 在浏览器开发者工具中查看 API 请求参数

### 问题3：Meter Events 未记录
**可能原因**：Meter 配置与 Price 不匹配

**解决方案**：
1. 在 Stripe Dashboard 确认 Price 关联到正确的 Meter
2. 检查 Meter Event Name 是否为 `vaultcaddy_credit_usage`

---

## 🎉 完成后

一旦用户提供 Price ID，立即：
1. 更新 `billing.html`
2. 部署 Firebase Functions
3. 创建测试订阅
4. 验证 Meter Events 是否正常记录





