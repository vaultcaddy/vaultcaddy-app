# Webhook 配置说明

## ⚠️ 需要修改的配置

### **问题**
当前 Stripe Webhook 监听的事件不正确

### **需要修改**
- ❌ 当前错误：`invoice.payment_succeeded`  
- ✅ 应该使用：`invoice.paid`

### **为什么**
- Firebase Cloud Function 代码监听的是 `invoice.paid`
- 使用错误的事件会导致订阅续费时无法正确添加 Credits

---

## 📋 修改步骤

1. 访问 Stripe Dashboard（生产模式）
   - 网址：https://dashboard.stripe.com/webhooks
   - ⚠️ 确保切换到生产模式

2. 编辑现有的 Webhook（vibrant-splendor）

3. 在事件列表中修改：
   - 取消选择：`invoice.payment_succeeded`
   - 选择：`invoice.paid`

4. 保存接收端点

---

## ✅ 完整事件列表（5个）

确保选择了以下 5 个事件：

```
✅ checkout.session.completed
✅ customer.subscription.created  
✅ customer.subscription.updated
✅ customer.subscription.deleted
✅ invoice.paid
```

---

## 🧪 测试

修改后进行一次真实支付测试，确认 Credits 正确添加。

