// ============================================
// VaultCaddy Document Detail Page
// 完全重寫的簡化版本
// ============================================

console.log('📦 document-detail-new.js 已加載 [v20260125]');

// 調試模式
const DEBUG_MODE = false;

// ============================================
// 多語言支持
// ============================================

// 獲取當前語言
function getCurrentLanguage() {
    const path = window.location.pathname;
    if (path.includes('/en/')) return 'en';
    if (path.includes('/jp/')) return 'ja';
    if (path.includes('/kr/')) return 'ko';
    return 'zh-TW'; // 默認中文
}

// 翻譯文本
const i18n = {
    'zh-TW': {
        verified: '已核對',
        date: '日期',
        type: '類型',
        description: '描述',
        payee: '收款人',
        reference: '參考編號',
        checkNumber: '支票號碼',
        category: '分類',
        memo: '備注',
        reconciled: '已對賬',
        unreconciled: '未對賬',
        attachment: '附件',
        amount: '金額',
        balance: '餘額',
        bankCode: '銀行代碼',
        branchName: '分行地址',
        accountType: '賬戶類型',
        account_info: '帳戶信息',
        editable: '(可編輯)',
        bank_name: '銀行名稱',
        account_number: '帳戶號碼',
        account_holder: '帳戶持有人',
        statement_period: '對帳單期間',
        statement_date: '對帳單日期',
        statement_date_placeholder: 'YYYY-MM-DD',
        opening_balance: '期初餘額',
        closing_balance: '期末餘額',
        currency: '貨幣',
        transactions: '交易記錄',
        total_transactions: '共 {count} 筆交易（顯示第 {start}-{end} 筆）',
        no_transactions: '無交易記錄',
        // 發票相關翻譯
        invoice_details: '發票詳情',
        invoice_number: '發票號碼',
        vendor: '供應商',
        total_amount: '總金額',
        line_items: '項目明細',
        code: '代碼',
        quantity: '數量',
        unit: '單位',
        unit_price: '單價',
        unit_default: '件',
        no_items: '無項目數據',
        // 分类相关
        actions: '操作',
        uncategorized: '未分類',
        income_categories: '收入類別',
        expense_categories: '支出類別',
        cat_salary: '工資',
        cat_sales: '銷售收入',
        cat_interest: '利息收入',
        cat_other_income: '其他收入',
        cat_office: '辦公費用',
        cat_transport: '交通費用',
        cat_meal: '餐飲費用',
        cat_utilities: '水電費',
        cat_rent: '租金',
        cat_salary_expense: '工資支出',
        cat_marketing: '營銷費用',
        cat_supplies: '耗材',
        cat_other_expense: '其他支出',
        income_click_to_expense: '收入（點擊改為支出）',
        expense_click_to_income: '支出（點擊改為收入）'
    },
    'en': {
        verified: 'Verified',
        date: 'Date',
        type: 'Type',
        description: 'Description',
        payee: 'Payee',
        reference: 'Reference',
        checkNumber: 'Check #',
        category: 'Category',
        memo: 'Memo',
        reconciled: 'Reconciled',
        unreconciled: 'Unreconciled',
        attachment: 'Attach',
        amount: 'Amount',
        balance: 'Balance',
        bankCode: 'Bank Code',
        branchName: 'Branch Address',
        accountType: 'Account Type',
        account_info: 'Account Information',
        editable: '(Editable)',
        bank_name: 'Bank Name',
        account_number: 'Account Number',
        account_holder: 'Account Holder',
        statement_period: 'Statement Period',
        statement_date: 'Statement Date',
        statement_date_placeholder: 'YYYY-MM-DD',
        opening_balance: 'Opening Balance',
        closing_balance: 'Closing Balance',
        currency: 'Currency',
        transactions: 'Transactions',
        total_transactions: '{count} transactions total (showing {start}-{end})',
        no_transactions: 'No transactions',
        // Invoice translations
        invoice_details: 'Invoice Details',
        invoice_number: 'Invoice Number',
        vendor: 'Vendor',
        total_amount: 'Total Amount',
        line_items: 'Line Items',
        code: 'Code',
        quantity: 'Quantity',
        unit: 'Unit',
        unit_price: 'Unit Price',
        unit_default: 'pcs',
        no_items: 'No item data',
        // Category related
        actions: 'Actions',
        uncategorized: 'Uncategorized',
        income_categories: 'Income Categories',
        expense_categories: 'Expense Categories',
        cat_salary: 'Salary',
        cat_sales: 'Sales Revenue',
        cat_interest: 'Interest Income',
        cat_other_income: 'Other Income',
        cat_office: 'Office Expenses',
        cat_transport: 'Transportation',
        cat_meal: 'Meals & Entertainment',
        cat_utilities: 'Utilities',
        cat_rent: 'Rent',
        cat_salary_expense: 'Salary Expense',
        cat_marketing: 'Marketing',
        cat_supplies: 'Supplies',
        cat_other_expense: 'Other Expenses',
        income_click_to_expense: 'Income (Click to change to Expense)',
        expense_click_to_income: 'Expense (Click to change to Income)'
    },
    'ja': {
        verified: '確認済',
        date: '日付',
        type: 'タイプ',
        description: '説明',
        payee: '受取人',
        reference: '参照番号',
        checkNumber: '小切手番号',
        category: 'カテゴリー',
        memo: 'メモ',
        reconciled: '照合済',
        unreconciled: '未照合',
        attachment: '添付',
        amount: '金額',
        balance: '残高',
        bankCode: '銀行コード',
        branchName: '支店住所',
        accountType: '口座種類',
        account_info: '口座情報',
        editable: '(編集可)',
        bank_name: '銀行名',
        account_number: '口座番号',
        account_holder: '口座名義人',
        statement_period: '明細期間',
        statement_date: '明細日付',
        statement_date_placeholder: 'YYYY年MM月DD日',
        opening_balance: '期首残高',
        closing_balance: '期末残高',
        currency: '通貨',
        transactions: '取引記録',
        total_transactions: '合計{count}件の取引（{start}～{end}件目を表示）',
        no_transactions: '取引記録がありません',
        // 請求書関連の翻訳
        invoice_details: '請求書詳細',
        invoice_number: '請求書番号',
        vendor: '仕入先',
        total_amount: '合計金額',
        line_items: '明細項目',
        code: 'コード',
        quantity: '数量',
        unit: '単位',
        unit_price: '単価',
        unit_default: '個',
        no_items: '項目データなし',
        // カテゴリー関連
        actions: '操作',
        uncategorized: '未分類',
        income_categories: '収入カテゴリー',
        expense_categories: '支出カテゴリー',
        cat_salary: '給与',
        cat_sales: '売上収入',
        cat_interest: '利息収入',
        cat_other_income: 'その他収入',
        cat_office: '事務所費用',
        cat_transport: '交通費',
        cat_meal: '接待交際費',
        cat_utilities: '水道光熱費',
        cat_rent: '家賃',
        cat_salary_expense: '給与支出',
        cat_marketing: 'マーケティング費用',
        cat_supplies: '消耗品',
        cat_other_expense: 'その他支出',
        income_click_to_expense: '収入（クリックで支出に変更）',
        expense_click_to_income: '支出（クリックで収入に変更）'
    },
    'ko': {
        verified: '확인됨',
        date: '날짜',
        type: '유형',
        description: '설명',
        payee: '수취인',
        reference: '참조번호',
        checkNumber: '수표번호',
        category: '카테고리',
        memo: '메모',
        reconciled: '조정완료',
        unreconciled: '미조정',
        attachment: '첨부',
        amount: '금액',
        balance: '잔액',
        bankCode: '은행코드',
        branchName: '지점 주소',
        accountType: '계좌유형',
        account_info: '계정 정보',
        editable: '(편집 가능)',
        bank_name: '은행명',
        account_number: '계좌 번호',
        account_holder: '계좌 소유자',
        statement_period: '명세서 기간',
        statement_date: '명세서 날짜',
        statement_date_placeholder: 'YYYY-MM-DD',
        opening_balance: '기초 잔액',
        closing_balance: '기말 잔액',
        currency: '통화',
        transactions: '거래 내역',
        total_transactions: '총 {count}건의 거래 ({start}~{end}건 표시)',
        no_transactions: '거래 내역 없음',
        // 송장 관련 번역
        invoice_details: '송장 상세',
        invoice_number: '송장 번호',
        vendor: '공급업체',
        total_amount: '총액',
        line_items: '항목 명세',
        code: '코드',
        quantity: '수량',
        unit: '단위',
        unit_price: '단가',
        unit_default: '개',
        no_items: '항목 데이터 없음',
        // 카테고리 관련
        actions: '작업',
        uncategorized: '미분류',
        income_categories: '수입 카테고리',
        expense_categories: '지출 카테고리',
        cat_salary: '급여',
        cat_sales: '판매 수익',
        cat_interest: '이자 수입',
        cat_other_income: '기타 수입',
        cat_office: '사무실 비용',
        cat_transport: '교통비',
        cat_meal: '식대',
        cat_utilities: '공과금',
        cat_rent: '임대료',
        cat_salary_expense: '급여 지출',
        cat_marketing: '마케팅 비용',
        cat_supplies: '소모품',
        cat_other_expense: '기타 지출',
        income_click_to_expense: '수입 (클릭하여 지출로 변경)',
        expense_click_to_income: '지출 (클릭하여 수입으로 변경)'
    }
};

