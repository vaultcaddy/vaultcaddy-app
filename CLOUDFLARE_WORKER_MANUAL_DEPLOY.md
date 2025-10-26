# 🚀 Cloudflare Worker 手动部署指南

## ⚠️ 重要提示
根据错误日志，DeepSeek Worker 部署失败的原因是：
1. **CORS 错误**: Worker 的 CORS 配置可能不正确
2. **404 错误**: Worker URL 可能不存在或未正确部署

---

## 📋 手动部署步骤

### 步骤 1: 打开 Cloudflare Workers 主页
访问：https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers-and-pages

### 步骤 2: 创建或编辑 Worker
1. 如果 `deepseek-proxy` Worker 不存在，点击 "Create Worker"
2. 如果存在，点击 Worker 名称进入编辑页面

### 步骤 3: 复制 Worker 代码
打开本地文件：`cloudflare-worker-deepseek.js`
复制所有内容（已包含你的 API Key: `sk-4a43b49a13a840009052be65f599b7a4`）

### 步骤 4: 粘贴并部署
1. 在 Cloudflare 编辑器中粘贴代码
2. 点击 "Save and Deploy" 按钮
3. 等待部署完成

### 步骤 5: 配置 Worker 路由（重要！）
1. 进入 Worker 的 "Triggers" 标签页
2. 确认 Worker URL 是：`https://deepseek-proxy.vaultcaddy.workers.dev`
3. 如果不是，点击 "Add Custom Domain" 或 "Add Route"

---

## 🔍 验证部署

### 测试 1: 检查 Worker 是否在线
在浏览器中访问：
```
https://deepseek-proxy.vaultcaddy.workers.dev
```

**预期结果**：应该返回类似以下内容：
```json
{"error":"Method not allowed","message":"只支持 POST 請求"}
```

### 测试 2: 测试 DeepSeek API
在浏览器控制台运行：
```javascript
fetch('https://deepseek-proxy.vaultcaddy.workers.dev', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [{ role: 'user', content: 'Hello!' }]
    })
}).then(r => r.json()).then(console.log);
```

**预期结果**：应该返回 DeepSeek 的响应，包含生成的文本

---

## 🔧 修复 CORS 错误

如果仍然出现 CORS 错误，请确认 Worker 代码中的 CORS 配置：

```javascript
// 允許的來源（CORS）
const ALLOWED_ORIGINS = [
  'https://vaultcaddy.com',
  'http://localhost:3000',
  'http://127.0.0.1:3000'
];
```

确保 `https://vaultcaddy.com` 在允许列表中。

---

## 🆘 常见问题

### Q: Worker URL 不存在
**A**: 在 "Triggers" 标签页中添加 `*.workers.dev` 路由

### Q: 仍然出现 404 错误
**A**: 确认 Worker 名称是 `deepseek-proxy`，并且已部署

### Q: CORS 错误持续存在
**A**: 检查 `ALLOWED_ORIGINS` 配置，确保包含你的域名

---

## ✅ 部署完成后

1. **刷新 VaultCaddy 页面**（Cmd+Shift+R）
2. **再次尝试上传图2**
3. **查看控制台日志**，确认使用 DeepSeek Vision

---

**创建时间**: 2025-10-26  
**作用**: Cloudflare Worker 手动部署指南  
**帮助**: 解决 DeepSeek Worker 部署问题

