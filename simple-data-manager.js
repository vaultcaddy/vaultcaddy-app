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
        this.initialized = false;
        
        console.log('📦 初始化 SimpleDataManager...');
        this.init();
    }
    
    // 初始化
    async init() {
        try {
            // 等待 Firebase
            await this.waitForFirebase();
            
            // 獲取實例
            this.db = firebase.firestore();
            this.storage = firebase.storage();
            this.auth = firebase.auth();
            this.initialized = true;
            
            console.log('✅ SimpleDataManager 已初始化');
            
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
        const user = this.auth.currentUser;
        if (!user) {
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
                // 創建用戶文檔
                await this.db.collection('users').doc(userId).set({
                    credits: 10, // 預設 10 個 credits
                    createdAt: firebase.firestore.FieldValue.serverTimestamp()
                });
                return 10;
            }
        } catch (error) {
            console.error('❌ 獲取用戶 Credits 失敗:', error);
            return 0;
        }
    }
    
    // 更新用戶 Credits
    async updateUserCredits(credits) {
        try {
            const userId = this.getUserId();
            await this.db.collection('users').doc(userId).update({
                credits: credits,
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log('✅ Credits 已更新:', credits);
        } catch (error) {
            console.error('❌ 更新 Credits 失敗:', error);
            throw error;
        }
    }
    
    // ============================================
    // 項目管理
    // ============================================
    
    // 獲取所有項目
    async getProjects() {
        try {
            const userId = this.getUserId();
            const snapshot = await this.db.collection('projects')
                .where('userId', '==', userId)
                .get();
            
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
                .orderBy('createdAt', 'desc')
                .get();
            
            const documents = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
            
            console.log(`✅ 獲取 ${documents.length} 個文檔`);
            return documents;
            
        } catch (error) {
            console.error('❌ 獲取文檔失敗:', error);
            return [];
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
            
            return {
                id: docRef.id,
                ...data
            };
            
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