// 獲取翻譯文本
function t(key) {
    const lang = getCurrentLanguage();
    return i18n[lang][key] || i18n['zh-TW'][key] || key;
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

// 交易記錄分頁變量（圖3需求）
let currentTransactionPage = 1;
let transactionsPerPage = 20;  // ✅ 從 10 改為 20
let totalTransactions = 0;

console.log('✅ 交易記錄分頁變量已初始化:', { currentTransactionPage, transactionsPerPage });

// ============================================
// 初始化函數
// ============================================

async function init() {
    console.log('🚀 初始化文檔詳情頁面...');
    
    try {
        // 步驟 1: 等待 SimpleAuth 初始化
        console.log('⏳ 步驟 1/5: 等待 SimpleAuth 初始化...');
        let attempts = 0;
        while (!window.simpleAuth || !window.simpleAuth.initialized) {
            if (attempts++ > 50) { // Max 5 seconds wait (reduced from 10s)
                console.error('❌ SimpleAuth 初始化超時');
                console.log('🔄 嘗試重新載入頁面...');
                setTimeout(() => window.location.reload(), 1000);
                return;
            }
            if (attempts % 10 === 0) {
                console.log(`⏳ 等待中... (${attempts}/50)`);
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        console.log('✅ SimpleAuth 已就緒');
        
        // 步驟 2: 等待用戶狀態確定
        console.log('⏳ 步驟 2/5: 等待用戶狀態確定...');
        attempts = 0;
        while (!window.simpleAuth.currentUser) {
            if (attempts++ > 30) { // Max 3 seconds wait (reduced from 10s)
                console.error('❌ 用戶未登入');
                if (!DEBUG_MODE) {
                    alert('請先登入');
                    window.location.href = 'index.html';
                }
                return;
            }
            if (attempts % 10 === 0) {
                console.log(`⏳ 檢查登入狀態... (${attempts}/30)`);
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
            if (attempts++ > 50) { // Max 5 seconds wait (reduced from 10s)
                console.error('❌ SimpleDataManager 初始化超時');
                alert('數據管理器初始化失敗，即將重新載入頁面...');
                setTimeout(() => window.location.reload(), 1000);
                return;
            }
            if (attempts % 10 === 0) {
                console.log(`⏳ 等待數據管理器... (${attempts}/50)`);
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        console.log('✅ SimpleDataManager 已就緒');
        
        // 步驟 5: 載入文檔
        console.log('⏳ 步驟 5/5: 載入文檔...');
        await loadDocument();
        console.log('✅ 初始化完成！');
    } catch (error) {
        console.error('❌ 初始化過程發生錯誤:', error);
        alert('頁面初始化失敗，即將重新載入...');
        setTimeout(() => window.location.reload(), 1000);
    }
}

// ============================================
// 文檔載入函數
// ============================================

// ✅ 全局变量：实时监听解除函数
let documentListener = null;

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
        // 🔥 添加超時保護：如果 5 秒內無法載入，顯示提示並允許重試
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('文檔載入超時')), 5000);
        });
        
        // 從 Firebase 獲取文檔
        console.log('🔍 從 Firebase 獲取文檔...');
        const doc = await Promise.race([
            window.simpleDataManager.getDocument(projectId, documentId),
            timeoutPromise
        ]);
        
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
        
        // ✅ 方案1：設置實時監聽（自動更新）
        setupDocumentListener(projectId, documentId);
        
    } catch (error) {
        console.error('❌ 載入文檔失敗:', error);
        alert('載入文檔失敗: ' + error.message);
        goBackToDashboard();
    }
}

// ============================================
// ✅ 方案1：實時監聽文檔更新
// ============================================

function setupDocumentListener(projectId, documentId) {
    console.log('👂 設置實時監聽...');
    
    // 如果已經有監聽，先解除
    if (documentListener) {
        documentListener();
        console.log('🔄 解除舊的監聽');
    }
    
    // 使用 Firebase onSnapshot 監聽文檔變化
    const docRef = window.firebase.firestore()
        .collection('projects')
        .doc(projectId)
        .collection('documents')
        .doc(documentId);
    
    documentListener = docRef.onSnapshot((snapshot) => {
        if (!snapshot.exists) {
            console.warn('⚠️ 文檔不存在');
            return;
        }
        
        const updatedDoc = { id: snapshot.id, ...snapshot.data() };
        console.log('🔄 文檔已更新:', updatedDoc);
        
        // 檢查狀態變化
        const oldStatus = currentDocument?.status;
        const newStatus = updatedDoc.status;
        
        console.log(`📊 狀態變化: ${oldStatus} → ${newStatus}`);
        
        // 更新當前文檔
        currentDocument = updatedDoc;
        
        // 如果從 processing 變為 completed，自動刷新顯示
        if (oldStatus === 'processing' && newStatus === 'completed') {
            console.log('🎉 處理完成！自動刷新顯示...');
            
            // 顯示成功提示
            showProcessingCompleteNotification();
            
            // 刷新顯示
            displayDocumentContent();
        }
        
        // 如果當前是 processing，刷新處理狀態
        if (newStatus === 'processing') {
            console.log('⏳ 處理中，更新進度顯示...');
            displayDocumentContent();
        }
    }, (error) => {
        console.error('❌ 監聽失敗:', error);
    });
    
    console.log('✅ 實時監聽已設置');
}

