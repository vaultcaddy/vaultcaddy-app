/**
 * FirstProject.html 自动修复补丁
 * 
 * 作用：
 * 1. 在页面加载时自动检测并修复可能导致"No results"的问题
 * 2. 改进loadDocuments函数，添加更多调试信息
 * 3. 改进clearDateFilters函数，使其更加用户友好
 * 
 * 使用方法：
 * 1. 将此脚本添加到 firstproject.html 的 <head> 部分
 * 2. 或在现有代码中插入相关函数
 */

// ==================== 补丁1：页面加载时自动检测和修复 ====================

/**
 * 在用户登录成功后自动运行的检测和修复函数
 * 插入位置：window.addEventListener('VaultCaddyUserLoginSuccess') 事件处理器的开头
 */
async function autoFixDocumentDisplay() {
    console.log('🔍 [AutoFix] 开始自动检测文档显示问题...');
    
    // 等待1秒，确保所有初始化完成
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 检查1：清除可能残留的日期筛选器值
    const filterInputs = ['date-from', 'date-to', 'upload-date-from', 'upload-date-to'];
    let hasFilters = false;
    
    filterInputs.forEach(id => {
        const input = document.getElementById(id);
        if (input && input.value) {
            console.log(`⚠️ [AutoFix] 检测到筛选器 ${id} 有值: ${input.value}`);
            hasFilters = true;
            // 清除值
            input.value = '';
        }
    });
    
    if (hasFilters) {
        console.log('✅ [AutoFix] 已自动清除日期筛选器');
    }
    
    // 检查2：验证文档数据
    if (window.allDocuments && window.allDocuments.length > 0) {
        console.log(`✅ [AutoFix] 检测到 ${window.allDocuments.length} 个文档`);
        
        // 如果filteredDocuments为空或长度不匹配，重置它
        if (!window.filteredDocuments || window.filteredDocuments.length !== window.allDocuments.length) {
            console.log('⚠️ [AutoFix] filteredDocuments状态异常，正在修复...');
            window.filteredDocuments = [...window.allDocuments];
            
            // 重新渲染
            if (typeof window.renderDocuments === 'function') {
                window.renderDocuments();
                console.log('✅ [AutoFix] 已重新渲染文档列表');
            }
        }
    }
    
    console.log('✅ [AutoFix] 自动检测完成');
}

// ==================== 补丁2：改进的loadDocuments函数 ====================

/**
 * 替换原有的loadDocuments函数
 * 添加了更详细的日志和错误处理
 */
async function loadDocumentsImproved() {
    try {
        if (!currentProjectId) {
            console.error('❌ [LoadDocs] 没有项目ID');
            return;
        }
        
        console.log('📄 [LoadDocs] 开始加载文档...');
        console.log(`   项目ID: ${currentProjectId}`);
        
        // 获取文档
        const documents = await window.simpleDataManager.getDocuments(currentProjectId);
        console.log(`✅ [LoadDocs] 从Firestore获取到 ${documents.length} 个文档`);
        
        // 保存到全局变量
        allDocuments = documents;
        window.allDocuments = documents;
        window.filteredDocuments = [...documents];
        console.log(`✅ [LoadDocs] 全局变量已更新:`);
        console.log(`   - allDocuments: ${allDocuments.length} 个`);
        console.log(`   - filteredDocuments: ${window.filteredDocuments.length} 个`);
        
        // 检查表格元素
        const tbody = document.getElementById('team-project-tbody');
        if (!tbody) {
            console.error('❌ [LoadDocs] 未找到表格tbody元素');
            return;
        }
        
        // 如果没有文档
        if (documents.length === 0) {
            console.log('⚠️ [LoadDocs] Firestore中没有文档，显示空状态');
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" style="text-align: center; padding: 4rem 2rem;">
                        <div style="color: #6b7280;">
                            <i class="fas fa-file-alt" style="font-size: 3rem; margin-bottom: 1rem; color: #d1d5db;"></i>
                            <h3 style="font-size: 1.2rem; margin-bottom: 0.5rem; color: #374151;">No results.</h3>
                            <p style="font-size: 0.875rem; color: #6b7280;">No documents found in this project.</p>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }
        
        // 渲染文档
        console.log('🎨 [LoadDocs] 开始渲染文档表格...');
        renderDocuments();
        console.log('✅ [LoadDocs] 文档列表渲染完成');
        
        // 自动处理pending状态的文档
        resumePendingDocuments(documents);
        
    } catch (error) {
        console.error('❌ [LoadDocs] 加载文档失败:', error);
        console.error('   错误堆栈:', error.stack);
        
        // 显示错误信息
        const tbody = document.getElementById('team-project-tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" style="text-align: center; padding: 4rem 2rem;">
                        <div style="color: #ef4444;">
                            <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                            <h3 style="font-size: 1.2rem; margin-bottom: 0.5rem;">加载失败</h3>
                            <p style="font-size: 0.875rem; color: #6b7280;">${error.message}</p>
                            <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer;">
                                重新加载
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }
    }
}

// ==================== 补丁3：改进的clearDateFilters函数 ====================

/**
 * 替换原有的clearDateFilters函数
 * 添加了用户反馈和更详细的日志
 */
