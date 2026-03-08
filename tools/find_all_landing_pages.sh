#!/bin/bash

echo "【查找所有Landing Page】"
echo ""

echo "1. 功能页面（index.html等）:"
ls -1 index.html features.html dashboard.html 2>/dev/null | wc -l | tr -d ' '

echo ""
echo "2. 学习中心/资源页面:"
ls -1 resources.html blog/index.html en/blog/index.html ja/blog/index.html kr/blog/index.html 2>/dev/null | wc -l | tr -d ' '

echo ""
echo "3. Solutions页面（4个语言版本）:"
find solutions en/solutions ja/solutions kr/solutions -name "index.html" 2>/dev/null | wc -l | tr -d ' '

echo ""
echo "4. 银行页面（已完成）:"
ls -1 *-bank-statement.html en/*-bank-statement.html ja/*-bank-statement.html kr/*-bank-statement.html 2>/dev/null | wc -l | tr -d ' '

echo ""
echo "5. Blog文章页面:"
find blog en/blog ja/blog kr/blog -name "*.html" -not -name "index.html" 2>/dev/null | wc -l | tr -d ' '

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "总计需要处理的页面"
echo "════════════════════════════════════════════════════════════════════"

total=0
count1=$(ls -1 index.html 2>/dev/null | wc -l | tr -d ' ')
count2=$(ls -1 resources.html en/resources.html ja/resources.html kr/resources.html 2>/dev/null | wc -l | tr -d ' ')
count3=$(find solutions en/solutions ja/solutions kr/solutions -name "index.html" 2>/dev/null | wc -l | tr -d ' ')
count4=$(ls -1 *-bank-statement.html en/*-bank-statement.html ja/*-bank-statement.html kr/*-bank-statement.html 2>/dev/null | wc -l | tr -d ' ')
count5=$(find blog en/blog ja/blog kr/blog -name "*.html" 2>/dev/null | wc -l | tr -d ' ')

total=$((count1 + count2 + count3 + count4 + count5))

echo "主页（index.html等）:     $count1"
echo "资源页（resources.html）:  $count2"
echo "Solutions页面:            $count3"
echo "银行页面（已完成）:        $count4"
echo "Blog页面:                 $count5"
echo "----------------------------------------"
echo "总计:                     $total"

