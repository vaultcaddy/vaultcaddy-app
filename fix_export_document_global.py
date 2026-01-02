#!/usr/bin/env python3
"""
🔧 修复 exportDocument 函数的全局暴露

问题：exportDocument 函数存在但未暴露到 window 对象
解决：添加 window.exportDocument = exportDocument;
"""

import os

def fix_export_document_global():
    """确保 exportDocument 函数暴露到全局作用域"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已暴露
    if 'window.exportDocument = exportDocument' in content:
        print("ℹ️  exportDocument 已暴露到全局作用域")
        return False
    
    # 找到 exportDocument 函数定义
    if 'async function exportDocument(format)' not in content:
        print("❌ 未找到 exportDocument 函数定义")
        return False
    
    # 在函数定义后添加全局暴露
    # 找到函数结束位置（函数定义后的第一个完整的闭合 }）
    pattern = 'async function exportDocument(format) {'
    func_start = content.find(pattern)
    
    if func_start == -1:
        print("❌ 未找到函数定义位置")
        return False
    
    # 找到函数结束的 }
    # 从函数定义开始查找，找到匹配的闭合括号
    brace_count = 0
    i = func_start + len(pattern)
    func_end = -1
    
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            if brace_count == 0:
                func_end = i + 1
                break
            brace_count -= 1
        i += 1
    
    if func_end == -1:
        print("❌ 未找到函数结束位置")
        return False
    
    # 在函数结束后添加全局暴露
    expose_code = '\n\n// 暴露到全局作用域\nwindow.exportDocument = exportDocument;\n'
    
    content = content[:func_end] + expose_code + content[func_end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已将 exportDocument 暴露到全局作用域")
    return True

def main():
    print("🔧 修复 exportDocument 全局暴露...\n")
    
    print("=" * 60)
    print("检查并修复 document-detail-new.js")
    print("=" * 60)
    
    fixed = fix_export_document_global()
    
    print("\n" + "=" * 60)
    if fixed:
        print("✅ 修复完成！")
    else:
        print("ℹ️  无需修复或修复失败")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• 将 exportDocument 函数暴露到 window 对象")
    print("• 确保 HTML 中的 onclick 事件能够调用该函数")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存（Ctrl+Shift+Delete）")
    print("2. 访问 document-detail 页面")
    print("3. 打开控制台，输入: typeof window.exportDocument")
    print("4. 应该显示: 'function'")
    print("5. 点击 Export 按钮测试")

if __name__ == '__main__':
    main()

