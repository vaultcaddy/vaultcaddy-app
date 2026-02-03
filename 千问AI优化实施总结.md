# 千问AI优化实施总结

> **日期：** 2026-02-03  
> **来源：** 千问AI（Qianwen AI）专业建议  
> **状态：** ✅ 已完成文档更新

---

## 📋 千问AI的核心建议

### 1. 优化后的Prompt - "VISUAL TEXT EXTRACTOR"模式

```
STRICT MODE: You are a VISUAL TEXT EXTRACTOR. 
ONLY copy visible text. ZERO calculation. ZERO inference. ZERO row merging.

📍 TARGET TABLE IDENTIFICATION:
- FIND table with headers: "Date" AND "Balance" (or "餘額"/"잔액"/"残高")
- IGNORE: "Summary"/"Total"/"總計"/"Account Summary"/"戶口摘要"
- CONFIRM: Dates in sequence (e.g., "22 Feb", "28 Feb", "7 Mar")

✂️ EXTRACTION RULES:
| Field       | Action                                                       |
|-------------|--------------------------------------------------------------|
| date        | COPY EXACT visible text. If blank → output "" (empty string)|
| description | COPY ALL text in row (including multi-line)                 |
| debit       | COPY number (remove commas) or 0 if blank                   |
| credit      | COPY number (remove commas) or 0 if blank                   |
| balance     | COPY number (remove commas). If blank/"—"/"N/A" → null      |

❗ ABSOLUTE COMMANDS:
- EACH VISUAL ROW = ONE transaction object. NEVER merge rows.
- If row has Description/Debit/Credit but blank Date → STILL output with date: ""
- Output ONLY valid JSON. NO explanations. NO markdown.
- Preserve original date format (e.g., "22 Feb", "2025-03-22")
```

**关键改进：**
- ✅ 从"OCR COPY MACHINE"升级为"VISUAL TEXT EXTRACTOR"
- ✅ 新增"ZERO row merging"规则
- ✅ 明确"EACH VISUAL ROW = ONE transaction"
- ✅ 多语言关键词支持

---

### 2. 规则引擎后处理 - 确定性逻辑处理

**Python伪代码（千问AI提供）：**

```python
def post_process(transactions):
    """轻量规则引擎：解决AI无法处理的跨行逻辑"""
    filled = []
    last_date = ""
    
    for tx in transactions:
        # ✅ 空日期填充（核心！）
        if not tx["date"].strip():
            tx["date"] = last_date  # 继承上一行日期
        else:
            last_date = tx["date"]  # 更新基准日期
        
        # ✅ 余额校验（预警异常跳变）
        if filled and tx["balance"] and filled[-1]["balance"]:
            delta = abs(tx["balance"] - filled[-1]["balance"])
            if delta > max(tx["debit"], tx["credit"]) * 1.5:  # 异常波动
                tx["warning"] = "balance_jump"
        
        filled.append(tx)
    
    return {
        "transactions": filled,
        "confidence": calculate_confidence(filled),  # 基于空字段率/警告数
        "needs_review": any(tx.get("warning") for tx in filled)
    }
```

**关键特点：**
- ✅ 规则1：空日期填充（解决同日多笔交易）
- ✅ 规则2：余额校验（预警异常跳变）
- ✅ 可扩展：轻松添加更多规则
- ✅ 可追溯：可记录规则应用日志

---

### 3. 多语言关键词映射库

**轻量JSON格式（非YAML爆炸）：**

```json
{
  "balance_keywords": ["Balance", "餘額", "잔액", "残高", "Solde"],
  "date_keywords": ["Date", "日期", "取引日", "거래일"],
  "ignore_sections": ["Summary", "總計", "합계", "Récapitulatif"]
}
```

**优势：**
- ✅ 轻量（1个JSON vs. 每家银行1个YAML）
- ✅ 易维护（添加新语言只需加几个关键词）
- ✅ 通用（适用于全球所有银行）

---

## ✅ 我们的实施状态

### 已完成：文档更新

1. **✅ CURRENT_WORKFLOW_EXPLANATION.md**
   - 更新为10步流程图
   - 集成千问AI的Prompt优化
   - 添加规则引擎详细说明
   - 新增多语言支持说明

