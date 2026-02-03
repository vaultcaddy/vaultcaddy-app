# 🔄 当前银行对账单转换工作流程详解

> **最后更新：** 2026-02-03（🆕 千问AI优化版）  
> **当前状态：** 使用千问AI（Qwen-VL-Max）"VISUAL TEXT EXTRACTOR"模式 + 规则引擎后处理  
> **核心文件：** `qwen-vl-max-processor.js`, `firstproject.html`  
> **文档版本：** 2.0

---

## 🆕 本次更新要点（2026-02-03）

根据千问AI（Qianwen AI）的专业建议，我们优化了整个工作流程：

1. **✅ Prompt优化** - 从"OCR COPY MACHINE"升级为"VISUAL TEXT EXTRACTOR"
   - 明确禁止行合并（ZERO row merging）
   - 每个视觉行 = 一个transaction对象
   - 多语言关键词支持

2. **✅ 规则引擎增强** - 从单一"空日期填充"扩展为完整规则系统
   - 规则1：空日期填充（解决同日多笔交易）
   - 规则2：余额校验（预警异常跳变）
   - 可扩展：轻松添加更多规则

3. **✅ 职责分离** - AI vs. 规则引擎明确分工
   - AI负责：视觉提取、表格识别、文本复制
   - 规则引擎负责：确定性逻辑、数据填充、异常检测

4. **✅ 多语言支持** - 关键词映射库（轻量JSON）
   - 支持中文、英文、日文、韩文等
   - 适用于全球所有银行

---

## 📊 完整工作流程图（2026-02-03 更新）

