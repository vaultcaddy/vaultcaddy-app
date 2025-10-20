/**
 * VaultCaddy 批量處理器
 * 
 * 核心功能:
 * 1. 多文件上傳支持
 * 2. 並行 AI 提取
 * 3. 批量進度追蹤
 * 4. 錯誤處理和重試
 * 
 * @version 1.0.0
 */

class BatchProcessor {
    constructor() {
        this.version = '1.0.0';
        this.maxConcurrent = 3;  // 最大並發處理數
        this.queue = [];
        this.processing = [];
        this.completed = [];
        this.failed = [];
        this.listeners = {};
    }
    
    /**
     * 添加批量上傳任務
     * 
     * @param {Array} files - 文件列表
     * @param {String} projectId - 項目 ID
     * @param {String} documentType - 文檔類型
     * @returns {String} 批次 ID
     */
    async addBatch(files, projectId, documentType) {
        const batchId = `batch-${Date.now()}`;
        
        console.log('📦 創建批量處理任務...');
        console.log(`   批次 ID: ${batchId}`);
        console.log(`   文件數量: ${files.length}`);
        console.log(`   項目 ID: ${projectId}`);
        console.log(`   文檔類型: ${documentType}`);
        
        // 創建任務
        const tasks = files.map((file, index) => ({
            id: `task-${batchId}-${index}`,
            batchId: batchId,
            file: file,
            projectId: projectId,
            documentType: documentType,
            status: 'pending',      // pending, processing, completed, failed
            progress: 0,
            result: null,
            error: null,
            startTime: null,
            endTime: null,
            retryCount: 0
        }));
        
        // 添加到隊列
        this.queue.push(...tasks);
        
        // 觸發事件
        this.emit('batchCreated', {
            batchId: batchId,
            totalTasks: tasks.length
        });
        
        // 開始處理
        this.processQueue();
        
        return batchId;
    }
    
    /**
     * 處理隊列
     */
    async processQueue() {
        // 檢查是否可以處理更多任務
        while (this.processing.length < this.maxConcurrent && this.queue.length > 0) {
            const task = this.queue.shift();
            this.processing.push(task);
            
            // 異步處理任務
            this.processTask(task).catch(error => {
                console.error(`❌ 任務處理失敗: ${task.id}`, error);
            });
        }
    }
    
