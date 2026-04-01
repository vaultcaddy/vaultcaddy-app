# 架构对比与最优迁移方案

## 📊 当前架构 vs 完整工业架构 - 详细对比

---

## 🔵 当前架构：AI端到端方案

### 完整转换流程（Step by Step）

```
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 1：文件上传与预处理                                          │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 1.1 用户上传 PDF 文件 (firstproject.html)
  │      └─ 输入：eStatement.pdf (可能是多页)
  │
  ├─ 1.2 PDF 转图片 (pdf-to-image-converter.js)
  │      └─ 使用：pdf.js
  │      └─ 输出：[page1.jpg, page2.jpg, page3.jpg]
  │      └─ 分辨率：150 DPI (可配置)
  │      └─ 格式：JPEG (Base64编码)
  │
  └─ 1.3 检测空白页 (可选)
         └─ 方法：计算图片亮度，过滤空白页
         └─ 输出：[page1.jpg, page3.jpg] (page2被过滤)

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 2：AI 端到端处理 (Qwen-VL-Max)                              │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 2.1 构建 AI 请求 (qwen-vl-max-processor.js)
  │      │
  │      ├─ 2.1.1 图片编码
  │      │       └─ 将所有页面转为 Base64
  │      │       └─ MIME类型：image/jpeg
  │      │
  │      ├─ 2.1.2 生成 Prompt (generatePrompt / generateMultiPagePrompt)
  │      │       └─ 包含：
  │      │           • 表格定位指令 ("FIND table with 戶口進支 AND 餘額")
  │      │           • 字段提取规则 (date, description, debit, credit, balance)
  │      │           • 输出格式 (JSON structure)
  │      │           • 示例数据 (同日多笔交易示例)
  │      │
  │      └─ 2.1.3 构建请求体
  │              └─ model: "qwen3-vl-plus-2025-12-19"
  │              └─ messages: [图片数组 + Prompt文本]
  │              └─ temperature: 0.1 (低随机性)
  │              └─ max_tokens: 4000-8000
  │
  ├─ 2.2 调用 Qwen-VL-Max API
  │      └─ 通过：Cloudflare Worker代理
  │      └─ 端点：https://deepseek-proxy.vaultcaddy.workers.dev
  │      └─ 处理时间：3-8秒/页
  │      └─ Token消耗：约1500-3000 tokens/页
  │
  ├─ 2.3 AI 内部处理（黑盒）
  │      │
  │      ├─ ⚠️ 视觉理解
  │      │    └─ 识别表格结构（但无坐标输出）
  │      │    └─ 识别文字（OCR）
  │      │    └─ 理解表格语义（"这是交易明细表"）
  │      │
  │      ├─ ⚠️ 字段提取
  │      │    └─ 根据Prompt指令提取字段
  │      │    └─ 问题：可能误读"Account Summary"
  │      │    └─ 问题：空白日期无法可靠填充（无行间状态）
  │      │
  │      └─ ⚠️ JSON生成
  │           └─ 输出结构化数据
  │           └─ 问题：可能包含Markdown代码块
  │
  └─ 2.4 解析 AI 响应 (parseJSON)
         └─ 尝试直接解析 JSON
         └─ 如失败：提取 ```json...``` 代码块
         └─ 如失败：提取 {...} 花括号内容
         └─ 输出：extractedData (原始JSON)

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 3：后处理与数据修复                                          │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 3.1 空白日期填充 (postProcessTransactions) ✅ 已实施
  │      └─ 遍历 transactions 数组
  │      └─ 如果 date === ""，使用上一笔的 date
  │      └─ 如果第一笔为空，从 statementPeriod 提取
  │      └─ 输出：processedData (日期已填充)
  │      └─ 准确率：70-90% (依赖AI提取顺序正确)
  │
  ├─ 3.2 余额校验 (可选，暂未实施)
  │      └─ 计算：openingBalance + Σcredit - Σdebit
  │      └─ 对比：是否等于 closingBalance
  │      └─ 如不匹配：标记警告
  │
  └─ 3.3 保存到 Firestore
         └─ 集合：documents
         └─ 字段：extractedData, processingTime, processor
         └─ 状态：completed

┌─────────────────────────────────────────────────────────────────┐
│ 当前架构的优势与问题                                              │
└─────────────────────────────────────────────────────────────────┘
  ✅ 优势：
     • 开发快速（已上线）
     • 对规范银行准确率高（工商银行 100%）
     • 代码简洁（约500行）
     • 支持多语言（Prompt可切换）
  
  ❌ 问题：
     • 恒生银行准确率低（72%）
     • AI黑盒，无法调试错误
     • Token消耗高（$0.005/页）
     • 无法精准定位"交易明细表"
     • 空白日期填充依赖AI提取顺序
```

