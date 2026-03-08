#!/bin/bash

# ============================================
# 为所有页面添加 Favicon 配置
# ============================================
# 作用：确保 vaultcaddy.com 下所有页面都使用相同的 Favicon
# 使用：./add-favicon-all-pages.sh
# ============================================

echo "🔍 开始检查并添加 Favicon 配置..."

# Favicon 配置（中文版根目录）
FAVICON_ROOT='    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="alternate icon" type="image/png" href="favicon.png">'

# Favicon 配置（子目录：en/jp/kr/）
FAVICON_SUBDIR='    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">'

# Favicon 配置（blog 目录）
FAVICON_BLOG='    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">'

# Favicon 配置（二级子目录：en/blog/, jp/blog/, kr/blog/）
FAVICON_BLOG_SUBDIR='    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../../favicon.png">'

# 计数器
count_added=0
count_exists=0
count_total=0

# ============================================
# 函数：检查文件是否已有 Favicon
# ============================================
check_favicon() {
    local file="$1"
    if grep -q "favicon" "$file"; then
        return 0  # 已存在
    else
        return 1  # 不存在
    fi
}

# ============================================
# 函数：添加 Favicon（在 <head> 之后）
# ============================================
add_favicon() {
    local file="$1"
    local favicon_code="$2"
    
    # 检查文件是否存在
    if [ ! -f "$file" ]; then
        echo "  ⏭️  跳过（文件不存在）: $file"
        return
    fi
    
    count_total=$((count_total + 1))
    
    # 检查是否已有 Favicon
    if check_favicon "$file"; then
        echo "  ✅ 已存在: $file"
        count_exists=$((count_exists + 1))
        return
    fi
    
    # 在 <head> 标签后添加 Favicon
    # 使用临时文件进行替换
    awk -v favicon="$favicon_code" '
        /<head>/ { 
            print; 
            print favicon; 
            next 
        } 
        { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    
    echo "  ➕ 已添加: $file"
    count_added=$((count_added + 1))
}

# ============================================
# 1. 根目录 HTML 文件
# ============================================
echo ""
echo "📁 检查根目录..."
for file in *.html; do
    [ -f "$file" ] && add_favicon "$file" "$FAVICON_ROOT"
done

# ============================================
# 2. 子目录（en/, jp/, kr/）的 HTML 文件
# ============================================
for lang in en jp kr; do
    echo ""
    echo "📁 检查 $lang/ 目录..."
    
    # 主页面
    for file in "$lang"/*.html; do
        [ -f "$file" ] && add_favicon "$file" "$FAVICON_SUBDIR"
    done
    
    # blog 子目录
    if [ -d "$lang/blog" ]; then
        echo ""
        echo "📁 检查 $lang/blog/ 目录..."
        for file in "$lang/blog"/*.html; do
            [ -f "$file" ] && add_favicon "$file" "$FAVICON_BLOG_SUBDIR"
        done
    fi
done

# ============================================
# 3. 中文 blog 目录
# ============================================
if [ -d "blog" ]; then
    echo ""
    echo "📁 检查 blog/ 目录..."
    for file in blog/*.html; do
        [ -f "$file" ] && add_favicon "$file" "$FAVICON_BLOG"
    done
fi

# ============================================
# 总结
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 处理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  检查文件总数: $count_total"
echo "  已有 Favicon: $count_exists"
echo "  新增 Favicon: $count_added"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 所有页面现在都使用相同的 Favicon！"
echo ""
echo "📝 Favicon 文件位置："
echo "  - favicon.svg (矢量图标)"
echo "  - favicon.png (位图图标)"
echo ""

