// 語言選擇器 - VaultCaddy 多語言支持
// Language Selector Component for VaultCaddy

(function() {
    'use strict';
    
    // 支持的語言列表
    const SUPPORTED_LANGUAGES = {
        'zh': { name: '繁體中文', flag: '🇭🇰', dir: '' },
        'en': { name: 'English', flag: '🇬🇧', dir: 'en' },
        'jp': { name: '日本語', flag: '🇯🇵', dir: 'jp' },
        'kr': { name: '한국어', flag: '🇰🇷', dir: 'kr' }
    };
    
    // 檢測當前語言
    function getCurrentLanguage() {
        const path = window.location.pathname;
        const match = path.match(/^\/(en|jp|kr)\//);
        return match ? match[1] : 'zh';
    }
    
    // 獲取當前頁面的路徑（不包含語言前綴）
    function getPagePath() {
        const path = window.location.pathname;
        // 移除語言前綴
        return path.replace(/^\/(en|jp|kr)\//, '/');
    }
    
    // 切換語言
    function switchLanguage(newLang) {
        const currentLang = getCurrentLanguage();
        if (currentLang === newLang) return;
        
        const pagePath = getPagePath();
        const newPath = newLang === 'zh' ? pagePath : `/${newLang}${pagePath}`;
        
        // 保存語言選擇到 localStorage
        localStorage.setItem('vaultcaddy_language', newLang);
        
        // 跳轉到新語言頁面
        window.location.href = newPath;
    }
    
    // 創建語言選擇器 HTML
    function createLanguageSelector() {
        const currentLang = getCurrentLanguage();
        const currentLangInfo = SUPPORTED_LANGUAGES[currentLang];
        
        const selectorHTML = `
            <div id="language-selector" style="position: relative; display: inline-block;">
                <button id="language-btn" style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    background: transparent;
                    border: 2px solid #e5e7eb;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 0.875rem;
                    font-weight: 600;
                    color: #374151;
                    transition: all 0.2s;
                " onmouseover="this.style.borderColor='#667eea'; this.style.background='#f9fafb'" 
                   onmouseout="this.style.borderColor='#e5e7eb'; this.style.background='transparent'">
                    <span style="font-size: 1.25rem;">${currentLangInfo.flag}</span>
                    <span>${currentLangInfo.name}</span>
                    <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
                </button>
                
                <div id="language-dropdown" style="
                    display: none;
                    position: absolute;
                    top: calc(100% + 0.5rem);
                    right: 0;
                    background: white;
                    border: 2px solid #e5e7eb;
                    border-radius: 8px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                    min-width: 160px;
                    z-index: 1000;
                    overflow: hidden;
                ">
                    ${Object.entries(SUPPORTED_LANGUAGES).map(([code, info]) => `
                        <button onclick="window.VaultCaddyLanguage.switch('${code}')" style="
                            width: 100%;
                            display: flex;
                            align-items: center;
                            gap: 0.75rem;
                            padding: 0.75rem 1rem;
                            background: ${code === currentLang ? '#f3f4f6' : 'white'};
                            border: none;
                            cursor: pointer;
                            font-size: 0.875rem;
                            font-weight: ${code === currentLang ? '600' : '500'};
                            color: #374151;
                            transition: background 0.2s;
                            text-align: left;
                        " onmouseover="if('${code}' !== '${currentLang}') this.style.background='#f9fafb'" 
                           onmouseout="if('${code}' !== '${currentLang}') this.style.background='white'">
                            <span style="font-size: 1.25rem;">${info.flag}</span>
                            <span>${info.name}</span>
                            ${code === currentLang ? '<i class="fas fa-check" style="margin-left: auto; color: #667eea;"></i>' : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
        
        return selectorHTML;
    }
    
    // 初始化語言選擇器
    function init() {
        // 等待 DOM 加載完成
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }
        
        // 檢查是否已經初始化
        if (window.VaultCaddyLanguage && window.VaultCaddyLanguage.initialized) {
            return;
        }
        
        console.log('🌍 初始化語言選擇器');
        
        // 查找語言選擇器容器（桌面版和手機版）
        const desktopContainer = document.getElementById('language-selector-desktop');
        const mobileContainer = document.getElementById('language-selector-mobile');
        
        const selectorHTML = createLanguageSelector();
        
        if (desktopContainer) {
            desktopContainer.innerHTML = selectorHTML;
            console.log('✅ 桌面版語言選擇器已添加');
        }
        
        if (mobileContainer) {
            mobileContainer.innerHTML = selectorHTML;
            console.log('✅ 手機版語言選擇器已添加');
        }
        
        // 添加點擊事件監聽器
        setTimeout(() => {
            const buttons = document.querySelectorAll('#language-btn');
            buttons.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const dropdown = this.nextElementSibling;
                    const isVisible = dropdown.style.display === 'block';
                    
                    // 關閉所有下拉菜單
                    document.querySelectorAll('#language-dropdown').forEach(d => {
                        d.style.display = 'none';
                    });
                    
                    // 切換當前下拉菜單
                    dropdown.style.display = isVisible ? 'none' : 'block';
                });
            });
            
            // 點擊外部關閉下拉菜單
            document.addEventListener('click', function() {
                document.querySelectorAll('#language-dropdown').forEach(dropdown => {
                    dropdown.style.display = 'none';
                });
            });
        }, 100);
        
        // 暴露 API
        window.VaultCaddyLanguage = {
            initialized: true,
            switch: switchLanguage,
            current: getCurrentLanguage,
            supported: SUPPORTED_LANGUAGES
        };
        
        console.log('✅ 語言選擇器初始化完成');
    }
    
    // 自動初始化
    init();
})();

