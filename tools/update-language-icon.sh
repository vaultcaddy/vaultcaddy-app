#!/bin/bash

# 更新所有頁面的語言圖標
# 從 fa-globe 改為 fa-language（更現代的語言圖標）

for file in index.html billing.html account.html firstproject.html dashboard.html document-detail.html; do
    if [ -f "$file" ]; then
        echo "更新 $file 的語言圖標..."
        # 使用 sed 替換
        sed -i '' 's|<i class="fas fa-globe"></i>|<i class="fas fa-language"></i>|g' "$file"
        echo "✅ $file 已更新"
    fi
done

echo "✅ 所有頁面的語言圖標已更新"
