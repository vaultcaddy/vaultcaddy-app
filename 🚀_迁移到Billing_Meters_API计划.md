# 🚀 迁移到 Stripe Billing Meters API 计划

## 背景
原有的 Usage Records API 方法一直存在时序问题，无法稳定地在订阅取消时收取超额费用。现在迁移到更稳定的 **Billing Meters API**（虽然是 Beta 版，但功能更强大）。

---

## 📋 实施步骤

### 第1步：在 Stripe 创建 Billing Meter

1. **登录 Stripe Dashboard**
   - 测试模式：https://dashboard.stripe.com/test/billing/meters
   - 生产模式：https://dashboard.stripe.com/billing/meters

2. **创建新的 Billing Meter**
   ```
   Event Name: vaultcaddy_credit_usage
   Display Name: VaultCaddy Credits Usage
   Aggregation: Sum
   Value Settings: Count occurrences
   ```

3. **记录 Meter ID**
   - 创建后会得到类似 `mtr_xxxxx` 的 ID
   - 需要在代码中使用这个 ID

---

### 第2步：更新 Stripe 价格配置

1. **创建新的价格对象**（关联到 Billing Meter）
   - 在 Stripe Dashboard 中创建新价格
   - 选择 "Based on usage" → "Metered billing" → 选择刚创建的 Meter
   - 配置梯度定价：
     ```
     0-100: HK$0
     101+: HK$0.50/credit
     ```

2. **更新产品配置**
   - 将新价格添加到现有产品
   - 暂时保留旧价格（用于已有订阅）

---

### 第3步：修改 Firebase Functions 代码

#### 3.1 修改 `deductCredits` 函数

**旧代码**（使用 totalCreditsUsed）：
```javascript
// 更新累计使用量（用于超额计费）
updateData.totalCreditsUsed = admin.firestore.FieldValue.increment(amount);
```

**新代码**（发送 Meter Event）：
```javascript
// 发送 Billing Meter Event 到 Stripe
if (userData.stripeCustomerId) {
  const stripeClient = userData.isTestMode ? stripe_test : stripe_live;
  
  await stripeClient.billing.meterEvents.create({
    event_name: 'vaultcaddy_credit_usage',
    payload: {
      stripe_customer_id: userData.stripeCustomerId,
      value: amount.toString()
    },
    timestamp: Math.floor(Date.now() / 1000)
  });
  
  console.log(`✅ 已发送 ${amount} Credits 使用量到 Stripe Billing Meter`);
}
```

#### 3.2 移除旧的 webhook 处理逻辑

**需要删除或简化的函数**：
- `handleInvoiceCreated` 中的超额检测和 `createUsageRecord` 逻辑
- `handleSubscriptionCancelled` 中的所有计费逻辑
- `manualReportOverage` 函数（不再需要）

#### 3.3 更新 `handleCheckoutCompleted` 函数

**移除字段**：
- `meteredSubscriptionItemId`（不再需要）
- `totalCreditsUsed`（不再需要）

**保留字段**：
- `stripeSubscriptionId`
- `stripeCustomerId`
- `monthlyCredits`

---

### 第4步：测试新系统

#### 4.1 创建测试订阅
1. 使用测试卡 `4242 4242 4242 4242`
2. 完成支付流程
3. 确认 Firestore 数据正确

#### 4.2 测试 Credits 扣除
1. 上传文档（触发 `deductCredits`）
2. 在 Stripe Dashboard 查看 Meter Events
3. 确认事件已记录

#### 4.3 测试超额计费
1. 手动修改 Firestore 数据：
   ```javascript
   users/testUserId:
   - currentCredits: -50
   - credits: -50
   ```
2. 触发计费周期（或手动创建发票）
3. 确认发票中包含超额费用 HK$25.00

#### 4.4 测试订阅取消
1. 立即取消订阅
2. 确认生成了包含超额费用的发票
3. 确认 Credits 重置为 0

---

### 第5步：部署到生产环境

1. **在生产模式 Stripe 中创建相同的 Meter**
2. **更新生产环境价格配置**
3. **部署 Firebase Functions**
   ```bash
   cd firebase-functions
   firebase deploy --only functions
   ```
4. **监控日志**
   - 确认没有错误
   - 确认 Meter Events 正常发送

---

### 第6步：清理工作

1. **删除旧代码**
   - 移除 `createUsageRecord` 相关代码
   - 移除 `totalCreditsUsed` 字段更新逻辑
   - 删除诊断工具 `overage-diagnostic.html`

2. **更新文档**
   - 创建新的 Billing Meters API 使用文档
   - 归档旧的 Usage Records API 文档

3. **通知现有用户**（如果需要）
   - 现有订阅继续使用旧系统
   - 新订阅自动使用新系统
   - 在下次续费时自动迁移

---

## ⚠️ 注意事项

1. **Beta 功能警告**
   - Billing Meters API 目前处于 Beta 阶段
   - API 可能会有变化（但 Stripe 通常会向后兼容）

2. **数据迁移**
   - 现有订阅的 `totalCreditsUsed` 数据可以保留
   - 新系统不会读取这个字段

3. **计费差异**
   - 新系统是**实时报告**使用量
   - 旧系统是**批量报告**（在 webhook 中）
   - 新系统更准确、更可靠

4. **成本考虑**
   - Meter Events API 调用次数可能较多
   - 每次扣除 Credits 都会调用一次 API
   - 但这是 Stripe 推荐的最佳实践

---

## 📊 预期结果

完成迁移后：
- ✅ 每次扣除 Credits 时，实时报告给 Stripe
- ✅ 订阅取消时，自动生成包含超额费用的发票
- ✅ 不再需要复杂的 webhook 时序处理
- ✅ 计费更准确、更可靠

---

## 🕐 预计时间

- **第1步**：15分钟（创建 Meter）
- **第2步**：20分钟（配置价格）
- **第3步**：60分钟（修改代码）
- **第4步**：30分钟（测试）
- **第5步**：15分钟（部署）
- **第6步**：20分钟（清理）

**总计：约2.5小时**

---

## 📚 参考文档

- [Stripe Billing Meters API](https://stripe.com/docs/billing/subscriptions/usage-based/implementation-guide)
- [Meter Events API Reference](https://stripe.com/docs/api/billing/meter-event)
- [从 Usage Records 迁移指南](https://stripe.com/docs/billing/subscriptions/usage-based/migrate-to-meters)

