#!/bin/bash
# 🌐 VaultCaddy 多语言同步 - 一键脚本
# 作用：快速同步中文版内容到英文、日文、韩文版本
# 使用：./sync-multilingual.sh [页面名称|all]

cd /Users/cavlinyeung/ai-bank-parser

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          🌐 VaultCaddy 多语言同步系统                                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

if [ $# -eq 0 ]; then
    echo "📝 使用方法："
    echo ""
    echo "  ./sync-multilingual.sh all              # 同步所有页面"
    echo "  ./sync-multilingual.sh dashboard        # 只同步Dashboard"
    echo "  ./sync-multilingual.sh firstproject     # 只同步项目页面"
    echo "  ./sync-multilingual.sh document-detail  # 只同步文档详情"
    echo "  ./sync-multilingual.sh account          # 只同步账户页面"
    echo "  ./sync-multilingual.sh billing          # 只同步计费页面"
    echo "  ./sync-multilingual.sh privacy          # 只同步隐私政策"
    echo "  ./sync-multilingual.sh terms            # 只同步服务条款"
    echo ""
    echo "💡 最常用："
    echo "  ./sync-multilingual.sh all"
    echo ""
    exit 0
fi

PAGE=$1

echo "🚀 开始同步..."
echo ""

python3 multilingual_sync_master.py $PAGE

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 同步完成！"
    echo ""
    echo "📝 验证链接："
    
    if [ "$PAGE" == "all" ] || [ "$PAGE" == "dashboard" ]; then
        echo "  - 英文：https://vaultcaddy.com/en/dashboard.html"
        echo "  - 日文：https://vaultcaddy.com/jp/dashboard.html"
        echo "  - 韩文：https://vaultcaddy.com/kr/dashboard.html"
    fi
    
    if [ "$PAGE" == "all" ] || [ "$PAGE" == "firstproject" ]; then
        echo "  - 英文：https://vaultcaddy.com/en/firstproject.html"
        echo "  - 日文：https://vaultcaddy.com/jp/firstproject.html"
        echo "  - 韩文：https://vaultcaddy.com/kr/firstproject.html"
    fi
    
    if [ "$PAGE" == "all" ] || [ "$PAGE" == "account" ]; then
        echo "  - 英文：https://vaultcaddy.com/en/account.html"
        echo "  - 日文：https://vaultcaddy.com/jp/account.html"
        echo "  - 韩文：https://vaultcaddy.com/kr/account.html"
    fi
    
    if [ "$PAGE" == "all" ] || [ "$PAGE" == "billing" ]; then
        echo "  - 英文：https://vaultcaddy.com/en/billing.html"
        echo "  - 日文：https://vaultcaddy.com/jp/billing.html"
        echo "  - 韩文：https://vaultcaddy.com/kr/billing.html"
    fi
    
    echo ""
    echo "🎉 完成！"
else
    echo ""
    echo "❌ 同步失败，请检查错误信息"
    exit 1
fi

