#!/bin/bash
# 自动转换MOV视频到优化的GIF
# 使用FFmpeg进行高质量转换

echo "🎞️  视频转GIF自动化脚本"
echo "============================================================"

# 检查FFmpeg是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 错误: 未找到FFmpeg"
    echo ""
    echo "请先安装FFmpeg:"
    echo "  brew install ffmpeg"
    echo ""
    exit 1
fi

echo "✅ FFmpeg已安装"
echo ""

# 设置参数
FPS=20  # 帧率（降低以减小文件大小）
WIDTH=1280  # 宽度
QUALITY=80  # 质量（1-100，80是好的平衡点）

# 定义文件映射
declare -A FILES=(
    ["chase-bank-demo-ko.mov"]="chase-bank-demo-ko.gif"
    ["chase-bank-demo-ja.mov"]="chase-bank-demo-ja.gif"
    ["chase-bank-demo-zh-hk.mov"]="chase-bank-demo-zh-hk.gif"
    ["chase-bank-demo-zh-tw.mov"]="chase-bank-demo-zh-tw.gif"
    ["chase-bank-demo-en.mov"]="chase-bank-demo-en.gif"
)

echo "🔍 检查视频文件..."
echo ""

FOUND_COUNT=0
for mov_file in "${!FILES[@]}"; do
    if [ -f "$mov_file" ]; then
        echo "  ✅ 找到: $mov_file"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    else
        echo "  ⚠️  未找到: $mov_file"
    fi
done

echo ""
echo "找到 $FOUND_COUNT 个视频文件"
echo ""

if [ $FOUND_COUNT -eq 0 ]; then
    echo "❌ 没有找到任何视频文件"
    echo ""
    echo "请确保以下文件存在于当前目录:"
    for mov_file in "${!FILES[@]}"; do
        echo "  - $mov_file"
    done
    echo ""
    exit 1
fi

echo "============================================================"
echo "开始转换..."
echo "============================================================"
echo ""

CONVERTED_COUNT=0
FAILED_COUNT=0

for mov_file in "${!FILES[@]}"; do
    if [ ! -f "$mov_file" ]; then
        continue
    fi
    
    gif_file="${FILES[$mov_file]}"
    
    echo "🎬 转换: $mov_file → $gif_file"
    
    # 获取原始文件大小
    original_size=$(du -h "$mov_file" | cut -f1)
    echo "   原始大小: $original_size"
    
    # 转换命令（两步法，更高质量）
    # 步骤1: 生成调色板
    echo "   步骤1/3: 生成调色板..."
    ffmpeg -i "$mov_file" -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,palettegen=max_colors=256" -y palette.png 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "   ❌ 生成调色板失败"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        continue
    fi
    
    # 步骤2: 使用调色板生成GIF
    echo "   步骤2/3: 生成GIF..."
    ffmpeg -i "$mov_file" -i palette.png -lavfi "fps=$FPS,scale=$WIDTH:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5" -y "$gif_file" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "   ❌ 生成GIF失败"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        continue
    fi
    
    # 清理临时文件
    rm -f palette.png
    
    # 检查输出文件
    if [ -f "$gif_file" ]; then
        gif_size=$(du -h "$gif_file" | cut -f1)
        gif_size_mb=$(du -m "$gif_file" | cut -f1)
        
        echo "   ✅ 转换成功"
        echo "   GIF大小: $gif_size"
        
        # 检查文件大小是否超过2MB
        if [ $gif_size_mb -gt 2 ]; then
            echo "   ⚠️  警告: GIF超过2MB，将在步骤3中优化"
        fi
        
        CONVERTED_COUNT=$((CONVERTED_COUNT + 1))
    else
        echo "   ❌ 转换失败"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
    
    echo ""
done

echo "============================================================"
echo "🎉 转换完成！"
echo "============================================================"
echo ""
echo "📊 统计:"
echo "   - 成功: $CONVERTED_COUNT"
echo "   - 失败: $FAILED_COUNT"
echo "   - 总计: $((CONVERTED_COUNT + FAILED_COUNT))"
echo ""

if [ $CONVERTED_COUNT -gt 0 ]; then
    echo "✅ 生成的GIF文件:"
    for gif_file in "${FILES[@]}"; do
        if [ -f "$gif_file" ]; then
            size=$(du -h "$gif_file" | cut -f1)
            echo "   - $gif_file ($size)"
        fi
    done
    echo ""
    echo "下一步:"
    echo "   1. 运行: python3 ../optimize_and_add_pause.py"
    echo "   2. 添加最后一帧停留1秒"
    echo "   3. 进一步优化文件大小"
fi

echo ""
echo "============================================================"

