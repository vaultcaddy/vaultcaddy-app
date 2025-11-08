// ============================================
// VaultCaddy Document Detail Page
// 完全重寫的簡化版本
// ============================================

// 調試模式
const DEBUG_MODE = false;

// 全局變量
let currentDocument = null;
let currentPageNumber = 1;
let totalPagesCount = 1;
let zoomLevel = 100;
let autoSaveTimeout = null;
let hasUnsavedChanges = false;

// ============================================
// 初始化函數
// ============================================

async function init() {
    console.log('🚀 初始化文檔詳情頁面...');
    
    // 步驟 1: 等待 SimpleAuth 初始化
    console.log('⏳ 步驟 1/5: 等待 SimpleAuth 初始化...');
    let attempts = 0;
    while (!window.simpleAuth || !window.simpleAuth.initialized) {
        if (attempts++ > 100) { // Max 10 seconds wait
            console.error('❌ SimpleAuth 初始化超時');
            if (!DEBUG_MODE) {
                alert('系統初始化失敗，請刷新頁面');
                window.location.href = 'index.html';
            }
            return;
        }
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    console.log('✅ SimpleAuth 已就緒');
    
    // 步驟 2: 等待用戶狀態確定
    console.log('⏳ 步驟 2/5: 等待用戶狀態確定...');
    attempts = 0;
    while (!window.simpleAuth.currentUser) {
        if (attempts++ > 100) { // Max 10 seconds wait
            console.error('❌ 用戶未登入');
            if (!DEBUG_MODE) {
                alert('請先登入');
                window.location.href = 'index.html';
            }
            return;
        }
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    console.log('✅ 用戶已登入:', window.simpleAuth.currentUser.email);
    
    // 步驟 3: 移除頁面保護並初始化 Navbar/Sidebar
    console.log('⏳ 步驟 3/5: 移除頁面保護並初始化 UI...');
    document.body.classList.remove('auth-checking');
    document.body.classList.add('auth-ready');
    
    // 初始化 Navbar 和 Sidebar
    if (window.VaultCaddyNavbar) {
        window.vaultcaddyNavbar = new window.VaultCaddyNavbar();
    }
    if (window.VaultCaddySidebar) {
        window.unifiedSidebar = new window.VaultCaddySidebar();
    }
    
    console.log('✅ 頁面已顯示');
    
    // 步驟 4: 等待 SimpleDataManager 初始化
    console.log('⏳ 步驟 4/5: 等待 SimpleDataManager 初始化...');
    attempts = 0;
    while (!window.simpleDataManager || !window.simpleDataManager.initialized) {
        if (attempts++ > 100) {
            console.error('❌ SimpleDataManager 初始化超時');
            alert('數據管理器初始化失敗');
            return;
        }
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    console.log('✅ SimpleDataManager 已就緒');
    
    // 步驟 5: 載入文檔
    console.log('⏳ 步驟 5/5: 載入文檔...');
    await loadDocument();
    console.log('✅ 初始化完成！');
}

// ============================================
// 文檔載入函數
// ============================================

async function loadDocument() {
    console.log('📄 開始載入文檔...');
    
    // 獲取 URL 參數
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');
    const documentId = urlParams.get('id');
    
    console.log('📋 參數:', { projectId, documentId });
    
    if (!projectId || !documentId) {
        console.error('❌ 缺少必要參數');
        alert('缺少必要參數');
        goBackToDashboard();
        return;
    }
    
    try {
        // 從 Firebase 獲取文檔
        console.log('🔍 從 Firebase 獲取文檔...');
        const doc = await window.simpleDataManager.getDocument(projectId, documentId);
        
        if (!doc) {
            console.error('❌ 找不到文檔');
            alert('找不到文檔');
            goBackToDashboard();
            return;
        }
        
        console.log('✅ 文檔載入成功:', doc);
        currentDocument = doc;
        
        // 更新頁面標題
        document.getElementById('documentTitle').textContent = doc.name || doc.fileName || '未命名文檔';
        
        // 顯示 PDF 預覽
        displayPDFPreview();
        
        // 顯示文檔內容
        displayDocumentContent();
        
    } catch (error) {
        console.error('❌ 載入文檔失敗:', error);
        alert('載入文檔失敗: ' + error.message);
        goBackToDashboard();
    }
}

// ============================================
// PDF 預覽函數
// ============================================

async function displayPDFPreview() {
    console.log('📄 顯示 PDF 預覽');
    const pdfViewer = document.getElementById('pdfViewer');
    
    if (!currentDocument) {
        pdfViewer.innerHTML = '<div class="loading"><div class="loading-spinner"></div><div>無法載入文檔</div></div>';
        return;
    }
    
    console.log('📄 文檔對象完整內容:', JSON.stringify(currentDocument, null, 2));
    console.log('📄 文檔對象所有鍵:', Object.keys(currentDocument));
    
    // 增強版：從多個來源獲取圖片 URL
    let imageUrl = null;
    
    console.log('🔍 開始載入文檔預覽...');
    console.log('📄 文檔對象:', JSON.stringify(currentDocument, null, 2));
    
    // 方法1：嘗試從文檔對象中的 URL 字段
    imageUrl = currentDocument.imageUrl || 
               currentDocument.downloadURL || 
               currentDocument.url || 
               currentDocument.fileUrl;
    
    console.log('📌 方法1 - 文檔對象 URL:', imageUrl || '無');
    
    // 方法2：如果沒有 URL，從 Firebase Storage 獲取
    if (!imageUrl) {
        try {
            const storage = firebase.storage();
            const userId = window.simpleAuth?.currentUser?.uid || firebase.auth().currentUser?.uid;
            const projectId = currentDocument.projectId;
            const fileName = currentDocument.fileName || currentDocument.name;
            
            if (!userId) {
                console.error('❌ 無法獲取用戶 ID');
                throw new Error('用戶未登入');
            }
            
            if (!projectId) {
                console.error('❌ 無法獲取項目 ID');
                throw new Error('項目 ID 不存在');
            }
            
            if (!fileName) {
                console.error('❌ 無法獲取文件名');
                throw new Error('文件名不存在');
            }
            
            console.log('📂 Storage 參數:', { userId, projectId, fileName });
            
            // 嘗試多個可能的路徑
            const possiblePaths = [
                `documents/${userId}/${projectId}/${fileName}`,  // simple-data-manager.js 路徑
                `users/${userId}/projects/${projectId}/${fileName}`,
                `projects/${projectId}/documents/${fileName}`,
                `${projectId}/${fileName}`,
                fileName
            ];
            
            console.log('🔍 嘗試以下 Storage 路徑:');
            for (let i = 0; i < possiblePaths.length; i++) {
                const path = possiblePaths[i];
                console.log(`  ${i + 1}. ${path}`);
                try {
                    const storageRef = storage.ref(path);
                    imageUrl = await storageRef.getDownloadURL();
                    console.log(`✅ 成功！使用路徑 ${i + 1}: ${path}`);
                    console.log(`🖼️ 圖片 URL: ${imageUrl}`);
                    break;
                } catch (error) {
                    console.log(`  ❌ 路徑 ${i + 1} 失敗: ${error.code}`);
                }
            }
            
            if (!imageUrl) {
                console.error('❌ 所有路徑都失敗了');
                console.log('💡 請在 Firebase Console Storage 中查找實際文件路徑');
                console.log('💡 文件名:', fileName);
                console.log('💡 項目ID:', projectId);
                console.log('💡 用戶ID:', userId);
                console.log('💡 文檔完整對象:', currentDocument);
            }
        } catch (error) {
            console.error('❌ 從 Storage 獲取失敗:', error.code, error.message);
            console.error('❌ 錯誤詳情:', error);
        }
    }
    
    console.log('🖼️ 最終圖片 URL:', imageUrl);
    if (!imageUrl) {
        console.log('⚠️ 圖片 URL 為空，可能的原因：');
        console.log('   1. 文檔對象中沒有保存 imageUrl/downloadURL');
        console.log('   2. Firebase Storage 中找不到文件');
        console.log('   3. 文件路徑不匹配');
        console.log('📝 文檔名稱:', currentDocument.name || currentDocument.fileName);
        console.log('📂 項目ID:', currentDocument.projectId);
        console.log('👤 用戶ID:', window.simpleAuth?.currentUser?.uid || firebase.auth().currentUser?.uid);
    }
    
    if (imageUrl) {
        pdfViewer.innerHTML = `
            <div class="pdf-page" style="transform: scale(${zoomLevel / 100}); transition: transform 0.2s; transform-origin: top center;">
                <img src="${imageUrl}" alt="Document Preview" 
                     style="max-width: 100%; height: auto; display: block; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
                     onerror="console.error('圖片載入失敗:', '${imageUrl}'); this.parentElement.innerHTML='<div style=\\'padding: 2rem; text-align: center; color: #6b7280;\\'>無法載入預覽<br><small style=\\'color: #9ca3af; font-size: 0.75rem; word-break: break-all;\\'>URL: ${imageUrl}</small></div>'">
            </div>
        `;
    } else {
        pdfViewer.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: #6b7280;">
                <i class="fas fa-file-image" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                <p>無預覽可用</p>
                <small style="color: #9ca3af; font-size: 0.75rem;">文檔可能尚未處理或不支持預覽</small>
                ${currentDocument.name ? `<br><small style="color: #9ca3af; font-size: 0.75rem;">文件名: ${currentDocument.name}</small>` : ''}
            </div>
        `;
    }
}

// ============================================
// 文檔內容顯示函數
// ============================================

function displayDocumentContent() {
    console.log('📋 顯示文檔內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    if (!currentDocument) {
        detailsSection.innerHTML = '<div class="loading"><div class="loading-spinner"></div><div>載入中...</div></div>';
        return;
    }
    
    const data = currentDocument.processedData || {};
    const docType = currentDocument.type || currentDocument.documentType || 'general';
    
    console.log('📊 文檔類型:', docType);
    console.log('📊 處理數據:', data);
    
    // 根據文檔類型顯示不同內容
    if (docType === 'invoice') {
        displayInvoiceContent(data);
    } else if (docType === 'bank_statement') {
        displayBankStatementContent(data);
    } else if (docType === 'receipt') {
        displayReceiptContent(data);
    } else {
        displayGeneralContent(data);
    }
}

// ============================================
// 發票內容顯示
// ============================================

function displayInvoiceContent(data) {
    console.log('📄 顯示發票內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    // 發票詳情卡片（改為單列卡片式布局）
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-file-invoice" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                發票詳情
            </h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">發票號碼</label>
                    <input type="text" id="invoiceNumber" value="${data.invoiceNumber || data.invoice_number || '—'}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">日期</label>
                    <input type="date" id="invoiceDate" value="${data.date || data.invoice_date || ''}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">供應商</label>
                    <input type="text" id="vendor" value="${data.vendor || data.supplier || data.merchantName || '—'}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">總金額</label>
                    <input type="text" id="totalAmount" value="${formatCurrency(data.total || data.totalAmount || 0)}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #10b981; background: white;">
                </div>
            </div>
        </div>
    `;
    
    // 項目明細表格（可編輯）
    const items = data.items || data.lineItems || [];
    
    let itemsHTML = '';
    items.forEach((item, index) => {
        // 安全地轉換為數字
        const unitPrice = parseFloat(item.unit_price || item.unitPrice || 0) || 0;
        const amount = parseFloat(item.amount || 0) || 0;
        const quantity = parseFloat(item.quantity || 0) || 0;
        
        itemsHTML += `
            <tr>
                <td contenteditable="true" data-field="code" data-index="${index}" style="padding: 0.75rem; color: #6b7280; cursor: text;">${item.code || item.itemCode || '—'}</td>
                <td contenteditable="true" data-field="description" data-index="${index}" style="padding: 0.75rem; color: #1f2937; font-weight: 500; cursor: text;">${item.description || '—'}</td>
                <td contenteditable="true" data-field="quantity" data-index="${index}" style="padding: 0.75rem; text-align: right; color: #1f2937; cursor: text;">${quantity}</td>
                <td contenteditable="true" data-field="unit" data-index="${index}" style="padding: 0.75rem; text-align: right; color: #6b7280; cursor: text;">${item.unit || '件'}</td>
                <td contenteditable="true" data-field="unit_price" data-index="${index}" style="padding: 0.75rem; text-align: right; color: #1f2937; cursor: text;">${unitPrice.toFixed(2)}</td>
                <td contenteditable="true" data-field="amount" data-index="${index}" style="padding: 0.75rem; text-align: right; color: #1f2937; font-weight: 500; cursor: text;">${amount.toFixed(2)}</td>
            </tr>
        `;
    });
    
    dataSection.innerHTML = `
        <div class="transactions-section">
            <h3 class="transactions-title" style="margin-bottom: 1rem;">
                <i class="fas fa-list" style="color: #8b5cf6; margin-right: 0.5rem;"></i>
                項目明細
                <span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;">(可編輯)</span>
            </h3>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th>代碼</th>
                        <th>描述</th>
                        <th style="text-align: right;">數量</th>
                        <th style="text-align: right;">單位</th>
                        <th style="text-align: right;">單價</th>
                        <th style="text-align: right;">金額</th>
                    </tr>
                </thead>
                <tbody id="itemsTableBody">
                    ${itemsHTML || '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #6b7280;">無項目數據</td></tr>'}
                </tbody>
            </table>
        </div>
    `;
    
    // 添加編輯事件監聽器
    addEditableListeners();
}

// ============================================
// 銀行對帳單內容顯示
// ============================================

function displayBankStatementContent(data) {
    console.log('🏦 顯示銀行對帳單內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    // 帳戶詳情
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-university" style="color: #10b981; margin-right: 0.5rem;"></i>
                帳戶信息
            </h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">帳戶名稱</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.accountName || '—'}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">帳戶號碼</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.accountNumber || '—'}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">期初餘額</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem; font-weight: 600;">${formatCurrency(data.openingBalance || 0)}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">期末餘額</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem; font-weight: 600;">${formatCurrency(data.closingBalance || 0)}</div>
                </div>
            </div>
        </div>
    `;
    
    // 交易列表
    const transactions = data.transactions || currentDocument.transactions || [];
    
    let transactionsHTML = '';
    transactions.forEach((tx, index) => {
        const amount = parseFloat(tx.amount || 0);
        const amountClass = amount >= 0 ? 'amount-positive' : 'amount-negative';
        
        transactionsHTML += `
            <tr>
                <td class="checkbox-cell"><input type="checkbox"></td>
                <td>${tx.date || '—'}</td>
                <td>${tx.description || '—'}</td>
                <td class="amount-cell ${amountClass}">${formatCurrency(amount)}</td>
                <td class="amount-cell">${formatCurrency(tx.balance || 0)}</td>
                <td class="action-cell">
                    <div class="action-btns">
                        <button class="icon-btn"><i class="fas fa-edit"></i></button>
                        <button class="icon-btn delete"><i class="fas fa-trash"></i></button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    dataSection.innerHTML = `
        <div class="transactions-section">
            <div class="transactions-header">
                <h3 class="transactions-title">
                    <i class="fas fa-exchange-alt" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                    交易記錄
                </h3>
            </div>
            <div class="transactions-info">
                共 ${transactions.length} 筆交易
            </div>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th class="checkbox-cell"><input type="checkbox"></th>
                        <th>日期</th>
                        <th>描述</th>
                        <th>金額</th>
                        <th>餘額</th>
                        <th class="action-cell">操作</th>
                    </tr>
                </thead>
                <tbody>
                    ${transactionsHTML || '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #6b7280;">無交易記錄</td></tr>'}
                </tbody>
            </table>
        </div>
    `;
}

// ============================================
// 收據內容顯示
// ============================================

function displayReceiptContent(data) {
    console.log('🧾 顯示收據內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-receipt" style="color: #8b5cf6; margin-right: 0.5rem;"></i>
                收據詳情
            </h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">商家</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.merchantName || data.vendor || '—'}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">日期</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.date || '—'}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">總金額</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #10b981;">${formatCurrency(data.total || data.totalAmount || 0)}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">付款方式</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.paymentMethod || '—'}</div>
                </div>
            </div>
        </div>
    `;
    
    dataSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1rem;">原始數據</h3>
            <pre style="background: #f9fafb; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem;">${JSON.stringify(data, null, 2)}</pre>
        </div>
    `;
}

// ============================================
// 通用內容顯示
// ============================================

function displayGeneralContent(data) {
    console.log('📋 顯示通用內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1rem;">
                <i class="fas fa-file-alt" style="color: #6b7280; margin-right: 0.5rem;"></i>
                文檔信息
            </h3>
            <div style="padding: 1rem; background: #f9fafb; border-radius: 6px;">
                <p style="color: #6b7280; font-size: 0.9rem;">此文檔尚未處理或類型未知</p>
            </div>
        </div>
    `;
    
    dataSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1rem;">原始數據</h3>
            <pre style="background: #f9fafb; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem;">${JSON.stringify(data, null, 2)}</pre>
        </div>
    `;
}

// ============================================
// 可編輯表格功能
// ============================================

function addEditableListeners() {
    console.log('✏️ 添加可編輯監聽器');
    
    const editableCells = document.querySelectorAll('[contenteditable="true"]');
    
    editableCells.forEach(cell => {
        // 輸入時標記為已更改
        cell.addEventListener('input', function() {
            const field = this.getAttribute('data-field');
            const index = parseInt(this.getAttribute('data-index'));
            const value = this.textContent.trim();
            
            console.log('✏️ 編輯中:', { field, index, value });
            
            // 更新 currentDocument
            if (!currentDocument.processedData.items) {
                currentDocument.processedData.items = [];
            }
            
            if (!currentDocument.processedData.items[index]) {
                currentDocument.processedData.items[index] = {};
            }
            
            // 根據字段類型轉換值
            if (field === 'quantity' || field === 'unit_price' || field === 'amount') {
                currentDocument.processedData.items[index][field] = parseFloat(value) || 0;
            } else {
                currentDocument.processedData.items[index][field] = value;
            }
            
            // 觸發自動保存
            markAsChanged();
        });
        
        // Enter 鍵移到下一個
        cell.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.blur();
            }
        });
    });
}

// ============================================
// 保存函數
// ============================================

// 顯示/隱藏 Saved 指示器
function showSavedIndicator() {
    const indicator = document.getElementById('savedIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
        hasUnsavedChanges = false;
        
        // 3 秒後隱藏
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 3000);
    }
}

// 標記有未保存的更改
function markAsChanged() {
    hasUnsavedChanges = true;
    
    // 清除之前的自動保存計時器
    if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout);
    }
    
    // 設置新的自動保存計時器（1 秒後保存）
    autoSaveTimeout = setTimeout(() => {
        autoSaveAllChanges();
    }, 1000);
}

