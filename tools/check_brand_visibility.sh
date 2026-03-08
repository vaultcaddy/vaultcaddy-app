#!/bin/bash
# VaultCaddy 品牌可见性诊断脚本
# 作用：检查网站索引状态、robots.txt、sitemap等关键SEO因素

echo "=========================================="
echo "🔍 VaultCaddy 品牌可见性诊断"
echo "=========================================="
echo ""

# 1. 检查网站是否可访问
echo "1️⃣ 检查网站是否可访问..."
echo "---"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://vaultcaddy.com)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ 网站可访问 (HTTP $HTTP_STATUS)"
else
    echo "❌ 网站访问异常 (HTTP $HTTP_STATUS)"
fi
echo ""

# 2. 检查首页
echo "2️⃣ 检查首页..."
echo "---"
INDEX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://vaultcaddy.com/index.html)
if [ "$INDEX_STATUS" = "200" ]; then
    echo "✅ 首页可访问 (HTTP $INDEX_STATUS)"
else
    echo "⚠️ 首页状态异常 (HTTP $INDEX_STATUS)"
fi
echo ""

# 3. 检查 robots.txt
echo "3️⃣ 检查 robots.txt..."
echo "---"
ROBOTS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://vaultcaddy.com/robots.txt)
if [ "$ROBOTS_STATUS" = "200" ]; then
    echo "✅ robots.txt 存在"
    echo ""
    echo "📄 内容："
    curl -s https://vaultcaddy.com/robots.txt
    echo ""
    echo ""
    
    # 检查是否阻止了所有抓取
    if curl -s https://vaultcaddy.com/robots.txt | grep -q "Disallow: /"; then
        if curl -s https://vaultcaddy.com/robots.txt | grep -q "Allow: /"; then
            echo "✅ robots.txt 配置正常（允许抓取）"
        else
            echo "🚨 警告：robots.txt 可能阻止了所有抓取！"
        fi
    else
        echo "✅ robots.txt 未阻止抓取"
    fi
else
    echo "⚠️ robots.txt 不存在 (HTTP $ROBOTS_STATUS)"
    echo "💡 建议：创建 robots.txt 文件"
fi
echo ""

# 4. 检查 sitemap.xml
echo "4️⃣ 检查 sitemap.xml..."
echo "---"
SITEMAP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://vaultcaddy.com/sitemap.xml)
if [ "$SITEMAP_STATUS" = "200" ]; then
    echo "✅ sitemap.xml 存在"
    echo ""
    
    # 统计URL数量
    URL_COUNT=$(curl -s https://vaultcaddy.com/sitemap.xml | grep -o "<loc>" | wc -l | tr -d ' ')
    echo "📊 Sitemap 包含 $URL_COUNT 个URL"
    echo ""
    
    # 显示前5个URL
    echo "📄 前5个URL："
    curl -s https://vaultcaddy.com/sitemap.xml | grep "<loc>" | head -5 | sed 's/.*<loc>//;s/<\/loc>.*//' | sed 's/^/   - /'
    echo ""
else
    echo "❌ sitemap.xml 不存在 (HTTP $SITEMAP_STATUS)"
    echo "🚨 严重问题：需要立即创建 sitemap.xml"
fi
echo ""

# 5. 检查首页 meta 标签
echo "5️⃣ 检查首页关键 meta 标签..."
echo "---"

# 检查 title
TITLE=$(curl -s https://vaultcaddy.com/index.html | grep -o "<title>.*</title>" | sed 's/<title>//;s/<\/title>//')
if [ -n "$TITLE" ]; then
    echo "✅ Title 标签存在"
    echo "   📝 内容：$TITLE"
    
    # 检查是否包含品牌名
    if echo "$TITLE" | grep -q -i "vaultcaddy"; then
        echo "   ✅ 包含品牌名"
    else
        echo "   ⚠️ 不包含品牌名（建议添加）"
    fi
else
    echo "❌ 未找到 title 标签"
fi
echo ""

# 检查 description
DESC=$(curl -s https://vaultcaddy.com/index.html | grep 'meta name="description"' | head -1)
if [ -n "$DESC" ]; then
    echo "✅ Description meta 标签存在"
else
    echo "⚠️ 未找到 description meta 标签（建议添加）"
fi
echo ""

# 检查 noindex
if curl -s https://vaultcaddy.com/index.html | grep -q 'noindex'; then
    echo "🚨 警告：检测到 noindex 标签！这会阻止索引！"
else
    echo "✅ 未检测到 noindex 标签"
fi
echo ""

# 6. 总结和建议
echo "=========================================="
echo "📊 诊断总结"
echo "=========================================="
echo ""

ISSUES=0

# 统计问题
if [ "$HTTP_STATUS" != "200" ]; then
    ISSUES=$((ISSUES+1))
fi

if [ "$ROBOTS_STATUS" != "200" ]; then
    ISSUES=$((ISSUES+1))
fi

if [ "$SITEMAP_STATUS" != "200" ]; then
    ISSUES=$((ISSUES+1))
fi

if [ -z "$TITLE" ]; then
    ISSUES=$((ISSUES+1))
fi

# 显示结果
if [ $ISSUES -eq 0 ]; then
    echo "✅ 技术检查通过！未发现明显问题。"
    echo ""
    echo "💡 可能的原因："
    echo "   1. 网站太新（需要30-90天建立权重）"
    echo "   2. Domain Authority 太低"
    echo "   3. 缺少外部链接"
    echo "   4. 品牌信号不足"
    echo ""
    echo "🚀 建议立即执行："
    echo "   1. 在 GSC 手动请求首页索引"
    echo "   2. 添加 Organization 结构化数据"
    echo "   3. 建立社交媒体链接"
    echo "   4. 提交商业目录"
else
    echo "🚨 发现 $ISSUES 个问题需要修复！"
    echo ""
    echo "📋 请按以下顺序修复："
    
    if [ "$ROBOTS_STATUS" != "200" ]; then
        echo "   1. 创建 robots.txt 文件"
    fi
    
    if [ "$SITEMAP_STATUS" != "200" ]; then
        echo "   2. 创建和提交 sitemap.xml"
    fi
    
    if [ -z "$TITLE" ]; then
        echo "   3. 添加首页 title 和 description"
    fi
    
    echo "   4. 在 GSC 手动请求索引"
fi

echo ""
echo "=========================================="
echo "🔗 下一步行动"
echo "=========================================="
echo ""
echo "1. 在 Google 搜索框输入："
echo "   site:vaultcaddy.com"
echo "   查看有多少页被索引"
echo ""
echo "2. 在 Google Search Console："
echo "   - 检查 '网页' 索引状态"
echo "   - 手动请求首页索引"
echo "   - 重新提交 sitemap"
echo ""
echo "3. 优化首页："
echo "   - 确保品牌名在 title 最前面"
echo "   - 添加 Organization 结构化数据"
echo ""
echo "4. 建立外部链接："
echo "   - Instagram Bio 添加网站链接"
echo "   - 创建 Google My Business"
echo "   - 提交商业目录"
echo ""
echo "预期时间：30-90天看到显著改善"
echo ""

