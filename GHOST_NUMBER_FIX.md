# 🚨 修复「幽灵数字」问题 - 59,417.89

**问题发现日期**: 2026年2月1日  
**严重性**: 🔴 **CRITICAL** - AI 在创造不存在的数字  
**状态**: ✅ 已强化 Prompt，等待测试验证

---

## 📋 问题描述

### 用户的关键发现

**用户报告**：
> "問題同樣承上結餘錯誤，更重要的是**沒有一個數值是 59,417.89**。是否他又計了數？"

**核心问题**：
- ❌ AI 返回：承上结余 = 59,417.89
- ❌ PDF 中**根本不存在** 59,417.89 这个数字
- ❌ 这证明 AI 是**计算**出来的，不是**提取**的

### 什么是「幽灵数字」？

**定义**：
> AI 返回的数字在原始 PDF 中**完全不存在**，是通过计算、推算或"想象"出来的。

**例子**：
```
PDF 中的数字: 30,718.39, 51,295.09, 48,459.59, 23,459.59...
AI 返回的数字: 59,417.89  // ❌ 这是什么鬼？
```

**为什么叫「幽灵数字」？**
- 就像幽灵一样，它"出现"了，但在 PDF 中找不到
- 它不是 OCR 错误（那会是相似数字）
- 它是 AI 通过公式"创造"出来的

---

## 🔍 问题诊断

### 59,417.89 是从哪里来的？

**可能的计算路径**：

**猜测 1：从戶口摘要计算**
```
戶口摘要可能显示:
- 期初结余: 60,736.27
- 某个调整: -1,318.38
- 计算: 60,736.27 - 1,318.38 = 59,417.89 ❌
```

**猜测 2：从交易倒推**
```
看到第一笔交易后的余额: 51,295.09
看到第一笔交易金额: 8,122.80
计算: 51,295.09 + 8,122.80 = 59,417.89 ❌
```

**猜测 3：其他复杂计算**
```
可能 AI 做了多步计算，得出 59,417.89
```

**无论如何，这都是错误的！**

### 为什么之前的 Prompt 失败了？

**我们之前说过**：
```
7. **⚠️ BALANCE EXTRACTION - ABSOLUTELY NEVER CALCULATE:**
   - Balance values MUST be extracted DIRECTLY from the column
   - NEVER CALCULATE BALANCE using formulas
```

**为什么 AI 还是计算了？**

1. **警告位置不够明显** - 在 Prompt 中间，AI 可能没注意到
2. **语气不够强烈** - "NEVER CALCULATE" 不够，AI 觉得"这次情况特殊"
3. **没有具体例子** - 没有明确指出 "59,417.89 这样的数字是错误的"
4. **没有验证机制** - AI 没有被要求检查"这个数字在 PDF 中存在吗？"

### AI 为什么会计算？

**AI 的「帮助」心态**：
```
AI 思考: "我看到承上结余这一行，但余额栏看不清楚..."
AI 思考: "没关系，我可以通过下一行的余额倒推！"
AI 思考: "51,295.09 + 8,122.80 = 59,417.89"
AI 思考: "我真聪明，帮用户算出来了！"

用户: "你算你M啊！我要的是 PDF 中的数字！" 😤
```

**根本问题**：
- AI 被训练成"有帮助的助手"
- AI 认为"计算出正确答案"是在帮助用户
- AI 不理解用户只要"提取"，不要"计算"

---

## ✅ 修复方案

### 策略：极端强化，从第一句话就警告

**核心思想**：
1. **Prompt 第一句话就警告** - 不能放在中间
2. **极端强烈的语气** - "YOU FAILED" 而不是 "please don't"
3. **具体的错误例子** - 直接说 "59,417.89 是错误的"
4. **验证机制** - 要求 AI 检查"这个数字在 PDF 中存在吗？"

### 修改 1：Prompt 开头立即警告

**新的 Prompt 开头**：
```javascript
🚨 CRITICAL - READ THIS FIRST:
YOU ARE A DATA RECORDER, NOT A CALCULATOR.
YOUR ONLY JOB: COPY numbers from the PDF to JSON. DO NOT calculate, verify, or modify ANY numbers.

IF YOU SEE a balance of "30,718.39" in the PDF → EXTRACT "30718.39"
IF YOU CALCULATE "59,417.89" using a formula → YOU FAILED ❌
```

