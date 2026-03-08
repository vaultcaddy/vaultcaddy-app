/**
 * ============================================
 * 🔥 VaultCaddy Firebase 配置 (Core Configuration)
 * ============================================
 * 項目: vaultcaddy-production-cbbe2
 * 創建日期: 2025-10-30
 * 用途: 系統中唯一且標準的 Firebase 初始化入口。
 *       請勿在其他檔案中再次呼叫 firebase.initializeApp()
 * ============================================
 * 
 * 功能：
 * 1. 初始化 Firebase App
 * 2. 配置 Firestore Database
 * 3. 配置 Cloud Storage
 * 4. 配置 Authentication
 * 
 * @version 2.0.0
 * @updated 2026-03-07
 */

// ============================================
// Firebase 配置（生產環境）
// ============================================
const firebaseConfig = {
    apiKey: "AIzaSyA_zC38DTF8lyOvLOfU7HHaBd3v2YCyMCs",
    authDomain: "vaultcaddy-production-cbbe2.firebaseapp.com",  // ⚠️ 必須用 Firebase 預設域名，因為網站託管在 GitHub Pages，沒有 __/auth/handler
    projectId: "vaultcaddy-production-cbbe2",
    storageBucket: "vaultcaddy-production-cbbe2.firebasestorage.app",
    messagingSenderId: "708649491465",
    appId: "1:708649491465:web:26e237cf5d8b32c34b2cd8",
    measurementId: "G-LWPEKNC7RQ"
};

// ============================================
// Firebase 服務實例
// ============================================
let app;
let db;
let storage;
let auth;

/**
 * 初始化 Firebase
 */
function initializeFirebase() {
    try {
        // 檢查 Firebase SDK 是否已加載
        if (typeof firebase === 'undefined') {
            console.error('❌ Firebase SDK 未加載');
            console.error('   請確保在 HTML 中正確引入 Firebase CDN');
            return false;
        }
        
        // 初始化 Firebase App
        if (!firebase.apps.length) {
            app = firebase.initializeApp(firebaseConfig);
            console.log('✅ Firebase App 已初始化');
            console.log('   項目 ID:', firebaseConfig.projectId);
        } else {
            app = firebase.app();
            console.log('✅ Firebase App 已存在');
        }
        
        // 初始化 Firestore
        db = firebase.firestore();
        console.log('✅ Firestore 已初始化');
        
        // 初始化 Cloud Storage
        storage = firebase.storage();
        console.log('✅ Cloud Storage 已初始化');
        console.log('   Storage Bucket:', firebaseConfig.storageBucket);
        
        // 設置 Firestore 設定（必須在 enablePersistence 之前）
        db.settings({
            cacheSizeBytes: firebase.firestore.CACHE_SIZE_UNLIMITED
        });
        
        // 啟用 Firestore 離線持久化
        db.enablePersistence({ synchronizeTabs: true })
            .then(() => {
                console.log('✅ Firestore 離線持久化已啟用');
                console.log('   數據將在離線時緩存到本地');
            })
            .catch((err) => {
                if (err.code === 'failed-precondition') {
                    console.warn('⚠️ 多個標籤頁打開，離線持久化僅在一個標籤頁啟用');
                } else if (err.code === 'unimplemented') {
                    console.warn('⚠️ 瀏覽器不支持離線持久化');
                } else {
                    console.warn('⚠️ Firestore 持久化失敗:', err.message);
                }
            });
        
        // 初始化 Authentication
        auth = firebase.auth();
        console.log('✅ Firebase Authentication 已初始化');
        
        return true;
    } catch (error) {
        console.error('❌ Firebase 初始化失敗:', error);
        console.error('   錯誤詳情:', error.message);
        return false;
    }
}

// ============================================
// 全局暴露 Firebase 服務
// ============================================
if (typeof window !== 'undefined') {
    window.firebaseConfig = firebaseConfig;
    window.initializeFirebase = initializeFirebase;
    window.getFirebaseApp = () => app;
    window.getFirestore = () => db;
    window.getFirebaseStorage = () => storage;
    window.getAuth = () => auth;
    
    // 簡化的全局變量（向後兼容）
    window.firebaseApp = app;
    window.firebaseDB = db;
    window.firebaseStorage = storage;
    window.firebaseAuth = auth;
}

// ============================================
// 自動初始化
// ============================================
if (typeof window !== 'undefined') {
    console.log('🔧 開始 Firebase 自動初始化...');
    
    // 等待 Firebase SDK 加載
    const checkFirebase = setInterval(() => {
        if (typeof firebase !== 'undefined' && firebase.apps !== undefined) {
            clearInterval(checkFirebase);
            console.log('✅ Firebase SDK 已加載');
            
            try {
                const success = initializeFirebase();
                
                if (success) {
                    // 設置全局標誌
                    window.firebaseInitialized = true;
                    console.log('✅ window.firebaseInitialized = true');
                    
                    // 觸發自定義事件，通知其他模塊 Firebase 已就緒
                    window.dispatchEvent(new CustomEvent('firebase-ready', {
                        detail: {
                            app: app,
                            db: db,
                            storage: storage,
                            auth: auth
                        }
                    }));
                    
                    console.log('🔥 Firebase 已就緒，觸發 firebase-ready 事件');
                } else {
                    console.error('❌ Firebase 初始化返回 false');
                }
            } catch (error) {
                console.error('❌ Firebase 自動初始化失敗:', error);
            }
        }
    }, 50); // 減少輪詢間隔到 50ms
    
    // 超時檢查（10 秒）
    setTimeout(() => {
        clearInterval(checkFirebase);
        if (typeof firebase === 'undefined') {
            console.error('❌ Firebase SDK 加載超時（10 秒）');
            console.error('   請檢查網絡連接和 CDN 可用性');
        } else if (!window.firebaseInitialized) {
            console.error('❌ Firebase 初始化超時（10 秒）');
            console.error('   Firebase SDK 已加載，但初始化失敗');
        }
    }, 10000);
}

console.log('✅ Firebase 配置模塊已載入');
console.log('   等待 Firebase SDK 加載...');
