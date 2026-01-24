/**
 * 用户菜单管理器 (User Menu Manager)
 * 作用: 统一管理所有页面的用户菜单逻辑，避免在每个 HTML 中重复定义
 * 版本: 1.0.0
 * 日期: 2026-01-23
 * 
 * 功能:
 *   - 用户登录状态检测
 *   - 用户头像显示
 *   - 下拉菜单管理
 *   - Credits 信息获取
 * 
 * 依赖:
 *   - window.simpleAuth (认证系统)
 *   - window.simpleDataManager (数据管理)
 *   - logger.js (日志工具)
 */

(function() {
    'use strict';
    
    // 用户信息缓存
    let userEmail = '';
    let userDisplayName = '';
    let userCredits = 0;
    
    /**
     * 获取用户首字母
     * 用于显示在头像中
     */
    function getUserInitial() {
        if (userDisplayName && userDisplayName !== '') {
            return userDisplayName.charAt(0).toUpperCase();
        }
        if (userEmail && userEmail !== '') {
            return userEmail.charAt(0).toUpperCase();
        }
        return 'U'; // 默认字母
    }
    
    /**
     * 切换下拉菜单
     */
    function toggleDropdown() {
        const dropdown = document.getElementById('user-dropdown');
        if (!dropdown) {
            logger.warn('下拉菜单元素未找到');
            return;
        }
        
        const isHidden = dropdown.style.display === 'none' || !dropdown.style.display;
        dropdown.style.display = isHidden ? 'block' : 'none';
        
        if (isHidden) {
            // 延迟绑定外部点击事件，避免立即触发
            setTimeout(() => {
                document.addEventListener('click', closeDropdownOutside);
            }, 10);
        }
    }
    
    /**
     * 点击外部关闭下拉菜单
     */
    function closeDropdownOutside(event) {
        const dropdown = document.getElementById('user-dropdown');
        const userMenu = document.getElementById('user-menu');
        
        if (dropdown && !dropdown.contains(event.target) && 
            (!userMenu || !userMenu.contains(event.target))) {
            dropdown.style.display = 'none';
            document.removeEventListener('click', closeDropdownOutside);
        }
    }
    
    /**
     * 更新用户菜单
     * 根据登录状态显示不同的内容
     */
    async function updateUserMenu() {
        const userMenu = document.getElementById('user-menu');
        if (!userMenu) {
            logger.warn('用户菜单元素未找到');
            return;
        }
        
        try {
            const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
            
            if (isLoggedIn) {
                // 已登录：显示用户头像
                const currentUser = window.simpleAuth.getCurrentUser();
                userEmail = currentUser.email || '';
                userDisplayName = currentUser.displayName || '';
                
                logger.log('用户已登录:', userEmail);
                
                // 从 Firestore 获取完整用户信息
                if (window.simpleDataManager && window.simpleDataManager.initialized) {
                    try {
                        const userDoc = await window.simpleDataManager.getUserDocument();
                        if (userDoc) {
                            userDisplayName = userDoc.displayName || userDisplayName;
                            userCredits = userDoc.credits || 0;
                            logger.log('从 Firestore 获取 Credits:', userCredits);
                        }
                    } catch (error) {
                        logger.error('无法从 Firestore 获取用户资料:', error);
                    }
                } else {
                    logger.log('SimpleDataManager 尚未初始化');
                }
                
                const userInitial = getUserInitial();
                logger.log('用户首字母:', userInitial);
                
                // 渲染用户头像
                userMenu.innerHTML = `
                    <div onclick="toggleDropdown()" class="user-menu-trigger">
                        <div class="user-avatar">${userInitial}</div>
                    </div>
                `;
                
                logger.log('用户菜单已更新');
            } else {
                // 未登录：显示登录按钮
                userMenu.innerHTML = `
                    <button onclick="window.location.href='auth.html'" class="login-button">
                        登入
                    </button>
                `;
                logger.log('显示登录按钮');
            }
        } catch (e) {
            logger.error('更新用户菜单失败:', e);
        }
    }
    
    /**
     * 初始化用户菜单
     */
    function initUserMenu() {
        logger.log('初始化用户菜单管理器');
        
        // 立即更新一次
        updateUserMenu();
        
        // 监听认证相关事件
        window.addEventListener('firebase-ready', () => {
            logger.log('Firebase 就绪，更新用户菜单');
            updateUserMenu();
        });
        
        window.addEventListener('user-logged-in', () => {
            logger.log('用户登录事件，更新用户菜单');
            updateUserMenu();
        });
        
        window.addEventListener('user-logged-out', () => {
            logger.log('用户登出事件，更新用户菜单');
            updateUserMenu();
        });
    }
    
    // 等待 DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUserMenu);
    } else {
        initUserMenu();
    }
    
    // 暴露到全局（兼容现有代码）
    window.toggleDropdown = toggleDropdown;
    window.updateUserMenu = updateUserMenu;
    window.getUserInitial = getUserInitial;
    
    // 新的命名空间方式（推荐）
    window.VaultCaddy = window.VaultCaddy || {};
    window.VaultCaddy.userMenu = {
        toggle: toggleDropdown,
        update: updateUserMenu,
        getInitial: getUserInitial,
        getUserEmail: () => userEmail,
        getUserDisplayName: () => userDisplayName,
        getUserCredits: () => userCredits
    };
    
    logger.log('用户菜单管理器已加载');
})();