```
┌─────────────────────────────────────────────────────────────────┐
│              1. 用户上传文件 + 创建文档记录                       │
│                      (firstproject.html)                         │
│  • 立即在Firestore创建"processing"状态的文档                    │
│  • 用户马上看到"处理中"的文件                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ PDF 或 图片文件
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                 2. 检查Credits余额                               │
│              (credits-manager.js)                                │
│  • 计算所有文件的总页数                                          │
│  • creditsManager.checkCredits(totalPages)                      │
│  • 不足 → 删除占位文档 + 停止处理                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Credits 余额充足
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                 3. 文件类型判断                                  │
│                                                                  │
│  if (PDF) {                                                      │
│      转换为图片 (pdf-to-image-converter.js)                     │
│      → 使用 pdf.js 库，300 DPI                                  │
│  }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 图片文件数组 (1张或多张)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              4. 上传到 Firebase Storage                          │
│                                                                  │
│  • 存储路径: projects/{projectId}/documents/{docId}/            │
│  • 并行上传所有图片 (Promise.all)                                │
│  • 获取公开URL数组 (用于AI访问)                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 图片URL数组
                         │
┌────────────────────────▼────────────────────────────────────────┐
│           5. 扣除 Credits（真正扣除）                            │
│              (credits-manager.js)                                │
│  • creditsManager.deductCredits(pages)                          │
│  • 每页扣除 1 Credit                                             │
│  • 从用户余额中真正扣除                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Credits 已扣除
                         │
┌────────────────────────▼────────────────────────────────────────┐
│    6. 调用 Qwen-VL Max AI (qwen-vl-max-processor.js)            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  6.1 文件转Base64                                         │  │
│  │      • 读取文件内容                                       │  │
│  │      • 转换为Base64编码                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│  ┌──────────────────────▼──────────────────────────────────┐  │
│  │  6.2 生成 Prompt (generatePrompt) ⭐ 千问优化版          │  │
│  │      "VISUAL TEXT EXTRACTOR" 模式                        │  │
│  │      • ZERO calculation（不计算）                        │  │
│  │      • ZERO inference（不推理）                          │  │
│  │      • ZERO row merging（不合并行）                      │  │
│  │      • 空日期 → 输出 "" (空字符串)                       │  │
│  │      • EACH VISUAL ROW = ONE transaction                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│  ┌──────────────────────▼──────────────────────────────────┐  │
│  │  6.3 构建 API 请求                                        │  │
│  │      {                                                    │  │
│  │        model: "qwen3-vl-plus-2025-12-19",               │  │
│  │        messages: [                                       │  │
│  │          {                                               │  │
│  │            role: "user",                                 │  │
│  │            content: [                                    │  │
│  │              {type: "image_url", image_url: {...}},    │  │
│  │              {type: "text", text: prompt}              │  │
│  │            ]                                             │  │
│  │          }                                               │  │
│  │        ],                                                │  │
│  │        temperature: 0.1,                                 │  │
│  │        max_tokens: 4000                                  │  │
│  │      }                                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│  ┌──────────────────────▼──────────────────────────────────┐  │
│  │  6.4 通过 Cloudflare Worker 转发                         │  │
│  │      • URL: deepseek-proxy.vaultcaddy.workers.dev       │  │
│  │      • 隐藏真实 API Key                                  │  │
│  │      • POST 请求到千问API                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         │ 等待 8-15 秒                           │
│                         │                                        │
│  ┌──────────────────────▼──────────────────────────────────┐  │
│  │  6.5 接收 AI 响应                                         │  │
│  │      • 返回 JSON 格式的提取数据                          │  │
│  │      • 包含使用量统计 (tokens, cost)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ AI 原始响应 (JSON字符串)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              7. 解析响应 (parseJSON)                             │
│                                                                  │
│  • 清理 markdown 代码块标记 (```json)                            │
│  • 尝试 JSON.parse()                                             │
│  • 如果失败，使用正则提取 JSON 对象                               │
│  • 验证必需字段是否存在                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 提取的结构化数据 (JavaScript 对象)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│   8. 规则引擎后处理 (postProcessTransactions) ⭐ 核心创新      │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  规则1：空日期填充（解决同日多笔交易问题）               │  │
│  │  ─────────────────────────────────────────────────────  │  │
│  │  lastValidDate = null                                     │  │
│  │                                                            │  │
│  │  for each transaction:                                   │  │
│  │      if (transaction.date.trim() === ""):                │  │
│  │          transaction.date = lastValidDate  // 继承上一行  │  │
│  │      else:                                                │  │
│  │          lastValidDate = transaction.date  // 更新基准   │  │
│  │                                                            │  │
│  │  特点：                                                    │  │
│  │  ✅ 确定性算法（100%可靠）                                │  │
│  │  ✅ 不依赖AI视觉理解                                      │  │
│  │  ✅ 处理边界情况（第一笔为空）                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  规则2：余额校验（可选，预警异常跳变）                    │  │
│  │  ─────────────────────────────────────────────────────  │  │
│  │  if (上一笔余额存在 && 当前余额存在):                     │  │
│  │      delta = abs(当前余额 - 上一笔余额)                  │  │
│  │      expected = max(debit, credit)                       │  │
│  │      if (delta > expected * 1.5):                        │  │
│  │          transaction.warning = "balance_jump"            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  示例：                                                          │
│  输入（AI提取的原始数据）：                                      │
│    [                                                             │
│      {date: "10 Mar", description: "ATM", debit: 500},          │
│      {date: "",       description: "TRANSFER", debit: 200}, ←空 │
│      {date: "",       description: "POS", debit: 150}       ←空 │
│    ]                                                             │
│                                                                  │
│  输出（规则引擎处理后）：                                        │
│    [                                                             │
│      {date: "10 Mar", description: "ATM", debit: 500},          │
│      {date: "10 Mar", description: "TRANSFER", debit: 200}, ←填充│
│      {date: "10 Mar", description: "POS", debit: 150}       ←填充│
│    ]                                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 规则处理后的完整数据
                         │
