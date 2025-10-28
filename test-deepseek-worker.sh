#!/bin/bash

# 測試 DeepSeek Cloudflare Worker
# 使用方法：./test-deepseek-worker.sh

echo "🧪 測試 DeepSeek Cloudflare Worker"
echo "=================================="
echo ""

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Worker URL
WORKER_URL="https://deepseek-proxy.vaultcaddy.workers.dev"

# 測試 1：檢查 Worker 是否運行
echo "📋 測試 1：檢查 Worker 是否運行"
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
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 測試 2：測試 deepseek-reasoner 模型
echo "📋 測試 2：測試 deepseek-reasoner 模型"
echo ""

TEST_REQUEST='{
  "model": "deepseek-reasoner",
  "messages": [
    {
      "role": "user",
      "content": "計算 123 + 456，並用 JSON 格式返回結果：{\"result\": 數字}"
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
    echo -e "${GREEN}✅ deepseek-reasoner 模型正常工作${NC}"
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
    echo -e "${RED}❌ deepseek-reasoner 模型測試失敗 (HTTP $HTTP_CODE)${NC}"
    echo "響應: $BODY"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 測試 3：測試 deepseek-chat 模型
echo "📋 測試 3：測試 deepseek-chat 模型"
echo ""

TEST_REQUEST_CHAT='{
  "model": "deepseek-chat",
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
  -d "$TEST_REQUEST_CHAT")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ deepseek-chat 模型正常工作${NC}"
    echo ""
    echo "響應內容："
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}❌ deepseek-chat 模型測試失敗 (HTTP $HTTP_CODE)${NC}"
    echo "響應: $BODY"
    exit 1
fi

echo ""
echo "=================================="
echo ""
echo -e "${GREEN}🎉 所有測試通過！${NC}"
echo ""
echo "下一步："
echo "1. 清除瀏覽器緩存（Ctrl+Shift+R）"
echo "2. 訪問 https://vaultcaddy.com/firstproject.html"
echo "3. 上傳測試發票"
echo "4. 查看控制台日誌"
echo ""

