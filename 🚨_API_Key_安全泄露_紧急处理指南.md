# 🚨 API Key 安全泄露 - 紧急处理指南

**泄露时间**: 2026-01-07  
**泄露的API Key**: `sk-cb90732bb403446a9a1dea2c49bf868a`  
**泄露方式**: 在对话/聊天记录中公开  
**风险等级**: 🔴 **极高**

---

## ⚠️ 当前安全状态分析

### 🔴 已确认的安全问题

#### 1. API Key 已在对话中公开 ⚠️⚠️⚠️

**问题**:
- 您刚才在对话中发送了完整的API Key：`sk-cb90732bb403446a9a1dea2c49bf868a`
- 这个API Key现在已经**永久记录**在对话历史中
- 如果这个对话记录被保存、分享或备份，API Key就会泄露

**风险**:
- ❌ 任何能访问这个对话记录的人都能获取您的API Key
- ❌ 如果对话记录被自动备份到云端，API Key可能被第三方获取
- ❌ 恶意用户可以使用这个API Key消耗您的额度
- ❌ 您的账单可能会突然暴增

**必须采取的行动**:
1. ✅ **立即删除这个API Key**（在阿里云控制台）
2. ✅ **创建新的API Key**
3. ✅ **监控账单**，检查是否有异常调用

---

#### 2. qwen-vl-config.js 的安全风险 ⚠️

**当前状态**:
- `qwen-vl-config.js` 文件**没有**在 `.gitignore` 中
- 这意味着如果您填入API Key后提交到Git，**API Key会被上传到GitHub/远程仓库**

**问题**:
```javascript
// qwen-vl-config.js（第26行）
apiKey: '', // 如果您在这里填入真实的API Key...
```

如果您这样做：
```javascript
apiKey: 'sk-cb90732bb403446a9a1dea2c49bf868a', // ❌ 危险！
```

然后运行 `git add .` 和 `git commit`，这个API Key就会被上传到远程仓库，**永久泄露**！

---

### ✅ 当前的安全措施（部分有效）

**`.gitignore` 已包含**:
```
.env
.env.local
.env.production
*.secret
*.key
*-token.txt
```

但是**缺少**:
- `qwen-vl-config.js` 没有被忽略
- 没有专门的 Qwen API Key 保护规则

---

## 🚀 立即执行的安全修复（3个步骤）

### 步骤 1: 立即删除泄露的API Key（5分钟）⚠️⚠️⚠️

1. **登录阿里云控制台**
   - 访问：https://bailian.console.alibabacloud.com/apikey

2. **找到泄露的API Key**
   - API Key: `sk-cb90732bb403446a9a1dea2c49bf868a`

3. **点击"删除"按钮**
   - 确认删除

4. **立即创建新的API Key**
   - 点击"创建API Key"
   - 复制新的API Key（但**不要在对话中发送**！）

**为什么必须立即删除？**
- ❌ 一旦泄露，无法撤回
- ❌ 任何人都可以使用这个API Key消耗您的额度
- ❌ 删除是唯一的补救措施

---

### 步骤 2: 使用环境变量安全存储API Key（10分钟）✅

**不要**直接在 `qwen-vl-config.js` 中存储API Key！

#### 方案 A: 使用 `.env` 文件（推荐）

**1. 创建 `.env` 文件**（在项目根目录）

```bash
# .env
QWEN_API_KEY=sk-你的新API-Key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen3-vl-plus-2025-12-19
```

**2. 更新 `qwen-vl-config.js`**

```javascript
// qwen-vl-config.js
const QWEN_VL_CONFIG = {
    apiKey: process.env.QWEN_API_KEY || '', // 从环境变量读取
    apiUrl: process.env.QWEN_BASE_URL || 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
    model: process.env.QWEN_MODEL || 'qwen3-vl-plus-2025-12-19',
    temperature: 0.1,
    maxTokens: 4000,
};
```

**3. 确认 `.env` 已在 `.gitignore` 中**

✅ 已确认：`.env` 在您的 `.gitignore` 第27行

---

#### 方案 B: 使用单独的 `qwen-vl-config.local.js` 文件（更简单）

**1. 创建 `qwen-vl-config.local.js`**（只在本地存在）

```javascript
// qwen-vl-config.local.js
const QWEN_VL_CONFIG = {
    apiKey: 'sk-你的新API-Key', // 只存在于本地，不会被提交到Git
    apiUrl: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
    model: 'qwen3-vl-plus-2025-12-19',
    temperature: 0.1,
    maxTokens: 4000,
};
```

**2. 更新 `.gitignore`**（添加这个文件）

```
# Qwen API 配置（本地）
qwen-vl-config.local.js
```

**3. 更新 `qwen-vl-test.html`**（引用新文件）

```html
<!-- 改为引用本地配置 -->
<script src="qwen-vl-config.local.js"></script>
```

