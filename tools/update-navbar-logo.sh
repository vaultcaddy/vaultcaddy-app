#!/bin/bash

# 新的 logo SVG - 使用文件圖標風格
NEW_LOGO='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>'

# 舊的 logo
OLD_LOGO='V'

# 更新所有頁面
for file in index.html billing.html account.html firstproject.html dashboard.html document-detail.html; do
    if [ -f "$file" ]; then
        echo "更新 $file..."
        # 使用 sed 替換
        sed -i '' "s|<div style=\"width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem;\">V</div>|<div style=\"width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem;\">$NEW_LOGO</div>|g" "$file"
        echo "✅ $file 已更新"
    fi
done

echo "✅ 所有頁面的 logo 已更新"
