# 🔍 Export 菜单诊断指南

**重要**: 请按顺序执行以下步骤

---

## 第 1 步：打开浏览器开发者工具

1. 访问页面：
   ```
   https://vaultcaddy.com/en/document-detail.html?project=SJJkhY7CFdqh8zyVAM6B&id=IsaVCQfMCaDyolwDC6xS
   ```

2. **强制刷新**（清除缓存）：
   - Mac: `Cmd + Shift + R`
   - Windows: `Ctrl + Shift + R`

3. 按 `F12` 打开开发者工具

4. 切换到 **Console** 标签

---

## 第 2 步：复制并运行诊断脚本

**复制以下完整代码**，粘贴到 Console 并按 Enter：

```javascript
console.log('='.repeat(60));
console.log('🔍 Export 菜单诊断开始');
console.log('='.repeat(60));

// 1. 检查 toggleExportMenu 函数
console.log('\n1️⃣ 检查 toggleExportMenu 函数:');
console.log('   typeof window.toggleExportMenu:', typeof window.toggleExportMenu);
if (typeof window.toggleExportMenu === 'function') {
    console.log('   ✅ 函数存在');
} else {
    console.log('   ❌ 函数不存在');
}

// 2. 检查 exportMenu 元素
console.log('\n2️⃣ 检查 exportMenu 元素:');
const menu = document.getElementById('exportMenu');
console.log('   menu:', menu);
if (menu) {
    console.log('   ✅ 元素存在');
    console.log('   display:', menu.style.display);
    console.log('   innerHTML.length:', menu.innerHTML.length);
} else {
    console.log('   ❌ 元素不存在');
}

// 3. 检查 Export 按钮
console.log('\n3️⃣ 检查 Export 按钮:');
const exportBtn = document.querySelector('button[onclick*="toggleExportMenu"]');
console.log('   exportBtn:', exportBtn);
if (exportBtn) {
    console.log('   ✅ 按钮存在');
    console.log('   onclick:', exportBtn.getAttribute('onclick'));
} else {
    console.log('   ❌ 按钮不存在');
}

// 4. 检查 currentDocument
console.log('\n4️⃣ 检查 currentDocument:');
console.log('   window.currentDocument:', window.currentDocument);
if (window.currentDocument) {
    console.log('   ✅ 文档数据存在');
    console.log('   type:', window.currentDocument.type);
    console.log('   documentType:', window.currentDocument.documentType);
} else {
    console.log('   ❌ 文档数据不存在');
}

// 5. 尝试手动调用
console.log('\n5️⃣ 尝试手动调用 toggleExportMenu:');
try {
    if (typeof window.toggleExportMenu === 'function') {
        console.log('   调用中...');
        window.toggleExportMenu();
        console.log('   ✅ 调用完成（检查页面是否显示菜单）');
    }
} catch(e) {
    console.log('   ❌ 调用失败:', e.message);
    console.error(e);
}

console.log('\n' + '='.repeat(60));
console.log('✅ 诊断完成');
console.log('='.repeat(60));
```

---

## 第 3 步：截图并发送

**请将 Console 的所有输出截图**，包括：
- 所有的 ✅ 和 ❌
- 所有的日志信息
- 任何错误信息（红色文字）

---

## 第 4 步：检查页面

运行脚本后：

### 桌面端
- [ ] 页面上是否出现了 Export 菜单？
- [ ] 菜单在什么位置？（居中？按钮下方？）
- [ ] 菜单有内容吗？

### 移动端（缩小窗口到 ≤ 768px）
再次运行脚本：
- [ ] 页面上是否出现了 Export 菜单？
- [ ] 菜单在什么位置？
- [ ] 菜单有内容吗？

---

## 第 5 步：如果菜单显示了

说明函数是正常的，但 Export 按钮的 onclick 事件没有触发。

**测试按钮绑定**：

在 Console 运行：
```javascript
const btn = document.querySelector('button[onclick*="toggleExportMenu"]');
console.log('按钮:', btn);
console.log('onclick:', btn.getAttribute('onclick'));

// 手动绑定点击事件
btn.addEventListener('click', function(e) {
    console.log('🎯 按钮被点击了！');
    window.toggleExportMenu(e);
});

console.log('✅ 已重新绑定，请点击 Export 按钮测试');
```

然后点击 Export 按钮，看是否有反应。

---

## 第 6 步：如果菜单内容是空的

说明 `updateExportMenuForDocumentDetail` 函数有问题。

**检查菜单内容生成**：

在 Console 运行：
```javascript
console.log('检查 window.currentDocument:');
console.log(window.currentDocument);

if (window.currentDocument) {
    const docType = window.currentDocument.type || window.currentDocument.documentType || 'general';
    console.log('文档类型:', docType);
} else {
    console.log('❌ currentDocument 不存在，这是问题所在');
}
```

---

## 常见问题

### Q: Console 显示 "❌ 函数不存在"
**A**: 说明 JavaScript 没有加载完成或有错误。请：
1. 刷新页面
2. 查看 Console 是否有红色错误信息
3. 截图发送所有错误

### Q: 菜单显示了但是空白
**A**: 说明 `window.currentDocument` 不存在或类型不对。请：
1. 运行第 6 步的检查脚本
2. 截图发送结果

### Q: 点击按钮没反应
**A**: 说明 onclick 事件绑定有问题。请：
1. 运行第 5 步的重新绑定脚本
2. 再次点击测试

---

**请按顺序执行所有步骤，并将结果（截图 + 描述）发给我！** 📸





