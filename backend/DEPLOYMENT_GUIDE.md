# Bank Statement Extractor 部署指南

## 📋 系统要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB以上（推荐8GB）
- **硬盘**: 10GB可用空间
- **GPU**: 可选（有GPU可提速3-5倍）

### 软件要求
- **Python**: 3.9 或更高版本
- **系统**:
  - macOS 10.15+
  - Ubuntu 20.04+
  - Windows 10+

---

## 🚀 快速部署（5分钟）

### 1. 安装系统依赖

#### macOS
```bash
brew install poppler
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

#### Windows
1. 下载 [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. 解压到 `C:\Program Files\poppler`
3. 添加 `C:\Program Files\poppler\Library\bin` 到系统PATH

---

### 2. 创建Python虚拟环境

```bash
cd /Users/cavlinyeung/ai-bank-parser/backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

---

### 3. 安装Python依赖

```bash
pip install --upgrade pip

# 安装所有依赖
pip install -r requirements.txt

# ⚠️ 如果有GPU（NVIDIA显卡），替换为GPU版本：
# pip uninstall paddlepaddle
# pip install paddlepaddle-gpu==2.6.0
```

**预计安装时间：** 5-10分钟（取决于网络速度）

---

### 4. 验证安装

```bash
python -c "from paddleocr import PPStructure; print('✅ PaddleOCR安装成功')"
python -c "from pdf2image import convert_from_path; print('✅ pdf2image安装成功')"
python -c "import yaml; print('✅ PyYAML安装成功')"
```

如果都显示 ✅，说明安装成功！

---

### 5. 启动API服务

```bash
python bank_statement_extractor.py
```

**启动成功后，您会看到：**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✅ 已加载 3 个银行配置
  ✅ zh_hangseng: 恒生银行
  ✅ zh_icbc: 中国工商银行
  ✅ en_hsbc: HSBC
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 测试API

### 1. 健康检查

```bash
curl http://localhost:8000/health
```

**预期输出：**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "configs_loaded": 3
}
```

---

### 2. 获取支持的银行列表

```bash
curl http://localhost:8000/api/banks
```

**预期输出：**
```json
{
  "banks": [
    {
      "key": "zh_hangseng",
      "name": "恒生银行",
      "language": "zh",
      "region": "HK",
      "currency": "HKD"
    },
    ...
  ],
  "total": 3
}
```

---

### 3. 提取银行对账单

```bash
curl -X POST http://localhost:8000/api/extract \
  -F "file=@/path/to/statement.pdf" \
  -F "bank_key=zh_hangseng"
```

**预期输出：**
```json
{
  "bankName": "恒生银行",
  "accountNumber": "AUTO_DETECT_LATER",
  "accountHolder": "AUTO_DETECT_LATER",
  "currency": "HKD",
  "statementPeriod": "10 Mar to 22 Mar",
  "openingBalance": 30718.39,
  "closingBalance": 30018.39,
  "transactions": [
    {
      "date": "10 Mar",
      "description": "ATM WITHDRAWAL",
      "debit": 500.00,
      "credit": 0,
      "balance": 30218.39
    },
    {
      "date": "10 Mar",
      "description": "POS PURCHASE",
      "debit": 200.00,
      "credit": 0,
      "balance": 30018.39,
      "_date_filled": true
    }
  ],
  "_extractionMethod": "paddleocr",
  "_bankConfig": "zh_hangseng"
}
```

✅ **注意 `_date_filled: true`** - 表示日期是自动填充的（同日多笔交易）

---

## 🔗 前端集成

### 1. 引入客户端SDK

```html
<!-- 在 firstproject.html 中引入 -->
<script src="backend-api-client.js"></script>
```

---

### 2. 修改文件上传逻辑

```javascript
// 在 firstproject.html 中
async function uploadFileDirect(file, pages, documentType) {
    try {
        // ✅ 调用Python后端
        const backendClient = new BackendAPIClient('http://localhost:8000');
        
        // 检查后端是否健康
        const health = await backendClient.healthCheck();
        if (health.status !== 'healthy') {
            throw new Error('后端服务不可用');
        }
        
        // 提取数据
        const result = await backendClient.extract(file);
        
        // 使用提取的数据
        const extractedData = result.extractedData;
        
        // ... 后续处理逻辑保持不变
        
    } catch (error) {
        console.error('后端提取失败，fallback到AI:', error);
        
        // ⚠️ Fallback: 如果后端失败，使用 Qwen-VL-Max
        const qwenProcessor = new QwenVLMaxProcessor();
        const result = await qwenProcessor.processDocument(file, documentType);
        
        // ... 使用AI结果
    }
}
```

---

## 📊 性能优化

### 1. 启用GPU加速（推荐）

如果您有NVIDIA显卡：

```bash
# 卸载CPU版本
pip uninstall paddlepaddle

# 安装GPU版本
pip install paddlepaddle-gpu==2.6.0

# 修改 bank_statement_extractor.py
# 将 use_gpu=False 改为 use_gpu=True
```

**提速效果：** 3-8秒/页 → **1-3秒/页**

---

### 2. 多进程部署

```bash
# 使用 gunicorn（生产级WSGI服务器）
pip install gunicorn

# 启动4个worker进程
gunicorn bank_statement_extractor:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

### 3. 反向代理（Nginx）

```nginx
# /etc/nginx/sites-available/bank-api
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.vaultcaddy.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;  # PDF处理可能需要较长时间
    }
}
```

---

## 🔐 生产环境配置

### 1. 环境变量

创建 `.env` 文件：

```bash
# .env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://vaultcaddy.com
LOG_LEVEL=INFO
GPU_ENABLED=False
CONFIG_DIR=bank_configs
```

---

### 2. 系统服务（systemd）

创建 `/etc/systemd/system/bank-api.service`:

```ini
[Unit]
Description=Bank Statement Extractor API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bank_statement_extractor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable bank-api
sudo systemctl start bank-api
sudo systemctl status bank-api
```

---

## 🐛 故障排查

### 问题1: `ModuleNotFoundError: No module named 'paddleocr'`
**解决：** 确认已激活虚拟环境
```bash
source venv/bin/activate
pip list | grep paddle
```

---

### 问题2: `PDFInfoNotInstalledError`
**解决：** 安装poppler
```bash
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

---

### 问题3: 提取速度慢（>10秒/页）
**解决：**
- 方案1: 启用GPU加速
- 方案2: 降低PDF分辨率（300 DPI → 200 DPI）
- 方案3: 使用多进程部署

---

## 📈 监控与日志

### 1. 查看日志

```bash
# 实时查看日志
tail -f /var/log/bank-api.log

# 搜索错误
grep "ERROR" /var/log/bank-api.log
```

---

### 2. 性能监控

```bash
# 安装监控工具
pip install prometheus-client

# 添加到 bank_statement_extractor.py
from prometheus_client import Counter, Histogram
from prometheus_client import start_http_server

request_count = Counter('requests_total', 'Total requests')
processing_time = Histogram('processing_seconds', 'Processing time')
```

---

## 📝 下一步

1. ✅ 部署Python后端
2. ✅ 测试API接口
3. 🔄 集成到前端（修改 `firstproject.html`）
4. 🧪 测试恒生银行对账单（验证准确率）
5. 📊 监控性能和错误率
6. 🚀 如果成功，逐步替换 Qwen-VL-Max

---

## 🆘 获取帮助

- **文档**: `ARCHITECTURE_COMPARISON_AND_MIGRATION.md`
- **配置**: `bank_configs/` 目录
- **日志**: 检查控制台输出

**最后更新:** 2026-02-02