**4. 保留 `qwen-vl-config.js` 作为模板**（不含真实API Key）

```javascript
// qwen-vl-config.js（模板）
const QWEN_VL_CONFIG = {
    apiKey: '', // 留空，作为模板
    // ...
};
```

---

### 步骤 3: 更新 `.gitignore`（2分钟）✅

添加以下规则到 `.gitignore`：

```
# Qwen API 配置
qwen-vl-config.local.js
qwen-api-key.txt

# 通用 API Key 保护
*-api-key.*
```

---

## 📋 安全检查清单

### 立即执行（今天）

- [ ] **删除泄露的API Key**（`sk-cb90732bb403446a9a1dea2c49bf868a`）
- [ ] **创建新的API Key**（但不要在对话中发送！）
- [ ] **更新 `.gitignore`**（添加 `qwen-vl-config.local.js`）
- [ ] **创建 `qwen-vl-config.local.js`**（存储真实API Key）
- [ ] **测试新配置**

### 本周执行

- [ ] **检查Git历史**，确认没有意外提交API Key
- [ ] **设置阿里云用量警报**（防止异常消费）
- [ ] **定期轮换API Key**（每3-6个月）

---

## 🔒 API Key 安全最佳实践

### ✅ 应该做的事

1. **使用环境变量或本地配置文件**
   - `.env` 或 `*.local.js`

2. **添加到 `.gitignore`**
   - 确保API Key不会被提交到Git

3. **定期轮换API Key**
   - 每3-6个月更换一次

4. **监控用量**
   - 设置阿里云用量警报

5. **使用最小权限原则**
   - 只授予API Key必需的权限

---

### ❌ 绝对不要做的事

1. ❌ **不要在对话/聊天中发送API Key**
   - 对话记录可能被保存、备份或分享

2. ❌ **不要硬编码API Key**
   - 不要直接写在代码文件中

3. ❌ **不要提交到Git**
   - 一旦提交，即使删除也会永久记录在Git历史中

4. ❌ **不要分享给他人**
   - 即使是信任的人，也应该让他们使用自己的API Key

5. ❌ **不要在公共场所展示**
   - 截图、录屏时要遮挡API Key

---

## 🚨 如果API Key已经泄露怎么办？

### 紧急处理流程

**步骤 1: 立即删除泄露的API Key**（5分钟）
- 登录阿里云控制台
- 找到泄露的API Key
- 点击"删除"
- 确认删除

**步骤 2: 监控账单**（10分钟）
- 检查最近24小时的API调用记录
- 查看是否有异常消费
- 如有异常，联系阿里云客服

**步骤 3: 创建新的API Key**（5分钟）
- 创建新的API Key
- 使用安全的方式存储（环境变量或本地配置文件）

**步骤 4: 检查Git历史**（15分钟）
- 运行 `git log --all --full-history --grep="sk-"`
- 如果发现API Key在Git历史中，考虑使用 `git filter-branch` 清除

**步骤 5: 通知相关人员**
- 如果是团队项目，通知团队成员
- 说明API Key已更换

---

## 💰 设置用量警报（防止异常消费）

### 在阿里云控制台设置

1. **进入 Billing Management**
   - 访问：https://billing.console.aliyun.com/

2. **点击 "Alerts"**

3. **创建新警报**
   - Threshold（阈值）: USD $10（或您的预算）
   - Email（邮箱）: 您的邮箱
   - SMS（短信）: 您的手机号（可选）

4. **保存**

**这样，如果有人恶意使用您的API Key，您会立即收到警报。**

---

## 📊 监控API使用情况

### 每周检查（推荐）

1. **登录阿里云控制台**
2. **进入 Model Studio**
3. **查看 API 调用历史**
   - 调用次数
   - 消费金额
   - 异常时间段

**如果发现异常**：
- 立即删除API Key
- 创建新的API Key
- 联系阿里云客服

---

## ✅ 总结

### 🚨 立即采取的行动（今天必须完成）

1. ✅ **删除泄露的API Key**：`sk-cb90732bb403446a9a1dea2c49bf868a`
2. ✅ **创建新的API Key**（但不要在对话中发送！）
3. ✅ **更新 `.gitignore`**（添加 `qwen-vl-config.local.js`）
4. ✅ **创建 `qwen-vl-config.local.js`**（存储真实API Key）
5. ✅ **设置用量警报**

### 📋 长期安全措施

1. **定期轮换API Key**（每3-6个月）
2. **监控用量**（每周检查）
3. **使用环境变量**（不要硬编码）
4. **教育团队成员**（API Key安全意识）

---

**文档创建时间**: 2026-01-07  
**泄露的API Key**: `sk-cb90732bb403446a9a1dea2c49bf868a`  
**状态**: 🔴 必须立即删除  
**下一步**: 删除泄露的API Key并创建新的API Key



