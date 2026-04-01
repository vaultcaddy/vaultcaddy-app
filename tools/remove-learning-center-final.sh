#!/bin/bash

# 最终清理：删除所有残留的学习中心引用

echo "🧹 开始最终清理..."
echo ""

# 定义所有需要检查的 HTML 文件
ALL_FILES=(
    jp/document-detail.html
    jp/privacy.html
    jp/terms.html
    kr/document-detail.html
    kr/privacy.html
    kr/terms.html
)

for file in "${ALL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "📝 清理: $file"
        
        # 删除导航栏链接（单行）
        sed -i '' '/<a href="[^"]*blog\/" [^>]*>学習センター<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="[^"]*blog\/" [^>]*>학습 센터<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="[^"]*blog\/" [^>]*>Learning Center<\/a>/d' "$file" 2>/dev/null
        
        # 删除移动端侧边栏中的学习中心（多行）
        # 删除包含 fa-graduation-cap 图标和文本的整个 <a> 标签
        sed -i '' '/<a href="[^"]*blog\/".*fa-graduation-cap/,/<\/a>/d' "$file" 2>/dev/null
        
        echo "   ✅ 完成"
    fi
done

# 删除 JSON-LD 中的学习中心引用
echo ""
echo "📝 清理 JSON-LD 结构化数据..."

for file in jp/index.html kr/index.html; do
    if [ -f "$file" ]; then
        echo "   处理: $file"
        # 删除包含学习中心的 JSON 对象
        sed -i '' '/{"@type": "SiteNavigationElement",/,/"name": "学習センター"/d' "$file" 2>/dev/null
        sed -i '' '/{"@type": "SiteNavigationElement",/,/"name": "학습 센터"/d' "$file" 2>/dev/null
    fi
done

echo ""
echo "🎉 最终清理完成！"
echo ""
echo "📊 验证结果："

# 验证日文版
JP_COUNT=$(grep -r "学習センター" jp/*.html 2>/dev/null | grep -v "// " | wc -l | tr -d ' ')
echo "日文版残留: $JP_COUNT 处"
if [ "$JP_COUNT" -eq "0" ]; then
    echo "   ✅ 日文版完全清理"
else
    echo "   ⚠️  仍有残留，显示前 5 条："
    grep -n "学習センター" jp/*.html 2>/dev/null | grep -v "// " | head -5
fi

echo ""

# 验证韩文版
KR_COUNT=$(grep -r "학습 센터" kr/*.html 2>/dev/null | grep -v "// " | wc -l | tr -d ' ')
echo "韩文版残留: $KR_COUNT 处"
if [ "$KR_COUNT" -eq "0" ]; then
    echo "   ✅ 韩文版完全清理"
else
    echo "   ⚠️  仍有残留，显示前 5 条："
    grep -n "학습 센터" kr/*.html 2>/dev/null | grep -v "// " | head -5
fi

