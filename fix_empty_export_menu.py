#!/usr/bin/env python3
"""
🔥 修复 Export 菜单内容为空的问题

问题：菜单打开但没有内容
原因：可能 window.currentDocument 为空或文档类型不匹配
解决：添加详细调试和默认内容
"""

import os
import re

def add_debug_to_update_function():
    """在 updateExportMenuForDocumentDetail 函数中添加调试"""
    
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
        
        # 在 updateExportMenuForDocumentDetail 函数开始处添加调试
        pattern = r"(function updateExportMenuForDocumentDetail\(\) \{)"
        replacement = r"\1\n            console.log('🔧 updateExportMenuForDocumentDetail 被调用');"
        
        content = re.sub(pattern, replacement, content)
        
        # 在设置 innerHTML 后添加调试
        pattern = r"(menu\.innerHTML = menuHTML;)"
        replacement = r"\1\n            console.log('📋 菜单 HTML 已设置, 长度:', menuHTML.length);\n            console.log('📋 菜单内容预览:', menuHTML.substring(0, 200));"
        
        content = re.sub(pattern, replacement, content)
        
        # 在 docType 判断后添加调试
        pattern = r"(console\.log\('📄 Export Menu - DocumentType:', docType\);)"
        replacement = r"\1\n            console.log('📄 文档对象:', window.currentDocument);"
        
        content = re.sub(pattern, replacement, content)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加调试到 {html_file}")

def add_fallback_content():
    """添加备用内容，以防文档类型不匹配"""
    
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
        
        # 查找 updateExportMenuForDocumentDetail 函数中的最后一个 menuHTML += '</div>';
        # 在它之前添加一个检查
        
        pattern = r"(menuHTML \+= '</div>';)\s+(menu\.innerHTML = menuHTML;)"
        replacement = r"""\1
            
            // 🔥 检查是否生成了内容
            if (menuHTML.trim() === '<div style="padding: 0.5rem 0; background: #ffffff;"></div>' || menuHTML.length < 100) {
                console.warn('⚠️ 菜单内容为空，添加默认选项');
                menuHTML = `
                    <div style="padding: 1rem;">
                        <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">Export Options</h3>
                        <button onclick="exportDocument('csv')" style="width: 100%; padding: 0.75rem; margin-bottom: 0.5rem; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 6px; text-align: left;">
                            <i class="fas fa-file-csv" style="color: #10b981; margin-right: 0.5rem;"></i>
                            Standard CSV
                        </button>
                        <button onclick="exportDocument('json')" style="width: 100%; padding: 0.75rem; margin-bottom: 0.5rem; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 6px; text-align: left;">
                            <i class="fas fa-file-code" style="color: #3b82f6; margin-right: 0.5rem;"></i>
                            JSON Format
                        </button>
                        <button onclick="closeExportMenu()" style="width: 100%; padding: 0.75rem; margin-top: 1rem; border: none; background: #ef4444; color: white; cursor: pointer; border-radius: 6px;">
                            Close
                        </button>
                    </div>
                `;
            }
            
            \2"""
        
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加备用内容到 {html_file}")

def main():
    print("🔧 修复 Export 菜单内容为空问题...\n")
    
    print("=" * 60)
    print("第 1 步：添加详细调试")
    print("=" * 60)
    add_debug_to_update_function()
    
    print("\n" + "=" * 60)
    print("第 2 步：添加备用内容")
    print("=" * 60)
    add_fallback_content()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• 添加了详细的调试信息")
    print("• 添加了备用内容（如果菜单为空）")
    print("• 确保菜单至少显示基本的导出选项")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存")
    print("2. 刷新页面")
    print("3. 打开控制台（F12）")
    print("4. 点击 Export 按钮")
    print("5. 查看控制台输出：")
    print("   - 🔧 updateExportMenuForDocumentDetail 被调用")
    print("   - 📄 Export Menu - DocumentType: xxx")
    print("   - 📋 菜单 HTML 已设置, 长度: xxx")
    
    print("\n💡 预期结果：")
    print("• 如果文档类型正确，显示对应的导出选项")
    print("• 如果文档类型不匹配或为空，显示默认的 CSV/JSON 选项")
    print("• 菜单至少有基本内容，不会是空白")

if __name__ == '__main__':
    main()