// 自動保存所有更改
async function autoSaveAllChanges() {
    if (!hasUnsavedChanges) {
        return;
    }
    
    console.log('💾 自動保存所有更改...');
    
    if (!currentDocument) {
        return;
    }
    
    // 如果是發票，獲取發票詳情
    const docType = currentDocument.type || currentDocument.documentType || 'general';
    if (docType === 'invoice') {
        const invoiceNumber = document.getElementById('invoiceNumber')?.value;
        const invoiceDate = document.getElementById('invoiceDate')?.value;
        const vendor = document.getElementById('vendor')?.value;
        const totalAmount = document.getElementById('totalAmount')?.value;
        
        if (invoiceNumber || invoiceDate || vendor || totalAmount) {
            currentDocument.processedData = {
                ...currentDocument.processedData,
                invoiceNumber: invoiceNumber,
                date: invoiceDate,
                vendor: vendor,
                total: parseFloat(totalAmount?.replace(/[^0-9.-]+/g, '')) || 0
            };
        }
    }
    
    // 保存到 Firebase
    await saveDocumentChanges();
    
    // 顯示 Saved 指示器
    showSavedIndicator();
}

// 自動保存發票詳情（觸發自動保存）
async function autoSaveInvoiceDetails() {
    markAsChanged();
}

