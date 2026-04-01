# 🔧 Prompt 优化报告 - 2026年2月1日

**优化原因**: 用户担心 Prompt 太长、有重复、前后矛盾  
**优化目标**: 更短、更清晰、更聚焦  
**状态**: ✅ 已完成并可测试

---

## 📋 发现的问题

### 1. ❌ **前后矛盾** - 规则 5 vs 规则 7

**规则 5（旧）**：
```
Extract the balance value from the "餘額/Balance" column (e.g., 59,417.89)
```

**规则 7（旧）**：
```
PDF shows "30,718.39" but you return "59,417.89" ❌ (You calculated it!)
```

**问题**：
- 规则 5 举例用了 `59,417.89`
- 规则 7 说 `59,417.89` 是**错误的例子**
- **自相矛盾！**

**影响**：
- AI 会困惑："到底 59,417.89 是对还是错？"
- 可能导致 AI 忽略其中一个规则

---

### 2. ❌ **大量重复** - 开头 + 规则 7 + 规则 8

**开头警告**：
```
YOU ARE A DATA RECORDER, NOT A CALCULATOR.
```

**规则 7**：
```
YOU ARE A DATA RECORDER: Your job is to COPY...
```

**规则 8**：
```
WE ARE DATA MOVERS, NOT ACCOUNTANTS...
```

**问题**：
- 同样的概念重复了 **3 次**
- 占用了大量空间
- 可能让 AI 觉得"我知道了，别说了"

**统计**：
- 规则 7: 15 行
- 规则 8: 3 行
- 合计: 18 行（都在说同一件事）

---

### 3. ❌ **Final Checklist 太长** - 17 行

**旧 Checklist（部分）**：
```
✅ Did I extract EVERY SINGLE ROW from the transaction table?
✅ Does each transaction have its OWN unique date (extracted, not guessed)?
✅ Does each transaction have its OWN unique amount (extracted, not modified)?
✅ Did I COPY all balance values from the PDF (NEVER calculated)?
✅ Can I find every balance number I returned in the original PDF?
✅ Did I NEVER use ANY formulas (balance = prev + credit - debit)?
✅ Did I NOT combine, merge, or summarize any rows?
✅ Did I NOT use Account Summary data (only Transaction Details)?
✅ Is "extracted data" = "uploaded data" (exactly the same)?
✅ Did I determine transactionSign correctly (Priority 1: columns, Priority 2: balance comparison)?
✅ Are all amounts pure numbers without symbols?
✅ Are all dates in YYYY-MM-DD format?
✅ Is the JSON valid and complete?
```

**问题**：
- 13 个检查项
- 太啰嗦
- AI 可能"走马观花"，不认真看

---

### 4. ⚠️ **Prompt 总体太长**

**统计**：
- 总行数: **150 行**
- 字符数: **~6500 字符**
- 估算字数: **~1100 词**

**问题**：
- AI 的注意力可能分散
- 关键规则可能被淹没
- 处理时间增加

**Qwen-VL-Max 的 Context Window**：
- 支持长 prompt
- 但更短更好（注意力更集中）

---

## ✅ 优化方案

### 优化 1：修复矛盾（规则 5）

**旧版本**：
```javascript
5. **Opening Balance / Brought Forward (承上結餘/上期結餘):**
   - This is the FIRST row in the Transaction Details section
   - It SHOULD be included in the transactions array
   - Extract the balance value from the "餘額/Balance" column (e.g., 59,417.89)  // ❌ 错误例子
   - DO NOT use the Account Summary total (e.g., 60,736.27) - that's the closing balance
```

**新版本**：
```javascript
5. **Opening Balance / Brought Forward (承上結餘/上期結餘):**
   - This is the FIRST row in the Transaction Details section
   - It SHOULD be included in the transactions array
   - Extract the balance value DIRECTLY from the "餘額/Balance" column  // ✅ 删除错误例子
   - DO NOT use Account Summary numbers - only use Transaction Details
```

**效果**：
- ✅ 消除矛盾
- ✅ 更简洁（减少 1 行）

---

