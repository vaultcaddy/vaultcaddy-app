#!/bin/bash

# 為所有主要 HTML 文件添加 Favicon

files=(
    "dashboard.html"
    "account.html"
    "billing.html"
    "firstproject.html"
    "document-detail.html"
    "auth.html"
    "verify-email.html"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        # 檢查是否已經有 favicon
        if ! grep -q "favicon.svg" "$file"; then
            echo "Adding favicon to $file..."
            # 在 </head> 前插入 favicon
            sed -i '' '/<\/head>/i\
    <!-- Favicon -->\
    <link rel="icon" type="image/svg+xml" href="favicon.svg">\
    <link rel="alternate icon" type="image/png" href="favicon.png">\
' "$file"
        else
            echo "$file already has favicon"
        fi
    fi
done

echo "✅ Favicon added to all files!"

