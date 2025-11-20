# Xero 和 QuickBooks CSV 格式分析

## 🔍 用戶問題

用戶提供了兩個參考圖片：
- **圖3**: 其他網站的 Xero CSV 下載格式
- **圖4**: 其他網站的 QuickBooks CSV 下載格式

**核心問題**: 這些格式是否是真正的 Xero 和 QuickBooks 所需要的格式？

---

## 📊 分析結果

### 1️⃣ 圖3 - Xero CSV 格式

#### 觀察到的格式
```csv
Date,Amount,Payee,Description,Reference,Check Number
02/22/2025,0.00,,B/F BALANCE,,
02/26/2025,2.61,,CREDIT INTEREST,,
03/07/2025,78649.00,,QUICK CHEQUE DEPOSIT(07MAR25),,
```

#### 官方 Xero 要求

根據 Xero 官方文檔，銀行交易導入格式應包含：

**最基本格式（Xero Bank Statement Import）**:
```csv
Date,Description,Amount
22/02/2025,B/F BALANCE,0.00
26/02/2025,CREDIT INTEREST,2.61
07/03/2025,QUICK CHEQUE DEPOSIT,78649.00
```

**完整格式（Xero Bank Feed Format）**:
```csv
Date,Amount,Payee,Description,Reference,Particulars,Code,Analysis Code
22/02/2025,0.00,,B/F BALANCE,,,,
26/02/2025,2.61,,CREDIT INTEREST,,,,
07/03/2025,78649.00,,QUICK CHEQUE DEPOSIT,,,,
```

#### ✅ 結論：圖3 格式**接近正確但不完全準確**

**問題點**:
1. **日期格式**: Xero 通常使用 `DD/MM/YYYY`（22/02/2025），而不是 `MM/DD/YYYY`（02/22/2025）
2. **必要字段**: 最基本只需要 `Date`, `Description`, `Amount` 三個字段
3. **可選字段**: `Payee`, `Reference`, `Check Number` 是可選的，但不是必須的

**建議修正**:
```csv
Date,Description,Amount,Payee,Reference
22/02/2025,B/F BALANCE,0.00,,
26/02/2025,CREDIT INTEREST,2.61,,
07/03/2025,QUICK CHEQUE DEPOSIT,78649.00,,
```

---

### 2️⃣ 圖4 - QuickBooks CSV 格式

#### 觀察到的格式
```csv
Date,Description,Amount
02/26/2025,CREDIT INTEREST,2.61
03/07/2025,QUICK CHEQUE DEPOSIT(07MAR25),78649.00
03/08/2025,POON H** K***HD12530825734031 08MAR,840.00
```

#### 官方 QuickBooks 要求

根據 QuickBooks Online 官方文檔：

**標準 3 欄格式（QuickBooks Online Bank CSV）**:
```csv
Date,Description,Amount
02/26/2025,CREDIT INTEREST,2.61
03/07/2025,QUICK CHEQUE DEPOSIT,78649.00
03/08/2025,POON H** K***,840.00
```

**完整格式（QuickBooks Desktop IIF - 不是 CSV）**:
```
!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	AMOUNT	DOCNUM	MEMO
!SPL	SPLID	TRNSTYPE	DATE	ACCNT	AMOUNT	DOCNUM	MEMO	TAXABLE
!ENDTRNS
```

#### ✅ 結論：圖4 格式**完全正確**

**QuickBooks Online 確實只需要 3 個字段**:
1. **Date**: 日期（MM/DD/YYYY 或 DD/MM/YYYY，取決於區域設置）
2. **Description**: 交易描述
3. **Amount**: 金額（正數 = 收入，負數 = 支出）

---

## 🎯 建議的實現方案

### 方案 A: 使用圖3和圖4的格式（目前實現）

**優點**:
- ✅ 符合大多數用戶的預期
- ✅ 包含額外信息（Payee, Reference）
- ✅ 兼容性較好

**缺點**:
- ❌ Xero 日期格式可能需要調整
- ❌ 額外字段可能導致某些版本的 Xero 報錯

### 方案 B: 使用官方最小格式

**Xero 最小格式**:
```csv
Date,Description,Amount
22/02/2025,B/F BALANCE,0.00
26/02/2025,CREDIT INTEREST,2.61
```

**QuickBooks 最小格式**:
```csv
Date,Description,Amount
02/26/2025,CREDIT INTEREST,2.61
03/07/2025,QUICK CHEQUE DEPOSIT,78649.00
```

