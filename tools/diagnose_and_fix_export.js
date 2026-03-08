// ============================================
// Export 按钮诊断和临时修复脚本
// 直接在浏览器控制台运行（无需清除缓存）
// ============================================

console.log('🔧 开始诊断 Export 按钮问题...\n');

// 第 1 步：检查按钮是否存在
console.log('📋 步骤 1: 检查 Export 按钮');
const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
if (exportBtn) {
    console.log('✅ Export 按钮存在');
    console.log('  - onclick 属性:', exportBtn.getAttribute('onclick'));
    console.log('  - 是否可见:', window.getComputedStyle(exportBtn).display !== 'none');
    console.log('  - z-index:', window.getComputedStyle(exportBtn).zIndex);
    console.log('  - pointer-events:', window.getComputedStyle(exportBtn).pointerEvents);
} else {
    console.error('❌ Export 按钮不存在！');
}

// 第 2 步：检查 toggleExportMenu 函数
console.log('\n📋 步骤 2: 检查 toggleExportMenu 函数');
if (typeof window.toggleExportMenu === 'function') {
    console.log('✅ toggleExportMenu 函数存在');
} else {
    console.error('❌ toggleExportMenu 函数不存在！');
}

// 第 3 步：检查 exportDocument 函数
console.log('\n📋 步骤 3: 检查 exportDocument 函数');
if (typeof window.exportDocument === 'function') {
    console.log('✅ exportDocument 函数存在');
} else {
    console.warn('⚠️ exportDocument 函数不存在');
}

// 第 4 步：检查 currentDocument
console.log('\n📋 步骤 4: 检查 currentDocument');
if (window.currentDocument) {
    console.log('✅ currentDocument 存在');
    console.log('  - type:', window.currentDocument.type);
    console.log('  - documentType:', window.currentDocument.documentType);
} else {
    console.warn('⚠️ currentDocument 不存在');
}

// 第 5 步：检查菜单元素
console.log('\n📋 步骤 5: 检查 Export 菜单元素');
const menu = document.getElementById('exportMenu');
if (menu) {
    console.log('✅ Export 菜单元素存在');
    console.log('  - display:', menu.style.display);
    console.log('  - innerHTML 长度:', menu.innerHTML.length);
} else {
    console.error('❌ Export 菜单元素不存在！');
}

// 第 6 步：尝试手动触发
console.log('\n📋 步骤 6: 尝试手动触发 Export 功能');
console.log('请等待 2 秒...');

setTimeout(() => {
    console.log('\n🧪 手动触发 toggleExportMenu...');
    
    if (typeof window.toggleExportMenu === 'function') {
        try {
            window.toggleExportMenu();
            console.log('✅ toggleExportMenu() 执行完成');
            
            setTimeout(() => {
                const m = document.getElementById('exportMenu');
                if (m && m.style.display === 'block') {
                    console.log('✅ Export 菜单已显示！');
                    console.log('\n💡 结论：函数正常，可能是按钮点击事件的问题');
                    console.log('\n🔧 正在创建临时解决方案...');
                    createTemporaryFixButton();
                } else {
                    console.log('❌ Export 菜单未显示');
                    console.log('  menu.style.display:', m ? m.style.display : 'null');
                }
            }, 500);
            
        } catch (error) {
            console.error('❌ toggleExportMenu() 执行出错:', error);
        }
    } else {
        console.error('❌ 无法执行：toggleExportMenu 函数不存在');
        console.log('\n🔧 正在创建完整的临时解决方案...');
        createFullTemporarySolution();
    }
}, 2000);

// 创建临时修复按钮
function createTemporaryFixButton() {
    console.log('\n🔧 创建临时 Export 按钮...');
    
    // 移除旧的临时按钮（如果存在）
    const oldBtn = document.getElementById('temp-export-btn');
    if (oldBtn) oldBtn.remove();
    
    // 创建新按钮
    const tempBtn = document.createElement('button');
    tempBtn.id = 'temp-export-btn';
    tempBtn.innerHTML = '<i class="fas fa-download"></i> Export (临时)';
    tempBtn.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999999;
        padding: 1rem 1.5rem;
        background: #f59e0b;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    
    tempBtn.onclick = function() {
        console.log('🟡 临时 Export 按钮被点击');
        if (typeof window.toggleExportMenu === 'function') {
            window.toggleExportMenu();
        } else {
            alert('Export 功能未加载');
        }
    };
    
    document.body.appendChild(tempBtn);
    console.log('✅ 临时 Export 按钮已创建（右上角橙色按钮）');
    console.log('   请点击临时按钮测试 Export 功能');
}

// 创建完整的临时解决方案
function createFullTemporarySolution() {
    console.log('\n🔧 创建完整的临时 Export 解决方案...');
    
    // 创建简化的 toggleExportMenu
    window.toggleExportMenu = function() {
        console.log('🟡 临时 toggleExportMenu 被调用');
        
        const menu = document.getElementById('exportMenu');
        if (!menu) {
            alert('Export 菜单元素不存在');
            return;
        }
        
        // 简单的菜单内容
        menu.innerHTML = `
            <div style="padding: 1.5rem;">
                <h3 style="margin: 0 0 1rem 0;">Export Options (临时版本)</h3>
                <button onclick="alert('CSV 导出功能')" style="width: 100%; padding: 0.75rem; margin-bottom: 0.5rem; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer;">
                    📄 Export CSV
                </button>
                <button onclick="alert('JSON 导出功能')" style="width: 100%; padding: 0.75rem; margin-bottom: 0.5rem; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer;">
                    📝 Export JSON
                </button>
                <button onclick="document.getElementById('exportMenu').style.display='none'" style="width: 100%; padding: 0.75rem; margin-top: 1rem; background: #ef4444; color: white; border: none; border-radius: 6px; cursor: pointer;">
                    ❌ Close
                </button>
            </div>
        `;
        
        menu.style.display = 'block';
        menu.style.position = 'fixed';
        menu.style.top = '50%';
        menu.style.left = '50%';
        menu.style.transform = 'translate(-50%, -50%)';
        menu.style.background = 'white';
        menu.style.borderRadius = '12px';
        menu.style.boxShadow = '0 25px 50px rgba(0,0,0,0.3)';
        menu.style.zIndex = '999999';
        menu.style.minWidth = '300px';
        
        console.log('✅ 临时菜单已显示');
    };
    
    console.log('✅ 临时函数已创建');
    createTemporaryFixButton();
}

console.log('\n✅ 诊断脚本已加载');
console.log('⏳ 等待自动测试...');

