# 🌐 VaultCaddy.com GoDaddy 域名設置完整指南

## 📋 設置概覽

您需要在 GoDaddy 中設置 DNS 記錄，將 `vaultcaddy.com` 指向 GitHub Pages。

## 🔧 GoDaddy DNS 設置步驟

### Step 1: 登入 GoDaddy
1. 前往 [godaddy.com](https://godaddy.com)
2. 點擊右上角 **Sign In**
3. 使用您的 GoDaddy 帳戶登入

### Step 2: 管理域名
1. 登入後，點擊 **My Products**
2. 在 **Domains** 區域找到 `vaultcaddy.com`
3. 點擊 **DNS** 按鈕（或三個點選單 → **Manage DNS**）

### Step 3: 刪除現有記錄
在設置新記錄之前，請刪除以下類型的現有記錄：
- 所有 **A records** 指向 `@`
- 任何 **CNAME records** 指向 `www`

### Step 4: 添加 GitHub Pages A Records

點擊 **Add** 按鈕，添加以下 4 個 A 記錄：

#### A Record 1
```
Type: A
Name: @
Value: 185.199.108.153
TTL: 1 Hour
```

#### A Record 2
```
Type: A
Name: @
Value: 185.199.109.153
TTL: 1 Hour
```

#### A Record 3
```
Type: A
Name: @
Value: 185.199.110.153
TTL: 1 Hour
```

#### A Record 4
```
Type: A
Name: @
Value: 185.199.111.153
TTL: 1 Hour
```

### Step 5: 添加 CNAME Record for WWW

```
Type: CNAME
Name: www
Value: vaultcaddy.github.io
TTL: 1 Hour
```

### Step 6: 保存設置
1. 檢查所有記錄都正確輸入
2. 點擊 **Save** 或 **Save All Records**

## ⏰ DNS 生效時間

- **預期時間**: 15分鐘 - 2小時
- **最長時間**: 24-48小時（很少見）
- **檢查方法**: 使用 `nslookup vaultcaddy.com` 或在線 DNS 檢查工具

## 🔍 驗證 DNS 設置

### 使用在線工具檢查
1. 前往 [whatsmydns.net](https://whatsmydns.net)
2. 輸入 `vaultcaddy.com`
3. 選擇 **A** 記錄類型
4. 檢查是否顯示 GitHub Pages IP 地址

### 使用命令行檢查 (Mac/Linux)
```bash
# 檢查 A 記錄
nslookup vaultcaddy.com

# 檢查 CNAME 記錄
nslookup www.vaultcaddy.com

# 詳細 DNS 查詢
dig vaultcaddy.com
```

### 使用命令行檢查 (Windows)
```cmd
nslookup vaultcaddy.com
nslookup www.vaultcaddy.com
```

## 📱 完整 DNS 記錄表

設置完成後，您的 DNS 記錄應該如下：

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 185.199.108.153 | 1 Hour |
| A | @ | 185.199.109.153 | 1 Hour |
| A | @ | 185.199.110.153 | 1 Hour |
| A | @ | 185.199.111.153 | 1 Hour |
| CNAME | www | vaultcaddy.github.io | 1 Hour |

## 🛠️ 常見問題和解決方案

### Q1: DNS 設置後無法訪問網站
**解決方案**:
1. 清除瀏覽器緩存
2. 嘗試無痕瀏覽模式
3. 使用不同的網絡連接測試
4. 等待更長時間（DNS 緩存問題）

### Q2: 顯示 "This site can't be reached"
**檢查項目**:
1. 確認 A 記錄 IP 地址正確
2. 確認 GitHub Pages 已啟用
3. 確認 CNAME 文件已上傳到 GitHub

### Q3: HTTPS 證書錯誤
**解決方案**:
1. 等待 GitHub 自動生成 SSL 證書（可能需要 24 小時）
2. 在 GitHub Pages 設置中勾選 "Enforce HTTPS"
3. 清除瀏覽器 HTTPS 緩存

### Q4: 重定向循環錯誤
**檢查項目**:
1. 確認只有一個 CNAME 記錄指向 www
2. 確認沒有重複的 A 記錄
3. 檢查 GitHub Pages 設置中的自定義域名

## ✅ 設置完成檢查清單

完成所有設置後，請確認：

- [ ] 4個 A 記錄都已正確添加
- [ ] CNAME 記錄已添加
- [ ] 舊的 DNS 記錄已刪除
- [ ] 等待 DNS 生效
- [ ] `https://vaultcaddy.com` 可以訪問
- [ ] `https://www.vaultcaddy.com` 可以訪問
- [ ] SSL 證書正常工作
- [ ] 網站內容正確顯示

## 🎯 下一步

DNS 設置完成並生效後：

1. **驗證網站**: 訪問 `https://vaultcaddy.com`
2. **測試功能**: 確保所有頁面和功能正常
3. **設置監控**: 配置 Google Analytics 等監控工具
4. **整合 API**: 添加真實的 Google AI API
5. **SEO 優化**: 提交 sitemap 到 Google Search Console

## 🆘 需要協助？

如果遇到問題：

1. **GoDaddy 支援**: 聯繫 GoDaddy 客服協助 DNS 設置
2. **GitHub 文檔**: 查看 GitHub Pages 自定義域名文檔
3. **社群協助**: Stack Overflow、GitHub Community
4. **專業協助**: 考慮聘請網站管理員協助

---

**🎉 設置完成後，VaultCaddy.com 將正式上線運營！**