function clearDateFiltersImproved() {
    console.log('🗑️ [ClearFilters] 清除所有日期筛选器...');
    
    // 记录清除前的状态
    const beforeState = {
        dateFrom: document.getElementById('date-from')?.value,
        dateTo: document.getElementById('date-to')?.value,
        uploadDateFrom: document.getElementById('upload-date-from')?.value,
        uploadDateTo: document.getElementById('upload-date-to')?.value
    };
    
    const hadFilters = Object.values(beforeState).some(v => v);
    
    if (hadFilters) {
        console.log('   清除前的筛选器:', beforeState);
    }
    
    // 重置筛选器状态
    dateFilters = {
        dateFrom: null,
        dateTo: null,
        uploadDateFrom: null,
        uploadDateTo: null
    };
    
    // 清空输入框
    ['date-from', 'date-to', 'upload-date-from', 'upload-date-to'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.value = '';
        }
    });
    
    // 重置筛选列表
    const beforeCount = window.filteredDocuments?.length || 0;
    window.filteredDocuments = [...allDocuments];
    const afterCount = window.filteredDocuments?.length || 0;
    
    console.log(`✅ [ClearFilters] 筛选器已清除`);
    console.log(`   文档数量: ${beforeCount} → ${afterCount}`);
    
    // 重新渲染
    renderDocuments();
    
    // 用户反馈
    if (hadFilters && afterCount > beforeCount) {
        // 显示一个临时提示
        showToast(`✅ 筛选器已清除，显示 ${afterCount} 个文档`, 'success');
    } else if (!hadFilters) {
        showToast('ℹ️ 没有活动的筛选器', 'info');
    }
}

// ==================== 补丁4：Toast通知函数 ====================

/**
 * 显示临时提示信息
 * @param {string} message - 提示信息
 * @param {string} type - 类型：'success', 'error', 'info', 'warning'
 * @param {number} duration - 显示时长（毫秒），默认3000
 */
function showToast(message, type = 'info', duration = 3000) {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.textContent = message;
    
    // 样式
    const colors = {
        success: { bg: '#10b981', border: '#059669' },
        error: { bg: '#ef4444', border: '#dc2626' },
        info: { bg: '#3b82f6', border: '#2563eb' },
        warning: { bg: '#f59e0b', border: '#d97706' }
    };
    
    const color = colors[type] || colors.info;
    
    Object.assign(toast.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        background: color.bg,
        color: 'white',
        borderRadius: '8px',
        border: `2px solid ${color.border}`,
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        zIndex: '99999',
        fontSize: '14px',
        fontWeight: '500',
        maxWidth: '400px',
        animation: 'slideInRight 0.3s ease-out'
    });
    
    // 添加到页面
    document.body.appendChild(toast);
    
    // 自动移除
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, duration);
}

// 添加动画样式
if (!document.getElementById('toast-animations')) {
    const style = document.createElement('style');
    style.id = 'toast-animations';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// ==================== 使用说明 ====================

/**
 * 如何应用这些补丁到 firstproject.html：
 * 
 * 1. 在 window.addEventListener('VaultCaddyUserLoginSuccess') 的开头添加：
 *    await autoFixDocumentDisplay();
 * 
 * 2. 替换现有的 loadDocuments 函数为 loadDocumentsImproved
 * 
 * 3. 替换现有的 clearDateFilters 函数为 clearDateFiltersImproved
 * 
 * 4. 添加 showToast 函数到全局作用域
 * 
 * 或者，直接在浏览器Console中运行这些函数来测试效果。
 */

// 导出到全局作用域（用于Console测试）
if (typeof window !== 'undefined') {
    window.autoFixDocumentDisplay = autoFixDocumentDisplay;
    window.loadDocumentsImproved = loadDocumentsImproved;
    window.clearDateFiltersImproved = clearDateFiltersImproved;
    window.showToast = showToast;
    
    console.log('✅ 补丁函数已加载到全局作用域');
    console.log('   - autoFixDocumentDisplay()');
    console.log('   - loadDocumentsImproved()');
    console.log('   - clearDateFiltersImproved()');
    console.log('   - showToast(message, type)');
}

// ==================== 开发者工具：一键应用所有补丁 ====================

/**
 * 在Console中运行此函数，立即应用所有改进
 */
window.applyAllPatches = function() {
    console.log('🔧 应用所有补丁...\n');
    
    // 1. 运行自动修复
    autoFixDocumentDisplay().then(() => {
        console.log('✅ 自动修复完成');
    });
    
    // 2. 替换函数
    if (typeof loadDocuments !== 'undefined') {
        window.loadDocuments = loadDocumentsImproved;
        console.log('✅ loadDocuments 已更新');
    }
    
    if (typeof clearDateFilters !== 'undefined') {
        window.clearDateFilters = clearDateFiltersImproved;
        console.log('✅ clearDateFilters 已更新');
    }
    
    console.log('\n🎉 所有补丁已应用！');
    console.log('   页面功能已增强，现在更容易诊断和修复问题。');
};

console.log('\n💡 提示: 运行 applyAllPatches() 立即应用所有改进');

