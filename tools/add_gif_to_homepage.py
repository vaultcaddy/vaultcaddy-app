#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在主要首页的All-in-One部分添加GIF演示
"""

import re

def add_gif_to_index():
    """在index.html添加GIF"""
    
    # 主要的4个首页
    index_files = [
        'index.html',           # 主首页
        'en/index.html',        # 英文版
        'zh-TW/index.html',     # 台湾繁体版  
        'zh-HK/index.html',     # 香港繁体版
    ]
    
    # GIF HTML
    gif_section = '''
                <!-- VaultCaddy Demo GIF -->
                <div style="text-align: center; margin: 50px auto; max-width: 1000px; padding: 0 20px;">
                    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 40px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                        <div style="margin-bottom: 20px;">
                            <i class="fas fa-video" style="color: #6366f1; font-size: 24px;"></i>
                        </div>
                        <h3 style="font-size: 24px; font-weight: 700; color: #0f172a; margin-bottom: 15px;">
                            🎬 See VaultCaddy in Action
                        </h3>
                        <p style="font-size: 16px; color: #64748b; margin-bottom: 30px;">
                            Watch how easy it is to upload and process your bank statement in 3 seconds
                        </p>
                        <img src="images/vaultcaddy-upload-demo.gif" 
                             alt="VaultCaddy Upload Demo - Process bank statements in 3 seconds" 
                             style="max-width: 100%; width: 900px; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); border: 3px solid #e2e8f0;" 
                             loading="lazy">
                        <p style="margin-top: 20px; color: #64748b; font-size: 14px; font-style: italic;">
                            Upload → AI Processing → Export to Excel/QuickBooks in 3 seconds
                        </p>
                    </div>
                </div>
'''
    
    updated_count = 0
    
    for file_path in index_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含All-in-One或类似的标题
            if 'All-in-One' not in content and 'Document Processing' not in content:
                continue
            
            # 检查是否已经添加过GIF
            if 'vaultcaddy-upload-demo.gif' in content:
                print(f"⚠️  {file_path} 已包含GIF，跳过")
                continue
            
            # 查找合适的位置插入GIF
            # 在Features部分之前或All-in-One标题之后
            patterns = [
                # 在Features section之前
                (r'(<section[^>]*class="[^"]*features[^"]*"[^>]*>)', r'{}\1'.format(gif_section)),
                # 在Hero section之后
                (r'(</section>)(\s*<section[^>]*class="[^"]*features)', r'\1{}\2'.format(gif_section)),
                # 在主要内容区域
                (r'(<div[^>]*class="[^"]*container[^"]*"[^>]*>.*?<h2[^>]*>)', r'{}\1'.format(gif_section)),
            ]
            
            modified = False
            for pattern, replacement in patterns:
                if re.search(pattern, content, re.DOTALL):
                    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
                    modified = True
                    break
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {file_path} - GIF已添加")
                updated_count += 1
            else:
                print(f"⚠️  {file_path} - 未找到合适位置")
                
        except FileNotFoundError:
            print(f"❌ {file_path} - 文件不存在")
        except Exception as e:
            print(f"❌ {file_path} - 错误: {e}")
    
    return updated_count

def main():
    print("=" * 80)
    print("📸 在首页添加VaultCaddy演示GIF")
    print("=" * 80)
    print()
    
    count = add_gif_to_index()
    
    print()
    print("=" * 80)
    print(f"✅ 已在 {count} 个首页添加GIF")
    print("=" * 80)

if __name__ == "__main__":
    main()
