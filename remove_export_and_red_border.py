#!/usr/bin/env python3
"""
🔥 删除Export按钮、相关内容和红色框

删除：
1. Export按钮（HTML）
2. 所有Export相关的JavaScript函数
3. Export Menu元素
4. 红色边框（调试样式）
"""

import os
import re

def remove_export_and_red_border():
    """删除Export功能和红色边框"""
    
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
            r'<div class="export-dropdown"[^>]*>.*?</div>',
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
        
        # 2. 删除所有Export相关的JavaScript函数
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
        print("✅ 删除Export函数")
        
        # 3. 删除Export Menu HTML元素
        content = re.sub(
            r'<div[^>]*class\s*=\s*["\']export-menu["\'][^>]*>.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )
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
        
        # 4. 删除红色边框（调试样式）
        # 删除 border: 5px solid red 或类似的调试样式
        content = re.sub(
            r'border:\s*\d+px\s+solid\s+red;?',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'border-color:\s*red;?',
            '',
            content,
            flags=re.IGNORECASE
        )
        # 删除包含红色边框的完整样式属性
        content = re.sub(
            r'style\s*=\s*["\'][^"\']*border[^"\']*red[^"\']*["\']',
            '',
            content,
            flags=re.IGNORECASE
        )
        print("✅ 删除红色边框")
        
        # 5. 删除Export相关的注释和console.log
        content = re.sub(r'console\.log\([^)]*[Ee]xport[^)]*\);?', '', content)
        content = re.sub(r'//.*?[Ee]xport.*?\n', '\n', content)
        content = re.sub(r'<!-- .*?[Ee]xport.*?-->', '', content, flags=re.DOTALL)
        
        # 6. 删除包含 "Export" 的 event listener
        content = re.sub(
            r'document\.addEventListener\([^)]*toggleExportMenu[^)]*\).*?\}\);',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'exportBtn\.addEventListener\([^)]*\).*?\}\);',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 7. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        deleted = original_length - len(content)
        print(f"✅ 总共删除 {deleted} 字节")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 删除Export按钮、相关内容和红色框\n")
    
    print("=" * 60)
    print("开始删除...")
    print("=" * 60)
    
    remove_export_and_red_border()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已删除：")
    print("• ✅ Export 按钮")
    print("• ✅ 所有 Export 函数")
    print("• ✅ Export Menu 元素")
    print("• ✅ 红色边框（调试样式）")
    print("• ✅ Export 相关注释和日志")
    
    print("\n🚀 请刷新页面！")
    print("• Export 按钮应该消失")
    print("• 红色框应该消失")
    print("• 页面功能正常")

if __name__ == '__main__':
    main()

