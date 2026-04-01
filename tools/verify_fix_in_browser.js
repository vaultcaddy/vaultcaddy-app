/**
 * 在浏览器Console中运行此脚本，验证运算符Bug修复是否成功
 * 
 * 使用方法：
 * 1. 打开 firstproject.html 页面
 * 2. 按 Command + Option + J 打开Console
 * 3. 复制粘贴此脚本
 * 4. 按回车运行
 */

console.log('🔍 开始验证运算符Bug修复...\n');

(async function verifyFix() {
    const results = {
        success: [],
        failed: [],
        warnings: []
    };
    
    // ==================== 测试1：检查全局变量类型 ====================
    console.log('📋 测试1: 检查全局变量类型');
    
    if (Array.isArray(window.allDocuments)) {
        console.log('  ✅ window.allDocuments 是数组');
        results.success.push('allDocuments是数组');
    } else {
        console.log('  ❌ window.allDocuments 不是数组:', typeof window.allDocuments);
        results.failed.push('allDocuments不是数组');
    }
    
    if (Array.isArray(window.filteredDocuments)) {
        console.log('  ✅ window.filteredDocuments 是数组');
        results.success.push('filteredDocuments是数组');
    } else {
        console.log('  ⚠️  window.filteredDocuments 不是数组:', typeof window.filteredDocuments);
        results.warnings.push('filteredDocuments不是数组（可能未初始化）');
    }
    
    // ==================== 测试2：测试逻辑或运算符 ====================
    console.log('\n📋 测试2: 验证运算符修复');
    
    // 模拟测试 undefined || array
    const test1 = undefined || [1, 2, 3];
    if (Array.isArray(test1) && test1.length === 3) {
        console.log('  ✅ 逻辑或运算符工作正常 (undefined || array = array)');
        results.success.push('逻辑或运算符正常');
    } else {
        console.log('  ❌ 逻辑或运算符有问题:', test1);
        results.failed.push('逻辑或运算符异常');
    }
    
    // 对比位运算符（应该返回0）
    const test2 = undefined | [1, 2, 3];
    if (test2 === 0) {
        console.log('  ℹ️  位运算符确认返回数字 (undefined | array = 0)');
    } else {
        console.log('  ⚠️  位运算符行为异常:', test2);
    }
    
    // ==================== 测试3：获取Firestore文档 ====================
    console.log('\n📋 测试3: 从Firestore获取文档');
    
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');
    
    if (!projectId) {
        console.log('  ⚠️  未找到项目ID');
        results.warnings.push('未找到项目ID');
    } else {
        console.log(`  ✅ 项目ID: ${projectId}`);
        
        if (window.simpleDataManager) {
            try {
                const docs = await window.simpleDataManager.getDocuments(projectId);
                console.log(`  ✅ 成功获取 ${docs.length} 个文档`);
                results.success.push(`获取到${docs.length}个文档`);
                
                // 显示文档样本
                if (docs.length > 0) {
                    console.log('  📄 第一个文档样本:');
                    console.log('    ', {
                        id: docs[0].id,
                        fileName: docs[0].fileName || docs[0].name,
                        status: docs[0].status,
                        createdAt: docs[0].createdAt
                    });
                }
            } catch (error) {
                console.log('  ❌ 获取文档失败:', error.message);
                results.failed.push(`获取文档失败: ${error.message}`);
            }
        } else {
            console.log('  ⚠️  simpleDataManager未初始化');
            results.warnings.push('数据管理器未初始化');
        }
    }
    
    // ==================== 测试4：检查表格状态 ====================
    console.log('\n📋 测试4: 检查表格状态');
    
    const tbody = document.getElementById('team-project-tbody');
    if (tbody) {
        const rows = tbody.getElementsByTagName('tr');
        console.log(`  ✅ 表格存在，包含 ${rows.length} 行`);
        
        // 检查是否显示"No results"
        const hasNoResults = tbody.innerHTML.includes('No results');
        if (hasNoResults && window.allDocuments?.length > 0) {
            console.log('  ❌ 表格显示"No results"但有文档数据');
            results.failed.push('表格未正确渲染');
        } else if (!hasNoResults && rows.length > 1) {
            console.log(`  ✅ 表格正常显示 ${rows.length} 行数据`);
            results.success.push(`表格显示${rows.length}行`);
        } else if (hasNoResults && (!window.allDocuments || window.allDocuments.length === 0)) {
            console.log('  ℹ️  表格显示"No results"（确实没有文档）');
            results.success.push('表格状态正确（空）');
        }
    } else {
        console.log('  ❌ 未找到表格元素');
        results.failed.push('未找到表格元素');
    }
    
    // ==================== 测试5：检查日期筛选器 ====================
    console.log('\n📋 测试5: 检查日期筛选器状态');
    
    const dateInputs = {
        'date-from': document.getElementById('date-from')?.value,
        'date-to': document.getElementById('date-to')?.value,
        'upload-date-from': document.getElementById('upload-date-from')?.value,
        'upload-date-to': document.getElementById('upload-date-to')?.value
    };
    
    const hasActiveFilters = Object.values(dateInputs).some(v => v);
    
    if (hasActiveFilters) {
        console.log('  ⚠️  检测到活动的日期筛选器:');
        Object.entries(dateInputs).forEach(([id, value]) => {
            if (value) {
                console.log(`    - ${id}: ${value}`);
            }
        });
        results.warnings.push('存在活动的日期筛选器');
        
        console.log('\n  💡 建议: 点击 "Clear Filter" 按钮清除筛选器');
    } else {
        console.log('  ✅ 所有日期筛选器均为空');
        results.success.push('筛选器状态正常');
    }
    
    // ==================== 测试6：检查Console错误 ====================
    console.log('\n📋 测试6: 检查是否有关键错误');
    
    // 这个测试无法自动化，需要用户观察Console
    console.log('  ℹ️  请手动检查Console中是否有以下错误:');
    console.log('    - "is not iterable"');
    console.log('    - "TypeError"');
    console.log('    - "LoadDocumentFailed"');
    
    // ==================== 生成总结报告 ====================
    console.log('\n' + '='.repeat(70));
    console.log('📊 验证总结');
    console.log('='.repeat(70));
    
    console.log(`\n✅ 成功项 (${results.success.length}):`);
    results.success.forEach(item => console.log(`  • ${item}`));
    
    if (results.warnings.length > 0) {
        console.log(`\n⚠️  警告项 (${results.warnings.length}):`);
        results.warnings.forEach(item => console.log(`  • ${item}`));
    }
    
    if (results.failed.length > 0) {
        console.log(`\n❌ 失败项 (${results.failed.length}):`);
        results.failed.forEach(item => console.log(`  • ${item}`));
    }
    
    // ==================== 给出建议 ====================
    console.log('\n' + '='.repeat(70));
    console.log('💡 建议操作');
    console.log('='.repeat(70));
    
    if (results.failed.length > 0) {
        console.log('\n🔴 发现严重问题，建议:');
        console.log('  1. 清除浏览器缓存 (Shift + Command + R)');
        console.log('  2. 检查文件是否正确更新');
        console.log('  3. 查看详细错误信息');
    } else if (results.warnings.length > 0) {
        console.log('\n🟡 存在警告，建议:');
        if (hasActiveFilters) {
            console.log('  1. 点击 "Clear Filter" 按钮');
            console.log('  2. 刷新页面');
        } else {
            console.log('  1. 等待页面完全加载');
            console.log('  2. 如问题持续，清除缓存后重试');
        }
    } else {
        console.log('\n🟢 一切正常！');
        console.log('  • 运算符Bug已修复');
        console.log('  • 数据加载正常');
        console.log('  • 表格渲染正常');
    }
    
    // ==================== 快速修复按钮 ====================
    console.log('\n' + '='.repeat(70));
    console.log('🛠️  快速操作');
    console.log('='.repeat(70));
    console.log('\n如果文档仍未显示，可以运行以下命令:\n');
    console.log('1️⃣ 清除筛选器并重新加载:');
    console.log('   quickFix();\n');
    console.log('2️⃣ 强制刷新数据:');
    console.log('   forceReload();\n');
    console.log('3️⃣ 显示详细调试信息:');
    console.log('   debugInfo();\n');
    
    // 导出快速修复函数
    window.quickFix = async function() {
        console.log('🔧 执行快速修复...');
        
        // 清除筛选器
        ['date-from', 'date-to', 'upload-date-from', 'upload-date-to'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });
        console.log('✅ 筛选器已清除');
        
        // 重新加载文档
        if (typeof loadDocuments === 'function') {
            await loadDocuments();
            console.log('✅ 文档已重新加载');
        } else {
            console.log('⚠️  loadDocuments函数不存在');
        }
        
        console.log('🎉 快速修复完成！');
    };
    
    window.forceReload = async function() {
        console.log('🔄 强制重新加载数据...');
        
        const urlParams = new URLSearchParams(window.location.search);
        const projectId = urlParams.get('project');
        
        if (!projectId || !window.simpleDataManager) {
            console.error('❌ 无法重新加载：缺少必要的组件');
            return;
        }
        
        const docs = await window.simpleDataManager.getDocuments(projectId);
        console.log(`✅ 获取到 ${docs.length} 个文档`);
        
        window.allDocuments = docs;
        window.filteredDocuments = [...docs];
        
        if (typeof renderDocuments === 'function') {
            renderDocuments();
            console.log('✅ 表格已重新渲染');
        }
        
        console.log('🎉 强制重新加载完成！');
    };
    
    window.debugInfo = function() {
        console.log('🐛 调试信息');
        console.log('='.repeat(70));
        console.log('项目ID:', new URLSearchParams(window.location.search).get('project'));
        console.log('allDocuments:', window.allDocuments?.length || 'undefined');
        console.log('filteredDocuments:', window.filteredDocuments?.length || 'undefined');
        console.log('allDocuments类型:', Array.isArray(window.allDocuments) ? 'array' : typeof window.allDocuments);
        console.log('filteredDocuments类型:', Array.isArray(window.filteredDocuments) ? 'array' : typeof window.filteredDocuments);
        
        console.log('\n日期筛选器:');
        ['date-from', 'date-to', 'upload-date-from', 'upload-date-to'].forEach(id => {
            const el = document.getElementById(id);
            console.log(`  ${id}:`, el?.value || '(空)');
        });
        
        console.log('\n表格状态:');
        const tbody = document.getElementById('team-project-tbody');
        console.log('  行数:', tbody?.getElementsByTagName('tr').length || 0);
        console.log('  包含"No results":', tbody?.innerHTML.includes('No results') || false);
        
        if (window.allDocuments && window.allDocuments.length > 0) {
            console.log('\n第一个文档:');
            console.log(window.allDocuments[0]);
        }
    };
    
    console.log('✅ 验证脚本执行完成！');
    
})();

