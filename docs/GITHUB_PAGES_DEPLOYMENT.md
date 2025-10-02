# 🚀 VaultCaddy GitHub Pages 部署指南

## 📋 部署狀態

✅ **已完成的更新**
- 智能OCR處理器 (Google AI + Tesseract.js)
- JavaScript版數據處理器 (類pandas功能)
- 智能OCR選擇器 (5種處理模式)
- 增強版統一文檔處理器
- 現代化演示界面

## 🌐 網站訪問地址

### 主要頁面
- **主頁**: https://vaultcaddy.github.io/vaultcaddy-app/
- **儀表板**: https://vaultcaddy.github.io/vaultcaddy-app/dashboard.html
- **增強版演示**: https://vaultcaddy.github.io/vaultcaddy-app/enhanced-demo.html
- **診斷工具**: https://vaultcaddy.github.io/vaultcaddy-app/DIAGNOSTIC_TOOL.html

### 測試頁面
- **文件處理測試**: https://vaultcaddy.github.io/vaultcaddy-app/test-file-processing.html

## 🎯 推薦測試流程

### 1. 增強版演示測試
```
訪問: enhanced-demo.html
測試內容:
✅ 5種OCR處理模式
✅ 拖放文件上傳
✅ 實時處理進度
✅ 質量評分顯示
✅ 多格式導出
```

### 2. 主系統測試
```
訪問: dashboard.html
測試內容:
✅ 上傳 img_5268.JPG 到收據頁面
✅ 驗證智能OCR處理
✅ 檢查數據提取準確性
✅ 測試文件持久化
✅ 驗證跨頁面數據同步
```

### 3. 診斷工具測試
```
訪問: DIAGNOSTIC_TOOL.html
檢查內容:
✅ 處理器載入狀態
✅ API密鑰配置
✅ 存儲數據檢查
✅ 系統健康狀態
```

## 🔧 部署方法

### 方法1: 使用部署腳本
```bash
# 在項目根目錄執行
./deploy-to-github.sh
```

### 方法2: 手動部署
```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "🚀 Deploy: 開源技術整合版本"

# 推送到GitHub
git push origin main
```

## 📊 新功能特色

### 🧠 智能OCR處理器
- **Google AI**: 高準確度，適合重要文檔
- **Tesseract.js**: 離線處理，保護隱私
- **智能選擇**: 根據文檔類型自動選擇最佳引擎

### 📈 處理模式
| 模式 | 特點 | 適用場景 |
|------|------|----------|
| 🎯 智能平衡 | 自動選擇最佳引擎 | 一般用戶推薦 |
| 🎯 準確度優先 | 使用最準確的引擎 | 重要文檔處理 |
| ⚡ 速度優先 | 選擇最快的引擎 | 批量處理 |
| 🔒 隱私模式 | 完全離線處理 | 敏感文檔 |
| 💰 預算模式 | 優先免費引擎 | 成本控制 |

### 📊 數據處理功能
- **統計分析**: 交易統計、分類分析、趨勢識別
- **智能洞察**: 現金流分析、異常檢測、消費模式
- **多格式導出**: CSV、Excel、JSON、PDF報告

## 🔍 故障排除

### 如果網站無法訪問
1. 檢查GitHub Pages是否已啟用
2. 確認倉庫是公開的
3. 等待幾分鐘讓GitHub Pages更新

### 如果AI功能無法使用
1. 檢查瀏覽器控制台是否有錯誤
2. 確認API密鑰是否正確設置
3. 使用診斷工具檢查系統狀態

### 如果文件上傳失敗
1. 檢查文件格式是否支援 (PDF, JPG, PNG)
2. 確認文件大小不超過20MB
3. 嘗試使用不同的瀏覽器

## 📱 移動端支援

所有頁面都已優化移動端體驗:
- 響應式設計
- 觸控友好界面
- 移動端拖放支援

## 🔐 隱私和安全

- **離線處理**: Tesseract.js模式完全在本地運行
- **數據加密**: 所有API通信使用HTTPS
- **無數據存儲**: 處理後的數據僅存儲在用戶瀏覽器中

## 📞 技術支援

如果遇到問題，請:
1. 查看瀏覽器控制台錯誤信息
2. 使用診斷工具檢查系統狀態
3. 提供詳細的錯誤描述和重現步驟

---

**🎉 享受VaultCaddy的全新AI文檔處理體驗！**
