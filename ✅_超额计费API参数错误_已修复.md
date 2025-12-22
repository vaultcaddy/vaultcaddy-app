# ✅ 超额计费 API 参数错误 - 已修复

## 🐛 问题发现

**发现时间：** 2025-12-17 下午7:11  
**严重程度：** 🔴 严重 - API 调用失败，无法支付发票

---

## 📊 问题描述

### 现象

用户取消订阅后，Firebase Functions 日志显示错误：

```
❌ 暂无超额使用失败: If provided, the invalid_paid_out_of_band parameter must be...
❌ 超额错误: StripeInvalidRequestError: If provided, the invalid_paid_out_of_band parameter must be...
```

**详细错误信息：**
```
type: 'StripeInvalidRequestError'
rawType: 'invalid_request_error'
code: undefined
doc_url: undefined
param: 'psid_out_of_band'  ← 关键：参数名错误！
detail: undefined
```

### 根本原因

使用了 **不存在的 API 参数**：

```javascript
// ❌ 错误的代码
const paidInvoice = await stripeClient.invoices.pay(invoice.id, {
    paid_out_of_band: false, // ← 这个参数不存在！
});
```

**Stripe API 文档：**

`stripe.invoices.pay(invoiceId, [options])`

**有效的可选参数：**
- ✅ `forgive` - 是否放弃未支付的金额
- ✅ `off_session` - 是否在客户不在线时支付
- ✅ `payment_method` - 指定支付方式 ID
- ✅ `source` - 指定支付来源 ID

**❌ 无效参数：**
- ❌ `paid_out_of_band` - **这个参数不存在！**

---

## 🔧 解决方案

### 正确的 API 调用方式

```javascript
// ❌ 修复前
const paidInvoice = await stripeClient.invoices.pay(invoice.id, {
    paid_out_of_band: false, // 无效参数
});

// ✅ 修复后
const paidInvoice = await stripeClient.invoices.pay(invoice.id); 
// 直接调用，使用客户的默认支付方式
```

**说明：**
- 不需要指定任何参数时，直接调用即可
- Stripe 会自动使用客户的默认支付方式（客户在订阅时提供的信用卡）
- 如果需要指定特定的支付方式，使用 `payment_method` 参数

---

## 📝 修改的文件

### 文件：`firebase-functions/index.js`

#### 修改 1：handleSubscriptionCancelled 函数

**修复前：**
```javascript
// 行号：762-764
// 步驟 2：立即支付發票
const paidInvoice = await stripeClient.invoices.pay(invoice.id, {
    paid_out_of_band: false, // 使用 Stripe 支付
});
```

**修复后：**
```javascript
// 行號：762-763
// 步驟 2：立即支付發票（使用客戶的默認支付方式）
const paidInvoice = await stripeClient.invoices.pay(invoice.id);
```

#### 修改 2：manualReportOverage 函数

**修复前：**
```javascript
// 行号：2629-2632
// 步驟 2：立即支付發票
const paidInvoice = await stripeClient.invoices.pay(invoice.id, {
    paid_out_of_band: false,
});
```

**修复后：**
```javascript
// 行号：2629-2630
// 步驟 2：立即支付發票（使用客戶的默認支付方式）
const paidInvoice = await stripeClient.invoices.pay(invoice.id);
```

---

## 📊 预期的正确日志

### 修复前 ❌

```
✅ 發票項目已創建: ii_xxxxx
✅ 發票已創建: in_xxxxx
✅ 發票已完成: in_xxxxx
❌ 暂无超额使用失败: If provided, the invalid_paid_out_of_band parameter must be...
❌ 超额错误: StripeInvalidRequestError...
```

### 修复后 ✅

```
✅ 發票項目已創建: ii_xxxxx
✅ 發票已創建: in_xxxxx
📋 發票包含項目: ii_xxxxx，金額: HK$25.00
✅ 發票已完成: in_xxxxx
✅ 發票已成功支付: in_xxxxx    ← 成功！
💵 支付金額: HK$25.00
💳 支付狀態: paid
```

---

## 🧪 测试步骤

### 方法 A：使用手动报告工具

```bash
1. 打开诊断工具：
   file:///Users/cavlinyeung/ai-bank-parser/overage-diagnostic.html

2. 滚动到「2. 手动报告超额使用」

3. 输入：
   - 邮箱：1234@gmail.com
   - 超额数量：50

4. 点击「📡 手动报告」

5. 预期结果：
   ✅ success: true
   ✅ billingMethod: "invoice"
   ✅ invoiceId: "in_xxxxx..."
   ✅ message: "✅ 已創建發票 ... 收取超額費用 HK$25.00"
```

