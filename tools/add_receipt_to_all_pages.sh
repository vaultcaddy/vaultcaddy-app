#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         🔧 为所有Landing Page添加收据关键词                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

updated_title=0
updated_desc=0
updated_kw=0
total_files=0

# 函数：处理单个HTML文件
process_file() {
    local file="$1"
    local lang="$2"  # zh/en/ja/kr
    
    if [ ! -f "$file" ]; then
        return
    fi
    
    ((total_files++))
    local modified=0
    
    # 备份
    cp "$file" "${file}.backup_receipt_all"
    
    # 根据语言添加Title关键词
    case "$lang" in
        zh)
            # 中文：对账单 -> 对账单及收据
            if grep -q '<title>.*AI.*處理' "$file" && ! grep -q '<title>.*收據' "$file"; then
                if grep -q 'title>.*對帳單.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*\)對帳單\(.*AI.*<\/title>\)/<title>\1對帳單及收據\2/g' "$file"
                    ((updated_title++))
                    modified=1
                elif grep -q 'title>.*银行.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*银行[^<]*\)\(AI.*<\/title>\)/<title>\1及收據\2/g' "$file"
                    ((updated_title++))
                    modified=1
                fi
            fi
            
            # Description
            if grep -q 'meta name="description".*AI' "$file" && ! grep -q 'description".*收據' "$file"; then
                if grep -q 'description".*對帳單' "$file"; then
                    sed -i '' 's/\(<meta name="description" content="[^"]*\)對帳單\([^"]*"\)/\1對帳單及收據\2/g' "$file"
                    ((updated_desc++))
                    modified=1
                fi
            fi
            
            # Keywords
            if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*收據' "$file"; then
                sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,收據處理,收據AI,發票處理"/g' "$file"
                ((updated_kw++))
                modified=1
            fi
            ;;
            
        en)
            # 英文：添加Receipt
            if grep -q '<title>.*AI' "$file" && ! grep -q '<title>.*Receipt' "$file"; then
                if grep -q 'title>.*Statement.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*\)Statement\(.*AI.*<\/title>\)/<title>\1Statement \& Receipt\2/g' "$file"
                    ((updated_title++))
                    modified=1
                elif grep -q 'title>.*Bank.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*Bank[^<]*\)\(AI.*<\/title>\)/<title>\1\& Receipt \2/g' "$file"
                    ((updated_title++))
                    modified=1
                fi
            fi
            
            # Description
            if grep -q 'meta name="description".*AI' "$file" && ! grep -q 'description".*receipt' "$file"; then
                sed -i '' 's/\(<meta name="description" content="[^"]*\)bank statement\([^"]*"\)/\1bank statement and receipt\2/gi' "$file"
                ((updated_desc++))
                modified=1
            fi
            
            # Keywords
            if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*receipt' "$file"; then
                sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,receipt processing,invoice AI,receipt automation"/g' "$file"
                ((updated_kw++))
                modified=1
            fi
            ;;
            
        ja)
            # 日文：明細 -> 明細・領収書
            if grep -q '<title>.*AI' "$file" && ! grep -q '<title>.*領収書' "$file"; then
                if grep -q 'title>.*明細.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*\)明細\(.*AI.*<\/title>\)/<title>\1明細・領収書\2/g' "$file"
                    ((updated_title++))
                    modified=1
                fi
            fi
            
            # Description
            if grep -q 'meta name="description".*AI' "$file" && ! grep -q 'description".*領収書' "$file"; then
                sed -i '' 's/\(<meta name="description" content="[^"]*\)明細\([^"]*AI[^"]*"\)/\1明細と領収書\2/g' "$file"
                ((updated_desc++))
                modified=1
            fi
            
            # Keywords
            if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*領収書' "$file"; then
                sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,領収書処理,レシート処理,請求書AI"/g' "$file"
                ((updated_kw++))
                modified=1
            fi
            ;;
            
        kr)
            # 韩文：명세서 -> 명세서 및 영수증
            if grep -q '<title>.*AI' "$file" && ! grep -q '<title>.*영수증' "$file"; then
                if grep -q 'title>.*명세서.*AI' "$file"; then
                    sed -i '' 's/<title>\(.*\)명세서\(.*AI.*<\/title>\)/<title>\1명세서 및 영수증\2/g' "$file"
                    ((updated_title++))
                    modified=1
                fi
            fi
            
            # Description
            if grep -q 'meta name="description".*AI' "$file" && ! grep -q 'description".*영수증' "$file"; then
                sed -i '' 's/\(<meta name="description" content="[^"]*\)명세서\([^"]*AI[^"]*"\)/\1명세서 및 영수증\2/g' "$file"
                ((updated_desc++))
                modified=1
            fi
            
            # Keywords
            if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*영수증' "$file"; then
                sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,영수증 처리,영수증 AI,송장 처리"/g' "$file"
                ((updated_kw++))
                modified=1
            fi
            ;;
    esac
    
    if [ $modified -eq 1 ]; then
        echo "  ✅ $file"
    fi
}

# ========== 处理各类型页面 ==========

echo "【1. 处理主页】"
process_file "index.html" "zh"
process_file "en/index.html" "en"
process_file "ja/index.html" "ja"
process_file "kr/index.html" "kr"

echo ""
echo "【2. 处理资源页】"
process_file "resources.html" "zh"
process_file "en/resources.html" "en"
process_file "ja/resources.html" "ja"
process_file "kr/resources.html" "kr"

echo ""
echo "【3. 处理Solutions页面】"
for file in solutions/*/index.html; do
    if [ -f "$file" ]; then
        process_file "$file" "zh"
    fi
done

for file in en/solutions/*/index.html; do
    if [ -f "$file" ]; then
        process_file "$file" "en"
    fi
done

for file in ja/solutions/*/index.html; do
    if [ -f "$file" ]; then
        process_file "$file" "ja"
    fi
done

for file in kr/solutions/*/index.html; do
    if [ -f "$file" ]; then
        process_file "$file" "kr"
    fi
done

echo ""
echo "【4. 处理Blog页面】"
for file in blog/**/*.html; do
    if [ -f "$file" ]; then
        process_file "$file" "zh"
    fi
done

for file in en/blog/**/*.html; do
    if [ -f "$file" ]; then
        process_file "$file" "en"
    fi
done

for file in ja/blog/**/*.html; do
    if [ -f "$file" ]; then
        process_file "$file" "ja"
    fi
done

for file in kr/blog/**/*.html; do
    if [ -f "$file" ]; then
        process_file "$file" "kr"
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "📊 处理统计"
echo "════════════════════════════════════════════════════════════════════"
echo "扫描文件：        $total_files 个"
echo "✅ Title更新：    $updated_title 个"
echo "✅ Description更新：$updated_desc 个"
echo "✅ Keywords更新： $updated_kw 个"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "🎉 所有Landing Page收据关键词添加完成！"
echo "════════════════════════════════════════════════════════════════════"

