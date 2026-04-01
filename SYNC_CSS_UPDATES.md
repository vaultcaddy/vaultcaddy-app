# CSS样式同步更新清单
**日期**: 2026-01-10  
**目标**: 将中文版的表格优化同步到英/日/韩语版本

## 需要同步的CSS改动

### 1. 紧凑布局优化 (行 636-676)
```css
/* 🎨 設計大師優化：響應式表格包裝器 */
.table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: 0 -1.25rem;  /* 從 -1.5rem 減少到 -1.25rem */
    padding: 0 1.25rem;  /* 從 1.5rem 減少到 -1.25rem */
}

/* 🎯 優化：減少表格內間距，更緊湊 */
.transactions-table th,
.transactions-table td {
    padding: 0.6rem 0.4rem !important;  /* 從 0.65rem 0.5rem 進一步減少到 0.6rem 0.4rem */
    font-size: 0.875rem;  /* 統一字體大小 */
}

/* 🎯 優化：已對賬列更窄 */
.checkbox-cell {
    width: 45px !important;
    padding: 0.5rem 0.2rem !important;  /* 從 0.3rem 減少到 0.2rem */
    text-align: center !important;
}

.checkbox-cell input[type="checkbox"] {
    width: 18px !important;
    height: 18px !important;
    cursor: pointer;
    accent-color: #10b981;  /* 綠色對勾 */
}

.action-cell {
    width: 80px !important;
    padding: 0.5rem !important;
}

/* 🎯 優化：金額和余額列右對齊且更緊湊 */
.amount-cell,
.transactions-table td[data-field="balance"] {
    text-align: right;
    min-width: 110px !important;
    max-width: 130px;
    padding: 0.65rem 0.75rem !important;
}
```

### 2. 響應式列隱藏 (行 692-794)
```css
/* 🎨 優化：默認隱藏次要列（適配所有屏幕，避免滾動） */

/* 列結構（從左到右）：
 * 1. checkbox（已對賬）✅ 保留
 * 2. date（日期）✅ 保留
 * 3. type（類型）❌ 隱藏
 * 4. description（描述）✅ 保留
 * 5. payee（收款人）✅ 保留
 * 6. reference（參考編號）❌ 隱藏
 * 7. check#（支票號）❌ 隱藏
 * 8. category（分類）✅ 保留（用戶需要）
 * 9. amount（金額）✅ 保留
 * 10. balance（余額）✅ 保留
 * 11. attachment（附件）❌ 隱藏
 * 12. actions（操作）✅ 保留
 */

/* 默認隱藏次要列 */
.type-cell,
.ref-cell,
.check-cell,
.attachment-cell,
.transactions-table th:nth-child(3),  /* Type header */
.transactions-table th:nth-child(6),  /* Reference header */
.transactions-table th:nth-child(7),  /* Check# header */
.transactions-table th:nth-child(11)  /* Attachment header */
{
    display: none !important;
}

/* ✅ 分類列始終顯示（用戶需要） */
.category-cell,
.transactions-table th:nth-child(8) {
    display: table-cell !important;
}

/* 🔍 超大屏幕（>2000px）：顯示所有列 */
@media (min-width: 2000px) {
    .type-cell,
    .ref-cell,
    .check-cell,
    .transactions-table th:nth-child(3),  /* Type header */
    .transactions-table th:nth-child(6),  /* Reference header */
    .transactions-table th:nth-child(7)   /* Check# header */
    {
        display: table-cell !important;
    }
}

/* 🔍 大屏幕（>1600px）：顯示部分列 */
@media (min-width: 1600px) and (max-width: 1999px) {
    .type-cell,
    .transactions-table th:nth-child(3)  /* Type header */
    {
        display: table-cell !important;
    }
}

/* 📱 平板（<1400px）：進一步隱藏 */
@media (max-width: 1400px) {
    .payee-cell,
    .transactions-table th:nth-child(5)  /* Payee header */
    {
        display: none !important;
    }
}

/* 🎨 顯示隱藏列提示 */
.transactions-section::before {
    content: '💡 精簡模式：已隱藏次要欄位（類型、參考編號、支票號、附件）。📊 如需查看完整數據（包括備注、附件等），請點擊頂部「Export」按鈕導出。';
    display: block;
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    color: #1e40af;
    font-size: 0.8rem;
    text-align: center;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    margin-bottom: 1rem;
    line-height: 1.5;
}

/* 大屏幕更新提示 */
@media (min-width: 1600px) {
    .transactions-section::before {
        content: '✅ 標準模式：顯示類型欄位。已隱藏：參考編號、支票號、附件。';
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        color: #166534;
        border-color: #bbf7d0;
    }
}

@media (min-width: 2000px) {
    .transactions-section::before {
        content: '🎉 完整模式：顯示所有欄位（已隱藏附件圖標以保持簡潔）。';
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border-color: #fcd34d;
    }
}
```

