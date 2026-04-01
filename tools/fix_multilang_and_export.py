#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复多语言混乱和Export菜单问题

问题1：document-detail.html中硬编码了中文，导致英文/日文/韩文版本显示中文
问题2：Export按钮可能存在运算符错误或菜单ID不匹配

作用：
1. 修复document-detail.html的lang属性
2. 移除所有硬编码中文
3. 修复Export相关的运算符错误
"""

import re
import os
from datetime import datetime

# 需要修复的文件
DOCUMENT_DETAIL_FILES = [
    ('en/document-detail.html', 'en'),
    ('jp/document-detail.html', 'ja'),
    ('kr/document-detail.html', 'ko'),
]

FIRSTPROJECT_FILES = [
    'en/firstproject.html',
    'jp/firstproject.html',
    'kr/firstproject.html',
    'firstproject.html'
]

def backup_file(filepath):
    """创建备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_multilang_fix_{timestamp}"
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 备份: {backup_path}")
        return True
    return False

def fix_document_detail_lang(filepath, lang_code):
    """修复document-detail.html的语言设置"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 修复: {filepath} (语言: {lang_code})")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 修复1：lang属性
    if lang_code == 'en':
        content = re.sub(r'<html lang="zh-TW">', '<html lang="en">', content)
        fixes.append('lang属性: zh-TW → en')
    elif lang_code == 'ja':
        content = re.sub(r'<html lang="zh-TW">', '<html lang="ja">', content)
        content = re.sub(r'<html lang="en">', '<html lang="ja">', content)
        fixes.append('lang属性 → ja')
    elif lang_code == 'ko':
        content = re.sub(r'<html lang="zh-TW">', '<html lang="ko">', content)
        content = re.sub(r'<html lang="en">', '<html lang="ko">', content)
        fixes.append('lang属性 → ko')
    
    # 修复2：硬编码中文确认对话框
    chinese_confirms = [
        (r"const confirmDelete = confirm\('確定要刪除此文檔嗎？此操作無法撤銷。'\);",
         "const confirmDelete = confirm(translations[currentLang]?.deleteConfirm || 'Are you sure you want to delete this document? This action cannot be undone.');"),
        (r"alert\('無法獲取文檔信息'\);",
         "alert(translations[currentLang]?.cannotGetDocInfo || 'Cannot get document information');"),
        (r"alert\('文檔刪除成功'\);",
         "alert(translations[currentLang]?.deleteSuccess || 'Document deleted successfully');"),
        (r"alert\('刪除失敗：' \+ error\.message\);",
         "alert((translations[currentLang]?.deleteFailed || 'Delete failed: ') + error.message);"),
    ]
    
    for pattern, replacement in chinese_confirms:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fixes.append(f'硬编码中文 → 翻译系统')
    
    # 修复3：运算符错误
    operator_fixes = [
        (r'if \(!projectId \| !documentId\)',
         'if (!projectId || !documentId)'),
        (r'if \(!docs \| docs\.length === 0\)',
         'if (!docs || docs.length === 0)'),
    ]
    
    for pattern, replacement in operator_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fixes.append(f'运算符: | → ||')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成！共 {len(fixes)} 处")
        for fix in fixes:
            print(f"  - {fix}")
        return True
    else:
        print(f"ℹ️  没有需要修复的内容")
        return False

def fix_export_operators(filepath):
    """修复firstproject.html中Export相关的运算符错误"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 修复Export: {filepath}")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fix_count = 0
    
    # Export相关的运算符修复
    export_fixes = [
        (r'if \(!docs \| docs\.length === 0\)',
         'if (!docs || docs.length === 0)'),
        (r'if \(!window\.BankStatementExport \| !window\.BankStatementExport\.',
         'if (!window.BankStatementExport || !window.BankStatementExport.'),
        (r'if \(!exportContent \| exportContent\.trim\(\) === \'\'\)',
         'if (!exportContent || exportContent.trim() === \'\')'),
    ]
    
    for pattern, replacement in export_fixes:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            fix_count += len(matches) if isinstance(matches, list) else 1
            print(f"  ✅ {pattern[:50]}... ({len(matches) if isinstance(matches, list) else 1}处)")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成！共 {fix_count} 处")
        return True
    else:
        print(f"ℹ️  没有需要修复的内容")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🔧 多语言混乱和Export菜单修复工具")
    print("=" * 70)
    print("\n修复内容:")
    print("1. ✅ document-detail.html lang属性")
    print("2. ✅ 移除硬编码中文文本")
    print("3. ✅ 修复运算符错误\n")
    
    fixed_detail = 0
    fixed_export = 0
    
    # 修复document-detail.html
    print("\n" + "=" * 70)
    print("第1部分：修复document-detail.html多语言问题")
    print("=" * 70)
    
    for filepath, lang_code in DOCUMENT_DETAIL_FILES:
        try:
            if fix_document_detail_lang(filepath, lang_code):
                fixed_detail += 1
        except Exception as e:
            print(f"❌ 修复失败: {e}")
    
    # 修复firstproject.html的Export
    print("\n" + "=" * 70)
    print("第2部分：修复firstproject.html Export功能")
    print("=" * 70)
    
    for filepath in FIRSTPROJECT_FILES:
        try:
            if fix_export_operators(filepath):
                fixed_export += 1
        except Exception as e:
            print(f"❌ 修复失败: {e}")
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 修复总结")
    print("=" * 70)
    print(f"✅ document-detail.html: {fixed_detail}/{len(DOCUMENT_DETAIL_FILES)} 个文件")
    print(f"✅ firstproject.html: {fixed_export}/{len(FIRSTPROJECT_FILES)} 个文件")
    
    if fixed_detail > 0 or fixed_export > 0:
        print("\n🎉 修复完成！")
        print("\n📝 下一步:")
        print("1. 强制刷新浏览器 (Shift + Command + R)")
        print("2. 测试英文/日文/韩文版本")
        print("3. 测试Export按钮功能")
        print("4. 检查document-detail页面语言显示")
    
    return fixed_detail > 0 or fixed_export > 0

if __name__ == '__main__':
    main()

