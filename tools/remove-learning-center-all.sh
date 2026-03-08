#!/bin/bash

# 批量删除所有页面导航栏中的"学习中心"
# 支持中文、英文、日文、韩文版本

echo "🔄 开始批量删除导航栏中的学习中心..."
echo ""

# 定义需要修改的文件列表
FILES=(
    "account.html"
    "firstproject.html"
    "billing.html"
    "jp/billing.html"
    "jp/account.html"
    "jp/firstproject.html"
    "jp/index.html"
    "jp/dashboard.html"
    "kr/index.html"
    "kr/dashboard.html"
    "kr/firstproject.html"
    "kr/account.html"
    "kr/billing.html"
)

# 删除主导航栏中的学习中心链接
# 中文版: 學習中心
# 日文版: 学習センター / 学習センター
# 韩文版: 학습 센터

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "📝 处理: $file"
        
        # 1. 删除主导航栏中的学习中心链接（中文）
        sed -i '' '/<a href="blog\/" style="color: #4b5563.*學習中心<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="\.\.\/blog\/" style="color: #4b5563.*學習中心<\/a>/d' "$file" 2>/dev/null
        
        # 2. 删除主导航栏中的学习中心链接（日文）
        sed -i '' '/<a href="blog\/" style="color: #4b5563.*学習センター<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="\.\.\/blog\/" style="color: #4b5563.*学習センター<\/a>/d' "$file" 2>/dev/null
        
        # 3. 删除主导航栏中的学习中心链接（韩文）
        sed -i '' '/<a href="blog\/" style="color: #4b5563.*학습 센터<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="\.\.\/blog\/" style="color: #4b5563.*학습 센터<\/a>/d' "$file" 2>/dev/null
        
        # 4. 删除主导航栏中的学习中心链接（英文）
        sed -i '' '/<a href="blog\/" style="color: #4b5563.*Learning Center<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="\.\.\/blog\/" style="color: #4b5563.*Learning Center<\/a>/d' "$file" 2>/dev/null
        
        # 5. 删除移动端侧边栏中的学习中心
        sed -i '' '/<a href="blog\/" style="padding:.*學習中心<\/span>/,/<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="blog\/" style="padding:.*学習センター<\/span>/,/<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="blog\/" style="padding:.*학습 센터<\/span>/,/<\/a>/d' "$file" 2>/dev/null
        sed -i '' '/<a href="blog\/" style="padding:.*Learning Center<\/span>/,/<\/a>/d' "$file" 2>/dev/null
        
        # 6. 删除包含学习中心图标的链接
        sed -i '' '/<i class="fas fa-graduation-cap".*<\/i>/,/學習中心<\/span>/d' "$file" 2>/dev/null
        sed -i '' '/<i class="fas fa-graduation-cap".*<\/i>/,/学習センター<\/span>/d' "$file" 2>/dev/null
        sed -i '' '/<i class="fas fa-graduation-cap".*<\/i>/,/학습 센터<\/span>/d' "$file" 2>/dev/null
        sed -i '' '/<i class="fas fa-graduation-cap".*<\/i>/,/Learning Center<\/span>/d' "$file" 2>/dev/null
        
        echo "   ✅ 完成"
    else
        echo "   ⚠️  文件不存在: $file"
    fi
done

echo ""
echo "🎉 批量删除完成！"
echo ""
echo "验证结果："
echo "1. 检查中文版页面："
grep -n "學習中心" account.html firstproject.html billing.html 2>/dev/null | head -5 || echo "   ✅ 中文版已清理"

echo ""
echo "2. 检查日文版页面："
grep -n "学習センター" jp/*.html 2>/dev/null | head -5 || echo "   ✅ 日文版已清理"

echo ""
echo "3. 检查韩文版页面："
grep -n "학습 센터" kr/*.html 2>/dev/null | head -5 || echo "   ✅ 韩文版已清理"

