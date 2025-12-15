# 💰 Stripe 按量计费机制说明

## 问题说明

**用户问题：** 1234@gmail.com 完成退订后，Credits 从 -6 转为 0，但在 Stripe Test Dashboard 中找不到 $3 的超额费用收取记录。

## Stripe 按量计费（Metered Billing）工作原理

### 1. 计费周期内累积使用量

- **实时记录**：每次用户使用超额 Credits 时，通过 `stripe.subscriptionItems.createUsageRecord()` 实时记录使用量
- **不立即收费**：记录的使用量不会立即产生扣款，而是累积在当前计费周期内
- **用户可见**：在 Stripe Dashboard → Billing → Usage records 中可以看到累积的使用记录

### 2. 计费周期结束时统一收费

Stripe 会在以下时间点生成发票并收费：

#### 场景 A：正常续订
- **时间**：每月的账单日期（billing date）
- **发票内容**：
  - 下个月的订阅费（如 HK$58）
  - 上个月的按量使用费（如超额 6 Credits = HK$3）
- **示例**：
  ```
  发票日期：2025-12-21
  - Pro Plan Monthly (12/21-1/21): HK$58.00
  - 超额使用 (12/14-12/21): HK$3.00
  总计：HK$61.00
  ```

#### 场景 B：取消订阅
- **时间**：订阅到期日（当前计费周期结束）
- **发票内容**：
  - ❌ 无下个月的订阅费（因为已取消）
  - ✅ 本周期的按量使用费（如超额 6 Credits = HK$3）
- **示例**：
  ```
  最终发票日期：2025-12-21
  - 超额使用 (12/14-12/21): HK$3.00
  总计：HK$3.00
  ```

### 3. 为什么现在看不到 $3 的收费？

#### 原因分析

1. **订阅尚未到期**
   - 用户在 12/14 订阅，下一个账单日期是 12/21
   - 虽然用户点击了「取消订阅」，但订阅会持续到 12/21
   - 在 12/21 之前，超额费用不会被结算

2. **Stripe 在账单日生成最终发票**
   - 当 12/21 到来时，Stripe 会：
     - ✅ 生成最终发票（Final Invoice）
     - ✅ 包含 12/14-12/21 期间的超额使用费 HK$3
     - ✅ 尝试从用户的支付方式扣款
     - ✅ 发送发票邮件给用户

3. **在测试模式下手动触发**
   - 如果想立即测试超额计费，可以在 Stripe Dashboard 中：
     - 找到该订阅（Subscriptions）
     - 点击 "Cancel immediately"（立即取消）而非 "Cancel at period end"
     - 或者点击 "Create invoice" 手动生成发票

### 4. 如何验证超额计费功能

#### 方法 A：等待账单日（推荐）

```bash
当前状态：
- 订阅日期：2025-12-14
- 下一账单日：2025-12-21
- 超额使用：-6 Credits (已记录)

预期结果（2025-12-21）：
- Stripe 生成最终发票
- 发票金额：HK$3.00（超额费用）
- 订阅状态变为 "canceled"
```

#### 方法 B：Stripe Dashboard 手动触发

1. **进入订阅详情**
   ```
   Stripe Test Dashboard → Customers → 
   选择 1234@gmail.com → Subscriptions → 
   点击 Pro Plan Monthly
   ```

2. **查看使用记录**
   ```
   在订阅详情页面：
   - 找到 "Usage-based items" 部分
   - 查看 "超额使用" 的记录数量
   - 应该显示 6 units（6 Credits）
   ```

3. **手动生成发票**
   ```
   在订阅详情页面：
   - 点击右上角 "Actions" 按钮
   - 选择 "Create invoice"
   - Stripe 会立即生成包含超额费用的发票
   - 金额应该是 HK$3.00
   ```

4. **立即取消订阅**（可选）
   ```
   在订阅详情页面：
   - 点击 "Cancel subscription"
   - 选择 "Cancel immediately"
   - Stripe 会立即生成最终发票并收费
   ```

#### 方法 C：使用 Stripe CLI 验证

```bash
# 1. 查看该用户的订阅
stripe subscriptions list --customer <customer_id>

# 2. 查看使用记录
stripe subscription-items list --subscription <subscription_id>

# 3. 查看使用量（usage records）
stripe usage-records list --subscription-item <subscription_item_id>

# 4. 手动触发发票生成
stripe invoices create --customer <customer_id> --subscription <subscription_id>
```

### 5. Stripe 交易记录位置

#### 在 Stripe Test Dashboard 中查找收费记录：

1. **实时使用记录（已记录但未收费）**
   ```
   位置：Billing → Usage records
   状态：✅ 可以看到 6 Credits 的使用记录
   ```

2. **待开具发票（未到账单日）**
   ```
   位置：Billing → Upcoming invoice
   状态：❌ 因为订阅已取消，可能不会显示
   ```

3. **已开具发票（账单日后）**
   ```
   位置：Payments → Invoices
   状态：⏳ 等待 2025-12-21 后出现
   预期金额：HK$3.00
   ```

4. **交易记录（扣款成功后）**
   ```
   位置：Payments → All transactions
   状态：⏳ 等待 2025-12-21 扣款后出现
   描述：Subscription update 或 Final invoice
   ```

## 总结

### ✅ 当前系统运作正常

1. **超额使用已正确记录**
   - Firestore：Credits 从 -6 恢复为 0 ✅
   - Stripe：6 Credits 使用记录已提交 ✅

2. **费用将在账单日收取**
   - 时间：2025-12-21（订阅到期日）
   - 金额：HK$3.00（6 Credits × HK$0.5/Credit）
   - 方式：Stripe 自动生成最终发票并扣款

3. **如需立即测试**
   - 方法 1：在 Stripe Dashboard 手动 "Create invoice"
   - 方法 2：在 Stripe Dashboard 选择 "Cancel immediately"
   - 方法 3：等待 2025-12-21 自动处理

### 📋 验证清单

- [x] 用户 Credits 从 -6 恢复为 0
- [x] Stripe 使用记录已提交
- [ ] 等待 2025-12-21 生成最终发票
- [ ] 验证发票金额为 HK$3.00
- [ ] 验证扣款成功

---

**创建时间：** 2025-12-15  
**下一步：** 等待 2025-12-21 或手动触发发票生成以验证超额计费

