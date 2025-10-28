/**
 * VaultCaddy 批量上傳處理器
 * 
 * 功能：
 * 1. 支持多文件選擇和上傳
 * 2. 並行處理多個文件
 * 3. 顯示每個文件的處理進度
 * 4. 錯誤處理和重試機制
 * 
 * @version 1.0.0
 * @updated 2025-10-26
 */

class BatchUploadProcessor {
    constructor() {
        this.maxConcurrent = 3; // 最多同時處理 3 個文件
        this.processingQueue = [];
        this.completedFiles = [];
        this.failedFiles = [];
        this.currentlyProcessing = 0;
        
        console.log('📦 批量上傳處理器初始化');
    }
    
    /**
     * 批量處理文件
     * @param {FileList} files - 要處理的文件列表
     * @param {string} documentType - 文檔類型
     * @param {string} projectId - 項目 ID
     * @param {Function} onProgress - 進度回調
     * @param {Function} onComplete - 完成回調
     */
    async processBatch(files, documentType, projectId, onProgress, onComplete) {
        console.log(`📦 開始批量處理 ${files.length} 個文件`);
        
        // 重置狀態
        this.processingQueue = Array.from(files);
        this.completedFiles = [];
        this.failedFiles = [];
        this.currentlyProcessing = 0;
        
        // 創建處理任務
        const tasks = [];
        for (let i = 0; i < Math.min(this.maxConcurrent, files.length); i++) {
            tasks.push(this.processNext(documentType, projectId, onProgress));
        }
        
        // 等待所有任務完成
        await Promise.all(tasks);
        
        // 調用完成回調
        if (onComplete) {
            onComplete({
                total: files.length,
                completed: this.completedFiles.length,
                failed: this.failedFiles.length,
                completedFiles: this.completedFiles,
                failedFiles: this.failedFiles
            });
        }
        
        console.log(`✅ 批量處理完成: ${this.completedFiles.length} 成功, ${this.failedFiles.length} 失敗`);
    }
    
    /**
     * 處理下一個文件
     */
    async processNext(documentType, projectId, onProgress) {
        while (this.processingQueue.length > 0) {
            const file = this.processingQueue.shift();
            this.currentlyProcessing++;
            
            try {
                console.log(`🔄 處理文件: ${file.name}`);
                
                // 更新進度
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'processing',
                        progress: 0
                    });
                }
                
                // 驗證文件
                const validation = this.validateFile(file);
                if (!validation.valid) {
                    throw new Error(validation.error);
                }
                
                // 更新進度：開始 AI 處理
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'processing',
                        progress: 20,
                        message: 'AI 處理中...'
                    });
                }
                
                // 使用 Google Smart Processor 處理文件
                const result = await window.googleSmartProcessor.processDocument(file, documentType);
                
                if (!result || !result.success) {
                    throw new Error('AI 處理失敗');
                }
                
                // 更新進度：AI 處理完成
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'processing',
                        progress: 60,
                        message: '數據驗證中...'
                    });
                }
                
                // 驗證和清理數據
                const cleanedData = this.validateAndCleanData(result.extractedData, documentType);
                
                // 更新進度：保存數據
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'processing',
                        progress: 80,
                        message: '保存數據...'
                    });
                }
                
                // 保存到 LocalStorage（稍後會改為 Firebase）
                const fileData = {
                    id: `doc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    fileName: file.name,
                    fileSize: file.size,
                    fileType: file.type,
                    documentType: documentType,
                    uploadDate: new Date().toISOString(),
                    status: 'Success',
                    processingProgress: 100,
                    processedData: cleanedData,
                    confidence: result.confidence || 0,
                    processor: result.processor || 'unknown'
                };
                
                // 保存到項目
                this.saveFileToProject(projectId, fileData);
                
                // 標記為完成
                this.completedFiles.push({
                    file: file,
                    data: fileData
                });
                
                // 更新進度：完成
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'completed',
                        progress: 100,
                        message: '✅ 完成'
                    });
                }
                
                console.log(`✅ 文件處理完成: ${file.name}`);
                
            } catch (error) {
                console.error(`❌ 文件處理失敗: ${file.name}`, error);
                
                // 標記為失敗
                this.failedFiles.push({
                    file: file,
                    error: error.message
                });
                
                // 更新進度：失敗
                if (onProgress) {
                    onProgress({
                        fileName: file.name,
                        status: 'failed',
                        progress: 0,
                        message: `❌ 失敗: ${error.message}`
                    });
                }
            } finally {
                this.currentlyProcessing--;
            }
        }
    }
    
    /**
     * 驗證文件
     */
    validateFile(file) {
        // 檢查文件大小（最大 10MB）
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            return {
                valid: false,
                error: `文件太大 (${(file.size / 1024 / 1024).toFixed(2)} MB)，最大支持 10 MB`
            };
        }
        
        // 檢查文件類型
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];
        if (!allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: `不支持的文件類型: ${file.type}`
            };
        }
        
        return { valid: true };
    }
    
    /**
     * 驗證和清理數據
     */
    validateAndCleanData(data, documentType) {
        // 這裡可以添加更多的數據驗證和清理邏輯
        // 目前只是簡單返回數據
        return data;
    }
    
    /**
     * 保存文件到項目
     */
    saveFileToProject(projectId, fileData) {
        try {
            // ✅ 修復：使用正確的存儲鍵（與 loadFilesForDocumentType 一致）
            const storageKey = `vaultcaddy_project_${projectId}_documents`;  // 從 _files 改為 _documents
            const existingFiles = JSON.parse(localStorage.getItem(storageKey) || '[]');
            
            // 添加新文件
            existingFiles.push(fileData);
            
            // 保存回 LocalStorage
            localStorage.setItem(storageKey, JSON.stringify(existingFiles));
            
            console.log(`💾 文件已保存到項目 ${projectId}:`, fileData.fileName);
            console.log(`   存儲鍵: ${storageKey}`);
            console.log(`   當前文件總數: ${existingFiles.length}`);
        } catch (error) {
            console.error('❌ 保存文件失敗:', error);
            throw error;
        }
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.BatchUploadProcessor = BatchUploadProcessor;
    window.batchUploadProcessor = new BatchUploadProcessor();
    console.log('✅ 批量上傳處理器模塊已載入');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BatchUploadProcessor;
}

