/**
 * ============================================
 * 📦 VaultCaddy 簡化數據管理系統
 * ============================================
 * 功能：
 * - 純 Firebase Firestore 和 Storage
 * - 項目管理（CRUD）
 * - 文檔管理（CRUD）
 * - 用戶 Credits 管理
 * - 簡潔清晰的代碼
 * ============================================
 */

class SimpleDataManager {
    constructor() {
        this.db = null;
        this.storage = null;
        this.auth = null;
        this.currentUser = null; // ✅ 緩存當前用戶
        this.initialized = false;
        
        console.log('📦 SimpleDataManager 構造函數執行');
        // 不在構造函數中初始化，等待 firebase-ready 事件
    }
    
    // 初始化
    async init() {
        try {
            console.log('📦 開始初始化 SimpleDataManager... [VERSION: 20251105-ultimate]');
            
            // 直接使用 Firebase（已由 firebase-config.js 初始化）
            if (!firebase || !firebase.firestore || !firebase.storage) {
                throw new Error('Firebase SDK 未加載');
            }
            
            this.db = firebase.firestore();
            this.storage = firebase.storage();
            this.auth = firebase.auth();
            
            // ✅ 等待 Auth 狀態確定（異步）
            console.log('⏳ 等待 Firebase Auth 狀態確定...');
            await new Promise((resolve) => {
                const unsubscribe = this.auth.onAuthStateChanged((user) => {
                    this.currentUser = user;
                    console.log('🔥 SimpleDataManager: Auth 狀態確定:', user ? user.email : '未登入');
                    unsubscribe(); // 只監聽第一次
                    resolve();
                });
                
                // 超時保護（5秒）
                setTimeout(() => {
                    if (!this.currentUser) {
                        console.warn('⚠️ Auth 狀態確定超時，使用當前狀態');
                        this.currentUser = this.auth.currentUser;
                    }
                    resolve();
                }, 5000);
            });
            
            // ✅ 繼續監聽後續變化
            this.auth.onAuthStateChanged((user) => {
                console.log('🔄 SimpleDataManager: Auth 狀態變化:', user ? user.email : '未登入');
                this.currentUser = user;
            });
            
            this.initialized = true;
            console.log('✅ SimpleDataManager 已初始化，currentUser:', this.currentUser ? this.currentUser.email : 'null');
            
        } catch (error) {
            console.error('❌ SimpleDataManager 初始化失敗:', error);
        }
    }
    
    // 等待 Firebase 就緒
    waitForFirebase() {
        return new Promise((resolve) => {
            if (window.firebaseInitialized && firebase && firebase.firestore && firebase.storage) {
                console.log('✅ Firebase 已就緒');
                resolve();
            } else {
                console.log('⏳ 等待 Firebase...');
                const checkInterval = setInterval(() => {
                    if (window.firebaseInitialized && firebase && firebase.firestore && firebase.storage) {
                        clearInterval(checkInterval);
                        console.log('✅ Firebase 已就緒');
                        resolve();
                    }
                }, 100);
                
                // 超時保護（15 秒）
                setTimeout(() => {
                    clearInterval(checkInterval);
                    console.error('❌ Firebase 初始化超時');
                    resolve(); // 仍然 resolve，避免卡住
                }, 15000);
            }
        });
    }
    
    // ============================================
    // 用戶管理
    // ============================================
    
    // 獲取當前用戶 ID
    getUserId() {
        // ✅ 優先使用緩存的用戶，再檢查 auth.currentUser
        const user = this.currentUser || this.auth.currentUser;
        
        console.log('🔍 SimpleDataManager.getUserId() 檢查:');
        console.log('   this.currentUser:', this.currentUser ? this.currentUser.email : 'null');
        console.log('   this.auth.currentUser:', this.auth.currentUser ? this.auth.currentUser.email : 'null');
        console.log('   最終 user:', user ? user.email : 'null');
        
        if (!user) {
            console.error('❌ getUserId: 用戶未登入');
            throw new Error('用戶未登入');
        }
        return user.uid;
    }
    
