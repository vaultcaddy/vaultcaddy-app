#!/bin/bash

FILE="en/billing.html"

echo "🔧 开始翻译 en/billing.html 为英文..."

# 1️⃣ HTML Head
sed -i '' 's|<html lang="zh-TW">|<html lang="en">|' "$FILE"
sed -i '' 's|帳戶與計費 - VaultCaddy|Billing \& Credits - VaultCaddy|' "$FILE"
sed -i '' 's|AI驅動的|AI-powered|g' "$FILE"
sed -i '' 's|銀行對帳單轉換工具|bank statement converter|g' "$FILE"
sed -i '' 's|3秒內將PDF轉換為Excel/QuickBooks/Xero|Convert PDF to Excel/QuickBooks/Xero in 3 seconds|g' "$FILE"
sed -i '' 's|準確率98%|98% accuracy|g' "$FILE"
sed -i '' 's|免費試用20頁，無需信用卡|Free 20-page trial, no credit card required|g' "$FILE"
sed -i '' 's|從¥926/月起|From ¥926/month|g' "$FILE"
sed -i '' 's|受到日本200+企業信賴|Trusted by 200+ Japanese companies|g' "$FILE"

# 2️⃣ Navigation
sed -i '' 's/機能/Features/g' "$FILE"
sed -i '' 's/價格/Pricing/g' "$FILE"
sed -i '' 's/儀表板/Dashboard/g' "$FILE"
sed -i '' 's/ダッシュボード/Dashboard/g' "$FILE"
sed -i '' 's/ホーム/Home/g' "$FILE"
sed -i '' 's/プライバシーポリシー/Privacy Policy/g' "$FILE"
sed -i '' 's/隱私政策/Privacy Policy/g' "$FILE"
sed -i '' 's/利用規約/Terms of Service/g' "$FILE"
sed -i '' 's/使用條款/Terms of Service/g' "$FILE"

# 3️⃣ User Menu
sed -i '' 's/アカウント/Account/g' "$FILE"
sed -i '' 's/帳戶/Account/g' "$FILE"
sed -i '' 's/請求/Billing/g' "$FILE"
sed -i '' 's/計費/Billing/g' "$FILE"
sed -i '' 's/ログアウト/Logout/g' "$FILE"
sed -i '' 's/登出/Logout/g' "$FILE"

# 4️⃣ Main Heading
sed -i '' 's/隱藏的費用無し、安全で信頼できる/Fair and Affordable Pricing/g' "$FILE"
sed -i '' 's/隱藏的費用なし、安全で信頼できる/Fair and Affordable Pricing/g' "$FILE"
sed -i '' 's/隠れた費用なし、安全で信頼できる/Fair and Affordable Pricing/g' "$FILE"
sed -i '' 's/数千の企業とともに、財務データ入力の時間を節約しましょう。/Join thousands of businesses saving time on financial data entry./g' "$FILE"
sed -i '' 's/與數千家企業一起節省財務數據輸入時間。/Join thousands of businesses saving time on financial data entry./g' "$FILE"

# 5️⃣ Pricing Plans
sed -i '' 's/月払い/Monthly/g' "$FILE"
sed -i '' 's/月繳/Monthly/g' "$FILE"
sed -i '' 's/年払い/Yearly/g' "$FILE"
sed -i '' 's/年繳/Yearly/g' "$FILE"
sed -i '' 's/含まれる内容/What'\''s Included/g' "$FILE"
sed -i '' 's/包含內容/What'\''s Included/g' "$FILE"

# 6️⃣ Credits
sed -i '' 's/月間100クレジット/100 Credits\/month/g' "$FILE"
sed -i '' 's/每月100積分/100 Credits\/month/g' "$FILE"
sed -i '' 's/年間1,200クレジット/1,200 Credits\/year/g' "$FILE"
sed -i '' 's/每年1,200積分/1,200 Credits\/year/g' "$FILE"
sed -i '' 's/超過後1ページ¥6/Then ¥6\/page/g' "$FILE"
sed -i '' 's/超過後每頁¥6/Then ¥6\/page/g' "$FILE"

# 7️⃣ Features
sed -i '' 's/バッチ処理無制限/Unlimited Batch Processing/g' "$FILE"
sed -i '' 's/無限批次處理/Unlimited Batch Processing/g' "$FILE"
sed -i '' 's/ワンクリック一括変換/One-Click Bulk Conversion/g' "$FILE"
sed -i '' 's/一鍵批量轉換/One-Click Bulk Conversion/g' "$FILE"
sed -i '' 's/ハイブリッドAI処理/Hybrid AI Processing/g' "$FILE"
sed -i '' 's/混合AI處理/Hybrid AI Processing/g' "$FILE"
sed -i '' 's/種言語支援/Languages Support/g' "$FILE"
sed -i '' 's/種語言支援/Languages Support/g' "$FILE"
sed -i '' 's/メールサポート/Email Support/g' "$FILE"
sed -i '' 's/電郵支援/Email Support/g' "$FILE"
sed -i '' 's/安全なファイルアップロード/Secure File Upload/g' "$FILE"
sed -i '' 's/安全的文件上傳/Secure File Upload/g' "$FILE"
sed -i '' 's/データ保持/Data Retention/g' "$FILE"
sed -i '' 's/數據保留/Data Retention/g' "$FILE"
sed -i '' 's/画像保持/Image Retention/g' "$FILE"
sed -i '' 's/圖像保留/Image Retention/g' "$FILE"

# 8️⃣ Buttons
sed -i '' 's/>始める</>Get Started</g' "$FILE"
sed -i '' 's/>開始</>Get Started</g' "$FILE"
sed -i '' 's/20%節約/Save 20%/g' "$FILE"
sed -i '' 's/節省20%/Save 20%/g' "$FILE"

# 9️⃣ Modal/Project
sed -i '' 's/建立新專案/Create New Project/g' "$FILE"
sed -i '' 's/新しいプロジェクトを作成/Create New Project/g' "$FILE"
sed -i '' 's/輸入專案名稱以作成新の文書プロジェクト/Enter project name to create a new document project/g' "$FILE"
sed -i '' 's/輸入專案名稱以創建新的文檔專案/Enter project name to create a new document project/g' "$FILE"
sed -i '' 's/專案名稱/Project Name/g' "$FILE"
sed -i '' 's/プロジェクト名/Project Name/g' "$FILE"
sed -i '' 's/>取消</>Cancel</g' "$FILE"
sed -i '' 's/>キャンセル</>Cancel</g' "$FILE"
sed -i '' 's/>建立</>Create</g' "$FILE"
sed -i '' 's/>作成</>Create</g' "$FILE"

# 🔟 Other
sed -i '' 's/本人確認中\.\.\./Verifying identity.../g' "$FILE"
sed -i '' 's/身份驗證中\.\.\./Verifying identity.../g' "$FILE"

echo "✅ 翻译完成！"
echo ""
echo "🔍 验证英文版:"
echo "   1. 检查定价标题..."
grep -q "Fair and Affordable" "$FILE" && echo "   ✅ 定价标题已翻译" || echo "   ❌ 定价标题未翻译"
echo "   2. 检查定价选项..."
grep -q "Monthly" "$FILE" && grep -q "Yearly" "$FILE" && echo "   ✅ 定价选项已翻译" || echo "   ❌ 定价选项未翻译"
echo "   3. 检查按钮..."
grep -q "Get Started" "$FILE" && echo "   ✅ 按钮已翻译" || echo "   ❌ 按钮未翻译"
echo ""
echo "📋 测试链接: https://vaultcaddy.com/en/billing.html"