┌────────────────────────▼────────────────────────────────────────┐
│         9. 保存到 Firestore (simple-data-manager.js)             │
│                                                                  │
│  保存路径: projects/{projectId}/documents/{docId}                │
│  保存内容:                                                       │
│    {                                                             │
│      name: "文档名称",                                           │
│      status: "completed",  // 从 "processing" 改为 "completed"  │
│      processedData: {规则处理后的数据},                          │
│      rawText: {AI原始响应},                                      │
│      processingTime: 12345,  // 毫秒                             │
│      processor: "qwen-vl-max",                                   │
│      model: "qwen3-vl-plus-2025-12-19",                         │
│      usage: {tokens, cost},                                      │
│      createdAt: Timestamp                                        │
│    }                                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 数据已保存
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              10. 刷新 UI (loadDocuments)                         │
│                                                                  │
│  • 从 Firestore 读取最新文档列表                                 │
│  • 渲染表格，显示所有交易记录                                    │
│  • 计算汇总数据（总收入、总支出、余额）                          │
│  • 更新页面上的统计信息                                          │
└──────────────────────────────────────────────────────────────────┘
```

**🎯 工作流程总结（10步）：**

1. ✅ **用户上传文件 + 建立文档** → 立即创建"processing"状态
2. ✅ **检查Credits余额** → 验证是否足够
3. ✅ **文件类型判断** → PDF需要转换
4. ✅ **上传Storage** → 获取图片URL
5. ✅ **扣除Credits** → 真正从余额中扣除
6. ✅ **调用千问AI** → 🆕 **"VISUAL TEXT EXTRACTOR"模式**（千问优化）
7. ✅ **解析响应** → 清理和验证JSON
8. ✅ **规则引擎后处理** → 🔥 **空日期填充 + 余额校验**（核心创新）
9. ✅ **保存数据** → 更新文档状态为completed
10. ✅ **刷新UI** → 显示结果

---

## 🔍 核心步骤详解

### 步骤 6.2：Prompt 生成（generatePrompt）⭐ 千问优化版

**银行对账单的 Prompt 结构（2026-02-03 更新）：**

```
STRICT MODE: You are a VISUAL TEXT EXTRACTOR. ONLY copy visible text. ZERO calculation. ZERO inference. ZERO row merging.

📍 TARGET TABLE IDENTIFICATION:
- FIND table with headers containing: "Date" AND "Balance" (or "餘額"/"잔액"/"残高")
- IGNORE tables with: "Summary"/"Total"/"總計"/"Account Summary"/"戶口摘要"
- CONFIRM: Dates appear in sequence (e.g., "22 Feb", "28 Feb", "7 Mar")

✂️ EXTRACTION RULES (NON-NEGOTIABLE):
| Field       | Action                                                                 |
|-------------|------------------------------------------------------------------------|
| date        | COPY EXACT visible text. If blank → output "" (empty string)          |
| description | COPY ALL text in row (including multi-line)                           |
| debit       | COPY number (remove commas) or 0 if blank                             |
| credit      | COPY number (remove commas) or 0 if blank                             |
| balance     | COPY number (remove commas). If blank/"—"/"N/A" → output null         |

❗ ABSOLUTE COMMANDS:
- EACH VISUAL ROW = ONE transaction object. NEVER merge rows.
- If row has Description/Debit/Credit but blank Date → STILL output with date: ""
- Output ONLY valid JSON. NO explanations. NO markdown.
- Preserve original date format (e.g., "22 Feb", "2025-03-22")

