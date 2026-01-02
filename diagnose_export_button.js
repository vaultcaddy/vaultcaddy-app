// ============================================
// VaultCaddy Export 按钮诊断脚本
// 复制整个脚本到浏览器控制台运行
// ============================================

console.log('🔍 开始诊断 Export 功能...\n');

// 1. 检查关键函数是否存在
console.log('📋 检查关键函数:');
console.log('  toggleExportMenu:', typeof window.toggleExportMenu);
console.log('  closeExportMenu:', typeof window.closeExportMenu);
console.log('  exportDocument:', typeof window.exportDocument);

// 2. 检查 DOM 元素
console.log('\n📋 检查 DOM 元素:');
const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
console.log('  Export 按钮:', exportBtn ? '✅ 存在' : '❌ 不存在');
if (exportBtn) {
    console.log('    - onclick属性:', exportBtn.getAttribute('onclick'));
    console.log('    - 可见性:', window.getComputedStyle(exportBtn).display !== 'none' ? '✅ 可见' : '❌ 隐藏');
}

const exportMenu = document.getElementById('exportMenu');
console.log('  Export 菜单:', exportMenu ? '✅ 存在' : '❌ 不存在');
if (exportMenu) {
    console.log('    - display:', exportMenu.style.display);
    console.log('    - innerHTML长度:', exportMenu.innerHTML.length);
}

const exportOverlay = document.getElementById('exportMenuOverlay');
console.log('  Export 遮罩:', exportOverlay ? '✅ 存在' : '❌ 不存在');

// 3. 检查当前文档
console.log('\n📋 检查当前文档:');
console.log('  window.currentDocument:', window.currentDocument ? '✅ 存在' : '❌ 不存在');
if (window.currentDocument) {
    console.log('    - id:', window.currentDocument.id);
    console.log('    - type:', window.currentDocument.type);
    console.log('    - documentType:', window.currentDocument.documentType);
    console.log('    - processedData:', window.currentDocument.processedData ? '✅ 有数据' : '❌ 无数据');
}

// 4. 尝试手动打开菜单
console.log('\n🧪 尝试手动触发 Export 菜单...');
if (typeof window.toggleExportMenu === 'function') {
    try {
        window.toggleExportMenu();
        console.log('✅ toggleExportMenu() 执行成功');
        
        // 检查菜单是否显示
        setTimeout(() => {
            const menu = document.getElementById('exportMenu');
            if (menu && menu.style.display === 'block') {
                console.log('✅ Export 菜单已显示');
                console.log('  菜单内容预览:', menu.innerHTML.substring(0, 200) + '...');
            } else {
                console.log('❌ Export 菜单未显示');
                if (menu) {
                    console.log('  display 状态:', menu.style.display);
                }
            }
        }, 100);
    } catch (error) {
        console.error('❌ toggleExportMenu() 执行出错:', error);
    }
} else {
    console.log('❌ toggleExportMenu 函数不存在');
}

// 5. 检查控制台错误
console.log('\n📋 其他检查:');
console.log('  页面URL:', window.location.href);
console.log('  视口宽度:', window.innerWidth);
console.log('  视口高度:', window.innerHeight);

console.log('\n✅ 诊断完成！请查看上方结果。');
console.log('如果看到任何 ❌，请截图并报告。');

