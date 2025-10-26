# 🚀 部署 DeepSeek Cloudflare Worker

## ✅ API Key 已更新
**DeepSeek API Key**: `sk-4a43b49a13a840009052be65f599b7a4`

---

## 📋 部署步骤

### 步骤 1: 复制 Worker 代码
1. 打开文件：`cloudflare-worker-deepseek.js`
2. 复制所有内容（Cmd+A, Cmd+C）

### 步骤 2: 打开 Cloudflare Worker 编辑器
访问：https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/deepseek-proxy/production

### 步骤 3: 粘贴代码
1. 删除编辑器中的所有旧代码
2. 粘贴新代码（Cmd+V）
3. 确认 API Key 已正确设置

### 步骤 4: 保存并部署
1. 点击 "Save and Deploy" 按钮
2. 等待部署完成（通常 5-10 秒）

### 步骤 5: 测试 Worker
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

**预期结果**：应该返回 DeepSeek 的响应，而不是 404 或 CORS 错误

---

## 🔍 问题诊断

### 当前错误分析（从图1-4）

#### 错误 1: DeepSeek CORS 错误
```
Access to fetch at 'firstproject.html?pr_ect=1761474211027:1' from origin 
'https://vaultcaddy.com' has been blocked by CORS policy
```

**原因**: Cloudflare Worker 的 CORS 配置可能不正确

**解决方案**: 
- 确保 Worker 中的 `ALLOWED_ORIGINS` 包含 `https://vaultcaddy.com`
- 重新部署 Worker

#### 错误 2: DeepSeek 404 错误
```
Failed to load deepseek-proxy.vaultcaddy.workers.dev/1
resource: net::ERR_FAILED
```

**原因**: Worker URL 可能不正确或未部署

**解决方案**:
- 确认 Worker URL: `https://deepseek-proxy.vaultcaddy.workers.dev`
- 重新部署 Worker

#### 错误 3: Gemini 404 错误
```
響應錯誤: 404 - {"error":"Gemini API 錯誤","status":404,"details":
{"code":404,"message":"models/gemini-1.5-flash-latest is not found for 
API version v1beta"}}
```

**原因**: Gemini API 模型名称不正确或区域限制

**解决方案**:
- 使用 DeepSeek 作为主要 AI（已配置）
- Gemini 作为备用（可选）

---

## ✅ 修复后的预期行为

### AI 处理顺序
1. **DeepSeek Vision** ← 最优先（准确度高，成本低）
2. **OpenAI GPT-4 Vision** ← 备用1
3. **Gemini AI** ← 备用2
4. **Vision AI** ← 备用3（OCR only）

### 成功标志
在控制台中应该看到：
```
🤖 使用 DeepSeek Vision Client...
✅ DeepSeek Vision Client 已初始化
✅ DeepSeek 原始響應: {...}
✅ AI 處理成功
```

---

## 🔧 快速修复命令

### 方法 1: 手动部署（推荐）
1. 访问 Cloudflare Dashboard
2. 复制 `cloudflare-worker-deepseek.js` 内容
3. 粘贴并部署

### 方法 2: 使用 Wrangler CLI（高级）
```bash
cd /Users/cavlinyeung/ai-bank-parser
wrangler deploy cloudflare-worker-deepseek.js --name deepseek-proxy
```

---

## 📊 验证清单

部署完成后，请验证：

- [ ] Worker 已部署到 Cloudflare
- [ ] API Key 已正确设置
- [ ] CORS 配置正确
- [ ] Worker URL 可访问
- [ ] 上传文件测试成功
- [ ] 控制台显示 "使用 DeepSeek Vision"

---

## 🆘 如果仍然失败

### 检查 1: Worker 状态
访问：https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/view/deepseek-proxy

确认：
- Status: Active ✅
- Last deployed: 最近时间

### 检查 2: API Key 有效性
在 DeepSeek 平台检查：
- API Key 是否有效
- 是否有足够余额
- 是否有使用限制

### 检查 3: 网络连接
在控制台运行：
```javascript
fetch('https://deepseek-proxy.vaultcaddy.workers.dev')
  .then(r => r.text())
  .then(console.log);
```

---

**创建时间**: 2025-10-26  
**作用**: DeepSeek Worker 部署指南  
**帮助**: 解决 CORS 和 404 错误

