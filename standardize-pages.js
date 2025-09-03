/**
 * VaultCaddy 頁面標準化腳本
 * 用於統一所有頁面的基本結構和功能
 */

// 標準頁面模板
const STANDARD_HEAD_TEMPLATE = `
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="VaultCaddy - AI-powered document processing platform">
<meta property="og:title" content="{{TITLE}} - VaultCaddy">
<meta property="og:description" content="VaultCaddy - Professional document processing with AI technology">
<meta property="og:url" content="https://vaultcaddy.com">
<meta property="og:type" content="website">
<link rel="canonical" href="https://vaultcaddy.com">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="dashboard.css">
<link rel="stylesheet" href="pages.css">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<script src="translations.js"></script>
<script src="unified-auth.js"></script>
<script src="navbar-component.js"></script>
`;

// 標準導航HTML
const STANDARD_NAVBAR = `
<!-- 導航欄 - 由 navbar-component.js 動態載入 -->
<div id="navbar-placeholder"></div>
`;

// 需要標準化的頁面列表
const PAGES_TO_STANDARDIZE = [
    'account.html',
    'billing.html', 
    'terms.html',
    'privacy.html',
    'result.html',
    'auth.html'
];

// 頁面特定設定
const PAGE_CONFIGS = {
    'account.html': {
        title: 'Account Settings',
        description: 'Manage your VaultCaddy account settings and profile information'
    },
    'billing.html': {
        title: 'Billing & Plans',
        description: 'View and manage your VaultCaddy subscription and billing information'
    },
    'terms.html': {
        title: 'Terms of Service',
        description: 'VaultCaddy Terms of Service and usage conditions'
    },
    'privacy.html': {
        title: 'Privacy Policy',
        description: 'VaultCaddy Privacy Policy and data protection information'
    },
    'result.html': {
        title: 'Processing Results',
        description: 'View your document processing results and download files'
    },
    'auth.html': {
        title: 'Authentication',
        description: 'Sign in to your VaultCaddy account'
    }
};

// 實用函數
const utils = {
    // 檢查頁面是否需要更新
    checkPageNeedsUpdate: function(pageContent, pageName) {
        const config = PAGE_CONFIGS[pageName];
        const hasStandardMeta = pageContent.includes('property="og:title"');
        const hasUnifiedAuth = pageContent.includes('unified-auth.js');
        const hasNavbarPlaceholder = pageContent.includes('navbar-placeholder');
        
        return !hasStandardMeta || !hasUnifiedAuth || !hasNavbarPlaceholder;
    },
    
    // 生成標準化的head內容
    generateStandardHead: function(pageName) {
        const config = PAGE_CONFIGS[pageName];
        return STANDARD_HEAD_TEMPLATE
            .replace('{{TITLE}}', config.title)
            .replace('VaultCaddy - AI-powered document processing platform', config.description);
    },
    
    // 檢查功能完整性
    checkFunctionality: function(pageContent) {
        const functions = {
            hasLoginCheck: pageContent.includes('checkLoginStatus'),
            hasNavbarInit: pageContent.includes('navbar-component.js'),
            hasErrorHandling: pageContent.includes('try') && pageContent.includes('catch'),
            hasLoadingStates: pageContent.includes('loading') || pageContent.includes('Loading')
        };
        
        return functions;
    }
};

// 頁面統一檢查清單
const STANDARDIZATION_CHECKLIST = {
    meta_tags: '✅ 統一Meta Tags',
    css_loading: '✅ 標準CSS載入順序', 
    js_loading: '✅ 統一JavaScript檔案',
    navbar_system: '✅ 使用navbar-component.js',
    auth_system: '✅ 使用unified-auth.js',
    error_handling: '✅ 錯誤處理機制',
    loading_states: '✅ 載入狀態顯示',
    responsive_design: '✅ 響應式設計',
    accessibility: '✅ 無障礙功能',
    seo_optimization: '✅ SEO優化'
};

console.log('📋 VaultCaddy 頁面標準化腳本已載入');
console.log('🎯 標準化清單：', STANDARDIZATION_CHECKLIST);
console.log('📄 需要處理的頁面：', PAGES_TO_STANDARDIZE);