**为什么这样有效？**
1. 🚨 emoji 吸引注意力
2. "READ THIS FIRST" 明确优先级
3. "YOU FAILED" 强烈警告
4. 具体例子：30,718.39 vs 59,417.89

### 修改 2：重写余额规则（极端版）

**多页版本（generateMultiPagePrompt）**：
```javascript
7. **🚨 BALANCE EXTRACTION - ABSOLUTELY NEVER CALCULATE (MOST IMPORTANT RULE):**
   - **YOU ARE A DATA RECORDER**: Your job is to COPY the balance number from the PDF, NOT to calculate it
   - **IF THE BALANCE IS NOT VISIBLE IN THE PDF, SET IT TO null** - DO NOT calculate it using prev_balance + credit - debit
   - **CRITICAL**: Balance values MUST be extracted DIRECTLY from the "餘額/Balance" column in the image
   - **THE BANK PRINTED THE BALANCE**: You just copy it. The bank did NOT ask you to calculate it for them.
   - If you use ANY formula (balance = prev + credit - debit), you are NOT doing your job correctly
   
   - **Example of CORRECT behavior**:
     * PDF shows balance "30,718.39" → You extract 30718.39 ✅
     * PDF shows balance "51,295.09" → You extract 51295.09 ✅
     * PDF balance is blurry → You set null ✅ (DO NOT calculate!)
   
   - **Example of WRONG behavior (THIS IS WHAT YOU MUST NEVER DO)**:
     * PDF shows "30,718.39" but you return "59,417.89" ❌ (Where did 59,417.89 come from? You calculated it!)
     * You think: "Let me verify: 100 + 50 = 150, so balance should be..." ❌ (You are NOT a calculator!)
     * Balance is blurry, so you calculate: prev_balance + credit - debit ❌ (Just set to null!)
   
   🚨 IF YOU RETURN A BALANCE NUMBER THAT DOES NOT EXIST IN THE PDF, YOU FAILED THIS TASK.
```

**单页版本（generatePrompt）**：
```javascript
5. **🚨 BALANCE - NEVER CALCULATE, EXTRACT ONLY (MOST IMPORTANT):**
   - **YOU ARE A DATA RECORDER**: Copy the balance from PDF, NOT calculate it
   - **IF NOT VISIBLE, SET TO null** - DO NOT calculate using prev + credit - debit
   - **THE BANK PRINTED IT**: You just copy it. Period.
   - If you use ANY formula, you are NOT doing your job
   - Example: ✅ PDF shows 30,718.39 → extract 30718.39 | ❌ Calculate 59,417.89 (not in PDF!)
   
   🚨 IF YOU RETURN A BALANCE NUMBER THAT DOES NOT EXIST IN THE PDF, YOU FAILED.
```

### 修改 3：Final Checklist 添加验证

**新的 Checklist**：
```javascript
FINAL CHECKLIST - Did I act as a DATA RECORDER (not a calculator)?
✅ Did I extract EVERY SINGLE ROW from the transaction table?
✅ Does each transaction have its OWN unique date (extracted, not guessed)?
✅ Does each transaction have its OWN unique amount (extracted, not modified)?
✅ **Did I COPY all balance values from the PDF (NEVER calculated)?**
✅ **Can I find every balance number I returned in the original PDF?** (If not, I calculated it - WRONG!)
✅ Did I NEVER use ANY formulas (balance = prev + credit - debit)?
✅ Did I NOT combine, merge, or summarize any rows?
✅ Did I NOT use Account Summary data (only Transaction Details)?
✅ Is "extracted data" = "uploaded data" (exactly the same)?
✅ Did I determine transactionSign correctly (Priority 1: columns, Priority 2: balance comparison)?
✅ Are all amounts pure numbers without symbols?
✅ Are all dates in YYYY-MM-DD format?
✅ Is the JSON valid and complete?

🚨 FINAL CHECK: Open the PDF and verify EVERY balance number exists in the PDF. If you calculated any balance, you FAILED.

Remember: I am a DATA RECORDER. I COPY numbers from PDF to JSON. I do NOT calculate, verify, or modify numbers.
```

