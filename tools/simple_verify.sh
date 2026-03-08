#!/bin/bash

echo "【简单验证】检查Title和Description是否都包含收据关键词"
echo ""

check_ok=0
check_total=0

# 中文版
for file in *-bank-statement.html; do
    if [ -f "$file" ]; then
        ((check_total++))
        if grep -q '<title>.*收據.*AI' "$file" && grep -q 'description".*收據' "$file"; then
            ((check_ok++))
        else
            echo "❌ $file"
        fi
    fi
done

# 英文版
for file in en/*-bank-statement.html; do
    if [ -f "$file" ]; then
        ((check_total++))
        title_has=$(grep '<title>' "$file" | grep -i 'receipt' | wc -l | tr -d ' ')
        desc_has=$(grep 'description"' "$file" | grep -i 'receipt' | wc -l | tr -d ' ')
        if [ "$title_has" -gt 0 ] && [ "$desc_has" -gt 0 ]; then
            ((check_ok++))
        else
            echo "❌ $file (title:$title_has desc:$desc_has)"
        fi
    fi
done

# 日文版
for file in ja/*-bank-statement.html; do
    if [ -f "$file" ]; then
        ((check_total++))
        if grep -q '<title>.*領収書.*AI' "$file" && grep -q 'description".*領収書' "$file"; then
            ((check_ok++))
        else
            echo "❌ $file"
        fi
    fi
done

# 韩文版
for file in kr/*-bank-statement.html; do
    if [ -f "$file" ]; then
        ((check_total++))
        if grep -q '<title>.*영수증.*AI' "$file" && grep -q 'description".*영수증' "$file"; then
            ((check_ok++))
        else
            echo "❌ $file"
        fi
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "✅ 符合要求：$check_ok/$check_total 个文件"
echo "════════════════════════════════════════════════════════════════════"

