#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为所有 v3 landing pages 添加演示视频
作用：在 Hero Section 和 Features Section 之间插入视频演示
"""

import os
import re
from pathlib import Path

# 视频演示 HTML 代码
VIDEO_DEMO_HTML = '''
    <!-- 🎥 Demo Video Section -->
    <section style="padding: 80px 24px; background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);">
        <div style="max-width: 1200px; margin: 0 auto;">
            <!-- 标题 -->
            <div style="text-align: center; margin-bottom: 60px;">
                <div style="display: inline-block; background: rgba(99, 102, 241, 0.1); border: 2px solid rgba(99, 102, 241, 0.3); padding: 12px 32px; border-radius: 50px; margin-bottom: 24px;">
                    <span style="color: #6366f1; font-weight: 700; font-size: 14px; letter-spacing: 1px;">
                        🎥 LIVE DEMONSTRATION
                    </span>
                </div>
                <h2 style="font-size: 48px; font-weight: 800; color: white; margin-bottom: 20px; line-height: 1.2;">
                    See VaultCaddy in Action
                </h2>
                <p style="font-size: 20px; color: #94a3b8; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                    Watch how Chase Bank statements are converted to Excel in seconds with 98% accuracy
                </p>
            </div>
            
            <!-- 视频容器 -->
            <div style="position: relative; max-width: 900px; margin: 0 auto; border-radius: 20px; overflow: hidden; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 100px rgba(99, 102, 241, 0.3); background: #000;">
                <!-- 视频 -->
                <video 
                    controls 
                    preload="metadata"
                    poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='506'%3E%3Crect fill='%23667eea' width='900' height='506'/%3E%3Ctext x='50%25' y='50%25' font-size='48' fill='white' text-anchor='middle' dy='.3em'%3E▶ Play Demo%3C/text%3E%3C/svg%3E"
                    style="width: 100%; height: auto; display: block;">
                    <source src="/video/Chase Bank vaultcaddy.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                
                <!-- 播放按钮覆盖层（点击后消失） -->
                <div id="videoPlayOverlay" onclick="playDemoVideo(this)" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: opacity 0.3s;">
                    <div style="width: 100px; height: 100px; background: rgba(99, 102, 241, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s, background 0.3s;" onmouseover="this.style.transform='scale(1.1)'; this.style.background='rgba(99, 102, 241, 1)';" onmouseout="this.style.transform='scale(1)'; this.style.background='rgba(99, 102, 241, 0.9)';">
                        <i class="fas fa-play" style="color: white; font-size: 36px; margin-left: 6px;"></i>
                    </div>
                </div>
            </div>
            
            <!-- 视频下方特点 -->
            <div style="margin-top: 60px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 900px; margin-left: auto; margin-right: auto;">
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 48px; color: #10b981; margin-bottom: 12px;">⚡</div>
                    <div style="font-size: 32px; font-weight: 800; color: white; margin-bottom: 8px;">3s</div>
                    <div style="font-size: 16px; color: #94a3b8;">Average Processing</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 48px; color: #6366f1; margin-bottom: 12px;">🎯</div>
                    <div style="font-size: 32px; font-weight: 800; color: white; margin-bottom: 8px;">98%</div>
                    <div style="font-size: 16px; color: #94a3b8;">Accuracy Rate</div>
                </div>
                
                <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.05); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="font-size: 48px; color: #ec4899; margin-bottom: 12px;">💰</div>
                    <div style="font-size: 32px; font-weight: 800; color: white; margin-bottom: 8px;">$5.59</div>
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
    
    <script>
    function playDemoVideo(overlay) {
        const video = overlay.previousElementSibling;
        if (video && video.tagName === 'VIDEO') {
            video.play();
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }
    }
    </script>

'''

def add_video_to_page(file_path):
    """为单个页面添加视频演示"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加过视频
        if '<!-- 🎥 Demo Video Section -->' in content:
            return 'skip', '已存在视频'
        
        # 查找插入位置：Hero Section 结束后，Features Section 之前
        # 寻找 </section> 后跟 <!-- Features Section -->
        pattern = r'(</section>\s*)\n(\s*<!-- Features Section -->)'
        
        if not re.search(pattern, content):
            return 'error', '未找到插入位置'
        
        # 插入视频演示
        new_content = re.sub(
            pattern,
            r'\1' + VIDEO_DEMO_HTML + r'\2',
            content,
            count=1
        )
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 'success', '已添加'
    
    except Exception as e:
        return 'error', str(e)

def main():
    print("🎥 开始为所有 v3 landing pages 添加演示视频...")
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
        status, message = add_video_to_page(str(page_path))
        
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
    print(f"✅ 成功添加: {success_count}")
    print(f"⏭️  已存在跳过: {skip_count}")
    print(f"❌ 失败: {error_count}")
    print(f"📊 总计: {len(v3_pages)}")
    print()
    print("📋 视频演示特点:")
    print("  ✅ 响应式设计（移动端友好）")
    print("  ✅ 自定义播放按钮")
    print("  ✅ 性能指标展示（3秒、98%、$5.59）")
    print("  ✅ 免费试用 CTA")
    print("  ✅ 视频路径：/video/Chase Bank vaultcaddy.mp4")

if __name__ == '__main__':
    main()

