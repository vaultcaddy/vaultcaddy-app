# document-detail.html 整合计划

## 目标
将以下功能整合到 `document-detail.html`：
1. ✅ 手动修正功能（已完成 - `editable-table.js`）
2. ✅ CSV/QuickBooks/JSON 导出（已完成 - `export-manager.js`）
3. ✅ 对账状态显示（已完成 - 进度条和状态）
4. ⏳ **UI 整合**（当前任务）

## 当前状态

### 已完成的功能模块
- ✅ `editable-table.js` - 可编辑表格功能
- ✅ `editable-table.css` - 可编辑表格样式
- ✅ `export-manager.js` - 导出管理器（CSV, IIF, QBO, JSON）
- ✅ `reconciliation-engine.js` - 对账引擎
- ✅ `batch-upload-processor.js` - 批量上传处理器
- ✅ `firebase-data-manager.js` - Firebase 数据持久化

### 需要整合的内容

#### 1. 添加导出按钮到 document-detail.html
在文档详情页面的右上角添加导出按钮：

```html
<!-- 导出按钮 -->
<div class="export-actions" style="position: absolute; top: 2rem; right: 2rem;">
    <button class="export-btn" onclick="toggleExportMenu(event)">
        <i class="fas fa-download"></i> Export
        <i class="fas fa-chevron-down"></i>
    </button>
    <div class="export-menu" id="exportMenu" style="display: none;">
        <div class="export-menu-item" onclick="exportDocument('csv')">
            <i class="fas fa-file-csv"></i> CSV
        </div>
        <div class="export-menu-item" onclick="exportDocument('iif')">
            <i class="fas fa-file-invoice"></i> IIF (QuickBooks)
        </div>
        <div class="export-menu-item" onclick="exportDocument('qbo')">
            <i class="fas fa-file-invoice-dollar"></i> QBO (QuickBooks)
        </div>
        <div class="export-menu-item" onclick="exportDocument('json')">
            <i class="fas fa-file-code"></i> JSON
        </div>
    </div>
</div>
```

#### 2. 启用可编辑表格功能
在文档详情页面的表格中启用内联编辑：

```javascript
// 初始化可编辑表格
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.invoice-details-table, .transactions-table');
    tables.forEach(table => {
        window.editableTable.makeTableEditable(table);
    });
});
```

#### 3. 添加对账状态显示
在发票详情中显示对账进度：

```html
<!-- 对账状态 -->
<div class="reconciliation-status">
    <div class="status-header">
        <h3>Reconciliation Status</h3>
        <span class="status-badge" id="reconciliationBadge">
            <i class="fas fa-sync-alt fa-spin"></i> Processing...
        </span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" id="reconciliationProgress" style="width: 0%"></div>
    </div>
    <p class="status-text" id="reconciliationText">Matching transactions...</p>
</div>
```

#### 4. 添加必要的脚本引用
在 `document-detail.html` 的 `<head>` 部分添加：

```html
<!-- 可编辑表格 -->
<link rel="stylesheet" href="editable-table.css">
<script src="editable-table.js"></script>

<!-- 导出管理器 -->
<script src="export-manager.js"></script>

<!-- 对账引擎 -->
<script src="reconciliation-engine.js"></script>
```

## 实施步骤

### 步骤 1: 更新 HTML 结构（10分钟）
1. 添加导出按钮到页面右上角
2. 添加对账状态显示区域
3. 更新表格结构以支持编辑

### 步骤 2: 添加脚本引用（5分钟）
1. 在 `<head>` 中添加 CSS 和 JS 文件引用
2. 确保加载顺序正确

### 步骤 3: 初始化功能（15分钟）
1. 初始化可编辑表格
2. 绑定导出按钮事件
3. 加载对账状态

### 步骤 4: 样式调整（10分钟）
1. 调整导出按钮位置
2. 优化对账状态显示
3. 确保与现有设计一致

### 步骤 5: 测试（20分钟）
1. 测试内联编辑功能
2. 测试导出功能（CSV, IIF, QBO, JSON）
3. 测试对账状态显示

## 预期效果

### 1. 导出功能
用户可以：
- 点击 "Export" 按钮
- 选择导出格式（CSV, IIF, QBO, JSON）
- 下载文件到本地

### 2. 手动修正功能
用户可以：
- 双击表格单元格进行编辑
- 修改发票金额、日期、描述等
- 按 Enter 保存，按 Esc 取消

### 3. 对账状态
用户可以：
- 查看对账进度（0-100%）
- 查看匹配状态（已匹配/未匹配）
- 查看匹配建议

## 代码示例

### 导出功能实现
```javascript
function exportDocument(format) {
    const documentId = getCurrentDocumentId();
    const document = loadDocumentFromStorage(documentId);
    
    if (!document) {
        alert('无法加载文档数据');
        return;
    }
    
    const exportManager = window.exportManager;
    let result;
    
    switch (format) {
        case 'csv':
            result = exportManager.exportToCSV([document]);
            break;
        case 'iif':
            result = exportManager.exportToIIF([document]);
            break;
        case 'qbo':
            result = exportManager.exportToQBO([document]);
            break;
        case 'json':
            result = exportManager.exportToJSON([document]);
            break;
    }
    
    if (result.success) {
        console.log('✅ 导出成功:', result.filename);
    } else {
        alert('导出失败: ' + result.error);
    }
}
```

### 可编辑表格实现
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // 初始化可编辑表格
    const invoiceTable = document.querySelector('.invoice-details-table');
    if (invoiceTable) {
        window.editableTable.makeTableEditable(invoiceTable);
    }
    
    // 监听编辑事件
    invoiceTable.addEventListener('cellEdited', function(e) {
        const { row, cell, oldValue, newValue } = e.detail;
        console.log('单元格已编辑:', { row, cell, oldValue, newValue });
        
        // 保存到 localStorage 或 Firebase
        saveDocumentChanges(getCurrentDocumentId(), {
            field: cell.dataset.field,
            value: newValue
        });
    });
});
```

### 对账状态实现
```javascript
async function updateReconciliationStatus(documentId) {
    const document = loadDocumentFromStorage(documentId);
    const reconciliationEngine = window.reconciliationEngine;
    
    // 获取对账结果
    const result = await reconciliationEngine.matchTransactions(
        document.transactions,
        [] // 银行对账单交易（待实现）
    );
    
    // 更新 UI
    const progress = result.matchedCount / result.totalCount * 100;
    document.getElementById('reconciliationProgress').style.width = progress + '%';
    document.getElementById('reconciliationText').textContent = 
        `${result.matchedCount} / ${result.totalCount} transactions matched`;
    
    // 更新状态徽章
    const badge = document.getElementById('reconciliationBadge');
    if (progress === 100) {
        badge.innerHTML = '<i class="fas fa-check-circle"></i> Complete';
        badge.className = 'status-badge success';
    } else {
        badge.innerHTML = `<i class="fas fa-sync-alt"></i> ${Math.round(progress)}%`;
        badge.className = 'status-badge processing';
    }
}
```

## 时间估算
- **步骤 1-2**: 15分钟
- **步骤 3**: 15分钟
- **步骤 4**: 10分钟
- **步骤 5**: 20分钟
- **总计**: 约 60分钟

## 下一步
1. 开始实施步骤 1：更新 HTML 结构
2. 测试导出功能
3. 测试可编辑表格
4. 测试对账状态显示

---

**创建时间**: 2025-10-26  
**作用**: 整合所有功能到 document-detail.html  
**帮助**: 提供详细的实施计划和代码示例

