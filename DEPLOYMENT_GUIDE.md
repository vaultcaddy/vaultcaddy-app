# 🌐 VaultCaddy 部署指南 - vaultcaddy.com

## 🎯 部署方案比較

| 方案 | 費用 | 難度 | 速度 | 推薦度 |
|------|------|------|------|--------|
| **Vercel** | 免費 | ⭐ | ⭐⭐⭐ | 🥇 推薦 |
| **GitHub Pages + Cloudflare** | 免費 | ⭐⭐ | ⭐⭐ | 🥈 次推薦 |
| **Google Cloud** | 付費 | ⭐⭐⭐ | ⭐⭐⭐ | 🥉 企業級 |

---

## 🚀 方案1：Vercel 部署（推薦）

### 步驟 1: 準備代碼倉庫
```bash
# 在專案目錄中初始化 Git
cd /Users/cavlinyeung/ai-bank-parser
git init
git add .
git commit -m "Initial VaultCaddy setup"

# 推送到 GitHub
# 先在 GitHub 建立新倉庫：vaultcaddy-app
git remote add origin https://github.com/你的用戶名/vaultcaddy-app.git
git branch -M main
git push -u origin main
```

### 步驟 2: Vercel 部署
1. 訪問 [vercel.com](https://vercel.com)
2. 使用 GitHub 帳號登入
3. 點擊 "New Project"
4. 選擇 `vaultcaddy-app` 倉庫
5. 部署設定：
   ```
   Framework Preset: Other
   Build Command: (留空)
   Output Directory: .
   Install Command: npm install
   ```

### 步驟 3: 環境變數設定
在 Vercel Dashboard → Settings → Environment Variables 添加：
```
GOOGLE_CLOUD_PROJECT_ID=fifth-handbook-470515-n2
GOOGLE_APPLICATION_CREDENTIALS=你的服務帳戶JSON內容
BANK_STATEMENT_PROCESSOR_ID=你的處理器ID
...
```

### 步驟 4: 自定義域名
1. Vercel Dashboard → Settings → Domains
2. 添加 `vaultcaddy.com`
3. 按照指示設定 DNS

---

## 🌍 方案2：GitHub Pages + Cloudflare

### 步驟 1: GitHub Pages 設定
```bash
# 建立 gh-pages 分支
git checkout -b gh-pages
git push origin gh-pages

# 回到 main 分支
git checkout main
```

### 步驟 2: Repository 設定
1. GitHub → Settings → Pages
2. Source: Deploy from a branch
3. Branch: gh-pages
4. 獲得臨時網址：`https://你的用戶名.github.io/vaultcaddy-app`

### 步驟 3: Cloudflare 設定
1. 註冊 [Cloudflare](https://cloudflare.com)
2. 添加網站：`vaultcaddy.com`
3. 更新 DNS 記錄：
   ```
   Type: CNAME
   Name: @
   Content: 你的用戶名.github.io
   ```

---

## ☁️ 方案3：Google Cloud Hosting

### 步驟 1: 啟用 Google Cloud Storage
```bash
# 建立儲存桶
gsutil mb gs://vaultcaddy-web

# 設定網站配置
gsutil web set -m index.html -e 404.html gs://vaultcaddy-web
```

### 步驟 2: 上傳檔案
```bash
# 複製所有檔案到儲存桶
gsutil -m cp -r * gs://vaultcaddy-web

# 設定公開訪問
gsutil -m acl ch -r -u AllUsers:R gs://vaultcaddy-web
```

### 步驟 3: 設定 Load Balancer
1. Google Cloud Console → Network services → Load balancing
2. 建立 HTTP(S) Load Balancer
3. 後端配置：指向 Cloud Storage bucket
4. 前端配置：設定 SSL 證書

---

## 🔧 DNS 設定（GoDaddy）

無論選擇哪種方案，都需要在 GoDaddy 設定 DNS：

### Vercel 設定：
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 600
```

### Cloudflare 設定：
1. 將 nameservers 改為 Cloudflare 提供的
2. 在 Cloudflare 管理 DNS

### Google Cloud 設定：
```
Type: A
Name: @
Value: Load Balancer IP 地址
TTL: 3600
```

---

## 🔐 SSL 證書設定

### 自動 SSL（推薦）：
- **Vercel**: 自動提供 SSL
- **Cloudflare**: 免費 SSL
- **Google Cloud**: 託管 SSL 證書

### 手動 SSL：
```bash
# 使用 Let's Encrypt
certbot certonly --manual -d vaultcaddy.com -d www.vaultcaddy.com
```

---

## 🚀 部署腳本

建立自動部署腳本：

```bash
#!/bin/bash
# deploy.sh

echo "🚀 開始部署 VaultCaddy..."

# 建構應用
echo "📦 準備檔案..."
cp index.html build/
cp -r *.css build/
cp -r *.js build/
cp -r assets build/

# 部署到選擇的平台
if [ "$1" = "vercel" ]; then
    echo "🔄 部署到 Vercel..."
    vercel --prod
elif [ "$1" = "gcloud" ]; then
    echo "☁️ 部署到 Google Cloud..."
    gsutil -m rsync -r -d build/ gs://vaultcaddy-web/
else
    echo "❌ 請指定部署平台: ./deploy.sh vercel 或 ./deploy.sh gcloud"
fi

echo "✅ 部署完成！"
```

---

## 📝 部署檢查清單

### 部署前：
- [ ] 代碼推送到 Git 倉庫
- [ ] 環境變數已設定
- [ ] API 密鑰已配置
- [ ] 域名已購買

### 部署後：
- [ ] 網站可正常訪問
- [ ] HTTPS 正常工作
- [ ] API 功能測試通過
- [ ] 文檔上傳測試成功

---

## 🔍 故障排除

### 常見問題：

1. **DNS 未生效**
   - 等待 24-48 小時傳播
   - 檢查 DNS 設定是否正確

2. **SSL 證書錯誤**
   - 確認域名驗證完成
   - 檢查證書是否包含 www 子域名

3. **API 調用失敗**
   - 更新 Google Cloud API 密鑰域名限制
   - 檢查 CORS 設定

4. **404 錯誤**
   - 確認 index.html 存在
   - 檢查路由設定

---

## 🎯 推薦流程

對於 VaultCaddy，我建議這個順序：

1. **第一步**: 使用 Vercel 快速部署測試
2. **第二步**: 設定自定義域名 vaultcaddy.com
3. **第三步**: 配置 SSL 和環境變數
4. **第四步**: 測試所有功能
5. **第五步**: 根據需要升級到 Google Cloud

準備好開始了嗎？告訴我你想用哪種方案！
