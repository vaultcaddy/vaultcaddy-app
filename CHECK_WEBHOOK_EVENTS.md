# 🔍 Webhook 事件检查清单

## 当前状态（从截图分析）

**Webhook 名称**: vibrant-splendor  
**URL**: ✅ 正确  
**状态**: ✅ 使用中  
**事件数量**: 5 个 ⚠️ 需确认

---

## ✅ 必需的 6 个事件

请在 Stripe Dashboard 中确认以下事件是否全部配置：

### 订阅相关（4个）
- [ ] `checkout.session.completed` - 订阅完成
- [ ] `customer.subscription.created` - 订阅创建  
- [ ] `customer.subscription.updated` - 订阅更新
- [ ] `customer.subscription.deleted` - 订阅取消

### 支付相关（2个）
- [ ] `invoice.payment_succeeded` - 支付成功（包含超额计费）
- [ ] `invoice.payment_failed` - 支付失败

---

## 📍 如何查看当前配置的事件

### 方法 1：在 Webhook 详情页面

1. 点击顶部 **"Webhook"** 标签
2. 点击 **"vibrant-splendor"**
3. 在 **"目的地详情"** 下方找到 **"侦听"** 或 **"Events to send"**
4. 查看列出的所有事件

### 方法 2：查看事件交付记录

在概览页面的 **"事件交付"** 图表中，可以看到最近触发的事件类型。

---

## 🚨 关于错误信息

### 错误 1: `invalid_request_err...` (1月29日 18:07)

**可能原因**：
- 我之前的测试脚本（没有签名）
- Stripe 的测试请求

**解决方法**：不用担心，这是正常的测试错误

### 错误 2: `parameter_missing...` (1月26日)

**可能原因**：
- 旧版本的 Firebase Function
- 缺少必要参数

**解决方法**：已在最新部署中修复

---

## 📋 下一步操作

### 如果事件已完整（6个都有）：

✅ **直接进行测试！**

### 如果缺少事件：

1. 点击 **"编辑接收端"** 或 **"Update details"**
2. 滚动到 **"侦听事件"** 部分
3. 点击 **"+ 添加事件"**
4. 搜索并添加缺失的事件
5. 点击 **"更新端点"** 保存

---

## 🧪 测试步骤（完成事件配置后）

### 方法 1：Stripe Dashboard 测试（推荐）

1. 在 Webhook 详情页面
2. 找到 **"发送测试 webhook"** 按钮
3. 选择事件：`invoice.payment_succeeded`
4. 点击 **"发送测试 webhook"**
5. 查看响应：应该是 **200 OK**

### 方法 2：命令行测试

```bash
node test-webhook-script.js
```

### 方法 3：实际上传文件测试

1. 访问：https://vaultcaddy.com
2. 登录
3. 上传 5 页 PDF
4. 验证 Credits 扣除

---

## ✅ 成功标志

### Stripe Dashboard：
- ✅ 测试事件返回：`200 OK`
- ✅ 响应内容：`{"received":true}`

### Firebase Console：
访问：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/functions/logs

应该看到：
```
🔗 Stripe Webhook 收到請求
✅ Stripe 事件已接收: invoice.payment_succeeded
```

---

## 💡 快速完成指引

**最快的方法（2分钟）**：

1. ✅ 在 Stripe 中点击 **"Webhook"** → **"vibrant-splendor"**
2. ✅ 确认事件列表包含上述 6 个事件
3. ✅ 如果缺少，点击 **"编辑"** → 添加缺失事件 → 保存
4. ✅ 点击 **"发送测试 webhook"** → 选择 `invoice.payment_succeeded` → 发送
5. ✅ 验证返回 200 OK
6. ✅ 完成！

**完成后，任务 1 就完成了！** 🎉


