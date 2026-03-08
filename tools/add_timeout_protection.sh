#!/bin/bash

# 批量为所有关键页面添加超时保护

echo "🔧 开始批量添加超时保护..."

# 需要更新的文件列表
files=(
    "en/firstproject.html"
    "jp/firstproject.html"
    "kr/firstproject.html"
    "en/document-detail.html"
    "jp/document-detail.html"
    "kr/document-detail.html"
    "account.html"
    "en/account.html"
    "jp/account.html"
    "kr/account.html"
)

# 超时保护代码
timeout_code='
        
        // ✅ 超時保護：10秒後強制顯示頁面（防止卡住）
        setTimeout(function() {
            if (document.body.classList.contains('\''auth-checking'\'')) {
                console.warn('\''⚠️ Auth 初始化超時（10秒），強制顯示頁面'\'');
                document.body.classList.remove('\''auth-checking'\'');
                document.body.classList.add('\''auth-ready'\'');
                
                // 如果沒有登入，重定向到首頁
                if (!window.simpleAuth || !window.simpleAuth.currentUser) {
                    console.log('\''❌ 超時且未登入，重定向到首頁'\'');
                    setTimeout(function() {
                        window.location.href = '\''index.html'\'';
                    }, 1000);
                }
            }
        }, 10000);'

# 遍历所有文件
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        # 检查文件是否已经包含超时保护
        if grep -q "超時保護" "$file"; then
            echo "⏭️  跳过 $file (已包含超时保护)"
        else
            echo "✅ 处理 $file"
            # 这里需要手动处理，因为每个文件的结构可能不同
            echo "   ⚠️  请手动检查并更新此文件"
        fi
    else
        echo "❌ 文件不存在: $file"
    fi
done

echo ""
echo "📋 需要手动更新的文件列表："
echo "   - en/firstproject.html"
echo "   - jp/firstproject.html"
echo "   - kr/firstproject.html"
echo "   - en/document-detail.html"
echo "   - jp/document-detail.html"
echo "   - kr/document-detail.html"
echo "   - account.html"
echo "   - en/account.html"
echo "   - jp/account.html"
echo "   - kr/account.html"
echo ""
echo "🔍 请在每个文件的 auth-checking script 标签中添加超时保护代码"

