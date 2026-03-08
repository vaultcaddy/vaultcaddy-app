#!/bin/bash

# 一次性优化脚本 - 阶段 1-2
# 作用: 自动化应用所有优化到 16 个 HTML 文件
# 日期: 2026-01-23
# 注意: 阶段 3（多语言统一）需要单独处理

PROJECT_DIR="/Users/cavlinyeung/ai-bank-parser"
cd "$PROJECT_DIR"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🚀 阶段 1-2 自动化优化脚本                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# 文件列表
FILES=(
    "billing.html"
    "account.html"
    "dashboard.html"
    "firstproject.html"
    "en/billing.html"
    "en/account.html"
    "en/dashboard.html"
    "en/firstproject.html"
    "jp/billing.html"
    "jp/account.html"
    "jp/dashboard.html"
    "jp/firstproject.html"
    "kr/billing.html"
    "kr/account.html"
    "kr/dashboard.html"
    "kr/firstproject.html"
)

echo -e "${YELLOW}📋 将要优化 ${#FILES[@]} 个文件${NC}"
echo ""

# 步骤 1: 添加新的文件引用
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}步骤 1: 添加新的 JS 和 CSS 文件引用${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  处理: ${file}"
        
        # 确定路径前缀（根据文件位置）
        if [[ $file == en/* ]] || [[ $file == jp/* ]] || [[ $file == kr/* ]]; then
            PREFIX="../"
        else
            PREFIX=""
        fi
        
        # 检查是否已经添加过
        if grep -q "user-menu-manager.js" "$file"; then
            echo -e "    ${GREEN}✓${NC} 已包含新文件引用"
        else
            # 在 font-awesome 后添加新文件
            sed -i.opt-bak "/<link href=\"https:\/\/cdnjs.cloudflare.com\/ajax\/libs\/font-awesome/a\\
    \\
    <!-- 优化后的公共组件 (2026-01-23) -->\\
    <link rel=\"stylesheet\" href=\"${PREFIX}user-menu-styles.css\">\\
    <script defer src=\"${PREFIX}logger.js\"></script>\\
    <script defer src=\"${PREFIX}init-manager.js\"></script>\\
    <script defer src=\"${PREFIX}user-menu-manager.js\"></script>\\
    <script defer src=\"${PREFIX}mobile-menu-manager.js\"></script>
" "$file"
            echo -e "    ${GREEN}✓${NC} 已添加新文件引用"
        fi
    fi
done

echo ""
echo -e "${GREEN}✅ 步骤 1 完成${NC}"
echo ""

# 步骤 2: 替换 console.log 为 logger.log
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}步骤 2: 替换 console.log 为 logger.log${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  处理: ${file}"
        
        # 计算替换次数
        count=$(grep -c "console\.log(" "$file" 2>/dev/null || echo "0")
        
        # 替换
        sed -i.console-bak \
            -e 's/console\.log(/logger.log(/g' \
            -e 's/console\.warn(/logger.warn(/g' \
            -e 's/console\.info(/logger.info(/g' \
            "$file"
        
        echo -e "    ${GREEN}✓${NC} 替换了 ${count} 个 console.log"
    fi
done

echo ""
echo -e "${GREEN}✅ 步骤 2 完成${NC}"
echo ""

# 步骤 3: 替换内联样式为 CSS 类
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}步骤 3: 替换用户菜单的内联样式为 CSS 类${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  处理: ${file}"
        
        # 替换用户头像的内联样式
        sed -i.style-bak \
            -e 's/<div onclick="toggleDropdown()" style="cursor: pointer; padding: 0\.5rem; border-radius: 8px; transition: background 0\.2s;" onmouseover="this\.style\.background=.*" onmouseout="this\.style\.background=.*">/<div onclick="toggleDropdown()" class="user-menu-trigger">/g' \
            -e 's/<div style="width: 32px; height: 32px; border-radius: 50%; background: #667eea; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0\.875rem; opacity: 1; transition: opacity 0\.3s;">/<div class="user-avatar">/g' \
            -e 's/<button onclick="window\.location\.href=.*auth\.html.*" style="padding: 0\.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0\.2s; font-size: 0\.875rem;" onmouseover="this\.style\.background=.*" onmouseout="this\.style\.background=.*">/<button onclick="window.location.href='"'"'auth.html'"'"'" class="login-button">/g' \
            "$file"
        
        echo -e "    ${GREEN}✓${NC} 已替换内联样式为 CSS 类"
    fi
done

echo ""
echo -e "${GREEN}✅ 步骤 3 完成${NC}"
echo ""

# 清理备份文件
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}清理临时备份文件${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

rm -f *.opt-bak *.console-bak *.style-bak
rm -f en/*.opt-bak en/*.console-bak en/*.style-bak
rm -f jp/*.opt-bak jp/*.console-bak jp/*.style-bak
rm -f kr/*.opt-bak kr/*.console-bak kr/*.style-bak

echo -e "${GREEN}✅ 临时文件已清理${NC}"
echo ""

# 验证
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}验证优化结果${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "检查新文件是否添加..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "user-menu-manager.js" "$file"; then
            echo -e "  ${GREEN}✓${NC} $file"
        else
            echo -e "  ${RED}✗${NC} $file"
        fi
    fi
done

echo ""
echo "检查 logger.log 替换..."
count=$(grep -c "logger\.log(" billing.html 2>/dev/null || echo "0")
echo -e "  billing.html: ${GREEN}${count}${NC} 个 logger.log"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ 阶段 1-2 自动化优化完成！                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📋 下一步:${NC}"
echo "  1. 手动检查 billing.html 是否正常"
echo "  2. 测试所有功能"
echo "  3. 如果有问题，使用备份恢复"
echo ""

