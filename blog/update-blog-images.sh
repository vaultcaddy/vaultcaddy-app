#!/bin/bash

# 為所有博客文章添加圖片樣式

# 文章列表和對應的圖標
declare -A articles
articles=(
    ["personal-bookkeeping-best-practices.html"]="fa-calculator"
    ["freelancer-tax-preparation-guide.html"]="fa-file-alt"
    ["small-business-document-management.html"]="fa-folder-open"
    ["ai-invoice-processing-for-smb.html"]="fa-robot"
    ["quickbooks-integration-guide.html"]="fa-link"
    ["accounting-firm-automation.html"]="fa-chart-line"
    ["client-document-management-for-accountants.html"]="fa-users"
    ["ocr-accuracy-for-accounting.html"]="fa-eye"
    ["accounting-workflow-optimization.html"]="fa-cogs"
)

for file in "${!articles[@]}"; do
    icon="${articles[$file]}"
    echo "更新 $file 的圖片為圖標 $icon"
    
    # 更新 CSS 樣式
    if grep -q "object-fit: cover;" "$file" 2>/dev/null; then
        sed -i.bak 's/object-fit: cover;/background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
            display: flex;\
            align-items: center;\
            justify-content: center;\
            color: white;\
            font-size: 8rem;\
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);/' "$file"
    fi
    
    # 更新 img 標籤為 div
    if grep -q '<img src="images/' "$file" 2>/dev/null; then
        sed -i.bak "s|<img src=\"images/[^\"]*\" alt=\"[^\"]*\" class=\"blog-image\">|<div class=\"blog-image\">\n                    <i class=\"fas $icon\"></i>\n                </div>|" "$file"
    fi
    
    # 刪除備份文件
    rm -f "${file}.bak"
done

echo "✅ 所有文章圖片已更新"
