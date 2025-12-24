// ============================================
// VaultCaddy Document Detail Page
// 完全重寫的簡化版本
// ============================================

// 調試模式
const DEBUG_MODE = true; // ⚠️ 临时启用，方便调试

// 🌐 多語言翻譯支持
const translations = {
    'zh': {
        accountInfo: '${t('accountInfo')}',
        editable: '可編輯',
        bankName: '銀行名稱',
        accountNumber: '帳戶號碼',
        accountHolder: '帳戶持有人',
        currency: '貨幣',
        statementPeriod: '對帳單期間',
        statementDate: '對帳單日期',
        openingBalance: '期初餘額',
        closingBalance: '期末餘額',
        transactionRecords: '${t('transactionRecords')}',
        totalTransactions: '共 {count} 筆交易（顯示第 {start}-{end} 筆）',
        noTransactions: '無${t('transactionRecords')}',
        date: '日期',
        description: '描述',
        amount: '金額',
        balance: '餘額'
    },
    'en': {
        accountInfo: 'Account Information',
        editable: 'Editable',
        bankName: 'Bank Name',
        accountNumber: 'Account Number',
        accountHolder: 'Account Holder',
        currency: 'Currency',
        statementPeriod: 'Statement Period',
        statementDate: 'Statement Date',
        openingBalance: 'Opening Balance',
        closingBalance: 'Closing Balance',
        transactionRecords: 'Transaction Records',
        totalTransactions: 'Total {count} transactions (Showing {start}-{end})',
        noTransactions: 'No transactions',
        date: 'Date',
        description: 'Description',
        amount: 'Amount',
        balance: 'Balance'
    },
    'ja': {
        accountInfo: 'アカウント情報',
        editable: '編集可能',
        bankName: '銀行名',
        accountNumber: '口座番号',
        accountHolder: '口座名義人',
        currency: '通貨',
        statementPeriod: '明細期間',
        statementDate: '明細日付',
        openingBalance: '期首残高',
        closingBalance: '期末残高',
        transactionRecords: '取引記録',
        totalTransactions: '合計{count}件の取引（{start}-{end}件目を表示）',
        noTransactions: '取引記録なし',
        date: '日付',
        description: '説明',
        amount: '金額',
        balance: '残高'
    },
    'ko': {
        accountInfo: '계정 정보',
        editable: '편집 가능',
        bankName: '은행 이름',
        accountNumber: '계좌 번호',
        accountHolder: '계좌 소유자',
        currency: '통화',
        statementPeriod: '명세서 기간',
        statementDate: '명세서 날짜',
        openingBalance: '기초 잔액',
        closingBalance: '기말 잔액',
        transactionRecords: '거래 기록',
        totalTransactions: '총 {count}개 거래 ({start}-{end}번째 표시)',
        noTransactions: '거래 기록 없음',
        date: '날짜',
        description: '설명',
        amount: '금액',
        balance: '잔액'
    }
};

// 獲取當前語言
function getCurrentLanguage() {
    const pathname = window.location.pathname;
    if (pathname.includes('/en/')) return 'en';
    if (pathname.includes('/jp/')) return 'ja';
    if (pathname.includes('/kr/')) return 'ko';
    return 'zh';
}

// 獲取翻譯文本
function t(key, replacements = {}) {
    const lang = getCurrentLanguage();
    let text = translations[lang]?.[key] || translations['zh'][key] || key;
    
    // 替換佔位符 {key}
    Object.keys(replacements).forEach(key => {
        text = text.replace(`{${key}}`, replacements[key]);
    });
    
    return text;
}

// 全局變量（也暴露到 window 對象以便其他腳本訪問）
let currentDocument = null;
// 🔥 暴露為全局變量
Object.defineProperty(window, 'currentDocument', {
    get: function() { return currentDocument; },
    set: function(val) { currentDocument = val; }
});
let currentPageNumber = 1;
let totalPagesCount = 1;
let zoomLevel = 100;
let autoSaveTimeout = null;
let hasUnsavedChanges = false;

// ${t('transactionRecords')}分頁變量（圖3需求）
let currentTransactionPage = 1;
let transactionsPerPage = 10;
let totalTransactions = 0;

console.log('✅ ${t('transactionRecords')}分頁變量已初始化:', { currentTransactionPage, transactionsPerPage });

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

// ✅ 全局變量：多頁支持
window.currentPageIndex = 0;
window.pageImages = [];

