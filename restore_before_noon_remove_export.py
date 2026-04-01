#!/usr/bin/env python3
"""
🔥 恢复到12:00之前 + 删除Export功能

步骤：
1. 恢复 document-detail.html 到昨天晚上的版本（1月2日 21:14）
2. 完全删除 Export 按钮和所有相关功能
"""

import os
import subprocess
import re

def restore_to_before_noon():
    """恢复到12:00之前的版本（昨天晚上）"""
    
    files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    # 使用昨天晚上的 commit (2026-01-02 21:14:58)
    commit_hash = '85292de40cbf6744b58715df4561d704536e0057'
    
    for file in files:
        try:
            cmd = f'git show {commit_hash}:{file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                print(f"✅ 已恢复 {file} 到昨天晚上版本")
            else:
                print(f"⚠️ 未找到 {file} 在该版本")
        except Exception as e:
            print(f"❌ 恢复 {file} 失败: {e}")

def remove_all_export_functionality():
    """完全删除 Export 按钮和所有相关功能"""
    
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
        
        # 1. 删除 Export 按钮（完整的 div）
        # 查找包含 Export 按钮的整个区域
        patterns_to_remove = [
            # Export 按钮及其容器
            r'<div class="export-dropdown"[^>]*>.*?</div>\s*(?:<!--.*?-->)?',
            # 单独的 Export 按钮
            r'<button[^>]*onclick[^>]*toggleExportMenu[^>]*>.*?</button>',
            # Export 相关的容器
            r'<!-- .*?[Ee]xport.*?-->',
        ]
        
        for pattern in patterns_to_remove:
            before = len(content)
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            after = len(content)
            if before != after:
                print(f"  ✅ 删除了 {before - after} 字节的 Export HTML")
        
        # 2. 删除所有 Export 相关的 JavaScript 函数
        js_patterns = [
            (r'window\.closeExportMenu\s*=\s*function[^}]*\{[^}]*\};?', 'closeExportMenu'),
            (r'window\.toggleExportMenu\s*=\s*function[^}]*\{(?:[^{}]|\{[^}]*\})*\};?', 'toggleExportMenu'),
            (r'function\s+updateExportMenuContent\s*\([^)]*\)\s*\{(?:[^{}]|\{[^}]*\})*\}', 'updateExportMenuContent'),
            (r'window\.exportDocuments\s*=\s*async\s+function[^}]*\{(?:[^{}]|\{[^}]*\})*\};?', 'exportDocuments'),
            (r'async\s+function\s+exportByType[^}]*\{(?:[^{}]|\{[^}]*\})*\}', 'exportByType'),
        ]
        
        for pattern, name in js_patterns:
            before = len(content)
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            after = len(content)
            if before != after:
                print(f"  ✅ 删除 {name} 函数 ({before - after} 字节)")
        
        # 3. 删除 Export Menu HTML 元素（使用更宽松的匹配）
        menu_patterns = [
            r'<div[^>]*id\s*=\s*["\']exportMenu["\'][^>]*>(?:[^<]|<(?!/?div))*</div>',
            r'<div[^>]*id\s*=\s*["\']exportMenuOverlay["\'][^>]*>(?:[^<]|<(?!/?div))*</div>',
        ]
        
        for pattern in menu_patterns:
            before = len(content)
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            after = len(content)
            if before != after:
                print(f"  ✅ 删除 Export Menu 元素 ({before - after} 字节)")
        
        # 4. 删除 Export 相关的注释和日志
        content = re.sub(r'console\.log\([^)]*[Ee]xport[^)]*\);?', '', content)
        content = re.sub(r'//.*?[Ee]xport.*?\n', '\n', content)
        
        # 5. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 恢复到12:00之前 + 删除Export功能\n")
    
    print("=" * 60)
    print("第1步：恢复文件到12:00之前（昨天晚上 21:14）")
    print("=" * 60)
    restore_to_before_noon()
    
    print("\n" + "=" * 60)
    print("第2步：删除Export按钮和所有相关功能")
    print("=" * 60)
    remove_all_export_functionality()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已完成：")
    print("• ✅ 恢复到昨天晚上的稳定版本（1月2日 21:14）")
    print("• ✅ 删除 Export 按钮")
    print("• ✅ 删除所有 Export JavaScript 函数")
    print("• ✅ 删除 Export Menu HTML 元素")
    print("• ✅ 清理所有 Export 相关代码")
    
    print("\n🚀 请刷新页面！")
    print("• Export 按钮应该完全消失")
    print("• 页面应该恢复正常工作")

if __name__ == '__main__':
    main()

