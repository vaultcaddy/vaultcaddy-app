#!/bin/bash

# VaultCaddy 狀態檢查工具
# 快速檢查本地和遠程的同步狀態

echo "🔍 VaultCaddy 狀態檢查工具"
echo "================================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 檢查 Git 狀態
echo -e "\n${BLUE}📊 Git 狀態檢查:${NC}"
echo "--------------------------------"

# 檢查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  有未提交的更改:${NC}"
    git status --short
    echo ""
    UNCOMMITTED=true
else
    echo -e "${GREEN}✅ 工作目錄乾淨，沒有未提交的更改${NC}"
    UNCOMMITTED=false
fi

# 檢查與遠程的同步狀態
echo -e "\n${BLUE}🔄 遠程同步狀態:${NC}"
echo "--------------------------------"

# 獲取遠程最新信息
git fetch origin main >/dev/null 2>&1

# 檢查是否有未推送的提交
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✅ 本地和遠程完全同步${NC}"
    SYNC_STATUS="synced"
elif [ -z "$(git log origin/main..main --oneline)" ]; then
    echo -e "${YELLOW}⬇️  遠程有新的提交，需要拉取${NC}"
    git log main..origin/main --oneline --graph --decorate
    SYNC_STATUS="behind"
else
    echo -e "${YELLOW}⬆️  本地有未推送的提交${NC}"
    git log origin/main..main --oneline --graph --decorate
    SYNC_STATUS="ahead"
fi

# 檢查最新提交信息
echo -e "\n${BLUE}📝 最新提交信息:${NC}"
echo "--------------------------------"
echo -e "${PURPLE}本地最新提交:${NC}"
git log -1 --pretty=format:"   %h - %an, %ar : %s" main
echo ""
echo -e "${PURPLE}遠程最新提交:${NC}"
git log -1 --pretty=format:"   %h - %an, %ar : %s" origin/main
echo ""

# 檢查網站狀態
echo -e "\n${BLUE}🌐 網站狀態檢查:${NC}"
echo "--------------------------------"

# 檢查網站是否可訪問
if command -v curl >/dev/null 2>&1; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://vaultcaddy.com)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "${GREEN}✅ https://vaultcaddy.com 正常運行 (HTTP $HTTP_STATUS)${NC}"
    else
        echo -e "${RED}❌ https://vaultcaddy.com 可能有問題 (HTTP $HTTP_STATUS)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  無法檢查網站狀態 (未安裝 curl)${NC}"
fi

# 檢查項目統計
echo -e "\n${BLUE}📈 項目統計:${NC}"
echo "--------------------------------"
echo -e "   總提交數: $(git rev-list --count main)"
echo -e "   總文件數: $(find . -type f -not -path './.git/*' | wc -l | xargs)"
echo -e "   代碼行數: $(find . -name "*.js" -o -name "*.html" -o -name "*.css" | xargs wc -l | tail -1 | awk '{print $1}')"
echo -e "   文檔文件: $(find . -name "*.md" | wc -l | xargs)"

# 檢查重要文件
echo -e "\n${BLUE}📋 重要文件檢查:${NC}"
echo "--------------------------------"

IMPORTANT_FILES=(
    "index.html"
    "dashboard.html" 
    "billing.html"
    "config.js"
    "google-auth.js"
    "seo-manager.js"
    "analytics-config.js"
    "sitemap.xml"
    "robots.txt"
    "DEPLOYMENT_GUIDE.md"
)

for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✅${NC} $file"
    else
        echo -e "   ${RED}❌${NC} $file (缺失)"
    fi
done

# 總結和建議
echo -e "\n${BLUE}💡 建議操作:${NC}"
echo "================================"

if [ "$UNCOMMITTED" = true ]; then
    echo -e "${YELLOW}📝 有未提交的更改，建議執行:${NC}"
    echo "   ./deploy.sh \"描述您的更改\""
elif [ "$SYNC_STATUS" = "ahead" ]; then
    echo -e "${YELLOW}⬆️  有未推送的提交，建議執行:${NC}"
    echo "   git push origin main"
elif [ "$SYNC_STATUS" = "behind" ]; then
    echo -e "${YELLOW}⬇️  遠程有新提交，建議執行:${NC}"
    echo "   git pull origin main"
elif [ "$SYNC_STATUS" = "synced" ]; then
    echo -e "${GREEN}🎉 一切都是最新的！${NC}"
    echo "   系統狀態良好，無需操作"
fi

echo -e "\n${BLUE}🔗 快速鏈接:${NC}"
echo "   網站: https://vaultcaddy.com"
echo "   GitHub: https://github.com/vaultcaddy/vaultcaddy-app"
echo "   OAuth 設置: file://$(pwd)/oauth-setup-tool.html"

echo -e "\n${GREEN}✨ 狀態檢查完成！${NC}"