---

## 🟢 完整工业架构：混合方案

### 完整转换流程（Step by Step）

```
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 1：文件上传与预处理（增强版）                                │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 1.1 用户上传 PDF 文件
  │      └─ 输入：eStatement.pdf
  │
  ├─ 1.2 PDF 转高质量图片 (增强)
  │      └─ 使用：pdf.js + OpenCV预处理
  │      └─ 分辨率：300 DPI (提升准确率)
  │      └─ 图像增强：
  │          • 去噪（Gaussian Blur）
  │          • 二值化（Otsu阈值）
  │          • 旋转校正（Hough Line Transform）
  │          • 对比度增强
  │      └─ 输出：[page1_enhanced.jpg, page2_enhanced.jpg]
  │
  └─ 1.3 银行识别 (新增) 🆕
         └─ 方法：快速OCR前100行 + 关键词匹配
         └─ 匹配：["HANG SENG BANK" → hangseng_hk.yaml]
         └─ 输出：bankConfig (银行专属配置)

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 2：表格定位层（核心新增）🆕                                  │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 2.1 OCR + 坐标提取 (PaddleOCR Layout)
  │      └─ 使用：PaddleOCR (开源免费)
  │      └─ 输出：
  │          • text: "10 Mar"
  │          • bbox: {x: 50, y: 300, width: 80, height: 20}
  │          • confidence: 0.98
  │      └─ 处理时间：2-3秒/页
  │      └─ 输出格式：
  │          [
  │            {text: "Date", bbox: [50,250,100,270], type: "header"},
  │            {text: "Description", bbox: [120,250,300,270], type: "header"},
  │            {text: "10 Mar", bbox: [50,300,100,320], type: "cell"},
  │            {text: "ATM WITHDRAWAL", bbox: [120,300,280,320], type: "cell"},
  │            {text: "", bbox: [50,340,100,360], type: "cell"},  ← 空白
  │            {text: "POS PURCHASE", bbox: [120,340,280,360], type: "cell"}
  │          ]
  │
  ├─ 2.2 表格区域定位 (关键步骤) 🎯
  │      │
  │      ├─ 2.2.1 关键词匹配
  │      │       └─ 扫描所有OCR结果
  │      │       └─ 查找：bankConfig.table_keywords
  │      │       └─ 示例：["TRANSACTION HISTORY", "戶口進支"]
  │      │       └─ 输出：tableHeaderY = 250 (表格标题的y坐标)
  │      │
  │      ├─ 2.2.2 忽略区域检测
  │      │       └─ 查找：bankConfig.ignore_sections
  │      │       └─ 示例：["ACCOUNT SUMMARY", "戶口摘要"]
  │      │       └─ 输出：ignoreRegions = [{y1: 100, y2: 200}]
  │      │
  │      ├─ 2.2.3 表格边界计算
  │      │       └─ 起始行：tableHeaderY + 30px
  │      │       └─ 结束行：下一个标题或页面底部
  │      │       └─ 输出：tableBBox = {y1: 280, y2: 800}
  │      │
  │      └─ 2.2.4 过滤OCR结果
  │              └─ 保留：y坐标在 [280, 800] 范围内
  │              └─ 排除：y坐标在 ignoreRegions 内
  │              └─ 输出：filteredOCR = [...] (仅交易明细)
  │
  └─ 2.3 列边界检测 (坐标聚类) 🎯
         │
         ├─ 2.3.1 提取所有 x 坐标
         │       └─ xCoords = [50, 50, 50, 120, 120, 450, 450, ...]
         │
         ├─ 2.3.2 K-Means 聚类
         │       └─ 假设：5-7列
         │       └─ 输出：clusters = [
         │           [50, 52, 48],      ← Date列
         │           [120, 118, 122],   ← Description列
         │           [450, 448, 452],   ← Debit列
         │           [580, 582, 578],   ← Credit列
         │           [720, 718, 722]    ← Balance列
         │         ]
         │
         ├─ 2.3.3 列名识别
         │       └─ 匹配：第一行（表头）的文本
         │       └─ 使用：bankConfig.column_mapping
         │       └─ 示例：
         │           • x=50 的表头是 "Date" → dateColumn
         │           • x=450 的表头是 "Withdrawal" → debitColumn
         │       └─ 输出：columnMap = {
         │           date: {xRange: [40, 110]},
         │           description: {xRange: [110, 400]},
         │           debit: {xRange: [400, 550]},
         │           credit: {xRange: [550, 700]},
         │           balance: {xRange: [700, 800]}
         │         }
         │
         └─ 2.3.4 输出表格结构
                 └─ 格式：
                     {
                       bbox: {y1: 280, y2: 800},
                       columns: columnMap,
                       rawOCR: filteredOCR
                     }

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 3：字段对齐层（规则驱动）🆕                                  │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 3.1 行分组 (基于 y 坐标)
  │      └─ 算法：相邻单词 y 坐标差 < 10px → 同一行
  │      └─ 输入：filteredOCR = [
  │          {text: "10 Mar", bbox: [50,300,100,320]},
  │          {text: "ATM", bbox: [120,300,180,320]},
  │          {text: "500", bbox: [450,300,490,320]},
  │          {text: "POS", bbox: [120,340,180,360]},  ← 新行（y=340）
  │          {text: "200", bbox: [450,340,490,360]}
  │        ]
  │      └─ 输出：rows = [
  │          Row1: [{text:"10 Mar",x:50}, {text:"ATM",x:120}, {text:"500",x:450}],
  │          Row2: [{text:"POS",x:120}, {text:"200",x:450}]
  │        ]
  │
  ├─ 3.2 单元格填充 (关键步骤) 🎯
  │      └─ 对每一行，按列边界分配单词
  │      └─ 示例：Row1
  │          • dateColumn (x=40-110): "10 Mar" ✅
  │          • descColumn (x=110-400): "ATM" ✅
  │          • debitColumn (x=400-550): "500" ✅
  │          • creditColumn (x=550-700): null (无单词)
  │          • balanceColumn (x=700-800): null (无单词)
  │      └─ 示例：Row2
  │          • dateColumn (x=40-110): null ❌ (空白)
  │          • descColumn (x=110-400): "POS" ✅
  │          • debitColumn (x=400-550): "200" ✅
  │      └─ 输出：structuredRows = [
  │          {date: "10 Mar", desc: "ATM", debit: 500, credit: 0, balance: null},
  │          {date: null, desc: "POS", debit: 200, credit: 0, balance: null}
  │        ]
  │
  ├─ 3.3 空值填充 (规则引擎) 🎯
  │      │
  │      ├─ 3.3.1 空白日期填充
  │      │       └─ 规则：bankConfig.empty_value_strategy.date = "carry_forward"
  │      │       └─ 逻辑：
  │      │           lastDate = null
  │      │           for row in structuredRows:
  │      │               if row.date is not null:
  │      │                   lastDate = row.date
  │      │               else:
  │      │                   row.date = lastDate  ✅ 确定性填充
  │      │                   row._dateFilled = true  (标记)
  │      │       └─ 输出：
  │      │           Row1: {date: "10 Mar", ...}
  │      │           Row2: {date: "10 Mar", _dateFilled: true, ...}
  │      │
  │      ├─ 3.3.2 空白余额填充
  │      │       └─ 规则：bankConfig.empty_value_strategy.balance = "null"
  │      │       └─ 逻辑：保持 null (后端累加计算)
  │      │
  │      └─ 3.3.3 日期格式转换
  │              └─ 规则：bankConfig.date_format = "DD MMM"
  │              └─ 转换："10 Mar" → "2025-03-10"
  │              └─ 使用：moment.js / dayjs
  │
  └─ 3.4 输出标准JSON
         └─ 格式：
             {
               bankName: "HANG SENG BANK",
               accountNumber: "766-450064-882",
               currency: "HKD",
               openingBalance: 30718.39,
               closingBalance: 30018.39,
               transactions: [
                 {date: "2025-03-10", desc: "ATM", debit: 500, balance: null, _dateFilled: false},
                 {date: "2025-03-10", desc: "POS", debit: 200, balance: null, _dateFilled: true}
               ],
               _method: "paddleocr + rule_engine"
             }

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 4：AI 辅助验证层（可选）🆕                                    │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 4.1 并行调用 Qwen-VL-Max
  │      └─ 目的：作为"第二意见"，验证OCR结果
  │      └─ Prompt简化：只需验证列名映射
  │      └─ 输出：aiResult (用于对比)
  │
  ├─ 4.2 结果对比
  │      └─ 对比：OCR提取 vs AI提取
  │      └─ 差异：如果金额差 > 1%，标记警告
  │      └─ 输出：mergedResult (OCR优先，AI补充)
  │
  └─ 4.3 不一致处理
         └─ 如果差异 > 阈值：
             • 记录日志
             • 展示双结果给用户选择
             • 触发人工审核

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 5：后验校验层 🆕                                             │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 5.1 余额校验
  │      └─ 计算：openingBalance + Σcredit - Σdebit
  │      └─ 对比：是否约等于 closingBalance (±0.01容差)
  │      └─ 如不匹配：
  │          • 标记警告："余额校验失败，差额HKD 2.61"
  │          • 可能原因：利息/手续费未计入
  │
  ├─ 5.2 日期排序校验
  │      └─ 检查：transactions 是否按日期递增
  │      └─ 允许：同日多笔（date相同）
  │      └─ 不允许：倒序（"10 Mar" 后出现 "9 Mar"）
  │
  ├─ 5.3 余额序列单调性检查
  │      └─ 检查：balance 变化是否合理
  │      └─ 示例：
  │          • Row1: balance = 30718.39
  │          • Row2: balance = 30218.39 (debit=500) ✅ 合理
  │          • Row3: balance = 50000.00 (debit=200) ❌ 异常跳跃
  │
  └─ 5.4 输出校验报告
         └─ 格式：
             {
               valid: true/false,
               warnings: [
                 "余额校验差额: HKD 2.61",
                 "第15笔交易日期倒序"
               ],
               confidence: 0.98
             }

┌─────────────────────────────────────────────────────────────────┐
│ 阶段 6：保存与展示                                                │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ 6.1 保存到 Firestore
  │      └─ 字段新增：
  │          • extractionMethod: "hybrid"
  │          • ocrEngine: "paddleocr"
  │          • bankConfig: "hangseng_hk.yaml"
  │          • validationReport: {...}
  │
  └─ 6.2 前端展示
         └─ 如果有警告：显示"⚠️ 校验发现异常"
         └─ 如果 _dateFilled: 标记"📅 日期已自动填充"

┌─────────────────────────────────────────────────────────────────┐
│ 完整工业架构的优势                                                │
└─────────────────────────────────────────────────────────────────┘
  ✅ 优势：
     • 准确率：98-99.5%（恒生银行从72% → 98%+）
     • 可调试：每一步有日志，可追溯错误
     • 成本：Token消耗减少80%（AI仅辅助）
     • 可扩展：新增银行只需添加YAML
     • 可审计：规则清晰，满足合规要求
     • 鲁棒性：多层校验，容错能力强
  
  ⚠️ 劣势：
     • 开发复杂度高（需1-2个月）
     • 依赖更多组件（PaddleOCR, OpenCV）
     • 初期维护成本高（YAML配置）
```