### 3. 智能列寬分配 (行 836-886)
```css
/* 🎨 設計大師優化：智能列寬分配（緊湊版） */
.transactions-table th:nth-child(1),  /* 復選框 */
.transactions-table td:nth-child(1) {
    width: 45px;
    min-width: 45px;
}

.transactions-table th:nth-child(2),  /* 日期 */
.transactions-table td:nth-child(2) {
    width: 100px;
    min-width: 100px;
    white-space: nowrap;
}

.transactions-table th:nth-child(4),  /* 描述 */
.transactions-table td:nth-child(4) {
    min-width: 150px;
    max-width: 280px;
}

.transactions-table th:nth-child(5),  /* 收款人 */
.transactions-table td:nth-child(5) {
    min-width: 120px;
    max-width: 200px;
}

.transactions-table th:nth-child(8),  /* 分類 */
.transactions-table td:nth-child(8) {
    width: 105px;
    min-width: 105px;
}

.transactions-table th:nth-child(9),  /* 金額 */
.transactions-table td:nth-child(9) {
    width: 145px;
    min-width: 145px;
    text-align: right;
}

.transactions-table th:nth-child(10),  /* 餘額 */
.transactions-table td:nth-child(10) {
    width: 120px;
    min-width: 120px;
    text-align: right;
}

.transactions-table th:last-child,  /* 操作 */
.transactions-table td:last-child {
    width: 70px;
    min-width: 70px;
}
```

## 翻译对照

### 英文 (EN)
- `精簡模式` → `Compact Mode`
- `標準模式` → `Standard Mode`
- `完整模式` → `Full Mode`
- `已隱藏次要欄位` → `Hidden secondary columns`
- `如需查看完整數據` → `To view complete data`
- `請點擊頂部「Export」按鈕導出` → `click the top 'Export' button`

### 日文 (JP)
- `精簡模式` → `コンパクトモード`
- `標準模式` → `標準モード`
- `完整模式` → `フルモード`
- `已隱藏次要欄位` → `補助列を非表示`
- `如需查看完整數據` → `完全なデータを表示するには`
- `請點擊頂部「Export」按鈕導出` → `上部の「Export」ボタンをクリック`

### 韩文 (KR)
- `精簡模式` → `컴팩트 모드`
- `標準模式` → `표준 모드`
- `完整模式` → `전체 모드`
- `已隱藏次要欄位` → `보조 열 숨김`
- `如需查看完整數據` → `전체 데이터를 보려면`
- `請點擊頂部「Export」按鈕導出` → `상단의 'Export' 버튼을 클릭하세요`

## 实施策略

由于文件结构复杂且CSS位置可能不同，最安全的方法是：

1. ✅ **不直接替换整个CSS块**（太危险）
2. ✅ **逐个关键属性更新**（更安全）
3. ✅ **保留各语言版本的现有注释**

### 关键更新点：

1. `.table-wrapper` margin 和 padding
2. `.transactions-table th, td` padding
3. `.checkbox-cell` width 和 padding
4. 列隐藏规则 (`nth-child` 选择器)
5. `.transactions-section::before` 提示信息
6. 列宽分配 (`nth-child` width/min-width)

---

**备注**: 由于各语言版本的HTML结构可能略有差异，需要手动验证`nth-child`选择器的正确性。

