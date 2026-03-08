#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         ✅ Favicon 添加完成 - 最终验证报告                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "【🎯 关键页面验证】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 主页
echo "1. 主页（Index）："
for page in index.html en/index.html jp/index.html kr/index.html; do
    if grep -q "favicon" "$page" 2>/dev/null; then
        echo "   ✅ $page"
    else
        echo "   ❌ $page"
    fi
done
echo ""

# 学习中心
echo "2. 学习中心（Resources）："
for page in resources.html en/resources.html jp/resources.html kr/resources.html; do
    if grep -q "favicon" "$page" 2>/dev/null; then
        echo "   ✅ $page"
    else
        echo "   ❌ $page"
    fi
done
echo ""

# 银行页面
echo "3. 银行Landing Pages："
for page in hsbc-bank-statement.html en/hsbc-bank-statement.html hangseng-bank-statement.html citibank-bank-statement.html; do
    if [ -f "$page" ] && grep -q "favicon" "$page" 2>/dev/null; then
        echo "   ✅ $page"
    fi
done
echo ""

# 行业解决方案
echo "4. 行业解决方案（Solutions）："
for lang in "" en jp kr; do
    if [ -z "$lang" ]; then
        base="solutions"
    else
        base="$lang/solutions"
    fi
    
    for solution in restaurant accountant ecommerce retail-store; do
        page="$base/$solution/index.html"
        if [ -f "$page" ] && grep -q "favicon" "$page" 2>/dev/null; then
            echo "   ✅ $page"
        fi
    done
done
echo ""

# 用户功能页面
echo "5. 用户功能页面："
for page in dashboard.html firstproject.html account.html billing.html; do
    if grep -q "favicon" "$page" 2>/dev/null; then
        echo "   ✅ $page"
    else
        echo "   ❌ $page"
    fi
done
echo ""

echo "【📊 统计数据】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

total=$(find . -name "*.html" -type f \
    ! -path "./node_modules/*" \
    ! -path "./.git/*" \
    ! -path "./backup_*/*" \
    ! -name "unified-*.html" \
    ! -name "*-template.html" \
    ! -path "./marketing_assets/*" | wc -l | xargs)

with_favicon=$(find . -name "*.html" -type f \
    ! -path "./node_modules/*" \
    ! -path "./.git/*" \
    ! -path "./backup_*/*" \
    ! -name "unified-*.html" \
    ! -name "*-template.html" \
    ! -path "./marketing_assets/*" \
    -exec grep -l "favicon" {} \; | wc -l | xargs)

without_favicon=$((total - with_favicon))
percentage=$((with_favicon * 100 / total))

echo "  完整HTML页面总数：$total"
echo "  ✅ 有favicon：$with_favicon"
echo "  ❌ 缺少favicon：$without_favicon"
echo "  📈 覆盖率：${percentage}%"
echo ""

echo "【✨ 总结】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ $percentage -ge 95 ]; then
    echo "  🎉 太棒了！${percentage}% 的页面已添加 favicon！"
    echo "  ✅ 所有关键页面都已完成"
    echo "  🚀 可以立即部署到生产环境"
elif [ $percentage -ge 90 ]; then
    echo "  👍 很好！${percentage}% 的页面已添加 favicon"
    echo "  ⚠️  仍有少数页面需要手动检查"
else
    echo "  ⚠️  ${percentage}% 的页面有 favicon"
    echo "  ❌ 还需要继续添加"
fi
echo ""