async function displayPDFPreview() {
    console.log('📄 顯示 PDF 預覽');
    const pdfViewer = document.getElementById('pdfViewer');
    
    if (!currentDocument) {
        pdfViewer.innerHTML = '<div class="loading"><div class="loading-spinner"></div><div>無法載入文檔</div></div>';
        return;
    }
    
    console.log('📄 文檔對象完整內容:', JSON.stringify(currentDocument, null, 2));
    console.log('📄 文檔對象所有鍵:', Object.keys(currentDocument));
    
    // ✅ 檢查是否有多頁（imageUrls 數組）
    if (currentDocument.imageUrls && Array.isArray(currentDocument.imageUrls) && currentDocument.imageUrls.length > 0) {
        console.log(`📚 檢測到多頁文檔：${currentDocument.imageUrls.length} 頁`);
        window.pageImages = currentDocument.imageUrls;
        window.currentPageIndex = 0;
        renderMultiPageDocument();
        return;
    }
    
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
            <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                <!-- 圖片控制工具欄 - 固定在頂部 -->
                <div style="background: #2d3748; border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.2); position: sticky; top: 1rem; z-index: 100;">
                    <!-- 縮小 -->
                    <button onclick="zoomOut()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="縮小">
                        <i class="fas fa-search-minus" style="font-size: 1.25rem;"></i>
                    </button>
                    
                    <!-- 縮放比例顯示 -->
                    <span style="color: white; font-size: 0.875rem; min-width: 60px; text-align: center; font-weight: 600;" id="zoom-display">100%</span>
                    
                    <!-- 放大 -->
                    <button onclick="zoomIn()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="放大">
                        <i class="fas fa-search-plus" style="font-size: 1.25rem;"></i>
                    </button>
                    
                    <div style="width: 1px; height: 24px; background: #4a5568; margin: 0 0.25rem;"></div>
                    
                    <!-- 向左旋轉 -->
                    <button onclick="rotateLeft()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="向左旋轉">
                        <i class="fas fa-undo" style="font-size: 1.25rem;"></i>
                    </button>
                    
                    <!-- 向右旋轉 -->
                    <button onclick="rotateRight()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="向右旋轉">
                        <i class="fas fa-redo" style="font-size: 1.25rem;"></i>
                    </button>
                    
                    <div style="width: 1px; height: 24px; background: #4a5568; margin: 0 0.25rem;"></div>
                    
                    <!-- 上一頁 -->
                    <button onclick="previousPage()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="上一頁" disabled>
                        <i class="fas fa-chevron-left" style="font-size: 1.25rem;"></i>
                    </button>
                    
                    <!-- 頁數顯示 -->
                    <span style="color: white; font-size: 0.875rem; min-width: 80px; text-align: center;" id="page-display">1 of 1</span>
                    
                    <!-- 下一頁 -->
                    <button onclick="nextPage()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="下一頁" disabled>
                        <i class="fas fa-chevron-right" style="font-size: 1.25rem;"></i>
                    </button>
                </div>
                
            <!-- 圖片顯示容器 - 支持拖拽滑動 + 修復滾動 -->
            <div id="image-scroll-container" style="width: 100%; max-height: calc(100vh - 200px); overflow: auto; display: flex; justify-content: center; align-items: flex-start; min-height: 400px; cursor: grab; position: relative;">
                <div class="pdf-page" id="image-container" style="transform: scale(1) rotate(0deg); transition: transform 0.3s; transform-origin: top center; display: inline-block; margin: 0 auto;">
                    <img src="${imageUrl}" alt="Document Preview" 
                         style="max-width: 100%; height: auto; display: block; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); user-select: none;"
                         onerror="console.error('圖片載入失敗:', '${imageUrl}'); this.parentElement.innerHTML='<div style=\\'padding: 2rem; text-align: center; color: #6b7280;\\'>無法載入預覽<br><small style=\\'color: #9ca3af; font-size: 0.75rem; word-break: break-all;\\'>URL: ${imageUrl}</small></div>'"
                         draggable="false">
                </div>
            </div>
            </div>
        `;
        
        // 初始化控制變量
        window.currentZoom = 100;
        window.currentRotation = 0;
        
        // 初始化拖拽滑動功能
        setTimeout(() => initImageDragScroll(), 100);
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
// 多頁文檔渲染和導航
// ============================================

function renderMultiPageDocument() {
    const pdfViewer = document.getElementById('pdfViewer');
    const currentPage = window.currentPageIndex + 1;
    const totalPages = window.pageImages.length;
    const currentImageUrl = window.pageImages[window.currentPageIndex];
    
    console.log(`📖 渲染第 ${currentPage}/${totalPages} 頁`);
    
    pdfViewer.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            <!-- 圖片控制工具欄 - 固定在頂部 -->
            <div style="background: #2d3748; border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.2); position: sticky; top: 1rem; z-index: 100;">
                <!-- 縮小 -->
                <button onclick="zoomOut()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="縮小">
                    <i class="fas fa-search-minus" style="font-size: 1.25rem;"></i>
                </button>
                
                <!-- 縮放比例顯示 -->
                <span style="color: white; font-size: 0.875rem; min-width: 60px; text-align: center; font-weight: 600;" id="zoom-display">100%</span>
                
                <!-- 放大 -->
                <button onclick="zoomIn()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="放大">
                    <i class="fas fa-search-plus" style="font-size: 1.25rem;"></i>
                </button>
                
                <div style="width: 1px; height: 24px; background: #4a5568; margin: 0 0.25rem;"></div>
                
                <!-- 向左旋轉 -->
                <button onclick="rotateLeft()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="向左旋轉">
                    <i class="fas fa-undo" style="font-size: 1.25rem;"></i>
                </button>
                
                <!-- 向右旋轉 -->
                <button onclick="rotateRight()" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="向右旋轉">
                    <i class="fas fa-redo" style="font-size: 1.25rem;"></i>
                </button>
                
                <div style="width: 1px; height: 24px; background: #4a5568; margin: 0 0.25rem;"></div>
                
                <!-- 上一頁 -->
                <button onclick="previousPage()" id="prevPageBtn" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s; ${currentPage === 1 ? 'opacity: 0.3; cursor: not-allowed;' : ''}" ${currentPage === 1 ? 'disabled' : ''} onmouseover="if(!this.disabled) this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="上一頁">
                    <i class="fas fa-chevron-left" style="font-size: 1.25rem;"></i>
                </button>
                
                <!-- 頁數顯示 -->
                <span style="color: white; font-size: 0.875rem; min-width: 80px; text-align: center;" id="page-display">${currentPage} of ${totalPages}</span>
                
                <!-- 下一頁 -->
                <button onclick="nextPage()" id="nextPageBtn" style="background: transparent; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; transition: background 0.2s; ${currentPage === totalPages ? 'opacity: 0.3; cursor: not-allowed;' : ''}" ${currentPage === totalPages ? 'disabled' : ''} onmouseover="if(!this.disabled) this.style.background='#4a5568'" onmouseout="this.style.background='transparent'" title="下一頁">
                    <i class="fas fa-chevron-right" style="font-size: 1.25rem;"></i>
                </button>
            </div>
            
            <!-- 圖片顯示容器 - 支持拖拽滑動 + 修復滾動 -->
            <div id="image-scroll-container" style="width: 100%; max-height: calc(100vh - 200px); overflow: auto; display: flex; justify-content: center; align-items: flex-start; min-height: 400px; cursor: grab; position: relative;">
                <div class="pdf-page" id="image-container" style="transform: scale(1) rotate(0deg); transition: transform 0.3s; transform-origin: top center; display: inline-block; margin: 0 auto;">
                    <img src="${currentImageUrl}" alt="Document Preview - Page ${currentPage}" 
                         style="max-width: 100%; height: auto; display: block; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); user-select: none;"
                         onerror="console.error('圖片載入失敗:', '${currentImageUrl}'); this.parentElement.innerHTML='<div style=\\'padding: 2rem; text-align: center; color: #6b7280;\\'>無法載入第 ${currentPage} 頁</div>'"
                         draggable="false">
                </div>
            </div>
        </div>
    `;
    
    // 初始化控制變量
    window.currentZoom = 100;
    window.currentRotation = 0;
    
    // 初始化拖拽滑動功能
    setTimeout(() => initImageDragScroll(), 100);
}

