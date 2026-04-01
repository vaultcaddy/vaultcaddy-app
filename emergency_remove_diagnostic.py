#!/usr/bin/env python3
"""
🔥 紧急：完全移除诊断代码

直接删除从 setTimeout 到 }, 2000); 的整块代码
"""

import os
import re

def emergency_remove_diagnostic():
    """紧急移除诊断代码"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n处理 {html_file}:")
        print("=" * 50)
        
        # 找到并删除整个 setTimeout 块（从 "// 🔍 终极诊断" 到 "}, 2000);"）
        pattern = r"// 🔍 终极诊断：找出为什么点击不工作\s*setTimeout\(function\(\) \{.*?\}, 2000\);\s*"
        
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            print(f"找到 {len(matches)} 个诊断块，删除中...")
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            print("✅ 已删除诊断代码")
        else:
            print("⚠️ 未找到诊断代码")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已处理 {html_file}")

def main():
    print("🔥 紧急移除诊断代码\n")
    
    print("=" * 60)
    print("开始移除...")
    print("=" * 60)
    
    emergency_remove_diagnostic()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n🚀 请刷新页面！")
    print("• 不应该再有自动弹出的红色框")
    print("• 点击 Export 按钮测试")

if __name__ == '__main__':
    main()

