#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         🔧 修复完整URL中的 ko → kr                            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

updated=0

# 修复 vaultcaddy.com/ko/ 为 vaultcaddy.com/kr/
echo "【修复完整URL链接】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for file in kr/*.html kr/**/*.html; do
    if [ -f "$file" ]; then
        if grep -q "vaultcaddy.com/ko/" "$file"; then
            echo "  修复: $file"
            # 替换 https://vaultcaddy.com/ko/ 为 https://vaultcaddy.com/kr/
            sed -i '' 's|https://vaultcaddy.com/ko/|https://vaultcaddy.com/kr/|g' "$file"
            # 替换 http://vaultcaddy.com/ko/ 为 http://vaultcaddy.com/kr/
            sed -i '' 's|http://vaultcaddy.com/ko/|http://vaultcaddy.com/kr/|g' "$file"
            updated=$((updated + 1))
        fi
    fi
done

echo ""
echo "✅ 更新了 $updated 个文件"

# 验证
echo ""
echo "【验证】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

remaining=$(grep -r "vaultcaddy.com/ko/" kr/ 2>/dev/null | wc -l | tr -d ' ')

if [ "$remaining" = "0" ]; then
    echo "✅ 所有完整URL已更新为 vaultcaddy.com/kr/"
else
    echo "⚠️  仍有 $remaining 个链接包含 vaultcaddy.com/ko/"
    grep -r "vaultcaddy.com/ko/" kr/ 2>/dev/null | head -3
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "              ✅ 完整URL修复完成！"
echo "════════════════════════════════════════════════════════════════════"

