#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将视频演示 Section 改为 GIF 演示
作用：移除视频播放器，改用自动循环的 GIF 动图
"""

import os
import re
from pathlib import Path

# GIF 演示 HTML 代码
GIF_DEMO_HTML = '''
    <!-- 🎬 Demo GIF Section -->
    <section style="padding: 80px 24px; background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);">
        <div style="max-width: 1200px; margin: 0 auto;">
            <!-- 标题 -->
            <div style="text-align: center; margin-bottom: 60px;">
                <div style="display: inline-block; background: rgba(99, 102, 241, 0.1); border: 2px solid rgba(99, 102, 241, 0.3); padding: 12px 32px; border-radius: 50px; margin-bottom: 24px;">
                    <span style="color: #6366f1; font-weight: 700; font-size: 14px; letter-spacing: 1px;">
                        🎬 LIVE DEMONSTRATION
                    </span>
                </div>
                <h2 style="font-size: 48px; font-weight: 800; color: white; margin-bottom: 20px; line-height: 1.2;">
                    See VaultCaddy in Action
                </h2>
                <p style="font-size: 20px; color: #94a3b8; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                    Watch how Chase Bank statements are converted to Excel in seconds with 98% accuracy
                </p>
            </div>
            
            <!-- GIF 容器 -->
            <div style="position: relative; max-width: 900px; margin: 0 auto; border-radius: 20px; overflow: hidden; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 100px rgba(99, 102, 241, 0.3); background: #000;">
                <!-- GIF 动图 - 自动播放循环 -->
                <img 
                    src="/video/chase-bank-demo.gif" 
                    alt="Chase Bank Statement Conversion Demo"
                    style="width: 100%; height: auto; display: block; border-radius: 20px;"
                    loading="lazy"
                >
                
                <!-- 自动播放标签 -->
                <div style="position: absolute; top: 20px; right: 20px; background: rgba(16, 185, 129, 0.95); backdrop-filter: blur(10px); padding: 8px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);">
                    <div style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: pulse 1.5s ease-in-out infinite;"></div>
                    <span style="color: white; font-weight: 600; font-size: 13px;">AUTO PLAYING</span>
                </div>
            </div>
            
            <!-- GIF 下方特点 -->
            <div style="margin-top: 60px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 900px; margin-left: auto; margin-right: auto;">
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">⚡</div>
                    <div style="font-size: 32px; font-weight: 800; color: #10b981; margin-bottom: 8px;">3s</div>
                    <div style="font-size: 16px; color: #94a3b8;">Average Processing</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">🎯</div>
                    <div style="font-size: 32px; font-weight: 800; color: #6366f1; margin-bottom: 8px;">98%</div>
                    <div style="font-size: 16px; color: #94a3b8;">Accuracy Rate</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='translateY(-5px)'; this.style.background='rgba(255, 255, 255, 0.08)';" onmouseout="this.style.transform='translateY(0)'; this.style.background='rgba(255, 255, 255, 0.05)';">
                    <div style="font-size: 48px; margin-bottom: 12px;">💰</div>
                    <div style="font-size: 32px; font-weight: 800; color: #ec4899; margin-bottom: 8px;">$5.59</div>
                    <div style="font-size: 16px; color: #94a3b8;">Starting From/Month</div>
                </div>
            </div>
            
            <!-- CTA 按钮 -->
            <div style="text-align: center; margin-top: 50px;">
                <a href="/signup.html" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 20px 50px; border-radius: 50px; font-weight: 700; font-size: 18px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); transition: transform 0.3s, box-shadow 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 15px 40px rgba(102, 126, 234, 0.5)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(102, 126, 234, 0.4)';">
                    🎁 Start Free Trial - 20 Pages Free
                </a>
                <p style="margin-top: 16px; color: #94a3b8; font-size: 14px;">No credit card required • Cancel anytime</p>
            </div>
        </div>
    </section>
    
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    @media (max-width: 768px) {
        h2 { font-size: 36px !important; }
        p { font-size: 16px !important; }
    }
    </style>

'''

def convert_video_to_gif(file_path):
    """将视频演示改为GIF演示"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有视频 section
        if '<!-- 🎥 Demo Video Section -->' not in content:
            return 'skip', '未找到视频section'
        
        # 移除整个视频 section（包括 script）
        pattern = r'    <!-- 🎥 Demo Video Section -->.*?</script>\n\n'
        
        if not re.search(pattern, content, re.DOTALL):
            return 'error', '未找到完整的视频section'
        
        # 替换为 GIF section
        new_content = re.sub(
            pattern,
            GIF_DEMO_HTML,
            content,
            flags=re.DOTALL
        )
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 'success', '已转换为GIF'
    
    except Exception as e:
        return 'error', str(e)

def main():
    print("🎬 开始将视频演示转换为GIF演示...")
    print("=" * 80)
    
    # 查找所有 v3 页面
    v3_pages = []
    
    # 根目录的 v3 页面
    root_v3 = list(Path('.').glob('*-v3.html'))
    v3_pages.extend(root_v3)
    
    # 各语言文件夹中的 v3 页面
    language_folders = ['zh-HK', 'zh-TW', 'ja-JP', 'ko-KR']
    for lang_folder in language_folders:
        if os.path.exists(lang_folder):
            lang_v3 = list(Path(lang_folder).glob('*-v3.html'))
            v3_pages.extend(lang_v3)
    
    print(f"📊 找到 {len(v3_pages)} 个 v3 landing pages")
    print()
    
    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    
    # 处理每个页面
    for page_path in v3_pages:
        status, message = convert_video_to_gif(str(page_path))
        
        if status == 'success':
            print(f"✅ {page_path}")
            success_count += 1
        elif status == 'skip':
            print(f"⏭️  {page_path} - {message}")
            skip_count += 1
        else:
            print(f"❌ {page_path} - {message}")
            error_count += 1
    
    print()
    print("=" * 80)
    print(f"🎉 完成！")
    print(f"✅ 成功转换: {success_count}")
    print(f"⏭️  跳过: {skip_count}")
    print(f"❌ 失败: {error_count}")
    print(f"📊 总计: {len(v3_pages)}")
    print()
    print("📋 GIF 演示特点:")
    print("  ✅ 自动播放（无需点击）")
    print("  ✅ 循环播放（持续吸引注意）")
    print("  ✅ 100%兼容性")
    print("  ✅ AUTO PLAYING 标签")
    print("  ✅ 响应式设计")
    print()
    print("⚠️  下一步：")
    print("  1. 使用视频转GIF工具创建 GIF 文件")
    print("  2. 将 GIF 保存为: /video/chase-bank-demo.gif")
    print("  3. 建议 GIF 尺寸: 1200x675px (16:9)")
    print("  4. 建议 GIF 时长: 10-15秒循环")
    print("  5. 建议 GIF 大小: <5MB")

if __name__ == '__main__':
    main()

