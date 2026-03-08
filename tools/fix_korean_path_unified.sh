#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         🔧 统一韩文版路径：ko/ → kr/                          ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: 移动ko目录的文件到kr目录
echo "【步骤1：移动文件】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "ko" ]; then
    echo "发现 ko/ 目录，开始移动文件到 kr/..."
    
    # 移动所有银行页面
    if ls ko/*-bank-statement.html 1> /dev/null 2>&1; then
        echo "  移动银行页面..."
        mv ko/*-bank-statement.html kr/ 2>/dev/null
    fi
    
    # 移动solutions目录
    if [ -d "ko/solutions" ]; then
        echo "  移动solutions目录..."
        if [ ! -d "kr/solutions" ]; then
            mkdir -p kr/solutions
        fi
        cp -r ko/solutions/* kr/solutions/ 2>/dev/null
    fi
    
    echo "✅ 文件移动完成"
else
    echo "⏭️  ko/ 目录不存在，跳过移动"
fi

echo ""

# Step 2: 更新所有HTML文件中的ko链接为kr
echo "【步骤2：更新链接】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

updated=0

# 查找所有包含/ko/的HTML文件
echo "正在搜索包含 /ko/ 链接的文件..."

for file in $(find . -name "*.html" -type f | grep -E "(kr/|ko/)" | grep -v ".backup"); do
    if grep -q "/ko/" "$file"; then
        echo "  更新: $file"
        # 创建备份
        cp "$file" "${file}.backup_ko_to_kr"
        # 替换所有 /ko/ 为 /kr/
        sed -i '' 's|/ko/|/kr/|g' "$file"
        # 替换所有 href="ko/ 为 href="kr/
        sed -i '' 's|href="ko/|href="kr/|g' "$file"
        updated=$((updated + 1))
    fi
done

echo ""
echo "✅ 更新了 $updated 个文件"

echo ""
echo "【步骤3：验证】"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查是否还有ko/链接
remaining=$(grep -r "/ko/" kr/*.html 2>/dev/null | wc -l)
echo "kr/ 目录剩余 /ko/ 链接: $remaining 个"

if [ $remaining -eq 0 ]; then
    echo "✅ 所有链接已更新为 /kr/"
else
    echo "⚠️  仍有 $remaining 个 /ko/ 链接需要检查"
    grep -r "/ko/" kr/*.html 2>/dev/null | head -5
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "              ✅ 韩文版路径统一完成！"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "下一步："
echo "1. 验证 kr/ 目录文件完整性"
echo "2. 测试几个韩文页面链接"
echo "3. 确认无误后删除 ko/ 目录"
echo ""