2. **✅ 当前转换流程说明.md**
   - 同步更新Prompt说明
   - 强调规则引擎概念
   - 添加职责分离说明

3. **✅ 工作流程摘要.md**
   - 更新核心机制说明
   - 添加千问AI优化对比表
   - 扩展用户体验亮点

---

### 待实施：代码更新

根据千问AI的建议，以下代码需要更新：

#### 1. 更新Prompt（qwen-vl-max-processor.js）

**需要修改的位置：**
```javascript
// 文件：qwen-vl-max-processor.js
// 函数：generatePrompt(documentType)
```

**修改内容：**
- [ ] 将"OCR COPY MACHINE"改为"VISUAL TEXT EXTRACTOR"
- [ ] 添加"ZERO row merging"规则
- [ ] 添加"EACH VISUAL ROW = ONE transaction"说明
- [ ] 更新多语言关键词（Balance/餘額/잔액/残高）

#### 2. 增强规则引擎（qwen-vl-max-processor.js）

**需要修改的位置：**
```javascript
// 文件：qwen-vl-max-processor.js
// 函数：postProcessTransactions(extractedData)
```

**修改内容：**
- [x] 规则1：空日期填充（已实施）
- [ ] 规则2：余额校验（待添加）
- [ ] 添加warning字段支持
- [ ] 添加confidence计算
- [ ] 添加needs_review标记

#### 3. 创建多语言关键词映射（新文件）

**建议创建：**
```
keywords-mapping.json
```

**内容：**
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

---

## 📊 千问AI优化前后对比

| 方面 | 旧版 | 新版（千问优化） | 改进 |
|------|------|------------------|------|
| **AI定位** | "OCR COPY MACHINE" | "VISUAL TEXT EXTRACTOR" | 更精准的职责定位 |
| **行处理** | 未明确 | "ZERO row merging" | 禁止AI自行合并行 |
| **规则引擎** | 单一规则 | 规则1+2（可扩展） | 系统化处理 |
| **职责分离** | 混合 | AI提取 + 规则处理 | 清晰分工 |
| **语言支持** | 中文为主 | 多语言关键词 | 全球适用 |
| **数据校验** | 无 | 余额跳变预警 | 异常检测 |
| **可扩展性** | 低 | 高 | 轻松添加新规则 |
| **可追溯性** | 低 | 高 | 可记录规则日志 |

---

## 🎯 下一步行动

### 优先级1：代码实施（核心功能）

1. **更新Prompt**
   - 修改`qwen-vl-max-processor.js`中的`generatePrompt()`
   - 测试新Prompt对恒生银行的识别效果

2. **增强规则引擎**
   - 在`postProcessTransactions()`中添加规则2（余额校验）
   - 添加warning字段支持

### 优先级2：多语言支持（扩展功能）

3. **创建关键词映射**
   - 创建`keywords-mapping.json`
   - 在Prompt中引用关键词

### 优先级3：测试验证

4. **测试恒生银行对账单**
   - 验证空日期填充是否有效
   - 检查余额校验是否正常工作

5. **测试其他银行**
   - 工商银行（已正确）
   - 其他银行（待测试）

---

## 📝 总结

**千问AI的核心贡献：**
1. ✅ 明确了AI和规则引擎的职责边界
2. ✅ 提供了"VISUAL TEXT EXTRACTOR"的精准定位
3. ✅ 建议了轻量级的多语言支持方案
4. ✅ 提出了可扩展的规则引擎架构

**我们的实施进度：**
- ✅ **文档更新**：100%完成
- 🔄 **代码实施**：部分完成（规则1已实施，规则2待添加）
- ⏳ **多语言支持**：待实施
- ⏳ **测试验证**：待进行

**预期效果：**
- ✅ 恒生银行同日多笔交易问题：规则1可解决
- ✅ 数据质量提升：规则2可预警异常
- ✅ 全球银行支持：多语言关键词可扩展
- ✅ 系统可维护性：规则引擎架构清晰

---

**文档版本：** 1.0  
**创建日期：** 2026-02-03  
**维护者：** AI助手  
**感谢：** 千问AI（Qianwen AI）的专业建议
