# ✅ Qwen-VL Max API Key 配置指南 - 快速开始

**适用对象**: 香港、新加坡及其他国际地区用户  
**所需时间**: 15-20分钟  
**所需材料**: 护照/身份证、国际信用卡、邮箱

---

## 🚀 5步快速开始

### 第1步：注册阿里云国际版（5分钟）

**访问**: https://www.alibabacloud.com/

1. 点击右上角 **"Free Account"**
2. 使用邮箱注册（推荐使用 Gmail）
3. 验证邮箱
4. 设置密码

✅ **完成标志**: 收到欢迎邮件，可登录控制台

---

### 第2步：实名认证（5-10分钟）

登录后系统会提示完成认证：

1. 选择 **"Individual Account"**（个人账号）
2. 上传护照或身份证照片
3. 填写个人信息（姓名、地址）
4. 提交审核

✅ **完成标志**: 收到认证通过通知（通常5-30分钟）

---

### 第3步：添加支付方式（3分钟）

1. 进入 **Billing Management** → **Payment Methods**
2. 点击 **"Add Payment Method"**
3. 选择 **"Credit Card"**
4. 填写信用卡信息（支持 Visa/Mastercard）
5. 完成验证（可能扣除USD $1，稍后退回）

✅ **完成标志**: 支付方式显示为"Active"

---

### 第4步：开通 Model Studio（2分钟）

1. 在控制台搜索 **"Model Studio"**
2. 点击进入服务页面
3. ⚠️ **重要**: 选择地域为 **"Singapore (Singapore)"**
4. 点击 **"Activate Now"**
5. 同意服务协议

✅ **完成标志**: 看到 Model Studio 控制台首页

---

### 第5步：创建 API Key（2分钟）

1. 在 Model Studio 控制台，点击左侧 **"API-KEY"**
2. 点击 **"Create API Key"**
3. 填写名称（例如："VaultCaddy Test"）
4. 点击 **"Create"**
5. ⚠️ **立即复制 API Key**（只显示一次！）

✅ **完成标志**: 获得格式为 `sk-xxxxxxxxxx` 的 API Key

---

## 📝 配置到测试页面

### 步骤 1: 打开配置文件

打开 `qwen-vl-config.js` 文件：

```javascript
const QWEN_VL_CONFIG = {
    apiKey: '', // 在这里填入您的 API Key
    baseURL: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
    model: 'qwen-vl-max',
};
```

### 步骤 2: 填入 API Key

```javascript
const QWEN_VL_CONFIG = {
    apiKey: 'sk-1234567890abcdef1234567890abcdef', // 填入您刚才复制的 API Key
    baseURL: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
    model: 'qwen-vl-max',
};
```

### 步骤 3: 保存文件

按 **Cmd+S** (Mac) 或 **Ctrl+S** (Windows) 保存。

---

## 🧪 测试 API Key

### 步骤 1: 启动本地服务器

在终端运行：

```bash
cd /Users/cavlinyeung/ai-bank-parser
python3 -m http.server 8000
```

### 步骤 2: 访问测试页面

在浏览器打开：
```
http://localhost:8000/qwen-vl-test.html
```

### 步骤 3: 上传测试文件

1. 选择 **"銀行對賬單測試"** 或 **"收據測試"** Tab
2. 点击上传区域或拖放文件
3. 等待处理结果

### 步骤 4: 查看结果

**成功示例**：
```
状态: ✅ Qwen-VL Max 處理成功！
結果: { "transactions": [...] }
```

**失败示例**（如果 API Key 错误）：
```
状态: ❌ 處理失敗: Invalid API Key
```

---

## 💰 费用说明

### 免费额度

- ✅ 新用户获得 **100万 Token 免费额度**
- ✅ 有效期 90 天
- ✅ 足够处理 **80-100 页**文档

### 实际成本（超出免费额度后）

| 文档类型 | 每页成本 | 1000页成本 |
|---------|---------|-----------|
| 银行对账单（10页） | HK$0.038 | HK$38 |
| 收据（单页） | HK$0.038 | HK$38 |

**对比现有方案**：
- Google Vision + DeepSeek: HK$0.6255/页
- Qwen-VL Max: HK$0.038/页
- **节省 93.9%**

---

## 🔒 安全提醒

1. ❌ **不要将 API Key 提交到 Git**
   - 确保 `qwen-vl-config.js` 在 `.gitignore` 中

2. ❌ **不要分享 API Key**
   - 每个人应该使用自己的 API Key

3. ✅ **定期检查用量**
   - 在控制台监控 API 调用次数

4. ✅ **如怀疑泄露，立即删除**
   - 在控制台删除旧 Key
   - 创建新 Key

---

## ❓ 遇到问题？

### 常见错误

**错误 1: "Invalid API Key"**
- 检查 API Key 是否完整（包括 `sk-` 前缀）
- 确认在控制台该 Key 仍然存在
- 尝试创建新的 API Key

**错误 2: "Service not activated"**
- 确认已开通 Model Studio 服务
- 确认选择了新加坡地域

**错误 3: "Insufficient balance"**
- 免费额度已用完
- 需要充值（最低 USD $10）

### 获取帮助

详细教学请查看：
📋 **`📋_Qwen-VL_Max_API_Key获取教学_国际版.md`**

或联系阿里云客服：
- 在线客服: https://www.alibabacloud.com/help
- 邮箱: support@alibabacloud.com

---

## ✅ 完成检查清单

- [ ] 注册阿里云国际版账号
- [ ] 完成实名认证
- [ ] 添加信用卡支付方式
- [ ] 开通 Model Studio（新加坡地域）
- [ ] 创建并保存 API Key
- [ ] 填入 `qwen-vl-config.js`
- [ ] 测试页面正常工作

**全部完成后，您就可以开始使用 Qwen-VL Max 了！**

---

**文档创建时间**: 2026-01-06  
**预计完成时间**: 15-20分钟  
**下一步**: 测试处理银行对账单和收据




