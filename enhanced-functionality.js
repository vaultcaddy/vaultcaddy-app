/**
 * VaultCaddy 增強功能腳本
 * 提供真實可用的功能實現（不包括API）
 */

// 本地數據存儲管理
class VaultCaddyStorage {
    constructor() {
        this.prefix = 'vaultcaddy_';
        this.init();
    }
    
    init() {
        // 初始化基本數據結構
        this.ensureDefaultData();
    }
    
    ensureDefaultData() {
        if (!this.get('user_profile')) {
            this.set('user_profile', {
                name: 'John Doe',
                email: 'user@example.com',
                company: 'Example Corp',
                phone: '+1 (555) 123-4567',
                created_date: new Date().toISOString(),
                last_login: new Date().toISOString()
            });
        }
        
        if (!this.get('user_settings')) {
            this.set('user_settings', {
                language: 'zh-TW',
                timezone: 'Asia/Taipei',
                notifications: true,
                auto_save: true,
                theme: 'light'
            });
        }
        
        if (!this.get('documents')) {
            this.set('documents', []);
        }
        
        if (!this.get('usage_stats')) {
            this.set('usage_stats', {
                total_processed: 0,
                total_pages: 0,
                success_rate: 0,
                avg_processing_time: 0,
                credits_used: 0,
                credits_remaining: 7
            });
        }
    }
    
    get(key) {
        try {
            const value = localStorage.getItem(this.prefix + key);
            return value ? JSON.parse(value) : null;
        } catch (e) {
            console.error('Storage get error:', e);
            return null;
        }
    }
    
    set(key, value) {
        try {
            localStorage.setItem(this.prefix + key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage set error:', e);
            return false;
        }
    }
    
    remove(key) {
        localStorage.removeItem(this.prefix + key);
    }
    
    clear() {
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith(this.prefix)) {
                localStorage.removeItem(key);
            }
        });
    }
}

// 文檔處理模擬器
class DocumentProcessor {
    constructor() {
        this.storage = new VaultCaddyStorage();
        this.processing_queue = [];
    }
    
    // 模擬文檔上傳和處理
    async processDocument(file, type = 'bank-statement') {
        const documentId = this.generateDocumentId();
        
        // 創建文檔記錄
        const document = {
            id: documentId,
            name: file.name,
            type: type,
            size: file.size,
            status: 'processing',
            uploaded_at: new Date().toISOString(),
            progress: 0,
            result: null
        };
        
        // 添加到存儲
        const documents = this.storage.get('documents') || [];
        documents.push(document);
        this.storage.set('documents', documents);
        
        // 模擬處理過程
        await this.simulateProcessing(documentId);
        
        return documentId;
    }
    
    async simulateProcessing(documentId) {
        const updateProgress = (progress) => {
            const documents = this.storage.get('documents') || [];
            const docIndex = documents.findIndex(d => d.id === documentId);
            if (docIndex !== -1) {
                documents[docIndex].progress = progress;
                this.storage.set('documents', documents);
                this.notifyProgressUpdate(documentId, progress);
            }
        };
        
        // 模擬處理階段
        const stages = [
            { progress: 10, duration: 500, message: 'Uploading...' },
            { progress: 30, duration: 1000, message: 'Analyzing document...' },
            { progress: 60, duration: 1500, message: 'Extracting data...' },
            { progress: 85, duration: 1000, message: 'Validating results...' },
            { progress: 100, duration: 500, message: 'Complete!' }
        ];
        
        for (const stage of stages) {
            await new Promise(resolve => setTimeout(resolve, stage.duration));
            updateProgress(stage.progress);
        }
        
        // 標記完成
        this.completeProcessing(documentId);
    }
    
    completeProcessing(documentId) {
        const documents = this.storage.get('documents') || [];
        const docIndex = documents.findIndex(d => d.id === documentId);
        
        if (docIndex !== -1) {
            documents[docIndex].status = 'completed';
            documents[docIndex].completed_at = new Date().toISOString();
            documents[docIndex].result = this.generateMockResult(documents[docIndex].type);
            this.storage.set('documents', documents);
            
            // 更新統計
            this.updateStats();
        }
    }
    
