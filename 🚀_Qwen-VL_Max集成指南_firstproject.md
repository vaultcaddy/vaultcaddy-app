# 🚀 Qwen-VL Max 集成指南 - firstproject.html

**创建日期**: 2026-01-07  
**目标**: 将 Qwen-VL Max 集成到主应用，替换 Google Vision + DeepSeek

---

## 📋 集成步骤

### 步骤1: 部署 Cloudflare Worker ⭐⭐⭐⭐⭐

#### 1.1 登录 Cloudflare Dashboard

访问: https://dash.cloudflare.com/

#### 1.2 创建新 Worker

1. 点击左侧菜单 "Workers & Pages"
2. 点击 "Create Application"
3. 选择 "Create Worker"
4. 命名为: `qwen-vl-proxy`
5. 点击 "Deploy"

#### 1.3 编辑 Worker 代码

1. 点击 "Edit Code"
2. 复制 `cloudflare-worker-qwen-vl-max.js` 的全部内容
3. 粘贴到编辑器中
4. 点击 "Save and Deploy"

#### 1.4 (推荐) 配置环境变量

为了安全起见，应将 API Key 存储在环境变量中：

1. 进入 Worker 设置: Settings → Variables
2. 添加环境变量:
   - **Name**: `QWEN_API_KEY`
   - **Value**: `YOUR_QWEN_API_KEY` (從阿里雲百煉控制台獲取)
   - **Type**: Environment Variable (Encrypted)
3. 点击 "Save"

然后修改 Worker 代码第16行：
```javascript
// 从环境变量读取 API Key
const QWEN_API_KEY = env.QWEN_API_KEY || 'YOUR_QWEN_API_KEY';
```

并修改 Worker 主函数：
```javascript
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request, event.env));
});

async function handleRequest(request, env) {
    // 现在可以访问 env.QWEN_API_KEY
}
```

#### 1.5 获取 Worker URL

部署成功后，复制 Worker URL，例如：
```
https://qwen-vl-proxy.vaultcaddy.workers.dev
```

#### 1.6 测试 Worker

使用 curl 测试：
```bash
curl -X POST https://qwen-vl-proxy.vaultcaddy.workers.dev \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-vl-plus-2025-12-19",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Hello, how are you?"}
        ]
      }
    ]
  }'
```

预期响应：
```json
{
  "id": "...",
  "choices": [
    {
      "message": {
        "content": "I'm doing well..."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

---

### 步骤2: 添加新处理器到 firstproject.html

#### 2.1 引入新的处理器文件

在 `firstproject.html` 的 `<head>` 部分添加：

```html
<!-- Qwen-VL Max 处理器 (新增) -->
<script src="qwen-vl-max-processor.js"></script>
```

**位置**: 在 `<script src="hybrid-vision-deepseek.js"></script>` 之后

#### 2.2 初始化处理器

在 `firstproject.html` 的初始化代码中添加：

**查找位置**: 搜索 `window.hybridProcessor = new HybridVisionDeepSeekProcessor();`

**在其后添加**:
```javascript
// ========== 初始化 Qwen-VL Max 处理器（新增）==========
console.log('🔧 初始化 Qwen-VL Max 处理器...');
window.qwenVLProcessor = new QwenVLMaxProcessor();
console.log('✅ Qwen-VL Max 处理器初始化完成');

// ========== 选择使用的处理器 ==========
// 选项1: 使用 Qwen-VL Max (推荐)
window.activeProcessor = window.qwenVLProcessor;
console.log('✅ 当前使用处理器: Qwen-VL Max');

