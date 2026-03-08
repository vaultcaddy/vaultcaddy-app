#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         🔧 批量添加收据关键词到所有银行页面                   ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# 统计
updated_title=0
updated_desc=0
updated_kw=0

# ========== 中文版 ==========
echo "【处理中文版】"
for file in *-bank-statement.html; do
    if [ -f "$file" ]; then
        # 备份
        cp "$file" "${file}.backup_batch"
        
        # Title: 对账单 -> 对账单及收据
        if grep -q '<title>.*對帳單.*AI' "$file" && ! grep -q '<title>.*對帳單及收據' "$file"; then
            sed -i '' 's/<title>\(.*\)對帳單\(.*AI.*<\/title>\)/<title>\1對帳單及收據\2/g' "$file"
            echo "  ✅ $file - title"
            ((updated_title++))
        fi
        
        # Description: 对账单 -> 对账单及收据
        if grep -q 'meta name="description".*對帳單' "$file" && ! grep -q 'description".*對帳單及收據' "$file"; then
            sed -i '' 's/\(<meta name="description" content="[^"]*\)對帳單\([^"]*"\)/\1對帳單及收據\2/g' "$file"
            ((updated_desc++))
        fi
        
        # Keywords: 添加收据关键词
        if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*收據' "$file"; then
            sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,銀行收據處理,收據AI處理,發票處理"/g' "$file"
            ((updated_kw++))
        fi
    fi
done

# ========== 英文版 ==========
echo ""
echo "【处理英文版】"
for file in en/*-bank-statement.html; do
    if [ -f "$file" ]; then
        # 备份
        cp "$file" "${file}.backup_batch"
        
        # Title: Statement -> Statement & Receipt
        if grep -q '<title>.*Statement.*AI' "$file" && ! grep -q '<title>.*Statement & Receipt' "$file"; then
            sed -i '' 's/<title>\(.*\)Statement\(.*AI.*<\/title>\)/<title>\1Statement \& Receipt\2/g' "$file"
            echo "  ✅ $file - title"
            ((updated_title++))
        fi
        
        # Description: bank statement -> bank statement and receipt
        if grep -q 'meta name="description".*bank statement' "$file" && ! grep -q 'description".*statement and receipt' "$file"; then
            sed -i '' 's/\(<meta name="description" content="[^"]*\)bank statement\([^"]*"\)/\1bank statement and receipt\2/gi' "$file"
            ((updated_desc++))
        fi
        
        # Keywords: 添加receipt
        if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*receipt' "$file"; then
            sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,receipt processing,invoice processing,bank receipt"/g' "$file"
            ((updated_kw++))
        fi
    fi
done

# ========== 日文版 ==========
echo ""
echo "【处理日文版】"
for file in ja/*-bank-statement.html; do
    if [ -f "$file" ]; then
        # 备份
        cp "$file" "${file}.backup_batch"
        
        # Title: 明細 -> 明細・領収書
        if grep -q '<title>.*明細.*AI' "$file" && ! grep -q '<title>.*明細・領収書' "$file"; then
            sed -i '' 's/<title>\(.*\)明細\(.*AI.*<\/title>\)/<title>\1明細・領収書\2/g' "$file"
            echo "  ✅ $file - title"
            ((updated_title++))
        fi
        
        # Description: 明細 -> 明細と領収書
        if grep -q 'meta name="description".*明細' "$file" && ! grep -q 'description".*明細と領収書' "$file"; then
            sed -i '' 's/\(<meta name="description" content="[^"]*\)明細\([^"]*"\)/\1明細と領収書\2/g' "$file"
            ((updated_desc++))
        fi
        
        # Keywords: 添加領収書
        if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*領収書' "$file"; then
            sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,領収書処理,レシート処理,請求書処理"/g' "$file"
            ((updated_kw++))
        fi
    fi
done

# ========== 韩文版 ==========
echo ""
echo "【处理韩文版】"
for file in kr/*-bank-statement.html; do
    if [ -f "$file" ]; then
        # 备份
        cp "$file" "${file}.backup_batch"
        
        # Title: 명세서 -> 명세서 및 영수증
        if grep -q '<title>.*명세서.*AI' "$file" && ! grep -q '<title>.*명세서 및 영수증' "$file"; then
            sed -i '' 's/<title>\(.*\)명세서\(.*AI.*<\/title>\)/<title>\1명세서 및 영수증\2/g' "$file"
            echo "  ✅ $file - title"
            ((updated_title++))
        fi
        
        # Description: 명세서 -> 명세서 및 영수증
        if grep -q 'meta name="description".*명세서' "$file" && ! grep -q 'description".*명세서 및 영수증' "$file"; then
            sed -i '' 's/\(<meta name="description" content="[^"]*\)명세서\([^"]*"\)/\1명세서 및 영수증\2/g' "$file"
            ((updated_desc++))
        fi
        
        # Keywords: 添加영수증
        if grep -q 'meta name="keywords"' "$file" && ! grep -q 'keywords".*영수증' "$file"; then
            sed -i '' 's/<meta name="keywords" content="\([^"]*\)"/<meta name="keywords" content="\1,영수증 처리,은행 영수증,영수증 AI"/g' "$file"
            ((updated_kw++))
        fi
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "📊 处理统计"
echo "════════════════════════════════════════════════════════════════════"
echo "✅ Title更新：   $updated_title 个文件"
echo "✅ Description更新：$updated_desc 个文件"
echo "✅ Keywords更新： $updated_kw 个文件"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "🎉 批量添加收据关键词完成！"
echo "════════════════════════════════════════════════════════════════════"

