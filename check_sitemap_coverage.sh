#!/bin/bash

echo "=========================================="
echo "🔍 检查Sitemap覆盖情况"
echo "=========================================="
echo ""

# 统计sitemap中的URL数量
sitemap_count=$(grep -c "<loc>" sitemap.xml)
echo "📊 Sitemap中的URL数量: $sitemap_count"
echo ""

# 统计实际的landing page数量
echo "📊 实际Landing Page统计:"
echo ""

# 中文银行页面
zh_bank=$(ls *-bank-statement.html 2>/dev/null | wc -l | tr -d ' ')
echo "  中文银行页面: $zh_bank 个"

# 英文银行页面
en_bank=$(ls en/*-bank-statement.html 2>/dev/null | wc -l | tr -d ' ')
echo "  英文银行页面: $en_bank 个"

# 日文银行页面
ja_bank=$(ls ja/*-bank-statement.html 2>/dev/null | wc -l | tr -d ' ')
echo "  日文银行页面: $ja_bank 个"

# 韩文银行页面
kr_bank=$(ls kr/*-bank-statement.html 2>/dev/null | wc -l | tr -d ' ')
echo "  韩文银行页面: $kr_bank 个"

echo ""

# 中文solutions页面
zh_solutions=$(find solutions -name "index.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  中文Solutions页面: $zh_solutions 个"

# 英文solutions页面
en_solutions=$(find en/solutions -name "index.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  英文Solutions页面: $en_solutions 个"

# 日文solutions页面
ja_solutions=$(find ja/solutions -name "index.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  日文Solutions页面: $ja_solutions 个"

# 韩文solutions页面
kr_solutions=$(find kr/solutions -name "index.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  韩文Solutions页面: $kr_solutions 个"

echo ""

# Blog页面
zh_blog=$(find blog -name "*.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  中文Blog页面: $zh_blog 个"

en_blog=$(find en/blog -name "*.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  英文Blog页面: $en_blog 个"

ja_blog=$(find ja/blog -name "*.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  日文Blog页面: $ja_blog 个"

kr_blog=$(find kr/blog -name "*.html" -not -path "*/\.*" 2>/dev/null | wc -l | tr -d ' ')
echo "  韩文Blog页面: $kr_blog 个"

echo ""

# Resources页面
resources_count=4  # 中英日韩各1个
echo "  Resources页面: $resources_count 个"

# 主页
index_count=4  # 中英日韩各1个
echo "  主页（index.html）: $index_count 个"

echo ""
echo "=========================================="
echo "📊 总计"
echo "=========================================="

total_bank=$((zh_bank + en_bank + ja_bank + kr_bank))
total_solutions=$((zh_solutions + en_solutions + ja_solutions + kr_solutions))
total_blog=$((zh_blog + en_blog + ja_blog + kr_blog))
total_other=$((resources_count + index_count))
total_landing=$((total_bank + total_solutions + total_blog + total_other))

echo "  银行页面总计: $total_bank 个"
echo "  Solutions页面总计: $total_solutions 个"
echo "  Blog页面总计: $total_blog 个"
echo "  其他页面（Resources+主页）: $total_other 个"
echo ""
echo "  【Landing Page总计】: $total_landing 个"
echo "  【Sitemap中的URL】: $sitemap_count 个"
echo ""

missing=$((total_landing - sitemap_count))
if [ $missing -gt 0 ]; then
    echo "  ⚠️  缺少: $missing 个页面未加入Sitemap"
    coverage=$((sitemap_count * 100 / total_landing))
    echo "  📈 覆盖率: $coverage%"
else
    echo "  ✅ 所有Landing Page都已加入Sitemap"
fi

echo ""
echo "=========================================="

