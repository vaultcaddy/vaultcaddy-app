/**
 * VaultCaddy Dashboard 統計和監控系統
 * 追蹤用戶使用情況、處理統計和系統狀態
 */

class VaultCaddyDashboardStats {
    constructor() {
        this.userStats = {
            totalProcessed: 0,
            successfulProcessed: 0,
            failedProcessed: 0,
            creditsUsed: 0,
            totalProcessingTime: 0,
            documentTypes: {
                'bank-statement': 0,
                'invoice': 0,
                'receipt': 0,
                'general': 0
            },
            dailyUsage: {},
            recentActivity: []
        };
        
        this.systemStats = {
            uptime: Date.now(),
            apiCalls: 0,
            errorRate: 0,
            averageProcessingTime: 0
        };
        
        this.init();
    }
    
    async init() {
        console.log('📊 Dashboard Stats 系統初始化...');
        await this.loadUserStats();
        this.setupEventListeners();
        this.startPeriodicUpdates();
        console.log('✅ Dashboard Stats 系統初始化完成');
    }
    
    /**
     * 載入用戶統計數據
     */
    async loadUserStats() {
        try {
            const stored = localStorage.getItem('vaultcaddy_user_stats');
            if (stored) {
                this.userStats = { ...this.userStats, ...JSON.parse(stored) };
            }
            
            // 初始化今日使用統計
            const today = new Date().toISOString().split('T')[0];
            if (!this.userStats.dailyUsage[today]) {
                this.userStats.dailyUsage[today] = {
                    processed: 0,
                    creditsUsed: 0,
                    documentTypes: { ...this.userStats.documentTypes }
                };
            }
            
        } catch (error) {
            console.error('載入用戶統計失敗:', error);
        }
    }
    
    /**
     * 儲存用戶統計數據
     */
    saveUserStats() {
        try {
            localStorage.setItem('vaultcaddy_user_stats', JSON.stringify(this.userStats));
        } catch (error) {
            console.error('儲存統計數據失敗:', error);
        }
    }
    
    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 監聽文檔處理完成
        document.addEventListener('documentProcessed', (event) => {
            this.recordDocumentProcessing(event.detail);
        });
        
        // 監聽批次處理完成
        document.addEventListener('batchProcessingComplete', (event) => {
            this.recordBatchProcessing(event.detail);
        });
        
        // 監聽 Credits 更新
        document.addEventListener('creditsUpdated', (event) => {
            this.recordCreditsUsage(event.detail);
        });
        
