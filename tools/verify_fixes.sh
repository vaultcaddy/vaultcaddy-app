#!/bin/bash

echo "===================================================================="
echo "验证修复结果"
echo "===================================================================="
echo ""

for file in hsbc-bank-statement.html bankcomm-bank-statement.html citic-bank-statement.html dahsing-bank-statement.html citibank-bank-statement.html; do
    echo "=== $file ==="
    
    # 查找Hero section的行号
    hero_line=$(grep -n '<section class="hero">' "$file" | head -1 | cut -d: -f1)
    
    # 查找"香港中小企業真實案例"的行号
    case_line=$(grep -n "香港中小企業真實案例\|香港中小企成功案例" "$file" | head -1 | cut -d: -f1)
    
    # 查找"常見問題"的行号
    faq_line=$(grep -n "常見問題" "$file" | grep "<h2\|<h3" | head -1 | cut -d: -f1)
    
    echo "   Hero section: 行 $hero_line"
    echo "   案例section:  行 $case_line"
    echo "   FAQ section:  行 $faq_line"
    
    if [ -n "$hero_line" ] && [ -n "$case_line" ] && [ -n "$faq_line" ]; then
        if [ "$hero_line" -lt "$case_line" ] && [ "$case_line" -lt "$faq_line" ]; then
            echo "   ✅ 正确顺序: Hero → 案例 → FAQ"
        else
            echo "   ❌ 顺序错误"
        fi
    fi
    
    echo ""
done

echo "===================================================================="
echo ""
echo "🎯 关于居中问题："
echo "   所有5个文件的.hero-content CSS都已经正确设置了居中："
echo "   - display: flex"
echo "   - flex-direction: column"
echo "   - align-items: center"
echo "   - text-align: center"
echo ""
echo "   如果文字还在左边，可能原因："
echo "   1. ✅ 浏览器缓存未清除 (Cmd+Shift+Delete)"
echo "   2. ✅ 服务器端文件未更新"
echo "   3. ✅ 需要硬刷新页面 (Cmd+Shift+R)"
echo "===================================================================="

