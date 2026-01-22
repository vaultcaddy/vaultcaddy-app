#!/bin/bash

# 翻译 en/billing.html 的功能列表

FILE="en/billing.html"

echo "🔄 开始翻译 billing.html 功能列表..."

# 功能列表翻译
sed -i '' 's|每月 100 Credits|100 Credits per month|g' "$FILE"
sed -i '' 's|超出後每頁 HKD \$0\.3|HKD \$0.3 per page after|g' "$FILE"
sed -i '' 's|批次處理無限制文件|Unlimited batch processing|g' "$FILE"
sed -i '' 's|一鍵轉換所有文件|One-click conversion|g' "$FILE"
sed -i '' 's|Excel/CSV 匯出|Excel/CSV Export|g' "$FILE"
sed -i '' 's|QuickBooks 整合|QuickBooks Integration|g' "$FILE"
sed -i '' 's|複合式 AI 處理|Advanced AI Processing|g' "$FILE"
sed -i '' 's|電子郵件支援|Email Support|g' "$FILE"
sed -i '' 's|安全文件上傳|Secure File Upload|g' "$FILE"
sed -i '' 's|圖片保留|Image Retention|g' "$FILE"
sed -i '' 's|開始使用|Get Started|g' "$FILE"

# JavaScript 中的中文文本
sed -i '' 's|付費功能正在設置中，請稍後再試或聯繫客服|Payment feature is being set up, please try again later or contact support|g' "$FILE"
sed -i '' 's|管理員需要在 Stripe 創建新的 Payment Links|Administrator needs to create new Payment Links in Stripe|g' "$FILE"

echo "✅ 翻译完成！"
echo ""
echo "验证结果："
grep -n "批次處理\|一鍵轉換\|匯出\|整合\|處理\|電子郵件\|安全文件\|圖片保留\|開始使用" "$FILE" | head -10

