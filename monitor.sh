#!/bin/bash

# VaultCaddy 實時監控工具
# 監控網站更新狀態和部署進度

echo "🔍 VaultCaddy 實時監控工具"
echo "=============================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 檢查最新提交
echo -e "\n${BLUE}📊 最新提交狀態:${NC}"
echo "------------------------------"
LATEST_COMMIT=$(git log -1 --pretty=format:"%h - %s (%cr)")
echo -e "   ${PURPLE}$LATEST_COMMIT${NC}"

# 檢查網站最後修改時間
echo -e "\n${BLUE}🌐 網站部署狀態:${NC}"
echo "------------------------------"

if command -v curl >/dev/null 2>&1; then
    echo -e "${YELLOW}正在檢查 https://vaultcaddy.com/ ...${NC}"
    
    # 獲取響應頭
    RESPONSE=$(curl -s -I https://vaultcaddy.com/)
    HTTP_STATUS=$(echo "$RESPONSE" | grep -E "^HTTP" | awk '{print $2}')
    LAST_MODIFIED=$(echo "$RESPONSE" | grep -i "last-modified" | cut -d' ' -f2-)
    CACHE_CONTROL=$(echo "$RESPONSE" | grep -i "cache-control" | cut -d' ' -f2-)
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "   ${GREEN}✅ 網站狀態: 正常運行 (HTTP $HTTP_STATUS)${NC}"
    else
        echo -e "   ${RED}❌ 網站狀態: 有問題 (HTTP $HTTP_STATUS)${NC}"
    fi
    
    if [ ! -z "$LAST_MODIFIED" ]; then
        echo -e "   ${BLUE}📅 最後修改: $LAST_MODIFIED${NC}"
        
        # 轉換時間並比較
        if command -v date >/dev/null 2>&1; then
            MODIFIED_TIMESTAMP=$(date -j -f "%a, %d %b %Y %H:%M:%S %Z" "$LAST_MODIFIED" "+%s" 2>/dev/null || echo "0")
            CURRENT_TIMESTAMP=$(date "+%s")
            TIME_DIFF=$((CURRENT_TIMESTAMP - MODIFIED_TIMESTAMP))
            
            if [ $TIME_DIFF -lt 300 ]; then
                echo -e "   ${GREEN}🚀 狀態: 最近更新 (${TIME_DIFF}秒前)${NC}"
            elif [ $TIME_DIFF -lt 3600 ]; then
                MINUTES=$((TIME_DIFF / 60))
                echo -e "   ${YELLOW}⏰ 狀態: ${MINUTES}分鐘前更新${NC}"
            else
                HOURS=$((TIME_DIFF / 3600))
                echo -e "   ${RED}⚠️  狀態: ${HOURS}小時前更新${NC}"
            fi
        fi
    fi
    
    if [ ! -z "$CACHE_CONTROL" ]; then
        echo -e "   ${BLUE}🗄️  緩存設置: $CACHE_CONTROL${NC}"
    fi
else
    echo -e "   ${RED}❌ 無法檢查網站狀態 (未安裝 curl)${NC}"
fi

# 檢查關鍵品牌元素
echo -e "\n${BLUE}🔍 品牌一致性檢查:${NC}"
echo "------------------------------"

if command -v curl >/dev/null 2>&1; then
    echo -e "${YELLOW}正在檢查品牌元素...${NC}"
    
    CONTENT=$(curl -s https://vaultcaddy.com/)
    
    # 檢查 VaultCaddy 出現次數
    VAULTCADDY_COUNT=$(echo "$CONTENT" | grep -o "VaultCaddy" | wc -l | xargs)
    
    # 檢查 SmartDoc Parser 出現次數
    SMARTDOC_COUNT=$(echo "$CONTENT" | grep -o "SmartDoc Parser" | wc -l | xargs)
    
    # 檢查價格
    PRICE_19=$(echo "$CONTENT" | grep -o "\$19" | wc -l | xargs)
    PRICE_39=$(echo "$CONTENT" | grep -o "\$39" | wc -l | xargs)
    PRICE_79=$(echo "$CONTENT" | grep -o "\$79" | wc -l | xargs)
    
    echo -e "   ${PURPLE}品牌名稱:${NC}"
    if [ "$VAULTCADDY_COUNT" -gt 0 ]; then
        echo -e "     ${GREEN}✅ VaultCaddy: $VAULTCADDY_COUNT 處${NC}"
    else
        echo -e "     ${RED}❌ VaultCaddy: 未找到${NC}"
    fi
    
    if [ "$SMARTDOC_COUNT" -gt 0 ]; then
        echo -e "     ${RED}⚠️  SmartDoc Parser: $SMARTDOC_COUNT 處 (需要修復)${NC}"
    else
        echo -e "     ${GREEN}✅ SmartDoc Parser: 已清理${NC}"
    fi
    
    echo -e "   ${PURPLE}價格方案:${NC}"
    if [ "$PRICE_19" -gt 0 ] && [ "$PRICE_39" -gt 0 ] && [ "$PRICE_79" -gt 0 ]; then
        echo -e "     ${GREEN}✅ 價格已更新: \$19, \$39, \$79${NC}"
    else
        echo -e "     ${YELLOW}⚠️  價格需要檢查: \$19($PRICE_19), \$39($PRICE_39), \$79($PRICE_79)${NC}"
    fi
else
    echo -e "   ${RED}❌ 無法檢查品牌一致性 (未安裝 curl)${NC}"
fi

# GitHub Pages 部署建議
echo -e "\n${BLUE}💡 部署優化建議:${NC}"
echo "------------------------------"

# 檢查是否有未推送的提交
if [ -n "$(git status --porcelain)" ]; then
    echo -e "   ${YELLOW}📝 有未提交的更改，建議執行:${NC}"
    echo -e "      ${BLUE}./deploy.sh \"描述您的更改\"${NC}"
elif [ -n "$(git log origin/main..main --oneline)" ]; then
    echo -e "   ${YELLOW}⬆️  有未推送的提交，建議執行:${NC}"
    echo -e "      ${BLUE}git push origin main${NC}"
else
    echo -e "   ${GREEN}✅ Git 狀態: 完全同步${NC}"
fi

# GitHub Pages 緩存清除建議
if [ "$TIME_DIFF" -gt 600 ]; then
    echo -e "   ${YELLOW}🔄 GitHub Pages 可能需要強制更新:${NC}"
    echo -e "      ${BLUE}git commit --allow-empty -m \"強制更新\" && git push${NC}"
fi

# 快速測試鏈接
echo -e "\n${BLUE}🔗 快速測試鏈接:${NC}"
echo "------------------------------"
echo -e "   ${GREEN}主頁:${NC} https://vaultcaddy.com/"
echo -e "   ${GREEN}Dashboard:${NC} https://vaultcaddy.com/dashboard.html"
echo -e "   ${GREEN}Billing:${NC} https://vaultcaddy.com/billing.html"
echo -e "   ${GREEN}GitHub:${NC} https://github.com/vaultcaddy/vaultcaddy-app"

# 監控總結
echo -e "\n${BLUE}📊 監控總結:${NC}"
echo "------------------------------"

if [ "$HTTP_STATUS" = "200" ] && [ "$VAULTCADDY_COUNT" -gt 0 ] && [ "$SMARTDOC_COUNT" -eq 0 ]; then
    echo -e "   ${GREEN}🎉 網站狀態: 優秀${NC}"
    echo -e "   ${GREEN}✅ 品牌統一: 完成${NC}"
    echo -e "   ${GREEN}✅ 部署狀態: 成功${NC}"
elif [ "$HTTP_STATUS" = "200" ] && [ "$SMARTDOC_COUNT" -gt 0 ]; then
    echo -e "   ${YELLOW}⚠️  網站狀態: 需要優化${NC}"
    echo -e "   ${YELLOW}⚠️  品牌統一: 部分完成${NC}"
    echo -e "   ${BLUE}💡 建議: 等待 2-5 分鐘讓 GitHub Pages 完成部署${NC}"
else
    echo -e "   ${RED}❌ 網站狀態: 需要檢查${NC}"
    echo -e "   ${RED}💥 建議: 檢查 GitHub Pages 設置或聯繫技術支援${NC}"
fi

# 自動刷新選項
echo -e "\n${YELLOW}是否每30秒自動刷新監控？ (y/N)${NC}"
read -r -t 10 refresh_choice

if [[ "$refresh_choice" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "\n${GREEN}🔄 自動監控已啟動 (Ctrl+C 停止)${NC}"
    while true; do
        sleep 30
        clear
        bash "$0"
    done
fi

echo -e "\n${GREEN}✨ 監控完成！${NC}"
