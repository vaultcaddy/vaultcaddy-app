/**
 * 移动端菜单管理器 (Mobile Menu Manager)
 * 作用: 统一管理所有页面的移动端侧边栏逻辑
 * 版本: 1.0.0
 * 日期: 2026-01-23
 * 
 * 功能:
 *   - 打开/关闭移动端侧边栏
 *   - 处理触摸和点击事件
 *   - 管理页面滚动状态
 * 
 * 依赖:
 *   - logger.js (日志工具)
 */

(function() {
    'use strict';
    
    /**
     * 打开侧边栏
     */
    function openSidebar() {
        const overlay = document.getElementById('mobile-sidebar-overlay');
        if (overlay) {
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            logger.log('侧边栏已打开');
        } else {
            logger.warn('侧边栏 overlay 元素未找到');
        }
    }
    
    /**
     * 关闭侧边栏
     */
    function closeSidebar() {
        const overlay = document.getElementById('mobile-sidebar-overlay');
        if (overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = 'auto';
            logger.log('侧边栏已关闭');
        }
    }
    
    /**
     * 初始化移动端菜单
     */
    function initMobileMenu() {
        const btn = document.getElementById('mobile-menu-btn');
        const overlay = document.getElementById('mobile-sidebar-overlay');
        
        if (!btn || !overlay) {
            logger.log('移动端菜单元素未找到，200ms 后重试');
            setTimeout(initMobileMenu, 200);
            return;
        }
        
        logger.log('初始化移动端菜单');
        
        // 按钮点击事件
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            logger.log('移动端菜单按钮被点击');
            openSidebar();
        });
        
        // 触摸事件（移动设备）
        btn.addEventListener('touchend', (e) => {
            e.preventDefault();
            e.stopPropagation();
            logger.log('移动端菜单按钮被触摸');
            openSidebar();
        });
        
        // 点击 overlay 背景关闭
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                logger.log('点击背景，关闭侧边栏');
                closeSidebar();
            }
        });
        
        // 关闭按钮
        const closeBtn = overlay.querySelector('.close-sidebar');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                logger.log('点击关闭按钮');
                closeSidebar();
            });
        }
        
        logger.log('移动端菜单初始化完成');
    }
    
    // 等待 DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }
    
    // 暴露到全局
    window.VaultCaddy = window.VaultCaddy || {};
    window.VaultCaddy.mobileMenu = {
        open: openSidebar,
        close: closeSidebar,
        init: initMobileMenu
    };
    
    logger.log('移动端菜单管理器已加载');
})();

