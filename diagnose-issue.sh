#!/bin/bash

# 診斷 VaultCaddy 問題
# 使用方法：./diagnose-issue.sh

echo "🔍 VaultCaddy 系統診斷"
echo "=================================="
echo ""

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Worker URL
WORKER_URL="https://deepseek-proxy.vaultcaddy.workers.dev"

# 測試 1：檢查 Worker 是否運行
echo -e "${BLUE}📋 測試 1：檢查 Cloudflare Worker${NC}"
echo "URL: $WORKER_URL"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" "$WORKER_URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "405" ]; then
    echo -e "${GREEN}✅ Worker 正常運行${NC}"
    echo "響應: $BODY"
else
    echo -e "${RED}❌ Worker 異常 (HTTP $HTTP_CODE)${NC}"
    echo "響應: $BODY"
    echo ""
    echo -e "${YELLOW}🔧 修復方法：${NC}"
    echo "1. 訪問 https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/deepseek-proxy/production"
    echo "2. 按照 URGENT_DEPLOYMENT_FIX.md 中的步驟更新 Worker 代碼"
    echo "3. 點擊 'Save and Deploy'"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 測試 2：檢查 Worker 是否支持 POST 請求
echo -e "${BLUE}📋 測試 2：測試 POST 請求${NC}"
echo ""

TEST_REQUEST='{
  "model": "deepseek-reasoner",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}'

echo "發送測試請求..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$WORKER_URL" \
  -H "Content-Type: application/json" \
  -d "$TEST_REQUEST")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Worker POST 請求正常${NC}"
    echo ""
    echo "響應內容："
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    
    # 檢查是否有 usage 信息
    if echo "$BODY" | grep -q "usage"; then
        echo ""
        echo -e "${GREEN}✅ Token 用量追蹤正常${NC}"
    else
        echo ""
        echo -e "${YELLOW}⚠️  未找到 Token 用量信息${NC}"
    fi
else
    echo -e "${RED}❌ Worker POST 請求失敗 (HTTP $HTTP_CODE)${NC}"
    echo "響應: $BODY"
    echo ""
    echo -e "${YELLOW}🔧 可能的原因：${NC}"
    echo "1. DeepSeek API Key 無效"
    echo "2. DeepSeek API 服務異常"
    echo "3. Worker 代碼有誤"
    echo ""
    echo -e "${YELLOW}🔧 修復方法：${NC}"
    echo "1. 檢查 Worker 中的 API Key: sk-4a43b49a13a840009052be65f599b7a4"
    echo "2. 訪問 https://platform.deepseek.com/ 確認 API Key 有效"
    echo "3. 查看 Worker 日誌了解詳細錯誤"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 測試 3：檢查網站是否可訪問
echo -e "${BLUE}📋 測試 3：檢查 VaultCaddy 網站${NC}"
echo ""

SITE_URL="https://vaultcaddy.com/firstproject.html"
echo "URL: $SITE_URL"

RESPONSE=$(curl -s -w "\n%{http_code}" "$SITE_URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 網站可訪問${NC}"
else
    echo -e "${RED}❌ 網站無法訪問 (HTTP $HTTP_CODE)${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 總結
echo -e "${GREEN}🎉 所有測試通過！${NC}"
echo ""
echo -e "${BLUE}下一步：${NC}"
echo "1. 清除瀏覽器緩存（Ctrl+Shift+R 或 Cmd+Shift+R）"
echo "2. 訪問 https://vaultcaddy.com/firstproject.html"
echo "3. 打開瀏覽器控制台（F12）"
echo "4. 檢查初始化日誌："
echo ""
echo "   預期日誌："
echo "   🔄 立即初始化混合處理器..."
echo "   ✅ 混合處理器已初始化"
echo "      ✅ Vision API OCR + DeepSeek 文本處理"
echo ""
echo "   🧠 智能處理器初始化"
echo "      🔄 使用: Vision API OCR + DeepSeek Reasoner (思考模式)"
echo "      ❌ 已禁用: OpenAI, Gemini, 其他 AI"
echo ""
echo "5. 上傳測試發票"
echo "6. 查看處理日誌"
echo ""
echo -e "${YELLOW}如果仍然有問題，請提供：${NC}"
echo "1. 瀏覽器控制台的完整日誌（特別是紅色錯誤）"
echo "2. 上傳文件時的錯誤信息"
echo "3. 網絡請求的詳細信息（Network 標籤）"
echo ""