### 优化 2：合并重复（规则 7 + 规则 8）

**旧版本（规则 7）**：
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

**旧版本（规则 8）**：
```javascript
8. **⚠️ WE ARE DATA MOVERS, NOT ACCOUNTANTS:**
   - **OUR JOB**: Move data from PDF to JSON. Extract exactly what we see, don't verify or calculate.
   - **BANK IS ALWAYS RIGHT**: We trust the bank's numbers 100%. Never change, verify, or "fix" them.
   - **GOAL**: Make sure "extracted data" = "uploaded data" (exactly the same)
```

**新版本（合并后的规则 7）**：
```javascript
7. **🚨 BALANCE - NEVER CALCULATE (MOST IMPORTANT):**
   Balance MUST be extracted from "餘額/Balance" column. If not visible → set to null.
   
   ✅ CORRECT: PDF shows "30,718.39" → extract 30718.39
   ❌ WRONG: PDF shows "30,718.39" but you return a different number (you calculated it!)
   ❌ WRONG: Balance is blurry → you calculate: prev + credit - debit (NO! Set to null!)
   
   🚨 Every balance number must exist in the PDF. If it doesn't exist in PDF, you FAILED.
```

**效果**：
- ✅ 从 18 行减少到 5 行（精简 **72%**）
- ✅ 保留核心信息
- ✅ 删除重复的"DATA RECORDER"说明（开头已经说了）

---

### 优化 3：精简 transactionSign 规则

**旧版本（规则 9）**：
```javascript
9. **How to determine transactionSign (debit/credit, expense/income)?**
   
   **PRIORITY 1 - Direct Extraction (if statement has clear columns):**
   - If statement has separate "支出/Debit" and "存入/Credit" columns:
     * Amount in debit column → debit: amount, transactionSign: "expense"
     * Amount in credit column → credit: amount, transactionSign: "income"
   - If statement has +/- signs on amounts:
     * Negative amount (-8,122.80) → debit: 8122.80, transactionSign: "expense"
     * Positive amount (+25,000.00) → credit: 25000.00, transactionSign: "income"
   
   **PRIORITY 2 - Balance Comparison (if no clear debit/credit columns):**
   - Compare CURRENT balance with PREVIOUS balance (use EXTRACTED balance, not calculated)
   - If current balance > previous balance → transactionSign: "income"
   - If current balance < previous balance → transactionSign: "expense"
   - This is NOT calculation, this is INFERENCE from facts (balance went up = deposit, went down = withdrawal)
   
   **IMPORTANT - Ignore unreliable text labels:**
   - Some statements have text like "支出" that conflicts with actual balance changes
   - ALWAYS prioritize: debit/credit columns > balance comparison > text labels
   - Example conflict:
     * Previous balance: 100.00
     * Current balance: 200.00 (increased!)
     * Text says: "支出" (expense)
     * CORRECT: "income" (because balance increased, ignore the text)
     * WRONG: "expense" (blindly following text)
```

**新版本（规则 8）**：
```javascript
8. **How to determine transactionSign?**
   
   PRIORITY 1 - If statement has debit/credit columns or +/- signs:
   - Debit column or negative amount → "expense"
   - Credit column or positive amount → "income"
   
   PRIORITY 2 - If only amount + balance columns:
   - Balance increased (current > previous) → "income"
   - Balance decreased (current < previous) → "expense"
   
   Ignore text labels if they conflict with columns/balance. Prioritize: columns > balance change > text.
```

**效果**：
- ✅ 从 23 行减少到 6 行（精简 **74%**）
- ✅ 保留核心逻辑
- ✅ 更易读

---

### 优化 4：精简 Final Checklist

**旧版本**：
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

**新版本**：
```javascript
FINAL CHECKLIST:
✅ Extracted EVERY row from transaction table (not combined/merged)?
✅ Each transaction has unique date & amount from PDF (not guessed)?
✅ ALL balance values exist in PDF (not calculated)?
✅ Used Transaction Details only (not Account Summary)?
✅ TransactionSign based on columns/balance (not unreliable text)?
✅ JSON valid and complete?

🚨 Can I find every number I returned in the PDF? If not, I FAILED.
```