---

## 🔍 共同点分析

| 步骤 | 当前架构 | 完整工业架构 | 是否共同？ |
|------|---------|-------------|-----------|
| **文件上传** | ✅ firstproject.html | ✅ 同样的入口 | ✅ **共同** |
| **PDF转图片** | ✅ pdf.js (150 DPI) | ✅ pdf.js + 增强 (300 DPI) | 🔄 **可复用** |
| **表格定位** | ❌ 依赖AI视觉理解 | ✅ PaddleOCR + 关键词 | ❌ **需新增** |
| **OCR提取** | ❌ 由AI内部完成（黑盒）| ✅ PaddleOCR (可控) | ❌ **需新增** |
| **字段映射** | ❌ 依赖Prompt指令 | ✅ 规则引擎 + YAML | ❌ **需新增** |
| **空白日期填充** | ✅ postProcessTransactions | ✅ 规则引擎（更可靠）| 🔄 **可升级** |
| **AI调用** | ✅ Qwen-VL-Max (主力) | ✅ Qwen-VL-Max (辅助) | 🔄 **角色变化** |
| **JSON解析** | ✅ parseJSON | ✅ 同样的逻辑 | ✅ **共同** |
| **保存数据** | ✅ Firestore | ✅ Firestore | ✅ **共同** |
| **余额校验** | ❌ 暂无 | ✅ 后验校验层 | ❌ **需新增** |

