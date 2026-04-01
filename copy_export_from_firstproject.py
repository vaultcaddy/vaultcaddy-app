#!/usr/bin/env python3
"""
🔥 将 firstproject.html 的 Export 功能完全复制到 document-detail.html

策略：
1. 保持 document-detail.html 的 Export 按钮样式
2. 但替换整个 toggleExportMenu 和相关函数
3. 使其工作方式与 firstproject.html 完全一样
"""

import os
import re

def copy_export_functions_from_firstproject():
    """从 firstproject.html 复制 Export 相关函数"""
    
    # 读取 firstproject.html 的 Export 函数
    with open('en/firstproject.html', 'r', encoding='utf-8') as f:
        firstproject_content = f.read()
    
    # 提取关键函数
    # 1. toggleExportMenu
    # 2. closeExportMenu  
    # 3. updateExportMenuContent
    # 4. exportDocuments
    # 5. exportByType
    
    # 查找 toggleExportMenu 函数
    toggle_start = firstproject_content.find('window.toggleExportMenu = function()')
    if toggle_start == -1:
        print("❌ 未找到 toggleExportMenu 函数")
        return None
    
    # 找到函数结束（匹配的闭合括号）
    brace_count = 0
    i = toggle_start
    started = False
    func_end = -1
    
    while i < len(firstproject_content):
        if firstproject_content[i] == '{':
            brace_count += 1
            started = True
        elif firstproject_content[i] == '}':
            brace_count -= 1
            if started and brace_count == 0:
                # 找到匹配的 };
                if i + 1 < len(firstproject_content) and firstproject_content[i+1] == ';':
                    func_end = i + 2
                else:
                    func_end = i + 1
                break
        i += 1
    
    if func_end == -1:
        print("❌ 未找到函数结束")
        return None
    
    toggle_export_menu = firstproject_content[toggle_start:func_end]
    
    # 也需要提取其他相关函数
    # closeExportMenu
    close_start = firstproject_content.find('window.closeExportMenu = function()')
    if close_start != -1:
        brace_count = 0
        i = close_start
        started = False
        close_end = -1
        
        while i < len(firstproject_content):
            if firstproject_content[i] == '{':
                brace_count += 1
                started = True
            elif firstproject_content[i] == '}':
                brace_count -= 1
                if started and brace_count == 0:
                    close_end = i + 2 if firstproject_content[i+1:i+2] == ';' else i + 1
                    break
            i += 1
        
        close_export_menu = firstproject_content[close_start:close_end] if close_end != -1 else ""
    else:
        close_export_menu = ""
    
    print(f"✅ 已提取 toggleExportMenu ({len(toggle_export_menu)} 字符)")
    print(f"✅ 已提取 closeExportMenu ({len(close_export_menu)} 字符)")
    
    return {
        'toggleExportMenu': toggle_export_menu,
        'closeExportMenu': close_export_menu
    }

def replace_export_in_document_detail():
    """替换 document-detail.html 的 Export 函数"""
    
    functions = copy_export_functions_from_firstproject()
    if not functions:
        return
    
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
        
        # 找到并替换 toggleExportMenu 函数
        # 查找现有的 window.toggleExportMenu = function
        pattern = r'window\.toggleExportMenu = function.*?\};'
        
        # 使用更安全的方法：找到函数开始和结束
        toggle_start_marker = 'window.toggleExportMenu = function'
        if toggle_start_marker in content:
            start_pos = content.find(toggle_start_marker)
            
            # 找到匹配的闭合
            brace_count = 0
            i = start_pos
            started = False
            end_pos = -1
            
            while i < len(content):
                if content[i] == '{':
                    brace_count += 1
                    started = True
                elif content[i] == '}':
                    brace_count -= 1
                    if started and brace_count == 0:
                        # 包括 };
                        end_pos = i + 2 if content[i+1:i+2] == ';' else i + 1
                        break
                i += 1
            
            if end_pos != -1:
                # 替换旧函数
                old_func = content[start_pos:end_pos]
                new_content = content[:start_pos] + functions['toggleExportMenu'] + content[end_pos:]
                
                # 如果有 closeExportMenu，也替换
                if functions['closeExportMenu']:
                    close_marker = 'window.closeExportMenu = function'
                    if close_marker in new_content:
                        start_pos = new_content.find(close_marker)
                        brace_count = 0
                        i = start_pos
                        started = False
                        end_pos = -1
                        
                        while i < len(new_content):
                            if new_content[i] == '{':
                                brace_count += 1
                                started = True
                            elif new_content[i] == '}':
                                brace_count -= 1
                                if started and brace_count == 0:
                                    end_pos = i + 2 if new_content[i+1:i+2] == ';' else i + 1
                                    break
                            i += 1
                        
                        if end_pos != -1:
                            new_content = new_content[:start_pos] + functions['closeExportMenu'] + new_content[end_pos:]
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 已更新 {html_file}")
            else:
                print(f"⚠️  {html_file} 未找到函数结束")
        else:
            print(f"⚠️  {html_file} 未找到 toggleExportMenu")

def main():
    print("🔥 复制 firstproject.html 的 Export 功能...\n")
    
    print("=" * 60)
    print("步骤 1: 从 firstproject.html 提取 Export 函数")
    print("=" * 60)
    
    replace_export_in_document_detail()
    
    print("\n" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📋 说明：")
    print("• document-detail.html 现在使用与 firstproject.html 相同的 Export 逻辑")
    print("• 需要先选中文档（勾选checkbox）才能导出")
    print("• Export 按钮的样式保持不变")
    
    print("\n⚠️  重要：")
    print("• document-detail 页面通常只显示单个文档")
    print("• 可能需要调整逻辑以自动选中当前文档")
    print("• 或者创建一个适配版本")

if __name__ == '__main__':
    main()

