#!/bin/bash
# VaultCaddy IG Post 一鍵生成腳本

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 VaultCaddy IG Post 自動生成器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3"
    echo "請先安裝 Python 3: https://www.python.org/downloads/"
    exit 1
fi

# 檢查依賴
if ! python3 -c "import PIL" &> /dev/null; then
    echo "📦 安裝依賴..."
    pip3 install -r requirements.txt
fi

# 運行生成器
echo "🎨 開始生成 IG 帖子..."
echo ""
python3 generator.py

# 打開輸出目錄
if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ 生成完成！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📂 打開輸出目錄..."
    open ig-posts/ 2>/dev/null || xdg-open ig-posts/ 2>/dev/null || echo "請手動打開: ig-posts/"
else
    echo ""
    echo "❌ 生成失敗"
    exit 1
fi

