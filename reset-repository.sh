#!/bin/bash

# GitHub 倉庫完全重置工具
# 刪除所有內容並重新上傳

echo "🗑️  GitHub 倉庫完全重置工具"
echo "=============================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${RED}⚠️  警告：這將刪除 GitHub 倉庫中的所有文件！${NC}"
echo -e "${YELLOW}📋 即將執行的操作：${NC}"
echo "1. 創建一個新的空分支"
echo "2. 刪除所有現有文件"
echo "3. 重新添加本地所有文件"
echo "4. 強制推送到 GitHub"
echo ""

echo -e "${YELLOW}確定要繼續嗎？這個操作不可逆！ (yes/NO)${NC}"
read -r confirmation

if [[ "$confirmation" != "yes" ]]; then
    echo -e "${GREEN}操作已取消。${NC}"
    exit 0
fi

echo -e "\n${BLUE}🚀 開始重置倉庫...${NC}"

# 備份當前狀態
echo -e "\n${BLUE}💾 創建本地備份...${NC}"
BACKUP_DIR="../vaultcaddy-backup-$(date +%Y%m%d-%H%M%S)"
cp -r . "$BACKUP_DIR"
echo -e "   ${GREEN}✅ 備份已保存到: $BACKUP_DIR${NC}"

# 創建新的孤兒分支
echo -e "\n${BLUE}🌿 創建新的孤兒分支...${NC}"
git checkout --orphan new-main

# 刪除所有追蹤的文件
echo -e "\n${BLUE}🗑️  清除 Git 歷史...${NC}"
git rm -rf .

# 重新添加所有文件
echo -e "\n${BLUE}📁 重新添加本地文件...${NC}"

# 確保關鍵文件存在
if [ ! -f "CNAME" ]; then
    echo "vaultcaddy.com" > CNAME
fi

if [ ! -f ".nojekyll" ]; then
    touch .nojekyll
fi

# 添加所有文件
git add .

# 提交
echo -e "\n${BLUE}💾 創建初始提交...${NC}"
git commit -m "🚀 VaultCaddy 重新部署

重新部署時間: $(date '+%Y-%m-%d %H:%M:%S')

✨ 功能包含:
- 🏠 主頁和導航系統
- 🔐 完整認證系統 (Google OAuth + 統一管理)
- 📊 Dashboard 和管理界面
- 💳 Billing 和訂閱系統 
- 🛠️ OAuth/Firebase 設置工具
- 📈 SEO 和分析系統
- 🔧 自動化部署工具

🌐 網站: https://vaultcaddy.com
📚 文檔: README.md 和 DEPLOYMENT_GUIDE.md"

# 刪除舊分支並重命名
echo -e "\n${BLUE}🔄 重置分支結構...${NC}"
git branch -D main 2>/dev/null || echo "舊的 main 分支不存在"
git branch -m main

# 強制推送
echo -e "\n${BLUE}⬆️  強制推送到 GitHub...${NC}"
git push -f origin main

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}🎉 倉庫重置成功！${NC}"
    echo -e "${GREEN}✅ 所有文件已重新上傳到 GitHub${NC}"
    echo -e "${GREEN}🌐 GitHub Pages 將在 5-10 分鐘內重新部署${NC}"
    
    echo -e "\n${BLUE}📊 重置摘要:${NC}"
    echo "   總文件數: $(find . -type f -not -path './.git/*' | wc -l | xargs)"
    echo "   提交時間: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "   備份位置: $BACKUP_DIR"
    echo "   倉庫 URL: https://github.com/vaultcaddy/vaultcaddy-app"
    echo "   網站 URL: https://vaultcaddy.com"
    
    echo -e "\n${BLUE}🔗 檢查部署狀態:${NC}"
    echo "   ./check-deployment.sh"
    
else
    echo -e "\n${RED}❌ 推送失敗！${NC}"
    echo -e "${YELLOW}💡 嘗試恢復:${NC}"
    echo "   git checkout main"
    echo "   cp -r $BACKUP_DIR/* ."
fi

echo -e "\n${GREEN}✨ 重置完成！${NC}"
