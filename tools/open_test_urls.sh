#!/bin/bash

# 读取URL列表并在Chrome中打开
urls=(
"https://vaultcaddy.com/zh-TW/ctbc-bank-statement-v3.html"
"https://vaultcaddy.com/ja-JP/scotiabank-statement-v3.html"
"https://vaultcaddy.com/zh-TW/dbs-bank-statement-v3.html"
"https://vaultcaddy.com/zh-HK/westpac-new-zealand-statement-v3.html"
"https://vaultcaddy.com/ko-KR/pnc-bank-statement-v3.html"
"https://vaultcaddy.com/nab-statement-v3.html"
"https://vaultcaddy.com/ko-KR/multi-company-management-v3.html"
"https://vaultcaddy.com/bank-statement-data-security-v3.html"
"https://vaultcaddy.com/real-estate-accounting-v3.html"
"https://vaultcaddy.com/zh-TW/batch-processing-solution-v3.html"
"https://vaultcaddy.com/zh-HK/us-bank-statement-v3.html"
"https://vaultcaddy.com/ja-JP/nonprofit-organization-accounting-v3.html"
"https://vaultcaddy.com/ja-JP/mobile-app-bank-statement-v3.html"
"https://vaultcaddy.com/zh-HK/restaurant-accounting-v3.html"
)

# 在macOS上使用open命令打开Chrome
for url in "${urls[@]}"; do
    open -a "Google Chrome" "$url"
    sleep 2
done

echo "✅ 所有14个测试页面已在Chrome中打开"
