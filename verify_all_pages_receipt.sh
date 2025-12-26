#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         🔍 验证所有页面的收据关键词                            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

check_file() {
    local file="$1"
    local lang="$2"
    
    if [ ! -f "$file" ]; then
        return 1
    fi
    
    local has_receipt=0
    
    case "$lang" in
        zh)
            if grep '<title>' "$file" | grep -q '收據' && \
               grep 'description' "$file" | grep -q '收據'; then
                has_receipt=1
            fi
            ;;
        en)
            if grep '<title>' "$file" | grep -qi 'receipt' && \
               grep 'description' "$file" | grep -qi 'receipt'; then
                has_receipt=1
            fi
            ;;
        ja)
            if grep '<title>' "$file" | grep -q '領収書' && \
               grep 'description' "$file" | grep -q '領収書'; then
                has_receipt=1
            fi
            ;;
        kr)
            if grep '<title>' "$file" | grep -q '영수증' && \
               grep 'description' "$file" | grep -q '영수증'; then
                has_receipt=1
            fi
            ;;
    esac
    
    return $((1 - has_receipt))
}

# 统计
total=0
ok=0

# 主页
for file in index.html en/index.html kr/index.html; do
    if [ -f "$file" ]; then
        ((total++))
        lang="zh"
        [[ "$file" == "en/"* ]] && lang="en"
        [[ "$file" == "kr/"* ]] && lang="kr"
        
        if check_file "$file" "$lang"; then
            ((ok++))
        fi
    fi
done

# 资源页
for file in resources.html en/resources.html ja/resources.html kr/resources.html; do
    if [ -f "$file" ]; then
        ((total++))
        lang="zh"
        [[ "$file" == "en/"* ]] && lang="en"
        [[ "$file" == "ja/"* ]] && lang="ja"
        [[ "$file" == "kr/"* ]] && lang="kr"
        
        if check_file "$file" "$lang"; then
            ((ok++))
        fi
    fi
done

# 银行页面
bank_total=0
bank_ok=0
for file in *-bank-statement.html en/*-bank-statement.html ja/*-bank-statement.html kr/*-bank-statement.html; do
    if [ -f "$file" ]; then
        ((bank_total++))
        lang="zh"
        [[ "$file" == "en/"* ]] && lang="en"
        [[ "$file" == "ja/"* ]] && lang="ja"
        [[ "$file" == "kr/"* ]] && lang="kr"
        
        if check_file "$file" "$lang"; then
            ((bank_ok++))
        fi
    fi
done

# Solutions页面
sol_total=0
sol_ok=0
for dir in solutions en/solutions ja/solutions kr/solutions; do
    if [ -d "$dir" ]; then
        for file in $dir/*/index.html; do
            if [ -f "$file" ]; then
                ((sol_total++))
                lang="zh"
                [[ "$file" == "en/"* ]] && lang="en"
                [[ "$file" == "ja/"* ]] && lang="ja"
                [[ "$file" == "kr/"* ]] && lang="kr"
                
                if check_file "$file" "$lang"; then
                    ((sol_ok++))
                fi
            fi
        done
    fi
done

echo "════════════════════════════════════════════════════════════════════"
echo "📊 验证结果"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "主页 + 资源页：       $ok/$total ✅"
echo "银行页面：           $bank_ok/$bank_total ✅"
echo "Solutions页面：      $sol_ok/$sol_total ✅"
echo ""
all_total=$((total + bank_total + sol_total))
all_ok=$((ok + bank_ok + sol_ok))
echo "----------------------------------------"
echo "总计：               $all_ok/$all_total ✅"
echo ""

if [ $all_ok -eq $all_total ]; then
    echo "🎉 所有页面都已包含收据关键词！"
else
    missing=$((all_total - all_ok))
    echo "⚠️  还有 $missing 个页面需要处理"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"

