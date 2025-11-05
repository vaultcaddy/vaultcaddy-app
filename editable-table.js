/**
 * VaultCaddy 可編輯表格功能
 * 
 * 作用：
 * 1. 讓用戶可以直接在表格中編輯 AI 提取的數據
 * 2. 自動保存編輯後的數據到 LocalStorage
 * 3. 顯示保存狀態指示器
 * 4. 支持數據驗證（日期、金額格式）
 * 
 * 參考：LedgerBox 圖3 的可編輯表格
 * 
 * @version 1.0.0
 * @updated 2025-10-26
 */

class EditableTable {
    constructor(tableId, options = {}) {
        this.tableId = tableId;
        this.options = {
            autoSave: true,
            saveDelay: 1000, // 1 秒後自動保存
            validateOnBlur: true,
            ...options
        };
        
        this.saveTimeout = null;
        this.unsavedChanges = new Set();
        
        console.log('📝 可編輯表格初始化');
        console.log('   表格 ID:', tableId);
        console.log('   自動保存:', this.options.autoSave);
    }
    
    /**
     * 初始化可編輯表格
     */
    init() {
        const table = document.getElementById(this.tableId);
        if (!table) {
            console.error(`❌ 找不到表格: ${this.tableId}`);
            return;
        }
        
        // 為所有可編輯單元格添加事件監聽器
        this.makeTableEditable(table);
        
        console.log('✅ 可編輯表格已初始化');
    }
    
    /**
     * 使表格可編輯
     */
    makeTableEditable(table) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        
        // 為每個單元格添加 contenteditable 屬性
        const editableCells = tbody.querySelectorAll('td[data-editable="true"]');
        
        editableCells.forEach(cell => {
            // 添加可編輯屬性
            cell.contentEditable = true;
            cell.classList.add('editable-cell');
            
            // 添加事件監聽器
            cell.addEventListener('focus', (e) => this.handleCellFocus(e));
            cell.addEventListener('blur', (e) => this.handleCellBlur(e));
            cell.addEventListener('input', (e) => this.handleCellInput(e));
            cell.addEventListener('keydown', (e) => this.handleCellKeydown(e));
        });
        
