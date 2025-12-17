# 📝 价格 ID 更新记录

## 更新时间
2025-12-17 下午 9:15

---

## 更新的价格 ID

### 测试模式 - 月费按量计费
**旧 Price ID**（Usage Records API）：
```
price_1Sdn7pJmiQ31C0GTTK1yVopH
```

**新 Price ID**（Billing Meter Events API）：
```
price_15dn7pJmiQ31C0GTK1yVopH
```

**关联的 Meter**：
- Meter ID: `mtr_test_61TnAddrAuQxlRy7p41JmiQ31C0GTJwG`
- Event Name: `vaultcaddy_credit_usage`
- 梯度定价：
  - 0-100: HK$0.00
  - 101+: HK$0.50

---

## 更新的文件

### 1. `firebase-functions/index.js`
**位置**：第2105-2115行

**函数**：`createStripeCheckoutSession`

**修改内容**：
```javascript
const testPriceMapping = {
    monthly: {
        basePriceId: 'price_1Sdn7oJmiQ31C0GT8BSefS3u',
        usagePriceId: 'price_15dn7pJmiQ31C0GTK1yVopH'  // ← 已更新
    },
    yearly: {
        basePriceId: 'price_1SdoMxJmiQ31C0GTsgCDQz8n',
        usagePriceId: 'price_1Sdn7qJmiQ31C0GTwJVp4q4Q'  // ← 保持不变
    }
};
```

---

## ⚠️ 待办事项

### 1. 年费价格
目前年费仍使用旧的 Usage Records API。

**建议**：
- 测试月费成功后，为年费也创建基于 Meter 的价格
- 或者如果不需要年费，可以移除相关代码

---

### 2. 生产模式价格
完成测试后，需要在生产模式中：
1. 创建相同的 Billing Meter
2. 创建相同配置的价格
3. 更新生产模式的 `usagePriceId`

**当前生产模式配置**（待更新）：
```javascript
const productionPriceMapping = {
    monthly: {
        basePriceId: 'price_1SdpzxJmiQ31C0GTLe5rYQn9',
        usagePriceId: 'price_1SdpzxJmiQ31C0GTAXBa4vHG'  // ← 需要更新
    },
    yearly: {
        basePriceId: 'price_1SdpzxJmiQ31C0GTV0iI5GK6',
        usagePriceId: 'price_1SdpzyJmiQ31C0GThRVdmVOH'  // ← 需要更新
    }
};
```

---

## 🎯 下一步

1. ✅ 部署 Firebase Functions
2. ✅ 创建测试订阅
3. ✅ 上传文档测试 Credits 扣除
4. ✅ 在 Stripe Dashboard 查看 Meter Events
5. ✅ 模拟超额使用并验证计费

---

## 📊 新旧系统对比

| 项目 | 旧系统 | 新系统 |
|------|--------|--------|
| **API** | Usage Records API | Billing Meter Events API |
| **Price ID** | `price_1Sdn7pJmiQ31C0GTTK1yVopH` | `price_15dn7pJmiQ31C0GTK1yVopH` |
| **Meter ID** | 无（使用 subscription item） | `mtr_test_61TnAddrAuQxlRy7p41JmiQ31C0GTJwG` |
| **报告方式** | 批量（webhook 中） | 实时（每次扣除） |
| **需要字段** | `meteredSubscriptionItemId` | `stripeCustomerId` |

