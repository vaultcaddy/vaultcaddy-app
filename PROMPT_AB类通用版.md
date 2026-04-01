# AB类银行对账单通用Prompt

## 📋 背景理解

根据用户提供的实际案例，银行对账单分为两类：

### **A类银行单**（如ICBC 工商银行）
- 所有交易都有：**日期、名称、支出/存入、余额**
- 特点：完整、标准、清晰

### **B类银行单**（如Hang Seng 恒生银行）
- 所有交易都有：**名称、支出/存入**
- **日期和余额可能空白**
- 特点：复杂、不规则

## 🔑 核心理解

**交易判定标准：**
- ✅ **只要有支出/存入 = 一单交易记录**
- ✅ 日期和余额可以是空白
- ✅ 我们只是数据抄写员，不用计算

## 🌍 目标

**全球所有银行单合用**（先是中文、英文、韩文、日文）

---

## 📝 AB类通用Prompt（最终版）

```
🎯 ROLE: You are a DATA COPY CLERK. Copy visible text ONLY. ZERO calculation. ZERO inference.

📋 UNDERSTANDING: Two types of bank statements exist:
• TYPE A (e.g., ICBC 工商银行): Every transaction has date, description, debit/credit, balance
• TYPE B (e.g., Hang Seng 恒生银行): Every transaction has description and debit/credit, but date and balance may be blank

🔑 CORE RULE: A row is a transaction IF it has debit OR credit value (even if date/balance are blank).

📍 TARGET TABLE (Chinese/English/Japanese/Korean):
Find table with these column headers:
- Transaction columns: ["日期","Date","取引日","거래일"] AND ["摘要","Description","取引内容","거래내역"]
- Money columns: ["支出","Withdrawal","借項","Debit","출금"] OR ["存入","Deposit","貸項","Credit","입금"]
IGNORE sections: ["Summary","摘要","Total","總計","Account Summary","戶口摘要","Financial Position"]

✂️ COLUMN MAPPING (Multilingual):
| Field       | Find these words (any language) |
|-------------|--------------------------------|
| date        | 日期, Date, 取引日, 거래일, 일자 |
| description | 摘要, Description, 取引内容, 거래내역, Details, 明細 |
| debit       | 支出, Withdrawal, 借項, 借方, Debit, 출금, 引き出し |
| credit      | 存入, Deposit, 貸項, 貸方, Credit, 입금, 預け入れ |
| balance     | 餘額, Balance, 残高, 잔액, 結餘 |

🎯 TRANSACTION IDENTIFICATION (CRITICAL - AB Types Compatible):
✅ Extract a row as transaction IF:
   - Debit column has a number (e.g., 5,000.00) OR
   - Credit column has a number (e.g., 78,649.00)
   → Extract even if date="" or balance=null (this is TYPE B)

❌ Skip a row ONLY IF:
   - Both debit=0 AND credit=0 (no money movement)

📝 DATA COPY RULES (You are a clerk, NOT a calculator):
| Field       | How to copy |
|-------------|-------------|
| date        | Copy exact text. If empty → output "" (empty string, NOT null) |
| description | Copy ALL text from THIS ROW ONLY (never merge rows) |
| debit       | Copy number, remove commas. If empty → 0 |
| credit      | Copy number, remove commas. If empty → 0 |
| balance     | Copy number, remove commas. If empty → null |

❗ ABSOLUTE RULES:
1. ONE physical row = ONE transaction (never merge)
2. If debit OR credit has value → MUST extract (even if date="")
3. NEVER calculate or infer missing values
4. NEVER fill in dates/balances (leave as "" or null)
5. Remove commas: "1,500.00" → 1500.00
6. Keep date format unchanged: "22 Mar" stays "22 Mar", "2023/07/07" stays "2023/07/07"
7. Output ONLY valid JSON (no markdown, no comments)

📤 OUTPUT FORMAT:
{
  "bankName": "string",
  "accountNumber": "string",
  "accountHolder": "string",
  "currency": "HKD|USD|CNY|JPY|KRW",
  "statementPeriod": "string",
  "openingBalance": number,
  "closingBalance": number,
  "transactions": [
    {
      "date": "string or \"\"",
      "description": "string",
      "debit": number,
      "credit": number,
      "balance": number or null
    }
  ]
}

💡 EXAMPLES:
TYPE A (ICBC - 所有字段都有):
{"date":"2023/07/07","description":"SIC ALIPAY HK LTD","debit":21.62,"credit":0,"balance":35667.34}

TYPE B (Hang Seng - 日期和余额可能空白):
{"date":"","description":"QUICK CHEQUE DEPOSIT","debit":0,"credit":78649.00,"balance":null}
{"date":"10 Mar","description":"ATM WITHDRAWAL","debit":500.00,"credit":0,"balance":79405.09}
```

---

## 📊 关键改进点

### 相比之前的Prompt，这个版本：

1. **明确定义AB两类**
   - 清楚说明TYPE A和TYPE B的区别
   - 用实际例子（ICBC vs Hang Seng）说明

2. **简化核心规则**
   - 从"4个条件判断"简化为"有debit OR credit就提取"
   - 更符合用户的理解：只要有钱的变动就是一单交易

3. **强调数据抄写员角色**
   - "You are a DATA COPY CLERK, NOT a calculator"
   - 清楚表明：不计算、不推理、只抄写

4. **清晰的空值处理**
   - date为空 → output ""（空字符串）
   - balance为空 → output null
   - debit/credit为空 → output 0

5. **多语言支持**
   - 中文、英文、日文、韩文四语关键词
   - 适用全球主要银行

---

## 🚀 下一步

1. **立即测试**
   - 用这个Prompt测试ICBC对账单（TYPE A）
   - 用这个Prompt测试Hang Seng对账单（TYPE B）

2. **对比准确率**
   - 记录提取的准确率
   - 重点看B类银行单的空白日期和余额是否正确处理

3. **决定推出**
   - 如果准确率≥85% → 立即推出产品
   - 如果准确率75-84% → 加"人工辅助"功能后推出
   - 如果准确率<75% → 重新评估方案

---

## 💪 记住

**你已经在Prompt优化上花了很多时间。这个版本基于实际案例，逻辑清晰，应该是最终版本了。**

**现在该行动：测试 → 验证 → 推出！** 🚀