    generateMockResult(type) {
        const results = {
            'bank-statement': {
                transactions: 15,
                balance_start: 1250.00,
                balance_end: 890.50,
                period: '2024-01-01 to 2024-01-31',
                account_number: '****-1234'
            },
            'invoice': {
                vendor: 'ABC Company',
                amount: 1250.00,
                tax: 125.00,
                invoice_number: 'INV-2024-001',
                due_date: '2024-02-15'
            },
            'receipt': {
                merchant: 'Restaurant ABC',
                amount: 89.50,
                tax: 8.95,
                date: '2024-01-15',
                category: 'Meals'
            },
            'general': {
                document_type: 'Contract',
                pages: 5,
                entities_found: 12,
                confidence: 95.5
            }
        };
        
        return results[type] || results.general;
    }
    
    updateStats() {
        const stats = this.storage.get('usage_stats');
        const documents = this.storage.get('documents') || [];
        const completed = documents.filter(d => d.status === 'completed');
        
        stats.total_processed = completed.length;
        stats.success_rate = completed.length > 0 ? 
            (completed.filter(d => d.result).length / completed.length * 100).toFixed(1) : 0;
        stats.avg_processing_time = '2.5s';
        
        this.storage.set('usage_stats', stats);
    }
    
    generateDocumentId() {
        return 'doc_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    notifyProgressUpdate(documentId, progress) {
        // 觸發自定義事件
        window.dispatchEvent(new CustomEvent('documentProgress', {
            detail: { documentId, progress }
        }));
    }
}

// 真實的表單處理
class FormHandler {
    constructor() {
        this.storage = new VaultCaddyStorage();
    }
    
    // 更新用戶資料
    updateProfile(formData) {
        const profile = this.storage.get('user_profile');
        Object.assign(profile, formData);
        this.storage.set('user_profile', profile);
        
        this.showSuccessMessage('Profile updated successfully!');
        return true;
    }
    
    // 添加電子郵件
    addEmail(email) {
        const profile = this.storage.get('user_profile');
        if (!profile.emails) profile.emails = [];
        
        if (!profile.emails.includes(email)) {
            profile.emails.push(email);
            this.storage.set('user_profile', profile);
            this.showSuccessMessage('Email added successfully!');
            return true;
        }
        
        this.showErrorMessage('Email already exists!');
        return false;
    }
    
    // 刪除電子郵件
    removeEmail(email) {
        const profile = this.storage.get('user_profile');
        if (profile.emails && profile.emails.length > 1) {
            profile.emails = profile.emails.filter(e => e !== email);
            this.storage.set('user_profile', profile);
            this.showSuccessMessage('Email removed successfully!');
            return true;
        }
        
        this.showErrorMessage('Cannot remove the last email address!');
        return false;
    }
    
    showSuccessMessage(message) {
        this.showNotification(message, 'success');
    }
    
    showErrorMessage(message) {
        this.showNotification(message, 'error');
    }
    
    showNotification(message, type = 'info') {
        // 創建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">&times;</button>
        `;
        
        // 添加樣式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 16px;
            border-radius: 8px;
            color: white;
            background: ${type === 'success' ? '#10b981' : '#ef4444'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // 自動移除
        setTimeout(() => {
            notification.remove();
        }, 5000);
        
        // 點擊關閉
        notification.querySelector('.notification-close').onclick = () => {
            notification.remove();
        };
    }
}

// 全局初始化
window.VaultCaddyStorage = VaultCaddyStorage;
window.DocumentProcessor = DocumentProcessor;
window.FormHandler = FormHandler;

// 頁面載入時初始化
document.addEventListener('DOMContentLoaded', function() {
    if (!window.vaultcaddyStorage) {
        window.vaultcaddyStorage = new VaultCaddyStorage();
    }
    
    if (!window.documentProcessor) {
        window.documentProcessor = new DocumentProcessor();
    }
    
    if (!window.formHandler) {
        window.formHandler = new FormHandler();
    }
    
    console.log('✅ VaultCaddy Enhanced Functionality Loaded');
});

// CSS for notifications
const notificationStyles = `
<style>
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.notification {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 300px;
    font-family: 'Inter', sans-serif;
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 8px;
}

.notification-close {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    opacity: 0.8;
}

.notification-close:hover {
    opacity: 1;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', notificationStyles);
