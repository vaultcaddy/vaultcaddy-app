#!/usr/bin/env python3
"""
🔥 强制修复 Export 菜单内容为空的问题

问题：菜单能打开但没有内容
原因：生成的 menuHTML 为空
解决：强制添加默认内容
"""

import os
import re

def force_add_menu_content():
    """强制在菜单显示时添加内容"""
    
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
        
        # 在 updateExportMenuForDocumentDetail 函数的最开始
        # 强制设置一个默认内容
        
        pattern = r'(function updateExportMenuForDocumentDetail\(\) \{[^\n]*\n[^\n]*console\.log[^\n]*\n[^\n]*const menu = document\.getElementById\(\'exportMenu\'\);[^\n]*\n[^\n]*if \(!menu\) return;)'
        
        replacement = r'''\1
            
            // 🔥 强制设置默认内容（调试用）
            console.log('🔥 强制设置默认菜单内容');
            menu.innerHTML = `
                <div style="padding: 1.5rem;">
                    <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem; color: #1f2937;">Export Options</h3>
                    <p style="margin-bottom: 1rem; font-size: 0.9rem; color: #6b7280;">Select export format:</p>
                    
                    <button onclick="exportDocument('bank_statement_csv')" style="width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #e5e7eb; background: white; cursor: pointer; border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">Standard CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">Complete fields format</div>
                        </div>
                    </button>
                    
                    <button onclick="exportDocument('xero_csv')" style="width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #e5e7eb; background: white; cursor: pointer; border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #2563eb; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">Xero CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">Xero official format</div>
                        </div>
                    </button>
                    
                    <button onclick="exportDocument('quickbooks_csv')" style="width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #e5e7eb; background: white; cursor: pointer; border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; transition: background 0.2s;">
                        <i class="fas fa-file-csv" style="color: #059669; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">QuickBooks CSV</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks official format</div>
                        </div>
                    </button>
                    
                    <button onclick="exportDocument('qbo')" style="width: 100%; text-align: left; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border: 1px solid #e5e7eb; background: white; cursor: pointer; border-radius: 6px; display: flex; align-items: center; gap: 0.75rem; transition: background 0.2s;">
                        <i class="fas fa-cloud" style="color: #8b5cf6; width: 20px;"></i>
                        <div>
                            <div style="font-weight: 500;">QBO</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks Online</div>
                        </div>
                    </button>
                    
                    <button onclick="closeExportMenu()" style="width: 100%; padding: 0.75rem 1rem; margin-top: 1rem; border: none; background: #ef4444; color: white; cursor: pointer; border-radius: 6px; font-weight: 500;">
                        Close
                    </button>
                </div>
            `;
            console.log('✅ 默认菜单内容已设置');
            return;  // 直接返回，不执行后面的逻辑'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已添加强制内容到 {html_file}")
        else:
            print(f"⚠️  {html_file} 未找到匹配位置")
    
    print()

def main():
    print("🔥 强制修复 Export 菜单内容...\n")
    
    print("=" * 60)
    print("添加强制默认内容")
    print("=" * 60)
    
    force_add_menu_content()
    
    print("=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复策略：")
    print("• 在 updateExportMenuForDocumentDetail() 开始就强制设置内容")
    print("• 跳过所有条件判断")
    print("• 直接显示完整的导出选项")
    print("• 包含 CSV、Xero、QuickBooks、QBO 选项")
    
    print("\n🔍 验证步骤：")
    print("1. 刷新页面（不需要清除缓存）")
    print("2. 点击 Export 按钮")
    print("3. 应该立即看到完整的导出选项")
    
    print("\n💡 这是临时解决方案：")
    print("• 确保菜单一定有内容")
    print("• 之后可以根据文档类型优化显示")
    print("• 但现在先保证功能可用")

if __name__ == '__main__':
    main()

