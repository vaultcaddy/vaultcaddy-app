#!/bin/bash

# 🔧 快速修復 Firebase Storage CORS

echo "🚀 開始設置 Firebase Storage CORS..."

# 切換到項目目錄
cd /Users/cavlinyeung/ai-bank-parser

# 設置 CORS（使用正確的 bucket 名稱）
echo "📝 正在設置 CORS..."
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.firebasestorage.app

# 驗證 CORS 設置
echo ""
echo "✅ 驗證 CORS 設置..."
gsutil cors get gs://vaultcaddy-production-cbbe2.firebasestorage.app

echo ""
echo "🎉 CORS 設置完成！"
echo ""
echo "📋 下一步："
echo "1. 刷新網頁（Ctrl+F5）"
echo "2. 上傳銀行對帳單測試"
echo "3. 查看控制台確認無 CORS 錯誤"

