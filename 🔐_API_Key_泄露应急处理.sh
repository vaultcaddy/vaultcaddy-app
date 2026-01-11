#!/bin/bash

# 🔐 Stripe API Key 泄露应急处理指南

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║              🚨 API Key 泄露应急处理 🚨                              ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# ====================================================================
# 立即行动 1: 撤销泄露的API Key（最重要！）
# ====================================================================
echo "🔥 立即行动 1: 撤销泄露的 Stripe API Key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "步骤："
echo "1. 立即前往: https://dashboard.stripe.com/apikeys"
echo "2. 找到泄露的 Key: sk_live_...012q"
echo "3. 点击 '...' → 'Roll key' 或 'Delete'"
echo "4. 生成新的 Secret Key"
echo "5. 更新 Firebase Functions 环境变量"
echo ""
echo "⚠️  这是最紧急的步骤！必须立即执行！"
echo ""
read -p "按 Enter 继续到下一步..."

# ====================================================================
# 立即行动 2: 从 Git 历史中删除敏感信息
# ====================================================================
echo ""
echo "🧹 立即行动 2: 清理 Git 历史记录"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "方法 A: 使用 git filter-repo（推荐）"
echo "----------------------------------------"
echo "# 安装 git-filter-repo"
echo "brew install git-filter-repo"
echo ""
echo "# 从历史中删除文件"
echo "git filter-repo --path create_promotion_code.sh --invert-paths"
echo ""
echo "方法 B: 使用 BFG Repo-Cleaner（更快）"
echo "----------------------------------------"
echo "# 安装 BFG"
echo "brew install bfg"
echo ""
echo "# 删除文件"
echo "bfg --delete-files create_promotion_code.sh"
echo ""
echo "⚠️  注意：这将重写 Git 历史，需要 force push"
echo ""
read -p "按 Enter 继续到下一步..."

# ====================================================================
# 立即行动 3: Force Push（警告：危险操作）
# ====================================================================
echo ""
echo "⚠️  立即行动 3: Force Push 清理后的历史"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "执行清理后，需要 force push:"
echo ""
echo "git push origin --force --all"
echo "git push origin --force --tags"
echo ""
echo "⚠️  警告："
echo "• 这将覆盖远程仓库的历史"
echo "• 其他协作者需要重新克隆仓库"
echo "• 确保已备份重要数据"
echo ""
read -p "按 Enter 继续到下一步..."

# ====================================================================
# 立即行动 4: 通知 GitHub 安全团队
# ====================================================================
echo ""
echo "📧 立即行动 4: 通知 GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "如果 API Key 已被 GitHub 检测到:"
echo ""
echo "1. 在 GitHub Secret Scanning 警告中点击 'Resolve'"
echo "2. 选择原因："
echo "   - 'Revoked the secret' (已撤销密钥)"
echo "3. 确认已撤销 Stripe API Key"
echo ""
read -p "按 Enter 继续到下一步..."

# ====================================================================
# 预防措施：设置环境变量
# ====================================================================
echo ""
echo "🔒 预防措施: 正确使用环境变量"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Firebase Functions 正确设置:"
echo ""
echo "# 设置 Stripe Live Key"
echo "firebase functions:config:set stripe.live_key=\"sk_live_NEW_KEY_HERE\""
echo ""
echo "# 设置 Stripe Test Key"
echo "firebase functions:config:set stripe.test_key=\"sk_test_KEY_HERE\""
echo ""
echo "# 部署"
echo "firebase deploy --only functions"
echo ""
echo "代码中使用:"
echo "const stripeLive = require('stripe')(functions.config().stripe.live_key);"
echo ""
read -p "按 Enter 继续到下一步..."

# ====================================================================
# 预防措施：.gitignore 配置
# ====================================================================
echo ""
echo "📝 预防措施: 更新 .gitignore"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "添加到 .gitignore:"
echo ""
echo "# API Keys 和敏感文件"
echo "*.key"
echo "*.pem"
echo "*_key.sh"
echo "*_secret.sh"
echo ".env"
echo ".env.local"
echo "config/secrets.js"
echo ""
read -p "按 Enter 查看总结..."

# ====================================================================
# 总结
# ====================================================================
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║                      📋 执行清单                                     ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ 必须立即完成:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. ✅ 在 Stripe Dashboard 撤销泄露的 API Key"
echo "2. ✅ 生成新的 API Key"
echo "3. ✅ 更新 Firebase Functions 环境变量"
echo "4. ✅ 使用 git-filter-repo 清理 Git 历史"
echo "5. ✅ Force push 清理后的历史"
echo "6. ✅ 在 GitHub 中标记警告为已解决"
echo ""
echo "✅ 预防措施:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. ✅ 更新 .gitignore"
echo "8. ✅ 使用 Firebase Functions Config"
echo "9. ✅ 设置 Secret Scanning 监控"
echo "10. ✅ 定期轮换 API Keys"
echo ""
echo "预计时间: 15-30分钟"
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║         ⚠️  记住：API Key 已泄露，必须立即撤销！⚠️                 ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"