**效果**：
- ✅ 从 17 行减少到 7 行（精简 **59%**）
- ✅ 合并相似检查项
- ✅ 保留关键检查

---

## 📊 优化效果总结

### 长度对比

| 指标 | 优化前 | 优化后 | 减少 |
|-----|-------|--------|------|
| **总行数** | 150 行 | 125 行 | **17%** ⬇️ |
| **字符数** | ~6500 | ~5400 | **17%** ⬇️ |
| **规则 7+8** | 18 行 | 5 行 | **72%** ⬇️ |
| **规则 9 (transactionSign)** | 23 行 | 6 行 | **74%** ⬇️ |
| **Final Checklist** | 17 行 | 7 行 | **59%** ⬇️ |

### 质量改进

| 维度 | 优化前 | 优化后 |
|-----|-------|--------|
| **矛盾** | ❌ 有（规则5 vs 规则7） | ✅ 无 |
| **重复** | ❌ 多（3处重复"DATA RECORDER"） | ✅ 无 |
| **清晰度** | ⚠️ 一般（太长） | ✅ 好 |
| **聚焦度** | ⚠️ 分散 | ✅ 集中 |

### 核心保留

**以下关键内容完全保留**：
1. ✅ 开头警告（🚨 CRITICAL - READ THIS FIRST）
2. ✅ Required fields（完整的 JSON 结构）
3. ✅ 8 个核心规则（所有关键要求）
4. ✅ 🚨 BALANCE - NEVER CALCULATE（最重要规则）
5. ✅ Final Checklist（精简但完整）

**删除的内容**：
- ❌ 重复的说明
- ❌ 冗长的例子
- ❌ 矛盾的例子
- ❌ 过度详细的解释

---

## 🎯 优化后的 Prompt 结构

### 多页版本（generateMultiPagePrompt）

```
1. 🚨 开头警告（6 行）
   - YOU ARE A DATA RECORDER, NOT A CALCULATOR
   - IF YOU SEE "30,718.39" → EXTRACT
   - IF YOU CALCULATE "59,417.89" → YOU FAILED

2. Required fields（28 行）
   - 完整的 JSON 结构

3. ⚠️ CRITICAL RULES（8 个规则，80 行）
   规则 1: EXTRACT EVERY SINGLE LINE（4 行）
   规则 2: DATE ACCURACY（4 行）
   规则 3: AMOUNT ACCURACY（4 行）
   规则 4: Account Summary vs Transaction Details（3 行）
   规则 5: Opening Balance（3 行）
   规则 6: Transaction type rules（11 行）
   规则 7: 🚨 BALANCE - NEVER CALCULATE（5 行）
   规则 8: TransactionSign（6 行）

4. FINAL CHECKLIST（7 行）
   - 6 个核心检查项
   - 🚨 FINAL CHECK

5. 结尾（1 行）
   - Return ONLY JSON

总计: 125 行
```

### 单页版本（generatePrompt）

**相同结构，但更短**（因为是单页）

---

## 🧪 测试建议

### 测试场景 1：正常提取

**目的**: 验证优化后准确率不降低

**步骤**:
1. 删除之前的文档
2. 重新上传相同的 PDF
3. 验证提取结果

**验证**:
- ✅ 所有余额与 PDF 一致
- ✅ transactionSign 判断正确
- ✅ 没有幽灵数字

### 测试场景 2：边缘情况

**目的**: 验证简化后规则仍然有效

**边缘情况**:
1. 余额模糊 → 应返回 null（不计算）
2. 文字标签冲突 → 应忽略文字（用余额判断）
3. 多个相似交易 → 应逐行提取（不合并）

### 测试场景 3：性能

**目的**: 验证是否更快

**预期**:
- ⚠️ 处理时间可能略微减少（Prompt 更短）
- ✅ Token 消耗减少（输入更短）

---

## 💡 优化原则

### 1. **Occam's Razor（奥卡姆剃刀）**