    // 獲取用戶 Credits
    async getUserCredits() {
        try {
            const userId = this.getUserId();
            const userDoc = await this.db.collection('users').doc(userId).get();
            
            if (userDoc.exists) {
                return userDoc.data().credits || 0;
            } else {
                // 創建用戶文檔（初始 0 Credits，驗證後贈送 20）
                await this.db.collection('users').doc(userId).set({
                    credits: 0,
                    currentCredits: 0,
                    emailVerified: false,
                    createdAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                return 0;
            }
        } catch (error) {
            console.error('❌ 獲取用戶 Credits 失敗:', error);
            return 0;
        }
    }
    
    // 更新用戶 Credits
    async updateUserCredits(newCredits) {
        try {
            const userId = this.getUserId();
            await this.db.collection('users').doc(userId).update({
                credits: newCredits,
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log('✅ 用戶 Credits 已更新:', newCredits);
            return true;
        } catch (error) {
            console.error('❌ 更新用戶 Credits 失敗:', error);
            return false;
        }
    }
    
    // ============================================
    // 項目管理
    // ============================================
    
    // 獲取所有項目
    async getProjects() {
        try {
            console.log('📂 getProjects() 開始執行...');
            const userId = this.getUserId();
            console.log('   userId:', userId);
            console.log('   準備查詢 Firestore collection: projects');
            
            const snapshot = await this.db.collection('projects')
                .where('userId', '==', userId)
                .get();
            
            console.log('   ✅ Firestore 查詢完成');
            console.log('   snapshot.empty:', snapshot.empty);
            console.log('   snapshot.size:', snapshot.size);
            console.log('   查詢結果:', snapshot.docs.length, '個項目');
            
            if (snapshot.empty) {
                console.warn('   ⚠️ Firestore 中沒有找到任何項目！');
                console.warn('   請檢查：');
                console.warn('   1. Firebase Console 中是否有項目數據');
                console.warn('   2. userId 是否匹配:', userId);
                console.warn('   3. Firestore 權限規則是否正確');
                console.warn('   4. collection 名稱是否為 "projects"');
            }
            
            // 在客戶端排序（避免需要 Firestore 索引）
            const projects = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            })).sort((a, b) => {
                // 按創建時間降序排序（最新的在前）
                const timeA = a.createdAt?.toMillis?.() || 0;
                const timeB = b.createdAt?.toMillis?.() || 0;
                return timeB - timeA;
            });
            
            console.log(`✅ 獲取 ${projects.length} 個項目`);
            return projects;
            
        } catch (error) {
            console.error('❌ 獲取項目失敗:', error);
            return [];
        }
    }
    
    // 創建項目
    async createProject(name) {
        try {
            const userId = this.getUserId();
            
            // 🔍 檢查是否已存在同名項目
            const existingProjects = await this.getProjects();
            const duplicateName = existingProjects.find(p => p.name === name);
            
            if (duplicateName) {
                console.warn('⚠️ 項目名稱已存在:', name);
                throw new Error(`項目名稱 "${name}" 已存在，請使用其他名稱`);
            }
            
            const projectData = {
                userId,
                name,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            const docRef = await this.db.collection('projects').add(projectData);
            console.log('✅ 項目已創建:', docRef.id);
            
            return {
                id: docRef.id,
                ...projectData
            };
            
        } catch (error) {
            console.error('❌ 創建項目失敗:', error);
            throw error;
        }
    }
    
    // 更新項目
    async updateProject(projectId, updates) {
        try {
            await this.db.collection('projects').doc(projectId).update({
                ...updates,
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log('✅ 項目已更新:', projectId);
        } catch (error) {
            console.error('❌ 更新項目失敗:', error);
            throw error;
        }
    }
    
    // 刪除項目
    async deleteProject(projectId) {
        try {
            // 刪除項目下的所有文檔
            const documents = await this.getDocuments(projectId);
            for (const doc of documents) {
                await this.deleteDocument(projectId, doc.id);
            }
            
            // 刪除項目
            await this.db.collection('projects').doc(projectId).delete();
            console.log('✅ 項目已刪除:', projectId);
            
        } catch (error) {
            console.error('❌ 刪除項目失敗:', error);
            throw error;
        }
    }
    
    // ============================================
    // 文檔管理
    // ============================================
    
    // 獲取項目的所有文檔
    async getDocuments(projectId) {
        try {
            const snapshot = await this.db.collection('documents')
                .where('projectId', '==', projectId)
                .get();
            
            // 在客戶端排序，避免需要 Firebase 複合索引
            const documents = snapshot.docs
                .map(doc => ({
                    id: doc.id,
                    ...doc.data()
                }))
                .sort((a, b) => {
                    const dateA = new Date(a.createdAt || 0);
                    const dateB = new Date(b.createdAt || 0);
                    return dateB - dateA; // 降序排列（最新的在前）
                });
            
            console.log(`✅ 獲取 ${documents.length} 個文檔`);
            return documents;
            
        } catch (error) {
            console.error('❌ 獲取文檔失敗:', error);
            return [];
        }
    }
    
    // ✅ 獲取單個文檔
    async getDocument(projectId, documentId) {
        try {
            const docRef = await this.db.collection('documents').doc(documentId).get();
            
            if (!docRef.exists) {
                console.warn('⚠️ 文檔不存在:', documentId);
                return null;
            }
            
            const document = {
                id: docRef.id,
                ...docRef.data()
            };
            
            console.log('✅ 獲取文檔成功:', documentId);
            return document;
            
        } catch (error) {
            console.error('❌ 獲取文檔失敗:', error);
            return null;
        }
    }
    
    // 創建文檔
    async createDocument(projectId, documentData) {
        try {
            const data = {
                projectId,
                ...documentData,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            const docRef = await this.db.collection('documents').add(data);
            console.log('✅ 文檔已創建:', docRef.id);
            
            // 返回文檔 ID（字符串）
            return docRef.id;
            
        } catch (error) {
            console.error('❌ 創建文檔失敗:', error);
            throw error;
        }
    }
    
    // 更新文檔
    async updateDocument(projectId, documentId, updates) {
        try {
            await this.db.collection('documents').doc(documentId).update({
                ...updates,
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log('✅ 文檔已更新:', documentId);
        } catch (error) {
            console.error('❌ 更新文檔失敗:', error);
            throw error;
        }
    }
    
    // 刪除文檔
    async deleteDocument(projectId, documentId) {
        try {
            // 獲取文檔信息
            const doc = await this.db.collection('documents').doc(documentId).get();
            
            // 刪除 Storage 中的文件
            if (doc.exists && doc.data().fileUrl) {
                try {
                    const fileRef = this.storage.refFromURL(doc.data().fileUrl);
                    await fileRef.delete();
                    console.log('✅ Storage 文件已刪除');
                } catch (error) {
                    console.warn('⚠️ Storage 文件刪除失敗（可能已不存在）:', error);
                }
            }
            
            // 刪除 Firestore 文檔
            await this.db.collection('documents').doc(documentId).delete();
            console.log('✅ 文檔已刪除:', documentId);
            
        } catch (error) {
            console.error('❌ 刪除文檔失敗:', error);
            throw error;
        }
    }
    
    // 上傳文件到 Storage
    async uploadFile(projectId, file) {
        try {
            const userId = this.getUserId();
            const fileName = `${Date.now()}_${file.name}`;
            const filePath = `documents/${userId}/${projectId}/${fileName}`;
            
            // 上傳文件
            const storageRef = this.storage.ref(filePath);
            const snapshot = await storageRef.put(file);
            
            // 獲取下載 URL
            const downloadURL = await snapshot.ref.getDownloadURL();
            
            console.log('✅ 文件已上傳:', downloadURL);
            return downloadURL;
            
        } catch (error) {
            console.error('❌ 上傳文件失敗:', error);
            throw error;
        }
    }
}

// 創建全局實例
console.log('📦 加載 SimpleDataManager...');
window.simpleDataManager = new SimpleDataManager();

// 向後兼容（供舊代碼使用）
window.firebaseDataManager = window.simpleDataManager;

// 監聽 firebase-ready 事件，自動初始化
window.addEventListener('firebase-ready', async () => {
    console.log('🔥 收到 firebase-ready 事件，初始化 SimpleDataManager');
    if (!window.simpleDataManager.initialized) {
        await window.simpleDataManager.init();
    } else {
        console.log('ℹ️ SimpleDataManager 已經初始化，跳過');
    }
});

// ✅ 後備檢查：如果 Firebase 已經就緒，立即初始化
setTimeout(async () => {
    if (window.firebaseInitialized && !window.simpleDataManager.initialized) {
        console.log('🔄 Firebase 已就緒但 SimpleDataManager 未初始化，立即初始化...');
        await window.simpleDataManager.init();
    }
}, 100); // 100ms 後檢查

// ✅✅ 終極後備：強制初始化（3秒後）
setTimeout(async () => {
    if (!window.simpleDataManager.initialized) {
        console.warn('⚠️ SimpleDataManager 3秒後仍未初始化，強制初始化');
        try {
            await window.simpleDataManager.init();
        } catch (error) {
            console.error('❌ 強制初始化失敗:', error);
        }
    }
}, 3000);