// 手動保存所有更改（保留以防其他地方調用）
async function saveAllChanges() {
    await autoSaveAllChanges();
}

async function saveDocumentChanges() {
    console.log('💾 保存文檔更改到 Firebase...');
    
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const projectId = urlParams.get('project');
        const documentId = urlParams.get('id');
        
        if (!projectId || !documentId) {
            console.error('❌ 缺少必要參數');
            return;
        }
        
        await window.simpleDataManager.updateDocument(projectId, documentId, {
            processedData: currentDocument.processedData,
            lastModified: new Date().toISOString()
        });
        
        console.log('✅ 保存成功');
    } catch (error) {
        console.error('❌ 保存失敗:', error);
        alert('保存失敗: ' + error.message);
    }
}

// ============================================
// PDF 控制函數
// ============================================

function zoomIn() {
    zoomLevel = Math.min(200, zoomLevel + 25);
    displayPDFPreview();
}

function zoomOut() {
    zoomLevel = Math.max(50, zoomLevel - 25);
    displayPDFPreview();
}

function resetZoom() {
    zoomLevel = 100;
    displayPDFPreview();
}

function previousPage() {
    if (currentPageNumber > 1) {
        currentPageNumber--;
        updatePageDisplay();
    }
}

function nextPage() {
    if (currentPageNumber < totalPagesCount) {
        currentPageNumber++;
        updatePageDisplay();
    }
}

