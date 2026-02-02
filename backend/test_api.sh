#!/bin/bash
# Test API Script
# API测试脚本

set -e

echo "🧪 Bank Statement API - 测试脚本"
echo "================================="
echo ""

API_URL="http://localhost:8000"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试1: 健康检查
echo "📋 测试1: 健康检查"
echo "   GET $API_URL/health"
echo ""

if curl -s "$API_URL/health" | jq . > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 健康检查通过${NC}"
    curl -s "$API_URL/health" | jq .
else
    echo -e "${RED}❌ 健康检查失败${NC}"
    echo "   请确认服务是否启动：python bank_statement_extractor.py"
    exit 1
fi
echo ""
echo "---"
echo ""

# 测试2: 获取支持的银行列表
echo "📋 测试2: 获取支持的银行列表"
echo "   GET $API_URL/api/banks"
echo ""

BANKS_RESPONSE=$(curl -s "$API_URL/api/banks")
BANK_COUNT=$(echo "$BANKS_RESPONSE" | jq '.total')

if [ "$BANK_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ 成功获取银行列表（共 $BANK_COUNT 个）${NC}"
    echo "$BANKS_RESPONSE" | jq '.banks[] | {key: .key, name: .name, region: .region}'
else
    echo -e "${YELLOW}⚠️  警告：未找到银行配置${NC}"
fi
echo ""
echo "---"
echo ""

# 测试3: 提取PDF（如果提供了测试文件）
if [ -n "$1" ]; then
    TEST_PDF="$1"
    
    if [ ! -f "$TEST_PDF" ]; then
        echo -e "${RED}❌ 测试文件不存在: $TEST_PDF${NC}"
        exit 1
    fi
    
    echo "📋 测试3: 提取PDF数据"
    echo "   POST $API_URL/api/extract"
    echo "   文件: $TEST_PDF"
    echo ""
    
    # 发送请求
    EXTRACT_RESPONSE=$(curl -s -X POST "$API_URL/api/extract" \
        -F "file=@$TEST_PDF" \
        -F "bank_key=zh_hangseng")
    
    # 检查是否成功
    if echo "$EXTRACT_RESPONSE" | jq -e '.bankName' > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 提取成功${NC}"
        echo ""
        
        # 提取关键信息
        BANK_NAME=$(echo "$EXTRACT_RESPONSE" | jq -r '.bankName')
        CURRENCY=$(echo "$EXTRACT_RESPONSE" | jq -r '.currency')
        PERIOD=$(echo "$EXTRACT_RESPONSE" | jq -r '.statementPeriod')
        OPENING=$(echo "$EXTRACT_RESPONSE" | jq -r '.openingBalance')
        CLOSING=$(echo "$EXTRACT_RESPONSE" | jq -r '.closingBalance')
        TXN_COUNT=$(echo "$EXTRACT_RESPONSE" | jq '.transactions | length')
        
        echo "   银行: $BANK_NAME"
        echo "   货币: $CURRENCY"
        echo "   周期: $PERIOD"
        echo "   期初余额: $OPENING"
        echo "   期末余额: $CLOSING"
        echo "   交易数量: $TXN_COUNT"
        echo ""
        
        # 显示前3笔交易
        echo "   前3笔交易:"
        echo "$EXTRACT_RESPONSE" | jq '.transactions[:3] | .[] | "   - \(.date) | \(.description) | Debit: \(.debit) | Credit: \(.credit) | Balance: \(.balance)"' -r
        
        # 检查日期填充
        FILLED_COUNT=$(echo "$EXTRACT_RESPONSE" | jq '[.transactions[] | select(._date_filled == true)] | length')
        if [ "$FILLED_COUNT" -gt 0 ]; then
            echo ""
            echo -e "${GREEN}   ✅ 自动填充了 $FILLED_COUNT 个空白日期${NC}"
        fi
        
    else
        echo -e "${RED}❌ 提取失败${NC}"
        echo "$EXTRACT_RESPONSE" | jq .
        exit 1
    fi
else
    echo "📋 测试3: 提取PDF数据"
    echo -e "${YELLOW}⏭️  跳过（未提供测试文件）${NC}"
    echo ""
    echo "   用法: $0 /path/to/statement.pdf"
fi

echo ""
echo "================================="
echo -e "${GREEN}🎉 所有测试完成！${NC}"
echo ""

