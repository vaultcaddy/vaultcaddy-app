#!/bin/bash

# Chrome MCP 快速啟動腳本
# 用途: 啟動 Chrome 並啟用遠端調試，然後啟動 MCP 伺服器

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Chrome MCP 啟動腳本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 檢查 Node.js 版本
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "❌ 錯誤: Node.js 版本需要 22 或更高"
    echo "   當前版本: $(node --version)"
    echo "   請升級 Node.js: https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js 版本檢查通過: $(node --version)"

# 檢查 Chrome 是否已安裝
if [ ! -d "/Applications/Google Chrome.app" ]; then
    echo "❌ 錯誤: 找不到 Google Chrome"
    echo "   請確保 Chrome 已安裝在 /Applications/Google Chrome.app"
    exit 1
fi
echo "✅ Chrome 已找到"

# 檢查端口 12306 是否被佔用
if lsof -Pi :12306 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  警告: 端口 12306 已被使用"
    echo "   正在嘗試關閉現有進程..."
    lsof -ti :12306 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 檢查端口 9222 (Chrome 遠端調試) 是否被佔用
if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  警告: Chrome 遠端調試端口 9222 已被使用"
    echo "   這可能表示 Chrome 已經在調試模式下運行"
else
    echo "🔧 啟動 Chrome 並啟用遠端調試..."
    
    # 關閉所有 Chrome 實例（可選，取消註釋以啟用）
    # killall "Google Chrome" 2>/dev/null
    # sleep 1
    
    # 啟動 Chrome 並啟用遠端調試
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
        --remote-debugging-port=9222 \
        --user-data-dir=/tmp/chrome-debug \
        > /dev/null 2>&1 &
    
    CHROME_PID=$!
    echo "✅ Chrome 已啟動 (PID: $CHROME_PID)"
    echo "   遠端調試端口: 9222"
    sleep 3
fi

# 檢查 Chrome 遠端調試是否可用
if curl -s http://localhost:9222/json >/dev/null 2>&1; then
    echo "✅ Chrome 遠端調試已啟用"
else
    echo "⚠️  警告: 無法連接到 Chrome 遠端調試"
    echo "   請手動訪問 chrome://inspect/#remote-debugging 啟用"
fi

# 啟動 MCP 伺服器
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 啟動 Chrome MCP 伺服器..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 提示:"
echo "   - MCP 伺服器將運行在 http://127.0.0.1:12306/mcp"
echo "   - 保持此終端窗口打開"
echo "   - 按 Ctrl+C 停止伺服器"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 啟動 MCP 伺服器
npx -y @modelcontextprotocol/server-chrome-devtools --port 12306