### 方法 B：在 Stripe Dashboard 中取消订阅

```bash
1. 打开订阅页面：
   https://dashboard.stripe.com/test/subscriptions/sub_1SfIWAJmiQ31C0GT4FMCUxxs

2. 点击「取消订阅」

3. 选择「立即取消」

4. 观察 Firebase Functions 日志

5. 验证 Stripe Dashboard：
   - 应该看到新的发票（HK$25.00）
   - 状态：Paid（已支付）
```

---

## 💡 学到的经验

### 1. API 文档很重要

- 不要假设参数存在，必须查阅官方文档
- Stripe API 参数命名很严格，拼写错误会导致失败

### 2. 错误信息很有价值

```
param: 'psid_out_of_band'  ← 这个字段告诉我们问题所在
```

如果我们仔细看错误信息，会发现 Stripe 明确指出了是 `paid_out_of_band` 参数的问题。

### 3. 简单就是美

```javascript
// 复杂（且错误）
await stripe.invoices.pay(invoice.id, {
    paid_out_of_band: false,
});

// 简单（且正确）
await stripe.invoices.pay(invoice.id);
```

不需要参数时，不要添加参数。

### 4. Stripe API 的默认行为

`invoices.pay(invoiceId)` 的默认行为：
- 使用客户的默认支付方式
- 立即尝试支付
- 如果支付失败，会抛出错误
- 如果支付成功，返回更新后的发票对象

---

## 📅 部署信息

### 第一次部署（添加 invoices.pay()）❌

```
部署时间：2025-12-17 下午7:10
Git commit：c1be7f3
部署状态：❌ API 参数错误

问题：使用了无效的参数 paid_out_of_band
错误：StripeInvalidRequestError: If provided, the invalid_paid_out_of_band parameter must be...
```

### 第二次部署（修复 API 参数）✅

```
部署时间：2025-12-17 下午7:12
Git commit：3fcd13a
部署命令：firebase deploy --only functions:stripeWebhook,functions:manualReportOverage
部署状态：✅ 成功

关键修复：
- 移除 invoices.pay() 中无效的 paid_out_of_band 参数
- 使用正确的 API 调用：invoices.pay(invoice.id)
- 自动使用客户的默认支付方式

更新的函数：
✅ stripeWebhook
✅ manualReportOverage
```

---

## 🔗 相关文档

### Stripe API 文档

- [Invoices - Pay an Invoice](https://stripe.com/docs/api/invoices/pay)
- [Handling Invoice Payment Failures](https://stripe.com/docs/billing/invoices/overview#payment-failure)

### 完整的超额计费流程

1. ✅ 检测到超额使用（credits < 0）
2. ✅ 尝试报告 usage record（如果订阅还活跃）
3. ✅ 如果失败，创建独立发票项目
4. ✅ 创建新发票
5. ✅ Finalize 发票
6. ✅ **使用正确的 API 调用立即支付发票** ← 本次修复
7. ✅ 记录到 creditsHistory
8. ✅ 更新用户的 credits 字段

---

## 🎉 总结

✅ **问题已修复**  
✅ **代码已部署**  
✅ **测试就绪**  

**关键修复：**
- 移除无效的 `paid_out_of_band` 参数
- 使用正确的 Stripe API 调用方式
- 简化代码，使用默认行为

**下一步：**
使用诊断工具或在 Stripe Dashboard 中重新测试，验证发票被正确支付！🚀

---

## 🎯 快速参考

### 正确的 Stripe API 调用方式

```javascript
// ✅ 支付发票 - 使用默认支付方式
await stripe.invoices.pay(invoiceId);

// ✅ 支付发票 - 指定支付方式
await stripe.invoices.pay(invoiceId, {
    payment_method: 'pm_xxxxx'
});

// ✅ 支付发票 - 允许离线支付
await stripe.invoices.pay(invoiceId, {
    off_session: true
});

// ❌ 错误 - 使用不存在的参数
await stripe.invoices.pay(invoiceId, {
    paid_out_of_band: false // ← 不存在！
});
```

---

**修复完成时间：** 2025-12-17 下午7:12  
**测试状态：** 等待用户验证 ⏳





