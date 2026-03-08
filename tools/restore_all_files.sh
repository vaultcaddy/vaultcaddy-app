#!/bin/bash

echo "=========================================="
echo "🔄 恢复所有修改的文件"
echo "=========================================="
echo ""

restored=0
not_found=0

# 1. 恢复 resources.html
if [ -f "resources.html.backup_before_image_spacing" ]; then
    cp resources.html.backup_before_image_spacing resources.html
    echo "✅ 已恢复: resources.html"
    restored=$((restored + 1))
else
    echo "⚠️  未找到备份: resources.html"
    not_found=$((not_found + 1))
fi

# 2. 恢复中文版银行页面
for file in *-bank-statement.html; do
    if [ -f "$file" ]; then
        # 尝试查找备份文件（可能有多个备份）
        if [ -f "$file.backup_restructure" ]; then
            cp "$file.backup_restructure" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        elif [ -f "$file.backup_reorg" ]; then
            cp "$file.backup_reorg" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        elif [ -f "$file.backup_before_image_spacing" ]; then
            cp "$file.backup_before_image_spacing" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        else
            echo "⚠️  未找到备份: $file"
            not_found=$((not_found + 1))
        fi
    fi
done

# 3. 恢复英文版银行页面
for file in en/*-bank-statement.html; do
    if [ -f "$file" ]; then
        if [ -f "$file.backup_simple" ]; then
            cp "$file.backup_simple" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        elif [ -f "$file.backup_final" ]; then
            cp "$file.backup_final" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        elif [ -f "$file.backup_reorg" ]; then
            cp "$file.backup_reorg" "$file"
            echo "✅ 已恢复: $file"
            restored=$((restored + 1))
        else
            echo "⚠️  未找到备份: $file"
            not_found=$((not_found + 1))
        fi
    fi
done

echo ""
echo "=========================================="
echo "📊 恢复统计"
echo "=========================================="
echo "✅ 已恢复: $restored 个文件"
echo "⚠️  未找到备份: $not_found 个文件"
echo ""
echo "🎉 恢复完成！所有文件已回到修改前状态"

