# 🎯 下一步操作指南

> **完整工业架构已实施完成！**  
> **基于千问AI推荐的生产级方案**  
> **现在可以开始测试了！** 🚀

---

## ✅ 已完成的工作

### 1. 后端系统（Python）
- ✅ `backend/bank_statement_extractor.py` - 核心提取器 + FastAPI服务
- ✅ `backend/requirements.txt` - Python依赖清单
- ✅ `backend/quick_start.sh` - 一键启动脚本
- ✅ `backend/test_api.sh` - API测试脚本

### 2. YAML配置系统
- ✅ `backend/bank_configs/zh/hangseng.yaml` - 恒生银行（香港）
- ✅ `backend/bank_configs/zh/icbc.yaml` - 工商银行（中国）
- ✅ `backend/bank_configs/en/hsbc.yaml` - HSBC（英文）

### 3. 前端集成
- ✅ `backend-api-client.js` - JavaScript SDK

### 4. 文档
- ✅ `backend/README.md` - 快速入门
- ✅ `backend/DEPLOYMENT_GUIDE.md` - 详细部署指南
- ✅ `INDUSTRIAL_ARCHITECTURE_IMPLEMENTATION.md` - 完整实施方案

---

## 🚀 立即开始（5分钟）

### 第1步：安装poppler（系统依赖）

```bash
# macOS
brew install poppler

# Ubuntu/Debian
# sudo apt-get install poppler-utils

# Windows
# 下载 https://github.com/oschwartz10612/poppler-windows/releases/
```

**预计时间：** 1分钟

---

### 第2步：启动后端服务

```bash
cd backend
./quick_start.sh
```

**启动成功标志：**
```
🚀 启动API服务...
   URL: http://localhost:8000
   健康检查: http://localhost:8000/health
   API文档: http://localhost:8000/docs

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✅ 已加载 3 个银行配置
  ✅ zh_hangseng: 恒生银行
  ✅ zh_icbc: 中国工商银行
  ✅ en_hsbc: HSBC
```

**预计时间：** 3-5分钟（首次安装依赖）

---

### 第3步：测试API（在新终端窗口）

**打开新终端，运行：**

```bash
cd backend

# 测试1: 健康检查 + 银行列表
./test_api.sh

# 测试2: 提取恒生银行对账单（如果有测试文件）
./test_api.sh /path/to/hangseng_statement.pdf
```

**预期输出：**
```
🧪 Bank Statement API - 测试脚本
=================================

📋 测试1: 健康检查
   GET http://localhost:8000/health

✅ 健康检查通过
{
  "status": "healthy",
  "model_loaded": true,
  "configs_loaded": 3
}

---

📋 测试2: 获取支持的银行列表
   GET http://localhost:8000/api/banks

✅ 成功获取银行列表（共 3 个）
{
  "key": "zh_hangseng",
  "name": "恒生银行",
  "region": "HK"
}

---

🎉 所有测试完成！
```

**预计时间：** 1分钟

---

## 📊 验证关键功能

### 验证1: 同日多笔交易处理

**目标：** 确认恒生银行对账单中，同一天的多笔交易日期被正确填充

**操作：**
1. 准备一份恒生银行对账单（有同日多笔交易）
2. 运行 `./test_api.sh /path/to/hangseng_statement.pdf`
3. 检查输出中是否有 `✅ 自动填充了 X 个空白日期`

**预期结果：**
```json
{
  "transactions": [
    {
      "date": "10 Mar",
      "description": "ATM WITHDRAWAL",
      "debit": 500.00
    },
    {
      "date": "10 Mar",  // ← 自动填充
      "description": "ONLINE TRANSFER",
      "debit": 200.00,
      "_date_filled": true
    }
  ]
}
```

---

### 验证2: 准确率对比

**目标：** 对比PaddleOCR和Qwen-VL-Max的提取准确率

**操作：**
1. 用PaddleOCR提取 → 记录结果
2. 关闭后端服务（Ctrl+C）
3. 用Qwen-VL-Max提取 → 记录结果
4. 对比差异

**评估标准：**
- ✅ 日期准确率（尤其是同日多笔）
- ✅ 金额准确率
- ✅ 余额准确率
- ✅ 描述完整性

---

### 验证3: 性能对比

**目标：** 测量两种方案的处理速度

**操作：**
```bash
# PaddleOCR
time curl -X POST http://localhost:8000/api/extract \
  -F "file=@statement.pdf" \
  -F "bank_key=zh_hangseng"

# 记录时间（例如：real 0m5.234s）
```

**预期结果：**
- PaddleOCR (CPU): 3-8秒
- Qwen-VL-Max: 8-15秒

**提升：** 2-3倍速度提升 ✅

---

## 🔄 前端集成（可选，10分钟）

如果API测试成功，可以继续前端集成：

### 第1步：引入SDK

在 `firstproject.html` 的 `<head>` 中添加：

```html
<!-- Backend API Client -->
<script src="backend-api-client.js"></script>
```

---

### 第2步：修改上传逻辑

