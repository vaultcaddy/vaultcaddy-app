# Chrome MCP 修復指南

## 🔍 問題診斷

根據檢查，您的 Chrome MCP 伺服器目前**沒有運行**。以下是問題和解決方案：

### 當前狀態
- ✅ Node.js 版本: v23.11.0 (符合要求，需要 22+)
- ✅ Chrome 版本: 144.0.7559.133 (符合要求，需要 M144+)
- ❌ Chrome MCP 伺服器: **未運行** (端口 12306 未被使用)
- ⚠️ 配置: 已配置但伺服器未啟動

---

## 🛠️ 解決步驟

### 步驟 1: 啟用 Chrome 遠端調試

1. **打開 Chrome 瀏覽器**
2. **訪問**: `chrome://inspect/#remote-debugging`
3. **啟用遠端調試**:
   - 找到 "Discover network targets" 選項
   - 確保已啟用
   - 或者點擊 "Open dedicated DevTools for Node"

### 步驟 2: 安裝 Chrome MCP 伺服器

根據您的配置，Chrome MCP 伺服器應該運行在 `http://127.0.0.1:12306/mcp`

**選項 A: 使用官方 Chrome DevTools MCP Server**

```bash
# 安裝 Chrome DevTools MCP Server
npm install -g @modelcontextprotocol/server-chrome-devtools

# 或者使用 npx 直接運行
npx @modelcontextprotocol/server-chrome-devtools
```

**選項 B: 使用本地安裝**

```bash
# 在項目目錄中安裝
npm install @modelcontextprotocol/server-chrome-devtools

# 運行伺服器
npx @modelcontextprotocol/server-chrome-devtools --port 12306
```

### 步驟 3: 更新 MCP 配置

如果使用官方伺服器，您可能需要更新 `/Users/cavlinyeung/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-chrome-devtools"
      ],
      "env": {
        "CHROME_REMOTE_DEBUGGING_PORT": "9222"
      }
    }
  }
}
```

或者如果使用 HTTP 模式（當前配置）：

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:12306/mcp"
    }
  }
}
```

### 步驟 4: 啟動 Chrome 並啟用遠端調試

**方法 1: 通過命令行啟動 Chrome（推薦）**

```bash
# 關閉所有 Chrome 實例
killall "Google Chrome" 2>/dev/null

# 使用遠端調試端口啟動 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug
```

**方法 2: 通過 Chrome 設置啟用**

1. 打開 Chrome
2. 訪問 `chrome://inspect/#remote-debugging`
3. 確保 "Discover network targets" 已啟用

### 步驟 5: 啟動 MCP 伺服器

```bash
# 如果使用 npx
npx @modelcontextprotocol/server-chrome-devtools --port 12306

# 或者如果已全局安裝
chrome-devtools-mcp-server --port 12306
```

### 步驟 6: 驗證連接

在終端中測試：

```bash
# 檢查端口是否在監聽
lsof -i :12306

# 測試 HTTP 連接
curl http://127.0.0.1:12306/mcp
```

---

## 🔧 常見問題排查

### 問題 1: "connection closed" 錯誤

**解決方案**:
- 確保 Chrome 已啟用遠端調試
- 檢查防火牆是否阻止了端口 12306
- 確認 Node.js 版本 >= 22

### 問題 2: 伺服器無法啟動

**解決方案**:
```bash
# 檢查端口是否被佔用
lsof -i :12306

# 如果被佔用，殺死進程或使用其他端口
kill -9 <PID>
```

### 問題 3: Chrome 遠端調試未啟用

**解決方案**:
1. 確保使用 Chrome M144 或更高版本
2. 通過命令行啟動 Chrome 並指定 `--remote-debugging-port=9222`
3. 或訪問 `chrome://inspect/#remote-debugging` 手動啟用

### 問題 4: MCP 配置錯誤

**檢查配置檔案**:
```bash
cat ~/.cursor/mcp.json
```

確保配置格式正確，特別是：
- `type: "streamable-http"` 用於 HTTP 模式
- `url` 必須正確指向伺服器地址
- 如果使用 command 模式，確保路徑正確

---

## 📝 快速修復腳本

創建一個啟動腳本 `start-chrome-mcp.sh`:

```bash
#!/bin/bash

# 關閉現有 Chrome 實例
killall "Google Chrome" 2>/dev/null

# 啟動 Chrome 並啟用遠端調試
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug \
  > /dev/null 2>&1 &

# 等待 Chrome 啟動
sleep 3

# 啟動 MCP 伺服器
echo "🚀 啟動 Chrome MCP 伺服器..."
npx -y @modelcontextprotocol/server-chrome-devtools --port 12306
```

使用方式：
```bash
chmod +x start-chrome-mcp.sh
./start-chrome-mcp.sh
```

---

## ✅ 驗證清單

完成以下步驟後，Chrome MCP 應該可以正常工作：

- [ ] Chrome 版本 >= M144
- [ ] Node.js 版本 >= 22
- [ ] Chrome 遠端調試已啟用
- [ ] MCP 伺服器正在運行（端口 12306）
- [ ] MCP 配置檔案正確
- [ ] Cursor 已重啟以載入新配置

---

## 🔗 參考資源

- [Chrome DevTools MCP 官方文檔](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- [Model Context Protocol 文檔](https://modelcontextprotocol.io/)
- [Chrome 遠端調試指南](https://developer.chrome.com/docs/devtools/remote-debugging/)

---

## 💡 提示

1. **保持 Chrome 運行**: MCP 伺服器需要 Chrome 保持運行狀態
2. **使用專用用戶資料**: 使用 `--user-data-dir` 可以避免影響正常瀏覽
3. **檢查日誌**: 如果仍有問題，檢查 Cursor 的 MCP 日誌
4. **重啟 Cursor**: 修改配置後記得重啟 Cursor

---

**最後更新**: 2026-02-11
