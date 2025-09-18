#!/bin/bash

# VaultCaddy 快速設置工具
# 一鍵完成 OAuth 和 Analytics 配置

echo "⚡ VaultCaddy 快速設置工具"
echo "============================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}這個工具將幫助您快速完成 VaultCaddy 的最後配置步驟${NC}"
echo ""

# 步驟 1: OAuth Client ID 設置
echo -e "${PURPLE}📋 步驟 1: Google OAuth Client ID 設置${NC}"
echo "----------------------------------------"
echo -e "${YELLOW}請先完成以下操作:${NC}"
echo "1. 打開 OAuth 設置工具:"
echo "   file://$(pwd)/oauth-setup-tool.html"
echo "2. 按照指南創建 OAuth Client ID"
echo "3. 複製您的 Client ID"
echo ""

echo -e "${BLUE}您是否已經獲得了 Google OAuth Client ID？ (y/N)${NC}"
read -r has_oauth
if [[ "$has_oauth" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}請輸入您的 OAuth Client ID:${NC}"
    read -r oauth_client_id
    
    if [[ $oauth_client_id == *".apps.googleusercontent.com"* ]]; then
        echo -e "${GREEN}✅ Client ID 格式正確${NC}"
        
        # 更新 google-auth.js 文件
        if [ -f "google-auth.js" ]; then
            # 創建備份
            cp google-auth.js google-auth.js.backup
            
            # 替換 Client ID
            sed -i.tmp "s/YOUR_GOOGLE_CLIENT_ID\.apps\.googleusercontent\.com/$oauth_client_id/g" google-auth.js
            sed -i.tmp "s/YOUR_DEV_GOOGLE_CLIENT_ID\.apps\.googleusercontent\.com/$oauth_client_id/g" google-auth.js
            rm google-auth.js.tmp
            
            echo -e "${GREEN}✅ OAuth Client ID 已更新到 google-auth.js${NC}"
            OAUTH_CONFIGURED=true
        else
            echo -e "${RED}❌ 找不到 google-auth.js 文件${NC}"
            OAUTH_CONFIGURED=false
        fi
    else
        echo -e "${RED}❌ Client ID 格式不正確，應該以 .apps.googleusercontent.com 結尾${NC}"
        OAUTH_CONFIGURED=false
    fi
else
    echo -e "${YELLOW}⏸️  跳過 OAuth 設置，您可以稍後手動配置${NC}"
    OAUTH_CONFIGURED=false
fi

echo ""

# 步驟 2: Analytics ID 設置
echo -e "${PURPLE}📊 步驟 2: Analytics 工具設置${NC}"
echo "--------------------------------"

# Google Analytics 4
echo -e "${BLUE}您是否有 Google Analytics 4 Measurement ID？ (y/N)${NC}"
read -r has_ga4
if [[ "$has_ga4" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}請輸入您的 GA4 Measurement ID (格式: G-XXXXXXXXXX):${NC}"
    read -r ga4_id
    
    if [[ $ga4_id == G-* ]]; then
        # 更新 analytics-config.js
        if [ -f "analytics-config.js" ]; then
            sed -i.tmp "s/G-XXXXXXXXXX/$ga4_id/g" analytics-config.js
            rm analytics-config.js.tmp
            echo -e "${GREEN}✅ Google Analytics 4 ID 已更新${NC}"
            GA4_CONFIGURED=true
        fi
    else
        echo -e "${RED}❌ GA4 ID 格式不正確${NC}"
        GA4_CONFIGURED=false
    fi
else
    echo -e "${YELLOW}⏸️  跳過 GA4 設置${NC}"
    GA4_CONFIGURED=false
fi

# Facebook Pixel
echo -e "${BLUE}您是否有 Facebook Pixel ID？ (y/N)${NC}"
read -r has_fb_pixel
if [[ "$has_fb_pixel" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo -e "${GREEN}請輸入您的 Facebook Pixel ID:${NC}"
    read -r fb_pixel_id
    
    if [[ $fb_pixel_id =~ ^[0-9]+$ ]]; then
        # 更新 analytics-config.js
        if [ -f "analytics-config.js" ]; then
            sed -i.tmp "s/XXXXXXXXXXXXXXXXX/$fb_pixel_id/g" analytics-config.js
            rm analytics-config.js.tmp
            echo -e "${GREEN}✅ Facebook Pixel ID 已更新${NC}"
            FB_CONFIGURED=true
        fi
    else
        echo -e "${RED}❌ Facebook Pixel ID 應該是純數字${NC}"
        FB_CONFIGURED=false
    fi
else
    echo -e "${YELLOW}⏸️  跳過 Facebook Pixel 設置${NC}"
    FB_CONFIGURED=false
fi

echo ""

# 步驟 3: 配置總結
echo -e "${PURPLE}📋 配置總結${NC}"
echo "-------------------"

if [ "$OAUTH_CONFIGURED" = true ]; then
    echo -e "${GREEN}✅ Google OAuth: 已配置${NC}"
else
    echo -e "${YELLOW}⚠️  Google OAuth: 未配置${NC}"
fi

if [ "$GA4_CONFIGURED" = true ]; then
    echo -e "${GREEN}✅ Google Analytics 4: 已配置${NC}"
else
    echo -e "${YELLOW}⚠️  Google Analytics 4: 未配置${NC}"
fi

if [ "$FB_CONFIGURED" = true ]; then
    echo -e "${GREEN}✅ Facebook Pixel: 已配置${NC}"
else
    echo -e "${YELLOW}⚠️  Facebook Pixel: 未配置${NC}"
fi

echo ""

# 步驟 4: 自動部署
if [ "$OAUTH_CONFIGURED" = true ] || [ "$GA4_CONFIGURED" = true ] || [ "$FB_CONFIGURED" = true ]; then
    echo -e "${BLUE}是否立即部署這些更改到生產環境？ (y/N)${NC}"
    read -r deploy_now
    if [[ "$deploy_now" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${GREEN}🚀 開始自動部署...${NC}"
        
        # 構建提交訊息
        COMMIT_MSG="快速設置完成"
        if [ "$OAUTH_CONFIGURED" = true ]; then
            COMMIT_MSG="$COMMIT_MSG - OAuth配置"
        fi
        if [ "$GA4_CONFIGURED" = true ]; then
            COMMIT_MSG="$COMMIT_MSG - GA4配置"
        fi
        if [ "$FB_CONFIGURED" = true ]; then
            COMMIT_MSG="$COMMIT_MSG - FB Pixel配置"
        fi
        
        # 執行部署
        if [ -f "deploy.sh" ]; then
            ./deploy.sh "$COMMIT_MSG"
        else
            git add .
            git commit -m "⚡ $COMMIT_MSG

$(date '+%Y-%m-%d %H:%M:%S') 自動化設置完成
- OAuth Client ID: $([ "$OAUTH_CONFIGURED" = true ] && echo "✅" || echo "⚠️")
- Google Analytics 4: $([ "$GA4_CONFIGURED" = true ] && echo "✅" || echo "⚠️")  
- Facebook Pixel: $([ "$FB_CONFIGURED" = true ] && echo "✅" || echo "⚠️")"
            git push origin main
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}🎉 部署成功！${NC}"
            echo -e "${GREEN}您的 VaultCaddy 已經準備好投入生產使用！${NC}"
        fi
    fi
fi

# 最終指南
echo ""
echo -e "${BLUE}🎯 下一步建議:${NC}"
echo "==================="

if [ "$OAUTH_CONFIGURED" = false ]; then
    echo -e "${YELLOW}📋 完成 OAuth 設置:${NC}"
    echo "   1. 打開: file://$(pwd)/oauth-setup-tool.html"
    echo "   2. 按照指南創建 Client ID"
    echo "   3. 重新運行: ./quick-setup.sh"
    echo ""
fi

if [ "$GA4_CONFIGURED" = false ]; then
    echo -e "${YELLOW}📊 設置 Google Analytics:${NC}"
    echo "   1. 前往: https://analytics.google.com/"
    echo "   2. 創建新屬性並獲取 Measurement ID"
    echo "   3. 重新運行: ./quick-setup.sh"
    echo ""
fi

echo -e "${GREEN}🌐 測試您的網站:${NC}"
echo "   本地: file://$(pwd)/index.html"
echo "   生產: https://vaultcaddy.com"
echo ""

echo -e "${BLUE}📚 文檔資源:${NC}"
echo "   部署指南: $(pwd)/DEPLOYMENT_GUIDE.md"
echo "   完成度檢查: $(pwd)/FINAL_COMPLETION_CHECKLIST.md"
echo "   OAuth 指南: $(pwd)/GOOGLE_OAUTH_SETUP.md"

echo -e "\n${GREEN}✨ 快速設置完成！${NC}"
