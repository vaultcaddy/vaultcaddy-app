#!/usr/bin/env python3
"""
🔥 只删除Export按钮和红色框

只删除：
1. Export按钮的HTML元素
2. 红色边框样式

不删除：
- JavaScript函数（保留所有功能代码）
- Export Menu元素（保留HTML结构）
- 其他任何代码
"""

import os
import re

def remove_only_button_and_red_border():
    """只删除按钮和红色边框"""
    
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
        
        # 1. 只删除Export按钮 - 找到包含"Export"文本且有onclick="toggleExportMenu"的按钮
        # 使用更精确的匹配，只删除Export按钮，不影响其他内容
        button_pattern = r'<button[^>]*class="export-button"[^>]*>.*?</button>'
        if re.search(button_pattern, content, re.DOTALL):
            content = re.sub(button_pattern, '', content, flags=re.DOTALL)
            print("✅ 删除Export按钮（方法1）")
        else:
            # 如果上面的模式没找到，尝试其他模式
            button_pattern2 = r'<button[^>]*onclick="toggleExportMenu\(event\)"[^>]*>.*?</button>'
            if re.search(button_pattern2, content, re.DOTALL):
                content = re.sub(button_pattern2, '', content, flags=re.DOTALL)
                print("✅ 删除Export按钮（方法2）")
            else:
                print("⚠️ 未找到Export按钮")
        
        # 2. 删除红色边框样式 - 只删除样式，不删除HTML元素
        # 删除 style 属性中的 border: ...px solid red
        content = re.sub(
            r'border:\s*\d+px\s+solid\s+red\s*;?',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # 删除 border-color: red
        content = re.sub(
            r'border-color:\s*red\s*;?',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # 清理空的 style 属性
        content = re.sub(r'style\s*=\s*["\']["\']', '', content)
        content = re.sub(r'style\s*=\s*["\']\s*["\']', '', content)
        
        print("✅ 删除红色边框样式")
        
        # 3. 清理多余的空行（只删除连续3个以上的空行）
        content = re.sub(r'\n\s*\n\s*\n\s*\n+', '\n\n', content)
        
        deleted = original_length - len(content)
        print(f"✅ 总共删除 {deleted} 字节")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已完成 {file}")

def main():
    print("🔥 只删除Export按钮和红色框\n")
    
    print("=" * 60)
    print("开始删除...")
    print("=" * 60)
    
    remove_only_button_and_red_border()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 已删除：")
    print("• ✅ Export 按钮（HTML）")
    print("• ✅ 红色边框样式")
    
    print("\n📋 保留：")
    print("• ✅ 所有 JavaScript 函数")
    print("• ✅ Export Menu HTML 元素")
    print("• ✅ 所有其他功能")
    
    print("\n🚀 请刷新页面！")
    print("• Export 按钮应该消失")
    print("• 红色框应该消失")
    print("• 页面功能应该正常")

if __name__ == '__main__':
    main()

