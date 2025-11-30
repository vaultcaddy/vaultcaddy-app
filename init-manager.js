/**
 * 統一初始化管理器
 * 目的：協調所有組件的初始化順序，避免重複和延遲
 * 
 * 初始化順序：
 * 1. Firebase SDK
 * 2. SimpleAuth (認證)
 * 3. SimpleDataManager (數據)
 * 4. Unified Components (UI 組件)
 */

(function() {
    'use strict';
    
    console.log('🚀 InitManager: 開始載入');
    
    // 初始化狀態追蹤
    const initState = {
        firebase: false,
        auth: false,
        dataManager: false,
        ui: false
    };
    
    // 初始化完成回調列表
    const readyCallbacks = [];
    
    /**
     * 註冊初始化完成回調
     */
    window.onAppReady = function(callback) {
        if (typeof callback === 'function') {
            if (isFullyReady()) {
                callback();
            } else {
                readyCallbacks.push(callback);
            }
        }
    };
    
    /**
     * 檢查是否完全就緒
     */
    function isFullyReady() {
        return initState.firebase && 
               initState.auth && 
               initState.dataManager && 
               initState.ui;
    }
    
    /**
     * 標記組件就緒
     */
    function markReady(component) {
        if (initState[component] === false) {
            initState[component] = true;
            console.log(`✅ InitManager: ${component} 就緒`);
            
            // 檢查是否全部就緒
            if (isFullyReady()) {
                console.log('🎉 InitManager: 所有組件就緒！');
                
                // 執行所有回調
                readyCallbacks.forEach(callback => {
                    try {
                        callback();
                    } catch (error) {
                        console.error('❌ InitManager: 回調執行失敗', error);
                    }
                });
                
                // 清空回調列表
                readyCallbacks.length = 0;
                
                // 觸發全局事件
                window.dispatchEvent(new Event('app-ready'));
            }
        }
    }
    
    /**
     * 初始化流程
     */
    async function init() {
        console.log('🔄 InitManager: 開始初始化流程');
        
        // 1. 等待 Firebase SDK 載入
        await waitForFirebase();
        
        // 2. 等待 SimpleAuth 初始化
        await waitForAuth();
        
        // 3. 等待 SimpleDataManager 初始化
        await waitForDataManager();
        
        // 4. UI 組件就緒
        markReady('ui');
    }
    
    /**
     * 等待 Firebase SDK
     */
    async function waitForFirebase() {
        console.log('⏳ InitManager: 等待 Firebase SDK...');
        
        let attempts = 0;
        const maxAttempts = 50; // 5 秒
        
        while (attempts < maxAttempts) {
            if (window.firebase && window.firebase.apps && window.firebase.apps.length > 0) {
                console.log('✅ InitManager: Firebase SDK 就緒');
                markReady('firebase');
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        
        console.error('❌ InitManager: Firebase SDK 載入超時');
    }
    
    /**
     * 等待 SimpleAuth
     */
    async function waitForAuth() {
        console.log('⏳ InitManager: 等待 SimpleAuth...');
        
        let attempts = 0;
        const maxAttempts = 50; // 5 秒
        
        while (attempts < maxAttempts) {
            if (window.simpleAuth && window.simpleAuth.initialized) {
                console.log('✅ InitManager: SimpleAuth 就緒');
                markReady('auth');
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        
        console.error('❌ InitManager: SimpleAuth 初始化超時');
        // 即使超時也標記為就緒，避免阻塞
        markReady('auth');
    }
    
    /**
     * 等待 SimpleDataManager
     */
    async function waitForDataManager() {
        console.log('⏳ InitManager: 等待 SimpleDataManager...');
        
        let attempts = 0;
        const maxAttempts = 50; // 5 秒
        
        while (attempts < maxAttempts) {
            if (window.simpleDataManager && window.simpleDataManager.initialized) {
                console.log('✅ InitManager: SimpleDataManager 就緒');
                markReady('dataManager');
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        
        console.error('❌ InitManager: SimpleDataManager 初始化超時');
        // 即使超時也標記為就緒，避免阻塞
        markReady('dataManager');
    }
    
    // 當 DOM 載入完成後開始初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // 暴露狀態檢查函數
    window.getInitState = function() {
        return { ...initState };
    };
    
    console.log('✅ InitManager: 腳本載入完成');
    
})();

