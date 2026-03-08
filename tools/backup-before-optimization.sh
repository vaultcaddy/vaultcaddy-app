#!/bin/bash

# 备份脚本 - 优化前完整备份
# 作用: 在进行代码优化前创建完整备份
# 日期: 2026-01-23

# 配置
PROJECT_DIR="/Users/cavlinyeung/ai-bank-parser"
BACKUP_DIR="/Users/cavlinyeung/ai-bank-parser-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_before_optimization_${TIMESTAMP}"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      📦 VaultCaddy 优化前备份脚本                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"
echo -e "${YELLOW}📁 备份目录: $BACKUP_DIR${NC}"
echo ""

# 检查项目目录
if [ ! -d "$PROJECT_DIR" ]; then
  echo -e "${RED}❌ 错误: 项目目录不存在${NC}"
  exit 1
fi

cd "$PROJECT_DIR"

# 显示将要备份的文件
echo -e "${BLUE}📋 将要备份的文件:${NC}"
echo "  • 主要 HTML 文件 (billing, account, dashboard, firstproject)"
echo "  • 多语言版本 (en/, jp/, kr/)"
echo "  • 所有 JavaScript 文件 (*.js)"
echo "  • 所有 CSS 文件 (*.css)"
echo ""

# 创建备份
echo -e "${YELLOW}📦 正在创建备份...${NC}"
tar -czf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" \
  billing.html \
  account.html \
  dashboard.html \
  firstproject.html \
  index.html \
  en/ \
  jp/ \
  kr/ \
  *.js \
  *.css \
  --exclude="node_modules" \
  --exclude=".git" \
  --exclude="*.bak" \
  2>/dev/null

# 验证备份
if [ -f "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" ]; then
  SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)
  echo -e "${GREEN}✅ 备份完成!${NC}"
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}📦 备份文件: ${BACKUP_NAME}.tar.gz${NC}"
  echo -e "${GREEN}📊 备份大小: ${SIZE}${NC}"
  echo -e "${GREEN}📁 保存位置: ${BACKUP_DIR}${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
else
  echo -e "${RED}❌ 备份失败${NC}"
  exit 1
fi

# 创建备份清单
echo ""
echo -e "${YELLOW}📋 创建备份清单...${NC}"
cat > "$BACKUP_DIR/${BACKUP_NAME}_manifest.txt" << EOF
═══════════════════════════════════════════════════════════
  VaultCaddy 优化前备份清单
═══════════════════════════════════════════════════════════

备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份文件: ${BACKUP_NAME}.tar.gz
备份大小: ${SIZE}

备份内容:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

主要 HTML 文件:
  • billing.html
  • account.html
  • dashboard.html
  • firstproject.html
  • index.html

多语言版本:
  • en/ (英文)
  • jp/ (日文)
  • kr/ (韩文)

JavaScript 文件:
  • 所有 .js 文件

CSS 文件:
  • 所有 .css 文件

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

文件列表:
$(tar -tzf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | head -50)
$([ $(tar -tzf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | wc -l) -gt 50 ] && echo "... 还有 $(($(tar -tzf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | wc -l) - 50)) 个文件")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

恢复方法:
cd $PROJECT_DIR
tar -xzf $BACKUP_DIR/${BACKUP_NAME}.tar.gz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

echo -e "${GREEN}✅ 备份清单已创建${NC}"
echo ""

# 显示备份列表
echo -e "${BLUE}📦 当前所有备份:${NC}"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
echo ""

# 成功提示
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ 备份完成！可以安全地开始优化了                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"
echo "  • 备份文件已保存到: $BACKUP_DIR"
echo "  • 备份清单: ${BACKUP_NAME}_manifest.txt"
echo "  • 恢复命令: tar -xzf $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
echo ""
echo -e "${BLUE}📚 下一步:${NC}"
echo "  1. 查看实施计划: 🚀_阶段1-3优化实施计划_2026-01-23.md"
echo "  2. 开始阶段 1 优化"
echo "  3. 测试验证"
echo ""

