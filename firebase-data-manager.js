/**
 * VaultCaddy Firebase 數據管理器
 * 
 * 功能：
 * 1. 管理項目數據（CRUD）
 * 2. 管理文檔數據（CRUD）
 * 3. 數據同步和緩存
 * 4. 從 LocalStorage 遷移數據
 * 
 * @version 1.0.0
 * @updated 2025-10-26
 */

class FirebaseDataManager {
    constructor() {
        this.db = null;
        this.auth = null;
        this.currentUser = null;
        this.isInitialized = false;
        
        console.log('🔥 Firebase 數據管理器初始化');
    }
    
    /**
     * 初始化數據管理器
     */
    async initialize() {
        try {
            // 獲取 Firestore 和 Auth 實例
            this.db = window.getFirestore();
            this.auth = window.getAuth();
            
            if (!this.db || !this.auth) {
                throw new Error('Firebase 未正確初始化');
            }
            
            // 監聽用戶狀態
            this.auth.onAuthStateChanged((user) => {
                this.currentUser = user;
                console.log('👤 用戶狀態變更:', user ? user.email : '未登入');
            });
            
            this.isInitialized = true;
            console.log('✅ Firebase 數據管理器初始化完成');
            return true;
        } catch (error) {
            console.error('❌ Firebase 數據管理器初始化失敗:', error);
            return false;
        }
    }
    
    /**
     * 獲取當前用戶 ID
     */
    getUserId() {
        if (!this.currentUser) {
            // 如果未登入，使用匿名 ID
            let anonymousId = localStorage.getItem('vaultcaddy_anonymous_id');
            if (!anonymousId) {
                anonymousId = `anonymous_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                localStorage.setItem('vaultcaddy_anonymous_id', anonymousId);
            }
            return anonymousId;
        }
        return this.currentUser.uid;
    }
    
    /**
     * 創建項目
     */
    async createProject(projectData) {
        try {
            const userId = this.getUserId();
            const projectId = projectData.id || `project_${Date.now()}`;
            
            const project = {
                ...projectData,
                id: projectId,
                userId: userId,
                createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .set(project);
            
            console.log('✅ 項目已創建:', projectId);
            return projectId;
        } catch (error) {
            console.error('❌ 創建項目失敗:', error);
            throw error;
        }
    }
    
    /**
     * 獲取所有項目
     */
    async getProjects() {
        try {
            const userId = this.getUserId();
            const snapshot = await this.db.collection('users').doc(userId)
                .collection('projects')
                .orderBy('createdAt', 'desc')
                .get();
            
            const projects = [];
            snapshot.forEach((doc) => {
                projects.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            console.log('✅ 獲取項目列表:', projects.length, '個項目');
            return projects;
        } catch (error) {
            console.error('❌ 獲取項目失敗:', error);
            throw error;
        }
    }
    
    /**
     * 更新項目
     */
    async updateProject(projectId, updates) {
        try {
            const userId = this.getUserId();
            
            await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .update({
                    ...updates,
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
            
            console.log('✅ 項目已更新:', projectId);
        } catch (error) {
            console.error('❌ 更新項目失敗:', error);
            throw error;
        }
    }
    
    /**
     * 刪除項目
     */
    async deleteProject(projectId) {
        try {
            const userId = this.getUserId();
            
            // 刪除項目下的所有文檔
            const documentsSnapshot = await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents')
                .get();
            
            const batch = this.db.batch();
            documentsSnapshot.forEach((doc) => {
                batch.delete(doc.ref);
            });
            
            // 刪除項目
            batch.delete(this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId));
            
            await batch.commit();
            
            console.log('✅ 項目已刪除:', projectId);
        } catch (error) {
            console.error('❌ 刪除項目失敗:', error);
            throw error;
        }
    }
    
    /**
     * 創建文檔
     */
    async createDocument(projectId, documentData) {
        try {
            const userId = this.getUserId();
            const documentId = documentData.id || `doc_${Date.now()}`;
            
            const document = {
                ...documentData,
                id: documentId,
                projectId: projectId,
                userId: userId,
                createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                updatedAt: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents').doc(documentId)
                .set(document);
            
            console.log('✅ 文檔已創建:', documentId);
            return documentId;
        } catch (error) {
            console.error('❌ 創建文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 獲取項目的所有文檔
     */
    async getDocuments(projectId) {
        try {
            const userId = this.getUserId();
            const snapshot = await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents')
                .orderBy('createdAt', 'desc')
                .get();
            
            const documents = [];
            snapshot.forEach((doc) => {
                documents.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            console.log('✅ 獲取文檔列表:', documents.length, '個文檔');
            return documents;
        } catch (error) {
            console.error('❌ 獲取文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 更新文檔
     */
    async updateDocument(projectId, documentId, updates) {
        try {
            const userId = this.getUserId();
            
            await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents').doc(documentId)
                .update({
                    ...updates,
                    updatedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
            
            console.log('✅ 文檔已更新:', documentId);
        } catch (error) {
            console.error('❌ 更新文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 刪除文檔
     */
    async deleteDocument(projectId, documentId) {
        try {
            const userId = this.getUserId();
            
            await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents').doc(documentId)
                .delete();
            
            console.log('✅ 文檔已刪除:', documentId);
        } catch (error) {
            console.error('❌ 刪除文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 從 LocalStorage 遷移數據到 Firebase
     */
    async migrateFromLocalStorage() {
        try {
            console.log('🔄 開始從 LocalStorage 遷移數據...');
            
            // 遷移項目
            const projectsJson = localStorage.getItem('vaultcaddy_projects');
            if (projectsJson) {
                const projects = JSON.parse(projectsJson);
                console.log(`   找到 ${projects.length} 個項目`);
                
                for (const project of projects) {
                    await this.createProject(project);
                    
                    // 遷移項目的文檔
                    const documentsJson = localStorage.getItem(`vaultcaddy_project_${project.id}_files`);
                    if (documentsJson) {
                        const documents = JSON.parse(documentsJson);
                        console.log(`   項目 ${project.id} 有 ${documents.length} 個文檔`);
                        
                        for (const doc of documents) {
                            await this.createDocument(project.id, doc);
                        }
                    }
                }
            }
            
            console.log('✅ 數據遷移完成');
            
            // 可選：清除 LocalStorage（謹慎操作）
            // localStorage.removeItem('vaultcaddy_projects');
            
        } catch (error) {
            console.error('❌ 數據遷移失敗:', error);
            throw error;
        }
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.FirebaseDataManager = FirebaseDataManager;
    window.firebaseDataManager = new FirebaseDataManager();
    console.log('✅ Firebase 數據管理器模塊已載入');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FirebaseDataManager;
}

