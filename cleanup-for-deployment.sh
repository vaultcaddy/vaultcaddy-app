#!/bin/bash

# VaultCaddy 部署前清理腳本
# 移除多餘的文檔和文件，保留核心功能

echo "🧹 開始清理VaultCaddy項目..."

# 創建docs目錄存放文檔
mkdir -p docs

# 移動重要文檔到docs目錄
echo "📁 移動文檔到docs目錄..."
mv OPENSOURCE_INTEGRATION_PLAN.md docs/ 2>/dev/null
mv GITHUB_PAGES_DEPLOYMENT.md docs/ 2>/dev/null
mv PUSH_TO_GITHUB.md docs/ 2>/dev/null
mv README.md docs/ 2>/dev/null

# 刪除舊的報告文檔
echo "🗑️ 刪除舊的報告文檔..."
rm -f VAULTCADDY_*.md
rm -f ARCHITECTURE_*.md
rm -f COMPLETE_*.md
rm -f DEBUG_*.md
rm -f FINAL_*.md
rm -f RECEIPT_*.md
rm -f AI_COMPETITIVE_ADVANTAGES.md
rm -f API_SETUP_COMPLETION_REPORT.md
rm -f DEPLOYMENT_GUIDE.md
rm -f FINAL_COMPLETION_CHECKLIST.md
rm -f GOOGLE_AI_API_SETUP.md
rm -f GOOGLE_OAUTH_SETUP.md
rm -f LEDGERBOX_INTEGRATION_GUIDE.md
rm -f PAYMENT_AND_STORAGE_SOLUTION.md
rm -f get-google-api-key.md

# 刪除備份文件
echo "🗑️ 刪除備份文件..."
rm -f index_backup.html
rm -f *_backup.*

# 刪除測試文件
echo "🗑️ 刪除測試文件..."
rm -f test-*.html
rm -f DIAGNOSTIC_TOOL.html
rm -f EMERGENCY_FIX.js

# 刪除不必要的配置文件
echo "🗑️ 刪除多餘配置..."
rm -f .htaccess
rm -f _config.yml

# 保留的核心文件列表
echo "✅ 保留的核心文件:"
echo "   - index.html (簡潔首頁)"
echo "   - dashboard.html (主功能頁面)"
echo "   - enhanced-demo.html (演示頁面)"
echo "   - 所有 .js 處理器文件"
echo "   - 所有 .css 樣式文件"
echo "   - 所有 .html 功能頁面"

# 顯示當前目錄結構
echo ""
echo "📋 清理後的項目結構:"
ls -la | grep -E "\.(html|js|css)$" | head -20

echo ""
echo "✅ 清理完成！項目現在更加簡潔，專注於核心AI功能。"
echo "🚀 可以執行 ./deploy-to-github.sh 進行部署"
