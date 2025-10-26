# 🔧 DeepSeek Worker CORS 修复指南

## 🔍 问题诊断

从浏览器控制台可以看到 CORS 错误：
```
Access to fetch at 'https://deepseek-proxy.vaultcaddy.workers.dev' 
from origin 'https://vaultcaddy.com' has been blocked by CORS policy
```

**根本原因**：Cloudflare Worker 在返回 405 错误时没有添加 CORS 头。

---

## ✅ 解决方案

已更新 `cloudflare-worker-deepseek.js` 文件，确保所有响应都包含 CORS 头。

---

## 📋 部署步骤

### 步骤 1: 打开 Cloudflare Worker 编辑器

1. 访问：https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/deepseek-proxy/production
2. 点击 **"Quick edit"** 按钮

### 步骤 2: 复制新的 Worker 代码

从 `cloudflare-worker-deepseek.js` 文件中复制所有内容（第 1 行到第 149 行）

### 步骤 3: 粘贴并保存

1. 在 Cloudflare 编辑器中，**全选并删除**现有代码
2. **粘贴**新的代码
3. 点击 **"Save and Deploy"** 按钮

### 步骤 4: 验证部署

等待几秒钟，然后在浏览器控制台运行：

```javascript
fetch('https://deepseek-proxy.vaultcaddy.workers.dev', {
  method: 'GET',
  headers: {
    'Origin': 'https://vaultcaddy.com'
  }
})
.then(r => r.json())
.then(d => console.log('✅ Worker 响应:', d))
.catch(e => console.error('❌ 错误:', e));
```

**预期结果**：应该看到 `{"error":"Method not allowed","message":"只支持 POST 請求"}` 并且**没有 CORS 错误**。

---

## 🧪 测试上传功能

部署完成后，测试文件上传：

1. 访问：https://vaultcaddy.com/firstproject.html
2. 点击 **"Upload files"** 按钮
3. 选择一个文件（发票、收据或银行对账单）
4. 等待 AI 处理

**预期结果**：
- ✅ 文件成功上传
- ✅ AI 开始处理
- ✅ 提取的数据显示在表格中

---

## 🔍 关键修改

### 修改前（有问题）：
```javascript
// 只接受 POST 請求
if (request.method !== 'POST') {
  return new Response(JSON.stringify({ 
    error: 'Method not allowed',
    message: '只支持 POST 請求'
  }), { 
    status: 405,
    headers: { 'Content-Type': 'application/json' }
  });  // ❌ 没有 CORS 头！
}
```

### 修改后（已修复）：
```javascript
// 只接受 POST 請求
if (request.method !== 'POST') {
  const errorResponse = new Response(JSON.stringify({ 
    error: 'Method not allowed',
    message: '只支持 POST 請求'
  }), { 
    status: 405,
    headers: { 'Content-Type': 'application/json' }
  });
  return addCORSHeaders(errorResponse, origin);  // ✅ 添加了 CORS 头！
}
```

---

## 📝 注意事项

1. **API Key 安全**：API Key 已安全存储在 Worker 中，不会暴露给客户端
2. **允许的来源**：Worker 只允许来自 `https://vaultcaddy.com` 的请求
3. **缓存时间**：CORS 预检请求缓存 24 小时

---

## ❓ 常见问题

### Q: 为什么还是看到 CORS 错误？

**A**: 可能的原因：
1. Worker 代码没有正确部署
2. 浏览器缓存了旧的预检响应（清除缓存并刷新）
3. Worker URL 不正确

### Q: 如何清除浏览器缓存？

**A**: 
1. 按 `Ctrl+Shift+Delete` (Windows) 或 `Cmd+Shift+Delete` (Mac)
2. 选择 "缓存的图片和文件"
3. 点击 "清除数据"
4. 刷新页面

### Q: 如何查看 Worker 日志？

**A**: 
1. 在 Cloudflare Dashboard 中，点击 Worker 名称
2. 点击 "Logs" 标签
3. 点击 "Begin log stream"

---

## ✅ 完成检查清单

- [ ] 已复制新的 Worker 代码
- [ ] 已粘贴到 Cloudflare 编辑器
- [ ] 已点击 "Save and Deploy"
- [ ] 已等待部署完成（约 10-30 秒）
- [ ] 已验证 Worker 响应（没有 CORS 错误）
- [ ] 已测试文件上传功能
- [ ] AI 成功提取数据

---

## 🎉 成功标志

当你看到以下情况时，说明修复成功：

1. ✅ 浏览器控制台**没有 CORS 错误**
2. ✅ 文件上传成功
3. ✅ AI 开始处理文件
4. ✅ 提取的数据显示在表格中
5. ✅ 控制台显示：`✅ DeepSeek Vision Client 已初始化`

---

如果还有问题，请提供：
1. 浏览器控制台的完整错误信息
2. Cloudflare Worker 日志
3. 网络请求的详细信息（从浏览器开发者工具的 Network 标签）

