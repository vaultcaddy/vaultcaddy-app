# 🔑 更新 Stripe 生产密钥

## 🚨 **错误信息**
```
Expired API Key provided: sk_live_***
```

**原因**: Stripe 生产密钥已过期或被撤销

---

## 🔧 **修复步骤（10分钟）**

### **步骤 1：创建新的 Stripe 生产密钥**

1. **访问 Stripe Dashboard**
   🔗 https://dashboard.stripe.com/apikeys
   - ⚠️ 确保在**生产模式**（右上角不显示"测试模式"）

2. **删除旧密钥（可选）**
   - 找到以 `sk_live_51S6Qv3JmiQ31C0GT...` 开头的密钥
   - 点击 "..." → "删除"

3. **创建新密钥**
   - 点击 "+ 创建密钥"
   - 类型：**标准密钥**（或**受限密钥**更安全）
   
4. **（推荐）创建受限密钥**
   - 如果选择受限密钥，设置权限：
     ```
     ✅ Products: 读取 + 写入
     ✅ Prices: 读取 + 写入
     ✅ Customers: 读取 + 写入
     ✅ Subscriptions: 读取 + 写入
     ✅ Invoices: 读取 + 写入
     ✅ Checkout Sessions: 读取 + 写入
     ✅ Payment Intents: 读取 + 写入
     ```

5. **复制新密钥**
   - ⚠️ 密钥只显示一次，务必立即复制！
   - 格式：`sk_live_...`

---

### **步骤 2：更新 Firebase Functions 环境变量**

```bash
cd /Users/cavlinyeung/ai-bank-parser

# 设置新的生产密钥
firebase functions:config:set stripe.live_secret_key="sk_live_你的新密钥"

# 验证配置
firebase functions:config:get
```

**预期输出**：
```json
{
  "stripe": {
    "live_secret_key": "sk_live_你的新密钥",
    "live_webhook_secret": "whsec_...",
    "test_secret_key": "sk_test_...",
    "test_webhook_secret": "whsec_..."
  }
}
```

---

### **步骤 3：重新部署 Firebase Functions**

```bash
cd /Users/cavlinyeung/ai-bank-parser

# 部署 Functions
firebase deploy --only functions
```

**预期输出**：
```
✔  functions: all functions deployed successfully!
```

---

### **步骤 4：验证修复**

1. **访问 billing 页面**
   🔗 https://vaultcaddy.com/billing.html

2. **点击 "開始使用" 按钮**
   - 应该成功跳转到 Stripe Checkout 页面
   - 不应该出现 "Expired API Key" 错误

3. **（可选）完成一次真实支付测试**
   - 使用真实信用卡
   - 金额：HK$58（月费）或 HK$552（年费）
   - 验证 Credits 是否正确添加

---

## ⚠️ **重要提醒**

### **密钥安全**
- ❌ 不要将密钥提交到 Git
- ❌ 不要在代码中硬编码密钥
- ✅ 只通过 Firebase Functions Config 管理
- ✅ 定期轮换密钥（每季度）

### **测试建议**
- 先用小金额测试（HK$58 月费）
- 确认 Credits 正确添加后再推广
- 监控 Firebase Functions 日志

---

## 🔍 **故障排查**

### **如果仍然报错**

#### **错误 1: "Invalid API Key"**
```bash
# 检查配置是否正确
firebase functions:config:get

# 确保密钥以 sk_live_ 开头
```

#### **错误 2: "Webhook signature verification failed"**
```bash
# 需要同时更新 Webhook 密钥
firebase functions:config:set stripe.live_webhook_secret="whsec_新密钥"
firebase deploy --only functions
```

#### **错误 3: "Network error"**
- 检查 Firebase Functions 是否正常运行
- 查看 Firebase Console 日志

---

## 📋 **检查清单**

- [ ] 访问 Stripe Dashboard（生产模式）
- [ ] 删除旧的生产密钥
- [ ] 创建新的生产密钥
- [ ] 复制新密钥（以 `sk_live_` 开头）
- [ ] 更新 Firebase Functions 配置
- [ ] 重新部署 Firebase Functions
- [ ] 测试支付流程
- [ ] 验证 Credits 正确添加

---

## 🎯 **快速命令**

```bash
# 一键更新和部署
cd /Users/cavlinyeung/ai-bank-parser
firebase functions:config:set stripe.live_secret_key="sk_live_你的新密钥"
firebase deploy --only functions

# 验证配置
firebase functions:config:get

# 查看部署日志
firebase functions:log
```

---

**预计时间**: 10-15 分钟  
**难度**: ⭐⭐☆☆☆（简单）  
**风险**: 🟢 低（旧密钥已失效，更新不影响现有用户）

