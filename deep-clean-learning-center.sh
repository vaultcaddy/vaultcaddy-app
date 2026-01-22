#!/bin/bash

# 更彻底地删除 Learning Center

echo "🔧 开始深度清理 Learning Center..."

# 定义所有可能的Learning Center文本
declare -a texts=(
    "Learning Center"
    "學習中心"
    "学习中心"
    "ラーニングセンター"
    "학습 센터"
)

# 定义所有需要处理的目录
declare -a dirs=(
    "."
    "en"
    "ja"
    "ko"
)

for dir in "${dirs[@]}"; do
    echo ""
    echo "📁 处理目录: $dir/"
    
    # 查找所有HTML文件（排除backup文件）
    find "$dir" -maxdepth 1 -name "*.html" -type f ! -name "*backup*" ! -name "*bak*" | while read -r file; do
        modified=false
        
        # 检查是否包含任何Learning Center文本
        for text in "${texts[@]}"; do
            if grep -q "$text" "$file"; then
                echo "   🔍 发现 '$text' in $file"
                modified=true
            fi
        done
        
        if [ "$modified" = true ]; then
            echo "   ✏️  修改: $file"
            
            # 删除包含Learning Center的完整<a>标签行
            # 模式1: 标准导航链接
            sed -i '' '/<a[^>]*>.*Learning Center.*<\/a>/d' "$file"
            sed -i '' '/<a[^>]*>.*學習中心.*<\/a>/d' "$file"
            sed-i '' '/<a[^>]*>.*学习中心.*<\/a>/d' "$file"
            sed -i '' '/<a[^>]*>.*ラーニングセンター.*<\/a>/d' "$file"
            sed -i '' '/<a[^>]*>.*학습 센터.*<\/a>/d' "$file"
            
            # 模式2: 包含在其他标签内的链接
            sed -i '' '/Learning Center/d' "$file"
            sed -i '' '/學習中心/d' "$file"
            sed -i '' '/学习中心/d' "$file"
            sed -i '' '/ラーニングセンター/d' "$file"
            sed -i '' '/학습 센터/d' "$file"
            
            echo "   ✅ 完成"
        fi
    done
done

echo ""
echo "✅ 深度清理完成！"
echo ""
echo "🔍 验证剩余数量："
echo "   英文版 Learning Center: $(grep -r "Learning Center" en/*.html 2>/dev/null | grep -v backup | wc -l | tr -d ' ')"
echo "   繁体版 學習中心: $(grep -r "學習中心" *.html 2>/dev/null | grep -v backup | wc -l | tr -d ' ')"
echo "   日文版 ラーニングセンター: $(grep -r "ラーニングセンター" ja/*.html 2>/dev/null | grep -v backup | wc -l | tr -d ' ')"
echo "   韩文版 학습 센터: $(grep -r "학습 센터" ko/*.html 2>/dev/null | grep -v backup | wc -l | tr -d ' ')"

