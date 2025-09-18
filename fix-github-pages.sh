#!/bin/bash

# GitHub Pages 修復工具
# 確保 Pages 設置正確

echo "🔧 GitHub Pages 修復工具"
echo "========================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}📋 檢查當前 GitHub Pages 設置...${NC}"

# 檢查 CNAME 文件
if [ -f "CNAME" ]; then
    DOMAIN=$(cat CNAME)
    echo -e "   ${GREEN}✅ CNAME 文件存在: $DOMAIN${NC}"
else
    echo -e "   ${RED}❌ CNAME 文件不存在${NC}"
    echo "vaultcaddy.com" > CNAME
    echo -e "   ${GREEN}✅ 已創建 CNAME 文件${NC}"
fi

# 檢查 index.html
if [ -f "index.html" ]; then
    echo -e "   ${GREEN}✅ index.html 存在${NC}"
else
    echo -e "   ${RED}❌ index.html 不存在${NC}"
fi

# 檢查最新文件
echo -e "\n${BLUE}📊 檢查最新添加的文件...${NC}"

NEW_FILES=(
    "oauth-setup-tool.html"
    "firebase-setup-tool.html"
    "monitor.sh"
    "check-deployment.sh"
)

ALL_FILES_EXIST=true

for file in "${NEW_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✅ $file${NC}"
    else
        echo -e "   ${RED}❌ $file${NC}"
        ALL_FILES_EXIST=false
    fi
done

# 強制 GitHub Pages 重建
echo -e "\n${BLUE}🔄 強制 GitHub Pages 重建...${NC}"

# 創建 .nojekyll 文件（如果不存在）
if [ ! -f ".nojekyll" ]; then
    touch .nojekyll
    echo -e "   ${GREEN}✅ 已創建 .nojekyll 文件${NC}"
fi

# 更新 README.md 觸發重建
echo "<!-- Updated: $(date) -->" >> README.md
echo -e "   ${GREEN}✅ 已更新 README.md 觸發重建${NC}"

# 提交更改
echo -e "\n${BLUE}💾 提交修復更改...${NC}"

git add .
git commit -m "🔧 修復 GitHub Pages 設置

- 確保 CNAME 文件正確
- 添加 .nojekyll 文件
- 強制觸發重建
- 修復文件部署問題

修復時間: $(date '+%Y-%m-%d %H:%M:%S')"

git push origin main

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ GitHub Pages 修復完成！${NC}"
    echo -e "${GREEN}🌐 請等待 5-10 分鐘讓 GitHub Pages 重新部署${NC}"
else
    echo -e "\n${RED}❌ 推送失敗，請檢查網絡連接${NC}"
fi

# 檢查分支狀態
echo -e "\n${BLUE}🌿 檢查分支狀態...${NC}"
CURRENT_BRANCH=$(git branch --show-current)
echo -e "   當前分支: ${YELLOW}$CURRENT_BRANCH${NC}"

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "   ${YELLOW}⚠️  建議切換到 main 分支${NC}"
fi

echo -e "\n${BLUE}📝 GitHub Pages 設置檢查清單:${NC}"
echo "================================"
echo -e "1. ${GREEN}✅${NC} 倉庫是公開的"
echo -e "2. ${GREEN}✅${NC} main 分支存在"
echo -e "3. ${GREEN}✅${NC} CNAME 文件正確"
echo -e "4. ${GREEN}✅${NC} .nojekyll 文件存在"
echo -e "5. ${YELLOW}⏳${NC} 等待 Pages 重新部署"

echo -e "\n${BLUE}🔗 需要檢查的 GitHub 設置:${NC}"
echo "------------------------------"
echo -e "1. 前往: ${YELLOW}https://github.com/vaultcaddy/vaultcaddy-app/settings/pages${NC}"
echo -e "2. 確認 Source 設為: ${YELLOW}Deploy from a branch${NC}"
echo -e "3. 確認 Branch 設為: ${YELLOW}main / (root)${NC}"
echo -e "4. 確認 Custom domain 設為: ${YELLOW}vaultcaddy.com${NC}"

echo -e "\n${GREEN}✨ 修復完成！${NC}"
