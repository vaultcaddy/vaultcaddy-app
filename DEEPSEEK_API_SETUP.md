# DeepSeek API 配置指南

## 步骤 1: 获取 DeepSeek API Key

### 方法 1: 手动获取（推荐）
1. 访问 https://platform.deepseek.com/
2. 登录你的账户
3. 进入 "API Keys" 页面
4. 点击 "Create API Key"
5. 复制生成的 API Key

### 方法 2: 使用 MCP 工具自动获取
我可以使用 Chrome MCP 工具帮你自动获取 API Key。

---

## 步骤 2: 配置 Cloudflare Worker

### 2.1 打开 Cloudflare Worker
访问: https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/deepseek-proxy/production

### 2.2 替换 API Key
在 Worker 代码中找到这一行：
```javascript
const DEEPSEEK_API_KEY = 'YOUR_DEEPSEEK_API_KEY_HERE';
```

替换为你的实际 API Key：
```javascript
const DEEPSEEK_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
```

### 2.3 保存并部署
点击 "Save and Deploy" 按钮

---

## 步骤 3: 测试 API

### 3.1 测试 Worker
在浏览器控制台运行：
```javascript
fetch('https://deepseek-proxy.vaultcaddy.workers.dev', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
            { role: 'user', content: 'Hello!' }
        ]
    })
}).then(r => r.json()).then(console.log);
```

### 3.2 测试上传
1. 打开 https://vaultcaddy.com/firstproject.html
2. 点击 "Upload files" 按钮
3. 选择一个发票或收据图片
4. 查看控制台日志，确认使用 DeepSeek AI

---

## 步骤 4: 验证配置

### 检查清单
- [ ] DeepSeek API Key 已获取
- [ ] Cloudflare Worker 已更新
- [ ] Worker 已部署
- [ ] API 测试成功
- [ ] 上传文件测试成功

---

## 常见问题

### Q: API Key 在哪里？
A: 登录 https://platform.deepseek.com/ → API Keys

### Q: Worker URL 是什么？
A: https://deepseek-proxy.vaultcaddy.workers.dev

### Q: 如何查看 API 使用量？
A: 在 DeepSeek 平台的 "Usage" 页面查看

### Q: 如何充值？
A: 在 DeepSeek 平台的 "Billing" 页面充值

---

**创建时间**: 2025-10-26  
**作用**: DeepSeek API 配置指南  
**帮助**: 快速配置 DeepSeek AI

