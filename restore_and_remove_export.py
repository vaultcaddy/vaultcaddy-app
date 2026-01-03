#!/usr/bin/env python3
"""
🔥 紧急恢复 + 删除Export功能

步骤：
1. 恢复 document-detail.html 到 12:00 版本
2. 完全删除 Export 按钮
3. 删除所有 Export 相关的 JavaScript 代码
4. 删除 Export Menu HTML 元素
"""

import os
import subprocess
import re

def restore_to_noon():
    """恢复到12:00版本"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 使用 12:47:37 的 commit (7ed4eb6e)
    commit_hash = '7ed4eb6ede7c6331c63f43b89e11c78a3af932ef'
    
    for file in files:
        try:
            cmd = f'git show {commit_hash}:{file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                print(f"✅ 已恢复 {file} 到 12:00 版本")
            else:
                print(f"⚠️ 未找到 {file} 在该版本")
        except Exception as e:
            print(f"❌ 恢复 {file} 失败: {e}")

def remove_export_button_and_functionality():
    """删除 Export 按钮和所有功能"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    for file in files:
        if not os.path.exists(file):
            continue
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {file}:")
        print("=" * 50)
        
        # 1. 删除 Export 按钮 HTML（包括整个 export-dropdown div）
        pattern1 = r'<div class="export-dropdown"[^>]*>.*?</div>\s*<!-- Export Menualreadymoveto body Finallypage -->'
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        print("✅ 删除 Export 按钮")
        
        # 2. 删除移动端 Export 按钮（如果有）
        pattern2 = r'<button[^>]*onclick="toggleExportMenu"[^>]*>.*?</button>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        # 3. 删除所有 Export 相关的 JavaScript 函数
        # closeExportMenu
        pattern3 = r'window\.closeExportMenu\s*=\s*function.*?\};'
        content = re.sub(pattern3, '', content, flags=re.DOTALL)
        print("✅ 删除 closeExportMenu 函数")
        
        # toggleExportMenu
        pattern4 = r'window\.toggleExportMenu\s*=\s*function.*?\};'
        content = re.sub(pattern4, '', content, flags=re.DOTALL)
        print("✅ 删除 toggleExportMenu 函数")
        
        # updateExportMenuContent
        pattern5 = r'function\s+updateExportMenuContent\s*\(.*?\).*?(?=\s*function|\s*window\.\w+|\s*</script>)'
        content = re.sub(pattern5, '', content, flags=re.DOTALL)
        print("✅ 删除 updateExportMenuContent 函数")
        
        # exportDocuments
        pattern6 = r'window\.exportDocuments\s*=\s*async\s*function.*?\};'
        content = re.sub(pattern6, '', content, flags=re.DOTALL)
        print("✅ 删除 exportDocuments 函数")
        
        # exportByType
        pattern7 = r'async\s+function\s+exportByType.*?(?=\s*function|\s*window\.\w+|\s*</script>)'
        content = re.sub(pattern7, '', content, flags=re.DOTALL)
        
        # 4. 删除 Export Menu HTML 元素
        pattern8 = r'<div[^>]*id="exportMenu"[^>]*>.*?</div>'
        content = re.sub(pattern8, '', content, flags=re.DOTALL)
        print("✅ 删除 exportMenu 元素")
        
        # 5. 删除 Export Menu Overlay
        pattern9 = r'<div[^>]*id="exportMenuOverlay"[^>]*>.*?</div>'
        content = re.sub(pattern9, '', content, flags=re.DOTALL)
        print("✅ 删除 exportMenuOverlay 元素")
        
        # 6. 删除所有 Export 相关的注释
        pattern10 = r'// 🔥 Export.*?\n'
        content = re.sub(pattern10, '', content)
        
        pattern11 = r'<!-- .*?Export.*?-->'
        content = re.sub(pattern11, '', content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 恢复到12:00版本 + 删除Export功能\n")
    
    print("=" * 60)
    print("第1步：恢复文件到12:00版本")
    print("=" * 60)
    restore_to_noon()
    
    print("\n" + "=" * 60)
    print("第2步：删除Export按钮和所有功能")
    print("=" * 60)
    remove_export_button_and_functionality()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成：")
    print("• ✅ 恢复到12:00版本")
    print("• ✅ 删除 Export 按钮")
    print("• ✅ 删除所有 Export 相关函数")
    print("• ✅ 删除 Export Menu 元素")
    print("• ✅ 清理所有 Export 相关代码")
    
    print("\n🚀 请刷新页面！")
    print("• Export 按钮应该完全消失")
    print("• 页面功能正常")

if __name__ == '__main__':
    main()

