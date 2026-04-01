/**
 * Google Ads 轉換追蹤腳本
 * 
 * 功能：
 * 1. 當用戶訪問 dashboard.html 時觸發轉換
 * 2. 當用戶訪問 firstproject.html 時觸發轉換
 * 3. 確保轉換事件正確發送到 Google Ads
 * 
 * @version 1.0
 * @date 2026-02-13
 */

(function() {
    'use strict';
    
    // 等待頁面完全加載
    function initConversionTracking() {
        // 檢查是否在目標頁面
        const currentPath = window.location.pathname;
        const isDashboard = currentPath.includes('dashboard.html');
        const isFirstProject = currentPath.includes('firstproject.html');
        
        if (!isDashboard && !isFirstProject) {
            return; // 不在目標頁面，不執行
        }
        
        // 等待 Firebase Auth 初始化（最多等待 5 秒）
        let checkCount = 0;
        const maxChecks = 50; // 5秒 (50 * 100ms)
        
        function checkAuthAndTrack() {
            checkCount++;
            
            // 檢查用戶是否已登入
            const isAuthenticated = (
                (window.simpleAuth && window.simpleAuth.currentUser) ||
                (window.firebase && window.firebase.auth && window.firebase.auth().currentUser)
            );
            
            if (isAuthenticated) {
                // 用戶已登入，觸發轉換
                triggerConversion(isDashboard ? 'dashboard_visit' : 'firstproject_visit');
            } else if (checkCount < maxChecks) {
                // 還未登入，繼續等待
                setTimeout(checkAuthAndTrack, 100);
            } else {
                // 超時，但還是嘗試觸發（可能用戶已登入但檢查失敗）
                console.log('⚠️ 轉換追蹤：無法確認登入狀態，但將觸發轉換事件');
                triggerConversion(isDashboard ? 'dashboard_visit' : 'firstproject_visit');
            }
        }
        
        // 開始檢查
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(checkAuthAndTrack, 500); // 等待 500ms 讓 Firebase 初始化
            });
        } else {
            setTimeout(checkAuthAndTrack, 500);
        }
    }
    
    /**
     * 觸發轉換事件
     * @param {string} eventLabel - 事件標籤
     */
    function triggerConversion(eventLabel) {
        try {
            console.log('📊 開始發送 Google Ads 轉換事件:', eventLabel);
            
            // 方法 1: 使用 dataLayer（最可靠，即使 gtag 未加載也能工作）
            if (window.dataLayer) {
                // 發送自定義轉換事件（用於 Google Ads）
                window.dataLayer.push({
                    'event': 'manual_event_PURCHASE',
                    'event_category': 'conversion',
                    'event_label': eventLabel,
                    'value': 1,
                    'currency': 'HKD',
                    'page_path': window.location.pathname,
                    'page_title': document.title
                });
                console.log('✅ 轉換事件已發送到 dataLayer: manual_event_PURCHASE');
                
                // 同時發送標準 GA4 事件
                window.dataLayer.push({
                    'event': 'page_view_conversion',
                    'event_category': 'conversion',
                    'event_label': eventLabel,
                    'value': 1,
                    'currency': 'HKD'
                });
                console.log('✅ GA4 事件已發送到 dataLayer: page_view_conversion');
            }
            
            // 方法 2: 使用 gtag（如果已加載）
            if (typeof gtag !== 'undefined') {
                // 發送自定義轉換事件
                gtag('event', 'manual_event_PURCHASE', {
                    'event_category': 'conversion',
                    'event_label': eventLabel,
                    'value': 1,
                    'currency': 'HKD',
                    'page_path': window.location.pathname,
                    'page_title': document.title
                });
                console.log('✅ 轉換事件已發送到 gtag: manual_event_PURCHASE');
                
                // 發送標準 GA4 事件
                gtag('event', 'page_view_conversion', {
                    'event_category': 'conversion',
                    'event_label': eventLabel,
                    'value': 1,
                    'currency': 'HKD'
                });
                console.log('✅ GA4 事件已發送到 gtag: page_view_conversion');
            }
            
            // 方法 3: 發送 sign_up 事件（如果這是首次訪問）
            if (eventLabel === 'dashboard_visit') {
                // 檢查是否為首次訪問（使用 sessionStorage）
                const conversionKey = 'vaultcaddy_conversion_tracked';
                if (!sessionStorage.getItem(conversionKey)) {
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'sign_up', {
                            'method': 'page_visit',
                            'value': 1,
                            'currency': 'HKD'
                        });
                        console.log('✅ 標準 sign_up 事件已發送');
                    }
                    
                    // 標記已追蹤（避免重複觸發）
                    sessionStorage.setItem(conversionKey, 'true');
                }
            }
            
            console.log('✅ 轉換追蹤完成:', eventLabel);
            
        } catch (error) {
            console.error('❌ 轉換追蹤錯誤:', error);
        }
    }
    
    // 初始化
    initConversionTracking();
    
    // 如果頁面是動態加載的，也監聽路由變化
    if (window.addEventListener) {
        window.addEventListener('popstate', function() {
            setTimeout(initConversionTracking, 100);
        });
    }
    
})();
