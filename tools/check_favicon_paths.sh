#!/bin/bash

echo "【检查所有子目录中favicon路径是否正确】"
echo ""

# 检查所有子目录中的HTML文件
for file in en/*.html jp/*.html kr/*.html; do
    if [ -f "$file" ]; then
        # 检查是否有favicon但路径不正确（缺少../）
        if grep -q 'href="favicon' "$file" 2>/dev/null; then
            echo "❌ $file - 路径错误（缺少 ../）"
        elif grep -q 'href="../favicon' "$file" 2>/dev/null; then
            echo "✅ $file"
        fi
    fi
done