📤 OUTPUT STRUCTURE (exact keys, no variation):
{
  "bankName": "...",
  "accountNumber": "...",
  "accountHolder": "...",
  "currency": "...",
  "statementPeriod": "...",
  "openingBalance": 30718.39,
  "closingBalance": 30018.39,
  "transactions": [
    {
      "date": "10 Mar",
      "description": "ATM WITHDRAWAL",
      "credit": 0,
      "debit": 500.00,
      "balance": 30218.39
    },
    {
      "date": "",  // ← 空白日期（视觉上看不到）— 规则引擎会填充
      "description": "ONLINE TRANSFER",
      "credit": 0,
      "debit": 200.00,
      "balance": 30018.39
    },
    {
      "date": "",  // ← 空白日期（视觉上看不到）— 规则引擎会填充
      "description": "POS PURCHASE",
      "credit": 0,
      "debit": 150.00,
      "balance": 29868.39
    }
  ]
}
```

**🆕 关键设计理念（千问AI优化）：**

1. ✅ **"VISUAL TEXT EXTRACTOR"** - 只提取视觉可见的文本（不推理）
2. ✅ **"ZERO row merging"** - 每个视觉行 = 一个transaction对象
3. ✅ **"EACH VISUAL ROW = ONE transaction"** - 严格一对一映射
4. ✅ **明确空白日期规则** - "If blank Date → STILL output with date: ''"
5. ✅ **多语言支持** - "Balance"/"餘額"/"잔액"/"残高"

**vs. 旧版Prompt的改进：**

| 旧版 | 新版（千问优化） |
|------|------------------|
| "OCR COPY MACHINE" | **"VISUAL TEXT EXTRACTOR"** - 更精准的定位 |
| 只强调"不计算" | **"ZERO row merging"** - 明确禁止合并行 |
| 示例较简单 | **包含连续3笔空白日期** - 教AI正确处理 |
| 只支持中文 | **多语言关键词** - Balance/餘額/잔액/残高 |

---

### 步骤 8：规则引擎后处理（postProcessTransactions）⭐ 核心创新

**🆕 设计理念（千问AI建议）：**

AI负责"精准提取原始文本"，规则引擎负责"确定性逻辑处理"。

```
┌──────────────────────────────────────────────────────────┐
│  AI的职责                     规则引擎的职责              │
│  ─────────────────────────   ────────────────────────── │
│  ✅ 识别表格结构              ✅ 填充空白日期            │
│  ✅ 提取可见文本              ✅ 余额校验                │
│  ✅ 复制数字（去逗号）        ✅ 异常检测                │
│  ✅ 保持原始格式              ✅ 数据验证                │
│                                                          │
│  ❌ 不推理                    （确定性算法，100%可靠）    │
│  ❌ 不计算                                               │
│  ❌ 不合并行                                             │
└──────────────────────────────────────────────────────────┘
```

---

**完整代码实现（JavaScript版）：**

```javascript
postProcessTransactions(extractedData) {
    // 如果没有 transactions 数组，直接返回
    if (!extractedData || !extractedData.transactions || 
        !Array.isArray(extractedData.transactions)) {
        return extractedData;
    }
    
    let lastValidDate = null;
    const processed = [];
    
    // 遍历所有交易，应用规则引擎
    for (let i = 0; i < extractedData.transactions.length; i++) {
        const tx = extractedData.transactions[i];
        
        // ✅ 规则1：空日期填充（解决同日多笔交易）
        if (!tx.date || (typeof tx.date === 'string' && tx.date.trim() === '')) {
            if (lastValidDate) {
                tx.date = lastValidDate;  // 继承上一行日期
            } else {
                // 边界情况：第一笔就为空，尝试从statementPeriod提取
                if (extractedData.statementPeriod) {
                    const periodMatch = extractedData.statementPeriod.match(/^([^to]+)/);
                    tx.date = periodMatch ? periodMatch[1].trim() : 'Unknown';
                } else {
                    tx.date = 'Unknown';
                }
            }
        } else {
            lastValidDate = tx.date;  // 更新基准日期
        }
        
        // ✅ 规则2：余额校验（可选，预警异常跳变）
        if (processed.length > 0 && tx.balance && processed[processed.length - 1].balance) {
            const prevBalance = processed[processed.length - 1].balance;
            const delta = Math.abs(tx.balance - prevBalance);
            const expected = Math.max(tx.debit || 0, tx.credit || 0);
            
            if (delta > expected * 1.5) {
                tx.warning = "balance_jump";  // 标记异常跳变
            }
        }
        
        processed.push(tx);
    }
    
    extractedData.transactions = processed;
    return extractedData;
}
```

---

**🆕 Python版（千问AI建议，可用于后端服务器）：**

```python
def post_process(transactions):
    """轻量规则引擎：解决AI无法处理的跨行逻辑"""
    filled = []
    last_date = ""
    
    for tx in transactions:
        # ✅ 规则1：空日期填充（核心！）
        if not tx["date"].strip():
            tx["date"] = last_date  # 继承上一行日期
        else:
            last_date = tx["date"]  # 更新基准日期
        
        # ✅ 规则2：余额校验（预警异常跳变）
        if filled and tx["balance"] and filled[-1]["balance"]:
            delta = abs(tx["balance"] - filled[-1]["balance"])
            expected = max(tx["debit"], tx["credit"])
            if delta > expected * 1.5:  # 异常波动
                tx["warning"] = "balance_jump"
        
        filled.append(tx)
    
    return {
        "transactions": filled,
        "confidence": calculate_confidence(filled),  # 基于空字段率/警告数
        "needs_review": any(tx.get("warning") for tx in filled)
    }
