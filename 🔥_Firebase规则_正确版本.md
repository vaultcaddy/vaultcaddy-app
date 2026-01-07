# 🔥 Firebase 安全规则 - 正确版本

**重要**: 根据您的实际数据结构更新

---

## 📋 您的数据结构（从截图分析）

从 Firebase Console 截图看到：
```
/documents/{documentId}
/projects/{projectId}
/creditsHistory/{historyId}
/verificationCodes/{email}
```

这是**顶层集合结构**，不是嵌套在 `/users/{userId}` 下。

---

## ✅ 正确的 Firebase 安全规则

**复制以下规则并替换到 Firebase Console**:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // 🔥 用户集合
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // 🔥 项目集合（顶层）
    match /projects/{projectId} {
      // 允许所有已认证用户访问
      // 如果需要更严格的权限，请告诉我项目如何关联用户
      allow read, write: if request.auth != null;
    }
    
    // 🔥 文档集合（顶层）- 发票/收据/银行对账单
    match /documents/{documentId} {
      // 允许所有已认证用户访问
      // 如果需要更严格的权限，需要知道文档如何关联用户
      allow read, write: if request.auth != null;
    }
    
    // 🔥 积分历史
    match /creditsHistory/{historyId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // 🔥 验证码（邮箱验证）
    match /verificationCodes/{email} {
      // 允许创建验证码
      allow create: if request.auth != null;
      // 只允许读取和更新自己邮箱的验证码
      allow read, update: if request.auth != null && 
                             (request.auth.token.email == email || 
                              request.auth.token.email == resource.data.email);
      // 允许删除（用于清理）
      allow delete: if request.auth != null;
    }
  }
}
```

---

## 🔍 如果还是无法打开发票

### 方案 1: 临时使用最宽松的规则（测试用）

**仅用于测试，找到问题后立即改回安全规则！**

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ⚠️ 警告：这允许所有已认证用户访问所有数据
    // 仅用于测试！
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

**使用这个规则测试**:
1. 如果能打开发票 → 说明是权限问题，我们再优化规则
2. 如果还是打不开 → 说明是代码问题，不是 Firebase 规则问题

---

## 🔍 排查步骤

### 步骤 1: 使用临时宽松规则测试

1. 复制上面的临时规则
2. 粘贴到 Firebase Console
3. 点击"发布"
4. 清除浏览器缓存
5. 尝试打开发票页面

### 步骤 2: 查看控制台错误

1. F12 打开控制台
2. 尝试打开发票
3. 截图控制台的错误信息
4. 告诉我具体的错误

### 步骤 3: 检查数据路径

在控制台运行以下代码，看看数据实际存储在哪里：

```javascript
// 查看当前文档的数据路径
console.log('Current URL:', window.location.href);
const params = new URLSearchParams(window.location.search);
console.log('Project ID:', params.get('project'));
console.log('Document ID:', params.get('id'));

// 尝试读取数据
if (firebase && firebase.firestore) {
    const db = firebase.firestore();
    const docId = params.get('id');
    
    // 尝试从不同路径读取
    console.log('尝试路径 1: /documents/' + docId);
    db.collection('documents').doc(docId).get()
        .then(doc => {
            if (doc.exists) {
                console.log('✅ 路径 1 成功:', doc.data());
            } else {
                console.log('❌ 路径 1: 文档不存在');
            }
        })
        .catch(err => console.error('❌ 路径 1 错误:', err));
    
    const projectId = params.get('project');
    if (projectId) {
        console.log('尝试路径 2: /projects/' + projectId + '/documents/' + docId);
        db.collection('projects').doc(projectId)
          .collection('documents').doc(docId).get()
            .then(doc => {
                if (doc.exists) {
                    console.log('✅ 路径 2 成功:', doc.data());
                } else {
                    console.log('❌ 路径 2: 文档不存在');
                }
            })
            .catch(err => console.error('❌ 路径 2 错误:', err));
    }
}
```

---

## 📊 数据结构判断

根据您的实际情况，告诉我：

### 场景 A: 文档在项目内
```
/projects/{projectId}/documents/{documentId}
```

**如果是这样，使用这个规则**:
```javascript
match /projects/{projectId} {
  allow read, write: if request.auth != null;
  
  match /documents/{documentId} {
    allow read, write: if request.auth != null;
  }
}
```

### 场景 B: 文档在顶层
```
/documents/{documentId}
```

**如果是这样，使用这个规则**:
```javascript
match /documents/{documentId} {
  allow read, write: if request.auth != null;
}
```

### 场景 C: 文档在用户下
```
/users/{userId}/projects/{projectId}/documents/{documentId}
```

**如果是这样，使用这个规则**:
```javascript
match /users/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
  
  match /projects/{projectId} {
    allow read, write: if request.auth != null && request.auth.uid == userId;
    
    match /documents/{documentId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## 🎯 快速解决方案

**立即执行**:

1. **使用临时宽松规则**（见上面"方案 1"）
2. **测试是否能打开发票**
3. **截图控制台**（F12 → Console）
4. **告诉我结果**

这样我就能确定：
- ✅ 如果能打开 → 是规则问题，我们调整规则
- ❌ 如果打不开 → 是代码问题，需要查看错误

---

## 💡 常见错误

### 错误 1: 规则太严格
```javascript
// ❌ 太严格：要求 userId 必须匹配
match /documents/{documentId} {
  allow read: if request.auth.uid == resource.data.userId;
}
// 如果文档没有 userId 字段，或字段名不对，就无法访问
```

### 错误 2: 路径不匹配
```javascript
// ❌ 规则路径
match /users/{userId}/documents/{documentId}

// 实际数据路径
/documents/{documentId}

// 结果：永远匹配不上
```

### 错误 3: 嵌套规则冲突
```javascript
// ❌ 外层允许，内层拒绝
match /projects/{projectId} {
  allow read: if request.auth != null;
  
  match /documents/{documentId} {
    allow read: if false; // 这会覆盖外层规则
  }
}
```

---

**请先使用临时宽松规则测试，然后告诉我结果！** 🔥



