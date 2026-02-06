# Qwen-VL-Plus Deep Thinking 格式修复

**日期：** 2026-02-06  
**问题：** `enable_thinking` 参数位置错误，导致深度思考模式未生效  
**修复者：** AI Assistant

---

## 🐛 问题根源

### **错误的实现（2026-02-06 之前）**

**前端：**
```javascript
const requestBody = {
    model: "qwen3-vl-plus",
    enable_thinking: true,  // ❌ 错误位置
    messages: [...]
};
```

**Firebase Functions：**
```javascript
if (requestBody.enable_thinking) {
    qwenRequestBody.enable_thinking = true;  // ❌ 错误格式
}
```

### **症状**

- ICBC 工商银行提取失败，返回空白或错误数据
- Hang Seng 恒生银行提取不稳定，借贷分类错误
- API 调用成功，但未启用深度思考逻辑

---

## ✅ 正确的实现（阿里云官方格式）

### **参考来源**

**阿里云官方文档示例：**
```python
completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=[...],
    stream=True,
    extra_body={  # ← 关键！在 extra_body 中
        'enable_thinking': True,
        "thinking_budget": 81920
    }
)
```

**链接：** https://modelstudio.console.alibabacloud.com/ap-southeast-1/#/doc/?type=model&url=2840914_2&modelId=qwen3-vl-plus

---

## 🔧 修复内容

### **1. 前端（qwen-vl-max-processor.js）**

#### **单页处理（processDocument）**

```javascript
const requestBody = {
    model: selectedModel,
    messages: [...],
    temperature: 0.1,
    max_tokens: 4000
};

// 🔥 添加深度思考参数到 extra_body（阿里云官方格式）
if (enableThinking) {
    requestBody.extra_body = {
        enable_thinking: true,
        thinking_budget: 4000  // 思考预算：4000 tokens
    };
}
```

#### **多页处理（processMultiPageDocument）**

```javascript
const requestBody = {
    model: selectedModel,
    messages: [...],
    temperature: 0.1,
    max_tokens: enableThinking ? 4000 : 8000
};

// 🔥 添加深度思考参数到 extra_body（阿里云官方格式）
if (enableThinking) {
    requestBody.extra_body = {
        enable_thinking: true,
        thinking_budget: 4000
    };
}
```

### **2. Firebase Functions (firebase-functions/index.js)**

```javascript
// 构建 Qwen API 请求
// 检查前端是否传入 extra_body（包含 enable_thinking）
const extraBody = requestBody.extra_body || {};
const enableThinking = extraBody.enable_thinking === true;

// 深度思考模式最大4000 tokens（阿里云限制），标准模式最大28000
const maxTokensLimit = enableThinking ? 4000 : 28000;

const qwenRequestBody = {
    model: model,
    messages: requestBody.messages,
    temperature: requestBody.temperature || 0.1,
    max_tokens: Math.min(requestBody.max_tokens || maxTokensLimit, maxTokensLimit),
    stream: false
};

// 🔥 如果启用深度思考，添加 extra_body 参数（阿里云官方格式）
if (enableThinking) {
    qwenRequestBody.extra_body = {
        enable_thinking: true,
        thinking_budget: extraBody.thinking_budget || 4000
    };
    console.log(`   深度思考模式: ✅ 開啟 (max_tokens: ${qwenRequestBody.max_tokens}, thinking_budget: ${qwenRequestBody.extra_body.thinking_budget})`);
} else {
    console.log(`   標準模式 (max_tokens: ${qwenRequestBody.max_tokens})`);
}
```

---

## 📊 部署状态

| 组件 | 文件路径 | 状态 | 部署时间 |
|------|---------|------|----------|
| 前端 | qwen-vl-max-processor.js | ✅ 已修复 | 2026-02-06 |
| 后端 | firebase-functions/index.js | ✅ 已部署 | 2026-02-06 |
| 测试 | ICBC + Hang Seng | 🧪 待验证 | - |

**部署命令：**
```bash
cd /Users/cavlinyeung/ai-bank-parser/firebase-functions
firebase deploy --only functions:qwenProxy
```

**部署结果：**
```
✔  functions[qwenProxy(us-central1)] Successful update operation.
Function URL: https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/qwenProxy
```

---

## 🔍 验证测试

### **测试步骤：**

1. 上传 ICBC 工商银行单（Type A）
   - 检查日期、金额、借贷分类是否正确
   - 检查 Firebase Logs 是否显示 "深度思考模式: ✅ 開啟"

2. 上传 Hang Seng 恒生银行单（Type B）
   - 检查空白日期是否填充
   - 检查单日多交易是否正确分类
   - 检查余额是否正确

3. 上传收据（Receipt）
   - 检查是否使用标准模式（qwen3-vl-plus-2025-12-19）
   - 检查提取速度（标准模式应更快）

### **预期结果：**

| 文档类型 | 模型 | 深度思考 | max_tokens | thinking_budget |
|---------|------|----------|------------|-----------------|
| 银行单 | qwen3-vl-plus | ✅ 开启 | 4000 | 4000 |
| 收据 | qwen3-vl-plus-2025-12-19 | ⭕ 关闭 | 8000 | - |

---

## 📚 参考文档

1. **阿里云官方文档：**  
   https://modelstudio.console.alibabacloud.com/ap-southeast-1/#/doc/?type=model&url=2840914_2&modelId=qwen3-vl-plus

2. **Qwen-VL-Plus 深度思考模式：**  
   - `enable_thinking`: 启用深度推理
   - `thinking_budget`: 最大推理过程 Token 数
   - 支持范围：4,000 - 81,920 tokens
   - 我们使用：4,000 tokens（匹配账户余额限制）

3. **相关文档：**
   - `PROMPT_AB类通用版.md` - AB类银行单通用 Prompt
   - `PROMPT_更新总结_AB类通用版.md` - Prompt 优化历史
   - `AI模型选择优化_2026-02-06.md` - 模型选择策略

---

## 🎯 下一步

1. **验证测试：** 上传真实 ICBC 和 HSBC 银行单，验证修复效果
2. **成本监控：** 观察深度思考模式的 token 消耗
3. **准确率统计：** 对比修复前后的提取准确率
4. **用户反馈：** 收集用户对提取质量的反馈

---

**修复完成！✅ 现在 `enable_thinking` 使用正确的阿里云官方格式！**
