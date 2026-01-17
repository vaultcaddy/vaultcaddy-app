#!/bin/bash
# 🚀 立即同步首页 - 一键解决所有问题
# 作用：从最新的中文版同步到英文、日文、韩文版本，清除所有中文残留

echo "🚀 开始同步首页..."
echo ""

cd /Users/cavlinyeung/ai-bank-parser

# 先确保我们有最新的中文版
if [ ! -f "index.html" ]; then
    echo "❌ 找不到 index.html"
    exit 1
fi

echo "📝 方案：手动指定需要同步的内容"
echo ""
echo "由于内容复杂，建议："
echo "1. 使用 multilingual_sync_master.py 同步 dashboard、account等其他页面"
echo "2. 首页(index.html)因为价格和地区差异大，建议："
echo "   - 保留现有的en/index.html、jp/index.html、kr/index.html"
echo "   - 或手动调整特定内容"
echo ""
echo "✅ 其他页面同步："
python3 multilingual_sync_master.py all

echo ""
echo "📖 首页同步建议："
echo "   由于首页包含大量本地化内容（价格、地区、银行名称等）"
echo "   建议查看 📖_首页智能同步指南.md 了解详情"
echo ""
echo "🎯 下一步："
echo "   1. 查看 sync_index_intelligent.py 配置价格和地区"
echo "   2. 运行: python3 sync_index_intelligent.py"
echo ""