**关键新增**：
1. "Can I find every balance number I returned in the original PDF?" - 自我验证
2. "FINAL CHECK: Open the PDF and verify EVERY balance" - 最后检查
3. "If you calculated any balance, you FAILED" - 强烈警告

---

## 📊 修复前 vs 修复后

### 修复前的 Prompt

**位置**：规则 7（在中间）
**语气**：警告（"NEVER CALCULATE"）
**例子**：抽象例子
**验证**：无

**结果**：
- ❌ AI 还是计算了
- ❌ 返回幽灵数字：59,417.89

### 修复后的 Prompt

**位置**：第一句话 + 规则 7
**语气**：极端警告（"YOU FAILED"）
**例子**：具体例子（59,417.89 是错误的）
**验证**：Final Check（检查每个数字是否在 PDF 中）

**预期结果**：
- ✅ AI 不再计算
- ✅ 只返回 PDF 中存在的数字
- ✅ 幽灵数字消失

---

## 🎯 核心理念

### 用户的智慧

> **"我們只是搬運工／數據記錄員，不要計算"**

### 角色定位对比

| 角色 | 工作内容 | 是否计算？ |
|-----|---------|-----------|
| **会计师** | 验证、审计、计算 | ✅ 计算 |
| **计算器** | 根据公式算出答案 | ✅ 计算 |
| **数据记录员** | 抄写、记录数据 | ❌ 不计算 |
| **搬运工** | 搬运数据（PDF → JSON） | ❌ 不计算 |
| **复印机** | 复制内容 | ❌ 不计算 |

### 我们要的是什么？

**✅ 我们要的**：
```
PDF: 30,718.39
JSON: 30718.39
```

**❌ 我们不要的**：
```
PDF: 30,718.39
AI: "让我算算... 51,295.09 + 8,122.80 = 59,417.89"
JSON: 59417.89
```

### 如果看不清楚怎么办？

**❌ 错误做法**：
```
AI: "余额列模糊，让我用公式算：prev + credit - debit = 150"
JSON: "balance": 150
```

**✅ 正确做法**：
```
AI: "余额列模糊，我看不清楚"
JSON: "balance": null
```

**原则**：
- 看不清楚 = 返回 null
- 不要猜测
- 不要计算
- 不要"帮倒忙"

---

## 🧪 测试验证

### 测试步骤

**1. 删除旧文档**
```
在 VaultCaddy 中删除 eStatement-CIF-20220228.pdf
（这个是用旧 Prompt 处理的，有幽灵数字）
```

**2. 重新上传**
```
上传相同的 PDF: eStatement-CIF-20220228.pdf
等待处理完成
```

**3. 验证结果**
```
打开 PDF 的"戶口進支"部分
找到第一行（承上結餘）的"餘額"列
记录这个数字（例如：30,718.39）

打开提取的 JSON 数据
找到第一笔交易（承上結餘）
检查 balance 字段

验证: JSON 中的数字 = PDF 中的数字
```

### 验证清单

**对于每一笔交易**：
- ✅ 打开 PDF，找到这一行
- ✅ 看"餘額"列的数字
- ✅ 打开 JSON，找到这笔交易的 balance
- ✅ 确认完全一致

**特别检查**：
- ✅ 承上结余的 balance
- ✅ 第一笔交易的 balance
- ✅ 最后一笔交易的 balance
- ✅ 随机抽查 5-10 笔交易的 balance

**幽灵数字检查**：
- ✅ 在 PDF 中搜索每个 balance 数字
- ✅ 如果找不到 → 这是幽灵数字 ❌
- ✅ 如果找到了 → 正确 ✅

### 预期结果

**修复前**：
```json
{
  "date": "2022-02-01",
  "description": "承上結餘",
  "balance": 59417.89  // ❌ PDF 中不存在
}
```

**修复后**：
```json
{
  "date": "2022-02-01",
  "description": "承上結餘",
  "balance": 30718.39  // ✅ PDF 中存在（假设是这个值）
}
```

**如果余额看不清楚**：
```json
{
  "date": "2022-02-01",
  "description": "承上結餘",
  "balance": null  // ✅ 看不清楚就返回 null（不计算）
}
```

---

## 💡 为什么这个问题这么严重？

### 信任问题

**用户的信任**：
```
用户上传 PDF → 相信我们准确提取
用户看到数字 → 相信这是 PDF 中的数字
用户用于会计 → 基于这些数字做决策
```