    /**
     * 處理單個任務
     */
    async processTask(task) {
        console.log(`🔄 開始處理任務: ${task.id}`);
        console.log(`   文件名: ${task.file.name}`);
        
        task.status = 'processing';
        task.startTime = Date.now();
        
        this.emit('taskStarted', task);
        
        try {
            // 步驟 1: 創建文檔記錄 (10%)
            task.progress = 10;
            this.emit('taskProgress', task);
            
            const documentId = `doc-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
            const processingDocument = {
                id: documentId,
                name: task.file.name,
                fileName: task.file.name,
                size: task.file.size,
                fileSize: task.file.size,
                type: task.file.type,
                uploadDate: new Date().toISOString(),
                status: 'Processing',
                isProcessing: true,
                processingProgress: 10,
                processedData: {
                    documentType: this.getDocumentTypeName(task.documentType),
                    accountHolder: '處理中...',
                    accountNumber: '—',
                    startDate: '—',
                    endDate: '—',
                    startBalance: 0,
                    endBalance: 0,
                    transactionCount: 0
                }
            };
            
            // 保存到 localStorage
            const storageKey = `vaultcaddy_project_${task.projectId}_documents`;
            const documents = JSON.parse(localStorage.getItem(storageKey) || '[]');
            documents.unshift(processingDocument);
            localStorage.setItem(storageKey, JSON.stringify(documents));
            
            // 步驟 2: AI 數據提取 (30% - 70%)
            task.progress = 30;
            this.emit('taskProgress', task);
            
            const aiResult = await this.extractDataWithAI(task.file, task.documentType, (progress) => {
                task.progress = 30 + (progress * 0.4); // 30% - 70%
                this.emit('taskProgress', task);
            });
            
            // 步驟 3: 解析數據 (80%)
            task.progress = 80;
            this.emit('taskProgress', task);
            
            const parsedData = this.parseAIResponse(aiResult, task.file);
            
            // 步驟 4: 更新文檔 (90%)
            task.progress = 90;
            this.emit('taskProgress', task);
            
            this.updateDocument(documentId, task.projectId, parsedData);
            
            // 完成
            task.status = 'completed';
            task.progress = 100;
            task.endTime = Date.now();
            task.result = {
                documentId: documentId,
                extractedData: parsedData
            };
            
            this.completed.push(task);
            this.emit('taskCompleted', task);
            
            console.log(`✅ 任務完成: ${task.id}`);
            console.log(`   處理時間: ${task.endTime - task.startTime}ms`);
            
        } catch (error) {
            console.error(`❌ 任務失敗: ${task.id}`, error);
            
            task.status = 'failed';
            task.error = error.message;
            task.endTime = Date.now();
            
            // 重試邏輯
            if (task.retryCount < 2) {
                task.retryCount++;
                task.status = 'pending';
                console.log(`🔄 重試任務 (${task.retryCount}/2): ${task.id}`);
                this.queue.push(task);
            } else {
                this.failed.push(task);
                this.emit('taskFailed', task);
            }
        } finally {
            // 從處理列表中移除
            const index = this.processing.indexOf(task);
            if (index !== -1) {
                this.processing.splice(index, 1);
            }
            
            // 繼續處理隊列
            this.processQueue();
            
            // 檢查批次是否完成
            this.checkBatchCompletion(task.batchId);
        }
    }
    
    /**
     * 使用 AI 提取數據
     */
    async extractDataWithAI(file, documentType, onProgress) {
        console.log('🤖 開始 AI 數據提取...');
        
        // 檢查是否有可用的 AI 處理器
        if (window.googleSmartProcessor) {
            return await window.googleSmartProcessor.processDocumentOptimized(file, documentType);
        } else if (window.googleAIProcessor) {
            return await window.googleAIProcessor.processDocument(file, documentType);
        } else {
            throw new Error('沒有可用的 AI 處理器');
        }
    }
    
    /**
     * 解析 AI 響應
     */
    parseAIResponse(aiResult, file) {
        // 這裡應該調用 firstproject.html 中的 parseAIResponse 函數
        // 為了簡化，我們直接返回提取的數據
        return aiResult.extractedData || {};
    }
    
    /**
     * 更新文檔
     */
    updateDocument(documentId, projectId, extractedData) {
        const storageKey = `vaultcaddy_project_${projectId}_documents`;
        const documents = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        const docIndex = documents.findIndex(doc => doc.id === documentId);
        if (docIndex !== -1) {
            documents[docIndex].status = 'Success';
            documents[docIndex].isProcessing = false;
            documents[docIndex].processingProgress = 100;
            documents[docIndex].processedData = extractedData;
            
            localStorage.setItem(storageKey, JSON.stringify(documents));
            console.log('💾 文檔已更新:', documentId);
        }
    }
    
    /**
     * 獲取文檔類型名稱
     */
    getDocumentTypeName(type) {
        const typeMap = {
            'bank_statement': 'Bank Statement',
            'invoice': 'Invoice',
            'receipt': 'Receipt',
            'general': 'General'
        };
        return typeMap[type] || 'Unknown';
    }
    
    /**
     * 檢查批次是否完成
     */
    checkBatchCompletion(batchId) {
        const allTasks = [...this.completed, ...this.failed].filter(t => t.batchId === batchId);
        const queueTasks = this.queue.filter(t => t.batchId === batchId);
        const processingTasks = this.processing.filter(t => t.batchId === batchId);
        
        // 如果沒有待處理或正在處理的任務，批次完成
        if (queueTasks.length === 0 && processingTasks.length === 0) {
            const completedTasks = this.completed.filter(t => t.batchId === batchId);
            const failedTasks = this.failed.filter(t => t.batchId === batchId);
            
            console.log('🎉 批次處理完成!');
            console.log(`   批次 ID: ${batchId}`);
            console.log(`   成功: ${completedTasks.length}`);
            console.log(`   失敗: ${failedTasks.length}`);
            
            this.emit('batchCompleted', {
                batchId: batchId,
                totalTasks: allTasks.length,
                completedTasks: completedTasks,
                failedTasks: failedTasks,
                successRate: allTasks.length > 0 
                    ? Math.round((completedTasks.length / allTasks.length) * 100) 
                    : 0
            });
        }
    }
    
    /**
     * 獲取批次狀態
     */
    getBatchStatus(batchId) {
        const allTasks = [
            ...this.queue,
            ...this.processing,
            ...this.completed,
            ...this.failed
        ].filter(t => t.batchId === batchId);
        
        if (allTasks.length === 0) {
            return null;
        }
        
        const pending = this.queue.filter(t => t.batchId === batchId).length;
        const processing = this.processing.filter(t => t.batchId === batchId).length;
        const completed = this.completed.filter(t => t.batchId === batchId).length;
        const failed = this.failed.filter(t => t.batchId === batchId).length;
        
        const totalProgress = allTasks.reduce((sum, task) => sum + task.progress, 0);
        const averageProgress = Math.round(totalProgress / allTasks.length);
        
        return {
            batchId: batchId,
            total: allTasks.length,
            pending: pending,
            processing: processing,
            completed: completed,
            failed: failed,
            progress: averageProgress,
            isComplete: pending === 0 && processing === 0
        };
    }
    
    /**
     * 取消批次
     */
    cancelBatch(batchId) {
        console.log(`🛑 取消批次: ${batchId}`);
        
        // 從隊列中移除
        this.queue = this.queue.filter(t => t.batchId !== batchId);
        
        // 標記正在處理的任務為取消
        this.processing.filter(t => t.batchId === batchId).forEach(task => {
            task.status = 'cancelled';
        });
        
        this.emit('batchCancelled', { batchId: batchId });
    }
    
    /**
     * 事件監聽
     */
    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }
    
    /**
     * 觸發事件
     */
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }
    
    /**
     * 獲取統計信息
     */
    getStats() {
        return {
            queue: this.queue.length,
            processing: this.processing.length,
            completed: this.completed.length,
            failed: this.failed.length,
            total: this.queue.length + this.processing.length + this.completed.length + this.failed.length
        };
    }
}

// 導出為全局變量
if (typeof window !== 'undefined') {
    window.BatchProcessor = BatchProcessor;
    window.batchProcessor = new BatchProcessor();
    console.log('✅ 批量處理器已加載');
}

// Node.js 環境導出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BatchProcessor;
}