        console.log(`✅ ${editableCells.length} 個單元格已設置為可編輯`);
    }
    
    /**
     * 處理單元格獲得焦點
     */
    handleCellFocus(event) {
        const cell = event.target;
        cell.classList.add('editing');
        
        // 保存原始值
        cell.dataset.originalValue = cell.textContent;
    }
    
    /**
     * 處理單元格失去焦點
     */
    handleCellBlur(event) {
        const cell = event.target;
        cell.classList.remove('editing');
        
        const newValue = cell.textContent.trim();
        const originalValue = cell.dataset.originalValue;
        
        // 如果值改變了
        if (newValue !== originalValue) {
            // 驗證輸入
            if (this.options.validateOnBlur) {
                const isValid = this.validateCell(cell);
                if (!isValid) {
                    // 恢復原始值
                    cell.textContent = originalValue;
                    return;
                }
            }
            
            // 標記為已修改
            cell.classList.add('modified');
            this.unsavedChanges.add(cell);
            
            // 自動保存
            if (this.options.autoSave) {
                this.scheduleSave();
            }
        }
    }
    
    /**
     * 處理單元格輸入
     */
    handleCellInput(event) {
        const cell = event.target;
        
        // 實時驗證（可選）
        // this.validateCell(cell);
    }
    
    /**
     * 處理鍵盤事件
     */
    handleCellKeydown(event) {
        const cell = event.target;
        
        // Enter 鍵：移動到下一行同一列
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.moveToNextRow(cell);
        }
        
        // Tab 鍵：移動到下一個可編輯單元格
        if (event.key === 'Tab') {
            event.preventDefault();
            if (event.shiftKey) {
                this.moveToPreviousCell(cell);
            } else {
                this.moveToNextCell(cell);
            }
        }
        
        // Escape 鍵：取消編輯
        if (event.key === 'Escape') {
            cell.textContent = cell.dataset.originalValue;
            cell.blur();
        }
    }
    
    /**
     * 驗證單元格
     */
    validateCell(cell) {
        const fieldType = cell.dataset.fieldType;
        const value = cell.textContent.trim();
        
        switch (fieldType) {
            case 'date':
                return this.validateDate(value, cell);
            case 'amount':
            case 'number':
                return this.validateNumber(value, cell);
            case 'text':
            default:
                return true;
        }
    }
    
    /**
     * 驗證日期格式
     */
    validateDate(value, cell) {
        // 支持多種日期格式
        const datePatterns = [
            /^\d{4}-\d{2}-\d{2}$/,  // YYYY-MM-DD
            /^\d{2}\/\d{2}\/\d{4}$/, // DD/MM/YYYY
            /^\d{2}\/\d{2}\/\d{2}$/  // DD/MM/YY
        ];
        
        const isValid = datePatterns.some(pattern => pattern.test(value));
        
        if (!isValid) {
            cell.classList.add('invalid');
            this.showError(cell, '日期格式無效（請使用 YYYY-MM-DD 或 DD/MM/YYYY）');
        } else {
            cell.classList.remove('invalid');
            this.hideError(cell);
        }
        
        return isValid;
    }
    
    /**
     * 驗證數字格式
     */
    validateNumber(value, cell) {
        // 移除貨幣符號和逗號
        const cleanValue = value.replace(/[$,\s]/g, '');
        const isValid = !isNaN(cleanValue) && cleanValue !== '';
        
        if (!isValid) {
            cell.classList.add('invalid');
            this.showError(cell, '請輸入有效的數字');
        } else {
            cell.classList.remove('invalid');
            this.hideError(cell);
        }
        
        return isValid;
    }
    
    /**
     * 顯示錯誤消息
     */
    showError(cell, message) {
        // 移除舊的錯誤消息
        this.hideError(cell);
        
        const error = document.createElement('div');
        error.className = 'cell-error-message';
        error.textContent = message;
        
        cell.parentElement.style.position = 'relative';
        cell.parentElement.appendChild(error);
    }
    
    /**
     * 隱藏錯誤消息
     */
    hideError(cell) {
        const error = cell.parentElement.querySelector('.cell-error-message');
        if (error) {
            error.remove();
        }
    }
    
    /**
     * 移動到下一行同一列
     */
    moveToNextRow(cell) {
        const row = cell.parentElement;
        const cellIndex = Array.from(row.children).indexOf(cell);
        const nextRow = row.nextElementSibling;
        
        if (nextRow) {
            const nextCell = nextRow.children[cellIndex];
            if (nextCell && nextCell.contentEditable === 'true') {
                nextCell.focus();
            }
        }
    }
    
    /**
     * 移動到下一個可編輯單元格
     */
    moveToNextCell(cell) {
        const allEditableCells = Array.from(
            document.querySelectorAll(`#${this.tableId} td[contenteditable="true"]`)
        );
        const currentIndex = allEditableCells.indexOf(cell);
        
        if (currentIndex < allEditableCells.length - 1) {
            allEditableCells[currentIndex + 1].focus();
        }
    }
    
    /**
     * 移動到上一個可編輯單元格
     */
    moveToPreviousCell(cell) {
        const allEditableCells = Array.from(
            document.querySelectorAll(`#${this.tableId} td[contenteditable="true"]`)
        );
        const currentIndex = allEditableCells.indexOf(cell);
        
        if (currentIndex > 0) {
            allEditableCells[currentIndex - 1].focus();
        }
    }
    
    /**
     * 安排保存
     */
    scheduleSave() {
        // 清除之前的定時器
        if (this.saveTimeout) {
            clearTimeout(this.saveTimeout);
        }
        
        // 設置新的定時器
        this.saveTimeout = setTimeout(() => {
            this.save();
        }, this.options.saveDelay);
        
        // 顯示保存中狀態
        this.showSavingIndicator();
    }
    
    /**
     * 保存更改
     */
    async save() {
        if (this.unsavedChanges.size === 0) {
            return;
        }
        
        console.log(`💾 保存 ${this.unsavedChanges.size} 個更改...`);
        
        // 收集所有更改
        const changes = {};
        this.unsavedChanges.forEach(cell => {
            const row = cell.parentElement;
            const rowIndex = row.dataset.rowIndex;
            const fieldName = cell.dataset.fieldName;
            const value = cell.textContent.trim();
            
            if (!changes[rowIndex]) {
                changes[rowIndex] = {};
            }
            changes[rowIndex][fieldName] = value;
        });
        
        // 保存到 Firestore
        await this.saveToFirestore(changes);
        
        // 清除未保存標記
        this.unsavedChanges.forEach(cell => {
            cell.classList.remove('modified');
        });
        this.unsavedChanges.clear();
        
        // 顯示保存成功
        this.showSavedIndicator();
        
        console.log('✅ 更改已保存');
    }
    
    /**
     * 保存到 Firestore
     */
    async saveToFirestore(changes) {
        // 獲取當前文檔 ID 和項目 ID
        const params = new URLSearchParams(window.location.search);
        const documentId = params.get('id');
        const projectId = params.get('project');
        
        if (!documentId || !projectId) {
            console.error('❌ 無法保存：缺少文檔 ID 或項目 ID');
            return;
        }
        
        // ✅ 使用 SimpleDataManager 保存到 Firebase
        if (!window.simpleDataManager || !window.simpleDataManager.initialized) {
            console.error('❌ SimpleDataManager 未初始化');
            return;
        }
        
        try {
            // 獲取當前文檔數據
            const doc = await window.simpleDataManager.getDocument(documentId);
            
            if (!doc) {
                console.error('❌ 找不到文檔');
                return;
            }
            
            // 更新文檔數據
            const transactions = doc.processedData?.transactions || [];
            
            Object.keys(changes).forEach(rowIndex => {
                const index = parseInt(rowIndex);
                if (transactions[index]) {
                    Object.assign(transactions[index], changes[rowIndex]);
                }
            });
            
            // 保存回 Firestore
            await window.simpleDataManager.updateDocument(documentId, {
                processedData: {
                    ...doc.processedData,
                    transactions
                }
            });
            
            console.log('✅ 數據已保存到 Firestore');
        } catch (error) {
            console.error('❌ 保存到 Firestore 失敗:', error);
        }
    }
    
    /**
     * 顯示保存中指示器
     */
    showSavingIndicator() {
        let indicator = document.getElementById('saveIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'saveIndicator';
            indicator.className = 'save-indicator saving';
            document.body.appendChild(indicator);
        }
        
        indicator.innerHTML = `
            <i class="fas fa-circle-notch fa-spin"></i>
            <span>保存中...</span>
        `;
        indicator.className = 'save-indicator saving';
    }
    
    /**
     * 顯示已保存指示器
     */
    showSavedIndicator() {
        let indicator = document.getElementById('saveIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'saveIndicator';
            document.body.appendChild(indicator);
        }
        
        indicator.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>已保存</span>
        `;
        indicator.className = 'save-indicator saved';
        
        // 3 秒後隱藏
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => {
                indicator.style.display = 'none';
            }, 300);
        }, 3000);
    }
}

// 導出為全局變量
if (typeof window !== 'undefined') {
    window.EditableTable = EditableTable;
    console.log('✅ 可編輯表格模塊已載入');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EditableTable;
}

