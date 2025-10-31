/**
 * ============================================
 * 🔥 VaultCaddy Firebase 數據管理器
 * ============================================
 * 
 * 功能：
 * 1. 項目管理（CRUD）
 * 2. 文檔管理（CRUD）
 * 3. 文件上傳到 Cloud Storage
 * 4. 數據同步和緩存
 * 5. 從 LocalStorage 遷移數據
 * 
 * 數據結構：
 * users/{userId}/projects/{projectId}/documents/{documentId}
 * 
 * @version 2.0.0
 * @updated 2025-10-30
 */

class FirebaseDataManager {
    constructor() {
        this.db = null;
        this.storage = null;
        this.auth = null;
        this.currentUser = null;
        this.isInitialized = false;
        
        console.log('🔥 Firebase 數據管理器初始化中...');
        
        // 監聽 Firebase 就緒事件
        if (typeof window !== 'undefined') {
            window.addEventListener('firebase-ready', () => {
                this.initialize();
            });
        }
    }
    
    /**
     * 初始化數據管理器
     */
    async initialize() {
        try {
            // 獲取 Firebase 服務實例
            this.db = window.getFirestore();
            this.storage = window.getFirebaseStorage();
            this.auth = window.getAuth();
            
            if (!this.db || !this.storage || !this.auth) {
                throw new Error('Firebase 服務未正確初始化');
            }
            
            // 監聽用戶狀態
            this.auth.onAuthStateChanged((user) => {
                this.currentUser = user;
                if (user) {
                    console.log('👤 用戶已登入:', user.email);
                } else {
                    console.log('👤 用戶未登入（使用匿名模式）');
                }
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
        // 優先使用 Firebase Auth 用戶 ID
        if (this.currentUser) {
            return this.currentUser.uid;
        }
        
        // 如果未登入，重定向到登錄頁
        console.warn('⚠️ 用戶未登入，需要登入才能訪問此功能');
        
        // 檢查是否在公開頁面
        const publicPages = ['login.html', 'register.html', 'index.html', 'privacy.html', 'terms.html'];
        const currentPage = window.location.pathname.split('/').pop();
        
        if (!publicPages.includes(currentPage)) {
            console.log('🔒 重定向到登錄頁...');
            window.location.href = 'login.html';
        }
        
        return null;
    }
    
    // ============================================
    // 項目管理
    // ============================================
    
    /**
     * 創建項目
     */
    async createProject(projectData) {
        try {
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
            const userId = this.getUserId();
            const snapshot = await this.db.collection('users').doc(userId)
                .collection('projects')
                .orderBy('createdAt', 'desc')
                .get();
            
            const projects = [];
            snapshot.forEach((doc) => {
                const data = doc.data();
                projects.push({
                    id: doc.id,
                    ...data,
                    // 轉換 Timestamp 為 Date
                    createdAt: data.createdAt?.toDate(),
                    updatedAt: data.updatedAt?.toDate()
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
    
    // ============================================
    // 文檔管理
    // ============================================
    
    /**
     * 創建文檔
     */
    async createDocument(projectId, documentData) {
        try {
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
            const userId = this.getUserId();
            const snapshot = await this.db.collection('users').doc(userId)
                .collection('projects').doc(projectId)
                .collection('documents')
                .orderBy('createdAt', 'desc')
                .get();
            
            const documents = [];
            snapshot.forEach((doc) => {
                const data = doc.data();
                documents.push({
                    id: doc.id,
                    ...data,
                    // 轉換 Timestamp 為 Date
                    createdAt: data.createdAt?.toDate(),
                    updatedAt: data.updatedAt?.toDate()
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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
    
    // ============================================
    // 文件上傳到 Cloud Storage
    // ============================================
    
    /**
     * 上傳文件到 Cloud Storage
     * @param {File} file - 文件對象
     * @param {string} projectId - 項目 ID
     * @param {Function} onProgress - 進度回調函數
     * @returns {Promise<string>} 文件 URL
     */
    async uploadFile(file, projectId, onProgress) {
        try {
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
            const userId = this.getUserId();
            const timestamp = Date.now();
            const fileName = `${timestamp}_${file.name}`;
            const filePath = `users/${userId}/projects/${projectId}/${fileName}`;
            
            console.log('📤 開始上傳文件:', fileName);
            
            // 創建 Storage 引用
            const storageRef = this.storage.ref(filePath);
            
            // 上傳文件
            const uploadTask = storageRef.put(file);
            
            // 監聽上傳進度
            return new Promise((resolve, reject) => {
                uploadTask.on('state_changed',
                    (snapshot) => {
                        // 計算進度
                        const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                        console.log(`   上傳進度: ${progress.toFixed(1)}%`);
                        
                        if (onProgress) {
                            onProgress(progress);
                        }
                    },
                    (error) => {
                        console.error('❌ 文件上傳失敗:', error);
                        reject(error);
                    },
                    async () => {
                        // 上傳完成，獲取下載 URL
                        try {
                            const downloadURL = await uploadTask.snapshot.ref.getDownloadURL();
                            console.log('✅ 文件上傳成功:', downloadURL);
                            resolve(downloadURL);
                        } catch (error) {
                            reject(error);
                        }
                    }
                );
            });
        } catch (error) {
            console.error('❌ 上傳文件失敗:', error);
            throw error;
        }
    }
    
    /**
     * 刪除 Cloud Storage 中的文件
     */
    async deleteFile(fileUrl) {
        try {
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
            const storageRef = this.storage.refFromURL(fileUrl);
            await storageRef.delete();
            
            console.log('✅ 文件已刪除:', fileUrl);
        } catch (error) {
            console.error('❌ 刪除文件失敗:', error);
            throw error;
        }
    }
    
    // ============================================
    // 數據遷移
    // ============================================
    
    /**
     * 從 LocalStorage 遷移數據到 Firebase
     */
    async migrateFromLocalStorage() {
        try {
            if (!this.isInitialized) {
                throw new Error('數據管理器未初始化');
            }
            
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

// ============================================
// 全局暴露
// ============================================
if (typeof window !== 'undefined') {
    window.FirebaseDataManager = FirebaseDataManager;
    window.firebaseDataManager = new FirebaseDataManager();
    console.log('✅ Firebase 數據管理器模塊已載入');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FirebaseDataManager;
}
