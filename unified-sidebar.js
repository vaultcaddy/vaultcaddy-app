/**
 * 統一左側欄系統
 * 用於 Dashboard, Account, Billing, FirstProject 頁面
 * 功能：顯示項目列表、搜索、配置鏈接
 */

(function() {
    'use strict';
    
    console.log('🔵 unified-sidebar.js 載入');
    
    let currentProjects = [];
    
    /**
     * 渲染左側欄 HTML
     */
    function renderSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) {
            console.error('❌ 找不到 .sidebar 元素');
            return;
        }
        
        const currentPath = window.location.pathname;
        const isAccountPage = currentPath.includes('account.html');
        const isBillingPage = currentPath.includes('billing.html');
        
        sidebar.innerHTML = `
            <div style="display: flex; flex-direction: column; height: 100%; padding: 1.5rem; padding-top: calc(1.5rem + 10pt);">
                
                <!-- 搜索欄 -->
                <div style="margin-bottom: 1.5rem;">
                    <input type="text" id="sidebar-project-search" placeholder="篩選文檔名稱..." style="width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 6px; font-size: 0.875rem; color: #6b7280; outline: none; transition: border 0.2s;" onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#e5e7eb'">
                </div>
                
                <!-- Project 區塊 -->
                <div style="flex: 1; margin-bottom: 1.5rem; overflow-y: auto;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                        <span style="font-size: 0.875rem; font-weight: 500; color: #6b7280;">project</span>
                        <button onclick="if(window.openCreateProjectModal) window.openCreateProjectModal()" style="background: none; border: none; color: #6b7280; cursor: pointer; font-size: 1.25rem; padding: 0; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;">+</button>
                    </div>
                    <div id="sidebar-projects-list">
                        <div style="padding: 2rem 1rem; text-align: center; color: #9ca3af;">
                            <i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;"></i>
                            <div style="font-size: 0.875rem;">載入中...</div>
                        </div>
                    </div>
                </div>
                
                <!-- 配置區塊 (底部) -->
                <div style="border-top: 1px solid #e5e7eb; padding-top: 1rem;">
                    <h3 style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 0.75rem 0;">配置</h3>
                    <div onclick="window.location.href='/account.html'" class="sidebar-nav-link ${isAccountPage ? 'active' : ''}" style="display: flex; align-items: center; padding: 0.5rem; color: ${isAccountPage ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; margin-bottom: 0.25rem; ${isAccountPage ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}" onmouseover="if(!this.classList.contains('active')) this.style.background='#f3f4f6'" onmouseout="if(!this.classList.contains('active')) this.style.background='transparent'">
                        <i class="fas fa-user" style="margin-right: 0.5rem; font-size: 1rem; width: 20px; color: ${isAccountPage ? '#2563eb' : 'inherit'};"></i>
                        <span style="font-size: 0.875rem;">帳戶</span>
                    </div>
                    <div onclick="window.location.href='/billing.html'" class="sidebar-nav-link ${isBillingPage ? 'active' : ''}" style="display: flex; align-items: center; padding: 0.5rem; color: ${isBillingPage ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; ${isBillingPage ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}" onmouseover="if(!this.classList.contains('active')) this.style.background='#f3f4f6'" onmouseout="if(!this.classList.contains('active')) this.style.background='transparent'">
                        <i class="fas fa-credit-card" style="margin-right: 0.5rem; font-size: 1rem; width: 20px; color: ${isBillingPage ? '#2563eb' : 'inherit'};"></i>
                        <span style="font-size: 0.875rem;">計費</span>
                    </div>
                </div>
            </div>
        `;
        
        console.log('✅ 左側欄 HTML 已渲染');
        
        // 綁定搜索事件
        bindSearchEvent();
    }
    
    /**
     * 載入項目列表
     */
    async function loadProjects() {
        console.log('🔵 loadProjects() 被調用');
        
        const projectsList = document.getElementById('sidebar-projects-list');
        if (!projectsList) {
            console.error('❌ 找不到 sidebar-projects-list 元素');
            return;
        }
        
        try {
            // 檢查 SimpleDataManager 是否就緒（不再輪詢等待）
            if (!window.simpleDataManager || !window.simpleDataManager.initialized) {
                console.warn('⚠️ SimpleDataManager 未就緒');
                projectsList.innerHTML = `
                    <div style="padding: 2rem 1rem; text-align: center; color: #9ca3af;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;"></i>
                        <div style="font-size: 0.875rem;">載入中...</div>
                    </div>
                `;
                return;
            }
            
            console.log('✅ SimpleDataManager 已就緒');
            
            // 獲取項目列表
            const projects = await window.simpleDataManager.getProjects();
            currentProjects = projects || [];
            
            if (currentProjects.length > 0) {
                console.log('🔵 獲取到的項目:', currentProjects);
                
                const urlParams = new URLSearchParams(window.location.search);
                const currentProjectId = urlParams.get('project');
                
                projectsList.innerHTML = currentProjects.map(project => {
                    const isActive = currentProjectId === project.id;
                    return `
                        <div class="project-item sidebar-project-item" onclick="window.location.href='/firstproject.html?project=${project.id}'" data-project-name="${project.name}" style="display: flex; align-items: center; padding: 0.5rem; color: ${isActive ? '#2563eb' : '#6b7280'}; cursor: pointer; border-radius: 4px; transition: background 0.2s; margin-bottom: 0.25rem; ${isActive ? 'background: #eff6ff; border-left: 3px solid #2563eb; margin-left: -1.5rem; padding-left: calc(0.5rem + 1.5rem - 3px);' : ''}" onmouseover="if(!this.classList.contains('active')) this.style.background='#f3f4f6'" onmouseout="if(!this.classList.contains('active')) this.style.background='transparent'">
                            <i class="fas fa-folder" style="margin-right: 0.5rem; font-size: 1rem; color: ${isActive ? '#2563eb' : 'inherit'};"></i>
                            <span class="project-name" style="font-size: 0.875rem;">${project.name}</span>
                        </div>
                    `;
                }).join('');
                
                console.log('✅ 項目列表已載入:', currentProjects.length, '個項目');
            } else {
                projectsList.innerHTML = `
                    <div style="padding: 2rem 1rem; text-align: center; color: #9ca3af;">
                        <i class="fas fa-folder-open" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;"></i>
                        <div style="font-size: 0.875rem;">沒有項目</div>
                    </div>
                `;
                console.log('⚠️ 沒有項目可載入');
            }
            
        } catch (error) {
            console.error('❌ 載入項目列表失敗:', error);
            projectsList.innerHTML = `
                <div style="padding: 2rem 1rem; text-align: center; color: #ef4444;">
                    <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.5;"></i>
                    <div style="font-size: 0.875rem;">載入失敗</div>
                </div>
            `;
        }
    }
    
    /**
     * 綁定搜索事件
     */
    function bindSearchEvent() {
        const searchInput = document.getElementById('sidebar-project-search');
        if (!searchInput) {
            console.error('❌ 找不到搜索輸入框');
            return;
        }
        
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();
            const projectItems = document.querySelectorAll('.sidebar-project-item');
            
            projectItems.forEach(item => {
                const projectName = item.getAttribute('data-project-name').toLowerCase();
                if (searchTerm === '' || projectName.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
        
        console.log('✅ 搜索事件已綁定');
    }
    
    /**
     * 初始化左側欄
     */
    async function init() {
        console.log('🔵 unified-sidebar.js init() 被調用');
        
        // 先渲染 HTML
        renderSidebar();
        
        // 等待 app-ready 再載入項目
        if (window.simpleDataManager && window.simpleDataManager.initialized) {
            await loadProjects();
        } else {
            console.log('⏳ 等待 app-ready 事件...');
            window.addEventListener('app-ready', async () => {
                console.log('✅ 收到 app-ready 事件，載入項目');
                await loadProjects();
            }, { once: true });
        }
        
        // 監聽項目變化
        window.addEventListener('projectCreated', loadProjects);
        window.addEventListener('projectDeleted', loadProjects);
        
        console.log('✅ unified-sidebar.js 初始化完成');
    }
    
    // DOM 載入完成後初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // 暴露到全局作用域（供其他腳本調用）
    window.unifiedSidebar = {
        reload: loadProjects
    };
    
})();