// ============================================
// 顯示處理完成通知
// ============================================

function showProcessingCompleteNotification() {
    // 創建通知元素
    const notification = document.createElement('div');
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 80px;
            right: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: slideInRight 0.5s ease-out, fadeOut 0.5s ease-in 2.5s;
        ">
            <i class="fas fa-check-circle" style="font-size: 1.5rem;"></i>
            <div>
                <div style="font-weight: 600; font-size: 1rem;">處理完成！</div>
                <div style="font-size: 0.875rem; opacity: 0.9;">數據已自動更新</div>
            </div>
        </div>
        <style>
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes fadeOut {
                from {
                    opacity: 1;
                }
                to {
                    opacity: 0;
                }
            }
        </style>
    `;
    
    document.body.appendChild(notification);
    
    // 3秒後自動移除
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ============================================
// 通用：顯示處理中狀態
// ============================================

function showProcessingStatus(detailsSection, dataSection, docTypeName = '文檔') {
    detailsSection.innerHTML = `
        <div style="
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 2px solid #3b82f6;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            animation: pulse 2s ease-in-out infinite;
        ">
            <div style="
                width: 80px;
                height: 80px;
                margin: 0 auto 1.5rem;
                border: 4px solid #3b82f6;
                border-top-color: transparent;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <h3 style="
                font-size: 1.5rem;
                font-weight: 600;
                color: #1e40af;
                margin-bottom: 0.75rem;
            ">
                <i class="fas fa-robot" style="margin-right: 0.5rem;"></i>
                AI 正在處理您的${docTypeName}...
            </h3>
            <p style="
                font-size: 1rem;
                color: #3b82f6;
                margin-bottom: 1.5rem;
                line-height: 1.6;
            ">
                我們正在使用 AI 技術提取${docTypeName}數據<br>
                預計需要 <strong>15-30 秒</strong>
            </p>
            <div style="
                background: white;
                border-radius: 12px;
                padding: 1rem;
                margin: 1.5rem auto 0;
                max-width: 400px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
            ">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.75rem;
                ">
                    <span style="font-size: 0.875rem; color: #6b7280;">
                        <i class="fas fa-check-circle" style="color: #10b981; margin-right: 0.25rem;"></i>
                        OCR 文字識別
                    </span>
                    <span style="font-size: 0.875rem; font-weight: 600; color: #10b981;">完成</span>
                </div>
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.75rem;
                ">
                    <span style="font-size: 0.875rem; color: #6b7280;">
                        <i class="fas fa-spinner fa-spin" style="color: #3b82f6; margin-right: 0.25rem;"></i>
                        AI 數據提取
                    </span>
                    <span style="font-size: 0.875rem; font-weight: 600; color: #3b82f6;">處理中...</span>
                </div>
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    color: #9ca3af;
                ">
                    <span style="font-size: 0.875rem;">
                        <i class="far fa-clock" style="margin-right: 0.25rem;"></i>
                        數據校驗
                    </span>
                    <span style="font-size: 0.875rem;">等待中</span>
                </div>
            </div>
            <p style="
                font-size: 0.875rem;
                color: #6b7280;
                margin-top: 1.5rem;
                font-style: italic;
            ">
                <i class="fas fa-info-circle" style="margin-right: 0.25rem;"></i>
                處理完成後，頁面將自動更新，無需手動刷新
            </p>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.95; }
            }
        </style>
    `;
    
    dataSection.innerHTML = '';
}

// ============================================
// 通用：顯示處理失敗狀態
// ============================================

function showFailedStatus(detailsSection, dataSection) {
    detailsSection.innerHTML = `
        <div style="
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border: 2px solid #ef4444;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        ">
            <div style="
                width: 80px;
                height: 80px;
                margin: 0 auto 1.5rem;
                background: #fee2e2;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <i class="fas fa-exclamation-triangle" style="
                    font-size: 2.5rem;
                    color: #ef4444;
                "></i>
            </div>
            <h3 style="
                font-size: 1.5rem;
                font-weight: 600;
                color: #b91c1c;
                margin-bottom: 0.75rem;
            ">處理失敗</h3>
            <p style="
                font-size: 1rem;
                color: #ef4444;
                margin-bottom: 1.5rem;
            ">
                AI 處理過程中遇到錯誤<br>
                <span style="font-size: 0.875rem; color: #6b7280;">${currentDocument?.error || '未知錯誤'}</span>
            </p>
            <button onclick="location.reload()" style="
                background: #ef4444;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                font-size: 1rem;
                transition: all 0.2s;
            " onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">
                <i class="fas fa-redo" style="margin-right: 0.5rem;"></i>
                重試
            </button>
        </div>
    `;
    
    dataSection.innerHTML = '';
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
               currentDocument.fileUrl ||
               currentDocument.imageBase64;
    
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
    
    console.log('📊 處理數據:', data);
    
    // 統一使用發票/收據的 IRD 扣稅分析介面
    displayInvoiceContent(data);
}

// ============================================
// 發票內容顯示
// ============================================

function displayInvoiceContent(data) {
    console.log('📄 顯示發票內容');
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    // ✅ 方案2：檢查文檔狀態
    const docStatus = currentDocument?.status || 'unknown';
    
    if (docStatus === 'processing') {
        showProcessingStatus(detailsSection, dataSection, '發票');
        return;
    }
    
    if (docStatus === 'failed') {
        showFailedStatus(detailsSection, dataSection);
        return;
    }
    
    // 發票/收據詳情卡片（桌面版2列，手機版1列）
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-receipt" style="color: #4F46E5; margin-right: 0.5rem;"></i>
                單據詳情 (IRD 扣稅分析)
            </h3>
            <div class="invoice-details-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">商戶名稱</label>
                    <input type="text" id="vendor" value="${data.merchant_name || data.vendor || data.supplier || data.merchantName || '—'}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">收據日期</label>
                    <input type="date" id="invoiceDate" value="${data.date || data.invoice_date || ''}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">總金額</label>
                    <input type="text" id="totalAmount" value="${formatCurrency(data.total_amount || data.total || data.totalAmount || 0)}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 700; color: #1f2937; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">開支類別</label>
                    <input type="text" id="expenseCategory" value="${data.expense_category || '未分類'}" 
                           onchange="autoSaveInvoiceDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="grid-column: 1 / -1; background: ${getTaxBgColor(data.tax_deductibility?.level)}; padding: 1rem; border-radius: 8px; border: 1px solid ${getTaxBorderColor(data.tax_deductibility?.level)};">
                    <label style="display: block; font-size: 0.75rem; color: ${getTaxTextColor(data.tax_deductibility?.level)}; margin-bottom: 0.5rem; font-weight: 700;">IRD 扣稅可能性</label>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <select id="taxLevel" onchange="autoSaveInvoiceDetails()" style="padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white; font-weight: 600;">
                            <option value="High" ${data.tax_deductibility?.level === 'High' ? 'selected' : ''}>✅ 100% 可扣稅 (High)</option>
                            <option value="Medium" ${data.tax_deductibility?.level === 'Medium' ? 'selected' : ''}>⚠️ 需確認 (Medium)</option>
                            <option value="Low" ${data.tax_deductibility?.level === 'Low' ? 'selected' : ''}>❌ 私人/交際 (Low)</option>
                            <option value="None" ${data.tax_deductibility?.level === 'None' ? 'selected' : ''}>🚫 不可扣稅 (None)</option>
                        </select>
                        <input type="text" id="taxReason" value="${data.tax_deductibility?.reason || ''}" placeholder="扣稅原因說明..."
                               onchange="autoSaveInvoiceDetails()"
                               style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                    </div>
                </div>
            </div>
            <style>
                /* 手機版改為1列 */
                @media (max-width: 768px) {
                    .invoice-details-grid {
                        grid-template-columns: 1fr !important;
                    }
                    .invoice-details-grid > div:last-child > div {
                        flex-direction: column;
                    }
                    .invoice-details-grid > div:last-child select,
                    .invoice-details-grid > div:last-child input {
                        width: 100%;
                    }
                }
            </style>
        </div>
    `;
    
    // 輔助函數：獲取扣稅標籤顏色
    function getTaxBgColor(level) {
        if (level === 'High') return '#ecfdf5';
        if (level === 'Medium') return '#fffbeb';
        if (level === 'Low') return '#fef2f2';
        return '#f9fafb';
    }
    function getTaxBorderColor(level) {
        if (level === 'High') return '#a7f3d0';
        if (level === 'Medium') return '#fde68a';
        if (level === 'Low') return '#fecaca';
        return '#e5e7eb';
    }
    function getTaxTextColor(level) {
        if (level === 'High') return '#065f46';
        if (level === 'Medium') return '#92400e';
        if (level === 'Low') return '#991b1b';
        return '#4b5563';
    }
    
    // 項目明細表格（改為顯示購買項目簡述）
    const itemsSummary = data.items_summary || '無項目簡述';
    
    dataSection.innerHTML = `
        <div class="transactions-section">
            <h3 class="transactions-title" style="margin-bottom: 1rem;">
                <i class="fas fa-list" style="color: #8b5cf6; margin-right: 0.5rem;"></i>
                購買項目簡述
            </h3>
            <div style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                <textarea id="itemsSummary" onchange="autoSaveItemsSummary()" style="width: 100%; min-height: 80px; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.95rem; background: white; resize: vertical; line-height: 1.5;">${itemsSummary}</textarea>
            </div>
            
            <!-- 隱藏原有的複雜明細表，保留代碼以防未來需要 -->
            <div style="display: none;">
                <table class="transactions-table invoice-items-table">
                    <tbody id="itemsTableBody"></tbody>
                </table>
            </div>
        </div>
    `;
    
    // 添加全局函數處理簡述更新
    window.autoSaveItemsSummary = function() {
        const summary = document.getElementById('itemsSummary')?.value;
        if (currentDocument && currentDocument.processedData) {
            currentDocument.processedData.items_summary = summary;
            markAsChanged();
        }
    };
}

