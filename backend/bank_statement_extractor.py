"""
Bank Statement Extractor - Production Grade
基于 PaddleOCR + YAML 配置的银行对账单提取器

功能：
- PDF → JSON 转换
- 多银行支持（通过YAML配置）
- 自动填充空白日期（同日多笔交易）
- RESTful API接口

作者：VaultCaddy
版本：1.0.0
日期：2026-02-02
"""

import os
import re
import cv2
import numpy as np
import yaml
from pathlib import Path
from paddleocr import PPStructure, draw_structure_result
from pdf2image import convert_from_path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankStatementExtractor:
    def __init__(self, config_dir="bank_configs"):
        """
        初始化提取器
        
        Args:
            config_dir: YAML配置文件目录
        """
        self.table_engine = PPStructure(
            show_log=False,
            use_gpu=False,  # ⚠️ 如果有GPU，改为True可提速3-5倍
            lang="ch"       # 多语言：ch/en/japan/korean
        )
        self.configs = self._load_bank_configs(config_dir)
        logger.info(f"✅ 已加载 {len(self.configs)} 个银行配置")
    
    def _load_bank_configs(self, config_dir):
        """加载所有银行YAML配置"""
        configs = {}
        config_path = Path(config_dir)
        
        if not config_path.exists():
            logger.warning(f"⚠️ 配置目录不存在: {config_dir}")
            return configs
        
        for lang_dir in config_path.iterdir():
            if not lang_dir.is_dir(): 
                continue
            
            for yaml_file in lang_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, encoding='utf-8') as f:
                        cfg = yaml.safe_load(f)
                        key = f"{cfg['language']}_{cfg['bank_code']}"
                        configs[key] = cfg
                        logger.info(f"  ✅ {key}: {cfg['bank_name']}")
                except Exception as e:
                    logger.error(f"  ❌ 加载失败 {yaml_file}: {e}")
        
        return configs
    
    def _clean_number(self, text):
        """
        清理并转换数字
        
        Examples:
            "1,234.56" → 1234.56
            "HKD 100" → 100
            "—" → None
        """
        if not text or text.strip() in ["—", "-", "N/A", "", " "]:
            return None
        
        # 移除货币符号、逗号、空格
        clean = re.sub(r'[,\s￥$HKD]', '', text.strip())
        
        # 处理括号（负数）
        if '(' in clean and ')' in clean:
            clean = '-' + clean.replace('(', '').replace(')', '')
        
        try:
            return float(clean) if '.' in clean else int(clean)
        except ValueError:
            logger.warning(f"⚠️ 无法转换数字: {text}")
            return None
    
    def _fill_empty_dates(self, transactions):
        """
        填充空白日期（同日多笔交易的核心逻辑）
        
        规则：
        - 如果日期为空，使用上一笔交易的日期
        - 如果第一笔为空，保留空（由后端处理）
        
        Args:
            transactions: 交易列表
            
        Returns:
            填充后的交易列表
        """
        last_date = None
        
        for trans in transactions:
            current_date = trans.get("date", "").strip()
            
            if current_date:
                # 有日期：更新最后有效日期
                last_date = current_date
            elif last_date:
                # 空日期：使用上一笔的日期
                trans["date"] = last_date
                trans["_date_filled"] = True  # 标记为自动填充
            # else: 第一笔就为空，保留空
        
        return transactions
    
    def _match_target_table(self, tables, config):
        """
        根据关键词筛选交易明细表（避免误读Account Summary）
        
        Args:
            tables: PaddleOCR识别的所有表格
            config: 银行配置
            
        Returns:
            目标表格或None
        """
        keywords = config.get("table_keywords", [])
        
        # 优先：关键词匹配
        for table in tables:
            html = table.get("res", {}).get("html", "")
            if any(kw in html for kw in keywords):
                logger.info(f"✅ 匹配到目标表格（关键词: {[k for k in keywords if k in html]}）")
                return table
        
        # 保底：取第一个表格
        if tables:
            logger.warning("⚠️ 未匹配到关键词，使用第一个表格")
            return tables[0]
        
        return None
    
    def _parse_table_to_transactions(self, table_html, config):
        """
        解析HTML表格 → 交易列表
        
        Args:
            table_html: PaddleOCR输出的HTML字符串
            config: 银行配置
            
        Returns:
            交易列表 (含空白日期填充)
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(table_html, 'html.parser')
        rows = soup.find_all('tr')
        
        if not rows:
            logger.warning("⚠️ 表格为空")
            return []
        
        # 1. 提取表头，建立列索引
        headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
        col_map = config["column_mapping"]
        
        # 查找每个字段对应的列索引
        idx = {}
        for key, col_names in col_map.items():
            if isinstance(col_names, str):
                col_names = [col_names]
            
            # 尝试匹配任意一个列名
            for col_name in col_names:
                try:
                    idx[key] = headers.index(col_name)
                    break
                except ValueError:
                    continue
            
            if key not in idx:
                idx[key] = -1
                logger.warning(f"⚠️ 未找到列: {key} (尝试过: {col_names})")
        
        # 2. 提取每一行数据
        transactions = []
        skip_rows = config.get("skip_rows", [])
        
        for row in rows[1:]:  # 跳过表头
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < max([v for v in idx.values() if v != -1], default=0) + 1:
                continue
            
            # 检查是否需要跳过（如"Sub-total"行）
            row_text = ' '.join([c.get_text(strip=True) for c in cells])
            if any(skip_word in row_text for skip_word in skip_rows):
                logger.info(f"⏭️  跳过行: {row_text[:50]}")
                continue
            
            # 提取字段
            trans = {
                "date": cells[idx["date"]].get_text(strip=True) if idx["date"] != -1 else "",
                "description": cells[idx["description"]].get_text(strip=True) if idx["description"] != -1 else "",
                "debit": self._clean_number(cells[idx["debit"]].get_text()) if idx["debit"] != -1 else 0,
                "credit": self._clean_number(cells[idx["credit"]].get_text()) if idx["credit"] != -1 else 0,
                "balance": self._clean_number(cells[idx["balance"]].get_text()) if idx["balance"] != -1 else None
            }
            
            # 确保debit/credit不为None
            if trans["debit"] is None:
                trans["debit"] = 0
            if trans["credit"] is None:
                trans["credit"] = 0
            
            transactions.append(trans)
        
        logger.info(f"✅ 提取了 {len(transactions)} 笔交易")
        
        # 3. 填充空白日期（关键步骤）
        return self._fill_empty_dates(transactions)
    
    def extract(self, pdf_path, bank_key=None):
        """
        主流程：PDF → JSON
        
        Args:
            pdf_path: PDF文件路径
            bank_key: 银行配置键（如"zh_hangseng"），None则自动识别
            
        Returns:
            标准JSON格式的对账单数据
        """
        logger.info(f"📄 开始处理: {pdf_path}")
        
        # 1. PDF转图像（300 DPI保证精度）
        logger.info("🖼️  PDF → 图像 (300 DPI)...")
        images = convert_from_path(pdf_path, dpi=300)
        logger.info(f"✅ 转换了 {len(images)} 页")
        
        # 2. 识别银行
        if not bank_key:
            bank_key = self._detect_bank(images[0]) if images else "zh_hangseng"
        
        config = self.configs.get(bank_key)
        if not config:
            logger.warning(f"⚠️ 未找到配置 {bank_key}，使用默认配置")
            config = list(self.configs.values())[0] if self.configs else {}
        
        logger.info(f"🏦 使用配置: {bank_key} ({config.get('bank_name', 'Unknown')})")
        
        # 3. 逐页处理
        all_txns = []
        
        for i, img in enumerate(images, 1):
            logger.info(f"📄 处理第 {i}/{len(images)} 页...")
            
            # 转换为OpenCV格式
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # PaddleOCR表格识别
            result = self.table_engine(img_cv)
            
            # 提取所有表格
            tables = [r for r in result if r.get("type") == "table"]
            logger.info(f"  📊 识别到 {len(tables)} 个表格")
            
            if not tables:
                logger.warning("  ⚠️ 未找到表格，跳过本页")
                continue
            
            # 匹配目标表格
            target_table = self._match_target_table(tables, config)
            
            if not target_table:
                logger.warning("  ⚠️ 未找到目标表格，跳过本页")
                continue
            
            # 解析表格
            txns = self._parse_table_to_transactions(
                target_table["res"]["html"], 
                config
            )
            
            all_txns.extend(txns)
        
        # 4. 构建最终JSON
        logger.info(f"✅ 共提取 {len(all_txns)} 笔交易")
        
        result = {
            "bankName": config.get("bank_name", "Unknown"),
            "accountNumber": "AUTO_DETECT_LATER",  # TODO: 从PDF元数据提取
            "accountHolder": "AUTO_DETECT_LATER",
            "currency": config.get("currency", "HKD"),
            "statementPeriod": self._extract_period(all_txns),
            "openingBalance": all_txns[0]["balance"] if all_txns else None,
            "closingBalance": all_txns[-1]["balance"] if all_txns else None,
            "transactions": all_txns,
            "_extractionMethod": "paddleocr",
            "_bankConfig": bank_key
        }
        
        return result
    
    def _extract_period(self, transactions):
        """从交易列表提取对账单周期"""
        if not transactions:
            return "Unknown"
        
        first_date = transactions[0].get("date", "")
        last_date = transactions[-1].get("date", "")
        
        if first_date and last_date:
            return f"{first_date} to {last_date}"
        
        return "Unknown"
    
    def _detect_bank(self, image):
        """
        简易银行识别（基于首页关键词）
        
        TODO: 生产环境建议使用：
        - 轻量级分类模型
        - 模板匹配
        - 关键词库
        
        Returns:
            bank_key (如 "zh_hangseng")
        """
        # 简化实现：返回默认值
        # 实际项目中，可以用PaddleOCR快速扫描首页关键词
        logger.info("🔍 使用默认银行配置（暂未实现自动识别）")
        return "zh_hangseng"


# =============== FastAPI 接口 ===============
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import shutil

app = FastAPI(
    title="Bank Statement API",
    version="1.0.0",
    description="生产级银行对账单提取API（基于PaddleOCR）"
)

# CORS配置（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局初始化提取器（启动时加载模型）
extractor = BankStatementExtractor()

@app.post("/api/extract")
async def extract_statement(
    file: UploadFile = File(...),
    bank_key: str = None  # 可选：前端指定银行（如"zh_hangseng"）
):
    """
    提取银行对账单数据
    
    Args:
        file: PDF文件
        bank_key: 银行配置键（可选）
        
    Returns:
        JSON格式的对账单数据
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "仅支持PDF文件")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        logger.info(f"📥 收到请求: {file.filename} (bank_key={bank_key})")
        result = extractor.extract(tmp_path, bank_key)
        logger.info(f"✅ 处理完成: {len(result['transactions'])} 笔交易")
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"❌ 处理失败: {str(e)}", exc_info=True)
        raise HTTPException(500, f"提取失败: {str(e)}")
    finally:
        # 清理临时文件
        Path(tmp_path).unlink(missing_ok=True)

@app.get("/api/banks")
async def list_supported_banks():
    """
    返回支持的银行列表（前端下拉框用）
    
    Returns:
        银行列表
    """
    banks = []
    for key, cfg in extractor.configs.items():
        banks.append({
            "key": key,
            "name": cfg["bank_name"],
            "language": cfg["language"],
            "region": cfg.get("region", "Unknown"),
            "currency": cfg.get("currency", "Unknown")
        })
    
    return {"banks": banks, "total": len(banks)}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "model_loaded": extractor.table_engine is not None,
        "configs_loaded": len(extractor.configs)
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 启动 Bank Statement API...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )

