#!/usr/bin/env python3
"""
🔥 恢复到今天16:00版本 + 删除Export功能

恢复到：2026-01-03 16:23:00
然后删除所有Export相关功能
"""

import os
import subprocess
import re

def restore_to_1600():
    """恢复到今天16:00版本"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 使用今天16:23的 commit
    commit_hash = '543c43f276fbabba15397aab35e0c4a2b42012e5'
    
    for file in files:
        try:
            cmd = f'git show {commit_hash}:{file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                print(f"✅ 已恢复 {file} 到 16:23 版本")
            else:
                print(f"⚠️ 未找到 {file} 在该版本")
        except Exception as e:
            print(f"❌ 恢复 {file} 失败: {e}")

def remove_export_completely():
    """完全删除Export功能"""
    
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
        
        original_length = len(content)
        
        # 1. 删除Export按钮HTML
        content = re.sub(
            r'<div class="export-dropdown"[^>]*>.*?</div>\s*(?:<!--.*?-->)?',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'<button[^>]*onclick[^>]*toggleExportMenu[^>]*>.*?</button>',
            '',
            content,
            flags=re.DOTALL
        )
        print("✅ 删除Export按钮")
        
        # 2. 删除所有Export JavaScript函数
        content = re.sub(
            r'window\.closeExportMenu\s*=\s*function.*?\};',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'window\.toggleExportMenu\s*=\s*function.*?\};',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'function\s+updateExportMenuContent\s*\(.*?\).*?(?=\s*function|\s*window\.\w+|\s*</script>)',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'window\.exportDocuments\s*=\s*async\s*function.*?\};',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'async\s+function\s+exportByType.*?(?=\s*function|\s*window\.\w+|\s*</script>)',
            '',
            content,
            flags=re.DOTALL
        )
        print("✅ 删除Export JavaScript函数")
        
        # 3. 删除Export Menu HTML元素
        content = re.sub(
            r'<div[^>]*id\s*=\s*["\']exportMenu["\'][^>]*>.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'<div[^>]*id\s*=\s*["\']exportMenuOverlay["\'][^>]*>.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )
        print("✅ 删除Export Menu元素")
        
        # 4. 删除Export相关注释和日志
        content = re.sub(r'console\.log\([^)]*[Ee]xport[^)]*\);?', '', content)
        content = re.sub(r'//.*?[Ee]xport.*?\n', '\n', content)
        content = re.sub(r'<!-- .*?[Ee]xport.*?-->', '', content, flags=re.DOTALL)
        
        # 5. 清理多余空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        deleted = original_length - len(content)
        print(f"✅ 总共删除 {deleted} 字节")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 恢复到今天16:00版本 + 删除Export\n")
    
    print("=" * 60)
    print("第1步：恢复到今天16:23版本")
    print("=" * 60)
    restore_to_1600()
    
    print("\n" + "=" * 60)
    print("第2步：删除Export功能")
    print("=" * 60)
    remove_export_completely()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成：")
    print("• ✅ 恢复到今天16:23版本")
    print("• ✅ 删除Export按钮")
    print("• ✅ 删除所有Export函数")
    print("• ✅ 删除Export Menu元素")
    
    print("\n🚀 请刷新页面测试！")

if __name__ == '__main__':
    main()