// 选项2: 使用原有的 Hybrid (Vision + DeepSeek)
// window.activeProcessor = window.hybridProcessor;
// console.log('✅ 当前使用处理器: Hybrid (Vision + DeepSeek)');
```

#### 2.3 修改文档处理逻辑

**查找位置**: 搜索 `uploadFile` 函数中调用处理器的地方

**原代码**:
```javascript
// 使用混合处理器处理每个文件
const result = await window.hybridProcessor.processDocument(imageFile, docType);
```

**修改为**:
```javascript
// 使用活动处理器处理每个文件
const result = await window.activeProcessor.processDocument(imageFile, docType);
```

**影响的函数**:
1. `uploadFile(file)` - 单文件上传
2. `uploadFileDirect(file, pages)` - 直接上传（跳过 Credits 检查）

**需要修改的具体位置**:

##### 位置1: `uploadFile` 函数 (约第3545-3650行)

**查找**:
```javascript
// 逐個處理文件
for (let i = 0; i < filesToProcess.length; i++) {
    // ...
    const result = await window.hybridProcessor.processDocument(imageFile, docType);
```

**修改为**:
```javascript
// 逐個處理文件
for (let i = 0; i < filesToProcess.length; i++) {
    // ...
    const result = await window.activeProcessor.processDocument(imageFile, docType);
```

##### 位置2: `uploadFileDirect` 函数 (约第3400-3470行)

**查找**:
```javascript
// 使用混合處理器處理每個文件
for (let i = 0; i < filesToProcess.length; i++) {
    // ...
    const result = await window.hybridProcessor.processDocument(imageFile, docType);
```

**修改为**:
```javascript
// 使用活動處理器處理每個文件
for (let i = 0; i < filesToProcess.length; i++) {
    // ...
    const result = await window.activeProcessor.processDocument(imageFile, docType);
```

---

### 步骤3: 测试和验证

#### 3.1 本地测试

1. 打开 Chrome 开发者工具 (F12)
2. 访问 `http://localhost:8000/firstproject.html`
3. 查看控制台，应该看到：
   ```
   🤖 Qwen-VL Max 处理器初始化
   ✅ 端到端处理（OCR + AI 分析一步完成）
   ✅ 支持图片和 PDF 直接处理
   📊 预期准确度: 92-95%
   💰 预估成本: ~$0.005/页 (HK$0.038/页)
   ⚡ 处理速度: 3-8 秒/页（比原方案快 100%）
   ✅ 当前使用处理器: Qwen-VL Max
   ```

#### 3.2 上传测试文件

1. 上传一张发票图片（JPG/PNG）
2. 观察控制台日志：
   ```
   📤 準備上傳文件: invoice.jpg
   📄 文件頁數: 1
   🚀 [Qwen-VL Max] 开始处理: invoice.jpg (invoice)
   🧠 Qwen-VL Max 端到端处理（OCR + 分析）...
   ✅ 处理完成 (5842ms)
   ✅ 文件處理完成並保存
   ```

3. 检查提取的数据是否正确

#### 3.3 性能对比测试

使用相同的文件分别测试两个处理器：

**测试1: Hybrid (Vision + DeepSeek)**
```javascript
// 在控制台执行
window.activeProcessor = window.hybridProcessor;
// 上传文件，记录时间
```

**测试2: Qwen-VL Max**
```javascript
// 在控制台执行
window.activeProcessor = window.qwenVLProcessor;
// 上传相同文件，记录时间
```

**预期结果**:
- Qwen-VL Max 速度快约 **50-100%**
- Qwen-VL Max 准确率更高（尤其手写）

---

### 步骤4: 多语言版本集成

需要在以下文件中进行相同的修改：

1. `en/firstproject.html` (英文版)
2. `kr/firstproject.html` (韩文版)
3. `jp/firstproject.html` (日文版)

**步骤**:
1. 引入 `qwen-vl-max-processor.js`
2. 初始化处理器
3. 修改 `uploadFile` 和 `uploadFileDirect` 函数

---

## 📊 预期效果

### 性能提升

| 指标 | 原方案 (Vision + DeepSeek) | Qwen-VL Max | 提升 |
|------|---------------------------|-------------|------|
| **处理步骤** | 2步 (OCR → 分析) | 1步 (端到端) | -50% |
| **处理时间** | 12秒/页 | 6秒/页 | +100% ⚡ |
| **成本** | HK$0.6255/页 | HK$0.038/页 | -93.9% 💰 |
| **准确率** | 85% | 92-95% | +8-11% ⭐ |
| **手写识别** | 75-80% | 96.5% | +20% ⭐ |
| **PDF支持** | 需转换 | 直接处理 | ✅ |

### 用户体验提升

- ✅ **更快**: 处理时间减半
- ✅ **更准**: 尤其是手写和复杂文档
- ✅ **更省**: 成本大幅降低
- ✅ **更简**: PDF 无需转换

---

## 🔄 回滚方案

如果遇到问题，可以快速回滚到原方案：

### 方法1: 切换处理器（推荐）

在浏览器控制台执行：
```javascript
window.activeProcessor = window.hybridProcessor;
console.log('✅ 已切换回 Hybrid 处理器');
```

### 方法2: 修改代码

修改初始化代码：
```javascript
// 使用原有的 Hybrid (Vision + DeepSeek)
window.activeProcessor = window.hybridProcessor;
console.log('✅ 当前使用处理器: Hybrid (Vision + DeepSeek)');
```

### 方法3: 删除新代码

1. 移除 `<script src="qwen-vl-max-processor.js"></script>`
2. 删除初始化 `window.qwenVLProcessor` 的代码
3. 恢复 `window.hybridProcessor.processDocument` 的调用

---

## 🐛 常见问题

### Q1: Worker 返回 CORS 错误

**症状**: 控制台显示 `Access-Control-Allow-Origin` 错误

**解决**:
1. 确认 Worker 中 CORS 头配置正确
2. 检查 `CORS_HEADERS` 是否包含在所有响应中

### Q2: API Key 无效

**症状**: Worker 返回 401 错误

**解决**:
1. 确认 API Key 正确（從阿里雲百煉控制台獲取）
2. 检查 API Key 是否在阿里云百炼控制台激活
3. 确认使用的是新加坡地域的 API Key

### Q3: 处理超时

**症状**: 240秒后返回超时错误

**解决**:
1. 检查文件大小（建议 < 5MB）
2. 检查文件页数（建议 < 20页）
3. 考虑分批处理大型文档

### Q4: JSON 解析失败

**症状**: `parseJSON` 函数返回 `rawText`

**解决**:
1. 检查 Qwen-VL 响应格式
2. 调整提示词，明确要求返回纯 JSON
3. 使用正则表达式提取 JSON

### Q5: 准确率不如预期

**解决**:
1. 优化提示词
2. 增加示例
3. 调整 temperature (当前 0.1)
4. 尝试更高级的模型 (qwen-vl-max)

---

## 📂 相关文件

| 文件 | 作用 |
|------|------|
| `cloudflare-worker-qwen-vl-max.js` | Cloudflare Worker 代码 |
| `qwen-vl-max-processor.js` | Qwen-VL Max 处理器 |
| `firstproject.html` | 主应用（繁体中文） |
| `en/firstproject.html` | 主应用（英文） |
| `kr/firstproject.html` | 主应用（韩文） |
| `jp/firstproject.html` | 主应用（日文） |

---

## ✅ 检查清单

### 部署前

- [ ] Cloudflare Worker 已创建并部署
- [ ] Worker URL 已复制
- [ ] API Key 已配置（推荐使用环境变量）
- [ ] Worker 已测试（curl 或 Postman）

### 代码修改

- [ ] `qwen-vl-max-processor.js` 已添加
- [ ] `firstproject.html` 已引入新处理器
- [ ] 处理器已初始化
- [ ] `uploadFile` 函数已修改
- [ ] `uploadFileDirect` 函数已修改

### 测试

- [ ] 本地测试通过（图片）
- [ ] PDF 文件测试通过
- [ ] 多页文档测试通过
- [ ] 发票和银行对账单都测试通过
- [ ] 性能对比完成
- [ ] 多语言版本测试通过

### 上线

- [ ] 生产环境 Worker 已部署
- [ ] 代码已提交到 Git
- [ ] 用户通知已发送（如需要）
- [ ] 监控已设置
- [ ] 回滚方案已准备

---

## 🚀 下一步

### 短期优化

1. **监控性能**: 收集实际使用数据
2. **优化提示词**: 根据反馈调整
3. **A/B 测试**: 对比两个处理器的效果

### 长期规划

1. **完全移除旧处理器**: 当 Qwen-VL 稳定后
2. **扩展到更多文档类型**: 保单、医疗发票等
3. **支持更多语言**: 日文、韩文文档
4. **批量处理优化**: 大型文档并行处理

---

**报告生成时间**: 2026-01-07  
**状态**: ✅ 集成指南创建完成  
**下一步**: 开始部署 Cloudflare Worker







