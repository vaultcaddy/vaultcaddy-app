# ✅ 修复 Price ID 映射错误

## 🐛 问题

Stripe Checkout 显示的价格是 **HK$0.50**（usage price），而不是月费 **HK$58**！

**原因**：Price IDs 映射错误，把 base 和 usage 搞反了。

---

## ✅ 正确的 Price ID 映射

### Production Mode（正式版）

#### Monthly（月付）
- **Base Price**（月费）：`price_1SdpzxJmiQ31C0GTLe5rYQn9` → **HK$58/月**
- **Usage Price**（使用量）：`price_1SfNw5JmiQ31C0GT7SHy0t44` → **HK$0.5/Credit**

#### Yearly（年付）
- **Base Price**（年费）：`price_1SdpzxJmiQ31C0GTV0iI5GK6` → **HK$552/年**
- **Usage Price**（使用量）：`price_1SfNvfJmiQ31C0GTFY4bhpzK` → **HK$0.5/Credit**

---

## 🔧 修改的代码

### firebase-functions/index.js（第2206-2215行）

#### ❌ 修改前（错误）
```javascript
const productionPriceMapping = {
    monthly: {
        basePriceId: 'price_1SfNw5JmiQ31C0GT7SHy0t44',  // ❌ 这是 usage price
        usagePriceId: 'price_1SdpzxJmiQ31C0GTLe5rYQn9'  // ❌ 这是 base price
    },
    yearly: {
        basePriceId: 'price_1SfNvfJmiQ31C0GTFY4bhpzK',  // ❌ 这是 usage price
        usagePriceId: 'price_1SdpzxJmiQ31C0GTV0iI5GK6'  // ❌ 这是 base price
    }
};
```

#### ✅ 修改后（正确）
```javascript
const productionPriceMapping = {
    monthly: {
        basePriceId: 'price_1SdpzxJmiQ31C0GTLe5rYQn9',  // ✅ HK$58/月
        usagePriceId: 'price_1SfNw5JmiQ31C0GT7SHy0t44'  // ✅ HK$0.5/Credit
    },
    yearly: {
        basePriceId: 'price_1SdpzxJmiQ31C0GTV0iI5GK6',  // ✅ HK$552/年
        usagePriceId: 'price_1SfNvfJmiQ31C0GTFY4bhpzK'  // ✅ HK$0.5/Credit
    }
};
```

---

## 🚀 已部署

```bash
✔  functions[createStripeCheckoutSession(us-central1)] Successful update operation.
```

---

## 🧪 测试步骤

1. **刷新页面**：https://vaultcaddy.com/billing.html
2. **点击 "Get Started"**
3. **预期**：
   - Monthly 应该显示 **HK$58.00 每月**
   - Yearly 应该显示 **HK$552.00 每年**
   - 不再显示 HK$0.50

---

## 📊 完整的价格结构

### Monthly Plan（月付）
```
订阅价格: HK$58/月（固定）
包含: 100 Credits
Email 赠送: 20 Credits
总免费额度: 120 Credits

超额计费: HK$0.5/Credit（从负数开始收费）
```

### Yearly Plan（年付）
```
订阅价格: HK$552/年（固定，Save 20%）
包含: 1,200 Credits
Email 赠送: 20 Credits
总免费额度: 1,220 Credits

超额计费: HK$0.5/Credit（从负数开始收费）
```

---

## 🎯 关键点

1. ✅ **Base Price**：显示在 Checkout 页面，用户订阅时支付
2. ✅ **Usage Price**：不显示在 Checkout，只在超额时计费
3. ✅ **Billing Meter**：自动累计使用量，月底生成账单

---

**请重新测试 Get Started 按钮，这次应该显示正确的价格了！** 🚀

