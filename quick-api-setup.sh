#!/bin/bash

# VaultCaddy 快速 API 設置腳本
set -e

echo "🚀 VaultCaddy 快速 API 設置"
echo "=========================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 檢查是否在正確的目錄
if [ ! -f "config.production.js" ]; then
    echo -e "${RED}❌ 錯誤：請在 VaultCaddy 專案根目錄中執行此腳本${NC}"
    exit 1
fi

echo -e "${BLUE}請在 Google Cloud Console 中完成以下步驟：${NC}"
echo
echo "1. 啟用 Generative Language API："
echo "   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com?project=vaultcaddy-production"
echo
echo "2. 創建 API 金鑰："
echo "   https://console.cloud.google.com/apis/credentials?project=vaultcaddy-production"
echo
echo "3. 設置 OAuth 2.0："
echo "   https://console.cloud.google.com/apis/credentials/consent?project=vaultcaddy-production"
echo

# 等待用戶確認
read -p "完成上述步驟後，按 Enter 繼續..."

echo
echo -e "${YELLOW}請輸入您獲得的 API 資訊：${NC}"

# 收集 API 資訊
echo -n "Google AI API Key (AIzaSy...): "
read -s GOOGLE_AI_API_KEY
echo

echo -n "Google OAuth Client ID: "
read GOOGLE_OAUTH_CLIENT_ID

echo -n "Stripe Publishable Key (可選，直接按 Enter 跳過): "
read STRIPE_KEY

# 驗證輸入
if [ -z "$GOOGLE_AI_API_KEY" ]; then
    echo -e "${RED}❌ 錯誤：Google AI API Key 不能為空${NC}"
    exit 1
fi

if [ -z "$GOOGLE_OAUTH_CLIENT_ID" ]; then
    echo -e "${RED}❌ 錯誤：Google OAuth Client ID 不能為空${NC}"
    exit 1
fi

# 備份當前配置
cp config.production.js config.production.js.backup
echo -e "${GREEN}✅ 已創建配置備份${NC}"

# 更新配置文件
echo -e "${YELLOW}正在更新 config.production.js...${NC}"

# 使用 sed 替換 API 金鑰
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/PLACEHOLDER_FOR_PRODUCTION/${GOOGLE_AI_API_KEY}/g" config.production.js
    sed -i '' "s/your-dev-client-id/${GOOGLE_OAUTH_CLIENT_ID}/g" config.production.js
    if [ -n "$STRIPE_KEY" ]; then
        sed -i '' "s/pk_test_your_dev_key/${STRIPE_KEY}/g" config.production.js
    fi
else
    # Linux
    sed -i "s/PLACEHOLDER_FOR_PRODUCTION/${GOOGLE_AI_API_KEY}/g" config.production.js
    sed -i "s/your-dev-client-id/${GOOGLE_OAUTH_CLIENT_ID}/g" config.production.js
    if [ -n "$STRIPE_KEY" ]; then
        sed -i "s/pk_test_your_dev_key/${STRIPE_KEY}/g" config.production.js
    fi
fi

echo -e "${GREEN}✅ 配置文件已更新${NC}"

# 創建 API 測試腳本
echo -e "${YELLOW}正在創建 API 測試腳本...${NC}"

cat > test-api-connection.sh << 'EOF'
#!/bin/bash

# 測試 Google AI API 連接
echo "🧪 測試 Google AI API 連接..."

# 從配置文件中提取 API Key（簡單方法）
API_KEY=$(grep -o 'AIzaSy[A-Za-z0-9_-]*' config.production.js | head -1)

if [ -z "$API_KEY" ]; then
    echo "❌ 無法找到 API Key"
    exit 1
fi

echo "使用 API Key: ${API_KEY:0:10}..."

# 測試 API 調用
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "請用繁體中文回答：VaultCaddy API 測試成功！今天是什麼日子？"
      }]
    }]
  }' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${API_KEY}" | \
  python3 -m json.tool 2>/dev/null || echo "API 調用失敗，請檢查 API Key 是否正確"
EOF

chmod +x test-api-connection.sh

echo -e "${GREEN}✅ API 測試腳本已創建${NC}"

# 測試 API 連接
echo
echo -e "${BLUE}正在測試 API 連接...${NC}"
./test-api-connection.sh

echo
echo -e "${GREEN}🎉 設置完成！${NC}"
echo
echo "下一步："
echo "1. 執行部署："
echo "   ${BLUE}./simple-deploy.sh${NC}"
echo
echo "2. 測試網站功能："
echo "   ${BLUE}https://vaultcaddy.com${NC}"
echo
echo "3. 如果需要回滾配置："
echo "   ${BLUE}cp config.production.js.backup config.production.js${NC}"

echo
echo -e "${YELLOW}配置摘要：${NC}"
echo "• Google AI API Key: ${GOOGLE_AI_API_KEY:0:10}..."
echo "• Google OAuth Client ID: ${GOOGLE_OAUTH_CLIENT_ID:0:20}..."
if [ -n "$STRIPE_KEY" ]; then
    echo "• Stripe Key: ${STRIPE_KEY:0:10}..."
fi
