#!/bin/bash

# 統一的導航欄 HTML
NAVBAR='    <!-- 統一靜態導航欄 -->
    <nav class="vaultcaddy-navbar" style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <a href="../index.html" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600; font-size: 1.125rem;">
                <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem;">V</div>
                <div>
                    <div>VaultCaddy</div>
                    <div style="font-size: 0.75rem; color: #6b7280; font-weight: 400; text-transform: uppercase; letter-spacing: 0.05em;">AI DOCUMENT PROCESSING</div>
                </div>
            </a>
        </div>
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <a href="../index.html#features" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500;">功能</a>
                <a href="../billing.html" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500;">價格</a>
                <a href="../index.html#pricing" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500;">儀表板</a>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; color: #6b7280; font-size: 0.875rem; cursor: pointer; padding: 0.5rem 0.75rem; border-radius: 6px;">
                <i class="fas fa-globe"></i>
                <span>繁體中文</span>
                <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
            </div>
            <div style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; padding: 0.5rem; border-radius: 8px;" onclick="window.location.href='"'"'../account.html'"'"'">
                <div style="width: 32px; height: 32px; border-radius: 50%; background: #667eea; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.875rem;">U</div>
            </div>
        </div>
    </nav>'

# 更新文件列表
FILES="ai-invoice-processing-guide.html best-pdf-to-excel-converter.html ocr-technology-for-accountants.html automate-financial-documents.html"

for file in $FILES; do
    echo "更新 $file..."
    # 使用 sed 替換 navbar-placeholder
    sed -i '' 's|<div id="navbar-placeholder"></div>|'"$NAVBAR"'|g' "$file"
    echo "✅ $file 已更新"
done

echo "✅ 所有 blog 文章的導航欄已更新"
