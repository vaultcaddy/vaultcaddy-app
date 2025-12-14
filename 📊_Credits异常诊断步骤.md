# 📊 Credits 异常增加诊断步骤

## 🚨 **问题**

用户 `osclin2002@gmail.com` 完成 1 次 Monthly 订阅，但 Credits 显示为 **80070**（应该是 **100**）

---

## 🔍 **诊断步骤**

### **步骤 1：检查 Firestore - processedStripeEvents**

1. 访问 Firebase Console
   ```
   https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/firestore/databases/-default-/data/~2FprocessedStripeEvents?hl=zh-cn
   ```

2. 查看最近的事件
   - 检查是否有**大量** `checkout.session.completed` 事件
   - 检查事件 ID 是否重复
   - 检查时间戳是否异常（同一秒内大量事件）

3. 预期结果
   - ✅ **正常**：只有 1 个 `checkout.session.completed` 事件
   - ❌ **异常**：有 800+ 个相同的 `checkout.session.completed` 事件

---

### **步骤 2：检查 Stripe Dashboard - Webhook 日志**

1. 访问 Stripe Webhook 日志
   ```
   https://dashboard.stripe.com/test/workbench/webhooks
   ```

2. 查找最近的 `checkout.session.completed` 事件
   - 点击进入事件详情
   - 查看"Webhook attempts"部分
   - 检查发送次数

3. 预期结果
   - ✅ **正常**：只发送 1 次，返回 200 OK
   - ❌ **异常**：发送了多次（可能是 500 错误导致重试）

---

### **步骤 3：检查用户 Credits 历史**

1. 访问 Firestore
   ```
   https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/firestore/databases/-default-/data/~2Fusers?hl=zh-cn
   ```

2. 找到 `osclin2002@gmail.com` 的文档
3. 点击 `creditsHistory` 子集合
4. 查看有多少条"添加 Credits"记录

5. 预期结果
   - ✅ **正常**：只有 1 条添加 100 Credits 的记录
   - ❌ **异常**：有 800+ 条重复的添加记录

---

### **步骤 4：检查 Stripe Webhook 配置**

1. 访问 Webhook 配置
   ```
   https://dashboard.stripe.com/test/webhooks
   ```

2. 检查是否有**多个** webhook endpoint 指向同一个 URL
   ```
   https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/stripeWebhook
   ```

3. 预期结果
   - ✅ **正常**：只有 1 个 webhook endpoint
   - ❌ **异常**：有多个 webhook endpoint（可能导致重复调用）

---

### **步骤 5：查看 Firebase Functions 日志**

1. 访问 Functions 日志
   ```
   https://console.firebase.google.com/u/1/project/vaultcaddy-production-cbbe2/functions/logs?hl=zh-cn
   ```

2. 筛选 `stripeWebhook` 函数的日志
3. 搜索 `checkout.session.completed`
4. 查看是否有大量重复的日志

5. 预期结果
   - ✅ **正常**：只有 1 条 "✅ 結帳完成" 日志
   - ❌ **异常**：有 800+ 条相同的日志

---

## 🔧 **可能的原因**

### **原因 1：Idempotency 检查失效**

如果 `processedStripeEvents.create()` 失败（例如网络问题），可能导致：

```javascript
// 第1次请求：成功创建文档，处理事件，添加 100 Credits
// 第2次请求：网络延迟，create() 认为文档不存在，再次处理，添加 100 Credits
// ...
// 第800次请求：重复处理
```

**解决方法**：改进 idempotency 检查，使用事务（transaction）

---

### **原因 2：Stripe Webhook 重试**

如果 Cloud Function 返回 500 错误，Stripe 会自动重试：

```
1. Stripe 发送 checkout.session.completed
2. Cloud Function 处理时抛出错误，返回 500
3. Stripe 认为失败，自动重试
4. Stripe 再次发送 checkout.session.completed
5. 重复 800 次...
```

**解决方法**：确保所有错误都被捕获，总是返回 200

---

### **原因 3：多个 Webhook Endpoint**

如果在 Stripe Dashboard 中配置了多个 webhook endpoint 指向同一个 URL：

```
Webhook 1: https://...cloudfunctions.net/stripeWebhook
Webhook 2: https://...cloudfunctions.net/stripeWebhook (重复)
...
Webhook 800: https://...cloudfunctions.net/stripeWebhook (重复)
```

**解决方法**：删除重复的 webhook endpoint

---

### **原因 4：测试模式和生产模式混用**

如果同一个支付同时触发了测试和生产模式的 webhook：

```
测试模式 webhook → 添加 100 Credits
生产模式 webhook → 添加 100 Credits
...（如果配置混乱，可能重复多次）
```

**解决方法**：确保测试和生产模式分离

---

## 🎯 **紧急修复流程**

### **第 1 步：手动修正 Credits**

1. 访问 Firebase Console
2. 找到用户文档
3. 修改字段：
   - `credits`: 80070 → **100**
   - `currentCredits`: 80070 → **100**
   - `totalCreditsUsed`: ??? → **0**
   - `includedCredits`: ??? → **100**

### **第 2 步：诊断根本原因**

按照上面的"诊断步骤"逐一检查：
1. ✅ 检查 processedStripeEvents
2. ✅ 检查 Stripe Webhook 日志
3. ✅ 检查 Credits 历史
4. ✅ 检查 Webhook 配置

### **第 3 步：删除重复的事件记录**

如果在 `processedStripeEvents` 中发现大量重复事件：

1. 在 Firebase Console 中批量删除
2. 或者创建清理脚本

### **第 4 步：删除重复的 Webhook Endpoint**

如果在 Stripe Dashboard 中发现多个 webhook：

1. 删除所有重复的
2. 只保留 1 个

---

## 📝 **需要您提供的信息**

为了准确诊断，请截图以下内容：

1. **Firestore - processedStripeEvents 集合**
   - 显示最近的 10-20 个事件
   - 特别注意 `checkout.session.completed` 的数量

2. **Stripe Dashboard - Webhook 日志**
   - 显示最近的 webhook 调用
   - 特别注意返回状态码（200 还是 500）

3. **Firestore - creditsHistory 集合**
   - 显示 `osclin2002@gmail.com` 用户的 Credits 历史
   - 特别注意有多少条"添加 Credits"记录

4. **Stripe Dashboard - Webhook 配置**
   - 显示所有的 webhook endpoints
   - 检查是否有重复

---

## ⚠️ **临时解决方案**

在找到根本原因前，您可以：

1. **立即手动修正 Credits**
   - Firebase Console → users → osclin2002@gmail.com
   - credits: 80070 → 100
   - currentCredits: 80070 → 100

2. **清空 processedStripeEvents**
   - 删除所有测试事件记录
   - 避免污染数据

3. **暂时禁用测试**
   - 等待诊断完成后再测试
   - 避免继续产生异常数据

---

**🚨 这是一个严重 bug，需要立即诊断和修复！**  
**请先手动修正 Credits，然后提供上述截图以便诊断！**