// 上一頁（兩個函數名都支持）
window.previousPage = window.prevPage = function() {
    if (window.currentPageIndex > 0) {
        window.currentPageIndex--;
        console.log(`⬅️ 上一頁: ${window.currentPageIndex + 1}/${window.pageImages.length}`);
        renderMultiPageDocument();
    }
};

// 下一頁
window.nextPage = function() {
    if (window.currentPageIndex < window.pageImages.length - 1) {
        window.currentPageIndex++;
        console.log(`➡️ 下一頁: ${window.currentPageIndex + 1}/${window.pageImages.length}`);
        renderMultiPageDocument();
    }
};

// ============================================
// 圖片拖拽滑動功能
// ============================================

function initImageDragScroll() {
    const scrollContainer = document.getElementById('image-scroll-container');
    if (!scrollContainer) {
        console.log('⚠️ 未找到圖片滾動容器');
        return;
    }
    
    let isDragging = false;
    let startX, startY;
    let scrollLeft, scrollTop;
    
    // 鼠標按下
    scrollContainer.addEventListener('mousedown', (e) => {
        // 只在放大時啟用拖拽（縮放比例 > 100%）
        if (window.currentZoom <= 100) return;
        
        isDragging = true;
        scrollContainer.style.cursor = 'grabbing';
        
        startX = e.pageX - scrollContainer.offsetLeft;
        startY = e.pageY - scrollContainer.offsetTop;
        scrollLeft = scrollContainer.scrollLeft;
        scrollTop = scrollContainer.scrollTop;
        
        // 禁用過渡動畫以獲得更流暢的拖拽體驗
        const imageContainer = document.getElementById('image-container');
        if (imageContainer) {
            imageContainer.style.transition = 'none';
        }
    });
    
    // 鼠標移動
    scrollContainer.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        
        e.preventDefault();
        
        const x = e.pageX - scrollContainer.offsetLeft;
        const y = e.pageY - scrollContainer.offsetTop;
        
        const walkX = (x - startX) * 1.5; // 拖拽速度倍數
        const walkY = (y - startY) * 1.5;
        
        scrollContainer.scrollLeft = scrollLeft - walkX;
        scrollContainer.scrollTop = scrollTop - walkY;
    });
    
    // 鼠標釋放
    scrollContainer.addEventListener('mouseup', () => {
        isDragging = false;
        scrollContainer.style.cursor = window.currentZoom > 100 ? 'grab' : 'default';
        
        // 恢復過渡動畫
        const imageContainer = document.getElementById('image-container');
        if (imageContainer) {
            imageContainer.style.transition = 'transform 0.3s';
        }
    });
    
    // 鼠標離開容器
    scrollContainer.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
            scrollContainer.style.cursor = window.currentZoom > 100 ? 'grab' : 'default';
            
            // 恢復過渡動畫
            const imageContainer = document.getElementById('image-container');
            if (imageContainer) {
                imageContainer.style.transition = 'transform 0.3s';
            }
        }
    });
    
    console.log('✅ 圖片拖拽滑動功能已初始化');
}