---

## 🎯 最优转换方案（三阶段渐进式）

### 📌 核心原则：
1. **复用现有投资**：保留 pdf.js, Qwen-VL-Max, Firestore
2. **渐进式替换**：逐步降低对AI的依赖
3. **A/B测试**：新旧架构并行运行，验证准确率
4. **零停机迁移**：不影响现有用户

---

### 🔹 Phase 1：增强当前架构（1周，投入产出比最高）

**目标：** 恒生银行 72% → 90%+

**实施内容：**

```javascript
// 1. 集成轻量级OCR（仅用于坐标提取）
npm install tesseract.js

// 2. 新增模块：ocr-coordinate-extractor.js
class OCRCoordinateExtractor {
    async extractWithCoordinates(imageFile) {
        // 使用 Tesseract.js 获取坐标
        const { data: { words } } = await Tesseract.recognize(imageFile);
        return words; // [{text, bbox: {x0,y0,x1,y1}}]
    }
    
    detectColumnBoundaries(words) {
        // K-Means 聚类识别列边界
        return columnBoundaries;
    }
    
    alignRows(words, columns) {
        // 基于y坐标分组为行
        return structuredRows;
    }
    
    fillEmptyDates(rows) {
        // 规则填充空白日期
        return filledRows;
    }
}

// 3. 修改 qwen-vl-max-processor.js
async processDocument(file, documentType) {
    // A. OCR预处理（新增）
    const ocrData = await this.ocrExtractor.extractWithCoordinates(file);
    const prefilledData = await this.ocrExtractor.fillEmptyDates(ocrData);
    
    // B. 调用 Qwen-VL-Max（保留）
    const aiResult = await this.callQwenVL(file, documentType);
    
    // C. 合并结果（OCR坐标优先，AI内容补充）
    const mergedData = this.mergeOCRAndAI(prefilledData, aiResult);
    
    return mergedData;
}
```

