# ✅ 更新 JS 版本号强制刷新缓存

## 🎯 问题

浏览器缓存了旧的 `credits-manager.js` 文件，导致新代码没有生效。

---

## ✅ 解决方案

更新 HTML 文件中的版本号，强制浏览器重新下载 JS 文件。

### 修改内容

**旧版本**：
```html
<script defer src="credits-manager.js?v=20251110"></script>
```

**新版本**：
```html
<script defer src="credits-manager.js?v=20251217-v2"></script>
```

### 修改的文件
- ✅ `firstproject.html`
- ✅ `en/firstproject.html`
- ✅ `jp/firstproject.html`
- ✅ `kr/firstproject.html`

---

## 🧪 现在请重新测试

1. **刷新页面**
   - 按 `Cmd + R`（Mac）或 `Ctrl + R`（Windows）
   - 或直接刷新浏览器

2. **上传 1 个文档**

3. **打开浏览器控制台**（F12）
   - 应该看到：
     ```
     💰 扣除 Credits (通過後端 Cloud Function)
     ✅ Credits 已扣除
     ```

4. **查看 Firebase Logs**
   - 搜索：`deductCreditsClient`
   - 应该能看到日志了！

---

## 📊 预期结果

### 浏览器控制台
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 扣除 Credits (通過後端 Cloud Function)
   用户 ID: 3bLhZuU9H0b3ExhwFCJuN4vZeGb2
   扣除頁數: 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Credits 已扣除: 1 頁，剩餘: -55
```

### Firebase Logs
```
📞 客户端调用 deductCreditsClient: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, amount=1
🔍 扣除 Credits: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, current=-54, deduct=1
📡 reportUsageToStripe: userId=3bLhZuU9H0b3ExhwFCJuN4vZeGb2, quantity=1
✅ 使用量已报告给 Stripe Billing Meter
```

### Stripe Meter
应该看到新的 Meter Event！

---

## ⚠️ 如果还是不行

在浏览器控制台运行这个命令检查：

```javascript
// 检查是否使用新版本
const funcStr = window.creditsManager.deductCredits.toString();
if (funcStr.includes('deductCreditsClient')) {
    console.log('✅ 使用新代码');
} else {
    console.log('❌ 还是旧代码，请强制刷新（Cmd+Shift+R）');
}
```