// ============================================
// 圖片控制函數 - 全局可訪問
// ============================================

window.zoomIn = function() {
    if (window.currentZoom < 200) {
        window.currentZoom += 25;
        updateImageTransform();
    }
};

window.zoomOut = function() {
    if (window.currentZoom > 25) {
        window.currentZoom -= 25;
        updateImageTransform();
    }
};

window.rotateLeft = function() {
    window.currentRotation -= 90;
    updateImageTransform();
};

window.rotateRight = function() {
    window.currentRotation += 90;
    updateImageTransform();
};

// ✅ 翻頁功能已在上方實現（lines 420-435），此處刪除重複定義

function updateImageTransform() {
    const container = document.getElementById('image-container');
    const zoomDisplay = document.getElementById('zoom-display');
    const scrollContainer = document.getElementById('image-scroll-container');
    
    if (container) {
        container.style.transform = `scale(${window.currentZoom / 100}) rotate(${window.currentRotation}deg)`;
    }
    
    if (zoomDisplay) {
        zoomDisplay.textContent = `${window.currentZoom}%`;
    }
    
    // 更新游標樣式
    if (scrollContainer) {
        scrollContainer.style.cursor = window.currentZoom > 100 ? 'grab' : 'default';
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
    
    // 發票詳情卡片（桌面版2列，手機版1列）
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-file-invoice" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                發票詳情
            </h3>
            <div class="invoice-details-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
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
            <style>
                /* 手機版改為1列 */
                @media (max-width: 768px) {
                    .invoice-details-grid {
                        grid-template-columns: 1fr !important;
                    }
                }
            </style>
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
                <span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;">(${t('editable')})</span>
            </h3>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th>代碼</th>
                        <th>${t('description')}</th>
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
    console.log('📊 原始數據:', JSON.stringify(data, null, 2));
    
    // 🔍 DEBUG - 详细诊断交易记录提取
    console.log('🔍 DEBUG - 完整数据结构:', data);
    console.log('🔍 DEBUG - processedData:', currentDocument?.processedData);
    console.log('🔍 DEBUG - 所有可能的transactions字段:');
    console.log('   data.transactions:', data.transactions);
    console.log('   data.transaction:', data.transaction);
    console.log('   data.items:', data.items);
    console.log('   currentDocument.transactions:', currentDocument?.transactions);
    console.log('🔍 DEBUG - currentDocument完整内容:', currentDocument);
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    // ✅ 提取${t('accountInfo')}（支持多種字段名稱 + 增強 Fallback）
    const bankName = data.bankName || 
                     data.bank_name || 
                     data.bank || 
                     data.bankname ||
                     '—';
    
    const accountNumber = data.accountNumber || 
                          data.account_number || 
                          data.accountNo || 
                          data.account_no ||
                          data.accountnum ||
                          '—';
    
    // ✅ 提取對帳單日期（優先使用 statementDate，否則從 statement_period 提取）
    let statementDate = data.statementDate || 
                        data.statement_date || 
                        data.date ||
                        data.statementdate ||
                        '';
    
    // 如果沒有單獨的日期，從 statement_period 提取結束日期
    if (!statementDate && (data.statementPeriod || data.statement_period)) {
        const period = data.statementPeriod || data.statement_period;
        const match = period.match(/to\s+(\d{2}\/\d{2}\/\d{4})/);
        if (match) {
            // 轉換 MM/DD/YYYY 為 YYYY-MM-DD
            const [month, day, year] = match[1].split('/');
            statementDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        }
    }
    
    if (!statementDate) statementDate = '—';
    
    const openingBalance = data.openingBalance || 
                           data.opening_balance || 
                           data.startBalance || 
                           data.start_balance ||
                           0;
    
    const closingBalance = data.closingBalance || 
                           data.closing_balance || 
                           data.endBalance || 
                           data.end_balance ||
                           data.finalBalance ||
                           data.final_balance ||
                           0;
    
    // ✅ 新增欄位：帳戶持有人、對帳單期間、貨幣
    const accountHolder = data.accountHolder ||
                          data.account_holder ||
                          data.holder ||
                          '—';
    
    const statementPeriod = data.statementPeriod ||
                            data.statement_period ||
                            '';
    
    const currency = data.currency || 'HKD';
    
    // ✅ 調試日誌
    console.log('🔍 提取的數據:');
    console.log('   銀行名稱:', bankName);
    console.log('   帳戶號碼:', accountNumber);
    console.log('   帳戶持有人:', accountHolder);
    console.log('   對帳單日期:', statementDate);
    console.log('   對帳單期間:', statementPeriod);
    console.log('   期初餘額:', openingBalance);
    console.log('   期末餘額:', closingBalance);
    console.log('   貨幣:', currency);
    
    // ✅ 帳戶詳情（可編輯）- 新增：帳戶持有人、對帳單期間、期初餘額、貨幣
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-university" style="color: #10b981; margin-right: 0.5rem;"></i>
                ${t('accountInfo')}
                <span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;">(${t('editable')})</span>
            </h3>
            <div class="bank-info-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('bankName')}</label>
                    <input type="text" id="bankName" value="${bankName}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('accountNumber')}</label>
                    <input type="text" id="accountNumber" value="${accountNumber}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('accountHolder')}</label>
                    <input type="text" id="accountHolder" value="${accountHolder}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('currency')}</label>
                    <input type="text" id="currency" value="${currency}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('statementPeriod')}</label>
                    <input type="text" id="statementPeriod" value="${statementPeriod}" 
                           onchange="autoSaveBankStatementDetails()"
                           placeholder="例如：2025-02-22 to 2025-03-22"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('statementDate')}</label>
                    <input type="date" id="statementDate" value="${statementDate}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white; max-width: 100%; overflow: hidden; text-overflow: ellipsis;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('openingBalance')}</label>
                    <input type="text" id="openingBalance" value="${formatCurrency(openingBalance)}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #3b82f6; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('closingBalance')}</label>
                    <input type="text" id="closingBalance" value="${formatCurrency(closingBalance)}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #10b981; background: white;">
                </div>
            </div>
            <style>
                /* ✅ 手機版：${t('accountInfo')}改為1列顯示 */
                @media (max-width: 768px) {
                    .bank-info-grid {
                        grid-template-columns: 1fr !important;
                    }
                    
                    /* ✅ 修復日期輸入框超出問題 */
                    input[type="date"] {
                        max-width: 100% !important;
                        overflow: hidden !important;
                    }
                }
            </style>
        </div>
        
        <!-- ✅ 其他賬戶（可展開/摺疊）-->
        <div class="bank-details-card" style="margin-top: 1rem;" id="otherAccountsCard">
            <div style="display: flex; align-items: center; justify-content: space-between; cursor: pointer;" onclick="toggleOtherAccounts()">
                <h3 class="card-title" style="margin: 0;">
                    <i class="fas fa-credit-card" style="color: #8b5cf6; margin-right: 0.5rem;"></i>
                    其他賬戶
                    <span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;" id="otherAccountsCount">(0)</span>
                </h3>
                <i class="fas fa-chevron-down" id="otherAccountsChevron" style="color: #6b7280; transition: transform 0.3s;"></i>
            </div>
            <div id="otherAccountsContent" style="display: none; margin-top: 1rem;">
                <div style="color: #6b7280; text-align: center; padding: 2rem;">
                    暫無其他賬戶信息
                </div>
            </div>
        </div>
    `;
    
    // ✅ 提取其他賬戶信息（從 DeepSeek 數據中）
    extractOtherAccounts(data);
    
    // ✅ 交易列表（支持多種字段名稱）
    const transactions = data.transactions || 
                         data.transaction || 
                         data.items ||
                         currentDocument.transactions || 
                         [];
    
    console.log('   交易數量:', transactions.length);
    
    // ✅ 設置全局變量用於分頁
    totalTransactions = transactions.length;
    const totalPages = Math.ceil(totalTransactions / transactionsPerPage);
    
    // ✅ 計算當前頁的${t('transactionRecords')}
    const startIndex = (currentTransactionPage - 1) * transactionsPerPage;
    const endIndex = Math.min(startIndex + transactionsPerPage, totalTransactions);
    const currentPageTransactions = transactions.slice(startIndex, endIndex);
    
    let transactionsHTML = '';
    currentPageTransactions.forEach((tx, pageIndex) => {
        const actualIndex = startIndex + pageIndex; // 實際在完整數組中的索引
        const amount = parseFloat(tx.amount || 0);
        const balance = parseFloat(tx.balance || 0);
        
        // ✅ 判斷交易類型（根據金額正負）
        const isIncome = amount >= 0;
        const amountSign = isIncome ? '+' : '-';
        const amountColor = isIncome ? '#10b981' : '#ef4444';
        const amountValue = Math.abs(amount);
        
        // ✅ 優化描述顯示（保留完整名稱）
        const description = tx.description || tx.details || tx.memo || '—';
        
        transactionsHTML += `
            <tr data-index="${actualIndex}">
                <td class="checkbox-cell">
                    <input type="checkbox" 
                           class="transaction-checkbox" 
                           data-index="${actualIndex}"
                           ${tx.checked ? 'checked' : ''}
                           onchange="handleTransactionCheckbox(${actualIndex}, this.checked)">
                </td>
                <td contenteditable="true" class="editable-cell" data-field="date" style="min-width: 100px;">${tx.date || '—'}</td>
                <td contenteditable="true" class="editable-cell" data-field="description" style="min-width: 200px;">${description}</td>
                <td class="amount-cell" style="position: relative;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <button onclick="toggleTransactionType(${actualIndex})" 
                                style="background: ${isIncome ? '#10b981' : '#ef4444'}; color: white; border: none; border-radius: 4px; padding: 0.25rem 0.5rem; cursor: pointer; font-weight: 600; font-size: 0.875rem; transition: all 0.2s;"
                                onmouseover="this.style.opacity='0.8'" 
                                onmouseout="this.style.opacity='1'"
                                title="點擊切換收入/支出">
                            ${amountSign}
                        </button>
                        <input type="text" 
                               value="${amountValue.toFixed(2)}" 
                               class="editable-amount" 
                               data-index="${actualIndex}"
                               data-field="amount"
                               style="border: 1px solid #e5e7eb; border-radius: 4px; padding: 0.25rem 0.5rem; text-align: right; color: ${amountColor}; font-weight: 600; width: 100px;"
                               onchange="updateTransactionAmount(${actualIndex}, this.value, ${isIncome})">
                    </div>
                </td>
                <td contenteditable="true" class="editable-cell" data-field="balance" style="text-align: right; font-weight: 600; color: #3b82f6;">${formatCurrency(balance)}</td>
            </tr>
        `;
    });
    
    // ✅ 分頁控制器 HTML
    const paginationHTML = totalPages > 1 ? `
        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-top: 1rem; padding: 1rem; border-top: 1px solid #e5e7eb;">
            <button onclick="changeTransactionPage(${currentTransactionPage - 1})" 
                    ${currentTransactionPage === 1 ? 'disabled' : ''}
                    style="background: #f3f4f6; border: 1px solid #d1d5db; color: #374151; padding: 0.5rem 1rem; border-radius: 6px; cursor: ${currentTransactionPage === 1 ? 'not-allowed' : 'pointer'}; opacity: ${currentTransactionPage === 1 ? '0.5' : '1'}; transition: all 0.2s;"
                    onmouseover="if(${currentTransactionPage !== 1}) this.style.background='#e5e7eb'"
                    onmouseout="this.style.background='#f3f4f6'">
                <i class="fas fa-chevron-left"></i>
            </button>
            <span style="color: #6b7280; font-size: 0.875rem; font-weight: 500;">
                ${currentTransactionPage} of ${totalPages}
            </span>
            <button onclick="changeTransactionPage(${currentTransactionPage + 1})" 
                    ${currentTransactionPage === totalPages ? 'disabled' : ''}
                    style="background: #f3f4f6; border: 1px solid #d1d5db; color: #374151; padding: 0.5rem 1rem; border-radius: 6px; cursor: ${currentTransactionPage === totalPages ? 'not-allowed' : 'pointer'}; opacity: ${currentTransactionPage === totalPages ? '0.5' : '1'}; transition: all 0.2s;"
                    onmouseover="if(${currentTransactionPage !== totalPages}) this.style.background='#e5e7eb'"
                    onmouseout="this.style.background='#f3f4f6'">
                <i class="fas fa-chevron-right"></i>
            </button>
        </div>
    ` : '';
    
    dataSection.innerHTML = `
        <div class="transactions-section">
            <div class="transactions-header">
                <h3 class="transactions-title">
                    <i class="fas fa-exchange-alt" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                    ${t('transactionRecords')}
                </h3>
            </div>
            <div class="transactions-info">
                ${t('totalTransactions', {count: transactions.length, start: startIndex + 1, end: endIndex})}
            </div>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th class="checkbox-cell"><input type="checkbox"></th>
                        <th>${t('date')}</th>
                        <th>${t('description')}</th>
                        <th>${t('amount')}</th>
                        <th>${t('balance')}</th>
                    </tr>
                </thead>
                <tbody>
                    ${transactionsHTML || '<tr><td colspan="5" style="text-align: center; padding: 2rem; color: #6b7280;">無${t('transactionRecords')}</td></tr>'}
                </tbody>
            </table>
            ${paginationHTML}
        </div>
    `;
    
    // ✅ 設置${t('transactionRecords')}編輯監聽器
    setTimeout(() => setupTransactionEditListeners(), 100);
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
// 自動保存快捷函數
// ============================================

// ✅ 銀行對帳單自動保存
window.autoSaveBankStatementDetails = function() {
    markAsChanged();
};

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
    } else if (docType === 'bank_statement' || docType === 'bank_statements') {
        // ✅ 如果是銀行對帳單，獲取帳戶詳情（包括新增欄位）
        const bankName = document.getElementById('bankName')?.value;
        const accountNumber = document.getElementById('accountNumber')?.value;
        const accountHolder = document.getElementById('accountHolder')?.value;
        const currency = document.getElementById('currency')?.value;
        const statementPeriod = document.getElementById('statementPeriod')?.value;
        const statementDate = document.getElementById('statementDate')?.value;
        const openingBalance = document.getElementById('openingBalance')?.value;
        const closingBalance = document.getElementById('closingBalance')?.value;
        
        if (bankName || accountNumber || accountHolder || statementDate || closingBalance) {
            currentDocument.processedData = {
                ...currentDocument.processedData,
                bankName: bankName,
                accountNumber: accountNumber,
                accountHolder: accountHolder,
                currency: currency,
                statementPeriod: statementPeriod,
                statementDate: statementDate,
                openingBalance: parseFloat(openingBalance?.replace(/[^0-9.-]+/g, '')) || 0,
                closingBalance: parseFloat(closingBalance?.replace(/[^0-9.-]+/g, '')) || 0
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
    // 獲取所有發票字段
    const invoiceNumber = document.getElementById('invoiceNumber')?.value;
    const invoiceDate = document.getElementById('invoiceDate')?.value;
    const vendor = document.getElementById('vendor')?.value;
    const totalAmount = document.getElementById('totalAmount')?.value;
    
    // 更新 currentDocument
    if (currentDocument && currentDocument.processedData) {
        currentDocument.processedData = {
            ...currentDocument.processedData,
            invoiceNumber: invoiceNumber,
            invoice_number: invoiceNumber,
            date: invoiceDate,
            invoice_date: invoiceDate,
            vendor: vendor,
            supplier: vendor,
            total: totalAmount,
            totalAmount: totalAmount
        };
    }
    
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

// ✅ 頁面導航函數已移至上方（window.prevPage 和 window.nextPage）

// ============================================
// 導出功能
// ============================================

function toggleExportMenu(event) {
    if (event) event.stopPropagation();
    const menu = document.getElementById('exportMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

// 點擊其他地方關閉菜單
document.addEventListener('click', function(event) {
    const menu = document.getElementById('exportMenu');
    const exportBtn = document.querySelector('[onclick*="toggleExportMenu"]');
    
    // 如果點擊的是菜單內部或按鈕，不關閉菜單
    if (menu && menu.style.display === 'block') {
        if (!menu.contains(event.target) && (!exportBtn || !exportBtn.contains(event.target))) {
            menu.style.display = 'none';
        }
    }
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
            
            case 'bank_statement_csv':
                // 標準銀行對帳單 CSV
                if (window.BankStatementExport) {
                    content = window.BankStatementExport.generateBankStatementCSV([currentDocument]);
                } else {
                    content = exportToCSV(data);
                }
                mimeType = 'text/csv';
                fileExtension = 'csv';
                break;
            
            case 'xero_csv':
                // Xero CSV 格式
                if (window.BankStatementExport) {
                    content = window.BankStatementExport.generateXeroCSV([currentDocument]);
                } else {
                    alert('Xero 導出模塊未載入');
                    return;
                }
                mimeType = 'text/csv';
                fileExtension = 'csv';
                break;
            
            case 'quickbooks_csv':
                // QuickBooks CSV 格式
                if (window.BankStatementExport) {
                    content = window.BankStatementExport.generateQuickBooksCSV([currentDocument]);
                } else {
                    alert('QuickBooks 導出模塊未載入');
                    return;
                }
                mimeType = 'text/csv';
                fileExtension = 'csv';
                break;
            
            case 'invoice_summary_csv':
                // 發票標準 CSV（總數）
                if (window.InvoiceExport) {
                    content = window.InvoiceExport.generateStandardInvoiceCSV([currentDocument]);
                } else {
                    content = exportToCSV(data);
                }
                mimeType = 'text/csv';
                fileExtension = 'csv';
                break;
            
            case 'invoice_detailed_csv':
                // 發票完整交易數據 CSV
                if (window.InvoiceExport) {
                    content = window.InvoiceExport.generateDetailedInvoiceCSV([currentDocument]);
                } else {
                    content = exportToCSV(data);
                }
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
// ${t('transactionRecords')}分頁函數
// ============================================

/**
 * 切換${t('transactionRecords')}頁面（圖3需求）
 */
window.changeTransactionPage = function(newPage) {
    console.log('🔄 changeTransactionPage 被調用:', { 
        newPage, 
        currentTransactionPage, 
        totalTransactions, 
        transactionsPerPage 
    });
    
    const totalPages = Math.ceil(totalTransactions / transactionsPerPage);
    
    if (newPage < 1 || newPage > totalPages) {
        console.warn(`⚠️ 頁碼超出範圍: ${newPage} (有效範圍: 1-${totalPages})`);
        return; // 超出範圍，不處理
    }
    
    currentTransactionPage = newPage;
    console.log(`✅ 切換到${t('transactionRecords')}第 ${newPage} 頁（共 ${totalPages} 頁）`);
    
    // 重新渲染${t('transactionRecords')}
    if (currentDocument && currentDocument.processedData) {
        displayBankStatementContent(currentDocument.processedData);
        
        // ✅ 滾動到${t('transactionRecords')}頂部
        const transactionsSection = document.querySelector('.transactions-section');
        if (transactionsSection) {
            transactionsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } else {
        console.error('❌ 無法重新渲染：currentDocument 或 processedData 不存在');
    }
};

// ============================================
// ${t('transactionRecords')}編輯函數
// ============================================

// ✅ 切換交易類型（+/-）
function toggleTransactionType(index) {
    console.log(`🔄 切換交易 ${index} 的類型`);
    
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    const transaction = currentDocument.processedData.transactions[index];
    if (!transaction) {
        console.error(`❌ 找不到交易 ${index}`);
        return;
    }
    
    // 切換金額正負
    transaction.amount = -parseFloat(transaction.amount || 0);
    
    // 更新 UI
    displayDocumentContent();
    
    // 標記為有未保存更改
    markAsChanged();
}

// ✅ 更新交易金額
function updateTransactionAmount(index, value, wasIncome) {
    console.log(`💰 更新交易 ${index} 的金額: ${value}`);
    
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    const transaction = currentDocument.processedData.transactions[index];
    if (!transaction) {
        console.error(`❌ 找不到交易 ${index}`);
        return;
    }
    
    // 解析金額並保持正負符號
    const numValue = parseFloat(value) || 0;
    transaction.amount = wasIncome ? numValue : -numValue;
    
    // 標記為有未保存更改
    markAsChanged();
}

// ✅ 處理${t('transactionRecords')}複選框變化
window.handleTransactionCheckbox = function(index, checked) {
    console.log(`✅ 交易 ${index} 複選框變化: ${checked}`);
    
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    const transaction = currentDocument.processedData.transactions[index];
    if (!transaction) {
        console.error(`❌ 找不到交易 ${index}`);
        return;
    }
    
    // 更新交易的 checked 狀態
    transaction.checked = checked;
    
    // 標記為有未保存更改並自動保存
    markAsChanged();
    
    console.log(`💾 交易 ${index} 已標記為 ${checked ? '已核對' : '未核對'}`);
};

// ✅ 監聽可編輯單元格的變化
function setupTransactionEditListeners() {
    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('blur', function() {
            const row = this.closest('tr');
            const index = parseInt(row.dataset.index);
            const field = this.dataset.field;
            const value = this.textContent.trim();
            
            if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
                return;
            }
            
            const transaction = currentDocument.processedData.transactions[index];
            if (!transaction) {
                return;
            }
            
            // 更新對應欄位
            if (field === 'date') {
                transaction.date = value;
            } else if (field === 'description') {
                transaction.description = value;
            } else if (field === 'balance') {
                transaction.balance = parseFloat(value.replace(/[^0-9.-]+/g, '')) || 0;
            }
            
            // 標記為有未保存更改
            markAsChanged();
        });
    });
}

// ============================================
// 其他賬戶功能
// ============================================

// ✅ 切換其他賬戶顯示
function toggleOtherAccounts() {
    const content = document.getElementById('otherAccountsContent');
    const chevron = document.getElementById('otherAccountsChevron');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        chevron.style.transform = 'rotate(180deg)';
    } else {
        content.style.display = 'none';
        chevron.style.transform = 'rotate(0deg)';
    }
}

// ✅ 提取其他賬戶信息（從 ACCOUNT SUMMARY）
function extractOtherAccounts(data) {
    console.log('🔍 提取其他賬戶信息...');
    
    // 從 DeepSeek 數據中提取其他賬戶
    const otherAccounts = data.otherAccounts || data.creditServices || data.linkedAccounts || [];
    const cardAccounts = data.cardAccounts || data.cards || [];
    
    const content = document.getElementById('otherAccountsContent');
    const countSpan = document.getElementById('otherAccountsCount');
    
    if (otherAccounts.length === 0 && cardAccounts.length === 0) {
        console.log('   ℹ️ 沒有找到其他賬戶信息');
        countSpan.textContent = '(0)';
        content.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 2rem;">暫無其他賬戶信息</div>';
        return;
    }
    
    let accountsHTML = '';
    let totalCount = 0;
    
    // ✅ 信貸服務（個人貸款、按揭等）
    if (otherAccounts.length > 0) {
        accountsHTML += `
            <div style="margin-bottom: 1rem;">
                <h4 style="font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.75rem;">
                    <i class="fas fa-hand-holding-usd" style="color: #f59e0b; margin-right: 0.5rem;"></i>
                    信貸服務
                </h4>
                <div style="display: grid; gap: 0.75rem;">
        `;
        
        otherAccounts.forEach(account => {
            totalCount++;
            const accountType = account.type || account.accountType || '個人貸款';
            const accountNumber = account.accountNumber || account.number || '—';
            const balance = parseFloat(account.balance || 0);
            const balanceColor = balance < 0 ? '#ef4444' : '#10b981';
            
            accountsHTML += `
                <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; border: 1px solid #fbbf24;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #78350f;">${accountType}</div>
                            <div style="font-size: 0.875rem; color: #92400e; margin-top: 0.25rem;">
                                ${accountNumber.length > 12 ? accountNumber.slice(-12) : accountNumber}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.875rem; color: #92400e;">餘額</div>
                            <div style="font-weight: 600; font-size: 1.125rem; color: ${balanceColor};">
                                ${formatCurrency(balance)}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        accountsHTML += `
                </div>
            </div>
        `;
    }
    
    // ✅ 信用卡
    if (cardAccounts.length > 0) {
        accountsHTML += `
            <div style="margin-bottom: 1rem;">
                <h4 style="font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.75rem;">
                    <i class="fas fa-credit-card" style="color: #8b5cf6; margin-right: 0.5rem;"></i>
                    信用卡
                </h4>
                <div style="display: grid; gap: 0.75rem;">
        `;
        
        cardAccounts.forEach(card => {
            totalCount++;
            const cardType = card.type || card.cardType || 'VISA';
            const cardNumber = card.cardNumber || card.number || '—';
            const balance = parseFloat(card.balance || 0);
            const balanceColor = balance < 0 ? '#ef4444' : '#10b981';
            
            accountsHTML += `
                <div style="background: #ede9fe; padding: 1rem; border-radius: 8px; border: 1px solid #a78bfa;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #5b21b6;">${cardType}</div>
                            <div style="font-size: 0.875rem; color: #6b21a8; margin-top: 0.25rem;">
                                **** **** **** ${cardNumber.slice(-4)}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.875rem; color: #6b21a8;">欠款</div>
                            <div style="font-weight: 600; font-size: 1.125rem; color: ${balanceColor};">
                                ${formatCurrency(balance)}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        accountsHTML += `
                </div>
            </div>
        `;
    }
    
    content.innerHTML = accountsHTML;
    countSpan.textContent = `(${totalCount})`;
    
    console.log(`   ✅ 找到 ${totalCount} 個其他賬戶`);
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

