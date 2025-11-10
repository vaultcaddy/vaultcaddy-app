/**
 * firstproject.html 增強功能
 * 
 * 功能列表：
 * 1. 文檔列表全選功能
 * 2. 項目名稱編輯功能
 * 3. 左側欄滾動條和搜索功能
 * 4. 文檔名稱過濾搜索功能
 * 5. 分頁控制功能
 * 6. 選中文件計數顯示
 * 7. 響應式設計改為滾動條
 */

// ============================================
// 全局變量
// ============================================

window.selectedDocuments = new Set(); // 選中的文檔ID集合
window.currentPage = 1;
window.rowsPerPage = 10;
window.totalDocuments = 0;
window.filteredDocuments = []; // 過濾後的文檔列表
window.allDocuments = []; // 所有文檔列表

// ============================================
// 1. 文檔列表全選功能
// ============================================

/**
 * 切換全選/取消全選（只選擇當前頁顯示的文檔）
 */
window.toggleSelectAll = function() {
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const isChecked = selectAllCheckbox.checked;
    
    // 獲取當前頁面顯示的所有文檔複選框
    const documentCheckboxes = document.querySelectorAll('#team-project-tbody input[type="checkbox"][data-doc-id]');
    
    console.log(`📋 當前頁顯示 ${documentCheckboxes.length} 個文檔`);
    
    documentCheckboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
        const docId = checkbox.getAttribute('data-doc-id');
        
        if (isChecked) {
            window.selectedDocuments.add(docId);
        } else {
            window.selectedDocuments.delete(docId);
        }
    });
    
    updateSelectedCount();
    console.log(`✅ ${isChecked ? '全選當前頁' : '取消全選當前頁'}: ${window.selectedDocuments.size} 個文檔已選中`);
};

/**
 * 切換單個文檔的選中狀態
 */
window.toggleDocumentSelection = function(docId) {
    if (window.selectedDocuments.has(docId)) {
        window.selectedDocuments.delete(docId);
    } else {
        window.selectedDocuments.add(docId);
    }
    
    // 更新全選複選框狀態
    updateSelectAllCheckbox();
    updateSelectedCount();
};

/**
 * 更新全選複選框狀態
 */
function updateSelectAllCheckbox() {
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const documentCheckboxes = document.querySelectorAll('#team-project-tbody input[type="checkbox"][data-doc-id]');
    
    if (documentCheckboxes.length === 0) {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = false;
        return;
    }
    
    const checkedCount = Array.from(documentCheckboxes).filter(cb => cb.checked).length;
    
    if (checkedCount === 0) {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = false;
    } else if (checkedCount === documentCheckboxes.length) {
        selectAllCheckbox.checked = true;
        selectAllCheckbox.indeterminate = false;
    } else {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = true;
    }
}

/**
 * 更新選中文件計數顯示
 */
function updateSelectedCount() {
    const countElement = document.querySelector('.selected-count-display');
    if (countElement) {
        const total = window.filteredDocuments.length || window.allDocuments.length;
        countElement.textContent = `${window.selectedDocuments.size} of ${total} row(s) selected.`;
    }
}

// ============================================
// 2. 項目名稱編輯功能
// ============================================

window.isEditingProjectName = false;

/**
 * 切換項目名稱編輯模式
 */
window.toggleProjectNameEdit = function() {
    const titleElement = document.getElementById('team-project-title');
    const editBtn = document.getElementById('edit-project-name-btn');
    
    if (!window.isEditingProjectName) {
        // 進入編輯模式
        window.isEditingProjectName = true;
        titleElement.contentEditable = 'true';
        titleElement.style.borderColor = '#3b82f6';
        titleElement.style.background = '#eff6ff';
        titleElement.focus();
        
        // 選中所有文字
        const range = document.createRange();
        range.selectNodeContents(titleElement);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        
        // 更改按鈕圖標為保存
        editBtn.innerHTML = '<i class="fas fa-check" style="font-size: 1.25rem; color: #10b981;"></i>';
        editBtn.title = '保存項目名稱';
        
        console.log('✏️ 進入項目名稱編輯模式');
    } else {
        // 保存並退出編輯模式
        saveProjectName();
    }
};

/**
 * 保存項目名稱
 */