// ============================================
// 銀行對帳單內容顯示
// ============================================

function displayBankStatementContent(data) {
    console.log('🏦 顯示銀行對帳單內容');
    console.log('📊 原始數據:', JSON.stringify(data, null, 2));
    
    // 🌐 獲取當前語言
    const currentLang = getCurrentLanguage();
    console.log('🌐 當前語言:', currentLang);
    
    // ✅ 方案2：檢查文檔狀態
    const docStatus = currentDocument?.status || 'unknown';
    console.log('📊 文檔狀態:', docStatus);
    
    const detailsSection = document.getElementById('documentDetailsSection');
    const dataSection = document.getElementById('documentDataSection');
    
    // ✅ 如果正在處理中，顯示處理狀態而不是 $0.00
    if (docStatus === 'processing') {
        console.log('⏳ 文檔處理中，顯示處理狀態...');
        showProcessingStatus(detailsSection, dataSection, '銀行對帳單');
        return;
    }
    
    // ✅ 如果處理失敗，顯示錯誤狀態
    if (docStatus === 'failed') {
        console.log('❌ 文檔處理失敗');
        showFailedStatus(detailsSection, dataSection);
        return;
    }
    
    // 🔍 DEBUG - 详细诊断交易记录提取（已禁用）
    // console.log('🔍 DEBUG - 完整数据结构:', data);
    // console.log('🔍 DEBUG - processedData:', currentDocument?.processedData);
    // console.log('🔍 DEBUG - 所有可能的transactions字段:');
    // console.log('   data.transactions:', data.transactions);
    // console.log('   data.transaction:', data.transaction);
    // console.log('   data.items:', data.items);
    // console.log('   currentDocument.transactions:', currentDocument?.transactions);
    // console.log('🔍 DEBUG - currentDocument完整内容:', currentDocument);
    
    // ✅ 提取帳戶信息（支持多種字段名稱 + 增強 Fallback）
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
    
    // 🔥 增強日期提取邏輯：從 statement_period 提取結束日期（支持多種格式）
    if (!statementDate && (data.statementPeriod || data.statement_period)) {
        const period = data.statementPeriod || data.statement_period;
        console.log('📅 嘗試從 period 提取日期:', period);
        
        // 嘗試多種日期格式
        let extractedDate = null;
        
        // 格式1: "to MM/DD/YYYY" 或 "to DD/MM/YYYY"
        let match = period.match(/to\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})/i);
        if (match) {
            const dateStr = match[1];
            const parts = dateStr.split(/[\/\-]/);
            
            // 判斷是 MM/DD/YYYY 還是 DD/MM/YYYY
            // 如果第一個數字 > 12，則為 DD/MM/YYYY
            if (parseInt(parts[0]) > 12) {
                // DD/MM/YYYY 格式
                extractedDate = `${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
            } else {
                // MM/DD/YYYY 格式
                extractedDate = `${parts[2]}-${parts[0].padStart(2, '0')}-${parts[1].padStart(2, '0')}`;
            }
            console.log('✅ 從 "to MM/DD/YYYY" 提取:', extractedDate);
        }
        
        // 格式2: "至 YYYY-MM-DD"
        if (!extractedDate) {
            match = period.match(/[至to]\s+(\d{4}[\-\/]\d{1,2}[\-\/]\d{1,2})/i);
            if (match) {
                extractedDate = match[1].replace(/\//g, '-');
                // 確保格式為 YYYY-MM-DD
                const parts = extractedDate.split('-');
                extractedDate = `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`;
                console.log('✅ 從 "至 YYYY-MM-DD" 提取:', extractedDate);
            }
        }
        
        // 格式3: "2018-12-03 to 2019-01-01"（完整格式）
        if (!extractedDate) {
            match = period.match(/(\d{4}[\-\/]\d{1,2}[\-\/]\d{1,2})\s+to\s+(\d{4}[\-\/]\d{1,2}[\-\/]\d{1,2})/i);
            if (match) {
                extractedDate = match[2].replace(/\//g, '-');
                // 確保格式為 YYYY-MM-DD
                const parts = extractedDate.split('-');
                extractedDate = `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`;
                console.log('✅ 從完整日期範圍提取結束日期:', extractedDate);
            }
        }
        
        // 格式4: 只有一個日期 "YYYY-MM-DD" 或 "MM/DD/YYYY"
        if (!extractedDate) {
            match = period.match(/(\d{4}[\-\/]\d{1,2}[\-\/]\d{1,2})/);
            if (match) {
                extractedDate = match[1].replace(/\//g, '-');
                const parts = extractedDate.split('-');
                if (parts[0].length === 4) {
                    // YYYY-MM-DD
                    extractedDate = `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`;
                }
                console.log('✅ 從單個日期提取:', extractedDate);
            }
        }
        
        if (extractedDate) {
            statementDate = extractedDate;
        } else {
            console.warn('⚠️ 無法從 period 提取日期:', period);
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
    
    // ✅ 提前計算總支出和總收入（在渲染之前）
    const transactions = data.transactions || 
                         data.transaction || 
                         data.items ||
                         currentDocument.transactions || 
                         [];
    
    let totalExpenses = 0;
    let totalIncome = 0;
    
    transactions.forEach(tx => {
        const amount = parseFloat(tx.amount || 0);
        // 根據 transactionSign 判斷是收入還是支出
        if (tx.transactionSign === 'expense' || (tx.debit && parseFloat(tx.debit) > 0)) {
            totalExpenses += amount;
        } else if (tx.transactionSign === 'income' || (tx.credit && parseFloat(tx.credit) > 0)) {
            totalIncome += amount;
        }
    });
    
    console.log('   總支出:', totalExpenses);
    console.log('   總收入:', totalIncome);
    console.log('   交易數量:', transactions.length);
    
    // ✅ 帳戶詳情（可編輯）- 新增：帳戶持有人、對帳單期間、期初餘額、貨幣
    detailsSection.innerHTML = `
        <div class="bank-details-card">
            <h3 class="card-title" style="margin-bottom: 1.5rem;">
                <i class="fas fa-university" style="color: #10b981; margin-right: 0.5rem;"></i>
                ${t('account_info')}
                <span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;">${t('editable')}</span>
            </h3>
            <div class="bank-info-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('bank_name')}</label>
                    <input type="text" id="bankName" value="${bankName}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">
                        ${t('bankCode')}
                        <span style="color: #9ca3af; font-weight: normal; font-size: 0.7rem;">(如: 024, 004)</span>
                    </label>
                    <input type="text" id="bankCode" value="${data.bankCode || ''}" 
                           onchange="autoSaveBankStatementDetails()"
                           placeholder="024"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('account_number')}</label>
                    <input type="text" id="accountNumber" value="${accountNumber}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('branchName')}</label>
                    <input type="text" id="branchName" value="${data.branchName || ''}" 
                           onchange="autoSaveBankStatementDetails()"
                           placeholder="${currentLang === 'zh-TW' ? '香港中環花園道33樓' : 'Central Branch Address'}"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('account_holder')}</label>
                    <input type="text" id="accountHolder" value="${accountHolder}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('accountType')}</label>
                    <select id="accountType" 
                            onchange="autoSaveBankStatementDetails()"
                            style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white; cursor: pointer;">
                        <option value="CHECKING" ${(data.accountType || 'CHECKING') === 'CHECKING' ? 'selected' : ''}>${currentLang === 'zh-TW' ? '支票賬戶' : 'Checking'}</option>
                        <option value="SAVINGS" ${data.accountType === 'SAVINGS' ? 'selected' : ''}>${currentLang === 'zh-TW' ? '儲蓄賬戶' : 'Savings'}</option>
                        <option value="CREDITCARD" ${data.accountType === 'CREDITCARD' ? 'selected' : ''}>${currentLang === 'zh-TW' ? '信用卡' : 'Credit Card'}</option>
                        <option value="MONEYMRKT" ${data.accountType === 'MONEYMRKT' ? 'selected' : ''}>${currentLang === 'zh-TW' ? '貨幣市場' : 'Money Market'}</option>
                    </select>
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('currency')}</label>
                    <input type="text" id="currency" value="${currency}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('statement_period')}</label>
                    <input type="text" id="statementPeriod" value="${statementPeriod}" 
                           onchange="autoSaveBankStatementDetails()"
                           placeholder="2021/01/14 - 2021/01/31"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('opening_balance')}</label>
                    <input type="text" id="openingBalance" value="${formatCurrency(openingBalance)}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #3b82f6; background: white;">
                </div>
                <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('closing_balance')}</label>
                    <input type="text" id="closingBalance" value="${formatCurrency(closingBalance)}" 
                           onchange="autoSaveBankStatementDetails()"
                           style="width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem; font-weight: 600; color: #10b981; background: white;">
                </div>
                <!-- 總支出和總收入已移除 -->
            </div>
            <style>
                /* ✅ 手機版：帳戶信息改為1列顯示 */
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
    `;
    
    // ✅ 設置全局變量用於分頁（交易列表已在前面提取）
    totalTransactions = transactions.length;
    const totalPages = Math.ceil(totalTransactions / transactionsPerPage);
    
    // ✅ 計算當前頁的交易記錄
    const startIndex = (currentTransactionPage - 1) * transactionsPerPage;
    const endIndex = Math.min(startIndex + transactionsPerPage, totalTransactions);
    const currentPageTransactions = transactions.slice(startIndex, endIndex);
    
    let transactionsHTML = '';
    // ✅ currentLang 已在函數開頭聲明，這裡直接使用
    const showRefAndCheck = (currentLang === 'zh-TW' || currentLang === 'en'); // 只有中文和英文版显示参考编号和支票号码
    
    currentPageTransactions.forEach((tx, pageIndex) => {
        const actualIndex = startIndex + pageIndex; // 實際在完整數組中的索引
        
        // ✅ 直接使用原始數據，不進行任何計算
        // ⚠️ 关键修复：使用 debit/credit，而不是已删除的 amount 字段
        const debitValue = parseFloat(tx.debit) || 0;
        const creditValue = parseFloat(tx.credit) || 0;
        const balanceStr = String(tx.balance || '0');
        
        // ✅ 根据 debit/credit 判断收入/支出
        let amountStr = '0';
        let isIncome = false;
        
        if (creditValue > 0) {
            // 有 credit = 收入
            amountStr = String(creditValue);
            isIncome = true;
            tx.transactionSign = 'income';
        } else if (debitValue > 0) {
            // 有 debit = 支出
            amountStr = String(debitValue);
            isIncome = false;
            tx.transactionSign = 'expense';
        } else {
            // 都为 0（例如承上结余）
            amountStr = '0';
            tx.transactionSign = tx.transactionSign || 'income';
        }
        
        // ✅ isIncome 已在上面定义，这里只需要根据 transactionSign 更新
        isIncome = tx.transactionSign === 'income';
        const amountSign = isIncome ? '+' : '-';
        const amountColor = isIncome ? '#10b981' : '#ef4444';
        const amountBgColor = isIncome ? '#d1fae5' : '#fee2e2';
        
        // 格式化顯示金額（保留原始數值，只添加千分位）
        const formatAmount = (val) => {
            const num = Math.abs(parseFloat(val.toString().replace(/[^0-9.-]+/g, '')) || 0);
            return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        };
        
        const displayAmount = formatAmount(amountStr);
        const displayBalance = formatAmount(balanceStr);
        
        // ✅ 優化描述顯示（保留完整名稱）
        const description = tx.description || tx.details || tx.memo || '—';
        
        // ✅ 获取所有字段数据
        const transactionType = tx.transactionType || '—';
        // ✅ 將 Unknown 改為 —
        const payee = (tx.payee && tx.payee.toLowerCase() !== 'unknown') ? tx.payee : '—';
        const referenceNumber = tx.referenceNumber || '';
        const checkNumber = tx.checkNumber || '';
        const category = tx.category || '';
        const memo = tx.memo || '';
        const reconciled = tx.reconciled || false;
        const hasAttachment = tx.hasAttachment || false;
        
        transactionsHTML += `
            <tr data-index="${actualIndex}" class="transaction-row">
                <!-- 🚫 展開按鈕已移除（2026-01-09） -->
                <!-- 🚫 選擇框已移除（2026-01-09）：用戶反饋有兩個復選框，刪除選擇功能 -->
                <td class="checkbox-cell">
                    <input type="checkbox" 
                           class="reconciled-checkbox" 
                           data-index="${actualIndex}"
                           ${reconciled ? 'checked' : ''}
                           onchange="handleReconciledChange(${actualIndex}, this.checked)"
                           title="${reconciled ? t('reconciled') : t('unreconciled')}">
                </td>
                <td contenteditable="true" class="editable-cell date-cell" data-field="date" style="min-width: 100px; font-size: 0.875rem;" data-date="${tx.date || '—'}">${tx.date || '—'}</td>
                <td contenteditable="true" class="editable-cell type-cell" data-field="transactionType" style="min-width: 75px; color: #6b7280; font-size: 0.8rem;">${transactionType}</td>
                <td contenteditable="true" class="editable-cell desc-cell" data-field="description" style="min-width: 150px; max-width: 280px; font-size: 0.875rem;">${description}</td>
                <td contenteditable="true" class="editable-cell payee-cell" data-field="payee" style="min-width: 120px; max-width: 200px; color: #6b7280; font-size: 0.8rem;">${payee}</td>
                ${showRefAndCheck ? `<td contenteditable="true" class="editable-cell ref-cell" data-field="referenceNumber" style="min-width: 85px; color: #6b7280; font-size: 0.8rem;">${referenceNumber}</td>` : ''}
                ${showRefAndCheck ? `<td contenteditable="true" class="editable-cell check-cell" data-field="checkNumber" style="min-width: 65px; color: #6b7280; font-size: 0.8rem;">${checkNumber}</td>` : ''}
                <td class="category-cell" style="min-width: 105px;">
                    <select class="category-select" data-index="${actualIndex}" onchange="handleCategoryChange(${actualIndex}, this.value)" style="width: 100%; padding: 0.3rem; font-size: 0.8rem; border: 1px solid #d1d5db; border-radius: 4px;">
                        <option value="">${t('uncategorized')}</option>
                        <optgroup label="${t('income_categories')}">
                            <option value="salary" ${category === 'salary' ? 'selected' : ''}>${t('cat_salary')}</option>
                            <option value="sales" ${category === 'sales' ? 'selected' : ''}>${t('cat_sales')}</option>
                            <option value="interest" ${category === 'interest' ? 'selected' : ''}>${t('cat_interest')}</option>
                            <option value="other-income" ${category === 'other-income' ? 'selected' : ''}>${t('cat_other_income')}</option>
                        </optgroup>
                        <optgroup label="${t('expense_categories')}">
                            <option value="office" ${category === 'office' ? 'selected' : ''}>${t('cat_office')}</option>
                            <option value="transport" ${category === 'transport' ? 'selected' : ''}>${t('cat_transport')}</option>
                            <option value="meal" ${category === 'meal' ? 'selected' : ''}>${t('cat_meal')}</option>
                            <option value="utilities" ${category === 'utilities' ? 'selected' : ''}>${t('cat_utilities')}</option>
                            <option value="rent" ${category === 'rent' ? 'selected' : ''}>${t('cat_rent')}</option>
                            <option value="salary-expense" ${category === 'salary-expense' ? 'selected' : ''}>${t('cat_salary_expense')}</option>
                            <option value="marketing" ${category === 'marketing' ? 'selected' : ''}>${t('cat_marketing')}</option>
                            <option value="supplies" ${category === 'supplies' ? 'selected' : ''}>${t('cat_supplies')}</option>
                            <option value="other-expense" ${category === 'other-expense' ? 'selected' : ''}>${t('cat_other_expense')}</option>
                        </optgroup>
                    </select>
                </td>
                <td class="amount-cell" style="position: relative; padding: 0.45rem 0.3rem !important;">
                    <div style="display: flex; align-items: center; gap: 0.35rem; justify-content: flex-start; white-space: nowrap;">
                        <button onclick="toggleTransactionType(${actualIndex})" 
                                class="transaction-sign-btn"
                                style="display: inline-flex !important; align-items: center; justify-content: center; width: 24px; height: 24px; background: ${amountColor}; color: white; border: none; border-radius: 3px; font-weight: 700; font-size: 0.9rem; cursor: pointer; flex-shrink: 0; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.1);"
                                onmouseover="this.style.opacity='0.85'; this.style.transform='scale(1.05)'" 
                                onmouseout="this.style.opacity='1'; this.style.transform='scale(1)'"
                                title="${isIncome ? t('income_click_to_expense') : t('expense_click_to_income')}">
                            ${amountSign}
                        </button>
                        <span contenteditable="true" 
                              class="editable-amount" 
                              data-index="${actualIndex}"
                              data-field="amount"
                              style="text-align: right; color: ${amountColor}; font-weight: 600; font-size: 0.85rem; min-width: 80px; padding: 0.25rem 0.4rem; border: 1px solid transparent; border-radius: 3px; white-space: nowrap; background: ${amountBgColor}20; flex: 1;"
                              onfocus="this.style.border='1px solid ${amountColor}'; this.style.background='${amountBgColor}40'"
                              onblur="this.style.border='1px solid transparent'; this.style.background='${amountBgColor}20'; updateTransactionAmount(${actualIndex}, this.textContent)">${displayAmount}</span>
                    </div>
                </td>
                <td contenteditable="true" class="editable-cell balance-cell" data-field="balance" style="text-align: right; font-weight: 600; color: #3b82f6; font-size: 0.85rem; white-space: nowrap; padding: 0.45rem 0.3rem !important;">${displayBalance}</td>
                <td class="attachment-cell">
                    <i class="fas fa-paperclip attachment-icon ${hasAttachment ? 'has-attachment' : 'no-attachment'}" 
                       onclick="handleAttachment(${actualIndex})"
                       title="${hasAttachment ? '查看附件' : '添加附件'}"></i>
                </td>
                <td class="action-cell">
                    <button class="icon-btn delete" onclick="confirmDeleteTransaction(${actualIndex})" title="刪除" style="background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; padding: 0.4rem 0.5rem; border-radius: 6px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='#fecaca'" onmouseout="this.style.background='#fee2e2'">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </td>
            </tr>
            <!-- 🚫 編輯表單面板已移除（2026-01-09）：用戶要求刪除圖2中的編輯UI -->
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
    
    // ✅ currentLang 已在函數開頭聲明，showRefAndCheck 已在前面聲明，這裡直接使用
    
    dataSection.innerHTML = `
        <div class="transactions-section">
            <div class="transactions-header">
                <h3 class="transactions-title">
                    <i class="fas fa-exchange-alt" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                    ${t('transactions')}
                </h3>
            </div>
            <div class="transactions-info">
                ${t('total_transactions').replace('{count}', transactions.length).replace('{start}', startIndex + 1).replace('{end}', endIndex)}
            </div>
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th class="checkbox-cell" style="width: 45px; text-align: center; font-size: 0.75rem; font-weight: 600;">✓ ${t('reconciled')}</th>
                        <th style="font-size: 0.875rem;">${t('date')}</th>
                        <th class="type-cell" style="font-size: 0.875rem;">${t('type')}</th>
                        <th style="font-size: 0.875rem;">${t('description')}</th>
                        <th style="font-size: 0.875rem;">${t('payee')}</th>
                        ${showRefAndCheck ? `<th class="ref-cell" style="font-size: 0.875rem;">${t('reference')}</th>` : ''}
                        ${showRefAndCheck ? `<th class="check-cell" style="font-size: 0.875rem;">${t('checkNumber')}</th>` : ''}
                        <th class="category-cell" style="font-size: 0.875rem;">${t('category')}</th>
                        <th style="font-size: 0.875rem; text-align: right;">${t('amount')}</th>
                        <th style="font-size: 0.875rem; text-align: right;">${t('balance')}</th>
                        <th class="attachment-cell" style="font-size: 0.875rem; text-align: center;">📎</th>
                        <th class="action-cell" style="font-size: 0.875rem; text-align: center;">${t('actions')}</th>
                    </tr>
                </thead>
                <tbody>
                    ${transactionsHTML || `<tr><td colspan="${showRefAndCheck ? 12 : 10}" style="text-align: center; padding: 2rem; color: #6b7280;">${t('no_transactions')}</td></tr>`}
                </tbody>
            </table>
            ${paginationHTML}
        </div>
    `;
    
    // ✅ 設置交易記錄編輯監聽器
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
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('date')}</label>
                    <div style="padding: 0.5rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem;">${data.date || '—'}</div>
                </div>
                <div>
                    <label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">${t('total_amount')}</label>
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
        const openingBalance = document.getElementById('openingBalance')?.value;
        const closingBalance = document.getElementById('closingBalance')?.value;
        
        if (bankName || accountNumber || accountHolder || statementDate || closingBalance) {
            currentDocument.processedData = {
                ...currentDocument.processedData,
                bankName: bankName || '',
                accountNumber: accountNumber || '',
                accountHolder: accountHolder || '',
                currency: currency || 'HKD',
                statementPeriod: statementPeriod || '',  // ✅ 避免 undefined
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
    const vendor = document.getElementById('vendor')?.value;
    const invoiceDate = document.getElementById('invoiceDate')?.value;
    const totalAmount = document.getElementById('totalAmount')?.value;
    const expenseCategory = document.getElementById('expenseCategory')?.value;
    const taxLevel = document.getElementById('taxLevel')?.value;
    const taxReason = document.getElementById('taxReason')?.value;
    
    // 更新 currentDocument
    if (currentDocument && currentDocument.processedData) {
        currentDocument.processedData = {
            ...currentDocument.processedData,
            merchant_name: vendor,
            vendor: vendor,
            date: invoiceDate,
            total_amount: parseFloat(totalAmount.replace(/[^0-9.-]+/g,"")) || 0,
            total: parseFloat(totalAmount.replace(/[^0-9.-]+/g,"")) || 0,
            expense_category: expenseCategory,
            tax_deductibility: {
                level: taxLevel,
                reason: taxReason
            }
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
        
        // ✅ 清理 processedData，移除所有 undefined 值（Firebase 不接受 undefined）
        const cleanProcessedData = JSON.parse(JSON.stringify(currentDocument.processedData, (key, value) => {
            return value === undefined ? null : value;
        }));
        
        await window.simpleDataManager.updateDocument(projectId, documentId, {
            processedData: cleanProcessedData,
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
            case 'excel':
                // Excel (.xlsx) 格式 - 使用 SheetJS
                if (typeof XLSX === 'undefined') {
                    alert('Excel 庫未加載，請刷新頁面後重試');
                    return;
                }
                try {
                    const excelData = [['Date', 'Type', 'Description', 'Payee', 'Reference', 'Amount', 'Balance']];
                    if (data.transactions && data.transactions.length > 0) {
                        data.transactions.forEach(t => {
                            excelData.push([
                                t.date || '',
                                t.transactionType || '',
                                t.description || '',
                                t.payee || '',
                                t.referenceNumber || '',
                                parseFloat(t.amount || 0),
                                parseFloat(t.balance || 0)
                            ]);
                        });
                    }
                    const wb = XLSX.utils.book_new();
                    const ws = XLSX.utils.aoa_to_sheet(excelData);
                    ws['!cols'] = [{wch: 12}, {wch: 10}, {wch: 40}, {wch: 25}, {wch: 15}, {wch: 12}, {wch: 12}];
                    XLSX.utils.book_append_sheet(wb, ws, "Bank Statement");
                    XLSX.writeFile(wb, fileName.replace(/\.(pdf|jpg|png)$/i, '') + '.xlsx');
                    console.log('✅ Excel 文件已下載');
                    return; // 直接返回，不需要後續的下載邏輯
                } catch (error) {
                    console.error('❌ Excel 導出失敗:', error);
                    alert('Excel 導出失敗: ' + error.message);
                    return;
                }
            
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

// 暴露到全局作用域
window.exportDocument = exportDocument;


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
// 交易記錄分頁函數
// ============================================

/**
 * 切換交易記錄頁面（圖3需求）
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
    console.log(`✅ 切換到交易記錄第 ${newPage} 頁（共 ${totalPages} 頁）`);
    
    // 重新渲染交易記錄
    if (currentDocument && currentDocument.processedData) {
        displayBankStatementContent(currentDocument.processedData);
        
        // ✅ 滾動到交易記錄頂部
        const transactionsSection = document.querySelector('.transactions-section');
        if (transactionsSection) {
            transactionsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } else {
        console.error('❌ 無法重新渲染：currentDocument 或 processedData 不存在');
    }
};

// ============================================
// 交易記錄編輯函數
// ============================================

// ✅ 切換交易類型標記（+/-）- 改變顯示標記並交換 debit/credit
function toggleTransactionType(index) {
    console.log(`🔄 切換交易 ${index} 的類型標記並交換 debit/credit`);
    
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    const transaction = currentDocument.processedData.transactions[index];
    if (!transaction) {
        console.error(`❌ 找不到交易 ${index}`);
        return;
    }
    
    // ✅ 1. 切換顯示標記
    transaction.transactionSign = transaction.transactionSign === 'income' ? 'expense' : 'income';
    
    // ✅ 2. 交換 debit 和 credit 的值
    const tempDebit = transaction.debit;
    transaction.debit = transaction.credit;
    transaction.credit = tempDebit;
    
    console.log(`✅ 交易 ${index} 已切換:`);
    console.log(`   - 標記: ${transaction.transactionSign}`);
    console.log(`   - Debit: ${transaction.debit}`);
    console.log(`   - Credit: ${transaction.credit}`);
    console.log(`   - Balance: ${transaction.balance} (余額保持不變)`);
    
    // 更新 UI
    displayDocumentContent();
    
    // 標記為有未保存更改
    markAsChanged();
}

// ✅ 更新交易金額 - 只更新amount值，不影響transactionSign標記
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
    
    // ✅ 只更新金額數值（保持原有的正負號和格式）
    // 移除逗號等格式符號，保留數字和小數點
    const cleanValue = value.toString().replace(/,/g, '');
    transaction.amount = cleanValue;
    
    console.log(`✅ 金額已更新為: ${transaction.amount}`);
    console.log(`📊 transactionSign 標記保持不變: ${transaction.transactionSign}`);
    
    // 標記為有未保存更改
    markAsChanged();
}

// ✅ 處理交易記錄複選框變化
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
            } else if (field === 'transactionType') {
                transaction.transactionType = value;
            } else if (field === 'description') {
                transaction.description = value;
            } else if (field === 'payee') {
                transaction.payee = value;
            } else if (field === 'referenceNumber') {
                transaction.referenceNumber = value;
            } else if (field === 'balance') {
                transaction.balance = parseFloat(value.replace(/[^0-9.-]+/g, '')) || 0;
            }
            
            // 標記為有未保存更改
            markAsChanged();
        });
    });
}

// ============================================
// 新功能處理函數
// ============================================

/**
 * 🚫 展开/折叠详情行（已禁用 2026-01-09）
 * 用戶要求移除編輯表單面板功能
 */
function toggleDetails(index) {
    // 功能已禁用
    console.log('⚠️ toggleDetails 功能已禁用');
    return;
}

/**
 * 🚫 全部展开/收起（已禁用 2026-01-09）
 */
function toggleAllDetails() {
    // 功能已禁用
    console.log('⚠️ toggleAllDetails 功能已禁用');
    return;
}

/**
 * 更新详情字段
 */
function updateDetailField(index, field, value) {
    console.log(`📝 更新交易 ${index} 的 ${field}:`, value);
    
    if (!currentDocument || !currentDocument.processedData) return;
    
    const transactions = currentDocument.processedData.transactions || [];
    if (transactions[index]) {
        transactions[index][field] = value;
        
        // 同步更新主表格中的字段
        const mainCell = document.querySelector(`.transaction-row[data-index="${index}"] .editable-cell[data-field="${field}"]`);
        if (mainCell) {
            mainCell.textContent = value;
        }
        
        // 保存到 Firestore
        saveTransactionChanges();
    }
}

/**
 * 展開/折疊備注行（旧版，保留兼容）
 */
function toggleMemo(index) {
    // 🚫 功能已禁用（2026-01-09）
    console.log('⚠️ toggleMemo 功能已禁用');
    return;
}

/**
 * 處理分類更改
 */
function handleCategoryChange(index, category) {
    console.log(`📁 更新交易 ${index} 的分類:`, category);
    
    if (!currentDocument || !currentDocument.processedData) return;
    
    const transactions = currentDocument.processedData.transactions || [];
    if (transactions[index]) {
        transactions[index].category = category;
        
        // 同步更新主表格中的下拉菜单
        const mainSelect = document.querySelector(`.transaction-row[data-index="${index}"] .category-select`);
        if (mainSelect && mainSelect !== event.target) {
            mainSelect.value = category;
        }
        
        // 🚫 詳情行同步代碼已移除（2026-01-09）
        
        // 保存到 Firestore
        saveTransactionChanges();
    }
}

/**
 * 處理對賬狀態更改
 */
function handleReconciledChange(index, reconciled) {
    console.log(`✓ 更新交易 ${index} 的對賬狀態:`, reconciled);
    
    if (!currentDocument || !currentDocument.processedData) return;
    
    const transactions = currentDocument.processedData.transactions || [];
    if (transactions[index]) {
        transactions[index].reconciled = reconciled;
        
        // 同步更新主表格中的复选框
        const mainCheckbox = document.querySelector(`.transaction-row[data-index="${index}"] .reconciled-checkbox`);
        if (mainCheckbox && mainCheckbox !== event.target) {
            mainCheckbox.checked = reconciled;
            mainCheckbox.title = reconciled ? t('reconciled') : t('unreconciled');
        }
        
        // 🚫 詳情行同步代碼已移除（2026-01-09）
        
        // 保存到 Firestore
        saveTransactionChanges();
    }
}

/**
 * 處理備注更改
 */
function handleMemoChange(index, memo) {
    console.log(`📝 更新交易 ${index} 的備注:`, memo);
    
    if (!currentDocument || !currentDocument.processedData) return;
    
    const transactions = currentDocument.processedData.transactions || [];
    if (transactions[index]) {
        transactions[index].memo = memo;
        
        // 保存到 Firestore
        saveTransactionChanges();
    }
}

/**
 * 處理附件操作
 */
function handleAttachment(index) {
    console.log(`📎 處理交易 ${index} 的附件`);
    
    const icon = document.querySelector(`.attachment-icon[onclick*="${index}"]`);
    const hasAttachment = icon && icon.classList.contains('has-attachment');
    
    if (hasAttachment) {
        // 查看附件（未來功能）
        alert('查看附件功能即將推出...');
    } else {
        // 上傳附件（未來功能）
        alert('上傳附件功能即將推出...\n\n提示：您可以使用文件管理系統上傳收據、發票等附件。');
    }
}

// ============================================
// 工具函數
// ============================================

function formatCurrency(amount) {
    const num = parseFloat(amount) || 0;
    return '$' + num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ✅ 確認刪除交易記錄
function confirmDeleteTransaction(index) {
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    const transaction = currentDocument.processedData.transactions[index];
    if (!transaction) {
        console.error(`❌ 找不到交易 ${index}`);
        return;
    }
    
    // 顯示確認對話框
    const description = transaction.description || '此交易';
    const amount = transaction.amount || 0;
    const formattedAmount = Math.abs(amount).toLocaleString('en-US', { 
        minimumFractionDigits: 2, 
        maximumFractionDigits: 2 
    });
    
    const confirmed = confirm(
        `確定要刪除此交易記錄嗎？\n\n` +
        `描述：${description}\n` +
        `金額：${amount >= 0 ? '+' : '-'}${formattedAmount}\n\n` +
        `此操作無法撤銷！`
    );
    
    if (confirmed) {
        deleteTransaction(index);
    }
}

// ✅ 刪除交易記錄
function deleteTransaction(index) {
    console.log(`🗑️ 刪除交易 ${index}`);
    
    if (!currentDocument || !currentDocument.processedData || !currentDocument.processedData.transactions) {
        console.error('❌ 無法找到交易數據');
        return;
    }
    
    // 從數組中刪除
    currentDocument.processedData.transactions.splice(index, 1);
    
    // 更新 UI
    displayDocumentContent();
    
    // 標記為有未保存更改
    markAsChanged();
    
    console.log(`✅ 交易 ${index} 已刪除`);
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

