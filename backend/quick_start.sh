#!/bin/bash
# Quick Start Script for Bank Statement Extractor
# 快速启动脚本

set -e  # 遇到错误立即退出

echo "🚀 Bank Statement Extractor - Quick Start"
echo "=========================================="
echo ""

# 检查Python版本
echo "📋 检查Python版本..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION"
echo ""

# 检查是否在正确的目录
if [ ! -f "bank_statement_extractor.py" ]; then
    echo "❌ 错误：请在 backend/ 目录下运行此脚本"
    echo "   cd /Users/cavlinyeung/ai-bank-parser/backend"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
    echo ""
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate
echo "✅ 已激活虚拟环境"
echo ""

# 检查依赖
echo "📦 检查依赖..."
if ! pip show paddleocr > /dev/null 2>&1; then
    echo "⏳ 首次安装依赖，可能需要5-10分钟..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi
echo ""

# 检查poppler（pdf2image依赖）
echo "🔍 检查系统依赖（poppler）..."
if command -v pdfinfo > /dev/null 2>&1; then
    echo "✅ poppler 已安装"
else
    echo "⚠️  警告：poppler 未安装"
    echo "   macOS: brew install poppler"
    echo "   Ubuntu: sudo apt-get install poppler-utils"
    echo ""
    read -p "   是否继续启动？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# 检查配置文件
echo "📁 检查配置文件..."
CONFIG_COUNT=$(find bank_configs -name "*.yaml" 2>/dev/null | wc -l)
if [ "$CONFIG_COUNT" -gt 0 ]; then
    echo "✅ 找到 $CONFIG_COUNT 个银行配置"
else
    echo "⚠️  警告：未找到银行配置文件"
fi
echo ""

# 启动服务
echo "🚀 启动API服务..."
echo "   URL: http://localhost:8000"
echo "   健康检查: http://localhost:8000/health"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "💡 提示：按 Ctrl+C 停止服务"
echo ""

python bank_statement_extractor.py

