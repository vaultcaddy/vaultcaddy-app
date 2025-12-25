# 🔧 Firebase Rules 修改指南

## 📍 在图1中的具体添加位置

### 位置1：在第18行之后添加

**当前代码（第16-18行）**：
```javascript
match /projects/{projectId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow write: if request.auth != null && request.auth.uid == userId;
```

**修改为（添加第3行）**：
```javascript
match /projects/{projectId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow write: if request.auth != null && request.auth.uid == userId;
  allow delete: if request.auth != null && request.auth.uid == userId;  // ✅ 添加这行
```

---

### 位置2：在第23行之后添加

**当前代码（第21-23行）**：
```javascript
match /documents/{documentId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow write: if request.auth != null && request.auth.uid == userId;
```

**修改为（添加第3行）**：
```javascript
match /documents/{documentId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow write: if request.auth != null && request.auth.uid == userId;
  allow delete: if request.auth != null && request.auth.uid == userId;  // ✅ 添加这行
```

---

## 📝 完整的修改后规则

复制以下完整规则，直接替换整个文件：

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // 用户文档规则
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Credits 历史记录
    match /creditsHistory/{historyId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    
    // 用户项目规则
    match /projects/{projectId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId;
      allow delete: if request.auth != null && request.auth.uid == userId;  // ✅ 新增
      
      // 项目文档规则
      match /documents/{documentId} {
        allow read: if request.auth != null && request.auth.uid == userId;
        allow write: if request.auth != null && request.auth.uid == userId;
        allow delete: if request.auth != null && request.auth.uid == userId;  // ✅ 新增
      }
    }
    
    // 验证码规则
    match /verificationCodes/{email} {
      allow read: if request.auth != null;
      allow write: if true; // 允许任何人写入验证码
    }
  }
}
```

---

## 🚀 操作步骤

### 步骤1：复制完整规则
复制上面的完整规则

### 步骤2：粘贴到Firebase Console
在图1的编辑器中：
1. 按 `Ctrl+A` 或 `Command+A` 全选
2. 粘贴新规则
3. 点击右上角的"发布"按钮

### 步骤3：等待生效（约5秒）

### 步骤4：测试删除功能
刷新Dashboard页面，尝试删除一个文档

---

## ✅ 预期效果

更新后：
- ✅ 可以正常删除项目
- ✅ 可以正常删除文档
- ✅ 只有项目所有者可以删除（安全）

---

*创建时间：2025年12月24日*