**如果有幽灵数字**：
```
用户对账 → 发现数字不对
用户检查 PDF → 找不到这个数字
用户的反应 → "这系统不靠谱，别用了"
```

### 数据准确性

**一个幽灵数字的连锁反应**：
```
承上结余错误 → 59,417.89 (实际应该是 30,718.39)
差异: 59,417.89 - 30,718.39 = 28,699.50

影响:
1. 承上结余错误
2. transactionSign 判断可能错误（因为基于错误的余额比较）
3. 用户的财务报表错误
4. 可能导致税务问题
5. 用户失去对系统的信任
```

### 为什么不能「差不多就行」？

**会计数据的特殊性**：
1. **精确性要求 100%** - 差 1 分钱都不行
2. **每个数字都重要** - 没有"不重要"的数字
3. **可审计性** - 每个数字都要能追溯到原始文档
4. **法律责任** - 错误的财务数据可能有法律后果

**我们的标准**：
- ❌ 90% 准确率 → 不够
- ❌ 99% 准确率 → 还不够
- ✅ 100% 提取准确率 → 这才是目标

**注意**：
- 我们不能保证 100% OCR 准确率（字符识别可能有误）
- 但我们可以保证 100% 提取准确率（不计算、不修改）

---

## 🎓 经验总结

### Prompt 工程的教训

**教训 1：最重要的规则要放在最前面**
- ❌ 放在中间 → AI 可能忽略
- ✅ 第一句话 → AI 一定看到

**教训 2：警告要极端强烈**
- ❌ "Please don't..." → AI 觉得可以例外
- ✅ "YOU FAILED" → AI 不敢违反

**教训 3：要有具体的错误例子**
- ❌ 抽象例子 → AI 觉得不适用
- ✅ 具体例子（59,417.89）→ AI 明白

**教训 4：要有验证机制**
- ❌ 只说"不要做" → AI 做了也不知道
- ✅ 要求检查 → AI 自我验证

### AI 的「帮助」陷阱

**问题**：AI 被训练成"有帮助的助手"

**表现**：
1. 看到"问题"就想"解决"
2. 看到"缺失"就想"填补"
3. 看到"模糊"就想"推算"

**在数据提取任务中**：
- ✅ 这些"帮助"行为都是**错误**的
- ✅ 我们要的是"笨"AI（只抄写，不思考）
- ✅ 不要"聪明"AI（会计算，会推理）

### 搬运工哲学

**核心**：
1. 我是搬运工，不是会计师
2. 我搬运数据，不计算数据
3. PDF 有什么，JSON 就有什么
4. PDF 没有的，JSON 不能有

**口号**：
- **"只抄写，不计算"**
- **"只搬运，不验证"**
- **"银行永远对"**
- **"看不清就 null"**

---

## 🚀 下一步

### 立即测试

**步骤**：
1. ✅ 删除旧文档（有幽灵数字的）
2. ✅ 重新上传 PDF
3. ✅ 验证所有余额
4. ✅ 确认没有幽灵数字

### 如果还有问题

**如果还是出现幽灵数字**：

1. **报告具体信息**：
   - 幽灵数字是什么？
   - PDF 中的正确数字是什么？
   - 截图 PDF 和 JSON

2. **进一步诊断**：
   - 检查是否是 OCR 错误
   - 检查是否是特定银行格式问题
   - 可能需要更极端的 Prompt

3. **终极方案**：
   - 在 Prompt 中明确列出"禁止计算公式清单"
   - 每个余额都要求 AI 说明"我从 PDF 的哪一行哪一列提取的"

---

## 📖 相关文档

- `BALANCE_CALCULATION_FIX.md` - 余额计算问题的首次修复
- `DATA_MOVER_PHILOSOPHY.md` - 搬运工哲学核心理念
- `PROMPT_FIX_DATE_AMOUNT_ACCURACY.md` - 日期和金额准确性修复

---

**生成时间**：2026年2月1日  
**核心问题**：AI 创造了 PDF 中不存在的「幽灵数字」  
**修复方案**：极端强化 Prompt，第一句话就警告  
**测试状态**：等待用户验证

**关键口号**：
> **"只抄写，不计算。PDF 中没有的数字，JSON 中不能有。"**

