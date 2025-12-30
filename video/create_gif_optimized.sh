#!/bin/bash
# 优化版：创建最后停留1秒的GIF
# 方法：在视频末尾添加1秒静帧，然后一次性转换

cd /Users/cavlinyeung/ai-bank-parser/video

echo "🎬 开始创建优化版GIF（最后停留1秒）..."

# 步骤1: 提取最后一帧作为图片
echo "📸 步骤1: 提取最后一帧..."
ffmpeg -y -sseof -1 -i "Chase Bank vaultcaddy.mp4" \
  -frames:v 1 \
  last_frame.png 2>&1 | grep -v "Metadata:" | tail -3

# 步骤2: 将最后一帧转换为1秒视频
echo "⏸️  步骤2: 创建1秒停留视频..."
ffmpeg -y -loop 1 -i last_frame.png \
  -t 1 \
  -pix_fmt yuv420p \
  pause_video.mp4 2>&1 | grep -v "Metadata:" | tail -3

# 步骤3: 合并原视频和停留视频
echo "🔗 步骤3: 合并视频..."
echo "file 'Chase Bank vaultcaddy.mp4'" > concat_list.txt
echo "file 'pause_video.mp4'" >> concat_list.txt

ffmpeg -y -f concat -safe 0 -i concat_list.txt \
  -c copy \
  combined_video.mp4 2>&1 | grep -v "Metadata:" | tail -3

# 步骤4: 生成调色板
echo "📊 步骤4: 生成调色板..."
ffmpeg -y -i combined_video.mp4 \
  -vf "fps=10,scale=900:-1:flags=lanczos,palettegen" \
  palette.png 2>&1 | grep "frame=" | tail -1

# 步骤5: 转换为GIF
echo "🎨 步骤5: 转换为GIF..."
ffmpeg -y -i combined_video.mp4 -i palette.png \
  -lavfi "fps=10,scale=900:-1:flags=lanczos [x]; [x][1:v] paletteuse" \
  chase-bank-demo.gif 2>&1 | grep "frame=" | tail -1

# 清理临时文件
rm last_frame.png pause_video.mp4 concat_list.txt combined_video.mp4 palette.png

# 显示结果
echo ""
echo "✅ 优化版GIF创建完成！"
ls -lh chase-bank-demo.gif
echo ""
echo "📊 效果:"
echo "  - 播放8.5秒动画"
echo "  - 最后一帧停留1秒"
echo "  - 然后循环播放"
echo "  - 文件大小优化"

