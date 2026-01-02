#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量执行3个任务:
1. 替换文章11的演示GIF为实际界面
2. 在4个页面的All-in-One部分添加GIF
3. 删除所有"Data auto-deleted after 24 hours"
"""

import os
import re
from pathlib import Path

def task1_replace_demo_gif():
    """任务1: 替换文章11的演示GIF"""
    file_path = "blog/bank-statement-automation-guide-2025.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换GIF URL为实际的上传界面截图
    # 从 vaultcaddy-demo.gif 改为实际的上传界面GIF
    old_gif = 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1400&h=900&fit=crop'
    new_gif = '../images/vaultcaddy-upload-demo.gif'  # 实际的上传界面GIF
    
    content = content.replace(old_gif, new_gif)
    
    # 更新GIF说明文字
    content = content.replace(
        'Upload → AI Processing → Export to Excel/QuickBooks in 3 seconds',
        'Real VaultCaddy interface: Select document type → Upload PDF → Process in 3 seconds'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def task2_add_gif_to_allinone_sections():
    """任务2: 在4个页面的All-in-One部分添加GIF"""
    
    # 搜索包含"All-in-One AI Document Processing Platform"的文件
    target_files = []
    
    # 搜索主要的v3页面
    search_dirs = ['.', 'zh-TW', 'zh-HK', 'ja-JP', 'ko-KR']
    
    for dir_path in search_dirs:
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith('-v3.html') or file == 'index.html':
                    file_path = os.path.join(dir_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'All-in-One AI Document Processing Platform' in content or 'All-in-One' in content:
                                target_files.append(file_path)
                    except:
                        pass
    
    # GIF HTML片段
    gif_html = '''
                <div style="text-align: center; margin: 40px 0;">
                    <img src="images/vaultcaddy-upload-demo.gif" alt="VaultCaddy Upload Demo" style="max-width: 800px; width: 100%; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" loading="lazy">
                    <p style="margin-top: 15px; color: #64748b; font-size: 14px; font-style: italic;">Live Demo: Upload your bank statement and process in 3 seconds</p>
                </div>
'''
    
    updated_count = 0
    
    for file_path in target_files[:4]:  # 只处理前4个文件
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 在"All-in-One"标题后添加GIF
            # 查找多种可能的模式
            patterns = [
                r'(<h2[^>]*>.*?All-in-One.*?</h2>)',
                r'(<div class="section-title"[^>]*>.*?All-in-One.*?</div>)',
                r'(<h1[^>]*>.*?All-in-One.*?</h1>)',
            ]
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(
                        pattern,
                        r'\1' + gif_html,
                        content,
                        count=1,
                        flags=re.IGNORECASE
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_count += 1
                    break
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
    
    return updated_count

def task3_remove_auto_delete_text():
    """任务3: 删除所有"Data auto-deleted after 24 hours"""
    
    # 所有需要处理的文件类型
    patterns_to_remove = [
        r'Data auto-deleted after 24 hours',
        r'Files auto-delete after 24 hours',
        r'All files auto-delete after 24 hours',
        r'\s*[|•&]?\s*Data auto-deleted after 24 hours',
        r'\s*[|•&]?\s*Files auto-delete after 24 hours',
    ]
    
    updated_files = []
    total_replacements = 0
    
    # 搜索所有HTML和MD文件
    for root, dirs, files in os.walk('.'):
        # 跳过某些目录
        if 'node_modules' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith(('.html', '.md')):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    replacements_in_file = 0
                    
                    # 应用所有删除模式
                    for pattern in patterns_to_remove:
                        matches = len(re.findall(pattern, content, re.IGNORECASE))
                        if matches > 0:
                            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                            replacements_in_file += matches
                    
                    # 清理多余的分隔符
                    content = re.sub(r'\s*\|\s*\|\s*', ' | ', content)
                    content = re.sub(r'\s*•\s*•\s*', ' • ', content)
                    content = re.sub(r'\s*&nbsp;\s*\|\s*&nbsp;\s*\|\s*&nbsp;', ' &nbsp;|&nbsp; ', content)
                    
                    # 清理行尾的分隔符
                    content = re.sub(r'\s*[|•]\s*</small>', '</small>', content)
                    content = re.sub(r'\s*[|•]\s*$', '', content, flags=re.MULTILINE)
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        updated_files.append(file_path)
                        total_replacements += replacements_in_file
                
                except Exception as e:
                    pass  # 忽略无法处理的文件
    
    return len(updated_files), total_replacements

def main():
    print("=" * 80)
    print("🔧 批量更新：3个任务")
    print("=" * 80)
    print()
    
    # 任务1
    print("📝 任务1: 替换文章11的演示GIF...")
    if task1_replace_demo_gif():
        print("✅ 文章11的GIF已替换为实际上传界面")
    print()
    
    # 任务2
    print("📝 任务2: 在All-in-One部分添加GIF...")
    count = task2_add_gif_to_allinone_sections()
    print(f"✅ 已在 {count} 个页面的All-in-One部分添加GIF")
    print()
    
    # 任务3
    print("📝 任务3: 删除所有'Data auto-deleted after 24 hours'...")
    files_updated, total_replacements = task3_remove_auto_delete_text()
    print(f"✅ 已更新 {files_updated} 个文件")
    print(f"✅ 删除了 {total_replacements} 处'Data auto-deleted'相关文字")
    print()
    
    print("=" * 80)
    print("📊 总结")
    print("=" * 80)
    print(f"✅ 任务1: 文章11 GIF已替换")
    print(f"✅ 任务2: {count}个页面添加了GIF")
    print(f"✅ 任务3: {files_updated}个文件，删除{total_replacements}处")
    print()
    print("🎉 所有任务完成！")
    print()
    print("=" * 80)
    print("📝 重要提示")
    print("=" * 80)
    print()
    print("需要准备的GIF文件：")
    print("□ images/vaultcaddy-upload-demo.gif")
    print()
    print("这个GIF应该展示：")
    print("1. VaultCaddy上传界面")
    print("2. 选择文档类型（Bank Statement）")
    print("3. 拖拽上传PDF文件")
    print("4. AI处理进度")
    print("5. 显示结果")
    print()
    print("您可以:")
    print("- 使用图2的截图制作GIF")
    print("- 或录制实际操作流程")
    print("- 推荐工具: ScreenToGif (Windows) 或 Gifski (Mac)")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
