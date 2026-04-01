/**
 * VaultCaddy 文档显示问题诊断和修复脚本
 * 
 * 作用：解决 firstproject.html 页面显示"No results"的问题
 * 使用方法：在浏览器开发者控制台中粘贴并运行此脚本
 */

console.log('🔍 开始诊断文档显示问题...\n');

// ==================== 步骤1：检查基本状态 ====================
async function diagnoseDocumentIssue() {
    const results = {
        projectId: null,
        documentsCount: 0,
        filteredCount: 0,
        dateFilters: {},
        errors: []
    };
    
    // 检查1：项目ID
    const urlParams = new URLSearchParams(window.location.search);
    results.projectId = urlParams.get('project');
    console.log(`✅ 项目ID: ${results.projectId || '❌ 未找到'}`);
    
    if (!results.projectId) {
        results.errors.push('URL中没有项目ID参数');
        console.error('❌ URL中没有项目ID！');
        return results;
    }
    
    // 检查2：SimpleDataManager是否初始化
    if (!window.simpleDataManager) {
        results.errors.push('SimpleDataManager未初始化');
        console.error('❌ SimpleDataManager未初始化！');
        return results;
    }
    console.log('✅ SimpleDataManager已初始化');
    
    // 检查3：获取原始文档数据
    try {
        const documents = await window.simpleDataManager.getDocuments(results.projectId);
        results.documentsCount = documents.length;
        console.log(`✅ 从Firestore获取到 ${documents.length} 个文档`);
        
        if (documents.length > 0) {
            console.log('\n📄 文档样本:');
            console.log(documents[0]);
        }
        
        // 保存到全局变量
        window.debugDocuments = documents;
        
    } catch (error) {
        results.errors.push(`获取文档失败: ${error.message}`);
        console.error('❌ 获取文档失败:', error);
        return results;
    }
    
    // 检查4：全局文档变量
    console.log(`\n📊 全局变量状态:`);
    console.log(`   allDocuments: ${window.allDocuments?.length || 0} 个`);
    console.log(`   filteredDocuments: ${window.filteredDocuments?.length || 0} 个`);
    results.filteredCount = window.filteredDocuments?.length || 0;
    
    // 检查5：日期筛选器状态
    const dateFrom = document.getElementById('date-from')?.value;
    const dateTo = document.getElementById('date-to')?.value;
    const uploadDateFrom = document.getElementById('upload-date-from')?.value;
    const uploadDateTo = document.getElementById('upload-date-to')?.value;
    
    results.dateFilters = {
        dateFrom,
        dateTo,
        uploadDateFrom,
        uploadDateTo
    };
    
    const hasFilters = dateFrom || dateTo || uploadDateFrom || uploadDateTo;
    console.log(`\n🗓️ 日期筛选器状态: ${hasFilters ? '✅ 已设置' : '❌ 未设置'}`);
    if (hasFilters) {
        console.log('   筛选器值:', results.dateFilters);
    }
    
    // 检查6：表格tbody状态
    const tbody = document.getElementById('team-project-tbody');
    if (tbody) {
        console.log(`\n📋 表格状态: tbody包含 ${tbody.children.length} 行`);
    } else {
        console.error('❌ 未找到表格tbody元素');
        results.errors.push('未找到表格tbody元素');
    }
    
    return results;
}

// ==================== 步骤2：应用修复 ====================
async function fixDocumentDisplay() {
    console.log('\n\n🔧 开始修复...\n');
    
    // 修复1：清除所有日期筛选器
    console.log('1️⃣ 清除日期筛选器...');
    const inputs = ['date-from', 'date-to', 'upload-date-from', 'upload-date-to'];
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.value = '';
        }
    });
    console.log('✅ 日期筛选器已清除');
    
    // 修复2：重新加载文档
    console.log('\n2️⃣ 重新加载文档...');
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');
    
    if (!projectId) {
        console.error('❌ 无法获取项目ID，修复失败');
        return;
    }
    
    try {
        const documents = await window.simpleDataManager.getDocuments(projectId);
        console.log(`✅ 获取到 ${documents.length} 个文档`);
        
        // 修复3：更新全局变量
        console.log('\n3️⃣ 更新全局变量...');
        window.allDocuments = documents;
        window.filteredDocuments = [...documents];
        console.log('✅ 全局变量已更新');
        
        // 修复4：重新渲染
        console.log('\n4️⃣ 重新渲染表格...');
        if (typeof window.renderDocuments === 'function') {
            window.renderDocuments();
            console.log('✅ 表格已重新渲染');
        } else {
            console.error('❌ renderDocuments函数不存在');
        }
        
        console.log('\n\n🎉 修复完成！请检查页面是否显示文档。');
        
    } catch (error) {
        console.error('❌ 修复失败:', error);
    }
}

// ==================== 步骤3：执行诊断和修复 ====================
(async function() {
    // 诊断
    const results = await diagnoseDocumentIssue();
    
    console.log('\n\n📊 诊断总结');
    console.log('====================');
    console.log(`项目ID: ${results.projectId || '未找到'}`);
    console.log(`Firestore文档数: ${results.documentsCount}`);
    console.log(`筛选后文档数: ${results.filteredCount}`);
    console.log(`错误数: ${results.errors.length}`);
    
    if (results.errors.length > 0) {
        console.log('\n❌ 发现的错误:');
        results.errors.forEach((error, index) => {
            console.log(`   ${index + 1}. ${error}`);
        });
    }
    
    // 如果有文档但没有显示，自动修复
    if (results.documentsCount > 0 && results.filteredCount === 0) {
        console.log('\n\n🤔 检测到: Firestore有文档但页面不显示');
        console.log('   可能原因: 日期筛选器过滤了所有文档');
        console.log('\n⏳ 将在3秒后自动修复...');
        
        setTimeout(async () => {
            await fixDocumentDisplay();
        }, 3000);
    } else if (results.documentsCount === 0) {
        console.log('\n\n⚠️ Firestore中没有文档数据');
        console.log('   可能原因:');
        console.log('   1. 项目ID不正确');
        console.log('   2. 文档还未上传');
        console.log('   3. Firestore权限问题');
    } else if (results.filteredCount > 0) {
        console.log('\n\n✅ 文档数据正常，尝试手动刷新...');
        await fixDocumentDisplay();
    }
})();

// ==================== 导出修复函数供手动调用 ====================
window.fixDocumentDisplay = fixDocumentDisplay;
console.log('\n\n💡 提示: 你可以随时运行 fixDocumentDisplay() 来重新加载文档');