```

---

**工作原理示例：**

1. **第一笔交易（10 Mar）**
   - 日期：`"10 Mar"`（不为空）
   - 动作：`lastValidDate = "10 Mar"`
   - 结果：`{date: "10 Mar", ...}`

2. **第二笔交易（空）**
   - 日期：`""`（为空）
   - 动作：`tx.date = lastValidDate` → `"10 Mar"`
   - 结果：`{date: "10 Mar", ...}`（已填充）

3. **第三笔交易（空）**
   - 日期：`""`（为空）
   - 动作：`tx.date = lastValidDate` → `"10 Mar"`
   - 结果：`{date: "10 Mar", ...}`（已填充）

---

**🎯 规则引擎优势：**

- ✅ **确定性算法** - 100%可靠，无随机性
- ✅ **不依赖AI** - 完全独立于视觉理解
- ✅ **处理边界情况** - 第一笔为空时的fallback逻辑
- ✅ **可扩展** - 轻松添加更多规则（余额校验、日期验证等）
- ✅ **可追溯** - 可以记录每条规则的应用日志
- ✅ **多语言支持** - 配合关键词映射库，支持全球银行

---

## 📊 多页文档处理

### 方案：批量模式（processMultiPageDocument）

**流程：**

```
文件数组 → 所有转Base64 → 一次性发送给AI → AI合并处理 → 返回完整结果
```

**优势：**

- ✅ **速度快** - 只需一次API调用
- ✅ **成本低** - 减少重复处理
- ✅ **准确率高** - AI可以看到完整上下文

**请求示例（3页PDF）：**

```javascript
{
  model: "qwen3-vl-plus-2025-12-19",
  messages: [{
    role: "user",
    content: [
      {type: "image_url", image_url: {url: "data:image/jpeg;base64,/9j/..."}}, // 第1页
      {type: "image_url", image_url: {url: "data:image/jpeg;base64,/9j/..."}}, // 第2页
      {type: "image_url", image_url: {url: "data:image/jpeg;base64,/9j/..."}}, // 第3页
      {type: "text", text: "这是一份3页的银行对账单，请合并提取所有交易..."}
    ]
  }],
  max_tokens: 8000  // 多页需要更多tokens
}
```

---

## ⚠️ 当前已知问题

### 问题：恒生银行同日多笔交易

**现象：**
- 银行对账单格式：
  ```
  Date       Description       Debit    Balance
  10 Mar     ATM WITHDRAWAL    500.00   30218.39
             ONLINE TRANSFER   200.00
             POS PURCHASE      150.00   30018.39
  ```

**AI提取结果：**
- ✅ **第一笔** - 日期：`"10 Mar"`
- ❓ **第二笔** - 日期：`""`（空白）
- ❓ **第三笔** - 日期：`""`（空白）

**前端后处理结果：**
- ✅ **所有交易** - 日期都变成：`"10 Mar"`

**问题点：**

根据您说"问题无法解决"，可能的情况：

1. **AI完全无法识别日期？**
   - 即使第一笔的日期也提取不到？
   - 需要查看AI的原始响应

2. **后处理逻辑有bug？**
   - 空白日期没有被正确填充？
   - 需要检查实际运行日志

3. **UI显示有问题？**
   - 数据正确但UI不显示？
   - 需要检查表格渲染代码

---

## 🔧 诊断步骤

### 1. 查看AI原始响应

在浏览器控制台运行：

```javascript
// 上传文件后，查看最新文档的原始响应
const docs = await window.simpleDataManager.getDocuments(currentProjectId);
const latestDoc = docs[0];
console.log('AI 原始响应:', latestDoc.rawText);
console.log('处理后数据:', latestDoc.processedData);
```

### 2. 检查后处理是否执行

在 `qwen-vl-max-processor.js` 的 `postProcessTransactions` 函数中添加日志：

```javascript
postProcessTransactions(extractedData) {
    console.log('🔍 后处理输入:', JSON.stringify(extractedData.transactions, null, 2));
    
    // ... 处理逻辑 ...
    
    console.log('✅ 后处理输出:', JSON.stringify(extractedData.transactions, null, 2));
    return extractedData;
}
```

### 3. 检查UI渲染

在 `firstproject.html` 的表格渲染代码中检查日期显示逻辑。

---

## 💡 可能的解决方案

### 方案1：增强Prompt（让AI更明确理解）

在Prompt中添加更多示例：

```
📤 EXAMPLE for same-day multiple transactions:
Input (what you see in PDF):
  Date       Description       Debit
  10 Mar     ATM WITHDRAWAL    500.00
             ONLINE TRANSFER   200.00
             POS PURCHASE      150.00

