#!/bin/bash

# 批量修复英文版会员菜单和删除Learning Center

echo "🔧 开始批量修复..."

# 修复的文件列表（排除首页，因为首页已经正确）
files_to_fix=(
    "en/dashboard.html"
    "en/firstproject.html"
    "en/document-detail.html"
    "en/account.html"
    "en/billing.html"
    "en/auth.html"
)

# 1️⃣ 修复英文版会员菜单（账户、计费、登出）
echo ""
echo "1️⃣ 修复英文版会员菜单..."

for file in "${files_to_fix[@]}"; do
    if [ -f "$file" ]; then
        echo "   处理: $file"
        
        # 修复"帳戶" → "Account"
        sed -i '' 's/帳戶/Account/g' "$file"
        
        # 修复"計費" → "Billing"  
        sed -i '' 's/計費/Billing/g' "$file"
        
        # 修复"登出" → "Logout"
        sed -i '' 's/登出/Logout/g' "$file"
        
        echo "   ✅ 完成: $file"
    else
        echo "   ⚠️  文件不存在: $file"
    fi
done

# 2️⃣ 删除所有语言版本的 Learning Center
echo ""
echo "2️⃣ 删除所有版本的 Learning Center..."

# 所有需要处理的语言版本
lang_versions=("" "en" "ja" "ko")

for lang in "${lang_versions[@]}"; do
    if [ -z "$lang" ]; then
        dir="."
        echo "   处理繁体中文版..."
    else
        dir="$lang"
        echo "   处理 $lang 版本..."
    fi
    
    # 查找所有HTML文件
    find "$dir" -maxdepth 1 -name "*.html" -type f | while read -r file; do
        # 检查文件是否包含 Learning Center 或 學習中心
        if grep -q "Learning Center\|學習中心\|学习中心\|ラーニングセンター\|학습 센터" "$file"; then
            echo "      修改: $file"
            
            # 删除导航栏中的 Learning Center 链接（多种可能的格式）
            # 格式1: <a href="/learning-center">...</a>
            sed -i '' '/<a[^>]*href="[^"]*learning-center[^"]*"[^>]*>.*<\/a>/d' "$file"
            
            # 格式2: <a href="learning-center.html">...</a>
            sed -i '' '/<a[^>]*href="learning-center\.html"[^>]*>.*<\/a>/d' "$file"
            
            # 格式3: 带class的完整链接
            sed -i '' '/<a class="nav-link"[^>]*>Learning Center<\/a>/d' "$file"
            sed -i '' '/<a class="nav-link"[^>]*>學習中心<\/a>/d' "$file"
            sed -i '' '/<a class="nav-link"[^>]*>学习中心<\/a>/d' "$file"
            sed -i '' '/<a class="nav-link"[^>]*>ラーニングセンター<\/a>/d' "$file"
            sed -i '' '/<a class="nav-link"[^>]*>학습 센터<\/a>/d' "$file"
            
            echo "      ✅ 完成"
        fi
    done
done

echo ""
echo "✅ 批量修复完成！"
echo ""
echo "📋 修复摘要："
echo "   1. 英文版会员菜单已更新为英文"
echo "   2. 所有版本的 Learning Center 已删除"
echo ""
echo "🔍 建议验证以下页面："
echo "   - https://vaultcaddy.com/en/dashboard.html"
echo "   - https://vaultcaddy.com/en/firstproject.html"
echo "   - https://vaultcaddy.com/dashboard.html"

