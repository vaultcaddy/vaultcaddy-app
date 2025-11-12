#!/bin/bash

echo "🔧 Firebase 配置和部署腳本"
echo "================================"
echo ""

# 檢查 Firebase CLI 是否安裝
if ! command -v firebase &> /dev/null
then
    echo "❌ Firebase CLI 未安裝"
    echo ""
    echo "請先安裝 Firebase CLI："
    echo "  npm install -g firebase-tools"
    echo ""
    exit 1
fi

echo "✅ Firebase CLI 已安裝"
echo ""

# 步驟 1：部署 Firestore 規則
echo "📋 步驟 1/3：部署 Firestore 規則"
echo "--------------------------------"
firebase deploy --only firestore:rules
if [ $? -eq 0 ]; then
    echo "✅ Firestore 規則部署成功"
else
    echo "❌ Firestore 規則部署失敗"
    exit 1
fi
echo ""

# 步驟 2：設置 Email 配置
echo "📧 步驟 2/3：設置 Email 配置"
echo "--------------------------------"
echo "Gmail 地址: osclin2002@gmail.com"
echo "應用專用密碼: vjslpwfvqaowyy za"
echo ""

# 設置 email.user
firebase functions:config:set email.user="osclin2002@gmail.com"
if [ $? -eq 0 ]; then
    echo "✅ email.user 設置成功"
else
    echo "❌ email.user 設置失敗"
    exit 1
fi

# 設置 email.password（去掉空格）
firebase functions:config:set email.password="vjslpwfvqaowyy za"
if [ $? -eq 0 ]; then
    echo "✅ email.password 設置成功"
else
    echo "❌ email.password 設置失敗"
    exit 1
fi
echo ""

# 驗證配置
echo "🔍 驗證配置..."
firebase functions:config:get
echo ""

# 步驟 3：部署 Cloud Functions
echo "☁️  步驟 3/3：部署 Cloud Functions"
echo "--------------------------------"
firebase deploy --only functions
if [ $? -eq 0 ]; then
    echo "✅ Cloud Functions 部署成功"
else
    echo "❌ Cloud Functions 部署失敗"
    exit 1
fi
echo ""

echo "================================"
echo "🎉 所有配置和部署已完成！"
echo ""
echo "📝 下一步："
echo "1. 前往 https://vaultcaddy.com/dashboard.html"
echo "2. 嘗試創建項目"
echo "3. 前往 https://vaultcaddy.com/auth.html"
echo "4. 註冊新帳戶並測試驗證碼"
echo ""
