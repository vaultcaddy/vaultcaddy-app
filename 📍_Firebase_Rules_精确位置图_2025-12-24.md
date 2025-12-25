# 📍 Firebase Rules 精确位置图

## 🎯 在图1中的具体操作

---

## 修改位置示意图

```javascript
1  rules_version = '2';
2  service cloud.firestore {
3    match /databases/{database}/documents {
4      
5      // 用户文档规则
6      match /users/{userId} {
7        allow read, write: if request.auth != null && request.auth.uid == userId;
8      }
9      
10     // Credits 历史记录
11     match /creditsHistory/{historyId} {
12       allow read: if request.auth != null && request.auth.uid == userId;
13       allow write: if request.auth != null && request.auth.uid == userId;
14     }
15     
16     // 用户项目规则
17     match /projects/{projectId} {
18       allow read: if request.auth != null && request.auth.uid == userId;
19       allow write: if request.auth != null && request.auth.uid == userId;
20       
21       ╔═══════════════════════════════════════════════════════════════════╗
22       ║  ✅✅✅ 在这里插入（第20行之后，第21行之前）:                  ║
23       ║  allow delete: if request.auth != null && request.auth.uid == userId; ║
24       ╚═══════════════════════════════════════════════════════════════════╝
25       
26       // 项目文档规则
27       match /documents/{documentId} {
28         allow read: if request.auth != null && request.auth.uid == userId;
29         allow write: if request.auth != null && request.auth.uid == userId;
30         
31         ╔═══════════════════════════════════════════════════════════════════╗
32         ║  ✅✅✅ 在这里插入（第30行之后，第31行之前）:                  ║
33         ║  allow delete: if request.auth != null && request.auth.uid == userId; ║
34         ╚═══════════════════════════════════════════════════════════════════╝
35         
36       }
37     }
38     
39     // 验证码规则
40     match /verificationCodes/{email} {
41       allow read: if request.auth != null;
42       allow write: if true; // 允许任何人写入验证码
43     }
44   }
45 }
```

---

## 🖱️ 鼠标操作步骤

### 第一处修改（项目删除权限）

1. **点击** 第19行末尾（`userId;` 之后）
2. **按 Enter** 创建新行
3. **输入两个空格**（对齐缩进）
4. **粘贴**：
   ```javascript
   allow delete: if request.auth != null && request.auth.uid == userId;
   ```

### 第二处修改（文档删除权限）

1. **点击** 第29行末尾（第二个 `userId;` 之后）
2. **按 Enter** 创建新行
3. **输入四个空格**（对齐缩进，文档规则嵌套更深）
4. **粘贴**：
   ```javascript
   allow delete: if request.auth != null && request.auth.uid == userId;
   ```

---

## ✅ 修改后的完整代码

复制以下内容，**全选替换**整个文件内容：

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

## 🚀 快速操作（推荐）

### 方法1：全选替换（最快）⭐

1. **打开图1的Firebase Console**
2. **点击编辑器内部**
3. **按 Ctrl+A（Windows）或 Command+A（Mac）** 全选
4. **粘贴上面的完整代码**
5. **点击"发布"按钮**

**优点**：
- ✅ 最快（1分钟）
- ✅ 不会出错
- ✅ 格式正确

---

### 方法2：手动添加两行（较慢）

如果您想保留现有格式，手动添加两行：

1. 在第19行后添加：`allow delete: if request.auth != null && request.auth.uid == userId;`
2. 在第29行后添加：`allow delete: if request.auth != null && request.auth.uid == userId;`

**注意缩进**：
- 第一处：2个空格
- 第二处：4个空格

---

## ⚠️ 常见错误

### 错误1：缩进不对齐

```javascript
// ❌ 错误（缩进太多）
    allow delete: if request.auth != null && request.auth.uid == userId;

// ✅ 正确（与上面的 allow read 对齐）
  allow delete: if request.auth != null && request.auth.uid == userId;
```

### 错误2：缺少分号

```javascript
// ❌ 错误
allow delete: if request.auth != null && request.auth.uid == userId

// ✅ 正确
allow delete: if request.auth != null && request.auth.uid == userId;
```

### 错误3：添加位置错误

```javascript
// ❌ 错误（在 match 外面）
match /projects/{projectId} {
  allow read: ...
  allow write: ...
}
allow delete: ...  // ❌ 不在 match 块内

// ✅ 正确（在 match 块内）
match /projects/{projectId} {
  allow read: ...
  allow write: ...
  allow delete: ...  // ✅ 在 match 块内
}
```

---

## ✅ 验证修改是否正确

发布后，您应该看到：

```
✅ 规则已发布
✅ 无错误
```

如果有错误，会显示红色提示，说明语法有问题。

---

## 🧪 测试删除功能

1. **刷新 Dashboard 页面**
2. **选择一个文档**
3. **点击 Delete 按钮**
4. **确认删除**

**预期结果**：
- ✅ 文档成功删除
- ✅ 页面自动刷新
- ✅ 文档从列表中消失

---

**推荐使用方法1（全选替换），最快最安全！** 🚀

---

*创建时间：2025年12月24日*  
*预计操作时间：1-2分钟*