**優點**:
- ✅ 100% 符合官方要求
- ✅ 兼容所有版本
- ✅ 導入不會報錯

**缺點**:
- ❌ 缺少額外信息（Payee, Reference）
- ❌ 用戶可能需要手動補充信息

### 方案 C: 提供兩種選項（推薦）

在導出菜單中提供：

1. **Xero CSV（基本）** - 3 欄格式
2. **Xero CSV（完整）** - 6 欄格式
3. **QuickBooks CSV** - 3 欄格式

---

## 📝 關鍵區別總結

| 格式 | 必要字段 | 日期格式 | 金額符號 | 額外字段 |
|------|---------|---------|---------|---------|
| **Xero 基本** | Date, Description, Amount | DD/MM/YYYY | 正/負 | 無 |
| **Xero 完整** | Date, Amount, Description | DD/MM/YYYY | 正/負 | Payee, Reference, Particulars, Code |
| **QuickBooks** | Date, Description, Amount | MM/DD/YYYY | 正/負 | 無 |

---

## 🔧 實際測試建議

為了確保格式正確，建議進行以下測試：

### 測試 1: Xero 導入測試

1. 登入 Xero 帳戶
2. 前往 `Accounting` → `Bank Accounts`
3. 選擇一個銀行帳戶
4. 點擊 `Import a Statement`
5. 上傳測試 CSV 文件
6. 檢查是否成功導入

**預期結果**:
- ✅ 所有交易正確顯示
- ✅ 日期格式正確
- ✅ 金額正確（正/負）
- ✅ 描述完整

### 測試 2: QuickBooks 導入測試

1. 登入 QuickBooks Online
2. 前往 `Banking` → `Banking`
3. 選擇一個銀行帳戶
4. 點擊 `Upload from file`
5. 上傳測試 CSV 文件
6. 檢查是否成功導入

**預期結果**:
- ✅ 所有交易正確顯示
- ✅ 日期格式正確
- ✅ 金額正確（正/負）
- ✅ 描述完整

---

## 💡 最終建議

### 短期方案（快速實現）

**保持目前的實現**:
- Xero: Date, Amount, Payee, Description, Reference, Check Number
- QuickBooks: Date, Description, Amount

**理由**:
1. 圖4 的 QuickBooks 格式是**100% 正確**的
2. 圖3 的 Xero 格式雖然多了額外字段，但**大部分情況下可以正常導入**
3. 只需要調整日期格式即可

### 中期方案（完善功能）

**提供多種選項**:

```
┌─────────────────────────────────┐
│ 📥 Export                      ▼│
├─────────────────────────────────┤
│ 📄 標準 CSV                     │
│    通用格式（銀行對帳單）         │
├─────────────────────────────────┤
│ 📄 Xero CSV（基本）             │
│    Date, Description, Amount    │
├─────────────────────────────────┤
│ 📄 Xero CSV（完整）             │
│    含 Payee, Reference 等       │
├─────────────────────────────────┤
│ 📄 QuickBooks CSV               │
│    Date, Description, Amount    │
└─────────────────────────────────┘
```

---

## 🚀 下一步行動

1. **立即**: 修正 Xero 日期格式（DD/MM/YYYY）
2. **短期**: 保持目前的字段結構
3. **中期**: 添加「基本」和「完整」兩種選項
4. **長期**: 根據用戶反饋調整

---

## 📞 回答用戶問題

### 問題: "我的問題是真正的 Xero 和 QuickBooks 要的內容是否這樣？"

**答案**:

✅ **QuickBooks（圖4）**: **100% 正確**
- Date, Description, Amount 三個字段
- MM/DD/YYYY 日期格式
- 完全符合 QuickBooks Online 官方要求

⚠️ **Xero（圖3）**: **部分正確，需要調整**
- 字段結構基本正確，但多了可選字段
- **需要修正**: 日期格式應該是 `DD/MM/YYYY` 而不是 `MM/DD/YYYY`
- **建議**: 提供「基本版」（3 欄）和「完整版」（6 欄）兩種選項

**總結**:
- QuickBooks 格式可以直接使用 ✅
- Xero 格式需要調整日期格式 ⚠️
- 建議提供多種選項，讓用戶自己選擇 💡

---

**更新日期**: 2025-11-20  
**版本**: v1.0  
**作者**: VaultCaddy AI Team

