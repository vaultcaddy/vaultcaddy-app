# 清除浏览器缓存指南

## 🔥 重要提示
修改CSS或HTML后，**必须清除浏览器缓存**才能看到更新！

---

## 方法1：硬刷新（最快）

### Chrome / Edge
1. **Windows:** 按 `Ctrl + Shift + R` 或 `Ctrl + F5`
2. **Mac:** 按 `Cmd + Shift + R`

### Safari
1. **Mac:** 按 `Cmd + Option + R`

### Firefox
1. **Windows:** 按 `Ctrl + Shift + R` 或 `Ctrl + F5`
2. **Mac:** 按 `Cmd + Shift + R`

---

## 方法2：完全清除缓存（最彻底）

### Chrome
1. 打开开发者工具（F12）
2. **右键点击刷新按钮**
3. 选择「清空缓存并硬性重新加载」

### 或者：
1. 按 `Ctrl + Shift + Delete`（Mac: `Cmd + Shift + Delete`）
2. 选择「图片和文件」
3. 时间范围选择「所有时间」
4. 点击「清除数据」

---

## 方法3：无痕模式测试

1. **Chrome:** `Ctrl + Shift + N`（Mac: `Cmd + Shift + N`）
2. **Safari:** `Cmd + Shift + N`
3. **Firefox:** `Ctrl + Shift + P`（Mac: `Cmd + Shift + P`）

在无痕模式下访问网站，不会使用缓存。

---

## 手机版清除缓存

### iPhone (Safari)
1. 设置 → Safari
2. 滚动到底部
3. 点击「清除历史记录与网站数据」

### Android (Chrome)
1. Chrome 设置 → 隐私和安全
2. 清除浏览数据
3. 选择「缓存的图片和文件」
4. 点击「清除数据」

---

## 验证是否清除成功

打开开发者工具（F12）→ Network 标签：
- 刷新页面
- 查看 `index.html` 的 Status
- 如果显示 `200`（而不是 `304`）说明已清除缓存

---

## 🎯 修复验证清单

清除缓存后，请验证：

### 桌面版
- [ ] 茶餐厅卡片和银行卡片宽度一样
- [ ] 标题字体：1.125rem（大且粗）
- [ ] 项目价格字体：1.125rem（大且粗）
- [ ] 总计字体：1.5rem（非常大且粗）
- [ ] 两个卡片只是旋转方向不同

### 手机版
- [ ] 茶餐厅卡片不旋转
- [ ] 所有文字清晰可见
- [ ] 卡片宽度与桌面版保持比例

---

## 如果清除缓存后仍有问题

1. **检查是否是旧版本：**
   - 打开开发者工具（F12）
   - Console 标签输入：`document.querySelector('.fade-in-right div').outerHTML`
   - 检查是否包含 `style="background: white; border-radius: 16px; padding: 2rem;..."`

2. **检查CSS是否覆盖：**
   - 右键点击茶餐厅卡片
   - 选择「检查」
   - 查看 Computed 标签
   - 确认 `padding: 2rem`, `font-size: 1.125rem` (项目), `font-size: 1.5rem` (总计)

3. **如果仍有问题：**
   - 截图 Console 标签
   - 截图 Computed 标签
   - 提供浏览器版本和操作系统

---

**修改已完成！请立即清除缓存测试！** 🚀

