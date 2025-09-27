#!/bin/bash

# VaultCaddy 簡化部署腳本
set -e

echo "🚀 開始部署 VaultCaddy..."

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# 檢查 Git 狀態
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 錯誤：不在 Git 倉庫中${NC}"
    exit 1
fi

# 檢查關鍵文件
required_files=("index.html" "auth.html" "dashboard.html")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ 缺少文件：$file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ 文件檢查通過${NC}"

# 添加文件到 Git
echo -e "${BLUE}📁 添加文件到 Git...${NC}"
git add .github/ config.production.js index.html dashboard.html auth.html result.html navbar-component.js

# 檢查是否有變更需要提交
if git diff --quiet --cached; then
    echo -e "${BLUE}ℹ️ 沒有新的變更需要提交${NC}"
else
    # 提交變更
    commit_message="🚀 部署更新 - $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$commit_message"
    echo -e "${GREEN}✅ 已提交變更${NC}"
fi

# 推送到 GitHub
echo -e "${BLUE}⬆️ 推送到 GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✅ 成功推送到 GitHub${NC}"
    echo ""
    echo -e "${GREEN}🎉 部署完成！${NC}"
    echo "網站將在幾分鐘內更新：https://vaultcaddy.com"
    echo "查看部署狀態：https://github.com/vaultcaddy/vaultcaddy-app/actions"
else
    echo -e "${RED}❌ 推送失敗${NC}"
    exit 1
fi
