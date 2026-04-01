// Instagram WebView 兼容性脚本
// 用于修复 Instagram 内置浏览器加载问题

(function() {
    'use strict';
    
    // 1. 检测 Instagram/Facebook WebView
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    const isInstagram = userAgent.indexOf('Instagram') > -1;
    const isFBWebView = userAgent.indexOf('FBAN') > -1 || userAgent.indexOf('FBAV') > -1;
    const isSocialWebView = isInstagram || isFBWebView;
    
    console.log('🔍 检测浏览器环境:', {
        userAgent: userAgent,
        isInstagram: isInstagram,
        isFBWebView: isFBWebView,
        isSocialWebView: isSocialWebView
    });
    
    if (isSocialWebView) {
        console.log('📱 检测到社交媒体内置浏览器，启用兼容模式');
        
        // 2. 添加超时保护 - 如果Firebase 3秒内未加载完成，直接显示页面
        let firebaseLoaded = false;
        let pageDisplayed = false;
        
        // 3秒超时
        setTimeout(function() {
            if (!firebaseLoaded && !pageDisplayed) {
                console.warn('⚠️ Firebase 加载超时，直接显示页面内容');
                displayPageContent();
            }
        }, 3000);
        
        // 3. 监听Firebase加载完成
        window.addEventListener('firebase-ready', function() {
            console.log('✅ Firebase 加载完成');
            firebaseLoaded = true;
            displayPageContent();
        });
        
        // 4. 确保页面内容可见
        function displayPageContent() {
            if (pageDisplayed) return;
            pageDisplayed = true;
            
            // 移除所有loading遮罩
            const loadingElements = document.querySelectorAll('.loading, .loading-overlay, [data-loading]');
            loadingElements.forEach(el => {
                el.style.display = 'none';
                el.remove();
            });
            
            // 确保body可见
            document.body.style.visibility = 'visible';
            document.body.style.opacity = '1';
            
            // 触发内容显示事件
            window.dispatchEvent(new CustomEvent('content-ready'));
            console.log('✅ 页面内容已显示');
        }
        
        // 5. 页面加载完成后立即显示
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(displayPageContent, 500);
            });
        } else {
            setTimeout(displayPageContent, 500);
        }
        
        // 6. 简化Firebase初始化（如果失败，继续显示页面）
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch.apply(this, args)
                .catch(function(error) {
                    console.warn('⚠️ Fetch 请求失败（Instagram 环境）:', error);
                    // 不阻止页面显示
                    displayPageContent();
                    throw error;
                });
        };
        
        // 7. 添加全局错误处理
        window.addEventListener('error', function(event) {
            console.error('❌ 全局错误:', event.error);
            // 即使有错误，也尝试显示页面
            displayPageContent();
        });
        
        // 8. 添加 Promise rejection 处理
        window.addEventListener('unhandledrejection', function(event) {
            console.error('❌ Promise rejection:', event.reason);
            // 即使有错误，也尝试显示页面
            displayPageContent();
        });
    }
    
    // 9. 通用优化：加快首屏渲染
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // 预加载关键资源
            const criticalImages = document.querySelectorAll('img[data-critical]');
            criticalImages.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        });
    }
    
    console.log('✅ Instagram 兼容性脚本加载完成');
})();

