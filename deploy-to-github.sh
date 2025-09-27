#!/bin/bash

# VaultCaddy GitHub 自動部署腳本
# 用途：快速部署到 GitHub Pages

set -e  # 遇到錯誤立即退出

echo "🚀 VaultCaddy 部署腳本啟動..."

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查是否在 Git 倉庫中
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 錯誤：不在 Git 倉庫中${NC}"
    echo "請在 VaultCaddy 項目根目錄執行此腳本"
    exit 1
fi

# 檢查是否有 GitHub remote
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ 未找到 GitHub remote，正在設置...${NC}"
    read -p "請輸入 GitHub 倉庫 URL: " repo_url
    git remote add origin "$repo_url"
fi

echo -e "${BLUE}📋 檢查項目狀態...${NC}"

# 檢查關鍵文件
required_files=("index.html" "auth.html" "dashboard.html" "config.js")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo -e "${RED}❌ 缺少關鍵文件：${missing_files[*]}${NC}"
    exit 1
fi

# 檢查配置
echo -e "${BLUE}🔧 檢查配置文件...${NC}"

if [ ! -f "config.production.js" ]; then
    echo -e "${YELLOW}⚠️ 未找到生產配置，將創建基本配置${NC}"
    cp config.js config.production.js 2>/dev/null || true
fi

# 替換配置中的佔位符（如果設置了環境變數）
if [ -n "$GOOGLE_AI_API_KEY" ]; then
    echo -e "${GREEN}✅ 找到 Google AI API Key，更新配置...${NC}"
    sed -i.bak "s/{{GOOGLE_AI_API_KEY}}/$GOOGLE_AI_API_KEY/g" config.production.js
fi

if [ -n "$GOOGLE_OAUTH_CLIENT_ID" ]; then
    echo -e "${GREEN}✅ 找到 Google OAuth Client ID，更新配置...${NC}"
    sed -i.bak "s/{{GOOGLE_OAUTH_CLIENT_ID}}/$GOOGLE_OAUTH_CLIENT_ID/g" config.production.js
fi

if [ -n "$STRIPE_PUBLIC_KEY" ]; then
    echo -e "${GREEN}✅ 找到 Stripe Public Key，更新配置...${NC}"
    sed -i.bak "s/{{STRIPE_PUBLIC_KEY}}/$STRIPE_PUBLIC_KEY/g" config.production.js
fi

# 清理備份文件
rm -f config.production.js.bak

# 更新版本號
if [ -f "package.json" ]; then
    echo -e "${BLUE}📦 更新版本...${NC}"
    # 增加 patch 版本號
    npm version patch --no-git-tag-version 2>/dev/null || true
fi

# 生成部署資訊（僅顯示在終端）
echo "# 🚀 VaultCaddy 部署資訊"
echo "**部署時間**: $(date)"
echo "**Git SHA**: $(git rev-parse --short HEAD)"
echo "**分支**: $(git branch --show-current)"
echo ""
echo "## 🔧 配置狀態"
echo "- Google AI API: $([ -n "$GOOGLE_AI_API_KEY" ] && echo "✅ 已設置" || echo "❌ 未設置")"
echo "- Google OAuth: $([ -n "$GOOGLE_OAUTH_CLIENT_ID" ] && echo "✅ 已設置" || echo "❌ 未設置")"
echo "- Stripe: $([ -n "$STRIPE_PUBLIC_KEY" ] && echo "✅ 已設置" || echo "❌ 未設置")"

echo -e "${BLUE}📝 準備提交變更...${NC}"

# 檢查是否有變更
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${YELLOW}ℹ️ 沒有新的變更需要提交${NC}"
else
    # 添加文件
    git add .
    
    # 提交變更
    commit_message="🚀 自動部署 - $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$commit_message"
    echo -e "${GREEN}✅ 已提交變更${NC}"
fi

# 推送到 GitHub
echo -e "${BLUE}⬆️ 推送到 GitHub...${NC}"

# 確保在 main 分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo -e "${YELLOW}⚠️ 目前不在 main 分支，切換中...${NC}"
    git checkout main 2>/dev/null || git checkout -b main
fi

# 推送
if git push origin main; then
    echo -e "${GREEN}✅ 成功推送到 GitHub${NC}"
else
    echo -e "${RED}❌ 推送失敗${NC}"
    exit 1
fi

# 等待 GitHub Actions 部署
echo -e "${BLUE}⏳ 等待 GitHub Pages 部署...${NC}"
echo "您可以在以下連結查看部署狀態："
echo "$(git remote get-url origin | sed 's/\.git$//')/actions"

# 顯示完成資訊
echo ""
echo -e "${GREEN}🎉 部署完成！${NC}"
echo ""
echo -e "${BLUE}📊 部署摘要：${NC}"
echo "• 網站地址: https://vaultcaddy.com"
echo "• 部署時間: $(date)"
echo "• Git SHA: $(git rev-parse --short HEAD)"
echo ""

# 如果有瀏覽器，詢問是否開啟
if command -v open >/dev/null 2>&1 || command -v xdg-open >/dev/null 2>&1; then
    read -p "是否要開啟網站查看結果？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v open >/dev/null 2>&1; then
            open "https://vaultcaddy.com"
        elif command -v xdg-open >/dev/null 2>&1; then
            xdg-open "https://vaultcaddy.com"
        fi
    fi
fi

echo -e "${GREEN}✨ 部署腳本執行完畢${NC}"
