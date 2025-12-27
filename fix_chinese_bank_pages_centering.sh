#!/bin/bash
# 修复中文版银行页面的居中问题

# 中文版银行页面列表
files=(
    "hsbc-bank-statement.html"
    "hangseng-bank-statement.html"
    "bochk-bank-statement.html"
    "sc-bank-statement.html"
    "dbs-bank-statement.html"
    "citibank-bank-statement.html"
    "bea-bank-statement.html"
    "bankcomm-bank-statement.html"
    "citic-bank-statement.html"
    "dahsing-bank-statement.html"
)

echo "========================================================================"
echo "修复中文版银行页面的居中问题"
echo "========================================================================"
echo ""

modified_count=0

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "处理: $file"
        
        # 备份
        cp "$file" "${file}.backup_centering"
        
        # 修复.bank-logo的CSS
        # 添加display: inline-block和确保text-align: center
        sed -i '' '/.bank-logo {/,/}/s/width: 120px;/display: inline-block;\
            width: auto;\
            text-align: center;/' "$file"
        
        # 修复.hero-content，确保使用flex布局居中
        sed -i '' '/.hero-content {/,/}/s/text-align: center;/display: flex;\
            flex-direction: column;\
            align-items: center;\
            text-align: center;/' "$file"
        
        # 修复.core-benefits，确保margin居中
        sed -i '' '/.core-benefits {/,/}/s/margin: 2rem auto;/margin: 2rem auto;\
            justify-content: center;/' "$file"
        
        echo "  ✅ 已修复"
        modified_count=$((modified_count + 1))
    else
        echo "  ⏭️  文件不存在，跳过"
    fi
    echo ""
done

echo "========================================================================"
echo "✅ 修复完成！"
echo ""
echo "📊 统计："
echo "   - 已修复文件数：$modified_count"
echo ""
echo "🔍 修复内容："
echo "   1. .bank-logo：添加 display: inline-block"
echo "   2. .hero-content：使用 flex 布局确保完美居中"
echo "   3. .core-benefits：添加 justify-content: center"
echo ""
echo "💡 验证方法："
echo "   打开浏览器查看任意银行页面，确认："
echo "   - 银行logo卡片在页面中央"
echo "   - 标题和副标题居中"
echo "   - 4个核心卖点卡片居中对齐"
echo "========================================================================"

