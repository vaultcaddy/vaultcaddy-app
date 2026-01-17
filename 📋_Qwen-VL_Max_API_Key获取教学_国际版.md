# 📋 Qwen-VL Max API Key 获取教学（国际版）

**创建日期**: 2026-01-06  
**适用地区**: 香港、新加坡及其他国际地区  
**服务**: 阿里云国际版（Alibaba Cloud International）

---

## 🌍 为什么需要国际版？

**国际版 vs 中国版**:
- ✅ **国际版**（推荐）：全球可用，支持国际信用卡，无需中国大陆手机号
- ❌ **中国版**：需要中国大陆手机号和身份证，香港用户不适用

---

## 📝 完整注册流程（约15-20分钟）

### 步骤 1: 访问阿里云国际版

1. **打开浏览器**，访问阿里云国际版官网：
   ```
   https://www.alibabacloud.com/
   ```

2. **点击右上角 "Free Account"** 或 **"Sign Up"** 按钮

   ![阿里云国际版首页](https://www.alibabacloud.com/)

---

### 步骤 2: 注册账号

#### 2.1 选择注册方式

有3种注册方式可选：

**选项 A: 使用邮箱注册**（推荐）
- ✅ 简单快速
- ✅ 支持任何邮箱（Gmail、Outlook等）
- 时间：5分钟

**选项 B: 使用手机号注册**
- 支持香港/国际手机号（+852、+65等）
- 时间：5分钟

**选项 C: 使用Google/LinkedIn账号**
- 一键注册
- 时间：2分钟

#### 2.2 填写注册信息

**使用邮箱注册的步骤**：

1. **输入邮箱地址**
   - 例如：your.email@gmail.com

2. **设置密码**
   - 至少8个字符
   - 包含大小写字母和数字
   - 例如：Password123!

3. **输入验证码**
   - 查看邮箱收到的验证码
   - 输入6位数字验证码

4. **勾选服务协议**
   - ☑️ I agree to the Alibaba Cloud Terms of Service

5. **点击 "Sign Up"**

---

### 步骤 3: 完成实名认证（Business Account）

注册后，需要完成实名认证才能使用API服务。

#### 3.1 选择账号类型

登录后，系统会提示选择账号类型：

**选项 A: Individual Account**（个人账号）
- 适合：个人开发者、小型项目
- 需要：护照或身份证
- 时间：5-10分钟

**选项 B: Enterprise Account**（企业账号）
- 适合：公司使用
- 需要：公司注册证明、营业执照
- 时间：1-3个工作日

**推荐**：选择 **Individual Account**，审核更快

#### 3.2 提交个人认证资料

1. **选择证件类型**
   - ☑️ Passport（护照）- 推荐
   - ☐ ID Card（香港身份证）
   - ☐ Driver's License（驾照）

2. **上传证件照片**
   - 拍摄或扫描护照/身份证
   - 确保照片清晰、四角完整
   - 支持格式：JPG、PNG
   - 文件大小：< 5MB

3. **填写个人信息**
   - Full Name（全名）：与证件一致
   - Country/Region：Hong Kong（香港）
   - Address：填写实际地址

4. **点击 "Submit for Review"**

**审核时间**：通常 5-30 分钟（工作时间）

---

### 步骤 4: 添加支付方式

实名认证通过后，需要添加支付方式才能使用付费服务。

#### 4.1 添加信用卡

1. **进入 "Billing Management"**
   - 点击右上角头像 → Billing Management

2. **点击 "Payment Methods"**

3. **点击 "Add Payment Method"**

4. **选择 "Credit Card"**

5. **填写信用卡信息**
   - Card Number（卡号）：16位数字
   - Expiry Date（有效期）：MM/YY
   - CVV：3位数字
   - Cardholder Name（持卡人姓名）

6. **支持的信用卡**
   - ✅ Visa
   - ✅ Mastercard
   - ✅ American Express
   - ✅ JCB

7. **点击 "Add"**

**注意**：系统可能会预授权 USD $1 来验证卡片，稍后会退回。

---

### 步骤 5: 开通 Model Studio 服务

Qwen-VL Max 位于 **Model Studio**（百炼）服务中。

#### 5.1 访问 Model Studio

1. **登录阿里云国际版控制台**
   ```
   https://console.alibabacloud.com/
   ```

2. **搜索 "Model Studio"**
   - 在搜索框输入 "Model Studio" 或 "Bailian"
   - 或访问：https://bailian.console.alibabacloud.com/

3. **点击 "Model Studio" 进入服务页面**

#### 5.2 开通服务

1. **点击 "Activate Now"** 或 **"Free Trial"**

2. **选择地域（Region）**
   - ⚠️ **重要**：必须选择 **"Singapore (Singapore)"**
   - 新加坡地域是国际版，全球可用
   - 不要选择中国大陆地域

3. **阅读服务协议**
   - ☑️ I agree to the Model Studio Service Agreement

4. **点击 "Activate"**

**激活时间**：立即生效（< 1分钟）

---

### 步骤 6: 创建 API Key

#### 6.1 进入 API Key 管理页面

1. **在 Model Studio 控制台**
   - 点击左侧菜单 "API-KEY" 或 "API Keys"
   - 或访问：https://bailian.console.alibabacloud.com/apikey

2. **查看当前 API Keys**
   - 如果是第一次使用，列表为空

#### 6.2 创建新的 API Key

1. **点击 "Create API Key"** 或 **"新建 API-KEY"**

2. **填写 API Key 信息**（可选）
   - Name（名称）：例如 "VaultCaddy Test"
   - Description（描述）：例如 "用于测试 Qwen-VL Max"

3. **点击 "Create"** 或 **"确定"**

4. **复制 API Key**
   - ⚠️ **重要**：API Key 只会显示一次！
   - 立即复制并保存到安全的地方
   - 格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxx`

**示例 API Key**:
```
sk-1234567890abcdef1234567890abcdef
```

#### 6.3 保存 API Key

**方法 1：保存到密码管理器**（推荐）
- 使用 1Password、LastPass、Bitwarden 等

**方法 2：保存到本地文件**
- 创建 `.env` 文件
- 不要提交到 Git 仓库

**方法 3：保存到配置文件**
```javascript
// qwen-vl-config.js
const QWEN_VL_CONFIG = {
    apiKey: 'sk-1234567890abcdef1234567890abcdef', // 填入您的 API Key
    // ...
};
```

---

## ✅ 验证 API Key 是否可用

### 方法 1：使用测试页面（推荐）

1. **打开 `qwen-vl-config.js`**
   ```javascript
   const QWEN_VL_CONFIG = {
       apiKey: 'sk-1234567890abcdef1234567890abcdef', // 填入您刚才复制的 API Key
       // ...
   };
   ```

2. **启动本地服务器**
   ```bash
   python3 -m http.server 8000
   ```

3. **访问测试页面**
   ```
   http://localhost:8000/qwen-vl-test.html
   ```

4. **上传测试文件**
   - 选择一张银行对账单或收据图片
   - 如果处理成功，说明 API Key 可用

### 方法 2：使用 curl 命令测试

在终端运行：

```bash
curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer sk-YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-vl-max",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Hello, can you see this?"
          }
        ]
      }
    ]
  }'
