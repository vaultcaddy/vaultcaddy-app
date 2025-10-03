/**
 * Google Cloud Storage 集成模塊
 * 用於將AI提取的數據保存到Google Cloud Storage
 */

class GoogleCloudStorage {
    constructor() {
        this.projectId = 'vaultcaddy-production';
        this.bucketName = 'vaultcaddy-documents';
        this.apiKey = null;
        this.isInitialized = false;
        
        console.log('🌥️ Google Cloud Storage 模塊初始化');
        this.init();
    }
    
    async init() {
        try {
            // 從配置中獲取API密鑰
            if (window.VaultCaddyConfig) {
                this.apiKey = window.VaultCaddyConfig.getGoogleCloudApiKey();
            }
            
            if (!this.apiKey) {
                console.warn('⚠️ Google Cloud API密鑰未設置，將使用模擬模式');
                this.mockMode = true;
            } else {
                console.log('✅ Google Cloud Storage API密鑰已載入');
                this.mockMode = false;
            }
            
            this.isInitialized = true;
            
        } catch (error) {
            console.error('❌ Google Cloud Storage 初始化失敗:', error);
            this.mockMode = true;
            this.isInitialized = true;
        }
    }
    
    /**
     * 保存文檔數據到Google Cloud Storage
     */
    async saveDocument(documentData, metadata = {}) {
        if (!this.isInitialized) {
            await this.init();
        }
        
        try {
            const documentId = this.generateDocumentId();
            const timestamp = new Date().toISOString();
            
            const cloudDocument = {
                id: documentId,
                timestamp: timestamp,
                metadata: {
                    originalFileName: metadata.fileName || 'unknown',
                    fileSize: metadata.fileSize || 0,
                    fileType: metadata.fileType || 'unknown',
                    processingEngine: metadata.engine || 'google-ai',
                    ...metadata
                },
                data: documentData,
                version: '1.0'
            };
            
            if (this.mockMode) {
                return await this.saveMockDocument(cloudDocument);
            } else {
                return await this.saveRealDocument(cloudDocument);
            }
            
        } catch (error) {
            console.error('❌ 保存文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 模擬模式：保存到本地存儲
     */
    async saveMockDocument(cloudDocument) {
        console.log('🔄 模擬保存到Google Cloud Storage...');
        
        // 模擬網絡延遲
        await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
        
        try {
            // 保存到localStorage
            const storageKey = 'vaultcaddy_cloud_documents';
            const existingDocs = JSON.parse(localStorage.getItem(storageKey) || '[]');
            
            existingDocs.push(cloudDocument);
            
            // 限制存儲數量（最多保留100個文檔）
            if (existingDocs.length > 100) {
                existingDocs.splice(0, existingDocs.length - 100);
            }
            
            localStorage.setItem(storageKey, JSON.stringify(existingDocs));
            
            const result = {
                success: true,
                documentId: cloudDocument.id,
                cloudPath: `gs://${this.bucketName}/documents/${cloudDocument.id}.json`,
                timestamp: cloudDocument.timestamp,
                size: JSON.stringify(cloudDocument).length,
                mode: 'mock'
            };
            
            console.log(`✅ 文檔已保存 (模擬模式): ${result.documentId}`);
            return result;
            
        } catch (error) {
            console.error('❌ 模擬保存失敗:', error);
            throw error;
        }
    }
    
    /**
     * 真實模式：保存到Google Cloud Storage
     */
    async saveRealDocument(cloudDocument) {
        console.log('🔄 保存到Google Cloud Storage...');
        
        try {
            const fileName = `documents/${cloudDocument.id}.json`;
            const uploadUrl = `https://storage.googleapis.com/upload/storage/v1/b/${this.bucketName}/o?uploadType=media&name=${encodeURIComponent(fileName)}&key=${this.apiKey}`;
            
            const response = await fetch(uploadUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(cloudDocument)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            const uploadResult = await response.json();
            
            const result = {
                success: true,
                documentId: cloudDocument.id,
                cloudPath: `gs://${this.bucketName}/${fileName}`,
                timestamp: cloudDocument.timestamp,
                size: uploadResult.size,
                mode: 'real',
                gsUrl: uploadResult.selfLink
            };
            
            console.log(`✅ 文檔已保存到Google Cloud: ${result.documentId}`);
            return result;
            
        } catch (error) {
            console.error('❌ Google Cloud Storage 保存失敗:', error);
            
            // 如果真實保存失敗，回退到模擬模式
            console.log('🔄 回退到模擬模式...');
            return await this.saveMockDocument(cloudDocument);
        }
    }
    
    /**
     * 從Google Cloud Storage獲取文檔
     */
    async getDocument(documentId) {
        if (!this.isInitialized) {
            await this.init();
        }
        
        try {
            if (this.mockMode) {
                return await this.getMockDocument(documentId);
            } else {
                return await this.getRealDocument(documentId);
            }
            
        } catch (error) {
            console.error('❌ 獲取文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 模擬模式：從本地存儲獲取文檔
     */
    async getMockDocument(documentId) {
        const storageKey = 'vaultcaddy_cloud_documents';
        const existingDocs = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        const document = existingDocs.find(doc => doc.id === documentId);
        
        if (!document) {
            throw new Error(`文檔不存在: ${documentId}`);
        }
        
        return document;
    }
    
    /**
     * 真實模式：從Google Cloud Storage獲取文檔
     */
    async getRealDocument(documentId) {
        const fileName = `documents/${documentId}.json`;
        const downloadUrl = `https://storage.googleapis.com/storage/v1/b/${this.bucketName}/o/${encodeURIComponent(fileName)}?alt=media&key=${this.apiKey}`;
        
        const response = await fetch(downloadUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    /**
     * 列出所有文檔
     */
    async listDocuments(limit = 50) {
        if (!this.isInitialized) {
            await this.init();
        }
        
        try {
            if (this.mockMode) {
                return await this.listMockDocuments(limit);
            } else {
                return await this.listRealDocuments(limit);
            }
            
        } catch (error) {
            console.error('❌ 列出文檔失敗:', error);
            throw error;
        }
    }
    
    /**
     * 模擬模式：列出本地文檔
     */
    async listMockDocuments(limit) {
        const storageKey = 'vaultcaddy_cloud_documents';
        const existingDocs = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        // 按時間戳排序（最新的在前）
        existingDocs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        return {
            documents: existingDocs.slice(0, limit).map(doc => ({
                id: doc.id,
                timestamp: doc.timestamp,
                metadata: doc.metadata,
                size: JSON.stringify(doc).length
            })),
            total: existingDocs.length,
            mode: 'mock'
        };
    }
    
    /**
     * 真實模式：列出Google Cloud Storage中的文檔
     */
    async listRealDocuments(limit) {
        const listUrl = `https://storage.googleapis.com/storage/v1/b/${this.bucketName}/o?prefix=documents/&maxResults=${limit}&key=${this.apiKey}`;
        
        const response = await fetch(listUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        return {
            documents: (result.items || []).map(item => ({
                id: item.name.replace('documents/', '').replace('.json', ''),
                timestamp: item.timeCreated,
                size: parseInt(item.size),
                cloudPath: `gs://${this.bucketName}/${item.name}`
            })),
            total: result.items ? result.items.length : 0,
            mode: 'real'
        };
    }
    
    /**
     * 生成唯一的文檔ID
     */
    generateDocumentId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 8);
        return `doc_${timestamp}_${random}`;
    }
    
    /**
     * 獲取存儲統計信息
     */
    async getStorageStats() {
        try {
            const documents = await this.listDocuments(1000);
            
            const stats = {
                totalDocuments: documents.total,
                totalSize: documents.documents.reduce((sum, doc) => sum + (doc.size || 0), 0),
                mode: documents.mode,
                lastUpdated: new Date().toISOString()
            };
            
            return stats;
            
        } catch (error) {
            console.error('❌ 獲取存儲統計失敗:', error);
            return {
                totalDocuments: 0,
                totalSize: 0,
                mode: this.mockMode ? 'mock' : 'real',
                error: error.message
            };
        }
    }
}

// 創建全局實例
window.GoogleCloudStorage = GoogleCloudStorage;
window.googleCloudStorage = new GoogleCloudStorage();

console.log('☁️ Google Cloud Storage 模塊已載入');