> "Entities should not be multiplied beyond necessity"  
> "如无必要，勿增实体"

**应用**:
- 删除所有冗余内容
- 只保留必要的说明
- 一个规则说一次就够了

### 2. **Clarity over Completeness**

**原则**: 清晰比完整更重要

**应用**:
- 精简的规则 > 冗长的解释
- 核心例子 > 所有可能的例子
- 重点突出 > 面面俱到

### 3. **Top-Heavy Structure**

**原则**: 最重要的放最前面

**应用**:
- 🚨 开头警告（第一眼就看到）
- 规则 7（🚨 BALANCE）最重要
- Final Checklist 最后检查

### 4. **No Contradictions**

**原则**: 绝对不能自相矛盾

**应用**:
- ✅ 删除规则 5 中的错误例子
- ✅ 所有规则一致
- ✅ 例子不冲突

---

## 📈 预期效果

### 对 AI 的影响

**优化前**:
```
AI: "这个 Prompt 好长啊..."
AI: "规则 7 说这个，规则 8 也在说这个..."
AI: "规则 5 的例子是 59,417.89，但规则 7 说这是错的，到底哪个对？"
AI: "Checklist 有 13 项，我懒得看了..."
```

**优化后**:
```
AI: "🚨 CRITICAL - 好，我要注意！"
AI: "YOU ARE A DATA RECORDER - 明白了"
AI: "规则清晰，没有重复"
AI: "Checklist 只有 6 项，我认真检查"
```

### 对准确率的影响

**预期**:
- ✅ 准确率**保持或提高**（更清晰 → 更容易遵守）
- ✅ 幽灵数字减少（规则更明确）
- ✅ 一致性提高（无矛盾）

### 对性能的影响

**预期**:
- ✅ Token 消耗减少 ~17%
- ✅ 处理时间可能略微减少
- ✅ 成本降低 ~17%

---

## 🚨 风险评估

### 可能的风险

**风险 1：过度精简**
- **可能性**: 低
- **原因**: 核心规则都保留了
- **缓解**: 如果发现问题，可以恢复特定规则

**风险 2：AI 不理解简化后的规则**
- **可能性**: 极低
- **原因**: 简化后更清晰，不是更复杂
- **缓解**: 监控测试结果

**风险 3：准确率下降**
- **可能性**: 极低
- **原因**: 只删除重复，不删除核心规则
- **缓解**: A/B 测试（旧 vs 新）

### 回滚计划

**如果优化失败**：
```bash
# 回滚到优化前的版本
git revert HEAD
```

**判断标准**：
- ❌ 准确率下降 > 5%
- ❌ 出现新的问题（之前没有的）
- ❌ 幽灵数字增加

---

## ✅ 优化完成

**优化前 Commit**:
```
commit 2d2513ec (之前的 commit)
```

**优化后 Commit**:
```
commit 7a998667
🔧 优化 Prompt - 修复矛盾、删除重复、减少 17% 长度
```

**变更统计**:
```
1 file changed, 33 insertions(+), 88 deletions(-)
```

**净减少**: **-55 行代码** 🎉

---

## 📚 相关文档

- `BALANCE_CALCULATION_FIX.md` - 余额计算问题修复
- `GHOST_NUMBER_FIX.md` - 幽灵数字问题修复
- `DATA_MOVER_PHILOSOPHY.md` - 搬运工哲学
- `PROMPT_FIX_DATE_AMOUNT_ACCURACY.md` - 日期和金额准确性

---

## 🎯 下一步

**立即测试**:
1. 删除旧文档
2. 重新上传 PDF
3. 验证准确率
4. 对比优化前后结果

**如果成功**:
- ✅ 继续使用优化后的 Prompt
- ✅ 监控长期表现

**如果失败**:
- ❌ 回滚
- ❌ 分析具体失败原因
- ❌ 有针对性地调整

---

**生成时间**: 2026年2月1日  
**优化效果**: 减少 17% 长度，消除矛盾和重复  
**核心保留**: 所有关键规则完整保留  
**状态**: ✅ 已完成，等待测试验证

