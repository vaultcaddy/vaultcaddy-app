# ✅ 修复客户端调用旧 API 问题

## 🐛 问题根源

发现 `credits-manager.js` 客户端代码在扣除 Credits 后会调用旧的 `reportCreditsUsage` 函数：

```javascript
const reportCreditsUsage = firebase.functions().httpsCallable('reportCreditsUsage');
const result = await reportCreditsUsage({ userId: user.uid });
```

这个旧函数使用 `createUsageRecord` API，导致与新的 Billing Meter Events API 冲突。

---

## ✅ 修复方案

**禁用客户端的手动报告调用**

原因：后端的 `deductCredits` 函数已经会自动调用 `reportUsageToStripe`（使用新的 Billing Meter Events API），所以客户端不需要再手动调用了。

### 修改位置
`credits-manager.js` 第338-349行

### 修改内容
- **移除**：对 `reportCreditsUsage` 的调用
- **添加**：说明使用量由后端自动报告的注释

---

## 🎯 新的工作流程

### 旧流程（有问题）
1. 客户端调用后端扣除 Credits
2. 后端扣除 Credits  
3. **客户端**手动调用 `reportCreditsUsage`（旧 API）❌

### 新流程（正确）
1. 客户端调用后端扣除 Credits
2. 后端扣除 Credits
3. **后端**自动调用 `reportUsageToStripe`（新 Billing Meter Events API）✅

---

## 📊 预期结果

修复后，当用户上传文档时：

1. ✅ Credits 正常扣除
2. ✅ 后端自动调用 `reportUsageToStripe`
3. ✅ 使用 Billing Meter Events API 报告使用量
4. ✅ 在 Stripe Dashboard 看到 Meter Events
5. ✅ Firebase Logs 显示成功报告

---

## 🧪 测试步骤

1. 清除浏览器缓存（确保加载新的 JS 文件）
2. 重新登录
3. 上传 1 个文档
4. 查看 Firebase Logs（应该只看到 `reportUsageToStripe`，不再看到 `reportCreditsUsage`）
5. 查看 Stripe Meter Events（应该有新事件）

