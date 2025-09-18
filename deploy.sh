#!/bin/bash

# VaultCaddy 自動化部署腳本
# 使用方法: ./deploy.sh "提交訊息"

echo "🚀 VaultCaddy 自動化部署開始..."

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查是否提供提交訊息
if [ -z "$1" ]; then
    echo -e "${YELLOW}請提供提交訊息，例如: ./deploy.sh \"修復登入問題\"${NC}"
    exit 1
fi

COMMIT_MESSAGE="$1"

echo -e "${BLUE}📋 檢查 Git 狀態...${NC}"
git status

echo -e "\n${BLUE}📝 添加所有更改到暫存區...${NC}"
git add .

echo -e "\n${BLUE}📊 顯示即將提交的更改...${NC}"
git diff --cached --stat

echo -e "\n${YELLOW}⚠️  即將提交以上更改，是否繼續？ (y/N)${NC}"
read -r response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${RED}❌ 部署已取消${NC}"
    exit 1
fi

echo -e "\n${BLUE}💾 提交更改...${NC}"
git commit -m "🚀 $COMMIT_MESSAGE

更新時間: $(date '+%Y-%m-%d %H:%M:%S')
部署環境: 生產環境 (vaultcaddy.com)
自動化部署: deploy.sh"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 提交失敗，請檢查更改${NC}"
    exit 1
fi

echo -e "\n${BLUE}⬆️  推送到 GitHub...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ 部署成功！${NC}"
    echo -e "${GREEN}🌐 您的更改將在 1-2 分鐘內在 https://vaultcaddy.com 上生效${NC}"
    
    # 顯示部署摘要
    echo -e "\n${BLUE}📊 部署摘要:${NC}"
    echo -e "   提交訊息: $COMMIT_MESSAGE"
    echo -e "   提交時間: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "   最新提交: $(git rev-parse --short HEAD)"
    echo -e "   線上網站: https://vaultcaddy.com"
    echo -e "   GitHub 倉庫: https://github.com/vaultcaddy/vaultcaddy-app"
    
    # 可選：自動打開網站
    echo -e "\n${YELLOW}是否打開 vaultcaddy.com 檢查部署結果？ (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        if command -v open >/dev/null 2>&1; then
            open https://vaultcaddy.com
        elif command -v xdg-open >/dev/null 2>&1; then
            xdg-open https://vaultcaddy.com
        else
            echo -e "${BLUE}請手動打開: https://vaultcaddy.com${NC}"
        fi
    fi
    
else
    echo -e "${RED}❌ 推送失敗，請檢查網絡連接和 Git 配置${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 部署完成！${NC}"
