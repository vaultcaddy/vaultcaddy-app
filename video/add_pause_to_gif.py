#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为GIF添加最后停留1秒效果
使用PIL库修改GIF帧延迟
"""

from PIL import Image
import os

def add_pause_to_gif(input_path, output_path, pause_duration=1000):
    """
    为GIF的最后一帧添加停留时间
    
    Args:
        input_path: 输入GIF路径
        output_path: 输出GIF路径
        pause_duration: 停留时间（毫秒），默认1000ms = 1秒
    """
    print(f"📖 读取GIF: {input_path}")
    
    # 打开GIF
    img = Image.open(input_path)
    
    # 获取所有帧
    frames = []
    durations = []
    
    try:
        frame_count = 0
        while True:
            frames.append(img.copy())
            # 获取当前帧的延迟时间（毫秒）
            duration = img.info.get('duration', 100)
            durations.append(duration)
            frame_count += 1
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    
    print(f"📊 总帧数: {frame_count}")
    print(f"⏱️  原始帧延迟: {durations[0]}ms")
    
    # 修改最后一帧的延迟
    if len(durations) > 0:
        original_last_delay = durations[-1]
        durations[-1] += pause_duration
        print(f"✨ 最后一帧延迟: {original_last_delay}ms → {durations[-1]}ms")
        print(f"📐 添加停留时间: {pause_duration}ms ({pause_duration/1000}秒)")
    
    # 保存新GIF
    print(f"💾 保存新GIF: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,  # 0 = 无限循环
        optimize=False
    )
    
    # 显示文件大小
    original_size = os.path.getsize(input_path)
    new_size = os.path.getsize(output_path)
    
    print(f"\n✅ 完成！")
    print(f"📦 原始文件: {original_size / 1024 / 1024:.2f} MB")
    print(f"📦 新文件: {new_size / 1024 / 1024:.2f} MB")
    print(f"📊 大小变化: {((new_size - original_size) / original_size * 100):+.1f}%")

if __name__ == '__main__':
    import sys
    
    # 文件路径
    video_dir = '/Users/cavlinyeung/ai-bank-parser/video'
    input_gif = os.path.join(video_dir, 'chase-bank-demo.gif')
    output_gif = os.path.join(video_dir, 'chase-bank-demo-new.gif')
    
    print("🎬 GIF停留效果添加工具")
    print("=" * 60)
    
    # 检查输入文件
    if not os.path.exists(input_gif):
        # 使用之前的1.1MB版本
        print(f"⚠️  未找到大文件，尝试使用备份...")
        # 检查是否有备份
        if os.path.exists(input_gif):
            print(f"✅ 找到GIF文件")
        else:
            print(f"❌ 错误: 未找到输入文件 {input_gif}")
            sys.exit(1)
    
    try:
        # 添加停留效果
        add_pause_to_gif(input_gif, output_gif, pause_duration=1000)
        
        # 替换原文件
        print(f"\n🔄 替换原文件...")
        os.replace(output_gif, input_gif)
        print(f"✅ 已更新: {input_gif}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