```

**成功响应示例**:
```json
{
  "choices": [
    {
      "message": {
        "content": "Yes, I can see your message!"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 8,
    "total_tokens": 18
  }
}
```

---

## 💰 费用和配额

### 免费额度

**新用户福利**：
- ✅ 注册后获得 **100万 Token 免费额度**
- ✅ 有效期：90天
- ✅ 适用于所有 Qwen 模型

**足够测试**：
- 可以处理约 **80-100 页**文档（银行对账单/收据）
- 足够验证效果

### 付费价格（超出免费额度后）

根据之前的分析（`📊_手写单处理能力与成本对比分析_HKD.md`）：

**Qwen-VL Max**:
- 输入：¥0.003 / 百万 tokens ≈ HK$0.00324 / 百万 tokens
- 输出：¥0.009 / 百万 tokens ≈ HK$0.00972 / 百万 tokens

**实际成本示例**（一页5000字符）:
- 每页约 HK$0.038
- 1000页约 HK$38
- **比现有方案节省 93.9%**

### 充值方式

如需充值：
1. 进入 "Billing Management" → "Recharge"
2. 选择充值金额（最低 USD $10）
3. 使用信用卡支付
4. 即时到账

---

## 🔒 安全最佳实践

### API Key 安全

1. **不要公开 API Key**
   - ❌ 不要提交到 Git 仓库
   - ❌ 不要在前端代码中硬编码
   - ❌ 不要分享给他人

2. **使用环境变量**（生产环境）
   ```javascript
   const apiKey = process.env.QWEN_API_KEY;
   ```

3. **定期轮换 API Key**
   - 每3-6个月更换一次
   - 如果怀疑泄露，立即删除旧 Key

4. **监控使用量**
   - 定期检查 API 调用次数
   - 设置用量警报

### 访问控制

在 Model Studio 控制台可以：
- 查看 API 调用历史
- 设置每日/每月用量限制
- 删除不再使用的 API Key

---

## 🐛 常见问题

### Q1: 收不到验证码邮件

**解决方法**：
1. 检查垃圾邮件文件夹
2. 等待5-10分钟（高峰期可能延迟）
3. 尝试使用其他邮箱（Gmail、Outlook）
4. 联系阿里云客服

### Q2: 实名认证失败

**可能原因**：
- 照片不清晰
- 证件信息与填写不一致
- 证件已过期

**解决方法**：
1. 重新上传高清照片
2. 确保信息完全一致
3. 使用有效证件
4. 联系客服人工审核

### Q3: 信用卡验证失败

**可能原因**：
- 卡片余额不足
- 不支持的卡片类型
- 银行拒绝国际交易

**解决方法**：
1. 确保卡片有足够余额（至少 USD $1）
2. 使用 Visa/Mastercard
3. 联系银行开通国际交易
4. 尝试其他信用卡

### Q4: API Key 调用失败（401 错误）

**可能原因**：
- API Key 输入错误
- API Key 已被删除
- 没有开通服务

**解决方法**：
1. 检查 API Key 是否完整（包括 `sk-` 前缀）
2. 确认 API Key 在控制台仍然存在
3. 确认 Model Studio 服务已激活
4. 重新创建 API Key

### Q5: 选错地域怎么办？

**如果选择了中国大陆地域**：
- API 端点不同，国际访问可能受限
- 需要重新注册或开通新加坡地域

**解决方法**：
1. 在控制台切换到新加坡地域
2. 重新开通 Model Studio 服务
3. 创建新的 API Key

---

## 📞 获取帮助

### 官方文档

- **API 文档**: https://help.alibabacloud.com/document_detail/2712576.html
- **Model Studio 文档**: https://help.alibabacloud.com/zh/model-studio/
- **定价说明**: https://help.alibabacloud.com/zh/model-studio/product-overview/billing

### 客服支持

**在线客服**：
1. 访问：https://www.alibabacloud.com/help
2. 点击右下角"Contact Us"
3. 选择"Live Chat"

**工作时间**：
- 周一至周五：9:00 - 18:00 (SGT 新加坡时间)
- 支持英语、中文

**紧急问题**：
- 邮箱：support@alibabacloud.com

---

## ✅ 完成检查清单

完成以下所有步骤后，您就可以开始使用 Qwen-VL Max 了！

### 注册和认证
- [ ] 注册阿里云国际版账号
- [ ] 完成邮箱验证
- [ ] 完成实名认证（Individual Account）
- [ ] 添加支付方式（信用卡）

### 开通服务
- [ ] 开通 Model Studio 服务
- [ ] 选择新加坡地域
- [ ] 创建 API Key
- [ ] 保存 API Key 到安全位置

### 配置和测试
- [ ] 将 API Key 填入 `qwen-vl-config.js`
- [ ] 启动本地服务器
- [ ] 访问测试页面
- [ ] 上传测试文件验证功能

### 监控和安全
- [ ] 设置用量警报
- [ ] 定期检查 API 调用历史
- [ ] 不将 API Key 提交到 Git

---

## 🎯 下一步

完成 API Key 配置后：

1. **测试基本功能**
   - 使用测试页面处理1-2张银行对账单
   - 使用测试页面处理1-2张收据
   - 验证准确率和处理速度

2. **记录测试结果**
   - 处理时间
   - 准确率
   - Token 使用量
   - 成本

3. **对比现有系统**
   - 准确率对比
   - 速度对比
   - 成本对比

4. **决定是否迁移**
   - 如果测试结果满意，制定迁移计划
   - 如果需要调整，优化提示词和参数

---

**文档创建时间**: 2026-01-06  
**预计完成时间**: 15-20分钟  
**下一步**: 开始注册阿里云国际版账号

祝您配置顺利！如有任何问题，请随时询问。







