#!/bin/bash

echo "🚀 VaultCaddy GitHub Pages 部署腳本"
echo "=================================="

# 檢查是否已設定remote
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ GitHub remote 已設定"
else
    echo "❌ 需要設定 GitHub remote"
    echo ""
    echo "請按照以下步驟操作："
    echo "1. 前往 https://github.com/new"
    echo "2. Repository name: vaultcaddy-app"
    echo "3. 設為 Public"
    echo "4. 不要選擇任何初始化選項"
    echo "5. 建立倉庫後，執行："
    echo "   git remote add origin https://github.com/你的用戶名/vaultcaddy-app.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    exit 1
fi

echo "📦 準備部署檔案..."

# 建立 gh-pages 分支
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "✅ gh-pages 分支已存在"
    git checkout gh-pages
else
    echo "🔄 建立 gh-pages 分支..."
    git checkout -b gh-pages
fi

# 確保在正確的分支
echo "📋 當前分支: $(git branch --show-current)"

# 推送到 GitHub
echo "⬆️ 推送到 GitHub Pages..."
git push origin gh-pages

echo ""
echo "✅ 部署完成！"
echo ""
echo "📝 下一步："
echo "1. 前往 GitHub Repository → Settings → Pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: gh-pages"
echo "4. 等待幾分鐘後，網站將在以下網址可用："
echo "   https://你的用戶名.github.io/vaultcaddy-app"
echo ""
echo "🌐 設定自定義域名："
echo "1. 在 GitHub Pages 設定中添加: vaultcaddy.com"
echo "2. 設定 Cloudflare DNS"
echo ""

# 回到 main 分支
git checkout main

echo "🎉 GitHub Pages 部署腳本執行完成！"

