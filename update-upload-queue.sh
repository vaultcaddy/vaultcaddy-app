#!/bin/bash

# 更新所有语言版本的 firstproject.html，添加上传队列机制

for file in en/firstproject.html jp/firstproject.html kr/firstproject.html; do
    if [ -f "$file" ]; then
        echo "更新 $file..."
        
        # 查找 window.handleUpload 函数的行号
        line_num=$(grep -n "window\.handleUpload = async function handleUpload" "$file" | head -1 | cut -d: -f1)
        
        if [ -n "$line_num" ]; then
            # 在 handleUpload 之前插入全局变量和 beforeunload 监听器
            sed -i '' "${line_num}i\\
        // ✅ 全局变量：跟踪是否有文件正在处理\\
        let isProcessingFiles = false;\\
        let processingCount = 0;\\
        const uploadQueue = [];\\
        \\
        // ✅ 防止用户在处理文件时离开页面\\
        window.addEventListener('beforeunload', (e) => {\\
            if (isProcessingFiles && processingCount > 0) {\\
                e.preventDefault();\\
                e.returnValue = '文件轉換進行中，請勿離開本頁。';\\
                return '文件轉換進行中，請勿離開本頁。';\\
            }\\
        });\\
        \\
" "$file"
            echo "✅ $file 已更新（添加了全局变量和 beforeunload）"
        else
            echo "⚠️ 在 $file 中未找到 handleUpload 函数"
        fi
    fi
done

echo "✅ 所有文件已更新"

