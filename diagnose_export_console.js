// 🔍 在浏览器 Console 运行这个诊断脚本

console.log('='.repeat(60));
console.log('🔍 Export 菜单诊断开始');
console.log('='.repeat(60));

// 1. 检查 toggleExportMenu 函数
console.log('\n1️⃣ 检查 toggleExportMenu 函数:');
console.log('   typeof window.toggleExportMenu:', typeof window.toggleExportMenu);
if (typeof window.toggleExportMenu === 'function') {
    console.log('   ✅ 函数存在');
} else {
    console.log('   ❌ 函数不存在或类型错误');
}

// 2. 检查 exportMenu 元素
console.log('\n2️⃣ 检查 exportMenu 元素:');
const menu = document.getElementById('exportMenu');
console.log('   menu:', menu);
if (menu) {
    console.log('   ✅ 元素存在');
    console.log('   menu.style.display:', menu.style.display);
    console.log('   menu.innerHTML.length:', menu.innerHTML.length);
} else {
    console.log('   ❌ 元素不存在');
}

// 3. 检查 exportMenuOverlay 元素
console.log('\n3️⃣ 检查 exportMenuOverlay 元素:');
const overlay = document.getElementById('exportMenuOverlay');
console.log('   overlay:', overlay);
if (overlay) {
    console.log('   ✅ 元素存在');
} else {
    console.log('   ⚠️  元素不存在（会动态创建）');
}

// 4. 检查 Export 按钮
console.log('\n4️⃣ 检查 Export 按钮:');
const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
console.log('   exportBtn:', exportBtn);
if (exportBtn) {
    console.log('   ✅ 按钮存在');
    console.log('   onclick 属性:', exportBtn.getAttribute('onclick'));
} else {
    console.log('   ❌ 按钮不存在');
}

// 5. 检查 currentDocument
console.log('\n5️⃣ 检查 currentDocument:');
console.log('   window.currentDocument:', window.currentDocument);
if (window.currentDocument) {
    console.log('   ✅ 文档数据存在');
    console.log('   type:', window.currentDocument.type);
    console.log('   documentType:', window.currentDocument.documentType);
} else {
    console.log('   ❌ 文档数据不存在');
}

// 6. 检查 closeExportMenu 函数
console.log('\n6️⃣ 检查 closeExportMenu 函数:');
console.log('   typeof window.closeExportMenu:', typeof window.closeExportMenu);

// 7. 检查 updateExportMenuForDocumentDetail 函数
console.log('\n7️⃣ 检查 updateExportMenuForDocumentDetail 函数:');
console.log('   typeof updateExportMenuForDocumentDetail:', typeof updateExportMenuForDocumentDetail);

// 8. 手动测试函数调用
console.log('\n8️⃣ 尝试手动调用 toggleExportMenu:');
try {
    if (typeof window.toggleExportMenu === 'function') {
        console.log('   调用 window.toggleExportMenu()...');
        window.toggleExportMenu();
        console.log('   ✅ 调用成功（检查页面是否显示菜单）');
    } else {
        console.log('   ❌ 无法调用，函数不存在');
    }
} catch(e) {
    console.log('   ❌ 调用失败:', e.message);
    console.error(e);
}

console.log('\n' + '='.repeat(60));
console.log('🔍 诊断完成');
console.log('='.repeat(60));

console.log('\n📋 请将以上所有输出截图发给我！');

