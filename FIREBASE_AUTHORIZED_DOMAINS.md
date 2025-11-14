# 🔧 Firebase OAuth 授權域名設置

## 問題
```
Firebase: This domain is not authorized for OAuth operations for your Firebase project. 
Edit the list of authorized domains from the Firebase console. 
(auth/unauthorized-domain).
```

---

## ✅ 解決方法：添加授權域名

### 步驟 1：前往 Firebase Console

1. 打開瀏覽器，前往：https://console.firebase.google.com/
2. 選擇項目：`vaultcaddy-production-cbbe2`

### 步驟 2：進入 Authentication 設置

1. 在左側菜單中，點擊 **Authentication**（身份驗證）
2. 點擊頂部的 **Settings**（設置）標籤
3. 向下滾動到 **Authorized domains**（授權域名）部分

### 步驟 3：添加授權域名

**已有的域名（應該已經存在）：**
- ✅ `vaultcaddy.com`
- ✅ `localhost`（如果不存在，請添加）

**需要添加的域名（根據您的測試環境）：**

如果您使用的是文件協議（`file://`）或本地服務器，請添加：

1. **localhost** - 用於本地開發
   ```
   localhost
   ```

2. **127.0.0.1** - 用於本地 IP
   ```
   127.0.0.1
   ```

3. **您當前的測試域名** - 查看瀏覽器地址欄，如果是其他域名（如 `192.168.x.x`），也需要添加

### 步驟 4：保存設置

1. 點擊 **Add domain**（添加域名）按鈕
2. 輸入域名（不包含 `http://` 或 `https://`）
3. 點擊 **Add**（添加）
4. 等待幾秒鐘讓設置生效

---

## 📋 推薦的授權域名列表

在 Firebase Console 的 **Authorized domains** 中，確保包含以下域名：

```
vaultcaddy.com
www.vaultcaddy.com
localhost
127.0.0.1
```

**如果您使用 Firebase Hosting：**
```
vaultcaddy-production-cbbe2.web.app
vaultcaddy-production-cbbe2.firebaseapp.com
```

---

## 🧪 測試步驟

### 1. 清除瀏覽器緩存

按 `Ctrl+Shift+Delete`（Windows）或 `Cmd+Shift+Delete`（Mac），清除：
- ✅ Cookie 和其他網站數據
- ✅ 緩存的圖片和文件

### 2. 重新打開頁面

```
# 方法 A：使用 localhost
http://localhost:8080/auth.html

# 方法 B：使用 127.0.0.1
http://127.0.0.1:8080/auth.html

# 方法 C：使用實際域名
https://vaultcaddy.com/auth.html
```

### 3. 測試 Google 登入

1. 點擊「使用 Google 登入」按鈕
2. 選擇帳戶
3. ✅ 應該成功登入，不再顯示錯誤

---

## 🔍 故障排除

### 問題 1：添加域名後仍然報錯

**解決方法：**
1. 等待 5-10 分鐘（Firebase 需要時間同步）
2. 清除瀏覽器緩存
3. 關閉所有瀏覽器窗口，重新打開

### 問題 2：不知道當前使用的域名

**查看方法：**
1. 打開瀏覽器控制台（F12）
2. 在 Console 中輸入：
   ```javascript
   console.log(window.location.origin)
   ```
3. 將顯示的域名添加到 Firebase 授權列表

### 問題 3：使用文件協議（file://）

**問題：** Firebase 不支持 `file://` 協議

**解決方法：** 使用本地服務器

```bash
# 方法 A：使用 Python（推薦）
cd /Users/cavlinyeung/ai-bank-parser
python3 -m http.server 8080

# 方法 B：使用 Node.js
npx http-server -p 8080

# 方法 C：使用 PHP
php -S localhost:8080
```

然後訪問：`http://localhost:8080/auth.html`

---

## 🚀 快速命令（使用 Firebase CLI）

如果您想使用命令行添加授權域名：

```bash
# 查看當前授權域名
firebase auth:export --project vaultcaddy-production-cbbe2

# 注意：Firebase CLI 不支持直接添加授權域名
# 必須通過 Firebase Console 網頁界面添加
```

---

## 📞 需要幫助？

如果添加授權域名後仍然有問題，請告訴我：

1. 您當前使用的域名是什麼？（瀏覽器地址欄）
2. Firebase Console 中顯示的授權域名列表
3. 完整的錯誤信息（打開控制台 F12）

我會幫您進一步診斷！🚀

