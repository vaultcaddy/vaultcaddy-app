/**
 * VaultCaddy 導航欄內容管理器
 * 實現上方導航也使用單頁應用模式
 */

class NavbarContentManager {
    constructor() {
        this.currentPage = 'home';
        this.contentCache = new Map();
        this.init();
    }
    
    init() {
        this.bindNavbarEvents();
        this.setupNavbarRouting();
    }
    
    // 綁定導航欄事件
    bindNavbarEvents() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.isNavbarLink(link)) {
                e.preventDefault();
                this.handleNavbarClick(link);
            }
        });
    }
    
    // 檢查是否為導航欄連結
    isNavbarLink(link) {
        const href = link.getAttribute('href');
        const navbarPages = ['#features', '#pricing', 'index.html'];
        
        // 檢查Solutions下拉選單中的連結
        if (link.closest('.solutions-menu')) {
            return true;
        }
        
        // 檢查主導航連結
        return navbarPages.some(page => href && href.includes(page));
    }
    
    // 處理導航欄點擊
    handleNavbarClick(link) {
        const href = link.getAttribute('href');
        
        // 處理Solutions下拉選單
        if (link.closest('.solutions-menu')) {
            // 關閉下拉選單
            this.closeSolutionsDropdown();
            return; // Solutions連結已經指向dashboard.html，讓它正常跳轉
        }
        
        // 處理主頁導航
        if (href.includes('index.html') || href === '#features' || href === '#pricing') {
            this.navigateToMainPage(href);
        }
    }
    
    // 導航到主頁面
    navigateToMainPage(href) {
        // 如果當前在Dashboard頁面，需要跳轉到主頁
        if (window.location.pathname.includes('dashboard.html')) {
            if (href.includes('#features')) {
                window.location.href = 'index.html#features';
            } else if (href.includes('#pricing')) {
                window.location.href = 'index.html#pricing';
            } else {
                window.location.href = 'index.html';
            }
        } else {
            // 在主頁內的導航
            if (href === '#features') {
                this.scrollToSection('features');
            } else if (href === '#pricing') {
                this.scrollToSection('pricing');
            }
        }
    }
    
    // 滾動到指定區域
    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    // 關閉Solutions下拉選單
    closeSolutionsDropdown() {
        const dropdown = document.getElementById('solutions-menu');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    }
    
    // 設置路由
    setupNavbarRouting() {
        // 監聽頁面載入
        window.addEventListener('load', () => {
            this.handlePageLoad();
        });
        
        // 監聽Hash變化
        window.addEventListener('hashchange', () => {
            this.handleHashChange();
        });
    }
    
    // 處理頁面載入
    handlePageLoad() {
        const hash = window.location.hash;
        if (hash && !window.location.pathname.includes('dashboard.html')) {
            // 在主頁且有hash，滾動到對應區域
            setTimeout(() => {
                const sectionId = hash.replace('#', '');
                this.scrollToSection(sectionId);
            }, 500);
        }
    }
    
    // 處理Hash變化
    handleHashChange() {
        if (!window.location.pathname.includes('dashboard.html')) {
            const hash = window.location.hash;
            if (hash) {
                const sectionId = hash.replace('#', '');
                this.scrollToSection(sectionId);
            }
        }
    }
}

// 全局導出
window.NavbarContentManager = NavbarContentManager;

// 自動初始化
document.addEventListener('DOMContentLoaded', function() {
    if (!window.navbarContentManager) {
        window.navbarContentManager = new NavbarContentManager();
    }
});

console.log('📄 Navbar Content Manager 載入完成');
