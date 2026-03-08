#!/bin/bash

echo "===================================================================="
echo "检查案例section的位置"
echo "===================================================================="
echo ""

for file in hsbc-bank-statement.html bankcomm-bank-statement.html citic-bank-statement.html dahsing-bank-statement.html citibank-bank-statement.html; do
    echo "=== $file ==="
    
    # 查找"香港中小企業真實案例"的行号
    case_line=$(grep -n "香港中小企業真實案例\|香港中小企成功案例" "$file" | head -1 | cut -d: -f1)
    
    # 查找"常見問題"的行号
    faq_line=$(grep -n "常見問題 FAQ\|## 💬 常見問題" "$file" | head -1 | cut -d: -f1)
    
    if [ -n "$case_line" ] && [ -n "$faq_line" ]; then
        if [ "$case_line" -lt "$faq_line" ]; then
            echo "   ✅ 案例在FAQ之前 (行$case_line < 行$faq_line)"
        else
            echo "   ❌ 案例在FAQ之后 (行$case_line > 行$faq_line) - 需要调整"
        fi
    elif [ -n "$case_line" ]; then
        echo "   ⚠️  有案例（行$case_line），但没找到FAQ section"
    elif [ -n "$faq_line" ]; then
        echo "   ⚠️  有FAQ（行$faq_line），但没找到案例section"
    else
        echo "   ⚠️  既没有案例也没有FAQ"
    fi
    
    echo ""
done

echo "===================================================================="