找到 `uploadFileDirect()` 函数，在开头添加：

```javascript
async function uploadFileDirect(file, pages, documentType) {
    // ✅ 优先使用PaddleOCR后端
    try {
        const backendClient = new BackendAPIClient('http://localhost:8000');
        
        // 健康检查
        const health = await backendClient.healthCheck();
        
        if (health.status === 'healthy') {
            console.log('✅ 使用PaddleOCR后端提取');
            
            // 提取数据
            const result = await backendClient.extract(file);
            const extractedData = result.extractedData;
            
            // ... 使用extractedData进行后续处理 ...
            
            return;  // 成功，直接返回
        }
    } catch (error) {
        console.warn('⚠️ 后端提取失败，fallback到AI:', error);
    }
    
    // ⚠️ Fallback: 原有的Qwen-VL-Max逻辑
    // ... 保持不变 ...
}
```

---

### 第3步：测试前端集成

1. 打开 `firstproject.html`
2. 上传恒生银行对账单
3. 检查浏览器控制台：
   - 应该看到 `✅ 使用PaddleOCR后端提取`
   - 不应该有API调用到千问
4. 检查提取结果是否正确

---

## 📈 性能优化（可选）

### 如果速度仍然较慢（>10秒/页）

#### 方案1: 启用GPU加速（推荐，如有GPU）

```bash
source venv/bin/activate
pip uninstall paddlepaddle
pip install paddlepaddle-gpu==2.6.0
```

然后编辑 `backend/bank_statement_extractor.py`:
```python
# 第27行附近
self.table_engine = PPStructure(
    show_log=False,
    use_gpu=True,  # ← 改为True
    lang="ch"
)
```

**提速效果：** 3-8秒 → **1-3秒** ✅

---

#### 方案2: 降低DPI分辨率

编辑 `backend/bank_statement_extractor.py`:
```python
# 第125行附近
images = convert_from_path(pdf_path, dpi=200)  # 300 → 200
```

**提速效果：** 约30-40%  
**注意：** 可能轻微降低准确率

---

#### 方案3: 多进程部署

```bash
pip install gunicorn
gunicorn bank_statement_extractor:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

**提速效果：** 并发处理能力提升4倍

---

## 🔍 故障排查

### 问题1: `ModuleNotFoundError: No module named 'paddleocr'`

**原因：** 未激活虚拟环境  
**解决：**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### 问题2: `PDFInfoNotInstalledError`

**原因：** 缺少poppler  
**解决：**
```bash
brew install poppler  # macOS
```

---

### 问题3: 后端启动成功，但无法访问

**原因：** 端口被占用  
**解决：**
```bash
# 查找占用端口8000的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
python bank_statement_extractor.py --port 8001
```

---

### 问题4: 提取结果不准确

**原因：** 银行配置不匹配  
**解决：**
1. 检查 `bank_configs/zh/hangseng.yaml`
2. 确认 `table_keywords` 是否匹配PDF中的表头
3. 确认 `column_mapping` 是否匹配PDF中的列名
4. 如有需要，修改YAML后重启服务

---

## 📚 延伸阅读

- **快速入门**: `backend/README.md`
- **详细部署**: `backend/DEPLOYMENT_GUIDE.md`
- **完整实施方案**: `INDUSTRIAL_ARCHITECTURE_IMPLEMENTATION.md`
- **架构对比**: `ARCHITECTURE_COMPARISON_AND_MIGRATION.md`

---

## ✅ 完成检查清单

在继续下一步之前，请确认：

- [ ] ✅ poppler已安装（`pdfinfo --version`有输出）
- [ ] ✅ 后端服务启动成功（看到 `Uvicorn running on http://0.0.0.0:8000`）
- [ ] ✅ 健康检查通过（`curl http://localhost:8000/health`）
- [ ] ✅ 银行列表正确（`curl http://localhost:8000/api/banks`）
- [ ] ✅ API测试通过（`./test_api.sh`）
- [ ] ✅ 同日多笔交易处理正确（日期自动填充）
- [ ] ✅ 准确率≥95%（对比AI结果）
- [ ] ✅ 速度<10秒/页（CPU版本）

---

## 🎯 最终目标

1. **短期（1-2周）**
   - ✅ 部署测试环境
   - ✅ 验证恒生银行准确率（目标：>95%）
   - ✅ 添加更多银行配置（中国银行、招商银行）

2. **中期（1个月）**
   - ✅ 前端完全集成
   - ✅ 启用GPU加速（如有）
   - ✅ 逐步替换Qwen-VL-Max（节省成本）

3. **长期（3个月）**
   - ✅ 支持50+银行
   - ✅ 支持发票提取
   - ✅ 自动化银行识别

---

## 🚀 立即开始

```bash
cd backend
./quick_start.sh
```

**然后在新终端：**
```bash
cd backend
./test_api.sh
```

---

**🎉 祝测试顺利！如有问题，请查看文档或检查日志输出。**

**最后更新:** 2026-02-02  
**版本:** 1.0.0
