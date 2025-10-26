/**
 * VaultCaddy Firebase 配置
 * 
 * 功能：
 * 1. 初始化 Firebase
 * 2. 配置 Firestore
 * 3. 配置 Authentication
 * 
 * @version 1.0.0
 * @updated 2025-10-26
 */

// Firebase 配置（請替換為你的 Firebase 項目配置）
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// 初始化 Firebase
let app;
let db;
let auth;

function initializeFirebase() {
    try {
        // 檢查 Firebase 是否已加載
        if (typeof firebase === 'undefined') {
            console.error('❌ Firebase SDK 未加載');
            return false;
        }
        
        // 初始化 Firebase App
        if (!firebase.apps.length) {
            app = firebase.initializeApp(firebaseConfig);
            console.log('✅ Firebase App 已初始化');
        } else {
            app = firebase.app();
            console.log('✅ Firebase App 已存在');
        }
        
        // 初始化 Firestore
        db = firebase.firestore();
        console.log('✅ Firestore 已初始化');
        
        // 初始化 Authentication
        auth = firebase.auth();
        console.log('✅ Firebase Authentication 已初始化');
        
        // 啟用 Firestore 離線持久化
        db.enablePersistence({ synchronizeTabs: true })
            .then(() => {
                console.log('✅ Firestore 離線持久化已啟用');
            })
            .catch((err) => {
                if (err.code === 'failed-precondition') {
                    console.warn('⚠️ 多個標籤頁打開，離線持久化僅在一個標籤頁啟用');
                } else if (err.code === 'unimplemented') {
                    console.warn('⚠️ 瀏覽器不支持離線持久化');
                }
            });
        
        return true;
    } catch (error) {
        console.error('❌ Firebase 初始化失敗:', error);
        return false;
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.firebaseConfig = firebaseConfig;
    window.initializeFirebase = initializeFirebase;
    window.getFirebaseApp = () => app;
    window.getFirestore = () => db;
    window.getAuth = () => auth;
}

// 自動初始化（當 Firebase SDK 加載後）
if (typeof window !== 'undefined') {
    // 等待 Firebase SDK 加載
    const checkFirebase = setInterval(() => {
        if (typeof firebase !== 'undefined') {
            clearInterval(checkFirebase);
            initializeFirebase();
        }
    }, 100);
    
    // 超時檢查（10 秒）
    setTimeout(() => {
        clearInterval(checkFirebase);
        if (typeof firebase === 'undefined') {
            console.error('❌ Firebase SDK 加載超時');
        }
    }, 10000);
}

console.log('✅ Firebase 配置模塊已載入');