function updatePageDisplay() {
    document.getElementById('currentPage').textContent = currentPageNumber;
    document.getElementById('totalPages').textContent = totalPagesCount;
    document.getElementById('prevPageBtn').disabled = currentPageNumber === 1;
    document.getElementById('nextPageBtn').disabled = currentPageNumber === totalPagesCount;
}

// ============================================
// 導出功能
// ============================================

function toggleExportMenu(event) {
    event.stopPropagation();
    const menu = document.getElementById('exportMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

// 點擊其他地方關閉菜單
document.addEventListener('click', function() {
    const menu = document.getElementById('exportMenu');
    if (menu) menu.style.display = 'none';
});

async function exportDocument(format) {
    console.log('📥 導出文檔:', format);
    
    if (!currentDocument) {
        alert('無法導出：未找到文檔數據');
        return;
    }
    
    const data = currentDocument.processedData || {};
    const fileName = currentDocument.name || currentDocument.fileName || 'document';
    
    try {
        let content = '';
        let mimeType = '';
        let fileExtension = '';
        
        switch (format) {
            case 'csv':
                content = exportToCSV(data);
                mimeType = 'text/csv';
                fileExtension = 'csv';
                break;
            
            case 'iif':
                content = exportToIIF(data);
                mimeType = 'text/plain';
                fileExtension = 'iif';
                break;
            
            case 'qbo':
                content = exportToQBO(data);
                mimeType = 'application/xml';
                fileExtension = 'qbo';
                break;
            
            case 'json':
                content = JSON.stringify(currentDocument, null, 2);
                mimeType = 'application/json';
                fileExtension = 'json';
                break;
            
            default:
                alert('不支持的導出格式');
                return;
        }
        
        // 創建下載
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${fileName}.${fileExtension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('✅ 導出成功');
        
    } catch (error) {
        console.error('❌ 導出失敗:', error);
        alert('導出失敗: ' + error.message);
    }
}

// CSV 導出
function exportToCSV(data) {
    const docType = currentDocument.type || currentDocument.documentType || 'general';
    
    if (docType === 'invoice') {
        // 發票 CSV
        let csv = 'Code,Description,Quantity,Unit,Unit Price,Amount\n';
        const items = data.items || data.lineItems || [];
        items.forEach(item => {
            csv += `"${item.code || ''}","${item.description || ''}",${item.quantity || 0},"${item.unit || ''}",${item.unit_price || item.unitPrice || 0},${item.amount || 0}\n`;
        });
        return csv;
    } else if (docType === 'bank_statement') {
        // 銀行對帳單 CSV
        let csv = 'Date,Description,Amount,Balance\n';
        const transactions = data.transactions || currentDocument.transactions || [];
        transactions.forEach(tx => {
            csv += `"${tx.date || ''}","${tx.description || ''}",${tx.amount || 0},${tx.balance || 0}\n`;
        });
        return csv;
    } else {
        // 通用 CSV
        return JSON.stringify(data, null, 2);
    }
}

// IIF 導出 (QuickBooks)
function exportToIIF(data) {
    let iif = '!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tMEMO\n';
    
    const docType = currentDocument.type || currentDocument.documentType || 'general';
    
    if (docType === 'invoice') {
        const invoiceDate = data.date || data.invoice_date || new Date().toISOString().split('T')[0];
        const vendor = data.vendor || data.supplier || 'Unknown';
        const total = data.total || data.totalAmount || 0;
        
        iif += `TRNS\t\tINVOICE\t${invoiceDate}\tAccounts Receivable\t${vendor}\t${total}\t${data.invoiceNumber || ''}\n`;
        
        const items = data.items || data.lineItems || [];
        items.forEach(item => {
            iif += `SPL\t\t\t${invoiceDate}\tIncome\t\t${item.amount || 0}\t${item.description || ''}\n`;
        });
    } else if (docType === 'bank_statement') {
        const transactions = data.transactions || currentDocument.transactions || [];
        transactions.forEach(tx => {
            iif += `TRNS\t\tDEPOSIT\t${tx.date || ''}\tBank Account\t\t${tx.amount || 0}\t${tx.description || ''}\n`;
        });
    }
    
    return iif;
}

// QBO 導出 (QuickBooks Online)
function exportToQBO(data) {
    const docType = currentDocument.type || currentDocument.documentType || 'general';
    
    let qbo = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    qbo += `<QBXML>\n`;
    qbo += `  <QBXMLMsgsRq onError="stopOnError">\n`;
    
    if (docType === 'invoice') {
        qbo += `    <InvoiceAddRq>\n`;
        qbo += `      <InvoiceAdd>\n`;
        qbo += `        <CustomerRef>\n`;
        qbo += `          <FullName>${data.vendor || 'Unknown'}</FullName>\n`;
        qbo += `        </CustomerRef>\n`;
        qbo += `        <TxnDate>${data.date || new Date().toISOString().split('T')[0]}</TxnDate>\n`;
        qbo += `        <RefNumber>${data.invoiceNumber || ''}</RefNumber>\n`;
        
        const items = data.items || data.lineItems || [];
        items.forEach(item => {
            qbo += `        <InvoiceLineAdd>\n`;
            qbo += `          <ItemRef>\n`;
            qbo += `            <FullName>${item.description || 'Item'}</FullName>\n`;
            qbo += `          </ItemRef>\n`;
            qbo += `          <Quantity>${item.quantity || 0}</Quantity>\n`;
            qbo += `          <Rate>${item.unit_price || item.unitPrice || 0}</Rate>\n`;
            qbo += `        </InvoiceLineAdd>\n`;
        });
        
        qbo += `      </InvoiceAdd>\n`;
        qbo += `    </InvoiceAddRq>\n`;
    }
    
    qbo += `  </QBXMLMsgsRq>\n`;
    qbo += `</QBXML>`;
    
    return qbo;
}

// ============================================
// 工具函數
// ============================================

function formatCurrency(amount) {
    const num = parseFloat(amount) || 0;
    return '$' + num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ============================================
// 頁面載入時初始化
// ============================================

// 等待 DOM 載入完成
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

