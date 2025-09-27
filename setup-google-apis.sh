#!/bin/bash

# VaultCaddy Google Cloud API 設置腳本
set -e

echo "🚀 開始設置 VaultCaddy Google Cloud APIs..."

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 檢查是否已設置 Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo -e "${YELLOW}⚠️ Google Cloud SDK 未安裝，請手動完成以下步驟${NC}"
    echo ""
    echo -e "${BLUE}📋 手動設置步驟：${NC}"
    echo ""
    echo "1. 在 Google Cloud Console 中導航到："
    echo "   https://console.cloud.google.com/apis/library?project=vaultcaddy-production"
    echo ""
    echo "2. 啟用以下 APIs："
    echo "   - Generative Language API (Gemini)"
    echo "   - Document AI API"
    echo "   - Vision API"
    echo "   - OAuth 2.0 API"
    echo ""
    echo "3. 創建憑證："
    echo "   - 前往：https://console.cloud.google.com/apis/credentials?project=vaultcaddy-production"
    echo "   - 點擊「建立憑證」"
    echo "   - 選擇「API 金鑰」"
    echo "   - 複製 API 金鑰"
    echo ""
    echo "4. 創建 OAuth 2.0 憑證："
    echo "   - 點擊「建立憑證」"
    echo "   - 選擇「OAuth 用戶端 ID」"
    echo "   - 應用程式類型：「網路應用程式」"
    echo "   - 授權 JavaScript 來源：https://vaultcaddy.com"
    echo "   - 授權重新導向 URI：https://vaultcaddy.com/auth.html"
    echo ""
    exit 1
fi

# 設置項目
PROJECT_ID="vaultcaddy-production"
echo -e "${BLUE}🔧 設置 Google Cloud 項目: $PROJECT_ID${NC}"
gcloud config set project $PROJECT_ID

# 啟用必要的 APIs
echo -e "${BLUE}🔌 啟用必要的 Google APIs...${NC}"

APIs=(
    "generativelanguage.googleapis.com"     # Gemini API
    "documentai.googleapis.com"             # Document AI API
    "vision.googleapis.com"                 # Vision API
    "oauth2.googleapis.com"                # OAuth 2.0 API
    "iamcredentials.googleapis.com"        # IAM Service Account Credentials API
)

for api in "${APIs[@]}"; do
    echo -e "${YELLOW}啟用 $api...${NC}"
    gcloud services enable $api
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $api 已啟用${NC}"
    else
        echo -e "${RED}❌ 啟用 $api 失敗${NC}"
    fi
done

echo ""
echo -e "${GREEN}🎉 API 啟用完成！${NC}"
echo ""
echo -e "${BLUE}📋 下一步：創建 API 憑證${NC}"
echo ""
echo "請在 Google Cloud Console 中完成以下步驟："
echo ""
echo "1. 前往憑證頁面："
echo "   https://console.cloud.google.com/apis/credentials?project=vaultcaddy-production"
echo ""
echo "2. 創建 API 金鑰："
echo "   - 點擊「+ 建立憑證」→「API 金鑰」"
echo "   - 複製生成的 API 金鑰"
echo "   - 限制 API 金鑰使用範圍（建議）"
echo ""
echo "3. 創建 OAuth 2.0 用戶端 ID："
echo "   - 點擊「+ 建立憑證」→「OAuth 用戶端 ID」"
echo "   - 應用程式類型：網路應用程式"
echo "   - 名稱：VaultCaddy Production"
echo "   - 授權 JavaScript 來源：https://vaultcaddy.com"
echo "   - 授權重新導向 URI：https://vaultcaddy.com/auth.html"
echo ""
echo "4. 使用以下指令更新配置："
echo "   export GOOGLE_AI_API_KEY=\"your_api_key_here\""
echo "   export GOOGLE_OAUTH_CLIENT_ID=\"your_client_id_here\""
echo "   ./update-production-config.sh"
echo ""
