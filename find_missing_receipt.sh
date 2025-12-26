#!/bin/bash

echo "【查找缺少收据关键词的页面】"
echo ""

missing=0

# 检查Solutions中文版
echo "=== Solutions中文版 ==="
for file in solutions/*/index.html; do
    if [ -f "$file" ]; then
        if ! (grep '<title>' "$file" | grep -q '收據' && grep 'description' "$file" | grep -q '收據'); then
            echo "❌ $file"
            ((missing++))
        fi
    fi
done

echo ""
echo "=== Solutions英文版 ==="
for file in en/solutions/*/index.html; do
    if [ -f "$file" ]; then
        if ! (grep '<title>' "$file" | grep -qi 'receipt' && grep 'description' "$file" | grep -qi 'receipt'); then
            echo "❌ $file"
            ((missing++))
        fi
    fi
done

echo ""
echo "=== Solutions日文版 ==="
for file in ja/solutions/*/index.html; do
    if [ -f "$file" ]; then
        if ! (grep '<title>' "$file" | grep -q '領収書' && grep 'description' "$file" | grep -q '領収書'); then
            echo "❌ $file"
            ((missing++))
        fi
    fi
done

echo ""
echo "=== Solutions韩文版 ==="
for file in kr/solutions/*/index.html; do
    if [ -f "$file" ]; then
        if ! (grep '<title>' "$file" | grep -q '영수증' && grep 'description' "$file" | grep -q '영수증'); then
            echo "❌ $file"
            ((missing++))
        fi
    fi
done

echo ""
echo "=== 资源页 ==="
for file in resources.html en/resources.html ja/resources.html kr/resources.html; do
    if [ -f "$file" ]; then
        lang="zh"
        [[ "$file" == "en/"* ]] && lang="en"
        [[ "$file" == "ja/"* ]] && lang="ja"
        [[ "$file" == "kr/"* ]] && lang="kr"
        
        case "$lang" in
            zh)
                if ! (grep '<title>' "$file" | grep -q '收據' && grep 'description' "$file" | grep -q '收據'); then
                    echo "❌ $file"
                    ((missing++))
                fi
                ;;
            en)
                if ! (grep '<title>' "$file" | grep -qi 'receipt' && grep 'description' "$file" | grep -qi 'receipt'); then
                    echo "❌ $file"
                    ((missing++))
                fi
                ;;
            ja)
                if ! (grep '<title>' "$file" | grep -q '領収書' && grep 'description' "$file" | grep -q '領収書'); then
                    echo "❌ $file"
                    ((missing++))
                fi
                ;;
            kr)
                if ! (grep '<title>' "$file" | grep -q '영수증' && grep 'description' "$file" | grep -q '영수증'); then
                    echo "❌ $file"
                    ((missing++))
                fi
                ;;
        esac
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "总计缺少：$missing 个文件"
echo "════════════════════════════════════════════════════════════════════"

