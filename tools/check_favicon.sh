#!/bin/bash

echo "【检查 Favicon 状态】"
echo ""
echo "检查主要页面..."
echo ""

# 定义要检查的主要页面
pages=(
    "index.html"
    "en/index.html"
    "jp/index.html"
    "kr/index.html"
    "resources.html"
    "en/resources.html"
    "jp/resources.html"
    "kr/resources.html"
    "account.html"
    "en/account.html"
    "jp/account.html"
    "kr/account.html"
    "firstproject.html"
    "en/firstproject.html"
    "jp/firstproject.html"
    "kr/firstproject.html"
    "dashboard.html"
    "billing.html"
    "hsbc-bank-statement.html"
    "en/hsbc-bank-statement.html"
    "solutions/restaurant/index.html"
    "en/solutions/restaurant/index.html"
)

for page in "${pages[@]}"; do
    if [ -f "$page" ]; then
        if grep -q "favicon" "$page"; then
            echo "✅ $page"
        else
            echo "❌ $page (缺少favicon)"
        fi
    else
        echo "⚠️  $page (文件不存在)"
    fi
done

echo ""
echo "统计所有HTML文件的favicon情况..."
total=$(find . -name "*.html" -type f | wc -l | xargs)
with_favicon=$(find . -name "*.html" -type f -exec grep -l "favicon" {} \; | wc -l | xargs)
without_favicon=$((total - with_favicon))

echo "总HTML文件数：$total"
echo "有favicon：$with_favicon"
echo "缺少favicon：$without_favicon"

