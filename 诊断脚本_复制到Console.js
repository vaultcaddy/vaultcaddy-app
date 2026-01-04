// ═══════════════════════════════════════════════════════════════════
// VaultCaddy Document Detail 诊断脚本
// 使用方法：复制整个文件内容 → 粘贴到浏览器Console → 回车
// ═══════════════════════════════════════════════════════════════════

(async function diagnose() {
    console.log('');
    console.log('🔍 ═════════════════════════════════════════════════════');
    console.log('🔍   VaultCaddy Document Detail 诊断开始');
    console.log('🔍 ═════════════════════════════════════════════════════');
    console.log('');
    
    // ===================================================================
    // 步骤1: 检查URL参数
    // ===================================================================
    console.log('📋 步骤 1/5: 检查URL参数');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');
    const documentId = urlParams.get('id');
    
    console.log('   当前URL:', window.location.href);
    console.log('   Project ID:', projectId || '❌ 缺失');
    console.log('   Document ID:', documentId || '❌ 缺失');
    
    if (!projectId || !documentId) {
        console.error('   ❌ 错误：缺少必要的URL参数');
        console.log('   解决方案：确保URL包含 ?project=xxx&id=xxx');
        return;
    } else {
        console.log('   ✅ URL参数正确');
    }
    console.log('');
    
    // ===================================================================
    // 步骤2: 检查Firebase
    // ===================================================================
    console.log('🔥 步骤 2/5: 检查Firebase');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    console.log('   Firebase存在:', !!window.firebase ? '✅ 是' : '❌ 否');
    console.log('   Firestore存在:', !!window.firebase?.firestore ? '✅ 是' : '❌ 否');
    console.log('   Auth存在:', !!window.firebase?.auth ? '✅ 是' : '❌ 否');
    console.log('   Storage存在:', !!window.firebase?.storage ? '✅ 是' : '❌ 否');
    
    if (!window.firebase) {
        console.error('   ❌ 错误：Firebase SDK未加载');
        console.log('   解决方案：');
        console.log('      1. 检查网络连接');
        console.log('      2. 检查firebase-config.js是否加载');
        console.log('      3. 查看Network标签确认Firebase CDN访问正常');
        return;
    } else {
        console.log('   ✅ Firebase SDK已加载');
    }
    console.log('');
    
    // ===================================================================
    // 步骤3: 检查SimpleAuth
    // ===================================================================
    console.log('👤 步骤 3/5: 检查SimpleAuth');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    console.log('   SimpleAuth存在:', !!window.simpleAuth ? '✅ 是' : '❌ 否');
    
    if (window.simpleAuth) {
        console.log('   SimpleAuth已初始化:', window.simpleAuth.initialized ? '✅ 是' : '❌ 否');
        console.log('   当前用户:', window.simpleAuth.currentUser?.email || '❌ 未登录');
        
        if (!window.simpleAuth.initialized) {
            console.error('   ❌ 错误：SimpleAuth未初始化');
            console.log('   解决方案：等待2秒后刷新页面');
        } else if (!window.simpleAuth.currentUser) {
            console.error('   ❌ 错误：用户未登录');
            console.log('   解决方案：');
            console.log('      1. 访问 https://vaultcaddy.com/ 登录');
            console.log('      2. 然后再访问document-detail页面');
        } else {
            console.log('   ✅ SimpleAuth正常，用户已登录');
        }
    } else {
        console.error('   ❌ 错误：SimpleAuth不存在');
        console.log('   解决方案：检查simple-auth.js是否加载（Network标签）');
    }
    console.log('');
    
    // ===================================================================
    // 步骤4: 检查SimpleDataManager
    // ===================================================================
    console.log('📦 步骤 4/5: 检查SimpleDataManager');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    console.log('   SimpleDataManager存在:', !!window.simpleDataManager ? '✅ 是' : '❌ 否');
    
    if (window.simpleDataManager) {
        console.log('   SimpleDataManager已初始化:', window.simpleDataManager.initialized ? '✅ 是' : '❌ 否');
        
        if (!window.simpleDataManager.initialized) {
            console.error('   ❌ 错误：SimpleDataManager未初始化');
            console.log('   解决方案：等待2秒后刷新页面');
        } else {
            console.log('   ✅ SimpleDataManager正常');
        }
    } else {
        console.error('   ❌ 错误：SimpleDataManager不存在');
        console.log('   解决方案：检查simple-data-manager.js是否加载（Network标签）');
    }
    console.log('');
    
    // ===================================================================
    // 步骤5: 尝试获取文档
    // ===================================================================
    console.log('📄 步骤 5/5: 尝试获取文档数据');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    if (!window.simpleDataManager || !window.simpleDataManager.initialized) {
        console.error('   ⚠️ 跳过：SimpleDataManager未就绪');
    } else if (!projectId || !documentId) {
        console.error('   ⚠️ 跳过：缺少URL参数');
    } else {
        try {
            console.log('   正在从Firebase获取文档...');
            
            const doc = await window.simpleDataManager.getDocument(projectId, documentId);
            
            if (doc) {
                console.log('   ✅ 文档获取成功！');
                console.log('');
                console.log('   文档详情：');
                console.log('   ├─ 文档ID:', doc.id || documentId);
                console.log('   ├─ 文档名称:', doc.name || doc.fileName || '未命名');
                console.log('   ├─ 文档类型:', doc.type || doc.documentType || '未知');
                console.log('   ├─ 处理状态:', doc.status || '未知');
                console.log('   ├─ 是否处理中:', doc.isProcessing ? '是' : '否');
                console.log('   ├─ 处理进度:', doc.processingProgress || 'N/A');
                console.log('   ├─ 有processedData:', !!doc.processedData ? '✅ 是' : '❌ 否');
                console.log('   └─ 创建时间:', doc.createdAt?.toDate?.() || doc.createdAt || '未知');
                
                if (!doc.processedData) {
                    console.warn('');
                    console.warn('   ⚠️ 警告：文档缺少processedData字段');
                    console.warn('   可能原因：');
                    console.warn('      1. 文档还在处理中');
                    console.warn('      2. 处理失败');
                    console.warn('      3. 数据结构不完整');
                }
                
                console.log('');
                console.log('   完整文档对象:');
                console.log(doc);
                
            } else {
                console.error('   ❌ 文档不存在');
                console.log('   可能原因：');
                console.log('      1. 文档已被删除');
                console.log('      2. 文档ID错误');
                console.log('      3. 没有权限访问');
                console.log('      4. Firestore规则太严格');
            }
            
        } catch (error) {
            console.error('   ❌ 获取文档失败');
            console.error('   错误信息:', error.message);
            console.error('   错误详情:', error);
            console.log('');
            console.log('   可能原因：');
            console.log('      1. 网络连接问题');
            console.log('      2. Firebase权限不足');
            console.log('      3. Firestore规则拒绝');
            console.log('      4. 文档路径错误');
        }
    }
    
    console.log('');
    console.log('🔍 ═════════════════════════════════════════════════════');
    console.log('🔍   诊断完成！');
    console.log('🔍 ═════════════════════════════════════════════════════');
    console.log('');
    console.log('📸 请截图整个Console内容发给开发者');
    console.log('');
    console.log('💡 小提示：');
    console.log('   • 如果看到 ❌ 错误，请按照对应的解决方案操作');
    console.log('   • 如果所有步骤都是 ✅，但页面仍无法显示，请联系开发者');
    console.log('   • 可以按 F12 → Network 标签检查文件加载情况');
    console.log('');
    
})();