        // 頁面卸載時儲存數據
        window.addEventListener('beforeunload', () => {
            this.saveUserStats();
        });
    }
    
    /**
     * 記錄文檔處理
     */
    recordDocumentProcessing(detail) {
        const { result, documentType } = detail;
        const today = new Date().toISOString().split('T')[0];
        
        // 更新總體統計
        this.userStats.totalProcessed++;
        
        if (result.status === 'success') {
            this.userStats.successfulProcessed++;
        } else {
            this.userStats.failedProcessed++;
        }
        
        // 更新文檔類型統計
        this.userStats.documentTypes[documentType] = 
            (this.userStats.documentTypes[documentType] || 0) + 1;
        
        // 更新處理時間
        this.userStats.totalProcessingTime += result.processingTime || 0;
        
        // 更新今日統計
        if (!this.userStats.dailyUsage[today]) {
            this.userStats.dailyUsage[today] = {
                processed: 0,
                creditsUsed: 0,
                documentTypes: {}
            };
        }
        
        this.userStats.dailyUsage[today].processed++;
        this.userStats.dailyUsage[today].documentTypes[documentType] = 
            (this.userStats.dailyUsage[today].documentTypes[documentType] || 0) + 1;
        
        // 記錄最近活動
        this.addRecentActivity({
            type: 'document_processed',
            documentType,
            fileName: result.fileName,
            status: result.status,
            timestamp: new Date().toISOString()
        });
        
        // 觸發統計更新事件
        this.triggerStatsUpdate();
        this.saveUserStats();
    }
    
    /**
     * 記錄 Credits 使用
     */
    recordCreditsUsage(detail) {
        const { used } = detail;
        const today = new Date().toISOString().split('T')[0];
        
        this.userStats.creditsUsed += used;
        
        if (this.userStats.dailyUsage[today]) {
            this.userStats.dailyUsage[today].creditsUsed += used;
        }
        
        this.saveUserStats();
    }
    
    /**
     * 添加最近活動
     */
    addRecentActivity(activity) {
        this.userStats.recentActivity.unshift(activity);
        
        // 只保留最近50個活動
        if (this.userStats.recentActivity.length > 50) {
            this.userStats.recentActivity = this.userStats.recentActivity.slice(0, 50);
        }
    }
    
    /**
     * 觸發統計更新事件
     */
    triggerStatsUpdate() {
        document.dispatchEvent(new CustomEvent('statsUpdated', {
            detail: {
                userStats: this.userStats,
                systemStats: this.systemStats
            }
        }));
    }
    
    /**
     * 開始定期更新
     */
    startPeriodicUpdates() {
        // 每30秒更新一次顯示
        setInterval(() => {
            this.updateDashboardDisplays();
        }, 30000);
        
        // 每5分鐘儲存一次統計
        setInterval(() => {
            this.saveUserStats();
        }, 300000);
    }
    
    /**
     * 更新 Dashboard 顯示
     */
    updateDashboardDisplays() {
        this.updateProcessingStats();
        this.updateCreditsDisplay();
        this.updateRecentActivity();
        this.updateUsageCharts();
    }
    
    /**
     * 更新處理統計顯示
     */
    updateProcessingStats() {
        // 更新總處理數
        const totalElement = document.querySelector('[data-stat="total-processed"]');
        if (totalElement) {
            totalElement.textContent = this.userStats.totalProcessed.toLocaleString();
        }
        
        // 更新成功率
        const successRateElement = document.querySelector('[data-stat="success-rate"]');
        if (successRateElement) {
            const rate = this.userStats.totalProcessed > 0 
                ? Math.round((this.userStats.successfulProcessed / this.userStats.totalProcessed) * 100)
                : 0;
            successRateElement.textContent = `${rate}%`;
        }
        
        // 更新使用的 Credits
        const creditsElement = document.querySelector('[data-stat="credits-used"]');
        if (creditsElement) {
            creditsElement.textContent = this.userStats.creditsUsed.toLocaleString();
        }
        
        // 更新平均處理時間
        const avgTimeElement = document.querySelector('[data-stat="avg-processing-time"]');
        if (avgTimeElement) {
            const avgTime = this.userStats.totalProcessed > 0 
                ? Math.round(this.userStats.totalProcessingTime / this.userStats.totalProcessed)
                : 0;
            avgTimeElement.textContent = `${avgTime}ms`;
        }
    }
    
    /**
     * 更新 Credits 顯示
     */
    updateCreditsDisplay() {
        const currentCredits = parseInt(localStorage.getItem('userCredits') || '7');
        
        // 更新導航欄 Credits
        const navCredits = document.querySelector('.credits-count');
        if (navCredits) {
            navCredits.textContent = currentCredits;
        }
        
        // 更新 Dashboard Credits 顯示
        const dashboardCredits = document.querySelector('[data-stat="current-credits"]');
        if (dashboardCredits) {
            dashboardCredits.textContent = currentCredits;
        }
        
        // Credits 警告
        if (currentCredits < 3) {
            this.showLowCreditsWarning();
        }
    }
    
    /**
     * 顯示低 Credits 警告
     */
    showLowCreditsWarning() {
        const existingWarning = document.getElementById('low-credits-warning');
        if (existingWarning) return; // 已經顯示過了
        
        const warning = document.createElement('div');
        warning.id = 'low-credits-warning';
        warning.innerHTML = `
            <div style="position: fixed; top: 90px; right: 20px; background: #fef3c7; border: 1px solid #fcd34d; color: #92400e; padding: 1rem; border-radius: 8px; max-width: 300px; z-index: 9999; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <i class="fas fa-exclamation-triangle" style="margin-right: 0.5rem;"></i>
                    <strong>Credits 不足</strong>
                </div>
                <p style="margin: 0 0 1rem 0; font-size: 0.875rem;">您的 Credits 已不足，請考慮升級方案以繼續使用服務。</p>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="billing.html" style="padding: 0.5rem 1rem; background: #f59e0b; color: white; text-decoration: none; border-radius: 4px; font-size: 0.875rem;">升級方案</a>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" style="padding: 0.5rem 1rem; background: transparent; color: #92400e; border: 1px solid #d97706; border-radius: 4px; cursor: pointer; font-size: 0.875rem;">稍後提醒</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(warning);
        
        // 10秒後自動隱藏
        setTimeout(() => {
            if (warning.parentNode) {
                warning.parentNode.removeChild(warning);
            }
        }, 10000);
    }
    
    /**
     * 更新最近活動
     */
    updateRecentActivity() {
        const activityContainer = document.querySelector('[data-component="recent-activity"]');
        if (!activityContainer) return;
        
        const activities = this.userStats.recentActivity.slice(0, 10); // 顯示最近10個
        
        let html = '';
        activities.forEach(activity => {
            const timeAgo = this.getTimeAgo(new Date(activity.timestamp));
            const icon = this.getActivityIcon(activity.type);
            const statusColor = activity.status === 'success' ? '#059669' : '#dc2626';
            
            html += `
                <div style="display: flex; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6;">
                    <i class="fas fa-${icon}" style="margin-right: 0.75rem; color: ${statusColor}; width: 1rem;"></i>
                    <div style="flex: 1;">
                        <div style="font-weight: 500; color: #1f2937;">${activity.fileName}</div>
                        <div style="font-size: 0.875rem; color: #6b7280;">${activity.documentType} • ${timeAgo}</div>
                    </div>
                    <div style="color: ${statusColor};">
                        <i class="fas fa-${activity.status === 'success' ? 'check' : 'times'}"></i>
                    </div>
                </div>
            `;
        });
        
        if (activities.length === 0) {
            html = '<div style="text-align: center; color: #6b7280; padding: 2rem;">尚無處理記錄</div>';
        }
        
        activityContainer.innerHTML = html;
    }
    
    /**
     * 獲取活動圖標
     */
    getActivityIcon(type) {
        const icons = {
            'document_processed': 'file-alt',
            'batch_processed': 'layer-group',
            'export_downloaded': 'download'
        };
        return icons[type] || 'file-alt';
    }
    
    /**
     * 獲取相對時間
     */
    getTimeAgo(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return '剛剛';
        if (diffMins < 60) return `${diffMins} 分鐘前`;
        if (diffHours < 24) return `${diffHours} 小時前`;
        if (diffDays < 7) return `${diffDays} 天前`;
        
        return date.toLocaleDateString('zh-TW');
    }
    
    /**
     * 更新使用圖表
     */
    updateUsageCharts() {
        this.updateDocumentTypeChart();
        this.updateDailyUsageChart();
    }
    
    /**
     * 更新文檔類型圖表
     */
    updateDocumentTypeChart() {
        const chartContainer = document.querySelector('[data-chart="document-types"]');
        if (!chartContainer) return;
        
        const data = this.userStats.documentTypes;
        const total = Object.values(data).reduce((sum, count) => sum + count, 0);
        
        if (total === 0) {
            chartContainer.innerHTML = '<div style="text-align: center; color: #6b7280; padding: 2rem;">尚無處理記錄</div>';
            return;
        }
        
        let html = '';
        const colors = {
            'bank-statement': '#3b82f6',
            'invoice': '#8b5cf6',
            'receipt': '#059669',
            'general': '#f59e0b'
        };
        
        const labels = {
            'bank-statement': '銀行對帳單',
            'invoice': '發票',
            'receipt': '收據',
            'general': '通用文檔'
        };
        
        Object.entries(data).forEach(([type, count]) => {
            if (count > 0) {
                const percentage = Math.round((count / total) * 100);
                html += `
                    <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                        <div style="width: 12px; height: 12px; background: ${colors[type]}; border-radius: 2px; margin-right: 0.75rem;"></div>
                        <div style="flex: 1; display: flex; justify-content: space-between;">
                            <span style="color: #374151;">${labels[type]}</span>
                            <span style="color: #6b7280; font-weight: 500;">${count} (${percentage}%)</span>
                        </div>
                    </div>
                `;
            }
        });
        
        chartContainer.innerHTML = html;
    }
    
    /**
     * 更新每日使用圖表
     */
    updateDailyUsageChart() {
        const chartContainer = document.querySelector('[data-chart="daily-usage"]');
        if (!chartContainer) return;
        
        // 獲取最近7天的數據
        const last7Days = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];
            last7Days.push({
                date: dateStr,
                label: date.toLocaleDateString('zh-TW', { month: 'short', day: 'numeric' }),
                data: this.userStats.dailyUsage[dateStr] || { processed: 0, creditsUsed: 0 }
            });
        }
        
        const maxValue = Math.max(...last7Days.map(d => d.data.processed), 1);
        
        let html = `
            <div style="display: flex; align-items: end; height: 120px; gap: 8px; margin-bottom: 1rem;">
        `;
        
        last7Days.forEach(day => {
            const height = (day.data.processed / maxValue) * 100;
            html += `
                <div style="flex: 1; display: flex; flex-direction: column; align-items: center;">
                    <div style="background: #3b82f6; width: 100%; height: ${height}%; min-height: 2px; border-radius: 2px 2px 0 0; margin-bottom: 4px;" title="${day.data.processed} 個文檔"></div>
                    <div style="font-size: 0.75rem; color: #6b7280;">${day.label}</div>
                </div>
            `;
        });
        
        html += `
            </div>
            <div style="font-size: 0.875rem; color: #6b7280; text-align: center;">最近7天處理量</div>
        `;
        
        chartContainer.innerHTML = html;
    }
    
    /**
     * 獲取用戶統計摘要
     */
    getUserStatsSummary() {
        return {
            totalProcessed: this.userStats.totalProcessed,
            successRate: this.userStats.totalProcessed > 0 
                ? Math.round((this.userStats.successfulProcessed / this.userStats.totalProcessed) * 100)
                : 0,
            creditsUsed: this.userStats.creditsUsed,
            averageProcessingTime: this.userStats.totalProcessed > 0 
                ? Math.round(this.userStats.totalProcessingTime / this.userStats.totalProcessed)
                : 0,
            todayProcessed: this.getTodayProcessed(),
            documentTypes: this.userStats.documentTypes
        };
    }
    
    /**
     * 獲取今日處理數量
     */
    getTodayProcessed() {
        const today = new Date().toISOString().split('T')[0];
        return this.userStats.dailyUsage[today]?.processed || 0;
    }
    
    /**
     * 導出統計數據
     */
    exportStats() {
        const data = {
            userStats: this.userStats,
            systemStats: this.systemStats,
            exportedAt: new Date().toISOString(),
            version: '1.0.0'
        };
        
        const content = JSON.stringify(data, null, 2);
        const fileName = `vaultcaddy_stats_${new Date().toISOString().split('T')[0]}.json`;
        
        const blob = new Blob([content], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        console.log('✅ 統計數據已導出');
    }
    
    /**
     * 重置統計數據
     */
    resetStats() {
        if (confirm('確定要重置所有統計數據嗎？此操作無法撤銷。')) {
            this.userStats = {
                totalProcessed: 0,
                successfulProcessed: 0,
                failedProcessed: 0,
                creditsUsed: 0,
                totalProcessingTime: 0,
                documentTypes: {
                    'bank-statement': 0,
                    'invoice': 0,
                    'receipt': 0,
                    'general': 0
                },
                dailyUsage: {},
                recentActivity: []
            };
            
            this.saveUserStats();
            this.updateDashboardDisplays();
            
            console.log('📊 統計數據已重置');
        }
    }
}

// 全局實例
window.VaultCaddyStats = new VaultCaddyDashboardStats();

// 導出給其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaultCaddyDashboardStats;
}
