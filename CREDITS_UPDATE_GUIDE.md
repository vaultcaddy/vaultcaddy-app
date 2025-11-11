# 更新用戶 Credits 指南

## 為特定用戶添加 Credits

### 方法 1：使用 Firebase Console（推薦）

1. 前往 [Firebase Console](https://console.firebase.google.com/)
2. 選擇您的項目
3. 點擊左側菜單的「Firestore Database」
4. 找到 `users` 集合
5. 搜索用戶 email：`osclin2002@gmail.com`
6. 點擊該用戶文檔
7. 編輯 `currentCredits` 欄位，設置為 `80000`
8. 點擊「更新」

### 方法 2：使用腳本（需要 Firebase Admin SDK）

#### 步驟 1：獲取 Firebase Admin SDK 密鑰

1. 前往 [Firebase Console](https://console.firebase.google.com/)
2. 點擊左上角的齒輪圖標 → 「專案設定」
3. 點擊「服務帳戶」標籤
4. 點擊「產生新的私密金鑰」
5. 下載 JSON 文件，重命名為 `serviceAccountKey.json`
6. 將文件放在項目根目錄

#### 步驟 2：安裝依賴

```bash
npm install firebase-admin
```

#### 步驟 3：運行腳本

```bash
node update-user-credits.js
```

#### 腳本會執行以下操作：
- ✅ 查找 email 為 `osclin2002@gmail.com` 的用戶
- ✅ 更新 `currentCredits` 為 `80000`
- ✅ 記錄 Credits 歷史
- ✅ 更新時間戳

---

## 方法 3：使用 Cloud Functions（最安全）

創建一個 Cloud Function 來更新 Credits：

```javascript
exports.updateUserCredits = functions.https.onCall(async (data, context) => {
    // 檢查是否為管理員
    if (!context.auth || context.auth.uid !== 'ADMIN_UID') {
        throw new functions.https.HttpsError('permission-denied', '無權限');
    }
    
    const { email, credits } = data;
    
    // 查找用戶
    const usersSnapshot = await admin.firestore()
        .collection('users')
        .where('email', '==', email)
        .limit(1)
        .get();
    
    if (usersSnapshot.empty) {
        throw new functions.https.HttpsError('not-found', '找不到用戶');
    }
    
    const userDoc = usersSnapshot.docs[0];
    const userId = userDoc.id;
    
    // 更新 Credits
    await admin.firestore().collection('users').doc(userId).update({
        currentCredits: credits,
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    // 記錄歷史
    await admin.firestore()
        .collection('users')
        .doc(userId)
        .collection('creditsHistory')
        .add({
            type: 'admin_adjustment',
            amount: credits,
            description: '管理員手動調整 Credits',
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            balanceAfter: credits
        });
    
    return { success: true, message: `已更新 ${email} 的 Credits 為 ${credits}` };
});
```

---

## 驗證更新

更新後，可以通過以下方式驗證：

### 1. Firebase Console
- 前往 Firestore Database
- 查看用戶文檔的 `currentCredits` 欄位

### 2. 用戶界面
- 登入 `osclin2002@gmail.com` 帳戶
- 查看右上角的 Credits 顯示
- 前往 `account.html` 查看 Credits 使用情況

### 3. Credits 歷史
- 在 Firestore 中查看 `users/{userId}/creditsHistory` 集合
- 應該會看到一條「管理員手動調整 Credits」的記錄

---

## 注意事項

⚠️ **安全提示：**
- 不要將 `serviceAccountKey.json` 提交到 Git
- 已添加到 `.gitignore`
- 只在安全的環境中使用管理員密鑰

⚠️ **數據一致性：**
- 更新 Credits 時會同時更新 `updatedAt` 時間戳
- 會記錄到 Credits 歷史中
- 確保數據可追溯

---

## 常見問題

### Q: 如何查看用戶的當前 Credits？
A: 
1. Firebase Console → Firestore Database
2. 找到 `users` 集合
3. 搜索用戶 email
4. 查看 `currentCredits` 欄位

### Q: 如何查看 Credits 使用歷史？
A: 
1. 找到用戶文檔
2. 展開 `creditsHistory` 子集合
3. 查看所有記錄

### Q: 更新後用戶看不到新的 Credits？
A: 
1. 確認 Firestore 中的數據已更新
2. 讓用戶重新登入或刷新頁面
3. 檢查 `navbar-interactions.js` 是否正確讀取 Credits

---

**完成！** ✅
