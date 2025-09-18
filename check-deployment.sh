#!/bin/bash

# VaultCaddy 部署狀態實時監控
# 檢查文件是否已部署到 vaultcaddy.com

echo "🔍 VaultCaddy 部署狀態檢查"
echo "=========================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 要檢查的文件列表
FILES_TO_CHECK=(
    "oauth-setup-tool.html"
    "firebase-setup-tool.html"
    "monitor.sh"
)

echo -e "\n${BLUE}📊 檢查最新提交狀態:${NC}"
echo "------------------------------"
LATEST_COMMIT=$(git log -1 --pretty=format:"%h - %s (%cr)")
echo -e "   ${YELLOW}$LATEST_COMMIT${NC}"

echo -e "\n${BLUE}🌐 檢查文件部署狀態:${NC}"
echo "------------------------------"

ALL_DEPLOYED=true

for file in "${FILES_TO_CHECK[@]}"; do
    echo -e "${YELLOW}檢查: $file${NC}"
    
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://vaultcaddy.com/$file")
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "   ${GREEN}✅ 已部署 (HTTP $HTTP_STATUS)${NC}"
    elif [ "$HTTP_STATUS" = "404" ]; then
        echo -e "   ${RED}❌ 未部署 (HTTP $HTTP_STATUS)${NC}"
        ALL_DEPLOYED=false
    else
        echo -e "   ${YELLOW}⚠️  狀態不明 (HTTP $HTTP_STATUS)${NC}"
        ALL_DEPLOYED=false
    fi
done

echo -e "\n${BLUE}📈 總體狀態:${NC}"
echo "------------------------------"

if [ "$ALL_DEPLOYED" = true ]; then
    echo -e "   ${GREEN}🎉 所有文件已成功部署！${NC}"
    echo -e "   ${GREEN}✅ OAuth 設置工具: https://vaultcaddy.com/oauth-setup-tool.html${NC}"
    echo -e "   ${GREEN}✅ Firebase 設置工具: https://vaultcaddy.com/firebase-setup-tool.html${NC}"
else
    echo -e "   ${YELLOW}⏳ 部署進行中...${NC}"
    echo -e "   ${BLUE}💡 GitHub Pages 通常需要 2-10 分鐘部署${NC}"
    echo -e "   ${BLUE}🔄 建議再等待 5 分鐘後重新檢查${NC}"
fi

# 提供本地文件訪問
echo -e "\n${BLUE}🏠 本地文件訪問:${NC}"
echo "------------------------------"
echo -e "   ${GREEN}OAuth 設置: file://$(pwd)/oauth-setup-tool.html${NC}"
echo -e "   ${GREEN}Firebase 設置: file://$(pwd)/firebase-setup-tool.html${NC}"

# 自動重試選項
echo -e "\n${YELLOW}是否每 30 秒自動檢查部署狀態？ (y/N)${NC}"
read -r -t 10 auto_check

if [[ "$auto_check" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "\n${GREEN}🔄 自動檢查已啟動 (Ctrl+C 停止)${NC}"
    
    while [ "$ALL_DEPLOYED" = false ]; do
        sleep 30
        echo -e "\n${BLUE}$(date '+%H:%M:%S') - 重新檢查...${NC}"
        
        ALL_DEPLOYED=true
        for file in "${FILES_TO_CHECK[@]}"; do
            HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://vaultcaddy.com/$file")
            if [ "$HTTP_STATUS" != "200" ]; then
                ALL_DEPLOYED=false
                echo -e "   ${YELLOW}$file: 仍在部署中...${NC}"
                break
            fi
        done
        
        if [ "$ALL_DEPLOYED" = true ]; then
            echo -e "\n${GREEN}🎉 部署完成！所有文件現在可以訪問了！${NC}"
            echo -e "   ${GREEN}✅ https://vaultcaddy.com/oauth-setup-tool.html${NC}"
            echo -e "   ${GREEN}✅ https://vaultcaddy.com/firebase-setup-tool.html${NC}"
            break
        fi
    done
fi

echo -e "\n${GREEN}✨ 檢查完成！${NC}"
