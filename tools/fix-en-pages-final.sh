#!/bin/bash

echo "🔧 修复英文版页面..."

# 1️⃣ 删除所有英文版的 Learning Center
echo ""
echo "1️⃣ 删除 Learning Center..."

en_files=(
    "en/dashboard.html"
    "en/firstproject.html"
    "en/account.html"
    "en/billing.html"
    "en/privacy.html"
    "en/terms.html"
    "en/document-detail.html"
)

for file in "${en_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   处理: $file"
        
        # 删除导航栏的 Learning Center 链接（日文版）
        sed -i '' '/<a[^>]*>学習センター<\/a>/d' "$file"
        sed -i '' '/<a[^>]*href="blog\/"[^>]*>Learning Center<\/a>/d' "$file"
        
        # 删除移动端侧边栏的 Learning Center
        sed -i '' '/<a[^>]*href="blog\/"[^>]*>.*<span>学習センター<\/span>/,/<\/a>/d' "$file"
        sed -i '' '/<a[^>]*href="blog\/"[^>]*>.*<span>Learning Center<\/span>/,/<\/a>/d' "$file"
        
        echo "   ✅ 完成"
    fi
done

# 2️⃣ 修复 en/billing.html 的日文内容
echo ""
echo "2️⃣ 修复 en/billing.html 日文内容..."

if [ -f "en/billing.html" ]; then
    echo "   替换日文为英文..."
    
    # 导航栏文字
    sed -i '' 's/機能/Features/g' "en/billing.html"
    sed -i '' 's/価格/Pricing/g' "en/billing.html"
    sed -i '' 's/ダッシュボード/Dashboard/g' "en/billing.html"
    sed -i '' 's/ホーム/Home/g' "en/billing.html"
    
    # 其他常用日文
    sed -i '' 's/本人確認中\.\.\./Verifying identity.../g' "en/billing.html"
    sed -i '' 's/隠れた費用なし、安全で信頼できる/Fair and Affordable Pricing/g' "en/billing.html"
    sed -i '' 's/数千の企業とともに、財務データ入力の時間を節約しましょう。/Join thousands of businesses saving time on financial data entry./g' "en/billing.html"
    
    # 定价相关
    sed -i '' 's/月払い/Monthly/g' "en/billing.html"
    sed -i '' 's/年払い/Yearly/g' "en/billing.html"
    sed -i '' 's/含まれる内容/What'\''s Included/g' "en/billing.html"
    sed -i '' 's/月間100クレジット/100 Credits\/month/g' "en/billing.html"
    sed -i '' 's/年間1,200クレジット/1,200 Credits\/year/g' "en/billing.html"
    sed -i '' 's/超過後1ページ¥6/Then ¥6\/page/g' "en/billing.html"
    sed -i '' 's/バッチ処理無制限/Unlimited Batch Processing/g' "en/billing.html"
    sed -i '' 's/ワンクリック一括変換/One-Click Bulk Conversion/g' "en/billing.html"
    sed -i '' 's/ハイブリッドAI処理/Hybrid AI Processing/g' "en/billing.html"
    sed -i '' 's/種言語支援/Languages Support/g' "en/billing.html"
    sed -i '' 's/メールサポート/Email Support/g' "en/billing.html"
    sed -i '' 's/安全なファイルアップロード/Secure File Upload/g' "en/billing.html"
    sed -i '' 's/データ保持/Data Retention/g' "en/billing.html"
    sed -i '' 's/画像保持/Image Retention/g' "en/billing.html"
    sed -i '' 's/始める/Get Started/g' "en/billing.html"
    sed -i '' 's/20%節約/Save 20%/g' "en/billing.html"
    
    # 其他UI文字
    sed -i '' 's/建立新專案/Create New Project/g' "en/billing.html"
    sed -i '' 's/輸入專案名稱以作成新の文書プロジェクト/Enter project name to create a new document project/g' "en/billing.html"
    sed -i '' 's/專案名稱/Project Name/g' "en/billing.html"
    sed -i '' 's/取消/Cancel/g' "en/billing.html"
    sed -i '' 's/建立/Create/g' "en/billing.html"
    
    # Schema.org 相关
    sed -i '' 's/プライバシーポリシー/Privacy Policy/g' "en/billing.html"
    sed -i '' 's/利用規約/Terms of Service/g' "en/billing.html"
    
    # 会员菜单（如果还有残留）
    sed -i '' 's/アカウント/Account/g' "en/billing.html"
    sed -i '' 's/請求/Billing/g' "en/billing.html"
    sed -i '' 's/ログアウト/Logout/g' "en/billing.html"
    
    echo "   ✅ 完成"
fi

echo ""
echo "✅ 所有修复完成！"
echo ""
echo "🔍 验证："
echo "   1. en/billing.html 日文 → 英文"
echo "   2. 所有英文版删除 Learning Center"
echo ""
echo "📋 建议测试："
echo "   - https://vaultcaddy.com/en/billing.html"
echo "   - https://vaultcaddy.com/en/dashboard.html"
echo "   - https://vaultcaddy.com/en/firstproject.html"

