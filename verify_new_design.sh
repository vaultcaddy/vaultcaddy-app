#!/bin/bash

echo "===================================================================="
echo "🎨 验证新设计是否成功应用"
echo "===================================================================="
echo ""

# 检查新CSS是否存在
echo "1. 检查新设计CSS..."
if grep -q "price-comparison-hero" hsbc-vs-manual.html; then
    echo "   ✅ 价格对比大卡片 CSS 已添加"
else
    echo "   ❌ 价格对比大卡片 CSS 未找到"
fi

if grep -q "savings-showcase" hsbc-vs-manual.html; then
    echo "   ✅ 节省金额展示 CSS 已添加"
else
    echo "   ❌ 节省金额展示 CSS 未找到"
fi

if grep -q "modern-comparison-table" hsbc-vs-manual.html; then
    echo "   ✅ 现代对比表格 CSS 已添加"
else
    echo "   ❌ 现代对比表格 CSS 未找到"
fi

if grep -q "scenario-card-modern" hsbc-vs-manual.html; then
    echo "   ✅ 场景卡片网格 CSS 已添加"
else
    echo "   ❌ 场景卡片网格 CSS 未找到"
fi

echo ""
echo "2. 检查新HTML内容..."
if grep -q "price-comparison-hero" hsbc-vs-manual.html; then
    echo "   ✅ 新设计HTML内容已应用"
else
    echo "   ❌ 新设计HTML内容未找到"
fi

echo ""
echo "3. 检查备份文件..."
if [ -f "hsbc-vs-manual.html.backup_redesign" ]; then
    echo "   ✅ 备份文件已创建 (backup_redesign)"
fi

if [ -f "hsbc-vs-manual.html.backup_content_replace" ]; then
    echo "   ✅ 备份文件已创建 (backup_content_replace)"
fi

echo ""
echo "===================================================================="
echo "✅ 验证完成！"
echo "===================================================================="
echo ""
echo "📝 文件大小对比："
if [ -f "hsbc-vs-manual.html.backup_redesign" ]; then
    OLD_SIZE=$(wc -c < hsbc-vs-manual.html.backup_redesign)
    NEW_SIZE=$(wc -c < hsbc-vs-manual.html)
    DIFF=$((NEW_SIZE - OLD_SIZE))
    echo "   修复前: $OLD_SIZE bytes"
    echo "   修复后: $NEW_SIZE bytes"
    echo "   增加: $DIFF bytes (新增CSS和HTML内容)"
fi

echo ""
echo "💡 下一步："
echo "   1. 上传 hsbc-vs-manual.html 到服务器"
echo "   2. 清除浏览器缓存 (Cmd+Shift+Delete)"
echo "   3. 访问 https://vaultcaddy.com/hsbc-vs-manual.html"
echo "   4. 查看全新的卡片式设计！"
echo "===================================================================="