**复用比例：** 80%（仅新增OCR模块，其他不变）

**效果：**
- ✅ 恒生银行：72% → 90%+
- ✅ Token消耗：不变
- ✅ 开发时间：5-7天

---

### 🔹 Phase 2：混合架构（3-4周）

**目标：** 恒生银行 90% → 98%+

**实施内容：**

```python
# 1. 后端API（Python FastAPI）
# file: bank-parser-api/main.py

from fastapi import FastAPI, UploadFile
from paddleocr import PPStructure
import yaml

app = FastAPI()

# 加载银行配置
with open('config/banks/hangseng_hk.yaml') as f:
    bank_configs = yaml.safe_load(f)

table_engine = PPStructure(show_log=False)

@app.post("/parse-statement")
async def parse_statement(file: UploadFile):
    # 1. OCR + 表格定位
    ocr_result = table_engine(file)
    
    # 2. 识别银行
    bank_name = detect_bank(ocr_result)
    config = bank_configs[bank_name]
    
    # 3. 表格定位
    table_region = locate_table(ocr_result, config)
    
    # 4. 字段对齐
    structured_data = align_fields(table_region, config)
    
    # 5. 空值填充
    filled_data = fill_empty_values(structured_data, config)
    
    # 6. 余额校验
    validation = validate_balance(filled_data)
    
    return {
        "data": filled_data,
        "validation": validation,
        "method": "hybrid"
    }
```

