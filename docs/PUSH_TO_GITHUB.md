# 🚀 推送到GitHub的簡單指令

## 方法1: 使用部署腳本（推薦）
```bash
cd /Users/cavlinyeung/ai-bank-parser
./deploy-to-github.sh
```

## 方法2: 手動推送
```bash
cd /Users/cavlinyeung/ai-bank-parser
git push origin main
```

## 如果需要認證
當系統提示輸入用戶名和密碼時：
- **用戶名**: 您的GitHub用戶名
- **密碼**: 您的GitHub Personal Access Token (不是密碼)

## 生成Personal Access Token
1. 前往 https://github.com/settings/tokens
2. 點擊 "Generate new token (classic)"
3. 選擇權限: `repo` (完整倉庫權限)
4. 複製生成的token
5. 在推送時使用token作為密碼

## 推送成功後
您的網站將在以下地址可用：

### 🌐 主要頁面
- **主頁**: https://vaultcaddy.github.io/vaultcaddy-app/
- **儀表板**: https://vaultcaddy.github.io/vaultcaddy-app/dashboard.html
- **增強版演示**: https://vaultcaddy.github.io/vaultcaddy-app/enhanced-demo.html

### 🔧 測試工具
- **診斷工具**: https://vaultcaddy.github.io/vaultcaddy-app/DIAGNOSTIC_TOOL.html
- **文件處理測試**: https://vaultcaddy.github.io/vaultcaddy-app/test-file-processing.html

## ⏱️ 注意事項
- GitHub Pages 通常需要2-5分鐘來更新網站
- 首次部署可能需要更長時間
- 確保倉庫是公開的才能使用GitHub Pages

## 🎯 推薦測試順序
1. 先訪問 **enhanced-demo.html** 體驗新功能
2. 然後測試 **dashboard.html** 的完整工作流程
3. 使用 **DIAGNOSTIC_TOOL.html** 檢查系統狀態
4. 上傳 img_5268.JPG 驗證收據處理功能

---
**準備好推送了嗎？執行上面的命令即可！** 🚀
