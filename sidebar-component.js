/**
 * VaultCaddy 統一側邊欄組件
 * 用於所有Dashboard頁面的一致導航
 * Google Cloud Vision API Client ID: 672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com
 */

class VaultCaddySidebar {
    constructor(activePage = 'bank-statement') {
        this.activePage = activePage;
        this.init();
    }
    
    init() {
        console.log('🎨 Sidebar: init() 開始');
        
        // ❌ 不要立即渲染，等待 SimpleDataManager 就緒
        // this.render();
        
        this.bindEvents();
        this.loadStats();
        this.setupLanguageListener();
        this.setupProjectListener();
        
        // ✅ 延遲渲染，等待 SimpleDataManager 和 Auth 就緒
        // 注意：這是 async 函數，會在背景執行
        this.delayedRender().catch(err => {
            console.error('❌ Sidebar: delayedRender() 失敗:', err);
        });
        
        console.log('🎨 Sidebar: init() 完成（delayedRender 在背景執行）');
    }
    
    // ✅ 延遲渲染：等待 SimpleDataManager 和 Auth 就緒
    async delayedRender() {
        console.log('⏳ Sidebar: delayedRender() 開始執行...');
        console.log('   window.simpleDataManager:', !!window.simpleDataManager);
        console.log('   window.simpleDataManager?.initialized:', window.simpleDataManager?.initialized);
        console.log('   window.simpleDataManager?.currentUser:', window.simpleDataManager?.currentUser?.email || 'null');
        
        try {
            // 等待 SimpleDataManager 初始化
            const maxWait = 10000; // 最多等 10 秒
            const startTime = Date.now();
            
            console.log('⏳ Sidebar: 開始輪詢等待 SimpleDataManager...');
            
            while (Date.now() - startTime < maxWait) {
                if (window.simpleDataManager && window.simpleDataManager.initialized) {
                    console.log('✅ Sidebar: SimpleDataManager 已就緒');
                    console.log('   currentUser:', window.simpleDataManager.currentUser ? window.simpleDataManager.currentUser.email : 'null');
                    
                    // 再等待 Auth 狀態（增加到 5 秒）
                    console.log('⏳ Sidebar: 等待 Auth 狀態...');
                    const user = await this.waitForUser(window.simpleDataManager, 5000);
                    if (user) {
                        console.log('✅ Sidebar: Auth 已就緒，開始渲染');
                        await this.render();
                        console.log('✅ Sidebar: render() 完成');
                        return;
                    } else {
                        console.warn('⚠️ Sidebar: Auth 超時，使用空項目列表渲染');
                        await this.render();
                        console.log('✅ Sidebar: render() 完成（空列表）');
                        return;
                    }
                }
                
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            
            console.error('❌ Sidebar: SimpleDataManager 初始化超時（10秒）');
            // 仍然渲染，但項目列表為空
            await this.render();
            console.log('✅ Sidebar: render() 完成（超時後）');
            
        } catch (error) {
            console.error('❌ Sidebar: delayedRender() 發生錯誤:', error);
            console.error('   錯誤堆棧:', error.stack);
            throw error;
        }
    }
    
    setupProjectListener() {
        // 監聽項目創建事件
        window.addEventListener('projectCreated', () => {
            console.log('🔄 側邊欄: 檢測到新項目創建，重新渲染');
            this.render();
        });
        
        // 監聽項目刪除事件
        window.addEventListener('projectDeleted', () => {
            console.log('🔄 側邊欄: 檢測到項目刪除，重新渲染');
            this.render();
        });
    }
    
    // ✅ 等待用戶登入
    waitForUser(dataManager, timeout = 3000) {
        return new Promise((resolve) => {
            // 立即檢查
            if (dataManager.currentUser) {
                console.log('✅ 用戶已登入:', dataManager.currentUser.email);
                resolve(dataManager.currentUser);
                return;
            }
            
            // 輪詢檢查
            const startTime = Date.now();
            const checkInterval = setInterval(() => {
                if (dataManager.currentUser) {
                    clearInterval(checkInterval);
                    console.log('✅ 用戶已登入:', dataManager.currentUser.email);
                    resolve(dataManager.currentUser);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(checkInterval);
                    console.warn('⏱️ 等待用戶登入超時');
                    resolve(null);
                }
            }, 50);
        });
    }
    
    async render() {
        // 支持兩種容器：#sidebar-root（新版）和 .sidebar（舊版）
        const sidebarContainer = document.getElementById('sidebar-root') || document.querySelector('.sidebar');
        if (!sidebarContainer) {
            console.error('找不到側邊欄容器 #sidebar-root 或 .sidebar');
            return;
        }
        
        console.log('✅ 找到側邊欄容器:', sidebarContainer.id || sidebarContainer.className);
        
        // 設置側邊欄為 flexbox 布局（向下 10pt）
        sidebarContainer.style.cssText = 'width: 280px; background: #ffffff; border-right: 1px solid #e5e7eb; padding: 1.5rem; padding-top: calc(1.5rem + 10pt); display: flex; flex-direction: column; visibility: visible;';
        
        const sidebarHTML = await this.getSidebarHTML();
        sidebarContainer.innerHTML = sidebarHTML;
        console.log('✅ 側邊欄 HTML 已插入，長度:', sidebarHTML.length);
    }
    
    async getSidebarHTML() {
        // 🔥 優先從 Firebase 獲取項目列表
        let projects = [];
        
        // 使用 simpleDataManager（新版）或 firebaseDataManager（向後兼容）
        const dataManager = window.simpleDataManager || window.firebaseDataManager;
        
        if (dataManager && dataManager.initialized) {
            try {
                // ✅ 等待用戶登入（最多 5 秒，給更多時間）
                const user = await this.waitForUser(dataManager, 5000);
                if (user) {
                    projects = await dataManager.getProjects();
                    console.log('✅ 側邊欄從 Firebase 加載項目:', projects.length);
                } else {
                    console.warn('⚠️ 用戶未登入，側邊欄項目列表為空');
                    projects = [];
                }
            } catch (error) {
                console.error('❌ 從 Firebase 加載項目失敗:', error);
                projects = [];
            }
        } else {
            console.warn('⚠️ SimpleDataManager 未初始化，側邊欄項目列表為空');
            projects = [];
        }
        
        // 獲取當前項目 ID（從 URL 參數）
        const urlParams = new URLSearchParams(window.location.search);
        const currentProjectId = urlParams.get('project');
        
        // 檢查當前頁面
        const currentPage = window.location.pathname.split('/').pop();
        const isAccountPage = this.activePage === 'account' || currentPage === 'account.html';
        const isBillingPage = this.activePage === 'billing' || currentPage === 'billing.html';
        
        // 生成項目列表 HTML
        const projectsHTML = projects.map(project => {
            const isActive = currentProjectId === project.id;
            return `
            <div onclick="window.location.href='firstproject.html?project=${project.id}'" style="display: flex; align-items: center; padding: 0.5rem; color: ${isActive ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; margin-bottom: 0.25rem; ${isActive ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}">
                <i class="fas fa-folder" style="margin-right: 0.5rem; font-size: 1rem;"></i>
                <span style="font-size: 0.875rem;">${project.name}</span>
            </div>
        `;
        }).join('');
        
        return `
            <!-- 搜索欄 -->
            <div style="margin-bottom: 1.5rem;">
                <input type="text" id="project-search-input" placeholder="篩選文檔名稱..." style="width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 0.875rem; color: #6b7280;" oninput="if(window.filterProjects){console.log('🔍 觸發搜尋:', this.value); window.filterProjects(this.value);}else{console.error('❌ window.filterProjects 未定義');}">
            </div>
            
            <!-- Project 區塊 -->
            <div style="margin-bottom: auto;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <span style="font-size: 0.875rem; font-weight: 500; color: #6b7280;">project</span>
                    <button onclick="openCreateProjectModal()" style="background: none; border: none; color: #6b7280; cursor: pointer; font-size: 1.25rem; padding: 0; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;">+</button>
                </div>
                ${projectsHTML}
            </div>
            
            <!-- 配置區塊 (底部) -->
            <div style="border-top: 1px solid #e5e7eb; padding-top: 1rem;">
                <h3 style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.75rem 0;">配置</h3>
                <div onclick="window.location.href='account.html'" style="display: flex; align-items: center; padding: 0.5rem; color: ${isAccountPage ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; margin-bottom: 0.25rem; ${isAccountPage ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}">
                    <i class="fas fa-user" style="margin-right: 0.5rem; font-size: 1rem; width: 20px; color: ${isAccountPage ? '#2563eb' : '#6b7280'};"></i>
                    <span style="font-size: 0.875rem;">帳戶</span>
                </div>
                <div onclick="window.location.href='billing.html'" style="display: flex; align-items: center; padding: 0.5rem; color: ${isBillingPage ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; ${isBillingPage ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}">
                    <i class="fas fa-credit-card" style="margin-right: 0.5rem; font-size: 1rem; width: 20px; color: ${isBillingPage ? '#2563eb' : '#6b7280'};"></i>
                    <span style="font-size: 0.875rem;">計費</span>
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // 為側邊欄導航項目添加點擊事件
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('.sidebar .nav-item a');
            if (navLink) {
                e.preventDefault();
                const href = navLink.getAttribute('href');
                
                // 如果當前在文檔詳細視圖，先回到列表視圖
                const detailView = document.getElementById('document-detail-view');
                const listView = document.getElementById('document-list-view');
                
                if (detailView && listView) {
                    if (detailView.style.display !== 'none') {
                        // 隱藏詳細視圖，顯示列表視圖
                        detailView.style.display = 'none';
                        listView.style.display = 'block';
                    }
                }
                
                // 導航到新的hash
                window.location.href = href;
                
                console.log('側邊欄導航到:', href);
            }
        });
        
        // ✅ 設置全域篩選函數（增強版：確保正確工作）
        window.filterProjects = (searchTerm) => {
            console.log('🔍 篩選項目開始 ====================================');
            console.log('   搜尋詞:', searchTerm);
            
            const projectItems = document.querySelectorAll('.project-item');
            console.log('   找到項目數:', projectItems.length);
            
            if (projectItems.length === 0) {
                console.error('❌ 沒有找到任何 .project-item 元素！');
                console.log('   當前 DOM 中的所有 class 包含 project 的元素:');
                document.querySelectorAll('[class*="project"]').forEach(el => {
                    console.log('     -', el.className, el.textContent.substring(0, 50));
                });
                return;
            }
            
            const lowerSearchTerm = searchTerm.toLowerCase().trim();
            
            let visibleCount = 0;
            projectItems.forEach((item, index) => {
                // ✅ 嘗試多種方式提取項目名稱
                let projectName = '';
                
                // 方法1：查找不是圖標的 span
                const textSpan = item.querySelector('span:not(.fas):not(.fa)');
                if (textSpan) {
                    projectName = textSpan.textContent.toLowerCase().trim();
                } else {
                    // 方法2：直接取 textContent 並移除圖標
                    projectName = item.textContent.replace(/[\uf000-\uf8ff]/g, '').toLowerCase().trim();
                }
                
                console.log(`   [${index}] 項目: "${projectName}" | 搜尋: "${lowerSearchTerm}"`);
                
                const shouldShow = lowerSearchTerm === '' || projectName.includes(lowerSearchTerm);
                
                if (shouldShow) {
                    item.style.display = 'flex';
                    visibleCount++;
                    console.log(`       ✅ 顯示`);
                } else {
                    item.style.display = 'none';
                    console.log(`       ❌ 隱藏`);
                }
            });
            
            console.log(`✅ 篩選完成: 顯示 ${visibleCount}/${projectItems.length} 個項目`);
            console.log('🔍 篩選項目結束 ====================================');
        };
        
        console.log('側邊欄事件已綁定');
    }
    
    loadStats() {
        // 從VaultCaddyStats載入統計數據
        if (window.VaultCaddyStats) {
            window.VaultCaddyStats.updateDashboardDisplays();
        }
    }
    
    setupLanguageListener() {
        // 監聽語言變更事件
        window.addEventListener('languageChanged', (e) => {
            console.log('Sidebar: 語言已變更為', e.detail.language);
            // 重新渲染側邊欄以應用新的翻譯
            this.render();
            // 重新應用翻譯
            if (window.languageManager) {
                window.languageManager.loadLanguage(e.detail.language);
            }
        });
    }
    
    updateActivePage(activePage) {
        this.activePage = activePage;
        
        // 更新側邊欄中的活躍狀態
        const navItems = document.querySelectorAll('.sidebar .nav-item');
        navItems.forEach(item => {
            item.classList.remove('active');
            
            const link = item.querySelector('a');
            if (link) {
                const href = link.getAttribute('href');
                if (href === `dashboard.html#${activePage}`) {
                    item.classList.add('active');
                }
            }
        });
        
        console.log('✅ 側邊欄活躍頁面已更新:', activePage);
    }
}

// 導出類
window.VaultCaddySidebar = VaultCaddySidebar;