async function saveProjectName() {
    const titleElement = document.getElementById('team-project-title');
    const editBtn = document.getElementById('edit-project-name-btn');
    const newName = titleElement.textContent.trim();
    
    if (!newName) {
        alert('項目名稱不能為空');
        return;
    }
    
    try {
        // 獲取當前項目ID
        const urlParams = new URLSearchParams(window.location.search);
        const projectId = urlParams.get('project');
        
        if (projectId && window.simpleDataManager) {
            // 更新 Firestore 中的項目名稱
            await window.simpleDataManager.updateProject(projectId, { name: newName });
            console.log('✅ 項目名稱已更新:', newName);
            
            // 更新左側欄中的項目名稱
            updateSidebarProjectName(projectId, newName);
        }
        
        // 退出編輯模式
        window.isEditingProjectName = false;
        titleElement.contentEditable = 'false';
        titleElement.style.borderColor = 'transparent';
        titleElement.style.background = 'transparent';
        
        // 恢復按鈕圖標
        editBtn.innerHTML = '<i class="fas fa-pen" style="font-size: 1.25rem;"></i>';
        editBtn.title = '編輯項目名稱';
        
    } catch (error) {
        console.error('❌ 保存項目名稱失敗:', error);
        alert('保存失敗，請重試');
    }
}

/**
 * 更新左側欄中的項目名稱
 */
function updateSidebarProjectName(projectId, newName) {
    const projectItem = document.querySelector(`.sidebar [data-project-id="${projectId}"]`);
    if (projectItem) {
        // 查找項目名稱的文本節點（通常在 span 或直接在元素中）
        const nameElement = projectItem.querySelector('.project-name') || projectItem;
        
        // 保留圖標，只更新文本
        const icon = nameElement.querySelector('i');
        if (icon) {
            nameElement.innerHTML = '';
            nameElement.appendChild(icon);
            nameElement.appendChild(document.createTextNode(' ' + newName));
        } else {
            // 如果沒有圖標，直接更新文本
            const textNode = Array.from(nameElement.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
            if (textNode) {
                textNode.textContent = ' ' + newName;
            }
        }
        
        console.log('✅ 左側欄項目名稱已更新:', newName);
    }
}

// 監聽 Enter 鍵保存
document.addEventListener('DOMContentLoaded', () => {
    const titleElement = document.getElementById('team-project-title');
    if (titleElement) {
        titleElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (window.isEditingProjectName) {
                    saveProjectName();
                }
            } else if (e.key === 'Escape') {
                // ESC 鍵取消編輯
                if (window.isEditingProjectName) {
                    window.location.reload();
                }
            }
        });
    }
});

// ============================================
// 3. 左側欄滾動條和搜索功能
// ============================================

/**
 * 初始化左側欄搜索功能
 */
function initSidebarSearch() {
    // 為左側欄項目列表添加搜索輸入框
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    // 查找或創建搜索輸入框
    let searchInput = sidebar.querySelector('.sidebar-search-input');
    if (!searchInput) {
        const searchContainer = sidebar.querySelector('.search-container');
        if (searchContainer) {
            searchInput = searchContainer.querySelector('input');
            if (searchInput) {
                searchInput.classList.add('sidebar-search-input');
                searchInput.addEventListener('input', filterSidebarProjects);
            }
        }
    }
    
    // 為項目列表容器添加滾動條樣式
    const projectList = sidebar.querySelector('.project-list');
    if (projectList) {
        projectList.style.maxHeight = 'calc(100vh - 400px)';
        projectList.style.overflowY = 'auto';
        projectList.style.overflowX = 'hidden';
    }
    
    console.log('✅ 左側欄搜索功能已初始化');
}

/**
 * 過濾左側欄項目（項目文件夾）
 */