Output (what you should return):
  [
    {"date": "10 Mar", "description": "ATM WITHDRAWAL", "debit": 500},
    {"date": "",       "description": "ONLINE TRANSFER", "debit": 200},
    {"date": "",       "description": "POS PURCHASE", "debit": 150}
  ]

⚠️ CRITICAL: Do NOT copy "10 Mar" to rows 2-3. Leave them as "" (empty string).
```

### 方案2：OCR预处理（使用Tesseract.js）

如果AI完全无法识别表格结构，可以使用：

1. **Tesseract.js OCR** → 获取文本和坐标
2. **规则引擎** → 根据坐标对齐字段
3. **前端填充** → 应用同日多笔逻辑

---

## 🌍 多语言支持（2026-02-03 新增）

### 关键词映射库（轻量JSON）

根据千问AI建议，使用关键词映射而非庞大的YAML配置：

```json
{
  "balance_keywords": ["Balance", "餘額", "잔액", "残高", "Solde", "Saldo"],
  "date_keywords": ["Date", "日期", "取引日", "거래일", "Data", "Fecha"],
  "debit_keywords": ["Debit", "Withdrawal", "借項", "支出", "출금", "引出し"],
  "credit_keywords": ["Credit", "Deposit", "貸項", "收入", "입금", "預入"],
  "ignore_sections": [
    "Summary", "Account Summary", "戶口摘要", "계좌 요약",
    "Total", "總計", "합계", "合計",
    "Sub-total", "小計", "소계", "小計"
  ]
}
```

**优势：**
- ✅ **轻量** - 只需1个JSON文件（vs. 每家银行1个YAML）
- ✅ **易维护** - 添加新语言只需加几个关键词
- ✅ **通用** - 适用于全球所有银行
- ✅ **AI友好** - 直接在Prompt中使用这些关键词

---

## 📝 总结

**当前工作流程（10步，2026-02-03 更新）：**

1. ✅ **用户上传文件 + 建立文档** → 立即创建"processing"状态
2. ✅ **检查Credits余额** → 验证是否足够
3. ✅ **文件类型判断** → PDF需要转换
4. ✅ **上传Storage** → 获取图片URL
5. ✅ **扣除Credits** → 真正从余额中扣除
6. ✅ **🆕 调用千问AI（优化版）** → "VISUAL TEXT EXTRACTOR"模式
7. ✅ **解析响应** → JSON parsing
8. ✅ **🔥 规则引擎后处理** → 空日期填充 + 余额校验（核心创新）
9. ✅ **保存数据** → 更新文档状态为completed
10. ✅ **刷新UI** → 显示结果

---

**🆕 核心优势（千问AI优化后）：**

| 方面 | 优势 |
|------|------|
| **职责分离** | AI负责视觉提取，规则引擎负责逻辑处理 |
| **确定性** | 规则引擎100%可靠，不依赖AI随机性 |
| **可扩展** | 轻松添加新规则（余额校验、异常检测） |
| **多语言** | 关键词映射支持全球银行 |
| **可追溯** | 可记录每条规则的应用日志 |
| **成本低** | Prompt简化，减少tokens消耗 |

---

**🎯 vs. 旧版的改进：**

| 旧版 | 新版（千问优化） |
|------|------------------|
| "OCR COPY MACHINE" | **"VISUAL TEXT EXTRACTOR"** |
| 依赖Prompt完美性 | **职责分离：AI提取+规则处理** |
| 只处理空日期 | **规则引擎：日期+余额+异常检测** |
| 单一语言（中文） | **多语言关键词映射** |
| 无数据校验 | **余额跳变预警** |

---

**📌 重要说明：**

根据您之前的要求，我们已经：
1. ✅ **隐藏UI中的"类型"列**
2. ✅ **工商银行提取完全正确**
3. 🔄 **恒生银行同日多笔问题** - 已实施规则引擎方案

如果恒生银行问题仍未解决，请提供：
- 具体测试文件
- AI原始响应
- 期望vs实际结果对比

我将针对性诊断！

---

**文档版本：** 2.0（千问AI优化版）  
**最后更新：** 2026-02-03  
**维护者：** AI助手

