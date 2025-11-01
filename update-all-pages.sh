#!/bin/bash

# 更新所有頁面的腳本引用

files=("dashboard.html" "firstproject.html" "document-detail.html" "billing.html" "index.html")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "更新 $file..."
        
        # 替換舊的認證腳本為新的簡化系統
        sed -i.bak 's|auth-handler\.js?v=[^"]*|simple-auth.js?v=20251101|g' "$file"
        sed -i.bak 's|firebase-data-manager\.js?v=[^"]*|simple-data-manager.js?v=20251101|g' "$file"
        
        # 更新版本號
        sed -i.bak 's|firebase-config\.js?v=[^"]*|firebase-config.js?v=20251101|g' "$file"
        sed -i.bak 's|navbar-component\.js?v=[^"]*|navbar-component.js?v=20251101|g' "$file"
        sed-i.bak 's|translations\.js?v=[^"]*|translations.js?v=20251101|g' "$file"
        
        echo "✅ $file 已更新"
    fi
done

echo "✅ 所有頁面已更新"