```javascript
// 2. 前端调用（JavaScript）
// file: qwen-vl-max-processor.js

async processDocumentHybrid(file, documentType) {
    // A. 调用Python API（主力）
    const formData = new FormData();
    formData.append('file', file);
    
    const ocrResult = await fetch('http://localhost:8000/parse-statement', {
        method: 'POST',
        body: formData
    }).then(r => r.json());
    
    // B. 并行调用 Qwen-VL-Max（验证）
    const aiResult = await this.callQwenVL(file, documentType);
    
    // C. 对比与合并
    if (Math.abs(ocrResult.data.closingBalance - aiResult.closingBalance) > 100) {
        console.warn('⚠️ OCR与AI结果差异较大，需人工审核');
        return {
            ...ocrResult,
            aiSecondOpinion: aiResult,
            needsReview: true
        };
    }
    
    return ocrResult;
}
```

```yaml
# 3. 银行配置（YAML）
# file: config/banks/hangseng_hk.yaml

bank_name: "HANG SENG BANK"
currency: "HKD"
locale: "zh-HK"

table_detection:
  keywords: ["TRANSACTION HISTORY", "戶口進支", "交易明細"]
  ignore_sections: ["ACCOUNT SUMMARY", "戶口摘要", "總計"]

column_mapping:
  date: ["Date", "日期", "交易日期"]
  description: ["Description", "摘要", "說明", "Particulars"]
  debit: ["Withdrawal", "Withdrawals", "借項", "支出", "Debit"]
  credit: ["Deposit", "Deposits", "貸項", "存入", "Credit"]
  balance: ["Balance", "餘額", "結餘"]

empty_value_strategy:
  date: "carry_forward"  # 使用上一行日期
  balance: "null"        # 输出null

date_format: "DD MMM"  # "10 Mar" → "2025-03-10"

validation_rules:
  balance_tolerance: 0.01  # ±0.01容差
  allow_same_date: true    # 允许同日多笔
```

**复用比例：** 50%（前端保留，新增Python后端）

**效果：**
- ✅ 恒生银行：90% → 98%+
- ✅ Token消耗：减少50%（OCR主力，AI辅助）
- ✅ 新增银行：10分钟（添加YAML）

---

### 🔹 Phase 3：完整工业架构（2-3个月）

**目标：** 全面替换AI主导，AI仅辅助

**实施内容：**
- ✅ 图像增强（OpenCV去噪/旋转校正）
- ✅ 表格检测模型（TableTransformer）
- ✅ 多语言OCR（PaddleOCR多语言包）
- ✅ 完整规则引擎（支持复杂逻辑）
- ✅ 后验校验系统（余额/日期/单调性）
- ✅ 审计日志（每一步可追溯）

**复用比例：** 20%（仅保留Firestore和前端UI）

**效果：**
- ✅ 准确率：98-99.5%
- ✅ Token消耗：减少80%
- ✅ 成本：从 $0.005/页 → $0.001/页

---

## 📊 三阶段对比

| 维度 | Phase 1 (增强) | Phase 2 (混合) | Phase 3 (完整) |
|------|---------------|---------------|---------------|
| **恒生准确率** | 90%+ | 98%+ | 99%+ |
| **开发时间** | 1周 | 3-4周 | 2-3个月 |
| **复用率** | 80% | 50% | 20% |
| **Token消耗** | 100% | 50% | 20% |
| **新增银行成本** | 高（调Prompt）| 中（写YAML）| 低（写YAML）|
| **可审计性** | 低 | 中 | 高 |
| **推荐时机** | ✅ 立即 | 3个月后 | 50+银行后 |

---

## ✅ 最终建议：三阶段渐进式迁移

```
当前（AI主导）
    │
    │  [1周] Phase 1
    ▼
增强版（AI + OCR坐标）90%+
    │
    │  [3-4周] Phase 2
    ▼
混合架构（OCR主力 + AI辅助）98%+
    │
    │  [2-3个月] Phase 3
    ▼
完整工业架构（规则主导 + AI兜底）99%+
```

**立即执行：Phase 1**
- 投入：1周开发
- 产出：恒生银行 72% → 90%+
- 风险：低（只新增模块，不破坏现有）

我可以立即帮您实施 Phase 1，需要我开始编写代码吗？🚀