function filterSidebarProjects(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    
    // 查找所有項目項目（帶有 data-project-id 的元素）
    const projectItems = document.querySelectorAll('.sidebar [data-project-id]');
    
    console.log(`🔍 搜索項目: "${searchTerm}", 找到 ${projectItems.length} 個項目`);
    
    if (!searchTerm) {
        // 如果搜索框為空，顯示所有項目
        projectItems.forEach(item => {
            item.style.display = '';
        });
        return;
    }
    
    projectItems.forEach(item => {
        const projectName = item.textContent.toLowerCase();
        if (projectName.includes(searchTerm)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// ============================================
// 4. 文檔名稱過濾搜索功能
// ============================================

/**
 * 初始化文檔名稱過濾功能
 */
function initDocumentFilter() {
    const filterInput = document.querySelector('input[placeholder="Filter document name..."]');
    if (filterInput) {
        filterInput.addEventListener('input', filterDocuments);
        console.log('✅ 文檔過濾功能已初始化');
    }
}

/**
 * 過濾文檔
 */
function filterDocuments(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    
    // 如果搜索框為空，恢復所有文檔
    if (!searchTerm) {
        window.filteredDocuments = [...window.allDocuments];
        console.log('🔄 恢復所有文檔:', window.allDocuments.length);
    } else {
        window.filteredDocuments = window.allDocuments.filter(doc => {
            const name = (doc.name || doc.fileName || '').toLowerCase();
            const vendor = (doc.vendor || doc.source || '').toLowerCase();
            return name.includes(searchTerm) || vendor.includes(searchTerm);
        });
        console.log(`🔍 過濾結果: ${window.filteredDocuments.length} / ${window.allDocuments.length} 個文檔`);
    }
    
    // 重置到第一頁
    window.currentPage = 1;
    
    // 清除所有選中狀態
    window.selectedDocuments.clear();
    
    // 重新渲染表格
    renderDocumentTable();
    updatePaginationControls();
    updateSelectedCount();
}

// ============================================
// 5. 分頁控制功能
// ============================================

/**
 * 初始化分頁控制
 */
function initPaginationControls() {
    // Rows per page 選擇器
    const rowsPerPageSelect = document.querySelector('select');
    if (rowsPerPageSelect) {
        rowsPerPageSelect.addEventListener('change', (e) => {
            window.rowsPerPage = parseInt(e.target.value);
            window.currentPage = 1;
            
            console.log(`📄 切換每頁顯示數: ${window.rowsPerPage}`);
            console.log(`📊 當前文檔總數: ${window.filteredDocuments.length}`);
            
            // 清除選中狀態
            window.selectedDocuments.clear();
            
            // 重新渲染
            renderDocumentTable();
            updatePaginationControls();
            updateSelectedCount();
        });
    }
    
    // 分頁按鈕
    const paginationButtons = document.querySelectorAll('.pagination-controls button');
    if (paginationButtons.length >= 4) {
        // << 首頁
        paginationButtons[0].onclick = () => goToPage(1);
        // < 上一頁
        paginationButtons[1].onclick = () => goToPage(window.currentPage - 1);
        // > 下一頁
        paginationButtons[2].onclick = () => goToPage(window.currentPage + 1);
        // >> 末頁
        paginationButtons[3].onclick = () => {
            const totalPages = Math.ceil(window.filteredDocuments.length / window.rowsPerPage) || 1;
            goToPage(totalPages);
        };
    }
    
    console.log('✅ 分頁控制已初始化');
}

/**
 * 跳轉到指定頁面
 */
window.goToPage = function(page) {
    const totalPages = Math.ceil(window.filteredDocuments.length / window.rowsPerPage);
    
    if (page < 1 || page > totalPages) return;
    
    window.currentPage = page;
    renderDocumentTable();
    updatePaginationControls();
    
    console.log(`📄 跳轉到第 ${page} 頁`);
};

/**
 * 更新分頁控制狀態
 */
function updatePaginationControls() {
    const totalPages = Math.ceil(window.filteredDocuments.length / window.rowsPerPage) || 1;
    
    // 更新頁碼顯示
    const pageDisplay = document.querySelector('.pagination-controls span:last-of-type');
    if (pageDisplay) {
        pageDisplay.textContent = `Page ${window.currentPage} of ${totalPages}`;
    }
    
    // 更新按鈕狀態
    const buttons = document.querySelectorAll('.pagination-controls button');
    if (buttons.length >= 4) {
        // 首頁和上一頁
        const isFirstPage = window.currentPage === 1;
        buttons[0].disabled = isFirstPage;
        buttons[1].disabled = isFirstPage;
        buttons[0].style.cursor = isFirstPage ? 'not-allowed' : 'pointer';
        buttons[1].style.cursor = isFirstPage ? 'not-allowed' : 'pointer';
        buttons[0].style.color = isFirstPage ? '#9ca3af' : '#374151';
        buttons[1].style.color = isFirstPage ? '#9ca3af' : '#374151';
        
        // 末頁和下一頁
        const isLastPage = window.currentPage === totalPages;
        buttons[2].disabled = isLastPage;
        buttons[3].disabled = isLastPage;
        buttons[2].style.cursor = isLastPage ? 'not-allowed' : 'pointer';
        buttons[3].style.cursor = isLastPage ? 'not-allowed' : 'pointer';
        buttons[2].style.color = isLastPage ? '#9ca3af' : '#374151';
        buttons[3].style.color = isLastPage ? '#9ca3af' : '#374151';
    }
}

/**
 * 渲染文檔表格
 */
function renderDocumentTable() {
    const tbody = document.getElementById('team-project-tbody');
    if (!tbody) return;
    
    // 計算當前頁的文檔
    const startIndex = (window.currentPage - 1) * window.rowsPerPage;
    const endIndex = startIndex + window.rowsPerPage;
    const pageDocuments = window.filteredDocuments.slice(startIndex, endIndex);
    
    if (pageDocuments.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" style="text-align: center; padding: 4rem 2rem;">
                    <div style="color: #6b7280;">
                        <i class="fas fa-file-alt" style="font-size: 3rem; margin-bottom: 1rem; color: #d1d5db;"></i>
                        <h3 style="font-size: 1.2rem; margin-bottom: 0.5rem; color: #374151;">No results.</h3>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    // 渲染文檔行
    tbody.innerHTML = pageDocuments.map(doc => `
        <tr style="border-bottom: 1px solid #e5e7eb; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='white'">
            <td style="padding: 1rem;">
                <input type="checkbox" data-doc-id="${doc.id}" ${window.selectedDocuments.has(doc.id) ? 'checked' : ''} onchange="toggleDocumentSelection('${doc.id}')">
            </td>
            <td style="padding: 1rem;">
                <a href="document-detail.html?project=${doc.projectId}&id=${doc.id}" style="color: #3b82f6; text-decoration: none; display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-file-pdf" style="color: #ef4444;"></i>
                    <span>${doc.name || doc.fileName || 'Untitled'}</span>
                </a>
            </td>
            <td style="padding: 1rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.25rem 0.75rem; background: #dbeafe; color: #1e40af; border-radius: 12px; font-size: 0.875rem;">
                    <i class="fas fa-file-invoice"></i>
                    <span>${doc.documentType || '發票'}</span>
                </span>
            </td>
            <td style="padding: 1rem; color: #374151;">${doc.vendor || doc.source || '-'}</td>
            <td style="padding: 1rem; text-align: right; color: #374151; font-weight: 600;">$${doc.amount || '0.00'}</td>
            <td style="padding: 1rem; color: #374151;">${doc.date || '-'}</td>
            <td style="padding: 1rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.25rem 0.75rem; background: #d1fae5; color: #065f46; border-radius: 12px; font-size: 0.875rem;">
                    ${doc.status === 'completed' ? '已完成' : doc.status === 'processing' ? '處理中' : '待處理'}
                </span>
            </td>
            <td style="padding: 1rem; color: #6b7280; font-size: 0.875rem;">${doc.uploadDate || new Date(doc.createdAt).toLocaleDateString('zh-TW')}</td>
            <td style="padding: 1rem; text-align: center;">
                <button onclick="deleteDocument('${doc.id}')" style="background: transparent; border: none; color: #6b7280; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: all 0.2s;" onmouseover="this.style.background='#fee2e2'; this.style.color='#dc2626'" onmouseout="this.style.background='transparent'; this.style.color='#6b7280'">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
    
    // 更新全選複選框狀態
    updateSelectAllCheckbox();
}

// ============================================
// 7. 響應式設計改為滾動條
// ============================================

/**
 * 初始化響應式滾動條
 */
function initResponsiveScroll() {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        mainContent.style.overflowX = 'auto';
        mainContent.style.overflowY = 'auto';
    }
    
    const tableContainer = document.querySelector('.table-container');
    if (tableContainer) {
        tableContainer.style.overflowX = 'auto';
        tableContainer.style.minWidth = '100%';
    }
    
    console.log('✅ 響應式滾動條已初始化');
}

// ============================================
// 初始化所有功能
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 初始化 firstproject 增強功能...');
    
    // 延遲初始化以確保 DOM 完全加載
    setTimeout(() => {
        initSidebarSearch();
        initDocumentFilter();
        initPaginationControls();
        initResponsiveScroll();
        updateSelectedCount();
        
        console.log('✅ firstproject 增強功能初始化完成');
    }, 500);
});

console.log('📦 firstproject-enhancements.js 已載入');

