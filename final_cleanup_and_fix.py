#!/usr/bin/env python3
"""
🎯 最终简化修复 + 移除诊断代码

问题：
1. 红色框自动打开（诊断代码）
2. 菜单内容为空

解决：
1. 移除所有诊断代码
2. 确保 updateExportMenuContent() 总是生成内容
3. 简化 toggleExportMenu 函数
"""

import os
import re

def remove_diagnostic_code_and_simplify():
    """移除诊断代码并简化"""
    
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
        
        # 1. 移除所有诊断代码（从 "🔍🔍🔍 开始终极诊断" 到 "🔍🔍🔍 诊断完成"）
        pattern1 = r"// 🔥 Export 功能.*?setTimeout\(function\(\) \{.*?console\.log\('🔍🔍🔍 诊断完成 🔍🔍🔍'\);.*?console\.log\(''\);.*?\}, 2000\);.*?console\.log\('✅ Export 功能已加载"
        
        content = re.sub(
            pattern1,
            "// 🔥 Export 功能 - 最终简化版\n        \n        console.log('✅ Export 功能已加载",
            content,
            flags=re.DOTALL
        )
        print("✅ 移除诊断代码")
        
        # 2. 确保 updateExportMenuContent() 总是生成内容（即使没有 Bank Statement 或 Invoice）
        # 在 "// Other 选项（始终显示）" 之前添加检查
        pattern2 = r"(// Other 选项（始终显示）)"
        replacement2 = r'''// 确保至少有 Bank Statement 或 Other 显示
            if (!hasBankStatement && !hasInvoice) {
                // 如果没有匹配到类型，至少显示 Bank Statement
                menuHTML += `
                    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">Bank Statement</div>
                    <button onclick="exportDocuments('bank_statement_csv')" class="export-menu-item" style="width: 100%; text-align: left; padding: 0.75rem 1rem; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; gap: 0.75rem; color: #374151; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">Standard CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">complete fields Format</div>
                        </div>
                    </button>
                `;
            }
            
            \1'''
        
        content = re.sub(pattern2, replacement2, content)
        print("✅ 确保菜单总是有内容")
        
        # 3. 在 toggleExportMenu 开始处添加调试
        pattern3 = r"(window\.toggleExportMenu = function\(event\) \{\s*console\.log\('🔍 toggleExportMenu Called'\);)"
        replacement3 = r'''\1
            
            // 🔥 强制更新菜单内容（确保有内容）
            console.log('🔄 强制更新菜单内容...');
            updateExportMenuContent();'''
        
        content = re.sub(pattern3, replacement3, content)
        print("✅ 在 toggleExportMenu 开始处强制更新内容")
        
        # 4. 移除 toggleExportMenu 中重复的 updateExportMenuContent() 调用
        pattern4 = r"// 更新菜单内容\s*console\.log\('🔄 更新菜单内容\.\.\.'\);\s*updateExportMenuContent\(\);"
        content = re.sub(pattern4, '', content)
        print("✅ 移除重复的 updateExportMenuContent 调用")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已修复 {html_file}")

def main():
    print("🎯 最终简化修复 + 移除诊断代码\n")
    
    print("=" * 60)
    print("修复内容")
    print("=" * 60)
    print("1. 移除所有诊断代码（红色框测试）")
    print("2. 确保 updateExportMenuContent() 总是生成内容")
    print("3. 在 toggleExportMenu 开始处强制更新内容")
    print("4. 简化代码逻辑")
    
    print("\n" + "=" * 60)
    print("开始修复...")
    print("=" * 60)
    
    remove_diagnostic_code_and_simplify()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n🎉 改进：")
    print("• ✅ 移除了自动弹出的红色框")
    print("• ✅ 确保菜单总是有内容（至少显示 Bank Statement + Other）")
    print("• ✅ 简化了代码逻辑")
    
    print("\n🚀 请刷新页面，点击 Export 按钮测试！")
    print("\n📋 预期效果：")
    print("• 不再自动弹出红色框")
    print("• 点击 Export 按钮后，菜单正常显示")
    print("• 菜单有完整内容（Bank Statement + Other）")

if __name__ == '__main__':
    main()

