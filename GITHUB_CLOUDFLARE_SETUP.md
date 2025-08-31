# 🚀 VaultCaddy GitHub Pages + Cloudflare 部署指南

## 📋 部署檢查清單

- [x] Git 倉庫已初始化
- [x] 代碼已提交
- [ ] GitHub 倉庫已建立
- [ ] GitHub Pages 已設定
- [ ] Cloudflare 已配置
- [ ] DNS 已設定
- [ ] SSL 已啟用

---

## 🔧 **步驟 1: 建立 GitHub 倉庫**

### 1.1 建立新倉庫
1. 前往 [https://github.com/new](https://github.com/new)
2. 填寫倉庫資訊：
   ```
   Repository name: vaultcaddy-app
   Description: VaultCaddy AI Document Processing Platform
   ✅ Public (必須是公開的才能使用免費的 GitHub Pages)
   ❌ 不要選擇任何初始化選項 (README, .gitignore, license)
   ```
3. 點擊 **"Create repository"**

### 1.2 連接本地倉庫
在你的終端機中執行：

```bash
# 添加 GitHub remote（替換成你的用戶名）
git remote add origin https://github.com/你的GitHub用戶名/vaultcaddy-app.git

# 確認分支名稱為 main
git branch -M main

# 推送代碼到 GitHub
git push -u origin main
```

**範例**（如果你的GitHub用戶名是 `cavlinyeung`）：
```bash
git remote add origin https://github.com/cavlinyeung/vaultcaddy-app.git
git branch -M main
git push -u origin main
```

---

## 📄 **步驟 2: 設定 GitHub Pages**

### 2.1 建立 gh-pages 分支
```bash
# 建立並切換到 gh-pages 分支
git checkout -b gh-pages

# 推送 gh-pages 分支到 GitHub
git push origin gh-pages

# 切換回 main 分支
git checkout main
```

### 2.2 啟用 GitHub Pages
1. 前往你的 GitHub 倉庫
2. 點擊 **"Settings"** 標籤
3. 在左側選單找到 **"Pages"**
4. 在 "Source" 部分：
   - 選擇 **"Deploy from a branch"**
   - Branch: **"gh-pages"**
   - Folder: **"/ (root)"**
5. 點擊 **"Save"**

### 2.3 驗證部署
- GitHub 會顯示：`Your site is published at https://你的用戶名.github.io/vaultcaddy-app`
- 等待 5-10 分鐘讓部署完成
- 訪問該網址確認網站正常運作

---

## ☁️ **步驟 3: 設定 Cloudflare**

### 3.1 註冊 Cloudflare
1. 前往 [https://cloudflare.com](https://cloudflare.com)
2. 點擊 **"Sign Up"** 建立免費帳戶
3. 驗證郵箱

### 3.2 添加網站
1. 登入後點擊 **"Add a Site"**
2. 輸入: `vaultcaddy.com`
3. 選擇 **"Free"** 方案
4. 點擊 **"Continue"**

### 3.3 DNS 設定
Cloudflare 會掃描現有的 DNS 記錄，然後：

1. 添加新的 DNS 記錄：
   ```
   Type: CNAME
   Name: @
   Content: 你的用戶名.github.io
   Proxy status: 🟠 Proxied (橘色雲朵圖示)
   TTL: Auto
   ```

2. 添加 www 記錄：
   ```
   Type: CNAME
   Name: www
   Content: 你的用戶名.github.io
   Proxy status: 🟠 Proxied
   TTL: Auto
   ```

3. 點擊 **"Continue"**

### 3.4 更新 Nameservers
Cloudflare 會提供兩個 nameserver，例如：
```
keenan.ns.cloudflare.com
roan.ns.cloudflare.com
```

**現在前往 GoDaddy 更新 nameservers：**

---

## 🌐 **步驟 4: 在 GoDaddy 設定 Nameservers**

### 4.1 登入 GoDaddy
1. 前往 [https://godaddy.com](https://godaddy.com)
2. 登入你的帳戶
3. 前往 **"My Products"**

### 4.2 修改 Nameservers
1. 找到 `vaultcaddy.com` 域名
2. 點擊 **"DNS"** 或 **"Manage"**
3. 找到 **"Nameservers"** 部分
4. 點擊 **"Change"** 或 **"Manage"**
5. 選擇 **"I'll use my own nameservers"**
6. 輸入 Cloudflare 提供的兩個 nameservers：
   ```
   Nameserver 1: keenan.ns.cloudflare.com
   Nameserver 2: roan.ns.cloudflare.com
   ```
7. 點擊 **"Save"**

⚠️ **重要**: DNS 更改可能需要 24-48 小時才能完全生效。

---

## 🔒 **步驟 5: 設定 SSL 和 GitHub Pages 自定義域名**

### 5.1 在 GitHub 設定自定義域名
1. 回到 GitHub 倉庫 → Settings → Pages
2. 在 **"Custom domain"** 欄位輸入: `vaultcaddy.com`
3. 點擊 **"Save"**
4. 等待 DNS 檢查完成（可能需要幾分鐘）
5. 勾選 **"Enforce HTTPS"**（DNS 生效後才能勾選）

### 5.2 Cloudflare SSL 設定
1. 在 Cloudflare Dashboard 中選擇 `vaultcaddy.com`
2. 前往 **"SSL/TLS"** 標籤
3. 設定 SSL/TLS encryption mode: **"Flexible"**
4. 前往 **"SSL/TLS" → "Edge Certificates"**
5. 確認 **"Always Use HTTPS"** 已啟用

---

## 🧪 **步驟 6: 測試部署**

### 6.1 DNS 傳播檢查
使用以下工具檢查 DNS 是否已生效：
- [https://www.whatsmydns.net](https://www.whatsmydns.net)
- 輸入 `vaultcaddy.com` 檢查 CNAME 記錄

### 6.2 網站測試
1. 訪問 `https://vaultcaddy.com`
2. 檢查以下功能：
   - [x] 網站正常載入
   - [x] HTTPS 正常工作（綠色鎖頭圖示）
   - [x] 登入按鈕功能正常
   - [x] 儀表板可以訪問
   - [x] 文件上傳界面正常

---

## 🚀 **自動化部署腳本**

我已經為你建立了部署腳本 `deploy-github.sh`：

```bash
# 使部署腳本可執行
chmod +x deploy-github.sh

# 執行部署
./deploy-github.sh
```

---

## 🔍 **故障排除**

### 問題 1: GitHub Pages 顯示 404
**解決方案:**
- 確認 `index.html` 在倉庫根目錄
- 檢查 GitHub Pages 設定是否正確
- 等待 5-10 分鐘讓部署完成

### 問題 2: 自定義域名無法工作
**解決方案:**
- 檢查 DNS 記錄是否正確設定
- 確認 nameservers 已更新到 Cloudflare
- 使用 `dig vaultcaddy.com` 檢查 DNS 解析

### 問題 3: SSL 證書錯誤
**解決方案:**
- 確認 Cloudflare SSL 設定為 "Flexible"
- 檢查 GitHub Pages 是否已啟用 "Enforce HTTPS"
- 等待證書發放（可能需要幾小時）

### 問題 4: Cloudflare 錯誤 525
**解決方案:**
- 將 SSL/TLS 模式改為 "Flexible"
- 確認源服務器（GitHub Pages）支援 SSL

---

## 📞 **需要幫助？**

如果遇到問題：

1. **檢查 DNS**: 使用 `nslookup vaultcaddy.com` 確認解析
2. **檢查 SSL**: 前往 [https://www.ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/)
3. **檢查 GitHub Pages**: 查看 Settings → Pages 中的狀態信息
4. **Cloudflare 狀態**: 檢查 Cloudflare Dashboard 中的分析數據

---

## 🎉 **完成後的結果**

成功部署後，你將擁有：

✅ **專業域名**: `https://vaultcaddy.com`  
✅ **免費 SSL**: 由 Cloudflare 提供  
✅ **全球 CDN**: Cloudflare 邊緣節點加速  
✅ **自動部署**: 推送代碼自動更新網站  
✅ **DDoS 保護**: Cloudflare 免費防護  

**你的 VaultCaddy 現在已經準備好為全世界提供服務了！** 🚀

