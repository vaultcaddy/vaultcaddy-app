#!/bin/bash
# 创建最后停留1秒的GIF
# 作用：生成演示GIF，最后一帧停留1秒后才循环

cd /Users/cavlinyeung/ai-bank-parser/video

echo "🎬 开始创建带停留效果的GIF..."

# 步骤1: 生成调色板
echo "📊 步骤1: 生成调色板..."
ffmpeg -y -i "Chase Bank vaultcaddy.mp4" \
  -vf "fps=10,scale=900:-1:flags=lanczos,palettegen" \
  palette.png 2>&1 | grep -E "frame=|Video:"

# 步骤2: 创建主要GIF（不包含最后一帧）
echo "🎨 步骤2: 创建主要部分..."
ffmpeg -y -i "Chase Bank vaultcaddy.mp4" -i palette.png \
  -lavfi "fps=10,scale=900:-1:flags=lanczos [x]; [x][1:v] paletteuse" \
  -t 8.4 \
  temp_main.gif 2>&1 | grep -E "frame=|size="

# 步骤3: 提取最后一帧作为单独的GIF（停留1秒 = 10帧）
echo "⏸️  步骤3: 创建停留帧..."
ffmpeg -y -ss 8.4 -i "Chase Bank vaultcaddy.mp4" -i palette.png \
  -lavfi "fps=10,scale=900:-1:flags=lanczos [x]; [x][1:v] paletteuse" \
  -frames:v 10 \
  temp_pause.gif 2>&1 | grep -E "frame=|size="

# 步骤4: 合并GIF
echo "🔗 步骤4: 合并GIF..."
ffmpeg -y -i temp_main.gif -i temp_pause.gif \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0" \
  chase-bank-demo.gif 2>&1 | grep -E "frame=|size="

# 清理临时文件
rm palette.png temp_main.gif temp_pause.gif

# 显示结果
echo ""
echo "✅ GIF创建完成！"
ls -lh chase-bank-demo.gif
echo ""
echo "📊 GIF信息:"
echo "  - 主要动画: 8.4秒"
echo "  - 停留时间: 1秒"
echo "  - 总时长: 9.4秒"
echo "  - 效果: 播放完后在最后一帧停留1秒，然后循环"

